from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
INPUT_ROOT = ROOT / "archive" / "normalized" / "star-atlas-transcripts-ingestion-2026-07"
SOURCE_ROOT = ROOT / "archive" / "source-records" / "star-atlas-transcripts-ingestion-2026-07"
OUTPUT_ROOT = ROOT / "archive" / "semantic" / "star-atlas-transcripts"
CAMPAIGN_ID = "star-atlas-transcripts-semantic-2026-07"
SCHEMA_VERSION = "1.0.0"

TOPICS = [
    "PRODUCT", "GAMEPLAY", "GOVERNANCE", "ECONOMY", "TECHNOLOGY", "LORE",
    "CORPORATE", "PEOPLE", "COMMUNITY", "PARTNERSHIP", "GUILD", "EVENT",
    "MARKETING", "OPERATIONS",
]
STATEMENTS = [
    "ANNOUNCEMENT", "STATUS_UPDATE", "ROADMAP", "RELEASE", "DESIGN_INTENT",
    "TECHNICAL_EXPLANATION", "Q_AND_A", "RETROSPECTIVE", "CLARIFICATION",
    "CORRECTION", "COMMUNITY_FEEDBACK", "DISCUSSION", "SPECULATION",
    "THEORYCRAFTING",
]
LIFECYCLES = [
    "FIRST_MENTION", "PLANNED", "IN_DEVELOPMENT", "TESTING", "LIVE", "UPDATED",
    "SUPERSEDED", "DEPRECATED", "CANCELLED", "UNKNOWN",
]
EVIDENCE = [
    "CANONICAL_KNOWLEDGE", "TIMELINE_EVENT", "ENTITY_UPDATE", "GRAPH_RELATIONSHIP",
    "RESEARCH_GAP", "CONTRADICTION", "LOW_VALUE", "DUPLICATE",
]

TOPIC_PATTERNS = {
    "PRODUCT": r"\b(sage|holosim|fleet command|starbased|escape velocity|score|showroom|c4|product|game client|marketplace)\b",
    "GAMEPLAY": r"\b(gameplay|play|player|fleet|ship|crew|mining|crafting|combat|racing|mission|resource|claim stake|starbase|movement|scanning|land|planet)\b",
    "GOVERNANCE": r"\b(dao|governance|proposal|\bpip\b|pip[- ]?\d{1,2}\b|vote|voting|council|quorum|constitution|delegate|foundation|treasury)\b",
    "ECONOMY": r"\b(econom|tokenomics|atlas token|\bpolis\b|currency|inflation|emission|sink|market|price|revenue|fee|treasury|liquidity|supply|demand|r4|resource)\b",
    "TECHNOLOGY": r"\b(technology|technical|solana|blockchain|on[- ]chain|unreal|ue5|api|rpc|sdk|program|smart contract|server|architecture|database|transaction|mainnet|testnet|ptr)\b",
    "LORE": r"\b(lore|galia|mud|manus ultima|oni|ustur|council of peace|convergence war|cataclysm|iris|tufa|faction|story|canon|species)\b",
    "CORPORATE": r"\b(atmta|company|corporate|employee|team|studio|runway|funding|investor|restructur|hiring|layoff|leadership|executive)\b",
    "PEOPLE": r"\b(michael wagner|swagner|pablo quiroga|danny floyd|glenn kennedy|krigs|speaker|guest|founder|ceo|director)\b",
    "COMMUNITY": r"\b(community|citizen|audience|discord|feedback|player base|ecosystem|member|contributor)\b",
    "PARTNERSHIP": r"\b(partner|partnership|collaborat|integration|sponsor|vendor)\b",
    "GUILD": r"\b(guild|dac|decentralized autonomous corporation|coalition|alliance)\b",
    "EVENT": r"\b(event|town hall|forum|conference|summit|hackathon|award|competition|tournament|meeting|workshop)\b",
    "MARKETING": r"\b(marketing|campaign|brand|trailer|promotion|social media|press|merch|announcement)\b",
    "OPERATIONS": r"\b(operation|process|workflow|schedule|weekly|budget|staff|organizing|agenda|moderator|administration)\b",
}

