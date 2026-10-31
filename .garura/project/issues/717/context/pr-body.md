Plan 717 lands on main: people plan work toward a business intent, and pick it up across days and people. Refs #717.

The plan is Done (set by the product owner with /update-plan): its epic #956 is closed as completed, 31 items are Done and 4 Dropped. The business intent #717 stays open — business intents are never closed by finishing their work.

## What lands

Every story came in through its own reviewed pull request into `plan/717/base`: #995, #998, #1003, #1006, #1008, #1009, #1010, #1012, #1013 and #1016 (#732, #733, #980, #984, #987 are on main already). The other commits on the branch are run records, plan-file updates, one install record and one merge of main.

- Build a plan (/shape-plan), view plans (/list-plans, /show-plan), and manage a plan in one session (/update-plan), with the plan file, GitHub and the product model kept in step.
- Start and land work against a plan: plan branches in start-change and merge-change; `/start-change plan <id>` starts a plan's work on its own (#989); an item's status follows its own issue (#1007).

Most of the diff's size is run records under `.garura/project/issues/`; the hand-written part is about 160 files in `core/`, the docs and 16 product-model pages.

Before this raise, a home-folder path and an employer name were taken out of run records of #989, #993 and #1011. Older commits on the branch still hold them in their history.

## Self-review

