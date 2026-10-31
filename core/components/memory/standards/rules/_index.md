# Rules

Canonical rules for every recipe-producing domain. Each file holds the single source of truth for "how must artifacts of this type look" or "what operational rules apply to this surface". Skills reference these files instead of inlining constraints in their own prose.

Agents and skills query this category when they need to know: **"What rules must this artifact or surface follow?"**

## Contents

### Naming

| Path | Description | Consumers |
|------|-------------|-----------|
| `naming.md` | How plays, loops, skills and agents are named — verb first, one meaning per verb, no tool built-ins, loops `complete-<phase>` (ADR 046) | every builder of a harness part, `create-play`, `create-loop` |
| `naming.yaml` | The machine half: the verb lists, industry terms, reserved built-in commands | `core/tools/lint-components` |
| `rename-map.yaml` | Every old name and its new name, from adopting the standard. A name mapped to `null` was removed with no successor (ADR 059): the old-name check still reports it, and the install has nothing to lay for it | the old-name check, `install-garura` |

### Knowledge rules

| Path | Description | Consumers |
|------|-------------|-----------|
| `resolution.md` | R1-R4 LTM resolution protocol — LTM hierarchy enforcement, authority semantics (LOCKED / DRAFT), resolution trace schema, context isolation exemptions; the decision trace every agent keeps (ADR 035 §6, ADR 037) | `tech-designer`, `repo-orchestrator`, every agent that reads LTM |

### Eval rules

| Path | Description | Consumers |
|------|-------------|-----------|
| `eval-format.md` | The rules of a slice's eval (ADR 057): its Gherkin story files and slice file, the tags and the Lines covered list, the fixed yardstick (a later run only adds; a moved story line is named for a person, never rewritten), and what an eval never holds | `/shape-eval`, `author-slice-eval`, the eval runner (later) |

### Operational rules (git and commits)

