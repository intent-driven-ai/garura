# Locked model — #758 (agreed with the product owner, 2026-10-22)

The product owner rejected the first questions draft ("these are all relationships we build into ontology ... show me the context or part of ontology") and agreed this view instead. It replaces draft-questions.md as checkpoint 1. The tests (questions Q8 onward) follow from it and go into the ontology unreviewed.

## The tree

Business intent      hypothesis · boundaries · rules · its capabilities
└─ Capability        serves one or more business intents · has one ICE
   └─ Functionality  has exactly one parent capability · has one ICE
      └─ Work        Story (builds it), and Spikes, Bugs, Chores under it

## The links

| From | To | Count | Meaning |
|---|---|---|---|
| Capability | Business intent | N:N | A capability serves one or more business intents; a business intent has one or more capabilities |
| Functionality | Capability | N:1 | A functionality has exactly one parent capability |
| ICE | Capability or Functionality | 1:1 | Each capability and each functionality has exactly one ICE |
| Work | ICE | N:1 | An ICE can have many pieces of work |
| Capability | Capability | N:N | "needs" (the other must be done first) and "identified by" (the other led us to find this one) |
| Functionality | anything | none | A functionality never needs anything and is never identified by anything; its order of work comes from its parent capability |
| Domain | Business intent, Capability | N:N | Loose link, for search only; never in a plan, never a stop |

## The ICE

- Its own page and its own spine entry.
- Three parts: Intent (goals, limits, fails if); Context (the rules for the sub-agent: what to read, what never to read, the persona, the scope); Expectation (scenarios, done means, quality needs).
- No link to a business intent. Its business intents are found through its part; a functionality's ICE goes through its parent capability.
- When a second business intent changes a capability, that one ICE is updated to cover both.

## The ready check, on each ICE

- Ready: its capability serves a confirmed business intent, every capability it needs is done, and the ICE has all three parts. Work starts.
- Partly ready: as ready, with gaps that do not stop work (no domain, no "identified by", a thin part such as an empty Context). Work starts; the gaps are listed.
- Not ready: no confirmed business intent, or a capability it needs is not done. Work stops; the page is kept.

## What changes from version 5

- A business intent holds no ICE; Garura never works on a business intent directly.
- The ICE leaves the capability and functionality pages and becomes its own node.
- "needs" and "identified by" join capabilities only.
- The ready rule moves to the ICE, with three answers.
- Garura's own model: fn-727 → fn-724 becomes cap-718 → cap-723 (the move is #765).

## Decisions behind it

- Option 1 (one ICE for each capability or functionality) replaces the earlier 1.B (one ICE for each pair of business intent and part).
- "needs" between capabilities only (option 1): a functionality never needs anything.
