---
layout: default
title: "Agent loop"
description: "The plan → act → answer loop: interface, guarantees, and the work_step seam."
---

# The agent loop

`startr_team.agent.Agent` orchestrates a run: decompose the request into steps,
work each step (tool or direct draft), then compose one final answer.

## Interface

```python
class Agent:
    def __init__(
        this,
        max_steps: int = 20,            # global action budget for the run
        max_steps_per_step: int = 5,    # actions allowed inside one step
        verbose: bool = False,          # token/latency logging + transcripts
        debug: bool = False,            # interactive prompt review before each call
        logger: Logger = None,
        interactive: bool = False,      # operator reviews/edits the plan first
        fallback_tool_call: Optional[Callable[[str], Optional[dict]]] = None,
    ): ...

    def run(this, query: str) -> str: ...
    def run_plan(this, plan, query: str = "") -> str: ...   # graph plans
```

## Phases

1. **Plan** — `plan_steps` asks the planning role for a short markdown
   checklist of atomic steps. An empty plan means the request is trivial:
   the loop skips straight to the answer phase. With `interactive=True`
   the operator approves or revises the plan before work starts.
2. **Act** — for each step, `work_step` loops (bounded by
   `max_steps_per_step`): NLT decides whether the step needs a registered
   tool; a selected tool is normalized, loop-guarded, executed, and its
   output recorded; when no tool is needed, the model drafts the step's
   work product directly and the step completes.
3. **Answer** — `generate_answer` composes the final result from the full
   run history, and the vault stores it as `99_summary/final_answer.md`.

## Guarantees

- **A vault checkpoint after every action.** Each tool result and each drafted
  step output is written to the run's vault before the loop continues.
- **Loop detection.** Four identical consecutive `tool:args` signatures inject
  a system warning into the history instead of executing a fifth time.
- **Budgets.** `max_steps` (global) and `max_steps_per_step` (local) stop
  runaway runs; a safety stop finalizes with the collected material and states
  why.
- **No hidden state.** All run state lives in an explicit `RunState`
  (`total_steps`, `run_history`, `artifact_counter`, safety flags).

## The `work_step` seam

`work_step(step, step_num, state, tools_scope=None, role="action")` is the act
phase both entry points share. `Agent.run` walks a linear checklist through
it; the [graph plan executor](/spec/graph-plans/) walks plan nodes through it,
passing each node's `tools:` scope and `role:` override. Anything that can
express its work as "a description plus context" can drive the same machinery.

## Extension seams

- `fallback_tool_call(step_description) -> dict | None` — invoked only when
  the model *claims* it lacks tool permission instead of working; a consumer
  who knows their tools can map the step to a call. The framework ships no
  default.
- Prompt overrides — see [Profile](/spec/profile/) and
  [Extending](/spec/extending/).
