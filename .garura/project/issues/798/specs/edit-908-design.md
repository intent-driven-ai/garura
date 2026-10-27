# Design draft: #908, `/shape-slice --edit`, with the shared part of #905

Status: draft for the product owner; nothing is built. 2026-10-27.

## What the person gets

`/shape-slice #788 --edit: <their words>` changes named parts of the slice that already exists, and
nothing else:
- the slice record: its name, outcome, or the tester's action;
- the slice's hidden file: the "when", "way back" or "who fixes" of named failure lines;
- a part's spine one-line (this takes in the earlier rule that a fill may replace a one-line).

## How a run goes (a separate edit path in the play)

1. start-change opens the change, as today.
2. The play reads the records the slice has (the slice record, the hidden file, the spine entries).
3. A skill turns the person's words into an exact list: for each change, the file, the part (for
   example "hidden file, fn-818, F8, who fixes"), the old text and the new text. The skill never
   changes anything; it only writes the list.
4. The brief shows the list: each changed line, old and new, and each other record the edit makes
   out of date (for example, an eval scenario that tests that line), named but not changed.
5. The pinned checkpoint: yes, change or stop. Nothing is written before the yes.
6. A script applies exactly the list, and refuses a line whose old text no longer matches.
7. A check compares each record before and after and refuses any change that is not on the list.
   Then the model check and the write guard run, as today.
8. The commit, and a history line on the record (who asked, when, their words). The end sequence
   lands the change.

The shaping steps (the gather, the questions, the shape, the reuse) do not run in an edit.

## What goes in the play's ICE (through /edit-play)

- A constraint: an edit starts only from a person's `--edit` words; it changes only the parts on
  the list the person saw and approved; every other line stays word for word.
- A failure condition: a change outside the list, an edit with no yes, or an edit of something the
  rule never edits.
- Its recovery: put back each change outside the list; nothing is kept without the yes.
- A scenario: an edit of two "who fixes" lines changes those two lines and nothing else.
- `--redraft` is removed from the play, its script and its test.

## The shared part (#905) that --edit needs

- The rule page: what an edit is, the command, what is never edited (eval files, accepted ADRs,
  code), the history line.
- The skill that turns the person's words into the exact list, shared by every play in #904.
- The two scripts, shared like the other shared scripts: apply the list, and check before against
  after.
- An ADR, through /record-decision.

## Where it is built

On the #798 branch, in the same change (PR #900): `/shape-slice` exists only on the plan 788 line,
not on main, so `--edit` replaces `--redraft` where it is. The six "who fixes" lines already fixed
stay as they are.
