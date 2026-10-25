# Build contract — #884, the content judge settles

The product owner approved this design on 2026-10-25: (1) a pass is kept while the page, its
parent page and the guidance do not change; (2) a fix round checks the fixes it was given, and
judges new points only on the lines that changed; (3) a new point on text that did not change
is a note, shown to the person at the checkpoint, and does not stop the run.

This contract covers the gate script, the judge skill and the rule. The two plays that call
the judge (`/discover-capabilities`, `/discover-domains`) change through `/edit-play`, not here.

## 1. The gate — `grounding_gate.py`

Canonical copy: `core/components/plays/discover-capabilities/scripts/grounding_gate.py`. Copy
it unchanged over every other copy (`find core/components -name grounding_gate.py`; 10 today).
Add a test file `test_grounding_gate.py` beside the canonical copy only.

### Command lines

```
grounding_gate.py --verdict V                                    # unchanged: all-pass, no state
grounding_gate.py --verdict V --state DIR --doc D --guidance G [--parent P]
grounding_gate.py kept  --state DIR --doc D --guidance G [--parent P]
grounding_gate.py prior --state DIR --doc D
```

The old use (no `--state`) must behave exactly as today: same output keys, same exit codes.

### The judge state

`DIR` holds one JSON file for each judged doc (name it from a hash of the doc path). It keeps:
the doc path; the fingerprint at the last verdict; whether the last verdict passed; the last
failures (`id`, `evidence`, `fix`); the doc's full text at the last verdict (the snapshot); and
the notes of the last verdict. Write it through a temp file and a rename.

The fingerprint is the sha256 of the doc's bytes, the parent's bytes (empty when no parent)
and the guidance's bytes, in that order, kept apart so a byte cannot move from one to another.

### `kept`

Prints `{"kept": true|false, "fingerprint": "<sha256>", "reason": "<plain words>"}`. Exit 0
when the state holds a passed verdict with the same fingerprint (the play then does not
dispatch a judge for this doc); exit 1 otherwise. A missing state folder or file is exit 1,
never an error.

### `prior`

Prints `{"round": "first"|"fix", "prior_failures": [{"id", "evidence", "fix"}]}`, exit 0.
`first` when the state has no record for the doc; `fix` otherwise. After a pass,
`prior_failures` is empty (the round is still `fix`).

### The gate with `--state`

- **First round** (no record for the doc): all-pass over the five criteria, as today.
- **Fix round** (a record exists, passed or failed):
  - The verdict must hold `prior`: one entry `{"id", "fixed": true|false, "evidence"}` for each
    of the record's last failures. A last failure with no entry fails closed (it is a failure).
    An entry with `fixed: false` is a failure.
  - A criterion that fails in this verdict is a **note**, not a failure, only when its
    `evidence` holds at least one quoted fragment (text inside straight double quotes `"…"`)
    and every fragment is found in the snapshot. Split a fragment on `...` and `…` and require
    each part. Compare after collapsing runs of whitespace to one space. Otherwise — a
    fragment not in the snapshot (changed or new text), or no quoted fragment at all — it is a
    failure.
- The doc passes when there is no failure and no missing criterion.
- Output: `{"ok", "overall", "doc", "round", "failures", "notes", "missing", "fingerprint"}`.
  `failures` and `notes` items are `{"id", "evidence", "fix"}` (a prior entry's failure uses
  its own id and evidence). Exit 0 pass, 1 fail, 2 usage or parse error.
