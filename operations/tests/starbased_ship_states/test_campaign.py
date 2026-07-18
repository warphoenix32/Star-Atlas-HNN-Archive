import csv
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).parents[3]
CAMPAIGN = ROOT / "operations" / "campaigns" / "starbased-ship-states-ingestion-2026-07"
BUILD_PATH = CAMPAIGN / "build_campaign.py"
SPEC = importlib.util.spec_from_file_location("starbased_ship_states", BUILD_PATH)
builder = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = builder
SPEC.loader.exec_module(builder)


def test_raw_artifact_is_preserved_with_expected_checksum():
    assert builder.RAW_PATH.is_file()
    assert builder.sha256(builder.RAW_PATH) == builder.EXPECTED_SHA256


def test_source_has_expected_dimensions_and_unique_identifiers():
    with builder.RAW_PATH.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)
        headers = list(reader.fieldnames or [])
    assert (len(rows), len(headers)) == (63, 26)
    assert headers[0] == ""
    assert len({row[headers[0]] for row in rows}) == 63
    assert len({row["NameLinks to Marketplace"] for row in rows}) == 63


def test_build_is_deterministic_and_stays_in_staging():
    first = builder.build()
    second = builder.build()
    assert first == second
    assert not (ROOT / "archive" / "normalized" / "starbased-ship-states").exists()
    preview = [json.loads(line) for line in first["normalized-preview.jsonl"].splitlines()]
    assert len(preview) == 63
    assert all(item["normalization_status"] == "SEMANTIC_REVIEW_REQUIRED" for item in preview)


def test_mapping_covers_each_source_column_once():
    rendered = builder.build()
    mapping = json.loads(rendered["normalization-map.json"])["columns"]
    source_headers = [item[0] for item in builder.COLUMN_MAP]
    assert [item["source_header"] for item in mapping] == source_headers
    assert len({item["normalized_field"] for item in mapping}) == 26


def test_context_questions_gate_semantic_promotion():
    questions = json.loads(builder.build()["context-questions.json"])
    assert len(questions["questions"]) == 8
    assert questions["blocking_question_count"] == 6
    assert all(item["decision_status"] == "OPEN" for item in questions["questions"])
