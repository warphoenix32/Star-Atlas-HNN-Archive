#!/usr/bin/env python3
"""Validate Starbased ship-state preservation and normalization staging."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any

from build_campaign import (
    CAMPAIGN_DIR,
    CAMPAIGN_ID,
    COLUMN_MAP,
    EXPECTED_SHA256,
    PROVENANCE_REL,
    RAW_PATH,
    ROOT,
    build,
)


def check(name: str, passed: bool, detail: Any) -> dict[str, Any]:
    return {"name": name, "passed": bool(passed), "detail": detail}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def validate() -> dict[str, Any]:
    generated = build()
    checks: list[dict[str, Any]] = []

    checks.append(check("raw_artifact_checksum", sha256(RAW_PATH) == EXPECTED_SHA256, sha256(RAW_PATH)))
    provenance = json.loads((ROOT / PROVENANCE_REL).read_text(encoding="utf-8"))
    checks.append(check(
        "provenance_reconciles_to_raw",
        provenance["raw_artifact"]["sha256"] == EXPECTED_SHA256
        and provenance["raw_artifact"]["byte_length"] == RAW_PATH.stat().st_size,
        provenance["raw_artifact"],
    ))
    checks.append(check(
        "provenance_excludes_local_personal_path",
        "Users/" not in json.dumps(provenance) and "Users\\" not in json.dumps(provenance),
        provenance["custody"]["original_filename"],
    ))

    with RAW_PATH.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)
        headers = list(reader.fieldnames or [])
    expected_headers = [item[0] for item in COLUMN_MAP]
    checks.append(check("exact_header_contract", headers == expected_headers, headers))
    checks.append(check("source_dimensions", len(rows) == 63 and len(headers) == 26, {"rows": len(rows), "columns": len(headers)}))
    checks.append(check("blank_first_header_only", headers[0] == "" and all(headers[1:]), headers[0]))
    checks.append(check("complete_cells", all(all(row[header].strip() for header in headers) for row in rows), None))
    checks.append(check("unique_ship_codes", len({row[headers[0]] for row in rows}) == len(rows), len(rows)))
    checks.append(check("unique_ship_names", len({row["NameLinks to Marketplace"] for row in rows}) == len(rows), len(rows)))
    checks.append(check("unique_complete_rows", len({tuple(row[header] for header in headers) for row in rows}) == len(rows), len(rows)))
    numeric_headers = [source for source, _, data_type, _, _ in COLUMN_MAP if data_type == "number"]
    numeric_failures = []
    for row_number, row in enumerate(rows, start=2):
        for header in numeric_headers:
            try:
                float(row[header])
            except ValueError:
                numeric_failures.append({"row": row_number, "header": header, "value": row[header]})
    checks.append(check("numeric_metric_cells", not numeric_failures, numeric_failures))

    for filename, expected_content in generated.items():
        path = CAMPAIGN_DIR / filename
        checks.append(check(
            f"generated_{filename}_fixed_point",
            path.is_file() and path.read_text(encoding="utf-8") == expected_content,
            filename,
        ))
    checks.append(check("deterministic_build", generated == build(), sorted(generated)))

    preview = load_jsonl(CAMPAIGN_DIR / "normalized-preview.jsonl")
    checks.append(check("preview_record_count", len(preview) == 63, len(preview)))
    checks.append(check("preview_record_ids_unique", len({item["record_id"] for item in preview}) == len(preview), len(preview)))
    checks.append(check(
        "preview_source_rows_resolve",
        [item["source"]["row_number"] for item in preview] == list(range(2, 65))
        and all(item["source"]["sha256"] == EXPECTED_SHA256 for item in preview),
        {"first": preview[0]["source"]["row_number"], "last": preview[-1]["source"]["row_number"]},
    ))
    checks.append(check(
        "preview_remains_semantic_review_required",
        all(item["normalization_status"] == "SEMANTIC_REVIEW_REQUIRED" for item in preview),
        len(preview),
    ))
    mapping = json.loads((CAMPAIGN_DIR / "normalization-map.json").read_text(encoding="utf-8"))
    checks.append(check(
        "mapping_is_complete_and_non_circular",
        len(mapping["columns"]) == len(headers)
        and {item["source_header"] for item in mapping["columns"]} == set(headers)
        and len({item["normalized_field"] for item in mapping["columns"]}) == len(headers),
        len(mapping["columns"]),
    ))
    questions = json.loads((CAMPAIGN_DIR / "context-questions.json").read_text(encoding="utf-8"))
    checks.append(check(
        "context_questions_are_open",
        len(questions["questions"]) == 8
        and questions["blocking_question_count"] == 6
        and all(item["answer"] is None and item["decision_status"] == "OPEN" for item in questions["questions"]),
        {"questions": len(questions["questions"]), "blocking": questions["blocking_question_count"]},
    ))
    checks.append(check(
        "normalized_archive_not_prematurely_written",
        not (ROOT / "archive/normalized/starbased-ship-states").exists(),
        "archive/normalized/starbased-ship-states",
    ))

    manifest = json.loads((CAMPAIGN_DIR / "manifest.json").read_text(encoding="utf-8"))
    manifest_failures = []
    for item in manifest["files"]:
        path = ROOT / item["path"]
        if not path.is_file() or sha256(path) != item["sha256"]:
            manifest_failures.append(item["path"])
    checks.append(check("manifest_checksums_resolve", not manifest_failures, manifest_failures))

    status = "pass" if all(item["passed"] for item in checks) else "fail"
    return {
        "campaign_id": CAMPAIGN_ID,
        "status": status,
        "checks": checks,
        "summary": {
            "checks_passed": sum(item["passed"] for item in checks),
            "checks_total": len(checks),
            "raw_artifacts": 1,
            "preview_records": len(preview),
            "open_context_questions": len(questions["questions"]),
        },
    }


if __name__ == "__main__":
    report = validate()
    (CAMPAIGN_DIR / "validation-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps({"campaign_id": CAMPAIGN_ID, "status": report["status"]}))
    raise SystemExit(0 if report["status"] == "pass" else 1)
