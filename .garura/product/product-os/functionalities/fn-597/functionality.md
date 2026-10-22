# Functionality: Rebuild the product model as an ontology

## What it does
The ontology is the written set of rules for the product model. It defines each kind of node that a plan uses: Business Intent, Capability, Functionality, Work and Plan. It also defines the needs and identified-by links, the loose domains and the ready rule. Each kind has examples from more than one domain.
- This page uses three terms. First, the questions Q1 to Q7 are the fixed list of questions that the ontology must answer about a product. For example, Q7 asks: "given a business intent, what is its plan?"
- Second, the spine (`_spine.yaml`) is the file that lists each model node and its links.
- Third, "needs" means this node cannot be built until that node is done. "Identified by" means this node was found during work on that node.
- The ontology is one written agreement, at `core/components/memory/standards/schemas/product-os/ontology.md`. A person and an agent both read it, so they use the same words for the same things. It says what each kind is, what it holds, how it connects and what must always be true.
- It grows one kind at a time, through the author-product-ontology skill, with the plan owner (the person who plans work toward a business intent). A script (check_ontology.py) checks its format, so it cannot change into free text.
- This functionality delivered version 5 (2026-10-21). Version 5 added Capability, Functionality, Work and Plan, the needs and identified-by links, the loose domains, the new ready rule and question Q7.

## Inputs / Outputs
- In: the questions that the ontology must answer (Q1 to Q7), the earlier version (v4), and the plan design and change list for #621.
- In: the plan owner's rulings of 2026-10-21. Nothing is blocked. Business intents are connected, not dependent. Domains are out of the plan tree.
- Out: the ontology file at version 5. For each kind, it gives what the kind is, who reads it and where it lives. It also gives a properties table, a relationships table, rules, states where they apply, and examples.
- Out: a log line for each version. The line says what changed and where the working notes are (`.garura/project/issues/621/specs/ontology-run.md` for v5).
- Out: the status of each question (answered, partly or not yet), and which kinds and links answer it.

## Rules & behavior
- Each kind that a plan uses is defined under "Kinds", not left under "Not yet defined". A play cannot write or check a kind that the ontology does not define. Thus a plan that names an undefined kind cannot be trusted.
- A kind that the tree, the file or the tracker link of a plan names is a kind that a plan uses.
- Domain stays under "Not yet defined" on purpose, because it is not a level of a plan. Its links are given there, and in the Capability and Business Intent kinds.
- Tracker Issue also stays under "Not yet defined". The tracker is where work is ordered, and it is not part of the product model.
- A plan gets to the tracker through Work. The "Issue" property of Work holds the tracker number, so the model needs only that number.
- Each kind has examples from more than one field (shop, clinic, bank). Thus the rules do not lean toward one type of product.
- Rules tell what is true when the product is aligned. They never stop a write. The model grows as plans are built in any order, and a blocked write would lose work that was already found.
- Only a person confirms or drops a business intent. A business intent is the goal of that person, and an agent must not decide it for them.
- A change to the ontology goes through author-product-ontology, one kind at a time, with the plan owner. Nobody edits it freehand. Thus the person who owns the model agrees to each change, and check_ontology.py can still check the format.
- The ontology calls the spine field `depends_on` ("needs") until the rename under #725 is done. Thus the words on the page and the field in the files never disagree without a note.
- Each change raises the version in the front matter and adds a log line. Thus a play or a person can tell which rules a page was written against. They can also find the working notes for that change.

## Acceptance criteria
- Given the ontology on this branch, when check_ontology.py runs on it, then it passes with no errors.
- Given the ontology, when a reader looks for Business Intent, Capability, Functionality, Work and Plan, then each has its own section under "Kinds" with properties, relationships, rules and examples.
- Given question Q7 ("what is its plan"), when a reader looks at its status, then it reads "answered" and names Plan, Capability, Functionality and Work.
- Given any kind defined in v5, when a reader counts its examples, then they come from at least two different fields.
- Given the Capability and Functionality kinds, when a reader looks at the ready rule, then it says that a node is ready when it serves a confirmed business intent and nothing it needs is open, and that a missing domain never blocks.
- Given the front matter and the log, when a reader checks them, then the version is 5, and a dated log line describes the v5 change and links its working notes.

## Out of scope
- Where the design outputs for the full project live (ADR 028, open question 3). There is no owner yet. Nobody has filed an issue to settle it. It stays tracked only as deferred in ADR 028, question 3. Version 5 does not answer it.
- Changing the ready check script. A capability or functionality is ready without a domain (fn-724) owns that.
- Checking that links point at real nodes, and the rename of `depends_on` to `needs`. fn-725 owns those.
- The full definition of the Domain and Tracker Issue kinds. A later ontology version owns it, written through the author-product-ontology skill with the plan owner, one kind at a time. Until then, both stay under "Not yet defined".

## Sources
- core/components/memory/standards/schemas/product-os/ontology.md, front matter "version: 5", and its log: "v5 (#597, plan #722, …): Capability, Functionality, Work and Plan defined."
- Q7 in the ontology: "Given a business intent, what is its plan … **Status:** answered".
- .garura/project/issues/621/specs/change-list.md: "F4.4 The ontology defines every kind plans use — Story #597 (reused, Feature → Story)".
- docs/adr/028-agentic-lifecycle-five-loops.md, question 3: "**Deferred.** The product model is to be rebuilt as an ontology".
- GitHub #597 (closed): "Rebuild the product model as an ontology".
- Shelf: none. No domain shelf holds the product model of a framework itself (routing for #723).

## Agent intent (ICE)
- Goal: every kind a plan uses is defined in the ontology, with examples from more than one domain.
- Goal: the ontology's links and ready rule match what the spine schema and the ready check do.
- Limit: one kind at a time, through author-product-ontology, with the plan owner.
- Limit: the ontology never claims a question is answered that its kinds do not answer.
- Fails if: a kind a plan uses is still under "Not yet defined".
- Fails if: the ontology and the spine schema give different ready rules.
- Context: serves the plan owner and every play and agent that reads or writes the product model; touches ontology.md, the author-product-ontology skill and check_ontology.py, and is read by the spine schema; in are the kinds and their rules, out is the ADR 028 design-outputs question.
- Checked by: check_ontology.py passes, and Q7 is marked answered.
- Checked by: a reader finds the same ready rule in the ontology's Capability kind and in the spine schema's tree rules.
