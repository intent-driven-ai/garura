**[BUG] Plays write a person's home-folder path into the run records they commit, and nothing stops the push**

## What is wrong

Plays write absolute local paths — a person's home folder, such as `/Users/<name>/...` — into the run records they commit under `.garura/project/issues/<issue>/`, and nothing checks for it before a commit or a push. The repository is public, so each push publishes the path at once.

Found on 2026-10-29 by the check-change review of PR #981 (plan 717 landing on main): 12 committed run-record files on `plan/717/base` held the home-folder path, and one more already on main from the PR #950 run. The person's name was also quoted inside copied diffs. The files were scrubbed before the merge and the merge was squashed so main's history does not carry them; the old commits stay in the pull request records of #980 and #981.

## Where it comes from

- `propose-change`: `resolved-rules.json` records the absolute path of the self-review rules file (Phoenix memory resolved under the home folder).
- `check-change`: the component linter's JSON output (`lint-components.json`) lists every violation with its absolute file path; the saved `pr.diff` copies carry whatever the diff carries.
- The run's text records (`self-review.md`, `pr-body.md`, template manifests) quote absolute paths.
- The session stamp markers also hold the path; they sit in `status/`, which git ignores, so they are not committed.

## Expected

- Every path a play writes into a run record is relative to the repository root, or uses `~` for the home folder.
- A machine check refuses a commit or a push that adds a home-folder path, a client name or a personal email — the scan the product owner's rule asks for "before every push". `commit-change`'s sensitive-file scan is the natural place; the pre-merge reviews (#672) are the second net.

## Rule

No client reference and no personal reference — not in files, not in history (the product owner, 2026-10-18).

## Related

- #672 — the pre-merge reviews enforce the no-client-names rule from project memory.
- #952 — Garura's way of working defined as engine rules and settings.
- #981, #980 — where it was found.
