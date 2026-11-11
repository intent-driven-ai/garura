# Redraft of the nine pages the no-context judge failed (issue 1021, capability 1)

Draft only. The copies are under `.garura/project/issues/1021/context/capability-1/redraft/product-os/`. The live model under `.garura/product/` is unchanged.

Every change went through the enrich-grounding skill's named-lines script (`change_lines.py`), from `.garura/project/issues/1021/context/capability-1/redraft/lines-request.json`; its report is `lines-report.json` beside this file. Every other line of each page is kept word for word.

Choice on the document page: the first acceptance criterion now says the test, not the run, works out the original's fingerprint and compares it with the one the record holds for the copy. The rule "No step works out the original's fingerprint or compares the two" stays as it is, because it is the truth about the built software.

Choice on the file page: the line "It finds views the same way as Specify from a deployed site ... with the same limits and the same skipped controls" is approved, so it stays word for word. The limits, the depth, the skipped controls and what found and kept mean are now stated directly in new lines below it.

Choice on the capability page: the structure check needs at least five words in each bullet, so each feature bullet carries a short line taken from the opening words of that feature's own page.

## .garura/product/product-os/software-delivery-planning/specify-product/capability.md

Failed criteria in the judge's verdict: self_explanation, discreteness_form, stranger_test.

### Changed lines

1. Old: Features: Specify intents (fn-specify-intents), Specify domains (fn-specify-domains), Specify capabilities (fn-specify-capabilities), Specify from a prototype's journeys (fn-specify-from-journeys), Specify from a video (fn-specify-from-video), Specify from a file (fn-specify-from-file), Specify from a project folder (fn-specify-from-folder), Specify from a deployed site (fn-specify-from-site), Specify from a document (fn-specify-from-document), Specify from plain words (fn-specify-from-words), Validate the attribution (fn-validate-attribution), Specify against what exists (fn-specify-against-existing).

   New: Features:

   Answers: discreteness_form: the run-on feature list becomes a bulleted index, one feature per line with its id

2. Old: Specify from a video, Validate the attribution and Specify against what exists are not built. Specify intents has four parts not built, and its page names them. Nothing checks an ICE against the rubric yet, and intents have no judge with no context yet.

   New: What is not built yet:

   Answers: discreteness_form: the not-built paragraph becomes one bullet per gap

3. Old: - How we will know: a new builder, who never saw the prototype, builds the product from the intents and the model alone. The rebuild test then tries what the prototype does on what the builder made. Design, layout and code may differ, but what a person can do and see may not. What is missing, half there or added is the drift. When the intents and the model do not bring the prototype back, they are not good enough to build from.

   New: - How we will know: a new builder, who never saw the prototype, builds the product from the intents and the model alone.

   Answers: discreteness_form: the How we will know bullet is split; this keeps its first point (who builds)

4. Old: - Out: linking parts that were written apart. Inside the discovery loop, a later step finds and makes those links. The work of managing the model owns the link rules.

   New: - Out: linking parts that were written apart. The discovery loop reads a prototype once and runs the three writers on that reading, in rounds: Specify intents, Specify domains and Specify capabilities. Inside the discovery loop, a later step finds and makes those links. The work of managing the model owns the link rules.

   Answers: stranger_test: names the three writers where the discovery loop is first mentioned

### Added lines

1. Added after: The product is understood from what a person gives, whether a video, a prototype, a brief …

   Added: It matters to software delivery planning because that domain turns a business intent into work that agents can build. This capability is where those business intents and the model come from.

   Answers: self_explanation and stranger_test: why this capability matters to Software delivery planning

2. Added after: Features: Specify intents (fn-specify-intents), Specify domains (fn-specify-domains), Spec…

   Added: - Specify intents (fn-specify-intents): drafts one business intent for each need the product meets, and the person confirms or drops each one.

   Answers: discreteness_form: one bullet per feature with its id; the short line after each is that feature's own opening words, so each bullet clears the structure check's five-word floor

3. Added after: Features: Specify intents (fn-specify-intents), Specify domains (fn-specify-domains), Spec…

   Added: - Specify domains (fn-specify-domains): finds each domain the product sits in and writes a full page for it.

   Answers: discreteness_form: one bullet per feature with its id; the short line after each is that feature's own opening words, so each bullet clears the structure check's five-word floor

4. Added after: Features: Specify intents (fn-specify-intents), Specify domains (fn-specify-domains), Spec…

   Added: - Specify capabilities (fn-specify-capabilities): writes a full page for each capability and creates its features with their pages.

   Answers: discreteness_form: one bullet per feature with its id; the short line after each is that feature's own opening words, so each bullet clears the structure check's five-word floor

5. Added after: Features: Specify intents (fn-specify-intents), Specify domains (fn-specify-domains), Spec…

   Added: - Specify from a prototype's journeys (fn-specify-from-journeys): uses the prototype one step at a time and keeps a picture and the text of every step.

   Answers: discreteness_form: one bullet per feature with its id; the short line after each is that feature's own opening words, so each bullet clears the structure check's five-word floor

6. Added after: Features: Specify intents (fn-specify-intents), Specify domains (fn-specify-domains), Spec…

   Added: - Specify from a video (fn-specify-from-video): what a video shows is captured, so intents can trace to moments in it.

   Answers: discreteness_form: one bullet per feature with its id; the short line after each is that feature's own opening words, so each bullet clears the structure check's five-word floor

7. Added after: Features: Specify intents (fn-specify-intents), Specify domains (fn-specify-domains), Spec…

   Added: - Specify from a file (fn-specify-from-file): saves an exact copy of one web-page file, and a picture and the text of each view.

   Answers: discreteness_form: one bullet per feature with its id; the short line after each is that feature's own opening words, so each bullet clears the structure check's five-word floor

