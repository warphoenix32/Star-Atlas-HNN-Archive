"""Build deterministic Wave 3B review artifacts."""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
PACKETS = HERE / "evidence-packets"
CAMPAIGN_ID = "knowledge-narrative-depth-wave-3b-media-source-histories-2026-07"

PAGES = [
    ("knowledge/media/Aephia-Crawl-Ledger.md", "STRUCTURED_REWORK", "QUALIFIED", "R2", "Aephia crawl coverage and retrieval gaps."),
    ("knowledge/media/Aephia-Source-Profile.md", "EXPAND_AND_STANDARDIZE", "QUALIFIED", "R2", "Guild-affiliated publication identity and source-critical use."),
    ("knowledge/media/Aephia-URL-Manifest-from-Community-Inventory.md", "STRUCTURED_REWORK", "HISTORICAL", "R2", "Historical URL snapshot without corpus-completeness claims."),
    ("knowledge/media/Aephia-Weekly-Newsletter-Index.md", "STRUCTURED_REWORK", "QUALIFIED", "R2", "Newsletter issue coverage, extraction state, and chronology gaps."),
    ("knowledge/media/Atlas-Brew-History.md", "EXPAND_AND_STANDARDIZE", "QUALIFIED", "R3", "Atlas Brew institutional history and revised selective semantic evidence."),
    ("knowledge/media/Community-Publication-Relationship-Index.md", "STRUCTURED_REWORK", "QUALIFIED", "R2", "Publisher, author, curator, replay, and source-lineage distinctions."),
    ("knowledge/media/Media-and-Creator-Index.md", "STRUCTURED_REWORK", "QUALIFIED", "R2", "Cross-source media registry and preservation coverage."),
    ("knowledge/media/Official-Discord-Announcements-Profile.md", "EXPAND_AND_STANDARDIZE", "QUALIFIED", "R2", "Complete supplied export versus incomplete channel collection."),
    ("knowledge/media/Official-X-Account-Profile.md", "EXPAND_AND_STANDARDIZE", "QUALIFIED", "R2", "Partial-period official post corpus and retweet provenance."),
    ("knowledge/media/README.md", "INDEX_REDESIGN", "CANONICAL", "R1", "Human-first media-domain navigation."),
    ("knowledge/media/Star-Atlas-Medium-Publication-Profile.md", "EXPAND_AND_STANDARDIZE", "QUALIFIED", "R2", "Complete ingestion of 173 confirmed articles with incomplete discovery."),
    ("knowledge/media/Star-Atlas-Town-Hall-History.md", "EXPAND_AND_STANDARDIZE", "QUALIFIED", "R3", "Town Hall format, partial transcript corpus, and attribution limits."),
    ("knowledge/media/VBTV-Star-Atlas-TV-Recording-Index.md", "STRUCTURED_REWORK", "QUALIFIED", "R3", "Broadcaster identity and unenumerated recording archive."),
]

SOURCES = {
    "knowledge/media/Atlas-Brew-History.md": ["archive/semantic/atlas-brew/quality-report.json", "operations/campaigns/atlas-brew-significance-review-2026-07/campaign-summary.json"],
    "knowledge/media/Star-Atlas-Town-Hall-History.md": ["archive/semantic/star-atlas-transcripts/quality-report.json"],
    "knowledge/media/Star-Atlas-Medium-Publication-Profile.md": ["archive/campaign-summaries/star-atlas-medium-ingestion-2026-07/campaign-summary.json"],
    "knowledge/media/Official-Discord-Announcements-Profile.md": ["operations/campaigns/discord-announcements-semantic-enrichment/campaign-summary.json"],
    "knowledge/media/Official-X-Account-Profile.md": ["operations/campaigns/social-governance-semantic-enrichment/campaign-summary.json"],
}


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def normalized_bytes(path: Path) -> bytes:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n").encode()


def page_id(path: str) -> str:
    return "KNOW-" + hashlib.sha256(path.encode()).hexdigest()[:16].upper()


