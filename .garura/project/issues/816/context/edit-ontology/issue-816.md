Feature: the ontology says that a Slice serves a business intent, and that `/shape-slice` makes the plan from the slice it shaped. Then a plan only reads the link. It does not pick a slice again.

## Why
Decided with the product owner on 2026-10-23. `/shape-slice` does the heavy work: it gets a business intent, grills the person, and puts the slice together. The plan must not do that work a second time. Today (ontology v8) the plan "picks a slice by two tests", and a Slice has no link to a business intent.

## Done when
- Through `/edit-ontology` (three checkpoints):
  - Slice gains the link "serves Business Intent" (many to many). `/shape-slice` writes it.
  - Plan: it is made by `/shape-slice` from the slice it shaped. The "two tests" go.
  - The rule "a slice has a screen or surface a person can test end to end" is a Slice rule.
  - The ontology names where the slice's eval lives, so that a builder never reads it.
- If this changes what ADR 048 decided, an ADR records it through `/record-decision`.

## Not in this issue
- Changing the plays (#795 and the stories after it).

## Links
- Serves: #788
- Part of: #794

