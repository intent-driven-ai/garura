# What this change holds (to help group it by concern)

One change for #719 (view plans) and #979 (a found part gets a thin page), on plan/717/719-view-plans.

- #719 — the plan-view template (core/components/memory/standards/templates/plan-view.md, _index.md), the plan tool (core/tools/plan/), the two plays (core/components/plays/list-plans/, show-plan/), the Next map entries (rules/pipeline-next.md), rule 19 (rules/work-plan.md).
- #719 — the six statuses: every plan file (.garura/project/plans/*.yaml) rewritten, and /shape-plan writes Not Started (core/components/plays/shape-plan/scripts/write_plan_file.py).
- #719 — install: the plan tool and the two plays in the harness list and its test (core/components/plays/install-garura/scripts/install.py, test_install.py), and the install record (.garura/install-manifest.json).
- #979 — the link-model-part skill (core/components/skills/link-model-part/), the page skill reaching intent pages (core/components/skills/enrich-grounding/SKILL.md), and the model sub-agent's route and rule (core/components/agents/product-os-keeper.md). The link-model-part line in install.py belongs with the install group above or with #979; either is fine.
- #719 — the product model brought up to what was built (.garura/product/product-os/: _spine.yaml, features fn-806 (new), fn-628, fn-729; persona fixes on cap-739, fn-731, fn-746 and intents bi-717, bi-722, bi-734).
- #719 — the issue's working record (.garura/project/issues/719/: design, context, model-update, issue-edits, templates).
