---
title: "Official Discord Announcements Profile"
knowledge_status: QUALIFIED
as_of: 2026-07-17
confidence: HIGH
page_risk_score: 5
page_risk_class: R2
canonical_entity: SOURCE-STAR-ATLAS-DISCORD-ANNOUNCEMENTS
aliases:
  - "Star Atlas Discord announcements"
  - "Official Star Atlas announcement channel export"
first_seen: 2021-03-16
last_reviewed: 2026-07-17
source_priority:
  - A2
  - C1
related_entities:
  - Star Atlas
  - ATMTA
depends_on:
  - archive/raw/discord-announcements/star-atlas-discord-announcements.md
  - archive/semantic/discord-announcements/announcement-semantic-records.jsonl
supersedes: []
superseded_by: []
evidence_basis:
  - "operations/campaigns/discord-announcements-semantic-enrichment/campaign-summary.json"
  - "operations/campaigns/discord-announcements-semantic-enrichment/validation-report.json"
  - "operations/campaigns/discord-announcements-semantic-enrichment/review-correction-status.json"
known_limitations:
  - "The export header states that collection was incomplete at acquisition, although it is the total available export supplied to the repository."
  - "Author grouping was inferred from the export structure and is not independently verified."
  - "Attachment binaries were not supplied."
research_gaps:
  - "Reconstruct stricter event sequences using shared event identifiers and bounded temporal adjacency."
  - "Corroborate promotion candidates claim by claim against independent source records."
review_after: 2027-01-17
---

# Official Discord Announcements Profile

The official Star Atlas Discord announcement export is a high-value chronological record of what appeared in the supplied announcement channel history. It is strongest as evidence of publication timing and channel text. It is not an exhaustive record of all Star Atlas communications, and its inferred author labels must not be treated as verified personal authorship.

## Preserved corpus

The validated corpus contains 1,071 unique announcements covering 2021-03-16 through 2026-07-12. Every message has a stable source record and a semantic decision record. The enrichment layer retains 148 single-source promotion candidates, 136 timeline candidates, 30 duplicate clusters, 31 security-alert records, and 70 incident-or-resolution records. [Campaign summary](../../operations/campaigns/discord-announcements-semantic-enrichment/campaign-summary.json) [Campaign validation](../../operations/campaigns/discord-announcements-semantic-enrichment/validation-report.json)

The user designates the supplied export as the total available announcements corpus. The export itself says `Collection complete: no`; therefore the archive can be described as the complete supplied or available export, not as proof that no announcement is missing.

## Review corrections

The first deterministic pass grouped 24 broad event sequences and placed 148 Discord candidates in a cross-source promotion queue. Curator review withdrew both overstatements. The corrected record contains zero accepted event sequences pending stricter identity-based clustering and zero cross-source promotion records pending an explicit second source. The 148 Discord-only candidates remain available for review. [Review corrections](../../operations/campaigns/discord-announcements-semantic-enrichment/REVIEW-CORRECTIONS.md) [Correction status](../../operations/campaigns/discord-announcements-semantic-enrichment/review-correction-status.json)

## Authority and attribution

- Preserved announcement text may be treated as A2 evidence of what the official channel published when channel provenance is clear.
- The export's grouped author name is C1 unless independently reconciled to another record.
- A linked article, video, or attachment is not preserved merely because its URL appears in a message.
- An announcement is not a release; a security alert is not a resolution; a vote notice is not a vote result; and an event notice is not evidence that the event occurred.
- Candidate confidence measures extraction quality, not factual truth.

## Recommended research use

Use the corpus for dated announcement discovery, incident chronology, corrections, release and test leads, governance notices, and links to underlying publications. Before promoting a material claim, follow the source ID into the message record and reconcile the claim with the linked or later evidence when practical.

## Evidence references

- [Raw supplied export](../../archive/raw/discord-announcements/star-atlas-discord-announcements.md)
- [Semantic announcement records](../../archive/semantic/discord-announcements/announcement-semantic-records.jsonl)
- [Promotion decisions](../../archive/semantic/discord-announcements/promotion-candidate-decisions.jsonl)
- [Timeline decisions](../../archive/semantic/discord-announcements/timeline-candidate-decisions.jsonl)
