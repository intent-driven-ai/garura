# #798 + #898 — design, round 3 (for the product owner's yes)

One change pipeline run (one start-change, commit, review, merge) for the eval play `/shape-eval` (#798) and the new
story #898. Running them together saves the pipeline's cost; it says nothing about their plans.

## Decided by the product owner (2026-10-26)
- Encryption is dropped, and #828 with it, closed as not planned with its reason ("drop encryption and drop 828 ... this
  feature needs to be dropped with reason. dont reweite 828."). Everything (ICE, constraints, the model) is plain text; the
  goal is not to hide the eval. "Once the slice happens, we need an eval, and that eval is what we need to pass ... when
  the agents are building, they don't only think through the evals, but they look at the intent and build for that."
- Evals stay in the repo ("you guys can't sit outside").
- Rebuilding an eval is wrong: an eval is a fixed yardstick.
- The new story #898 ("Agents build for the business intent, not only to pass the eval") sits under epic #794. Done.

## Order of work
1. `/shape-slice 788`: add #898's feature ("the build is given the business intent, never the eval") under the eval
   capability, with its ICE, into slice `sl-intent-to-design`, with its hidden-file entry. Its checkpoint needs the
   product owner's yes. The plan file then marks #898 as that feature's story.
2. `/shape-eval` (#798, through `/create-play`): reads the epic, its stories and the hidden file only; writes one eval
   per slice into `plans/<plan>/evals/<slice>/`, in plain text; each check tests, from the outside through the usage
   guide, what the business intent promises; anything it cannot test yet is named; one pinned checkpoint.
3. #898: a lint check that no build play's inputs name the evals folder, the eval or the hidden file; a check over a build
   session's ledger that flags a read of the evals folder (it flags, it does not block), with tests.
4. The rules: ADR 049 ("Encrypting the evals is #828") and `docs/philosophy/idd-principles.md` ("the evals are encrypted")
   say instead that the build is given the intent, never the eval (through `/record-decision`, amending ADR 049);
   the ontology and `managing-work.md` match.
5. #798's GitHub text drops its "encrypting it (#828)" line.
6. Land through the change plays.

## Out of scope
Running the eval (also on Griffin); where a handoff plan is kept; the loop's one checkpoint (#796); blocking reads by
hook (#893).