8. Added after: Features: Specify intents (fn-specify-intents), Specify domains (fn-specify-domains), Spec…

   Added: - Specify from a project folder (fn-specify-from-folder): keeps the project's written docs and captures its running app.

   Answers: discreteness_form: one bullet per feature with its id; the short line after each is that feature's own opening words, so each bullet clears the structure check's five-word floor

9. Added after: Features: Specify intents (fn-specify-intents), Specify domains (fn-specify-domains), Spec…

   Added: - Specify from a deployed site (fn-specify-from-site): saves each view of a deployed site as a full-page picture and its visible text.

   Answers: discreteness_form: one bullet per feature with its id; the short line after each is that feature's own opening words, so each bullet clears the structure check's five-word floor

10. Added after: Features: Specify intents (fn-specify-intents), Specify domains (fn-specify-domains), Spec…

   Added: - Specify from a document (fn-specify-from-document): saves an exact copy of a document, such as a brief or a PDF.

   Answers: discreteness_form: one bullet per feature with its id; the short line after each is that feature's own opening words, so each bullet clears the structure check's five-word floor

11. Added after: Features: Specify intents (fn-specify-intents), Specify domains (fn-specify-domains), Spec…

   Added: - Specify from plain words (fn-specify-from-words): keeps the words a person types, byte for byte.

   Answers: discreteness_form: one bullet per feature with its id; the short line after each is that feature's own opening words, so each bullet clears the structure check's five-word floor

12. Added after: Features: Specify intents (fn-specify-intents), Specify domains (fn-specify-domains), Spec…

   Added: - Validate the attribution (fn-validate-attribution): a judge with no context says whether what was given was fully and correctly used.

   Answers: discreteness_form: one bullet per feature with its id; the short line after each is that feature's own opening words, so each bullet clears the structure check's five-word floor

13. Added after: Features: Specify intents (fn-specify-intents), Specify domains (fn-specify-domains), Spec…

   Added: - Specify against what exists (fn-specify-against-existing): what's given is sorted against what exists: a new intent, an enhancement, a new feature under one, or a clash.

   Answers: discreteness_form: one bullet per feature with its id; the short line after each is that feature's own opening words, so each bullet clears the structure check's five-word floor

14. Added after: Specify from a video, Validate the attribution and Specify against what exists are not bui…

   Added: - Specify from a video is not built.

   Answers: discreteness_form: one bullet per gap

15. Added after: Specify from a video, Validate the attribution and Specify against what exists are not bui…

   Added: - Validate the attribution is not built.

   Answers: discreteness_form: one bullet per gap

16. Added after: Specify from a video, Validate the attribution and Specify against what exists are not bui…

   Added: - Specify against what exists is not built.

   Answers: discreteness_form: one bullet per gap

17. Added after: Specify from a video, Validate the attribution and Specify against what exists are not bui…

   Added: - Specify intents has four parts not built, and its page names them.

   Answers: discreteness_form: one bullet per gap

18. Added after: Specify from a video, Validate the attribution and Specify against what exists are not bui…

   Added: - Nothing checks an ICE against the rubric yet. An ICE is the agent's intent for one capability or feature: what an agent must make true there, for whom, and how it is checked. The rubric is the written rule for what a good ICE looks like.

   Answers: stranger_test: says in plain words what an ICE and the rubric are

19. Added after: Specify from a video, Validate the attribution and Specify against what exists are not bui…

   Added: - Intents have no judge with no context yet.

   Answers: discreteness_form: one bullet per gap

20. Added after: - How we will know: a new builder, who never saw the prototype, builds the product from th…

   Added:   - The rebuild test then tries what the prototype does on what the builder made.

   Answers: discreteness_form: a split-out point of How we will know (what the rebuild test tries, what may differ, what counts as drift, when the model is not good enough)

21. Added after: - How we will know: a new builder, who never saw the prototype, builds the product from th…

   Added:   - Design, layout and code may differ, but what a person can do and see may not.

   Answers: discreteness_form: a split-out point of How we will know (what the rebuild test tries, what may differ, what counts as drift, when the model is not good enough)

22. Added after: - How we will know: a new builder, who never saw the prototype, builds the product from th…

   Added:   - What is missing, half there or added is the drift.

   Answers: discreteness_form: a split-out point of How we will know (what the rebuild test tries, what may differ, what counts as drift, when the model is not good enough)

23. Added after: - How we will know: a new builder, who never saw the prototype, builds the product from th…

   Added:   - When the intents and the model do not bring the prototype back, they are not good enough to build from.

   Answers: discreteness_form: a split-out point of How we will know (what the rebuild test tries, what may differ, what counts as drift, when the model is not good enough)

24. Added after: - core/tools/rebuild-eval/README.md: "A fresh agent, with no sight of the prototype and"

   Added: - .garura/product/product-os/software-delivery-planning/domain.md: "This domain turns a business intent into work that agents can build"

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

25. Added after: - core/tools/rebuild-eval/README.md: "A fresh agent, with no sight of the prototype and"

   Added: - The short line beside each feature: the opening words of that feature's own page.

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

26. Added after: - core/tools/rebuild-eval/README.md: "A fresh agent, with no sight of the prototype and"

   Added: - standards/schemas/product-os/ontology.md, in Phoenix memory: "The agent's intent for one capability or one feature: what an agent must make true there, for whom, and how it will be checked."

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

27. Added after: - core/tools/rebuild-eval/README.md: "A fresh agent, with no sight of the prototype and"

   Added: - standards/rules/ice-rubric.md, in Phoenix memory: "What a good ICE looks like."

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

28. Added after: - core/tools/rebuild-eval/README.md: "A fresh agent, with no sight of the prototype and"

   Added: - core/components/loops/complete-discovery/SKILL.md: "reads the prototype once and runs /discover-intent, /discover-domains and /discover-capabilities on that one reading"

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

