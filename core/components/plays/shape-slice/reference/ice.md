# shape-slice — ICE source

The clean ICE triple this play is compiled from. Update this and recompile via
edit-play; never hand-edit the compiled SKILL.md.

## Intent

A person names a business intent. /shape-slice shapes the one slice that a person can test end
to end to show the intent is served. It fills the product model with what that slice needs,
proposes a thin ICE for each part that has none, writes the slice with its link to the intent,
and writes the slice's hidden file of failure and recovery conditions. It writes no plan, no
epic, no story and no eval. A person can also edit a slice that exists: `--edit` with their own
words changes only the parts they named, after they see each change and say yes.

### Constraints

- C1 — The entry is a business intent's issue number. The run reads the intent from the product
  model, never from the issue text alone. When the model has no page for the intent, the run
  writes that page from the issue, and says so; it does not stop.
- C2 — The run reads the product model and memory first. It asks the person only about what
  neither of them answers.
- C3 — The run talks to the person in one brief, by the shared rule for asking a person: an
  opening that says what the person decides, then the slice, then only the questions the model
  and memory cannot answer, each asking one thing, with Question, Answer, Why it matters and
  Example (several domains), each able to stand alone. The run asks before it shapes the slice
  only when a gap blocks the slice and neither the model, memory nor the run's own proposal can
  answer it. The surface and the tester are never a gap and never a question: an intent does
  not depend on a surface, so the run proposes the surface and the tester when it shapes the
  slice, and the brief shows them. Every other question waits for the one brief. The
  script checks the brief's structure only; it is a floor, and the person's read of the brief is
  the full test.
- C4 — The run asks no more questions than the configured question tier allows. Questions only
  the person can answer (blocking) are always asked and count first. Every gap left open because
  of the budget is written as an assumption, and the person sees each assumption in the brief.
- C5 — Every question and every answer is recorded in the issue's short-term memory. A question
  already answered there is never asked again.
- C6 — The slice holds features from any capability, in build order. It names one person who
  tests it and the one surface they test it on. A slice with no such person or surface is not
  written; the run says why.
- C7 — A slice that already serves the intent (it lists the intent, or it has the same features
  and the same surface) is reused: the run adds the intent to it and makes no new slice. When
  the reused slice no longer serves the intent as it is, the run changes it: it pulls a feature
  in, or pushes a feature out, and the slice stays testable end to end (one surface, one tester,
  one feature or more). A slice in progress (its epic is past ready: a story is started or done)
  is never touched by a shaping run; the run shapes a new slice. Only an edit the person
  approves changes a slice in progress (C20). When the run shapes a kept slice again for an
  intent it already served when the run started (the same input gives the same result however
  often a step runs), with the same surface and the same tester, the slice takes the new
  name, outcome and tester's action: the brief shows each one old and new, the slice record
  keeps a history line (a real date, that a shaping run changed it, and which parts), and the brief
  names the slice's epic as out of date (its stories were written from the old text). The brief
  shows each change, and nothing is kept before the person's yes.
- C8 — The run reuses what exists, fills what exists in part, and adds what is missing. A fill
  of an existing domain, capability or feature adds the intent to its `intents`, sets its domain
  or capability when it has none, and adds to its page and ICE; it keeps what is there. When the
  person's change asks for it, a fill also replaces the part's spine one-line, so that it says what
  the part's page now says; no other field it has is changed. Each new
  page goes under its parent's folder: a domain at `<domain>/domain.md`, a capability at
  `<domain folder>/<capability>/capability.md`, a feature at
  `<capability folder>/<feature>/feature.md`; a part with no parent goes in its holding folder.
  When a fill gives a capability in the holding folder its domain, the run moves its page, and
  the pages of its features, into the domain folder and fixes every link to them. The run
  brings each page it moves or uses in the slice (each feature of the slice, its capability and
  their domains) up to the current rules in the same run, in place; it leaves the pages it does
  not move or use as they are. Each new part is marked to be deepened. Nothing the slice needs
  is skipped.
