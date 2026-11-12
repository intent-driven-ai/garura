/shape-plan and /design-eval move to one epic per plan and one Feature issue per feature (ADR 068, ADR 069), and the product model now holds each feature's own state (ADR 070, ontology v18).

- /shape-plan: one epic and one Feature issue per feature still to build; no Stories. It reads each feature's state from the model, leaves out Completed and Dropped features, and sets Planned on the features it takes in, after the product owner's yes. A closed Feature issue is opened again on the yes; never a second one.
- /design-eval: one eval for the plan over its Feature issues; dropped slices and dropped plan items are left out.
- The model: a feature's `status` (Unplanned, Planned, In progress, Completed, Dropped) in the spine schema and link-model-part; the old status field is gone; Garura's own spine is swapped (all features Unplanned until the confirmed clean-up marks the built ones Completed).

Closes #1025
Closes #1034
Closes #1035

Also serves #975 (code done; its live-tracker check cannot be shown), #954 (the managing-work guide still owes its text) and #1056 (later steps owed: /start-work, merge-work, /reshape-plan, /design-slice, the clean-up). These stay open.

# Self-review: #1025 (/shape-plan reworked to one epic per plan and one Feature issue per feature), with the feature state from #1056

Rules: the base self-review rules (standards/rules/self-review.md, Phoenix memory), no project override.
Branch: feature/1025-shape-plan-reuses-open-story, against main. 27 commits (2 are merges of main), 132 files, +9950 -2657. Nothing is blocking.

## What the branch does

/shape-plan now makes one plan with one epic, and one Feature issue for each feature that is not yet built. It reads each feature's state from the product model, leaves out Completed and Dropped features without searching the tracker, sets Planned on the features it takes in (after the person's yes), opens a closed Feature issue again instead of filing a second one, and files no Stories. /design-eval now writes one eval for the whole plan, over Feature issues, and leaves out dropped slices and dropped plan items. The product model now records each feature's state: the spine schema, the model-linking skill (set a state, one-time move off the old status), the scripts that wrote the old status, the model-keeper agent, the direct-model-write rule, and Garura's own spine (the old status is off 280 entries, and all 239 features read Unplanned). The ready check and the plan helpers read each part by its own shape.

Size, by kind: 52 hand-written files in core (+3071 -1778), 18 test files (+1649 -442), 15 repeated copies of three shared scripts (+718 -155), 45 run records (+4271), 1 spine file (+239 -280), 1 docs line pair. Read one copy of each shared script: the 8 platform-adapter copies, the 3 plan-helper copies and the 4 ready-check copies each have one checksum.

## Which issues this covers

- #1025 (/shape-plan reuses an open story instead of filing a second one): fully covered in intent. A feature's earlier work is found again with no plan file, and a rebuilt plan files no second set. The mechanism is not the one the issue text names: the model holds no issue number any more (ADR 068, ADR 069), so the work is found by the exact `Represents: <feature id>` line on a Feature issue, and no Stories are filed. Tests: no plan file, found by the line and never by title, a second match stops the run, a closed issue is opened again, two slices share one feature (test_find_work_items.py, test_scenarios.py S12 to S19). The issue text still says "story" and "named in the model" and is out of date.
- #1034 (the ready check and plan helpers misread older parts): fully covered. Run on Garura's own model after the spine swap, the ready check reads 279 entries as partly ready and none as not ready, and none stops on "no ICE".
- #1035 (the work-items change drafts older features' stories from words): fully covered. The feature copy script, run on the real model for fn-818, now returns ready with a clean ICE copy; its test passes.
- #975 (/shape-plan expected only Stories under an Epic): covered in the code, the play's intent and the tests. A Feature issue under the epic is the plan's own item, not misplaced work, and the tracker check, plan-file check and misplaced-work search accept it. One acceptance line cannot be shown: "/shape-plan 788 runs on today's tracker". Plan 788's file is gone and its epic is closed, so the first rebuilt plan is the real run. Also, the issue text says Stories sit under the Features; this play now files none.
- #954 (one Epic for each plan): not fully covered. The play, its intent, the tracker check, the plan-file check and the scenario for two slices all do one epic for the plan, and the ontology on main already says so. But the issue's last criterion, writing the rule in the managing-work guide, is not done: that guide still says an Epic stands for one slice and a plan holds one Epic for each slice.
- #1056 (the model records each feature's state): partly covered. Done here: the spine and schema, the model-linking skill (set a state, one-time migration), the scripts that add features (new feature reads Unplanned, a domain or capability gets no status), the model-keeper agent, the direct-model-write rule, Garura's own spine, and /shape-plan setting Planned. Not done here, and named by ADR 070: /start-work setting In progress, /merge-work and /reshape-plan setting Completed, Dropped and bring-back, /design-slice reading state from the model, the one-time Completed clean-up for features built before ADR 068 (all 239 read Unplanned), the glossary Feature row and the Work Tracking text in CLAUDE.md.

