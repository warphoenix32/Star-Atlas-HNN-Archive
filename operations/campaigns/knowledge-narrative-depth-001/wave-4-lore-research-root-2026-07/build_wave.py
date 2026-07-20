"""Build deterministic Knowledge Narrative Depth Wave 4 artifacts."""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
PACKETS = HERE / "evidence-packets"
CAMPAIGN_ID = "knowledge-narrative-depth-wave-4-lore-research-root-2026-07"

PAGES = [
    ("knowledge/README.md", "INDEX_REDESIGN", "CANONICAL", "R1", "Human-first knowledge entry point and evidence boundaries."),
    ("knowledge/Entity-Relationship-Map.md", "STRUCTURED_REWORK", "QUALIFIED", "R2", "Cross-domain navigation without creating graph facts."),
    ("knowledge/controversies/README.md", "INDEX_REDESIGN", "CANONICAL", "R1", "Evidence and review method for disputes, corrections, and trust events."),
    ("knowledge/lore/README.md", "INDEX_REDESIGN", "CANONICAL", "R1", "Lore navigation and canonical vocabulary boundary."),
    ("knowledge/lore/Canon-Registry.md", "STRUCTURED_REWORK", "QUALIFIED", "R3", "Operator-confirmed lore authority, taxonomy, continuity, and historical-snapshot rules."),
    ("knowledge/research/README.md", "INDEX_REDESIGN", "CANONICAL", "R1", "Research navigation and evidence-based gap closure."),
    ("knowledge/research/Community-Source-Attribution-Backlog.md", "STRUCTURED_REWORK", "QUALIFIED", "R2", "Publication, author, speaker, mirror, and lineage research."),
    ("knowledge/research/Research-Backlog.md", "STRUCTURED_REWORK", "QUALIFIED", "R2", "Prioritized cross-domain acquisition targets and closure criteria."),
]


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def page_id(path: str) -> str:
    return "KNOW-" + hashlib.sha256(path.encode()).hexdigest()[:16].upper()


def sources_for(path: str) -> list[str]:
    if path.startswith("knowledge/lore/"):
        return [
            "archive/normalized/lore/taxonomy.json",
            "operations/campaigns/lore-repository-ingestion-2026-07/human-review-items.md",
        ]
    if path.startswith("knowledge/research/"):
        return [
            "operations/campaigns/canonical-pip-governance-ledger-2026-07/governance-research-backlog.md",
            "operations/campaigns/discord-community-indexing-001/discord-channel-coverage.json",
        ]
    if "controversies" in path:
        return [
            "operations/campaigns/discord-community-indexing-001/README.md",
            "operations/agents/RISK-AND-REVIEW-AGENT-CONTRACT.md",
        ]
    return [
        "knowledge/index/source-registry/Public-Source-Registry.md",
        "operations/campaigns/knowledge-narrative-depth-001/campaign-summary.md",
    ]


def main() -> None:
    PACKETS.mkdir(parents=True, exist_ok=True)
    inventory, ledger = [], []
    for path_text, action, status, risk, scope in PAGES:
        path = ROOT / path_text
        identifier = page_id(path_text)
        packet_name = path_text.replace("knowledge/", "").replace("/", "-").replace(".md", "") + ".json"
        source_authority = "MIXED_A2_A3_OPERATOR" if risk == "R3" else "MIXED_A2_A3_B2"
        packet = {
            "campaign_id": CAMPAIGN_ID,
            "page_id": identifier,
            "proposed_path": path_text,
            "page_action": action,
            "proposed_knowledge_status": status,
            "page_risk_score": {"R1": 2, "R2": 5, "R3": 8}[risk],
            "page_risk_class": risk,
            "subject_entities": [],
            "aliases": [],
            "scope": scope,
            "material_claims": [{
                "claim_id": identifier + "-C01",
                "claim_text": scope,
                "claim_type": "KNOWLEDGE_BOUNDARY",
                "temporal_scope": "AS_OF_2026-07-20",
                "lifecycle_state": "UNKNOWN",
                "supporting_sources": sources_for(path_text),
                "source_authority": source_authority,
                "corroboration_status": "QUALIFIED" if risk != "R1" else "CORROBORATED",
                "contradiction_status": "PRESERVED_WHERE_IDENTIFIED",
                "attribution_required": True,
                "confidence": "MEDIUM" if risk == "R3" else "HIGH",
                "allowed_in_page": True,
            }],
            "known_limitations": ["The page describes the reviewed repository state as of 2026-07-20 and does not claim total source completeness."],
            "research_gaps": ["See page-specific limitations and missing-artifact requirements."],
            "review_required": True,
            "review_after": "2026-10-20" if risk == "R3" else "2027-01-20",
        }
        dump(PACKETS / packet_name, packet)
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        inventory.append({
            "page_id": identifier,
            "path": path_text,
            "action": action,
            "knowledge_status": status,
            "risk_class": risk,
            "word_count": len(re.findall(r"\b[\w'-]+\b", text)),
            "sha256_utf8_lf": hashlib.sha256(text.encode()).hexdigest(),
        })
        ledger.append({
            "page_id": identifier,
            "path": path_text,
            "disposition": "ACCEPTED",
            "reason": scope,
            "human_review_required": risk == "R3",
        })

    dump(HERE / "page-inventory.json", {"campaign_id": CAMPAIGN_ID, "page_count": len(PAGES), "pages": inventory})
    dump(HERE / "revision-ledger.json", {
        "campaign_id": CAMPAIGN_ID,
        "accepted": len(PAGES), "deferred": 0, "duplicate": 0, "rejected": 0,
        "records": ledger,
    })
    summary = {
        "campaign_id": CAMPAIGN_ID,
        "status": "READY_FOR_REVIEW",
        "pages_revised": len(PAGES),
        "pages_created": 0,
        "risk_distribution": dict(sorted(Counter(item[3] for item in PAGES).items())),
        "knowledge_status_distribution": dict(sorted(Counter(item[2] for item in PAGES).items())),
        "human_adjudication_incorporated": ["LRH-001", "LRH-010", "LRH-014"],
        "archive_evidence_rewritten": False,
        "semantic_evidence_rewritten": False,
        "graph_modified": False,
        "publication_modified": False,
    }
    dump(HERE / "campaign-summary.json", summary)
    (HERE / "campaign-summary.md").write_text(
        "# Knowledge Narrative Depth Wave 4\n\n"
        "**Status:** `READY_FOR_REVIEW`\n\n"
        "Eight root, lore, controversy, and research pages were revised. The lore registry now applies the accepted authority boundary, and the research backlogs identify exact missing artifacts rather than generic topics.\n\n"
        "- Risk: R1 = 4; R2 = 3; R3 = 1\n"
        "- Knowledge status: CANONICAL = 4; QUALIFIED = 4\n"
        "- Human adjudications incorporated: LRH-001, LRH-010, LRH-014\n"
        "- Archive, semantic, graph, and publication changes: none\n",
        encoding="utf-8", newline="\n"
    )


if __name__ == "__main__":
    main()
