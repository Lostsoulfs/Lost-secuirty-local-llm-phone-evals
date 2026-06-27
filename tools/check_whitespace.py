from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
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


def tracked_files() -> list[Path]:
    completed = subprocess.run(["git", "ls-files"], cwd=ROOT, text=True, capture_output=True, check=False)
    if completed.returncode == 0 and completed.stdout.strip():
        return [ROOT / line.strip() for line in completed.stdout.splitlines() if line.strip()]
    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file() and not any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts)
    ]


def check_file(path: Path) -> list[str]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        return [f"{path}: unreadable: {exc}"]
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return []
    errors: list[str] = []
    if raw and not raw.endswith(b"\n"):
        errors.append(f"{path}: missing final newline")
    if raw.endswith(b"\n\n") or raw.endswith(b"\r\n\r\n"):
        errors.append(f"{path}: extra blank line at EOF")
    for index, line in enumerate(text.splitlines(), start=1):
        if line.rstrip(" \t") != line:
            errors.append(f"{path}:{index}: trailing whitespace")
    return errors


def main() -> int:
    errors: list[str] = []
    for path in tracked_files():
        rel = path.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if not path.is_file():
            continue
        errors.extend(check_file(path))
    if errors:
        print("\n".join(errors))
        return 1
    print("PASS: whitespace check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