| Path | Description | Consumers |
|------|-------------|-----------|
| `commits.md` | Commit categorization (feat / fix / refactor / etc.), conventional-format quality rules, subject / body rules, scope validation, large-file thresholds, secret detection | `assess-changes`, `assess-pr`, `commit-files`, `commit-code`, `repo-orchestrator` |
| `git.md` | Branch naming conventions (plan/<plan-id>/base and plan/<plan-id>/<issue>-<slug> for a plan's work, feature/, fix/, hotfix/, etc.) and how branch patterns map to quality-gate priorities | `repo-orchestrator`, `cut-branch`, `start-change` |
| `pr.md` | PR severity taxonomy — deterministic mapping from quality standard IDs (SEC, ARCH, BE, CODE, FE, TEST, DOC, OPS, PERF, DATA, DEBT) to P1–P4 severity buckets with grep / path match rules. No LLM judgment. | `review-pr`, `check-pr-quality`, `assess-pr` |
| `self-review.md` | Base scope-and-quality self-review checklist a change runs before it is raised. Resolved via `standards_order` (most-specific wins); overrideable per project. Informational (rides in the PR), not the approve/reject gate. | `propose-change`, `assess-pr` |

### Play lifecycle rules (auto-emitted by the play compiler)

| Path | Description | Consumers |
|------|-------------|-----------|
| `evidence-recording.md` | D1 evidence rule (#434) — evidence recording is play-only (never agents, never skills); fires on `evidence.record`, tunable per play via `evidence.plays.<name>`. | `create-play`, `core/tools/lint-components`, every play |
| `pipeline-position.md` | D2 pipeline rule (#434) — a play declares `position: start\|end\|both\|none`; create-play injects start-change (start) and the commit → propose → review → merge end sequence (end). Members: start-change + the four end plays. | `create-play`, `core/tools/lint-components`, every play |
| `pipeline-next.md` | The Next-line map: for each play and loop, the command its close names next and why. A loop's knowledge step is not a play and has no row | every play's and loop's close (`play-close.md`), `lint_play.py --next-map`, `lint_loop.py --next-map` |
| `surface-contract.md` | Surface contract (ADR 022, #442) — an epic's user-facing surface (`web_dashboard\|server_api\|cli\|library\|service_read_model`) is DECLARED at the `/shape-slice` cut and checked downstream, never re-derived; per-type required runnable evidence, valid deploy targets, downgrade ordering, and surface-debt blocking. | `/shape-slice`, `/build-epic`, `/validate-epic`, `/release-epic`, `core/tools/lint-components` |
| `no-unbacked-recommendation.md` | The cardinal rule (2026-09-08) — a play that recommends must be able to cite what backs it. Where it cannot, it says NOTHING: no default, no generic pointer, no substitute play name — and it reports how many entries it could not recommend for. Wired as a constraint + failure condition + step eval + strip-not-replace recovery. Reference implementation: `focus` (C12/F10/S8/REC10). | `create-play`, `edit-play`, `lint_play.py`; wired in `/list-focus-issues`; caught-not-yet-wired in `/check-change` |
| `user-questions.md` | Questions a play asks a person (from the old product rules' Rule 12, ADR 050) — every question goes to the issue's short-term memory, `context/grounding-questions.md`, with a unique ID and a place for the answer; the file only grows; an answer is a fact and is not asked again; open questions come back at the next checkpoint. | every play and skill that shows an inference to a person |
| `play-orchestration.md` | When a play skips an agent — if a value comes from a sure source (branch name, path, config key), the play makes the agent's output itself, in the same shape, and does not start the agent. | every play, `create-play` |
| `play-patterns.md` | Patterns learned from building plays — a test gate after each commit when a play makes many commits; tech skills made at run time from a tech playbook, so a play names no stack when it is built. | `create-play`, `edit-play` |
| `work-plan.md` | Work plans (ADR 030) — when a plan must exist (the opening `start-change` → `plan-change` → `approve-change`, only when needed), what it may contain (a plan, never a design; every item explains itself; say what kind of done; name what it serves), who keeps it current (small vs big updates; a loop's updates approved at its end), when it is done (the check script decides), and how status is shown (a tree). Format in `templates/work-plan.md`. | `author-plan-file`, `project-orchestrator`; `/create-play` and `/edit-play` once plan mode is wired (#621) |
| `concurrent-fanout.md` | Concurrent read-only fan-out (#468, epic #460 Stage 5) — the one allowed intra-step concurrency: a step runs independent read-only sub-tasks at once when three conditions hold (read-only over shared inputs, distinct output paths, no sibling dependency), then joins. Bounded + joined + order-stable, so the step stays a single deterministic node (ADR 025). Also the scoped-write fan-out (#615): sub-tasks that write the model at once, each only inside its own declared folder, no shared file, one keyed persist and one guard after the join. Parallel code-building is #488. | `create-play`, `core/tools/lint-components`, `/discover-domains`, `/discover-capabilities`, `/validate-epic` |

### Loop rules (ADR 029, ADR 041)

| Path | Description | Consumers |
|------|-------------|-----------|
| `loop-contract.md` | Loop contract (ADR 029, #614) — what a loop hands a play (`loop_run_id`, `loop`, `branch`, `issue`, `review_dir`, per-play `inputs`/`answers`) and how a play runs inside a loop: write everything under the loop's issue (the issue ID governs), read no memory itself, open nothing, keep its own commit, never wait at a conditional checkpoint (a review record + `deferred_to_loop_review` instead), never defer a pinned one by contract, hand a question it cannot answer to the loop (`open-<play>.json`) and finish what it can — the loop loops over its plays, runs its knowledge step, and briefs the person only on what none answers (ADR 059); the contract carries the `round`. Shared checker `check_loop_contract.py`, writer `write_loop_review.py`. | `/discover-domains` (wired), `/discover-intent` (own check), `/discover-capabilities` (#615), the loops |
| `run-status.md` | Run status (#613) — what a long run is doing now: the loop writes `status/run-<name>.json` (state, round, play, step, times) through `loop_status.py`, whole, at every step; it never displays anything. A display — for Claude Code, a separate plugin — reads the file. The two are decoupled. | the loops; a status plugin (later) |

## Deferred follow-ups

These rule files are named in issue #210 but are not yet authored. They should be created when the corresponding plays / skills are built or rebuilt:

- `roadmap.md` — rules for roadmap structure (buckets, bets, circuit breakers)
- `plan.md` — rules for execution plans, i.e. `/build-epic`'s **build plan** (DAG, file-level changes, tests). Not the work plan — that is `work-plan.md` above.

## When to Add Here

A file belongs in `rules/` if:
- It answers "how must this artifact / surface be structured?"
- It is enforced by at least one skill (validator, generator, orchestrator)
- It is the single source of truth for the domain — not a copy of skill prose

A file does NOT belong here if:
- It is an output template (those go in `templates/`)
- It is a YAML schema contract (those go in `schemas/`)
- It is resolvable from the code itself (those stay in the code)
