---
layout: default
title: "Messaging"
description: "The Channel ABC, the roll, and gated dispatch — the LLM never sends."
---

# Messaging (`[messaging]` extra)

Three pieces: **channels** (transport adapters), the **roll** (who the agent
may write to), and **dispatch** (deterministic, dry-run-first delivery). The
governing rule: **the agent composes; the LLM never sends.** A human holds the
switch.

## Channel — the transport seam

```python
class Channel(ABC):
    name: str = "channel"

    @abstractmethod
    def validate_recipient(this, address: str) -> bool: ...

    @abstractmethod
    def send(this, to, subject, body, fmt="markdown", metadata=None) -> SendResult:
        """Deliver body to `to`. Never raises for delivery failure — returns a
        SendResult with ok=False and a detail instead."""

@dataclass
class SendResult:
    to: str
    ok: bool
    detail: str = ""
```

**The never-raise contract is the contract.** A failed recipient must not
abort delivery to the rest; every adapter converts its failures (SMTP errors,
missing binaries, HTTP faults, timeouts) into `SendResult(ok=False, detail=…)`.

Reference adapters: `SmtpChannel` (stdlib SMTP), `SignalChannel` (signal-cli
subprocess, direct or group), `WhatsAppChannel` (wuzapi REST). Registry:

```python
get_channel("signal") -> Channel        # KeyError names the valid channels
register_channel("pigeon", CarrierPigeon)
```

Registry names align with the roll's channel kinds, so one `--channel` flag
picks both the adapter and each participant's address.

## The roll

```python
class Participant(BaseModel):
    id, name, pronouns
    email / signal / whatsapp          # one address per channel kind
    groups, aliases
    role: str                          # free-form; consumers define vocabularies
    standing, avg_response_hours, asked, fulfilled   # reliability over time
    links: List[str]                   # pointers to external records
    def address_for(this, kind) -> str | None
    def reliability(this) -> float | None

class ParticipantStore:                # CSV-backed; the single persistence seam
    list / get / find / members_of / groups
    add / update / remove / add_link / remove_link
    record_outcome(id, fulfilled=…, responded_in_hours=…)
```

The store is deliberately a seam: callers never touch CSV, so the backing can
become SQLite without changing one caller. The register holds private contact
data — it lives in `data/`, gitignored, backed up, never in the wipeable vault.

`resolve_recipients(tokens, channel, store)` turns names, aliases, and group
labels into addresses for the chosen channel — literal addresses pass
through — and **raises with the known names/groups listed** when a token
cannot be resolved. A herald never guesses who to write to.

## Gated dispatch

```python
@dataclass
class Dispatch:
    body: str; recipients: List[str]; subject: str; channel: str = "email"

def deliver(dispatch, channel, *, dry_run: bool = True, vault=None) -> dict:
    ...
```

- **Dry-run is the default.** It validates every recipient and writes the full
  delivery record — without contacting the channel.
- A real send happens only when a human passes `dry_run=False` (a `--send`
  flag in every reference CLI).
- Every attempt, dry or real, renders a markdown delivery record (channel,
  subject, per-recipient outcome, the exact body) into the vault under
  `98_dispatch/`.

Between composition and delivery sits the **cleanup pipeline**
(`startr_team.clean`) — an ordered list of small, named, LLM-free steps
(unwrap fences, flatten markdown to prose, strip chatty preambles, house
style, whitespace). `split_subject` lifts a leading `Subject:` line into the
real subject. Appending a step (say, an HTML renderer) is one line.

## Intake — defined, deferred

A complete herald also *listens* (Lia Fáil polls an IMAP inbox and replies
through the same compose/dispatch path). Intake is deliberately **not** in
v0.1 of the reference lib; the contract sketch is an `Inbox` seam
(`fetch_unseen(mark_seen=…) -> list[InboundMessage]`) symmetrical to
`Channel`. The framework is not send-only by design — only by sequencing.
