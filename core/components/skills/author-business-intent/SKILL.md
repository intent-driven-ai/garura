---
name: author-business-intent
description: Draft two levels of intent from what a person shared — a prototype (its saved snapshot), a document, or a plain statement — plus their own answers. The lower level is ICE — one per separate thing the source lets the person see, decide or do, as plain goals, never merged, with every part of the source mapped to one. The upper level is the person's Business Intents — what they want for the business — found by asking "why?" above the ICE until the answer no longer names the product; each ICE is built from one of them. Each business intent holds title, outcome, why, asked by, proof it is met, must not, and the provenance of every property (source or person). Also writes what each source shows and the questions the sources cannot answer, each with example answers. Written for a business reader, never a description of the source. Generative artifact production for the /intent play; writes the draft only, never the product model. Use when /intent needs the intents drafted, or re-drafted after the person answers.
user-invocable: false
model: opus
allowed-tools: Read, Write, Glob
---

# author-business-intent

Turns what a person shared into a **draft** of two levels of intent, both kinds of the product
ontology (`standards/schemas/product-os/ontology.md`):

- **ICE** — the agents' level: the separate things the person must be able to see, decide or
  do. A source shows this level best.
- **Business Intents** — the person's level: what they want for the business, with why it
  matters and how we will know it is met. A source rarely shows these; they sit one "why?"
  above the ICE, and the person often supplies them.

The person confirms or drops each business intent later; you only draft.

The source shows *one way* the intents could be built. You pull out what the person needs and
wants, and leave how the source does it behind (IDD Principle 1).

## Input

| Field | Required | Meaning |
|-------|----------|---------|
| `source_manifests` | yes | One or more Source manifests — each with its kind, `snapshot_dir` and snapshot files (screenshots with their text, page HTML, the copied file, or the statement text). A project folder gives two: its written docs and the running app. All are read together |
| `journeys` | for a prototype | The prototype's journeys (`journeys.yaml`, from `walk-prototype`): who it serves, what each sets out to do, the steps walked and what they showed, what they end with. A prototype's intents are drafted from these (C15) |
| `answers` | no | The person's answers so far (`<working>/answers.yaml`): replies to earlier questions (with the examples offered and whether one was picked), intents they stated, items they named as missing or merged, and any correction |
| `draft_path` | yes | Where to write the draft (`<working>/intent-draft.yaml`) |
| `ontology_path` | yes | The ontology, copied into short-term memory by the agent through the memory tool. Read this copy — never memory itself (ADR 039). |
| `spine_path` | no | The product model's `_spine.yaml`, when one exists — read only, to see which domains the model already has |

## Process

0. **For a prototype, start from its journeys.** Each journey's person and what they set out
   to do is where a business intent comes from: ask "why does this person want that?" until
   the answer is what the person or the business gets — then that is the business intent, and
   it names the journey (`from_journey`). A business intent is never a rule the system enforces
   ("agents work only from approved knowledge" is a rule; "a product owner signs off
   everything a drive made in one sitting" is what a person gets). The steps of a journey are
   where its ICE come from. Sample data inside a prototype is sample data, not the product.
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
4. **Find the business intents above them.** For each ICE ask "why does the person want
   this?", one level at a time, and stop when the answer no longer names the product — that
   answer is a business intent. ICE that reach the same answer share it. Keep an intent the
   person stated even if no part of the source shows it; it starts with no ICE. Qualities that
   every intent must keep — fresh, trusted, private — are `must_not` limits, not intents.
5. **Fill only what you can back.** For each business intent property, write it only if a
   source shows it or the person said it, and record which (`source` or `person`). Sources
   rarely say why it matters or how we will know it is met: leave those empty and add a
   question, tagged with its intent. Never fill a gap yourself.
6. **Give every question example answers.** Up to three short, different examples, drawn from
   the sources and the person's words so far, so the person can pick one, change one, or write
   their own.
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
    title: <the intent in one line, in the person's words>
    outcome: <what should be true for the business when it is met>
    why: <why it matters to the business>          # often from the person
    asked_by: <the person who wants it>            # often from the person
    proof: <how we will know it is met>            # often from the person
    must_not: <limits the person stated, and qualities every intent keeps>   # optional
    provenance: { title: source|person, outcome: …, why: …, asked_by: …, proof: …, must_not: … }
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
- **Nothing invented.** A property with no source and no answer stays empty, with a question and examples. A domain is named only when something shows it.
- **Plain words.** The draft is read by a business person.
