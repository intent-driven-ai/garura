  software-delivery-planning/domain.md:6
- > To be deepened later: written by /shape-slice for bi-788 at the directional depth. /discover-domains or /discover-capabilities raises it to the detailed depth.
+ > To be deepened later: written by /shape-slice at the directional depth. /discover-domains or /discover-capabilities raises it to the detailed depth.

  software-delivery-planning/cap-718/capability.md:6
- Added by /shape-slice for bi-788 (ontology v9 and v10, ADR 049): a business intent has one plan, and never a second; the plan's ID is the intent's issue number. The plan holds every slice that serves its intent, found from the link "slice serves business intent", and it takes the slice that was shaped; it does not pick or test slices. For each slice it makes one epic, or uses the one that exists, and one story for each feature of the slice. A story's scope of work holds the goal, the limits and the expectations from its feature's ICE and that feature's capability's ICE, and its Context guidance is its own property. A story never holds a failure condition. The plan play does not write the slice's hidden file; /shape-slice writes it (decision 6 of #844, recorded in ADR 052, which amends ADR 049 Decisions 1.2 and 4). The product owner agreed on 2026-10-24 (#844) to change the old words "a tracker issue for every node" to this rule: under ontology v7 and later a capability and a feature get no tracker issue; only the epic and the stories do.
+ Added by /shape-slice (ontology v9 and v10, ADR 049): a business intent has one plan, and never a second; the plan's ID is the intent's issue number. The plan holds every slice that serves its intent, found from the link "slice serves business intent", and it takes the slice that was shaped; it does not pick or test slices. For each slice it makes one epic, or uses the one that exists, and one story for each feature of the slice. A story's scope of work holds the goal, the limits and the expectations from its feature's ICE and that feature's capability's ICE, and its Context guidance is its own property. A story never holds a failure condition. The plan play does not write the slice's hidden file; /shape-slice writes it (decision 6 of #844, recorded in ADR 052, which amends ADR 049 Decisions 1.2 and 4). The product owner agreed on 2026-10-24 (#844) to change the old words "a tracker issue for every node" to this rule: under ontology v7 and later a capability and a feature get no tracker issue; only the epic and the stories do.

  software-delivery-planning/cap-718/capability.md:8
- > To be deepened later: written by /shape-slice for bi-788 at the directional depth. /discover-domains or /discover-capabilities raises it to the detailed depth.
+ > To be deepened later: written by /shape-slice at the directional depth. /discover-domains or /discover-capabilities raises it to the detailed depth.

  software-delivery-planning/shape-eval/capability.md:8
- > To be deepened later: written by /shape-slice for bi-788 at the directional depth. /discover-domains or /discover-capabilities raises it to the detailed depth.
+ > To be deepened later: written by /shape-slice at the directional depth. /discover-domains or /discover-capabilities raises it to the detailed depth.

  software-delivery-planning/cap-718/fn-818/feature.md:6
- > To be deepened later: written by /shape-slice for bi-788 at the directional depth. /discover-domains or /discover-capabilities raises it to the detailed depth.
+ > To be deepened later: written by /shape-slice at the directional depth. /discover-domains or /discover-capabilities raises it to the detailed depth.

  software-delivery-planning/cap-718/fn-818/feature.md:60
- - Checked by: the product owner runs /shape-plan 788 in Claude Code after /shape-slice and finds the plan file, one epic and one story for each feature, with no failure line in any story.
+ - Checked by: the product owner runs /shape-plan on a business intent in Claude Code after /shape-slice and finds the plan file, one epic and one story for each feature, with no failure line in any story.

  software-delivery-planning/shape-eval/fn-798/feature.md:6
- > To be deepened later: written by /shape-slice for bi-788 at the directional depth. /discover-domains or /discover-capabilities raises it to the detailed depth.
+ > To be deepened later: written by /shape-slice at the directional depth. /discover-domains or /discover-capabilities raises it to the detailed depth.

  software-delivery-planning/shape-eval/fn-798/feature.md:48
- - Checked by: the product owner runs /shape-eval 788 in Claude Code after /shape-plan and finds the eval in plans/788/evals/<slug>/.
+ - Checked by: the product owner runs /shape-eval on a business intent in Claude Code after /shape-plan and finds the eval in its plan's evals folder.

  software-delivery-planning/shape-eval/fn-898/feature.md:6
- > To be deepened later: written by /shape-slice for bi-788 at the directional depth. /discover-domains or /discover-capabilities raises it to the detailed depth.
+ > To be deepened later: written by /shape-slice at the directional depth. /discover-domains or /discover-capabilities raises it to the detailed depth.

  features/fn-931/feature.md:33
