# Feature: Rename the change, plan, knowledge and record plays to the standard

## What it does
The plays that open, check and land a change, the plays that make and show a plan, the knowledge plays and the play that records a decision are renamed to the naming standard in force in one batch, with every reference to them, so a person types one kind of name for every play.
- Built under ADR 046, these plays took their new names:
  - `review-change` became /check-change, `refactor` /refactor-code, `adr` /record-decision, and `focus` /list-focus-issues;
  - the two knowledge plays, `build-knowledge` and `review-knowledge`, were later removed with no successor, because "the knowledge step is a step of the loop, not a play" (ADR 059);
  - the plan plays took the plan verbs: /show-plan, /update-plan and /list-plans; the play that makes a plan is /shape-plan, and no /draft-plan was built;
  - the change plays /start-change, /commit-change, /propose-change, /merge-change and /fix-bug already fit the change verbs.
- The old page said "next and focus stay one word". Neither did: /next was dropped (ADR 051), and `focus` became /list-focus-issues because "`focus` becomes `list-focus-issues` (Claude Code has `/focus`)".
- Under ADR 066, decided and not applied: /check-change becomes /validate-work, /refactor-code /refactor-work, /fix-bug /fix-work, /record-decision /design-adr, /update-plan /reshape-plan, /show-plan /view-plan and /list-focus-issues /list-issues; /shape-plan and /list-plans stay; /view-issue is new. The change plays /start-change, /commit-change, /propose-change and /merge-change become /start-work, /commit-work, /review-work and /merge-work, and "Their final place is still open."
- Approved pages wait on it: the rename to /list-issues is handed here by See the issues worth attention now.
- Examples, in different kinds of project:
  - In a bank's payments service, the team renames its play that reviews a change to the name its rule gives, and every guide, script and setting key that named the old play changes in the same batch.
  - In a clinic's booking app, the team drops its one-word play `/today`, which the coding tool may take for its own, and names it by the rule.
  - In a harness repository, ADR 066 renames the plan plays to the orchestrator's verbs, `reshape` and `view`, after the reviews.
- How it meets the capability: the plays people type most each day follow the one rule.

Status: built, under ADR 046, by #744 (rename the change, plan, knowledge and record plays, closed), landed in PR #749, which published the standard. Not built, or open:
- ADR 066's names for this family are decided and not applied; the rename runs after the reviews of BI-10 and BI-11, as one change.
- The final place of the four change plays is open, and so is the name for /release-increment.
- A project's learned gate policies are kept by play name, so they start again under each new name.

## Inputs / Outputs
- In: the rename map's lines for this family, and the agreed new names.
- In: every reference to the old names, the setting keys named after plays included.
- Out: the plays under their new names, with every reference changed and each ICE changed in wording only.
- Out: the old-name check's report, with none of this family's old names left.

## Rules & behavior
- Names and references only. The reason: "Names and references only: no behaviour changes."
- No play keeps a one-word name. The reason: keeping one word as an exception means "Two rules to learn and to teach".
- A removed play stays in the map with no new name. The reason: "`null` keeps the old name caught by the old-name check; the install has no new name to lay."
- A setting keyed by a play's name changes with it, and a learned policy starts again. The reason: "a project's learned policy for a renamed play starts again under the new name."
- ADR 066's rename is one change. The reason: "The rename, as one change".
- Not decided: the final place of /start-work, /commit-work, /review-work and /merge-work.

## Acceptance criteria
- Given ADR 046's rename, when the old-name check runs, then it finds none of `review-change`, `build-knowledge` or `review-knowledge`, and no `/adr` or `/focus` command.
- Given a setting keyed by a renamed play, when the rename lands, then the key carries the new name.
- Given ADR 066's rename has landed, when a person types /list-issues, then the play that was /list-focus-issues runs. This is not built.
- Given ADR 066's rename has landed, when the old-name check runs, then it finds no use of /check-change, /update-plan, /show-plan or /record-decision. This is not built.

## Out of scope
- The rule the names follow. Name every part by one rule, with five roles owning the verbs (fn-736) does it.
- The rename map and the check. Map every old name to its new one, and check that no old name is left (fn-741) does it.
- What the change plays do. Ship every change the same way, in Developer tooling, owns it.
- What the plan plays do. Orchestrate agent work through planning, in Orchestration, owns it.
- Taking out the old names in a project. Take out the parts Garura renamed or dropped (fn-748), in Upgrade a project, does it.

## Sources
- .garura/project/issues/1021/context/capabilities.md, line 118, the product owner's answer 7: "ADR 066's rename runs after the BI-10 and BI-11 reviews"
- core/components/memory/standards/rules/rename-map.yaml, lines 21-27 and 32: "the knowledge step is a step of the loop, not a play", "`null` keeps the old name caught by the old-name check; the install has no new name to lay."
- core/tools/naming/apply_renames.py, line 12: "Names and references only: no behaviour changes."
- docs/adr/046-one-naming-standard-for-every-harness-part.md, lines 50-51, 96-97 and 105: "`focus` becomes `list-focus-issues` (Claude Code has `/focus`)", "a project's learned policy for a renamed play starts again under the new name.", "Two rules to learn and to teach"
- docs/adr/051-the-next-play-is-dropped-the-plan-is-the-work-list.md: /next is dropped
- docs/adr/066-names-say-who-does-the-work-five-roles-own-the-verbs.md, lines 73, 83 and 149: the name for /release-increment is open, "Their final place is still open.", "The rename, as one change"
- .garura/project/issues/1021/context/names.md, lines 9, 12-19 and 26-27: the agreed new names of this family
- .garura/product/product-os/software-delivery-planning/track-execution/fn-see-issues-worth-attention/feature.md, line 66: "The plays' names, and the rename to /list-issues."
- .garura/product/product-os/features/fn-744/feature.md, the old page, lines 4 and 8: "the planned plan plays take draft-plan, show-plan, update-plan, list-plans", "next and focus stay one word."
- GitHub #744 (closed): "Rename the change, plan, knowledge and record plays"; PR #749 (merged)
- The stock-take, .garura/project/issues/1021/context/bi-10-inventory/inventory.md, section 8