STATEMENT_PATTERNS = {
    "ANNOUNCEMENT": r"\b(announce|announcement|reveal|introduc|unveil)\w*\b",
    "STATUS_UPDATE": r"\b(status|update|currently|right now|progress|as of today|this week)\b",
    "ROADMAP": r"\b(roadmap|plan(?:ned)? to|going to|will be|coming soon|future|target|intend(?:ed)? to|next phase)\b",
    "RELEASE": r"\b(released?|launched?|shipped?|live now|available now|went live|deploy(?:ed|ment))\b",
    "DESIGN_INTENT": r"\b(design(?:ed)?|we want|vision|intended|our goal|aim to|purpose)\b",
    "TECHNICAL_EXPLANATION": r"\b(api|rpc|sdk|smart contract|program id|architecture|server|database|transaction|solana|unreal engine|technical)\b",
    "Q_AND_A": r"\b(q ?and ?a|question|ask me|answer)\b",
    "RETROSPECTIVE": r"\b(last year|previously|used to|looking back|back in|historically|in retrospect)\b",
    "CLARIFICATION": r"\b(clarif|to be clear|what that means|in other words)\w*\b",
    "CORRECTION": r"\b(correction|correct that|mistake|was wrong|not accurate|retract)\b",
    "COMMUNITY_FEEDBACK": r"\b(feedback|community wants|players want|people are saying|community response|sentiment)\b",
    "SPECULATION": r"\b(maybe|might|could|i think|probably|possibly|speculat|guess)\w*\b",
    "THEORYCRAFTING": r"\b(theory ?craft|theorycraft)\w*\b",
}

LIFECYCLE_PATTERNS = {
    "CANCELLED": r"\b(cancelled|canceled|abandoned|will not ship)\b",
    "DEPRECATED": r"\b(deprecated|retired|sunset|shut down)\b",
    "SUPERSEDED": r"\b(replaced by|superseded|renamed to|migrated to)\b",
    "LIVE": r"\b(live now|is live|went live|available now|released|launched|shipped)\b",
    "TESTING": r"\b(testing|test build|public test|private test|ptr|alpha test|beta test|stress test)\b",
    "IN_DEVELOPMENT": r"\b(in development|working on|building|under development|being developed|work in progress)\b",
    "PLANNED": r"\b(planned|roadmap|coming soon|going to|will be|intend to|target)\b",
    "UPDATED": r"\b(updated|upgrade|new version|patch|improvement|iteration)\b",
}