### Reasons not found

None.

## .garura/product/product-os/software-delivery-planning/specify-product/fn-specify-intents/feature.md

Failed criteria in the judge's verdict: self_explanation, stranger_test.

### Changed lines

1. Old: - In: on a later round of the discovery loop, what the other two writers put in the model. It only reads these.

   New: - In: on a later round of the discovery loop, what the other two writers put in the model. It only reads these. The discovery loop reads a prototype once and runs three writers on that reading, in rounds. The other two writers are Specify domains and Specify capabilities.

   Answers: stranger_test: what the discovery loop is and who the other two writers are

2. Old: - Out: one page for each saved intent, with its title, outcome, why, asked by, proof it is met, any must-not, its stage and its Sources.

   New: - Out: one page for each saved intent, with its title, outcome, why, asked by, proof it is met, any must-not, its stage and its Sources. The stage is proposed until the person confirms the intent, and then it reads confirmed. Each page is named by the intent's short name, its id, such as bi-1.

   Answers: stranger_test: what the stage of an intent means, and what a short name is

3. Old: - Depth is fixed today. The draft always writes at the level of the product. No step asks for a depth preference or reads one yet.

   New: - Depth is fixed today. The draft always writes at the level of the product. The reason: in an earlier run, asking "why?" again and again took the intents above the product, into the process behind its screens. No step asks for a depth preference or reads one yet.

   Answers: self_explanation: why depth is fixed at the product's level

4. Old: - A rule or a quality is not an intent. "Only approved items are used" is a rule the system enforces, and "fresh" or "private" is a quality. A quality goes in as a must-not line.

   New: - A rule or a quality is not an intent. "Only approved items are used" is a rule the system enforces, and "fresh" or "private" is a quality. A quality goes in as a must-not line. A part that shows a rule maps to the intent whose need the rule serves.

   Answers: stranger_test: resolves the clash between 'Every part must map to an intent' and 'A rule or a quality is not an intent'

5. Old: - The draft writes why, asked by and proof itself and names its basis. It never asks for them and never leaves them open, and the person corrects them when they decide. Asked by is a persona: a role the field knows and what it does there, such as "a team lead who plans a software team's work".

   New: - The draft writes why, asked by and proof itself and names its basis. It never asks for them and never leaves them open, and the person corrects them when they decide. The reason: an earlier run that left them open ended with every proof open. Asked by is a persona: a role the field knows and what it does there, such as "a team lead who plans a software team's work".

   Answers: self_explanation: why why, asked by and proof are never asked of the person

6. Old: - Each filled property records where it came from: the source, a journey, memory, the model, the person, or our own proposal with its basis. A title, an outcome or a limit cannot be our own proposal.

   New: - Each filled property records where it came from: the source, a journey, memory, the model, the person, or our own proposal with its basis. A title, an outcome or a limit cannot be our own proposal. The reason: these three say what the person wants, so each must rest on one of the other bases, not on our own proposal.

   Answers: self_explanation: why a title, an outcome or a limit cannot be our own proposal

7. Old: - The check refuses a title, outcome or proof that copies eight or more words in a row from the source. It also refuses code-like text, and any property under three words except asked by.

   New: - The check refuses a title, outcome or proof that copies eight or more words in a row from the source. The reason: an intent states the outcome the person wants, not a copy of the source. It also refuses code-like text, and any property under three words except asked by.

   Answers: self_explanation: why a copy of eight or more words is refused

8. Old: - A save refuses a draft that holds an ICE, a domain, a capability or a feature. It checks everything before its first write, so a refusal writes nothing.

   New: - A save refuses a draft that holds an ICE, a domain, a capability or a feature. It checks everything before its first write, so a refusal writes nothing. An ICE is the agent's intent for one capability or feature: what an agent must make true there, for whom, and how it is checked. The reason for refusing them: each kind has its own writer, so one wrong reading of the source cannot spread to the whole model.

   Answers: self_explanation and stranger_test: what an ICE is, and why a save refuses an ICE, a domain, a capability or a feature

### Added lines

1. Added after: A person shares something that explains what they want: a prototype, a document or plain w…

   Added: A person wants this to confirm what the product is for without writing a spec first.

   Answers: stranger_test: why a person wants this feature

2. Added after: - standards/schemas/product-os/ontology.md, in Phoenix memory: "Only a person confirms or …

   Added: - .garura/product/product-os/intents/bi-1.md: "A person confirms the intents without writing a spec."

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

3. Added after: - standards/schemas/product-os/ontology.md, in Phoenix memory: "Only a person confirms or …

   Added: - core/components/loops/complete-discovery/SKILL.md: "reads the prototype once and runs /discover-intent, /discover-domains and /discover-capabilities on that one reading"

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

4. Added after: - standards/schemas/product-os/ontology.md, in Phoenix memory: "Only a person confirms or …

   Added: - core/components/plays/discover-intent/reference/ice.md: "becomes `confirmed` only on the person's typed confirmation", "the intents rose into the process behind the screens", "left every proof open", "Nothing without a basis", "every title, outcome and limit traces to what the source shows", "no copied content", "one wrong intent spread to the whole model"

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

5. Added after: - standards/schemas/product-os/ontology.md, in Phoenix memory: "Only a person confirms or …

   Added: - core/components/plays/discover-intent/scripts/persist_intent.py: "ids become file names", "another play writes those kinds"

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

6. Added after: - standards/schemas/product-os/ontology.md, in Phoenix memory: "Only a person confirms or …

   Added: - core/components/plays/discover-intent/scripts/check_intent.py: "outcome, not build"

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

