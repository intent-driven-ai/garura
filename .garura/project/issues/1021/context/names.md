# The names, agreed with the product owner on 2026-11-03

Nothing is renamed yet. The rule: a verb belongs to one role, and a role can have several verbs. The verb says who does it; the intent says which move it serves.

## Specifier
/specify-intent (was /discover-intent) · /specify-domains (was /discover-domains) · /specify-capabilities (was /discover-capabilities) · /specify-ontology (was /edit-ontology) · /learn-outcomes (stays)

## Designer
/design-slice (was /shape-slice) · /design-eval (was /shape-eval) · /design-adr (was /record-decision) · /design-surface (was /shape-ux-lens) · /design-env (was /shape-run-lens, covers deployments) · /design-architecture (was /shape-architecture-lens) · /design-quality (was /shape-quality-lens) · /design-agentic (was /shape-agentic-lens)
Dropped: /shape-marketing-lens, /shape-measure-lens.

## Builder
/build-work (was /build-epic; one work item, whether a slice, feature, story or chore) · /fix-work (was /fix-bug) · /refactor-work (was /refactor-code) · /build-play (was /create-play) · /fix-play (was /edit-play) · /build-loop (was /create-loop) · /fix-loop (was /edit-loop)

## Validator
/validate-work (was /check-change) · /validate-slice (was /validate-epic) · /validate-uat (was /release-epic) · /validate-perf (new) · /validate-security (new)

## Orchestrator
/shape-plan (stays) · /reshape-plan (was /update-plan) · /view-plan (was /show-plan) · /list-plans (stays) · /view-issue (new) · /list-issues (was /list-focus-issues). list means more than one; view means one.
Open: the name for /release-increment. /release-slice is the proposal; it sits under Validation → Run.

## Loops, their own category, one for each transition
/loop-product-spec (was /complete-discovery) · /loop-spec-design · /loop-design-code · /loop-code-validation · /loop-validation-run · /loop-run-product
There is no Ship loop.

## Work plays: anyone can run them, under Developer tooling
/start-work (was /start-change) · /commit-work (was /commit-change) · /review-work (was /propose-change) · /merge-work (was /merge-change). Their final place is still open.

## Product plays, no role
/install-garura, /uninstall-garura (both stay)

## Not plays
Lock the design is a governance check. Initialize and seeding memory, and upgrade, are engine things, like installation.

## Rule changes these need
- A name may not be exactly a tool's built-in command; it may start with one. That allows design-, review-, loop-.
- env, perf and uat join the allowed short words.
- complete-<phase> for loops is replaced by loop-<from>-<to>.
- The fixed verb lists are replaced by each role's verbs.
