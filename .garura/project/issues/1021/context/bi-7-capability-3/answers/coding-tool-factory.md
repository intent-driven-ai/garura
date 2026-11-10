Read on the tool's own documentation on 2026-11-10. Each fact names the page it came from.

# What Factory loads from a project

- What it is: Factory (Factory.ai), "the agent-native software development platform", whose agent is Droid, run from the Droid CLI; docs.factory.ai now leads to docs.factory.com. https://docs.factory.com/llms.txt
- Instructions: AGENTS.md; Droid also reads compatible names, CLAUDE.md among them. https://docs.factory.com/harness/agents-md.md
- Custom droids (sub-agents): <repo>/.factory/droids/<name>.md, name required, `model` (inherit by default, or a model id) and `reasoningEffort`; an import reads .claude/agents/ and maps sonnet, haiku or opus to the first available model of that family. https://docs.factory.com/harness/subagents.md
- Skills: <repo>/.factory/skills/<name>/SKILL.md, and for compatibility <repo>/.agents/skills/**/SKILL.md; no model field in the frontmatter reference. https://docs.factory.com/harness/skills.md
- Commands: <repo>/.factory/commands; skills are preferred for new work. https://docs.factory.com/harness/custom-slash-commands.md
- Hooks and settings: .factory/hooks.json, or the hooks key of a settings.json; a PreToolUse hook that exits with code 2 blocks the tool call; settings in ~/.factory/settings.json with a settings.local.json beside any settings.json. https://docs.factory.com/harness/hooks.md and https://docs.factory.com/droid-cli/settings.md
- Built-in commands include /review, /skills, /droids, /hooks, /missions and /settings. https://docs.factory.com/droid-cli/cli-reference.md
- Model for each part: for a custom droid, not for a skill.
