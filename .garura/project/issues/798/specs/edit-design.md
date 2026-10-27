# Design draft: one standard way for a play to edit a record that already exists

Status: draft for the product owner; nothing is built. 2026-10-27, from the PR #900 round 3 review.

## The problem

Every play that writes the product model or the work items is add-only by design ("keeps what is
there"), so it never overwrites what a person confirmed. When a person wants to change a record
that already exists, no play can. Change #798 hit this four times: the proof line of intent #788
(#901), two spine one-lines, the slice's name, and six "who fixes" lines of the hidden file. Each
time it was patched a different way: a new rule in one play, a script change, a hand edit, and the
`--redraft` option that the review raised to P1.

## The proposal

1. One word for it: **edit**. Garura's names already use "edit" for "change a thing that exists"
   (`/edit-play`, `/edit-loop`, `/edit-ontology`). "refactor" means a new shape with the same
   meaning, which is the wrong word for a content change. "redraft" names how the text is made
   and suggests the whole record is rewritten.
2. How a person asks: the play's usual command, then `edit:` and their words, for example
   `/discover-intent 788 edit: the proof line should say …`. The play's skill turns the words into
   an exact list of what changes (record, section, line) and shows that list back.
3. The rules every such play follows, kept in one shared rule file:
   - Only a person starts an edit. A play never edits a confirmed record on its own.
   - An edit changes only what the person named; every other line stays word for word. One shared
     script compares before and after and refuses any other change.
   - Show before write: one brief with each changed line, old and new, and each other record the
     edit makes out of date (named, not changed). Nothing is written before the person's yes.
   - The record keeps a history line: who asked, when, and their words.
   - Never edited: eval files (a fixed yardstick, only added to), accepted ADRs (a new ADR
     supersedes them), and code.
4. Plays that get it: `/discover-intent` (business intents, #901), `/discover-domains` (domains),
   `/discover-capabilities` (capabilities, features and their ICE), `/shape-slice` (the slice
   record and the hidden file's entries), `/shape-plan` (the plan file, the epic and story text).
   Not `/shape-eval`, not `/record-decision`.
5. How it is built: an ADR through `/record-decision`; the shared rule and script in the standards,
   promoted to Phoenix memory; each play through its ICE and `/edit-play` (one constraint, one
   failure condition, one recovery, one scenario); `/create-play` learns it for new plays.

## What happens in #798

- Take back the `--redraft` commit (d756e304). The six "who fixes" lines (8fceddab) stay; the
  product owner approved them.
- The edit design is its own work, filed on its own, not inside #798.
