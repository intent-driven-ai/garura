# Decision brief

shape: markdown

## Decision

A business intent and ICE are two different levels. The person's Business Intent sits above:
what they want for the business, with why it matters and the proof it is met; only a person
confirms or drops it. ICE sits below: one per separate thing the person must see, decide or
do, built from a business intent.

No play owns a kind of thing in the product model: any play may write the intents, ICE or other
kinds it finds, in any order, inside its own declared write scope. The ontology's rules say what
holds once aligned and never block a write; an Alignment drive fixes drift later.

ICE is placed at once: written inline on a proposed capability, even before the capability has a
domain; /vision attaches the domain later. The grounding linter warns on a missing domain instead
of failing.

An ICE is workable only when it is built from a confirmed business intent; otherwise it is kept
but no play works on it.

Inside a drive, /intent does not stop for approval: it saves intents as proposed, and the person
confirms them at the drive's final review. Run by hand, /intent asks the person to confirm before
it saves — and so it confirms before it writes.

## Why now

Two trials of /intent on a real prototype showed one intent in ICE form collapses several
wants into one shallow line, and that the business intent sits one "why?" above what a prototype
shows. A first fix used separate unplaced ICE files, which the product model's spine no longer
allows.

## Options considered

- One intent per run, in ICE form — collapses several wants into one shallow line.
- Separate unplaced ICE files — the spine retired separate ICE files.
- Refuse to write an ICE with no business intent — blocks the write; keeping it but refusing work is as safe.
- A stored "workable" status field — can drift from the link; deriving it cannot.

## Decided by

Kapil

## Decided in

#612 (the /intent play) and the review of PR #631
