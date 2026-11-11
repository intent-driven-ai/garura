# Feature: Work out the plans a plan waits on

## What it does
Each plan's Waits on list is worked out from the needs of its parts in the product model, never set by hand: a plan waits on another plan when a feature in it belongs to a capability that needs a capability whose features are in that other plan. So the order of the work across plans comes from the model, and every view, the removal of a plan and the choice of the next item read a list that is true.
- How it is worked out, from the plan side, because the model never names a plan:
  - each feature the plan holds, found by the mark on the story that stands for it;
  - the capability each of those features belongs to;
  - each capability that capability needs, read from the model's index;
  - each other plan that holds a feature of a needed capability.
- The list is written in the plan file's Waits on field, `needs_plans`, and nowhere else. A plan that no need explains any more leaves the list. Nothing is written in the model or the tracker.
- A plan file is changed where the plan's own rules say: on the plan's own branch while its work is in progress.
- Two plans that need each other: both are named, with the needs that join them. Nothing is stopped: no session, no view and no landing waits on it.
- It orders the work and holds nothing back. A plan's branch still lands on main when the plan pauses, whatever the plan waits on.
- The needs links it reads sit in the model's index. Today their field there is still `depends_on`; "Needs" and "identified by" link capabilities and features (fn-725) renames it `needs`.
- Outside Garura, a tracker can hold the same kind of link: "GitHub issues can be marked as blocked by, or blocking, other issues". Whether the plans' epics get such a link is not decided.
- The list it writes is read by the card of every plan, by the tree of one plan, by the removal of a plan, and by the choice of the next item.
- Examples, in different kinds of project:
  - In a bank's payments service, the plan for new statements holds the feature for downloading a statement. Its capability needs the capability for reading account data, whose features are in the plan for the account data feed. So the statements plan's Waits on reads the feed's plan.
  - In a logistics app, the plan for parcel tracking waits on the plan for carrier links. When the need between the two capabilities is taken out of the model, the next working out takes the carrier plan off the list.
  - In a clinic's booking app, the plan for reminders and the plan for self-booking come to need each other. Both plans are named with the needs that join them, and the product owner's session on reminders still lands.
- How it meets the capability: "sees every plan and where it stands" includes what each plan waits on, and that is true only when the list comes from the model's needs and not from a hand edit.

Status: not built. No issue is filed for it. The plan file's list is read by /list-plans, /show-plan and the removal of a plan, and it is written by no step. The needs links it reads come with #725 ("Needs" and "identified by" link capabilities and features), whose feature is proposed in the model, so the index's field is still `depends_on`.

## Inputs / Outputs
- In: every plan file in the plans folder: each plan's id and tree, with the mark on each story that names the feature it stands for.
- In: the product model's index: each feature's capability, and the needs of each capability.
- Out: each plan file's Waits on list, as worked out, in the plan file only.
- Out: a note that names two plans that need each other, with the needs that join them.
- Out: nothing in the product model and nothing in the tracker.

## Rules & behavior
- Worked out, never set by hand. The reason: "The other plans it needs — worked out from its features' capabilities' needs, never set by hand", and "The plan plays find the needs of a plan from the needs of its nodes. Nobody sets them by hand."
- From the needs of a feature's capability. The reason: "It needs another plan when a feature in it belongs to a capability that needs a capability whose features are in that plan."
- A feature is found by its story's mark, never by a title. The reason: "a play finds the Story of a Feature by the `represents` mark only".
- From the plan side, and written only in the plan files. The reason: the model never names a plan: "Plans sit outside the model and come and go, so no model page may depend on one."
- It orders the work and holds back no landing. The reason: "the link gives the order of work, not a gate on landing", and "Plan order (`needs_plans`) no longer holds a plan off main."
- Two plans that need each other are named, and nothing stops. The reason: "Two plans that need each other are one plan.", and Orchestration's Must not: "Stop a person. Every gate has a way past it that records what's owed."
- A plan file changes only where the plan's rules allow. The reason: "While its work is in progress, a plan has its own branch, `plan/<id>/base`, and the plan changes only there."
- Not decided: whether a plan's Waits on is worked out from its parts' needs, set by a person, or dropped.
- Not decided: when it is worked out: at each landing that changes a plan's items, each time a plan is shown, or on request.
- Not decided: whether a feature's own needs count too, as the page of fn-725 says, or only the needs of its capability, as the ontology says.
- Not decided: when two plans need each other, whether the two plans are merged into one or one need is dropped, and who does it.
- Not decided: whether the tracker also shows the list, as a blocked-by link between the plans' epics.

