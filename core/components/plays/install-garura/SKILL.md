---
name: install-garura
description: 'Install Garura into a target project or repository so its skills, agents, and plays become discoverable by a host coding tool — Claude Code or the OpenAI Codex CLI. Reads this garura checkout''s core/components and runs a per-tool ADAPTER that lays them down in the host''s native shape: for claude, .claude/ skills + agents with model tiers resolved to Claude models; for codex, .agents/skills Agent Skills plus AGENTS.md and ~/.codex model/sandbox/approval profiles. Always writes a .garura/ tooling tree (config + STM scaffold) and copies shared memory to the machine-global ~/.garura, and records an install manifest so uninstall-garura can reverse exactly what was placed. Use when the user wants to install, set up, bootstrap, add, or enable Garura in another folder or repo for claude or codex — "install garura into X", "set up garura in this repo for codex", "bootstrap garura", "make codex see the garura skills". Takes the target path, an optional --tool, and an optional --scope (full = every component except the meta harness plays and the harness-only skills, the default; harness = meta plays + harness-only skills + change chain + discover-capabilities + their workers only). For the reverse, see uninstall-garura.'
user-invocable: true
---

# install-garura

Install **this** garura checkout into a **target** project so a host coding tool can discover
and run its skills, agents, and plays there. You run this from the garura repo (where the
source lives); the target is some other folder or repo the user names. The host tool is
chosen with `--tool`: **claude** (Claude Code, the default) or **codex** (the OpenAI Codex
CLI).

After a successful install the target has a `.garura/` tooling tree (config + an STM scaffold)
and — depending on the tool — either a `.claude/` tree (Claude Code) or a `.agents/skills/`
tree plus an `AGENTS.md` (Codex). Shared memory (the standards/KB) always goes to the
machine-global `~/.garura`.

## How this play is built (read this first)

This is a **bootstrap meta-play** — like create-play, it is hand-authored, not compiled from
an ICE source, and it is **harness-led**: the play decides and reports, a bundled script does
the deterministic file work. The orchestrator [`scripts/install.py`](scripts/install.py)
walks the source, handles the tool-agnostic work (shared memory, garura's own config, the STM
scaffold, the manifest), and **delegates the host surface to a per-tool adapter** under
[`scripts/adapters/`](scripts/adapters/). Don't re-implement that work in prose; call the
script and reason about its result.

**The adapter is the seam.** Garura's components carry a `model:` hint (best / opus / sonnet /
haiku). That value is a *tier* signal, not a literal host model id. `adapters/common.py` folds
it to a neutral tier (deep / standard / fast), and each adapter maps the tier onto its host's
real model selection. If you find yourself special-casing a host's model names or file layout
in the orchestrator, stop — that belongs in the adapter.

## What "installed" means

`install.py --tool claude` produces, in the target:

- `.claude/agents/<id>.md` — one per garura agent, with its **model tier resolved and kept**
  (`best` → `opus`; the `opus`/`sonnet`/`haiku` shorthands pass through) so the agent runs on
  the intended tier.
- `.claude/skills/<id>/` — one per garura skill, and one per garura **play** (Claude Code has
  no separate play type), copied whole with their own `references/`/`scripts/`. The `model:`
  line is dropped on skills (a Claude skill has no model field).

`install.py --tool codex` produces, in the target:

- `.agents/skills/<id>/` — one Codex Agent Skill per garura skill, play, **and agent** (Codex
  has no separate agent type), carrying only `name` + `description` frontmatter, with the
  recommended tier noted in the body (Codex can't pin a model per skill).
- `AGENTS.md` — the project instructions (`project-instructions.md`: how plays run, memory only
  through its tool, how to talk to the person — not Garura's own development guide), retitled
  for the target (Codex's equivalent of CLAUDE.md). Written as `AGENTS.md.new` if one already exists. The memory guide is the one
  exception: it is added to an existing `AGENTS.md` as a marked block (below).
- `~/.codex/config.toml` + `~/.codex/{deep,standard,fast}.config.toml` — base defaults and the
  three tier profiles (model + reasoning effort + sandbox + approval), so the model and the
  "forking"/sandbox settings the tier implies are actually selectable via `codex --profile`.
  Existing files are **kept**, never clobbered; only files this run creates are recorded.

Both tools also get:

- `.garura/core/config.yaml` — garura's config (source: `core/config.yaml`) transformed for the target (name, type
  `Project`, component paths pointed at the tool's install location, memory at
  `~/.garura/core/memory/`, the `platform`/`github` lines dropped). Kept on re-run unless
  `--force-config`.
- `.garura/project/specs/` — an empty STM scaffold.
- `.garura/.gitignore` — keeps status/resume markers (`**/status/`, `**/_status/`) machine-local
  and out of git; they sit on disk for resume and are never committed (ADR 021).
- `.garura/install-manifest.json` — the exact list of what was placed (including the tool and
  any machine-global files), so `uninstall-garura` can reverse precisely this set.
- **The memory system** (ADR 035 §8), laid by `scripts/memory_system.py`, which the public
  installer (`installer/install.sh`) runs too:
  - `.garura/core/tools/memory/` — the memory tool (from `core/tools/memory/`, without its
    tests and samples) with `settings.json` beside it. The settings name short-term memory
    (`.garura/project/issues/`, made by the install), Garura memory (read inside `.garura/`:
    `core/memory/`, then the product model `product/`), Phoenix memory's place on the machine
    (`~/.phoenix/core/memory`) and where it is downloaded from (ADR 039). A re-install
    replaces the tool and keeps settings a person edited; a tool an older install laid at
    `.garura/tools/memory/` is removed, and its settings are written new.
  - The memory guide every agent reads (`core/tools/memory/GUIDE.md`): for Claude Code,
    `.claude/rules/garura-memory.md`, which loads for every session and every sub-agent; for
    Codex, one marked block in `AGENTS.md`, added to the project's own file when it has one.
  - **The install brings no memory into the project.** The tool downloads Phoenix memory to
    its place the first time a command needs it. A play run after the install, `initialize`
    (not built yet), will set up the project's own memory. The old machine-wide copy of all
    memory (below, `--memory-dest`) is still laid until it is retired.
  - **The check.** The install runs the tool's `health` command the way an agent does. It
    fails (exit 1, after writing the manifest) when the tool cannot run or short-term or
    Garura memory cannot be reached. Phoenix memory not downloaded yet is reported, not
    failed; the check asks its source whether it answers, and notes it when it does not.

**Direct-edit deviation note (#441/ADR 021):** the `.garura/.gitignore` scaffold artifact and
its manifest record were added directly to `scripts/install.py` (and its reversal to
`uninstall-garura/scripts/uninstall.py`) as a mechanical scaffold detail within the play's
existing "writes the `.garura` tooling tree" intent — no ICE guarantee, eval, or decision
changed, so this was not routed through a recompile.

**Shared memory** goes to `--memory-dest` (default `~/.garura/core/memory`), machine-global and
shared across projects; the manifest records the resolved path. Source artifacts whose name
starts with `_` or `.`, and folders with no `SKILL.md`, are skipped.

## Pre-flight

Before running, confirm:

1. **A target is named.** The user must say which folder/repo to install into. If they didn't,
   ask — don't guess. The target is created if absent.
2. **The tool is known.** Default is `claude`. Install for Codex with `--tool codex`. If the
   user said "for codex" (or "for claude"), pass it through.
3. **You're in (or can point at) the garura checkout.** The script auto-derives the source by
   walking up until it finds `core/components/` and `core/config.yaml` (the config's source,
   ADR 040; an older checkout keeps it at `.garura/core/config.yaml`). When run
   detached from source, pass `--source <garura-checkout>`.
4. **Python 3 is available.** The script is Python 3, no third-party packages.

If a pre-flight fails, say what's missing in plain words and stop.

## Run it

From the garura repo root the source is auto-derived; you normally only pass `--target` and,
for Codex, `--tool codex`:

```
python3 core/components/plays/install-garura/scripts/install.py --target <path> [--tool claude|codex]
```

Options:
- `--tool claude|codex` — which host tool to target (default `claude`).
- `--scope full|harness` — which component set the target receives (default `full`, every
  component except the meta harness plays and the harness-only skills). `harness` installs
  only the meta plays (create-play, edit-play), the harness-only skills
  (author-product-ontology), the five *change plays, `/discover-capabilities` (it writes the
  full ICE for a harness repo's own capabilities and features, #753), and the worker
  skills/agents those plays dispatch — for harness-type repos (garura itself) that must not
  carry the other product plays. The scope filters **components only**;
  shared memory, config, the STM scaffold, and the manifest are written the same either way.
  The manifest records the scope, and since retirement is manifest-driven, re-running with
  `--scope harness` over a previously full install retires the out-of-scope components
  cleanly. The `harness` membership list lives in `scripts/install.py` (`SCOPES`) — when a
  kept play gains a new worker, add it there in the same change.
- `--source <garura-checkout>` — point at the garura checkout explicitly (needed only when the
  script can't sit beside the source).
- `--memory-dest <path>` — where shared memory goes (default `~/.garura/core/memory`). Point it
  at a temp dir for a dry test so you never touch the real machine KB. For a Codex dry test,
  also set `CODEX_HOME=<tempdir>` in the environment so the profile writes are isolated.
- `--force-config` — overwrite an existing target `.garura/core/config.yaml` instead of keeping
  it.
- `--phoenix-place <path>` / `--phoenix-source <address>` — where Phoenix memory lives on this
  machine (default `~/.phoenix/core/memory`) and where the memory tool downloads it from.
  Point the place at a temp dir for a dry test.
- `--quiet` — less output.

The script is **idempotent**: re-running re-lays the components in place and refreshes shared
memory, but preserves an existing config unless forced. Re-running never produces duplicates.

Re-running also **retires**: any component the previous install's manifest placed that this
install did not re-place (renamed or retired in source) is removed from the target and
reported as `retired:`. Only manifest-recorded paths are candidates — the user's own
skills/files are never touched. So a rename like `sud-install-garura` → `install-garura`, or
a play retirement, cleans itself up on the next install instead of leaving a stale copy.

## Report back

After the script returns, read the printed summary and the written
`.garura/install-manifest.json`, then tell the user in plain language:

- which target it installed into and **for which tool**,
- how many agents and skills/plays were installed,
- for Codex: that the tier profiles were written (or kept) under `~/.codex` and the next step
  is `codex --profile deep|standard|fast`,
- whether a config was written fresh or an existing one was kept,
- where the shared memory went,
- what the memory check said: each tier reached or not, and that Phoenix memory arrives on
  first use when it is not on the machine yet; on exit 1, what failed and what to fix,
- the one next step: open the target in the host tool and the garura skills/agents are now
  discoverable.

Keep it short. The detail lives in the manifest; your job is the human summary.

## Boundaries

- **Never hand-edit an installed copy** under a target's `.claude/` or `.agents/`. It is
  generated — edit the garura source and re-install.
- **Don't delete the user's own files.** Install only writes the Garura artifacts named above
  (and never clobbers an existing CLAUDE.md / AGENTS.md / ~/.codex config; into an existing
  `AGENTS.md` it adds only the memory guide's marked block, which the manifest records and
  uninstall removes, keeping the rest). Removing install
  artifacts is `uninstall-garura`'s job, and even that reverses only what the manifest records.
- **Protect the shared memory and the Codex home.** `~/.garura/core/memory` and any existing
  `~/.codex/*` are machine-global and merged into, never wiped, on install. When testing,
  redirect `--memory-dest` and `CODEX_HOME` to temp dirs.

**Direct-edit deviation note (#434):** this bootstrap meta-play is hand-authored (no
`intent.yaml`); the adapter split, the `--tool` parameter, and the Codex adapter were added by
direct edit to this SKILL.md and `scripts/`.

**Direct-edit deviation note (#478):** the `--scope` option (named component subsets: `full`
default, `harness` = meta plays + change chain + their workers) was added by direct edit to
this SKILL.md, `scripts/install.py` (the `SCOPES` table, the manifest `scope` field), and both
adapters' `lay_components` (an `allow` filter) — same bootstrap-meta-play path as #434; no ICE
source exists to recompile. Uninstall needs no change: it reverses what the manifest records,
and a scoped manifest records exactly what was placed.

**Direct-edit deviation note (#546):** `full` no longer means *everything*. The four meta
harness plays (create-play, edit-play, install-garura, uninstall-garura) are garura's own
build tooling and are excluded from every target install; `full` is now resolved against the
source tree at run time (`META_PLAYS` + `resolve_scope` in `scripts/install.py`), and both
adapters' `allow` filter learned a per-kind `None` ("install all of this kind"). `harness` is
unchanged — it is an explicit allow-list and still names create-play and edit-play, which
is how garura installs its own build tooling into itself.

Level 3 note (#466): bootstrap meta-play — exempt from the goal-loop recompile (no ICE
source, like create-play); runs are session-stamped by the host play when invoked through
the pipeline.
