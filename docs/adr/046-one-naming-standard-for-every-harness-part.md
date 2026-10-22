# ADR 046 — One Naming Standard for Every Harness Part: Verb First, One Meaning per Verb, Loops Named complete-<phase>, No Tool Built-ins

**Status:** Accepted
**Date:** 2026-10-22
**Level:** framework
**Decided by:** Kapil Viren Ahuja · **Decided in:** #734 (Garura publishes a standard for building agentic harnesses), the naming discussion of 2026-10-22
**Supersedes:** ADR 006 (in full — the naming conventions) · ADR 018 (in full — the short bare names of the pipeline plays)
**Amends:** ADR 045 — §"the five loops are run by their names": a loop's command is now `complete-<phase>` (the Discovery loop is `/complete-discovery`); the loop keeps its plain name in writing · ADR 004 — none in substance; agent names stay `<domain>-<role>`, now also checked by the linter
**Affects:** every play, loop, skill and agent name in `core/components/` (27 plays, 1 loop, 69 skills and 2 agents renamed; the list is `core/components/memory/standards/rules/rename-map.yaml`), `standards/rules/naming.md` and `naming.yaml` (new), `standards/rules/pipeline-next.md`, `core/config.yaml` (play and loop keys), `core/tools/lint-components/` (naming rules), `core/tools/naming/` (old-name check, rename tool), `install-garura` (clears old names), `docs/standards/harness-standard.md` (new), `CLAUDE.md`, the glossary and the component docs
**ICE impact:** Wording only. Every ICE source that names a renamed part uses the new name, and its fingerprint is stamped again. No constraint, failure condition, scenario or guarantee changes in meaning.
**Business intent check:** none — a framework naming decision; no person's business intent changes
**Related:** ADR 004, ADR 006, ADR 018, ADR 029, ADR 045, #734, #735–#748, #717

## Context

Garura's names grew in four shapes: one noun (`vision`, `arch`), one verb (`understand`, `grill`),
verb then object (`fix-bug`, `start-change`), and object then role (`play-creator`). ADR 006 said every
play is `<action>-<object>`; ADR 018 then renamed six plays to short single words. Skills used several
verbs for one meaning — `author-`, `draft-`, `write-` and `build-` all made a document — and two skills
had near-same names for different jobs (`kb-search`, `search-kb`). A planned `manage-plan` play
clashed with an existing `manage-plan` skill.

Kapil, 2026-10-22: "this is the new code.. so we really need standards and practices we can take to
clients", and "let's record this as a clear-cut standard ... so that we can publish it as a standard
for creating these kinds of harnesses". People will mostly run loops ("eventually the plays should
simply vanish"), so loop names matter most, and names must not clash with the coding tools' own
commands: "We can't use review and plan. They will just simply overlap with what Claude is putting".

The built-in commands of Claude Code (https://code.claude.com/docs/en/commands.md) and Codex
(https://github.com/openai/codex/blob/main/codex-rs/tui/src/slash_command.rs) were read on
2026-10-22. Both use one short word for their most used commands and verb-then-object for the rest
(`/add-dir`, `/reload-plugins`, `/setup-default-sandbox`). A folder prefix does not work the same in
both tools: Claude Code turns `commands/plan/show.md` into `/plan:show`, and Codex ignores the folder.
Anthropic's skill guide asks for lowercase words and hyphens, at most 64 characters, and one pattern
for a whole set of skills (https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).

## Decision

### 1. One rule for every name

Lowercase words joined by `-`, at most 64 characters, the verb first and the object after it. Each
verb has one meaning, listed in `standards/rules/naming.yaml`. No word is shortened, except a fixed
list of industry terms (`pr`, `mvp`, `nfr`, `rca`, `lld`, `kb`, `ice`, `ux`, `tech`, `ci`, `yaml`, `adr`).
Every name is used once, across all kinds.

### 2. No tool built-ins

No name is, or starts with, a built-in command of Claude Code or Codex. The list is kept in
`naming.yaml`. Checking it moved three verbs that had been agreed in discussion: Intent → Design uses
`shape` (Claude Code has `/design`), loops use `complete` (Claude Code has `/run`), and `focus` becomes
`list-focus-issues` (Claude Code has `/focus`). The agent `loop-checker` becomes `result-checker`
(Claude Code has `/loop`).

### 3. Loops are `complete-<phase>`

A loop runs its plays in rounds until its phase is complete. `complete` is used by loops only, so a
loop is told apart from a play at a glance. In writing, a loop keeps its plain name — the Discovery
loop — and its command is `/complete-discovery`.

### 4. Plays take the verb of what they do

Lifecycle plays take the verb of the phase they move a product through: `discover` (Product → Intent),
`shape` (Intent → Design), `build` (Design → Code), `validate` (Code → Validation), `release`
(Validation → Run), `learn` (Run → Product). Change plays use `start`, `commit`, `propose`, `check`,
`merge`, `fix`, `refactor`; plan plays `draft`, `show`, `update`, `list`; knowledge plays `search`,
`research`, `check`; `record` writes a decision; harness plays `create`, `edit`, `install`,
`uninstall`. One play keeps one word: `next`. Objects use the product model's words (feature,
capability), never a word the model dropped (epic, slice).

### 5. Skills use the skill verbs; agents end in a role

Skills use `author`, `infer`, `derive`, `scan`, `check`, `judge`, `assess`, `find`, `link`, `enrich`,
`propose`, `research`, `rank`, `recommend`, `collect`, `walk`, `deploy`, `track`, and the git verbs
`commit`, `open`, `merge`, `cut`, each with one meaning. A verb that already says where its input comes
from is not repeated (`infer-scope`, not `infer-scope-from-code`). `platform-adapter` is the one named
exception. Agents stay `<domain>-<role>` (ADR 004).

### 6. The checks come first and are enforced

`lint-components` fails any name that breaks the rules. `core/tools/naming/check_old_names.py` fails
while any old name is still used outside past records. An install removes a component left under its
old name when Garura placed it.

## Consequences

### Positive

- One rule, learned once, for people and for clients building their own harness.
- No command a person types collides with the coding tool's own.
- A new name that breaks the standard cannot land.

### Negative / Risks

- Every command people type changes (`/vision` → `/discover-domains`). The installed copies in a
  project change only on the next install.
- Learned gate policies are keyed by play name (`ux:prose_edits`), so a project's learned policy for a
  renamed play starts again under the new name.
- Names grow longer (`discover-capabilities`). Kapil, 2026-10-22: "If it makes the command longer, so
  be it. At least it's going to give clarity."

## Alternatives Considered

| Alternative | Reason rejected |
|-------------|-----------------|
| Keep one word for lifecycle and lens plays as an exception | Two rules to learn and to teach; Kapil chose one standard |
| Object first (`plan-show`, `change-start`) so families sort together | Reads backwards; neither tool names its own commands this way |
| Folder prefixes (`/plan:show`) | Works in Claude Code only; Codex ignores the folder |
| One-word loops (`/discover`, `/build`) | A tool can add that word as a built-in at any time |
| Short forms for long words (`discover-caps`) | A new word every client must learn |

## References

- `core/components/memory/standards/rules/naming.md`, `naming.yaml`, `rename-map.yaml`
- `docs/standards/harness-standard.md`
- Evidence before and after the rename: `.garura/project/issues/734/evidence/naming/`
