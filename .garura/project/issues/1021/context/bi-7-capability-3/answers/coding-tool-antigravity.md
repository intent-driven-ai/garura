Read on the tool's own documentation on 2026-11-10. Each fact names the page it came from.

# What Antigravity loads from a project

- What it is: Google Antigravity, Google's agentic coding platform, with an App, a CLI, an IDE, IDE extensions and an SDK. https://antigravity.google/llms.txt
- Instructions and rules: in the workspace folder and each parent up to the repository root, AGENTS.md or GEMINI.md, .agents/AGENTS.md or .agents/GEMINI.md, and .agents/rules/*.md (and the older .agent/rules/); AGENTS.md and GEMINI.md are always on; each rules/*.md must start with frontmatter naming a valid trigger, or it is silently discarded. https://antigravity.google/docs/rules
- Skills: .agents/skills/<folder>/SKILL.md, description required, name optional; a person can type /<skill-name>. No model field is listed. https://antigravity.google/docs/skills
- Custom sub-agents: .agents/agents/<name>.md or .agents/agents/<name>/agent.md, name and description required, `model` is a tier: inherit, flash or pro; available in the App and the CLI, not the IDE. https://antigravity.google/docs/subagents
- Hooks: .agents/hooks.json in the App, the CLI and the IDE; a PreToolUse decision of deny hard-blocks the tool call. https://antigravity.google/docs/hooks
- Everything sits in the project's .agents/ folder plus AGENTS.md and GEMINI.md; MCP servers in mcp_config.json. https://antigravity.google/docs/customization-discovery
- Model choice: a person picks the model for a conversation; a custom sub-agent names a tier. https://antigravity.google/docs/models
- Built-in commands include /plan, /goal, /learn, /schedule, /browser, /boost and /teamwork. https://antigravity.google/docs/slash-commands
