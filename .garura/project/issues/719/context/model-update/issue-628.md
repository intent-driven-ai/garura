# #628 Show one plan as a tree, from its plan file alone

> **Design agreed, 2026-10-29 (the product owner).** The design is `.garura/project/issues/719/specs/design.md`; this section holds the part for this issue. Built in one change with #729 and #806, opened on #719. The skill named above (`manage-plan`) is not used: this is the `/show-plan` play, which reads `.garura/project/plans/<id>.yaml`.

> Parent: #621. Source of truth: [ADR 030 — Plan Mode](docs/adr/030-plan-mode.md), decided in spike #619.

## What

A `show` mode for the `manage-plan` skill. A script prints the plan as a short **tree** — GOAL → DONE → NOW → NEXT → WAIT (on the human) — and follows `serves_plan` so the parent level shows too.

Every line says in plain words what the item is, with its issue number beside it — never a bare number — so a reader coming back after two days knows where things stand from the tree alone. Every DONE line says what kind of done: **decided**, **built**, or **shipped**, and what is still pending. Thorough, but crisp. (Kapil, 2026-10-08, after a long readout and then an over-compressed one both failed; rules in `standards/rules/work-plan.md`, rule 19.)

## Acceptance criteria

- [ ] `/show-plan <id>` prints the plan as a tree, the same way every time, from the plan files alone: one node per line, its mark, issue number and title; the legend first.
- [ ] It shows `Not Started`, `In Progress`, `Now` and `Blocked`. It hides `Done` and `Dropped`, and ends with one line that counts them.
- [ ] Every line has a plain-words title; no line is only an issue number.
- [ ] A plan it needs (`needs_plans`) prints after it, on the same screen.
- [ ] It says plainly when no plan exists.

_Replaced on 2026-10-29 (the product owner): the GOAL / DONE / NOW / NEXT / WAIT grouping, and "decided, built or shipped" on each done line. The plan files hold no field for those; the marked tree of 2026-10-22 replaces the grouping._

## Out of scope

Changing the plan format.




## Design (agreed 2026-10-29)

- The layout is in the `plan-view.md` template; the plan tool prints it with no model call.
- Statuses in every plan: `Not Started`, `In Progress` (started, no one on it in an open change), `Now` (worked in an open change), `Done`, `Blocked`, `Dropped` (closed as not planned; hidden in every view). `next` and `later` go and become `Not Started`.
- Example, `/show-plan 717`:

```
○ Not Started · ◐ In Progress · ▶ Now · ⛔ Blocked

○ #717  People plan work toward a business intent, and pick it up across days and people
└─ ○ #956  A person builds, views and manages the plan of a business intent
   ├─ ◐ #718  Build a plan
   │  └─ ○ #896  /shape-plan stops when the business intent already has a plan
   ├─ ○ #719  View plans
   │  ├─ ○ #729  List every plan
   ...
5 Done · 1 Dropped (not shown)
```


