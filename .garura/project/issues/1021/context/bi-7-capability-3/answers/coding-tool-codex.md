Read on the tool's own documentation on 2026-11-10. Each fact names the page it came from.

# What Codex loads from a project

- What it is: OpenAI's Codex CLI, IDE extension and cloud automation. Its docs moved from developers.openai.com/codex/ to learn.chatgpt.com/docs/. https://learn.chatgpt.com/docs/llms.txt
- Instructions: AGENTS.md, read before any work, from ~/.codex and from each folder from the project root down to the working folder; AGENTS.override.md takes a folder's place; the joined files stop at project_doc_max_bytes, 32 KiB by default. https://learn.chatgpt.com/docs/agent-configuration/agents-md.md
- Skills: .agents/skills in every folder from the working folder up to the repository root; SKILL.md must include name and description. A 1,024-character cap on a description is not stated on the page read. https://learn.chatgpt.com/docs/build-skills.md
- Custom agents (sub-agents): standalone TOML files in .codex/agents/ (project) or ~/.codex/agents/; each defines name, description and developer_instructions, and may set model and model_reasoning_effort. https://learn.chatgpt.com/docs/agent-configuration/subagents.md
- Commands: custom prompts are deprecated in favour of skills; they live in the Codex home and are not shared through the repository. https://learn.chatgpt.com/docs/custom-prompts.md
- Hooks: <repo>/.codex/hooks.json or [hooks] in <repo>/.codex/config.toml, with a PreToolUse event that can block an action by an explicit denial; project hooks load only when the project's .codex/ layer is trusted; a PreToolUse error, timeout or malformed answer can let the tool run. https://learn.chatgpt.com/docs/hooks.md
- Settings: ~/.codex/config.toml, a project's .codex/config.toml for trusted projects only, and profile files ~/.codex/<name>.config.toml chosen with --profile. https://learn.chatgpt.com/docs/config-file/config-basic.md
- Model for each part: yes for a custom agent; skills inherit from the parent. https://learn.chatgpt.com/docs/agent-configuration/subagents.md
- Differs from Garura's adapter, which says "There is no named-subagent file" and lays each agent as a skill.
