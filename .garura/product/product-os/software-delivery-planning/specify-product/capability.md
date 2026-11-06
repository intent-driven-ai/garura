# Capability: Specify the product

## Directional intent
The product is understood from what a person gives, whether a video, a prototype, a brief or all of those, and becomes confirmed intents, domains, capabilities and features.
It matters to software delivery planning because that domain turns a business intent into work that agents can build. This capability is where those business intents and the model come from.

What makes it unique: it starts from something that works, not from a written spec.

Features:
- Specify intents (fn-specify-intents): drafts one business intent for each need the product meets, and the person confirms or drops each one.
- Specify domains (fn-specify-domains): finds each domain the product sits in and writes a full page for it.
- Specify capabilities (fn-specify-capabilities): writes a full page for each capability and creates its features with their pages.
- Specify from a prototype's journeys (fn-specify-from-journeys): uses the prototype one step at a time and keeps a picture and the text of every step.
- Specify from a video (fn-specify-from-video): what a video shows is captured, so intents can trace to moments in it.
- Specify from a file (fn-specify-from-file): saves an exact copy of one web-page file, and a picture and the text of each view.
- Specify from a project folder (fn-specify-from-folder): keeps the project's written docs and captures its running app.
- Specify from a deployed site (fn-specify-from-site): saves each view of a deployed site as a full-page picture and its visible text.
- Specify from a document (fn-specify-from-document): saves an exact copy of a document, such as a brief or a PDF.
- Specify from plain words (fn-specify-from-words): keeps the words a person types, byte for byte.
- Validate the attribution (fn-validate-attribution): a judge with no context says whether what was given was fully and correctly used.
- Specify against what exists (fn-specify-against-existing): what's given is sorted against what exists: a new intent, an enhancement, a new feature under one, or a clash.

What is not built yet:
- Specify from a video is not built.
- Validate the attribution is not built.
- Specify against what exists is not built.
- Specify intents has four parts not built, and its page names them.
- Nothing checks an ICE against the rubric yet. An ICE is the agent's intent for one capability or feature: what an agent must make true there, for whom, and how it is checked. The rubric is the written rule for what a good ICE looks like.
- Intents have no judge with no context yet.

### Benefit hypothesis
- Who it serves: the product owner, who wants to confirm what a product is for without writing a spec first.
- What we believe: a person can give something that works and get a full product model from it, if the work stands on these rules:
  - What the person gave stays readable as it was. Every later step can go back to it.
  - A prototype is used, not only read. Its screens show what it has, and using it shows what it is for.
  - Each kind of part has its own writer. One wrong reading of the source then cannot spread to every other kind.
- How we will know: a new builder, who never saw the prototype, builds the product from the intents and the model alone.
  - The rebuild test then tries what the prototype does on what the builder made.
  - Design, layout and code may differ, but what a person can do and see may not.
  - What is missing, half there or added is the drift.
  - When the intents and the model do not bring the prototype back, they are not good enough to build from.

### Boundary (In / Out / Never)
- In: keeping what a person gives as a Source. A Source is a saved copy of a file, a project folder, a deployed site, a document or a person's own words. Later steps read this copy, so they do not need the original.
- In: walking a prototype in journeys. A journey is one person's way through it, from what they set out to do to what they end with.
- In: writing business intents, domains, capabilities and features. These kinds are the model that all later work reads.
- In: setting each capability's quality and compliance needs, and rolling them up into the product profile. The profile holds the product's shape and the quality levels it commits to.
- Out: linking parts that were written apart. The discovery loop reads a prototype once and runs the three writers on that reading, in rounds: Specify intents, Specify domains and Specify capabilities. Inside the discovery loop, a later step finds and makes those links. The work of managing the model owns the link rules.
- Out: choosing what to build first. Later shaping work picks the features a person can test end to end and turns them into work items.
- Out: keeping intents up to date as the product changes. This capability does not do it, and no capability in the model owns it yet.
- Never: write over finished work. An intent page is never overwritten, a domain page keeps each section it had, and a capability at full depth is not detailed again. Other parts may already rely on these pages.
- Never: set a capability to active, or rank one part above another. Ranking belongs to the later shaping work, and no step sets a capability active today.

