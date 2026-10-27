Installed parts read only installed files. `core/components/` and `core/tools/` are Garura's source, which is precompiled code: the install compiles and deploys it, and a product project has no `core/` folder. Until now, installed parts read the source at run time, so they broke after an install. ADR 055 (accepted) records the rule.

Closes #860 (a priority-one bug).

## What changes

- **The install lays every tool.** `install-garura` (new `tools_system.py`) lays each tool under `core/tools/` into `.garura/core/tools/<name>/`: lint-components (with its `node_modules`), the new `lint-play`, naming and rebuild-eval. It does not lay the play-reviewer prototype, tests or caches. The manifest records the tools; a reinstall removes a tool that left the source, and uninstall removes them all. `installer/install.sh` runs the same step.
- **`lint_play.py` is its own tool** (`core/tools/lint-play/`). create-play and edit-play keep copies, and a new lint check keeps every copy identical to the tool.
- **lint-components can check the installed layout** (`--layout installed --target .claude`).
- **Every use of a tool names its installed place.** check-change runs the installed linters and hands lint_play the Next-line map (fetched through the memory tool); a missing tool is recorded as "not installed", never a pass and never a halt. discover-intent runs the installed rebuild eval.
- **Memory is read only through the memory tool.** quality-auditor fetches the review rules (`pr.md`) into short-term memory and passes that copy to check-pr-quality; change-reviewer fetches the review playbooks; the other agents that read memory by a path do the same for their skills. `fetch_pr_context.py` names no memory folder. The config key `standards.pr-severity-taxonomy` goes.
- **Pointers name installed files.** list-focus-issues, tech-designer, /shape-slice SE-25, track-issue and the close steps of fix-bug, build-epic, refactor-code and validate-epic. No installed part points to Garura's own docs; five agents now hold their failure format in their own text.
- **Notes of origin are deleted** from installed parts ("source of truth", "canonical copy"), including the old edit-history sections of four change plays.
- **The Codex installer is deprecated** until it is redesigned (#863): `--tool codex` stops with a plain message and writes nothing.
- **A lint rule checks the rule** (`installed-paths/source-path`), in both layouts, with the source-only plays, dev tests and repo-layout text as named exceptions. The rule is written in CLAUDE.md and the harness standard (principle 11).
- **An empty-project test** installs into a folder with no `core/`, runs the installed linter, fetches `pr.md` through the installed memory tool and runs the installed review scan with it, runs the installed `fetch_pr_context.py`, and checks that no installed file names the source.

## For the product owner's eye

1. `~/.garura/core/memory` is still written by the install (decision 8); it goes once the memory tool is fully live.
2. The `intent-resolver` agent has the Bash tool now, so it can call the memory tool.
3. The edit notes removed from start-, propose- and merge-change will meet plan 717's rewrite of those plays (#731, #673); that conflict is resolved when the plans meet.
4. Seven plays failed the play check before this change; none gains a gap.

## Checks

| Check | Result |
|---|---|
| Hidden acceptance checks (rounds 1–3), written before the build and kept from the builder | 22 / 22 pass |
| Python tests (52 files), install tests (60 tests incl. 6 empty-project tests) | all pass |
| lint-components tests | all pass |
| Old-name check | passes |
| Component lint errors | 37 → 36; no `installed-paths` error |
| Play check (lint_play) | no new gap on any play |

## Round 4 — every finding of the first review fixed (decisions 17–25)

- **SEC-07 fires only on unsafe loads** (`pickle`, `marshal`, `yaml.load` without a safe loader, `yaml.unsafe_load`, `JSON.parse` of request input). A plain `JSON.parse` of a file or a tool's own output is no finding. It reaches Phoenix memory only after this merges.
- **A laid tool must run.** The install gets a Node tool's packages (`npm ci --omit=dev`), runs a smoke check on every laid tool, and stops with a plain message naming a tool that fails. It writes `.garura/core/tools/.gitignore`; uninstall removes it. The naming tool is source-only and is not laid.
- **The review lints what the PR changes, where it sits.** When the PR changes `core/components`, the installed tools lint the source layout; else the installed layout. Only a violation in a changed path is a finding; the rest are counted as "there before". A tool that crashes is "did not run", never a pass.
- **The review's fan-out writes no shared file.** Step 2 copies what the review shares; each grounding agent writes its own `grounding-<category>/` folder. change-reviewer writes each category's treatment into `categories.yaml`, and the play reads only that.
- **One shared memory protocol for agents.** `agents/_shared/` holds the memory reading protocol, the failure format and `copy_memory.py`; 11 agents point to them, and a new lint rule (`memory-reading/*`) checks it.
- **Templates come only from template-manager.** check-change and record-decision ask it and hand the copy on (both recompiled); the orchestrators ask it themselves.
- **lint_play and lint_loop need the Next-line map** (`--next-map`, else exit 2); no memory-folder fallback.
- **Docs:** the Codex install is marked stopped (#863) in the glossary, CLAUDE.md and README; install/uninstall-garura list what they lay and remove; harness-standard principle 11 names ADR 055.
- **ADR 055, factual corrections for the product owner's eye:** the ADR 038 citation is §5; check-pr-quality's contract changes shape (`standards_set` became `standards_order`, a list of short-term copies); intent-resolver gains Bash only for the memory tool; the tools ignore file, the agents' `_shared/`, the source-only naming tool and the smoke check are named.

| Round 4 check | Result |
|---|---|
| Hidden acceptance checks (35; 13 new, written first and failing before the build) | 35 / 35 pass |
| install tests | 74 OK |
| lint-components tests | 6 files pass |
| scan tests / loop-lint tests / copy script tests / change-fetch tests | 27 / 39 / 11 / 13 pass |
| Component lint (source) | same 18 error kinds as before, none new |
| Play check | no new gap on any changed play |

The product owner's decisions: `.garura/project/issues/860/context/decisions.md`. Filed on the way: #862 (initialize: a project gets only the memory and review rules that fit it), #863 (redesign the Codex installer).
