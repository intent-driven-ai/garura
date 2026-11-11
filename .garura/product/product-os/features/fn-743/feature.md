# Feature: Rename the harness plays and the loop to the standard

## What it does
The plays that build and install the harness, and the loop, are renamed to the naming standard in force in one batch, with every reference to them, so the parts that make the harness follow the same rule as every other part.
- Under ADR 046, built: `play-creator` became /create-play, `play-editor` /edit-play, `loop-creator` /create-loop and `loop-editor` /edit-loop, and the Discovery loop's command became /complete-discovery. /install-garura and /uninstall-garura already fit the harness verbs, and /edit-ontology uses the harness verb `edit`.
- The old page asked for `run-discovery`. It became /complete-discovery because "loops use `complete` (Claude Code has `/run`)".
- The rename tool did the work, "Names and references only: no behaviour changes.", and each renamed play's ICE changed in wording only: "Every ICE source that names a renamed part uses the new name, and its fingerprint is stamped again."
- Under ADR 066, decided and not applied: /create-play becomes /build-play, /edit-play /fix-play, /create-loop /build-loop and /edit-loop /fix-loop, the builder's verbs; /complete-discovery becomes /loop-product-spec; /edit-ontology becomes /specify-ontology; and /install-garura and /uninstall-garura stay, as product plays with no role.
- Examples, in different kinds of project:
  - In a bank's payments service, the team's harness renames the play that makes plays from `play-maker` to `create-play`. Every guide and script that named it changes in the same batch, and the old-name check finds none left.
  - In a clinic's booking app, the loop that runs the intake plays takes the loop name of the rule, and the plays it runs keep their own names.
  - In a harness repository, ADR 066 renames the builders to the builder role's verbs, `build` and `fix`, in one change after the reviews.
- How it meets the capability: the parts that build the harness are named by the same rule that the checks hold every part to.

Status: built, under ADR 046, by #743 (rename the harness plays and the loops, closed), landed in PR #749, which published the standard. Not built, or open:
- ADR 066's names for this family are decided and not applied. The product owner answered that the rename runs after the reviews of BI-10 and BI-11, as one change.

## Inputs / Outputs
- In: the rename map's lines for this family, and the agreed new names.
- In: every reference to the old names in the source, the docs, the installer and the guides.
- Out: the plays and the loop under their new names, with every reference changed and each ICE changed in wording only, with its fingerprint stamped again.
- Out: the old-name check's report, with none of this family's old names left.

## Rules & behavior
- Names and references only. The reason: "Names and references only: no behaviour changes."
- A renamed play's ICE changes in wording only. The reason: "Every ICE source that names a renamed part uses the new name, and its fingerprint is stamped again."
- A batch is done when the old-name check finds none of its names. The reason: "`core/tools/naming/check_old_names.py` fails while any old name is still used outside past records."
- A loop's name tells it apart from a play. The reason, under ADR 046: "`complete` is used by loops only, so a loop is told apart from a play at a glance."; under ADR 066: "Only a loop's name starts with `loop`."
- ADR 066's rename is one change. The reason: "The rename, as one change".

## Acceptance criteria
- Given ADR 046's rename, when the old-name check runs, then it finds none of `play-creator`, `play-editor`, `loop-creator` or `loop-editor`, and no `/discovery` command.
- Given a renamed play, when its ICE is compared with the one before the rename, then only the names changed.
- Given ADR 066's rename has landed, when a person types /build-play, then the play that was /create-play runs. This is not built.
- Given ADR 066's rename has landed, when the old-name check runs, then it finds no use of /create-play, /edit-play, /create-loop, /edit-loop or /complete-discovery. This is not built.

## Out of scope
- The rule the names follow. Name every part by one rule, with five roles owning the verbs (fn-736) does it.
- The rename map and the check. Map every old name to its new one, and check that no old name is left (fn-741) does it.
- Building and changing plays and loops with these plays. Build your own harness, in Standards, structure, settings and memory, owns it.
- Taking out the old names in a project. Take out the parts Garura renamed or dropped (fn-748), in Upgrade a project, does it.
- Running the loop. Run plays as loops, in Orchestration, owns it.

## Sources
- .garura/project/issues/1021/context/capabilities.md, line 118, the product owner's answer 7: "ADR 066's rename runs after the BI-10 and BI-11 reviews"
- core/components/memory/standards/rules/rename-map.yaml, lines 28-31 and 40: the four builders and the loop
- core/tools/naming/apply_renames.py, line 12: "Names and references only: no behaviour changes."
- docs/adr/046-one-naming-standard-for-every-harness-part.md, lines 10, 50 and 80-81: "Every ICE source that names a renamed part uses the new name, and its fingerprint is stamped again.", "loops use `complete` (Claude Code has `/run`)", "`core/tools/naming/check_old_names.py` fails while any old name is still used outside past records."
- core/components/memory/standards/rules/naming.md, lines 32-33: "`complete` is used by loops only, so a loop is told apart from a play at a glance."
- docs/adr/066-names-say-who-does-the-work-five-roles-own-the-verbs.md, lines 77, 87 and 149: "Only a loop's name starts with `loop`.", the install plays with no role, "The rename, as one change"
- .garura/project/issues/1021/context/names.md, lines 6, 13, 23 and 30: /specify-ontology, /build-play, /fix-play, /build-loop, /fix-loop, /loop-product-spec, and the install plays that stay
- .garura/product/product-os/features/fn-743/feature.md, the old page, line 4: "the Discovery loop's command → run-discovery"
- GitHub #743 (closed): "Rename the harness plays and the loops"; PR #749 (merged)
- The stock-take, .garura/project/issues/1021/context/bi-10-inventory/inventory.md, section 8
