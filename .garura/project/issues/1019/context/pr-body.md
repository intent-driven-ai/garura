## Story #1019: three skills let an approved reorganisation run

Closes #1019. It sits under #722 (a product model can be managed).

### What a person gets

The product owner approved a reorganisation of Garura's business intents on 2026-11-02. Three of its jobs had no skill, and the model and the plans change only through a sub-agent and a skill. These three make those jobs possible. Nothing here runs them; the reorganisation is its own change.

- **`remove-model-part`**: repoints a part's business intents one part at a time, removes an intent's page once nothing names it, merges a capability into another, and removes a slice. It refuses while any page still mentions what is going, and it needs the name of the person who approved it. All or nothing.
- **`author-intent-page`**: writes or rewrites a business intent's page under its issue number, from a draft, including its Touches list. It never drafts a word, and it writes confirmed only when told who confirmed.
- **`remove-plan`**: deletes plans and their folders. It refuses a plan on a live branch or one a remaining plan needs, and it never opens a file under a plan's folder.

### What else changed

- The verb `remove` joins the naming rules, in `naming.yaml` and `naming.md`.
- `product-os-keeper` and `project-orchestrator` list their skills. `product-os-keeper`'s never-remove rule now allows `remove-model-part`, because a request names the person who approved it.
- A harness install lays all three, with a test.
- The skills page lists them.

### Checks

- Acceptance check, written first and failing before the build (68 of 84 failed): 87 of 87 pass now. One check was wrong and was fixed in its own commit, with the reason in its message.
- Tests: `remove-model-part` 60, `author-intent-page` 50, `remove-plan` 31, install 76. All pass.
- Component linter from the repo root: 36 errors and 1 warning, the same as before this work, none in a file this change touches.

### Owed after merge

- Phoenix memory's copy of `naming.yaml` has no `remove` verb. Lint on an installed project using that copy will reject these three names until the product owner promotes it.
- The skills reach this repo's installed copy only on an install the product owner asks for.

### Self-review

# Self-review for #1019 (three skills that let an approved reorganisation remove model parts, write intent pages and delete plans)

Base: main. Twelve commits, 35 files. Rules: the base self-review rules, with no project override (`resolved-rules.json`). This is the second pass, over the branch after the commits were rewritten to clean the record files.

The three skills, their wiring and their tests do what the issue asks. The personal-path problem from the first pass is gone. Three smaller points from the first pass still hold, and two small points are new. None of them holds up the raise.

Blocking findings: none.

## Scope

- Matches the issue: yes. The change adds `remove-model-part`, `author-intent-page` and `remove-plan`, each with its `SKILL.md`, a script and tests. It adds the verb `remove` to the naming rules with its one meaning. It lists the skills in `product-os-keeper` and `project-orchestrator`, lays them in the harness install, and updates the skills page in the docs.
- One addition goes past the issue's words, and it was asked for: `author-intent-page` now writes the Touches list of an intent from the draft, and keeps or replaces it on a rewrite. The issue only said a rewrite keeps the Touches list. It stays inside the same skill and the same page.
- The issue's boundary holds. Nothing in the product model, the plans or any other issue is changed. The only files under `.garura/` in the diff are this issue's own run records.
- Size: 35 files and about 4,700 added lines. About 1,640 of those are run records and the eval check. Of the code, docs and wiring (about 3,070 lines), nearly half is tests. Three skills in one story is what the issue asks for, and each skill reads on its own.
- Stray artifacts: none in the code. One small mix-up in the commits is finding 4.

## Quality

- Personal paths: gone. Checked over every one of the twelve commits from main to HEAD, not only the tip, for the account name, its dashed form, the sandbox scratch folder names, the system temp folders, any home-folder path, and the bare first and last name and the company and employer names. Three passes: the added lines of each commit, each commit's message and author fields, and the full content of every file the branch changes, read at each commit. All came back with zero hits. The same scan on an old file on main that is known to carry the name returned many hits, so the scan does find the pattern. No file the branch changes holds more hits than it did on main. The two files that held the paths (the manifest and `eval-before.json`) now carry repo-relative paths. The working tree and the review files of this issue are clean too. The remote branch still sits at main's tip, so nothing from this branch is pushed.
- Tests present: yes. Run on this branch, all pass: `remove-model-part` 60, `author-intent-page` 50 (14 new for Touches), `remove-plan` 31, and the install tests 76. The tests cover each refusal in the issue and check that a failed delete or a failed report write puts every file back.
- Checked against real data: the scripts were run on scratch copies of the real product model and the real plans. Nothing in the repo was touched. Merging two plan capabilities worked and kept the spine's comments and layout. Removing the one slice worked. Removing every plan that nobody needs worked, and removing plan 722 (a product model can be managed, and grows as plans are built) was refused, correctly, because plans 717 (people plan work toward a business intent) and 756 (the agent intent is its own part of the model) need it.
- Component linter, run from the repo root: 36 errors and 1 warning, the same as before. All are in other plays and skills. None is in a file this change touches.
- Commits are clean: conventional format, one concern each, each names #1019. No Claude attribution lines.
- No secrets or keys in the diff.
- Docs in step: yes. The skills page, both agent tables and the naming rules are updated, and the `author-intent-page` row in the agent table now says what a rewrite keeps.
- Nothing obviously broken: no debug output, no left-over TODOs.

