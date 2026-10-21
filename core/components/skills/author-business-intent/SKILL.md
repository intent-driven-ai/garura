---
name: author-business-intent
description: Draft the person's Business Intents from what a person shared — a prototype (its saved snapshot), a document, or a plain statement — plus their own answers. One business intent per need the product meets for its user, never merged, with every part of the source mapped to the intent it serves. Each names that need at the level of the product and in its users' words, and holds title, outcome, why, asked by (a persona), proof it is met (measurable), must not, and the provenance of every property; why, asked by and proof are drafted with their basis, never left open or asked. Drafts business intents only (ADR 043) — no ICE, capability or domain; other plays write those. Also writes what each source shows and the questions the sources cannot answer, each with example answers. Written for a business reader, never a description of the source. Generative artifact production for the /intent play; writes the draft only, never the product model. Use when /intent needs the intents drafted, or re-drafted after the person answers.
user-invocable: false
model: opus
allowed-tools: Read, Write, Glob
---

# author-business-intent

Turns what a person shared into a **draft** of the person's **Business Intents**, a kind of the
product ontology (`standards/schemas/product-os/ontology.md`): each need the product meets for
its user, with why the business needs it, who asks for it, and how we will know it is met. One
business intent per thing the product offers its user — follow the product's own main areas.

You draft business intents only (ADR 043). No ICE, no capability, no domain: `/vision` writes
the domains and `/understand` the capabilities and functionalities with their ICE, each from the
screens itself; the links between the kinds are made later.

The person confirms or drops each business intent later; you only draft.

The source shows *one way* the intents could be built. You pull out what the person needs and
wants, and leave how the source does it behind (IDD Principle 1).

## Input

| Field | Required | Meaning |
|-------|----------|---------|
| `source_manifests` | yes | One or more Source manifests — each with its kind, `snapshot_dir` and snapshot files (screenshots with their text, page HTML, the copied file, or the statement text). A project folder gives two: its written docs and the running app. All are read together |
| `journeys` | for a prototype | The prototype's journeys (`journeys.yaml`, from `walk-prototype`): who it serves, what each sets out to do, the steps walked and what they showed, what they end with. A prototype's intents are drafted from these (C15) |
| `memory_context` | no | What the agent found in memory about the product — what it is, its domain, who uses it — as short-term copies |
| `model` | no | On a later round of a loop: the product model the loop's other plays wrote (read only) |
| `answers` | no | The person's answers so far (`<working>/answers.yaml`): replies to earlier questions (with the examples offered and whether one was picked), intents they stated, items they named as missing or merged, and any correction |
| `draft_path` | yes | Where to write the draft (`<working>/intent-draft.yaml`) |
| `ontology_path` | yes | The ontology, copied into short-term memory by the agent through the memory tool. Read this copy — never memory itself (ADR 039). |

## Process

