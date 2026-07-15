# Star Atlas Transcript Semantic Enrichment 2026-07

This campaign creates a review-only semantic evidence layer for the 36 Economic Forum, DAO, and Town Hall transcripts preserved by `star-atlas-transcripts-ingestion-2026-07`.

## Method

Segments are selected using lexical topic signatures, explicit conversational transitions, transcript time gaps, and maximum-coherence safeguards. They are not fixed timestamp slices.

Each segment preserves:

- Source ID and recording ID
- Start and end timestamps
- Exact transcript path and line range
- Caption count and content checksum
- Unknown speaker status
- Controlled topics and statement classifications
- Product lifecycle language
- Canonical entity mentions and unresolved references
- Evidence classifications and promotion targets

## Controlled topics

`PRODUCT`, `GAMEPLAY`, `GOVERNANCE`, `ECONOMY`, `TECHNOLOGY`, `LORE`, `CORPORATE`, `PEOPLE`, `COMMUNITY`, `PARTNERSHIP`, `GUILD`, `EVENT`, `MARKETING`, `OPERATIONS`

## Statement classifications

`ANNOUNCEMENT`, `STATUS_UPDATE`, `ROADMAP`, `RELEASE`, `DESIGN_INTENT`, `TECHNICAL_EXPLANATION`, `Q_AND_A`, `RETROSPECTIVE`, `CLARIFICATION`, `CORRECTION`, `COMMUNITY_FEEDBACK`, `DISCUSSION`, `SPECULATION`, `THEORYCRAFTING`

## Evidence safety

- All promotion candidates remain `PROPOSED_ONLY` and require manual review.
- Lifecycle tags describe transcript wording; they do not prove release, execution, or current status.
- PIP tags establish mentions or discussions, not proposal outcomes.
- Quotations are preserved with `speaker: UNKNOWN` and require attribution review.
- No `FIRST_MENTION` tag is assigned because corpus ordering and partial dates cannot establish historical priority.
- No canonical knowledge, graph fact, or publication output is changed.

## Reproduction

From the repository root:

```text
python operations/campaigns/star-atlas-transcripts-semantic-2026-07/generate_semantic_index.py
python operations/campaigns/star-atlas-transcripts-semantic-2026-07/validate_semantic_index.py
```
