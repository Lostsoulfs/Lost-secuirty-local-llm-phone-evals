from __future__ import annotations

from phone_eval_kit.proof import run_proof


def test_proof_baseline_passes():
    result = run_proof()
    assert result["passed"] is True
    assert result["proof_case_count"] >= 5
    assert result["planted_bad_controls_passed"] is True
    assert result["repeatability_self_test_passed"] is True
    assert result["redaction_self_test_passed"] is True