### Guiding rules
- Every Source is kept the same way. A capture saves the Source's files with the run's evidence and writes one capture record: the kind of Source, the date it was read, who gave it (the git user running the work) and a fingerprint of each saved file. A fingerprint is a short code worked out from a file's bytes, so any change to the file changes the code. The reason: the Source must outlive the link or the file.
- A failed capture stops the work. A missing file, a link that does not open, or no name for who gave the Source fails the capture. The person hears what could not be opened and gets asked for a readable copy or a working link. The reason: a model drawn from a source nobody read has no basis.
- A gap another step left is a warning, not a stop. A missing intent page or a light domain page goes on record, and the run goes on. The reason: a person can start from whatever they have.
- There are two ways to run. Started by hand, a step opens its own change, stops at its checkpoint, and lands the change. Inside the discovery loop, which runs the three writers together in rounds, a step opens nothing and does not wait: it works on the loop's branch, and the person decides at the loop's final review. The reason: the person decides once, on the whole result.
- Inside the loop, one reader captures and walks the prototype once, and every writer reads that one capture. The reason: walking is long work that needs little judgment, so it runs once and apart from the writers.
- Sample data is only an example. A tool shown with a bakery's tasks is about any team's work, not about bakeries. So intents, domains, capabilities and features hold for any such content, and never name the sample's company, items or counts.
- Domain, capability and feature pages get two checks. A structure check tests the headings and the links. A judge then reads each page with no context: it gets only the page, its parent page and the guidance for its kind. The reason: a page can have the right shape and still be thin. A pass stands while those inputs do not change, so a second run does not judge the same text again.
- Each writer starts from a clean model and checks its own scope at the end. A step stops if the model has unsaved changes when it starts. After it writes, a guard compares the model with how it started. A file outside the step's scope fails the step and goes back as it was. The reason: the comparison then shows only this run's work.

## Sources
- The one line, the unique line and the feature list the product owner approved on 2026-11-03.
- .garura/product/product-os/intents/bi-1.md: "A person confirms the intents without writing a spec."
- core/components/plays/discover-intent/reference/ice.md: "The Source is kept as it was when read", "A prototype is understood by using it", "one wrong intent spread to the whole model", "Stands alone, or runs inside a loop"
- core/components/plays/discover-intent/scripts/capture_source.py: "keep a Source exactly as it was when read"
- core/components/plays/discover-intent/scripts/persist_intent.py: "a business intent is never overwritten"
- core/components/plays/discover-domains/reference/ice.md: "Starts from whatever is there, and never blocks", "keeping every section it had", "The eval settles"
- core/components/plays/discover-capabilities/reference/ice.md: "never prioritizes (no slices, no", "Runs inside a loop without stopping", "Clean tree in, committed delta out", "Profile roll-up is monotonic-up"
- core/components/agents/prototype-reader.md: "none walks the prototype again"
- core/components/skills/author-business-intent/SKILL.md: "a work-tracking tool shown with a bakery's tasks is about any team's work"
- core/tools/rebuild-eval/README.md: "A fresh agent, with no sight of the prototype and"
- .garura/product/product-os/software-delivery-planning/domain.md: "This domain turns a business intent into work that agents can build"
- The short line beside each feature: the opening words of that feature's own page.
- standards/schemas/product-os/ontology.md, in Phoenix memory: "The agent's intent for one capability or one feature: what an agent must make true there, for whom, and how it will be checked."
- standards/rules/ice-rubric.md, in Phoenix memory: "What a good ICE looks like."
- core/components/loops/complete-discovery/SKILL.md: "reads the prototype once and runs /discover-intent, /discover-domains and /discover-capabilities on that one reading"
- Shelf: none. No knowledge shelf covers software delivery planning.
