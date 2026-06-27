# Learnings

Append durable gotchas, tool behavior, setup notes, and evidence here.

## 2026-06-27

- Empty GitHub repositories need special handling because default-branch refs do
  not exist until the first commit.
- V1 keeps LiteRT-LM execution command-template based instead of hard-coding a
  CLI spelling. This avoids baking in a moving external tool interface.
- Phone and model runs are intentionally opt-in. CI proves harness behavior, not
  real-device or real-model performance.
- The empty repo bootstrap had to create `main` directly before normal PR flow
  could work, because GitHub needs an existing base branch for PRs.
- CI now checks pytest, proof, report generation, whitespace, scanner self-test,
  and a repo-wide sensitive-data scan.
