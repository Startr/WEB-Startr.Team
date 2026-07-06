---
layout: default
title: "LLM interface"
description: "call_llm — one function, any OpenAI-compatible provider, per-role model routing."
---

# LLM interface

One function talks to the model. It works against any OpenAI-compatible API
and routes per-role so different phases can use different models.

## Interface

```python
def call_llm(
    prompt: str,
    model: Optional[str] = None,        # highest-precedence override
    system_prompt: Optional[str] = None,
    tools: Optional[List[BaseTool]] = None,  # structured-calling path only
    verbose: bool = False,
    role: Optional[str] = None,         # "planning" | "action" | "answer" | any
) -> AIMessage: ...

def get_llm_config(role: Optional[str] = None) -> dict: ...
```

## Provider-agnostic

| Provider | Setup |
| --- | --- |
| OpenAI | `OPENAI_API_KEY` |
| OpenRouter | `OPENAI_API_KEY` + `OPENAI_BASE_URL=https://openrouter.ai/api/v1` |
| Ollama | `OPENAI_BASE_URL=http://localhost:11434/v1` + `LLM_MODEL=...` |
| llama.cpp | `OPENAI_BASE_URL=http://localhost:8080/v1` |

A localhost base URL relaxes the API-key requirement automatically.

## Per-role routing

Any role name maps to a family of overrides checked before the base config:

```text
LLM_{ROLE}_MODEL   LLM_{ROLE}_BASE_URL   LLM_{ROLE}_API_KEY   LLM_{ROLE}_TEMPERATURE
```

Precedence: explicit `model` argument > role override > base env var > default.

The engine uses roles `planning`, `action`, `answer`, and `transition` (graph
edge judgments). **Graph plan nodes mint their own roles** via `role:`
frontmatter — a node with `role: review` routes through `LLM_REVIEW_*`, so a
strong model can judge while a cheap local model drafts, declared in the plan
itself.

## Guarantees

- Three attempts with backoff on transient connection errors.
- Braces in system prompts are escaped before templating, so prompts may
  contain literal JSON examples safely.
- With `verbose`, latency and token usage print per call, and `call_llm_safe`
  writes the full exchange to the vault as a transcript.

## Structured-calling path

`tools=` binds LangChain tools for JSON function calling — the pluggable
alternative to the default [NLT path](/spec/tools-and-nlt/). The engine itself
never passes `tools=`; it selects with NLT and executes selected tools in
plain code.