- After the gate decides, write the record: the new fingerprint, passed or not, the failures,
  the snapshot (the doc's text now) and the notes.

### Tests (`test_grounding_gate.py`)

Cover: the old use unchanged; a first-round fail is recorded and `prior` lists it; a fix round
with every prior fixed and a new point on unchanged text passes with one note; a prior marked
not fixed fails; a missing prior entry fails closed; a new point on changed text fails; a new
point with no quote fails; a passed page is kept three times with one fingerprint; a changed
parent breaks the kept pass; after a pass, `prior` reads a fix round with no failures.

## 2. The judge skill — `core/components/skills/judge-grounding/SKILL.md`

- New optional input `prior_failures`: the list the play got from `grounding_gate.py prior`.
- When it is given (a fix round), the judge also writes `"prior": [{"id", "fixed": true|false,
  "evidence"}]`, one entry for each prior failure, saying only whether the cited fix was made,
  with a quote of the text that shows it. It still scores the five criteria.
- Every `evidence` quotes the doc's exact text inside straight double quotes, so the gate can
  find it. Several quotes may be given; join them with a space.
- Keep the five criteria, the clean-context rule and "the judge never decides pass or fail".
- Update the verdict shape block to show the optional `prior` array.

## 3. The rule — `core/components/memory/standards/rules/grounding-eval.md`

Add a section on how the gate settles: the kept pass (by fingerprint of doc, parent and
guidance), the fix round (prior failures checked; new points judged only on changed text), and
the notes (new points on unchanged text; shown at the checkpoint; they never block). Keep the
all-pass rule for the first round.

## Checks the build runs before it reports

- `python3 -m unittest test_grounding_gate` beside the canonical copy passes.
- Every `grounding_gate.py` copy is byte for byte the same.
- `node core/tools/lint-components/index.js --target core/components` from the repo root: no
  error in a new or touched file.
- No absolute home path and no real name in any changed file.

## Round 2 (review of PR #885; decision 2: fix all seven)

The plays (`/discover-capabilities`, `/discover-domains`) again change through `/edit-play`, not here.

- **A (P2) — the gate decides, not the judge.** In a fix round, a prior failure counts as fixed
  only when all three hold: the prior entry says `fixed: true`; the doc's text changed since the
  verdict that failed (compare with the snapshot); and the entry's `evidence` holds at least one
  quoted fragment, each found in the doc's current text. Otherwise it is a failure. Tests: an
  unchanged doc with `fixed: true` fails; a quote not on the current page fails; a changed page
  with a quote of the new text passes.
- **D (P3) — a stricter judge ends old passes.** Add `--judge J` to the gate (with `--state`)
  and to `kept`: the judge skill file whose bytes join the fingerprint (doc, parent, guidance,
  judge, kept apart). A changed judge file ends the kept pass. Tests.
- **F (P3) — a script collects the notes.** New command `grounding_gate.py notes --state DIR
  --out FILE`: writes `{"notes": [{"doc", "id", "evidence", "fix"}]}` with every note held in
  the state's records (passed and kept docs included). `kept` also prints the record's stored
  `notes`. Tests.
- Copy the canonical gate unchanged over every other copy again.
- **B (P3)** — `grounding-eval.md`, "How the judge runs": in a fix round the judge also gets its
  own earlier failures for that doc (`prior_failures`), and only those; still no brief, no
  author reasoning, no gold example. Say why this keeps the clean-context aim (the failures are
  the judge's own words, not the author's).
- **C (P3)** — `standards/schemas/product-os/grounding/_content-standard.md`: where it says a
  doc failing any line is rejected, add that a fix round follows the settling rule in
  `standards/rules/grounding-eval.md`: a new point on unchanged text is a note, shown at the
  checkpoint, not a reject.
- **D (rule)** — `grounding-eval.md`: the fingerprint includes the judge's own text; a
  calibration run uses no judge state (every doc is judged fresh).
- **E (P3)** — `judge-grounding/SKILL.md`: name the shape of the prior file the play hands over
  (`{"round": "first"|"fix", "prior_failures": [...]}`), say the play hands it only when `round`
  is `fix`, and that a `first` round is judged as today.
- **G (P4)** — `grounding-eval.md` title: v2 (from v1).

### Checks the build runs before it reports (round 2)
- `python3 -m unittest test_grounding_gate` passes, with the new tests.
- Every `grounding_gate.py` copy is byte for byte the same.
- Component lint: no error in a new or touched file. No home path, no real name.
