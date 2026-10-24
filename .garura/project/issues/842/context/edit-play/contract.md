# /shape-slice (#842): interfaces the build must provide

These are the names, flags and file shapes the change must expose. They come from the
change map (`.garura/project/issues/842/context/edit-play/change-map.md`) and the product
owner's decisions (`decisions.md`). Where the map left a name open, it is fixed here.
Scripts live in `core/components/plays/shape-slice/scripts/` unless named otherwise.
"Exit 2" always means refused, with nothing written.

## record_questions.py

- `filter --record <md> --questions <file> --out <open.json>`: `--questions` takes a JSON list,
  or the object that `proposals` writes (`{questions, settled, ...}`). It reads `questions`.
- `brief --brief <brief.md> --split <split.json>` replaces `message`. It prints `{ok, problems}`
  and exits 0 when ok, 1 on problems. Each problem names the heading or part that is missing.
  - The opening is the text before the first Markdown heading. It has two or three sentences and
    says what the person decides. The opening may name a question id.
  - Required H2 headings: `What you run`, `Who tests it`, `Features`, `Hidden file`, `Left out`,
    `Assumptions`, `Model check`, `Questions`.
  - Each asked question in the split sits under `## Questions` as `### <id>`, with the parts
    `**Question**`, `**Answer**`, `**Why it matters**` and `**Example**`.
- `answers`: when the first non-empty line of the reply is a bare `yes`, each asked question that
  the reply does not answer by id gets
  `{"id", "answer": "yes — accepted as proposed", "decision": "accepted"}`.

## render_brief.py (new)

`render_brief.py --working <dir> --root <model> --spine <spine> --opening <opening.md> --out <brief.md>`

It reads these files from `<dir>`: `slice.json`, `fills.json`, `persist-fills.json`,
`persist-slice.json`, `slice-check.json`, `hidden-file.json`, `split.json`,
`questions-checked.json` and `gather.json`. It writes `brief.md`: the opening, then the H2
sections listed under `brief`. It adds `## Thin ICE` when any part of the slice is thin, and
`## Kept slice` when `persist-slice.json` reads `reused: true`. Each section has a fixed shape:

| Section | Content |
|---------|---------|
| What you run | the surface's `name` and `user_action` |
| Who tests it | the surface's `persona_ref` |
| Features | one block per capability: `### <capability name> (<cap id>) — <new\|filled\|reused>`, then `Domain: [<domain name>](<link that ends in the domain's doc path>)`, then `<n>. <feature name> (<feature id>) — <new\|filled\|reused>`, where n is the place in build order. A part is new when it is in `persist-fills.json` `written`, filled when it is in `updated`, and reused otherwise. |
| Hidden file | `Place: <path>`, `Fails if lines: <n>`, `The builder can fix alone: <n>`, `A person must decide: <n>` (from `hidden-file.json`) |
| Left out | each `slice.json` `left_out[].what`, or `Nothing is left out.` |
| Assumptions | each `split.json` `assumptions[].assume` |
| Model check | `Older problems: <n>`, then each `slice-check.json` `older_problems` and `warnings` entry as a bullet, word for word |
| Questions | `Questions with no proposed answer: <n>` (from `questions-checked.json` `no_proposed_answer`), then each asked question as `### <id>` with its four parts. When `gather.json` has `rule_missing`, a line that holds the words "rule for asking a person" and `rule_missing.memory_update`. |
| Thin ICE | each thin part's id, and `/discover-capabilities`. A part is thin when `fills.json` `thin`, its spine `metadata.thin`, or its `hidden-file.json` entry's `thin` names it. |
| Kept slice | each `persist-slice.json` `differences` entry, word for word; each `upgraded_to_v2` and `dropped_fields` entry in plain words, with the field's own word (for example "name" or "status") in the line |

New record fields:
- `slice.json`: `left_out: [{"what", "why"}]`.
- `gather.json`, when no memory tier holds the rule for asking a person:
  `rule_missing: {"tiers": [...], "memory_update": "mu-..."}`.

## write_hidden_file.py (new)

```
write_hidden_file.py lines --root <model> --spine <spine> --slice-id <id> --plans-root <plans dir> --out <hidden-lines.json>
write_hidden_file.py write --lines <hidden-lines.json> --recoveries <hidden-recoveries.json> --plans-root <plans dir> --out <hidden-write.json>
write_hidden_file.py check --root <model> --spine <spine> --slice-id <id> --plans-root <plans dir> --out <hidden-file.json>
```

- The file goes at `<plans-root>/<plan-id>/evals/<slug>/failure-and-recovery.md`. `<plan-id>` is
  the number of the slice's first intent: `bi-340` gives `340`.
