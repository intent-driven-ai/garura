## What this delivers

**Phoenix memory has its own home.** `intent-driven-ai/phoenix-memory` is a private repository, seeded with everything in Garura's memory (`core/components/memory/`): 147 of 147 files identical, plus its README. It is cloned at `~/.garura/phoenix-memory/`.

**Memory is clean before it moved.** No client name, company name, personal name, personal knowledge-vault link or home-folder path is left in memory (3 commits).

**Two commands to bring memory into a project.** `pull` copies a piece from Phoenix memory into the project's Garura memory and records it in `pulled.json` (path, Phoenix version, fingerprint). `pulled --behind` names pieces that changed in Phoenix memory since. They live in `core/tools/memory/pull.py`, for the memory tool (#657) to use. 12 tests pass.

**Dead memory settings are gone.** Nothing read `components.memory`, `ltm.source` or `ltm.global-target`. All three are removed from `.garura/core/config.yaml`, and the installer no longer writes a memory line into projects' config.

**The PR review rules are read from Garura memory.** `standards.pr-severity-taxonomy` now points at `.garura/core/memory/standards/rules/pr.md`. Kapil, 2026-10-18: "Skill should always point to .Garura core memory … If nothing exists because it hasn't been pulled, it will actually fail, and that is the whole point." The file gets into Garura memory when the pull tool runs.

**Both plans carry Kapil's decisions of 18 October** (`.garura/project/issues/656/specs/plan.md`, `.garura/project/issues/653/specs/plan.md`):
- The installer pulls nothing. Three set-up plays, not filed yet, will fill a project's first memory.
- `core/components/memory/` moves into Phoenix memory. It is removed after the memory tool exists, and then its readers are fixed: ADRs, docs, 35 skills, 7 agents and 2 scripts.
- Skills read only short-term memory, or call an agent for context. Memory is read in order: short-term, then Garura memory (`.garura/`), then Phoenix memory.
- The memory tool comes first (#657). Its test is Kapil's login and change-password story.

Closes #656

## Where the issue text no longer matches

The issue on GitHub still describes the first version of this story. Kapil changed it on 18 October; the plan is current, the issue text is not.

| Issue says | What happened |
|---|---|
| The Phoenix memory repository exists and holds the seeded content | Delivered |
| An install pulls only the starting set | Dropped: the installer pulls nothing (Kapil: "it install with no memory") |
| A check shows which pulled pieces are behind | Delivered, as `pulled --behind` |
| Neither stale copy is written or read | Moved: `.garura/` clean-up is #670; the tool's test covers the rest |
| A project with nothing pulled still runs its plays | Holds; nothing changed it |
| Memory keys point at Phoenix and Garura memory | Partly: 3 dead keys removed, PR rules key moved; `review-pr.standards_order` unchanged |

## Not in this change

- The memory tool (#657), on its own branch.
- Removing `core/components/memory/` and fixing what reads it, after the tool.
- ADR 035 §2 (it still says the installer pulls a starting set): its own `/adr` change.
- The `.garura/` clean-up (#670).

## Self-review

Rules: `standards/rules/self-review.md` from Phoenix memory (Garura memory had no copy). Blocking: **0**. Non-blocking: 13. Full review: `.garura/project/issues/656/context/self-review.md`.

Checks run: `pull` tests 12/12; memory contract check passes; the installer's config rewrite loads for both host tools; memory-reading tests 30 and 37 pass; both plan checks valid; merges cleanly with main; no client, personal or secret strings in the diff, memory or Phoenix memory.

For the reviewer (non-blocking):
- The PR rules setting points at a folder git ignores, and the copy there is the old 30 May one. A fresh clone has no such file. This is what Kapil asked for.
- One commit subject (`d65770f8`) is 84 characters; the rules allow 72.
- The `install-garura` play text still says installed config has memory at `~/.garura/core/memory/`.
- A refused `pull` still leaves an empty `pulled.json`. For #657.

## After the first review (harness reject)

The first review rejected on one P1: rule DATA-18 on the demo address `t@example.com` in `core/tools/memory/test_pull.py`, a throwaway test repository. Kapil approved it as an exception ("these are demos emails, and part of tool that is using this as sample data. this is exception that is approved"); a comment at the line records it (`9bbada8a`). The 9 memory wording findings are fixed (`218a2d54`), in Phoenix memory too (`5fcd88e`, pushed).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
