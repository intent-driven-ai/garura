# Feature: Scan every push for client, company and personal references

## What it does
Before any change play pushes to the code host, one scan reads every file in the commits it pushes, and stops the push, with nothing pushed, when it finds a client or company name, a personal reference such as a person's own email, or a home-folder path, so no such reference reaches the repository or its history.
- The rule is the product owner's: "No client reference and no personal reference — not in files, not in history". A push to a shared or public repository publishes at once, and a reference in the history stays in the code host's records even after the branch is rewritten.
- Every push a change play makes is scanned, not only the change's own files:
  - the raise's push of the branch;
  - the review's push of its own records;
  - the push of main's plan file when a plan's work starts, and the merge's push of its own records.
- What the scan looks for in every file it reads:
  - the names on the project's list of clients and companies it protects;
  - personal references, such as a person's own email or user name;
  - a home-folder path, a path inside a person's home folder, or a session's scratch folder, which hold the user name and the layout of the machine.
- The list of names is kept outside the repository, because a list of client names in the repository is itself the reference the rule forbids.
- The plays write every path in their records relative to the repository's root, so the scan finds nothing to stop in a clean run.
- Examples, in different kinds of project:
  - In a consultancy's product repository, a review record names the client the work is for; the push of that record stops, and nothing leaves the machine.
  - In an open-source library, a run record holds a path in the developer's home folder; the push stops and names the file and the line.
  - In a bank's payments service, a clean change is scanned and pushed with no stop.
- How it meets the capability: nothing sensitive reaches the code host on any step of the path, the same for every change.

Status: not built. The commit's scan looks for secrets only: keys, credentials and secret patterns. Nothing scans a push for client, company or personal references, and the review's records are committed and pushed with no scan. The rule is not yet in project memory, where the reviews would read it. Run records committed today hold home-folder paths, such as the path of the self-review's rules file. Planned: a scan of every push for client, company and personal references, with the rule in project memory and only repository paths in run records.

## Inputs / Outputs
- In: the commits a change play is about to push, and every file in them.
- In: the list of names the project protects, kept outside the repository.
- In: the shapes of a personal reference and of a home-folder path.
- Out: the push, when nothing is found.
- Out: when something is found, no push, and a message that names each file and line.

## Rules & behavior
- Every push a change play makes runs the scan first. The reason: a review record that named a company was pushed at once by the review's own step, after the scan of the change's own files was done.
- A found reference stops the push; it is never only a warning. The reason: a reference that reaches the code host stays in its records; when it happened, "The branch had to be rewritten and force-pushed".
- The list of names never sits in a file in the repository. The reason: "The list of names the rule protects is kept outside every repository, on the machine only."
- Paths in the plays' records are relative to the repository's root. The reason: an absolute path in a record "publishes the person's user name and folder layout".
- Not decided: where the list of names lives and how the scan reads it. One plan puts the rule in Garura's project memory and the list on the machine only; another says the scan reads "its word list from the project's own memory", and Garura memory sits in the repository.

## Acceptance criteria
- Given a commit that adds a protected name to a review record, when a change play pushes it, then the push stops and nothing reaches the code host. This is not built.
- Given a run record that holds a home-folder path, when the raise pushes it, then the push stops and the message names the file and the line. This is not built.
- Given a clean change, when it is pushed, then the scan passes and the push goes through. This is not built.

## Out of scope
- Keeping a secret's value out of each commit. Commit each change by concern, with its issue named and nothing sensitive (fn-commit-by-concern) does it.
- Checking the change against the project's rules in the review. Check the code against its standards, in Code → Validation, does it.
- Writing the rule and the project's own memory. Standards, structure, settings and memory owns it.

## Sources
- The product owner on 2026-11-10: "Ship every change the same way: Every change goes from opening to merge through the same steps, with a self-review, an outside review and a person's yes.", "yes, record it with self-review dropped"
- The product owner's rule of 2026-10-18: "No client reference and no personal reference — not in files, not in history", "Every path a play writes into a run record is relative to the repository root, or uses `~` for the home folder."
- core/components/plays/commit-change/scripts/analyze_changeset.py: "Scans the changeset for sensitive files"
- core/components/plays/check-change/SKILL.md: "commits+pushes the review run artifacts"
- core/components/plays/merge-change/scripts/merge_pr.py: "PUSHES the records commit"
