## Story #1019: three skills let an approved reorganisation run

Closes #1019. It sits under #722 (a product model can be managed).

### What a person gets

The product owner approved a reorganisation of Garura's business intents on 2026-11-02. Three of its jobs had no skill, and the model and the plans change only through a sub-agent and a skill. These three make those jobs possible. Nothing here runs them; the reorganisation is its own change.

- **`remove-model-part`**: repoints a part's business intents one part at a time, removes an intent's page once nothing names it, merges a capability into another, and removes a slice. A merge leaves no record of itself in the model. It refuses while any page still mentions what is going, and it needs the name of the person who approved it. All or nothing.
- **`author-intent-page`**: writes or rewrites a business intent's page under its issue number, from a draft, including its Touches list. It never drafts a word, and it writes confirmed only when told who confirmed.
- **`remove-plan`**: deletes plans and their folders. It refuses a plan on a live branch or one a remaining plan needs, and it never opens a file under a plan's folder.

### What else changed

- The verb `remove` joins the naming rules, in `naming.yaml` and `naming.md`.
- `product-os-keeper` and `project-orchestrator` list their skills. `product-os-keeper`'s never-remove rule now allows `remove-model-part`, because a request names the person who approved it.
- A harness install lays all three, with a test.
- The skills page lists them.
- The rule on who may write the model's index now names `link-model-part`'s and `remove-model-part`'s scripts.

### Checks

- Acceptance check, written first and failing before the build (68 of 84 failed): 87 of 87 pass now. One check was wrong and was fixed in its own commit, with the reason in its message.
- Tests: `remove-model-part` 63, `author-intent-page` 50, `remove-plan` 31, install 76. All pass.
- Component linter from the repo root: 36 errors and 1 warning, the same as before this work, none in a file this change touches.

### Owed after merge

- Phoenix memory's copy of `naming.yaml` has no `remove` verb. The product owner chose to leave this for now, because the verbs change next.
- The skills reach this repo's installed copy only on an install the product owner asks for.

### Self-review

# Self-review for #1019 (three skills that let an approved reorganisation remove model parts, write intent pages and delete plans)

Base: main. Twenty commits. Rules: the base self-review rules, with no project override (`resolved-rules.json`). This is the third pass, over the branch after the product owner's changes: a capability merge now leaves no record on the survivor, and the rule file for direct model writes names the two writers of the spine outside a play.

The three skills, their wiring and their tests do what the issue asks. Two points from the first pass still hold and a few small ones remain. None of them holds up the raise.

Blocking findings: none.

## Scope

- Matches the issue: yes. The change adds `remove-model-part`, `author-intent-page` and `remove-plan`, each with its `SKILL.md`, a script and tests. It adds the verb `remove` to the naming rules with its one meaning. It lists the skills in `product-os-keeper` and `project-orchestrator`, lays them in the harness install, and updates the skills page in the docs.
- Two additions go past the issue's first words, and both were asked for. `author-intent-page` writes the Touches list from the draft. The rule file `direct-model-write.md` now names `link-model-part`'s and `remove-model-part`'s scripts as writers of the spine outside a play; the agent text already did, and the rule file lagged behind it.
- The merge change is consistent across the code, the tests, the `SKILL.md` and the agent table: the survivor gets the intents and decisions, no `merged_from` note, and the report's `merged` list is the only record of the run. The issue text says the same.
- The issue's boundary holds. Nothing in the product model, the plans or any other issue is changed. The only files under `.garura/` in the diff are this issue's own run records.
- Size: the code, docs and wiring are about 3,100 added lines, nearly half of them tests. The rest is run records, the eval check and the check-change round 1 files (a saved copy of the pull request diff makes most of it). Three skills in one story is what the issue asks for.
- The verb `remove` and its wording stay as they are, and the Phoenix memory copy of the naming rules is not promoted, as the product owner said. That is left alone here.

## Quality

