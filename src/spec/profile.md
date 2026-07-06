---
layout: default
title: "Profile"
description: "agent.yaml — one YAML file retargets the whole engine."
---

# Profile — `agent.yaml`

One YAML file defines who the agent is. Its persona block is prepended to every
system prompt; swap the file and the same engine is a different agent. This is
the seam that let one codebase be both an education agent and a governance
herald.

## Interface

```python
@dataclass
class AgentProfile:
    name: str = "Agent"
    pronouns: str = "they/them"
    role: str = "an assistant"
    focus: str = "general assistance"
    mission: str = ""
    priorities: List[str] = field(default_factory=list)
    tone: str = "clear and concise"
    traits: List[str] = field(default_factory=list)
    scope_note: str = ""

    def persona_block(this) -> str: ...          # the identity preamble
    def default_system_prompt(this) -> str: ...  # persona + operating rules
    def fill(this, text: str) -> str: ...        # substitutes {name}/{role}/{focus}/...

def load_profile() -> AgentProfile: ...
```

## The file

```yaml
name: Lia Fáil
pronouns: they/them            # agents take singular they/them
role: a governance and herald agent
focus: time management and office coordination

mission: >
  Guard the vault, carry the word out faithfully, gather the answers back,
  and keep an honest record. Speak only when asked.

priorities:
  - Never invent facts, names, dates, or commitments
  - Clarity and brevity over length

disposition:
  tone: warm, precise, and calm
  traits: [methodical, discreet, dependable]

scope_note: >
  If a request falls outside coordination and communication, say so plainly.
```

## Resolution order

1. `$AGENT_PROFILE` if set,
2. `agent.yaml` in the current working directory,
3. `agent.yaml` at the repo root,
4. built-in defaults — the agent always runs, even with no file.

## Guarantees

- The persona block leads **every** system prompt (planning, action, answer,
  graph planning); an agent cannot drift out of character between phases.
- `fill()` substitutes only profile tokens, leaving other braces (like a
  `tools` placeholder) intact for later templating.
- A malformed or missing YAML degrades to defaults, never to a crash.

## Extension seam

Prompts read the profile at import; structural (non-persona) guidance lives in
`startr_team.prompts` as module attributes that consumers may override — see
[Extending](/spec/extending/).
