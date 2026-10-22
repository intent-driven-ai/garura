# Change list — plans and the product ontology (proposed, 2026-10-21)

Nothing here is done. Every item waits for Kapil's go.

Rule from here on (Kapil, 2026-10-21): Garura is built to the product ontology, and nothing is blocked. The product model is built in real time as plans are built; `/vision` and `/understand` can fill the gaps later.

## A. The two plans (the tree that becomes issues)

```
BI-A  People plan work toward a business intent, and pick it up across days and people
├─ C1 Build a plan                                            Feature (new)
│  ├─ F1.1 Build the plan tree from a business intent          Story (new)   needs F4.1
│  └─ F1.2 Create or link a tracker issue for every node       Story (new)
├─ C2 View plans                                              Feature (new)
│  ├─ F2.1 List every plan                                     Story (new)
│  └─ F2.2 Show one plan as a tree                             Story #628 (reused)
├─ C3 Manage a plan                                           Feature (new)
│  └─ F3.1 Update, edit, delete the plan file, and connect it to its issues   Story (new)
└─ C5 Start and land work against a plan                      Feature (new)  identified by C3
   ├─ F5.1 start-change cuts the plan's branch, and each issue's branch from it, taking in main   Story (new)
   └─ F5.2 merge-change lands an issue on its plan branch; a plan lands on main only when done, after the plans it needs   Story #673 (reused)

BI-B  A product model can be managed, and plans build on it as it grows     identified by BI-A
└─ C4 Link the product model                                  Feature (new)  identified by C1
   ├─ F4.1 A capability or functionality is ready without a domain   Story (new)
   ├─ F4.2 "Needs" and "identified by" across capabilities and functionalities   Story (new)
   ├─ F4.3 Domains link to business intents and capabilities   Story (new)
   └─ F4.4 The ontology defines every kind plans use           Story #597 (reused, Feature → Story)
```

Because F1.1 needs F4.1, plan BI-A needs plan BI-B: BI-A cannot merge into main until BI-B is done.

C3 is orchestration only: it changes the plan file and the tracker, never branches or code (Kapil, 2026-10-21). Branches belong to the implementation plays — start-change, commit-change, merge-change — so the branch rules are their own capability, C5.

Each capability and functionality gets an ICE (goal, limit, fails if, checked by) on its model page, and a copy in its issue.

## B. Files (on a branch; nothing committed yet)

1. `core/components/memory/standards/schemas/product-os/ontology.md` — version 4 → 5: define Capability, Functionality, Work, Plan; "needs" and "identified by"; domains link to business intents and capabilities; new ready rule; Q7; three examples per kind; log line.
2. `core/components/memory/standards/schemas/product-os/spine.yaml` — `identified_by` on capabilities and functionalities; "needs" may name a capability or a functionality; tree rules: a missing domain is a warning.
3. `core/components/plays/play-creator/references/check_ice_workable.py` and its copy in `core/components/plays/intent/scripts/`, plus `test_check_ice_workable.py` — drop the domain requirement; a node whose needs are not done is not ready.
4. Garura's own product model, new at `.garura/product/product-os/`: the spine, 2 business intent pages, 5 capability pages, 11 functionality pages (in the holding folders — no domains yet).
5. The plan files, new at `.garura/project/plans/`: one per business intent, named by its issue number, plus `index.yaml`.
6. `CLAUDE.md` (Work Tracking) and `.garura/user-provided/managing-work.md` — Garura's work follows the product ontology, not Feature → Story.
7. One ADR through `/adr`: plans (amends ADR 030) and the ready rule (amends ADR 043).

## C. GitHub

- New: 2 Business Intent issues, 5 Feature issues, 8 Story issues = 15.
- Reused and re-parented: #628 (under C2), #673 (under C5), #597 (under C4, type Feature → Story; its own children stay).
- Closed as replaced: #621 and #622–#627 = 7.

## Open

- The spine field is `depends_on` in 53 files today (epics and slices use it too). Rename it to `needs` now, or keep the field name and use "needs" in the ontology and pages, renaming later as part of F4.2.
- Which branch carries this first change: the work is F4.4 and F4.1 (BI-B), but start-change does not know plans yet (F5.1), so the plan branch and the issue branches are made by hand this once.
