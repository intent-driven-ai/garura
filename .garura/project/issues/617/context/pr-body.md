## What this decides

A drive runs its plays without stopping, so a person has to review its work at the end. This change records how that review works, and what "approved" means for the product model.

- **ADR 032 — a drive ends with a review of its outcome.** The review is the drive's last step. The person reviews the outcome — the business intents (BInt), the agent intents (ICE) under them, and the product model — never the plays, in a review tool, not on the pull request. Each piece is accepted, sent back with a comment, or dropped. A failed drive gets the same review; a dropped box-move lowers the limit again.
- **ADR 033 — approval is part of the product model.** Every piece carries approved, changed or in progress. Agents build only from approved pieces. Any command may still change a piece; that moves it back to changed by the fingerprint of its words.
- **The review tool is designed, not built.** A server Garura calls, kept in its own folder so it can move to Griffin. Intents and Product views, Final or Changes, Only changed or Everything, comments on words or an area, edits, and a Catch up mode that shows one change per card. Light only. Plan: `.garura/project/issues/617/specs/review-tool.md`; clickable mockup: `.garura/project/issues/617/specs/review-tool-mockup.html`.

## Stories filed

Under #594: #641 contract, #642 server, #643 reading, #644 acting (with Catch up), #648 open and listen, #649 send-back loop, #650 the review step.
Under #597: #645 approval states, #646 agents build only from approved, #647 spike on approval outside the review.
#613 (Kickoff) now ends with the review; #569 closed with a pointer.

Nothing is built in this change: it is documents and notes only.

Closes #617

## Self-review

Rules: base `standards/rules/self-review.md` (no project override). Findings that stop the raise: **none**.

**Scope**
- [PASS] Matches the issue: the answers are in ADR 032 and ADR 033; the stories are filed.
- [PASS] No scope creep: the two ADRs, one-line forward pointers on ADRs 026, 029, 030, 031 and the index, one edit to `docs/philosophy/idsd.md`, and notes under `.garura/project/issues/617/` and `.garura/project/issues/_adr/`.
- [PASS] Size: +3329 / −8 across 39 files, but about 90 % is notes (incl. the 1069-line mockup). The decision text to read is 271 lines.
- [PASS] No stray artifacts.

**Quality**
- [PASS] No runtime code; the ADR lint passes on both ADRs.
- [PASS] Commits are conventional, one concern each, and name #617.
- [PASS] No secrets (only the word "token" in design prose).
- [PASS] Docs in step: older ADRs point forward; a fresh index rebuild matches the committed index.
- [PASS] No merge conflicts with main.

**For the reviewer**
- ADR 032 and ADR 033 read Accepted. Kapil accepted both by typed word during `/adr` (run records under `.garura/project/issues/_adr/20261017-102548/decision.yaml` and `.garura/project/issues/_adr/20261018-063523/decision.yaml`).
- ADR 033 amends ADR 032 in the same branch, so a reader meets both at once.
- The commit-change run for the last two note commits closed HALTED: its run record went to a git-ignored folder instead of `context/commits.yaml`. The commits themselves are fine (tree clean, nothing pushed by it). The record was not recreated by hand.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
