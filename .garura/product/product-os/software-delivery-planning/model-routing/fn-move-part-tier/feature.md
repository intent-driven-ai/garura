# Feature: Move a part up or down a tier on that record, and check the move with an eval

## What it does
When the record of its runs shows a part is slow or costly for a simple job, or falls short on a hard one, a person moves the part down or up a tier, and an eval checks that the part still does its job on the new tier before the move lands, so each part's tier follows what its runs show.
- It completes the product owner's answer on who chooses a part's model: each run records what each part ran on and cost, "so a person can move a part up or down".
- The memory page on choosing a model for each step says when and how: "re-route that step up or down" when a step on a small model "starts failing (inputs got harder)", or a step on a large model "became routine"; and "Re-run evals on any model change.", because a model swap is "a behavior change that must pass the eval suite". That page is written for agents built into a product on a cloud platform with a range of models, not for Garura's own parts; it is the basis of the answer the product owner took as yes.
- After a move in a part's source, the next install lays the new tier: Support each coding tool says, "Given a part whose source tier is changed by Intelligent model routing, when Garura is installed again, then the new tier is laid."
- The evals there are today: each play compiled by /create-play holds step evals and scenario evals, and the rebuild eval tests what the Discovery loop made from a prototype. No rule says which of them checks a move, and no rule says when a part moves.
- Examples, in different kinds of project:
  - In a bank's payments service, the record shows a skill that only formats a report runs on `opus`; a person moves it to `haiku`, the skill's eval passes on `haiku`, and the move lands.
  - In a hospital's appointment system, the record shows the sub-agent that sorts referrals fails one case in five on `sonnet`; a person moves it to `opus`, and its eval now passes every case.
  - In a news site's publishing tool, a person moves the headline skill down to `haiku`, its eval fails on two headlines, and the skill keeps `sonnet`.
- How it meets the capability: a part stays "on the right model and effort for its job" only when its tier moves as its job and its runs change.

Status: not built. Not built, or open:
- No rule says when a part moves up or down, or who moves it.
- No eval is named to check a move, and nothing runs one when a tier changes.
- The record a move rests on is not built (Record each run's model, effort, time and cost for each part, fn-record-run-cost).

## Inputs / Outputs
- In: the record of the part's runs: its model, effort, time and cost.
- In: the part's eval, and the tier the person moves it to.
- Out: the part on its new tier, once its eval passes on it.
- Out: the move's record: the part, the old and the new tier, the runs it rests on and the eval's result.
- Out: the part on its old tier, when the eval fails.

## Rules & behavior
- A person moves a part, on the record of its runs. The reason: the answer the product owner took as yes, "so a person can move a part up or down".
- Every move is checked by an eval before it lands. The reason: "Re-run evals on any model change."
- A part moves both ways: down when its job proves simple, up when it falls short. The reason: "re-route that step up or down".
- Not decided: whether a move is made in the part's source, by its maker, or in the project's settings, by the team.
- Not decided: which eval checks a move: the play's own step and scenario evals, the rebuild eval, or an eval made for the move.
- Not decided: what on the record calls for a move: a cost, a time, a failed run, or a mix of them.

## Acceptance criteria
- Given a skill whose record shows it runs on `opus` for a job that only formats output, when a person moves it to `haiku`, then the skill's eval runs on `haiku` and passes before the move lands. This is not built.
- Given a move whose eval fails on the new tier, when the eval ends, then the move does not land and the part keeps its tier. This is not built.
- Given a move that landed, when a person reads its record, then it names the part, the old and the new tier, the runs it rests on and the eval's result. This is not built.

## Out of scope
- The record a move rests on. Record each run's model, effort, time and cost for each part (fn-record-run-cost) does it.
- Laying the moved tier in each coding tool. Map each part's model tier onto each tool's own setting (fn-map-model-tier), in Support each coding tool, does it.
- The evals a compiled play holds, and building a play with them. Build your own harness, in Standards, structure, settings and memory, owns them.
- Opening and landing the change that holds a move. Ship every change the same way, in Developer tooling, owns it.

## Sources
- The capability list: "Taken as yes to the list and to each proposed answer"; the product owner's answer 4 as recorded on 2026-11-11: "each run records model, effort and cost per part"
- The stock-take of Standards, structure, settings and memory (2026-11-11), the proposed answer to question 4: "so a person can move a part up or down"; its basis: Phoenix memory's "Route, don't over-provision" and "Re-run evals on any model change"
- knowledge/technology/agent-model-selection.md, in Phoenix memory, read through the memory tool, lines 4-8: its conditions, an agentic feature on Bedrock or Vertex; line 35: "a behavior change that must pass the eval suite"; line 49: "starts failing (inputs got harder)"; line 50: "became routine", "re-route that step up or down", "Re-run evals on any model change."
- .garura/product/product-os/software-delivery-planning/support-coding-tools/fn-map-model-tier/feature.md, line 43: "Given a part whose source tier is changed by Intelligent model routing, when Garura is installed again, then the new tier is laid."
- core/components/plays/create-play/SKILL.md, lines 319-322: the step evals and the scenario evals of each compiled play
- core/tools/rebuild-eval/README.md, lines 1-12: the test of what a Discovery loop made from a prototype
- The stock-take (2026-11-11), section 6.4: "No rule says when."
