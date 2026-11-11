# #1021's last model work: the plan shown to the product owner (not applied)

2026-11-11. From #1021's work order: "delete the 5 old ones", "Merge the old capabilities in, keeping the 33 features", "Drop every line naming a particular plan, delete the one slice", and "Plans: delete all seven, with plans/788/ and its evals." Every intent but the parked BI-5 is reviewed and closed. Nothing is applied before the product owner's yes. Landing #1021 is asked for separately.

## Steps (each through product-os-keeper and its skills, or project-orchestrator for the plans)
1. enrich-grounding, named lines (lines-request.json): 25 lines on 17 pages; changes-diff.md shows each.
   - "for bi-788" leaves the five "To be deepened later" marks; ids of old intents and old capabilities give way to titles; Sources that cite the two old capability pages cite the copies in old-pages/; Sources that cite the five moving feature pages cite their new paths; the four lines naming a particular plan (/shape-plan 788, /shape-eval 788 with plans/788/, plan 717) name none.
2. remove-model-part (remove-request-1.json): repoint Build a plan and its three features from bi-717 and bi-788 to bi-1; Write the hidden eval and its two features from bi-788 to bi-3; drop bi-717 and bi-788 from the domain; remove the slice sl-intent-to-design and its record.
3. remove-model-part (remove-request-2.json): remove the five old intent pages, bi-717, bi-722, bi-734, bi-756, bi-788.
4. link-model-part (link-request.json): file fn-727, fn-728 and fn-818 under Turn intents into agent work, and fn-798 and fn-898 under Write the evals, each page moved into its new capability's folder.
5. remove-model-part (remove-request-3.json): merge the two emptied capabilities, Build a plan into Turn intents into agent work and Write the hidden eval into Write the evals; their pages go.
6. author-intent-page: BI-1's Touches gains 3 lines and BI-3's 2, each "changes"; every other line kept.
7. remove-plan, through project-orchestrator: delete the seven plan files (606, 717, 722, 734, 756, 767, 788) and plans/788/ with its evals, by name only, never opened. Every plan is Paused or Done with no branch. Git keeps them.
8. My checks: only the named lines changed; the index lost exactly the two capabilities, the slice and nothing else, and gained no part; no page names a removed id or an old path; BI-1 and BI-3's Touches equal the parts naming them; the plans folder is empty of the seven; no new structure error; no personal path. Then commit on "commit and cp".

## Left as it is
- The five moved features keep their pages as they are, with their ICE still inside the page; each gets its own ICE page under #765 (move each ICE to its own page).
- One index line still names a plan in metadata no skill can change: fn-931's `created_by: '/update-plan (plan 717, ...)'`.
