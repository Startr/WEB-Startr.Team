A messaging agent: composes a dispatch from an instruction, resolves recipients
from a roll (names and groups, not raw addresses), and delivers over a channel —
**dry-run by default**. Nothing is sent unless a human passes `--send`. Every
attempt, real or dry, writes a delivery record to the vault.
