from __future__ import annotations

import hashlib
import statistics
import uuid
from datetime import datetime, timezone
from typing import Any

from .adapters.base import RuntimeAdapter
from .checks import run_checks
from .redaction import find_sensitive, redact_text
from .reporting import validate_report
from .schemas import EvalCase


def prompt_hash(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


def run_cases(
    cases: list[EvalCase],
    adapter: RuntimeAdapter,
    model_id: str,
    device_snapshot: dict[str, Any] | None = None,
) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    redaction_count = 0
    for case in cases:
        runtime_result = adapter.generate(case.prompt, case)
        check_results = run_checks(case, runtime_result)
        redacted_text, findings = redact_text(runtime_result.text)
        redaction_count += len(findings)
        results.append(
            {
                "id": case.id,
                "suite": case.suite,
                "tags": case.tags,
                "prompt_sha256": prompt_hash(case.prompt),
                "passed": all(check.passed for check in check_results),
                "checks": [
                    {"name": check.name, "passed": check.passed, "message": check.message}
                    for check in check_results
                ],
                "latency_ms": round(runtime_result.latency_ms, 3),
                "output_text": redacted_text,
            }
        )
    latencies = [item["latency_ms"] for item in results]
    report = {
        "run_id": f"run-{uuid.uuid4().hex[:12]}",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "runtime": adapter.name,
        "model_id": model_id,
        "device_snapshot": device_snapshot or {"status": "not_collected"},
        "case_results": results,
        "metrics": {
            "case_count": len(results),
            "pass_count": sum(1 for item in results if item["passed"]),
            "fail_count": sum(1 for item in results if not item["passed"]),
            "latency_ms_min": min(latencies) if latencies else None,
            "latency_ms_max": max(latencies) if latencies else None,
            "latency_ms_mean": statistics.fmean(latencies) if latencies else None,
        },
        "redaction_status": {
            "redacted": redaction_count > 0,
            "finding_count": redaction_count,
        },
    }
    validate_report(report)
    serialized = str(report)
    if find_sensitive(serialized):
        report["redaction_status"]["post_write_sensitive_findings"] = True
    else:
        report["redaction_status"]["post_write_sensitive_findings"] = False
    return report
