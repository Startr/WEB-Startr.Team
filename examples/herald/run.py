"""herald — compose a dispatch, resolve recipients from the roll, deliver gated.

Dry run (default — validates recipients, sends NOTHING):
    python run.py "Tell the design team standup moved to 10" --to "design team"

Real send (a human flips the switch; SMTP_* env must be configured):
    python run.py "..." --to "design team" --send
"""

import argparse

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

from startr_team import Agent
from startr_team.channels import get_channel
from startr_team.clean import clean_body, split_subject
from startr_team.dispatch import Dispatch, deliver, first_line_subject
from startr_team.roll import ParticipantStore, resolve_recipients

parser = argparse.ArgumentParser(description="Compose a dispatch; optionally send it.")
parser.add_argument("instruction", help="What to say.")
parser.add_argument("--to", required=True, help="Names, groups, or literal addresses (comma-separated).")
parser.add_argument("--channel", choices=["email", "signal", "whatsapp"], default="email")
parser.add_argument("--send", action="store_true", help="Actually send (default: dry-run).")
args = parser.parse_args()

# 1. Resolve who — from the roll, by name or group. Fails loudly on unknowns.
store = ParticipantStore(path="participants.example.csv")
recipients = resolve_recipients(
    [t.strip() for t in args.to.split(",")], args.channel, store
)

# 2. Compose — the agent writes; the cleanup pipeline makes it ready-to-send.
agent = Agent()
subject, body = split_subject(clean_body(agent.run(args.instruction)))

# 3. Deliver — deterministic and gated. The LLM never touches this switch.
dispatch = Dispatch(
    body=body,
    recipients=recipients,
    subject=subject or first_line_subject(body),
    channel=args.channel,
)
result = deliver(dispatch, get_channel(args.channel), dry_run=not args.send, vault=agent.vault)

print()
print(result["record"])
if result["dry_run"]:
    print("\n[dry-run] Nothing was sent. Re-run with --send to deliver.")
