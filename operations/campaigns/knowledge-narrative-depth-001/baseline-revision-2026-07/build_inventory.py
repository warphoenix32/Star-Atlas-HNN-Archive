#!/usr/bin/env python3
"""Build a deterministic inventory of every knowledge Markdown page."""

from __future__ import annotations

from collections import Counter
from datetime import date
import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
AS_OF = "2026-07-20"
REQUIRED_METADATA = (
    "title", "knowledge_status", "as_of", "confidence", "evidence_basis",
    "known_limitations", "research_gaps", "review_after", "seo_title", "seo_description",
    "page_risk_score", "page_risk_class",
)
STRUCTURED_NAMES = ("registry", "index", "ledger", "catalog", "inventory", "timeline", "map", "backlog")


def frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, text
    raw = text[4:end]
    values: dict[str, str] = {}
    for line in raw.splitlines():
        match = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$", line)
        if match:
            values[match.group(1)] = match.group(2).strip()
    return values, text[end + 5:]


def page_kind(path: Path) -> str:
    name = path.stem.casefold()
    if path.name == "README.md":
        return "DOMAIN_INDEX"
    if any(token in name for token in STRUCTURED_NAMES):
        return "STRUCTURED_REFERENCE"
    if "profile" in name:
        return "SOURCE_OR_ENTITY_PROFILE"
    return "NARRATIVE_ARTICLE"


def action_for(kind: str, words: int, missing: list[str], taxonomy_markers: int) -> str:
    if kind == "DOMAIN_INDEX":
        return "INDEX_REDESIGN"
    if kind == "STRUCTURED_REFERENCE":
        return "STRUCTURED_REWORK"
    if words < 250:
        return "REWRITE"
    if words < 650 or missing or taxonomy_markers > 12:
        return "EXPAND_AND_STANDARDIZE"
    return "NARRATIVE_REVIEW_AND_REFRESH"


def wave_for(domain: str) -> int:
    if domain in {"governance", "economy"}:
        return 1
    if domain in {"gameplay", "technology", "events", "timeline"}:
        return 2
    if domain in {"organizations", "guilds", "people", "media", "index"}:
        return 3
    return 4


def build() -> dict[str, object]:
    pages = []
    for path in sorted((ROOT / "knowledge").rglob("*.md")):
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        metadata, body = frontmatter(text)
        domain = path.relative_to(ROOT / "knowledge").parts[0] if len(path.relative_to(ROOT / "knowledge").parts) > 1 else "knowledge"
        kind = page_kind(path)
        missing = [field for field in REQUIRED_METADATA if field not in metadata]
        words = len(re.findall(r"\b[\w'-]+\b", body))
        headings = len(re.findall(r"(?m)^##\s+", body))
        evidence_links = len(re.findall(r"\]\([^)]*(?:archive|operations)/", body))
        source_ids = len(set(re.findall(r"\b(?:SRC|SA-DISCORD)-[A-Z0-9-]+", text)))
        taxonomy_markers = len(re.findall(r"`(?:R[1-5]|[A-Z][A-Z0-9_]{3,})`", body))
        current_state_mentions = len(re.findall(r"(?i)\b(current(?:ly)?|as of|remains live|is live|active)\b", body))
        action = action_for(kind, words, missing, taxonomy_markers)
        priority = "HIGH" if words < 250 or kind == "DOMAIN_INDEX" else ("MEDIUM" if missing or taxonomy_markers > 12 else "NORMAL")
        pages.append({
            "page_id": hashlib.sha256(rel.encode()).hexdigest()[:16].upper(),
            "path": rel,
            "domain": domain,
            "page_kind": kind,
            "recommended_action": action,
            "revision_wave": wave_for(domain),
            "priority": priority,
            "metrics": {
                "word_count": words,
                "h2_sections": headings,
                "archive_or_operations_links": evidence_links,
                "source_id_mentions": source_ids,
                "inline_machine_taxonomy_markers": taxonomy_markers,
                "current_state_mentions": current_state_mentions,
            },
            "metadata_present": sorted(metadata),
            "missing_required_metadata": missing,
            "review_requirements": [
                "re-open underlying evidence before changing material claims",
                "preserve lifecycle and authority distinctions",
                "consolidate reader-facing taxonomy",
                "validate links, dates, limitations, and research gaps",
            ],
        })
    actions = Counter(page["recommended_action"] for page in pages)
    domains = Counter(page["domain"] for page in pages)
    waves = Counter(str(page["revision_wave"]) for page in pages)
    return {
        "campaign_id": "knowledge-baseline-revision-2026-07",
        "as_of": AS_OF,
        "status": "INVENTORIED_FOR_DOMAIN_REVISION",
        "page_count": len(pages),
        "action_counts": dict(sorted(actions.items())),
        "domain_counts": dict(sorted(domains.items())),
        "wave_counts": dict(sorted(waves.items())),
        "pages": pages,
    }


def main() -> None:
    payload = build()
    (OUT / "page-inventory.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    lines = [
        "# Knowledge Baseline Page Inventory", "",
        f"As of {AS_OF}, the repository contains **{payload['page_count']}** Markdown knowledge pages. Every page is assigned a deliberate revision action; none is accepted solely because it already exists.", "",
        "## Revision portfolio", "",
        "| Action | Pages |", "| --- | ---: |",
    ]
    lines.extend(f"| `{key}` | {value} |" for key, value in payload["action_counts"].items())
    lines.extend(["", "## Domain waves", "", "| Wave | Pages |", "| --- | ---: |"])
    lines.extend(f"| {key} | {value} |" for key, value in payload["wave_counts"].items())
    lines.extend(["", "## Page decisions", "", "| Wave | Domain | Page | Action | Priority | Words | Missing metadata |", "| ---: | --- | --- | --- | --- | ---: | --- |"])
    for page in payload["pages"]:
        missing = ", ".join(page["missing_required_metadata"]) or "none"
        lines.append(f"| {page['revision_wave']} | {page['domain']} | `{page['path']}` | `{page['recommended_action']}` | {page['priority']} | {page['metrics']['word_count']} | {missing} |")
    (OUT / "page-inventory.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
