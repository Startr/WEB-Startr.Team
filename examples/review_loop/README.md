A graph plan: `plans/` is a wikilinked markdown vault — open it in Obsidian or
SilverBullet and you'll see the graph. The agent drafts, reviews its own work,
and loops back to revise until the review approves — with a visit budget so the
loop cannot spin. The `review` node runs under `role: review`, so
`LLM_REVIEW_MODEL` can put a stronger model on judgment while a cheap one
drafts. The run vault records the traversal trace: every node, every edge
taken, and why.
