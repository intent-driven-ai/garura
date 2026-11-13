# Feature: Commit each change by concern, with its issue named and nothing sensitive

## What it does
When the work of a change is done, every changed file is committed on the change's branch, in commits of one concern each, each in the same form and naming its issue, and a sensitive file stops the commit, so the tree is clean and the history can be read from the log alone before the change is raised.
- A concern is one coherent part of the work, such as the code of a fix, its tests, or its docs. Each commit holds one concern, so a reviewer can read each commit on its own.
- Each message has the conventional form, `type(scope): subject (#issue)`: its kind of work, the area, a plain subject and exactly one issue.
- Every changed file is committed or set aside with its reason, such as a file the repository's ignore rules leave out. The play's own run records are its last commit, so the tree it hands to the raise is clean.
- A sensitive file stops the commit, whatever the settings say:
  - a file named like a key, a certificate or a credentials file, such as `.env`, `.pem` or `id_rsa`, always stops it;
  - a secret's pattern, such as a password or a private key written in a file, stops it in code;
  - the same pattern in a document, such as the rules that name those patterns, is a warning shown to the person, not a stop, because documents carry those patterns on purpose.
- It commits only. It never pushes: the raise pushes when it opens the pull request.
- One concern is committed by script alone, with no agent. Several concerns go to an agent, which groups the files; a script then makes the commits.
- It works in rounds until the tree is clean and its proof holds, at most five rounds. After the fifth it stops and names what is left.
- Its checkpoint fires only on a sensitive file, a warning, or an issue it could not match with confidence, and it is off by setting. A warning is then shown in the run's report, and a weak issue match is recorded as weak, never made firm.
- A tree with nothing to commit ends the run with no commit.
- Examples, in different kinds of project:
  - In a clinic's booking app, a fix to the cancel button and its tests become two commits, each naming the fix's issue.
  - In a bank's payments service, a change that also holds a `.env` file with a database password is stopped, and nothing is committed until the file is out of the change.
  - In a harness repository, a rule file that names the patterns the scan looks for is committed, with a warning shown, because it is a document.
- How it meets the capability: this is the commit in "the same steps": every change reaches the raise with its work committed by concern, its issue named in each commit, and nothing sensitive in it.

Status: built, in /commit-change. Not built, or open:
- A secret's pattern in a document is only a warning, so a real secret written in a document is not stopped.
- The scan looks for secrets only. It does not look for client, company or personal references, or for home-folder paths. Scan every push for client, company and personal references (fn-scan-every-push) does that, and it is not built.
- Its record can read clean on a tree that is not, its record sits outside the folder its last step commits, and a double quote in a subject breaks its record.

## Inputs / Outputs
- In: the uncommitted changes on the change's branch.
- In: the issue, read from the branch name, or matched from the open issues when the branch does not name it.
- In: the patterns of sensitive file names and of secrets.
- Out: the commits on the branch, one concern each, each naming its issue.
- Out: the record of what was committed and what was set aside with its reason, and of each warning.
- Out: a clean tree, and nothing pushed.

## Rules & behavior
- On the change's branch, never on main. The reason: "Work is committed on a feature branch, never on main."
- One concern for each commit. The reason: a commit that mixes concerns cannot be reviewed, or taken back, on its own.
- Exactly one issue in each message, in one form. The reason: the log shows which issue each commit serves, and a reviewer reads the history "from the log alone".
- Every changed file is committed or set aside with its reason. The reason: a file left behind with no reason is work lost or work hidden.
- A sensitive file stops the commit, and no setting lifts the stop. The reason: "Sensitive files (secrets, credentials, keys) are never committed; their presence blocks the commit."
- A pattern in a document is a warning, never silent. The reason: the rules and the review's own files name the patterns on purpose, and a stop on them would stop every change to those files; the warning keeps a person's eye on it.
- Commits only, never pushes. The reason: the raise pushes once its own checks pass, so nothing leaves the machine before them.
- A script does the fixed steps, and an agent only groups several concerns. The reason: a fixed step run by an agent can drift, and grouping is the one judgment.
- At most five rounds. The reason: the cap stops a run that cannot finish; it is never a target.
- Not decided: whether a secret's pattern in a document should stop the commit, as it does in code.

## Acceptance criteria
- Given a change with a fix and its tests, when it is committed, then there are two commits, each in the conventional form with exactly one issue named, and the tree is clean.
- Given a change that holds a file named `.env`, when it is committed, then the run stops and no commit is made.
- Given a change that holds a secret's pattern in a code file, when it is committed, then the run stops and no commit is made.
- Given a change with nothing uncommitted, when it is committed, then the run ends with no commit.
- Given a commit run, when it ends, then nothing was pushed and the branch on the code host is as it was.

## Out of scope
- Opening the change and its branch. Open each change where it will land (fn-731) does it.
- Pushing, and the checks before the pull request opens. Raise each change for review against where it lands (fn-raise-change) does them.
- Scanning for client, company and personal references. Scan every push for client, company and personal references (fn-scan-every-push) does it.
- Testing the code for security. Test security, in Code → Validation, does it.

## Sources
- The product owner on 2026-11-10: "Ship every change the same way: Every change goes from opening to merge through the same steps, with a self-review, an outside review and a person's yes.", "yes, record it with self-review dropped"
- core/components/plays/commit-change/SKILL.md: "commits only; it does not push", "exactly one issue reference", "reviewable from the log alone"
- core/components/plays/commit-change/reference/ice.md: "Work is committed on a feature branch, never on main.", "Changes are grouped by concern; each commit holds one coherent concern.", "Every changed file lands in a commit or has a stated exclusion reason", "Sensitive files (secrets, credentials, keys) are never committed; their presence blocks the commit.", "an iteration cap of 5"
- core/components/plays/commit-change/scripts/analyze_changeset.py: "A content match in these paths is a NON-BLOCKING warning", "a content match anywhere else, and every FILENAME match (.env, .pem, id_rsa, ...), stays a hard block."
- .garura/product/product-os/software-delivery-planning/test-security/capability.md: "keeping a secret's value out of each commit, and landing the change. Ship every change the same way, in Developer tooling, owns them."
