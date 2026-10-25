Feature: `/shape-slice` gets a business intent, grills the person within the grilling tier, and puts together the slice that delivers the intent. It writes the slice into the product model with its link to the intent.

## Done when
- It takes a business intent issue number as its entry point, finds that intent in the product model, and works from the model. If the model has no page for it, it writes the page from the issue. It does not need a slice that the seven lenses stamped "realized".
- It reads the product model and memory first, and asks only about the gaps — all at once, each question standing alone — within the tier's budget (#817). It records the answers in short-term memory.
- It picks the features that serve the intent, from any capability, and names the person who tests the slice and the one surface they test it on. A slice with no such surface is not written.
- It finds a slice that already serves the intent before it makes a new one.
- It fills the model as it goes: a domain, capability, feature or ICE the slice needs and the model lacks is added at the depth it knows, never skipped.
- It writes the slice (`features` in build order, `vertical`, `intents`) into the spine's `slices` list, with its record at `product-os/slices/<id>.yaml` (a slice links to capabilities, and through them to its domains; it has no domain home), and the grounding linter passes.
- Until #796, it shows the slice at a typed checkpoint (yes / change / stop) and commits only after yes.
- Built fresh with `/create-play` (the old play's job, cutting epics, is gone; decisions: `.garura/project/issues/795/context/decisions.md`).

## Not in this issue
- The eval (#798), the plan (#818), the pinned checkpoint (#796), the tier setting (#817).
- The design, build and test of the epic (the build-stage business intent).

## Links
- Serves: #788
- Part of: #794
- Needs: #816


