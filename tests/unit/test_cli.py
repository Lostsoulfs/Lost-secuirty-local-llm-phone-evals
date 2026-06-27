from __future__ import annotations

import json

from phone_eval_kit.cli import doctor_report, main


def test_doctor_report_shape():
    report = doctor_report()
    assert report["python"]["supported"] is True
    assert "adb" in report
    assert "litert_lm" in report


def test_cli_proof_passes(capsys):
    code = main(["proof"])
    captured = capsys.readouterr()
    assert code == 0
    assert "PASS" in captured.out


def test_cli_run_fake_writes_report(tmp_path):
    code = main(["run", "--runtime", "fake", "--suite", "safety", "--out", str(tmp_path)])
    assert code == 0
    reports = list(tmp_path.glob("*.json"))
    assert reports
    report = json.loads(reports[0].read_text(encoding="utf-8"))
    assert report["runtime"] == "fake"
    assert report["metrics"]["fail_count"] == 0
