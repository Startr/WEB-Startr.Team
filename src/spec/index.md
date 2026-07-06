---
layout: default
title: "Specification"
description: "The Startr.Team agent framework specification — contracts, guarantees, and extension seams."
---

# Startr.Team Agent Framework — Specification

**Status:** Draft v0.1.0 · **License:** Apache-2.0 ·
**Reference implementation:** [`startr-team` (Python)](https://github.com/Startr/startr-team-py)

This spec describes a small agent framework with an unusual set of priorities:
every run is **auditable** (markdown vault), plans are **human-editable**
(wikilinked markdown graphs), tool selection is **natural language first**
(NLT), and outbound action is **gated** (a human holds the send switch). It was
extracted from two working agents — Downes (education) and Lia Fáil (a
governance herald) — that had independently converged on the same engine.

## Architecture

```text
agent.yaml ──► AgentProfile ──► persona block in every system prompt
                                        │
 instruction ──► Agent.run() ───────────┤
                 1. plan   (steps, or a graph plan)
                 2. act    (per step: NLT selects a tool, or draft directly)
                 3. answer (compose the final result)
                                        │
                 Vault ◄── every artifact, transcript, and trace
                                        │
      [messaging] Roll ──► resolve recipients ──► clean ──► deliver()
                                            (dry-run first; human gates --send)
```

Two install surfaces:

- **core** — the loop, profile, LLM interface, tools + NLT, vault, graph plans.
- **`[messaging]` extra** — channels, the roll, gated dispatch, cleanup pipeline.

## The contracts

| Page | Contract |
| --- | --- |
| [Agent loop](/spec/agent-loop/) | `Agent.run()` — plan → act → answer, safety guards, the `work_step` seam |
| [Readable code](/spec/style/) | House style: `this`, narrating helpers, why |
| [Profile](/spec/profile/) | `agent.yaml` → `AgentProfile` → every prompt |
| [LLM interface](/spec/llm-interface/) | `call_llm` — provider-agnostic, per-role overrides |
| [Tools + NLT](/spec/tools-and-nlt/) | The registry, `@tool` convention, NLT-first selection |
| [Vault](/spec/vault/) | Run directories, artifacts, LLM transcripts |
| [Graph plans](/spec/graph-plans/) | Plans as wikilinked markdown vaults; loops, budgets, resume |
| [Messaging](/spec/messaging/) | `Channel` ABC, the roll, gated dispatch |
| [Configuration](/spec/config/) | The full environment surface |
| [Extending](/spec/extending/) | Recipes: new tool, new channel, new agent |
| [Examples](/spec/examples/) | The runnable examples, rendered from source |

## Design positions

1. **Audit is a feature, not a log level.** Everything the agent reads,
   decides, and produces lands in the vault as markdown a human can read.
2. **NLT-first.** JSON function calling is a pluggable alternative, not the
   default. Small, local decisions in plain language beat schema serialization,
   especially on small models.
3. **Plans belong to people.** A plan you cannot open, read, and edit in your
   notes app is a plan you do not really control. Code-defined graphs
   (LangGraph et al.) are powerful; ours are legible.
4. **The LLM composes; it never sends.** Delivery is deterministic code with a
   dry-run default.
5. **One engine, many agents.** Domain lives in `agent.yaml`, the tool
   registry, and (optionally) overridden prompts — never in the engine.
