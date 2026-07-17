---
title: "Official Star Atlas X Account Profile"
knowledge_status: QUALIFIED
as_of: 2026-07-17
confidence: HIGH
page_risk_score: 4
page_risk_class: R2
canonical_entity: SOURCE-STAR-ATLAS-X
aliases:
  - "@staratlas"
  - "Official Star Atlas Twitter account"
first_seen: 2024-11-05
last_reviewed: 2026-07-17
source_priority:
  - A2
related_entities:
  - Star Atlas
  - ATMTA
depends_on:
  - archive/raw/social-governance-semantic-enrichment/social-media/sorsa_export_1784085327119.csv
  - archive/semantic/social-media/staratlas-posts-semantic.jsonl
supersedes: []
superseded_by: []
evidence_basis:
  - "operations/campaigns/social-governance-semantic-enrichment/campaign-summary.json"
  - "operations/campaigns/social-governance-semantic-enrichment/validation-report.json"
known_limitations:
  - "The supplied collection begins in November 2024 and is not presented as the account's complete lifetime history."
  - "Linked media binaries were not included in the source package."
  - "Retweets prove official resharing, not first-party authorship of the underlying claim."
research_gaps:
  - "Recover earlier account history and linked media."
  - "Reconcile high-value posts with newsroom, Discord, release, and governance records."
review_after: 2027-01-17
---

# Official Star Atlas X Account Profile

The preserved `@staratlas` collection is an official social-publication corpus useful for announcement discovery and dated public positioning. Original posts and retweets have different evidentiary meaning and remain explicitly separated.

## Preserved corpus

The validated collection contains 796 unique posts dated 2024-11-05 through 2026-07-14: 528 original account posts and 268 retweets. The precision review retained 28 promotion candidates, 26 timeline candidates, and 25 duplicate clusters. [Campaign summary](../../operations/campaigns/social-governance-semantic-enrichment/campaign-summary.json) [Validation report](../../operations/campaigns/social-governance-semantic-enrichment/validation-report.json)

This date range describes the supplied archive, not the full lifetime of the account. Absence of an earlier post from the collection is not evidence that it was never published.

The campaign summary still carries a stale overall `FAIL` field from an earlier packaging state, while the final validation report records `PASS`. This profile relies on the reconciled counts and final validator result and preserves the discrepancy for operational follow-up rather than silently rewriting campaign artifacts.

## Authority boundary

- An original `@staratlas` post is A2 evidence of what the official account stated on its publication date.
- A retweet is evidence that the official account reshared another source. It does not convert the underlying author's statement into a first-party Star Atlas claim.
- A post announcing a product, partnership, test, vote, or event does not establish delivery, outcome, result, or occurrence.
- A repeated marketing post is not independent corroboration of an earlier claim.
- Candidate confidence describes extraction quality rather than truth.

## Research use

The corpus is appropriate for locating first public mentions within the captured period, official terminology, announcement timing, corrections, and links to longer-form material. Material knowledge claims should cite the stable `SRC-X-STARATLAS-*` record and, where the claim concerns release or execution, a separate release, deployment, transaction, or operational source.

## Evidence references

- [Raw social export](../../archive/raw/social-governance-semantic-enrichment/social-media/sorsa_export_1784085327119.csv)
- [Semantic post records](../../archive/semantic/social-media/staratlas-posts-semantic.jsonl)
- [Promotion decisions](../../archive/semantic/social-media/promotion-candidate-decisions.jsonl)
- [Timeline decisions](../../archive/semantic/social-media/timeline-candidate-decisions.jsonl)
