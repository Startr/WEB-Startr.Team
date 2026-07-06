---
layout: default
title: "Tools + NLT"
description: "The tool registry and natural-language tool selection — why NLT is the default."
---

# Tools and NLT

The framework ships an **empty tool registry**; consumers define tools with
LangChain's `@tool` decorator and register them once. Selection is **NLT-first**:
the engine asks a plain-text YES/NO grid which tools a step needs, instead of
binding JSON schemas.

## Defining and registering a tool

```python
from langchain_core.tools import tool
from pydantic import BaseModel, Field

class ResolveAudienceInput(BaseModel):
    audience: str = Field(description="A name, alias, group label, or comma-separated list.")

@tool(args_schema=ResolveAudienceInput)
def resolve_audience(audience: str) -> str:
    """Resolve a name/alias/group to people and how to reach them."""
    ...

from startr_team.tools import register_tools
register_tools(resolve_audience)
```

## Registry interface

```python
def register_tools(*tools) -> None: ...          # idempotent by tool name
def set_tools(tools) -> None: ...                # replace (tests)
def all_tools() -> tuple[BaseTool, ...]: ...
def get_tool(name: str) -> BaseTool | None: ...
def tool_specs(names: list[str] | None = None) -> list[ToolSpec]: ...  # NLT bridge
def invoke_tool(tool, args) -> Any: ...          # invoke → run → call, in order
```

`tool_specs(names)` scopes the grid: a [graph plan node](/spec/graph-plans/)
listing `tools: [fetch_url]` presents a one-row grid at that node — shorter
grids select more accurately, especially on small models.

## Why NLT is the default

[nlt-py](https://github.com/Startr/nlt-py) replaces structured function
calling with two natural-language phases: a YES/NO relevance grid over all
tools, then per-tool argument extraction. Validated across 14 models and 8,560
trials: **+14.9pp selection accuracy, 93% fewer errors, 25.2% token savings** —
and the gap is widest on small/open models, which is exactly where our agents
run.

```python
from nlt import NLTConfig, select_tools

selected = select_tools(
    user_message=step_description,
    tools=tool_specs(scope),           # registered tools, optionally scoped
    call_llm=nlt_callable,             # (user_prompt, system_prompt) -> str
    config=NLTConfig(max_tools_per_turn=2),
    context=prior_step_outputs,
)
```

The engine turns each `SelectedTool` into a normalized, loop-guarded execution
— selection and execution never mix.

## The pluggable alternative

Consumers who want JSON function calling bind tools directly:
`call_llm(prompt, tools=[...])` returns an `AIMessage` whose `tool_calls` the
same execution path understands. Nothing else changes.

## Guarantees

- No JSON schema serialization on the hot path; grids are plain text.
- `invoke_tool` tolerates the three LangChain calling conventions.
- A selected-but-unknown tool logs and skips; it never crashes the run.
