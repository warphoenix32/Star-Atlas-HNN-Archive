import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CONTRACTS = ROOT / "operations" / "agents"


class AgentContractTests(unittest.TestCase):
    def test_contract_validator(self):
        result = subprocess.run(
            [sys.executable, str(CONTRACTS / "validate_contracts.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_manifest_preserves_human_publication_boundary(self):
        payload = json.loads((CONTRACTS / "contracts.json").read_text(encoding="utf-8"))
        authoring = payload["knowledge_authoring"]
        self.assertTrue(authoring["human_first"])
        self.assertTrue(authoring["narrative_required"])
        self.assertEqual(authoring["inline_machine_taxonomy"], "PROHIBITED_BY_DEFAULT")
        self.assertEqual(payload["merge_authority"], "HUMAN_OR_BRANCH_PROTECTION")
        self.assertIn("RESEARCH-GAP-ANALYST-CONTRACT.md", payload["specialist_contracts"])

    def test_transcription_profile_preserves_quality_and_attribution_boundaries(self):
        manifest = json.loads(
            (CONTRACTS / "contracts.json").read_text(encoding="utf-8")
        )
        profile = json.loads(
            (CONTRACTS / manifest["transcription_profile"]).read_text(encoding="utf-8")
        )
        cpu = profile["profiles"]["CPU_ARCHIVAL_BASELINE"]
        gpu = profile["profiles"]["GPU_ARCHIVAL_QUALITY"]
        self.assertEqual(cpu["cpu_thread_policy"]["rule"], "PHYSICAL_CORES_MINUS_2")
        self.assertEqual(cpu["num_workers"], 1)
        self.assertTrue(cpu["word_timestamps"])
        self.assertEqual(gpu["model"], "large-v3-turbo")
        self.assertTrue(profile["quality_review"]["two_pass_required"])
        speaker_policy = profile["speaker_policy"]
        self.assertFalse(speaker_policy["candidate_roster_is_attribution_evidence"])
        self.assertEqual(
            [
                item["display_name"]
                for item in speaker_policy["atlas_brew_operator_supplied_candidates"]
            ],
            ["Jose", "Dominic", "Santi", "Michael Wagner"],
        )
        self.assertIn(
            "CANDIDATE_ROSTER_ALONE",
            speaker_policy["prohibited_assignment_bases"],
        )


if __name__ == "__main__":
    unittest.main()
