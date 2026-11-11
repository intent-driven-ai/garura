## What this does

Garura's product model now holds its own work as eleven business intents, each reviewed with the product owner one
at a time: Product → Spec (BI-1), Spec → Design (BI-2), Design → Code (BI-3), Code → Validation (BI-4), Validation → Run
(BI-5, parked by the product owner on 2026-11-10), Run → Product (BI-6), Install and distribute (BI-7), Developer tooling
(BI-8), Orchestration (BI-9), Standards, structure, settings and memory (BI-10) and Product model (BI-11).

- **The intents.** Eleven intent pages, each confirmed by the product owner, each listing the parts it touches.
- **The capabilities and features.** 40 capabilities and 239 features in software delivery planning. Each page was drafted from what Garura has built and reviewed page by page or, where most of it is built, drafted, written and checked, then shown at commit.
- **The ICE.** 273 ICE pages, each beside its part's page: a full ICE where the part is built, a thin one (138) where it is not.
- **What went.** The old intents #717 (people plan work toward an intent across days and people), #722 (a product model can be managed), #734 (a standard for building harnesses), #756 (the ICE is its own part) and #788 (agents design the work, then build it) are removed, with their slice and the seven plans 606, 717, 722, 734, 756, 767 and 788 (plan 788's evals deleted by name, never opened). Their parts now serve the new intents; capabilities that did the same job are merged.
- **The decisions.** ADR 065 (the model's index is changed through two skills, the model never names a plan, and only tools know the tracker) and ADR 066 (names say who does the work: five roles own the verbs).

Every write went through product-os-keeper and its skills, and every intent closed on the product owner's word. The
last step's checks: 71 of 71 pass, with no new structure error against the state before it
(`.garura/project/issues/1021/context/cleanup/verify.json`).

## Why it is this big

2,872 files, 79% of them short-term memory records under `.garura/project/issues/1021/`: each intent's stock-take,
drafts, approvals, write requests, reports and checks are kept as the record of what the product owner decided and
from what. Read it one intent at a time: the model under `.garura/product/product-os/`, then that intent's records
(`bi-<n>-*` folders and `cleanup/` for the last step).

## Raised past a failed self-review line

The self-review fails one must-have line: 83 of the 108 commit subjects are over the 72-character cap. The pre-push
check (`check_self_review.py`) read the self-review as clean because it does not see FAIL in a table cell; the push was
stopped, and the product owner chose to raise past the line ("raise past"), recorded in
`.garura/project/issues/1021/context/raise-past-check.md`. The long subjects stay in the history, and this run of
/propose-change does not close COMPLETED.

Closes #1021