0. **Read the source as the product.** The screens show what the product offers its user.
   Their sample data is only an example of what the product handles: write each intent so it
   holds for any such content, and never name the sample's specifics — its company, its items,
   its counts (a work-tracking tool shown with a bakery's tasks is about any team's work, not
   the bakery). Any process, tool or system the screens talk about is content the product
   shows: describe what the user gets from the product, never how that process works behind
   it. Write in the words the product's own users would use. You may know the tools that run
   this drafting; the product does not, so their words never appear in an intent.
   **For a prototype, start from its main areas and journeys.** Each main area the product
   offers its user — a menu item, a section, a tab — and each journey through it is where a
   business intent comes from: one business intent per need the product meets there, named
   at the level of the product (it names the journey it came from: `from_journey`). **Every
   main section has a business intent of its own**, from its own journey; never fold one
   section's need into another section's intent. A business
   intent is never a rule the system enforces ("only approved items are used" is a rule; "able
   to see every piece of work on one board, by its stage" is what a person gets). The steps of
   a journey are where its outcome comes from.

   An example, from a work-tracking tool (not this product):

   > **Title:** Able to see every piece of work on one board, by its stage
   > **Outcome:** A team lead opens the Board and sees each item in its stage column; opening
   > an item shows its owner, its due date and what it waits on.
   > **Why:** The team's work is spread over many tools; the lead needs one place to see where
   > work stands before planning the week.
   > **Asked by:** A team lead who plans a software team's work
   > **Proof it is met:** Nine in ten of the team's items are on the board, and the lead plans
   > the week from it without asking anyone for status.

   **Use what memory and the model hold.** Context the agent copied from memory (what the
   product is, its domain, who uses it) and, on a later round of a loop, what the model holds
   (the domain and capabilities `/vision` and `/understand` wrote) may sharpen `why`, `proof`
   and `asked_by` — provenance `memory` or `model`.
1. **Read the ontology's Business Intent kind** — its properties and rules. Then
   read every snapshot file every manifest lists: look at every screenshot (one per page or
   tab) and read its text, the documents, or the statement.
2. **List the parts of what the sources show.** Go page by page and tab by tab. For each part,
   write one plain line: what a person can see, decide or do there. Do not skip a part
   because it looks small. This is the coverage list.
3. **Group the parts by the need they meet.** Group the parts by what the person gets from
   them — the need a main area of the product meets for its user. Each group is one business
   intent. Two parts that serve the same need share an intent; two that serve different needs
   are two. Every part is mapped to the intent it serves (the coverage map); never merge two
   needs, never leave a part out.
4. **Write each business intent.** Name the need at the level of the product, and write its
   outcome: what the person can do or see when the need is met. Ask "why does the person want
   this?" once: the answer is the intent's `why`, not a new, higher intent. Keep an intent the
   person stated even if no part of the source shows it; no part maps to it. Qualities that
   every intent must keep — fresh, trusted, private — are `must_not` limits, not intents.
   Never write screens, fields, tabs, charts, or how the source works.
5. **Draft why, asked by and proof yourself, with their basis.** `title` and `outcome` come
   from what the source and its journeys show (provenance `source` or `journey`), or from the
   person. `why`, `asked_by` and `proof` are yours to draft — never left empty, never asked:
   - `asked_by` — a persona: a role the product's domain knows and what that role does there
     ("a team lead who plans a software team's work"), never a task ("a person who is asked
     to…") and never a step in a process. One person who uses several sections is one persona:
     name the same role across those intents.
   - `why` — the business reason the product needs this, read from what the product is for.
   - `proof` — a result someone can measure, with a number or a clear yes/no, about the need
     being met for the persona. The build itself is checked separately: the product passes
     the journeys this intent came from.
   Record each as provenance `proposed` with its basis in `basis.<property>`: what in the
   source, the journeys, memory or the model it rests on. Where the source or memory states
   it outright, use that provenance instead. The person confirms or corrects these.
6. **Ask only what nothing can draft.** A question goes to the person only when the source,
   its journeys and memory give no basis at all for a property other than why, asked by and
   proof. Give it up to three example answers, drawn from the sources and the person's words
   so far.
7. **Write for a business reader.** Plain sentences a business person reads without another
   document open. No code, no file paths, no jargon, no bare labels.
8. **Summarise what each source shows** in two to four plain sentences (`sources[].shows`).
   This describes the source; the intents do not.
9. **Apply the answers.** Take each reply as the person's own words (provenance `person`); a
   reply marked as a picked example stays marked. Add intents they named as missing,
   split ones they named as merged, apply any other correction, and fill each answered
   question's `answer` with their reply.

## Output

Write `draft_path`, and return its path — never the content:

```yaml
intents:
  - id: <short-slug-from-the-title>
    title: <the need, at the level of the product, in its users' words>
    outcome: <what the person can do or see when the need is met>
    why: <the business reason the product needs it>
    asked_by: <a persona: the role and what they do in the domain>
    proof: <a measurable result: a number or a clear yes/no>
    must_not: <limits the person stated, and qualities every intent keeps>   # optional
    from_journey: <the journey it came from>       # for a prototype
    provenance: { title: source|journey|person, outcome: …, why: proposed|…, asked_by: …, proof: …, must_not: … }
    basis: { why: <what it rests on>, asked_by: …, proof: … }   # for each `proposed` property
sources:
  - snapshot_dir: <the manifest's snapshot_dir, exactly>
    shows: <what this source shows, in plain words>
coverage:
  - part: <one part of what a source shows, in plain words>
    intent: <the id of the business intent it serves>
questions:
  - intent: <an intent id, or "all">
    ask: <a plain question for the person>
    examples: [<up to three example answers>]
    answer: ""                                    # filled from answers on the next pass
```

## Constraints

- **Draft only.** Never write the product model, and never set a stage — only the person confirms or drops.
- **Business intents only (ADR 043).** No `ice`, `domains`, `capabilities` or `functionalities` in the draft — other plays write those kinds.
- **One intent per need; every part mapped.** Never merge two needs; never leave a part unmapped.
- **Intents above, not beside.** A business intent says what the business wants; it never restates what the source shows.
- **Outcome, not build.** Nothing that describes the source belongs in an intent.
- **Nothing without a basis.** Title and outcome come from what the source shows or the person said. Why, asked by and proof are drafted, each with its basis — never left open, never asked.
- **The product, not the machinery or the sample.** An intent names what the product's user gets, in the product's words — never the process or tools behind the screens, and never the sample data's specifics.
- **Plain words.** The draft is read by a business person.

## Questions that make sense to the person

A question is for whoever shared the source — for Discovery, the person who gave the prototype.
Write each one so that person can answer it without knowing Garura's words:

- Ask about something they have seen: name the intent or part in their words, never an id.
- Never ask for why, asked by or proof: draft them (step 5).
- One question, once: when the same question applies to several intents, ask it once with
  `intent: all` — never once per intent.
- Say what it is for in one plain clause ("so the agents know who to build it for").
- Give up to three example answers, drawn from the journeys and memory, not made up.
- Record `intent`, the `property` it fills, `ask`,
  `examples`, and `for_person: false` when a later play or memory may still answer it.
