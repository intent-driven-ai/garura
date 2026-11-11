# Support each coding tool: research and drafts (issue 1021, BI-7 capability 3)

Draft only. Nothing under `.garura/product/`, `.garura/core/` or `.claude/`, on GitHub or in git changed. The drafts are in `.garura/project/issues/1021/context/bi-7-capability-3/drafts/product-os/software-delivery-planning/support-coding-tools/`: the capability page and its ICE page, and six feature pages, each with its ICE page. They sit under software delivery planning for now, beside Install into a project, Upgrade a project and Initialize, and the capability page says so.

In one line: one of the five tools gets an install today. Claude Code is built. Codex has an adapter that is stopped until its redesign (#863). Factory was supported once, through a sync skill, and that was removed. GitHub Copilot and Antigravity have nothing built and no issue. What the five tools load from a project was read on their own documentation on 2026-11-10; those facts wait as five memory updates for the product owner's yes, so the pages say what Garura's own sources say and name each waiting update by its id.

## What each tool is and what it loads from a project (read on the web, 2026-11-10)

The rule for these facts: nothing Garura's own code, docs, issues or memory do not say may be used on a page from an agent's own knowledge. So each fact below was read on the tool's own documentation, with its link and the date read. Each is raised as a memory update (the next section), and the pages state none of them as known until the product owner approves the update. "Confirmed" means the page read says it in the words quoted. "Not confirmed" means the page read does not say it either way.

### Claude Code (Anthropic)

Garura's own sources say what Garura lays for it (the adapter, `core/components/plays/install-garura/scripts/adapters/claude.py`), but memory holds no page on what Claude Code loads. Phoenix memory's naming rule only lists its built-in commands, read from https://code.claude.com/docs/en/commands.md on 2026-10-22 (`standards/rules/naming.yaml` line 59).
- Instructions file. `./CLAUDE.md` or `./.claude/CLAUDE.md`, which "Claude reads them at the start of every session". Confirmed. https://code.claude.com/docs/en/memory.md, read 2026-11-10.
- `AGENTS.md` is read only when there is no `CLAUDE.md`: "By default, Claude reads `AGENTS.md` only when you have no `CLAUDE.md` in your working directory or above it." Reading it "requires Claude Code v2.1.277 or later". Confirmed. https://code.claude.com/docs/en/memory.md, read 2026-11-10.
- Rules files. `.claude/rules/*.md`: "Rules without `paths` frontmatter are loaded at launch with the same priority as `.claude/CLAUDE.md`." Confirmed; it matches what Garura's memory system says of its guide. https://code.claude.com/docs/en/memory.md, read 2026-11-10.
- Sub-agents. Project sub-agents sit in `.claude/agents/`, one Markdown file each, with `name` and `description` required. Its `model` field takes "`sonnet`, `opus`, `haiku`, `fable`, a full model ID such as `claude-opus-5-5`, or `inherit`", and an `effort` field sets the effort level. Confirmed. https://code.claude.com/docs/en/sub-agents.md, read 2026-11-10.
- Skills and commands. Project skills sit in `.claude/skills/<skill-name>/SKILL.md`. "Custom commands have been merged into skills.", and `.claude/commands/` "is the older format and still works". Confirmed. https://code.claude.com/docs/en/skills.md, read 2026-11-10.
- A skill can name its model. The skill frontmatter has a `model` field, "Model to use when this skill is active. The override applies for the rest of the current turn", and an `effort` field. Confirmed. This differs from Garura's adapter, which drops the model line on every skill because "A Claude skill has no model field". https://code.claude.com/docs/en/skills.md, read 2026-11-10.
- Hooks and settings. Hooks live in the settings files. `.claude/settings.json` is the "Shared project" file for "Team permissions, hooks, plugins, and the environment variables the project needs". A `PreToolUse` hook runs "Before a tool call executes. Can block it". Confirmed. https://code.claude.com/docs/en/settings.md and https://code.claude.com/docs/en/hooks.md, read 2026-11-10.
- Plugins. "A Claude Code plugin is a directory of skills, agents, hooks, MCP servers, or other components that Claude Code installs and loads as one unit", with a manifest at `.claude-plugin/plugin.json`. Confirmed. https://code.claude.com/docs/en/plugins.md, read 2026-11-10.
- A model for each part: yes, for a sub-agent and for a skill (above).

### Codex (OpenAI)

The old addresses under developers.openai.com/codex/ now lead to learn.chatgpt.com/docs/ (both were read on 2026-11-10; for example https://developers.openai.com/codex/skills leads to https://learn.chatgpt.com/docs/build-skills).
- What it is. "Build with the Codex CLI, IDE extension, and cloud automation to speed up development." Confirmed. https://learn.chatgpt.com/docs/llms.txt, read 2026-11-10.
- Instructions file. "Codex reads `AGENTS.md` files before doing any work.", from `~/.codex/AGENTS.md` and from each folder from the project root down to the working folder, with an `AGENTS.override.md` taking a folder's place; the files joined stop at `project_doc_max_bytes`, "32 KiB by default". Confirmed. https://learn.chatgpt.com/docs/agent-configuration/agents-md.md, read 2026-11-10.
- Skills. "For repositories, Codex scans `.agents/skills` in every directory from your current working directory up to the repository root.", and "The `SKILL.md` file must include `name` and `description`." Confirmed; it matches the adapter. The 1,024-character cap on a description that the adapter names is not on the page read: not confirmed. https://learn.chatgpt.com/docs/build-skills.md, read 2026-11-10.
- Custom agents (sub-agents). "add standalone TOML files under `~/.codex/agents/` for personal agents or `.codex/agents/` for project-scoped agents"; each must define `name`, `description` and `developer_instructions`, and "If a custom agent file sets `model` or `model_reasoning_effort`, the value in the file takes precedence." Confirmed. This differs from Garura's adapter, which says "There is no named-subagent file" and lays every agent as a skill. https://learn.chatgpt.com/docs/agent-configuration/subagents.md, read 2026-11-10.
- Commands. "Custom prompts are deprecated. Use skills"; custom prompts sit in the Codex home, "so they're not shared through your repository". Confirmed. https://learn.chatgpt.com/docs/custom-prompts.md, read 2026-11-10.
- Hooks. In `<repo>/.codex/hooks.json` or as `[hooks]` in `<repo>/.codex/config.toml`, with a `PreToolUse` event: "A supported hook can block an action by returning an explicit denial." Two limits: "Project-local hooks load only when the project `.codex/` layer is trusted.", and "A `PreToolUse` error, timeout, or malformed response can let the tool run." Confirmed. https://learn.chatgpt.com/docs/hooks.md, read 2026-11-10.
- Settings. `~/.codex/config.toml`, a project's `.codex/config.toml` for "trusted projects only", and profile files `~/.codex/profile-name.config.toml` chosen with `--profile`. Confirmed; the profiles match what the adapter writes. https://learn.chatgpt.com/docs/config-file/config-basic.md, read 2026-11-10.
- A model for each part: yes for a custom agent (above); a skill does not name one: "Skills inherit from the parent". Confirmed. https://learn.chatgpt.com/docs/agent-configuration/subagents.md, read 2026-11-10.

### GitHub Copilot (GitHub)

- Where it runs. Visual Studio Code, Visual Studio, JetBrains IDEs, Eclipse, Xcode, GitHub.com (its cloud agent) and Copilot CLI, each with its own set of customizations (the support table of the cheat sheet). Confirmed. https://docs.github.com/en/copilot/reference/customization-cheat-sheet, read 2026-11-10.
- Instructions files. `.github/copilot-instructions.md` for the whole repository; `.github/instructions/NAME.instructions.md` for some paths; `AGENTS.md` files, where "the nearest `AGENTS.md` file in the directory tree will take precedence"; and "Alternatively, you can use a single `CLAUDE.md` or `GEMINI.md` file stored in the root of the repository." Confirmed. https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions, read 2026-11-10.
- Custom agents. `.github/agents/AGENT-NAME.md` (also `.agent.md`), with `description` required and a `model` field, "Model to use when this custom agent executes. If unset, inherits the default model." The how-to says the `model` property is for "VS Code, JetBrains IDEs, Eclipse, or Xcode", so whether GitHub.com uses it is not confirmed. https://docs.github.com/en/copilot/reference/custom-agents-configuration and https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/create-custom-agents-in-your-ide, read 2026-11-10.
- Sub-agents. "N/A (runtime process, not a user-configured file)". Confirmed. https://docs.github.com/en/copilot/reference/customization-cheat-sheet, read 2026-11-10.
- Skills. "Project skills, stored in your repository (`.github/skills`, `.claude/skills`, or `.agents/skills`)". Supported in VS Code, Visual Studio, GitHub.com and Copilot CLI; in preview in JetBrains; not in Eclipse or Xcode. Confirmed. Whether a skill can name a model is not on the pages read: not confirmed. https://docs.github.com/en/copilot/concepts/agents/about-agent-skills and the cheat sheet, read 2026-11-10.
- Prompt files (commands). `.github/prompts/*.prompt.md`, run by hand from chat; supported in VS Code and Visual Studio, in preview in JetBrains and Xcode, and not on GitHub.com or in Copilot CLI. In VS Code a prompt file's `model` is "The language model used when running the prompt." Confirmed. https://docs.github.com/en/copilot/reference/customization-cheat-sheet and https://code.visualstudio.com/docs/agent-customization/prompt-files, read 2026-11-10.
- Hooks. `.github/hooks/*.json`, supported on GitHub.com and in Copilot CLI, in preview in VS Code, and not in the other IDEs; a hook can "Programmatically approve or deny tool executions.", with a `preToolUse` event. Confirmed. https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-hooks and https://docs.github.com/en/copilot/reference/hooks-configuration, read 2026-11-10.
- Built-in commands of Copilot CLI include `/plan`, `/review`, `/research`, `/update`, `/skills`, `/agent` and `/init`. Confirmed. https://docs.github.com/en/copilot/reference/cli-command-reference, read 2026-11-10.
- A model for each part: for a custom agent and a prompt file in the IDEs (above); not confirmed for a skill or on GitHub.com.

### Antigravity (Google)

- What it is. "Google Antigravity is an advanced agentic coding platform and CLI designed for orchestrating autonomous subagents, scheduled tasks, and interactive code verification.", with an App, a CLI, an IDE, IDE extensions and an SDK. Confirmed: it is Google's, and the IDE is one of its surfaces. https://antigravity.google/llms.txt, read 2026-11-10.
- Instructions and rules. In the workspace folder and each parent up to the repository root: `AGENTS.md` or `GEMINI.md`, `.agents/AGENTS.md` or `.agents/GEMINI.md`, and `.agents/rules/*.md` (and the older `.agent/rules/`). `AGENTS.md` and `GEMINI.md` take no frontmatter and are always on; each file in `rules/` "must start with YAML frontmatter declaring a valid trigger", or "Antigravity silently discards the rule". Confirmed. https://antigravity.google/docs/rules, read 2026-11-10.
- Skills. `<workspace-root>/.agents/skills/<skill-folder>/` with a `SKILL.md`, whose frontmatter has `name` (optional) and `description` (required); a person can also type `/<skill-name>`. Confirmed. No model field is listed: not confirmed either way. https://antigravity.google/docs/skills, read 2026-11-10.
- Custom sub-agents. `.agents/agents/<name>.md` or `.agents/agents/<name>/agent.md`, with `name` and `description` required and a `model` field, "Model tier used when invoked ( inherit , flash , or pro )". The page says "Available on: Antigravity App Antigravity CLI", so not the IDE. Confirmed. https://antigravity.google/docs/subagents, read 2026-11-10.
- Hooks. `.agents/hooks.json`, in the App, the CLI and the IDE, with a `PreToolUse` event whose decision "deny" "Hard blocks execution immediately." Confirmed. https://antigravity.google/docs/hooks, read 2026-11-10.
- Where it all sits. "Workspace : the .agents/ folder in your project, plus AGENTS.md and GEMINI.md files.", with MCP servers in `mcp_config.json`. Confirmed. https://antigravity.google/docs/customization-discovery, read 2026-11-10.
- Model choice. A person picks the model for a conversation from a selector (Gemini, Claude and GPT-OSS models), and a custom sub-agent names a tier (above). Confirmed. https://antigravity.google/docs/models, read 2026-11-10.
- Built-in commands include `/plan`, `/goal`, `/learn`, `/schedule`, `/browser`, `/boost` and `/teamwork`. Confirmed. https://antigravity.google/docs/slash-commands, read 2026-11-10.

### Factory (Factory.ai, its agent Droid)

- What it is. "Factory, the agent-native software development platform", whose agent is Droid, run from the Droid CLI. The address docs.factory.ai now leads to docs.factory.com. Confirmed: Factory.ai's Droids. https://docs.factory.com/llms.txt, read 2026-11-10.
- Instructions file. `AGENTS.md`; Droid "also reads compatible filenames", among them `CLAUDE.md`, for "Compatibility with existing Claude-oriented instructions." Confirmed. https://docs.factory.com/harness/agents-md.md, read 2026-11-10.
- Custom droids (sub-agents). "Project droids sit in `<repo>/.factory/droids/`", one Markdown file each, with `name` required and `model` (`inherit` by default, or a model id) and `reasoningEffort`. Its import "scans both `<repo>/.claude/agents/` (project scope) and `~/.claude/agents/`", and "`sonnet`, `haiku`, or `opus` map to the first available model in that family". Confirmed. https://docs.factory.com/harness/subagents.md, read 2026-11-10.
- Skills. `<repo>/.factory/skills/<skill-name>/SKILL.md`, and for compatibility `<repo>/.agents/skills/**/SKILL.md`. The frontmatter reference lists no model field. Confirmed. https://docs.factory.com/harness/skills.md, read 2026-11-10.
- Commands. `<repo>/.factory/commands`; "For new reusable workflows, prefer Skills". Confirmed. https://docs.factory.com/harness/custom-slash-commands.md, read 2026-11-10.
- Hooks and settings. `.factory/hooks.json` for a project, or the `hooks` key of a `settings.json`; for `PreToolUse`, exit code 2 "blocks the tool call". Settings sit in `~/.factory/settings.json`, with a `settings.local.json` beside any `settings.json`. Confirmed. https://docs.factory.com/harness/hooks.md and https://docs.factory.com/droid-cli/settings.md, read 2026-11-10.
- Built-in commands include `/review`, `/skills`, `/droids`, `/hooks`, `/missions` and `/settings`. Confirmed. https://docs.factory.com/droid-cli/cli-reference.md, read 2026-11-10.
- A model for each part: for a custom droid (above); not for a skill.

### Where the web differs from Garura's own code

- Claude Code skills take a `model` field; the Claude Code adapter drops it because "A Claude skill has no model field" (`claude.py` lines 15-16).
- Codex has project custom agents in `.codex/agents/`; the Codex adapter says "There is no named-subagent file" and lays each agent as a skill (`codex.py` lines 15-17). #260 (closed, 2026-04-18) once planned "Codex custom subagents" as TOML files in `.codex/agents`.
- The 1,024-character cap on a Codex skill's description (`codex.py` lines 23-27, citing openai/codex#13941) is not on the skills page read.

## The memory updates raised

Raised with the memory tool's `propose` command on 2026-11-10: issue 1021, target tier short-term, `draft_source` "web", `requested_by` "product-os-keeper (BI-7 capability 3 draft, #1021)". Each waits for the product owner's approval; none was decided or applied. The tool's `sources` field takes only memory lines (tier, path, lines, fingerprint), not web links, so each update's sources name the lines of this file where its facts and their links are written, and its draft carries each link beside its fact.

| Id | Tool | Its facts, in this file | Written, once approved, to |
|---|---|---|---|
| mu-20261110-001 | Claude Code | lines 11-22, and 70-74 | `1021/context/bi-7-capability-3/answers/coding-tool-claude-code.md` |
| mu-20261110-002 | Codex | lines 24-34, and 70-74 | `1021/context/bi-7-capability-3/answers/coding-tool-codex.md` |
| mu-20261110-003 | GitHub Copilot | lines 36-46 | `1021/context/bi-7-capability-3/answers/coding-tool-github-copilot.md` |
| mu-20261110-004 | Antigravity | lines 48-57 | `1021/context/bi-7-capability-3/answers/coding-tool-antigravity.md` |
| mu-20261110-005 | Factory | lines 59-68 | `1021/context/bi-7-capability-3/answers/coding-tool-factory.md` |

The records are in `.garura/project/issues/1021/review/memory-updates/`. Until one is approved, a page says what Garura's own sources say and names the update, for example "what Antigravity loads from a project rests on memory update mu-20261110-004, waiting for a person's approval". The two assumptions on BI-7's list rest on them too: that Antigravity is Google's agent tool (mu-20261110-004) and that Factory is Factory.ai's Droid (mu-20261110-005).

## The name

*Support each coding tool*, folder `support-coding-tools`, as the product owner named it on the list he set on 2026-11-10 (`capabilities.md` line 74), and as the brief gave the folder. Kept as it is.

Words the pages use, and why:
- **Coding tool**: the agent tool a team works in, as on Install into a project.
- **Adapter**: the part of the install that lays Garura in one coding tool's own shape (`scripts/adapters/claude.py`, `codex.py`). The install play's own words: "The adapter is the seam."
- **A tool's shape**: the files and folders a coding tool reads parts from, such as its instructions file and its folders for sub-agents and skills.
- **Model tier**: the `model:` hint a part carries in its source, folded to deep, standard or fast (`common.py` lines 11-39).
- **A tool's state**: built, stopped, removed, or neither (no build and no issue), the four states the brief and the stock-take use.

## What is built, and what is only planned

Built:
- **The adapter seam.** `install.py` picks an adapter by `--tool` and calls the same four things on each: its name, `lay_components`, `write_instruction_surface` and `write_global_config` (`adapters/__init__.py` lines 5-16). The tools on offer are the adapters known (`install.py` line 529, `choices=known()`), so a tool with no adapter is refused before anything is written. The record names the tool (`install.py` line 357).
- **Claude Code**, through both front doors. The adapter lays each sub-agent in `.claude/agents/` with its tier kept (`best` and `deep` read as `opus`, lines 29-39), each play, loop and skill in `.claude/skills/` with the model line dropped ("A Claude skill has no model field", lines 15-16), the shared files in `.claude/skills/_shared/` (line 121), and Garura's instructions as `CLAUDE.md` or beside the team's as `CLAUDE.md.new` (lines 128-138); it writes nothing machine-wide (lines 141-143). The memory guide is the rules file `.claude/rules/garura-memory.md` (`memory_system.py` lines 12-14, 146-152). The one-line command lays Claude Code only: every part under `.claude/` (`installer/install.sh` lines 310-346), and the memory step with `--tool claude` (line 223). The installed-layout lint checks `.claude` (Phoenix memory `knowledge/review/harness.md` lines 31-33).
- **The tier fold**, shared: `best`, `deep` and `opus` to deep, `sonnet` to standard, `haiku` to fast, anything else to standard (`common.py` lines 29-49). 17 sub-agents name a model (12 `sonnet`, 4 `opus`, 1 `haiku`); 75 skills, plays and loops name one (39 `sonnet`, 23 `opus`, 8 `best`, 4 `haiku`, one with no value), and the Claude Code adapter drops it on all 75.

Stopped:
- **Codex.** The adapter is in the source and marked deprecated (`codex.py` lines 3-7). It lays skills, plays and loops in `.agents/skills/`, every sub-agent as a skill ("There is no named-subagent file", lines 15-17), the tier as a note in each skill and three profiles and a base settings file in the Codex home folder (lines 18-22, 210-260, each written only when none is there), descriptions cut at 1,024 characters (lines 23-29), and `AGENTS.md` or `AGENTS.md.new` (lines 196-207). The memory guide is one marked block in `AGENTS.md` (`memory_system.py` lines 15-16, 153-156). Fixed in July 2026 (`CHANGELOG.md` line 22, #503, #504, #505). Stopped on 2026-10-25 (ADR 055 §7, line 69; `install.py` lines 78-89); the redesign is #863 (open).
- A gap of the stopped adapter not named in #863: its settings in the Codex home folder sit outside the project's folder and the machine's own Garura folders, where Install into a project says the install works.

Removed:
- **Factory.** #123 (closed 2026-03-24) added a `sync-droids` skill that "Transforms Claude Code agent definitions into Factory Droid format (tool names, model IDs, frontmatter)". #256 (closed 2026-04-19) removed the `.factory/` tree, and #430 (closed 2026-05-31; commit 64f3ace9, "remove sync-claude and sync-droids skills") removed the sync skills. Left behind: `core/config.yaml` lines 50-58, which no script reads (#947), and `AGENTS.md`, written "to Factory Droids" (line 3) and naming "The sudarshan `/sud:install` factory adapter" (line 28), which does not exist.

Neither (no build and no issue):
- **GitHub Copilot.** Named in the person's brief kept in Garura memory (`product/user-provided/project-brief.md` lines 45 and 51) and counted by the review shelf, which lists `COPILOT.md` among files that point at other files (Phoenix memory `knowledge/review/config-maps.md` line 6). No issue names it (searched 2026-11-10).
- **Antigravity.** Only the agreed line names it. No mention in the repository, in any memory tier or in any issue (searched 2026-11-10).

Planned elsewhere, for one tool:
- The guardrails, laid "in the coding tool's own form by Support each coding tool" (`install-into-project/fn-lay-guardrails/feature.md`); for Claude Code #893 names a hook, "a script Claude Code runs before each tool call". Not built.
- The status display, "a plugin installed only when the install chooses Claude Code" (Phoenix memory `standards/rules/run-status.md` lines 9-10; ADR 041 line 128). Not built.

Not an install: a loop's checker may be Codex ("a coding-agent checker is Codex", `core/config.yaml` line 122), and the test model setting may name it (`build-work-test-first/fn-write-failing-tests/feature.md` line 40). Both use a tool beside the installed one and install nothing for it.

Found and not filed:
- The memory guide's place for each tool is chosen inside the shared memory step, by a branch for `claude` and one for `codex` (`memory_system.py` lines 146-158), not by the tool's adapter. A new tool needs a change there, which the rule "No coding tool in the engine" does not allow.
- The naming lint still refuses a name that starts with a built-in command (`core/tools/lint-components/lib/rules/naming.js` lines 43-45), while ADR 066 §6 says a name "may start with one". It bears on open point 4.

## The open points: options and a lean

Each lean is a proposal, not a decision. None is written on a page.

### 1. The order in which the tools come after Claude Code (open question 4 of the stock-take)

What each tool would need from the engine: nothing, by the guiding rule, except the memory guide's place (found above). What each would need of its own:
- **Codex**: the redesign #863 asks for (every part a play needs, the installed-layout lint on `.agents/`, the empty-project test), a choice on the settings it writes in the Codex home folder, and a fresh look at how sub-agents and hooks are laid (mu-20261110-002 says Codex now has project custom agents and hooks). An adapter, tests and an issue already exist.
- **GitHub Copilot**: a new adapter and an issue. Per mu-20261110-003 it reads `.claude/skills`, `AGENTS.md` and a root `CLAUDE.md`, so part of what Claude Code gets may be read as it is; its sub-agents are runtime only, and its custom agents, prompt files and hooks have their own folders and work on some of its surfaces only.
- **Factory**: a new adapter (the old sync skill is gone) and an issue. Per mu-20261110-005 it reads `CLAUDE.md` and `.agents/skills`, imports `.claude/agents/`, and has its own droids, hooks and settings in `.factory/`.
- **Antigravity**: a new adapter and an issue. Per mu-20261110-004 everything sits in `.agents/`, a rules file needs a trigger in its frontmatter or is dropped, and custom sub-agents work in its App and CLI, not its IDE.

Options:
- **A. Codex first, then the others in the order the product owner names them**, each with its own issue. Codex is the only one with an adapter, tests and an open issue.
- **B. By how much of Claude Code's shape each tool already reads**: Codex, then Copilot and Factory, then Antigravity. This rests on the waiting updates.
- **C. By a team that asks**: no tool is built until a team that wants Garura uses it. No source names such a team.

**Lean: A**, with B as the product owner's tie-breaker once the updates are approved: Codex is already designed and stopped on one known gap, and the order of the others is a product choice no source settles.

### 2. What "Each tool gets what it supports" means when a tool lacks something a part uses

Examples from the evidence: Codex has no per-skill model ("the per-skill tier can't be *pinned*"), and the adapter wrote it once as "no named-subagent file"; Copilot's sub-agents are runtime only and its hooks work on some surfaces (mu-20261110-003); Antigravity's sub-agents are not in its IDE (mu-20261110-004).
- **A. Leave it out and say so**: the part, or the piece of it the tool cannot hold, is not laid, and the report names it.
- **B. Lay a fallback**: what the Codex adapter does today, an agent laid as a skill and the tier written as a note with profiles.
- **C. Refuse to install that part**, or the whole tool, as Codex is stopped today.

**Lean: B where a fallback keeps the part whole and working, else A, and C only for a tool that cannot run the plays at all.** It follows the approved Never on Install into a project, "lay a part without what it needs to run", and keeps the team told. Every fallback and every part left out is named in the report.

### 3. Factory's leftovers (`core/config.yaml` lines 50-58 and `AGENTS.md`)

- **A. Remove both** now that no adapter exists.
- **B. Update**: remove the config sections under #947 (no script reads them), and rewrite `AGENTS.md` as Garura's own instructions for any tool that reads it, without the Factory-only parts (the tool name map, the `.factory/` folders, `/sud:install`).
- **C. Keep both** until a Factory adapter is built.

**Lean: B.** #947 already asks for the config sections ("rename it to the current name, or remove it"), and per the waiting updates Codex, Copilot, Antigravity and Factory all read `AGENTS.md`, so a stale one misleads any of them in Garura's own repository. Change nothing here; these are findings on the page only.

### 4. Which tools the naming rule's built-in-command check covers (ADR 046 line 48 names Claude Code and Codex)

What the lists read on 2026-11-10 show (in the waiting updates): no Garura name is exactly a built-in command of Copilot CLI, Antigravity or Factory. Three start with one: `update-plan` (Copilot CLI's `/update`), `research-domain-context` (Copilot CLI's `/research`) and `learn-outcomes` (Antigravity's `/learn`). ADR 066 §6 allows a name to start with a command, but the lint still refuses it (found above), so adding those lists today would fail three names.
- **A. Every tool on the agreed list.**
- **B. Each tool that gets an install, added in the same change that builds its adapter**: Claude Code and Codex now.
- **C. Keep the two.**

**Lean: B.** A name collides only in a tool Garura is laid in, and each list is read when its adapter is built. Before any list is added, the lint should follow ADR 066 §6; that is Standards' work.

### Also found, and not one of the four

- **One project, two tools.** The install record names one tool, and the five tools read some of the same files (`AGENTS.md`, per the waiting updates). Whether one project may hold Garura for two tools at once is not decided by any source. It is named on the capability page as not decided.

## The persona

- **Lean: the product owner**, as on Install into a project and Upgrade a project. BI-7 is asked by the product owner; the choice of which tool gets an install, and what is left out where a tool lacks something, is the product owner's. The developers who work in the tool every day are named on the capability page as served, not as the persona.
- Other options weighed:
  - **The developer.** They meet each tool's shape every day, but the approved pages give the developer no choice about what is installed.
  - **The technical lead.** Close to which tools a team uses, but no approved page gives the technical lead a choice about the project's tools.

## The features found

Each is a job a person can do inside the capability: a team that works in one coding tool gets Garura laid in that tool's shape.

1. **Install Garura for Claude Code** (`fn-install-for-claude-code`): every sub-agent in `.claude/agents/` with its tier, every play, loop and skill in `.claude/skills/`, the shared files, the memory guide as a rules file, Garura's instructions beside the team's. Built, through both front doors. Sources: `claude.py`, `memory_system.py`, `installer/install.sh`, the install play's `SKILL.md`, #893, run status.
2. **Install Garura for Codex** (`fn-install-for-codex`): every part where Codex reads it, with Garura's instructions as a marked block in the team's `AGENTS.md`. Stopped; the redesign is planned only (#863). Sources: `codex.py`, `memory_system.py`, ADR 055 §7, #863, #503-#505.
3. **Install Garura for GitHub Copilot** (`fn-install-for-copilot`). Neither: named by the agreed line and the brief. Sources: the agreed line, the brief, the review shelf, mu-20261110-003.
4. **Install Garura for Antigravity** (`fn-install-for-antigravity`). Neither: named by the agreed line only. Sources: the agreed line, mu-20261110-004.
5. **Install Garura for Factory** (`fn-install-for-factory`). Removed: once a sync skill, removed by #256 and #430, with leftovers. Sources: #123, #256, #430, `core/config.yaml`, `AGENTS.md`, #947, mu-20261110-005.
6. **Map each part's model tier onto each tool's own setting** (`fn-map-model-tier`), the shared part the evidence shows: the tier a part names is folded once and each adapter maps it onto its tool. Built in part: kept on Claude Code sub-agents, dropped on its skills, a note and profiles in the stopped Codex adapter. Sources: `common.py`, `claude.py`, `codex.py`, the install play's `SKILL.md`. Which model each part runs on is Intelligent model routing's (`capabilities.md` line 102).

Not a feature here, and why:
- The guardrails in each tool's form: a rule of each tool's feature, laid by Lay Garura's guardrails with the install, whose page hands the form to this capability.
- The naming check's lists: Standards' rule; this capability only says which tools get an install (open point 4).
- A tool used beside the installed one (Codex as a loop's checker or a test model): it installs nothing.
- Moving a project from one tool to another: no source plans it; a new run with another tool goes through Update what the project gets as the project changes, and two tools at once is named as not decided.

## The hand-offs

- **Install into a project** (BI-7, approved): the engine, its two front doors, the record, the kinds, the check and the take-out. It hands this capability "laying Garura in each coding tool's own shape, and which tools get an install", and its guardrails feature hands the form of each guardrail.
- **Upgrade a project** (BI-7, approved): the same adapters on an upgrade; it "names no tool in its rules".
- **Set a project up after the install (Initialize)** (BI-7, next): starts where the install stops, whichever tool. Not drafted here.
- **Standards, structure, settings and memory (BI-10)**: what Garura's parts are and how they are built (Standards), the naming rule and its lists (Standards), where each part lives once laid (Structure), and which model and effort each part runs on (Intelligent model routing, which "Also serves Install and distribute").
- **Orchestration (BI-9)**: what each guardrail guards and the way past it.

## What this run did besides reading

- It re-read the stock-take's lines it relies on (section 4, sections 9, 10 and 12) against their files: `adapters/claude.py`, `adapters/codex.py`, `adapters/common.py`, `adapters/__init__.py`, `install.py` (header, lines 78-89, 136-142, 345-357, 529), `memory_system.py` (header and lines 104-158), the install play's `SKILL.md` (lines 1-80), `installer/install.sh` (lines 210-239, 310-346), `core/config.yaml` (lines 40-58, 117-131), `AGENTS.md`, `CHANGELOG.md` line 22, ADR 046 (line 48), ADR 055 (§3 to §9 and Negative), ADR 066 §6, ADR 041 line 128, and the naming lint. Every line held. One correction: the stock-take's "17 agents carry a model" and "Seventy-five skills and plays" hold, and the 75 split as 39 `sonnet`, 23 `opus`, 8 `best`, 4 `haiku` and one with no value.
- It read GitHub, read only: #863, #123, #256, #430, #260, #947, #893, and the pull requests #503, #504 and #505. It searched every issue for "copilot", "antigravity", "droid", "gemini" and "cursor"; none names GitHub Copilot or Antigravity.
- It searched memory through the memory tool (`--issue 1021`), in Garura memory and Phoenix memory, for Codex, Copilot, Antigravity, Factory, Droid, coding tool, hook, sub-agent, `AGENTS.md`, `CLAUDE.md`, plugin and slash command. No tier holds a page on what a coding tool loads from a project. What it found is cited above.
- It copied the memory files it decided from into `bi-7-capability-3/memory/`, with `manifest.json`: from Phoenix memory the grounding content standard and the capability and feature templates, the naming rule, the run status rule, and the review shelves on the harness and on config maps; from Garura memory the person's brief.
- It read each tool's own documentation on the web (the section above), and raised five memory updates.
- It recorded no decision trace with `memory.py cite`, because that tool writes outside this run's folder.
- The pages were written by hand in short-term memory, as on the earlier runs: no skill drafts pages of the approved shape outside the live model.

## Checks

- The structure check (`.claude/skills/discover-capabilities/scripts/lint_grounding.py`) was run on each draft page, the capability page with `--stage directional`; all seven pages pass with no error and no warning. The results are in `bi-7-capability-3/checks/lint.json`. The first run refused three short job lines on the capability page as labels; they were written out.
- Each ICE page was checked for its shape (one Goal, the Limits and Fails if, at most three of each when thin, the fixed Read line, Never read, Persona, Scope, a Scenario where known and a Done means checked by someone other than the doer, the thin mark exactly where the part is not built, and no ICE section on the part's own page). All seven pass: four full (the capability, Claude Code, Codex, the model tier) and three thin (GitHub Copilot, Antigravity, Factory). Each Goal was read against its Limits for a contradiction, and two Goals were worded so they do not pick an option an open point leaves open. The results are in `bi-7-capability-3/checks/ice-shape.json`.
- Every quote in the pages' Sources was checked against its file, its GitHub issue (read only), the commit message, or its copy in `bi-7-capability-3/memory/`, by a script that looks for each quoted string in its source with spaces and line breaks evened out: 103 quotes, all found. Every quote of three words or more in the pages' own text was also looked for in the sources that page lists: 93, all found. Fourteen Sources lines name no file (the memory updates, the searches, the counts, the stock-take and the shelf). The results are in `bi-7-capability-3/checks/quotes.json`.
- Every quote of a tool's documentation in this file was looked for in that tool's pages as downloaded on 2026-11-10, with Markdown links and bold marks taken out: 50 quotes, 48 found in the tools' pages and 2 that are quotes of Garura's own adapters, found there. The results are in `bi-7-capability-3/checks/web-quotes.json`.
- The pages were scanned for a lean, a home-folder path, a temporary folder, a real name and a plan's number: none found.
