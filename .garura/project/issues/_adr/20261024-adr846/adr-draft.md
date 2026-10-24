# ADR 052 — /shape-slice Writes the Slice's Hidden File and Proposes a Thin ICE, the Plan Play Only Plans, and a Thin ICE Is Partly Ready

**Status:** Proposed
**Date:** 2026-10-24
**Level:** framework
**Decided by:** · **Decided in:** #844 (decisions 6 and 7, from the first real `/shape-slice` run, PR #845) and #846 (product ontology v11, the three `/edit-ontology` checkpoints: questions, kinds, links and rules; PR #849, whose review found DF-1 and DF-2), plan #788
**Amends:** ADR 049 — §1.1 ("/shape-slice … writes nothing else"), §1.2 (the plan play makes "the slice's hidden file"), §4 ("The plan play reads all of each ICE, once", "The hidden file, written by the plan play", and "made again together"), §5 (the recovery rule "covers a story"; its Affects and References name the old rule section "A story's recovery (product ICE)", now "A feature's recovery (product ICE)"), and the Consequence "Each ICE is interpreted once, by the plan play" · ADR 047 — §6 (partly ready covered only gaps outside the ICE's parts), §7 (the check now also counts no lines) and §8 ("The richness of an ICE is assessed and reported")
**Affects:** `core/components/memory/standards/schemas/product-os/ontology.md` (v11, landed in #846), `core/components/memory/standards/rules/expectation-generation.md` (the section "A story's recovery (product ICE)" is now "A feature's recovery (product ICE)", landed in #846), `core/components/memory/standards/schemas/product-os/spine.yaml` (`ices` metadata `thin`, and the `/shape-slice` fill rule), `core/components/memory/standards/schemas/product-os/slice.yaml` (its header and fill rule), `core/components/plays/create-play/references/check_ice_workable.py` and its test `test_check_ice_workable.py`, the copy `core/components/plays/discover-intent/scripts/check_ice_workable.py`, `core/components/plays/shape-slice/` (follows in its `/edit-play` change), and the plan play and the eval play (not built yet)
**ICE impact:** The product ICE keeps its three parts (ADR 047). It gains one optional mark, thin: the Thin line on its page and `thin: true` in its spine entry's metadata. `/shape-slice` sets the mark; the play that deepens the ICE removes it. Each line of an ICE has one reader: `/shape-slice` reads the "Fails if" lines and writes the hidden file; the plan play reads every other line and writes the story. The ready check changes: the thin mark gives "partly ready" with the gap "thin ICE"; one mark without the other is a drift gap; the light/full richness report is removed. The ICE of `/shape-slice` changes in meaning when it is rebuilt with `/edit-play`. The plan play and the eval play get their ICE when they are built. No play's ICE source changes with this ADR.
**Business intent check:** none — ontology v11 does not change the Business Intent kind (it changes the Slice, ICE, Plan, Epic and Story kinds), and no page in `.garura/product/product-os/intents/` changes on #846
**Related:** ADR 047, ADR 048, ADR 049, #788, #844, PR #845, #846, PR #849

## Context

ADR 049 put the shaping work in three plays, one after the other: `/shape-slice`, the plan play, the eval play. It gave the plan play the slice's hidden file (`failure-and-recovery.md`): one entry for each story, with its failure conditions and one recovery condition for each.

The first real `/shape-slice` run (#844, PR #845) showed a problem. The stories do not exist when the slice is shaped. A hidden file keyed by story cannot be written until the plan play runs. The product owner then decided two things (#844, decisions 6 and 7). First, the plan only plans: it must not write failure conditions. Second, when a part the slice needs has no ICE, `/shape-slice` proposes one and warns the person; it never forces the person back to a discovery play.

Ontology v11 (#846, PR #849) records these decisions. The product owner agreed it at the three `/edit-ontology` checkpoints. The review of PR #849 (DF-1, DF-2) found that ADR 049 and ADR 047 still say the old thing. This ADR brings them in line with v11.

Notes from the ADR keeper:

- The brief names ADR 049 Decisions 1.2, 4 and 5. ADR 049 §1.1 also says the old thing: "/shape-slice … writes nothing else". Under v11, `/shape-slice` also writes a thin ICE and the hidden file. So §1.1 is amended too.
- ADR 047 §8 says the richness of an ICE "is assessed and reported". Under v11 the ready check removes the richness report. So that line of §8 is amended too.
- ADR 048 §3 (a story writes its scope of work from two ICE) still holds: v11 says every line except "Fails if", and ADR 049 already took those lines out of the story. ADR 048 is not amended.

## Decision

### 1. `/shape-slice` writes the slice's hidden file

`/shape-slice` writes the slice's hidden file when it shapes the slice. The file has one entry for each feature of the slice. Each entry is written from the feature's ICE and its capability's ICE, by `standards/rules/expectation-generation.md`: exactly one recovery condition for each "Fails if" line. When one of the two ICE is thin, the entry says so. When the slice gains a feature, `/shape-slice` adds that feature's entry.

`/shape-slice` makes the eval folder `.garura/project/plans/<plan-id>/evals/<slug>/` in the home plan's folder, also when no plan file exists yet. It still writes no plan, no epic, no story and no eval.

### 2. The plan play only plans

The plan play writes only the plan file, the epic and the stories. It writes nothing in the evals folder.

### 3. The epic keeps the feature-to-story map

The epic keeps the map from each feature to its story. The eval play uses this map to join each hidden-file entry to its story.

### 4. Each line of an ICE has one reader

`/shape-slice` reads the "Fails if" lines and writes the hidden file from them. The plan play reads every other line and writes the story's scope of work and Context guidance from them. So each line of an ICE has one interpretation.

### 5. A part with no ICE gets a thin ICE

When a part the slice needs has no ICE, `/shape-slice` proposes a thin ICE from the person's answers. A thin ICE has at least:

- in Intent: a goal, a limit and one "Fails if" line;
- in Context: one line;
- in Expectation: one line.

`/shape-slice` marks it thin in two places that agree: a Thin line at the top of its page, and `thin: true` in its spine entry's metadata. It warns the person that a thin ICE can cause problems later and that `/discover-capabilities` can deepen it. It never sends the person back, and nothing stops. The play that deepens the ICE removes both marks.

### 6. The ready check reads only the thin mark

A thin ICE is "partly ready", with the gap "thin ICE". Work starts, and the gap is listed. When only one of the two marks is there, the check lists a drift gap. The check counts no lines and judges no richness. An ICE with few lines and no mark is not thin; the product owner judges its depth.

### 7. When an ICE changes, two plays act in the same round

When an ICE changes after its story and its hidden-file entry are made, both are drift for the Alignment loop. In the same Alignment round, the plan play makes the story again and `/shape-slice` makes the entry again, from the same two ICE.

### What this changes in older ADRs

- **ADR 049 §1.1** — amended. `/shape-slice` also writes a thin ICE for each part the slice needs that has no ICE, and the slice's hidden file. It still writes no plan, epic, story or eval.
- **ADR 049 §1.2** — amended. The plan play does not make the hidden file.
- **ADR 049 §4** — amended. The plan play does not read all of each ICE; it reads every line except "Fails if". `/shape-slice`, not the plan play, writes the hidden file, one entry for each feature, not for each story. "Made again together" now means: in the same Alignment round, by two plays.
- **ADR 049 §5** — amended. The rule section is "A feature's recovery (product ICE)", and `/shape-slice` writes it. ADR 049's Affects and References name the old section "A story's recovery (product ICE)".
- **ADR 049, Consequences** — "Each ICE is interpreted once, by the plan play" now reads: each line of an ICE is interpreted once, by its one reader.
- **ADR 047 §6** — amended. Partly ready also covers the thin mark, which is on the ICE itself, not outside its parts.
- **ADR 047 §7** — amended in its words only. A present part is still enough to start; the check now also counts no lines.
- **ADR 047 §8** — amended. The ready check no longer assesses or reports richness. The only depth signal it reads is the thin mark.

### What this does not change

- ADR 049 §2 (one plan for each business intent) and §3 (where the eval, the hidden file and the usage guide live). The read rules for the builder and the running eval, and the handoff plan.
- ADR 047 §1–§5, the not-ready rule, the business intent as the gate, and no separate approval for an ICE.
- ADR 048 and ADR 017.
- The routing table in `docs/philosophy/idd-principles.md`.
- No person's business intent.

## Consequences

### Positive

- `/shape-slice` does not stall. The hidden file is keyed by feature, and the features exist when the slice is shaped.
- The plan play only plans and writes no failure condition, as the product owner said.
- Each line of an ICE has one interpretation. The hidden file and the story cannot read the same line in two ways.
- A person is never sent back for a missing ICE. The slice is shaped, the person is warned, and the gap is listed.
- The ready check stays mechanical: one mark, no line counts, no judgment.

### Negative / Risks

- Work can start on a thin ICE. A poor outcome from it is on the person who wrote it (ADR 047 §8 stands on this).
- The thin mark is in two places. When only one is there, it is drift; the check reports it, but the Alignment loop must fix it.
- The join from a hidden-file entry to its story depends on the epic's feature-to-story map. A missing line in the map breaks the join for the eval play.
- Until `/shape-slice` is rebuilt with `/edit-play` and the plan play and the eval play are built, the plays and the ontology say different things.
- When an ICE changes, two plays must act in one Alignment round.

## Alternatives Considered

- **Keep the plan play as the writer of the hidden file (ADR 049 as it is)** — lost: the plan play would then write failure conditions, which the product owner said it must not; and the shaping would be split across two plays.
- **Key the hidden file by story, and have `/shape-slice` wait for the stories** — lost: the stories come after `/shape-slice`, so it would stall.
- **A thin ICE with Intent only, as a new reason for "partly ready" (decision 7 as first worded)** — lost: with no Context and no Expectation, the story has nothing to write from. The product owner chose one line in each part (checkpoint 1, C1; checkpoint 3, L1).
- **Force the person back to `/discover-capabilities` for a part with no ICE** — lost: the product owner said never force; warn instead (decision 7).

## Work This Creates

- `/edit-play` on `/shape-slice`: write the hidden file, one entry for each feature, and propose a thin ICE with its two marks and the warning.
- Build the plan play (the plan file, the epic with its feature-to-story map, the stories; nothing in the evals folder) and the eval play (it joins each entry to its story through the map).
- After acceptance: the forward pointers on ADR 049 and ADR 047.

## References

- `.garura/project/issues/_adr/20261024-adr846/brief.md` — the brief
- `.garura/project/issues/846/context/edit-ontology/decisions.json` — the three checkpoints, all agreed
- `.garura/project/issues/846/context/edit-ontology/draft-questions.md`, `draft-kinds.md`, `draft-links.md` — what the product owner agreed
- `core/components/memory/standards/schemas/product-os/ontology.md` — v11: the Slice, ICE, Plan, Epic and Story kinds; Q33, Q34 and Q36–Q40
- `core/components/memory/standards/rules/expectation-generation.md` — "A feature's recovery (product ICE)"
