from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from phone_eval_kit.redaction import find_sensitive, scan_path

SKIP_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    "reports",
    "artifacts",
    "models",
    "model-cache",
    "device-dumps",
    "screenshots",
    "captures",
}


def staged_files() -> list[Path]:
    completed = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMRT"],
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        return []
    return [Path(line.strip()) for line in completed.stdout.splitlines() if line.strip()]


def repo_files() -> list[Path]:
    completed = subprocess.run(["git", "ls-files"], text=True, capture_output=True, check=False)
    files = [Path(line.strip()) for line in completed.stdout.splitlines() if line.strip()]
    if files:
        return files
    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file() and not any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts)
    ]


def scan_files(files: list[Path]) -> dict[str, list[str]]:
    findings: dict[str, list[str]] = {}
    for path in files:
        full_path = path if path.is_absolute() else ROOT / path
        if not full_path.exists() or any(part in SKIP_DIRS for part in full_path.relative_to(ROOT).parts):
            continue
        findings.update(scan_path(full_path))
    return findings


def self_test() -> bool:
    clean = "this report contains synthetic local eval output only"
    sensitive = "email " + "person" + "@" + "example.test" + " key " + "sk-" + ("x" * 24)
    return not find_sensitive(clean) and bool(find_sensitive(sensitive))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan staged files for sensitive-looking values.")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--all", action="store_true", help="scan all tracked files, or all repo files before first commit")
    args = parser.parse_args(argv)
    if args.self_test:
        ok = self_test()
        print("PASS: redaction scanner self-test" if ok else "FAIL: redaction scanner self-test")
        return 0 if ok else 1
    files = repo_files() if args.all else staged_files()
    findings = scan_files(files)
    if findings:
        for path, labels in sorted(findings.items()):
            rel = Path(path)
            try:
                rel = rel.relative_to(ROOT)
            except ValueError:
                pass
            print(f"{rel}: sensitive-looking data detected: {', '.join(labels)}")
        return 1
    print("PASS: no sensitive-looking data detected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
