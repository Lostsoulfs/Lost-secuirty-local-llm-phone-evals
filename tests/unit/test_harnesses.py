from __future__ import annotations

from phone_eval_kit.cases import load_cases
from phone_eval_kit.harnesses import HARNESS_REGISTRY, harness_ids


def test_five_production_harnesses_are_registered():
    assert harness_ids() == {
        "prompt_injection_boundary",
        "privacy_secret_leakage",
        "output_schema_contract",
        "latency_repeatability_smoke",
        "adb_device_telemetry_boundary",
    }
    assert len(HARNESS_REGISTRY) == 5


def test_harness_safe_fixtures_exist_for_jsonl_suites():
    cases = {case.id for case in [*load_cases(suite="safety"), *load_cases(suite="performance")]}
    jsonl_harnesses = [harness for harness in HARNESS_REGISTRY if harness.suite in {"safety", "performance"}]
    assert jsonl_harnesses
    assert {harness.safe_fixture for harness in jsonl_harnesses}.issubset(cases)
