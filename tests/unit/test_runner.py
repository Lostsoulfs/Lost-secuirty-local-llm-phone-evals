from __future__ import annotations

import json

from phone_eval_kit.adapters.fake import FakeRuntimeAdapter
from phone_eval_kit.cases import load_cases
from phone_eval_kit.reporting import REQUIRED_REPORT_KEYS, validate_report
from phone_eval_kit.runner import run_cases


def test_fake_runtime_report_passes_and_matches_schema():
    report = run_cases(load_cases(suite="safety"), FakeRuntimeAdapter(), model_id="fake-safe")
    validate_report(report)
    assert REQUIRED_REPORT_KEYS.issubset(report)
    assert report["metrics"]["fail_count"] == 0
    assert report["redaction_status"]["post_write_sensitive_findings"] is False
    serialized = json.dumps(report)
    assert "ignore previous instructions" not in serialized


def test_unsafe_fake_runtime_has_failures():
    report = run_cases(load_cases(suite="safety"), FakeRuntimeAdapter(mode="unsafe"), model_id="fake-unsafe")
    assert report["metrics"]["fail_count"] > 0