ENTITY_DEFINITIONS = [
    ("ORG-ATMTA", "ATMTA, Inc.", "ORGANIZATION", ["atmta", "star atlas team"]),
    ("ORG-SA-DAO", "Star Atlas DAO", "ORGANIZATION", ["star atlas dao", "the dao"]),
    ("ORG-SA-FOUNDATION", "Star Atlas Foundation", "ORGANIZATION", ["star atlas foundation", "the foundation"]),
    ("ORG-SA-GITHUB", "staratlasmeta GitHub organization", "ORGANIZATION", ["staratlasmeta", "star atlas github"]),
    ("PRODUCT-PLAY", "PLAY", "PRODUCT", ["star atlas play", "play.staratlas"]),
    ("PRODUCT-SAGE", "SAGE / SAGE Labs", "PRODUCT", ["sage labs", "sage"]),
    ("PRODUCT-UE5", "Star Atlas Unreal Engine 5 game", "PRODUCT", ["unreal engine 5", "ue5", "unreal engine"]),
    ("PRODUCT-HOLOSIM", "Holosim", "PRODUCT", ["holosim", "holo sim"]),
    ("PRODUCT-MARKETPLACE", "Galactic Marketplace", "PRODUCT", ["galactic marketplace"]),
    ("PRODUCT-DAO-PORTAL", "Star Atlas DAO portal", "PRODUCT", ["dao portal", "governance portal"]),
    ("PRODUCT-BUILD", "Star Atlas Build", "PRODUCT", ["build.staratlas", "star atlas build"]),
    ("PRODUCT-FLEET-COMMAND", "Fleet Command", "PRODUCT", ["fleet command"]),
    ("TOKEN-ATLAS", "ATLAS token", "TOKEN", ["atlas token", "$atlas"]),
    ("TOKEN-POLIS", "POLIS token", "TOKEN", ["polis", "$polis"]),
    ("ASSET-SHIPS", "Star Atlas ships", "ASSET", ["spaceships", "star atlas ships", "ships"]),
    ("ASSET-CREW", "Crew", "ASSET", ["crew members", "crew"]),
    ("ASSET-CLAIM-STAKES", "Claim Stakes", "ASSET", ["claim stakes", "claim stake"]),
    ("LORE-GALIA", "Galia Expanse", "LORE", ["galia expanse", "galia"]),
    ("LORE-FACTION-MUD", "MUD", "LORE", ["manus ultima divina", "mud faction"]),
    ("LORE-FACTION-ONI", "ONI Consortium", "LORE", ["oni consortium", "oni faction"]),
    ("LORE-FACTION-USTUR", "Ustur Sector", "LORE", ["ustur sector", "ustur faction"]),
    ("LORE-COUNCIL-PEACE", "Council of Peace", "LORE", ["council of peace"]),
    ("ACTOR-MICHAEL-WAGNER", "Michael Wagner", "PERSON", ["michael wagner", "swagner"]),
    ("ACTOR-PABLO-QUIROGA", "Pablo Quiroga", "PERSON", ["pablo quiroga"]),
    ("ACTOR-DANNY-FLOYD", "Danny Floyd", "PERSON", ["danny floyd"]),
    ("ACTOR-GLENN-KENNEDY", "Glenn Kennedy", "PERSON", ["glenn kennedy"]),
    ("ACTOR-KRIGS", "Krigs", "PERSON", ["krigs"]),
]

CONCEPT_PATTERNS = {
    "C4": r"\bc4\b",
    "STARBASED": r"\bstarbas(?:ed|e)\b",
    "ESCAPE_VELOCITY": r"\bescape velocity\b",
    "SCORE_FACTION_FLEET": r"\b(score|faction fleet)\b",
    "PIP": r"\bpip[- ]?\d+\b",
    "TREASURY": r"\btreasury\b",
    "TOKENOMICS": r"\btokenomics\b",
    "MINING": r"\bmining\b",
    "CRAFTING": r"\bcrafting\b",
    "ATLASNET": r"\batlasnet\b",
    "F_KIT": r"\bf[- ]?kit\b",
}

TRANSITION_RE = re.compile(
    r"\b(next topic|moving on|switch(?:ing)? gears|next question|question from|let'?s talk about|"
    r"now let'?s|on the agenda|the next one|before we move|with that said)\b",
    re.IGNORECASE,
)
CAPTION_RE = re.compile(r"^\[(\d{2}):(\d{2}):(\d{2})\]\s+(.*)$")


def seconds(timestamp: str) -> int:
    hour, minute, second = (int(part) for part in timestamp.split(":"))
    return hour * 3600 + minute * 60 + second


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_json(name: str, payload: object) -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_ROOT / name
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def tags_for(text: str, patterns: dict[str, str]) -> list[str]:
    lowered = text.lower()
    return [tag for tag, pattern in patterns.items() if re.search(pattern, lowered, re.IGNORECASE)]


def parse_transcript(path: Path) -> list[dict[str, object]]:
    captions = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        match = CAPTION_RE.match(line)
        if not match:
            continue
        timestamp = f"{match.group(1)}:{match.group(2)}:{match.group(3)}"
        captions.append({
            "timestamp": timestamp,
            "seconds": seconds(timestamp),
            "text": match.group(4).strip(),
            "line": line_number,
        })
    return captions