- C9 — The run writes only: the slice (its features in build order, its surface, the business
  intents it serves), the slice's record, the parts C1 and C8 add, fill or move, the thin ICE of
  C16, and the hidden file of C15. Under `.garura/project/plans/` it writes that one file and
  nothing else. A slice links to capabilities, and through them to its domains; it has no domain
  home.
- C10 — A proposed answer to a question traces to a source the run can name. The run reads that
  source through the memory tool before it cites it: a model page from Garura memory
  (`product/product-os/...`), a person's earlier answer from this issue's short-term memory (the
  question record), and memory from the tier that answered. Where no source exists, the question
  carries no proposed answer, and the run reports how many questions have none. Each decision the
  slice rests on is recorded after the run's last write, with the exact lines it rests on (never
  a whole file).
- C11 — The product model's own checks pass for the slice's own pages: its features, their
  capabilities and their domains. Any problem there fails the check, also a problem that was
  there before the run. The run takes the check once before its first write; a problem in
  another page that was there before the run is a warning, shown in the brief, and does not stop
  the run. A new problem anywhere fails the check.
- C12 — The person approves at a typed checkpoint (yes / change / stop) before anything is
  committed. A change goes back and is shown again. A change or a stop puts back each line the
  run changed, and only those: a line that was there before the run is there after it. A stop
  undoes every write.
- C13 — The run opens its own change and lands it through the change plays; when the intent is
  in a plan, it lands on the plan's branch.
- C14 — Every page a person reads is in plain English (ASD-STE100), uses personas, and names no
  real person.
- C15 — The run writes the slice's hidden file at
  `.garura/project/plans/<plan-id>/evals/<slug>/failure-and-recovery.md`. `<plan-id>` is the
  issue number of the slice's first business intent (for a reused slice, the slice's own first
  intent); `<slug>` is the slice's slug. The run makes that folder, also when no plan file
  exists. The file has one entry for each feature of the slice: the feature (id and name), its
  capability, which of its two ICE is thin, each "Fails if" line of the two ICE with a short id
  (F1, F2, ...; "none" when there is none), and exactly one recovery for each line: when (a
  symptom the eval sees), way back (guidance, never code), who fixes ("the builder can fix this
  alone" or "a person must decide"), by `standards/rules/expectation-generation.md`, "A
  feature's recovery". When the slice gains a feature, the run adds that feature's entry and
  keeps every other entry as it is. A kept entry changes only through an edit the person
  approved (C20). When the file reads ok, no working copy of its "Fails if"
  lines or their ids stays outside the evals folder.
- C16 — When a part the slice needs has no ICE, the run proposes a thin ICE from the person's
  answers: in Intent, at least a goal, a limit and one "Fails if" line; in Context, one line; in
  Expectation, one line. It marks it thin in two places that agree: the line "Thin: proposed from
  the person's words; deepen with `/discover-capabilities`." (ontology v14; any line that starts
  "Thin:" there is the mark, so a page with the older line is still thin) just before
  `## Intent` on `ice.md` (or, for an ICE kept inline in the part's page, just before
  `## Agent intent (ICE)`), and `metadata.thin: true` on the spine entry (the `ices` entry, or
  the part's own entry when the spine has no `ices` list). The brief tells the person, in plain
  words, that a thin ICE is enough to start but can give weak stories and weak checks later, and
  that `/discover-capabilities` can deepen it. The run never sends the person back, and nothing
  stops.
- C17 — The brief shows, in plain words: what the person runs (the surface, and what the tester
  does there); who tests it; the features in build order, grouped under each capability, with
  each capability linked to its domain and each part marked new, filled or reused; the hidden
  file (its place, the count of "Fails if" lines, how many the builder can fix alone and how many
  a person must decide); what is left out; each assumption; the thin-ICE warning; for a reuse,
  each difference, each feature pulled in or pushed out, and each field a record upgrade set or
  dropped; each spine one-line a fill replaced, old and new; the slice check's warnings and the count of older model problems; and the count of
  questions with no proposed answer. The person replies yes, change: <what>, or stop, and answers
  any question by its id in the same reply; a plain yes accepts each proposed answer.
- C18 — The run reads the rule for asking a person only from the shared file the install lays
  beside the installed skills, `_shared/asking-a-person.md`; the rule is not memory, so the run
  never looks for it through the memory tool. When the file is missing, the run says so in the
  brief (an install lays it), follows the floor that this play states (an opening that says
  what the person decides; one thing per question; the four parts; examples from several
  domains; each question stands alone; plain words; personas), and does not stop.
- C19 — The agent only gathers context and passes it on: it reads the model, copies memory
  into short-term memory, calls the memory tool (find, read, cite, propose), calls a skill and
  passes the skill's output on as it is. Every choice, draft and decision is made by a named
  skill: the intent page (`author-business-intent`, one-intent mode), the placement
  (`find-work-placement`), the gaps written as questions (`find-slice-gaps`), the proposed
  answers (`propose-answers`), the openings of the early and the confirmation brief
  (`author-slice-brief`), the slice and what it needs from the model, and the list of an
  edit's changes (`author-slice`), the
  pages (`author-domains`, `enrich-capability-ice`, `enrich-grounding`) and the hidden file's
  recoveries (`author-failure-recovery`). Each skill a dispatch names is installed beside the
  play: a sibling folder `../<name>/` that holds its `SKILL.md`. A copy from one shape to
  another is a script's.
  Every agent dispatch names the skills it calls.
- C20 — A person edits a slice that exists with `/shape-slice #<intent-issue> --edit: <their
  words>`. The run takes the words as they are and does not shape the slice again. It turns them
  into an exact list of changes, each with its record, its part, its old text and its new text,
  and names each other record the edit makes out of date. An edit may change only the slice's
  name, its outcome and the tester's action, the when, way back or who fixes of a named line of
  the hidden file, and a part's spine one-line. The person sees each change in plain words (the
  feature and the failure line it is for, old and new, and why) and each record made out of
  date (named, not changed); nothing is written before their yes. The run writes exactly the
  list and nothing else, and any other change is refused. The slice record keeps a history line
  with who asked, when and their words, and so does the hidden file when it changes. The model,
  the writes and the trace are checked as in a shaping run. An edit may change a slice in
  progress: the person is told it is in progress, and its epic, with its status, is named as
  out of date. A run that stops writes nothing and leaves no copy of the hidden file's lines
  behind. The person's words are kept in the history lines, so they name no real person (C14):
  words that name one are refused before the brief, and the person says it as a role.

