from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REQUIRED_REPORT_KEYS = {
    "run_id",
    "timestamp_utc",
    "runtime",
    "model_id",
    "device_snapshot",
    "case_results",
    "metrics",
    "redaction_status",
}


def validate_report(report: dict[str, Any]) -> None:
    missing = sorted(REQUIRED_REPORT_KEYS.difference(report))
    if missing:
        raise ValueError(f"report missing required keys: {', '.join(missing)}")
    if not isinstance(report["case_results"], list):
        raise ValueError("report case_results must be a list")
    if not isinstance(report["metrics"], dict):
        raise ValueError("report metrics must be an object")
    if not isinstance(report["redaction_status"], dict):
        raise ValueError("report redaction_status must be an object")


def write_report(report: dict[str, Any], out: Path) -> Path:
    validate_report(report)
    if out.suffix.lower() == ".json":
        out.parent.mkdir(parents=True, exist_ok=True)
        target = out
    else:
        out.mkdir(parents=True, exist_ok=True)
        target = out / f"{report['run_id']}.json"
    target.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target
