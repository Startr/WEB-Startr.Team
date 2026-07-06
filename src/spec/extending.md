---
layout: default
title: "Extending"
description: "Recipes: build an agent, add a tool, add a channel, override prompts, machine-check a transition."
---

# Extending the framework

## Build a new agent

1. `pip install -e startr-team-py` (plus `[messaging]` if it sends).
2. Write an `agent.yaml` — name, mission, priorities, tone
   ([Profile](/spec/profile/)). Agents take singular they/them.
3. Register your tools ([Tools + NLT](/spec/tools-and-nlt/)).
4. `Agent().run(instruction)` — or author a plan vault and
   `Agent().run_plan("plans/…")`.

Domain lives in those three places. If you are editing the engine to make
your agent work, the engine has a bug — report it.

## Add a tool

```python
class LookupInput(BaseModel):
    ticket: str = Field(description="The ticket id, e.g. OPS-42.")

@tool(args_schema=LookupInput)
def lookup_ticket(ticket: str) -> str:
    """Fetch a ticket's current status and owner."""
    ...

register_tools(lookup_ticket)
```

The docstring and field descriptions **are** the NLT grid text — write them
for a reader deciding "do I need this now?", not for a parser.

## Add a channel

Implement the two methods, honor never-raise, register it:

```python
class MatrixChannel(Channel):
    name = "matrix"

    def validate_recipient(this, address):
        return address.startswith("@") and ":" in address

    def send(this, to, subject, body, fmt="markdown", metadata=None):
        try:
            ...  # deliver
            return SendResult(to=to, ok=True, detail="sent")
        except Exception as exc:
            return SendResult(to=to, ok=False, detail=f"matrix error: {exc}")

register_channel("matrix", MatrixChannel)
```

To give participants a matrix address, extend the roll model — `CHANNEL_KINDS`
and a column — in your repo's specialization.

## Override a prompt

Structural prompts are module attributes, read at call time:

```python
import startr_team.prompts as prompts

prompts.ANSWER_SYSTEM_PROMPT = prompts.PROFILE.persona_block() + """

You are composing the FINAL dispatch. The first line is "Subject:" then a
short, specific subject; then a blank line; then plain prose. …
"""
```

That is exactly how a herald turns the generic answer phase into a
subject-lined dispatch. Persona stays in `agent.yaml`; only structure moves.

## Machine-check a transition

When an edge condition is checkable in code, take it away from the LLM:

```python
from startr_team.plans import register_predicate

register_predicate("tests pass", lambda ctx: run_tests().ok)
```

Predicates always win over NLT judgment ([Graph plans](/spec/graph-plans/)).

## Consumer specializations

A consumer repo may go further — Lia Fáil layers a Crown/Court/Realm role
vocabulary and contract links onto the roll, and adds IMAP intake. The rule
of thumb: **specialize by wrapping and registering, not by forking the
engine.** When two consumers grow the same wrapper, propose it upstream to
the spec.
