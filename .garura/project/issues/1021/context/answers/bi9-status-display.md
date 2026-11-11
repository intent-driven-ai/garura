Read on each tool's own pages on 2026-11-10, for BI-9 (Orchestration). Each fact names the page it came from.

# Showing a long run in Claude Code

- The status line is a command set in settings (statusLine). It gets the session's data as JSON on its input and shows whatever it prints, so it can read any file, such as a run's status file. https://code.claude.com/docs/en/statusline
- It runs when a new assistant message arrives and on a few other events, batched every 300 ms. Those events can go quiet while the main session waits on sub-agents; refreshInterval re-runs it every N seconds (at least 1). https://code.claude.com/docs/en/statusline
- subagentStatusLine draws each sub-agent's row in the agent panel from a command. https://code.claude.com/docs/en/statusline
- A plugin cannot set the main status line: a plugin's settings take effect only for agent and subagentStatusLine. A plugin can ship monitors, background commands whose changes are shown as notifications. https://code.claude.com/docs/en/plugins-reference