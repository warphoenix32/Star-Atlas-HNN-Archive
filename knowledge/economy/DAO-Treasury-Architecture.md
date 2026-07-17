---
title: "Star Atlas DAO Treasury Architecture"
knowledge_status: QUALIFIED
as_of: 2026-07-17
confidence: HIGH
page_risk_score: 6
page_risk_class: R2
canonical_entity: SYSTEM-STAR-ATLAS-DAO-TREASURY
aliases:
  - "DAO Treasury"
  - "Star Atlas treasury"
first_seen: 2024-07-08
last_reviewed: 2026-07-17
source_priority:
  - A1
  - A2
  - A3
related_entities:
  - Star Atlas DAO
  - Star Atlas Foundation
  - Star Atlas Council
  - Ecosystem Fund
depends_on:
  - knowledge/governance/Ecosystem-Fund.md
  - knowledge/governance/Governance-Implementation-and-Evidence-States.md
supersedes: []
superseded_by: []
evidence_basis:
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json"
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-02-1E2D7066.json"
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-23-0ECF2928.json"
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-33-397FEE39.json"
  - "archive/source-records/governance/council-pip-tracker/SA-COUNCIL-TRACKER-D1DADF7EB8437119.json"
  - "operations/campaigns/social-governance-semantic-enrichment/input-council-tracker/council-pip-tracker-semantic-records.jsonl"
  - "archive/source-records/campaign-delta-official/SRC-OFF-4312E3B0005E60A3.md"
known_limitations:
  - "This page describes the captured governance design, not current balances, signers, or independently verified control of every account."
  - "Council tracker payment and milestone fields remain attributed operational assessments."
research_gaps:
  - "Verify current multisig signers, upgrade authorities, account ownership, and transaction history on-chain."
  - "Reconcile every Council-reported payment to a transaction and every milestone to a deliverable."
review_after: 2027-01-17
---

# Star Atlas DAO Treasury Architecture

The Star Atlas DAO treasury is the set of governed accounts, programs, and institutional responsibilities used to authorize and execute DAO financial actions. A proposal can authorize spending without proving that a transfer occurred or that funded work was completed.

## Constitutional framework

PIP-1 identifies a DAO Treasury account among the programs and accounts comprising the governance system and requires on-chain DAO approval before treasury disbursements. It assigns successful PIPs to the Star Atlas Foundation for implementation. [PIP-1; SRC-PIP-01-BC8475E4](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json)

PIP-2 describes the Foundation as the DAO's legal and operational agent and supports administrative, contracting, multisig, and implementation functions within the proposal's limits. Those institutional powers do not remove the requirement to distinguish authorization from execution. [PIP-2; SRC-PIP-02-1E2D7066](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-02-1E2D7066.json)

## On-chain execution layer

Official support documentation describes a Goki smart wallet as an m-of-n multisig capable of executing Solana transactions and a Tribeca governor program that manages proposal lifecycle and queues approved actions for execution. This is official technical description as of its 2025 update; current deployment, signers, and upgrade authority require direct verification. [SRC-OFF-4312E3B0005E60A3](../../archive/source-records/campaign-delta-official/SRC-OFF-4312E3B0005E60A3.md)

## Ecosystem Fund relationship

PIP-23 is the controlling captured Ecosystem Fund framework. It specifies the DAO Treasury and Ecosystem Fund wallets, allocation and refill formulas, the USDC reserve threshold, USDC-denominated requests, ATLAS payments, and Council stewardship boundaries. The proposal includes transaction references for prior refills, but each transaction and later payment still requires claim-specific reconciliation. [PIP-23; SRC-PIP-23-0ECF2928](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-23-0ECF2928.json)

The Ecosystem Fund is a bounded treasury suballocation, not the only route by which POLIS holders may authorize a treasury obligation. PIP-33 expressly presents its reimbursement request as a direct, extraordinary DAO Treasury measure outside the standard Ecosystem Fund cap. The Council tracker semantic record also marks the proposal as not using the Ecosystem Fund. The semantic registry's contrary `STAR_ATLAS_ECOSYSTEM_FUND` funding-source label is therefore not promoted into knowledge. [PIP-33; SRC-PIP-33-397FEE39](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-33-397FEE39.json) [Council tracker semantic records](../../operations/campaigns/social-governance-semantic-enrichment/input-council-tracker/council-pip-tracker-semantic-records.jsonl)

## Evidence states

The repository uses separate states for requested funding, passage, implementation pending, reported payment, partial implementation, completion, termination, cancellation, withdrawal, and independent verification. Council tracker fields use:

```yaml
assessment_source: STAR_ATLAS_COUNCIL_TRACKER
assessment_type: COUNCIL_AUTHORED_OPERATIONAL_ASSESSMENT
independent_verification_status: UNKNOWN
```

## Current state

As of 2026-07-17, the archive supports the institutional and program architecture above. It does not establish live balances, current signers, or transaction-level verification of every disbursement. See [PIP-33 ATMTA Historic Expense Reimbursement](../governance/PIP-33-ATMTA-Historic-Expense-Reimbursement.md) for the direct-treasury case and its unresolved payment state.
