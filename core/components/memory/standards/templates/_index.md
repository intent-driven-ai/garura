# Templates

Canonical output-shape templates for artifacts the system produces — GitHub issues, approval prompts, checkpoint files, evidence files, knowledge files. Every skill that produces such an artifact instantiates the matching template instead of inlining its own prose.

Replaces the former `memory/formats/` directory (#209 + structural cleanup).

Agents and skills query this category when they need to know: **"What does the output artifact look like?"**

## Contents

| Path | Description | Consumers |
|------|-------------|-----------|
| `github-issue.md` | GitHub issue body template and field derivation rules | `track-issue`, `project-orchestrator` |
| `approval-prompt.md` | The one checkpoint format: an opening, four parts per question, and a plain typed reply. Every checkpoint-gated play uses this instead of its own prompt text. | `specify`, `design`, `arch`, every checkpoint-gated play |
| `checkpoint.md` | Canonical checkpoint artifact format. Written by the play alongside every approval prompt; retained as STM audit trail. | every checkpoint-gated play |
| `evidence-file.md` | Canonical evidence file format. Written by the play at close; contains step/scenario eval results, checkpoint decisions, recovery attempts, next consumers. | every play that closes with an evidence step |
| `knowledge-file.md` | Canonical knowledge-file template. Tier 1 (all files) and Tier 2 (core-scoped) metadata requirements, staleness rules, and index registration conventions. | `knowledge-extractor`, `capture-learning` |
| `issue-comment-rca-approved.md` | Canonical GitHub issue comment posted when a user approves an RCA + fix plan at the fix-it approval checkpoint; mirrors the decision from STM to the issue thread. | `fix-it`, future plays producing `rca.yaml` + `design.yaml` |
| `commit-message.md` | Canonical commit message shape — `<type>(<scope>): <subject>` format, field rules, and related pointer to `rules/commits.md` quality rules. | `commit-files`, `assess-changes`, `commit-code`, `repo-orchestrator` |
| `work-plan.md` | Canonical work-plan format (ADR 030): what gets done, in what order, and why — never how. The human's interface to a business intent; instantiated at `{stm_base}{issue}/specs/plan.md`. Rules in `rules/work-plan.md`. Not the `/build-epic` build plan. | `author-plan-file` (skill), via `project-orchestrator` |
| `plan-update.md` | What `/update-plan` shows a person — the plan found, the stop on uncommitted work, each entry taken, a rule break and its override, the approval screen (the plan before and after, and what changed) with its question (approved, rejected, abort), the landing and the abort — in a settings block the play's render script reads (#730). | `/update-plan` |
| `plan-view.md` | The three views of the plans: the list of every plan, one plan as a tree, every plan as a graph against main. Holds the six statuses (Not Started, In Progress, Now, Done, Blocked, Dropped), their marks and the layout of each view, in a settings block the plan tool reads (#719). | `/list-plans`, `/show-plan`, the plan tool |
| `product-ontology.md` | Canonical product ontology format: the questions it must answer, each kind (what it is, who reads it, where it lives, properties, relationships, rules, example), kinds not yet defined, and a log. Person-facing kinds are written for a business reader. | `author-product-ontology` (skill) |
| `adr.md` | The one decision-record (ADR) template: core fields shared by two shapes — Markdown for Garura's ADRs (`docs/adr/`), `decision.yaml` records for product decisions — plus the rules (accepted ADRs never edited; forward pointers both ways; never changes a person's business intent). | `/record-decision` (play), `author-decision` (skill) and its `adr.py lint` |
| `pr-body.md` | Canonical PR body shape — Summary, Quality Checklist (Required/Optional), Verification Evidence table, Eval Results (conditional), generated-by footer. Includes Eval Results instantiation rules. | `open-pr`, `assess-pr` |
| `pr-review-comment.md` | Canonical PR review comment shape — `<!-- review-pr:marker -->` sentinel (required), Confidence line, P1–P4 sections with counts, Reviewers section. Supports in-place update detection via marker. | `review-pr` |
| `delivery-report.md` | Canonical human-readable delivery report — Run Summary (play, issue, status, timestamps), Pipeline Steps table, Artifacts Produced table, Next Steps (optional). Per-play field notes for ship, fix-it, implement. | `ship`, `fix-it`, `implement`, every play that closes with a delivery step |
| `eval-story.feature.md` | The shape of one story file of a slice's eval (`eval.<feature-id>.feature.md`): Markdown with Gherkin, its `Feature:` is the story, one tag line per scenario naming what it covers (`@goal-<n>`, `@expectation-<n>`, `@F<n>`), steps from the surface kind's step library, exact Then results, an Untestable list and a Lines covered list; the rules are in `rules/eval-format.md` (#798, ADR 057). | `/shape-eval`, `author-slice-eval` |
| `eval-slice.md` | The shape of a slice's eval file (`eval.<slice-id>.md`): the stories in build order, the surface kind, the time limit for each scenario, the pass rule (every scenario passes, no score), the names the usage guide maps, the Context guidance; the rules are in `rules/eval-format.md` (#798, ADR 057). | `/shape-eval`, `author-slice-eval` |

## Scope Notes

- **`issue-list.md`** — Considered and deferred as of #209 closure. `templates/_index.md` requires a template to be "instantiated by at least one skill or play." No play currently renders a user-facing issue list (`gh issue list` is used only for existence checks). Deferred until a play is built that renders issue lists to users.
- **`pr-findings.yaml`** — Routed to `standards/schemas/` rather than `templates/`. It is a typed YAML schema contract with field-level constraints, rejection rules, and sort-order requirements — it belongs in `schemas/` per the category rule ("YAML schema contracts belong in `schemas/`"), not in `templates/`.

## When to Add Here

A file belongs in `templates/` if:
- It defines the shape/structure of an output artifact
- It is instantiated by at least one skill or play
- It answers "what should this look like?" / "what fields go where?"

A file does NOT belong here if:
- It defines WHICH artifacts to produce (that's play / skill contract territory)
- It defines rules for artifact content (that's `rules/`)
- It is a YAML schema contract (that's `schemas/`)
