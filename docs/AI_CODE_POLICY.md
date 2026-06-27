# AI-Assisted Code Review Policy

AI-assisted code is useful, but it is not trusted by default.

Required for AI-assisted changes:

1. State what was AI-assisted.
2. Trace the implementation to real repo files and tests.
3. Run the relevant proof checks.
4. Keep claims scoped to observed behavior.
5. Do not bypass security, CI, provenance, or review rules.

For eval or test changes, use `docs/AI_AUTHORED_TEST_AUDIT.md`. AI-authored or
AI-assisted tests are untrusted until safe fixtures and planted-bad controls show
that the test catches the named failure mode.
