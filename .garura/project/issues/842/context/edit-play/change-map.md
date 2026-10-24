# /edit-play change map — /shape-slice (#842)

Steps 1–2 of /edit-play: load and map, classify and blast radius. Read only; nothing in the
play is changed yet.

**What this change is about.** The first real run of /shape-slice (#844, plan #788) worked,
but a person had to do part of the work by hand: write the slice's hidden file, fill an
existing capability, move pages into their domain folders, convert a record so the next
script could read it, and accept a model check that failed on problems the run did not make.
Ontology v11 and ADR 052 now give /shape-slice two more jobs (the hidden file and the thin
ICE), and the product owner asked for one confirmation brief, not a list of questions. This
change makes the play do all of that itself, and closes the four small gaps of #842 (R3-1 to
R3-4).

**Class.** Intent change. It adds and changes constraints, failure conditions, scenarios,
Done means and the agent/skill flow. So it goes through `reference/ice.md` and a recompile
with /edit-play. Item o (fn-818) is a model-page edit, not a play edit; it goes in the same
change.

Sources read: `reference/ice.md`, `SKILL.md`, `stop-condition.yaml`, every script and test in
`scripts/`; ontology v11 (Capability, Feature, Slice, ICE); ADR 052; the rule
`expectation-generation.md` ("A feature's recovery"); `spine.yaml`, `slice.yaml`;
`asking-a-person.md`; #844 `decisions.md` (1–8); #842 text and comments; #852; the #844 run
records and model commits `fef40169`, `c8910319`, `a3c95551`.

---

## 1. The current ICE map

Paths below are relative to `core/components/plays/shape-slice/`. "Agent" means
`product-os-keeper`.

### Intent and constraints

| Id | One line | Step | Script / agent |
|----|----------|------|----------------|
| Intent | Shape the one slice that shows a business intent is served; fill the model; "does nothing else" (ice.md 8–11, SKILL.md 11–16) | all | — |
| C1 | Read the intent from the model; write its page from the issue when missing; do not stop | 1 | `platform_adapter.py`, `write_intent_page.py`; agent + `author-business-intent` |
| C2 | Read model and memory first; ask only what neither answers | 2, 3 | agent (`find-work-placement`, `find-model-gaps`); `record_questions.py proposals` (settled) |
| C3 | Questions follow the rule for asking a person (all at once, opening, four parts, stand alone) | 3, 5 | `record_questions.py proposals` (shape), `record_questions.py message` |
| C4 | No more questions than the tier; blocking first; each gap not asked is an assumption shown at the checkpoint | 4, 5, 11 | `grill_budget.py tier/split`, `record_questions.py add` |
| C5 | Every question and answer recorded; an answered question is never asked again | 4, 5 | `record_questions.py filter/add/answers/answer/check` |
| C6 | One tester, one surface; no slice without them | 6, 8, 9 | agent (`no-slice.json`); `persist_slice.py` (`one_surface`); `slice_check.py` |
| C7 | Reuse a slice that already serves the intent | 7, 8 | `find_serving_slice.py`; `persist_slice.py --reuse` |
| C8 | Add every part the slice needs and the model lacks, marked to be deepened | 6, 8 | agent (`author-domains`, `enrich-capability-ice`); `persist_fills.py` |
| C9 | Write only the slice, its record, and what C1 and C8 add | 8, 10 | `persist_fills.py`, `persist_slice.py`, `scoped_write_guard.py` |
| C10 | A proposed answer traces to a named source; else none, and the count is shown | 3, 5, 11 | agent + `memory.py cite`; `record_questions.py proposals` (strip, count) |
| C11 | The model's own checks pass after the write | 9 | `slice_check.py` (runs `lint_grounding.py`, `model_names.py`) |
| C12 | Typed yes / change / stop before any commit; a stop undoes every write | 11, 12 | `record_approval.py` (+ `verify`), `scoped_write_guard.py --restore`, `persist_fills.py --undo` |
| C13 | Open and land the change through the change plays, on the plan's branch | 0, E1–E4 | start-change, commit/propose/check/merge-change |
| C14 | Plain English, personas, no real name | 11 | SE-16 grep |

### Failure conditions

| Id | One line | Step | Script |
|----|----------|------|--------|
| F1 | Worked from the issue text alone, or stopped for a missing intent page | 1 | `write_intent_page.py` |
| F2 | Asked what the model or memory answers | 3 | `record_questions.py proposals` |
| F3 | A question broke the asking rule | 3, 5 | `record_questions.py proposals/message` |
| F4 | Over the tier, a gap with no assumption, or an assumption not shown | 4, 11 | `grill_budget.py` |
| F5 | A question or answer not recorded, or asked again | 4, 5 | `record_questions.py filter/check` |
| F6 | A slice with no tester, no surface, or more than one surface | 6, 8 | `persist_slice.py` |
| F7 | A new slice for an intent a slice already serves | 7 | `find_serving_slice.py` |
| F8 | A needed part was skipped | 6, 8 | `persist_fills.py` (SE-9) |
| F9 | A write outside C9 (plan, epic, story, eval, other file) | 8, 10 | `scoped_write_guard.py` |
| F10 | A proposed answer with no source, or a wrong "no proposed answer" count | 3 | `record_questions.py proposals` |
| F11 | The model checks fail and the run went on | 9 | `slice_check.py` |
| F12 | A commit without yes, or a stop left writes | 11, 12 | `record_approval.py verify`, guard `--restore` |
| F13 | Landed outside the change plays or on the wrong branch | E1–E4 | change plays |
| F14 | A real name, or text a person cannot follow | 11 | SE-16 |

