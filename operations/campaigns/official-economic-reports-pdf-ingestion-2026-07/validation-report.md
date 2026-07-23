# Official Economic Reports PDF Validation

**Result:** `PASS`

## Checks

- **PASS - input_file_count:** {'manifest': 19, 'raw': 19}
- **PASS - raw_checksums:** []
- **PASS - pdf_signatures:** 19
- **PASS - q4_2026_duplicate:** q4-2026 is preserved as a duplicate of q4-2025
- **PASS - unique_document_count:** 18
- **PASS - paired_artifacts:** ['SRC-ECON-2022-Q2', 'SRC-ECON-2022-Q3', 'SRC-ECON-2022-Q4', 'SRC-ECON-2023-Q1', 'SRC-ECON-2023-Q2', 'SRC-ECON-2023-Q3', 'SRC-ECON-2023-Q4', 'SRC-ECON-2024-Q1', 'SRC-ECON-2024-Q2', 'SRC-ECON-2024-Q3', 'SRC-ECON-2024-Q4', 'SRC-ECON-2025-Q1', 'SRC-ECON-2025-Q2', 'SRC-ECON-2025-Q3', 'SRC-ECON-2025-Q4', 'SRC-ECON-2026-Q1', 'SRC-ECON-2026-Q2', 'SRC-ECON-PAPER-2021']
- **PASS - no_false_2026_q4_record:** ['SRC-ECON-2022-Q2', 'SRC-ECON-2022-Q3', 'SRC-ECON-2022-Q4', 'SRC-ECON-2023-Q1', 'SRC-ECON-2023-Q2', 'SRC-ECON-2023-Q3', 'SRC-ECON-2023-Q4', 'SRC-ECON-2024-Q1', 'SRC-ECON-2024-Q2', 'SRC-ECON-2024-Q3', 'SRC-ECON-2024-Q4', 'SRC-ECON-2025-Q1', 'SRC-ECON-2025-Q2', 'SRC-ECON-2025-Q3', 'SRC-ECON-2025-Q4', 'SRC-ECON-2026-Q1', 'SRC-ECON-2026-Q2', 'SRC-ECON-PAPER-2021']
- **PASS - quarterly_series_count:** ['SRC-ECON-2022-Q2', 'SRC-ECON-2022-Q3', 'SRC-ECON-2022-Q4', 'SRC-ECON-2023-Q1', 'SRC-ECON-2023-Q2', 'SRC-ECON-2023-Q3', 'SRC-ECON-2023-Q4', 'SRC-ECON-2024-Q1', 'SRC-ECON-2024-Q2', 'SRC-ECON-2024-Q3', 'SRC-ECON-2024-Q4', 'SRC-ECON-2025-Q1', 'SRC-ECON-2025-Q2', 'SRC-ECON-2025-Q3', 'SRC-ECON-2025-Q4', 'SRC-ECON-2026-Q1', 'SRC-ECON-2026-Q2', 'SRC-ECON-PAPER-2021']
- **PASS - economics_paper_present:** ['SRC-ECON-2022-Q2', 'SRC-ECON-2022-Q3', 'SRC-ECON-2022-Q4', 'SRC-ECON-2023-Q1', 'SRC-ECON-2023-Q2', 'SRC-ECON-2023-Q3', 'SRC-ECON-2023-Q4', 'SRC-ECON-2024-Q1', 'SRC-ECON-2024-Q2', 'SRC-ECON-2024-Q3', 'SRC-ECON-2024-Q4', 'SRC-ECON-2025-Q1', 'SRC-ECON-2025-Q2', 'SRC-ECON-2025-Q3', 'SRC-ECON-2025-Q4', 'SRC-ECON-2026-Q1', 'SRC-ECON-2026-Q2', 'SRC-ECON-PAPER-2021']
- **PASS - json_parses:** []
- **PASS - page_boundaries_reconcile:** {'errors': [], 'pages': 294}
- **PASS - duplicate_ledger:** [{'disposition': 'EXACT_DUPLICATE_MISLABELED_PACKAGE_MEMBER', 'duplicate_of_filename': 'q4-2025.pdf', 'duplicate_of_source_id': 'SRC-ECON-2025-Q4', 'evidence': ['Byte-identical SHA-256', 'Embedded PDF title states Q4 2025', 'First-page title states Q4 2025'], 'filename': 'q4-2026.pdf', 'manual_review_required': True, 'preserved_raw': True, 'sha256': 'f14f6dbb338f1b074abc396b74a40aaaa8238d58f0db2785ae2f6cca67f88f8c', 'source_record_created': False}]
- **PASS - summary_reconciles:** {'as_of': '2026-07-22', 'body_acquisition': 'OPERATOR_PROVIDED_PDF_PACKAGE', 'campaign_id': 'official-economic-reports-pdf-ingestion-2026-07', 'economics_papers': 1, 'exact_duplicates': 1, 'extractions': 18, 'input_package_files': 19, 'knowledge_promotion': 'NOT_PERFORMED', 'manual_review_queue': ['q4-2026.pdf'], 'normalized_records': 18, 'quarterly_coverage': {'first': '2022 Q2', 'last': '2026 Q2'}, 'quarterly_reports': 17, 'schema_version': '1.0.0', 'semantic_enrichment': 'NOT_PERFORMED', 'source_records': 18, 'status': 'INGESTION_COMPLETE_MANUAL_DUPLICATE_REVIEW_OPEN', 'total_extracted_characters': 390574, 'total_unique_pages': 294, 'unique_documents': 18, 'urls_fetched_for_body': False, 'valid_pdf_files': 19, 'visual_validation_status': 'PASS_REPRESENTATIVE_RENDER_REVIEW'}
- **PASS - visual_validation:** {'campaign_id': 'official-economic-reports-pdf-ingestion-2026-07', 'result': 'PASS', 'renderer': 'Poppler pdftoppm', 'first_pages_rendered': 19, 'representative_pages_inspected': ['q2-2022.pdf page 1', 'q1-2023.pdf page 1', 'q3-2024.pdf page 1', 'q2-2026.pdf page 1', 'star-atlas-economics-paper.pdf page 1', 'q2-2022.pdf page 5', 'q1-2023.pdf page 4', 'star-atlas-economics-paper.pdf page 10'], 'findings': ['Representative covers, body text, tables, and styled economics-paper pages rendered without clipping, overlap, missing glyphs, or corruption.', 'q4-2025.pdf and q4-2026.pdf produced identical first-page renders, consistent with their identical binary checksums.', 'Charts and table geometry remain authoritative in the raw PDF rather than the extracted Markdown.'], 'as_of': '2026-07-22'}
- **PASS - manifest_checksums:** []
- **PASS - schema_v2_1_package:** {'campaign_id': 'official-economic-reports-pdf-ingestion-2026-07', 'generated_as_of': '2026-07-22', 'package_id': 'INGEST-OFFICIAL-ECONOMIC-REPORTS-001', 'repository_schema': '2.1'}

## Manual review

- `q4-2026.pdf` is an exact duplicate of the internally identified Q4 2025 report; it is preserved but not promoted to a Source Record.

## Limitations

- Validation proves archival integrity and extraction reconciliation, not the independent accuracy of publisher-reported economic claims.
- Charts and table geometry remain authoritative only in the raw PDFs.
- No on-chain verification or semantic promotion was performed.
