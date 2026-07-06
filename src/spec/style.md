---
layout: default
title: "Readable code"
description: "House style: this instead of self, narrating helper names, and why."
---

# Readable code

Startr.Team code narrates. Two conventions carry that:

## `this`, not `self`

Methods take `this` as their receiver:

```python
def create_run_dir(this, initial_prompt: str):
    this.run_dir = os.path.join(this.base_dir, ...)
```

Python permits any name for the first parameter; `self` is only convention
(PEP 8). We choose `this` deliberately:

- **Grammar.** `self` is a reflexive pronoun — English never uses it as a
  possessor ("self's vault" is not a sentence). `this` is a demonstrative:
  `this.vault` reads as "this agent's vault", and
  `this.llm.plan_steps(query)` parses as an English clause.
- **Model priors.** Language models have seen orders of magnitude more `this`
  (JavaScript, TypeScript, Java, C#, C++, PHP) than `self`. This framework's
  code crosses into LLM context constantly — vault transcripts, prompts, spec
  pages — so the token models already bind to "the current entity" wins.
- **Lineage.** It sits beside the HyperTalk-style helpers below; `self` would
  be the inconsistency.

Tooling: `ruff` is configured with `N805` ignored. One line in `ruff.toml`,
documented in the reference repo's README.

## Narrating helpers

Steps of a procedure are named as actions with articles, so call sites read as
instructions to a person:

```python
result = run_the_tool(tool_to_run, tool_name, optimized_args, this)
save_the_artifact(this, current_step, step_num, tool_name, result, counter)
record_the_outcome(state.run_history, output)
```

The test is simple: **read the loop body aloud.** If it does not make sense as
spoken English, rename until it does.

## What this is not

Not a license for cuteness. Names still say exactly what happens; the
narration is a constraint (plain, accurate English), not decoration.
