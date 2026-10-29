**Reviewer's verdict (human, product owner): approve.**

Round 2. All ten round-1 findings (H1–H10) are fixed; H11–H15 are filed as #951. Layer 1: the three change plays pass the play linter; the component linter finds nothing new (create-play's 4 errors were there before); ADR 060 lints clean; ontology v13 is valid; all 16 shared test files and the linter's own tests pass.

Left for a follow-up chore (no P1, no P2):

- **N1 (P3)** `core/components/plays/start-change/SKILL.md`:4 — The frontmatter description still says the play cuts "a feature branch off up-to-date main". The ICE intent (reference/ice.md:11-13) and the lead of the same file (lines 10-14) now say an issue in a plan gets a sub-branch of its plan's branch. The description of the other two plays was updated in the same change.
- **N2 (P4)** `core/components/plays/merge-change/SKILL.md`:172 — Step 3 and the evals SE-6, SCE-1 and SCE-4 still say the run records are committed "on main" and that "main is level with origin". For an issue in a plan the script commits and pushes on the plan's branch (merge_pr.py pushes to the base it was given). SE-3 and SCE-5 are already right.
- **N3 (P3)** `core/components/plays/start-change/scripts/setup_branch.py`:82 — The fix for the stale plan branch (H10) deletes the local plan branch whenever origin shows none, using git branch -D. A failed lookup of origin (offline, or a host error) prints nothing, so _on_origin reads it as "not on origin". The delete also does not check that the local branch holds commits that exist nowhere else. The push on line 108 is not checked either, so a local-only plan branch is po
- **N4 (P4)** `core/components/plays/create-play/references/test_setup_branch.py`:87 — Four test names and comments carry the round-1 review labels (H1, H4, H9, H10). The labels point to a review file that is not part of the product. The stamped scripts themselves are clean.
- **MEM-1 (P3)** `.garura/product/product-os/features/fn-673/feature.md`:4 — An agent that reads the product model page for this feature learns the old landing rule and believes it still holds. The page is not in this diff and is outside the ontology, so it does not block this change. It is the one place left that keeps the old rule alive.

The 16 standards items on `core/tools/lint-components/lib/rules/shared-scripts.js` are checks with no tool to run them (each matched because the file changed), not defects.
