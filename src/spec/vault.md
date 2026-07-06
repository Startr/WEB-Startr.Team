---
layout: default
title: "Vault"
description: "Timestamped, markdown-first artifact storage — the audit trail."
---

# The vault

Every run writes a timestamped directory of markdown. The vault is not logging;
it is the **audit trail** — what the agent read, decided, produced, and why, in
files a human opens and reads.

## Interface

```python
class Vault:
    def __init__(this, base_dir: str = "vault"): ...
    def create_run_dir(this, initial_prompt: str) -> str: ...
    def save_artifact(this, step_name: str, artifact_name: str, content: Any) -> str: ...
    def save_llm_transcript(
        this, operation_name: str, prompt: str, system_prompt: str,
        response: Any = None, metadata: dict | None = None,
    ) -> str: ...
```

## The run tree

```text
vault/
└── 20260703_141530_draft-the-launch-note/
    ├── 00_planning/
    │   ├── task_list.md               # or plan/ — a saved graph plan vault
    │   └── plan/…
    ├── 00_plan-trace/trace.md          # graph runs: every hop + rationale
    ├── 01_draft-the-note/
    │   └── 01_llm_response.md
    ├── 02_review-the-draft/…
    ├── 98_dispatch/delivery_record_dryrun.md   # [messaging]
    ├── 99_summary/final_answer.md
    └── llm_transcripts/
        ├── step-planning_1.md          # full system + user prompt + response
        └── action-tool-selection-nlt_1.md
```

## Guarantees

- **Markdown everywhere.** Non-string content serializes to fenced JSON/text;
  everything renders in any notes app.
- **One run, one directory**, named `YYYYMMDD_HHMMSS_<prompt-slug>` —
  chronological by construction.
- **Collision-free.** Artifact paths get incremental suffixes; the first
  artifact in a step folder takes the folder's name for readability.
- **Transcripts on demand.** With `verbose` or `debug`, every LLM exchange
  (system prompt, user prompt, metadata, response — including errors) is
  persisted under `llm_transcripts/`.

## Boundaries

The vault holds **run products**, which are disposable. Two things never live
in it: the [roll](/spec/messaging/) (private contact data, kept in `data/`)
and [plan vaults](/spec/graph-plans/) authored by humans (persistent,
version-controlled). `make things_clean` may wipe `vault/`; it must warn
before touching `data/`.
