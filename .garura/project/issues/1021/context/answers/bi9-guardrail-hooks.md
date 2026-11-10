Read on each tool's own pages on 2026-11-10, for BI-9 (Orchestration). Each fact names the page it came from.

# A Claude Code hook as a guardrail with a way past

All from https://code.claude.com/docs/en/hooks :
- A PreToolUse hook runs before each tool call and may answer allow, deny, ask or defer.
- deny stops the call; its reason is shown to Claude, not to the person.
- ask shows the person a permission prompt with the hook's reason; the person confirms or refuses.
- allow skips the prompt (deny and ask rules still apply); defer ends the turn so the call can be resumed later, in non-interactive mode only.
- A hook that exits with code 2 blocks the call, with its error text as the reason. Any other failure, or a time-out, does not block unless the hook is set to block on failure.

So a guardrail can answer ask instead of deny: the person sees what it guards and why, and can pass it on purpose; the hook can itself write a record of each pass.