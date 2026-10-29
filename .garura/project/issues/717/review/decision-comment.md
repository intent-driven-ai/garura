Harness verdict (gate off per gates.plays.check-change): approve

No blocking finding (no P1). Every suite the change touches is green: plan tool 15, link-model-part 17, shape-plan writer 9, shape-slice scripts 129, install 75. The plan files all read with the six statuses; /shape-slice's thin check finds no problem on the model. This is a recorded harness verdict, not a human review.

**Categories reviewed:** harness, memory and product-model (design-grounded from committed sources on main), executable-code, tests, documentation, config-maps; plan-files and run-evidence read by hand (no playbook yet).

**Fixed during this review:** the exact Thin line and the re-marked pages; the plan tool's plain messages for missing git, a non-folder repo and a non-mapping node; the spine skill's refusal of a malformed request; and the home-folder path and the person's name removed from every run record (filed as #982 so plays stop writing them).

**Findings — {'P3': 13, 'P4': 12, 'P2': 2}**

P2:
- **H-01** (harness) The skill now writes on intent pages (`kind: intent`, step 5, the Rules line "On an intent page, change only the lines the request names"). On main the same Rules line says "Never write ... an intent page". An intent page is a sha
- **H-02** (harness) The "Never" bullet "Write a shared model file yourself (the spine, the profile, an intent page)" is replaced by "Change the product model by hand. You may change any part of it ... but only through a skill (the product owner, 2026

P3:
- **Q-01** (code-and-tests) plan() is one function of 77 lines with about 43 branch points; it carries the whole decision of which model files change, in a script that writes the product model. Hard to test branch by branch and to review.
- **Q-02** (code-and-tests) check() is 68 lines with about 33 branch points: it runs every stop-condition check in one function.
- **Q-03** (code-and-tests) check() is 73 lines with about 31 branch points: it runs every stop-condition check in one function.
- **Q-04** (code-and-tests) The README never says plan.py needs the PyYAML package (plan.py imports yaml) or which Python version runs it, and does not list exit codes 0 and 1 (only exit 2 is named). A person setting the tool up on a bare machine finds neith
- **H-03** (harness) The new routing row and the description ("any play or run that finds a part the model lacks") give the keeper an order of work and a fan-out: "one run per part, in parallel when there are several (each writes only its own page); o
- **H-04** (harness) The Context of both ICE sources points to `.garura/project/issues/719/specs/design.md` ("#719 design"). The install lays reference/ice.md into the project (.claude/skills/list-plans/reference/ice.md), but the design note is a shor
- **MEM-1** (memory) Rule 19 replaces the GOAL / DONE / NOW / NEXT / WAIT tree with a tree of six statuses that hides Done and Dropped, and no decision record carries the change. ADR 030 item 7 is the committed source of the old rule: its tree has a D
- **MEM-2** (memory) Rule 19 now describes the status view of the plan files (.garura/project/plans/<id>.yaml, read by /show-plan), but the file it sits in is the rulebook for the work plan at {stm_base}{issue}/specs/plan.md. The file's title, 'Where 
- **MEM-3** (memory) The six node statuses (Not Started, In Progress, Now, Blocked, Done, Dropped) are defined only here, in the branch's own new text. The committed Plan kind gives the plan one Status of active, done or dropped, one `Now` item, and s
- **MEM-4** (memory) The template says a change to a mark or a line is made in its settings block, never in the tool, and each status has a `shown` setting. The tool does not honour that fully: core/tools/plan/plan.py counts a plan's open nodes as eve
- **PM-1** (product-model) The new feature page has only 'What it does' and the Agent intent section, so it misses four of the five required headings (Inputs / Outputs, Rules & behavior, Acceptance criteria, Out of scope). The grounding linter goes from 70 
- **PM-2** (product-model) The feature reads git (branches, commits ahead of and behind main), and its output changes when git changes, but its parent capability cap-719 (not changed by this PR) says plans are shown "from the plan files alone", with the lim
- **PM-3** (product-model) The page says the tree opens with "the legend first, with the marks of Not Started, In Progress, Now and Blocked". The tool, as built, prints a legend of all six statuses (it shows the Done and Dropped marks too: '○ Not Started · 

P4:
- **Q-05** (code-and-tests) RepoPlansTest skips itself (self.skipTest) when the repository has no plans folder, and otherwise reads the repository's live plan files, so the test result changes when someone edits a plan. It ran, not skipped, in this check.
- **Q-06** (code-and-tests) Two bare 'except Exception' blocks (lines 49 and 93) turn any failure into None or a default marker with no message, so a broken ledger or marker file is silently treated as absent. The same file is copied to show-plan.
- **Q-07** (code-and-tests) Four scripts are byte-for-byte copies across list-plans and show-plan (session_stamp.py, preflight.py, check_stop_condition.py), and safe_write.py is a byte-for-byte copy in link-model-part and shape-slice. A fix to one copy must 
- **Q-08** (code-and-tests) Committed run records carry the author's local home path (~/...) and the author's first name. Seen in 717/context/resolved-rules.json, 719/context/pr-body.md, self-review.md, resolved-rules.json, templates/manifest-close-start-cha
- **H-05** (harness) The description says "Read only and position none: it writes nothing". The play writes its working folder and, when evidence.record resolves true, an evidence file at the close (Step C1). Its own ICE (C2) is narrower and correct: 
- **MEM-5** (memory) The prose still tells the person to pick the next piece of work 'from the plan (one plan for each business intent, with done / now / next) or from /list-focus-issues'. The same file now maps two plays, /list-plans and /show-plan, 
- **MEM-6** (memory) The two new rows do not line up with the row above (`list-focus-issues: {`). The yaml still parses, so this is layout only.
- **PM-4** (product-model) Issue #806's "Done when" asked for more than the page covers: the plan's links (identified_by, needs_plans) on the graph, and each plan's open and landed issues. The agreed design section of the same issue narrows it to branch, ah
- **PM-5** (product-model) The three pages carry the fixed line "Thin: proposed by `/shape-slice` from the person's answers". None of them was proposed by /shape-slice: fn-628 and fn-729 were written earlier and re-marked, and fn-806 was added by the #719 c
- **PM-6** (product-model) The scrub of the product owner's name (10 occurrences, now 0) is complete and well made: roles in place of the name, and the confirmation by a person kept on each Stage line. But it is outside the agreed design and scope of #719 (
- **PM-7** (product-model) Information only, not a fault of the diff. The ontology (v13) puts a feature's ICE on its own page (ice.md) and says it is "never a section of the feature page". The model's feature pages still hold the ICE as an inline '## Agent 
- **PM-8** (product-model) Cross-category note for the memory review. fn-628 drops its Fails-if line "a done line does not say decided, built or shipped" (agreed on issue #628, 2026-10-29: Done nodes are hidden). The committed work-plan rule 10 on main stil

**Routing:** approve → merge into main, squashed so main's history carries only the scrubbed records. The P2 findings are decisions to record (an ADR for the spine writer and intent-page edits; ADR 030's status tree), not code fixes.
