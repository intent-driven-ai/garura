# Feature: Write the usage guide that tells the eval how to reach the built work

## What it does
With the build, the builder writes the slice's usage guide: what its surface is, how to reach it, and the steps a person takes there, so that the eval, when it runs later, can reach the built work.
- An eval is the outside test of a slice, on the surface where a person uses it. Write the evals that check the work writes it before the build; Test with evals the builder never sees runs it later, in Code → Validation. The running eval reaches the built work only through this guide.
- A surface is where a person, or another system, opens the product to use it: a browser page, a mobile app, a command line command or a backend endpoint.
- The guide says, from what was built:
  - what kind of surface the slice is on;
  - how to reach it, such as the command to run, the address of the page, or the address of the endpoint;
  - the steps a person takes there for each story under the chosen item, with the real names of the commands, pages and fields the work made.
- A slice has one usage guide. It is kept in the guides folder of the slice's home plan, the plan of the business intent the slice was first shaped for, beside the evals folder and never in it.
- When an item of the slice is built, the guide gains that item's part, and the parts already there stay.
- The builder writes it, and never sees the eval while it writes it.
- How it meets the capability: the build is not whole until the outside check can reach it. In the words of the decision on where the guide lives: "The build writes the usage guide. It is the eval's only way into the built product."

Status: not built. Nothing writes a usage guide, and no eval has run, because the runner is not built either.

## Inputs / Outputs
- In: the code as built, with its real commands, pages, addresses and fields.
- In: the design's surface part, which says what a person sees and does on the surface, and the builder's part of each story.
- In: the slice's one surface, as the slice names it, and the guide already there for the slice, if any.
- Out: the slice's usage guide in the guides folder of its home plan: what the surface is, how to reach it, and the steps for each built story.

## Rules & behavior
- The builder writes the guide and never reads the eval, the hidden file or the evals folder. The reason: the guide is kept "beside the evals folder but not in it, so the builder writes the guide and never sees the eval."
- One guide for each slice, in its home plan's guides folder; another plan that holds the slice points to it and never copies it. The reason: a slice "has one eval, one hidden file and one usage guide, also when two plans hold it", and "Another plan that holds it points to them and never copies them."
- The guide names the real things the build made: the real command, address and field. The reason: the eval writes "What only the build will make (a command, a page address, a field)" as a name in square brackets, and "A guide that maps a name wrongly makes a scenario fail for the wrong reason."
- The guide says how to use the work, never whether it works. It holds no test result and no expected result. The reason: judging the work is the eval's, and the guide is only its way in.
- Each built item adds its part, and a part already there changes only when what it describes changed. The reason: the guide must keep saying how to reach every built part of the slice.
- Not decided: how each name the eval uses is matched in the guide, when the builder who writes the guide never sees the names.
- Not decided: what the guide holds for a chore or a spike that changes nothing on the surface.

## Acceptance criteria
- Given a slice on a command line with two stories built, when the guide is written, then it names the command, how a person runs it and answers it, and the steps for each of the two stories.
- Given a guide written by the builder, when the build session's record is checked, then it shows no read of the evals folder, an eval or the hidden file.
- Given a slice held by two plans, when its guide is written, then it is kept once, in the guides folder of its home plan.
- Given a third story of the same slice built later, when the guide is updated, then that story's part is added and the parts already there are unchanged.
- Given a finished guide, when it is read, then it holds no test result and no expected result.

## Out of scope
- Writing the eval and naming what only the build will make. Write the evals that check the work does it.
- Matching each name in the eval to the guide, running the eval, and giving the verdict. Test with evals the builder never sees, in Code → Validation, does it.
- Declaring the project's surfaces. Manage surfaces does it.
- Designing what a person sees and does on the surface. Design the work does it.

## Sources
- .garura/product/product-os/software-delivery-planning/write-work-evals/capability.md: "Out: the code-level tests written before the code, the code, and the usage guide the build delivers. Build the work test first owns them, and the developer does that work."
- .garura/product/product-os/software-delivery-planning/write-work-evals/fn-write-work-evals/feature.md: "Not decided: how each name the eval uses is matched in the usage guide, when the builder who writes the guide never sees the names.", "The usage guide, which maps each name to the real thing. Build the work test first delivers it with the build."
- docs/adr/049-a-slice-is-shaped-then-planned-then-given-its-eval.md: "The build writes the usage guide. It is the eval's only way into the built product."
- docs/adr/057-a-slices-eval-is-plain-text-gherkin-that-runs-with-no-agent.md: "What only the build will make (a command, a page address, a field) is written as a name in square brackets.", "A guide that maps a name wrongly makes a scenario fail for the wrong reason.", "The runner that runs the eval is not built yet (#819). Until then an eval is written but never run."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "The build delivers its usage guide with the slice, in the guides folder beside the evals folder but not in it, so the builder writes the guide and never sees the eval.", "What its surface is (a browser page, a mobile app, a command line command or a backend endpoint), how to reach it, and the steps a person takes."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "It has one eval, one hidden file and one usage guide, also when two plans hold it.", "Another plan that holds it points to them and never copies them."
- .garura/product/product-os/software-delivery-planning/write-work-evals/capability.md: "Out: running the evals, giving the verdict, and writing the handoff plan, which tells the builder or a person what went wrong and the way back. Test with evals the builder never sees, in Code → Validation, owns them."
