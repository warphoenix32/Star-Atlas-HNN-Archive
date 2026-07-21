"""Validate the completed Knowledge Narrative Depth revision portfolio."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
BUILD = HERE / "build_closeout.py"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_text(encoding="utf-8").replace("\r\n", "\n").encode()).hexdigest()


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, encoding="utf-8", errors="replace", capture_output=True, check=False)


def main() -> int:
    generated = [HERE / name for name in ("page-review-ledger.json", "page-review-ledger.md", "campaign-summary.json", "campaign-summary.md")]
    before = {str(path): sha(path) for path in generated}
    first = run(sys.executable, str(BUILD)); middle = {str(path): sha(path) for path in generated}
    second = run(sys.executable, str(BUILD)); after = {str(path): sha(path) for path in generated}
    summary = json.loads((HERE / "campaign-summary.json").read_text(encoding="utf-8"))
    ledger = json.loads((HERE / "page-review-ledger.json").read_text(encoding="utf-8"))["records"]
    paths = [item["path"] for item in ledger]
    checks = {
        "deterministic_generation": first.returncode == second.returncode == 0 and before == middle == after,
        "baseline_page_count": len(ledger) == 80,
        "unique_pages": len(paths) == len(set(paths)) == 80,
        "wave_assignment_complete": summary["wave_assignments"] == 80 and not summary["duplicate_wave_assignments"] and all(item["revision_wave"] for item in ledger),
        "eight_revision_waves": len(summary["waves"]) == 8 and sum(item["page_count"] for item in summary["waves"]) == 80,
        "required_metadata_complete": summary["pages_with_required_metadata"] == 80,
        "risk_class_complete": "UNSPECIFIED" not in summary["risk_class_distribution"],
        "review_status_complete": summary["pages_with_review_status"] == 80,
        "review_dates_present": all(item["review_after"] for item in ledger),
        "no_adjudication_blocker": not summary["human_adjudication_blockers"],
    }

    broken: list[str] = []
    for item in ledger:
        page = ROOT / item["path"]
        for target in re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", page.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            clean = target.split("#", 1)[0]
            if clean and not (page.parent / clean).resolve().exists():
                broken.append(f"{item['path']} -> {target}")
    checks["internal_links"] = not broken
    changed = set(run("git", "diff", "--name-only", "origin/main...HEAD").stdout.splitlines()) | set(run("git", "diff", "--name-only").stdout.splitlines())
    checks["forbidden_paths_untouched"] = not any(path.startswith(("archive/", "graph/", "publication/")) for path in changed)
    checks["git_diff_check"] = run("git", "diff", "--check").returncode == 0

    errors = [f"failed check: {name}" for name, passed in checks.items() if not passed] + broken
    status = "PASS" if not errors else "FAIL"
    report = {"campaign_id": "knowledge-narrative-depth-001-closeout-2026-07", "status": status, "checks": checks, "errors": errors}
    (HERE / "validation-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    (HERE / "validation-report.md").write_text(
        "# Knowledge Narrative Depth Closeout Validation\n\n**Result:** `" + status + "`\n\n" +
        "\n".join(f"- {'PASS' if passed else 'FAIL'}: {name}" for name, passed in checks.items()) + "\n",
        encoding="utf-8", newline="\n"
    )
    print(json.dumps(report))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
