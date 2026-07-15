#!/usr/bin/env python3
"""Apply Chief of Staff review corrections after build_campaign.py.

Run this immediately after the base generator until the stricter event-identity and
cross-source linkage logic is incorporated directly into the primary generator.
"""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SEMANTIC = REPO / "archive/semantic/discord-announcements"
RECON = REPO / "archive/semantic/reconciliation"


def write(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    write(SEMANTIC / "event-sequences.json", {
        "campaign_id": "discord-announcements-semantic-enrichment",
        "sequence_count": 0,
        "sequences": [],
        "review_disposition": "WITHHELD_PENDING_EVENT_IDENTITY_RECLUSTERING",
        "reason": "Category-plus-entity grouping joined unrelated events across long time periods.",
        "required_future_method": {
            "minimum_identity_signals": [
                "shared explicit event or incident identifier",
                "shared PIP number, release name, transaction, outage, or program instance",
                "bounded temporal adjacency appropriate to the event class"
            ],
            "prohibited_basis": "category-plus-entity alone"
        },
        "evidence_preservation": "All underlying source records remain preserved."
    })
    write(RECON / "cross-source-promotion-candidates.json", {
        "campaign_id": "discord-announcements-semantic-enrichment",
        "record_count": 0,
        "records": [],
        "review_disposition": "WITHHELD_PENDING_SECOND_SOURCE_LINKAGE",
        "reason": "Single-source Discord candidates are not cross-source candidates.",
        "required_fields_for_future_records": [
            "discord_source_id", "additional_source_ids", "relationship",
            "claim_or_event_identity", "cross_source_basis",
            "manual_review_required", "canonical_promotion_status"
        ],
        "single_source_queue": "archive/semantic/discord-announcements/promotion-candidates.json"
    })
    write(RECON / "cross-source-contradictions.json", {
        "campaign_id": "discord-announcements-semantic-enrichment",
        "automated_rule_conflict_count": 0,
        "records": [],
        "review_status": "NOT_EXHAUSTIVELY_HUMAN_REVIEWED",
        "interpretation": "No explicit conflicts were found by the evaluated deterministic rules; this does not establish that the corpora contain no contradictions.",
        "remaining_work": [
            "claim-level lifecycle and current-state review",
            "correction, delay, cancellation, and supersession review",
            "manual comparison of differing dates, names, metrics, and implementation states"
        ]
    })


if __name__ == "__main__":
    main()
