# Feature: Rename the lifecycle and lens plays to the standard

## What it does
The plays that move a product through its phases, and the design lens plays, are renamed to the naming standard in force in one batch, with every reference to them, so each lifecycle play's name says which move it makes.
- Built under ADR 046, these plays took their new names:
  - `intent` became /discover-intent, `vision` /discover-domains, `understand` /discover-capabilities and `grill` /shape-slice;
  - the seven lens plays `ux`, `arch`, `quality`, `measure`, `run`, `agentic` and `marketing` became /shape-ux-lens, /shape-architecture-lens, /shape-quality-lens, /shape-measure-lens, /shape-run-lens, /shape-agentic-lens and /shape-marketing-lens;
  - `implement` became /build-epic, `validate` /validate-epic, `launch` /release-epic, `deploy` /release-increment and `learn` /learn-outcomes;
  - Renaming Functionality to Feature on disk then freed the word feature: the four feature plays took the epic and slice names, such as `shape-features` to /shape-slice and `build-feature` to /build-epic.
- The old page asked for `design-` names for the plays between intent and design. They took `shape`, because "Intent → Design uses `shape` (Claude Code has `/design`)". /shape-scope and /shape-roadmap were later dropped (ADR 053).
- Under ADR 066, decided and not applied:
  - the specifier's plays: /discover-intent, /discover-domains and /discover-capabilities become /specify-intent, /specify-domains and /specify-capabilities, and /learn-outcomes stays;
  - the designer's plays: /shape-slice becomes /design-slice, /shape-eval /design-eval, /shape-ux-lens /design-surface, /shape-run-lens /design-env, /shape-architecture-lens /design-architecture, /shape-quality-lens /design-quality and /shape-agentic-lens /design-agentic;
  - two lens plays go: "`/shape-marketing-lens` and `/shape-measure-lens` get no new name, and they go.";
  - the builder's and the validator's plays: /build-epic becomes /build-work, /validate-epic /validate-slice and /release-epic /validate-uat; /validate-perf and /validate-security are new;
  - "the name for `/release-increment` is still open, and `/release-slice` is the proposal".
- Examples, in different kinds of project:
  - In a bank's payments service, the team renames its play that turns a request into a spec to the specifier's verb, and every guide that named it changes in the same batch.
  - In a clinic's booking app, the team drops a lens play that no one ran, records why in an ADR, and gives it no new name.
  - In a harness repository, ADR 066 renames the design plays to `design-` names, allowed now that a name may start with a coding tool's own command.
- How it meets the capability: the plays that carry a product through its phases follow the one rule, and their verbs say who does the work.

Status: built, under ADR 046, and, for the four feature plays, by renaming Functionality to Feature on disk. Not built, or open:
- ADR 066's names for this family are decided and not applied; the rename runs after the reviews of BI-10 and BI-11, as one change.
- The two dropped lens plays and their skills are not deleted yet: "Nothing is deleted by this decision."
- The name for /release-increment is open.

## Inputs / Outputs
- In: the rename map's lines for this family, and the agreed new names.
- In: every reference to the old names, in the source, the docs, the installer and the guides.
- Out: the plays under their new names, with every reference changed and each ICE changed in wording only.
- Out: the old-name check's report, with none of this family's old names left.

## Rules & behavior
- Names and references only. The reason: "Names and references only: no behaviour changes."
- Moving these plays onto the new model is separate work. The reason, from the old page's limit: "Names only; moving these plays onto the new model is separate work."
- A dropped play is recorded in an ADR with its reason. The reason, in the product owner's words: "They didn't have good reasons to exist. They'll be added if needed, and for now they go."
- A name may start with a coding tool's own command, once ADR 066's rename lands. The reason: "A name may not be exactly a tool's built-in command, but it may start with one."
- ADR 066's rename is one change. The reason: "The rename, as one change".
- Not decided: the name that /release-increment takes under the standard.

## Acceptance criteria
- Given ADR 046's rename, when the old-name check runs, then it finds no `/vision`, `/understand`, `/grill`, `/implement` or `/launch` command.
- Given a renamed lifecycle play, when its ICE is compared with the one before the rename, then only the names changed.
- Given ADR 066's rename has landed, when a person types /design-slice, then the play that was /shape-slice runs. This is not built.
- Given ADR 066's rename has landed, when the plays are listed, then /shape-marketing-lens and /shape-measure-lens are not among them. This is not built.

## Out of scope
- The rule the names follow. Name every part by one rule, with five roles owning the verbs (fn-736) does it.
- The rename map and the check. Map every old name to its new one, and check that no old name is left (fn-741) does it.
- What each lifecycle play does. The capabilities of each phase own it, such as Specify the product, in Product → Spec.
- Taking out the old names in a project. Take out the parts Garura renamed or dropped (fn-748), in Upgrade a project, does it.

## Sources
- The product owner's answer 7 (2026-11-11): "ADR 066's rename runs after the BI-10 and BI-11 reviews"
- core/components/memory/standards/rules/rename-map.yaml, lines 5-20 and 33-38: the renames of ADR 046 and of the rename of Functionality to Feature on disk
- core/tools/naming/apply_renames.py, line 12: "Names and references only: no behaviour changes."
- docs/adr/046-one-naming-standard-for-every-harness-part.md, lines 49-50: "Intent → Design uses `shape` (Claude Code has `/design`)"
- docs/adr/053-shape-scope-and-shape-roadmap-are-dropped.md: /shape-scope and /shape-roadmap are dropped
- docs/adr/066-names-say-who-does-the-work-five-roles-own-the-verbs.md, lines 73, 91, 95 and 149: "the name for `/release-increment` is still open, and `/release-slice` is the proposal", "A name may not be exactly a tool's built-in command, but it may start with one.", "`/shape-marketing-lens` and `/shape-measure-lens` get no new name, and they go.", "They didn't have good reasons to exist. They'll be added if needed, and for now they go.", "Nothing is deleted by this decision.", "The rename, as one change"
- The names agreed with the product owner on 2026-11-03: the agreed new names of this family
- .garura/product/product-os/features/fn-745/feature.md, the old page, lines 4 and 8: "shape → design-scope", "Names only; moving these plays onto the new model is separate work."
- The stock-take (2026-11-11), section 8
