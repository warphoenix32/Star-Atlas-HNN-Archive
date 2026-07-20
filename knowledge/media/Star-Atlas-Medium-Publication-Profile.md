---
title: "Star Atlas Medium Publication Profile"
seo_title: "Official Star Atlas Medium Archive and Publication History"
seo_description: "A source-critical profile of the official Star Atlas Medium corpus: 173 confirmed articles, 2021–2025 coverage, retrieval provenance, deferred discovery leads, and completeness limits."
knowledge_status: QUALIFIED
as_of: 2026-07-20
confidence: HIGH
page_risk_score: 5
page_risk_class: R2
canonical_entity: SOURCE-STAR-ATLAS-MEDIUM
aliases:
  - "Star Atlas Medium"
  - "Official Star Atlas Medium publication"
first_seen: 2021-01-15
last_reviewed: 2026-07-20
source_priority:
  - A2
related_entities:
  - Star Atlas
  - ATMTA
depends_on:
  - archive/campaign-summaries/star-atlas-medium-ingestion-2026-07/campaign-summary.json
  - archive/source-records/medium/star-atlas/
supersedes: []
superseded_by: []
evidence_basis:
  - "archive/campaign-summaries/star-atlas-medium-ingestion-2026-07/campaign-summary.json"
  - "operations/campaigns/star-atlas-medium-ingestion-2026-07/campaign-manifest.json"
  - "operations/campaigns/star-atlas-medium-ingestion-2026-07/manual-review-adjudication.json"
known_limitations:
  - "Ingestion is complete for 173 confirmed included articles, but publication-level discovery remains incomplete."
  - "Fifty-one discovery leads remain explicitly deferred after review."
  - "Current live text may contain edits made after an article's original publication."
  - "Article media is URL-referenced rather than downloaded."
research_gaps:
  - "Resolve deferred shortlinks, malformed URLs, inaccessible records, deleted stories, and unindexed publication pages."
  - "Reconcile article-level revisions and recover historical snapshots where current text may have changed."
review_after: 2027-01-20
---

# Star Atlas Medium Publication Profile

The official Star Atlas Medium publication is one of the archive's most substantial first-party written corpora. The repository now preserves **173 confirmed articles** published from January 2021 through October 2025. All 173 included records were retrieved and extracted successfully. That achievement is complete ingestion of the confirmed set—not proof that every article ever published by Star Atlas on Medium has been discovered.

## What the campaign preserved

The publication-native campaign separated URL discovery from retrieval. It discovered 686 candidate URLs, classified 173 as included, excluded 462, and explicitly deferred 51 after adjudicating 329 manual-review candidates. Every included article has a stable Source ID, raw capture, normalized record, Source Record, ingestion package, checksums, dates, author and publisher fields, links, and retrieval provenance.

| Retrieval path | Articles | Meaning |
|---|---:|---|
| Live direct HTML | 134 | Article body recovered from current public HTML |
| Live browser DOM | 1 | Browser rendering was required to recover the article |
| RSS content | 1 | Feed content was accepted only after completeness checks |
| Web-archive snapshot | 37 | An archived snapshot preserved an unavailable or historical page |

Extraction confidence is `HIGH` for 172 articles and `MEDIUM` for one. Media binaries were intentionally not downloaded; 239 article-body media references remain URL-preserved with placement metadata.

## Coverage by year

| Year | Confirmed articles ingested |
|---:|---:|
| 2020 | 0 |
| 2021 | 50 |
| 2022 | 67 |
| 2023 | 32 |
| 2024 | 12 |
| 2025 | 12 |
| 2026 | 0 |

The 2020 publication and profile surfaces were searched, but no 2020 article belonging to the official Star Atlas publication was confirmed or included. This is a coverage finding, not proof that no such article ever existed.

## Why discovery remains incomplete

Medium's year archives can expose hydration shells or incomplete rendered results. RSS covers only a recent subset, and available sitemaps are not exhaustive. Deleted or unindexed stories may remain undiscoverable when no repository link or web-archive record survives. Shortlinks and truncated historical URLs can also lose the post ID needed for deterministic identity.

The 51 deferred leads remain visible in the manual-review queue. They were not counted as failures or silently excluded. Each record states the deferral reason, next action, and artifact required to decide publication membership.

## Publisher and author identity

An article belongs to the official Star Atlas publication only when captured page evidence establishes that membership. The individual author remains a separate field. A Star Atlas profile URL and publication URL can point to the same Medium post ID; that is one article with multiple observed URLs, not two sources.

Official sharing alone does not transform a partner or community article into Star Atlas-authored content. Reposts, responses, account activity, author profiles, and landing pages were excluded and ledgered rather than treated as publications.

## Authority and citation boundary

An official article is strong evidence of what Star Atlas published, the terminology it used, and the timing of that publication. It does not automatically prove delivery, execution, economic accuracy, partnership outcomes, or event occurrence.

- An announcement is not a release.
- A roadmap date is not a delivery date.
- A governance proposal is not passage or implementation.
- A current article is not proof that identical wording appeared on the original date.
- Repetition across Medium, Discord, and X may show dissemination without independent corroboration.

When an article quotes, summarizes, or republishes another source, its source lineage should preserve that original creator and relationship.

## Research use

Researchers should cite the article-level Source Record rather than this profile. A durable citation includes the `SRC-MEDIUM-STARATLAS-*` identifier, canonical and observed URLs, author, publisher, original and normalized dates, retrieval tier, capture timestamp, and checksum. Historical-text comparisons should prefer archived snapshots or explicit revision evidence.

## Evidence references

- [Campaign summary](../../archive/campaign-summaries/star-atlas-medium-ingestion-2026-07/campaign-summary.md)
- [Article Source Records](../../archive/source-records/medium/star-atlas/)
- [Campaign manifest](../../operations/campaigns/star-atlas-medium-ingestion-2026-07/campaign-manifest.json)
- [Deferred review queue](../../operations/campaigns/star-atlas-medium-ingestion-2026-07/manual-review-queue.json)

## Review status

`QUALIFIED`. The 173 confirmed included articles are completely ingested and validated. The historical publication inventory remains incomplete until deferred and undiscovered material can be resolved.