- - The approved /update-plan session on plan 717, entry 3: "A person adds a new feature found while a plan is in progress, to the model, its slice and its epic"
+ - An approved /update-plan session, entry 3: "A person adds a new feature found while a plan is in progress, to the model, its slice and its epic"

  software-delivery-planning/manage-model/capability.md:6
- This capability takes in the old capability Link the product model, filed under the closed intent bi-722 (A product model can be managed, and grows as plans are built). Its old page said that "work can start before the model is complete, if the model links its parts by these rules". Its ready check is built; its link check and its search by domain are not. Three of its features stay here, with their ids and their folders, each rewritten to what was built: fn-724 is the ready check, fn-725 the links between parts, and fn-726 the list of what serves an intent and what sits in a domain. Its fourth feature, fn-597, the ontology itself, belongs to Define what a product is made of.
+ This capability takes in the old capability Link the product model, filed under an older business intent, now closed (A product model can be managed, and grows as plans are built). Its old page said that "work can start before the model is complete, if the model links its parts by these rules". Its ready check is built; its link check and its search by domain are not. Three of its features stay here, with their ids and their folders, each rewritten to what was built: fn-724 is the ready check, fn-725 the links between parts, and fn-726 the list of what serves an intent and what sits in a domain. Its fourth feature, fn-597, the ontology itself, belongs to Define what a product is made of.

  software-delivery-planning/define-product/capability.md:6
- This capability takes in one feature of an older capability, Link the product model, which was filed under the closed intent bi-722 (A product model can be managed, and grows as plans are built): Rebuild the product model as an ontology (fn-597). It keeps its id and its folder. Its page is rewritten to what was built: the map at version 15.
+ This capability takes in one feature of an older capability, Link the product model, which was filed under an older business intent, now closed (A product model can be managed, and grows as plans are built): Rebuild the product model as an ontology (fn-597). It keeps its id and its folder. Its page is rewritten to what was built: the map at version 15.

  software-delivery-planning/standards/capability.md:6
- This capability takes in three older capabilities, filed under the closed intent bi-734 (Garura publishes a standard for building agentic harnesses): The harness standard, written down; The naming checks, built before any rename; and Every name moved to the standard, one family at a time. All three are built. Their nine features stay here, with their ids and their folders, and each is rewritten to what was built. One of them, fn-741, keeps its id also because Take out the parts Garura renamed or dropped (fn-748), in Upgrade a project, depends on it.
+ This capability takes in three older capabilities, filed under an older business intent, now closed (Garura publishes a standard for building agentic harnesses): The harness standard, written down; The naming checks, built before any rename; and Every name moved to the standard, one family at a time. All three are built. Their nine features stay here, with their ids and their folders, and each is rewritten to what was built. One of them, fn-741, keeps its id also because Take out the parts Garura renamed or dropped (fn-748), in Upgrade a project, depends on it.

  software-delivery-planning/manage-model/fn-close-model-gaps/feature.md:9
- - Their run on Garura's own model on 2026-11-11: one loose part, the old capability Link the product model, which has no domain; four intents nothing serves (bi-11, bi-5, bi-734 and bi-756); 21 links kept on one side only; no duplicates and no link to nothing.
+ - Their run on Garura's own model on 2026-11-11: one loose part, the old capability Link the product model, which has no domain; four intents nothing served then (bi-11, bi-5, and two older intents since removed); 21 links kept on one side only; no duplicates and no link to nothing.

  software-delivery-planning/turn-intents-into-work/capability.md:71
- - .garura/product/product-os/software-delivery-planning/cap-718/fn-818/feature.md: "A story never names the eval, the hidden file or the plan's evals folder."
+ - .garura/product/product-os/software-delivery-planning/turn-intents-into-work/fn-818/feature.md: "A story never names the eval, the hidden file or the plan's evals folder."

  software-delivery-planning/turn-intents-into-work/capability.md:72
- - The old model parts this capability takes in: Build a plan (cap-718) with fn-727, fn-728 and fn-818, and from Manage a plan the work-item changes of fn-730 and fn-931; fn-931 is filed under this capability, and the rest of Manage a plan merged into Orchestrate agent work through planning (cap-orchestrate-agent-work).
+ - The old model parts this capability takes in: Build a plan with fn-727, fn-728 and fn-818, and from Manage a plan the work-item changes of fn-730 and fn-931; fn-931 is filed under this capability, and the rest of Manage a plan merged into Orchestrate agent work through planning (cap-orchestrate-agent-work).

  software-delivery-planning/turn-intents-into-work/fn-cut-intent-into-work/feature.md:51
