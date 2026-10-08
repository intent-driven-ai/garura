## What this decides and builds

Spike #619 decides **plan mode** (ADR 030): every change works from a plan on disk — what gets done, in what order, and why, never how — kept current, and done only when the plan is done. It also builds the first pieces and records core doctrine.

**Core doctrine (in `docs/philosophy/idsd.md`):** the plan is the person's interface; the product model is the agents'. A person has two interfaces — the intent they give and the output they see — and the loop has two handoffs: Kickoff in, a handover drive out.

## Decided (ADR 030)
- A change opens with `start-change` → `plan-change` → `approve-change`, only when needed.
- Plans live in STM; a script decides "done"; each plan names the plan it serves (business intent → agent work).
- Small updates need no human; big updates are approved (inside a drive, at its end).
- Plays drop their task lists once the plan takes over their four jobs.

## Built
- Plan template (`standards/templates/plan.md`) and the first real plans (#606, #619).
- `manage-plan` skill and its check script; `project-orchestrator` gathers the plan context.
- Reading an issue now returns its type, parent and sub-issues (needs gh 2.94.0+).

## Filed
Feature #621 (plan mode wiring) with Stories #622–#628, under #539.

Closes #619

---

<details><summary>Self-review</summary>

# Self-review — #619 Plan mode (feature/619-plan-mode vs main)

Rules: `/Users/kapilahuja/.garura/core/memory/standards/rules/self-review.md` (base, not an override; see `resolved-rules.json`).
Diff: 11 commits, 25 files, +912 / -17. About 470 of those lines are the STM plan and evidence files; the rest is the ADR, the template, the skill and its script, the agent edit, the adapter change and two doctrine edits.

Summary: the change does what the spike's owner chose to build (decision P2) and set as doctrine, and nothing outside it. Nothing here stops the raise.

Blocking: none.

## Scope checks

- Matches the issue: PASS. The spike's "done when" is an ADR that answers every question (ADR 030, answering the ten recorded decisions) plus stories filed for the next steps (#621 with #622 to #628, all open, all filed under the feature). The extra build (plan template, `manage-plan` skill and its check script, plan-context step in `project-orchestrator`, `read-issue` returning issueType/parent/subIssues) is the owner's recorded choice in `decisions.md` P2.
- No scope creep: REVIEW (owner-directed, so noted, not flagged). Two edits go past the spike's literal question: the doctrine "the plan is the human's interface" in `docs/philosophy/idsd.md` and ADR 029 (Kickoff as the human interface, plus a placeholder for a handover drive). The owner asked for core doctrine to be set during this spike. The reviewer should confirm that is acceptable in this PR rather than a separate one.
- Reasonable size: PASS. Roughly 440 lines of non-STM change across 14 files, in 5 separate feature/docs commits; the STM files are plain records. Readable in one sitting.
- No stray artifacts: PASS, with one note. No debug prints, no commented-out blocks, no scratch files. The only `print` calls are the intended JSON output of `check_plan.py` and the adapter. `.garura/project/issues/619/context/resolved-rules.json` is untracked and is the self-review's own record; commit it with the review or leave it out, as the play decides.

## Quality checks

- Tests present: REVIEW (gap, not a stopper). The existing adapter test passes (`python3 core/components/plays/play-creator/references/test_platform_adapter.py` gives 18 passed, 0 failed), but it does not pin the new `read-issue` fields, so the change to the field list is untested. `check_plan.py` is new and has no test file. I exercised it by hand: valid-and-open plan exits 1, valid-and-done plan exits 0, a malformed plan exits 2 and lists every problem, a missing file exits 3. A small fixture test for the script and one for the `view-issue` argv would be the natural follow-up; not needed for the spike to land.
- Evidence run, plan check on #606: `valid: true, done: false, status: active, now: 2`, 12 open items, no problems (exit 1, the normal state while work runs).
- Evidence run, plan check on #619: `valid: true, done: true, status: done, open_items: []`, `serves_plan` points at #606's plan and was confirmed to exist (exit 0).
- Adapter change consistent: PASS. The four `platform_adapter.py` copies (merge-change, propose-change, review-change, play-creator/references) have the same checksum, and `verbs.md` for GitHub and `adapter.md` list the same field set. The new fields work live: `gh issue view 619` returns Spike, parent 539 and 2 sub-issues (gh 2.102.0 here; the docs say 2.94.0 or newer). The GitLab gap is stated in its `verbs.md`.
- Commits are clean: PASS with a note. All 11 are conventional-format, scoped, and reference #619. The `chore(stm)` commits are the play's own evidence commits. Only the first commit carries a Co-Authored-By line; the others have none. Style only.
- No secrets: PASS. Scanned the added lines of the non-STM diff for key, token, password and private-key patterns: nothing found.
- No merge conflicts: PASS. The branch is cut from current main; the diff is new files plus small edits.
- Docs in step: PASS. The new template has its `_index.md` row; the agent's skill table and "when to use" rows list `manage-plan`; ADR 025 carries a status note pointing to ADR 030; the GitLab gap is documented.
- ADR checks: PASS. ADR 030 has Status (Accepted), Context, Decision, Consequences, Alternatives, and follows the `NNN-*.md` numbering. ADR 025's status line is still a valid status with an amendment note.
- Skill checks: PASS. `manage-plan/SKILL.md` has name, description, user-invocable and allowed-tools in its front matter, and Input and Output sections. It has a "Rules" section rather than one titled "Constraints" (nice-to-have only).
- Deployed copies in step: REVIEW. `core/components/**` changed, so the target `.claude/` needs a redeploy through `install-garura` (deployed copies are gitignored and not part of this diff). Do it after merge, before using `manage-plan`.
- Nothing obviously broken: PASS. No leftover TODO or FIXME in the added lines. Known and intended: ADR 030 describes plays (`plan-change`, `approve-change`) and a `show` mode that do not exist yet; they are filed as #622 and #628, so the ADR is a decision, not a claim that they are built. The #619 plan reads `done` while issue #619 is still open; that is correct until the owner closes the spike.

## Verdict

Ready to raise. Blocking count: 0. Items for the reviewer: the doctrine edits riding with the spike (scope), and the two missing tests (quality).

</details>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
