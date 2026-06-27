from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request

from phone_eval_kit.schemas import EvalCase, RuntimeResult


class OpenAICompatibleAdapter:
    name = "openai-compatible"

    def __init__(
        self,
        api_base: str,
        model: str,
        api_key_env: str = "PHONE_EVALS_OPENAI_COMPATIBLE_API_KEY",
        timeout_seconds: int = 120,
    ) -> None:
        self.api_base = api_base.rstrip("/")
        self.model = model
        self.api_key_env = api_key_env
        self.timeout_seconds = timeout_seconds

    def generate(self, prompt: str, case: EvalCase) -> RuntimeResult:
        body = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
        }
        data = json.dumps(body).encode("utf-8")
        request = urllib.request.Request(
            f"{self.api_base}/v1/chat/completions",
            data=data,
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        api_key = os.environ.get(self.api_key_env)
        if api_key:
            request.add_header("Authorization", f"Bearer {api_key}")
        started = time.perf_counter()
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            raise RuntimeError(f"OpenAI-compatible endpoint request failed: {exc}") from exc
        latency_ms = (time.perf_counter() - started) * 1000
        try:
            text = payload["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError("OpenAI-compatible endpoint returned an unsupported response shape") from exc
        return RuntimeResult(text=str(text), latency_ms=latency_ms, raw_metadata={"model": self.model})
