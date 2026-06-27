from __future__ import annotations

import argparse
import json
import platform
import shutil
import sys
from pathlib import Path
from typing import Any

from .adapters.fake import FakeRuntimeAdapter
from .adapters.litert_lm import LiteRTLMCommandAdapter
from .adapters.openai_compatible import OpenAICompatibleAdapter
from .cases import load_cases
from .device.adb import snapshot_device
from .proof import proof_summary_text, run_proof
from .reporting import write_report
from .runner import run_cases


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="phone-evals")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="check local environment")
    doctor.add_argument("--json", action="store_true", help="print JSON")
    doctor.add_argument("--strict", action="store_true", help="return non-zero when optional tools are missing")
    doctor.set_defaults(func=cmd_doctor)

    run = subparsers.add_parser("run", help="run eval cases")
    run.add_argument("--runtime", choices=["fake", "litert-lm", "openai-compatible"], required=True)
    run.add_argument("--suite", default="safety")
    run.add_argument("--cases", type=Path)
    run.add_argument("--model-path")
    run.add_argument("--model-id")
    run.add_argument("--out", type=Path, required=True)
    run.add_argument("--fake-mode", choices=["safe", "unsafe"], default="safe")
    run.add_argument("--command-json", help="LiteRT-LM command JSON array; prompt is sent on stdin")
    run.add_argument("--api-base", help="OpenAI-compatible local API base URL")
    run.add_argument("--api-model", help="OpenAI-compatible model name")
    run.add_argument("--api-key-env", default="PHONE_EVALS_OPENAI_COMPATIBLE_API_KEY")
    run.add_argument("--with-device-snapshot", action="store_true")
    run.set_defaults(func=cmd_run)

    device = subparsers.add_parser("device", help="device commands")
    device_sub = device.add_subparsers(dest="device_command", required=True)
    snapshot = device_sub.add_parser("snapshot", help="write read-only ADB device snapshot")
    snapshot.add_argument("--out", type=Path, required=True)
    snapshot.set_defaults(func=cmd_device_snapshot)

    proof = subparsers.add_parser("proof", help="run proof baseline")
    proof.add_argument("--json", action="store_true")
    proof.set_defaults(func=cmd_proof)
    return parser


def doctor_report() -> dict[str, Any]:
    known_litert_commands = ["litertlm", "litert-lm", "litert_lm"]
    return {
        "python": {
            "version": platform.python_version(),
            "supported": sys.version_info >= (3, 11),
        },
        "adb": {
            "path": shutil.which("adb"),
            "available": shutil.which("adb") is not None,
        },
        "litert_lm": {
            "known_command_path": next((shutil.which(name) for name in known_litert_commands if shutil.which(name)), None),
            "command_json_configured": bool(
                __import__("os").environ.get("PHONE_EVALS_LITERT_LM_COMMAND_JSON")
            ),
        },
        "phone_evals_device_opt_in": __import__("os").environ.get("PHONE_EVALS_DEVICE") == "1",
    }


def cmd_doctor(args: argparse.Namespace) -> int:
    report = doctor_report()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"python {report['python']['version']} supported={report['python']['supported']}")
        print(f"adb available={report['adb']['available']} path={report['adb']['path']}")
        print(
            "litert-lm known_command_path="
            f"{report['litert_lm']['known_command_path']} "
            f"command_json_configured={report['litert_lm']['command_json_configured']}"
        )
        print(f"device opt-in={report['phone_evals_device_opt_in']}")
    if args.strict:
        required_ok = bool(report["python"]["supported"] and report["adb"]["available"])
        return 0 if required_ok else 1
    return 0


def _adapter_from_args(args: argparse.Namespace):
    if args.runtime == "fake":
        return FakeRuntimeAdapter(mode=args.fake_mode), args.model_id or f"fake-{args.fake_mode}"
    if args.runtime == "litert-lm":
        return (
            LiteRTLMCommandAdapter(model_path=args.model_path, command_json=args.command_json),
            args.model_id or args.model_path or "litert-lm-local",
        )
    if args.runtime == "openai-compatible":
        if not args.api_base or not args.api_model:
            raise SystemExit("--api-base and --api-model are required for openai-compatible runtime")
        return (
            OpenAICompatibleAdapter(args.api_base, args.api_model, api_key_env=args.api_key_env),
            args.model_id or args.api_model,
        )
    raise SystemExit(f"unsupported runtime: {args.runtime}")


def cmd_run(args: argparse.Namespace) -> int:
    cases = load_cases(path=args.cases, suite=args.suite)
    adapter, model_id = _adapter_from_args(args)
    device_snapshot = snapshot_device() if args.with_device_snapshot else None
    report = run_cases(cases, adapter, model_id=model_id, device_snapshot=device_snapshot)
    target = write_report(report, args.out)
    print(f"wrote {target}")
    print(f"pass={report['metrics']['pass_count']} fail={report['metrics']['fail_count']}")
    return 0 if report["metrics"]["fail_count"] == 0 else 1


def cmd_device_snapshot(args: argparse.Namespace) -> int:
    snapshot = snapshot_device()
    out = args.out
    if out.suffix.lower() == ".json":
        out.parent.mkdir(parents=True, exist_ok=True)
        target = out
    else:
        out.mkdir(parents=True, exist_ok=True)
        target = out / "device-snapshot.json"
    target.write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {target}")
    return 0 if snapshot["status"] in {"collected", "skipped"} else 1


def cmd_proof(args: argparse.Namespace) -> int:
    result = run_proof()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(proof_summary_text(result))
    return 0 if result["passed"] else 1


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except BrokenPipeError:
        return 1
