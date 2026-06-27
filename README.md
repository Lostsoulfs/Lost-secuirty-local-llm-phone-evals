# Lost Security Local LLM Phone Evals

Google-first local LLM phone evaluation kit for Android devices, with the Galaxy
S26 Ultra 1TB class device as the primary baseline. V1 is host-side Python plus
ADB: no Kotlin app code is required for the initial harness.

The repo tests safety and performance signals for local/on-device LLM runs:
prompt injection, privacy leakage, refusal boundaries, output contracts,
latency, repeatability, and read-only device telemetry.

## What this repo is

- A local evaluation harness for phone-hosted or phone-adjacent LLM runs.
- A proof-oriented test kit with safe fixtures and planted-bad controls.
- A place to document Google-first Android targets: LiteRT-LM, AI Edge Gallery,
  Gemini Nano/AICore, and ML Kit GenAI.
- Dependency-permissive, as long as dependencies are documented and useful.

## What this repo is not

- Not a model-weight repository.
- Not an APK store.
- Not a cloud eval service.
- Not a device-management or phone-forensics toolkit.
- Not a claim that any model, app, or phone is safe in all cases.

## Quickstart

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest
phone-evals proof
phone-evals doctor
```

Run a safe local smoke report with the fake runtime:

```powershell
phone-evals run --runtime fake --suite safety --out reports/local
```

Run a read-only ADB snapshot only after opting in:

```powershell
$env:PHONE_EVALS_DEVICE = "1"
phone-evals device snapshot --out reports/device
```

## Command surface

```text
phone-evals doctor
phone-evals run --runtime fake --suite safety --out reports/local
phone-evals run --runtime litert-lm --suite safety --model-path models/gemma-local --command-json "[\"your-litert-command\", \"--model\", \"{model_path}\"]" --out reports/litert
phone-evals device snapshot --out reports/device
phone-evals proof
```

`litert-lm` execution is intentionally command-template based in V1 because
Google's tooling surface can move faster than this repo. Configure the local
command through `PHONE_EVALS_LITERT_LM_COMMAND_JSON` or
`--command-json`; prompts are passed on stdin instead of interpolated into a
shell command.

## Layout

```text
phone_eval_kit/       Python CLI, adapters, checks, reports, ADB helpers
phone_eval_kit/evals/ Built-in JSONL eval suites
tests/                Unit, proof, and opt-in device tests
tools/                Scanner and proof/report wrappers
docs/                 Reviewer, Android setup, eval design, and policy docs
MODEL_PROVENANCE.md   Model/tool source, license, and checksum log
```

## Main docs

- `docs/REVIEWER_QUICKSTART.md` - review path and current proof limits.
- `docs/EVAL_DESIGN.md` - eval case and report interfaces.
- `docs/HARNESS_CATALOG.md` - production-grade harness inventory.
- `docs/DEVICE_SETUP_ANDROID.md` - Android and ADB setup boundaries.
- `docs/HARDWARE_BASELINE.md` - Galaxy S26 Ultra 1TB baseline assumptions.
- `docs/PROOF_TEST_STANDARD.md` - safe fixture plus planted-bad proof rule.
- `docs/AI_AUTHORED_TEST_AUDIT.md` - checklist for AI-assisted test trust.
- `MODEL_PROVENANCE.md` - model, app, and runtime provenance log.

## 2026 target sources

- LiteRT-LM overview: https://developers.google.com/edge/litert-lm/overview
- LiteRT-LM Android API: https://developers.google.com/edge/litert-lm/android
- AI Edge Gallery: https://developers.google.com/edge/gallery
- AI Edge Gallery source: https://github.com/google-ai-edge/gallery
- Gemini Nano: https://developer.android.com/ai/gemini-nano
- ML Kit GenAI: https://developers.google.com/ml-kit/genai
- Android Debug Bridge: https://developer.android.com/tools/adb
- Android Power Profiler: https://developer.android.com/studio/profile/power-profiler
- Samsung Galaxy S26 Ultra: https://www.samsung.com/us/smartphones/galaxy-s26-ultra/
- Samsung device comparison support: https://www.samsung.com/us/support/answer/ANS10010342/
- OWASP Top 10 for LLM Applications: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- NIST AI Risk Management Framework: https://www.nist.gov/itl/ai-risk-management-framework
