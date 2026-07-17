"""Build deterministic evidence packets and campaign ledgers."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
PACKETS = HERE / "evidence-packets"

SPECS = [
    ("official-discord", "knowledge/media/Official-Discord-Announcements-Profile.md", "CREATE", "QUALIFIED", 5, "R2", ["archive/raw/discord-announcements/star-atlas-discord-announcements.md", "operations/campaigns/discord-announcements-semantic-enrichment/campaign-summary.json", "operations/campaigns/discord-announcements-semantic-enrichment/validation-report.json", "operations/campaigns/discord-announcements-semantic-enrichment/review-correction-status.json"], "The validated corpus contains 1,071 dated announcement records; author inference and absent attachments limit use."),
    ("official-x", "knowledge/media/Official-X-Account-Profile.md", "CREATE", "QUALIFIED", 4, "R2", ["operations/campaigns/social-governance-semantic-enrichment/validation-report.json", "archive/normalized/social-governance-semantic-enrichment/social-media/staratlas-posts.jsonl"], "The captured official account corpus contains 796 unique posts; originals and retweets have different authority."),
    ("official-medium", "knowledge/media/Star-Atlas-Medium-Publication-Profile.md", "CREATE", "QUALIFIED", 6, "R2", ["archive/semantic/discord-announcements/announcement-semantic-records.jsonl"], "The official Medium publication is a discoverable source family, but complete article-by-article review is absent."),
    ("pvp", "knowledge/economy/PVP-Voting-Power.md", "CREATE", "QUALIFIED", 4, "R2", ["archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json", "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-0D4A8B8F235B43B8.json"], "PVP is time-weighted POLIS voting power; the 2022 reward target remains historical announced intent."),
    ("dao-treasury", "knowledge/economy/DAO-Treasury-Architecture.md", "CREATE", "QUALIFIED", 6, "R2", ["archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json", "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-23-0ECF2928.json", "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-33-397FEE39.json", "operations/campaigns/social-governance-semantic-enrichment/input-council-tracker/council-pip-tracker-semantic-records.jsonl"], "The DAO Treasury is broader than the bounded Ecosystem Fund; authorization does not prove transfer."),
    ("holosim", "knowledge/gameplay/Holosim.md", "CREATE", "QUALIFIED", 4, "R2", ["archive/source-records/campaign-delta-official/SRC-OFF-4850F98FBD1F1541.md", "archive/normalized/social-governance-semantic-enrichment/social-media/staratlas-posts.jsonl", "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-D8337FA27E0A550A.json"], "Official records establish test, Chapter 1, delay, and Chapter 2 release states without implying mainnet delivery."),
    ("pip-33", "knowledge/governance/PIP-33-ATMTA-Historic-Expense-Reimbursement.md", "CREATE", "PROVISIONAL", 7, "R3", ["archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-33-397FEE39.json", "archive/source-records/governance/council-pip-tracker/SA-COUNCIL-TRACKER-D1DADF7EB8437119.json", "operations/campaigns/social-governance-semantic-enrichment/input-council-tracker/council-pip-tracker-semantic-records.jsonl"], "PIP-33 passed as a direct DAO Treasury measure; payment remains unverified."),
    ("sage", "knowledge/gameplay/SAGE.md", "EXPAND", "QUALIFIED", 5, "R2", ["archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-6DF1790F1F2402FA.json", "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-A37A8B7B245E7776.json", "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-9FFFF91025488D09.json", "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-76D9861DCB3FE798.json", "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-CCF4600A4C08F697.json"], "Official records establish exact SAGE Labs and Starbased live dates while retaining planned dates and delays."),
    ("product-registry", "knowledge/gameplay/Product-Registry.md", "EXPAND", "QUALIFIED", 5, "R2", ["archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-A37A8B7B245E7776.json", "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-CCF4600A4C08F697.json", "archive/normalized/social-governance-semantic-enrichment/social-media/staratlas-posts.jsonl"], "The registry records dated SAGE Labs, Starbased, and Holosim states without collapsing test, release, or mainnet."),
    ("product-timeline", "knowledge/timeline/Product-Timeline.md", "EXPAND", "QUALIFIED", 6, "R2", ["archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-A37A8B7B245E7776.json", "archive/normalized/social-governance-semantic-enrichment/social-media/staratlas-posts.jsonl"], "The product chronology is corrected with dated first-party SAGE, Starbased, and Holosim lifecycle records."),
    ("master-timeline", "knowledge/timeline/Master-Timeline.md", "EXPAND", "QUALIFIED", 6, "R2", ["archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-A37A8B7B245E7776.json", "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-33-397FEE39.json"], "The master chronology gains corrected product states and a qualified PIP-33 passage record."),
    ("pip-registry", "knowledge/governance/PIP-Registry.md", "EXPAND", "QUALIFIED", 6, "R2", ["archive/semantic/governance/pip-registry-semantic.json", "archive/source-records/governance/council-pip-tracker/SA-COUNCIL-TRACKER-D1DADF7EB8437119.json"], "Failed PIPs do not acquire implementation milestones, and PIP-33 is not an Ecosystem Fund proposal."),
    ("ecosystem-fund", "knowledge/governance/Ecosystem-Fund.md", "EXPAND", "QUALIFIED", 6, "R2", ["archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-23-0ECF2928.json", "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-33-397FEE39.json", "operations/campaigns/social-governance-semantic-enrichment/input-council-tracker/council-pip-tracker-semantic-records.jsonl"], "PIP-23 reports two fund refills with transaction references; this campaign did not independently reconcile them."),
    ("governance-economy", "knowledge/governance/Governance-and-Economy-Overview.md", "EXPAND", "QUALIFIED", 5, "R2", ["archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json", "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-23-0ECF2928.json"], "PVP, the general DAO Treasury, and the bounded Ecosystem Fund are distinct institutional concepts."),
]

LINK_MAINTENANCE = [
    "knowledge/Entity-Relationship-Map.md", "knowledge/economy/README.md",
    "knowledge/gameplay/README.md",
    "knowledge/governance/README.md", "knowledge/index/source-registry/Public-Source-Registry.md",
    "knowledge/media/Media-and-Creator-Index.md", "knowledge/media/README.md",
]

SOURCE_AUTHORITIES = {
    "archive/raw/discord-announcements/star-atlas-discord-announcements.md": ["A2"],
    "operations/campaigns/discord-announcements-semantic-enrichment/campaign-summary.json": [],
    "operations/campaigns/discord-announcements-semantic-enrichment/validation-report.json": [],
    "operations/campaigns/discord-announcements-semantic-enrichment/review-correction-status.json": [],
    "operations/campaigns/social-governance-semantic-enrichment/validation-report.json": [],
    "archive/normalized/social-governance-semantic-enrichment/social-media/staratlas-posts.jsonl": ["A2"],
    "archive/semantic/discord-announcements/announcement-semantic-records.jsonl": ["A2", "C1"],
    "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json": ["A1"],
    "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-23-0ECF2928.json": ["A1"],
    "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-33-397FEE39.json": ["A1"],
    "archive/source-records/governance/council-pip-tracker/SA-COUNCIL-TRACKER-D1DADF7EB8437119.json": ["A3"],
    "operations/campaigns/social-governance-semantic-enrichment/input-council-tracker/council-pip-tracker-semantic-records.jsonl": ["A3"],
    "archive/semantic/governance/pip-registry-semantic.json": ["A1", "A3"],
    "archive/source-records/campaign-delta-official/SRC-OFF-4850F98FBD1F1541.md": ["A2"],
}
SOURCE_ROLES = {
    "operations/campaigns/discord-announcements-semantic-enrichment/campaign-summary.json": "DERIVED_OPERATIONAL_SUMMARY",
    "operations/campaigns/discord-announcements-semantic-enrichment/validation-report.json": "DERIVED_OPERATIONAL_VALIDATION",
    "operations/campaigns/discord-announcements-semantic-enrichment/review-correction-status.json": "DERIVED_CURATOR_CORRECTION_STATUS",
    "operations/campaigns/social-governance-semantic-enrichment/validation-report.json": "DERIVED_OPERATIONAL_VALIDATION",
}
for source in {s for spec in SPECS for s in spec[6]}:
    if source.startswith("archive/normalized/discord-announcements/messages/"):
        SOURCE_AUTHORITIES[source] = ["A2"]

def write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def main() -> None:
    PACKETS.mkdir(parents=True, exist_ok=True)
    for page_id, path, action, status, score, risk, sources, claim in SPECS:
        details = [{"source": source, "authority": SOURCE_AUTHORITIES[source], "source_role": SOURCE_ROLES.get(source, "EVIDENCE_SOURCE")} for source in sources]
        authorities = sorted({authority for item in details for authority in item["authority"]})
        packet = {
            "page_id": page_id, "proposed_path": path, "page_action": action,
            "proposed_knowledge_status": status, "page_risk_score": score,
            "page_risk_class": risk, "scope": "Evidence-qualified refresh from material merged on main as of 2026-07-17.",
            "material_claims": [{"claim_id": f"{page_id.upper()}-1", "claim_text": claim,
                "claim_type": "INSTITUTIONAL_OR_LIFECYCLE_SYNTHESIS", "temporal_scope": "DATE_BOUND",
                "supporting_sources": sources, "supporting_source_authorities": details, "source_authority": authorities,
                "corroboration_status": "REVIEWED", "contradiction_status": "DISCLOSED_WHERE_PRESENT",
                "attribution_required": True, "confidence": "MEDIUM" if risk == "R3" else "HIGH", "allowed_in_page": True}],
            "known_limitations": ["Current-state claims are date-bound.", "Source authority does not imply independent factual verification."],
            "research_gaps": ["Resolve the page-specific limitations recorded in knowledge front matter."],
            "review_required": True, "review_after": "2026-10-17" if risk == "R3" else "2027-01-17"
        }
        write(PACKETS / f"{page_id}.json", packet)

    accepted = [{"path": p, "action": a, "packet": f"evidence-packets/{i}.json"} for i, p, a, *_ in SPECS]
    accepted += [{"path": p, "action": "INDEX_LINK_MAINTENANCE", "packet": None} for p in LINK_MAINTENANCE]
    ledger = {
        "campaign_id": "knowledge-context-refresh-2026-07-17", "accepted": accepted,
        "deferred": [
            {"candidate": "knowledge/gameplay/StarPath.md", "reason": "Sunset execution requires independent confirmation."},
            {"candidate": "knowledge/technology/Technical-Platform.md", "reason": "Starcomm-to-direct-RPC migration deferred to a focused technical review."},
            {"candidate": "knowledge/gameplay/ATOM.md", "reason": "Current evidence establishes an award, not stable product identity or lifecycle."},
            {"candidate": "knowledge/governance/Recipient-Payment-Ledger.md", "reason": "Council amounts are not yet reconciled to primary transactions."},
            {"candidate": "SAGE 3D exact release date", "reason": "Only month-level reviewed community evidence is available."},
        ],
        "duplicate": [
            {"candidate": "knowledge/gameplay/SCREAM.md", "canonical_path": "knowledge/gameplay/SAGE.md", "reason": "SCREAM is retained as SAGE development history, not a duplicate canonical product page."},
            {"candidate": "knowledge/governance/DAO-Treasury.md", "canonical_path": "knowledge/economy/DAO-Treasury-Architecture.md", "reason": "Treasury identity and evidence boundaries belong in the economy domain."},
        ],
        "rejected": [
            {"candidate": "Classify PIP-33 as Ecosystem Fund", "reason": "Official proposal and Council tracker identify a direct DAO Treasury measure."},
            {"candidate": "Promote completion state for failed PIPs 13, 15, 19, and 26", "reason": "Failure supplies no PIP authorization; tracker-derived N/A normalization is not an implementation milestone."},
        ],
    }
    write(HERE / "promotion-ledger.json", ledger)
    write(HERE / "campaign-summary.json", {
        "campaign_id": ledger["campaign_id"], "as_of": "2026-07-17", "base": "origin/main",
        "knowledge_pages_created": 7, "knowledge_pages_expanded": 7,
        "index_pages_updated": len(LINK_MAINTENANCE), "evidence_packets": len(SPECS),
        "knowledge_status_distribution": {"QUALIFIED": 13, "PROVISIONAL": 1},
        "risk_class_distribution": {"R2": 13, "R3": 1},
        "deferred": len(ledger["deferred"]), "duplicate": len(ledger["duplicate"]), "rejected": len(ledger["rejected"])
    })
    (HERE / "promotion-ledger.md").write_text(
        "# Promotion Ledger\n\nAccepted 14 substantive pages plus 7 index-link updates. "
        "Deferred 5 candidates, redirected 2 duplicates, and rejected 2 unsupported semantic promotions. "
        "See `promotion-ledger.json` for exact dispositions.\n", encoding="utf-8")
    (HERE / "campaign-summary.md").write_text(
        "# Campaign Summary\n\nCreated 7 knowledge pages, substantively expanded 7, and updated 7 indexes. "
        "No page relies on C1 or C2 alone; 13 outputs are R2/QUALIFIED and PIP-33 is R3/PROVISIONAL. "
        "No archive, graph, or publication evidence was rewritten.\n", encoding="utf-8")

if __name__ == "__main__":
    main()
