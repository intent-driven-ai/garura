---
name: author-business-intent
description: Draft two levels of intent from what a person shared — a prototype (its saved snapshot), a document, or a plain statement — plus their own answers. The lower level is ICE — one per separate thing the source lets the person see, decide or do, as plain goals, never merged, with every part of the source mapped to one. The upper level is the person's Business Intents; each ICE is built from one of them. Each business intent names a need the product meets for its user, at the level of the product and in its users' words, and holds title, outcome, why, asked by (a persona), proof it is met (measurable), must not, and the provenance of every property; why, asked by and proof are drafted with their basis, never left open or asked. Also writes what each source shows and the questions the sources cannot answer, each with example answers. Written for a business reader, never a description of the source. Generative artifact production for the /intent play; writes the draft only, never the product model. Use when /intent needs the intents drafted, or re-drafted after the person answers.
user-invocable: false
model: opus
allowed-tools: Read, Write, Glob
---

# author-business-intent

Turns what a person shared into a **draft** of two levels of intent, both kinds of the product
ontology (`standards/schemas/product-os/ontology.md`):

- **ICE** — the agents' level: the separate things the person must be able to see, decide or
  do. A source shows this level best.
- **Business Intents** — the person's level: each need the product meets for its user, with
  why the business needs it, who asks for it, and how we will know it is met. One business
  intent per thing the product offers its user — follow the product's own main areas.

The person confirms or drops each business intent later; you only draft.

The source shows *one way* the intents could be built. You pull out what the person needs and
wants, and leave how the source does it behind (IDD Principle 1).

## Input

| Field | Required | Meaning |
|-------|----------|---------|
| `source_manifests` | yes | One or more Source manifests — each with its kind, `snapshot_dir` and snapshot files (screenshots with their text, page HTML, the copied file, or the statement text). A project folder gives two: its written docs and the running app. All are read together |
| `journeys` | for a prototype | The prototype's journeys (`journeys.yaml`, from `walk-prototype`): who it serves, what each sets out to do, the steps walked and what they showed, what they end with. A prototype's intents are drafted from these (C15) |
| `memory_context` | no | What the agent found in memory about the product — what it is, its domain, who uses it — as short-term copies |
| `model` | no | On a later round of a drive: the product model the drive's other plays wrote (read only) |
| `answers` | no | The person's answers so far (`<working>/answers.yaml`): replies to earlier questions (with the examples offered and whether one was picked), intents they stated, items they named as missing or merged, and any correction |
| `draft_path` | yes | Where to write the draft (`<working>/intent-draft.yaml`) |
| `ontology_path` | yes | The ontology, copied into short-term memory by the agent through the memory tool. Read this copy — never memory itself (ADR 039). |
| `spine_path` | no | The product model's `_spine.yaml`, when one exists — read only, to see which domains the model already has |

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
   a journey are where its ICE come from.

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
   product is, its domain, who uses it) and, on a later round of a drive, what the model holds
   (the domain and capabilities `/vision` and `/understand` wrote) may sharpen `why`, `proof`
   and `asked_by` — provenance `memory` or `model`.
1. **Read the ontology's Business Intent and ICE kinds** — their properties and rules. Then
   read every snapshot file every manifest lists: look at every screenshot (one per page or
   tab) and read its text, the documents, or the statement.
2. **List the parts of what the sources show.** Go page by page and tab by tab. For each part,
   write one plain line: what a person can see, decide or do there. Do not skip a part
   because it looks small. This is the coverage list.
