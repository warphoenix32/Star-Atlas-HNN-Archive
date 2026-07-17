---
title: "Holosim"
knowledge_status: QUALIFIED
as_of: 2026-07-17
confidence: HIGH
page_risk_score: 4
page_risk_class: R2
canonical_entity: PRODUCT-HOLOSIM
aliases:
  - "HoloSim"
  - "Star Atlas Holosim"
first_seen: 2025-06-04
last_reviewed: 2026-07-17
source_priority:
  - A2
related_entities:
  - Fleet Command
  - Star Atlas
  - zATLAS
depends_on:
  - knowledge/gameplay/Product-Registry.md
supersedes: []
superseded_by: []
evidence_basis:
  - "archive/source-records/campaign-delta-official/SRC-OFF-4850F98FBD1F1541.md"
  - "archive/source-records/campaign-delta-official/SRC-OFF-5E3C884FBE440C33.md"
  - "archive/normalized/social-governance-semantic-enrichment/social-media/staratlas-posts.jsonl"
  - "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-6DC571942A250D14.json"
  - "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-D8337FA27E0A550A.json"
  - "knowledge/gameplay/Official-Current-State-Snapshot-2026-07-12.md"
known_limitations:
  - "The principal product page has no preserved publication or update date."
  - "Official current copy does not independently establish historical launch timing, user counts, economic outcomes, or delivery of every related Fleet Command feature."
research_gaps:
  - "Reconcile Holosim, Fleet Command, and later product terminology by build and environment."
review_after: 2027-01-17
---

# Holosim

Holosim is the official browser-based Star Atlas fleet simulation presented as a free-to-play entry point that does not require special hardware or a crypto wallet to begin. The reviewed records do not establish whether every mode or progression path is independent of owned assets.

## Identity and scope

The captured official product page describes Holosim as bringing Fleet Command-style strategic fleet gameplay to a browser, with fleet management, resource management, tactical combat, and an optional path toward the broader Star Atlas economy. These are official product claims, not independent measurements of depth, progression, or economic connection. [SRC-OFF-4850F98FBD1F1541](../../archive/source-records/campaign-delta-official/SRC-OFF-4850F98FBD1F1541.md)

Official support documentation separately states that no crypto wallet is required to start and that the game is designed for direct browser access. [SRC-OFF-5E3C884FBE440C33](../../archive/source-records/campaign-delta-official/SRC-OFF-5E3C884FBE440C33.md)

## Lifecycle and platform

The dated official social corpus establishes a build-specific public chronology:

- On 2025-06-04, `SRC-X-STARATLAS-1930380671010385958` announced that Holosim's test phase was live. A companion post, `SRC-X-STARATLAS-1930380673174647013`, described Holosim as a pre-mainnet feature-testing environment. This supports `TESTING`, not mainnet delivery.
- On 2025-08-20, `SRC-X-STARATLAS-1958322079927079252` stated that Season 1, Chapter 1 was live.
- On 2026-02-18, `SRC-X-STARATLAS-2024197285215948920` said the planned February 19 Chapter 2 launch was delayed. The missed date remains a delay record, not a release.
- Official Discord later rescheduled Chapter 2 for March 10 (`SA-DISCORD-ANN-6DC571942A250D14`). On 2026-03-10, official X and Discord records stated that Chapter 2 was live (`SRC-X-STARATLAS-2031445052623606253`; `SA-DISCORD-ANN-D8337FA27E0A550A`).

The official website snapshot captured on 2026-07-12 linked an active Holosim portal and described the product as available. Together, the dated records support `LIVE / UPDATED` for the browser surface as of the capture date. They do not establish that every adjacent Fleet Command roadmap feature was delivered. [Official current-state snapshot](Official-Current-State-Snapshot-2026-07-12.md)

## Related systems

Support records describe fleet management, crafting, attacks and safe conditions, crew transport, and the simulated `zATLAS` currency. Each mechanic should be treated as build- and date-specific. Holosim's relationship to Fleet Command is a product relationship stated by official copy; it is not evidence that the separate Fleet Command roadmap surface reached general release.

## Current state

As of 2026-07-17, the supported lifecycle state is `LIVE / UPDATED` for the browser surface. Feature status remains build-specific, and Holosim test availability is not evidence of mainnet deployment.

## Evidence references

- [Official Holosim page record](../../archive/source-records/campaign-delta-official/SRC-OFF-4850F98FBD1F1541.md)
- [Holosim support records](../../archive/source-records/campaign-delta-official/)
- [Official X normalized records](../../archive/normalized/social-governance-semantic-enrichment/social-media/staratlas-posts.jsonl)
- [Chapter 2 rescheduling record](../../archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-6DC571942A250D14.json)
- [Chapter 2 live record](../../archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-D8337FA27E0A550A.json)
- [Product Registry](Product-Registry.md)
