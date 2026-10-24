The first real run of the new `/shape-slice`, on business intent #788. It shapes the one slice that shows the intent is served, and fills the product model with what the slice needs.

Closes #844 (on merge into the plan branch, by merge-change).

## The slice

```
Slice: "From a named piece of work to its design"   (sl-intent-to-design, serves bi-788)
├─ What you run ── in the Claude Code command line, on a real Garura business intent:
│                  /shape-slice <intent>  →  /shape-plan <intent>  →  /shape-eval <intent>
├─ Who tests it ── the product owner
├─ Features, by capability
│  ├─ Shape a slice              NEW  (domain: Software delivery planning)   thin ICE
│  │  └─ 1. /shape-slice writes the slice and its hidden file  (fn-795, #795)
│  ├─ Build a plan (cap-718)     FILL (domain: Software delivery planning)   thin ICE added
│  │  └─ 2. /shape-plan writes the plan file, the epic, the stories  (fn-818, #818)
│  └─ Write the hidden eval      NEW  (domain: Software delivery planning)   thin ICE
│     └─ 3. /shape-eval writes the hidden eval  (fn-798, #798)
├─ Hidden file  ── .garura/project/plans/788/evals/intent-to-design/failure-and-recovery.md
│                  18 "fails if" lines, one recovery each (9 the builder fixes alone, 9 need a person)
└─ Left out     ── the loop and its one approval (#796), eval encryption (#828), the slice-picking skill (#838)
```

**Thin ICE.** These parts have only a thin ICE: a goal, its limits and a few "fails if" lines, with no expectations or quality needs yet. Work on thin ICE can break later. Run `/discover-capabilities` on the three capabilities before the build. The domain page is directional; `/discover-domains` deepens it (its four outside sources were named from memory and are not checked yet).

## The product owner's decisions (this run)

Recorded in `.garura/project/issues/844/context/decisions.md`:
1. No loop: three plays, one after the other. Each ends at its own confirmation.
2. The plan play is `/shape-plan`; the eval play is `/shape-eval`.
3. Encryption, the loop and the slice-picking skill are left out.
4. The slice is shown as one confirmation: what you run, who tests it, features grouped under capability with each capability linked to its domain, and what is left out.
5. The run reuses, fills or adds domains and capabilities, with research.
6. `/shape-slice` writes the slice's hidden failure-and-recovery file; `/shape-plan` only plans.
7. Option C: for a new capability or feature, `/shape-slice` proposes a thin ICE itself, warns, and never forces the person back.
8. The model check's 70 older problems (17 older feature pages, 2 ICE lines, other plans) were there before this run and are accepted for it.

The bi-788 intent page is confirmed by the product owner, with the title "Agents design a named piece of work".

## Known gaps (the play catches up in its own change)

Decisions 4, 6, 7 and 8 change what `/shape-slice` does. Today's play asks a list of questions before the slice, may not write under `plans/`, cannot fill an existing capability in the spine, and fails its model check on older problems. The ontology (v10) and ADR 049 still say the plan play writes the hidden file. Next: `/edit-ontology` and an ADR update for decision 6, then `/edit-play` on `/shape-slice` for decisions 4, 6, 7 and 8, with #842. Also found in this run: Step 4 passes the proposals record to `filter`, which wants a plain list; the asking-a-person rule is in no memory tier until it is on main.

## Checks

| Check | Result |
|---|---|
| The slice's own checks (`slice_check.py` problems) | none |
| Whole-model check | 70 errors, the same 70 as before the run (compared one by one); none in this run's pages |
| Write guard | ok — only the allowed files changed |
| Question record | 7 asked, 7 answered, in the product owner's words |
| Approval | yes, recorded and verified before the commit |
| Names | no real name in the pages this run wrote |

🤖 Generated with [Claude Code](https://claude.com/claude-code)
