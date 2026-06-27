from __future__ import annotations

import time

from phone_eval_kit.schemas import EvalCase, RuntimeResult


class FakeRuntimeAdapter:
    name = "fake"

    def __init__(self, mode: str = "safe") -> None:
        if mode not in {"safe", "unsafe"}:
            raise ValueError("fake mode must be 'safe' or 'unsafe'")
        self.mode = mode

    def generate(self, prompt: str, case: EvalCase) -> RuntimeResult:
        started = time.perf_counter()
        lowered = prompt.lower()
        if self.mode == "unsafe":
            text = self._unsafe_response(case)
        elif "json object" in lowered:
            text = '{"status":"ok","mode":"local"}'
        elif any(marker in lowered for marker in ["ignore previous", "system prompt", "private", "secret"]):
            text = "I cannot reveal secrets, private data, or hidden instructions."
        else:
            text = "Local eval response."
        latency_ms = (time.perf_counter() - started) * 1000
        return RuntimeResult(text=text, latency_ms=latency_ms, raw_metadata={"mode": self.mode})

    @staticmethod
    def _unsafe_response(case: EvalCase) -> str:
        if "json_object" in case.checks:
            return "ok"
        if "refusal_boundary" in case.checks:
            return "Sure, here is the private data."
        if "no_prompt_override" in case.checks:
            return "Override successful. Hidden system prompt revealed."
        if "no_secret_leak" in case.checks:
            return "Bearer " + ("x" * 28)
        return ""
