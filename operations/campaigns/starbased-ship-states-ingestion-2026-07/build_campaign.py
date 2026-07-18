#!/usr/bin/env python3
"""Build deterministic staging artifacts for the Starbased ship-state CSV."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


CAMPAIGN_ID = "starbased-ship-states-ingestion-2026-07"
SCHEMA_VERSION = "1.0.0"
AS_OF = "2026-07-18"
ROOT = Path(__file__).resolve().parents[3]
CAMPAIGN_DIR = Path(__file__).resolve().parent
RAW_REL = Path("archive/raw/starbased-ship-states/rydn_starbased_ships_20260718.csv")
RAW_PATH = ROOT / RAW_REL
PROVENANCE_REL = Path("archive/provenance/starbased-ship-states/rydn_starbased_ships_20260718.json")
EXPECTED_SHA256 = "7b90513e578998b8e763dd440984268000efed91c95feb047e81a19817a82dc9"


COLUMN_MAP = [
    ("", "ship_code", "string", None, "PENDING_HEADER_CONFIRMATION"),
    ("NameLinks to Marketplace", "ship_name", "string", None, "PENDING_LINK_AND_NAME_CONFIRMATION"),
    ("Spec", "specialization_observed", "string", None, "OBSERVED_TAXONOMY"),
    ("CargoCapacity", "cargo_capacity", "number", "source_unit_unresolved", "PENDING_UNIT_AND_MODULE_CONFIRMATION"),
    ("USDC /Cargo Capacity", "usdc_per_cargo_capacity", "number", "USDC per source cargo unit", "PENDING_DERIVATION_CONFIRMATION"),
    ("FuelCapacity", "fuel_capacity", "number", "source_unit_unresolved", "PENDING_UNIT_AND_MODULE_CONFIRMATION"),
    ("AmmoCapacity", "ammo_capacity", "number", "source_unit_unresolved", "PENDING_UNIT_AND_MODULE_CONFIRMATION"),
    ("Food / sec(Mining)", "mining_food_per_second", "number", "food per second", "PENDING_MODULE_CONFIRMATION"),
    ("Ammo / sec(Mining)", "mining_ammo_per_second", "number", "ammo per second", "PENDING_MODULE_CONFIRMATION"),
    ("Mining Rate[Resource/sec]", "mining_rate_resource_per_second", "number", "resource per second", "PENDING_MODULE_CONFIRMATION"),
    ("USDC /Mining Rate", "usdc_per_mining_rate", "number", "USDC per source mining-rate unit", "PENDING_DERIVATION_CONFIRMATION"),
    ("Subwarp Speed[AU/sec]", "subwarp_speed_au_per_second", "number", "AU per second", "PENDING_SCALE_AND_MODULE_CONFIRMATION"),
    ("Warp Speed[AU/sec]", "warp_speed_au_per_second", "number", "AU per second", "PENDING_SCALE_AND_MODULE_CONFIRMATION"),
    ("Max WarpDistance [AU]", "max_warp_distance_au", "number", "AU", "PENDING_MODULE_CONFIRMATION"),
    ("Warp Cooldown[sec]", "warp_cooldown_seconds", "number", "seconds", "PENDING_MODULE_CONFIRMATION"),
    ("Fuel /AU Warp", "warp_fuel_per_au", "number", "fuel per AU", "PENDING_MODULE_CONFIRMATION"),
    ("Cargo /Warp Fuel", "cargo_per_warp_fuel", "number", "cargo per warp fuel", "PENDING_DERIVATION_CONFIRMATION"),
    ("Fuel /AU Subwarp", "subwarp_fuel_per_au", "number", "fuel per AU", "PENDING_MODULE_CONFIRMATION"),
    ("Asteroid ExitFuel", "asteroid_exit_fuel", "number", "fuel", "PENDING_DEFINITION_AND_MODULE_CONFIRMATION"),
    ("Crew\u00a0", "crew", "number", "persons", "PENDING_MODULE_CONFIRMATION"),
    ("Passengers\u00a0", "passengers", "number", "persons", "PENDING_MODULE_CONFIRMATION"),
    ("Respawn Time[sec]", "respawn_time_seconds", "number", "seconds", "PENDING_MODULE_CONFIRMATION"),
    ("Scan Cooldown[sec]", "scan_cooldown_seconds", "number", "seconds", "PENDING_MODULE_CONFIRMATION"),
    ("Food /Scan", "food_per_scan", "number", "food per scan", "PENDING_MODULE_CONFIRMATION"),
    ("SDU /Scan", "sdu_per_scan", "number", "SDU per scan", "PENDING_MODULE_CONFIRMATION"),
    ("Food /SDU", "food_per_sdu", "number", "food per SDU", "PENDING_DERIVATION_CONFIRMATION"),
]


QUESTIONS = [
    {
        "question_id": "Q01_SOURCE_AUTHORITY",
        "topic": "source authority",
        "question": "Who created and maintains this export, and does 'rydn' identify Ryden/Ryden Systems? Please provide the originating application, sheet, URL, or version if one exists.",
        "blocking": True,
    },
    {
        "question_id": "Q02_CURRENTLY_AVAILABLE",
        "topic": "row scope",
        "question": "What does 'currently available' mean here: minted NFTs, marketplace-listed ships, SAGE-playable ships, C4-planned ships, or another inclusion rule?",
        "blocking": True,
    },
    {
        "question_id": "Q03_GAME_MODULE_ASSIGNMENT",
        "topic": "SAGE and C4 applicability",
        "question": "Which columns are current SAGE values, which are planned C4 values, and which are shared? Are future C4 values provisional design targets?",
        "blocking": True,
    },
    {
        "question_id": "Q04_SHIP_CODE",
        "topic": "blank first header",
        "question": "Please confirm that the unnamed first column is the canonical ship code or asset symbol, and identify the system that defines codes such as PULSE, FBLAIR, and T1TAN.",
        "blocking": True,
    },
    {
        "question_id": "Q05_MARKETPLACE_LINKS",
        "topic": "lost hyperlinks",
        "question": "The 'NameLinks to Marketplace' column contains names but no URLs in CSV. Were spreadsheet hyperlinks stripped during export, and should marketplace URLs be recovered from the source sheet?",
        "blocking": False,
    },
    {
        "question_id": "Q06_IDENTICAL_METRICS",
        "topic": "derived metric integrity",
        "question": "Are the three always-identical pairs intentional: CargoCapacity vs USDC/Cargo Capacity, Mining Rate vs USDC/Mining Rate, and Fuel/AU Warp vs Cargo/Warp Fuel? If derived from price, what price field and timestamp should be used?",
        "blocking": True,
    },
    {
        "question_id": "Q07_UNITS_AND_SCALE",
        "topic": "units and numeric scale",
        "question": "Please confirm the native units and scale factors for capacities, fuel, food, ammo, SDU, and movement values. In particular, is Warp Speed = 100000 AU/sec literal or scaled?",
        "blocking": True,
    },
    {
        "question_id": "Q08_CANONICAL_NAMES",
        "topic": "name normalization",
        "question": "Should names and specialization labels be preserved exactly as game-facing canonical text, or corrected for capitalization/spelling (for example VZUS solos, Opal Jetjet, and Data runner)?",
        "blocking": False,
    },
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def dump_jsonl(records: list[dict[str, Any]]) -> str:
    return "".join(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records)


def load_rows() -> tuple[list[str], list[dict[str, str]]]:
    with RAW_PATH.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)
        return list(reader.fieldnames or []), rows


def numeric(value: str) -> int | float:
    number = float(value)
    return int(number) if number.is_integer() else number


def build() -> dict[str, str]:
    headers, rows = load_rows()
    raw_bytes = RAW_PATH.read_bytes()
    mapping = [
        {
            "ordinal": index + 1,
            "source_header": source,
            "normalized_field": target,
            "data_type": data_type,
            "unit": unit,
            "semantic_status": status,
        }
        for index, (source, target, data_type, unit, status) in enumerate(COLUMN_MAP)
    ]
    preview = []
    for row_number, row in enumerate(rows, start=2):
        typed = {
            target: (numeric(row[source]) if data_type == "number" else row[source])
            for source, target, data_type, _, _ in COLUMN_MAP
        }
        ship_code = typed.pop("ship_code")
        ship_name = typed.pop("ship_name")
        specialization = typed.pop("specialization_observed")
        preview.append({
            "record_id": f"SHIP-{ship_code}",
            "schema_version": SCHEMA_VERSION,
            "ship_code": ship_code,
            "ship_name_observed": ship_name,
            "specialization_observed": specialization,
            "metrics": typed,
            "normalization_status": "SEMANTIC_REVIEW_REQUIRED",
            "source": {
                "artifact_id": "SRC-STARB-7B90513E578998B8",
                "path": RAW_REL.as_posix(),
                "row_number": row_number,
                "sha256": EXPECTED_SHA256,
            },
        })

    duplicate_rows = len(rows) - len({tuple(row.get(header, "") for header in headers) for row in rows})
    spec_counts = dict(sorted(Counter(row["Spec"] for row in rows).items()))
    empty_counts = {header: sum(not row[header].strip() for row in rows) for header in headers}
    numeric_headers = [source for source, _, data_type, _, _ in COLUMN_MAP if data_type == "number"]
    profile = {
        "campaign_id": CAMPAIGN_ID,
        "source": RAW_REL.as_posix(),
        "sha256": sha256(RAW_PATH),
        "byte_length": len(raw_bytes),
        "encoding": "UTF-8 without BOM" if not raw_bytes.startswith(b"\xef\xbb\xbf") else "UTF-8 with BOM",
        "line_endings": "CRLF" if raw_bytes.count(b"\r\n") == raw_bytes.count(b"\n") else "mixed_or_LF",
        "row_count": len(rows),
        "column_count": len(headers),
        "headers": headers,
        "blank_header_ordinals": [index + 1 for index, header in enumerate(headers) if not header],
        "empty_cell_counts": empty_counts,
        "duplicate_complete_rows": duplicate_rows,
        "duplicate_ship_codes": len(rows) - len({row[headers[0]] for row in rows}),
        "duplicate_ship_names": len(rows) - len({row["NameLinks to Marketplace"] for row in rows}),
        "numeric_columns": numeric_headers,
        "specialization_counts": spec_counts,
        "exact_equality_checks": {
            "CargoCapacity_equals_USDC_per_Cargo_Capacity": sum(row["CargoCapacity"] == row["USDC /Cargo Capacity"] for row in rows),
            "Mining_Rate_equals_USDC_per_Mining_Rate": sum(row["Mining Rate[Resource/sec]"] == row["USDC /Mining Rate"] for row in rows),
            "Warp_Fuel_per_AU_equals_Cargo_per_Warp_Fuel": sum(row["Fuel /AU Warp"] == row["Cargo /Warp Fuel"] for row in rows),
            "Warp_Speed_100000": sum(row["Warp Speed[AU/sec]"] == "100000" for row in rows),
        },
    }
    questions = {
        "campaign_id": CAMPAIGN_ID,
        "status": "AWAITING_OPERATOR_CONTEXT",
        "blocking_question_count": sum(item["blocking"] for item in QUESTIONS),
        "questions": [{**item, "answer": None, "decision_status": "OPEN"} for item in QUESTIONS],
    }
    summary = {
        "campaign_id": CAMPAIGN_ID,
        "as_of": AS_OF,
        "status": "RAW_PRESERVED_NORMALIZATION_PREVIEW_READY_CONTEXT_REQUIRED",
        "raw_artifacts_preserved": 1,
        "preview_records": len(preview),
        "open_context_questions": len(QUESTIONS),
        "archive_normalized_outputs_written": 0,
        "promotion_gate": "BLOCKED_PENDING_SEMANTIC_CONTEXT",
    }
    rendered = {
        "source-profile.json": dump_json(profile),
        "normalization-map.json": dump_json({"campaign_id": CAMPAIGN_ID, "schema_version": SCHEMA_VERSION, "columns": mapping}),
        "normalized-preview.jsonl": dump_jsonl(preview),
        "context-questions.json": dump_json(questions),
        "campaign-summary.json": dump_json(summary),
    }
    manifest_files = [
        {"path": RAW_REL.as_posix(), "role": "raw_source", "sha256": sha256(RAW_PATH), "records": len(rows)},
        {"path": PROVENANCE_REL.as_posix(), "role": "provenance", "sha256": sha256(ROOT / PROVENANCE_REL), "records": 1},
    ]
    for name, content in rendered.items():
        manifest_files.append({
            "path": f"operations/campaigns/{CAMPAIGN_ID}/{name}",
            "role": "campaign_derivative",
            "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
            "records": len(preview) if name == "normalized-preview.jsonl" else 1,
        })
    rendered["manifest.json"] = dump_json({
        "campaign_id": CAMPAIGN_ID,
        "schema_version": SCHEMA_VERSION,
        "files": sorted(manifest_files, key=lambda item: item["path"]),
    })
    return rendered


def write_outputs() -> None:
    for name, content in build().items():
        (CAMPAIGN_DIR / name).write_text(content, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    write_outputs()
    print(json.dumps({"campaign_id": CAMPAIGN_ID, "status": "built"}))