## The new Touches code in `author-intent-page`

Read in full and run. On a copy of the real intent page for #788 (agents design a named piece of work), a rewrite kept the old Touches block and the What-was-done block byte for byte. A rewrite with touches replaced the block. A new page got the block just before What-was-done. The written lines match the existing reader that the shape-slice play uses for Touches. Links to a missing file, a file outside the model, an absolute path, a link with a fragment and a link with a closing bracket were each refused, and the page was left as it was. A title with a square bracket or a line break is refused, which keeps every line readable by that reader. The `SKILL.md` now says the optional fields `rules`, `serves`, `identified_by` and `touches` are added by the caller, which is true: `author-business-intent` writes none of them. The first-pass finding about that sentence is closed. Two small points are findings 5 and 6.

## Findings

1. A capability merge can refuse with no way forward when the capability carries a decision. This is not blocking. The merge moves the decision's pointer to the surviving capability, but the decision's own file (`decisions/*.yaml`) still names the old capability in its `node_ref`. The mention check scans that file and refuses, and the page skill (`enrich-grounding`) changes only `.md` pages. A scratch test with one decision reproduced it. The same shape appears when a slice is repointed to a new intent and its old intent is then removed: the slice's own record file still lists the old intent, the spine entry is repointed but the record is not, and the removal refuses. On today's model neither case is hit by the planned reorganisation (the one slice is removed, not repointed, and the only decision belongs to a capability that cannot merge anyway because feature pages sit in its folder). Either repoint those fields in the same all-or-nothing pass, or write in `SKILL.md` that these two cases refuse and who handles them. The code is unchanged since the first pass.

2. A merge forgets earlier merges. This is not blocking. When capability A is merged into B, B records A's issue number. If B is later merged into C, only B's number is recorded; A's record is lost with B. A tiny test model showed it. The issue says a merged capability's issue number stays on record. The planned four-into-one merge is one request into one survivor, so it is safe. Fix by carrying the removed capability's own `merged_from` list to the survivor. The code is unchanged since the first pass.

3. The `Serves` line is not a part of the ontology's Business Intent kind. This is not blocking, and no change is asked. The ontology says a business intent points only at its capabilities, the intents it was identified by and, loosely, its domains. The product owner approved the line for the 11 intents that say they serve #539 (Garura becomes true product engineering, with IDSD and ADLC as the operating model), in the approved proposal of 2026-11-02, as reported by the session; that proposal is not in the repo, so this review could not read it. The line is optional and only written when the caller adds it. If it is to be a lasting part of the kind, the ontology needs it through `/edit-ontology`, or the alignment check will later report these pages as drifting.

4. The eval commit also carries three template copies (the manifest and two files under `context/templates/standards/`) that belong with the start-change run records. This is not blocking and is only tidiness. Moving them means rewriting the commits again, so it may not be worth it.

5. A rewrite cannot clear a Touches list. This is not blocking. An empty `touches` list is treated as "the draft gives none", so the old block is kept; the only way to change it is to give at least one entry. The `SKILL.md` says so, and a test covers it, but the words "an empty list gives none" can be read as "clears it". If a kept intent loses all its parts after a repoint, its page will keep stale lines until someone gives a new list. Say it more plainly in `SKILL.md`, or let an empty list clear the block.

6. Touches accepts the kind `feature`, which the ontology's text for the Touches property does not (it names domains and capabilities, and says a feature is reached through its parent capability). This is not blocking. The existing Touches writer in the shape-slice play accepts it too, and a real intent page already carries a feature line, so this matches how pages are written today and differs only from the ontology's words.

Worth knowing for the next step, not a defect here: `remove-model-part` writes no page. After it repoints parts to a new intent that already has a page, that page's Touches list changes only if the page is rewritten through `author-intent-page` with the new `touches`, which needs the whole draft again.
