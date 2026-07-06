"""hello_agent — the smallest Startr.Team agent.

Setup:
    export OPENAI_API_KEY=...        # or OPENAI_BASE_URL for a local model
    export AGENT_PROFILE=agent.yaml  # this folder's persona
    python run.py "Draft a Tuesday standup note: shipped the vault, next is intake."
"""

import sys

try:  # optional: read a .env if python-dotenv is around
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

from startr_team import Agent, register_tools
from startr_team.tools import todays_date

register_tools(todays_date)  # the registry starts empty; you add your tools

instruction = " ".join(sys.argv[1:]) or "Write a two-line note on why plans should be readable."

agent = Agent(verbose=True)
answer = agent.run(instruction)

print("\n--- final answer ---\n")
print(answer)
print(f"\nAudit trail: {agent.vault.run_dir}/")
