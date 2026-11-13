# Feature: Choose the model and effort by the job at run time

## What it does
At run time, a router reads what a step must do and chooses its model and effort, so a simple step runs fast and cheap and a hard step runs on a strong model, in place of the fixed tier its maker wrote; it comes only once the records of runs show it pays.
- It is the product owner's answer, as recorded: "a run-time router comes later only if the records show it pays". Until then, each part runs on the tier its maker or its project names.
- Today nothing picks a model or an effort from what a step must do; each part keeps the tier its maker wrote, and no issue plans a router.
- The memory page on choosing a model for each step names the gain a router is for: "Route, don't over-provision.", and "call the frontier model only for the steps that need it". It is written for agents built into a product, and is the basis of the answer the product owner took as yes.
- What would show it pays comes from the record of each part's runs, and from the moves made on it.
- Examples, in different kinds of project:
  - In a shop's support desk, a router sends a short order-status reply to a fast model at low effort, and a refund dispute to a strong model at high effort.
  - In a law firm's contract review, the records show a router would save little, and every step stays on the tier its maker wrote.
  - In a game studio's build, a router lowers the effort for a step that only renames asset files, and keeps a strong model for the step that plans a level.
- How it meets the capability: "the right model and effort for its job" is chosen step by step, for the job in front of it, once the records show this pays more than a fixed tier.

Status: not built. It comes later, only if the records show it pays. Not built, or open:
- No router, and no record yet to show whether one pays (Record each run's model, effort, time and cost for each part, fn-record-run-cost).

## Inputs / Outputs
- In: what a step must do.
- In: the step's tier from its source or its project's settings.
- In: the records of runs that show a router pays.
- Out: the model and the effort the step runs on, with the router's choice in the run's record.

## Rules & behavior
- A router comes only after the records show it pays. The reason, in the product owner's answer as recorded: "a run-time router comes later only if the records show it pays".
- No step runs on a stronger model than its job needs. The reason: "Route, don't over-provision."
- Not decided: what "pays" means: which saving in time or tokens, against which loss of quality, is enough.
- Not decided: what the router reads to judge a step's job, and whether it may choose a tier above the one the part's maker wrote.
- Not decided: on which coding tools a choice made at run time can take effect.

## Acceptance criteria
- Given the records of a month of runs, when a person weighs a router, then the records show the time and the tokens it would save, before any router is built. This is not built.
- Given a router in place and a step that only formats output, when the step runs, then it runs on the fast tier and the run's record names the router's choice. This is not built.
- Given records that show no gain, when a person weighs a router, then none is built and each part keeps its tier. This is not built.

## Out of scope
- The fixed tier and effort each part's maker writes. Give each part a model tier and an effort by a written rule (fn-tier-by-rule) does it.
- The record a router's case rests on. Record each run's model, effort, time and cost for each part (fn-record-run-cost) does it.
- Carrying a chosen model into each coding tool. Support each coding tool, in Install and distribute, owns it.

## Sources
- The product owner's answer 4 as recorded on 2026-11-11: "a run-time router comes later only if the records show it pays"
- knowledge/technology/agent-model-selection.md, in Phoenix memory, read through the memory tool, line 31: "Route, don't over-provision."; line 32: "call the frontier model only for the steps that need it"; lines 4-8: its conditions, an agentic feature on Bedrock or Vertex
- The stock-take (2026-11-11), section 6.4: "Nothing picks a model or an effort from what a step must do"; and the proposed answer the product owner took as yes: "A run-time router comes later, if the records show it pays."
- GitHub, a search of the open issues on 2026-11-11 for model tier, effort, Sonnet, Opus, Haiku and routing: no issue plans model choice
