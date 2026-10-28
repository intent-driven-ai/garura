# #920 redesign: the Discovery loop's knowledge step

Status: proposed, waiting for the product owner's yes. Nothing is built.

## Today

When a round ends with open questions, the loop runs three plays one after another
(`/search-knowledge`, `/research-knowledge`, `/check-knowledge`). Each carries its own
pre-flight, loop-contract check, session stamp, stop condition and close, and each hands its
judgment to the same agent, `knowledge-builder`. Then the loop shows the brief and records the
reply with a script that lives in `/check-knowledge`'s folder.

## Proposed

One step of the loop, "close the open questions", run by `knowledge-builder` through one
contract. No plays.

| Today | Becomes |
|---|---|
| `/search-knowledge` merges repeat questions (`group_questions.py`) | a loop script, `group_questions.py`, in the loop's `scripts/` |
| `/search-knowledge` answers from the prototype (`find-answers-in-sources`) | the agent calls the same skill |
| `/search-knowledge` looks in memory | the agent calls the memory tool directly (`search`, `find`, `read`, `cite`); no skill |
| `/research-knowledge` researches outside the repository (`author-knowledge-page`) | the agent calls the same skill; the skill only drafts the page, and the agent raises it with the memory tool's `propose` (today the skill calls `propose` itself, against the memory rule) |
| `/research-knowledge` drafts answers only a person can confirm (`propose-answers`) | the agent calls the same skill, unchanged for `/shape-slice` |
| `/check-knowledge` writes the brief (`author-knowledge-brief`) | the agent calls the same skill; "the knowledge brief" |
| three check scripts | one loop script, `check_knowledge.py`, with the same checks; the loop runs it after the agent and sends a failure back at most twice |
| `record_review.py` in `/check-knowledge`'s folder | a loop script |
| waiting memory updates listed four or five times | listed once, by the agent through the memory tool, and once by the check script (read-only, as ADR 042 allows) |
| `round_state.py` reads memory-update files by path | asks the memory tool (`updates`) |

Removed: the three play folders, their stop conditions and stamped scripts; the loop's
"member plays" in `loop_preflight.py`, `lint_loop.py`, `pipeline-next.md` and the loop docs.

## Where it lands

- The decision: `/record-decision`, amending ADR 042 (and ADR 041 §3-4).
- The loop: `/edit-loop complete-discovery` (an intent change: its C5 names the plays).
- The shared loop run (`loops/_shared/loop-run.md`, R5b/R5c) and `create-loop`'s references and
  example loop: direct edits, since they are shared scaffolding.
- The agent and the research skill: direct edits.
- Tests, linters, installer lists, rename map, glossary, docs, the Current Commands page.

## Found on the way

- `/research-knowledge` and `/check-knowledge` write their done records under their old names
  (`stop-condition-build-knowledge.yaml`, `stop-condition-review-knowledge.yaml`), so the loop's
  done check cannot find them. The redesign removes the cause.
- `propose-answers` says it drafts from memory, but in this flow it is handed no memory.
