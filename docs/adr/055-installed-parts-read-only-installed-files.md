# ADR 055 — Installed Parts Read Only Installed Files, Because Garura's Source Is Precompiled Code

**Status:** Accepted
**Date:** 2026-10-25
**Level:** framework
**Decided by:** the product owner · **Decided in:** plan 788, issue #860, 2026-10-25
**Amends:** ADR 039 — §5 "The `.garura/` layout": `.garura/core/tools/` holds every tool the install lays, one folder for each (`.garura/core/tools/<name>/`), not only the memory tool; the memory tool stays at `.garura/core/tools/memory/`, and the play-reviewer prototype is never laid; the rest of §5 stands
**Affects:** the install — `core/components/plays/install-garura/scripts/install.py` (lays the tools, records them in the install manifest, and stops at once for `--tool codex`), `core/components/plays/install-garura/scripts/tools_system.py` (new: lays each tool of `core/tools/` except `memory` and `play-reviewer` in `.garura/core/tools/<name>/`), `core/components/plays/install-garura/scripts/test_install.py`, `core/components/plays/install-garura/SKILL.md`, `core/components/plays/uninstall-garura/scripts/uninstall.py` (removes the laid tools) and `installer/install.sh` (runs the same script); the tools — `core/tools/lint-play/lint_play.py` (new tool; `create-play` and `edit-play` keep copies in their `scripts/` folders, which the linter holds identical to it), `core/tools/lint-components/lib/rules/installed-paths.js` (new rule `installed-paths/source-path`, in both layouts) with `core/tools/lint-components/test/installed-paths.test.js`, and `core/tools/lint-components/index.js` (`--layout installed`); the rule text — `CLAUDE.md` and `docs/standards/harness-standard.md` (principle 11); the parts that read the source until now — `core/components/plays/check-change/` (`SKILL.md`, `reference/ice.md`, `scripts/fetch_pr_context.py`), `core/components/agents/quality-auditor.md`, `core/components/skills/check-pr-quality/` (`SKILL.md`, `reference/input-contract.md`, `reference/finding-schema.md`), `core/components/plays/discover-intent/reference/ice.md`, `core/components/plays/shape-slice/reference/ice.md`, `core/components/loops/_shared/loop-run.md`, `core/components/plays/_shared/play-close.md`, and the other plays, loops, agents and skills on the #860 branch that named `core/components/` or `core/tools/`
**ICE impact:** `/check-change` changes in its guarantees. C2: the check-knowledge shelf is read only through the memory tool; `change-reviewer` copies the playbooks into the issue's short-term memory. C10: `fetch_pr_context.py` names no memory folder. A new C12: Layer 1 runs the installed tools (`.garura/core/tools/lint-components/index.js --layout installed` and `.garura/core/tools/lint-play/lint_play.py`), never the source; when a tool is not installed, the review records "not installed" for that check, which is never a pass and never a halt. F13 and REC13 match C12. `/discover-intent` and `/shape-slice` change in wording only: their text points to installed places (the rebuild eval tool, the ontology through the memory tool, each skill as an installed sibling folder); no guarantee changes in meaning. Other plays get direct edits to path text that change no guarantee. `quality-auditor` and `check-pr-quality` change the values in their contract (the severity taxonomy is now a short-term copy), not the shape of the contract. The ICE kind does not change.
**Business intent check:** none — a framework decision on what an installed part may read and where the install lays the tools. The Business Intent kind and its rules do not change, and no page in `.garura/product/product-os/intents/` names any part here. The harness standard (bi-734) gains a principle that serves its outcome; its outcome, proof and limits do not change.
**Related:** ADR 035, ADR 038, ADR 039, ADR 040, ADR 046, ADR 054, #860, #863, PR #858, plan 788

## Context

Installed parts read Garura's source folders when they run (#860, priority P1). In Garura's own repository this works only by chance, because the source is there. A product project that installs Garura has no `core/` folder, so these parts break after the install. The problem was found when the review of PR #858 read its rules from `./core/components/memory/...`.

The product owner, 2026-10-25: "When these skills are run (literally executed), they should not touch core components. That is precompiled code." And: "this is true for everything installed, not just skills".

Older records already say parts of this rule:

- ADR 035 §4 and ADR 039 §2 say memory is read only through the memory tool, and a skill reads only what its agent puts in short-term memory.
- ADR 038 §4 says agents call the memory tool, never a path.
- ADR 039 §9 says the install lays the shared close file beside the plays.
- ADR 054 §2 says the rule for asking a person is read by its installed path.
- ADR 040 §2 says `core/` is the source and `.garura/` is the installed copy.

But no record says the rule for every installed part, and no record says where the other tools go. The install laid only the memory tool, so a play that ran the component linter or the play linter had to run it from the source.

