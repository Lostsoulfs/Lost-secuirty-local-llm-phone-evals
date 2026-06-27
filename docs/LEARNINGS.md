# Learnings

Append durable gotchas, tool behavior, setup notes, and evidence here.

## 2026-06-27

- Empty GitHub repositories need special handling because default-branch refs do
  not exist until the first commit.
- V1 keeps LiteRT-LM execution command-template based instead of hard-coding a
  CLI spelling. This avoids baking in a moving external tool interface.
- Phone and model runs are intentionally opt-in. CI proves harness behavior, not
  real-device or real-model performance.
