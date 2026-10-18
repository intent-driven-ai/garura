## What this delivers

**Every decision an agent makes keeps its trace.** A trace is the steps the agent took, in order. Each step says what the agent looked for, what it found, and the memory lines that said so: the tier (short-term, Garura or Phoenix memory), the file, the lines and a fingerprint of that text. A sign-in decision, for example, reads the product's profile (who the users are), the domain that covers sign-in, the profile's security level and compliance, and then the knowledge lines those values select. The record keeps the exact text, the memory version, and up to three lines around each source, so a person sees every step in its place.

Kapil, 2026-10-19: "the issue is you are showing 1 or 2 lines, which leave no context. the source should show a few lines before and after and then the part of section which influenced should be highlighted... it will be multiple... a project profile, domain, its security level and then the file where knowledge is put... these are called traces".

- **The memory tool** (`core/tools/memory/citations.py`) gains `cite` and `citations`. `cite` reads every source first and refuses one that is gone (`not_found`) or changed (`changed`). A decision from an approved memory update names it, and the update's written file is the source of a step. `citations --check` reads every step's source again: no trace, a source that is gone, and a source that changed are each a problem, named by its step, with the lines as they are now. Decision records and waiting drafts are never found by a lookup.
- **Contract version 4** (`core/tools/memory/contract/v4.json`; versions 1 to 3 kept unchanged), with its check, samples and broken samples.
- **The drive review record** (`write_drive_review.py`, canonical plus the `/vision` and `/understand` copies) takes `--decisions`, and refuses decisions of another play or issue.
- **The resolution rule** gains a "Decision Records" section. At landing it is also promoted to Phoenix memory.
- **The review tool's design and mockup** (`.garura/project/issues/617/specs/`): five sections, Intents | Product | ADRs | Memory (with a mocked plain-words "Ask memory") | Agent decisions. Agent decisions shows each decision's trace, step by step, with the source lines numbered and the used lines marked; a changed step shows what the lines say now. Its data is the memory tool's real output: 12 decisions over a sample shop's profile and real Phoenix memory lines (`.garura/project/issues/659/evidence/make_decisions.py`, `decisions.json`, `updates.json`). Mock only; the tool is built in the #606 plan.

What this does not do yet: no agent calls `cite`, and no play passes `--decisions` (agents move over in #661 and #663). The old R1 to R4 trace in the resolution rule is not rewritten here. The check proves the named lines still say what they said; it does not prove the answer follows from them.

Closes #659

## Where the issue text no longer matches

| Issue says | What happened |
|---|---|
| A decision names "the tier, the file, the lines and a fingerprint" | A decision keeps a trace of steps, each with its source, the exact text, the version and the lines around it (Kapil, 2026-10-19: "these are called traces") |
| The review tool is not in this story | The diff carries the review tool's five-section design and a mock of Agent decisions and Ask memory, on Kapil's word of 2026-10-18/19 ("design the interface and create some mocks for now. no need to build this whole this now"); about 28% of the diff |
| A script checks each named source | `citations --check` in the memory tool, with problems named by step |

## How it was checked

- Memory tool: 130 tests pass (61 tool, 13 pull, 56 contract). The contract check passes: 26 samples valid, 32 broken samples refused, no boundary problems.
- Drive review record: 32 checks pass; the three copies are identical.
- `lint-components`: 116 findings, the same as on main; none in a changed file.
- The three plans (#659, #653, #606) are valid; the #659 plan closes in the last commit before the merge.
- The evidence script re-runs to the same 12 records and 3 problems.
- Merges cleanly with main. No client, personal or secret text.

## Self-review

The full self-review is in `.garura/project/issues/659/context/self-review.md`: 0 blocking, 13 notes.

Fixed after the self-review: one unreadable line in an issue's decision records now answers `unreadable` for that issue only, and no longer stops every other issue; a failed decision write names short-term memory; the drive record refuses another play's or issue's decisions; the README and two design lines describe the trace.

Carried: ADR 035 §6 and ADRs 032 and 036 still describe one source and a "Memory and ADRs" section (their own `/adr` change); four older commit subjects are 74 to 83 characters against 72.

Where to read: `core/tools/memory/citations.py`, the changes to `memory.py` and `contract/check_contract.py`, the lines of `v4.json` that differ from `v3.json`, the tests, the README, the resolution rule section, and one copy of `write_drive_review.py` (about 855 lines). The rest is the contract copy, samples, evidence, plans and the mock.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
