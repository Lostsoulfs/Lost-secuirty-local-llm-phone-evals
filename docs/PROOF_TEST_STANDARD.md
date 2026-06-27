# Proof Test Standard

Every new eval, check, or adapter must prove two things:

1. A safe fixture passes for the intended reason.
2. A planted-bad fixture fails for the intended reason.

## Required evidence

- JSONL eval cases must be loadable by `phone_eval_kit.cases`.
- Each check listed by a case must exist in `phone_eval_kit.checks`.
- Proof tests must reject deliberately unsafe, malformed, or sensitive-looking
  outputs for the relevant failure mode.
- Reports must not persist raw sensitive-looking output.

This standard is a current proof baseline, not a total correctness proof. It
shows that the harness catches fixture-defined failures under current tooling.