7. Added after: - standards/schemas/product-os/ontology.md, in Phoenix memory: "Only a person confirms or …

   Added: - core/components/skills/author-business-intent/SKILL.md: "Every part is mapped to the intent it serves"

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

8. Added after: - standards/schemas/product-os/ontology.md, in Phoenix memory: "Only a person confirms or …

   Added: - standards/schemas/product-os/ontology.md, in Phoenix memory: "What a person or the organisation wants, in their words"

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

9. Added after: - standards/schemas/product-os/ontology.md, in Phoenix memory: "Only a person confirms or …

   Added: - standards/schemas/product-os/ontology.md, in Phoenix memory: "The agent's intent for one capability or one feature: what an agent must make true there, for whom, and how it will be checked."

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

### Reasons not found

- Why the run stops after three rounds with the check still unclean (self_explanation). core/components/plays/discover-intent/SKILL.md says only "after 3 rounds still unclean, halt and show the person what is left"; no ADR, issue or play file gives a reason for three.

## .garura/product/product-os/software-delivery-planning/specify-product/fn-specify-domains/feature.md

Failed criteria in the judge's verdict: self_explanation, stranger_test.

### Changed lines

1. Old: - A knowledge shelf comes first. A domain with no shelf gets a proposal that names it as its research names it, with the research links. The name never comes from the product's screens or sample data. The run records the proposal and goes on.

   New: - A knowledge shelf comes first. A domain with no shelf gets a proposal that names it as its research names it, with the research links. The name never comes from the product's screens or sample data. The reason: a domain is a field the industry names, and sample data is only an example of what the product handles. The run records the proposal and goes on.

   Answers: self_explanation: why the name never comes from the screens or sample data

2. Old: - From a capture, every main section must sit in a domain, with the line from the shelf or research that covers its work and where that line is from. For a section no field covers, the run researches the field that does that work and never stretches a found field over it.

   New: - From a capture, every main section must sit in a domain, with the line from the shelf or research that covers its work and where that line is from. A main section is a main part of the prototype, such as a tab, a top menu item or a part of its first screen. For a section no field covers, the run researches the field that does that work and never stretches a found field over it. The grounding check is a script that tests this. It checks that each domain has its shelf or research and its Sources, and that each main section sits in a domain.

   Answers: stranger_test: what a main section is and what the grounding check is

3. Old: - A page that exists is grown. A light page is raised to a full one and keeps what it said. An entry's depth never goes down, no domain is added twice, and a run with nothing new changes nothing.

   New: - A page that exists is grown. A light page is raised to a full one and keeps what it said. The reason: no one play owns a domain page, so each play writes what it knows and a later play raises it. An entry's depth never goes down, no domain is added twice, and a run with nothing new changes nothing.

   Answers: self_explanation: why a page is grown and never cut back

4. Old: - The profile stays rough, at the directional state. The run never sets it firm, because the capabilities' real needs are not known yet.

   New: - The profile stays rough, at the directional state. Directional means the profile holds only the product's shape and rough quality levels. The run never sets it firm, because the capabilities' real needs are not known yet.

   Answers: stranger_test: what the directional state means

5. Old: - One checkpoint shows each domain and the profile, with the real changes to the model. A learned policy may pass a known shape of change with no wait, but only when no check found a blocking problem. Each crossing goes in a log. A cancel puts the model back.

   New: - One checkpoint shows each domain and the profile, with the real changes to the model. Run by hand, a checkpoint is where the run stops and waits for the person's yes. The reason for one: the person reviews the whole change once, and nothing is committed before that. A learned policy may pass a known shape of change with no wait, but only when no check found a blocking problem. A learned policy is a project rule learned from the person's earlier answers. A shape of change the person approved three times in a row, with no edit, may then pass. The reason: the person has already approved that shape. Each crossing goes in a log. A cancel puts the model back.

   Answers: self_explanation and stranger_test: what the checkpoint is, why there is one wait, what a learned policy is and why it may skip the wait

### Added lines

1. Added after: This feature finds each domain the product sits in and writes a full page for it. A domain…

   Added: The model needs domains because they group its capabilities into fields the industry knows, at the level a business leader talks about.

   Answers: stranger_test: why the model needs domains

2. Added after: - core/components/skills/author-domains/SKILL.md: "A recognised domain, never a made-up on…

   Added: - standards/schemas/product-os/ontology.md, in Phoenix memory: "A big area of the product that groups capabilities."

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

3. Added after: - core/components/skills/author-domains/SKILL.md: "A recognised domain, never a made-up on…

   Added: - core/components/plays/discover-domains/reference/ice.md: "Everything here is strategic and directional — CXO altitude.", "The sample data on the screens is an example of what the product handles, never its domain.", "the profile carries `state: directional` (shape dimensions + rough NFR levels only)", "Present the proposed change at a single human checkpoint and commit it to the product model only on approval."

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

4. Added after: - core/components/skills/author-domains/SKILL.md: "A recognised domain, never a made-up on…

   Added: - core/components/skills/walk-prototype/SKILL.md: "its main sections — the tabs, the top-level menu, the parts of its first screen"

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

5. Added after: - core/components/skills/author-domains/SKILL.md: "A recognised domain, never a made-up on…

   Added: - core/components/plays/discover-domains/scripts/grounding_check.py: "assert every domain /discover-domains wrote is grounded"

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

6. Added after: - core/components/skills/author-domains/SKILL.md: "A recognised domain, never a made-up on…

   Added: - standards/schemas/product-os/grounding/domain.md, in Phoenix memory: "No play owns a domain (ontology v3): any play writes the page at the depth of what it knows, and a later play raises it."

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

