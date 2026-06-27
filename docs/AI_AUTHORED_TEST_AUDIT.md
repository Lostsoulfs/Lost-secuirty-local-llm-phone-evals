# AI-Authored Test Audit Checklist

AI-assisted tests are useful, but authorship is not evidence. Review the fixture
logic and the failure mode directly.

## Triage checklist

- The eval names one specific failure mode it catches.
- The safe fixture passes for the intended reason.
- The planted-bad fixture fails for the intended reason.
- The bad fixture is deterministic and does not rely on uncontrolled network,
  timing, or phone state.
- The paired unit or proof test covers public behavior.
- The test would fail if the core check were deleted, inverted, or replaced by a
  no-op.
- Coverage is not treated as proof by itself.
- Claims in docs match actual fixture behavior.
- Limitations and unsampled areas are stated when the eval is narrow.

## Common failure modes

| Failure mode | Review signal |
| --- | --- |
| Hallucinated API | Test assumes tools, CLIs, schemas, or model behavior not in the repo. |
| Weak fixture | Safe and bad examples are too similar or do not exercise the named risk. |
| Missing planted-bad control | Test only shows the happy path. |
| Wrong claim | Docs say the eval proves more than the fixture shows. |
| Sensitive fixture | Test embeds raw secrets, personal data, phone logs, or private prompts. |
