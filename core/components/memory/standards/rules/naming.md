# Naming — how every harness part is named

The single source for naming plays, loops, skills and agents (ADR 046, #736). The machine half is
`naming.yaml` beside this file: `lint-components` reads it, so a name that breaks a rule cannot land.
`rename-map.yaml` lists every name changed when this standard was adopted.

## Why one rule

A harness is used by people who learn its words once and then type them every day. When names grow
in four shapes (`vision`, `understand`, `fix-bug`, `play-creator`), a person has to remember each one
on its own. When one verb means two things ("build" a plan, "build" code), the name stops telling
you what the part does. One rule, learned once, removes both problems, and it is the rule a client
can take for their own harness.

## The rules

1. **Plain words, spelled out.** Lowercase words joined by `-`, at most 64 characters. No shortened
   words (`arch`, `env`, `impl`). Only the fixed industry terms in `naming.yaml` may stay short:
   `pr`, `mvp`, `nfr`, `rca`, `lld`, `kb`, `ice`, `ux`, `tech`, `ci`, `yaml`, `adr`.
2. **The verb comes first, then the object.** The verb says what the part does; the object is the
   thing it works on, in the product model's words (feature, capability, slice, epic, plan — never
   a word the model dropped). Epic and slice are model words.
3. **One verb, one meaning.** Every verb is listed in `naming.yaml` with its one meaning. A new
   verb is added there first, with its meaning, or it cannot be used.
4. **Never a tool's own command.** No name is, or starts with, a built-in command of Claude Code or
   Codex (`plan`, `review`, `design`, `run`, `focus`, `init`, …; the full list is in `naming.yaml`).
   A person typing `/review` must not have to choose between theirs and ours.
5. **Every name is used once**, across plays, loops, skills and agents.

## By kind

**Loops** — what people run. `complete-<phase>`: a loop runs its plays in rounds until its phase is
complete. `complete` is used by loops only, so a loop is told apart from a play at a glance.
In writing, a loop keeps its plain name: the Discovery loop is run as `/complete-discovery`.

**Plays** — `<verb>-<object>`, the verb from the play verbs. The lifecycle verbs follow the phases
a product moves through:

| Phase | Verb | Example |
|-------|------|---------|
| Product → Intent | `discover` | `discover-domains` |
| Intent → Design | `shape` | `shape-slice` |
| Design → Code | `build` | `build-epic` |
| Code → Validation | `validate` | `validate-epic` |
| Validation → Run | `release` | `release-increment` |
| Run → Product | `learn` | `learn-outcomes` |

Change plays use `start`, `commit`, `propose`, `check`, `merge`, `fix`, `refactor`; plan plays
`draft`, `show`, `update`, `list`; `record` writes a
decision; harness plays `create`, `edit`, `install`, `uninstall`.

**Skills** — `<verb>-<object>`, the verb from the skill verbs (`author`, `infer`, `derive`, `scan`,
`check`, `judge`, `assess`, `find`, `link`, `enrich`, `propose`, `research`, `rank`, `recommend`,
`collect`, `walk`, `deploy`, `track`, and the git verbs `commit`, `open`, `merge`, `cut`). A verb
that already says where its input comes from is not repeated: `scan-test-surface`, not
`scan-test-surface-from-code`. One named exception: `platform-adapter`, the tool every script calls.

**Agents** — `<domain>-<role>`, ending in a role noun (`adr-keeper`, `quality-auditor`; ADR 004).

## Adding a name

1. Pick the verb from `naming.yaml`. If none fits, add the verb with its one meaning first.
2. Pick the object from the product model's words.
3. Run `node core/tools/lint-components/index.js --target core/components` from the repo root.
