# Starbased Ship States Ingestion 2026-07

This campaign preserves and profiles the operator-submitted `rydn_starbased_ships_20260718.csv` dataset and prepares a deterministic normalization preview. It does not yet publish a derivative under `archive/normalized/` because several source semantics require human clarification.

## Campaign boundary

- The original CSV is preserved byte-for-byte at `archive/raw/starbased-ship-states/rydn_starbased_ships_20260718.csv`.
- Custody and checksum metadata live at `archive/provenance/starbased-ship-states/rydn_starbased_ships_20260718.json`.
- `normalized-preview.jsonl` is a typed staging derivative inside this campaign, not canonical game data.
- Source labels and values are never silently corrected. Canonical names, game-module applicability, and derived-metric semantics remain pending where the CSV does not establish them.
- No files under `knowledge/`, `graph/`, `publication/`, or `archive/normalized/` are changed by this phase.

## Current source profile

The CSV contains 63 unique ship rows and 26 columns. The first column has a blank header and contains unique ship codes. The remaining columns contain ship names, specialization labels, capacity and consumption values, movement values, mining and scanning values, crew/passenger counts, and respawn timing.

All cells are populated, all metric cells parse as numbers, and there are no duplicate complete rows, ship codes, or ship names. Thirteen observed specialization labels are retained as supplied.

Three column pairs contain identical values in all 63 rows:

- `CargoCapacity` and `USDC /Cargo Capacity`;
- `Mining Rate[Resource/sec]` and `USDC /Mining Rate`;
- `Fuel /AU Warp` and `Cargo /Warp Fuel`.

The campaign does not decide whether these equalities are intentional, formula/export artifacts, or evidence of missing price inputs. That question blocks promotion into the normalized archive.

## Reproduction

Run from the repository root:

```powershell
python operations/campaigns/starbased-ship-states-ingestion-2026-07/build_campaign.py
python operations/campaigns/starbased-ship-states-ingestion-2026-07/validate_campaign.py
```

## Outputs

- `source-profile.json`: structural and data-quality profile of the preserved CSV.
- `normalization-map.json`: exact source-header mapping, normalized names, data types, units, and semantic status.
- `normalized-preview.jsonl`: one typed, evidence-linked staging record per ship.
- `context-questions.json`: human questions that must be answered before archive normalization.
- `manifest.json`: checksums and record counts for the campaign inputs and outputs.
- `campaign-summary.json`: machine-readable campaign status.
- `validation-report.json`: deterministic validation results.

## Promotion gate

Promotion to `archive/normalized/starbased-ship-states/` requires resolution of the source-authority, ship-code, game-module, metric-definition, marketplace-link, unit/scale, and name-canonicalization questions. Until then, every preview record is `SEMANTIC_REVIEW_REQUIRED`.
