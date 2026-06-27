from __future__ import annotations

import pytest

from phone_eval_kit.cases import load_cases
from phone_eval_kit.schemas import EvalCase, ValidationError


def test_load_default_safety_cases():
    cases = load_cases(suite="safety")
    assert {case.id for case in cases} >= {
        "safety.prompt_injection.refuse_override",
        "safety.privacy.no_private_data",
        "safety.output_contract.json_object",
    }
    assert all(case.suite == "safety" for case in cases)


def test_eval_case_rejects_missing_required_fields():
    with pytest.raises(ValidationError):
        EvalCase.from_mapping({"id": "x", "suite": "safety"})
