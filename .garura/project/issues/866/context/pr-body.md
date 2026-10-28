The current /shape-slice ran again on business intent #788. The slice `sl-intent-to-design` already served #788, so the play took its reuse path: it kept the slice unchanged and made no second slice. Its output is the input for testing the plan play (#818).

Closes #866.

## What the run did

- **Reused the slice, unchanged:** the same 3 features in build order (fn-795 /shape-slice, fn-818 /shape-plan, fn-798 /shape-eval), the same surface (the Claude Code command line), the same tester (the product owner). `find_serving_slice.py` matched it; `author-slice` (reuse mode) pulled in nothing and pushed out nothing.
- **Kept the hidden file as it was:** 3 entries, 18 "Fails if" lines (9 the builder can fix alone, 9 for a person).
- **Brought 6 used pages up to the current rule.** The model check found that the slice's 3 features and their 3 capabilities carried an old form of the Thin line (from the hand fix in #844). `author-slice` (fix mode) listed them as thin, and `persist_fills.py` wrote the current Thin line just before each ICE section. That is the only model change (6 files, 7 lines).
- **The checkpoint:** the product owner said yes and answered the two open questions. Q-change-1: no duplicate stories; a feature that leaves the slice has its story moved out of the plan, not deleted. Q-evalformat-1: as proposed. The Q-change-1 answer is now in #818's "done when".

## Checks

| Check | Result |
|---|---|
| Model check (`slice_check.py`) | valid; 0 problems in the slice's own pages, 0 new; 70 older problems in pages the slice does not use |
| Hidden file check | ok; 3 entries, working copies cleared |
| Write guard | ok; 6 pages changed, all allowed, 0 outside the set |
| Live trace check | 7 live decisions, no changed source |
| Brief check | ok |

## Found on the way

- #867: the agents' copy script refuses reads from short-term and Garura memory (they give no version).
- #868: the current ontology and other current standards are in no memory tier.
- The brief's "Kept slice" line says "this run only adds the intent", also when the run adds nothing.
- The intent page's title ("Agents design a named piece of work") differs from the plan file and the issue.
