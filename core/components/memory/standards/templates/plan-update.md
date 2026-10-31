# Plan Update Template

What `/update-plan` shows a person, from the moment it finds the plan to the moment the changes
land. The play's `render_screen.py` prints each
screen from the settings below and the session's own files; nothing on a screen is worded at run
time. A change to how a screen reads is made here, never in the play.

Consumer: `/update-plan` (#730). It gets a copy of this file and of `plan-view.md` (the status
marks) from `template-manager`.

## The screens

- **found** — a description matched one plan. The person types yes, or names another plan.
- **not found** — no plan, or two equally good plans, matched. Names the candidates. Nothing
  else happens.
- **stopped** — the branch the person is on has uncommitted work. Names each file. Nothing was
  written; the person cleans up and runs the play again.
- **on the branch** — the session is on the plan's branch, and names where it goes back to. When
  the plan had no branch, it says main's plan file was set and the branch was cut.
- **taken** — one line for each entry an instruction added to the list.
- **break** — an instruction would break a rule: the rule, what works instead, and the override
  ("do it anyway"), which is recorded.
- **confirm** — a big change (drop an epic, move a feature between slices, any model change,
  close an item with open work under it) is shown and waits for a yes before it joins the list.
  A new feature also says its ICE will be thin, and, when its slice is in progress, names the
  slice's epic as out of date (ADR 058, ADR 062).
- **question** — what no rule settles, asked in four parts: the question, the answer we have
  (or that there is none yet), why it matters, and examples from different domains.
- **list** — the whole list and the one question: approved or rejected. A story added for a
  feature in the model carries one note under its line: drafted from the feature's ICE, or the
  feature has no ready ICE and the story uses the person's words.
- **model** — the answer to a lookup in the model ("which feature is #931?"): the feature, its
  one line and its ICE pages, or that no feature matches, or that more than one does. It adds
  nothing to the list.
- **rejected** — nothing lands; the session goes on, and the play asks what to change.
- **aborted** — the person said "abort": nothing was written, the list is dropped, a branch the
  session cut is undone, and the session is back where it started.
- **landed** — what changed in the model, GitHub and the plan file, the agreement check, what is
  owed, and the branch the session went back to.
- **resume** — a list from an earlier session is waiting: carry on with it, or start fresh.

The list is the approval screen. It shows the plan and the business intent it serves; the plan
**before** and **after** the list, printed like `/show-plan` but only the parts the list touches
(each touched item with the items above it), each with the plan's Status and Direction; then
**what changed**, one plain line for each entry, numbered so the person can say "take out 3".

```
Plan 717 — serves #717: People plan work toward a business intent, and pick it up across days and people

Before — Status In Progress · Direction ⏵
└─ ○ #956  A person builds, views and manages the plan of a business intent
   ├─ ○ #720  Manage a plan with /update-plan
   │  └─ ○ #730  The /update-plan session
   │     └─ ○ #917  The findings left by the PR #916 review
   └─ ○ #721  Start and land work against a plan
      ├─ ✓ #731  start-change cuts a plan's branch
      │  └─ ○ #779  start-change reads plan files from the checked-out branch
      └─ ○ #989  start-change starts a plan on its own

After — Status Paused · Direction ⏵⏵
└─ ○ #956  A person builds, views and manages the plan of a business intent
   ├─ ○ #720  Manage a plan with /update-plan
   │  ├─ ✓ #730  The /update-plan session
   │  │  └─ ✓ #917  The findings left by the PR #916 review
   │  └─ ○ NEW  A person can undo the last /update-plan landing
   ├─ ○ #721  Start and land work against a plan
   │  ├─ ✓ #731  start-change cuts a plan's branch
   │  └─ ○ #989  start-change starts a plan on its own
   │     └─ ○ #779  start-change reads plan files from the checked-out branch
   └─ ○ NEW  Tidy the comments in the plan files

What changed
  1  #730 finished
  2  #917 finished
  3  #779 moved under #989
  4  New chore "Tidy the comments in the plan files" under #956 — you chose to override: a chore does not sit under an epic; it sits under a story
  5  New feature "A person can undo the last /update-plan landing" under #720 — also added to the product model; its slice and eval scenarios are left for later
  6  Plan status Paused
  7  Plan direction ⏵⏵

Type approved; rejected to change the list; or abort to drop it all and go back.
```

## Settings

`render_screen.py` reads this block. `{…}` are the values the play passes; a `_line` setting is
printed once for each item of its list.

