# #637 — design: `/intent` and `/vision` both write the one product model

Kapil, 2026-10-17: "ensure that intent and vision both support the core
product-model. this is important. also remember nothing is blocked as a chain,
anything can be updated as the information is gathered. some light, some more
depending on the level of information." Then "yes" to #637 also changing
`/intent`.

Grounds: ADR 031 part 2 (no play owns a kind; rules never stop a write) and
part 3 (a capability may exist before its domain); ontology v3; the /intent ICE
already says "/vision attaches the capabilities to domains and adds to them".

## 1. One model, depth shown by stage

- The tree is domain → capability → functionality, intents beside it, one
  `_spine.yaml` (product-os.yaml, spine.yaml v2).
- A **domain gets two stages**, like a capability already has:
  `detail: directional` (a light page: `# Theme:` + `## Intent`) or
  `detail: detailed` (the full Theme page, as today).
- The grounding linter becomes stage-aware for domains, the same way it is for
  capabilities. A domain entry with no `detail` is inferred from its page, so
  every existing model still passes.
- Files: the domain template, `spine.yaml` (domains get `detail`), and
  `lint_grounding.py` (12 identical copies, changed together).

## 2. `/intent` writes into the tree

- For each ICE, the draft may name the domain it belongs to: from the source,
  the person's words, or a domain already in the model.
- Domain named → the capability page goes to
  `<domain>/<capability>/capability.md`, its spine entry carries the domain.
  If the domain is not in the model yet, `/intent` adds a light domain page
  (directional) and its spine entry (proposed, directional). If it is, `/intent`
  links to it and leaves its page alone.
- No domain can be told → the holding folder, as today; the linter warns.
- Nothing about confirming intents changes.

## 3. `/vision` works from whatever is there and never blocks

- Input: business intents (by id or `/intent`'s save record), a typed goal,
  or both. With neither, it asks, as today.
- It reads what the model holds: intent pages (proposed is fine; it never runs
  the workable check), their capabilities wherever they sit, the domains.
- It updates in place, at its own depth:
  - a light domain page becomes the full page, keeping what was there;
  - a capability page someone else wrote may get light additions to its
    directional intent; it stays directional (full detail is `/understand`);
  - a capability in the holding folder gets a domain, and its page moves into
    the domain's folder unchanged; the link on the intent page is fixed by the
    script, and nothing else on that page changes;
  - a KB candidate that matches an existing capability is recorded as the same
    thing, never added twice;
  - every capability it adds names the intent it serves, when it started from
    intents.
- Anything missing or odd is a **warning** in the run record, for the
  Alignment drive. Nothing is refused and the close never fails because another
  play did or did not run first.

## 4. What still guards the model

- The save script (`persist_seed.py`): adds new spine entries; on an existing
  entry it may set an empty `domain`, repoint `doc`, raise `detail` (never
  lower it), refresh `one_line`, and add to `intents`. It never removes an
  entry or changes an id. Moving a capability from one domain to another is
  left to the Alignment drive, as a warning.
- A keep check (`check_kept.py`): every existing page the run changed still has
  each section it had, and every agent-intent line.
- The safety check after writing (`scoped_write_guard.py`, 14 identical
  copies plus the canonical one): gains "may only be removed" and "may only be changed" kinds, and
  stops git from hiding a removal inside a rename. `/vision` may change domain
  and capability pages; the holding folder may only lose pages; intent pages
  may only be changed (the link rule is kept by the script).
- The linter, the content judge (for pages `/vision` writes or extends) and
  the human checkpoint over the real diff stay as they are.

## 5. The agent intent gets its own section (Kapil, 2026-10-17: "fix them inside #637")

- Every capability and functionality page may end with `## Agent intent (ICE)`:
  labelled lines — Goal, Limit, Fails if, Context, Checked by, Quality need —
  filled as far as is known. At least one Goal.
- Required once the node's spine entry names a business intent in `intents`;
  optional otherwise, so pages written before this still pass.
- `/intent`'s loose "Goals:" list moved into it.

## 6. A business intent is linked to every level, both ways

- Domain entries in the spine get `intents`, like capabilities and
  functionalities.
- Each intent page has a **Touches** list: every domain, capability and
  functionality it reaches, marked adds / changes / removes, with a link. One
  shared script writes it (`intent_touches.py`, canonical in play-creator
  references, stamped into /intent and /vision); it replaces the old "ICE built
  from it" list and converts it on first touch.
- The ontology is version 4 and records all of this.