7. Added after: - core/components/skills/author-domains/SKILL.md: "A recognised domain, never a made-up on…

   Added: - standards/rules/gate-config.md, in Phoenix memory: "Fires unless the learned per-project policy says this change SHAPE is auto", "the human's real action is the verdict that teaches the policy"

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

8. Added after: - core/components/skills/author-domains/SKILL.md: "A recognised domain, never a made-up on…

   Added: - .garura/core/config.yaml: "streak: 3", "clean approvals a shape needs to earn auto"

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

### Reasons not found

None.

## .garura/product/product-os/software-delivery-planning/specify-product/fn-specify-capabilities/feature.md

Failed criteria in the judge's verdict: self_explanation, stranger_test.

### Changed lines

1. Old: This feature writes a full page for each capability, creates the capability's features with their pages, and sets what the capability needs in quality and compliance. It takes its work from three places: the capabilities a person names, every capability in the model still at the directional depth, and the capabilities a prototype's screens show. One run does all of them together. It is the last detailing step, so the writing is complete but still in product words, not code.

   New: This feature writes a full page for each capability, creates the capability's features with their pages, and sets what the capability needs in quality and compliance. It takes its work from three places: the capabilities a person names, every capability in the model still at the directional depth, and the capabilities a prototype's screens show. A capability at the directional depth has a short page with only its directional intent. This feature raises it to full depth, called detailed in the model's index, with its benefit hypothesis, boundary, guiding rules and features. One run does all of them together. It is the last detailing step, so the writing is complete but still in product words, not code. The earlier steps are Specify intents and Specify domains, which write the business intents and the domains, but it needs neither to run first.

   Answers: stranger_test: directional depth versus full depth, and what the last detailing step comes after

2. Old: Status: built, except checking each ICE against the rubric.

   New: Status: built, except checking each ICE against the rubric. An ICE is the agent's intent for one capability or feature: what an agent must make true there, for whom, and how it is checked. The rubric is the written rule for what a good ICE looks like.

   Answers: stranger_test: what an ICE and the rubric are

3. Old: - In: the capability's knowledge shelf, and the product profile as it stands when the run starts.

   New: - In: the capability's knowledge shelf, and the product profile as it stands when the run starts. The product profile holds the product's shape and the quality levels it commits to.

   Answers: stranger_test: what the product profile is

4. Old: - A capability seeded here holds only what its source said: the person's recorded answers, or the screens it was read from. The save refuses any other seed.

   New: - A capability seeded here holds only what its source said: the person's recorded answers, or the screens it was read from. The save refuses any other seed. The save is the one script step that writes the model's index, the profile and the decision records.

   Answers: stranger_test: what the save is

5. Old: - A named capability the model lacks starts with questions. The run asks for all of them at once, before it opens any change. With no answer, or a domain the model lacks, it stops and says what it needs, and it leaves nothing behind. Inside the loop, that capability becomes the loop's question and the others go on.

   New: - A named capability the model lacks starts with questions. The run asks for all of them at once, before it opens any change. With no answer, or a domain the model lacks, it stops and says what it needs, and it leaves nothing behind. Inside the loop, that capability becomes the loop's question and the others go on. The loop is the discovery loop, which reads a prototype once and runs Specify intents, Specify domains and this feature on that reading, in rounds.

   Answers: stranger_test: what the loop is

6. Old: - A capability from the screens with no known domain waits in a holding folder. It is kept, and it is not ready until it is linked to a domain.

   New: - A capability from the screens with no known domain waits in a holding folder. The holding folder is a place in the model for capabilities whose domain is not known yet. It is kept, and it is not ready until it is linked to a domain.

   Answers: stranger_test: what the holding folder is

7. Old: - The first run firms a still-rough profile to set, with no decision record. On a set profile, a need above its level stops at the checkpoint as its own line, and each move gets its own decision record. Inside the loop, these records read proposed.

   New: - The first run firms a still-rough profile to set, with no decision record. Set means its levels are now committed. The reason there is no record: a rough profile has no committed level yet, so firming it moves nothing. On a set profile, a need above its level stops at the checkpoint as its own line, and each move gets its own decision record. The checkpoint is the one point where the run shows the person every change and, run by hand, waits for a yes before anything is committed. Inside the loop, these records read proposed.

   Answers: self_explanation: what 'firms a still-rough profile to set' means and why the first run writes no decision record; stranger_test: what the checkpoint is

8. Old: - One run has one save, one checkpoint and one commit for all its capabilities. If one cannot pass its checks, the whole run stops and nothing is committed.

   New: - One run has one save, one checkpoint and one commit for all its capabilities. The reason: one capability at a time was too slow, and the person approves every capability and every profile move together, before anything is committed. If one cannot pass its checks, the whole run stops and nothing is committed.

   Answers: self_explanation: why all capabilities share one save, one checkpoint and one commit

9. Old: - The structure check reads the label and the length of each agent intent line. No step reads the ICE rubric yet.

   New: - The structure check reads the label and the length of each agent intent line. An agent intent line is one line of an ICE, such as its Goal. No step reads the ICE rubric yet. So nothing checks yet that an ICE keeps the rubric's rules, such as exactly one Goal.

   Answers: self_explanation: what the structure check leaves unchecked; stranger_test: what an agent intent line is

### Added lines

1. Added after: This feature writes a full page for each capability, creates the capability's features wit…

   Added: A product owner gets from it the detailed capabilities and features that later shaping work turns into slices a person can test end to end.

   Answers: stranger_test: why the feature exists, what a product owner gets from it

2. Added after: - standards/rules/ice-rubric.md, in Phoenix memory: "What a good ICE looks like."

   Added: - core/components/plays/discover-capabilities/reference/ice.md: "promote its `capability.md` from the directional stage to the detailed stage (benefit hypothesis, boundary, guiding rules, features)", "one at a time is too slow", "one human checkpoint that approves every target's detailed grounding and every box-move before anything is committed", "On a still-directional box the roll-up establishes it and firms it to `set`.", "Against an already-`set` box, a need (an NFR level or a compliance regime) that exceeds the committed ceiling is an out-of-box event", "in the holding folder `capabilities/<capability>/` with its domain empty", "is done by the deterministic keyed persist script"

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

