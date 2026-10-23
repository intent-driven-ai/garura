# Need (#816, plan 788)

In the product owner's words (2026-10-23): "The shape slice is going to cut out a slice. That's going to identify a business intent that it would be delivering towards." "When I give Plan a business intent to execute, the linking of the slice should be much simpler and easier to find because all of the linking has been set up in the product model. The rethinking and recalculation should not be done. Plan's job is just executing the plan and shaping slices, where the heavy-lifting work happens." /shape-slice "gets a business intent, reads a configuration, and does grill the user ... assembles everything ... offers the user whether it should set up a plan for it ... also builds the eval".

What changes:
1. Slice gains the link "serves Business Intent". /shape-slice writes it.
2. Plan: it is made by /shape-slice from the slice it shaped; it reads the link. The "picks a slice by two tests" goes.
3. The rule "a slice has a screen or surface a person can test end to end" becomes a Slice rule.
4. The ontology names where the slice's eval lives, so a builder never reads it. The eval tests whether the business intent is met, from the outside, on the slice's surface.

Sources: issue #816; the 2026-10-23 decisions recorded on #794, #795, #798, #818, #796.

## Touches
Slice
Plan
Business Intent
Epic
Story
