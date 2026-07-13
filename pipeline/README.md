# Public written corpus ingestion

This directory contains the review-gated ingestion pipeline. The initial stage
turns the creator-grouped source inventory into one deterministic record per
canonical URL. It performs no network requests and never modifies its input.

## Run the normalizer

```powershell
python -m star_atlas_ingest.cli normalize `
  ..\data\manifests\star_atlas_content_url_inventory_2026-07-12.json `
  ..\data\manifests\normalized-urls.jsonl
```

Run from `pipeline/` with `PYTHONPATH=src`, or install the package in editable
mode. Output is sorted by stable `url_id`, so rerunning the same inventory is
reproducible. Written public platforms are marked `PENDING`; audiovisual,
private, and unsupported platforms are retained as metadata with `DEFERRED`.

## Safety boundaries

- Preserve source manifests byte-for-byte and record their SHA-256 digest.
- Do not fetch, bypass robots rules, or evade access controls in normalization.
- Keep raw retrievals and generated state out of canonical knowledge files.
- Promote generated records only after human review.