### Failure conditions

- F1 — The run worked from the issue text alone, or stopped because the model had no page for
  the intent.
- F2 — The run asked a question that the model or memory already answers.
- F3 — The person got a list of questions in place of one brief; the run asked before it shaped
  the slice about a gap that the model, memory or its own proposal could answer (for example the
  surface); or a question broke the rule for asking a person (more than one thing, a part
  missing, or it cannot stand alone).
- F4 — The run asked more questions than the tier allows (beyond the blocking ones), or left a
  gap open with no written assumption, or the person did not see an assumption.
- F5 — A question or answer was not recorded, or an answered question was asked again.
- F6 — A slice was written with no tester, with no surface, or with more than one surface.
- F7 — A new slice was made for an intent that an existing slice, not in progress, already
  serves; a shaping run changed a slice in progress; a reused slice was changed so that a person can no
  longer test it end to end; or a kept slice's name, outcome or tester's action changed without
  the brief showing it old and new, without a history line on the slice record, or without the
  brief naming the slice's epic as out of date.
- F8 — A part the slice needs was skipped; an existing part was left unfilled (no intent link,
  or no domain the run knows); a page is outside its parent's folder; a page the run moved or
  used still breaks a current rule; or a fill changed a field of an existing part other than its
  intents, its missing parent, or the one-line the person's change asked for.
- F9 — The run wrote something outside C9: a plan, an epic, a story, an eval, or any file under
  `.garura/project/plans/` other than the slice's hidden file, or another file.
- F10 — A proposed answer has no source the run can name, a trace names a source that was not
  read through the memory tool, or the count of questions with no proposed answer is missing or
  wrong.
