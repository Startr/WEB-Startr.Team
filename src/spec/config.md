---
layout: default
title: "Configuration"
description: "The full environment surface — LLM, roles, persona, roll, channels."
---

# Configuration

Everything configures through environment variables (a `.env` next to your
project works — the reference examples load it when `python-dotenv` is
present). Each subsystem owns its prefix.

## LLM

| Variable | Meaning | Default |
| --- | --- | --- |
| `OPENAI_API_KEY` | API key (relaxed automatically for localhost base URLs) | — |
| `OPENAI_BASE_URL` / `OPENAI_API_BASE` | OpenAI-compatible endpoint (OpenRouter, Ollama, llama.cpp) | OpenAI |
| `LLM_MODEL` | Model name | `gpt-4.1` |
| `LLM_TEMPERATURE` | Temperature | `0` |

## Per-role overrides

For any role — the engine's (`planning`, `action`, `answer`, `transition`) or
one a [graph plan node](/spec/graph-plans/) declares via `role:`:

| Variable | Meaning |
| --- | --- |
| `LLM_{ROLE}_MODEL` | Model for this role |
| `LLM_{ROLE}_BASE_URL` | Endpoint for this role |
| `LLM_{ROLE}_API_KEY` | Key for this role |
| `LLM_{ROLE}_TEMPERATURE` | Temperature for this role |

Example — cheap local drafting, strong judgment:

```bash
OPENAI_BASE_URL=http://localhost:11434/v1
LLM_MODEL=deepseek-r1:14b
LLM_REVIEW_MODEL=gpt-4.1
LLM_REVIEW_BASE_URL=https://openrouter.ai/api/v1
LLM_REVIEW_API_KEY=sk-or-...
```

## Persona

| Variable | Meaning | Default |
| --- | --- | --- |
| `AGENT_PROFILE` | Path to `agent.yaml` | `./agent.yaml`, then repo root, then defaults |

## Roll (`[messaging]`)

| Variable | Meaning | Default |
| --- | --- | --- |
| `STARTR_TEAM_DATA_DIR` | Directory holding `participants.csv` | `data` |

## Channels (`[messaging]`)

| Variable | Channel | Meaning |
| --- | --- | --- |
| `SMTP_HOST` / `SMTP_PORT` | email | Server (port default 587, STARTTLS) |
| `SMTP_USERNAME` / `SMTP_PASSWORD` | email | Login (app passwords work) |
| `DISPATCH_FROM_EMAIL` | email | From address (falls back to username) |
| `SIGNAL_CLI_PATH` | signal | Binary path (default `signal-cli`) |
| `SIGNAL_FROM_NUMBER` | signal | The registered account (E.164) |
| `WUZAPI_URL` / `WUZAPI_TOKEN` | whatsapp | Self-hosted wuzapi gateway |

An unconfigured channel is not an error at import — it reports
`SendResult(ok=False, detail="… not configured …")` at send time, and dry-run
still validates recipients.

The reference repo ships a documented [`env.example`](https://github.com/Startr/startr-team-py/blob/develop/env.example).
