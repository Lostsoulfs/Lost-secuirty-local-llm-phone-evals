# Next Operator Steps

These steps require local hardware, app installation, or model downloads. They
are intentionally not run in CI.

## 1. Prepare the Galaxy S26 Ultra

1. Install Android platform tools or otherwise make `adb` available on `PATH`.
2. Enable Developer Options and USB debugging on the phone.
3. Connect the phone by USB and accept the ADB authorization prompt on-device.
4. Verify the host can see the phone:

```powershell
adb devices
phone-evals doctor
```

## 2. Capture the first read-only device snapshot

```powershell
$env:PHONE_EVALS_DEVICE = "1"
phone-evals device snapshot --out reports/device
```

Do not commit `reports/`. The snapshot should only contain the allowed fields
from `docs/DEVICE_SETUP_ANDROID.md`.

## 3. Record model and app provenance

Before running real model tests, update `MODEL_PROVENANCE.md` with:

- AI Edge Gallery app source/version or release tag.
- LiteRT-LM tool source/version when installed.
- Model name, provider, license, quantization, checksum if available, and local
  path pattern.

Never commit model files, APKs, private logs, or raw generated reports.

## 4. Run first Google-first local eval

Use AI Edge Gallery or LiteRT-LM first. For LiteRT-LM-style local command runs,
configure the command template and run:

```powershell
$env:PHONE_EVALS_LITERT_LM_COMMAND_JSON = '["your-litert-command", "--model", "{model_path}"]'
phone-evals run --runtime litert-lm --suite safety --model-path models/gemma-local --out reports/litert
```

The command template is intentionally local because Google runtime command names
and install paths can change.

## 5. Optional local endpoint lane

After the Google-first path works, test an operator-approved local
OpenAI-compatible endpoint:

```powershell
phone-evals run --runtime openai-compatible --api-base http://127.0.0.1:8080 --api-model local-model --suite safety --out reports/local-endpoint
```

Use only local endpoints or explicitly approved sinks.

## Current blocking facts

- ADB was not available on this host during bootstrap verification.
- LiteRT-LM command tooling was not configured on this host during bootstrap
  verification.
- No real model run has been attempted yet.