## Scope checks

- Matches the issue: PASS for #1025, #1034, #1035 and #975, with the notes above. The #1056 and #954 pieces ride along on purpose: the rework cannot read or set a state without them, and the commits name #1056.
- No scope creep: PASS. Each group of files maps to one of the issues above. Design-eval and the model-state files are part of the stated rework.
- Reasonable size: NOTE. 132 files and about 10,000 added lines is large for one sitting. About 4,300 lines are run records and about 700 are repeated script copies, so the real review surface is the shape-plan and design-eval plays (SKILL.md, ICE, scripts, tests) and the link-model-part change.
- No stray artifacts: PASS. No debug prints, no commented-out blocks, no scratch files; the added lines hold no absolute path and no home-folder path. The committed run records include copies of memory files and a full PR diff under the issue's review folder; they are records, not stray, but they are bulky.

## Quality checks

- Tests present: PASS. All of these ran and pass: the shape-plan suites (find 21, tracker 17, scenarios 23, states 15, drafts 18, plan 12, gather 32, brief 17, write 26 and the rest), the design-eval suite (70), reshape-plan (feature copy and plan helpers), design-slice (all files), specify-capabilities, specify-domains, the model-linking skill (58), the ready check (49) and the plan tool (21). Play lint on shape-plan and design-eval: 0 gaps; the fingerprint of each play file matches its ICE source.
- Commits are clean: PASS. All 25 non-merge commits are conventional and name an issue (#1025 or #1056). Two merges of main are in the history. A few subjects are long (over 120 characters).
- No secrets: PASS. Scanned the added lines for keys, tokens, passwords and private key markers; the only hits are the review rule table's own search patterns.
- Docs in step: PARTIAL. Done: ADR 068 to 070 and the ontology are on main, the plan tool README, the platform-adapter docs, the agent docs, the eval rule and templates. Owed: the managing-work guide (#954), the glossary Feature row, CLAUDE.md Work Tracking, and `specify-capabilities/reference/ice.md` line 59, which still says a seeded capability gets `status: proposed` while its play file was changed by hand to "no status" (the ICE source and the play file now disagree, and the next rebuild would bring the old text back).
- Nothing obviously broken: PASS. No leftover TODOs; no merge conflict with main (merge-tree is clean); the whole-repo component linter reports 36 errors, none in a file this branch touches (all in build-play, build-loop, fix-play, fix-loop, install-garura, uninstall-garura and four older skills); the model linter on Garura's own model gives the same 21 errors and 279 warnings as on main.

## Findings (none blocking)

1. The PR on GitHub is behind the branch. GitHub holds the earlier head (the first story-reuse version, 39 files); this branch has 75 commits the PR does not show, and the PR title and text still describe story reuse. The earlier validate-work approval and the earlier self-review and PR-body records in the issue's folder cover that old head only. After the push, the title, the text and the records must be refreshed, and validate-work run again on the new head.
2. /reshape-plan, /start-work and /merge-work are not yet moved to the Feature-issue shape and the feature state (ADR 070 names each). /reshape-plan's play file still speaks of Stories under the epic (29 mentions, none of a Feature issue). The plans /shape-plan now writes (epic, then Feature issue nodes) are read by it through the shared plan helper, whose tests pass, but its own steps are not reworked. No open issue was found for this; one is owed under #1056.
3. Garura's own spine still has 23 feature entries that carry an `issue:` line, which ontology v18 forbids (a feature names no issue). Same count on main, so not new here, but the swap commit says the spine is moved to v18.
4. The PR text, when refreshed, should say which issues it covers fully (#1025, #1034, #1035), which in part (#975's live run, #1056) and which not (#954), so the orchestrator can choose the closing keywords.
