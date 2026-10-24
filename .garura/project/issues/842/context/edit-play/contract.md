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
