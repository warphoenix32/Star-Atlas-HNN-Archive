import copy
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "operations" / "ci" / "promotion_contract.py"
SPEC = importlib.util.spec_from_file_location("promotion_contract", MODULE_PATH)
promotion_contract = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = promotion_contract
SPEC.loader.exec_module(promotion_contract)


def example():
    path = ROOT / "operations" / "schema" / "examples" / "promotion-campaign-v1.json"
    return json.loads(path.read_text(encoding="utf-8"))


def reconcile_summary(payload):
    candidates = payload["candidates"]
    payload["summary"] = {
        "candidate_count": len(candidates),
        "risk_counts": dict(sorted(Counter(item["risk_class"] for item in candidates).items())),
        "review_mode_counts": dict(sorted(Counter(item["review_mode"] for item in candidates).items())),
        "disposition_counts": dict(sorted(Counter(item["disposition"] for item in candidates).items())),
        "open_human_decisions": sum(item["status"] == "OPEN" for item in payload["human_review_queue"]),
        "research_gap_count": len(payload["research_gaps"]),
    }


def test_example_is_valid_and_paths_resolve():
    assert promotion_contract.validate_campaign_report(example(), root=ROOT) == []


def test_r1_requires_every_automatic_eligibility_check():
    payload = example()
    payload["candidates"][0]["automatic_eligibility"]["no_conflict"] = False
    failures = promotion_contract.validate_campaign_report(payload, root=ROOT)
    assert any("every R1 eligibility check must pass" in failure for failure in failures)


def test_non_r1_cannot_be_automatically_approved():
    payload = example()
    candidate = payload["candidates"][0]
    candidate["risk_class"] = "R2"
    candidate["review_mode"] = "BATCH"
    failures = promotion_contract.validate_campaign_report(payload, root=ROOT)
    assert any("only R1 candidates may be AUTO_APPROVED" in failure for failure in failures)


def test_current_state_claim_requires_as_of():
    payload = example()
    payload["candidates"][0]["material_claims"][0]["as_of"] = None
    failures = promotion_contract.validate_campaign_report(payload, root=ROOT)
    assert any("current-state claim requires as_of" in failure for failure in failures)


def test_open_r3_decision_requires_evidence_consequences_and_defer():
    payload = example()
    candidate = payload["candidates"][0]
    candidate.update({
        "risk_class": "R3",
        "review_mode": "INDIVIDUAL",
        "disposition": "PENDING_REVIEW",
        "human_decision_id": "HRA-001",
    })
    candidate.pop("automatic_eligibility")
    payload["human_review_queue"] = [{
        "decision_id": "HRA-001",
        "question": "Should this qualified interpretation be promoted?",
        "evidence": [{"repository_path": "operations/docs/OPERATING-DOCTRINE.md"}],
        "recommendation": "Defer pending corroboration.",
        "consequences": ["Promotion would encode an unresolved interpretation."],
        "allowed_decisions": ["APPROVE", "REJECT", "DEFER"],
        "status": "OPEN",
    }]
    reconcile_summary(payload)
    assert promotion_contract.validate_campaign_report(payload, root=ROOT) == []

    missing_defer = copy.deepcopy(payload)
    missing_defer["human_review_queue"][0]["allowed_decisions"] = ["APPROVE", "REJECT"]
    failures = promotion_contract.validate_campaign_report(missing_defer, root=ROOT)
    assert any("must include DEFER" in failure for failure in failures)


def test_approved_r4_requires_explicit_authorization():
    payload = example()
    candidate = payload["candidates"][0]
    candidate.update({
        "risk_class": "R4",
        "review_mode": "INDIVIDUAL",
        "disposition": "APPROVED",
        "human_decision_id": "HRA-004",
    })
    candidate.pop("automatic_eligibility")
    payload["human_review_queue"] = [{
        "decision_id": "HRA-004",
        "question": "Should this elevated-risk candidate be approved?",
        "evidence": [{"repository_path": "operations/docs/OPERATING-DOCTRINE.md"}],
        "recommendation": "Approve only with explicit authorization.",
        "consequences": ["Approval permits the candidate to enter a draft PR."],
        "allowed_decisions": ["APPROVE", "REJECT", "DEFER"],
        "status": "RESOLVED",
        "decision": "APPROVE",
        "decision_authority": "HUMAN",
        "decided_by": "repository-owner",
        "decided_at": "2026-07-19",
    }]
    failures = promotion_contract.validate_campaign_report(payload, root=ROOT)
    assert any("requires authorization_id" in failure for failure in failures)


def test_r5_is_archive_only_and_has_no_canonical_target():
    payload = example()
    candidate = payload["candidates"][0]
    candidate.update({
        "risk_class": "R5",
        "review_mode": "ARCHIVE_ONLY",
        "disposition": "ARCHIVE_ONLY",
        "target_paths": [],
    })
    candidate.pop("automatic_eligibility")
    reconcile_summary(payload)
    assert promotion_contract.validate_campaign_report(payload, root=ROOT) == []


def test_merge_authority_cannot_be_automated():
    payload = example()
    payload["merge_authority"] = "AUTOMATED"
    failures = promotion_contract.validate_campaign_report(payload, root=ROOT)
    assert any("merge_authority must remain HUMAN_OR_BRANCH_PROTECTION" in failure for failure in failures)


def test_r1_requires_authoritative_evidence_and_complete_preservation():
    payload = example()
    payload["candidates"][0]["material_claims"][0]["source_authority"] = "B2"
    payload["preservation"]["provenance_complete"] = False
    failures = promotion_contract.validate_campaign_report(payload, root=ROOT)
    assert any("R1 claims require A1, A2, or A3 authority" in failure for failure in failures)
    assert any("preservation.provenance_complete=true" in failure for failure in failures)


def test_weak_machine_or_secondary_evidence_is_archive_only():
    payload = example()
    candidate = payload["candidates"][0]
    candidate["risk_class"] = "R2"
    candidate["review_mode"] = "BATCH"
    candidate["disposition"] = "APPROVED"
    candidate.pop("automatic_eligibility")
    candidate["material_claims"][0]["source_authority"] = "C2"
    failures = promotion_contract.validate_campaign_report(payload, root=ROOT)
    assert any("C1 or C2 evidence alone is archive-only" in failure for failure in failures)


def test_repository_paths_cannot_escape_the_checkout():
    payload = example()
    payload["candidates"][0]["material_claims"][0]["supporting_evidence"][0]["repository_path"] = "../outside.md"
    failures = promotion_contract.validate_campaign_report(payload, root=ROOT)
    assert any("not a safe repository-relative path" in failure for failure in failures)


def test_malformed_nested_values_report_failures_instead_of_crashing():
    payload = example()
    payload["preservation"]["source_ids"] = [{"invalid": True}]
    payload["candidates"][0]["candidate_id"] = {"invalid": True}
    payload["candidates"][0]["material_claims"] = ["not-a-claim"]
    failures = promotion_contract.validate_campaign_report(payload, root=ROOT)
    assert any("source_ids must contain non-empty strings" in failure for failure in failures)
    assert any("candidate_id is required" in failure for failure in failures)
    assert any("claim_id is required" in failure for failure in failures)
