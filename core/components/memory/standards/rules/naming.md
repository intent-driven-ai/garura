# Naming — how every harness part is named

The single source for naming plays, loops, skills and agents (ADR 046, #736; ADR 066, #1044). The
machine half is `naming.yaml` beside this file: `lint-components` reads it, so a name that breaks a
rule cannot land. `rename-map.yaml` lists every name changed when a rule changed.

## Why one rule

A harness is used by people who learn its words once and then type them every day. When names grow
in four shapes (`vision`, `understand`, `fix-bug`, `play-creator`), a person has to remember each one
on its own. When one verb means two things ("build" a plan, "build" code), the name stops telling
you what the part does. And when a verb does not say who acts, a person cannot tell whose work a
command is. One rule, learned once, removes these problems, and it is the rule a client can take for
their own harness.

## The rules

1. **Plain words, spelled out.** Lowercase words joined by `-`, at most 64 characters. No shortened
   words (`arch`, `impl`). Only the fixed short words in `naming.yaml` may stay short:
   `pr`, `mvp`, `nfr`, `rca`, `lld`, `kb`, `ice`, `ux`, `tech`, `ci`, `yaml`, `adr`, `env`, `perf`, `uat`.
2. **The verb comes first, then the object.** The verb says who does the work and what they do; the
   object is the thing it works on (`slice`, `plan`, `work`, `env`).
3. **One verb, one meaning.** Every verb is listed in `naming.yaml` with its one meaning. A new
   verb is added there first, with its meaning, or it cannot be used.
4. **Never exactly a tool's own command.** No name is a built-in command of Claude Code or Codex
   (`plan`, `review`, `design`, `run`, `focus`, `init`, …; the full list is in `naming.yaml`). A person
   typing `/review` must not have to choose between theirs and ours. A name may start with one:
   `design-slice` and `review-work` are allowed.
5. **Every name is used once**, across plays, loops, skills and agents.

## By kind

**Plays** — `<verb>-<object>`. Five roles own the play verbs (ADR 066). A verb belongs to one role,
and a role can have several verbs; the verb says who does the work.

| Role | Verbs | Examples |
|------|-------|----------|
| Specifier | `specify`, `learn` | `specify-intent`, `specify-domains`, `learn-outcomes` |
| Designer | `design` | `design-slice`, `design-eval`, `design-adr` |
| Builder | `build`, `fix`, `refactor` | `build-work`, `fix-work`, `build-play`, `fix-play` |
| Validator | `validate` | `validate-work`, `validate-slice`, `validate-uat` |
| Orchestrator | `shape`, `reshape`, `view`, `list` | `shape-plan`, `reshape-plan`, `view-plan`, `list-plans` |

`view` means one thing; `list` means more than one. Some plays have no role: the work plays
(`start`, `commit`, `review`, `merge` — anyone can run them: `start-work`, `review-work`), the product
plays (`install`, `uninstall`), and `release`, which has no role until the name of
`release-increment` is settled.

**Loops** — `loop-<from>-<to>`: a loop runs the plays of one transition between two of the six
phases (Product, Spec, Design, Code, Validation, Run), in rounds, until it is done. A loop has no
role. Only a loop's name starts with `loop`, so a loop is told apart from a play at a glance, and a
loop's full name is its command.

| Transition | Loop |
|------------|------|
| Product → Spec | `loop-product-spec` |
| Spec → Design | `loop-spec-design` |
| Design → Code | `loop-design-code` |
| Code → Validation | `loop-code-validation` |
| Validation → Run | `loop-validation-run` |
| Run → Product | `loop-run-product` |

**Skills** — `<verb>-<object>`, the verb from the skill verbs (`author`, `infer`, `derive`, `scan`,
`check`, `judge`, `assess`, `find`, `link`, `enrich`, `propose`, `research`, `rank`, `recommend`,
`collect`, `walk`, `deploy`, `track`, `remove`, and the git verbs `commit`, `open`, `merge`, `cut`). A verb
that already says where its input comes from is not repeated: `scan-test-surface`, not
`scan-test-surface-from-code`. One named exception: `platform-adapter`, the tool every script calls.
Skills keep these verbs until a later decision gives them their own roles (ADR 066).

**Agents** — `<domain>-<role>`, ending in a role noun (`adr-keeper`, `quality-auditor`; ADR 004).

## Adding a name

1. Pick the verb from `naming.yaml`. If none fits, add the verb with its one meaning first.
2. Pick the object: the thing the part works on.
3. Run `node core/tools/lint-components/index.js --target core/components` from the repo root.
