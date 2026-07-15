from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SEMANTIC_ROOT = ROOT / "archive" / "semantic" / "star-atlas-transcripts"
SOURCE_ROOT = ROOT / "archive" / "source-records" / "star-atlas-transcripts-ingestion-2026-07"
CAPTION_RE = re.compile(r"^\[(\d{2}:\d{2}:\d{2})\]\s+(.*)$")


def load(name: str) -> dict:
    return json.loads((SEMANTIC_ROOT / name).read_text(encoding="utf-8"))


def seconds(timestamp: str) -> int:
    hour, minute, second = (int(value) for value in timestamp.split(":"))
    return hour * 3600 + minute * 60 + second


def main() -> None:
    errors: list[str] = []
    json_files = sorted(SEMANTIC_ROOT.glob("*.json"))
    documents = {}
    for path in json_files:
        try:
            documents[path.name] = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # validation boundary
            errors.append(f"invalid JSON {path}: {exc}")

    required = {
        "collection-index.json", "source-index.json", "segment-index.json", "topic-index.json",
        "concept-index.json", "entity-links.json", "quote-index.json", "timeline-candidates.json",
        "promotion-candidates.json", "research-gaps.json", "quality-report.json",
    }
    if set(documents) != required:
        errors.append(f"semantic artifact set mismatch: {sorted(set(documents) ^ required)}")
    if errors:
        raise SystemExit("\n".join(errors))

    source_doc = documents["source-index.json"]
    segment_doc = documents["segment-index.json"]
    sources = source_doc["sources"]
    segments = segment_doc["segments"]
    source_ids = [source["source_id"] for source in sources]
    segment_ids = [segment["segment_id"] for segment in segments]
    if len(source_ids) != len(set(source_ids)):
        errors.append("duplicate source IDs")
    if len(segment_ids) != len(set(segment_ids)):
        errors.append("duplicate segment IDs")

    package_source_ids = {
        json.loads(path.read_text(encoding="utf-8"))["source_id"] for path in SOURCE_ROOT.rglob("*.json")
    }
    if set(source_ids) != package_source_ids:
        errors.append("semantic source IDs do not reconcile to package source records")

    source_map = {source["source_id"]: source for source in sources}
    segment_map = {segment["segment_id"]: segment for segment in segments}
    segments_by_source: dict[str, list[dict]] = defaultdict(list)
    caption_total = 0
    for segment in segments:
        source_id = segment["source_id"]
        if source_id not in source_map:
            errors.append(f"orphan segment source: {segment['segment_id']}")
            continue
        segments_by_source[source_id].append(segment)
        reference = segment["transcript_reference"]
        transcript = ROOT / reference["path"]
        if not transcript.exists():
            errors.append(f"missing transcript: {transcript}")
            continue
        lines = transcript.read_text(encoding="utf-8").splitlines()
        start_line = reference["line_start"]
        end_line = reference["line_end"]
        if not (1 <= start_line <= end_line <= len(lines)):
            errors.append(f"invalid line range: {segment['segment_id']}")
            continue
        caption_lines = []
        for line_number in range(start_line, end_line + 1):
            match = CAPTION_RE.match(lines[line_number - 1])
            if match:
                caption_lines.append((line_number, match.group(1), match.group(2)))
        if len(caption_lines) != reference["caption_lines"]:
            errors.append(f"caption line mismatch: {segment['segment_id']}")
        elif caption_lines:
            if caption_lines[0][1] != segment["start_timestamp"]:
                errors.append(f"start timestamp mismatch: {segment['segment_id']}")
            if caption_lines[-1][1] != segment["end_timestamp"]:
                errors.append(f"end timestamp mismatch: {segment['segment_id']}")
        if seconds(segment["start_timestamp"]) > seconds(segment["end_timestamp"]):
            errors.append(f"timestamp regression: {segment['segment_id']}")
        caption_total += reference["caption_lines"]

    for source in sources:
        source_segments = sorted(segments_by_source[source["source_id"]], key=lambda item: item["transcript_reference"]["line_start"])
        if [segment["segment_id"] for segment in source_segments] != source["segment_ids"]:
            errors.append(f"source segment index mismatch: {source['source_id']}")
        if sum(segment["transcript_reference"]["caption_lines"] for segment in source_segments) != source["caption_lines"]:
            errors.append(f"source caption coverage mismatch: {source['source_id']}")
        for previous, current in zip(source_segments, source_segments[1:]):
            if previous["transcript_reference"]["line_end"] >= current["transcript_reference"]["line_start"]:
                errors.append(f"overlapping segments: {previous['segment_id']} / {current['segment_id']}")

    if caption_total != 78752:
        errors.append(f"global caption coverage mismatch: {caption_total}")

    links = documents["entity-links.json"]["links"]
    if {link["segment_id"] for link in links} != set(segment_ids):
        errors.append("entity-link coverage mismatch")
    registry_text = "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in (ROOT / "knowledge").rglob("*.md"))
    linked_entity_ids = {
        entity["entity_id"] for link in links for entity in link["canonical_entities"]
    }
    for entity_id in linked_entity_ids:
        if entity_id not in registry_text:
            errors.append(f"unregistered entity ID: {entity_id}")

    for quote in documents["quote-index.json"]["quotes"]:
        segment = segment_map.get(quote["segment_id"])
        if segment is None or segment["source_id"] != quote["source_id"]:
            errors.append(f"orphan quote: {quote['quote_id']}")
            continue
        transcript_lines = (ROOT / segment["transcript_reference"]["path"]).read_text(encoding="utf-8").splitlines()
        expected = f"[{quote['timestamp']}] {quote['verbatim_quote']}"
        if expected not in transcript_lines:
            errors.append(f"quote not verbatim: {quote['quote_id']}")

    for name in ("timeline-candidates.json", "promotion-candidates.json"):
        for candidate in documents[name]["candidates"]:
            segment = segment_map.get(candidate["segment_id"])
            if segment is None or segment["source_id"] != candidate["source_id"]:
                errors.append(f"orphan candidate in {name}: {candidate['candidate_id']}")

    gap_source_ids = {gap["source_id"] for gap in documents["research-gaps.json"]["gaps"]}
    if gap_source_ids != set(source_ids):
        errors.append("research-gap source coverage mismatch")

    topic_doc = documents["topic-index.json"]
    for topic, record in topic_doc["topics"].items():
        expected = {segment["segment_id"] for segment in segments if topic in segment["topic_tags"]}
        if set(record["segment_ids"]) != expected or record["segment_count"] != len(expected):
            errors.append(f"topic index mismatch: {topic}")

    quality = documents["quality-report.json"]
    for artifact in quality["manifest"]["artifacts"]:
        path = ROOT / artifact["path"]
        if not path.exists():
            errors.append(f"missing quality-manifest artifact: {path}")
            continue
        if path.stat().st_size != artifact["size_bytes"]:
            errors.append(f"quality-manifest size mismatch: {path}")
        if hashlib.sha256(path.read_bytes()).hexdigest() != artifact["sha256"]:
            errors.append(f"quality-manifest hash mismatch: {path}")

    print(f"json_documents={len(documents)}")
    print(f"sources={len(sources)}")
    print(f"segments={len(segments)}")
    print(f"caption_lines={caption_total}")
    print(f"entity_links={len(links)}")
    print(f"quotes={documents['quote-index.json']['quote_count']}")
    print(f"timeline_candidates={documents['timeline-candidates.json']['candidate_count']}")
    print(f"promotion_candidates={documents['promotion-candidates.json']['candidate_count']}")
    if errors:
        raise SystemExit("SEMANTIC_VALIDATION_FAILED\n" + "\n".join(errors))
    print("SEMANTIC_VALIDATION_OK")


if __name__ == "__main__":
    main()