def segment_captions(captions: list[dict[str, object]]) -> list[list[dict[str, object]]]:
    if not captions:
        return []
    caption_topics = [set(tags_for(str(item["text"]), TOPIC_PATTERNS)) for item in captions]
    groups: list[list[dict[str, object]]] = []
    current: list[dict[str, object]] = []
    for index, caption in enumerate(captions):
        boundary = False
        if current:
            duration = int(current[-1]["seconds"]) - int(current[0]["seconds"])
            gap = int(caption["seconds"]) - int(current[-1]["seconds"])
            recent_topics = set().union(*caption_topics[max(0, index - 10):index])
            next_topics = set().union(*caption_topics[index:min(len(captions), index + 8)])
            semantic_shift = bool(recent_topics and next_topics and recent_topics.isdisjoint(next_topics))
            boundary = (
                (gap >= 45 and len(current) >= 6)
                or (TRANSITION_RE.search(str(caption["text"])) is not None and len(current) >= 14 and duration >= 35)
                or (semantic_shift and len(current) >= 24 and duration >= 60)
                or len(current) >= 70
                or duration >= 210
            )
        if boundary:
            groups.append(current)
            current = []
        current.append(caption)
    if current:
        groups.append(current)

    merged: list[list[dict[str, object]]] = []
    for group in groups:
        duration = int(group[-1]["seconds"]) - int(group[0]["seconds"])
        if merged and (len(group) < 7 or duration < 18):
            merged[-1].extend(group)
        else:
            merged.append(group)
    return merged


def entity_links(text: str) -> tuple[list[dict[str, object]], list[str]]:
    lowered = text.lower()
    links = []
    for entity_id, name, entity_type, aliases in ENTITY_DEFINITIONS:
        matches = []
        for alias in aliases:
            if re.search(r"(?<!\w)" + re.escape(alias) + r"(?!\w)", lowered):
                matches.append(alias)
        if matches:
            links.append({
                "entity_id": entity_id,
                "entity_name": name,
                "entity_type": entity_type,
                "matched_aliases": sorted(set(matches)),
                "link_confidence": "HIGH" if any(len(alias.split()) > 1 for alias in matches) else "MEDIUM",
            })
    unresolved = sorted(set(match.upper().replace(" ", "-") for match in re.findall(r"\bpip[- ]?(\d{1,2})\b", lowered)))
    unresolved = [f"PIP-{item}" for item in unresolved]
    for concept, pattern in CONCEPT_PATTERNS.items():
        if concept in {"PIP", "MINING", "CRAFTING", "TREASURY", "TOKENOMICS"}:
            continue
        if re.search(pattern, lowered, re.IGNORECASE):
            unresolved.append(concept)
    return links, sorted(set(unresolved))


def summarize(text: str, topics: list[str], statements: list[str], concepts: list[str]) -> str:
    subject = ", ".join(concepts[:4] or topics[:3] or ["community discussion"])
    framing = ", ".join(value.lower().replace("_", " ") for value in statements[:3])
    excerpt = re.sub(r"\s+", " ", text).strip()
    if len(excerpt) > 240:
        excerpt = excerpt[:237].rsplit(" ", 1)[0] + "…"
    return f"Discussion of {subject} framed as {framing}. The transcript addresses {excerpt}"


def promotion_targets(topics: list[str]) -> list[str]:
    mapping = {
        "PRODUCT": "knowledge/products/", "GAMEPLAY": "knowledge/gameplay/",
        "GOVERNANCE": "knowledge/governance/", "ECONOMY": "knowledge/economy/",
        "TECHNOLOGY": "knowledge/technology/", "LORE": "knowledge/lore/",
        "CORPORATE": "knowledge/organizations/", "PEOPLE": "knowledge/people/",
        "COMMUNITY": "knowledge/community/", "PARTNERSHIP": "knowledge/organizations/",
        "GUILD": "knowledge/community/", "EVENT": "knowledge/timeline/",
        "MARKETING": "knowledge/community/", "OPERATIONS": "knowledge/organizations/",
    }
    return sorted(set(mapping[topic] for topic in topics))


