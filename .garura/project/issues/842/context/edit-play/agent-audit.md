# Agent audit — /shape-slice and product-os-keeper

The product owner's rule: the agent only collects context. A skill does the actual work.
(CLAUDE.md Behavioral Rule 4; `core/components/plays/edit-play/references/agent-audit.md`,
P1–P11, P7 above all.)

This audit reads each dispatch to the agent in `core/components/plays/shape-slice/SKILL.md`
(compiled from `reference/ice.md`) and gives each part of it a verdict:

- **CONTEXT** — the agent reads, gathers, copies memory into short-term memory, calls the
  memory tool (find, read, cite, propose), or calls a skill and passes its output on.
- **WORK** — the agent chooses, drafts, decides or writes content that no named skill makes.

Read: the play's SKILL.md and ICE; `core/components/agents/product-os-keeper.md`; the skills
`author-business-intent`, `find-work-placement`, `find-model-gaps`, `propose-answers`,
`enrich-capability-ice`, `author-domains`, `author-failure-recovery`; and, to look for a skill
that already does a WORK part, `author-scope`, `author-roadmap`, `author-knowledge-brief`,
`find-answers-in-sources`, `link-model-gaps`. Issue #838 (author-slice) read with `gh issue view`.

## Result in short

The play sends the agent 9 contracts (7 written as JSON, 2 sent as "send it back to the agent").
Only 3 are pure context: the intent draft (Step 1), the hidden-file recoveries (Step 8b) and the
live re-cite (Step 10b). The other 6 hold work the agent does itself. Count of work parts: 14.
Not one of them is fully covered by an existing skill.