- The script reads the "Fails if" lines from the inline `## Agent intent (ICE)` section
  (`- Fails if: ...`). When the spine has an `ices` list, it reads them from the `## Intent`
  section of `ice.md`. It reads the lines of each feature and of the feature's capability.
- `hidden-lines.json` is
  `{slice, plan_id, path (relative to plans-root), entries: [{feature, name, capability, thin: ["feature"|"capability", ...], kept: bool, lines: [{id, from: "feature"|"capability", text}]}]}`.
  `kept: true` means the entry is already in the file.
- `hidden-recoveries.json` is
  `{entries: [{feature, recoveries: [{line, when, way_back, who_fixes}]}]}`. `who_fixes` is
  exactly `the builder can fix this alone` or `a person must decide`.
- `write` refuses with exit 2 when a line has no recovery or two, when `who_fixes` is any other
  text, or when the path is outside plans-root. It makes the folder. It keeps each entry that is
  already in the file, byte for byte, and adds the new ones.
- File shape:
  - one `## <feature id>: <name>` heading for each feature;
  - `### Failure conditions`, with `- F<n> (from the feature ICE): <text>`, or
    `(from the capability ICE)`, or `- none`;
  - `### Recovery`, with `- For F<n>` followed by `  - When:`, `  - Way back:` and `  - Who fixes:`;
  - ids F1, F2, … are unique in the whole file, and a kept entry keeps its ids;
  - the entry says when one of its two ICE is thin.
- `hidden-file.json` is
  `{ok, path, entries: [{feature, capability, thin, lines}], counts: {lines, builder_alone, person}, problems}`.
  Exit 0 when ok, 1 when not ok (for example, a "Fails if" line of the ICE is not in the file).

## scoped_write_guard.py

The canonical copy is in `create-play/references/`. Every stamped copy must stay byte for byte
the same as it.
- New flag `--also-tree <repo-relative dir>`, which can repeat. The changed paths in that tree
  join the same check and the same restore. Calls without the flag behave as they do now.

## persist_fills.py

- `fills.json` gains:
  - `thin: [<part ids>]`, which sets `metadata.thin: true` on those spine entries;
  - `updates: [{id, kind: domain|capability|feature, add_intents: [...], domain|capability: <id> (only when the entry has none), page: true}]`,
    which fills an entry that already exists.
- Folder rule:
  - a domain page is at `<d>/domain.md`;
  - a capability page is at `<dirname of its domain's doc>/<folder>/capability.md`, or in the
    holding folder `capabilities/<id>/capability.md` while it has no domain;
  - a feature page is at `<dirname of its capability's doc>/<folder>/feature.md`, or in the
    holding folder `features/<id>/feature.md` while it has no capability.
  - A new page outside its folder is refused (exit 2).
- When an update gives a capability in a holding folder its domain, the script moves the
  capability's page, and the pages of its features, under the domain folder. It also fixes the
  links to them.
- `persist-fills.json` gains `updated: [ids]`, `moved: [{id, from, to}]` (paths relative to the
  model) and `remove_only: ["product-os/<old path>"]`. `allow` names the new paths.
- On the intent page, the Touches line for a filled domain or capability is marked `— changes`.
- `--undo` keeps every line that was on the page before the run, including
  `**Touches:** none yet`.

## slice_check.py

```
slice_check.py baseline --root <model> --spine <spine> --out <lint-before-run.json>
slice_check.py --root <model> --spine <spine> --slice-id <id> --intent <bi-id> --baseline <lint-before-run.json> --out <slice-check.json>
```

- The output gains `older_problems: [str]`.
- `valid` is false when:
  - any of the slice's own pages has a problem (its features, their capabilities, and their
    domains), even a problem that the baseline already had;
  - the linter finds an error that the baseline did not have;
  - the thin marks of a slice part do not agree: `metadata.thin` and the Thin line disagree, or a
    thin ICE lacks one of `Goal`, `Limit`, `Fails if`, `Context` and `Checked by`.
- A lint error in another page that the baseline already had goes in `older_problems`.
- The Thin line is
  ``Thin: proposed by `/shape-slice` from the person's answers; deepen with `/discover-capabilities`.``
  It sits just before `## Agent intent (ICE)`, or just before `## Intent` in an `ice.md`.

## find_serving_slice.py and persist_slice.py

- `find_serving_slice.py`: the output gains `in_progress: [slice ids]`. A slice is in progress
  when a spine `epics` entry with `slice_ref` equal to its id has the status `in_delivery`,
  `validated`, `fix_required` or `delivered`. A slice in progress is never a match: `match` is
  null and `reuse_args` is `[]`.
- `persist_slice.py --reuse <id> [--pull-in <feature id>]... [--push-out <feature id>]...`:
  - a feature pulled in takes its place in the order of `slice.json` `feature_refs`;
  - the result gains `pulled_in` and `pushed_out`;
  - the script refuses (exit 2) to reuse a slice in progress, a push-out that leaves the slice
    with no feature, and a pull-in of a feature that is not in the spine.

