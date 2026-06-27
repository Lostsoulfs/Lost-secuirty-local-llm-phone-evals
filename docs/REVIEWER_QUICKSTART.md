# Reviewer Quickstart

This repo is a local LLM phone evaluation kit. The useful review question is:

"Does each eval show a reproducible safe case, a reproducible bad case, and a
report that avoids persisting sensitive data?"

## What the repo proves

- The current proof baseline can load built-in JSONL eval cases.
- The fake runtime passes safe fixtures under deterministic conditions.
- Planted-bad outputs fail the intended checks.
- Reports include required top-level fields and redact sensitive-looking output.
- Device tests are opt-in and skipped unless `PHONE_EVALS_DEVICE=1`.

## What the repo does not prove

- It does not prove a real model is safe.
- It does not prove the Galaxy S26 Ultra, AI Edge Gallery, LiteRT-LM, Gemini
  Nano, or ML Kit GenAI is safe in all cases.
- It does not replace live device QA, model licensing review, or app security
  review.
- It does not benchmark real models in CI.

## Core verification commands

```powershell
python -m pytest
python -m phone_eval_kit proof
python tools/scan_staged.py --self-test
```

After editable install:

```powershell
phone-evals proof
phone-evals doctor
```

Run real device commands only when intended:

```powershell
$env:PHONE_EVALS_DEVICE = "1"
phone-evals device snapshot --out reports/device
```

## Inspect one eval

1. Open `phone_eval_kit/evals/safety.jsonl`.
2. Pick one case.
3. Confirm the prompt is synthetic and does not contain real private data.
4. Confirm each listed check exists in `phone_eval_kit/checks.py`.
5. Confirm the proof baseline includes a bad output that fails the check.
6. Confirm generated reports store redacted output and prompt hashes instead of
   raw prompts.