Recovery: REC1–REC14, one per F (11 autonomous, 3 human: REC6, REC12, REC13).

### Success scenarios and their evals (Step 13)

| Id | One line | Eval |
|----|----------|------|
| S1 | A new slice: features in order, one surface and tester, intent linked, checks pass, commit after yes | SCE-1 |
| S2 | No intent page: the run writes it from the issue and says so | SCE-2 |
| S3 | A slice already serves: no new slice, the intent added to it | SCE-3 |
| S4 | Tier xs and 8 gaps (2 blocking): at most 5 asked, both blocking, the rest are assumptions | SCE-4 |
| S5 | No surface: no slice written, the reason recorded | SCE-5 |
| S6 | Stop at the checkpoint: the model is as before, no commit | SCE-6 |

### Done means (`stop-condition.yaml`, `check_stop_condition.py`, Step 14 C0)

| Id | One line | File checked |
|----|----------|--------------|
| D1 | The slice check reads valid | `context/shape-slice/slice-check.json` `valid: true` |
| D2 | The approval reads yes | `context/shape-slice/approval.json` `decision: yes` |
| D3 | Only allowed paths written | `context/shape-slice/guard-report.json` `ok: true` |
| D4 | The question record exists | `context/grounding-questions.md` |
| D5 | The trace check names no changed source | `context/shape-slice/citations-check.json` `problems: []` |

### Step evals

| SE | Guards | Step |
|----|--------|------|
| SE-1 | F1/C1 intent page read or written | 1 |
| SE-2 | F2/C2 no question the model answers | 3 |
| SE-3 | F10/C10 no unbacked proposed answer | 3 |
| SE-4 | F4/C4 tier split | 4 |
| SE-5 | F5/C5 nothing asked twice | 4 |
| SE-6 | F3/C3 one message, four parts | 5 |
| SE-7 | F5/C5 every question and answer in the record | 5 |
| SE-8 | F6/C6 one surface with a persona | 6 |
| SE-9 | F8/C8 every feature in the spine or the fills | 6 |
| SE-10 | F7/C7 reuse ran with `--reuse` | 7 |
| SE-11 | F9/C9 persist ok; no path under `.garura/project/plans/` | 8 |
| SE-12 | F11/C11 slice check valid after the last write | 9 |
| SE-13 | F9/C9 guard ok | 10 |
| SE-14 | F4/C4 each assumption shown at the checkpoint | 11 |
| SE-15 | F12/C12 commit only after yes; stop leaves nothing | 11 |
| SE-16 | F14/C14 no real name | 11 |
| SE-17 | F13/C13 change plays in order, right branch | E1–E4 |

---

## 2. The change list

Each item: what is wrong today (with evidence), the ICE elements it adds or changes (draft
text), the step and script it touches, and one acceptance check that fails today and passes
after the fix. New ids continue the current numbers: C15–C18, F15–F18, S7–S10, D6,
SE-18–SE-23, SCE-7–SCE-10, REC15–REC18.

### Change 1 (a, #842 R3-1) — The brief shows what a reuse changed and the slice check's warnings

