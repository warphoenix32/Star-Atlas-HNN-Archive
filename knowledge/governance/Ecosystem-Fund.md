---
title: "Star Atlas Ecosystem Fund"
knowledge_status: QUALIFIED
as_of: 2026-07-17
confidence: MEDIUM
page_risk_score: 6
page_risk_class: R2
evidence_basis:
  - "archive/semantic/governance/pip-registry-semantic.json"
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-23-0ECF2928.json"
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-33-397FEE39.json"
  - "operations/campaigns/social-governance-semantic-enrichment/input-council-tracker/council-pip-tracker-semantic-records.jsonl"
known_limitations:
  - "Current-state statements are date-bound."
  - "Absence of evidence is not evidence of non-occurrence."
research_gaps:
  - "Independent execution evidence remains incomplete where explicitly noted."
review_after: 2027-01-15
---

# Star Atlas Ecosystem Fund
The Ecosystem Fund is a DAO policy instrument for financing ecosystem work. Its controlling captured framework is PIP-23, which refreshes and supersedes PIP-4.

## Policy history

PIP-4 proposed the original fund, including a budget linked to 20% of the DAO treasury and a stated USD limitation. PIP-23 later continued the fund and expressly replaced PIP-4. Historical references to PIP-4 remain useful, but current interpretation must begin with PIP-23. [PIP-4 and PIP-23](../../archive/semantic/governance/pip-registry-semantic.json)

PIP-23 allocates 20% of ATLAS and 20% of USDC above a $500,000 DAO-treasury reserve threshold. It calls for quarterly refills when the fund falls below those formulas. Funding applications must state their request in USDC, while the fund pays only in ATLAS; the text also calls for received USDC to be converted to ATLAS while USDC remains an insignificant treasury component. No single PIP may exceed 5% of the “Balance After” value from the last refill transaction or run longer than 12 months. [PIP-23; SRC-PIP-23-0ECF2928](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-23-0ECF2928.json)

The Council's specified duties are to review and steward eligible proposals, coordinate special approval where needed, implement passed PIPs, and track payments. The same text says the Council does not authorize legally binding contracts, execute fund-refill transactions, conduct KYC/KYB, or approve a PIP before voting. These are policy assignments, not proof that a particular transfer occurred.

PIP-23 reports two fund-refill transactions in its own proposal text: 159,713,142 ATLAS on 2024-10-04 and 87,551,239 ATLAS on 2025-07-03. It includes transaction references for transfers into the fund wallet, but this campaign did not independently reconcile those transactions. The proposal therefore establishes an attributed refill report, not independently verified refills, recipient payments, or completed work.

[PIP-33](PIP-33-ATMTA-Historic-Expense-Reimbursement.md) is outside this mechanism. Its proposal expressly requests a direct DAO Treasury measure exceeding the ordinary Ecosystem Fund limit, and the Council tracker semantic record marks `ecosystem_fund: NO`. It must not be used when calculating or describing Ecosystem Fund recipient activity. [Council tracker semantic records](../../operations/campaigns/social-governance-semantic-enrichment/input-council-tracker/council-pip-tracker-semantic-records.jsonl)

## Decision and payment boundaries

An approved grant proposal authorizes an action under the applicable policy. It does not by itself establish that funds were transferred, milestones were accepted, or deliverables were completed. Council tracker fields are retained as attributed operational assessments:

```yaml
assessment_source: STAR_ATLAS_COUNCIL_TRACKER
assessment_type: COUNCIL_AUTHORED_OPERATIONAL_ASSESSMENT
independent_verification_status: UNKNOWN
```

## Current state

As of 2026-07-17, PIP-23 is the supported superseding policy. Its two reported refill references do not independently verify the refills, recipient payments, or deliverables, which remain incomplete for many funded PIPs.

## Evidence references

- [PIP registry](PIP-Registry.md)
- [PIP-23 source record](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-23-0ECF2928.json)
