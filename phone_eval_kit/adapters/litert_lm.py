from __future__ import annotations

import json
import os
import shlex
import subprocess
import time
from pathlib import Path

from phone_eval_kit.schemas import EvalCase, RuntimeResult


class LiteRTLMCommandAdapter:
    name = "litert-lm"

    def __init__(
        self,
        model_path: str | None,
        command_json: str | None = None,
        timeout_seconds: int = 120,
    ) -> None:
        self.model_path = model_path
        self.command_json = command_json or os.environ.get("PHONE_EVALS_LITERT_LM_COMMAND_JSON")
        self.timeout_seconds = timeout_seconds

    def generate(self, prompt: str, case: EvalCase) -> RuntimeResult:
        if not self.command_json:
            raise RuntimeError(
                "LiteRT-LM command JSON is not configured. Set "
                "PHONE_EVALS_LITERT_LM_COMMAND_JSON or pass --command-json."
            )
        command = self._load_command()
        started = time.perf_counter()
        completed = subprocess.run(
            command,
            input=prompt,
            text=True,
            capture_output=True,
            timeout=self.timeout_seconds,
            check=False,
        )
        latency_ms = (time.perf_counter() - started) * 1000
        if completed.returncode != 0:
            stderr = completed.stderr.strip().splitlines()[:3]
            raise RuntimeError(f"LiteRT-LM command failed with exit {completed.returncode}: {' | '.join(stderr)}")
        return RuntimeResult(
            text=completed.stdout.strip(),
            latency_ms=latency_ms,
            raw_metadata={"command": command[0], "stderr_lines": len(completed.stderr.splitlines())},
        )

    def _load_command(self) -> list[str]:
        assert self.command_json is not None
        try:
            parsed = json.loads(self.command_json)
            if not isinstance(parsed, list) or not all(isinstance(item, str) for item in parsed):
                raise ValueError
            return [self._format_arg(item) for item in parsed]
        except json.JSONDecodeError:
            return [self._format_arg(item) for item in shlex.split(self.command_json)]

    def _format_arg(self, value: str) -> str:
        model_path = str(Path(self.model_path)) if self.model_path else ""
        return value.format(model_path=model_path)
