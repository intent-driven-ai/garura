Harness verdict (gate off per gates.plays.check-change): approve

No blocking finding. test_change_lines 10 OK; test_platform_adapter 55/55; the 7 adapter copies and 3 safe_write copies are identical; lint-components: 37 violations, all there before, none in this change; lint-play not applicable (no play changed). This is a recorded harness verdict, not a human review.

**Findings — {'P2': 1, 'P3': 6, 'P4': 8}**

P2:
- **QF-01** (code-and-tests) The all-or-nothing promise has holes. Only OSError is caught in the write loop, so any other failure on page 2 leaves page 1 already changed with a traceback and exit 1 (the module says exit 0 or 2 and 'any failure ... writes nothing'). Run

P3:
- **QF-02** (code-and-tests) 'Keeps every other line word for word' is not true for some pages. The page is read with universal newlines and split with str.splitlines(), then joined with "\n". Run: a page with CRLF endings came back entirely LF (every untouched line ch
- **QF-03** (code-and-tests) An {after, add} change is not idempotent. Run: the same request sent twice put the added line on the page twice. {old, new} is safe (the second run refuses because 'old' is gone), so a retried run after a lost report adds duplicates only fo
- **QF-04** (code-and-tests) The ten tests pass and assert real outcomes, but the branches the script advertises as its safety net have no test: the put-back when a write fails part way (change_lines.py 166-170, the branch QF-01 shows is incomplete), the refusal 'a lin
- **H-1** (harness) The new named-lines step lets a request replace a line or remove it (`new: null`) on any page, but the skill keeps its older, stricter rules unchanged beside it: step 7 says every section and line from step 1 must still be on the page and b
- **H-2** (harness) Two statements about who makes lines-request.json disagree. The Input table lists `lines_request` as a field handed to the skill, but step 5 tells the skill to write each line into lines-request.json itself and then run the script. In this 
- **F1** (product-model) The Limit of both pages says 'Nothing is written before a plain approved', and cap-720 'Fails if' says 'a plan is changed anywhere but on its own branch'. Yet both pages also let the play cut a missing plan branch first, and that step (main

P4:
- **QF-05** (code-and-tests) atomic_write does not fsync the temp file before os.replace, so the 'old file whole or new one whole' promise holds for a process that stops but not for a power cut (the new name can point at an empty file). _mode_for reads the umask by set
- **QF-06** (code-and-tests) Seven platform_adapter.py copies and three safe_write.py copies are kept equal by hand. They are byte-identical now (md5 checked), but no test or linter in core/tools compares them, so the next one-copy edit would drift silently. create-pla
- **QF-07** (code-and-tests) plan_page is about 55 lines with a branch chain that does planning, validation and rendering in one function; the 'basename == _spine.yaml' test on line 85 can never be true after the '.md' test on the same line, so it is dead code. The ' "
- **H-3** (harness) The `out` input still says it is where `grounding-report.json` is written, while a named-lines request writes `lines-report.json` (the script's `--out`). The Output section says "instead" but the one `out` field the agent passes is not desc
- **F2** (product-model) The new 'Directional intent' is one long run-on sentence of about 90 words with a colon list, and it says what the capability does but not why it matters. The capability template asks for what it is about, its rough scope and why it matters
- **F3** (product-model) The page title uses a dash ('The /update-plan session - instructions, checks, one approval, one landing on the plan's branch') while the spine one_line, the plan 717 title and the #730 issue title use a colon. On base the page title was ide
- **F4** (product-model) There before, not changed by this PR: the feature page holds only 'What it does' and the ICE. It lacks the required feature sections (Inputs / Outputs, Rules & behavior, Acceptance criteria, Out of scope), so lint_grounding.py gives 4 error
- **F5** (product-model) There before, not changed by this PR: both pages keep the ICE inline as an 'Agent intent (ICE)' section with the old labels (Goal, Limit, Fails if, Checked by). The ontology on the base (version 13) and ADR 047 make the ICE its own page wit

**Routing:** approve → `/merge-change` onto `plan/717/base`. The product owner decides whether QF-01…QF-04 and H-1…H-3 are fixed in this change before the merge.
