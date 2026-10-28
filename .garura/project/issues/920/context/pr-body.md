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

- **Severity rules** (`standards/rules/severity.md`), written for any harness built on the Phoenix architecture: its parts, its six guardrails, whether a finding is a defect or a change, P1 to P4 with named rules and examples from several kinds of work. The reviewer agent and the work rules point to it. Each Bug of epic #922 now opens with its severity.
- The old-name check skips ADR 059, which quotes the old names on purpose, and the rename tool skips names removed with no successor.
- The branch history was rewritten so no commit holds a home-folder path.

Still waiting, outside this change: sending the corrected memory pages and the new severity page to Phoenix memory (#929).

## Self-review (round 2)

# Self-review: issue 920 (branch feature/920-knowledge-steps-become-skills, against main), round 2

Rules used: the base self-review rules, read through the memory tool (phoenix tier,
standards/rules/self-review.md, fingerprint sha256:d630c3f6...). Those rules say this review is
informational and does not stop the raise on its own. They name no item that stops it.

Findings that stop the raise: 0. No finding below is serious enough to hold the change back.
There are 5 smaller items to look at, listed at the end.

## What the change does

The Discovery loop used to close its missing knowledge with three separate plays that no person
ever runs. Now it is one step, run by the knowledge-builder agent (ADR 059, which retires ADR
042). The three plays are removed. Only agents (and the two named check scripts) call the memory
tool. The memory rule pages, glossary and component docs are corrected. Plan 606 and a
work-tracking rule for epic 922 are added. Round 2 answers the nine findings the person raised on
the first review (H-2, H-1, F1, F2, H-3, H-4, F3, F4, F5) and adds a written rule for how a
finding gets its severity.

Size: 24 commits, 151 files. 51 of those files are the issue's own record folder. Outside it,
100 files: about 3,970 lines added and 3,590 removed, mostly the three deleted plays plus ADR 059.

## Did round 2 fix what was asked

All nine are fixed. I checked each against the code, not the commit message.

- H-2, the grouping script asked the memory tool. Fixed. The script now reads the waiting
  updates from the round record that round_state.py already wrote, and has no tool call or
  subprocess left. Its three copies (the loop, the create-loop reference, the compiled example)
  are byte-for-byte the same. The names it reads ("open" list, "from", "ask") match what
  round_state.py writes. The loop run text and the script's own header say the same. The
  exception in ADR 059 (check_knowledge.py and round_state.py only) now matches the code.
- H-1, adr-keeper could read memory by path. Fixed: the carve-out sentence is gone, and the
  paragraph now says only "through the tool".
- F1, the old-name check lost two names. Fixed: both are kept in the rename map as "removed,
  no successor" (null). I confirmed the old-name check still catches them. But see item 2
  below: one other tool trips over the null.
- F2, the ADR template field had no schema or linter. Fixed: the schema lists
  for_the_accepter, and both copies of adr.py lint it (the two copies are identical). ADR 059
  lints valid. The adr.py tests pass: 47 passed, 0 failed.
- H-3, the run-step lists were stale. Fixed in the opening of loop-run.md and in the glossary
  Loop entry.
- H-4, for_project_memory could be lost. Fixed: knowledge-builder now says to carry the
  draft's for_project_memory into the build group.
- F3, "six" change plays. Fixed to "five", and the new sentence no longer repeats a count.
- F4, two paragraphs not re-wrapped. Fixed in naming.md and loop-contract.md.
- F5, pipeline-next.md missing from the rules index. Fixed: it has a row now, and so does the
  new severity.md.

## Scope checks

- Matches the issue: PASS. Every area touched is named in ADR 059's "Affects" list, in the
  scope given for epic 922, or is a round 2 fix to a finding the person raised. The new
  severity rules page was asked for by the person in the round 1 reply.
- No scope creep: PASS. One thing to know: 13 run-record files from the record-decision run sit
  under .garura/project/issues/_adr/ (outside issue 920's own folder). They are the evidence of
  the run that wrote ADR 059, so they belong, but a reviewer will see them.
- Reasonable size: REVIEW. Large, but it is one decision, and ADR 059 explains it in one place.
  Round 2 itself is small: 20 source files, 267 lines added and 95 removed.
- No stray artifacts: PASS for the diff. No debug prints, TODOs or compiled caches were added.
  One file outside the diff: CLAUDE.md.new is untracked. Keep it out of the commit unless you
  meant it.

## Quality checks

- Tests present: PASS. Loop scripts: 82 tests pass in test_loop_scripts.py and 9 in
  test_discovery_scripts.py. The ADR script: 47 pass. The naming tools: 23 pass. The group
  questions tests were changed to match the new input.
- Commits are clean: PASS. All 24 commits use the conventional format and end with (#920). None
  carries a Claude attribution line.
- No secrets: PASS. A scan of the added lines for keys, tokens, passwords and private-key
  headers found nothing.
- Docs in step: PASS, with notes. The glossary, loop run text, agents, memory rule pages and the
  ADR index are updated. Two carry-overs from round 1 still stand: ADR 059 lists
  docs/components/skills.md, install.py and the product page fn-744 as affected, but none of the
  three changed in this diff. I looked at them before and found no stale reference in skills.md
  or install.py. The fn-744 line that maps review-knowledge to check-knowledge reads as rename
  history and may be fine.
- Nothing obviously broken: PASS. The component checker reports 36 errors; main reports the
  same 36 (4 are in create-loop's SKILL.md, hand-written, same on main). No merge conflicts with
  main (merge-tree is clean). The edit-loop checker passes the Discovery loop with 0 gaps.

## Other checks (assess-pr's own rules for this kind of project)

- No merge conflicts: PASS.
- ADRs: ADR 059 is Accepted and lints valid; ADR 042 is Superseded. PASS.
- Agent and skill files changed: structure not changed by this diff; no new checker error.
- Configuration (yaml): every changed yaml file parses. PASS.
- Components deploy (core/components changed): REVIEW. After the merge, install into a project's
  .claude/ with install-garura; this review did not do it.

## Items to look at (none stops the raise)

1. The old-name check now fails on this branch, and it was clean on main. It reports 28 hits,
   all in the new ADR 059, which quotes the old play names on purpose while describing the old
   Phoenix memory pages (lines 69, 70, 85, 109). Older ADRs that quote old names are skipped by
   the check (ADR 53, and the ones before 46). ADR 059 is not, yet. The harness standard names
   this check as one to run, but no run gate calls it. Smallest fix: add 59 to the quoting-ADR
   set in core/tools/naming/check_old_names.py, as ADR 53 was. Minor.
2. The rename tool apply_renames.py crashes if it meets a name mapped to null. I tried it on a
   scratch folder with one stale use of build-knowledge: it stopped with a TypeError. Today it
   does not trigger, because no stale use is left in the repo, so a dry run passes. The old-name
   check handles null fine. Smallest fix: skip a null in apply_renames.py's rewrite and move.
   Minor.
3. The new severity.md page is not in any memory tier yet. The memory tool finds nothing for it
   in short-term, Garura or Phoenix memory. change-reviewer now tells the agent to read it, so
   until the page is promoted to Phoenix memory (a person's step, like the other rule pages),
   the agent finds nothing. ADR 059 does not list it in "Affects" either. Minor.
4. Not caused by this change, and left alone: the loop script prepare_check.py also calls the
   memory tool (citations --check). That call is read-only and was there before, but it is not
   in ADR 059's list of allowed scripts. The same class of thing as the round 1 H-2, so worth a
   later look. Nit.
5. Carry-overs and notes: the untracked CLAUDE.md.new, the fn-744 line, the large size, and the
   install step after merge (all above).

## Result

Ready: yes. Findings that stop the raise: 0. Round 2's nine fixes hold up against the code. Five
smaller items are listed above; items 1 to 3 are cheap to fix in this change if you want them
closed before review.
