# CLAUDE.md - local LLM phone evals notes

Follow `AGENTS.md` for the repo contract. `AGENTS.md` is the canonical
cross-tool source of truth.

## Claude-specific notes

- Read `SECURITY.md` before writes, installs, permission changes, device
  commands, generated artifacts, or outbound messages.
- For subagents, tell them to read `AGENTS.md`, `SECURITY.md`, and
  `docs/LEARNINGS.md` first, then report verified versus assumed facts.
- Do not edit `.claude/`, hooks, settings, or agent permissions unless
  explicitly asked.
- If push or a tool call is blocked, report the exact blocker and the next safe
  option. Do not claim persistence until the remote branch or commit is
  verified.
