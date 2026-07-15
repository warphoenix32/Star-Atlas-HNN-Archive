# Knowledge Generation Risk Assessment Matrix

## Purpose

Balance page quantity against factual, temporal, reputational, governance, and interpretive risk. The campaign may relax completeness thresholds, but not provenance, attribution, lifecycle separation, or uncertainty disclosure.

## Page risk score

Score each proposed page from 0–3 on each dimension. Lower is safer.

| Dimension | 0 — Low risk | 1 | 2 | 3 — High risk |
|---|---|---|---|---|
| Source authority | Multiple primary official sources | One strong primary source | Attributed institutional or strong secondary source | Anonymous, inferred, weak, or unsourced |
| Cross-source agreement | Multiple sources agree | No contradiction found | Minor discrepancies | Material contradiction |
| Temporal stability | Immutable historical fact | Slowly changing | Active operational state | Highly fluid/current |
| Interpretive burden | Direct explicit statement | Straightforward synthesis | Contextual inference | Speculative reconstruction |
| Consequence of error | Minor descriptive effect | Moderate confusion | Institutional, financial, or reputational impact | Legal, accusatory, governance, or severe financial impact |

Maximum score: 15.

## Risk classes

| Score | Class | Default knowledge status | Publication rule |
|---:|---|---|---|
| 0–3 | R1 — Canonical | `CANONICAL` | Normal semantic review and validation |
| 4–6 | R2 — Qualified canonical | `QUALIFIED` | Publish with claim-level citations, scope, and limitations |
| 7–9 | R3 — Provisional | `PROVISIONAL` | Visible provisional status, research gaps, and scheduled review |
| 10–12 | R4 — Research synthesis | `HISTORICAL` or research note | Do not present as settled current knowledge without explicit approval |
| 13–15 | R5 — Archive only | none | Preserve evidence; do not synthesize into canonical knowledge |

## Claim overrides

A page-level score does not automatically authorize every claim. Apply these overrides:

### Automatically elevate to at least R3

- current staff or leadership roles;
- live operational metrics;
- current product availability without recent official confirmation;
- implementation or milestone completion based on one attributed report;
- partnership outcomes beyond the original announcement;
- financial disbursement without transaction-level reconciliation;
- inferred successor or dependency relationships.

### Automatically elevate to at least R4

- claim reconstructed from unknown speakers;
- roadmap promise presented as likely delivery;
- technical architecture inferred from user-facing behavior;
- community interpretation presented as official lore;
- current organizational role based only on old material;
- disputed event with materially conflicting sources.

### Automatically classify R5

- accusation of wrongdoing without strong multi-source evidence;
- identification of an unknown or pseudonymous real person by inference;
- legal conclusion not explicitly documented by authoritative evidence;
- financial claim built from ambiguous rows or unverified arithmetic;
- invented implementation state;
- unsupported motive, intent, causality, or blame.

## Source authority classes

| Class | Description | Typical use |
|---|---|---|
| A1 | Immutable primary evidence: official proposal text, vote totals, transaction, deployed artifact | canonical factual claims |
| A2 | Official first-party publication or announcement | announcement, release, policy, current-state claims with date scope |
| A3 | Official institutional operational record, including Council tracker | attributed operations, milestones, administrative state |
| B1 | Reviewed transcript or direct statement with known speaker | attributed claims and institutional interpretation |
| B2 | Reviewed community publication with demonstrated sourcing | contextual synthesis and qualified corroboration |
| C1 | Unknown speaker, unattributed export, or weak secondary source | research lead only |
| C2 | Inference, machine extraction, or unresolved reconstruction | archive and research-gap layer |

## Lifecycle risk controls

The following pairs must never be collapsed:

| Evidence says | It does not prove |
|---|---|
| proposal published | vote occurred |
| vote passed | implementation began |
| implementation announced | implementation completed |
| milestone reported | milestone independently verified |
| product announced | product released |
| product released | all promised features delivered |
| event announced | event occurred |
| partnership announced | partnership generated results |
| payment reported | payment independently verified |
| role held historically | role held currently |

## Decision matrix by content type

| Content type | Normal range | Main failure risk | Required control |
|---|---:|---|---|
| PIP title, dates, result | R1–R2 | stale portal state or election ambiguity | reconcile portal, corpus review, and Council evidence |
| Governance authority | R1–R2 | conflating legal, administrative, and voting power | cite constitutional proposal sections |
| Product identity and release | R1–R2 | announcement/release confusion | exact lifecycle state and date |
| Product current state | R2–R3 | staleness | `as_of` and review date |
| Council ROI claim | R2–R3 | attribution becoming fact | label Council-authored assessment |
| Treasury/payment state | R2–R4 | reported values treated as verified | independent verification field |
| Event chronology | R1–R3 | announcement treated as occurrence | separate event notice and completion evidence |
| Partnership announcement | R1–R2 | outcome inference | restrict page to announced scope unless corroborated |
| Partnership impact | R3–R4 | unsupported outcome | require execution evidence |
| Technical architecture | R2–R4 | undocumented inference | source-class separation |
| Lore canon | R2–R4 | community interpretation | publication and canon-status fields |
| Incident history | R2–R4 | incomplete or one-sided account | narrow factual scope and visible limitations |
| Controversy | R4–R5 | reputational harm | elevated human review; strong evidence only |

## Quantity policy

The campaign should optimize useful coverage subject to these constraints:

- at least 70% of promoted pages must be R1 or R2;
- no more than 25% may be R3;
- R4 pages require explicit curator approval and must be visibly historical or research-facing;
- R5 material remains in the archive/research layer;
- incomplete sections are acceptable when marked;
- uncited claims are not acceptable;
- one authoritative source may support a page when the claim is direct and low-consequence;
- provisional pages may exist before all research gaps are closed.

## Example assessments

| Claim or page | Indicative class | Treatment |
|---|---|---|
| PIP-23 superseded PIP-4 | R1 | canonical |
| PIP-13 failed | R1 | canonical |
| PIP-31 passed and was later withdrawn | R1–R2 | preserve both lifecycle states |
| PIP-14 was terminated for non-performance | R2 | attribute reason to Council tracker |
| ATOM processed about 100,000 transactions per day | R2–R3 | Council-reported metric, date-scoped |
| Showroom was released on an official announcement date | R1 | canonical release event |
| Showroom delivered every roadmap promise | R4 | do not infer |
| A partnership was announced | R1 | canonical announcement fact |
| The partnership produced major business results | R3–R4 | requires execution evidence |
| Historical executive role | R2 | date-bound |
| Current executive role | R3 unless recently confirmed | current-state review date |
| Lore interpretation from unknown transcript speakers | R4 | research note |
| Official security warning | R2 | narrow advisory history |
| Allegation against a named party | R5 absent exceptional evidence | archive only |

## Review cadence

- R1: review only when contradicted or superseded.
- R2: review after 12 months or on material source change.
- R3: review after 90–180 days.
- R4: review before any elevation into ordinary knowledge navigation.
- Current-state product, role, treasury, or operational pages: review after 90 days unless a shorter period is justified.