**Wrong today.** `persist_slice.py` returns `upgraded_to_v2` and `dropped_fields`
(`persist_slice.py:388–391`). `slice_check.py` returns `warnings` for other slices
(`slice_check.py:148–149`). The checkpoint text names only `differences`
(`SKILL.md:431–436`); `grep -c upgraded_to_v2 SKILL.md` gives 0. A kept slice got a new name
and nobody saw it (#842 body).

**ICE.** Covered by the new C17 (Change 9). Adds:
- F17 — The brief hid a result of the run: a reuse difference, a field a record upgrade set
  or dropped, a slice-check warning, an older model problem, a thin ICE, or an assumption.
- REC17 (F17) — Show the hidden result in the brief, in plain words, and ask again. Handoff:
  autonomous.
- SE-18 (F17/C17) — every line of `persist-slice.json` `differences`, `upgraded_to_v2` and
  `dropped_fields`, and every `slice-check.json` warning, has a plain-words line in
  `brief.md`.

**Touches.** Step 11; the new `render_brief.py` (Change 9) reads `persist-slice.json` and
`slice-check.json`.

**Acceptance.** A test in `test_shape_slice_scripts.py`: a reused slice whose record is
pre-v2, plus a second broken slice; `render_brief.py` output holds a line for each
`upgraded_to_v2` field ("The kept slice had no name; it now takes the name '…'") and for the
warning. Fails today (no script; `grep -c upgraded_to_v2 SKILL.md` is 0).

### Change 2 (b, #842 R3-2) — The trace step names the tier

**Wrong today.** Step 3 says a trace source can be "that page's lines or the record entry"
for a model page or a person's earlier answer (`SKILL.md:210`). `memory.py cite` needs tier,
path, lines and fingerprint from a `read` answer. Checked: both sources can be read through
the tool —
`memory.py read --issue <issue> --tier garura --path product/product-os/<page> --start n --end m`
and
`memory.py read --issue <issue> --tier short-term --path <issue>/context/grounding-questions.md --start n --end m`
(a short-term path without the issue folder is refused, `bad_request`).

**ICE.** Change C10:
- C10 — A proposed answer traces to a source the run can name. The run reads that source
  through the memory tool before it cites it: a model page from Garura memory
  (`product/product-os/…`), a person's earlier answer from this issue's short-term memory
  (the question record), and memory from the tier that answered. Where no source exists, the
  question has no proposed answer, and the run reports how many questions have none.
- F10 (add) — … or a trace names a source that was not read through the memory tool.

**Touches.** Steps 3 and 6 contracts (the cite instructions). No script.

**Acceptance.** `grep -n "tier garura --path product/product-os/" SKILL.md` and
`grep -n "tier short-term --path <issue>/context/grounding-questions.md" SKILL.md` each find
a line in Step 3 (0 today).

### Change 3 (c, #842 R3-3) — Undo keeps a "**Touches:** none yet" line

**Wrong today.** In the "lines removed" undo path, a page that held `**Touches:** none yet`
loses that line. `touches.read()` gives `[]` for "none yet", so `had_list` is false and the
heading is deleted (`persist_fills.py:194–201`). Reproduced: page with `**Touches:** none yet`
→ fill → a later edit → `--undo` → the line is gone.

**ICE.** Change C12 and F12:
- C12 (add) — A change or a stop puts back each line the run changed, and only those; a line
  that was there before the run is there after it.
- F12 (add) — … or an undo removed a line that was on the page before the run.

**Touches.** Step 11 (change path); `persist_fills.py undo()`. `intent_touches.py` stays
as it is (it is a stamped copy).

**Acceptance.** New case in `test_fills_undo`: page with `**Touches:** none yet`, fill, append
a line, undo → the page holds `**Touches:** none yet` and the appended line. Fails today.

### Change 4 (d, #842 R3-4) — The message check is a floor, and says so

**Wrong today.** `record_questions.py message` tests the opening by sentence count and the
word "decide" only, and the opening ends at the first line that names a question id
(`record_questions.py:368–376`). Reproduced: an opening that names `Q-surface-1` gives "no
opening before the first question".

**Pick: say it is a floor, and fix the one false fail.** Why: the rest of the rule (plain
words, stands alone for a stranger, examples from different domains) is judgment that no
script can test well; a stronger script gives false fails and false trust. A floor that
gives a false fail must still be fixed. The person's read at the confirmation is the full
test.

**ICE.** Change C3 (with Change 9): "… The script checks the structure only; it is a floor.
The person's read of the brief is the full test." Adds to the Step 5/11 text the same words.

**Touches.** Step 11 (the brief check); `record_questions.py message` becomes
`record_questions.py brief` (Change 9): the opening ends at the first question heading, not
at the first id named.

**Acceptance.** New test: an opening that names `Q-surface-1` in its first sentence, then a
`### Q-surface-1` heading with the four parts → exit 0. Fails today (exit 1).

### Change 5 (e, v11) — /shape-slice writes the slice's hidden file

**Wrong today.** No step or script writes the hidden file; the #844 run wrote
`.garura/project/plans/788/evals/intent-to-design/failure-and-recovery.md` by hand (commit
`fef40169`, then fixed in `8fe62e17`, `c8910319`, `a3c95551`). SE-11 forbids any path under
`.garura/project/plans/` (`SKILL.md:387–389`). C9 and F9 do not allow it (`ice.md:37–39, 65`).

**ICE.**
- C15 (new) — The run writes the slice's hidden file at
  `.garura/project/plans/<plan-id>/evals/<slug>/failure-and-recovery.md`. `<plan-id>` is the
  issue number of the slice's first business intent (for a reused slice, the slice's own
  first intent); `<slug>` is the slice's slug. The run makes that folder, also when no plan
  file exists. The file has one entry for each feature of the slice: the feature (id and
  name), its capability, which of its two ICE is thin, each "Fails if" line of the two ICE
  with a short id (F1, F2, …; "none" when there is none), and exactly one recovery for each
  line: when (a symptom the eval sees), way back (guidance, never code), who fixes ("the
  builder can fix this alone" or "a person must decide"), by
  `standards/rules/expectation-generation.md`, "A feature's recovery". When the slice gains a
  feature, the run adds that feature's entry and keeps every other entry as it is.
- F15 (new) — The hidden file is missing, is outside the home plan's evals folder, has no
  entry for a feature of the slice, leaves out a "Fails if" line, or gives a line no recovery
  or more than one.
- REC15 (F15) — Write the missing entry or line from the two ICE, with one recovery each, in
  the home plan's folder. Handoff: autonomous.
- S10 (new) — (product owner, no plan file) Given an intent with no plan file and a slice
  with three features, when the run ends, then the hidden file is in
  `plans/<id>/evals/<slug>/` with three entries, and each "Fails if" line has one recovery.
  Measure: `hidden-file.json` reads `ok: true` with three entries.
- D6 (new) — the hidden-file check reads ok.
  `check: { type: field_equals, file: "context/shape-slice/hidden-file.json", field: "ok", equals: true }`
- SE-19 (F15/C15) — `hidden-file.json` reads `ok: true`; its entries equal the slice's
  `feature_refs`; its line count equals the "Fails if" count of the two ICE of each feature.
- SCE-10 (S10).
- S1 and SCE-1 (add) — `hidden-file.json` reads `ok: true`.

**Who drafts, who writes.** No existing skill covers it: `author-play-ice` writes a play's
intent, not a product feature's recovery, and no other skill drafts recovery from "Fails if"
lines (searched every `skills/*/SKILL.md`). So, as with the slice choice today (P7, author-slice
#838): the script lists the lines (mechanical), the agent drafts when / way back / who fixes
(judgment) and documents that no skill exists, and the script checks and writes. No new skill
in this change (see open question 3).
- New script `write_hidden_file.py` with three commands:
  - `lines` — reads each slice feature's ICE and its capability's ICE (inline
    `## Agent intent (ICE)` "Fails if:" lines, or `ice.md` `## Intent`), keeps the ids of
    entries already in the file, and writes `hidden-lines.json`.
  - `write` — takes the agent's `hidden-recoveries.json`, refuses (exit 2, nothing written)
    a line with no recovery or two, a "who fixes" that is not one of the two phrases, or a
    path outside the plans folder; makes the folder; writes the file through a temp file;
    adds entries for new features and keeps the others.
  - `check` — writes `hidden-file.json` (`ok`, entries, lines, counts by who fixes) for D6
    and for the brief.
- New Step 8b "Write the hidden file" (after persist, so thin ICE pages exist): `lines` →
  agent contract → `write` → `check`.
- Step 12 commit adds the hidden file: `git add -- <model> <hidden file>`.
- Pre-flight (after Step 0): the plans tree is clean too
  (`git status --porcelain -- .garura/project/plans` empty), so a restore never takes back a
  person's own plan edits.

**Acceptance.** New `test_write_hidden_file.py`: a spine with one slice of two features (one
with two "Fails if" lines, one with none) and no plan file → `write` makes
`plans/340/evals/self-booking/failure-and-recovery.md` with two entries (one "none"), and
`check` reads ok; a recovery missing for one line → exit 2. Fails today (no script).

### Change 6 (f, v11) — The write guard allows that one evals file and nothing else under plans/

**Wrong today.** The guard looks only at `<product_base>product-os`
(`scoped_write_guard.py:179–183`). A stray file under `plans/` is never seen. The script is a
stamped copy; `create-play/references/test_scoped_write_guard.py:137–141` requires every copy
to equal the canonical one (14 copies today, all equal).

**ICE.** Change C9 and F9:
- C9 — The run writes only: the slice (features in build order, surface, intents), its
  record, the parts C1 and C8 add or fill, the thin ICE of C16, and the hidden file of C15.
  Under `.garura/project/plans/` it writes that one file and nothing else. A slice links to
  capabilities, and through them to domains; it has no domain home.
- F9 — The run wrote something outside C9: a plan, an epic, a story, an eval, or any file
  under `plans/` other than the slice's hidden file.
- SE-11 (change) — "no path under `.garura/project/plans/` except the hidden file".

**Touches.** Step 10 and the change/stop restores in Step 11. Add one option to the
canonical guard, `--also-tree <repo-relative dir>` (repeatable): its changed paths join the
same check and the same restore, matched against the repo-relative path. Old calls behave the
same. Restamp all 14 copies byte for byte, so the identity test holds. The play calls:
`--also-tree .garura/project/plans --allow '.garura/project/plans/<plan-id>/evals/<slug>/failure-and-recovery.md'`.
A stop (empty allow set) then also removes the hidden file; the restore removes the empty
folders the run made.
Why not a play-own guard: the plan play (#818) will write under `plans/` too; one tool for
both is fewer moving parts.

**Acceptance.** New cases in `test_scoped_write_guard.py`: with `--also-tree plans`, the
allowed hidden file → ok; a second file under `plans/` → violation; `--restore` removes it.
Today a stray `plans/` file reads `ok: true`.

### Change 7 (g, ADR 052 §5) — A thin ICE for a part with no ICE

**Wrong today.** The Step 6 contract does not say what to do for a part with no ICE
(`SKILL.md:320`). `persist_fills.py` sets only `created_by` and `deepen` (`MARK`, line 68);
it never sets `thin`. The #844 run set the marks by hand (`a3c95551`), with words that differ
from the ontology ("> Thin ICE: proposed by …" in place of "Thin: …").

**ICE.**
- C16 (new) — When a part the slice needs has no ICE, the run proposes a thin ICE from the
  person's answers: in Intent, at least a goal, a limit and one "Fails if" line; in Context,
  one line; in Expectation, one line. It marks it thin in two places that agree: the line
  "Thin: proposed by `/shape-slice` from the person's answers; deepen with
  `/discover-capabilities`." just before `## Intent` on `ice.md` (or, for an ICE kept inline
  in the part's page, just before `## Agent intent (ICE)`), and `metadata.thin: true` on the
  spine entry (the `ices` entry, or the part's own entry when the spine has no `ices` list).
  The brief tells the person, in plain words, that a thin ICE is enough to start but can
  give weak stories and weak checks later, and that `/discover-capabilities` can deepen it.
  The run never sends the person back, and nothing stops.
- F16 (new) — A part the slice needs was left with no ICE; a thin ICE lacks one of the
  minimum lines; only one of the two marks is set; the brief has no thin-ICE warning; or the
  run stopped or sent the person to a discovery play.
- REC16 (F16) — Write the missing lines or the missing mark, and add the warning; go on.
  Handoff: autonomous.
- S7 (new) — (product owner, a part with no ICE) Given a feature the slice needs with no
  ICE, when the run ends, then it has a thin ICE with both marks, its hidden-file entry says
  it is thin, the brief warns, and the run did not stop. Measure: `slice-check.json` lists no
  thin-mark problem for the run's parts, and `hidden-file.json` shows the entry as thin.
- SE-20 (F16/C16) — each part in `fills.json` `thin` has both marks and the minimum lines.
- SCE-7 (S7).

**Touches.** Step 6 contract (agent + `enrich-capability-ice`, which already writes the
inline ICE, seeded from the answers; it now writes the Thin line too); `fills.json` gains
`thin: [<part ids>]`; `persist_fills.py` sets `metadata.thin: true` for them;
`slice_check.py` checks the two marks agree and the minimum lines exist, for the run's parts
only; `render_brief.py` writes the warning.

**Acceptance.** New test: a fill with `thin: ["fn-1"]` and a page with the Thin line →
the spine entry has `metadata.thin: true`; a page with no Thin line → `slice_check.py` lists
"thin mark drift" as a problem. Fails today (`thin` is never written).

### Change 8 (h) — The "does nothing else" text

**Wrong today.** `SKILL.md:15–16` and `ice.md:10–11` say the play "does nothing else: no
plan, no epic, no story, no eval". It now also writes a thin ICE and the hidden file. Also
`SKILL.md:15` and `ice.md:75` name ontology v10; the Context names "the plan play (#818)" and
"the eval play (#798)", now `/shape-plan` and `/shape-eval` (#844 decision 2); the
description front matter says "Writes no plan, epic, story or eval" only.

**ICE.** Intent statement:
"A person names a business intent. /shape-slice shapes the one slice that a person can test
end to end to show the intent is served. It fills the product model with what that slice
needs, proposes a thin ICE for each part that has none, writes the slice with its link to the
intent, and writes the slice's hidden file of failure and recovery conditions. It writes no
plan, no epic, no story and no eval."
Context: ontology v11; ADR 052; `expectation-generation.md` ("A feature's recovery");
#844 `decisions.md`; personas `/shape-plan` (#818) and `/shape-eval` (#798).

**Touches.** `reference/ice.md` Intent and Context; SKILL.md intro, description, Compiled
From, Metadata (by the recompile).

**Acceptance.** `grep -n "does nothing else" core/components/plays/shape-slice/SKILL.md core/components/plays/shape-slice/reference/ice.md`
finds nothing, and `grep -n "v10" …/SKILL.md` finds nothing (both find lines today).

### Change 9 (i, decision 4) — One slice-confirmation brief, not a questionnaire

**Wrong today.** Step 5 shows a list of questions before the slice exists (`SKILL.md:263–287`);
the #844 message was seven questions in a row (`844/context/shape-slice/message.md`). The
checkpoint is a separate list of fields (`SKILL.md:427–436`). Decision 4: "One confirmation,
yes or change — not a list of questions first."

**ICE.**
- C3 (change) — The run talks to the person in one brief, by the shared rule for asking a
  person: an opening that says what the person decides, then the slice, then only the
  questions the model and memory cannot answer, each with Question, Answer, Why it matters
  and Example (several domains), each able to stand alone. The script checks the structure;
  it is a floor, and the person's read is the full test.
- C17 (new) — The brief shows, in plain words: what the person runs (the plays and the
  surface); who tests it; the features in build order, grouped under each capability, with
  each capability linked to its domain and each part marked new, filled or reused; the
  hidden file (its place, the count of "Fails if" lines, how many the builder can fix alone
  and how many a person must decide); what is left out; each assumption; the thin-ICE
  warning; for a reuse, each difference and each field an upgrade set or dropped; the slice
  check's warnings and the count of older model problems; and the count of questions with no
  proposed answer. The person replies yes, change: <what>, or stop, and answers any question
  by its id in the same reply.
- F3 (change) — The person got a list of questions in place of one brief, or a question broke
  the asking rule.
- S1 (add to measure) — the brief has every C17 section.
- SE-6 (change) — `record_questions.py brief` reads `ok: true` for the brief that was shown.
- SE-21 (F3/C17) — `brief.md` has each C17 section; questions appear only inside it.

**Touches.** Steps 5 and 11 merge into one brief at Step 11 (see open question 1 for a
blocking gap with no proposed answer). New script `render_brief.py`: it builds `brief.md`
from the records (`slice.json`, the spine, `fills.json`, `persist-fills.json`,
`persist-slice.json`, `slice-check.json`, `hidden-file.json`, `split.json`,
`questions-checked.json`), so no section can be left out; the agent writes only the opening
and the question text. `record_questions.py message` becomes `brief` (checks the sections and
the four parts; Change 4). `record_questions.py answers/answer/check` read the same reply; a
plain `yes` records each asked question as "accepted as proposed", in the person's words.
The approval prompt from `template-manager` stays the frame.

**Acceptance.** New test: records for a slice with two capabilities in two domains (one new,
one filled), a hidden file with 6 lines (4 builder-alone, 2 person) → `brief.md` holds "What
you run", "Who tests it", both capabilities each with a domain link, "new"/"filled" marks,
"6 … 4 … 2", "Left out", and the thin-ICE warning. Fails today (no script).

### Change 10 (j, decision 5 + run finding) — Fill an existing part, and put pages in their folders

**Wrong today.**
- A fill only adds: an id already in the spine is refused (`persist_fills.py:127–128`). The
  run needed `cap-718` (existing, no domain) to gain `bi-788` and the new domain; that was
  done by hand, outside `fills.json` (`fills.json` has no cap-718; `guard-report.json` allows
  `capabilities/cap-718/capability.md` by hand; spine diff in `fef40169`).
- No folder rule: the doc path is only checked to be on disk (`persist_fills.py:130`). The
  run wrote `capabilities/cap-shape-slice/…` and `features/fn-795/…` for parts that had a
  domain and a capability; commit `c8910319` moved them by hand. Ontology v11: a capability
  lives "under its one domain's folder, or the holding folder `capabilities/<id>/`"; a
  feature "under its capability's folder, or the holding folder `features/<id>/`".

**ICE.**
- C8 (change) — The run reuses what exists, fills what exists in part, and adds what is
  missing. A fill of an existing domain, capability or feature adds the intent to its
  `intents`, sets its domain or capability when it has none, and adds to its page and ICE; it
  keeps what is there. Each new page goes under its parent's folder: a domain at
  `<domain>/domain.md`, a capability at `<domain>/<capability>/capability.md`, a feature at
  `<…capability folder>/<feature>/feature.md`; a part with no parent goes in its holding
  folder. When a fill gives a capability in a holding folder its domain, the run moves its
  page, and the pages of its features, into the domain folder and fixes every link to them.
  Each new part is marked to be deepened. Nothing the slice needs is skipped.
- F8 (change) — A part the slice needs was skipped; an existing part was left unfilled (no
  intent link, or no domain the run knows); or a page is outside its parent's folder.
- REC8 (change) — Add or fill the part at the depth known, at its folder, marked to be
  deepened. Handoff: autonomous.
- S9 (new) — (product owner, an existing capability) Given a needed capability in the spine
  with no domain, when the run ends, then its entry lists the intent and the domain, its
  page and its features' pages are under the domain folder, and the brief marks it filled.
  Measure: `persist-fills.json` `updated` names it, and `lint_grounding.py --spine` finds no
  orphan page.
- SE-9 (change) — also: every page in `fills.json` is at its folder; every filled part is in
  `persist-fills.json` `updated`.
- SCE-9 (S9).

**Touches.** Step 6 contract (`fills.json` gains `updates: [{id, kind, add_intents, domain |
capability (only when empty), page: true}]` and the folder rule); `persist_fills.py` (fills
existing entries, refuses a doc outside its folder, moves pages with their `remove-only` /
`add-only` paths for the guard, records what it changed for undo; links on the intent page
use `intent_touches.relink` and mark a filled part "— changes"); Step 10 allow set from
`persist-fills.json`.

**Acceptance.** Two new cases in `test_fills_paths`: (1) `updates` for an existing capability
→ exit 0, `intents` gains the intent and `domain` is set (exit 2 today, "already in the
model"); (2) a new capability with a domain whose doc is `capabilities/cap-x/capability.md`
→ exit 2 (exit 0 today).

### Change 11 (k, decision 8) — The model check fails only on this run's own problems

**Wrong today.** `valid` is the whole linter's `ok` and this slice's problems
(`slice_check.py:148`). In #844, 70 errors were all older (`lint-before-run.json` 70 errors
vs `slice-check.json`), none in a page the run wrote, and D1 read not valid; the product
owner chose to go on (decision 8).

**ICE.**
- C11 (change) — The model's own checks pass for the parts this run wrote. The run takes the
  check once before its first write. A problem that was there before the run is a warning,
  shown at the brief; it does not stop the run. A new problem stops the run until it is
  fixed.
- F11 (change) — A new problem from this run is left and the run went on; or the run stopped
  on a problem that was there before it.
- S8 (new) — (product owner, an older model) Given a model with older errors in pages the
  run does not write, when the run writes valid parts, then the slice check reads valid and
  the older errors are listed as warnings in the brief. Measure: `slice-check.json` `valid:
  true`, `older_problems` equals the baseline's errors.
- SE-12 (change) — `valid: true` with every new problem gone; `older_problems` shown.
- SCE-8 (S8). D1 keeps its clause; its meaning follows C11.

**Touches.** Step 1 (before any write): `slice_check.py baseline --out lint-before-run.json`.
Step 9: `slice_check.py --baseline <working>lint-before-run.json`. A lint error is "older"
when the baseline holds the same message for the same part; the part is named by its spine
id, so a page the run moved keeps its older errors as older (see open question 4).
`lint_grounding.py` stays as it is (stamped copy).

**Acceptance.** New case in `test_slice_check`: a model with one old feature page that lacks
a section, plus a valid new fill → `valid: true`, the old error in `older_problems` (today
`valid: false`, exit 1); a new fill page that lacks a section → `valid: false`.

### Change 12 (l, run finding) — Step 4 reads the proposals record

**Wrong today.** `proposals` writes a JSON object `{questions, settled, …}`
(`record_questions.py:197–199`); Step 4 passes that file to `filter --questions`
(`SKILL.md:241–242`), which wants a list (`record_questions.py:141–142`). Reproduced with the
#844 file: `filter` exits 2, "the questions file must hold a JSON list". The run made
`questions-checked-list.json` by hand.

**ICE.** No change to a C or F (it is a contract fault inside C5's step). SE-5 (add): the
`filter` step reads the `proposals` output with no file made by hand.

**Touches.** Step 4; `record_questions.py filter` accepts the `proposals` object and reads its
`questions` (a plain list still works).

**Acceptance.** New test: `proposals --out qc.json` then `filter --questions qc.json` →
exit 0. Fails today (exit 2).

### Change 13 (m, run finding) — The rule for asking a person is reachable, and the run knows what to do when it is not

**Wrong today.** The Step 2 contract loads `asking-a-person.md` through the memory tool
(`SKILL.md:197`). No tier holds it: `memory.py find --glob "**/asking-a-person.md"
--every-tier` gives no match. Garura memory is the installed copy, and
`.garura/core/memory/standards/rules/` has no such file; the rule landed in the source
(`core/components/memory/standards/rules/`, #820) after the last install. Memory update
`mu-20261024-002` waits in #844's short-term memory, so no other issue's run can find it
(short-term memory is one issue only).

**The right way.** The rule reaches Garura memory by an install of the source, which a person
asks for. The play never reads the source path. The agent that already reads memory at
Step 2 (`product-os-keeper`) keeps the job; `template-manager` is not used for it, because it
hands out templates, not rules, and it would hit the same missing tier.

**ICE.**
- C18 (new) — The run gets the rule for asking a person only through the memory tool. When
  no tier holds it, the run says so in the brief, follows the floor that this play states
  (an opening that says what the person decides; one thing per question; the four parts;
  examples from several domains; each question stands alone; plain words; personas), and
  raises one memory update that names the gap and says that an install brings the rule. The
  update does not block, and the run does not stop.
- F18 (new) — The run read the rule from a file path, stopped because the rule was missing,
  or went on without saying it was missing.
- REC18 (F18) — Drop the copy read from a path, say the rule is missing, use the play's
  floor, and raise the memory update. Handoff: autonomous.
- SE-22 (F18/C18) — `gather.json` shows the rule found through the tool (tier, path,
  fingerprint), or `rule_missing` with the tiers looked in, a memory update id, and a line
  in `brief.md`.

**Touches.** Step 2 contract; the floor text in Step 11; `render_brief.py` adds the
"rule missing" line. Install is outside this change.

**Acceptance.** `render_brief.py` test with `gather.json` `rule_missing` → `brief.md` holds
the "rule missing" line (fails today: no script, and Step 2 has no missing-rule path:
`grep -n rule_missing SKILL.md` finds nothing).

### Change 14 (n, #852) — The trace check counts only the decisions the slice now rests on

**Wrong today.** D5 reads `citations-check.json` `problems: []`. In #844 it had 7 problems on
5 decisions: 4 were replaced by a later decision of the product owner (decision 1), and one
(`cite-20261024-008`) cites the whole spine, lines 1–378, which Step 8 of the same run then
rewrites. The check also runs at Step 7, before Step 8's writes (`SKILL.md:352`). The tool
cannot mark a record as replaced (#852).

**ICE.**
- D5 (change) — the trace check of the decisions the slice rests on, recorded after the
  run's last write, names no source that is gone or changed.
  `check: { type: field_equals, file: "context/shape-slice/trace-check.json", field: "problems", equals: [] }`
- C10 (add) — Each decision the slice rests on is recorded after the run's last write, with
  the exact lines it rests on (never a whole file).
- SE-23 (D5/C10) — the live set holds one decision for each of: the features and their
  order, the surface, the tester, the reuse, and each proposed answer the slice uses; each
  was recorded after `persist-slice.json`; `trace-check.json` lists the other records apart
  as "not live".

**Touches.** Move the check from Step 7 to a new Step 10b (after the guard, before the
brief): the agent re-records each live decision against the current lines and writes
`citations-live.json`; new script `trace_check.py` runs
`memory.py citations --issue <issue> --check`, keeps the problems of live records as
`problems`, and lists the rest as `not_live` (shown in the brief). When #852 lands, the
script can read the tool's "replaced" mark; nothing here waits for it.

**Acceptance.** New test with the #844 shape: 14 records, 7 problems on 5 records, a live set
of the 9 current ones → `trace-check.json` `problems: []` and 5 `not_live`; a live record
whose source changed → a problem. D5 reads unmet today.

### Change 15 (o) — fn-818 names the feature-to-story map in its acceptance criteria

**Wrong today.** fn-818's Out line names the map
(`.garura/product/product-os/software-delivery-planning/cap-718/fn-818/feature.md:13`), but
its acceptance criteria (lines 24–28) do not (#842 comment from PR #845 round 6).

**ICE.** None in the play. A model-page edit in the same change, add under
"## Acceptance criteria":
"- Given a slice with three features, when the product owner runs /shape-plan and types
yes, then the epic holds the feature-to-story map: one line for each feature, with the story
that delivers it."
Its "Fails if" lines do not change, so its hidden-file entry stays as it is.

**Touches.** That one page. No script.

**Acceptance.**
`awk '/^## Acceptance criteria/{f=1;next} /^## /{f=0} f' <page> | grep -c "feature-to-story map"`
gives 1 (0 today), and `lint_grounding.py --doc <page>` still reads ok.

---

## 3. Blast radius

**ICE elements**
- Added (17): C15, C16, C17, C18; F15, F16, F17, F18; S7, S8, S9, S10; D6; REC15–REC18 (4,
  one per new F).
- Changed (17): Intent statement; C3, C8, C9, C10, C11, C12; F3, F8, F9, F10, F11, F12;
  S1 (measure); D5 (file and meaning); REC8; Context (sources and personas).
- Removed: none.
- Step evals: added SE-18 to SE-23; changed SE-5, SE-6, SE-9, SE-11, SE-12. Scenario evals:
  added SCE-7 to SCE-10; SCE-1 changed.
- Steps: Steps 5 and 11 merge into one brief at Step 11; new Step 8b (hidden file); the trace
  check moves from Step 7 to a new Step 10b; Step 1 takes the lint baseline; pre-flight
  checks the plans tree; Step 12 commits the hidden file.

**Scripts**
- Changed in this play: `persist_fills.py` (fill existing parts, folder rule, thin mark, page
  moves, undo of "none yet"), `slice_check.py` (baseline, own vs older, thin-mark check),
  `record_questions.py` (`filter` reads the proposals object; `message` becomes `brief`, the
  opening fix), `scoped_write_guard.py` (restamped).
- Added in this play: `write_hidden_file.py`, `render_brief.py`, `trace_check.py`, and
  `test_write_hidden_file.py`, `test_render_brief.py`, `test_trace_check.py`; new cases in
  `test_shape_slice_scripts.py`.
- Changed outside this play: `create-play/references/scoped_write_guard.py` and its test
  (`--also-tree`), restamped byte for byte into the 13 other plays that carry a copy (same
  behavior for their calls).
- Unchanged: `persist_slice.py`, `find_serving_slice.py`, `write_intent_page.py`,
  `record_approval.py`, `grill_budget.py`, `spine_text.py`, `preflight.py`,
  `session_stamp.py`, `check_stop_condition.py`, `platform_adapter.py`, and the stamped
  `lint_grounding.py`, `model_names.py`, `intent_touches.py`.

**Stop condition** (`stop-condition.yaml`)
- D5 changed: file `context/shape-slice/trace-check.json` (was `citations-check.json`).
- D6 added: `context/shape-slice/hidden-file.json` `ok: true`.
- D1, D2, D3, D4 clauses unchanged (D1 and D3 now mean more: own problems only; both trees).

**Agents and skills.** Same agents (`product-os-keeper`, `template-manager`); no new skill.
The agent gains two documented P7 jobs (drafting recoveries, re-recording live decisions)
beside the slice choice.

**Model page.** fn-818 `feature.md`, one acceptance line.

**Untouched.** The ontology, ADR 052, the schemas and the rules (they already say v11);
`check_ice_workable.py`; the memory tool (#852 stays its own fix); the install (the asking
rule reaches Garura memory only when a person asks for an install); the plan play and the
eval play; C1, C2, C4, C5, C6, C7, C13, C14 and their F and REC; S2–S6.

---

## 4. Open questions for the product owner

Only the forks that neither the rules nor the #844 decisions settle.

**1. When a gap that blocks the slice has no proposed answer, does the run ask before it shapes the slice?**
- **Answer (proposed):** yes, but only for that kind of gap. The run first shows a short
  brief: what it understood, the gap, and its context. It shapes the slice after the answer,
  and ends with the one confirmation. Every other question waits for the confirmation brief.
  Basis: C6 (no slice without a surface and a tester), decision 4 (one confirmation, not a
  list of questions first), and the rule to present a brief, not a questionnaire.
- **Why it matters:** with no surface the run cannot shape a slice. If the run shapes on a
  guess, the person may reject the whole slice and the run starts again.
- **Example:** a clinic team has not said whether patients test on the booking screen or by
  phone; a shop has not said whether checkout is tested in the mobile app or on the web; a
  bank has not said whether the loan check is tested by an applicant on a form or by a
  clerk on an internal screen.

**2. When a slice that already serves the intent is reused, and the new shape has more features, does the slice gain them?**
- **Answer (proposed):** not on its own. The brief shows the extra features. The person types
  "change: add <feature>" to add them. Then the run adds them to the slice in build order,
  and adds their entries to the hidden file. Basis: C7 keeps a reused slice's features
  today; ontology v11 says that when a slice gains a feature `/shape-slice` adds its entry,
  but not how the slice gains it.
- **Why it matters:** if the run adds features with no yes, the plan and the eval of a slice
  that is already planned change without the person's choice.
- **Example:** a clinic's "Self-booking" slice gets "Pay a deposit"; a shop's "Pay without an
  account" slice gets "Save the card"; a school's "Notes home" slice gets "Read receipt".

**3. Does the agent draft the recoveries now, or do we build a skill for it in this change?**
- **Answer (proposed):** the agent drafts them now and says no skill exists (the same way it
  chooses the slice today), and the job moves into the author-slice skill (#838) when that is
  built. Basis: the instruction "no new skill unless needed"; no existing skill drafts a
  feature's recovery. Against it: the repo rule that agents gather context and skills do the
  work.
- **Why it matters:** a review can mark the agent doing skill work as a fault, and the
  recovery text is the part the eval and the builder's handoff depend on.
- **Example:** a shop's "a card is charged twice" needs a refund and a person; a clinic's "a
  slot is booked twice" the builder can fix alone; a bank's "a loan is approved with no ID"
  needs a person.

**4. Does a page the run only moves into its domain folder count as the run's own, so its older problems stop the run?**
- **Answer (proposed):** no. A problem counts as the run's own only when it is new since the
  run started. A moved page keeps its older problems as warnings. Basis: decision 8 compared
  the problems one by one against the check before the run. Against it: decision 8's fix says
  "the parts the run wrote", and a move writes the page.
- **Why it matters:** in #844 the run moved two older feature pages with 8 older problems
  between them. If a move counts, the run stops on problems it did not make.
- **Example:** a clinic capability moves into its "Scheduling" domain with an old page that
  lacks a section; a shop's "Returns" capability moves with an old feature page that has a
  one-word limit; a bank's "Lending" capability moves with an old page that has no
  acceptance criteria.
