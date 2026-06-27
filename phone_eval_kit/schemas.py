from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


class ValidationError(ValueError):
    """Raised when an eval case or report does not match the repo interface."""


@dataclass(frozen=True)
class EvalCase:
    id: str
    suite: str
    prompt: str
    checks: list[str]
    tags: list[str] = field(default_factory=list)
    notes: str = ""

    @classmethod
    def from_mapping(cls, data: dict[str, Any]) -> "EvalCase":
        required = ["id", "suite", "prompt", "checks", "tags"]
        missing = [name for name in required if name not in data]
        if missing:
            raise ValidationError(f"eval case missing required fields: {', '.join(missing)}")
        if not isinstance(data["id"], str) or not data["id"].strip():
            raise ValidationError("eval case id must be a non-empty string")
        if not isinstance(data["suite"], str) or not data["suite"].strip():
            raise ValidationError("eval case suite must be a non-empty string")
        if not isinstance(data["prompt"], str) or not data["prompt"].strip():
            raise ValidationError("eval case prompt must be a non-empty string")
        if not isinstance(data["checks"], list) or not all(
            isinstance(item, str) and item for item in data["checks"]
        ):
            raise ValidationError("eval case checks must be a non-empty list of strings")
        if not data["checks"]:
            raise ValidationError("eval case checks must not be empty")
        if not isinstance(data["tags"], list) or not all(isinstance(item, str) for item in data["tags"]):
            raise ValidationError("eval case tags must be a list of strings")
        notes = data.get("notes", "")
        if not isinstance(notes, str):
            raise ValidationError("eval case notes must be a string when present")
        return cls(
            id=data["id"],
            suite=data["suite"],
            prompt=data["prompt"],
            checks=list(data["checks"]),
            tags=list(data["tags"]),
            notes=notes,
        )


@dataclass(frozen=True)
class CheckResult:
    name: str
    passed: bool
    message: str


@dataclass(frozen=True)
class RuntimeResult:
    text: str
    latency_ms: float
    raw_metadata: dict[str, Any] = field(default_factory=dict)
