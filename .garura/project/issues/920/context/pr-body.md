## What this changes

The Discovery loop's knowledge step was built as three plays that no person runs (`/search-knowledge`, `/research-knowledge`, `/check-knowledge`). It is now one step of the loop, run by the `knowledge-builder` agent with the four skills that already existed, and three small scripts the loop owns: group the repeated questions, check the step's records, record the person's reply (ADR 059). The three plays are removed.

On the way it fixes the defects the unplanned epic #922 gathers:

- the loop's done check could never find two of the plays' records, because they kept their old names (#923);
- the loop's pre-flight named the plays and the loop by their old names, so it never read the loop's own settings (#924);
- the round script read waiting memory updates from their files instead of asking the memory tool (#925);
- the research skill called the memory tool itself, though only agents may (#926);
- the proposed-answers skill was handed no memory (#927);
- the ADR keeper agent read Phoenix memory by its file paths (#928).

It also adds a section to the ADR template that tells the person accepting a decision what was found on the way (#930), corrects the memory pages in Garura's source that taught the old setup, writes plan 606 for the unplanned epic, and adds the rule "An unplanned epic gathers defects being fixed together" to the work rules.

Not in this change: sending the corrected memory pages to Phoenix memory (#929, waits for the product owner's yes), and the Phoenix memory capability in the product model (after this lands).

Closes #920
Closes #923
Closes #924
Closes #925
Closes #926
Closes #927
Closes #928
Closes #930

## Checks

- Every test file in the source passes (64 files).
- The loop linter passes on the Discovery loop and the worked example.
- The component linter shows the same 36 errors as main, none new.

## Round 2 (after the product owner's reject)

The product owner rejected round 1 and set the severities. All fixed:

- **P1** — the grouping script asked the memory tool for waiting updates, which ADR 059 allows only the knowledge step's check and the round script. It now reads them from the round record the round script writes, and never calls the tool (shared copy, both loops, the shared run's step, tests).
- **P2** — the ADR keeper's memory paragraph said the memory seed "is a repository file: read it as one", which invited an installed agent to read memory by its path. The sentence is gone.
- **P3** — the old-name check stopped catching the two removed play names. The rename map keeps them mapped to `null` ("removed, no successor"); the check catches them again and the install skips them.
- **A change, not a defect** — the ADR template's new field `for_the_accepter` is now in the decision schema, and the ADR linter checks it in both shapes (tests added; ADR 059 lints clean).
- Small fixes: the shared run's step list and the glossary name the knowledge step; the agent carries `for_project_memory` into its build record; "five" change plays, not six; re-wrapped paragraphs; the rules index names the Next-line map.

Also in round 2:

- ~~Severity rules page~~ — moved out of this change to **#934** (one severity, P1 to P4, in three layers on an industry base), with **#933** (the Phoenix architecture memory it tests against).
- The old-name check skips ADR 059, which quotes the old names on purpose, and the rename tool skips names removed with no successor.
- The branch history was rewritten so no commit holds a home-folder path.

Still waiting, outside this change: sending the corrected memory pages to Phoenix memory (#929).

## Round 3 (after the product owner's second reject)

The product owner accepted the round-1 fixes and rejected round 2 for the severity page only.

- The severity page and its four pointers are out of this change; `standards/rules/pr.md` and the reviewer agent are back to what main has. The work is #934, with #933.
- The work rules keep one severity value on each Bug's first line (`Severity: P<n> — why`), set by the product owner until #934 lands; the Bugs of epic #922 carry it.
- Four over-long lines re-wrapped (the shared loop run, the Discovery loop's ICE — fingerprint refreshed — and create-loop); the knowledge agent now hands the research skill the place to write its draft.
- Checks: the loop tests (121 + 9), the ADR tests (47), the naming tests (23), the installer tests and the loop linter pass; the old-name check finds nothing; the component linter shows the same 36 errors as main.

## Self-review (round 3)

# Self-review: issue 920 (branch feature/920-knowledge-steps-become-skills, against main), round 3

Rules used: the base self-review rules, read through the memory tool (phoenix tier,
standards/rules/self-review.md, fingerprint sha256:d630c3f6...). Those rules say this review is
informational and does not stop the raise on its own. They name no item that stops it.

Findings that stop the raise: 0. Nothing below holds the change back. There are 3 small items to
look at, listed at the end.

## What the change does

The Discovery loop used to close its missing knowledge with three separate plays that no person
ever runs. Now it is one step, run by the knowledge-builder agent (ADR 059, which retires ADR
042). The three plays are removed. Only agents (and the two named check scripts) call the memory
tool. The memory rule pages, glossary and component docs are corrected. Plan 606 and a
work-tracking rule for epic 922 are added. Round 2 answered the nine findings the person raised
on the first review. Round 3 takes the new severity page out of this change (it moves to #934),
re-wraps the loop files, and tells the research skill where to write its draft.

Size: 34 commits, 167 files. 81 of those files are the issue's own record folder. Outside it, 86
files: about 2,770 lines added and 3,590 removed, mostly the three deleted plays plus ADR 059.

## The three round 3 commits

- Severity rules taken out (865faa23). Done cleanly. The severity page is deleted, and its row in
  the rules index and its pointer in the PR rules page are gone. change-reviewer no longer tells
  the agent to read it: it goes back to "a severity drawn from the PR severity taxonomy", and the
  grounding row no longer lists it. The work-tracking rule for a Bug says the product owner sets
  the severity until #934 gives the rules. I searched the whole repo for any other mention of the
  page: none is left outside the issue's own record folder, where old review records still name
  it as history. This also closes the old worry that the page was not in any memory tier: it no
  longer exists to be missing.
- Loop files re-wrapped and the fingerprint refreshed (ad3c3c0a). The Discovery loop's stored
  fingerprint is sha256:2ed346c2..., and a fresh hash of reference/ice.md gives the same value,
  so it is in step with the file it describes. Only line breaks and one sentence moved in
  loop-run.md, ice.md and create-loop; no meaning changed.
- knowledge-builder names the draft path (ad3c3c0a). It now hands the research skill the topic,
  the context and the draft path (pages/<topic-slug>.json under the knowledge folder), and says
  the skill writes the draft there. This matches the next step, where the agent raises that draft.

## Scope checks

- Matches the issue: PASS. Round 3 only removes the severity work (moved to #934), re-wraps, and
  names a path. Nothing new rides along.
- No scope creep: PASS. Round 3 reduces scope. As before, 13 run-record files from the
  record-decision run sit under .garura/project/issues/_adr/. They are the evidence of the run
  that wrote ADR 059, so they belong, but a reviewer will see them.
- Reasonable size: REVIEW. Large, but it is one decision, and ADR 059 explains it in one place.
  Round 3 itself is 5 source files with about 14 lines added and 10 removed, plus the severity
  removal.
- No stray artifacts: PASS for the diff. No debug prints, TODOs or caches were added. One file
  outside the diff: CLAUDE.md.new is untracked. Keep it out of the commit unless you meant it.

## Quality checks

- Tests present: PASS. The loop scripts tests, the Discovery loop tests and the naming tools
  tests (23 pass) all pass when run now. Round 3 changed no script.
- Commits are clean: PASS. Every commit uses the conventional format and ends with (#920). None
  carries a Claude attribution line (checked in all 34 commit messages).
- No secrets: PASS. A scan of the added lines in the source, docs and rules for keys, tokens,
  passwords and private-key headers found nothing.
- Docs in step: PASS. The glossary, loop run text, agents, rules index and ADR index agree with
  each other, and the severity pointers are gone from all of them.
- Nothing obviously broken: PASS. The component checker reports 36 errors, the same count as on
  main. The old-name check now reports 0 hits (it reported 28 in round 2, all in ADR 059; ADR 59
  is now in its set of ADRs that quote old names on purpose). The rename tool skips a name mapped
  to null. All changed yaml files parse. No merge conflicts with main (merge-tree is clean).

## Other checks (assess-pr's own rules for this kind of project)

- No merge conflicts: PASS.
- ADRs: ADR 059 is Accepted and lints valid; ADR 042 is Superseded. PASS.
- Agent and skill files changed: structure not changed by round 3; no new checker error.
- Configuration (yaml): every changed yaml file parses. PASS.
- Components deploy (core/components changed): REVIEW. After the merge, install into a project's
  .claude/ with install-garura; this review did not do it.

## Items to look at (none stops the raise)

1. The re-wrap in create-loop/SKILL.md is partial. Two paragraphs near the edited lines still run
   past 120 characters (the lines starting "A loop loops over its plays" and "Add only what the
   End section names", and the next one). The edited lines are fine; these were not touched.
   Nit.
2. The loop script prepare_check.py also calls the memory tool (citations --check). That call is
   read-only and was there before this change, but it is not in ADR 059's list of allowed
   scripts. Not caused by this change; worth a later look. Nit.
3. Carry-overs: the untracked CLAUDE.md.new, the large size, and ADR 059 listing
   docs/components/skills.md, install.py and the product page fn-744 as affected while none of
   the three changed (I found no stale reference in them before). Also the install step after
   merge.

## Result

Ready: yes. Findings that stop the raise: 0. The severity removal is complete with no dangling
pointer, the Discovery loop's fingerprint matches its file, and the research draft path is
named.
