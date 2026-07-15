---
title: "Governance Implementation and Evidence States"
knowledge_status: CANONICAL
as_of: 2026-07-15
confidence: HIGH
page_risk_score: 3
page_risk_class: R1
evidence_basis:
  - "archive/semantic/governance/pip-registry-semantic.json"
known_limitations:
  - "Current-state statements are date-bound."
  - "Absence of evidence is not evidence of non-occurrence."
research_gaps:
  - "Independent execution evidence remains incomplete where explicitly noted."
review_after: 2027-07-15
---

# Governance Implementation and Evidence States
Governance records answer different questions at different stages. This model prevents an approved proposal from being reported as a completed outcome without execution evidence.

## State model

| State | What the evidence establishes | What it does not establish |
|---|---|---|
| PROPOSED | A request was published | approval or execution |
| VOTING | A decision process opened | final result |
| PASSED / FAILED | The applicable vote result | payment, deployment, or completion |
| IMPLEMENTATION_ANNOUNCED | An actor stated that implementation would begin | completed action |
| PARTIAL_OR_IN_PROGRESS | Attributed operational work is reported | full delivery |
| PAID | A payment record is identified | successful deliverables |
| EXECUTED | A concrete action is evidenced | every promised outcome |
| TERMINATED / CANCELED / WITHDRAWN | Later activity ended or authorization was withdrawn | reversal of the historical vote |
| INDEPENDENTLY_VERIFIED | A separate primary record corroborates the claimed operation | universal correctness beyond its scope |

## Council tracker treatment

```yaml
assessment_source: STAR_ATLAS_COUNCIL_TRACKER
assessment_type: COUNCIL_AUTHORED_OPERATIONAL_ASSESSMENT
independent_verification_status: UNKNOWN
```

The tracker may be the best available operational account, but it is the Council's own assessment. PIP-14's reported termination, PIP-17's reported cancellation, and PIP-31's post-passage withdrawal/non-implementation are therefore preserved as Council-attributed lifecycle findings unless independent evidence is linked. [Governance registry](../../archive/semantic/governance/pip-registry-semantic.json)

## Use in knowledge pages

Pages must name the source of an operational assessment and retain uncertainty. Payment, implementation, and completion require separate evidence fields. “No independent evidence identified” means the archive review did not find it; it is not proof that the event never occurred.

## Related pages

- [PIP Registry](PIP-Registry.md)
- [PIP lifecycle](PIP-Lifecycle-and-Legislative-Process.md)
