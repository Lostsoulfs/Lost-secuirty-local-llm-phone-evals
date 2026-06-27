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
    cases = load_cases(suite="safety")
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
    passed = bool(safe_passed and planted_ok and redaction_ok and report_clean)
    return {
        "passed": passed,
        "safe_case_count": len(cases),
        "safe_report_passed": safe_passed,
        "planted_bad_controls_passed": planted_ok,
        "redaction_self_test_passed": redaction_ok,
        "report_sensitive_scan_passed": report_clean,
        "planted_failures": planted_failures,
    }


def proof_summary_text(result: dict[str, object]) -> str:
    status = "PASS" if result["passed"] else "FAIL"
    return (
        f"{status}: {result['safe_case_count']} safe cases, "
        f"planted_bad={result['planted_bad_controls_passed']}, "
        f"redaction={result['redaction_self_test_passed']}, "
        f"report_scan={result['report_sensitive_scan_passed']}"
    )
