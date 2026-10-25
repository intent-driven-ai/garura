# Build contract — /shape-plan (#818)

Build the play from its ICE, `core/components/plays/shape-plan/reference/ice.md`, by the
create-play method (`core/components/plays/create-play/SKILL.md`, steps 3–7). The product
owner's decisions are in `.garura/project/issues/818/context/decisions.md`. This file fixes the
parts' names and the scripts' command lines; the ICE fixes what they must do.

## The play

- Folder `core/components/plays/shape-plan/`: `SKILL.md` (a full compiled play, frontmatter
  `name: shape-plan`, `user-invocable: true`, `position: both`), `reference/ice.md` (exists — do
  not change its meaning), `stop-condition.yaml` (the ICE's Done means D1–D5, unchanged), and
  `scripts/`.
- Run as `/shape-plan <intent-issue>` (for example `/shape-plan 788`). The intent is
  `bi-<intent-issue>`; the plan ID is the issue number.
- Copied unchanged from `core/components/plays/create-play/references/`: `preflight.py`,
  `session_stamp.py`, `check_stop_condition.py`, `platform_adapter.py`,
  `check_ice_workable.py`, `scoped_write_guard.py`.
- One pinned checkpoint (class: one-way-door, pinned): the brief shows every tracker write and
  the plan-file change; the person types yes, change or stop. Nothing reaches the tracker and the
  plan file is not written before yes.
- Agents: `product-os-keeper` (gathers and calls the skill; never writes content) and
  `template-manager` (the approval prompt and the close templates). No other agent.
- The Next-line map (`core/components/memory/standards/rules/pipeline-next.md`): `shape-slice` →
  `shape-plan` (why: the slice is shaped; make its plan, epic and stories); `shape-plan` → null
  (why: the eval play, #798, is not built yet). Update the map's prose for the shaping loop to
  match.

## The new skill

`core/components/skills/author-work-items/SKILL.md` (frontmatter `name: author-work-items`,
`user-invocable: false`). It writes, for one slice: the epic's title (what a person can see the
product do) and one story for each ready feature. Input: `gather.json` and the clean ICE copies
it names (no "Fails if" lines). Output `drafts.json`:

```json
{ "slices": [ { "slice": "<slice id>",
    "epic": { "title": "...", "delivers": "<one line>" },
    "stories": [ { "feature": "<feature id>", "title": "...",
        "scope_of_work": { "goals": ["..."], "limits": ["..."], "expectations": ["..."] },
        "context_guidance": { "read": "...", "never_read": "...", "persona": "...", "in_out": "..." },
        "written_from": ["<feature ICE page>", "<capability ICE page>"] } ] } ] }
```

It never reads an ICE page itself (only the clean copies), never writes a failure or recovery
condition, and writes plain words with personas.

## The scripts (all in `scripts/`, each with a test file `test_<name>.py` beside it)

All take paths and write JSON to `--out`; exit 0 ok, 1 a check failed (the JSON says why), 2 a
refusal or bad input. The tracker is reached through `platform_adapter.py`, or, for tests and
dry runs, through `--tracker-file <json>`: a JSON file `{"issues": [{"number", "title", "type",
"labels": [], "state", "body", "sub_issues": [numbers]}]}` that the script reads and (for
writes) updates in place, giving a new issue the next free number.

1. `gather_plan.py --root <model dir> --spine <spine> --intent bi-<n> --plans <plans dir> --out <working>/gather.json`
   Finds every slice whose `intents` lists the intent (spine order), its `feature_refs` in build
   order, each feature's capability, and the ICE page of the feature and of its capability. For
   each feature it runs the ready check on both ICE (`check_ice_workable.py`); `ready: false`
   with a `reason` when either is not ready. For each ready feature it writes one clean copy,
   `<working>/ice/<feature id>.md`, holding both ICE with every "Fails if" line removed.
   Output: `{intent, plan_id, plan_file, slices: [{id, slug, name, outcome, features: [{id,
   capability, ready, reason, ice_pages: [..], clean_ice}]}]}`. Exit 2 when no slice serves the
   intent.
2. `find_work_items.py --gather <gather.json> --plan-file <plans>/<id>.yaml [--tracker-file <json>] --out <working>/work-items.json`
   For each slice: the epic is `use` when a plan-file node has `represents: <slice id>`, else
   `make`. For each feature: `use` (its marked story has both sections), `add-sections` (marked,
   but "Scope of work" or "Context guidance" is missing; lists `missing`), `make` (no marked
   story), or `skip` (not ready, with the reason). `move_out`: each marked story under the epic
   whose feature is no longer in the slice. Never matches by title. Output: `{slices: [{slice,
   epic: {action, issue}, stories: [{feature, action, issue, missing}], move_out: [{issue,
   feature}]}]}`.
3. `check_drafts.py --drafts <drafts.json> --gather <gather.json> --out <working>/drafts-check.json`
   `ok: true` only when each slice has an epic title, each ready feature has exactly one story,
   no story for a skipped feature, each story has non-empty goals, limits, expectations and the
   four Context guidance fields, and no text in the epic or a story contains a "Fails if" line of
   its two ICE (read from the original pages), the words "Fails if", or a recovery phrase ("the
   builder can fix this alone", "a person must decide").
4. `render_brief.py --gather <> --work-items <> --drafts <> --out <working>/brief.md`
   The brief: what the run will write in the tracker (each epic and story: make, use, add
   sections, move out), the plan-file change, each skipped feature with its reason.
5. `record_approval.py --decision yes|change|stop --reply "<the person's words>" --at <UTC> --out <working>/approval.json`
   and `record_approval.py verify --file <approval.json>` (exit 0 only on yes).
6. `write_work_items.py --work-items <> --drafts <> --approval <approval.json> --plan-id <id> [--tracker-file <json>] --out <working>/tracker-record.json`
   Refuses (exit 2, writes nothing) unless the approval reads yes. Makes each epic as an issue of
   type Feature and each story as an issue of type Story, a sub-issue of its epic, with no label;
   sets type Feature on a used epic that has another or no type; on `add-sections` appends only
   the missing sections and keeps every line of the body; writes the epic's "Feature-to-story
   map" section (one line `<feature id> → #<story>` for each feature); for `move_out` takes the
   story off the epic's sub-issues and off the map, and leaves it open. Each story body has the
   sections "Scope of work" and "Context guidance" and a "Represents: <feature id>" line; the
   epic body has "Represents: <slice id>". Record: `{created: [..], updated: [..], moved_out:
   [..], epics: {slice: issue}, stories: {feature: issue}}`.
7. `write_plan_file.py --plan-file <plans>/<id>.yaml --gather <> --record <tracker-record.json> --out <working>/plan-write.json`
   Makes the plan file when it is missing (`id`, `title`, `status: active`, `tree`), or updates
   it: for each slice an epic node (`issue`, `kind: epic`, `represents: <slice id>`, title,
   status) with one story node per feature (`issue`, `kind: story`, `represents: <feature id>`,
   title, status) as children; takes moved-out story nodes out of the tree; keeps every other node
   and line. With nothing to change, the file stays byte for byte the same.
8. `check_plan.py --plan-file <> --gather <> --record <> --out <working>/plan-check.json`
   `ok: true` only when each ready feature of each slice has exactly one story node under its
   slice's epic node, no story node stands for a feature outside its slice, and each epic's map
   in the record names the same story for each feature as the tree. Skipped features are listed,
   not failed.
9. `check_tracker.py --record <> [--tracker-file <json>] --out <working>/tracker-check.json`
   `ok: true` only when each issue in the record exists, each epic has type Feature and each
   story type Story, none has a label, each epic's sub-issues are its stories, and each moved-out
   story is open and not a sub-issue of its epic.

## Checks the build runs before it reports

- Every test file beside the scripts passes.
- `python3 .garura/core/tools/lint-play/lint_play.py core/components/plays/shape-plan/SKILL.md --next-map core/components/memory/standards/rules/pipeline-next.md` reads PASS.
- The fingerprint in SKILL.md equals `shasum -a 256` of `reference/ice.md`.
- `node core/tools/lint-components/index.js --target core/components` from the repo root: no
  error in a new or touched file.

## Round 2 (the review of PR #873; decision 6)

- **DF-1 — a write that fails part way makes no copy on the next run.** Make each new issue in
  one call that sets its type and its parent together (GitHub GraphQL `createIssue` with
  `issueTypeId` and `parentIssueId`). `write_work_items.py` writes `tracker-record.json` after
  every tracker write, not only at the end, so a failure keeps every issue already made; the
  record then reads `ok: false` with the `failed` step. `write_plan_file.py` accepts a record
  that reads `ok: false` and writes the marks for every issue the record lists (the run still
  closes HALTED). A test makes the second write fail and shows the next run uses the issue the
  first run made.
- **DF-2 — a "Fails if" line with lines under it never leaks.** `gather_plan.py` removes a
  "Fails if" line and every line under it that is indented deeper or continues it (nested
  bullets, wrapped text). `check_drafts.py` compares the drafts with every line of each "Fails
  if" block, children included. Tests with a nested form.
- **DF-3 — the skill gets no ICE page path.** `gather_plan.py` also writes
  `<working>/skill-input.json`: for each slice its id, name and outcome, and for each ready
  feature its id and its clean copy's path — no ICE page path. The skill reads only that file and
  the clean copies. `written_from` is filled by `write_work_items.py` from `gather.json`, not by
  the skill. The skill and the play's contract say so.
- **DF-4 — the tracker jobs go through the shared adapter.** Add verbs to
  `core/components/plays/create-play/references/platform_adapter.py`: `create-issue-typed`
  (title, body, issue type, parent — one call), `set-issue-type`, `edit-issue-body`,
  `remove-label`, `remove-sub-issue`. On GitLab each one stops with a plain message (no issue
  types there). Copy the new adapter unchanged over every copy (`find core/components -name
  platform_adapter.py`). `write_work_items.py` and `check_tracker.py` call the adapter only — no
  raw `gh` in the play's scripts. Tests for the new verbs with a fake runner.
- **DF-5 — the yes is tied to what the person saw.** `record_approval.py` takes `--brief
  <brief.md> --work-items <> --drafts <>` and records the sha256 of each. `write_work_items.py`
  refuses (exit 2, writes nothing) when any of the three files no longer matches its recorded
  hash. Tests.

### Checks the build runs before it reports
- The checks above, plus every test beside the scripts and beside the adapter's other copies'
  plays that have tests, lint_play on shape-plan, the fingerprint, and lint-components (no new
  error).
