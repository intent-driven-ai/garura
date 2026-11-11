# Feature: Let the changes the product owner allows go ahead on their own, and show each one with a way back

## What it does
The product owner sets, in the project's settings, which kinds of change may go ahead on their own; a change of such a kind that rests on a clear want of the product's own consumers goes ahead without waiting for his yes, and is shown to him at once, with its findings and items, waiting for his review, and with a way back, so that the work he trusts the agent with is done for him and nothing changes without him seeing it.
- The setting names, for each kind of change, one of two values: recommend, which every kind starts with, or go ahead on its own.
- Some kinds can never be set to go ahead on their own: a new business intent; new words, proof, must-not or stage on an intent; retiring or replacing an intent; new words on a page that exists; and taking any part out.
- The one kind proposed as ever allowed is a new feature under a capability that already serves a confirmed intent. A confirmed intent is a business intent that a person has confirmed says the right thing; work starts only from one.
- A change of an allowed kind goes ahead on its own only when all of these hold:
  - it rests on at least one want of the product's own consumers that is not weak;
  - no finding it rests on goes against an intent;
  - it rests on more than what competitors are doing.
- Going ahead means it is handed to its owning part through Start each change down the path that builds it, through the part that owns each step (fn-start-changes), without a yes from this capability, marked as set going by this capability and waiting for review. Each owning part keeps its own rules, and today each asks a person before it writes, so the change meets the product owner there.
- He sees each one at once, apart in the list of recommendations: what changed, where, the findings and items it rests on, and how to take it back.
- To take it back, he turns it down. Before it is built, it is taken back through the part that made it, such as a feature removed from the model with his name, or its work items dropped. Once it is built, taking it back is a new change, which he decides.
- Setting a kind back to recommend stops every further change of that kind at once.
- Beside the setting he sees how he answered the changes of each kind: how many he approved as they were, changed or turned down. He widens or narrows the setting on that record.
- What it does, for example, in different kinds of product: for a clinic's booking app with new features allowed, a feature for evening appointments goes ahead under the booking capability and he sees it the same day; for a team's planning tool, a calendar view wanted only because a rival has one stays a recommendation; for a recipe app, a want that rests on two posts stays a recommendation, because it is weak.
- How it meets the capability: the product owner asked for this work "automatically, or at least making those recommendations", and for "an autonomous kind of agent running that goes back and does this thing for me."; this is the half that goes ahead, and only as far as he allows.