3. Added after: - standards/rules/ice-rubric.md, in Phoenix memory: "What a good ICE looks like."

   Added: - core/components/plays/discover-domains/reference/ice.md: "Each kind has one writer: /discover-intent writes business intents, /discover-domains writes domains, /discover-capabilities writes capabilities and features. None needs another to run first", "shaping the detailed model into slices a person can test end to end"

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

4. Added after: - standards/rules/ice-rubric.md, in Phoenix memory: "What a good ICE looks like."

   Added: - core/components/loops/complete-discovery/SKILL.md: "reads the prototype once and runs /discover-intent, /discover-domains and /discover-capabilities on that one reading"

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

5. Added after: - standards/rules/ice-rubric.md, in Phoenix memory: "What a good ICE looks like."

   Added: - standards/schemas/product-os/ontology.md, in Phoenix memory: "The agent's intent for one capability or one feature: what an agent must make true there, for whom, and how it will be checked."

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

6. Added after: - standards/rules/ice-rubric.md, in Phoenix memory: "What a good ICE looks like."

   Added: - standards/rules/ice-rubric.md, in Phoenix memory: "Exactly one. This is not negotiable."

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

### Reasons not found

None.

## .garura/product/product-os/software-delivery-planning/specify-product/fn-specify-from-file/feature.md

Failed criteria in the judge's verdict: completeness, stranger_test.

### Changed lines

1. Old: - Out: the capture record, with the kind "prototype — file" and how many views were found and kept, and each view not reached with why.

   New: - Out: the capture record, with the kind "prototype — file" and how many views were found and kept, and each view not reached with why. The record also holds a fingerprint of each saved file. A fingerprint is a short code worked out from a file's bytes, so any change to the file changes the code. The run does not compare it with the original. A test can, to show the copy is exact.

   Answers: stranger_test: what a fingerprint is, the first time it is used, and why it is checked

### Added lines

1. Added after: - It finds views the same way as Specify from a deployed site (fn-specify-from-site), with…

   Added: - The browser goes two clicks deep. It clicks each control on the first screen, then each new control those views add.

   Answers: completeness and stranger_test: how deep the capture goes, stated on this page

2. Added after: - It finds views the same way as Specify from a deployed site (fn-specify-from-site), with…

   Added: - A view is found when a click reaches it. It is kept when its visible text differs from each view already kept. So a control that shows a repeat counts as found, and is not kept again.

   Answers: completeness: what found and kept mean, and the branch where a view is found but not kept

3. Added after: - It finds views the same way as Specify from a deployed site (fn-specify-from-site), with…

   Added: - The size limit is 40 views beyond the first screen, or 160 clicks. Each control not tried then goes on the record as not reached, with the limit as the reason.

   Answers: completeness and stranger_test: the limits, stated on this page

4. Added after: - It finds views the same way as Specify from a deployed site (fn-specify-from-site), with…

   Added: - A click that fails goes on the record as not reached, with the error, and the browser goes on to the next control.

   Answers: completeness: the branch where a view is not reached

5. Added after: - It finds views the same way as Specify from a deployed site (fn-specify-from-site), with…

   Added: - The browser does not follow mail, phone or script links, or any link that starts with http or https. It follows relative links.

   Answers: completeness and stranger_test: the links the capture does not follow

6. Added after: - It finds views the same way as Specify from a deployed site (fn-specify-from-site), with…

   Added: - A named control is clicked with no word test. A named control that cannot be found fails the capture.

   Answers: completeness: the named-control branch

7. Added after: - It finds views the same way as Specify from a deployed site (fn-specify-from-site), with…

   Added: - The browser does not click a control with any of these words: accept, approve, reject, drop, send back, delete, remove, edit, comment, finish, submit, undo, save, reset, log out, sign out, point, upload, pay, buy. The test also finds these words inside longer words, and the record does not list the controls it skipped.

   Answers: completeness and stranger_test: the skipped controls, stated on this page

8. Added after: - standards/schemas/product-os/ontology.md, in Phoenix memory: "a copy of the file for a f…

   Added: - core/components/plays/discover-intent/scripts/capture_source.py: "Find every view the page offers, two clicks deep", "a control whose view repeats one already kept is found but not kept again", "MAX_VIEWS = 40", "MAX_CLICKS = 160", "the exploration limit was reached", "record it, keep exploring", "leaves the prototype", "Controls that answer or change data rather than show a view: never clicked while exploring.", "a named control that cannot be found is a failure, not a skip", "def sha256(path):"

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

9. Added after: - standards/schemas/product-os/ontology.md, in Phoenix memory: "a copy of the file for a f…

   Added: - core/components/plays/discover-intent/reference/ice.md: "The Source is kept as it was when read"

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

10. Added after: - standards/schemas/product-os/ontology.md, in Phoenix memory: "a copy of the file for a f…

   Added: - .garura/product/product-os/software-delivery-planning/specify-product/capability.md: "A fingerprint is a short code worked out from a file's bytes, so any change to the file changes the code."

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

### Reasons not found

None.

## .garura/product/product-os/software-delivery-planning/specify-product/fn-specify-from-folder/feature.md

Failed criteria in the judge's verdict: self_explanation, stranger_test.

### Changed lines

