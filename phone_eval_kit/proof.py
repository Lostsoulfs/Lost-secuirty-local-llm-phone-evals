from __future__ import annotations

import json

from .adapters.fake import FakeRuntimeAdapter
from .cases import load_cases
from .checks import run_checks
from .redaction import find_sensitive, redact_text
from .reporting import validate_report
from .runner import run_cases
from .schemas import RuntimeResult


def run_proof() -> dict[str, object]:
    safety_cases = load_cases(suite="safety")
    performance_cases = load_cases(suite="performance")
    cases = [*safety_cases, *performance_cases]
    safe_report = run_cases(cases, FakeRuntimeAdapter(mode="safe"), model_id="fake-safe")
    validate_report(safe_report)
    safe_passed = safe_report["metrics"]["fail_count"] == 0

    planted_failures: list[dict[str, object]] = []
    unsafe_adapter = FakeRuntimeAdapter(mode="unsafe")
    for case in cases:
        unsafe = unsafe_adapter.generate(case.prompt, case)
        checks = run_checks(case, unsafe)
        failed = [check.name for check in checks if not check.passed]
        planted_failures.append({"id": case.id, "failed_checks": failed})

    sensitive_sample = "contact " + "user" + "@" + "example.test" + " token " + "sk-" + ("x" * 24)
    redacted, findings = redact_text(sensitive_sample)
    redaction_ok = bool(findings) and "example.test" not in redacted and "sk-" not in redacted

    report_text = json.dumps(safe_report, sort_keys=True)
    report_clean = not find_sensitive(report_text)
    planted_ok = all(item["failed_checks"] for item in planted_failures)
    repeat_case = next(
        (case for case in performance_cases if case.id == "performance.repeatability.fake_runtime"),
        None,
    )
    if repeat_case is None:
        repeatability_ok = False
    else:
        first = FakeRuntimeAdapter(mode="safe").generate(repeat_case.prompt, repeat_case)
        second = FakeRuntimeAdapter(mode="safe").generate(repeat_case.prompt, repeat_case)
        first_checks = run_checks(repeat_case, first)
        bad_latency_checks = run_checks(
            repeat_case,
            RuntimeResult(text=first.text, latency_ms=-1, raw_metadata={"planted_bad": "negative_latency"}),
        )
        repeatability_ok = (
            first.text == second.text
            and all(check.passed for check in first_checks)
            and any(check.name == "latency_recorded" and not check.passed for check in bad_latency_checks)
        )
    passed = bool(safe_passed and planted_ok and redaction_ok and report_clean and repeatability_ok)
    return {
        "passed": passed,
        "proof_case_count": len(cases),
        "safe_report_passed": safe_passed,
        "planted_bad_controls_passed": planted_ok,
        "repeatability_self_test_passed": repeatability_ok,
        "redaction_self_test_passed": redaction_ok,
        "report_sensitive_scan_passed": report_clean,
        "planted_failures": planted_failures,
    }


def proof_summary_text(result: dict[str, object]) -> str:
    status = "PASS" if result["passed"] else "FAIL"
    return (
        f"{status}: {result['proof_case_count']} proof cases, "
        f"planted_bad={result['planted_bad_controls_passed']}, "
        f"repeatability={result['repeatability_self_test_passed']}, "
        f"redaction={result['redaction_self_test_passed']}, "
        f"report_scan={result['report_sensitive_scan_passed']}"
    )
