# Feature: Specify intents

## What it does
A person shares something that explains what they want: a prototype, a document or plain words. This feature reads it and drafts one business intent for each need the product meets for its user. A business intent names that need in its users' words, and holds an outcome, why the business wants it, who asks for it, a proof someone can measure and any limits. The person then confirms or drops each one. Each confirmed intent is saved as a page in the product model, linked to the Sources it came from.
A person wants this to confirm what the product is for without writing a spec first.

Status: built, except reading existing intents, writing attribution, choosing a depth, and marking a part as not an intent.

## Inputs / Outputs
- In: one or more Sources, each with its saved files and its capture record. The Specify-from features make these.
- In: a prototype's journeys, from Specify from a prototype's journeys (fn-specify-from-journeys). A document or plain words have none.
- In: the person's answers so far, in their exact words, with the examples they were offered and whether they picked one.
- In: the Business Intent kind in the ontology, which is the agreed map of what each kind of part holds.
- In: on a later round of the discovery loop, what the other two writers put in the model. It only reads these. The discovery loop reads a prototype once and runs three writers on that reading, in rounds. The other two writers are Specify domains and Specify capabilities.
- Out: one page for each saved intent, with its title, outcome, why, asked by, proof it is met, any must-not, its stage and its Sources. The stage is proposed until the person confirms the intent, and then it reads confirmed. Each page is named by the intent's short name, its id, such as bi-1.
- Out: one Source record beside each saved Source, with its kind, the date it was read, its saved files, what it shows in plain words, who gave it and every intent it shows.
- Out: a run record that says whether each intent was decided, each Source was saved and each link exists on both sides.
- Out: inside the loop, the open questions for the loop to ask, each with what it is about, what it blocks and its example answers.

## Rules & behavior
- Not built: reading existing intents. The draft does not read the intent pages already in the model, so it cannot say that a new draft repeats or clashes with one.
- Not built: writing attribution. The person sees a map from each part of the source to its intent, but the run keeps this map only in its working files. It writes no attribution record for a judge to read.
- Depth is fixed today. The draft always writes at the level of the product. The reason: in an earlier run, asking "why?" again and again took the intents above the product, into the process behind its screens. No step asks for a depth preference or reads one yet.
- Parts are grouped by need. The draft groups the parts of a source by what the person gets from them. Each main section of a prototype gets an intent of its own, and each intent names the journey it came from.
- Every part must map to an intent. The check reports any part with no intent, and the draft goes back to be fixed. A part cannot yet be marked as not an intent, with its reason.
- A rule or a quality is not an intent. "Only approved items are used" is a rule the system enforces, and "fresh" or "private" is a quality. A quality goes in as a must-not line. A part that shows a rule maps to the intent whose need the rule serves.
- The draft writes why, asked by and proof itself and names its basis. It never asks for them and never leaves them open, and the person corrects them when they decide. The reason: an earlier run that left them open ended with every proof open. Asked by is a persona: a role the field knows and what it does there, such as "a team lead who plans a software team's work".
- Each filled property records where it came from: the source, a journey, memory, the model, the person, or our own proposal with its basis. A title, an outcome or a limit cannot be our own proposal. The reason: these three say what the person wants, so each must rest on one of the other bases, not on our own proposal.
- The check refuses a title, outcome or proof that copies eight or more words in a row from the source. The reason: an intent states the outcome the person wants, not a copy of the source. It also refuses code-like text, and any property under three words except asked by.
- A question goes to the person only when nothing else can answer it, with up to three example answers. A reply that matches an example is marked as picked, so it stays clear who wrote it. After three rounds with the check still unclean, the run stops and shows the person what is left.
- Before deciding, the person sees what each source shows and the map of its parts. They can type "missing" or "merged" to send the draft back.
- For each intent, the person types confirm, drop, change or stop. Confirm and drop record their exact words. Change goes back to the draft. Stop saves nothing and ends the run as halted. A dropped intent is not saved.
- A save refuses a draft that holds an ICE, a domain, a capability or a feature. It checks everything before its first write, so a refusal writes nothing. An ICE is the agent's intent for one capability or feature: what an agent must make true there, for whom, and how it is checked. The reason for refusing them: each kind has its own writer, so one wrong reading of the source cannot spread to the whole model.
- Inside the loop, the save stores every intent as proposed, and names each gap as open. A later round updates only pages this same loop saved that are still proposed.

## Acceptance criteria
- Given a prototype with three main sections, when the draft is checked against the journeys, then each section has an intent of its own and each intent names the journey it came from.
- Given a draft with a part that maps to no intent, when the check runs, then it reports that part and the run does not go on to the person's decision.
- Given a draft whose proof reads "to be confirmed", when the check runs, then it reports the proof as left open and no question about it goes to the person.
- Given a decision with no typed reply, when the save runs, then it refuses and writes nothing.
- Given a person who types stop, when the run ends, then no intent page exists and the run reads halted with the reason.
- Given an intent page that already has the same short name, when the save runs by hand, then it refuses and the page stays as it was.
- Given a run inside the loop, when the save runs, then each saved intent reads proposed and no person's decision is on record.

## Out of scope
- Sorting what is given against the intents that exist. Specify against what exists (fn-specify-against-existing) will do this, and it is not built.
- Checking that what was given was fully used. Validate the attribution (fn-validate-attribution) will do this, and it is not built.
- Keeping each kind of source. Specify from a file (fn-specify-from-file), a project folder (fn-specify-from-folder), a deployed site (fn-specify-from-site), a document (fn-specify-from-document) and plain words (fn-specify-from-words) do this.
- Writing domains, capabilities and features. Specify domains (fn-specify-domains) and Specify capabilities (fn-specify-capabilities) do this.

## Sources
- The product owner approved this page and its ICE on 2026-11-06.
- core/components/plays/discover-intent/reference/ice.md: "Nothing merged, nothing lost", "Questions help the person answer", "The product, at the product's level", "Only a person confirms"
- core/components/plays/discover-intent/SKILL.md: "ask the person to type one of", "after 3 rounds still unclean"
- core/components/plays/discover-intent/scripts/persist_intent.py: "Every check runs before the", "a business intent is never overwritten"
- core/components/plays/discover-intent/scripts/check_intent.py: "copy no run of 8 or more words from the", "maps to no business intent"
- core/components/skills/author-business-intent/SKILL.md: "One business intent per thing the product offers its user", "a team lead who plans a software team's work"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "Only a person confirms or drops it; an agent never does."
- .garura/product/product-os/intents/bi-1.md: "A person confirms the intents without writing a spec."
- core/components/loops/complete-discovery/SKILL.md: "reads the prototype once and runs /discover-intent, /discover-domains and /discover-capabilities on that one reading"
- core/components/plays/discover-intent/reference/ice.md: "becomes `confirmed` only on the person's typed confirmation", "the intents rose into the process behind the screens", "left every proof open", "Nothing without a basis", "every title, outcome and limit traces to what the source shows", "no copied content", "one wrong intent spread to the whole model"
- core/components/plays/discover-intent/scripts/persist_intent.py: "ids become file names", "another play writes those kinds"
- core/components/plays/discover-intent/scripts/check_intent.py: "outcome, not build"
- core/components/skills/author-business-intent/SKILL.md: "Every part is mapped to the intent it serves"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "What a person or the organisation wants, in their words"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "The agent's intent for one capability or one feature: what an agent must make true there, for whom, and how it will be checked."