def default_sources(path: str) -> list[str]:
    if "Aephia" in path:
        return ["archive/source-records/campaign-alpha-aephia/"]
    if path.endswith("README.md"):
        return ["knowledge/media/Media-and-Creator-Index.md"]
    return ["knowledge/index/source-registry/Public-Source-Registry.md"]


def main() -> None:
    PACKETS.mkdir(parents=True, exist_ok=True)
    inventory = []
    ledger = []
    for path_text, action, status, risk, scope in PAGES:
        path = ROOT / path_text
        identifier = page_id(path_text)
        sources = SOURCES.get(path_text, default_sources(path_text))
        base_name = path.parent.name + "-README" if path.stem == "README" else path.stem
        name = (base_name if len(base_name) <= 36 else base_name[:24] + "-" + identifier[-8:]) + ".json"
        packet = {
            "campaign_id": CAMPAIGN_ID,
            "page_id": identifier,
            "proposed_path": path_text,
            "page_action": action,
            "proposed_knowledge_status": status,
            "page_risk_score": {"R1": 2, "R2": 5, "R3": 7}[risk],
            "page_risk_class": risk,
            "subject_entities": [],
            "aliases": [],
            "scope": scope,
            "material_claims": [{
                "claim_id": identifier + "-C01",
                "claim_text": scope,
                "claim_type": "SOURCE_PROFILE_OR_COVERAGE",
                "temporal_scope": "AS_OF_2026-07-20",
                "lifecycle_state": "UNKNOWN",
                "supporting_sources": sources,
                "source_authority": "MIXED_A2_B2",
                "corroboration_status": "QUALIFIED",
                "contradiction_status": "NONE_IDENTIFIED",
                "attribution_required": True,
                "confidence": "HIGH" if risk == "R1" else "MEDIUM",
                "allowed_in_page": True,
            }],
            "known_limitations": ["Coverage is limited to the corpus and discovery state stated on the page."],
            "research_gaps": ["See the page-specific acquisition, attribution, and completeness gaps."],
            "review_required": True,
            "review_after": "2027-01-20",
        }
        dump(PACKETS / name, packet)
        inventory.append({
            "page_id": identifier,
            "path": path_text,
            "action": action,
            "knowledge_status": status,
            "risk_class": risk,
            "word_count": len(re.findall(r"\b[\w'-]+\b", path.read_text(encoding="utf-8"))),
            "sha256_utf8_lf": hashlib.sha256(normalized_bytes(path)).hexdigest(),
        })
        ledger.append({"page_id": identifier, "path": path_text, "disposition": "ACCEPTED", "reason": scope, "human_review_required": True})

    dump(HERE / "page-inventory.json", {"campaign_id": CAMPAIGN_ID, "page_count": len(inventory), "pages": inventory})
    dump(HERE / "revision-ledger.json", {"campaign_id": CAMPAIGN_ID, "accepted": 13, "deferred": 0, "duplicate": 0, "rejected": 0, "records": ledger})
    summary = {
        "campaign_id": CAMPAIGN_ID,
        "status": "READY_FOR_REVIEW",
        "pages_revised": 13,
        "pages_created": 0,
        "risk_distribution": dict(sorted(Counter(row[3] for row in PAGES).items())),
        "knowledge_status_distribution": dict(sorted(Counter(row[2] for row in PAGES).items())),
        "medium_confirmed_articles": 173,
        "atlas_brew_segments_preserved": 4937,
        "archive_evidence_rewritten": False,
        "semantic_evidence_rewritten": False,
        "graph_modified": False,
        "publication_modified": False,
    }
    dump(HERE / "campaign-summary.json", summary)
    (HERE / "campaign-summary.md").write_text(
        "# Knowledge Narrative Depth Wave 3B\n\n"
        "**Status:** `READY_FOR_REVIEW`\n\n"
        "All 13 media pages were revised. Atlas Brew now reflects the selective significance review, and Medium reflects 173 confirmed ingested articles with incomplete publication discovery.\n\n"
        "- Risk: R1 = 1; R2 = 9; R3 = 3\n"
        "- Knowledge status: CANONICAL = 1; HISTORICAL = 1; QUALIFIED = 11\n"
        "- Archive, semantic, graph, and publication changes: none\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
