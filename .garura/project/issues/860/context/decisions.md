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

## Round 4 (2026-10-25, the review of PR #864)

17. Fix every finding of the review: the 3 SEC-07 hits, the 3 P2 (H1–H3), the 11 P3 (H4–H11, M1, M2, M6) and the 7 P4 (H12–H15, M3–M5). The product owner's words: "fix p1 and p2 and 14 small and 7 cosmetic ones too".
18. SEC-07 is fixed in the rule, as #851 fixed SEC-18 and BE-19: it fires on an unsafe load (`pickle`, `marshal`, `yaml.load` without a safe loader, `yaml.unsafe_load`) and on `JSON.parse` of request-shaped input, not on every `JSON.parse`. The rule reaches Phoenix memory only after this change merges: the branch is never its own standard.
19. Layer 1 lints the parts the PR changes, where they sit in the repository under review, with the installed tools: the source layout when the PR changes `core/components/`, the installed layout otherwise. Only violations in a changed path become findings; the rest are counted as there before.
20. A laid tool that crashes is "did not run", never a pass. The install gets each tool's packages and runs each tool's smoke check; a failure stops the install and names the tool.
21. The memory reading protocol and the failure format live once, in a shared file for agents, laid in the installed `_shared/` folder. A shared script writes a short-term copy and its manifest line. The concurrent grounding agents each write their own copy folder and manifest.
22. Templates come only from template-manager. A play hands an agent without the Task tool the template copy it needs.
23. The naming tool is a source-only tool: the install does not lay it.
24. The install keeps the tools' packages and caches out of git in a project (an ignore file in `.garura/core/tools/`).
25. ADR 055 gets four factual corrections before it merges: the check-pr-quality contract changes shape, the ADR 038 citation is §5, intent-resolver gains Bash only for the memory tool, and the agents' shared file and the tools ignore file are named.