Four new skills cover all 14, with the author-slice skill (#838) taking the most.

## Rows — one per dispatch, split where a contract mixes context and work

| # | Step | Task, in short | What the agent is asked to do | Verdict | Skill |
|---|------|----------------|-------------------------------|---------|-------|
| 1 | 1 | Draft the intent page from the issue | Copy the ontology's Business Intent kind into short-term memory; call author-business-intent with the issue as a plain statement; pass the draft on | CONTEXT | `author-business-intent` (exists; fit gap A1) |
| 2a | 2 | Gather the model and memory | Read the intent page, spine and the pages it reaches; memory.py search / read / find; copy what it reads into short-term memory; record tier, path, lines, fingerprint in `gather.json` | CONTEXT | — |
| 2b | 2 | Get the rule for asking a person | memory.py find + read into `asking-a-person.md`; when missing, memory.py propose (text given by the play) and write `rule_missing` | CONTEXT | — |
| 2c | 2 | Place the intent's outcome | Call find-work-placement with the domain shelves | CONTEXT | `find-work-placement` (exists) |
| 2d | 2 | List what the slice needs and the model lacks | "find-model-gaps lists what the slice needs and the model lacks or holds in part" | WORK | no skill — `find-model-gaps` does not do this (fit gap A2). Needs `find-slice-gaps` |
| 2e | 2 | Write each gap as a question | Write id, topic, question, why, two or more examples from different domains, blocking, assume, settled with basis | WORK | no skill — needs `find-slice-gaps` |
| 2f | 2 | Propose the surface and the tester | "propose them yourself (topic surface or tester) from the intent and the model" | WORK | no skill — needs `author-slice` |
| 3a | 3 | Propose an answer for each question | Call propose-answers; put each answer and its basis into `questions.json` | CONTEXT (skill does it) | `propose-answers` (exists; fit gap A3) |
| 3b | 3 | Propose the surface and the tester again | "Propose the surface and the tester yourself" | WORK | no skill — needs `author-slice` |
| 3c | 3 | Record each proposed answer | memory.py read of each source, then memory.py cite; list the cites | CONTEXT | — |
| 3d | 3 (REC3) | Rewrite the questions that break the shape | The play sends the `record_questions.py proposals` exit-1 list back "to the agent to rewrite" | WORK | no skill — needs `find-slice-gaps` (rewrite mode) |
| 4 | 5 | Write the early brief | "have the agent write a short brief": an opening of two or three sentences, then each early question with its four parts. No JSON contract is written for this dispatch (P1 fail) | WORK | no skill — needs `author-slice-brief` for the opening; the questions part is layout and goes to a script |
| 5a | 6 | Choose the slice | Name the one surface and its tester; pick the features from any capability in build order; why_this_order; left_out; `no_slice` with its reason. Contract says "No skill does this choice yet … make it yourself (P7)" | WORK | no skill — needs `author-slice` (#838) |
| 5b | 6 | Decide what the slice needs from the model | Decide each part that is new, filled or updated; for an update set `add_intents`, the domain or capability when the part has none, and `page: true`; write `fills.json` | WORK | no skill — needs `author-slice` (the needs list); the placement reasoning under it can come from `find-work-placement` |
| 5c | 6 | Write a new domain page | Call author-domains | CONTEXT (skill does it) | `author-domains` (exists; fit gap A5) |
| 5d | 6 | Write a new capability, its features and their ICE | Call enrich-capability-ice, seeded from the person's answers | CONTEXT (skill does it) | `enrich-capability-ice` (exists; fit gap A4) |
| 5e | 6 | Write a new feature page under a capability that exists | Not named to a skill. enrich-capability-ice details a whole capability and re-identifies all its features, so it over-reaches for one feature | WORK | no skill — needs `enrich-grounding` |
| 5f | 6 | Bring each page the slice moves or uses up to the current rules, in place | "Bring each page … up to the current rules, in place, and list it as an update"; "edit an existing page where it is now" | WORK | no skill — needs `enrich-grounding`. (`author-domains` can raise a light domain page and keep its sections, which covers the domain case only.) |
| 5g | 6 | Write a thin ICE for a part with none | "write a thin ICE from the person's answers (Goal, Limit, one Fails if, Context, Checked by …)" | WORK | no skill — needs `enrich-grounding` (thin-ICE mode) |
| 5h | 6 | Write `slice.json` and `fills.json` | The content of both files is the choice of 5a and 5b | WORK | no skill — `author-slice` writes them |
| 5i | 6 | Record the features, order, surface and tester decisions | memory.py cite with the trace | CONTEXT | — |
| 6 | 7 | Decide what a reused slice pulls in or pushes out | Compare features; pull in, push out; keep it testable end to end; write `reuse.json`; then cite | WORK (the decision); CONTEXT (the cite) | no skill — needs `author-slice` (reuse mode) |
| 7 | 8b | Draft the recovery of each "Fails if" line | Copy `expectation-generation.md` through the memory tool; gather the ICE pages; call author-failure-recovery; pass on `hidden-recoveries.json` | CONTEXT | `author-failure-recovery` (exists; fit gap A6) |
| 8 | 9 (REC11) | Fix each problem the model check lists | "send `slice-check.json` to the agent (Step 6 contract plus problems), let it fix each problem" | WORK | no skill — the skill that wrote the page fixes it: `enrich-grounding` for a page the slice uses; `author-slice` for `slice.json` or `fills.json` |
| 9 | 10b | Record the live decisions again | memory.py read of the current lines, memory.py cite, list the new ids in `citations-live.json` | CONTEXT | — |
| 10 | 11 | Write the opening of the confirmation brief | Two or three plain sentences: what the person decides, what happens with the reply, that the intent page was written from the issue; by the rule for asking a person | WORK | no skill — needs `author-slice-brief` |

## The skills needed — grouped

Every name follows `core/components/memory/standards/rules/naming.md`: a skill verb from
`naming.yaml` first, then the object. None of the four is a reserved command, and none is used
by a play, loop, skill or agent now.

### 1. `author-slice` (issue #838) — the choice of the slice

Takes the intent page, the gathered context, the placement result, the question record and the
assumptions. Writes `slice.json` and `fills.json`, with the reason and the basis for each choice.
Issue #838 already gives it rows 5a and 5h. These also belong in it, because each is a part of
the same choice:

- the surface and the tester as proposed answers, with their basis, for the question record
  (rows 2f, 3b) — the same choice it makes in 5a, made early so the brief can show it;
- the needs list: which domain, capability, feature and ICE are new, filled or updated, and the
  parent of a part that has none (row 5b); it takes the placement from `find-work-placement`;
- the reuse mode: given the kept slice and `serving.json`, write `reuse.json` (row 6);
- `no-slice.json` with its reason when no surface can be tested end to end (5a; #838's third
  "done when" line);
- a fix mode for problems the check finds in `slice.json` or `fills.json` (row 8).

### 2. `find-slice-gaps` — the questions

List each thing the slice needs that neither the model nor memory answers, and write each as one
question by the rule for asking a person (the copy in short-term memory): id, topic, question,
why, examples from several domains, blocking, assume, and `settled` with its basis when the
context answers it. The surface and the tester are never blocking. A rewrite mode takes the list
`record_questions.py proposals` refuses and rewrites only those (rows 2d, 2e, 3d).

Why a new skill and not `find-model-gaps`: that skill finds loose links in the whole model
(unattributed nodes, one-way intent links, duplicates) and sends missing work to
`/discover-capabilities`, `/discover-domains` and `/discover-intent`. /shape-slice must fill the
model itself and must never send the person to a discovery play (C8, C16). Its input has no
intent and no slice. The two jobs do not share a rule.

### 3. `author-slice-brief` — the words the person reads first

Write the opening of the early brief (row 4) and of the confirmation brief (row 10): two or three
plain sentences that say what the person decides, what the run understood, and what happens with
the reply, by the rule for asking a person (or the play's floor when the rule is missing).

The brief does **not** belong in `author-slice`, for three reasons:

- the early brief runs at Step 5, before the slice is shaped, so `author-slice` has nothing to
  say yet;
- the brief follows the shared rule for asking a person, which is a different rule from the
  rules of a slice;
- the rest of the confirmation brief is already built by a script (`render_brief.py`), so the
  skill writes only the opening; the early brief's questions part should also go to a script
  (for example a `render_brief.py --early` mode), so that the skill writes only words.

`author-knowledge-brief` is close in purpose but does not fit: it is the knowledge-builder's
brief for `/check-knowledge`, its input is `search.json` and `build.json`, and its rule says
"Never a question; never example answers to pick from". A later change can merge the two into
one brief skill for every play that talks to a person; this audit does not ask for that now.

### 4. `enrich-grounding` — the pages the slice uses

Write on the pages of the parts the slice needs, from the person's answers and the assumptions,
keeping every section and line a page had:

- bring an existing domain, capability or feature page the slice moves or uses up to the current
  grounding template, in place (row 5f);
- write one new feature page under a capability that exists, at the depth the run knows, without
  re-detailing the capability (row 5e);
- thin-ICE mode: write the minimum thin ICE of C16 — a goal, a limit, one "Fails if" line, one
  context line, one check (row 5g); the script still writes the two thin marks;
- fix mode: fix each problem the model check finds in those pages (row 8).

The thin ICE could be a fifth skill (`author-thin-ice`), because C16 has its own minimum and
`/discover-capabilities` deepens it later. It goes in `enrich-grounding` here because it is page
content for the same parts, from the same answers, in the same step.

## Fit gaps in the existing skills the play uses

- **A1 — `author-business-intent`.** It is written for `/discover-intent`: `source_manifests` is
  required, it drafts one intent *per need* (often several), and it also writes coverage and
  questions, to a YAML draft. The play wants one intent page for one issue, as
  `intent-draft.json`. If the skill returns more than one intent, the agent must choose one: that
  is work. The skill needs a one-intent mode (input: one statement; output: one intent), or the
  play's contract must match the skill's.
- **A2 — `find-model-gaps`.** The play and the agent's own skill table say it "lists what the
  slice needs and the model lacks". It does not (see skill 2 above). Remove it from Step 2, or
  keep it only for the model's loose links, and fix the line in `product-os-keeper.md`.
- **A3 — `propose-answers`.** Its description says it is used by the knowledge-builder agent in
  `/research-knowledge`. Its input is `gaps`, `sources`, `run`; its output is `proposals.json`
  with `group`, `closed_by`, `answer`, `basis`, `context`. The play wants `questions.json` with
  `proposed_answer` and `basis {kind, ref}`. Moving the one shape into the other is a mechanical
  copy: give it to a script (or give the skill the play's shape), so that the agent does not
  reshape answers. Also, its step 2 says "mark a value the person must set … as our default"; the
  play's cardinal rule says no answer without a named source. The two must agree.
- **A4 — `enrich-capability-ice`.** It always writes the capability at the detailed stage
  ("Never leave it directional"). The play says "at the depth the run knows … marked to be
  deepened", and `persist_fills.py` sets `detail: directional` and `metadata.deepen: true` on the
  spine. The page and the spine then disagree. Its description also names only
  `/discover-capabilities` as the caller.
- **A5 — `author-domains`.** It needs `grounding_path` (a routing result) and writes a
  `seed-manifest.yaml` that can hold a directional profile block. The profile is outside C9 for
  /shape-slice; `persist_fills.py` must ignore it, or the skill needs a mode with no profile.
- **A6 — `author-failure-recovery`.** It needs `ice_pages` and `rule` as inputs. The play's Step
  8b contract passes neither (it passes `spine` and `product_base`). The agent gathering them is
  context, but the contract should name them (P2).

## Wrong direction — places that tell the agent to do work

- **`author-failure-recovery`, Process step 5:** "Add the line's id to `vague` so the agent can
  tell the person." The agent never talks to the person (P5), and telling the person is the
  brief's job. It should say: "so the play shows it in the brief".
- **`enrich-capability-ice`, Rules:** "Only a business rule … goes back to the caller as a
  question." The caller is the agent, which would then have to write the question. It should
  return the gap as data, for `find-slice-gaps` (or the calling play's question skill) to write.
- **`product-os-keeper.md`, Core Principle:** "YOU decide … HOW to interpret skill output —
  shaping it into the caller's contract." This invites the agent to reshape a skill's output,
  which is how row 3a turns into work. It should say: pass the skill's output on, or give the
  copy to a script.
- **`product-os-keeper.md`, skill table:** `find-model-gaps` for /shape-slice "(what the slice
  needs and the model lacks)" — the skill does not do that (A2).
- **`shape-slice/SKILL.md`, Role and Agent boundaries:** "You hand every piece of judgment to
  the `product-os-keeper` agent", and the agent's domain lists "shape the slice … draft the hidden
  file's recoveries; write the brief's opening". The judgment should go to skills, through the
  agent. The play also says "The agent does that choice itself … (agent principle P7)". P7 allows
  that only as a written gap; the product owner's rule does not allow it at all.

`find-work-placement` is the right direction and a good model for the new skills: "Reasoning is
yours (the skill); the agent only retrieves."

A change to which agent or skill does a step is a change to the play's agent/skill flow, so it is
an intent change: it goes through `reference/ice.md` and `/edit-play`, not a direct edit of the
compiled SKILL.md.

## Summary

| Step | Verdict | Skill |
|------|---------|-------|
| 1 — intent page | CONTEXT | `author-business-intent` (exists; needs a one-intent mode) |
| 2 — gather, memory, asking rule, placement | CONTEXT | `find-work-placement` (exists) |
| 2 — gaps the slice needs, written as questions | WORK | `find-slice-gaps` (new) |
| 2 — surface and tester proposal | WORK | `author-slice` (new, #838) |
| 3 — proposed answers, cites | CONTEXT | `propose-answers` (exists; shape gap → script) |
| 3 — surface and tester proposal | WORK | `author-slice` (new, #838) |
| 3 (REC3) — rewrite questions | WORK | `find-slice-gaps` (new) |
| 5 — early brief | WORK | `author-slice-brief` (new) + a script for the questions part |
| 6 — choose features, order, surface, tester, left out, no slice | WORK | `author-slice` (new, #838) |
| 6 — the needs list (`fills.json`) | WORK | `author-slice` (new, #838) |
| 6 — new domain page | CONTEXT | `author-domains` (exists) |
| 6 — new capability with features and ICE | CONTEXT | `enrich-capability-ice` (exists; depth conflict) |
| 6 — new feature under a capability that exists | WORK | `enrich-grounding` (new) |
| 6 — pages moved or used, up to current rules | WORK | `enrich-grounding` (new) |
| 6 — thin ICE | WORK | `enrich-grounding` (new, thin-ICE mode) |
| 6 — cites | CONTEXT | — |
| 7 — reuse: pull in, push out | WORK | `author-slice` (new, #838, reuse mode) |
| 8b — hidden-file recoveries | CONTEXT | `author-failure-recovery` (exists) |
| 9 (REC11) — fix check problems | WORK | `enrich-grounding` / `author-slice` (fix modes) |
| 10b — live re-cite | CONTEXT | — |
| 11 — brief opening | WORK | `author-slice-brief` (new) |

New skills: `author-slice` (#838, grown), `find-slice-gaps`, `author-slice-brief`,
`enrich-grounding`.

One naming note: `naming.md` rule 2 still says an object must never be "a word the model
dropped, such as epic or slice". Ontology v11 has Slice again, and `/shape-slice` and #838 use
the word. That line needs an update before a `*-slice*` skill lands (`naming.yaml` has no list
of dropped words, so the linter does not check it).