## Acceptance criteria
- Given plan A, which holds a feature whose capability needs a capability whose features are in plan B, when the plans a plan waits on are worked out, then A's Waits on reads B, and nothing in the model or the tracker changed. This is not built.
- Given a plan whose Waits on names a plan that no need explains, when it is worked out, then that plan is no longer in the list. This is not built.
- Given two plans whose features' capabilities need each other, when it is worked out, then both plans are named with the needs that join them, and a session on either plan still lands. This is not built.
- Given a plan that waits on a plan that is not Done, when the plan pauses and its branch is raised to main, then its Waits on holds nothing back. This is not built.
- Given the same plan files and the same model, when it is worked out twice, then the two lists are the same. This is not built.

## Out of scope
- The needs links on capabilities and features, and their name in the model's index. Product model owns them: "Needs" and "identified by" link capabilities and features (fn-725).
- Showing what a plan waits on. See every plan and where it stands (fn-729) and See one plan as a tree (fn-628) do it.
- Refusing to remove a plan that another plan needs. Remove a plan on a person's approval (fn-remove-plan) does it.
- When a plan's branch lands on main. Ship every change the same way, in Developer tooling, owns it.
- Choosing which item is worked next. Choose which item is worked next (fn-choose-next-item) will do it; it is not built.
- Writing a link in the tracker. Track execution in the team's tracker, in Orchestration, owns it.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/capabilities.md: "A person chooses what is delivered next as a slice, sees every plan and where it stands, and sets the order and status of the work as it runs."
- .garura/product/product-os/intents/bi-9.md: "Stop a person. Every gate has a way past it that records what's owed."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "The other plans it needs — worked out from its features' capabilities' needs, never set by hand", "It needs another plan when a feature in it belongs to a capability that needs a capability whose features are in that plan.", "Two plans that need each other are one plan.", "a play finds the Story of a Feature by the `represents` mark only", "While its work is in progress, a plan has its own branch, `plan/<id>/base`, and the plan changes only there."
- .garura/product/product-os/features/fn-725/feature.md: "Its field is still `depends_on`.", "A need that names a node in a different plan makes this plan need that plan.", "The plan plays find the needs of a plan from the needs of its nodes. Nobody sets them by hand.", "To fix it, drop one need, or merge the plans of the nodes into one plan."
- docs/adr/060-a-plans-branch-merges-into-main-when-the-plan-pauses.md: "the link gives the order of work, not a gate on landing", "Plan order (`needs_plans`) no longer holds a plan off main."
- docs/adr/065-the-models-index-is-changed-through-two-skills-the-model-never-names-a-plan-and-only-tools-know-the-tracker.md: "Plans sit outside the model and come and go, so no model page may depend on one."
- standards/templates/plan-view.md, in Phoenix memory: "each plan it needs, with its title; blank when none."
- core/components/skills/remove-plan/SKILL.md: "A plan that stays and names a plan being removed in `needs_plans`"
- 1021/context/answers/bi9-waits-on.md, in short-term memory, from memory update mu-20261110-011, approved by the product owner on 2026-11-10: "GitHub issues can be marked as blocked by, or blocking, other issues"
- The stock-take of Orchestration, .garura/project/issues/1021/context/bi-9-inventory/inventory.md, section 1.9: "Nothing is filed for choosing what is built next, a view across every intent, writing the branch field on a pause, or working out `needs_plans`."
