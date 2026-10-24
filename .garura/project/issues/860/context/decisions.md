# Decisions for #860, the product owner, 2026-10-25

1. The rule covers everything installed: plays, loops, sub-agents, skills, their scripts and reference files, the shared `_shared/` files and the tools. Each refers only to the installed version of a file. A pointer in an installed file points to another installed file.
2. Fix every real run-time read of `core/components/` or `core/tools/`.
3. Notes of origin ("source of truth", "canonical copy", "compiled from core/...") are deleted from installed parts, not reworded: once deployed, the source makes no sense.
4. commit-change's changeset analysis sorts every path of the repo (core, `.garura`, docs ...). It stays as it is.
5. create-play, edit-play, create-loop, edit-loop, install-garura and edit-ontology work on the source only, never on the installed copy. Dev tests run on the source only.
6. Every tool under `core/tools/` is deployed to `.garura/core/tools/` by the installer (except the play-reviewer prototype), because plays and skills use them after the install. Wherever a tool is used, it is referred to inside the install folder, never the source.
7. Memory is never read by path. Every part reads it through the memory tool.
8. `~/.garura/core/memory` stays for now. It goes once the memory tool is fully live, and Phoenix becomes the home of memory.
9. The review rule groups per project are held for `initialize` (#862).

## Round 2 (2026-10-25)

10. Installed parts do not point to `docs/` either: the install never copies `docs/`.
11. The Codex installer is deprecated for now; it is to be redesigned completely. `--tool codex` stops with a plain message.
12. check-change hands the Next-line map to lint_play; a check keeps the copies of `lint_play.py` identical to the tool.
13. The rule gets its own ADR (the product owner accepts it).
14. open-pr and check-quality (model, allowed-tools, sections) go to chore #861.
15. intent-resolver may have the Bash tool, for the memory tool.
16. The note deletions in start-, propose- and merge-change stay; the conflict with plan 717 is resolved when the plans meet.