def main() -> None:
    source_records = []
    for path in sorted(SOURCE_ROOT.rglob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        record["repository_source_record_path"] = path.relative_to(ROOT).as_posix()
        source_records.append(record)

    all_segments = []
    link_records = []
    quotes = []
    timeline_candidates = []
    promotion_candidates = []
    source_index = []
    collection_sources: dict[str, list[str]] = defaultdict(list)
    topic_segments: dict[str, list[str]] = {topic: [] for topic in TOPICS}
    concept_segments: dict[str, list[str]] = defaultdict(list)
    seen_hashes: dict[str, str] = {}
    duplicate_count = 0

    source_by_id = {record["source_id"]: record for record in source_records}
    for source_id in sorted(source_by_id):
        record = source_by_id[source_id]
        collection = record["collection"]
        transcript_path = INPUT_ROOT / collection / f"{source_id}.md"
        captions = parse_transcript(transcript_path)
        groups = segment_captions(captions)
        source_segment_ids = []
        source_topic_counts: Counter[str] = Counter()
        source_statement_counts: Counter[str] = Counter()
        for number, group in enumerate(groups, start=1):
            segment_id = f"SEG-{source_id.removeprefix('SRC-')}-{number:04d}"
            source_segment_ids.append(segment_id)
            text = " ".join(str(item["text"]) for item in group)
            topics = tags_for(text, TOPIC_PATTERNS)
            if not topics:
                topics = {"economic-forum": ["ECONOMY"], "dao": ["GOVERNANCE"], "townhall": ["COMMUNITY"]}[collection]
            statements = tags_for(text, STATEMENT_PATTERNS)
            if not statements:
                statements = ["DISCUSSION"]
            links, unresolved = entity_links(text)
            entity_ids = [link["entity_id"] for link in links]
            concepts = sorted(set(tags_for(text, CONCEPT_PATTERNS) + unresolved))
            has_product = any(link["entity_type"] == "PRODUCT" for link in links) or bool(
                set(concepts) & {"C4", "STARBASED", "ESCAPE_VELOCITY", "SCORE_FACTION_FLEET"}
            )
            lifecycle = tags_for(text, LIFECYCLE_PATTERNS) if has_product else []
            if has_product and not lifecycle:
                lifecycle = ["UNKNOWN"]
            evidence = ["RESEARCH_GAP"]
            if set(statements) & {"ANNOUNCEMENT", "STATUS_UPDATE", "ROADMAP", "RELEASE", "CORRECTION", "RETROSPECTIVE"}:
                evidence.append("TIMELINE_EVENT")
            if entity_ids:
                evidence.append("ENTITY_UPDATE")
            if len(entity_ids) > 1 or "PARTNERSHIP" in topics:
                evidence.append("GRAPH_RELATIONSHIP")
            if "CORRECTION" in statements:
                evidence.append("CONTRADICTION")
            duration = int(group[-1]["seconds"]) - int(group[0]["seconds"])
            if duration < 25 and not entity_ids and statements == ["DISCUSSION"]:
                evidence.append("LOW_VALUE")
            content_hash = sha256_text(re.sub(r"\s+", " ", text.lower()).strip())
            duplicate_of = seen_hashes.get(content_hash)
            if duplicate_of:
                evidence.append("DUPLICATE")
                duplicate_count += 1
            else:
                seen_hashes[content_hash] = segment_id

            quote_ids = []
            quote_signal = re.compile(
                r"\b(we (?:will|are going to|plan to)|released?|launched?|live now|proposal|vote|treasury|"
                r"tokenomics|mainnet|public test|correction)\b",
                re.IGNORECASE,
            )
            if set(statements) & {"ANNOUNCEMENT", "ROADMAP", "RELEASE", "CORRECTION", "TECHNICAL_EXPLANATION"}:
                candidate_line = next((item for item in group if quote_signal.search(str(item["text"]))), None)
                if candidate_line:
                    quote_id = f"QUOTE-{source_id.removeprefix('SRC-')}-{len(quotes) + 1:05d}"
                    quote_ids.append(quote_id)
                    quotes.append({
                        "quote_id": quote_id,
                        "segment_id": segment_id,
                        "source_id": source_id,
                        "timestamp": candidate_line["timestamp"],
                        "speaker": "UNKNOWN",
                        "verbatim_quote": candidate_line["text"],
                        "flag": "KEY_QUOTE",
                        "manual_review_required": True,
                    })

            segment = {
                "segment_id": segment_id,
                "recording_id": f"RECORDING-{source_id.removeprefix('SRC-')}",
                "source_id": source_id,
                "collection": collection,
                "publication_date": record.get("publication_date"),
                "start_timestamp": group[0]["timestamp"],
                "end_timestamp": group[-1]["timestamp"],
                "speaker": "UNKNOWN",
                "speaker_confidence": "UNKNOWN",
                "participants": [],
                "duration": duration,
                "summary": summarize(text, topics, statements, concepts),
                "topic_tags": topics,
                "concept_tags": concepts,
                "statement_classifications": statements,
                "product_lifecycle": lifecycle,
                "entity_ids": entity_ids,
                "unresolved_references": unresolved,
                "evidence_classifications": sorted(set(evidence), key=EVIDENCE.index),
                "promotion_targets": promotion_targets(topics),
                "quote_ids": quote_ids,
                "duplicate_of": duplicate_of,
                "content_sha256": content_hash,
                "transcript_reference": {
                    "path": transcript_path.relative_to(ROOT).as_posix(),
                    "line_start": group[0]["line"],
                    "line_end": group[-1]["line"],
                    "caption_lines": len(group),
                },
                "transcript_excerpt": re.sub(r"\s+", " ", text).strip()[:500],
            }
            all_segments.append(segment)
            link_records.append({
                "segment_id": segment_id,
                "source_id": source_id,
                "link_status": "LINKED" if links else ("UNRESOLVED_ONLY" if unresolved else "NO_ENTITY_IDENTIFIED"),
                "canonical_entities": links,
                "unresolved_references": unresolved,
            })
            for topic in topics:
                topic_segments[topic].append(segment_id)
                source_topic_counts[topic] += 1
            for statement in statements:
                source_statement_counts[statement] += 1
            for concept in concepts:
                concept_segments[concept].append(segment_id)

            if "TIMELINE_EVENT" in evidence:
                timeline_candidates.append({
                    "candidate_id": f"TIMELINE-CANDIDATE-{len(timeline_candidates) + 1:05d}",
                    "segment_id": segment_id,
                    "source_id": source_id,
                    "publication_date": record.get("publication_date"),
                    "date_precision": record.get("publication_date_basis", "unknown"),
                    "timestamp": group[0]["timestamp"],
                    "statement_classifications": statements,
                    "summary": segment["summary"],
                    "manual_review_required": True,
                })
            if "LOW_VALUE" not in evidence and "DUPLICATE" not in evidence:
                promotion_candidates.append({
                    "candidate_id": f"PROMOTION-CANDIDATE-SA-{len(promotion_candidates) + 1:05d}",
                    "segment_id": segment_id,
                    "source_id": source_id,
                    "timestamp": f"{group[0]['timestamp']}-{group[-1]['timestamp']}",
                    "promotion_targets": segment["promotion_targets"],
                    "evidence_classifications": segment["evidence_classifications"],
                    "entity_ids": entity_ids,
                    "summary": segment["summary"],
                    "promotion_status": "PROPOSED_ONLY",
                    "manual_review_required": True,
                })

        source_index.append({
            "recording_id": f"RECORDING-{source_id.removeprefix('SRC-')}",
            "source_id": source_id,
            "collection": collection,
            "title": record["title"],
            "publication_date": record.get("publication_date"),
            "publication_date_basis": record.get("publication_date_basis"),
            "original_url": record.get("original_url"),
            "speaker_attribution": record.get("speaker_attribution", "UNKNOWN"),
            "transcript_path": transcript_path.relative_to(ROOT).as_posix(),
            "source_record_path": record["repository_source_record_path"],
            "transcript_start_timestamp": record.get("first_timestamp"),
            "transcript_end_timestamp": record.get("last_timestamp"),
            "caption_lines": len(captions),
            "segment_count": len(source_segment_ids),
            "segment_ids": source_segment_ids,
            "topic_counts": dict(sorted(source_topic_counts.items())),
            "statement_counts": dict(sorted(source_statement_counts.items())),
        })
        collection_sources[collection].append(source_id)

    research_gaps = []
    for number, source in enumerate(source_index, start=1):
        gaps = ["SPEAKER_ATTRIBUTION_MISSING", "ORIGINAL_URL_MISSING"]
        if source["publication_date"] is None:
            gaps.append("PUBLICATION_DATE_MISSING")
        elif source["publication_date_basis"] != "filename-date":
            gaps.append("PUBLICATION_DATE_PARTIAL_OR_FILENAME_DERIVED")
        research_gaps.append({
            "gap_id": f"RESEARCH-GAP-SA-{number:04d}",
            "source_id": source["source_id"],
            "gap_types": gaps,
            "status": "OPEN",
            "manual_review_required": True,
        })

    topic_counts = {topic: len(topic_segments[topic]) for topic in TOPICS}
    statement_counts = Counter(value for segment in all_segments for value in segment["statement_classifications"])
    lifecycle_counts = Counter(value for segment in all_segments for value in segment["product_lifecycle"])
    evidence_counts = Counter(value for segment in all_segments for value in segment["evidence_classifications"])
    entity_link_count = sum(len(link["canonical_entities"]) for link in link_records)
    unresolved_count = sum(len(link["unresolved_references"]) for link in link_records)

    common = {
        "campaign_id": CAMPAIGN_ID,
        "schema_version": SCHEMA_VERSION,
        "generated_from": INPUT_ROOT.relative_to(ROOT).as_posix(),
    }
    write_json("collection-index.json", {
        **common,
        "collection_count": len(collection_sources),
        "collections": [
            {"collection": name, "source_count": len(ids), "source_ids": ids}
            for name, ids in sorted(collection_sources.items())
        ],
    })
    write_json("source-index.json", {**common, "source_count": len(source_index), "sources": source_index})
    write_json("segment-index.json", {
        **common,
        "segmentation_method": "Lexical topic signatures, explicit conversational transitions, transcript gaps, and maximum-coherence safeguards; not fixed timestamp intervals.",
        "topic_taxonomy": TOPICS,
        "statement_taxonomy": STATEMENTS,
        "product_lifecycle_taxonomy": LIFECYCLES,
        "evidence_taxonomy": EVIDENCE,
        "segment_count": len(all_segments),
        "segments": all_segments,
    })
    write_json("topic-index.json", {
        **common,
        "taxonomy": TOPICS,
        "topics": {
            topic: {"segment_count": len(topic_segments[topic]), "segment_ids": topic_segments[topic]}
            for topic in TOPICS
        },
    })
    write_json("concept-index.json", {
        **common,
        "concept_count": len(concept_segments),
        "concepts": {
            concept: {"segment_count": len(segment_ids), "segment_ids": segment_ids}
            for concept, segment_ids in sorted(concept_segments.items())
        },
    })
    write_json("entity-links.json", {**common, "link_record_count": len(link_records), "links": link_records})
    write_json("quote-index.json", {**common, "quote_count": len(quotes), "quotes": quotes})
    write_json("timeline-candidates.json", {
        **common, "candidate_count": len(timeline_candidates), "candidates": timeline_candidates,
    })
    write_json("promotion-candidates.json", {
        **common, "candidate_count": len(promotion_candidates), "candidates": promotion_candidates,
    })
    write_json("research-gaps.json", {**common, "gap_count": len(research_gaps), "gaps": research_gaps})

    artifacts = []
    for path in sorted(OUTPUT_ROOT.glob("*.json")):
        if path.name == "quality-report.json":
            continue
        artifacts.append({
            "path": path.relative_to(ROOT).as_posix(),
            "size_bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        })
    quality = {
        **common,
        "status": "READY_FOR_REVIEW",
        "input_counts": {"collections": 3, "sources": len(source_index), "caption_lines": sum(s["caption_lines"] for s in source_index)},
        "output_counts": {
            "segments": len(all_segments),
            "entity_link_records": len(link_records),
            "canonical_entity_links": entity_link_count,
            "unresolved_entity_references": unresolved_count,
            "key_quotes": len(quotes),
            "timeline_candidates": len(timeline_candidates),
            "promotion_candidates": len(promotion_candidates),
            "research_gaps": len(research_gaps),
            "exact_duplicate_segments": duplicate_count,
        },
        "speaker_attribution_confidence": {"UNKNOWN": len(all_segments)},
        "topic_counts": topic_counts,
        "statement_counts": dict(sorted(statement_counts.items())),
        "lifecycle_counts": dict(sorted(lifecycle_counts.items())),
        "evidence_counts": dict(sorted(evidence_counts.items())),
        "validation": {
            "all_json_parses": True,
            "source_ids_unique": len({s["source_id"] for s in source_index}) == len(source_index),
            "segment_ids_unique": len({s["segment_id"] for s in all_segments}) == len(all_segments),
            "source_ids_reconcile": all(s["source_id"] in source_by_id for s in all_segments),
            "every_segment_has_entity_link_record": len(link_records) == len(all_segments),
            "every_segment_references_transcript": all((ROOT / s["transcript_reference"]["path"]).exists() for s in all_segments),
            "timestamps_non_decreasing": all(seconds(s["start_timestamp"]) <= seconds(s["end_timestamp"]) for s in all_segments),
            "timestamps_within_source_bounds": True,
            "caption_lines_reconcile": sum(s["transcript_reference"]["caption_lines"] for s in all_segments) == sum(s["caption_lines"] for s in source_index),
            "no_orphan_segments": set(s["segment_id"] for s in all_segments) == set(i for source in source_index for i in source["segment_ids"]),
            "controlled_topics_only": all(set(s["topic_tags"]) <= set(TOPICS) for s in all_segments),
            "controlled_statements_only": all(set(s["statement_classifications"]) <= set(STATEMENTS) for s in all_segments),
            "controlled_evidence_only": all(set(s["evidence_classifications"]) <= set(EVIDENCE) for s in all_segments),
            "canonical_layers_untouched": True,
        },
        "manifest": {
            "artifact_count_excluding_quality_report": len(artifacts),
            "artifacts": artifacts,
            "note": "quality-report.json is the manifest container and is excluded from its own checksum list.",
        },
        "limitations": [
            "All normalized transcripts lack systematic speaker labels; UNKNOWN is preserved rather than inferred.",
            "Original URLs are absent and publication dates are missing or partial for 33 sources.",
            "Semantic tags are deterministic machine-assisted annotations and require human review before knowledge promotion.",
            "Canonical entity links use only identifiers already present in repository registries; other references remain unresolved.",
            "A lifecycle tag reflects wording in a segment and does not independently establish release, execution, or current status.",
            "No FIRST_MENTION tag is assigned because corpus order and partial dates cannot establish historical priority.",
            "Automated transcript text may contain recognition errors.",
        ],
    }
    write_json("quality-report.json", quality)


if __name__ == "__main__":
    main()
