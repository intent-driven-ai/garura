Read on the tool's own documentation on 2026-11-10. Each fact names the page it came from.

# What Claude Code loads from a project

- Instructions: ./CLAUDE.md or ./.claude/CLAUDE.md, read at the start of every session. AGENTS.md is read only when there is no CLAUDE.md (Claude Code v2.1.277 or later). https://code.claude.com/docs/en/memory.md
- Rules: .claude/rules/*.md; a rule with no `paths` frontmatter loads at launch with the same priority as .claude/CLAUDE.md. https://code.claude.com/docs/en/memory.md
- Sub-agents: .claude/agents/<name>.md, with name and description required; `model` takes sonnet, opus, haiku, fable, a full model id or inherit; `effort` sets the effort level. https://code.claude.com/docs/en/sub-agents.md
- Skills and commands: .claude/skills/<name>/SKILL.md; custom commands are merged into skills, and .claude/commands/ still works. https://code.claude.com/docs/en/skills.md
- A skill can name its model: the skill frontmatter has `model` (for the rest of the current turn) and `effort`. https://code.claude.com/docs/en/skills.md
- Hooks: in the settings files; .claude/settings.json is the shared project file for team permissions, hooks and plugins; a PreToolUse hook runs before a tool call and can block it. https://code.claude.com/docs/en/settings.md and https://code.claude.com/docs/en/hooks.md
- Plugins: a directory of skills, agents, hooks and MCP servers that Claude Code installs and loads as one unit, with a manifest at .claude-plugin/plugin.json. https://code.claude.com/docs/en/plugins.md
- Model for each part: yes, for a sub-agent and for a skill.
- Differs from Garura's adapter, which drops the model line on every skill because "A Claude skill has no model field".