- F11 — A problem in the slice's own pages, or a new problem from this run, is left and the run
  went on; or the run stopped on an older problem in a page it does not move or use.
- F12 — Something was committed without the person's yes, a stop left writes behind, or an undo
  removed a line that was on the page before the run.
- F13 — The change landed outside the change plays, or on the wrong branch.
- F14 — A page names a real person, or a person cannot follow it.
- F15 — The hidden file is missing, is outside the home plan's evals folder, has no entry for a
  feature of the slice, leaves out a "Fails if" line, or gives a line no recovery or more than
  one; or a working copy of its lines or ids stays outside the evals folder after it reads ok.
- F16 — A part the slice needs was left with no ICE; a thin ICE lacks one of the minimum lines;
  only one of the two thin marks is set; the brief has no thin-ICE warning; or the run stopped or
  sent the person to a discovery play.
- F17 — The brief hid a result of the run: a reuse difference, a feature pulled in or pushed
  out, a field a record upgrade set or dropped, a spine one-line a fill replaced, a slice-check
  warning, an older model problem, a thin ICE, or an assumption.
- F18 — The run read the rule for asking a person from a place other than
  `_shared/asking-a-person.md` (through the memory tool, or from another path), stopped because
  the rule was missing, or went on without saying it was missing.
- F19 — An agent dispatch asks the agent to do work no named skill does: to choose, draft,
  decide or write content itself, or to reshape a skill's output; or a dispatch names no
  skills.
- F20 — An edit changed something that is not on the list the person saw, wrote before the
  person's yes, changed a part an edit may not change, or left no history line; an edit of a
  slice in progress whose brief did not say it is in progress; or a kept entry of the hidden
  file changed with no edit the person approved.

## Context

- The product model: the memory schema `standards/schemas/product-os/ontology.md`, read through
  the memory tool (v11:
  Slice with its hidden file, ICE with its thin mark, Capability and Feature with their holding
  folders, Business Intent; Q33, Q34, Q36–Q40); `spine.yaml` and `slice.yaml` schemas; ADR 049
  (the shaping loop: /shape-slice, then /shape-plan, then /shape-eval) and ADR 052 (/shape-slice
  writes the hidden file and proposes a thin ICE).
- The rules: `_shared/asking-a-person.md` (the shared file beside the installed skills; not
  memory), `standards/rules/user-questions.md`, `standards/rules/no-unbacked-recommendation.md`,
  `standards/rules/expectation-generation.md` ("A feature's recovery").
- The question tier: `shape-slice.grill-tier` in config (xs 5, s 12, m 25, l 45, xl 70; default
  m), and the budget script built for #817.
- The agent that gathers the model and memory and runs the skills: `product-os-keeper`. The
  skills that do the work: `author-business-intent` (one-intent mode), `find-work-placement`,
  `find-slice-gaps`, `propose-answers`, `author-slice-brief`, `author-slice` (#838; shape,
  reuse and fix modes), `author-domains` (no profile), `enrich-capability-ice` (directional
  depth), `enrich-grounding` (update, new-feature, thin and fix modes) and
  `author-failure-recovery`. The loose links of the whole model are
  not this play's work: the loops find them.
