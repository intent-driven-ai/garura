## Decision
Every installed part refers only to installed files. `core/components/` and `core/tools/` are Garura's source, which is precompiled code; the install compiles and deploys it.

1. When an installed part runs (a play, loop, sub-agent, skill, its scripts and reference files, the shared `_shared/` files, a tool), it never reads, runs or names a path under `core/components/` or `core/tools/`, and never points to Garura's own documentation under `docs/`, which the install does not copy. A pointer in an installed file points to another installed file.
2. Memory is never read by a folder path. Every part reads it through the memory tool: the agent fetches the file into the issue's short-term memory, and the skill reads that copy.
3. The installer deploys every tool under `core/tools/` to `.garura/core/tools/<name>/` (not the play-reviewer prototype). `lint_play.py` becomes its own tool. Every use of a tool names its installed place. lint-components can check the installed layout.
4. Notes of origin ("source of truth", "canonical copy") are deleted from installed parts: once a part is deployed, its source makes no sense to it.
5. The source-only parts are the named exceptions: create-play, edit-play, create-loop, edit-loop, install-garura, uninstall-garura, edit-ontology and author-product-ontology; dev tests; and repo-layout text that names the folders of the repo under review or being worked on (commit-change's path sorting, a project's own `docs/adr/`, a review's grounding folders, the review taxonomy's path globs).
6. The lint rule `installed-paths/source-path` checks the rule, in both layouts. The rule is written in CLAUDE.md and the harness standard.
7. The Codex installer is deprecated until it is redesigned (#863): `--tool codex` stops with a plain message.
8. `~/.garura/core/memory` is still written by the install for now; it goes once the memory tool is fully live and Phoenix is the home of memory.

## Why now
#860 (P1): installed parts read Garura's source tree at run time. In Garura's own repo this works by chance, because the source is there; in a product project the folders do not exist and the parts break after the install. Found when the review of PR #858 read its rules from `./core/components/memory/...`. The product owner, 2026-10-25: "When these skills are run (literally executed), they should not touch core components. That is precompiled code." and "this is true for everything installed, not just skills".

## Options considered
- Leave the source paths and rely on Garura's own repo — lost: every product project breaks after the install.
- Copy the source tree into every project — lost: the source is not what a project runs, and two copies drift.
- Install only the memory tool and skip the steps that need other tools — lost: plays use those tools after the install; a skipped step is a hidden gap.

## Decided by
the product owner

## Decided in
plan 788, issue #860, 2026-10-25

## Shape
markdown
