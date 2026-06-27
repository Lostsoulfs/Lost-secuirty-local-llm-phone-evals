from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Finding:
    label: str
    start: int
    end: int


SENSITIVE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("openai_key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b")),
    ("private_key", re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----")),
    ("bearer_token", re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{20,}\b", re.IGNORECASE)),
    ("email", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("ssn", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
    ("phone", re.compile(r"(?<!\d)(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}(?!\d)")),
)


def find_sensitive(text: str) -> list[Finding]:
    findings: list[Finding] = []
    for label, pattern in SENSITIVE_PATTERNS:
        for match in pattern.finditer(text):
            findings.append(Finding(label=label, start=match.start(), end=match.end()))
    return sorted(findings, key=lambda finding: (finding.start, finding.end, finding.label))


def redact_text(text: str) -> tuple[str, list[Finding]]:
    findings = find_sensitive(text)
    if not findings:
        return text, []
    parts: list[str] = []
    cursor = 0
    for finding in findings:
        if finding.start < cursor:
            continue
        parts.append(text[cursor : finding.start])
        parts.append(f"[REDACTED:{finding.label}]")
        cursor = finding.end
    parts.append(text[cursor:])
    return "".join(parts), findings


def redact_obj(value):
    if isinstance(value, str):
        return redact_text(value)[0]
    if isinstance(value, list):
        return [redact_obj(item) for item in value]
    if isinstance(value, dict):
        return {key: redact_obj(item) for key, item in value.items()}
    return value


def scan_texts(items: Iterable[tuple[str, str]]) -> dict[str, list[str]]:
    results: dict[str, list[str]] = {}
    for name, text in items:
        labels = sorted({finding.label for finding in find_sensitive(text)})
        if labels:
            results[name] = labels
    return results


def scan_path(path: Path) -> dict[str, list[str]]:
    if path.is_dir():
        files = [item for item in path.rglob("*") if item.is_file()]
    else:
        files = [path]
    inputs: list[tuple[str, str]] = []
    for file_path in files:
        try:
            text = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        inputs.append((str(file_path), text))
    return scan_texts(inputs)
