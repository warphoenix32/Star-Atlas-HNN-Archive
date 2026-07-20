"""Validation for the opt-in simplified promotion campaign contract."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


PIPELINE_VERSION = "1.0"
STAGES = ("PRESERVE", "DRAFT", "REVIEW", "PUBLISH")
RISK_REVIEW_MODES = {
    "R1": "AUTOMATED",
    "R2": "BATCH",
    "R3": "INDIVIDUAL",
    "R4": "INDIVIDUAL",
    "R5": "ARCHIVE_ONLY",
}
DISPOSITIONS = {"PENDING_REVIEW", "AUTO_APPROVED", "APPROVED", "REVISE", "DEFERRED", "REJECTED", "ARCHIVE_ONLY"}
R1_CHECKS = {
    "direct_evidence",
    "established_entity_ids",
    "established_taxonomy",
    "no_conflict",
    "no_identity_resolution",
    "no_financial_legal_reputational_claim",
    "no_treasury_or_governance_execution_claim",
    "no_sensitive_claim",
    "no_lifecycle_inference",
    "current_state_date_scoped",
    "citations_resolve",
}


class PromotionContractError(ValueError):
    """Raised when a campaign report violates the simplified contract."""


def _require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def validate_campaign_report(payload: Any, root: Path | None = None) -> list[str]:
    failures: list[str] = []
    _require(isinstance(payload, dict), "report must be a JSON object", failures)
    if not isinstance(payload, dict):
        return failures

    _require(payload.get("pipeline_version") == PIPELINE_VERSION, "pipeline_version must be 1.0", failures)
    _require(bool(payload.get("campaign_id")), "campaign_id is required", failures)
    _require(payload.get("current_stage") in STAGES, "current_stage is invalid", failures)
    _require(payload.get("merge_authority") == "HUMAN_OR_BRANCH_PROTECTION", "merge_authority must remain HUMAN_OR_BRANCH_PROTECTION", failures)

    stages = payload.get("stages")
    _require(isinstance(stages, list) and [item.get("stage") for item in stages if isinstance(item, dict)] == list(STAGES), "stages must declare PRESERVE, DRAFT, REVIEW, PUBLISH in order", failures)
    for item in stages if isinstance(stages, list) else []:
        _require(isinstance(item, dict) and item.get("status") in {"PENDING", "IN_PROGRESS", "COMPLETE", "BLOCKED"}, "each stage requires a valid status", failures)

    candidates = payload.get("candidates")
    _require(isinstance(candidates, list), "candidates must be a list", failures)
    candidates = candidates if isinstance(candidates, list) else []
    preservation = payload.get("preservation")
    _require(isinstance(preservation, dict), "preservation object is required", failures)
    if isinstance(preservation, dict):
        source_ids = preservation.get("source_ids")
        _require(isinstance(source_ids, list), "preservation.source_ids must be a list", failures)
        if isinstance(source_ids, list):
            source_ids_valid = all(isinstance(value, str) and bool(value) for value in source_ids)
            _require(source_ids_valid, "preservation.source_ids must contain non-empty strings", failures)
            if source_ids_valid:
                _require(len(source_ids) == len(set(source_ids)), "preservation.source_ids must be unique", failures)
        for field in ("raw_immutable", "provenance_complete", "normalization_deterministic"):
            _require(isinstance(preservation.get(field), bool), f"preservation.{field} must be boolean", failures)
    candidate_ids: set[str] = set()
    claim_ids: set[str] = set()
    review_decisions: dict[str, dict[str, Any]] = {}

    queue = payload.get("human_review_queue")
    _require(isinstance(queue, list), "human_review_queue must be a list", failures)
    queue = queue if isinstance(queue, list) else []
    for decision in queue:
        if not isinstance(decision, dict):
            failures.append("human review items must be objects")
            continue
        raw_decision_id = decision.get("decision_id")
        decision_id = raw_decision_id if isinstance(raw_decision_id, str) and raw_decision_id else "<invalid-decision-id>"
        _require(decision_id != "<invalid-decision-id>", "human review item requires decision_id", failures)
        _require(str(decision_id) not in review_decisions, f"{decision_id}: duplicate decision_id", failures)
        _require(bool(decision.get("question")), f"{decision_id}: question is required", failures)
        _require(bool(decision.get("recommendation")), f"{decision_id}: recommendation is required", failures)
        decision_evidence = decision.get("evidence")
        _require(isinstance(decision_evidence, list) and bool(decision_evidence), f"{decision_id}: evidence is required", failures)
        for ref in decision_evidence if isinstance(decision_evidence, list) else []:
            _require(isinstance(ref, dict) and (bool(ref.get("source_id")) or bool(ref.get("repository_path"))), f"{decision_id}: evidence needs source_id or repository_path", failures)
            repository_path = ref.get("repository_path") if isinstance(ref, dict) else None
            if root and repository_path:
                safe_path = isinstance(repository_path, str) and "\\" not in repository_path and ".." not in Path(repository_path).parts and not Path(repository_path).is_absolute()
                _require(safe_path, f"{decision_id}: evidence path is not a safe repository-relative path: {repository_path}", failures)
                if safe_path:
                    _require((root / repository_path).exists(), f"{decision_id}: evidence path does not resolve: {repository_path}", failures)
        _require(isinstance(decision.get("consequences"), list) and bool(decision.get("consequences")), f"{decision_id}: consequences are required", failures)
        options = decision.get("allowed_decisions")
        _require(isinstance(options, list) and "DEFER" in options, f"{decision_id}: allowed_decisions must include DEFER", failures)
        _require(decision.get("status") in {"OPEN", "RESOLVED"}, f"{decision_id}: status must be OPEN or RESOLVED", failures)
        if decision.get("status") == "RESOLVED":
            _require(decision.get("decision") in {"APPROVE", "REVISE", "REJECT", "DEFER"}, f"{decision_id}: resolved item requires a valid decision", failures)
            _require(decision.get("decision_authority") == "HUMAN", f"{decision_id}: resolved item requires HUMAN decision authority", failures)
            _require(bool(decision.get("decided_by")), f"{decision_id}: resolved item requires decided_by", failures)
            _require(bool(decision.get("decided_at")), f"{decision_id}: resolved item requires decided_at", failures)
        if decision_id != "<invalid-decision-id>":
            review_decisions[str(decision_id)] = decision

    for candidate in candidates:
        if not isinstance(candidate, dict):
            failures.append("candidates must contain objects")
            continue
        raw_candidate_id = candidate.get("candidate_id")
        cid = raw_candidate_id if isinstance(raw_candidate_id, str) and raw_candidate_id else "<invalid-candidate-id>"
        _require(cid != "<invalid-candidate-id>", "candidate_id is required", failures)
        _require(cid not in candidate_ids, f"{cid}: duplicate candidate_id", failures)
        candidate_ids.add(cid)
        risk = candidate.get("risk_class")
        mode = candidate.get("review_mode")
        disposition = candidate.get("disposition")
        _require(risk in RISK_REVIEW_MODES, f"{cid}: invalid risk_class", failures)
        if risk in RISK_REVIEW_MODES:
            _require(mode == RISK_REVIEW_MODES[risk], f"{cid}: {risk} requires {RISK_REVIEW_MODES[risk]} review", failures)
        _require(disposition in DISPOSITIONS, f"{cid}: invalid disposition", failures)

        target_paths = candidate.get("target_paths")
        _require(isinstance(target_paths, list), f"{cid}: target_paths must be a list", failures)
        for target in target_paths if isinstance(target_paths, list) else []:
            safe_target = isinstance(target, str) and "\\" not in target and ".." not in Path(target).parts and not Path(target).is_absolute()
            _require(safe_target and target.startswith(("knowledge/", "graph/")), f"{cid}: target path must be a safe repository path under knowledge/ or graph/", failures)

        claims = candidate.get("material_claims")
        _require(isinstance(claims, list) and bool(claims), f"{cid}: at least one material claim is required", failures)
        for claim in claims if isinstance(claims, list) else []:
            raw_claim_id = claim.get("claim_id") if isinstance(claim, dict) else None
            claim_id = raw_claim_id if isinstance(raw_claim_id, str) and raw_claim_id else "<invalid-claim-id>"
            _require(claim_id not in claim_ids, f"{cid}/{claim_id}: duplicate claim_id", failures)
            claim_ids.add(claim_id)
            _require(claim_id != "<invalid-claim-id>", f"{cid}: claim_id is required", failures)
            _require(isinstance(claim, dict) and bool(claim.get("claim_text")), f"{cid}/{claim_id}: claim_text is required", failures)
            _require(bool(claim.get("claim_type")) if isinstance(claim, dict) else False, f"{cid}/{claim_id}: claim_type is required", failures)
            authority = claim.get("source_authority") if isinstance(claim, dict) else None
            _require(authority in {"A1", "A2", "A3", "B1", "B2", "C1", "C2"}, f"{cid}/{claim_id}: source_authority is required", failures)
            _require(bool(claim.get("temporal_scope")) if isinstance(claim, dict) else False, f"{cid}/{claim_id}: temporal_scope is required", failures)
            _require(claim.get("contradiction_status") in {"NONE_IDENTIFIED", "CONFLICTED", "UNRESOLVED"} if isinstance(claim, dict) else False, f"{cid}/{claim_id}: contradiction_status is required", failures)
            evidence = claim.get("supporting_evidence") if isinstance(claim, dict) else None
            _require(isinstance(evidence, list) and bool(evidence), f"{cid}/{claim_id}: supporting evidence is required", failures)
            for ref in evidence if isinstance(evidence, list) else []:
                _require(isinstance(ref, dict) and (bool(ref.get("source_id")) or bool(ref.get("repository_path"))), f"{cid}/{claim_id}: evidence needs source_id or repository_path", failures)
                repository_path = ref.get("repository_path") if isinstance(ref, dict) else None
                if root and repository_path:
                    safe_path = isinstance(repository_path, str) and "\\" not in repository_path and ".." not in Path(repository_path).parts and not Path(repository_path).is_absolute()
                    _require(safe_path, f"{cid}/{claim_id}: evidence path is not a safe repository-relative path: {repository_path}", failures)
                    if safe_path:
                        _require((root / repository_path).exists(), f"{cid}/{claim_id}: evidence path does not resolve: {repository_path}", failures)
            if isinstance(claim, dict) and claim.get("current_state"):
                _require(bool(claim.get("as_of")), f"{cid}/{claim_id}: current-state claim requires as_of", failures)

        if risk == "R1":
            _require(disposition == "AUTO_APPROVED", f"{cid}: R1 automated candidate must be AUTO_APPROVED", failures)
            checks = candidate.get("automatic_eligibility")
            _require(isinstance(checks, dict), f"{cid}: R1 requires automatic_eligibility", failures)
            if isinstance(checks, dict):
                _require(set(checks) == R1_CHECKS, f"{cid}: R1 eligibility checklist is incomplete or contains unknown checks", failures)
                _require(all(value is True for value in checks.values()), f"{cid}: every R1 eligibility check must pass", failures)
            for claim in claims if isinstance(claims, list) else []:
                if not isinstance(claim, dict):
                    continue
                _require(claim.get("source_authority") in {"A1", "A2", "A3"}, f"{cid}: R1 claims require A1, A2, or A3 authority", failures)
                _require(claim.get("contradiction_status") == "NONE_IDENTIFIED", f"{cid}: R1 claims cannot contain unresolved contradictions", failures)
        elif disposition == "AUTO_APPROVED":
            failures.append(f"{cid}: only R1 candidates may be AUTO_APPROVED")

        if risk != "R5":
            for claim in claims if isinstance(claims, list) else []:
                if not isinstance(claim, dict):
                    continue
                _require(claim.get("source_authority") not in {"C1", "C2"}, f"{cid}: C1 or C2 evidence alone is archive-only", failures)

        if disposition in {"AUTO_APPROVED", "APPROVED"} and isinstance(preservation, dict):
            _require(bool(preservation.get("source_ids")), f"{cid}: approved promotion requires at least one preserved Source ID", failures)
            for field in ("raw_immutable", "provenance_complete", "normalization_deterministic"):
                _require(preservation.get(field) is True, f"{cid}: approved promotion requires preservation.{field}=true", failures)

        if risk == "R5":
            _require(disposition == "ARCHIVE_ONLY", f"{cid}: R5 must remain ARCHIVE_ONLY", failures)
            _require(not target_paths, f"{cid}: R5 cannot target canonical knowledge or graph paths", failures)

        if risk in {"R3", "R4"}:
            decision_id = candidate.get("human_decision_id")
            _require(bool(decision_id), f"{cid}: {risk} candidate requires human_decision_id", failures)
            decision = review_decisions.get(str(decision_id))
            _require(decision is not None, f"{cid}: human_decision_id must resolve to the human review queue", failures)
            if decision:
                if decision.get("status") == "OPEN":
                    _require(disposition == "PENDING_REVIEW", f"{cid}: OPEN human decision requires PENDING_REVIEW disposition", failures)
                else:
                    expected = {"APPROVE": "APPROVED", "REVISE": "REVISE", "REJECT": "REJECTED", "DEFER": "DEFERRED"}.get(decision.get("decision"))
                    _require(disposition == expected, f"{cid}: disposition does not match resolved human decision", failures)
        if risk == "R4" and disposition == "APPROVED":
            _require(bool(candidate.get("authorization_id")), f"{cid}: approved R4 candidate requires authorization_id", failures)

    summary = payload.get("summary")
    _require(isinstance(summary, dict), "summary object is required", failures)
    if isinstance(summary, dict):
        def counts(field: str) -> dict[str, int]:
            values = [item.get(field) for item in candidates if isinstance(item, dict) and isinstance(item.get(field), str)]
            return dict(sorted(Counter(values).items()))

        expected_risks = counts("risk_class")
        expected_modes = counts("review_mode")
        expected_dispositions = counts("disposition")
        _require(summary.get("candidate_count") == len(candidates), "summary.candidate_count does not reconcile", failures)
        _require(summary.get("risk_counts") == expected_risks, "summary.risk_counts do not reconcile", failures)
        _require(summary.get("review_mode_counts") == expected_modes, "summary.review_mode_counts do not reconcile", failures)
        _require(summary.get("disposition_counts") == expected_dispositions, "summary.disposition_counts do not reconcile", failures)
        _require(summary.get("open_human_decisions") == sum(item.get("status") == "OPEN" for item in queue if isinstance(item, dict)), "summary.open_human_decisions does not reconcile", failures)
        gaps = payload.get("research_gaps")
        _require(isinstance(gaps, list), "research_gaps must be a list", failures)
        _require(summary.get("research_gap_count") == (len(gaps) if isinstance(gaps, list) else 0), "summary.research_gap_count does not reconcile", failures)

    validation = payload.get("validation")
    _require(isinstance(validation, dict), "validation object is required", failures)
    if isinstance(validation, dict):
        _require(validation.get("status") in {"PASS", "FAIL", "PARTIAL"}, "validation.status is invalid", failures)
        checks = validation.get("checks")
        _require(isinstance(checks, list) and bool(checks), "validation checks are required", failures)
        for check in checks if isinstance(checks, list) else []:
            _require(isinstance(check, dict) and bool(check.get("name")) and isinstance(check.get("passed"), bool), "validation checks require name and boolean passed", failures)
        if validation.get("status") == "PASS" and isinstance(checks, list):
            _require(all(check.get("passed") is True for check in checks if isinstance(check, dict)), "PASS validation cannot contain failed checks", failures)

    return failures


def validate_file(path: Path, root: Path | None = None) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    failures = validate_campaign_report(payload, root=root)
    if failures:
        raise PromotionContractError("\n".join(failures))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reports", nargs="+", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    failed = False
    for path in args.reports:
        try:
            validate_file(path, root=args.root)
            print(f"PASS simplified-promotion-contract: {path}")
        except (OSError, json.JSONDecodeError, PromotionContractError) as exc:
            failed = True
            print(f"FAIL simplified-promotion-contract: {path}: {exc}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
