---
title: "Star Atlas Product Registry"
knowledge_status: QUALIFIED
as_of: 2026-07-17
confidence: MEDIUM
page_risk_score: 5
page_risk_class: R2
evidence_basis:
  - "archive/semantic/atlas-brew/segment-index.json"
  - "archive/source-records/campaign-delta-official/"
  - "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-A37A8B7B245E7776.json"
  - "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-CCF4600A4C08F697.json"
  - "archive/normalized/social-governance-semantic-enrichment/social-media/staratlas-posts.jsonl"
  - "knowledge/gameplay/Official-Current-State-Snapshot-2026-07-12.md"
known_limitations:
  - "Current-state statements are date-bound."
  - "Absence of evidence is not evidence of non-occurrence."
research_gaps:
  - "Independent execution evidence remains incomplete where explicitly noted."
review_after: 2027-01-15
---

# Star Atlas Product Registry
This registry is an evidence-qualified map of major Star Atlas product surfaces. Lifecycle labels are current only as of 2026-07-17 and do not convert roadmap language into delivery.

## Registry

| Product | Entity ID | Supported lifecycle | Evidence note |
|---|---|---|---|
| PLAY | PRODUCT-PLAY | LIVE | Official account and asset hub in the dated current-state capture. |
| [SCORE / Faction Fleet](SCORE-and-Faction-Fleet.md) | PRODUCT-SCORE | HISTORICAL / DEPRECATED | Earlier fleet-staking surface; community chronology reports emissions ended in 2024. |
| [SAGE / SAGE Labs](SAGE.md) | PRODUCT-SAGE | LIVE / UPDATED | Official records establish SAGE Labs live on 2023-09-21 and Starbased live on 2024-04-04; other phases remain build-specific. |
| [UE5 / Showroom](UE5-Showroom.md) | PRODUCT-UE5 | TESTING / UPDATED | Early-access client with build-specific capabilities; planned features are not assumed delivered. |
| Fleet Command | PRODUCT-FLEET-COMMAND | IN_DEVELOPMENT | Captured official page describes development; no general release is asserted. |
| [Holosim](Holosim.md) | PRODUCT-HOLOSIM | LIVE / UPDATED | Official records establish a live public test on 2025-06-04, Chapter 1 on 2025-08-20, and Chapter 2 on 2026-03-10 after a delay. |
| C4 / C4 PTR | unresolved | TESTING | June 2026 support records establish PTR mining, not a mainnet or general release. |
| [Galactic Marketplace](Galactic-Marketplace.md) | PRODUCT-MARKETPLACE | LIVE | Official product surfaces describe asset trading. |
| DAO portal | PRODUCT-DAO-PORTAL | LIVE | Proposal voting and POLIS governance surface. |
| Star Atlas Build | PRODUCT-BUILD | LIVE | Builder documentation and developer-resource hub. |

## Lifecycle rules

The controlled states are FIRST_MENTION, PLANNED, IN_DEVELOPMENT, TESTING, LIVE, UPDATED, DEGRADED, RESOLVED, SUPERSEDED, DEPRECATED, CANCELED, and UNKNOWN. A state is assigned to a named product or feature and a dated evidence record. Announcement, test access, public release, and delivery of all promised features remain separate.

## Evidence references

- [Official current-state snapshot](Official-Current-State-Snapshot-2026-07-12.md)
- [Atlas Brew semantic segments](../../archive/semantic/atlas-brew/segment-index.json)
- [Official source records](../../archive/source-records/campaign-delta-official/)