1. Old: A person gives a project folder. The run treats it as two Sources: the project's written docs and its running app. It keeps the docs first. It then starts the app the way the README (the project's main instruction file) says, captures the running app the way it captures a deployed site, and stops the app. The intent draft reads both Sources together.

   New: A person gives a project folder. The run treats it as two Sources: the project's written docs and its running app. It keeps the docs first. It then starts the app the way the README (the project's main instruction file) says, captures the running app the way it captures a deployed site, and stops the app. The intent draft reads both Sources together. A Source is a saved copy of what a person gave, which later steps read instead of the original. A folder gives two because a runnable source is also run through, so what it does is seen, not only what its docs say. The intent draft is the first version of the business intents, which the person then confirms or drops.

   Answers: self_explanation and stranger_test: why a folder is two Sources, and what a Source and the intent draft are

2. Old: - Out: the docs Source: a copy of each written doc at the top of the folder. Its capture record reads "prototype — project".

   New: - Out: the docs Source: a copy of each written doc at the top of the folder. Its capture record reads "prototype — project". A capture record is what each capture writes about its Source: its kind, the date it was read, who gave it and its saved files.

   Answers: stranger_test: what a capture record is

3. Old: - The agent running the work starts and stops the app by following the README. No fixed script does this, and no check confirms that the app stopped.

   New: - The agent running the work starts and stops the app by following the README. No fixed script does this, and no check confirms that the app stopped. So an app left running after the capture is not caught.

   Answers: self_explanation: what the missing stop check risks

4. Old: - Both Sources link to every intent the run confirms.

   New: - Both Sources link to every intent the run confirms. An intent is confirmed when the person types confirm for it.

   Answers: stranger_test: what a confirmed intent is

### Added lines

1. Added after: - core/components/plays/discover-intent/reference/ice.md: "A project folder is two Sources…

   Added: - core/components/plays/discover-intent/reference/ice.md: "a runnable source is also run through, so what it does is seen, not only what it says", "becomes `confirmed` only on the person's typed confirmation"

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

2. Added after: - core/components/plays/discover-intent/reference/ice.md: "A project folder is two Sources…

   Added: - core/components/plays/discover-intent/SKILL.md: "draft the person's Business Intents from these sources and their answers", "ask the person to type one of"

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

3. Added after: - core/components/plays/discover-intent/reference/ice.md: "A project folder is two Sources…

   Added: - core/components/plays/discover-intent/scripts/capture_source.py: "takes its snapshot into the run's evidence folder, so it outlives the link or the file, and writes the source manifest"

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

4. Added after: - core/components/plays/discover-intent/reference/ice.md: "A project folder is two Sources…

   Added: - .garura/product/product-os/software-delivery-planning/specify-product/capability.md: "Later steps read this copy, so they do not need the original."

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

### Reasons not found

- Why only .md and .txt files at the top of the folder are kept, and not subfolders or other formats (self_explanation). capture_source.py and the play's SKILL.md and ice.md state the rule ("top-level written docs (README, SPEC, *.md, *.txt)") but give no reason, and the commit that added it (94c51bff, #612) gives none.
- Why the agent starts the app by following the README rather than a fixed script (self_explanation). The SKILL.md says "start the project the way its README says" with no reason. The page now states only the consequence of the missing stop check, which follows from what is built.

## .garura/product/product-os/software-delivery-planning/specify-product/fn-specify-from-site/feature.md

Failed criteria in the judge's verdict: self_explanation.

### Changed lines

1. Old: - The browser does not click a control with any of these words: accept, approve, reject, drop, send back, delete, remove, edit, comment, finish, submit, undo, save, reset, log out, sign out, point, upload, pay, buy. This is a list of words, so a button such as "Create" or "Confirm" is clicked. The test also finds these words inside longer words, so a tab named "Payments" or "Appointments" is skipped. The record does not list the controls it skipped.

   New: - The browser does not click a control with any of these words: accept, approve, reject, drop, send back, delete, remove, edit, comment, finish, submit, undo, save, reset, log out, sign out, point, upload, pay, buy. The reason: these controls answer or change data rather than show a view. On a deployed site, only a journey the person cleared may change data. This is a list of words, so a button such as "Create" or "Confirm" is clicked. The test also finds these words inside longer words, so a tab named "Payments" or "Appointments" is skipped. The record does not list the controls it skipped.

   Answers: self_explanation: why the controls with these words are never clicked

### Added lines

1. Added after: - standards/schemas/product-os/ontology.md, in Phoenix memory: "screenshots and images for…

   Added: - core/components/plays/discover-intent/reference/ice.md: "a step that changes data (pay, delete, submit, accept …) is taken only when the person said the site is safe for it"

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

### Reasons not found

