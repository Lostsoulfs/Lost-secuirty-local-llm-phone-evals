# Runtime Targets - 2026 Baseline

This repo starts with Google-first Android/on-device model targets and keeps
other local runtimes as optional adapters.

## First-class targets

- LiteRT-LM: production-oriented orchestration layer for running LLMs with
  LiteRT. Source: https://developers.google.com/edge/litert-lm/overview
- AI Edge Gallery: Google app and source project for on-device AI experiments
  and benchmarking. Sources: https://developers.google.com/edge/gallery and
  https://github.com/google-ai-edge/gallery
- Gemini Nano/AICore: Android on-device Gemini Nano API surface. Source:
  https://developer.android.com/ai/gemini-nano
- ML Kit GenAI: Google ML Kit generative AI APIs for Android. Source:
  https://developers.google.com/ml-kit/genai

## Optional later targets

- Local OpenAI-compatible HTTP endpoints, including llama.cpp server-style
  flows. Source: https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md
- Promptfoo, lm-evaluation-harness, and OpenAI eval workflows as optional
  benchmark integrations, not mandatory CI.

## V1 decision

No native Android/Kotlin sample is included in V1. The host-side harness and ADB
telemetry need to stabilize first.

## Local endpoint lane

The `openai-compatible` adapter is present for local/operator-approved servers
only. It should be used for local endpoints such as llama.cpp server-style flows
after the Google-first phone path is verified.
