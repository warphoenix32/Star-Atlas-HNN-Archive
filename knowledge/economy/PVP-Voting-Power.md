---
title: "POLIS Voting Power (PVP)"
knowledge_status: QUALIFIED
as_of: 2026-07-17
confidence: HIGH
page_risk_score: 4
page_risk_class: R2
canonical_entity: SYSTEM-POLIS-VOTING-POWER
aliases:
  - "PVP"
  - "POLIS Voting Power"
first_seen: 2022-07-31
last_reviewed: 2026-07-17
source_priority:
  - A1
  - A2
related_entities:
  - POLIS
  - Star Atlas DAO
  - POLIS Locker
depends_on:
  - knowledge/governance/Star-Atlas-DAO.md
  - knowledge/governance/PIP-Lifecycle-and-Legislative-Process.md
supersedes: []
superseded_by: []
evidence_basis:
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json"
  - "archive/source-records/campaign-delta-official/SRC-OFF-45B0F6196BC7966E.md"
  - "archive/source-records/campaign-delta-official/SRC-OFF-4312E3B0005E60A3.md"
  - "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-0D4A8B8F235B43B8.json"
known_limitations:
  - "The reviewed sources describe the inputs and decay behavior but do not provide a complete independently verified implementation formula."
  - "Current interface instructions and reward parameters may change."
research_gaps:
  - "Reconcile the exact deployed calculation with program code and version history."
  - "Document historical changes to lock multipliers, rewards, and proposal-activation requirements."
review_after: 2027-01-17
---

# POLIS Voting Power (PVP)

POLIS Voting Power, abbreviated PVP, is the voting-weight measure used by the Star Atlas DAO. It is obtained by locking POLIS, and its weight depends on both the amount locked and the lock duration.

## Governance role

PIP-1 defines the DAO as a system in which people lock and vote with POLIS and states that voting weight is based on the amount controlled and the duration of the lock. This establishes PVP as the formal weight used in PIP voting; it does not establish that every interface or reward parameter has remained unchanged since ratification. [PIP-1; SRC-PIP-01-BC8475E4](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json)

Official support documentation updated in December 2025 states that longer locks receive more PVP per POLIS and that locked POLIS cannot be withdrawn before the selected period ends. [SRC-OFF-45B0F6196BC7966E](../../archive/source-records/campaign-delta-official/SRC-OFF-45B0F6196BC7966E.md)

An official Discord announcement dated 2022-07-31 said PVP locking rewards would go live on 2022-08-02 and described ATMTA's intention to target approximately 65% of total PVP in the near term, initially using a five-year team lock. This is evidence of announced intent and timing, not proof that the target was continuously maintained or that the described locks remain current. [SA-DISCORD-ANN-0D4A8B8F235B43B8](../../archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-0D4A8B8F235B43B8.json)

## Technical behavior

The official DAO-program overview describes the Tribeca locked-voter component as calculating PVP from locked amount and duration, with voting power decaying linearly over time. It separately describes a snapshot component that records historical voting-power states. These descriptions are A2 technical documentation, not a substitute for code-level verification of the deployed version. [SRC-OFF-4312E3B0005E60A3](../../archive/source-records/campaign-delta-official/SRC-OFF-4312E3B0005E60A3.md)

## Decision boundaries

PVP measures voting weight. It does not by itself establish proposal passage, implementation, or execution. PIP-1 contains historical quorum language but does not specify a numeric quorum threshold in the captured text. The repository's reviewed completed-binary rule compares YES and NO PVP, while abstentions are preserved as non-decisive; elections use their separate ranked-choice mechanism. This distinction is preserved rather than silently replacing the charter language. See the [PIP Registry](../governance/PIP-Registry.md) and [PIP lifecycle](../governance/PIP-Lifecycle-and-Legislative-Process.md).

## Current state

As of 2026-07-17, the repository supports amount-and-duration weighting, lock-period restrictions, linear decay in official technical documentation, and use of PVP in governance. The exact live formula, deployed program version, and historical parameter changes remain open for code and on-chain reconciliation.