3. **Draft the ICE — one per separate thing.** Group the parts by what the person gets from
   them: the understanding or decision they have that they did not have before. Each group is
   one ICE. Two parts that give the same thing share an ICE; two that give different things
   are two. Write its goals as plain outcomes: what the person can see **and** what they can
   decide or judge from it (not only "see each model's use" but "tell whether moves to newer
   models happen consistently"). Never write screens, fields, tabs, charts, or how the source
   works. Each ICE becomes a proposed capability, so also write its `one_line` (one sentence:
   what this capability is) and its `directional_intent` (a short paragraph a stranger
   understands: what it is about, what it will broadly own, and why it matters — the why
   comes from the business intent it serves). Where the source or the person says what must
   not happen there, or what would count as failing, add it as `limits` or `fails_if` — only
   what is shown or said.
   **Name its domain when something shows it.** If the sources, the person's words, or a
   domain already in the model (`spine_path`) make clear which big area of the product this
   ICE belongs to, set its `domain` and list that domain under `domains` with `shown_by`
   (`source`, `person` or `model`; for a model domain, use its id from the spine). A domain
   not in the model gets a `title`, a `one_line` and a light `intent` paragraph: what the
   area is for and why, in plain words. If nothing shows the domain, leave `domain` out —
   the capability waits for `/vision`. Never guess a domain to avoid that.
4. **Name the business intent each ICE serves.** A business intent is the need, at the level
   of the product, that a main area meets for its user — the ICE are the separate things the
   person sees and does to get it. Ask "why does the person want this?" once: the answer is the
   intent's `why`, not a new, higher intent. ICE that serve the same need share it. Keep an
   intent the person stated even if no part of the source shows it; it starts with no ICE.
   Qualities that every intent must keep — fresh, trusted, private — are `must_not` limits,
   not intents.
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
   This describes the source; the intents and ICE do not.
9. **Apply the answers.** Take each reply as the person's own words (provenance `person`); a
   reply marked as a picked example stays marked. Add intents or ICE they named as missing,
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
ice:                                              # each becomes a proposed capability
  - id: <short-slug>                              # lower-case letters, digits, dashes
    title: <the separate thing, in plain words>   # the capability's name
    one_line: <one sentence: what this capability is>
    directional_intent: <a short paragraph: what it is about, what it broadly owns, why it matters>
    built_from: <the id of the business intent it serves>
    domain: <a domain id from `domains`>         # optional — only when something shows it
    goals:
      - <what the person can see, and what they can decide or judge from it>
    limits: [<what must not happen here>]         # optional — only what is shown or said
    fails_if: [<what would count as failing>]     # optional — only what is shown or said
domains:                                          # optional — the big areas the ICE belong to
  - id: <short-slug, or the model's id>           # never `capabilities` or `intents`
    title: <the area's name>
    one_line: <one sentence: what this area is>
    intent: <a short paragraph: what the area is for and why>   # 12 words or more
    shown_by: source|person|model
sources:
  - snapshot_dir: <the manifest's snapshot_dir, exactly>
    shows: <what this source shows, in plain words>
coverage:
  - part: <one part of what a source shows, in plain words>
    ice: <the id of the ICE it serves>
questions:
  - intent: <an intent id, or "all">
    ask: <a plain question for the person>
    examples: [<up to three example answers>]
    answer: ""                                    # filled from answers on the next pass
```

## Constraints

- **Draft only.** Never write the product model, and never set a stage — only the person confirms or drops.
- **One ICE per separate thing; every ICE under an intent.** Never merge; never leave a part unmapped.
- **Intents above, not beside.** A business intent says what the business wants; it never restates what the source shows.
- **Outcome, not build.** Nothing that describes the source belongs in an intent or an ICE goal.
- **Nothing without a basis.** Title and outcome come from what the source shows or the person said. Why, asked by and proof are drafted, each with its basis — never left open, never asked. A domain is named only when something shows it.
- **The product, not the machinery or the sample.** An intent names what the product's user gets, in the product's words — never the process or tools behind the screens, and never the sample data's specifics.
- **Plain words.** The draft is read by a business person.

## Questions that make sense to the person

A question is for whoever shared the source — for Kickoff, the person who gave the prototype.
Write each one so that person can answer it without knowing Garura's words:

- Ask about something they have seen: name the intent or part in their words, never an id.
- Never ask for why, asked by or proof: draft them (step 5).
- One question, once: when the same question applies to several intents, ask it once with
  `intent: all` — never once per intent.
- Say what it is for in one plain clause ("so the agents know who to build it for").
- Give up to three example answers, drawn from the journeys and memory, not made up.
- Record `intent`, the `property` it fills, `ask`,
  `examples`, and `for_person: false` when a later play or memory may still answer it.
