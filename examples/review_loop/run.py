"""review_loop — an agent traversing a graph plan with a draft → review cycle.

The plan is the `plans/` folder: three markdown notes wired with [[wikilinks]].
Open it in Obsidian while this runs — node `status:` frontmatter updates live,
and an interrupted run resumes where it stopped.

    export OPENAI_API_KEY=...          # or OPENAI_BASE_URL for a local model
    # optional: a stronger judge than drafter
    # export LLM_REVIEW_MODEL=gpt-4.1
    python run.py "a note thanking the team for shipping the vault feature"
"""

import sys
from pathlib import Path

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

from startr_team import Agent
from startr_team.plans import load_plan
from startr_team.plans.markdown_io import update_status

args = [a for a in sys.argv[1:] if a != "--resume"]
resume = "--resume" in sys.argv[1:]
topic = " ".join(args) or "a note thanking the team for a good sprint"

plan_dir = Path(__file__).parent / "plans"

# Fresh demo run by default; pass --resume to pick up an interrupted traversal.
if not resume:
    for node_id in load_plan(plan_dir).nodes:
        update_status(plan_dir, node_id, "pending")

agent = Agent(verbose=True)
answer = agent.run_plan(plan_dir, query=f"Write {topic}")

print("\n--- final answer ---\n")
print(answer)
print(f"\nTraversal trace and artifacts: {agent.vault.run_dir}/")
