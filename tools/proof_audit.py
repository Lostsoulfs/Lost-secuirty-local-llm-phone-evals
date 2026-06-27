from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from phone_eval_kit.proof import proof_summary_text, run_proof


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the local phone eval proof baseline.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = run_proof()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(proof_summary_text(result))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