- Why the size limit is 40 views or 160 clicks (self_explanation). capture_source.py sets MAX_VIEWS = 40 and MAX_CLICKS = 160 and records "the exploration limit was reached"; neither the play nor the commit that added them (d617f19a, #613) says what the limit protects against.

## .garura/product/product-os/software-delivery-planning/specify-product/fn-specify-from-document/feature.md

Failed criteria in the judge's verdict: self_explanation, stranger_test.

### Changed lines

1. Old: A person gives a document, such as a brief or a PDF. The run saves an exact copy under the document's own name, with the run's evidence, so the document outlives the original file. At this step the run does not open or read the document. A later step reads the copy and writes what it shows in a separate record beside the copy.

   New: A person gives a document, such as a brief or a PDF. The run saves an exact copy under the document's own name, with the run's evidence, so the document outlives the original file. The run's evidence is the folder where a run keeps what it read and did, committed with its change. At this step the run does not open or read the document. A later step reads the copy and writes what it shows in a separate record beside the copy.

   Answers: stranger_test: what the run's evidence is

2. Old: - Any file whose name does not end in .html or .htm counts as a document. A video counts too, so today a video is only copied. Reading one belongs to Specify from a video (fn-specify-from-video), and it is not built.

   New: - Any file whose name does not end in .html or .htm counts as a document. The reason: a web-page file is a prototype, and Specify from a file (fn-specify-from-file) captures it view by view in a browser. A video counts too, so today a video is only copied. Reading one belongs to Specify from a video (fn-specify-from-video), and it is not built.

   Answers: self_explanation: why the .html and .htm split exists

3. Old: - The capture does not open the file. So a damaged file, or a format no later step can read, passes this step.

   New: - The capture does not open the file. The reason: this step only keeps and records, and saying what a document shows is judgment that a later step does. So a damaged file, or a format no later step can read, passes this step.

   Answers: self_explanation: why the capture leaves the file unopened

4. Old: - The capture record holds the fingerprint of the saved copy. No step works out the original's fingerprint or compares the two.

   New: - The capture record holds the fingerprint of the saved copy. A fingerprint is a short code worked out from a file's bytes, so any change to the file changes the code. No step works out the original's fingerprint or compares the two. So the run cannot tell when the copy differs from the original.

   Answers: self_explanation and stranger_test: what a fingerprint is, and what follows from no step comparing it with the original

5. Old: - Given a brief in a file, when it is captured, then the fingerprint of the copy equals one worked out from the original and the record reads "document".

   New: - Given a brief in a file, when it is captured, then the record reads "document" and holds the copy's fingerprint, which equals one the test works out from the original.

   Answers: stranger_test: removes the clash with the rule; the test, not the run, works out the original's fingerprint

### Added lines

1. Added after: - standards/schemas/product-os/ontology.md, in Phoenix memory: "It is kept as it was when …

   Added: - core/components/plays/discover-intent/SKILL.md: "Each Source's snapshot goes to the issue's evidence folder", "committed with the run, so it outlives the link or the file", "An HTML file is copied and rendered"

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

2. Added after: - standards/schemas/product-os/ontology.md, in Phoenix memory: "It is kept as it was when …

   Added: - core/components/plays/discover-intent/scripts/capture_source.py: "a copy of the file + a rendered screenshot of every view", "is judgment and is filled in later by the play; this script only keeps and records"

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

3. Added after: - standards/schemas/product-os/ontology.md, in Phoenix memory: "It is kept as it was when …

   Added: - .garura/product/product-os/software-delivery-planning/specify-product/capability.md: "A fingerprint is a short code worked out from a file's bytes, so any change to the file changes the code."

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

### Reasons not found

None.

## .garura/product/product-os/software-delivery-planning/specify-product/fn-specify-from-words/feature.md

Failed criteria in the judge's verdict: self_explanation, stranger_test.

### Changed lines

1. Old: A person types what they want, with no file or link. The agent running the work writes those exact words into a working file. A script then copies this file byte for byte into the run's evidence. The kept text is the Source, and the run drafts its intents from it. Nothing edits the kept text after that.

   New: A person types what they want, with no file or link. The agent running the work writes those exact words into a working file. A script then copies this file byte for byte into the run's evidence. The run's evidence is the folder where a run keeps what it read and did, committed with its change. The kept text is the Source, and the run drafts its intents from it. A Source is a saved copy of what a person gave, which later steps read instead of the original. Nothing edits the kept text after that. The reason: the Source is kept as it was when read, so every later step can go back to what the person said.

   Answers: stranger_test and self_explanation: what the run's evidence and a Source are, and why the words are kept byte for byte

2. Old: - In: what the person typed, held in a working file, and who gave it.

   New: - In: what the person typed, held in a working file, and who gave it. Who gave it is the git user running the work.

   Answers: self_explanation: who 'who gave it' is

3. Old: - Out: the capture record, with the kind "statement".

   New: - Out: the capture record, with the kind "statement". The record also holds a fingerprint of the kept text. A fingerprint is a short code worked out from the text's bytes, so any change to the text changes the code.

   Answers: stranger_test: what a fingerprint is

4. Old: - What the person says later goes in the answers record. The kept text stays as it was.

   New: - What the person says later goes in the answers record. The answers record keeps each reply the person types to a question, exactly as typed. The kept text stays as it was.

   Answers: stranger_test: what the answers record is

### Added lines

1. Added after: - A missing working file fails the capture.

   Added: - No name for who gave it also fails the capture.

   Answers: self_explanation: what happens when no giver can be named

2. Added after: - standards/schemas/product-os/ontology.md, in Phoenix memory: "the exact text for a state…

   Added: - core/components/plays/discover-intent/reference/ice.md: "The Source is kept as it was when read"

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

3. Added after: - standards/schemas/product-os/ontology.md, in Phoenix memory: "the exact text for a state…

   Added: - core/components/plays/discover-intent/SKILL.md: "The given-by is the git user running the play", "Record each reply in `<working>/answers.yaml` exactly", "committed with the run, so it outlives the link or the file"

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

4. Added after: - standards/schemas/product-os/ontology.md, in Phoenix memory: "the exact text for a state…

   Added: - core/components/plays/discover-intent/scripts/capture_source.py: "given-by is empty — it must be the git user running the play", "def sha256(path):"

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

5. Added after: - standards/schemas/product-os/ontology.md, in Phoenix memory: "the exact text for a state…

   Added: - .garura/product/product-os/software-delivery-planning/specify-product/capability.md: "Later steps read this copy, so they do not need the original.", "A fingerprint is a short code worked out from a file's bytes, so any change to the file changes the code."

   Answers: Sources: the quoted words this redraft rests on (rule 3: every new source with its quoted words).

### Reasons not found

- Why who gave the words is recorded (self_explanation). The play's ice.md, SKILL.md and the ontology's Source kind require it ("who gave it (the git user running the play)") but give no reason. The page now says who it is (the git user running the work) and what happens when it is missing.
