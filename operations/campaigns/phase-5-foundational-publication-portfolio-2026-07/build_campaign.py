"""Build the deterministic Phase 5 draft publication manifest and reports."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
CAMPAIGN = Path(__file__).resolve().parent
PORTFOLIO_PATH = CAMPAIGN / "portfolio.json"
MANIFEST_PATH = ROOT / "publication/manifests/publication-manifest.json"
SUMMARY_JSON = CAMPAIGN / "campaign-summary.json"
SUMMARY_MD = CAMPAIGN / "campaign-summary.md"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    canonical = text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def word_count(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"^---.*?---", "", text, count=1, flags=re.DOTALL)
    return len(re.findall(r"\b[\w’'-]+\b", text, flags=re.UNICODE))


def build_manifest(portfolio: dict[str, Any]) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    for article in portfolio["articles"]:
        content_path = ROOT / article["content_path"]
        entries.append(
            {
                "publication_id": article["publication_id"],
                "slug": article["slug"],
                "title": article["title"],
                "type": "ARTICLE",
                "status": "DRAFT",
                "audience": article["audience"],
                "content_path": article["content_path"],
                "source_knowledge_paths": article["source_knowledge_paths"],
                "as_of": portfolio["as_of"],
                "editorial": {
                    "human_first": True,
                    "narrative_review": False,
                    "seo_review": False,
                    "comprehensiveness_review": False,
                    "approval_record": None,
                },
                "evidence": {
                    "material_claims_reviewed": False,
                    "references_resolve": True,
                    "conflicts_disclosed": True,
                    "limitations_disclosed": True,
                },
                "presentation": {
                    "summary": article["summary"],
                    "description": article["description"],
                    "primary_topic": article["primary_topic"],
                    "related_topics": article["related_topics"],
                },
                "provenance": {
                    "content_sha256": sha256(content_path),
                    "manifested_at": portfolio["as_of"],
                    "manifested_by": portfolio["campaign_id"],
                },
                "visibility": {
                    "taxonomy": "HIDDEN",
                    "source_ids": "EVIDENCE_PANEL",
                    "workflow_metadata": "HIDDEN",
                },
                "related_publication_ids": article["related_publication_ids"],
                "revision_history": [],
            }
        )
    entries.sort(key=lambda value: value["publication_id"])
    return {
        "manifest_version": "1.0",
        "manifest_id": "publication-manifest-star-atlas-library",
        "as_of": portfolio["as_of"],
        "lifecycle_phase": "PORTFOLIO_DEVELOPMENT",
        "public_base_path": "/library/",
        "source_of_truth": {
            "archive_root": "archive/",
            "knowledge_root": "knowledge/",
            "publication_root": "publication/",
        },
        "build_policy": {
            "include_statuses": ["PUBLISHED"],
            "exclude_internal_fields": [
                "editorial",
                "evidence",
                "provenance",
                "revision_history",
            ],
            "taxonomy_presentation": "HIDDEN",
            "ordering": "publication_id",
        },
        "entries": entries,
    }


def build_summary(portfolio: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    words = {
        article["publication_id"]: word_count(ROOT / article["content_path"])
        for article in portfolio["articles"]
    }
    risk_counts = Counter(article["risk_class"] for article in portfolio["articles"])
    topic_counts = Counter(article["primary_topic"] for article in portfolio["articles"])
    return {
        "campaign_id": portfolio["campaign_id"],
        "as_of": portfolio["as_of"],
        "status": "DRAFT_PORTFOLIO_COMPLETE_AWAITING_HUMAN_SEMANTIC_REVIEW",
        "portfolio": {
            "articles_drafted": len(portfolio["articles"]),
            "manifest_entries": len(manifest["entries"]),
            "published_entries": sum(
                entry["status"] == "PUBLISHED" for entry in manifest["entries"]
            ),
            "total_words": sum(words.values()),
            "word_counts": words,
            "risk_class_counts": dict(sorted(risk_counts.items())),
            "primary_topic_counts": dict(sorted(topic_counts.items())),
        },
        "community_extension": {
            "publication_id": "PUB-011",
            "evidence_packet": (
                "operations/campaigns/phase-5-foundational-publication-portfolio-2026-07/"
                "community-evidence-development.json"
            ),
            "decision": "SUFFICIENT_FOR_BOUNDED_OVERVIEW",
            "future_knowledge_work_required_for_exhaustive_profiles": True,
        },
        "boundaries": {
            "archive_evidence_modified": False,
            "knowledge_modified": False,
            "graph_modified": False,
            "publication_site_modified": False,
            "drafts_in_public_build": False,
            "intergalactic_herald_profile_included": False,
        },
        "human_adjudication_required": True,
        "human_review_scope": [
            "Narrative accuracy and emphasis",
            "Comprehensiveness for the intended audience",
            "SEO titles and descriptions",
            "Material claim and limitation review",
            "Approval or revision of each article before publication",
        ],
        "next_gate": "Human semantic review of all eleven draft articles",
    }


def write_markdown(summary: dict[str, Any], portfolio: dict[str, Any]) -> None:
    article_rows = "\n".join(
        "| {id} | [{title}](../../../{path}) | {risk} | {words} | DRAFT |".format(
            id=article["publication_id"],
            title=article["title"],
            path=article["content_path"],
            risk=article["risk_class"],
            words=summary["portfolio"]["word_counts"][article["publication_id"]],
        )
        for article in portfolio["articles"]
    )
    markdown = f"""# Phase 5 Foundational Publication Portfolio

Status: **{summary['status']}**

The first publication portfolio contains eleven human-first articles derived
from reviewed Knowledge. Every article remains `DRAFT`; the public build still
includes only `PUBLISHED` manifest entries, so none of these drafts is publicly
released by this campaign.

| ID | Draft | Risk | Words | State |
| --- | --- | ---: | ---: | --- |
{article_rows}

## Portfolio metrics

- Draft articles: {summary['portfolio']['articles_drafted']}
- Total narrative words: {summary['portfolio']['total_words']}
- Published entries: {summary['portfolio']['published_entries']}
- Risk distribution: {json.dumps(summary['portfolio']['risk_class_counts'], sort_keys=True)}

## Community extension

The operator added an eleventh article on players, guilds, creators and community
memory. The campaign completed a supplemental evidence assessment and found the
reviewed Knowledge sufficient for a bounded overview. Exhaustive biographies,
guild rosters and rivalry case studies remain future Knowledge work.

Intergalactic Herald is not a central source or profile in this portfolio.

## Boundaries

No Archive evidence, canonical Knowledge, graph fact or site file changed. Draft
metadata and machine taxonomy remain hidden from public narrative. The manifest
continues to exclude all non-`PUBLISHED` entries from the public build.

## Human gate

Human semantic review is required for narrative accuracy, emphasis,
comprehensiveness, SEO language, evidence boundaries and final approval. The
Library Publisher must not publish or self-approve these drafts.
"""
    SUMMARY_MD.write_text(markdown, encoding="utf-8", newline="\n")


def main() -> int:
    portfolio = load_json(PORTFOLIO_PATH)
    manifest = build_manifest(portfolio)
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    summary = build_summary(portfolio, manifest)
    SUMMARY_JSON.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    write_markdown(summary, portfolio)
    print(
        f"BUILT {len(manifest['entries'])} draft articles; "
        f"{summary['portfolio']['total_words']} words"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
