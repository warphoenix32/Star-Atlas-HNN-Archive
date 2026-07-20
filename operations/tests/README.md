# Tests

Repository tests cover ingestion compatibility, schema contracts, campaign-specific validation, the Library front end, and the simplified promotion pipeline. The promotion tests verify that only fully qualified R1 candidates can be automatically approved onto draft branches and that elevated-risk candidates retain human-review and authorization requirements.

Run from the repository root:

```bash
python -m pytest -c operations/pipeline/pyproject.toml operations/tests/pipeline
python operations/tests/schema/test_schema_compatibility.py
python operations/migrations/validate_wave_1_5.py
```
