# Repository CI

`validate_repository.py` supplies non-network repository and campaign gates for pull requests. It parses tracked JSON and JSONL, checks declared schema compatibility, reconciles extraction IDs with Source Records, validates local Markdown links, enforces campaign-specific path boundaries, and verifies deterministic campaign outputs.

Campaign CI never runs live discovery or retrieval. Medium validation operates only on the frozen manifest and preserved artifacts.

Run locally from the repository root:

```text
python operations/ci/validate_repository.py --mode repository --base-ref origin/main
python operations/ci/validate_repository.py --mode campaign --base-ref origin/main
```
