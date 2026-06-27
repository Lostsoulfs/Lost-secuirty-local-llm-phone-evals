# Android Device Setup

V1 uses host-side Python plus read-only ADB. Native Android/Kotlin samples are
deferred until the host-side harness is stable.

## Official references

- Android Debug Bridge: https://developer.android.com/tools/adb
- Android Power Profiler: https://developer.android.com/studio/profile/power-profiler
- Android thermal status API: https://developer.android.com/reference/android/os/PowerManager.OnThermalStatusChangedListener
- LiteRT-LM Android API: https://developers.google.com/edge/litert-lm/android
- AI Edge Gallery: https://developers.google.com/edge/gallery
- AI Edge Gallery source: https://github.com/google-ai-edge/gallery
- Gemini Nano: https://developer.android.com/ai/gemini-nano
- ML Kit GenAI: https://developers.google.com/ml-kit/genai

## Device boundary

Set `PHONE_EVALS_DEVICE=1` before running device commands. Without that opt-in,
the CLI refuses device snapshots and pytest skips device tests.

Allowed V1 telemetry:

- ADB availability and authorized-device status.
- Device manufacturer, model, Android version, and SDK level.
- Hashed device serial.
- Battery level, plugged state, and temperature.
- Thermal service summary.
- Memory summary from `/proc/meminfo`.

Not allowed by default:

- Raw logcat dumps.
- Contacts, messages, photos, accounts, location history, browser data, or app
  private data.
- Rooting, factory reset, destructive ADB commands, sideloading untrusted APKs,
  or changing phone security settings.

## AI Edge Gallery runbook

1. Install AI Edge Gallery from the official Google source or release channel.
2. Record app source, version, release tag, and checksum if available in
   `MODEL_PROVENANCE.md`.
3. Download or select a model inside the app.
4. Record model name, source, license, version, quantization, and checksum when
   available.
5. Run built-in app benchmarks manually and store generated notes outside git
   under `reports/`.
6. Summarize only non-sensitive metrics in PRs or docs.

## First live-device commands

Run these only after the phone is connected, USB debugging is enabled, and the
ADB authorization prompt has been accepted on the device:

```powershell
$env:PHONE_EVALS_DEVICE = "1"
phone-evals doctor
phone-evals device snapshot --out reports/device
```

Keep `reports/` out of git. Summarize only non-sensitive metrics in follow-up
docs or PRs.