- Personal references: none. Checked over every one of the twenty commits from main to HEAD, in three passes: the added lines of each commit; each commit's message, author and committer fields; and the full content of every file the branch changes, read at each commit. The words searched were the account name, its dashed form, the sandbox scratch folder names, the system temp folders, any home-folder path, the first and last name, and the company and project names. The only hits are the author's own name in the standard commit author field, and one line in a saved diff of a lint rule that holds the text of a URL pattern (not a path to this machine). No file the branch changes holds more hits than on main, and the untracked review files in the issue folder are clean. A control file on main that carries the name returns hundreds of hits, so the scan works. The home-folder paths found in the first pass stay gone.
- Tests present: yes. Run on this branch, all pass: `remove-model-part` 63, `author-intent-page` 50, `remove-plan` 31. The install tests (76) pass, and the install code and tests are unchanged since that run. The new merge tests check that no record, no issue number and no one-line text of the merged capability stays in the spine, and that a removed id hidden in a part's notes still refuses the request.
- Component linter, run from the repo root: 36 errors and 1 warning, the same as before. All are in other plays and skills. None is in a file this change touches.
- Commits are clean: conventional format, one concern each, each names #1019. No Claude attribution lines.
- No secrets or keys in the diff.
- Docs in step: yes. The skills page, both agent tables, the naming rules and the direct-write rule are updated.
- Nothing obviously broken: no debug output, no left-over TODOs.

## Findings

1. A capability merge can refuse with no way forward when the capability carries a decision. This is not blocking. The merge moves the decision's pointer to the surviving capability, but the decision's own file (`decisions/*.yaml`) still names the old capability in its `node_ref`. The mention check scans that file and refuses, and the page skill (`enrich-grounding`) changes only `.md` pages. A scratch test just now reproduced it again, and the merge went through only after the decision file was edited by hand. The same shape appears when a slice is repointed to a new intent and its old intent is then removed: the slice's own record file still lists the old intent, the spine entry is repointed but the record is not, and the removal refuses. On today's model neither case is hit by the planned reorganisation (the one slice is removed, not repointed, and the only decision belongs to a capability that cannot merge anyway because feature pages sit in its folder). Either repoint those fields in the same all-or-nothing pass, or write in `SKILL.md` that these two cases refuse and who handles them.

2. The `Serves` line is not a part of the ontology's Business Intent kind. This is not blocking, and no change is asked. The ontology says a business intent points only at its capabilities, the intents it was identified by and, loosely, its domains. The product owner approved the line for the 11 intents that say they serve #539 (Garura becomes true product engineering, with IDSD and ADLC as the operating model), and it stays as plain text. The proposal of 2026-11-02 is not in the repo, so this review could not read it. Nothing reads the line today. If it is to be a lasting part of the kind, the ontology needs it through `/edit-ontology`, or the alignment check may later report these pages as drifting.

3. A rewrite cannot clear a Touches list. This is not blocking. An empty `touches` list is treated as "the draft gives none", so the old block is kept; the only way to change it is to give at least one entry. The `SKILL.md` says so and a test covers it, but "an empty list gives none" can be read as "clears it". If a kept intent loses all its parts after a repoint, its page keeps stale lines until someone gives a new list. Say it more plainly in `SKILL.md`, or let an empty list clear the block.

4. Touches accepts the kind `feature`, which the ontology's text for the Touches property does not (it names domains and capabilities, and says a feature is reached through its parent capability). This is not blocking. The existing Touches writer in the shape-slice play accepts it too, and a real intent page already carries a feature line, so this matches how pages are written today and differs only from the ontology's words.

5. The eval commit also carries three template copies (the manifest and two files under `context/templates/standards/`) that belong with the start-change run records. This is not blocking and is only tidiness. Moving them means rewriting the commits again, so it is probably not worth it.

Closed since the first pass: the personal paths in the record files; the wrong sentence in the `SKILL.md` about what `author-business-intent` writes; and the loss of an earlier merge's record, which is gone because a merge no longer keeps any record on the survivor. One consequence to know, by the product owner's choice: after a merge, the merged capability's issue number is no longer in the model, and only the report of the run and the tracker hold it.

Worth knowing for the next step, not a defect here: `remove-model-part` writes no page. After it repoints parts to a new intent that already has a page, that page's Touches list changes only if the page is rewritten through `author-intent-page` with the new `touches`, which needs the whole draft again.