## trace_check.py (new)

`trace_check.py --issue <n> --live <citations-live.json> [--check <citations-check.json>] --out <trace-check.json>`

- `citations-live.json` is `{"live": [citation ids]}`.
- `--check` is the memory tool's `citations --check` answer. Without it, the script runs the tool.
- The output is `{ok, live, problems, not_live}`. `problems` holds the problems of live records
  only, plus `{citation_id, problem: "not_recorded"}` for a live id that has no record.
- Exit 0 when `problems` is empty, else 1.

## New skill

`core/components/skills/author-failure-recovery/SKILL.md`, with front matter
`name: author-failure-recovery`. It drafts each feature's hidden-file entry by
`standards/rules/expectation-generation.md`. The play's agent table and its `skills_used`
metadata name it.

## stop-condition.yaml

- D5: `context/shape-slice/trace-check.json`, where `problems` equals `[]`.
- D6: `context/shape-slice/hidden-file.json`, where `ok` equals `true`.

# Round 2 (PR #853 review, round 1: DF-1, DF-2, DF-3, Q-1, Q-2, and the product owner's rule)

The product owner's rule: **an agent only gathers context; a skill does the work.** The agent
reads, copies memory into short-term memory, calls the memory tool, calls a skill and passes
the skill's output on. It never chooses, drafts, decides or writes content itself. The audit
that lists every place the play breaks this rule is
`.garura/project/issues/842/context/edit-play/agent-audit.md`. Fix every row marked WORK, every
fit gap (A1–A6) and every "wrong direction" line in it. This is an intent change: it goes
through `reference/ice.md` and a recompile (fingerprint, `lint_play.py`).

## ICE

- New constraint **C19**: the agent only gathers context and passes it on; every choice, draft
  and decision is made by a named skill. With **F19** (an agent dispatch asks the agent to do
  work no named skill does), **REC19** and a step eval **SE-25**. Compiled From then reads
  C1–C19 and F1–F19.
- Every step eval id is used once. The early-brief eval of Step 5 gets the id **SE-24**; the
  final-brief eval of Step 11 keeps SE-6. The Compilation Metadata count of step evals equals
  the number of distinct SE ids in the file.

## Agent contracts in SKILL.md

- Every JSON contract that has a `task_id` also has `"skills": [<skill names>]`. Each name is a
  folder in `core/components/skills/`. Only `shape-slice-trace` (the live re-cite) has
  `"skills": []`.
- The words "yourself", "No skill does this", "make it yourself", "have the agent write",
  "The agent does that choice itself" and "hand every piece of judgment to" appear nowhere in
  `SKILL.md` or `reference/ice.md`.
- The Role section says the agent gathers context and the skills do the work.
- `skills_missing` in the Compilation Metadata reads `none`.
- `find-model-gaps` is not used by /shape-slice: not in its agent table, not in `skills_used`,
  and the `product-os-keeper.md` row for `find-model-gaps` does not name /shape-slice.
- The surface and the tester are never a question in the gap list. `author-slice` proposes
  them in Step 6, and the brief shows them for the person's yes.

| Step | task_id | skills |
|------|---------|--------|
| 1 | shape-slice-intent | author-business-intent (one-intent mode) |
| 2 | shape-slice-gather | find-work-placement, find-slice-gaps |
| 3 | shape-slice-propose | propose-answers |
| 3 (REC3) | shape-slice-rewrite | find-slice-gaps (rewrite mode) |
| 5 | shape-slice-early-opening | author-slice-brief |
| 6 | shape-slice-shape | author-slice, author-domains, enrich-capability-ice, enrich-grounding |
| 7 | shape-slice-reuse | author-slice (reuse mode) |
| 8b | shape-slice-hidden | author-failure-recovery |
| 9 (REC11) | shape-slice-fix | author-slice (fix mode), enrich-grounding (fix mode) |
| 10b | shape-slice-trace | (none) |
| 11 | shape-slice-opening | author-slice-brief |

- Step 8b's contract names `ice_pages` and `rule` in its inputs.

## New skills

Each is `core/components/skills/<name>/SKILL.md` with front matter `name: <name>`,
`description`, `user-invocable: false`, and the sections `## Input` (a table), `## Output` and
`## Rules`. Each description names /shape-slice. Names follow `naming.md` (skill verbs from
`naming.yaml`).

