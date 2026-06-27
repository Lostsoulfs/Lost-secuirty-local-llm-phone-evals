from __future__ import annotations

from typing import Protocol

from phone_eval_kit.schemas import EvalCase, RuntimeResult


class RuntimeAdapter(Protocol):
    name: str

    def generate(self, prompt: str, case: EvalCase) -> RuntimeResult:
        ...
