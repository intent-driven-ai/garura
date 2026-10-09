# Trial — `/intent` on the token-burn dashboard (2026-10-08)

Source: `~/cto/token-burn-dashboard` — its written docs (README, SPEC and three more) and the
running app on port 3010, all four tabs (Overview, Models, Recipes, Tokens). Run inside Garura,
then removed (Kapil's choice). Kept here: `intent-draft.yaml` (the four intents), `answers.yaml`
(Kapil's words), `intent-check.json` (clean).

Ended by Kapil at the confirm step: "i think i am okay with trial. update /intent". Save, guard
and stop condition did not run on real data; the tests cover them.

## What happened, pass by pass

1. **A general agent stood in for the planned agent.** Kapil: a specific agent is needed. Built
   `business-intent-keeper` (the person's side), apart from `product-os-keeper` (the agents' side).
2. **One shallow intent.** The agent saw all four tabs but pressed them into one line. Cause: the
   play, skill and save script allowed one intent per run, though the ontology allows many.
   Fixed: one intent per separate thing, a coverage map, decide each intent.
3. **Ten intents.** Depth right. Kapil: "these dont sound like intent... intent will be deeper."
   The ten are what the person must see and decide — one level below a business intent.
4. **Kapil's four deep intents** — token economics; harness usefulness and agent autonomy;
   framework adoption across teams; collect the data across teams (only from Kapil, not in the
   dashboard — "the intent that i want to run with"). The ten map under the first three.
5. **Why and proof, one question at a time, with three examples each.** Examples helped: Kapil
   picked one once, adapted others. All eight answered; the check came back clean.

## Findings that change `/intent`

- **Two levels.** A source shows the lower level (what a person sees and decides); the business
  intent sits above it and mostly comes from the person. The lower level is what `/vision`
  needs to make capabilities and their ICE.
- **Stop rule and proof keep the upper level from being "anything".** Ask "why?" one level at a
  time; stop when the answer no longer names the product. A business intent with no provable
  proof fails.
- **An intent may come from the person alone** (intent 4). The check now allows it.
- **Qualities are limits, not intents.** "Stays current", "trusted", "safe to share" became
  must-nots.
- **Offer examples with each question**, and record when the person picks one (`chose`).
- **Each view keeps its text**, not only its picture (fixed in capture).
- **The agent returns only its contract** (fixed).
- **The check lists a missing property twice** (as a gap and as its question) — fixed 2026-10-09: one line per intent.
- **Two intents can share a measure** — the autonomy score proves intents 2 and 3.

# Re-run — two levels, unattended (2026-10-09, run 20261009-023928)

Kapil away, no questions asked. Same dashboard: five docs and all four tabs, each with its
picture and text. Kept in `rerun-20261009-023928/`: both drafts, both check reports, the replayed
answers, the guard report and the stop-condition verdict. All model and evidence output removed.

**Pass A — no answers.** The agent proposed 5 business intents with 12 ICE: where AI spend goes;
hand more work to AI steadily; the right model for the work; less steering from people; share
the numbers safely. Closer to Kapil's four than the first trial's ten; one "why?" above the
dashboard. It could not find framework adoption or collecting across teams (no source shows
them) and asked "is there an intent you hold that these sources do not show?" — the right move.

**Pass B — Kapil's recorded answers replayed** (his exact words; the examples he was shown;
two picked). Result: exactly Kapil's four intents, 13 ICE under them (token economics 9,
harness autonomy 1, framework adoption 2, collect across teams 1), 44 parts mapped, all eight
answers in his words, answers record clean.

**One new question for Kapil — still open:** "Today's written rules keep each person's numbers
private: no client or project names, no prompts, no file locations, and nothing sent anywhere
without the owner's go-ahead. A roll-up from each person to team, account and unit needs to
know who each person is and where they belong, and the workflow view already names projects.
What may the collected numbers carry?" A real run stops here (Step 3).

**Save path, on a SIMULATED confirmation** (labelled in the file, not Kapil's): 4 intent pages
and 13 ICE files (ICE shape, unplaced, built from their intent) written; every source names
every intent; no hand-off file. Guard ok (only new intent and ICE files). Stop condition held
(D1–D5). Scenario checks SCE-3, 6, 7, 8 pass.

## Findings from the re-run

- **Fixed:** an answer the person gives unprompted (Kapil's four intents) needs no examples —
  the check now accepts `volunteered: true`; the play says so.
- **Fixed:** the agent's file now tells it to check the answers record too.
- **Open — qualities still become items.** Pass A made "share safely" an intent and both passes
  kept "trust the numbers" as an ICE (11 parts mapped to it), though the skill says qualities
  are limits. The skill rule is not strong enough.
- **Open — a new agent does not load mid-session.** Installing the agent file did not make it
  callable until later; Pass A ran on a general agent given the agent file as is.
