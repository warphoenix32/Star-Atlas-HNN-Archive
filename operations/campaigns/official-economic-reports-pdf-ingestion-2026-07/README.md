# Official Economic Reports PDF Ingestion

This campaign ingests the operator-provided `Star Atlas Econ Reports.zip` package. The supplied PDFs are the preserved document bodies; the previously discovered 17 official URLs remain canonical identifiers and cross-references only.

## Scope

- 19 supplied PDF files
- 18 unique documents
- 17 quarterly reports from 2022 Q2 through 2026 Q2
- 1 foundational economics paper
- 1 exact duplicate/mislabeled package member (`q4-2026.pdf`, identical to Q4 2025)

## Commands

Initial acquisition from the operator package:

```text
python build_campaign.py --input-zip "C:\path\to\Star Atlas Econ Reports.zip"
```

Deterministic regeneration from committed raw PDFs and the frozen package manifest:

```text
python build_campaign.py
python validate_campaign.py
```

The build step requires `pypdf`; validation uses only the Python standard library.

## Evidence boundary

The campaign preserves raw PDFs, page-boundary text, PDF metadata, provenance, Source Records, ingestion extractions, duplicate disposition, and checksums. It does not promote claims, construct time series, infer metric continuity, independently verify reported figures, or perform on-chain verification.

URLs were not fetched for report bodies. The original URLs remain useful for identity and discovery, but the supplied PDFs are the acquisition source.

## Duplicate adjudication

`q4-2026.pdf` is byte-identical to `q4-2025.pdf`; its embedded PDF title and first page both identify Q4 2025. Both filenames are preserved as supplied. Only the Q4 2025 Source Record is generated, and the duplicate remains visible in `duplicate-ledger.json` for human review.
