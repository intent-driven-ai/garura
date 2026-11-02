# Self-review for #1019 (three skills that let an approved reorganisation remove model parts, write intent pages and delete plans)

Base: main. Nine commits, 33 files. Rules: the base self-review rules, with no project override (`resolved-rules.json`).

The three skills, their wiring and their tests do what the issue asks. One thing must be fixed before the branch is pushed: personal paths sit in two record files. Four smaller points follow. None of those four holds up the raise.

Blocking findings: 1.

## Scope

- Matches the issue: yes. The change adds `remove-model-part`, `author-intent-page` and `remove-plan`, each with its `SKILL.md`, a script and tests. It adds the verb `remove` to the naming rules with its one meaning. It lists the skills in `product-os-keeper` and `project-orchestrator`, lays them in the harness install, and updates the skills page in the docs.
- The issue's boundary holds. Nothing in the product model, the plans or any other issue is changed. The only files under `.garura/` in the diff are this issue's own run records.
- No scope creep in the skills' purpose. Two small additions go past the issue's words: the `Serves` part in the intent page (finding 4) and the `decisions` move in a capability merge (finding 2).
- Size: 33 files and about 4,500 added lines. About 1,650 of those are run records and the eval check. Of the rest, about half is tests. Three skills in one story is what the issue asks for, and each skill reads on its own.
- Stray artifacts: none in the code. The three template copies inside the eval commit are a small mix-up (finding 5).

## Quality

- Tests present: yes. Run on this branch, all pass: `remove-model-part` 60, `author-intent-page` 36, `remove-plan` 31, and the install tests 76 (one new test checks the harness install lays all three skills). The tests cover each refusal in the issue and check that a failed delete or a failed report write puts every file back.
- Checked against real data: the scripts were run on scratch copies of the real product model and the real plans. Nothing in the repo was touched. Merging two plan capabilities worked and kept the spine's comments and layout. Removing the one slice worked. Removing every plan that nobody needs worked, and removing plan 722 (a product model can be managed, and grows as plans are built) was refused, correctly, because plans 717 (people plan work toward a business intent) and 756 (the agent intent is its own part of the model) need it.
- Component linter, run from the repo root: 36 errors and 1 warning, all in other plays and skills. None is in a file this change touches.
- Commits are clean: conventional format, one concern each, each names #1019. No Claude attribution lines.
- No secrets or keys in the diff. The personal paths are finding 1.
- Docs in step: yes. The skills page, both agent tables and the naming rules are updated.
- Nothing obviously broken: no debug output, no left-over TODOs.

## Findings

1. BLOCKER: personal paths are committed in two record files.
   - Files: `.garura/project/issues/1019/context/templates/manifest-close-start-change.json` (2 lines) and `.garura/project/issues/1019/evidence/eval/eval-before.json` (23 lines).
   - They hold the machine's full home-folder path, with the account name. Both come in with the commit "test(eval): acceptance check for the three reorganisation skills, failing before the build". No tracked file on main holds this path.
   - Why it stops the raise: the repo is public, and the owner's rule is no personal reference in files or in history. Nothing from this branch is pushed yet (the remote branch still sits at main's tip), so this is the last cheap moment to fix it.
   - Fix: change those paths to repo-relative ones, in the commit that added them and in the commits after it, before the first push. A new commit on top that only edits the two files would leave the paths in the pull request's history. This review changed nothing; rewriting commits is the caller's call.

2. A capability merge can refuse with no way forward when the capability carries a decision. This is not blocking. The merge moves the decision's pointer to the surviving capability, but the decision's own file (`decisions/*.yaml`) still names the old capability in its `node_ref`. The mention check scans that file and refuses, and the page skill (`enrich-grounding`) changes only `.md` pages. A scratch test with one decision reproduced it. The same shape appears when a slice is repointed to a new intent and its old intent is then removed: the slice's own record file still lists the old intent (the real record names it at line 16), the spine entry is repointed but the record is not, and the removal refuses. On today's model neither case is hit by the planned reorganisation (the one slice is removed, not repointed, and the only decision belongs to a capability that cannot merge anyway because feature pages sit in its folder). Either repoint those fields in the same all-or-nothing pass, or write in `SKILL.md` that these two cases refuse and who handles them.

3. A merge forgets earlier merges. This is not blocking. When capability A is merged into B, B records A's issue number. If B is later merged into C, only B's number is recorded; A's record is lost with B. A tiny test model showed it. The issue says a merged capability's issue number stays on record. The planned four-into-one merge is one request into one survivor, so it is safe. Fix by carrying the removed capability's own `merged_from` list to the survivor.

4. `author-intent-page` takes parts the ontology does not give a business intent, and its `SKILL.md` says the wrong thing about the draft. This is not blocking. The ontology's rule is that a business intent points only at its capabilities, the intents it was identified by and, loosely, its domains. The page writer accepts a `Serves` line that points the other way, and nothing in the issue or the ontology asks for it. Also, `SKILL.md` says `author-business-intent` writes `rules`, `serves` and `identified_by` in its draft; it writes none of them. Remove `Serves`, or say where it comes from, and correct the sentence about the draft.

5. The eval commit also carries three template copies (`manifest-close-start-change.json` and two files under `context/templates/standards/`) that belong with the start-change run records. This is not blocking. While the commit is rewritten for finding 1, they can move to the record commit.

Worth knowing for the next step, not a defect here: `remove-model-part` writes no page, so after it repoints parts to a new intent, that intent's page does not list them under Touches. Another step must write those lines.
