# Phase 5 Foundational Publication Portfolio

Campaign ID: `phase-5-foundational-publication-portfolio-2026-07`

This campaign turns the Phase 4 dossier routes into eleven human-first draft
articles. It adds one operator-approved community-and-people article after a
supplemental evidence assessment.

## Scope

- Draft eleven reader-facing publication articles.
- Preserve the distinction between Archive, Knowledge and Publication.
- Populate the publication manifest with deterministic `DRAFT` entries.
- Keep all drafts outside the public build.
- Hide internal taxonomy and workflow metadata from article prose.
- Require human semantic, narrative, SEO and comprehensiveness review.

No Archive evidence, canonical Knowledge, graph fact or site file may change.
Intergalactic Herald is not a central narrative source or profile in this
initial portfolio.

## Deterministic commands

```text
python operations/campaigns/phase-5-foundational-publication-portfolio-2026-07/build_campaign.py
python operations/campaigns/phase-5-foundational-publication-portfolio-2026-07/validate_campaign.py origin/main
python -m unittest discover operations/tests/phase5_publication_portfolio
```

`build_campaign.py` recalculates canonical UTF-8/LF content checksums, the
internal publication manifest and campaign summary. Line-ending normalization
keeps article identities deterministic across Windows and Linux checkouts.
`validate_campaign.py` checks article structure, front matter, knowledge inputs,
local evidence links, manifest state, visibility policy, community evidence
limits and protected paths.

## Stop gate

The campaign stops after opening a draft PR. Automated checks cannot approve
editorial judgment. A human must review all eleven narratives before any entry
may move from `DRAFT`.
