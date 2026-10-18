# Brief — inside a drive, a play answers from memory and asks only when memory has nothing

Shape: markdown (a framework decision, `docs/adr/`).

## Decision

Inside a drive, the plays run with a high level of autonomy. When a play reaches a question it
would ask a person, it answers it from **memory and from what the system gives it**, and may
assume from them. It does not stop and ask at every point. It asks the person **only when
nothing in memory or the system supports an answer.** It never answers from the underlying
model's own knowledge with nothing behind it.

Kapil, 2026-10-18, in his own words:

> These three players internally have to run with a high level of autonomy: wrapping things
> up, taking care of any domain capabilities, and understanding what to do together. They
> should not stop and ask for every single point in time in review, but really decide when
> they cannot come up with an answer.
>
> It's okay to take assumptions based on the memories that are given to them because there is
> a memory element to it, but they cannot fabricate and create some things completely from
> scratch. If they have no information about the memory or anything that the system has
> provided, then they should definitely ask.
>
> In other words, reading the memory, making decisions from there, and coming up with things
> is absolutely okay. If you do not give any direction from the user or the memory, going to
> the underlying LLM and making a decision is the wrong move.

What counts as memory and what the system gives, as the plays have it today: the answers the
drive gathered before it started (the drive contract's `answers`), the sources the person gave
(the prototype and its saved snapshots), the product model, the knowledge base, and the
learned checkpoint answers.

Every answer a play takes this way is recorded with where it came from, so the drive's review
(ADR 032) shows the person what was assumed and on what basis. An answer with no source is not
allowed: that question stops the drive and goes to the person, as ADR 029 §2 says today.

This changes ADR 029 §2 ("A new question stops it … It never picks an answer for itself"): a
new question stops the drive only when memory and the system hold nothing to answer it. It
changes rule 4 of the drive contract (`core/components/memory/standards/rules/drive-contract.md`,
"a question the drive did not answer stops the play") the same way.

## Why now

The Kickoff drive (#613) is built next. A read of its three plays inside a drive (18 October)
found that `/intent` asks every open question it finds in its draft one at a time, up to three
rounds, and that these questions come out of the draft, so they cannot all be asked before the
drive starts. Under ADR 029 §2 and the drive contract's rule 4, each one would stop the drive.
Kickoff would stop on nearly every run, and the plays would not run on their own as Kapil
wants. The rule must be set before the runner and the play fixes are built (#613 plan,
items 1 to 3).

## Options considered

- **Keep ADR 029 §2 as it is: every question not answered before the drive started stops it.**
  Lost: the plays would "stop and ask for every single point in time" (Kapil), and Kickoff would
  stop on nearly every run.
- **Let the play answer every question itself, from the model's own knowledge.** Lost: it
  fabricates. Kapil: "going to the underlying LLM and making a decision is the wrong move."
- **Answer from memory and the system, record where each answer came from, and ask only when
  nothing supports an answer.** Chosen.

## Decided by

Kapil Ahuja, 2026-10-18.

## Decided in

#613 (the Kickoff drive), plan item 1 (`.garura/project/issues/613/specs/plan.md`), under #594
and business intent #606.
