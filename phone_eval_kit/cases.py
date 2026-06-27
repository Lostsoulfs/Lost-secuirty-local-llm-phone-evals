from __future__ import annotations

import json
from importlib import resources
from pathlib import Path
from typing import Iterable

from .checks import CHECKS
from .schemas import EvalCase, ValidationError


def default_cases_path(suite: str) -> Path:
    resource = resources.files("phone_eval_kit").joinpath("evals", f"{suite}.jsonl")
    return Path(str(resource))


def load_cases(path: Path | str | None = None, suite: str = "safety") -> list[EvalCase]:
    case_path = Path(path) if path else default_cases_path(suite)
    cases: list[EvalCase] = []
    with case_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            try:
                data = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValidationError(f"{case_path}:{line_number}: invalid JSON: {exc.msg}") from exc
            case = EvalCase.from_mapping(data)
            cases.append(case)
    validate_cases(cases)
    return cases


def validate_cases(cases: Iterable[EvalCase]) -> None:
    seen: set[str] = set()
    for case in cases:
        if case.id in seen:
            raise ValidationError(f"duplicate eval case id: {case.id}")
        seen.add(case.id)
        unknown = [name for name in case.checks if name not in CHECKS]
        if unknown:
            raise ValidationError(f"eval case {case.id} references unknown checks: {', '.join(unknown)}")
    if not seen:
        raise ValidationError("no eval cases loaded")
