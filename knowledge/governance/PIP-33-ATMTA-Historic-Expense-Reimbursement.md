---
title: "PIP-33 — ATMTA Historic Expense Reimbursement"
knowledge_status: PROVISIONAL
as_of: 2026-07-17
confidence: MEDIUM
page_risk_score: 7
page_risk_class: R3
canonical_entity: GOVERNANCE-PIP-33
aliases:
  - "PIP-33"
  - "ATMTA Historic Expense Reimbursement"
first_seen: 2026-06-24
last_reviewed: 2026-07-17
source_priority:
  - A1
  - A2
  - A3
related_entities:
  - ATMTA
  - Michael Wagner
  - Star Atlas DAO
  - DAO Treasury
depends_on:
  - knowledge/governance/PIP-Registry.md
  - knowledge/economy/DAO-Treasury-Architecture.md
supersedes: []
superseded_by: []
evidence_basis:
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-33-397FEE39.json"
  - "archive/source-records/governance/council-pip-tracker/SA-COUNCIL-TRACKER-D1DADF7EB8437119.json"
  - "operations/campaigns/social-governance-semantic-enrichment/input-council-tracker/council-pip-tracker-semantic-records.jsonl"
  - "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-AA9B47413B9C587D.json"
known_limitations:
  - "The expense, tax, invoice, runway, and supporting-document statements originate in the proposal and its author-provided appendices and are not independently audited by this repository."
  - "The Council tracker contains no populated payment fields for this proposal."
  - "Passage authorizes the proposal but does not prove either scheduled tranche was paid."
research_gaps:
  - "Reconcile both scheduled tranches to primary transactions and Foundation execution records."
  - "Independently review the cited tax calculation, Walkers services, Leeward invoice, reserve condition, and conflict-management process."
review_after: 2026-10-17
---

# PIP-33 — ATMTA Historic Expense Reimbursement

PIP-33 is a passed proposal authorizing a historic-expense reimbursement to ATMTA. It is an extraordinary direct DAO Treasury measure, not an Ecosystem Fund disbursement. Its passage, scheduled payment terms, and actual payment state remain separate.

## Proposal and disclosed conflict

The official proposal was authored by Michael Wagner on behalf of ATMTA and requested $469,513.53. It identified ATMTA as the sole beneficiary and disclosed the author's conflict of interest. The request comprised $318,092.47 for a tax obligation the proposal attributed to 2021 DAO R4-sale income of $1,533,271.51, $142,779.80 for Walkers services, and $8,641.26 for a Leeward invoice. Those descriptions and appendices are author-provided evidence; this repository does not independently validate the expenses. [SRC-PIP-33-397FEE39](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-33-397FEE39.json)

## Funding channel and schedule

The proposal describes itself as a `DAO Treasury` measure that exceeds the ordinary Ecosystem Fund limit. It specifies a 75% USDC and 25% ATLAS mix and two scheduled tranches of $234,756.76, with the second due 180 days later subject to the proposal's reserve protection. These are approved terms, not evidence that either transfer occurred.

## Vote result

The captured portal record contains 170,240,400.0117 YES PVP, 24,857,540.3494 NO PVP, and 83,860,459.5491 abstaining PVP. Under the reviewed binary rule, the result is `PASSED`. An official Discord acknowledgment on 2026-07-12 also described the proposal as passed and characterized participation as the highest PVP participation since DAO inception. The vote totals support the comparison within the captured PIP-1–33 corpus; the broader historical characterization remains an attributed statement. [SA-DISCORD-ANN-AA9B47413B9C587D](../../archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-AA9B47413B9C587D.json)

## Implementation state

As of 2026-07-17, the Council tracker semantic record has no populated payment fields and retains `independent_verification_status: UNKNOWN`. The supported state is therefore `IMPLEMENTATION_PENDING` / `PAYMENT_UNVERIFIED`, not paid or completed. [Council tracker semantic records](../../operations/campaigns/social-governance-semantic-enrichment/input-council-tracker/council-pip-tracker-semantic-records.jsonl)

## Evidence interpretation

- Proposal publication establishes the request and disclosed terms.
- Vote totals establish the reviewed passing result.
- The scheduled tranches establish intended timing, not transfer.
- Proposed Council or Foundation verification controls do not prove that verification occurred.
- No statement here independently validates the underlying expense claims.
