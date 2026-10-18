# Memory review — what the Kickoff plays answer from

#613, plan item 2. Written 2026-10-18, after ADR 034 was accepted and before the
runner is designed. Kapil: "Before we build the drive, we need to review the
memory mechanism and make sure it is done absolutely correctly."

## The short answer

Memory is not ready for ADR 034. ADR 034 says a play inside a drive answers its
questions from memory and names where each answer came from. Today three things
stop that:

1. **The plays read three different copies of Garura's long-term memory, and two
   of them are out of date.** One run can read rules from one copy, templates
   from another, and the knowledge base from a third.
2. **Two of the five kinds of memory ADR 034 names cannot answer a question.**
   The "learned checkpoint answers" hold no answers, only yes/no verdicts on
   checkpoints, and the file does not exist yet. The prototype's sources are
   saved by `/intent` and then never read again.
3. **Nothing can record where an answer came from.** There is no shared shape
   for "an answer and its source", no place for it in the drive's review
   record, and two scripts reject any answer that did not come from a person.

None of this is hard to fix. But every later item in the plan rests on it.

Kapil, 2026-10-18: Griffin is not built yet, but a lot of this will go into
Griffin later. So whatever is fixed here is kept in one place, behind a small
written contract, so it can move — the same rule as the review tool
(`.garura/project/issues/617/specs/review-tool.md`).

## Each kind of memory, as it stands

| Memory (ADR 034 §2) | Can a play read it in a drive? | Is it current? | Can an answer name it as its source? |
|---|---|---|---|
| The drive's up-front answers (contract `answers`) | `/understand` yes; `/vision` keys unsettled; `/intent` never reads them | yes | no — no question ids for `/intent`; `/understand` stamps them as typed by a person |
| The prototype's sources | only `/intent`, which wrote them | yes, hashed | partly — a file path, but sources link to every intent of the run, not the one they support |
| The product model | yes | yes, but no approval states yet (ADR 033 unbuilt) | yes for intents and spine ids; no for ICE lines; page paths move |
| The knowledge base | `/vision` and `/understand`; not `/intent` | depends which copy is read | no — its node ids renumber on every rebuild; citations are free text no check looks up |
| The learned checkpoint answers | — | file does not exist | no — it holds checkpoint verdicts, never answers to questions |

## What is broken

**The copies of long-term memory**
- Three copies exist: the source (`core/components/memory/`, 151 files), the
  project copy (`.garura/core/memory/`, 41 files, last written 30 May, git
  ignores it), and the machine copy (`~/.garura/core/memory/`, 241 files).
- ADR 015 says plays read the machine copy. But the close of 28 of 32 plays
  reads the project copy (`standards/rules/play-close.md:105-110`), which nothing
  writes any more (`install-garura/scripts/install.py:250-256`). In a project
  Garura is installed into, that copy does not exist at all.
- The machine copy is behind the source: no drive contract rule, ontology
  version 3 instead of 4, and two knowledge shelves deleted in #434 still served
  (`install.py` copies but never deletes).
- The knowledge-base skills hard-code the source path
  (`skills/search-kb/SKILL.md:20`, `skills/propose-kb-node/SKILL.md:28`), and
  `kb_search.py` looks in the wrong folder once installed (`:82`); a missing
  knowledge base returns an empty answer, not an error.

**Answers and their sources**
- `/intent` never reads the contract's answers, and its questions have no ids,
  so the drive cannot answer them up front (`intent/SKILL.md:85,100-101`;
  `skills/author-business-intent/SKILL.md:120-124`).
- `/vision` reads its goal from `inputs` in one place and `answers` in another
  (`vision/SKILL.md:134`; `play-creator/references/test_drive_contract.py:44`).
- `/intent`'s check accepts an answer only from the source or the person
  (`intent/scripts/check_intent.py:141`); `/understand` accepts a new
  capability's answers only from a person (`understand/scripts/persist_understand.py:99-101`),
  and stamps contract answers as a person's (`pick_targets.py:139`).
- `/intent`'s "where this came from" is a label the drafting agent writes about
  itself; no script checks it against the source or the answers, and it is
  never saved in the model (`check_intent.py:137-143`).
- The drive's review record has no place for assumptions or their sources, and
  is written only when a checkpoint would have waited; `/intent` writes none
  (`play-creator/references/write_drive_review.py:72-75`).
- The rule on reading memory still lets a play fall back to the model's own
  knowledge when memory has nothing (`standards/rules/resolution.md:71-74`,
  rule R4). That contradicts ADR 034 §3, which did not amend it.

**The prototype's sources**
- `/vision` and `/understand` never read them; `read_intents.py` passes on only
  an intent's outcome, why and stage — not its proof, who asked, or must-not
  (`vision/scripts/read_intents.py:34`).
- Every source links to every intent of the run, so nobody can tell which
  source supports which intent (`intent/scripts/persist_intent.py:365-383`).

## What is risky

- `/understand` picks every rough capability in the whole model, not only the
  drive's own (`pick_targets.py:113`).
- Nothing tells "written earlier in this drive" from "approved by a person":
  no drive id on any piece; a decision can read `accepted` with no person.
- `/vision`'s proposal for a new knowledge-base node rests on web research, not
  memory, and never reaches the drive's review (`vision/SKILL.md:262-264,450-454`).
- `config.yaml` names a `profile.yaml` that does not exist; the profile lives in
  the spine.

## What is fine

- Intent ids and spine ids are stable. Source snapshots are exact copies with
  hashes, committed on the drive's branch.
- The shared contract checker and review writer are identical in every play
  that has them, and a test enforces it.
- The knowledge base's architecture learnings (`kb-search`) have stable ids.
- Two ready-made pieces exist and fit ADR 034: a citation format
  (`resolution.md:87-93`: where an answer was resolved from, the source, the
  section) and a durable question store with stable ids and the person's answers
  (`standards/rules/product.md`, rule 12: `grounding-questions.md`, "questions
  answered in prior runs are not re-asked; the pipeline reads their answers as
  facts").

## What "done correctly" needs, for Kickoff

1. **One copy of memory.** Every play reads the machine copy, as ADR 015 says;
   the installer keeps it equal to the source (deletes what the source deleted);
   the project copy is retired.
2. **One shape for "an answer and its source"**: the question, the answer, and
   where it came from — which kind of memory, the exact file or id, and the words
   it rests on. Built from the existing citation format.
3. **Stable question ids** for every question `/intent`, `/vision` and
   `/understand` can ask, and a contract check that knows them.
4. **The plays accept answers from memory**, each with its source; a script
   checks every source exists; a play with no source asks.
5. **The review record carries every answer taken from memory**, for every
   play, including `/intent`.
6. **The "learned answers" are made real or dropped** from ADR 034's list.
7. **Rule R4 no longer applies inside a drive**: no fallback to the model alone.
8. **Pieces cited from the product model are cited by id**, not page path.

Left for later (or Griffin): stable knowledge-base node ids, the knowledge
base's index and staleness check, `review-change`'s missing review shelf, the
installer's config paths in installed projects, and approval states (ADR 033,
#645–#646).

## Sources of this review

Three read-only reviews on 2026-10-18 (the knowledge base and memory copies; the
product model and sources; contract answers, learned answers and answer
sources), with their main claims checked against the files.
