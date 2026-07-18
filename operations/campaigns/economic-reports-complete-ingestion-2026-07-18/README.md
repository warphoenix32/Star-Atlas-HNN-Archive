# Economic Reports Complete Ingestion Campaign

## Objective

Ingest the complete official Star Atlas quarterly economic-report series currently published by the DAO, covering 2022 Q2 through 2026 Q2.

## Current campaign state

- Official index reviewed: `https://govern.staratlas.com/economy/economic-reports`
- Reports identified: 17
- Coverage: 2022 Q2 through 2026 Q2
- Canonical PDF URLs recorded: 17/17
- Page counts recorded: 17/17
- Source registry entries created: 17/17
- Automated text parsing available: 14/17
- Parser failures requiring render/OCR review: 2022 Q3, 2022 Q4, 2023 Q1
- Semantic report review: pending
- Metric extraction: pending
- Methodology reconciliation: pending
- Raw PDF binary preservation and SHA-256 hashing: blocked in the current connector runtime

## Preservation boundary

The official PDFs were resolved and read through the public report index, but the active GitHub connector does not accept a remote URL as a binary repository file, and the container download path could not resolve the Google Storage host. The branch therefore records each canonical PDF URL and ingestion status without claiming that the binary has been preserved or hashed.

No source record may be treated as fully archived until it contains:

1. the original PDF binary;
2. SHA-256 checksum;
3. retrieval timestamp;
4. page count and document metadata;
5. extracted text with page boundaries;
6. visual validation of tables and charts;
7. report-level semantic review;
8. methodology and metric dictionary reconciliation.

## Required output per report

- stable source identifier;
- canonical URL and retrieval metadata;
- raw PDF and checksum;
- title, period, authors, publication date, and page count;
- page-preserving text extraction;
- table and chart inventory;
- metric definitions and units;
- measured/modelled/estimated/forward-looking classification;
- headline findings with page citations;
- methodology changes from the preceding report;
- conflicts, revisions, appendices, and known limitations.

## Next execution steps

1. Acquire the 17 PDF binaries through a network-capable Yggy or local runner.
2. Hash and store them under `archive/raw/economic-reports/`.
3. Run render-first extraction and visual validation.
4. OCR the three parser-failure reports.
5. Generate one source record and one semantic report record per quarter.
6. Build a metric dictionary before constructing longitudinal series.
7. Reconcile the duplicated 2025 Q2 archive presentation at the page and binary level.
8. Update the Economic Report Catalog only after complete preservation and semantic review.

## Evidence rule

Until full ingestion is complete, economic-report claims remain report-attributed A2 evidence. Figures must stay bound to their source quarter, definition, unit, methodology, and measurement window. Similar metric names must not be treated as continuous time series without reconciliation.