```yaml plan-update
found: |-
  Plan {plan} — {title}
  Matched on: "{matched}" ({where})
  Is this the plan? Type yes, or name another.
not_found: |-
  No single plan matches "{description}".
  {candidates}
  Run /update-plan with the plan's number.
candidate_line: "  #{plan}  {title}"
no_candidates: "  No plan has those words."
stopped: |-
  Stopped. {branch} has uncommitted work:
  {files}
  Commit or clean it, then run /update-plan {plan} again.
file_line: "  {file}"
on_branch: |-
  Plan {plan} · on {plan_branch}{back}
  Tell me what to change.
back_note: " · I will come back to {back_to} at the end."
cut_note: |-
  Plan {plan} had no branch. Main's plan file now says In Progress on {plan_branch} (commit {commit}), and {plan_branch} was cut from it.
taken: "Added {row}"
taken_plan: "Added: the plan's {changes}"
already: "Already so: {ref} {what} — nothing to add."
break: |-
  {ref} "{title}" under {parent}: {problem}.
  What works: {fix}.
  Say which, or "do it anyway" — I will record that you overrode the rule.
confirm: |-
  {row}
  This needs your yes first: {why}.
  Type yes to add it to the list, or tell me what to change.
thin_warning: "  Its ICE will be thin: written from your words only. A thin ICE can cause problems later; /discover-capabilities can deepen it."
from_ice_note: "drafted from {feature}'s ICE and its capability's ICE"
no_ice_note: "{feature}: {reason}, so the story uses your words"
model_found: "#{story} is the story of {feature}: {one_line}\n  Its ICE: {pages}"
model_feature: "{feature}: {one_line}\n  Its ICE: {pages}"
model_not_found: "No feature in the model matches {ref}."
model_many: "More than one feature matches {ref}: {matches}. Name one."
model_join: "; "
slice_in_progress: "  Its slice {slice} is in progress: {epics} is out of date, because work already started from the old text."
epic_line: "epic {epic} ({status})"
epic_join: ", "
question: |-
  Question: {question}
  Answer: {answer}
  Why it matters: {why}
  Examples:
  {examples}
example_line: "  - {example}"
list_head: "Plan {plan} — serves #{plan}: {title}"
before_head: "Before — Status {status} · Direction {direction}"
after_head: "After — Status {status} · Direction {direction}"
changed_head: "What changed"
change_line: "{n:>3}  {text}"
tree_line: "{mark} {ref}  {title}"
tree_mid: "├─ "
tree_last: "└─ "
tree_pipe: "│  "
tree_space: "   "
no_direction: "none"
change:
  status:
    Done: "{ref} finished"
    Dropped: "{ref} dropped"
    In Progress: "{ref} started"
    Now: "{ref} being worked on now"
    Blocked: "{ref} blocked"
    Not Started: "{ref} set back to not started"
  add_existing: "{ref} added under {parent}"
  add_new: "New {kind} \"{title}\" under {parent}"
  move: "{ref} moved under {to}"
  retitle: "{ref} renamed to \"{to}\""
  text: "{ref}'s text changed: {summary}"
  kind: "{ref} is now a {to}"
  new-feature: "New feature \"{title}\" under {parent} — also added to the product model; its slice and eval scenarios are left for later"
  feature-of-story: "{ref}'s feature added to the product model — \"{title}\"; its slice and eval scenarios are left for later"
  plan-status: "Plan status {to}"
  plan-direction: "Plan direction {to}"
override_note: " — you chose to override: {override}"
row: "{n:>3}  {mark} {ref:<6} {title:<36} {what:<20} {where}"
title_width: 36
title_cut: "…"
under_line: "             {kind}: {text}"
plan_row: "  Plan  {changes}"
plan_change: "{field} {from} → {to}"
plan_join: " · "
owed_join: ", "
ask: "Type approved; rejected to change the list; or abort to drop it all and go back."
empty: "The list is empty. Tell me what to change, or type rejected to end."
rejected: "Not approved, so nothing lands. Tell me what to change in the list."
aborted: "Aborted. Nothing was written and the list is dropped.{undo} Back on {back_to}."
aborted_undo: " Plan {plan}'s new branch is gone, and main's plan file is as it was."
landed: |-
  Landed on {plan_branch} (commit {commit}), pushed.
    Model    {model}
    GitHub   {github}
    Plan     {plan_changes}
    Check    {check}
  {owed}{back}
landed_owed: "  Owed     {owed}\n"
landed_model: "{n} new feature(s), thin"
landed_plan: "{n} changes"
landed_counts: {close: "{n} closed", reopen: "{n} reopened", create: "{n} made", parent: "{n} moved", title: "{n} renamed", body: "{n} text changed", type: "{n} type changed"}
landed_join: ", "
landed_back: "Back on {back_to}."
landed_stay: "Still on {plan_branch}."
resume: |-
  A list of {count} from {at} is waiting for plan {plan}.
  Type carry on to work with it, or start fresh to set it aside.
what:
  status: "{from} → {to}"
  add: "under #{parent}"
  move: "#{from} → #{to}"
  retitle: "rename"
  text: "new text"
  kind: "kind {from} → {to}"
  new-feature: "under #{parent}"
where:
  close-completed: "close as completed"
  close-not-planned: "close as not planned"
  reopen: "reopen"
  create: "new {type}"
  parent: "parent"
  title: "title"
  body: "text"
  type: "type"
  model-page: "thin page"
  model-index: "index"
  model-slice: "slice"
where_github: "GitHub: {items}"
where_model: "model: {items}"
where_join: ", "
where_sides_join: " · "
new_ref: "NEW"
check_ok: "plan file, GitHub and the model agree; nothing else changed"
none: "nothing"
```
