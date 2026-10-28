**Reviewer verdict (human): reject.**

Nothing blocks the change itself, but the product owner asked for the six severity-3 findings to be fixed before the merge:

1. **H-1:** the helper's instruction page (`core/components/skills/platform-adapter/SKILL.md`, lines 25 and 139) still says 16 commands, and forbids adding any beyond 16, while the same page lists 23. Fix: say 23.
2. **H-2:** the page's "unknown command" message lists 18 of the 23 commands, and the five older GitHub-only commands have no entry in the GitHub or GitLab reference pages. An agent following the page would call them unknown. Fix: list all 23, and give each of the five an entry.
3. **H-3:** two doc lines (`SKILL.md` line 37, `reference/github/verbs.md` line 33) say the compare command is for pull requests over 3,000 files, but the script tries it first for anything over 300. Fix: reword both.
4. **Q-001:** the play builder's copy of the context test (`core/components/plays/create-play/references/test_fetch_pr_context.py`) has no compare cases, though its copy of the script changed. Fix: add them.
5. **Q-002:** the three tries have no pause between them, and they retry failures that can never succeed. Fix: wait between tries, and stop at once on a "not found" or a command the host does not support.
6. **Q-003:** for a pull request from a fork, the compare call names the fork's branch as if it sat in the main repository, which can read the wrong diff. Fix: name the fork's owner in the compare call.

Five severity-4 findings are filed as one chore. Findings with their sources: `.garura/project/issues/889/review/findings.yaml`.