## Decision

### 1. An installed part refers only to installed files

When an installed part runs, it never reads, runs or names a path under `core/components/` or `core/tools/`. An installed part is a play, a loop, a sub-agent, a skill, their scripts and reference files, the shared `_shared/` files, or a tool. It also never points to Garura's own documentation under `docs/`, because the install does not copy it. A pointer in an installed file points to another installed file.

### 2. Memory is never read by a folder path

Every part reads memory through the memory tool. The agent fetches the file into the issue's short-term memory, and the skill reads that copy.

### 3. The install lays every tool

- The installer lays each tool under `core/tools/` in `.garura/core/tools/<name>/`. It does not lay the play-reviewer prototype.
- `lint_play.py` becomes its own tool, `lint-play`.
- Each use of a tool names its installed place.
- The component linter (`lint-components`) can check the installed layout.

This amends ADR 039 §5. Its tree showed `.garura/core/tools/` with the memory tool only.

### 4. Notes of origin are deleted

Notes such as "source of truth" or "canonical copy" are deleted from installed parts. When a part is installed, its source is not available to it, so the note has no use.

### 5. The source-only parts are named exceptions

These parts work on the source by design, and the rule does not apply to them:

- the plays `create-play`, `edit-play`, `create-loop`, `edit-loop`, `install-garura`, `uninstall-garura` and `edit-ontology`, and the skill `author-product-ontology`;
- dev tests;
- text that names the folders of the repository that is under review or is being worked on: the path sorting of `commit-change`, a project's own `docs/adr/`, the grounding folders of a review, and the path globs of the review taxonomy.

### 6. A lint rule checks the rule, and the rule is written down

The lint rule `installed-paths/source-path` checks the rule in both layouts: the source layout and the installed layout. The rule is written in `CLAUDE.md` and in the harness standard (`docs/standards/harness-standard.md`, principle 11).

### 7. The Codex installer is deprecated until it is redesigned

`--tool codex` stops with a plain message and writes nothing. The Codex installer is redesigned in #863.

### 8. The machine-wide memory copy stays for now

The install still writes `~/.garura/core/memory`. It stops when the memory tool is fully live and Phoenix memory is the home of memory.

### 9. What this changes in older records

- **ADR 039 §5** — `.garura/core/tools/` holds every tool the install lays, one folder for each, and not only the memory tool. The rest of §5 stands.

These records do not change:

- **ADR 017 §1.** ADR 039 §10 made its whitelist the tree of ADR 039 §5. So the change is made in ADR 039 §5, and a reader of ADR 017 finds it through the pointer on ADR 039.
- **ADR 035 §4 and §8, ADR 038 §4, ADR 039 §2 and §9, and ADR 054 §2.** Each already says a part of this rule, for memory or for a shared file. This ADR makes the rule general. No line of them changes.
- **ADR 040 §2.** This ADR builds on it.
- **ADR 046.** It names plays, loops, skills and agents. A tool folder is not one of these, and no name changes. The harness standard gains a principle; the naming decision does not change.
- No older ADR decided that the install supports Codex, so part 7 amends none.

## Consequences

### Positive

- An installed part works in a product project, where `core/` does not exist.
- One rule, checked by a linter in both layouts. A new source path cannot land.
- Each tool is installed. A play that runs a tool after the install finds it at one known place.

### Negative / Risks

- The source-only exceptions are a fixed list in `installed-paths.js`. A new source-only part must be added to that list by hand, or the linter fails it.
- A fix to a tool reaches a project only on the next install of Garura there, as ADR 038 says for the memory tool.
- People who use Codex cannot install Garura until the Codex installer is redesigned (#863).
- The install still writes `~/.garura/core/memory`. So the rule holds for installed parts, but the install itself still writes a memory folder.
- A Node tool is laid with its `node_modules` folder, so the installed tools folder is large.

## Alternatives Considered

- **Leave the source paths and rely on Garura's own repository** — lost: every product project breaks after the install.
- **Copy the source tree into every project** — lost: the source is not what a project runs, and two copies drift apart.
- **Install only the memory tool, and skip the steps that need other tools** — lost: plays use those tools after the install, and a skipped step is a hidden gap.

## Work This Creates

- After acceptance: the forward pointer on ADR 039.
- Redesign the Codex installer (#863).
- Stop writing `~/.garura/core/memory` when the memory tool is fully live and Phoenix memory is the home of memory.

## References

- `.garura/project/issues/_adr/20261024T211640Z/brief.md` — the brief
- The review of PR #858, which read its rules from `./core/components/memory/`
- `core/tools/lint-components/lib/rules/installed-paths.js` — the lint rule
- `docs/standards/harness-standard.md` — principle 11