- - .garura/product/product-os/software-delivery-planning/cap-718/capability.md: "the same trees that were filed by hand on 2026-10-21"
+ - .garura/project/issues/1021/context/cleanup/old-pages/build-a-plan.md, which keeps the page of Build a plan as it was before the merge: "the same trees that were filed by hand on 2026-10-21"

  software-delivery-planning/turn-intents-into-work/fn-cut-intent-into-work/feature.md:52
- - .garura/product/product-os/software-delivery-planning/cap-718/fn-818/feature.md: "A change to a plan that exists, a later slice's epic and stories included. /update-plan makes it"
+ - .garura/product/product-os/software-delivery-planning/turn-intents-into-work/fn-818/feature.md: "A change to a plan that exists, a later slice's epic and stories included. /update-plan makes it"

  software-delivery-planning/turn-intents-into-work/fn-write-story-from-ice/feature.md:52
- - .garura/product/product-os/software-delivery-planning/cap-718/fn-818/feature.md: "A story never names the eval, the hidden file or the plan's evals folder."
+ - .garura/product/product-os/software-delivery-planning/turn-intents-into-work/fn-818/feature.md: "A story never names the eval, the hidden file or the plan's evals folder."

  software-delivery-planning/gather-work-under-item/fn-collect-story-context/feature.md:56
- - .garura/product/product-os/software-delivery-planning/shape-eval/fn-898/feature.md: "A build's inputs are the slice's stories and the context that the build's context sub-agent collects from each story's Context guidance."
+ - .garura/product/product-os/software-delivery-planning/write-work-evals/fn-898/feature.md: "A build's inputs are the slice's stories and the context that the build's context sub-agent collects from each story's Context guidance."

  software-delivery-planning/write-work-evals/capability.md:74
- - .garura/product/product-os/software-delivery-planning/shape-eval/capability.md: "Write the eval that checks, from the outside, that a business intent is met on its slice's surface.", "It matters because a builder that sees the test can build to the test, and then a pass proves nothing."
+ - .garura/project/issues/1021/context/cleanup/old-pages/write-the-hidden-eval.md, which keeps the page of Write the hidden eval as it was before the merge: "Write the eval that checks, from the outside, that a business intent is met on its slice's surface.", "It matters because a builder that sees the test can build to the test, and then a pass proves nothing."

  software-delivery-planning/write-work-evals/capability.md:91
- - The old model parts this capability takes over: Write the hidden eval (cap-shape-eval) with its features fn-798 and fn-898. Its hidden file part comes from the slice play, /shape-slice (fn-795).
+ - The old model parts this capability takes over: Write the hidden eval with its features fn-798 and fn-898. Its hidden file part comes from the slice play, /shape-slice (fn-795).

  software-delivery-planning/write-work-evals/fn-keep-evals-from-builder/feature.md:49
- - .garura/product/product-os/software-delivery-planning/shape-eval/fn-898/feature.md: "For now we should record this under evidence.", "When the list named only some plays, a play that builds code and is not on the list could be given the eval, and a pass would prove less than the intent asks."
+ - .garura/product/product-os/software-delivery-planning/write-work-evals/fn-898/feature.md: "For now we should record this under evidence.", "When the list named only some plays, a play that builds code and is not on the list could be given the eval, and a pass would prove less than the intent asks."

  software-delivery-planning/write-work-evals/fn-keep-evals-from-builder/feature.md:50
- - .garura/product/product-os/software-delivery-planning/shape-eval/fn-898/feature.md: "A build session with no read of the evals folder passes with no flag, so a flag always means a real read.", "Thin: what the ledger check does when it cannot find a build session's ledger is not set yet."
+ - .garura/product/product-os/software-delivery-planning/write-work-evals/fn-898/feature.md: "A build session with no read of the evals folder passes with no flag, so a flag always means a real read.", "Thin: what the ledger check does when it cannot find a build session's ledger is not set yet."

  software-delivery-planning/write-work-evals/fn-keep-evals-from-builder/feature.md:51
- - .garura/product/product-os/software-delivery-planning/shape-eval/fn-898/feature.md: "Blocking a read by hook is the guardrails work (#893).", "The flag is recorded in the build run's evidence, and for now only there"
+ - .garura/product/product-os/software-delivery-planning/write-work-evals/fn-898/feature.md: "Blocking a read by hook is the guardrails work (#893).", "The flag is recorded in the build run's evidence, and for now only there"