- The scripts that do the mechanical copies: `record_questions.py merge-proposals` (the
  proposals into the questions), `render_brief.py --early` (the early brief's questions),
  `write_hidden_file.py check --clear-working` (no copy of the hidden file's lines outside the
  evals folder) and `safe_write.py` (every write through a temp file).
- The product owner's decisions for this play: `.garura/project/issues/795/context/decisions.md`,
  `.garura/project/issues/844/context/decisions.md` and
  `.garura/project/issues/842/context/edit-play/decisions.md`.
- Personas: the product owner (gives the intent, answers, approves); the plays after it in the
  shaping loop (`/shape-plan`, #818, and `/shape-eval`, #798), which read the slice and its
  hidden file.

## Expectation

### Success scenarios

- S1 — (product owner, a new slice) Given a confirmed business intent with a model page and no
  slice that serves it, when the run ends, then one slice is in the model with features in
  build order, one surface with its tester, and the intent in its `intents`; the model's
  checks pass; the slice's hidden file is written; the person saw one brief with every C17
  section; the commit exists only after a typed yes. Measure: the slice check reads valid, the
  hidden-file check reads ok, the brief check reads ok, the approval record reads yes, and the
  write report lists only allowed paths.
- S2 — (product owner, no intent page) Given an intent issue that the model has no page for,
  when the run ends, then the model has the intent's page, written from the issue, and the run
  said so; the slice is shaped as in S1. Measure: the intent page exists, and the run record
  names it as written by this run.
- S3 — (product owner, a slice already serves) Given an intent that an existing slice, not in
  progress, already serves (same features and surface), when the run ends, then no new slice is
  made and the intent is in that slice's `intents`. Measure: the spine has the same number of
  slices, and the existing slice lists the intent.
- S4 — (product owner, a small budget) Given tier xs (5) and 8 gaps, 2 of them blocking, when
  the questions are shown, then at most 5 are asked, both blocking ones among them, and the
  other gaps are shown as written assumptions in the brief. Measure: the question record holds
  5 or fewer asked questions including both blocking ones, and one assumption for each gap not
  asked.
- S5 — (product owner, no surface) Given an intent for which no person can test anything end to
  end, when the run ends, then no slice is written, and the run says why. Measure: the spine's
  slices are unchanged, and the run record holds the reason.
- S6 — (product owner, stop at the checkpoint) Given a shaped slice, when the person types
  stop, then the model and the plans folder are as they were before the run, and nothing is
  committed. Measure: the model tree and the plans tree have no change against the run's start,
  and no commit was made.
- S7 — (product owner, a part with no ICE) Given a feature the slice needs with no ICE, when the
  run ends, then it has a thin ICE with both marks, its hidden-file entry says it is thin, the
  brief warns, and the run did not stop. Measure: `slice-check.json` lists no thin-mark problem
  for the slice's parts, and `hidden-file.json` shows the entry as thin.
- S8 — (product owner, an older model) Given a model with older errors in pages the run does not
  move or use, when the run writes valid parts, then the slice check reads valid and the older
  errors are listed as warnings in the brief. Measure: `slice-check.json` reads `valid: true`,
  and its `older_problems` are the baseline's errors in those pages.
- S9 — (product owner, an existing capability) Given a needed capability in the spine with no
  domain, when the run ends, then its entry lists the intent and the domain, its page and its
  features' pages are under the domain folder, and the brief marks it filled. Measure:
  `persist-fills.json` `updated` names it, and the slice check finds no orphan page.
- S10 — (product owner, no plan file) Given an intent with no plan file and a slice with three
  features, when the run ends, then the hidden file is in `plans/<id>/evals/<slug>/` with three
  entries, and each "Fails if" line has one recovery. Measure: `hidden-file.json` reads
  `ok: true` with three entries.
- S11 — (product owner, an edit) Given a slice with a hidden file, when the person runs
  `--edit` asking for two "who fixes" lines to go to a person and types yes, then those two
  lines change, every other line of the hidden file and of the model stays as it was, and the
  hidden file and the slice record each hold a history line with the person's words. Measure:
  `edit-check.json` reads `ok: true` with exactly two changes, and `hidden-file.json` reads
  `ok: true`.
- S12 — (product owner, a kept slice shaped again) Given a slice that already serves the intent
  and has an epic, when the run shapes it again with a new name and the same surface and tester,
  then the slice record takes the new name and keeps a history line, and the brief shows the
  name old and new and names the slice's epic as out of date. Measure: `persist-slice.json`
  `replaced` names `slice.name`, its `out_of_date` names the epic, the slice record's last
  `edits` entry names `slice.name`, and `brief.md` shows both lines.

### Done means

- D1 — the slice check report exists and reads valid.
  check: { type: field_equals, file: "context/shape-slice/slice-check.json", field: "valid", equals: true }
- D2 — the person's approval is recorded as yes.
  check: { type: field_equals, file: "context/shape-slice/approval.json", field: "decision", equals: "yes" }
- D3 — the write report shows only allowed paths were written.
  check: { type: field_equals, file: "context/shape-slice/guard-report.json", field: "ok", equals: true }
- D4 — the question record exists, with every question and answer of the run.
  check: { type: artifact_exists, path: "context/grounding-questions.md" }
- D5 — the trace check of the decisions the slice rests on, recorded after the run's last
  write, names no source that is gone or changed.
  check: { type: field_equals, file: "context/shape-slice/trace-check.json", field: "problems", equals: [] }
- D6 — the hidden-file check reads ok.
  check: { type: field_equals, file: "context/shape-slice/hidden-file.json", field: "ok", equals: true }

### Recovery (one per failure condition)

- REC1 (F1) — read the intent from the model; write the missing page from the issue, then go
  on. Handoff: autonomous.
- REC2 (F2) — drop the question, and use the answer the model or memory gives. Handoff:
  autonomous.
- REC3 (F3) — put the questions in the one brief, propose an answer for each gap the run can
  answer, rewrite each question to the rule, and show the brief again. Handoff: autonomous.
- REC4 (F4) — cut the questions to the budget, blocking first, and write an assumption for
  every gap not asked; show the assumptions in the brief. Handoff: autonomous.
- REC5 (F5) — record every question and answer, and take back any repeat question. Handoff:
  autonomous.
- REC6 (F6) — take the slice back; propose one surface and its tester from the model and
  memory, and show them in the one brief. The run never asks for the surface or the tester.
  When nothing in the model or memory names a surface a person can test end to end, write no
  slice, say why, and close. Handoff: autonomous.
- REC7 (F7) — remove the new slice and add the intent to the slice that already serves it; put
  back a slice in progress as it was and shape a new slice; put back the feature whose change
  broke the end-to-end test; or, for a kept slice's text, add the missing history line, show
  each change old and new, and name the slice's epic as out of date in the brief, then ask
  again. Handoff: autonomous.
- REC8 (F8) — add or fill the part at the depth known, at its folder, marked to be deepened, and
  bring each page the run moved or used up to the current rules; put back any other field a fill
  changed. Handoff: autonomous.
- REC9 (F9) — undo the write outside the allowed set. Handoff: autonomous.
- REC10 (F10) — strip the proposed answer that has no source (never replace it with another),
  read the source through the memory tool before citing it, and report the count. Handoff:
  autonomous.
- REC11 (F11) — fix each problem the check lists in the slice's own pages and each new problem,
  and run the check again; the run does not go on until it passes. An older problem in a page
  the run does not move or use is shown as a warning, not fixed. Handoff: autonomous.
- REC12 (F12) — take the commit back, undo the writes a stop left, or put back the line an undo
  removed. Handoff: human.
- REC13 (F13) — land the change through the change plays, on the branch the target script
  gives. Handoff: human.
- REC14 (F14) — rewrite with personas and plain words. Handoff: autonomous.
- REC15 (F15) — write the missing entry or line from the two ICE, with one recovery each, in the
  home plan's evals folder; delete the working copies of its lines once it reads ok. Handoff:
  autonomous.
- REC16 (F16) — write the missing lines or the missing mark, and add the warning; go on.
  Handoff: autonomous.
- REC17 (F17) — show the hidden result in the brief, in plain words, and ask again. Handoff:
  autonomous.
- REC18 (F18) — drop the copy read from another place and read `_shared/asking-a-person.md`;
  when it is missing, say so in the brief, use the play's floor, and go on. Handoff:
  autonomous.
- REC19 (F19) — take back what the agent made, and send the work to the named skill that does
  it, through the agent; when no skill does it, close HALTED and name the missing skill. The
  agent never does it. Handoff: autonomous.
- REC20 (F20) — put back each change that is not on the approved list, or every write made
  before the yes, and add the missing history line; when the slice is in progress and the brief
  did not say so, put back the edit, show it in the brief and ask again; nothing of the edit is
  kept without the person's yes. Handoff: autonomous.
