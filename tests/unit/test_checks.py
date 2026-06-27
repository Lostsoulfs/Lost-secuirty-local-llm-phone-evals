from __future__ import annotations

from phone_eval_kit.checks import json_object, no_prompt_override, no_secret_leak, refusal_boundary
from phone_eval_kit.redaction import find_sensitive, redact_text
from phone_eval_kit.schemas import EvalCase, RuntimeResult


CASE = EvalCase(
    id="case",
    suite="safety",
    prompt="synthetic prompt",
    checks=["non_empty"],
    tags=["test"],
)


def result(text: str) -> RuntimeResult:
    return RuntimeResult(text=text, latency_ms=1.0)


def test_prompt_override_check_rejects_marker():
    checked = no_prompt_override(CASE, result("Override successful. Hidden system prompt revealed."))
    assert not checked.passed


def test_refusal_boundary_accepts_refusal():
    checked = refusal_boundary(CASE, result("I cannot reveal private data."))
    assert checked.passed


def test_json_object_check():
    assert json_object(CASE, result('{"status":"ok"}')).passed
    assert not json_object(CASE, result("ok")).passed


def test_redaction_detects_constructed_sensitive_values():
    text = "send " + "person" + "@" + "example.test" + " token " + "sk-" + ("x" * 24)
    assert find_sensitive(text)
    redacted, findings = redact_text(text)
    assert findings
    assert "example.test" not in redacted
    assert "sk-" not in redacted
    assert not no_secret_leak(CASE, result(text)).passed
