Read on the tool's own documentation on 2026-11-10. Each fact names the page it came from.

# What GitHub Copilot loads from a project

- Where it runs: VS Code, Visual Studio, JetBrains IDEs, Eclipse, Xcode, GitHub.com (the cloud agent) and Copilot CLI, each with its own set of customizations. https://docs.github.com/en/copilot/reference/customization-cheat-sheet
- Instructions: .github/copilot-instructions.md (whole repository), .github/instructions/NAME.instructions.md (some paths), AGENTS.md files (the nearest wins), or one CLAUDE.md or GEMINI.md at the root. https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions
- Custom agents: .github/agents/AGENT-NAME.md (or .agent.md), description required, with a `model` field; the how-to names the model property for VS Code, JetBrains IDEs, Eclipse and Xcode, so GitHub.com's use of it is not confirmed. https://docs.github.com/en/copilot/reference/custom-agents-configuration and https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/create-custom-agents-in-your-ide
- Sub-agents: a runtime process, not a file a team writes. https://docs.github.com/en/copilot/reference/customization-cheat-sheet
- Skills: .github/skills, .claude/skills or .agents/skills in the repository; in VS Code, Visual Studio, GitHub.com and Copilot CLI, in preview in JetBrains, not in Eclipse or Xcode. A model field for a skill is not stated. https://docs.github.com/en/copilot/concepts/agents/about-agent-skills
- Prompt files (commands): .github/prompts/*.prompt.md, run by hand; in VS Code and Visual Studio, in preview in JetBrains and Xcode, not on GitHub.com or in Copilot CLI; in VS Code a prompt file names its model. https://code.visualstudio.com/docs/agent-customization/prompt-files
- Hooks: .github/hooks/*.json, on GitHub.com and in Copilot CLI, in preview in VS Code, not in the other IDEs; a preToolUse hook can approve or deny a tool call. https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-hooks and https://docs.github.com/en/copilot/reference/hooks-configuration
- Built-in commands of Copilot CLI include /plan, /review, /research, /update, /skills, /agent and /init. https://docs.github.com/en/copilot/reference/cli-command-reference
