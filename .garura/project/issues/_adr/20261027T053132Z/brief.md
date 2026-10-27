# Decision brief

## Decision

In `/shape-slice`, a slice in progress (its epic is past ready: a story is started or done) is never reworked by a shaping run. But a person's edit, `/shape-slice #<intent> --edit: <their own words>`, which they see and approve, may change it. The edit brief then says that the slice is in progress, and names its epic, with its status, as out of date (named, not changed).

## Why now

The edit option (#908, business intent #904) lets a person change a slice that exists. The play's rule said a slice in progress is never touched, so an edit could not fix a slice once its build had started, which is exactly when a wrong "who fixes" line or a wrong name is found. The review of PR #911 found the edit path did not check the rule, and the product owner decided to allow the edit.

## Options considered

- Refuse an edit on a slice in progress, so it changes only after its work ends or through a new slice. Lost: the person could not fix a mistake in a slice while it is being built, when the mistake matters most, and a new slice for a one-line fix is far more work.
- Allow the edit with no warning. Lost: the person would not know that work already started from the old text, so nothing would make them check it.
- Allow the edit, and say so in the brief and name the epic as out of date (chosen): the old rule protects work in flight from silent change; an edit is never silent, because the person sees each change and types yes.

## Decided by

The product owner, 2026-10-27: "yes we need to allow slice to be updated even when in progress."

## Decided in

Change #908 (business intent #904), PR #911 into plan/788/798-shape-eval. The rule lives in the `/shape-slice` play's intent: `core/components/plays/shape-slice/reference/ice.md`, C7, C20, F7 and F20.

## Shape

markdown (a Garura framework decision, docs/adr/)