- **`author-slice`** (#838). Writes `slice.json` and `fills.json` from the intent page, the
  gathered context, the placement result, the question record and the assumptions: the one
  surface and the persona who tests it there; the features from any capability in build
  order, with `why_this_order`; `left_out`; `no-slice.json` with its reason when no surface can
  be tested end to end; and the needs list (`fills.json` new parts, `updates`, `thin`). Reuse
  mode: given the kept slice and `serving.json`, writes `reuse.json` (`pull_in`, `push_out`,
  `why`), keeps the slice testable end to end, and never changes a slice in progress. Fix
  mode: fixes the problems the model check finds in `slice.json` or `fills.json`. Its text
  holds the words: surface, tester, persona, build order, left_out, no-slice, fills, updates,
  thin, reuse, pull_in, push_out, in progress, testable end to end, fix.
- **`find-slice-gaps`**. Lists each thing the slice needs that neither the model nor memory
  answers, and writes each as one question by the rule for asking a person: id, topic,
  question, why, examples from several domains, blocking, assume, and `settled` with its
  basis. The surface and the tester are never a question. Rewrite mode: rewrites only the
  questions that `record_questions.py proposals` refuses. Its text holds: blocking, assume,
  settled, examples, rewrite, surface, tester.
- **`author-slice-brief`**. Writes the opening of the early brief and of the confirmation
  brief: two or three plain sentences that say what the person decides and what happens with
  the reply, by the rule for asking a person, or by the play's floor when the rule is missing.
  Its text holds: opening, early, confirmation, two or three sentences, rule for asking a
  person, rule_missing.
- **`enrich-grounding`**. Writes on the pages of the parts the slice needs, from the person's
  answers and the assumptions, and keeps every section and line a page had: brings a page the
  slice moves or uses up to the current rules in place; writes one new feature page under a
  capability that exists without re-detailing the capability; thin-ICE mode (Goal, Limit,
  Fails if, Context, Checked by); fix mode. It never writes `_spine.yaml`. Its text holds: in
  place, new feature, thin, Goal, Limit, Fails if, Context, Checked by, fix, _spine.yaml.

## Changes to existing skills and the agent

- `author-business-intent`: a one-intent mode — input one plain statement, output one intent
  as `intent-draft.json`. Its text holds "one-intent" and "intent-draft.json"; its description
  names /shape-slice.
- `propose-answers`: its description names /shape-slice; the text "as our default" is gone; a
  value with no source gets no proposed answer. Each proposal's `basis` is
  `{kind, ref}`.
- `enrich-capability-ice`: a `depth` input; with `depth: directional` the page stays at the
  directional stage and is marked to be deepened. The text "goes back to the caller as a
  question" is gone: a gap is returned as data in its manifest's `gaps`. Its description names
  /shape-slice.
- `author-domains`: input `profile: false` writes no profile block. Its description names
  /shape-slice.
- `author-failure-recovery`: the text "so the agent can tell the person" is gone (the play
  shows `vague` in the brief).
- `product-os-keeper.md`: the text "shaping it into the caller's contract" is gone; it says the
  agent passes a skill's output on as it is; its skill table has a row for each of the four new
  skills that names /shape-slice.
- `core/components/memory/standards/rules/naming.md` rule 2: the words "such as epic or slice"
  are gone; epic and slice are model words.

## Scripts

- **`safe_write.py`** (new, in the play's `scripts/`): `atomic_write(path, text)` writes through
  a temp file in the same folder, then `os.replace`. No other script in the play's `scripts/`
  (tests aside) calls `os.replace` or `tempfile.mkstemp`. `persist_fills.py`,
  `persist_slice.py`, `write_hidden_file.py`, `render_brief.py` and `write_intent_page.py`
  write their output files and pages through it.
- **`write_hidden_file.py check ... --clear-working <path>`** (repeatable): when the check reads
  ok (exit 0), it deletes each named file; when it is not ok (exit 1), it keeps them. It refuses
  (exit 2, nothing deleted) a path under `--plans-root`. Step 8b passes
  `<working>hidden-lines.json` and `<working>hidden-recoveries.json`, so no copy of the "Fails
  if" lines or the ids is left outside the evals folder.
- **`render_brief.py --early --working <dir> --opening <opening.md> --split <early-split.json> --out <early-brief.md>`**:
  writes the opening, then `## Questions` with each question of the split as `### <id>` and its
  **Question**, **Answer** (`no proposed answer yet` when it has none), **Why it matters** and
  **Example**. The result passes `record_questions.py brief --early`.
- **`record_questions.py merge-proposals --questions <questions.json> --proposals <proposals.json> --out <questions.json>`**:
  copies `propose-answers` output into the questions. A proposal's `group` is the question id.
  `closed_by: proposal` with `basis.kind` in model, memory or person and a non-empty
  `basis.ref` sets `proposed_answer` and `basis`. `closed_by: settled` sets `settled: true` and
  `settled_basis`. Any other basis leaves `proposed_answer: null`. A proposal for an id that is
  not a question is refused (exit 2, nothing written).