Status: not built. No setting says which kinds of change may go ahead on their own, and no part writes the model on this capability's word. What exists covers only patterns for it:
- The plays' checkpoint settings can learn from a person's answers which kinds of change pass without waiting: "Any rejection, requested edit, or correction resets the shape to gated.", and a person can pin a kind for good, "the human's permanent pin". Phoenix memory pins the checkpoint of the old, stale learning play: "a wrong model learning bends the product model".
- Add a feature found during work writes the model only after the person's "approved", and the planned thin page for a part found during work asks to "Approve the page before it is written, as with any model write." (#979).
- The planned way for the model to move with the work marks each piece it changes "in review, not approved; a person approves it later." (#990).

## Inputs / Outputs
- In: the project's setting for which kinds of change may go ahead on their own.
- In: each change, with its findings, from Work out the change each finding calls for, with why and how sure (fn-propose-changes).
- In: the product owner's earlier answers, for the record beside the setting.
- Out: each change that goes ahead on its own, handed to Start each change down the path that builds it, through the part that owns each step (fn-start-changes), marked as set going by this capability and waiting for review.
- Out: each such change, shown at once to the product owner with its findings, items and way back.
- Out: each change that may not go ahead, for Recommend each change to the product owner, and keep his answer (fn-recommend-changes).
- Out: the record of his answers by kind of change, shown beside the setting.

## Rules & behavior
- Nothing goes ahead on its own until he allows its kind. The reason: his words put recommending as the least, "or at least making those recommendations", and a design note holds that "resolution is owned deliberately, at a level of autonomy someone chose, and never assumed by default."
- Some kinds never go ahead on their own. The reason: Run → Product must not "Change an intent, or promote memory, without a person."; "Only a person confirms or drops it; an agent never does."; and Specify against what exists already holds that "nothing existing changes on its own".
- Only on a clear want of the product's own consumers. The reason: "a weak finding shown as strong sends the next capability after the wrong change"; a finding against an intent is the product owner's to settle; and a rival's move says what another product does, not what this product's consumers want.
- Shown at once, waiting for review. The reason: "Skips are always visible in evidence — a silent gate is not a gate."
- A way back for each. The reason: memory's learning on agents that act on their own keeps them away from what cannot be undone, "Not for irreversible, high-consequence actions".
- Setting a kind back stops it at once. The reason: how far the agent goes is the product owner's choice, so taking it back must work at once; memory's guardrails for agents name "A kill switch." for the same reason.
- Each owning part keeps its own rules. The reason: "Each fix is made by the part that owns it", and Turn intents into agent work holds that "Nothing reaches the tracker, the plan file or the model before the product owner's typed yes".
- His record sits beside the setting. The reason: memory's learning on agents that suggest keeps what was suggested and what the person did as "the data that later justifies (or denies) more autonomy".
- Not decided: whether a kind can earn going ahead on its own from his answers, the way the plays' checkpoint settings learn, or only by his word in the setting.
- Not decided: whether the owning parts may write a new feature on this capability's word, marked waiting for review. Today they write the model only after a person's yes, and the change is theirs to make.
- Not decided: whether other kinds may ever be allowed, such as making the work items of an allowed feature without the product owner's typed yes in Turn intents into agent work. That changes that part's rule, and depends on Orchestrate agent work through planning, which is not yet reviewed.
- Not decided: whether the pinned checkpoint of the old learning play binds this capability.

## Acceptance criteria
- Given no kind allowed in the setting, when a strong want calls for a new feature, then it becomes a recommendation and nothing goes ahead.
- Given new features allowed under capabilities that serve a confirmed intent, and a strong want placed on such a capability, when the change is worked out, then it is handed to its owning part, marked as set going by this capability and waiting for review, and the product owner sees it at once with its findings and a way back.
- Given the same setting and a want that is weak, against an intent, or resting only on what a rival does, when the change is worked out, then it becomes a recommendation.
- Given any setting, when a change would add a business intent, change an intent's words or stage, retire a part or change a page that exists, then it becomes a recommendation.
- Given he sets a kind back to recommend, when the next change of that kind comes, then it becomes a recommendation.
- Given he turns down a change that went ahead on its own before it was built, when it is taken back, then the record shows both the change and its taking back.

## Out of scope
- Working out the changes. Work out the change each finding calls for, with why and how sure (fn-propose-changes) does it.
- Making the change. The part that owns it does, through Start each change down the path that builds it, through the part that owns each step (fn-start-changes).
- Where the project's settings live. The review of Settings, in Standards, structure, settings and memory, owns it.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/bi-6-capability-3/page-approvals.md, spelling tidied: "start building features into the product or start updating the product intent model automatically, or at least making those recommendations", "an autonomous kind of agent running that goes back and does this thing for me."
- The capability list the product owner agreed on 2026-11-03, in .garura/project/issues/1021/context/capabilities.md: "Settings: Everything that can be turned on or off lives in settings."
- .garura/product/product-os/intents/bi-6.md: "Change an intent, or promote memory, without a person."
- .garura/product/product-os/software-delivery-planning/understand-consumers-and-competition/capability.md: "a weak finding shown as strong sends the next capability after the wrong change"
- .garura/product/product-os/software-delivery-planning/specify-product/fn-specify-against-existing/ice.md: "Limit: A person decides any clash, and nothing existing changes on its own."
- .garura/product/product-os/software-delivery-planning/keep-spec-matched/capability.md: "Each fix is made by the part that owns it"
- .garura/product/product-os/software-delivery-planning/turn-intents-into-work/capability.md: "Nothing reaches the tracker, the plan file or the model before the product owner's typed yes"
- .garura/product/product-os/software-delivery-planning/turn-intents-into-work/fn-add-found-feature/feature.md: "The model is written only through the model's own skills, never by hand, and only after "approved"."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "Only a person confirms or drops it; an agent never does."
- standards/rules/gate-config.md, in Phoenix memory: "Any rejection, requested edit, or correction resets the shape to gated.", "the human's permanent pin", "a wrong model learning bends the product model", "Skips are always visible in evidence — a silent gate is not a gate."
- knowledge/architecture/agent-supervised-autonomous.md, in Phoenix memory: "Not for irreversible, high-consequence actions"
- knowledge/architecture/agent-assistive.md, in Phoenix memory: "data that later justifies (or denies) more autonomy"
- knowledge/architecture/agentic-guardrails-baseline.md, in Phoenix memory: "A kill switch."
- docs/philosophy/intent-and-adlc.md, a design note marked "designed, not in force": "resolution is owned deliberately, at a level of autonomy someone chose, and never assumed by default."
- GitHub #979 (open): "Approve the page before it is written, as with any model write."
- GitHub #990 (open): "Each piece it changes is marked in review, not approved; a person approves it later."
