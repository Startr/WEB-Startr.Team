---
layout: default
title: "Graph plans"
description: "Plans as wikilinked markdown vaults — loops, budgets, NLT transitions, resume."
---

# Graph plans

A plan is a **folder of markdown notes**: one node per file, transitions as
labeled `[[wikilinks]]`, execution knobs in YAML frontmatter. No DSL. The
folder opens natively in Obsidian or SilverBullet — graph view included — so
humans author, read, and edit the same plan the agent traverses. A linear plan
is just the degenerate case: a path graph.

Where other frameworks define agent graphs in code, **these are notes your
team can edit mid-run.**

## The node file

```markdown
---
type: step          # step | start | terminal-by-shape (no outgoing edges)
status: pending     # pending | active | done   ← the resume marker
tools: [fetch_url]  # optional: scope the NLT grid at this node
role: review        # optional: route LLM calls via LLM_REVIEW_*
max_visits: 3       # per-node visit budget (default 3)
---
# Review the draft

Read the latest draft critically. Approved, or what must change?

## Next
- approved -> [[send]]
- needs revision -> [[draft]]
```

Only links under the `## Next` heading are edges — body prose may wikilink
freely. An edge labeled `next` (or unlabeled) is unconditional; any other
label is a natural-language condition.

## Interfaces

```python
# graph
class PlanNode:  id, title, body, type, status, tools, role, max_visits, edges
class Edge:      label, target
class PlanGraph:
    def validate(this) -> None          # raises PlanValidationError

# markdown_io
def load_plan(plan_dir) -> PlanGraph
def save_plan(graph, plan_dir) -> Path
def update_status(plan_dir, node_id, status) -> None
def parse_plan_document(text) -> PlanGraph      # LLM-emitted single document
def path_graph_from_steps(steps) -> PlanGraph   # linear degradation target

# transitions
def register_predicate(label, fn) -> None       # deterministic override
def choose_edge(node, context, call_llm) -> tuple[Edge | None, str]  # + rationale

# executor
Agent.run_plan(plan_dir_or_graph, query) -> str
```

## Validation — before anything runs

`validate()` rejects a plan that could misbehave, **before the first LLM call**:

- an edge to a node that does not exist;
- **a cycle with no exit** — every strongly-connected cycle must have at least
  one edge leaving it;
- no start node (mark one `type: start` when the loop points back at it);
- no terminal reachable from the start.

## Execution semantics

Node execution **is** the [act loop](/spec/agent-loop/): the node body is the
step description handed to `work_step`, with the node's `tools:` scoping the
NLT grid and `role:` routing its LLM calls. The graph changes only what
happens *between* steps:

1. On entry a node goes `status: active` (persisted — watch it in Obsidian).
2. After the work, `status: done`, then the transition is judged.
3. **Predicates win over the LLM**: a label registered with
   `register_predicate` is decided by code. Remaining conditional labels go to
   one small NLT YES/NO grid judged against the freshest outputs. No condition
   held → the unconditional edge, if any; otherwise the node re-works
   (budget-guarded self-loop).
4. Every hop is recorded in the run vault's `00_plan-trace/trace.md`: node,
   visit count, edge taken, and the **raw rationale** for the judgment.

## Safety

Per-node `max_visits` bounds every loop the validator allowed; the agent's
global `max_steps` still applies underneath. Exceeding a budget is a safety
stop that finalizes with what was collected and says why.

## Resume

`status:` frontmatter is the checkpoint. An interrupted run leaves one node
`active`; running the same plan vault again picks up there, and nodes already
`done` skip straight to their transitions. In-memory graphs (including
LLM-emitted ones) are persisted into the run vault first, so every run is
resumable and inspectable.

## Both authorship directions

Humans author plan vaults in their notes app. The planner can also **emit** a
graph (`Agent.llm.plan_graph(query)`) in the same `## node-id` format —
parsed by the same code, checked by the same validator, and **degraded to a
linear path graph** (today's behavior, never worse) when a small model emits
something invalid.

## Roadmap (not in v0.1)

Named state machines: `type: state` nodes with guard conditions and explicit
events. The file format already leaves room; the executor semantics above are
deliberately the subset that cannot surprise.
