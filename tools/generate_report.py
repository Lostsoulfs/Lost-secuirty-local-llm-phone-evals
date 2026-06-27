from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from phone_eval_kit.adapters.fake import FakeRuntimeAdapter
from phone_eval_kit.cases import load_cases
from phone_eval_kit.runner import run_cases


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate or check a fake-runtime baseline report.")
    parser.add_argument("--check", action="store_true", help="validate report generation without writing")
    parser.add_argument("--out", type=Path, default=Path("reports/baseline-report.json"))
    args = parser.parse_args(argv)
    report = run_cases(load_cases(suite="safety"), FakeRuntimeAdapter(), model_id="fake-safe")
    if args.check:
        print(json.dumps({"status": "ok", "case_count": report["metrics"]["case_count"]}, sort_keys=True))
        return 0
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
