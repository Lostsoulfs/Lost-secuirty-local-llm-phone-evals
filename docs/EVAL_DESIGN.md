# Eval Design

This repo uses small inspectable eval cases with explicit checks and generated
JSON reports.

## Eval case JSONL

Each non-empty line is a JSON object with:

- `id`: stable case id.
- `suite`: suite name such as `safety` or `performance`.
- `prompt`: synthetic prompt text.
- `checks`: list of check names.
- `tags`: short labels for filtering and review.
- `notes`: optional short note.

Built-in cases live in `phone_eval_kit/evals/`.

## V1 harnesses

The current production harnesses are listed in `docs/HARNESS_CATALOG.md` and
registered in `phone_eval_kit.harnesses`. New harnesses should update both
places unless they are experimental.

## Report JSON

Reports include:

- `run_id`
- `timestamp_utc`
- `runtime`
- `model_id`
- `device_snapshot`
- `case_results`
- `metrics`
- `redaction_status`

Reports store a prompt hash instead of the raw prompt. Runtime output is redacted
before writing.

## Runtime adapters

- `fake`: deterministic local adapter used by tests and proof checks.
- `litert-lm`: Google-first command adapter. Use a local trusted command JSON
  template and pass prompts on stdin.
- `openai-compatible`: optional endpoint adapter for local servers. It is not a
  default CI dependency and should be used only against local/operator-approved
  endpoints.
