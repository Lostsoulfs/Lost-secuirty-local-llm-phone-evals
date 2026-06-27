## Scope

What changed and why:

## AI assistance

- [ ] No AI-assisted code
- [ ] AI-assisted code present

If present, list the AI-assisted files or areas:

## Risk area

- [ ] Docs only
- [ ] Tests or harnesses
- [ ] Runtime adapter
- [ ] Device or ADB behavior
- [ ] Security, privacy, or redaction
- [ ] Dependency or CI

## Proof and limits

- [ ] Safe fixture passes
- [ ] Planted-bad control fails
- [ ] Report redaction checked
- [ ] Claims are scoped to the current proof baseline

Known limits or skipped surfaces:

## Verification

- [ ] `python -m pytest`
- [ ] `phone-evals proof`
- [ ] `python tools/scan_staged.py --self-test`
- [ ] Device tests skipped intentionally or run with `PHONE_EVALS_DEVICE=1`
