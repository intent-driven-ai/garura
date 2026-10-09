# Ontology run — Business Intent (#612)

Working notes for `/build-product-ontology`. Agreed items move into the ontology at the end.

## Step 1 — questions (agreed one at a time with Kapil)

- **Q1 (agreed 2026-10-08)** — Given a business intent and the product as it is today, which types of work does it need — Feature, Story, Bug, Chore, Spike — what value does each bring to the intent, and when would a type of work be wrong for it? (Cost is a right ask but not needed now; value is. "Wrong for it" makes it usable as an eval.)
- **Q2 (agreed 2026-10-08)** — Given a new business intent, which parts of the product does it touch — and for each, does it change something that already exists, add something new, or remove something — at the level of a domain (a big area), a capability (something the product can do), or a function (one specific action)? ("Where it enters the shape" was unclear; this says it plainly.)
- **Q3 (agreed 2026-10-08)** — When two intents touch the same part of the product and want opposite things, is that shown to a person before any work starts? (Reworded to match the plain example.)
- **Q4 (agreed 2026-10-08)** — For this intent, which work did agents finish on their own, and where did a person have to step in?
- **Q5 (dropped 2026-10-08)** — "What stages can a business intent be in?" is not a question a person asks of their intents; it is a design choice about the kind. The skill derives the Business Intent's states itself at step 6 (from the sources: met by outcome, never closed by its children; #542's stages), and shows them to Kapil to confirm there. A specific intent's current stage is read from the model, not asked.
- **Q6 (dropped 2026-10-08)** — "Can a business reader read it?" is a quality bar, not a question a person asks of the ontology. Its content becomes the Business Intent's properties at step 5 (what was asked, who asked, why); its bar becomes a rule at step 6 (written for a business reader, in plain words).
- **Q7 (agreed 2026-10-08)** — What evidence was this intent drawn from, and what did that evidence show at the time? (Widened from "which prototype": today the evidence is a prototype; later it may be a conversation or a document.)
- **Q8 (agreed 2026-10-08)** — Is this intent met yet, and how would we know? (Met by its outcome, with a proof stated when the intent is written — never just because its work is done.)

**Step 1 result — six questions, renumbered:**
1. Work needed — types, value, and when a type is wrong (was Q1)
2. What it touches — change, add or remove, at domain / capability / function level (was Q2)
3. Clashes — two intents wanting opposite things in the same part, shown before work starts (was Q3)
4. Who did the work — agents alone, or where a person stepped in (was Q4)
5. Evidence — what the intent was drawn from, and what it showed then (was Q7)
6. Met — is it met, and what proves it (was Q8)

Lesson for the skill: a step-1 question is something a person wants to *find out*; a quality bar becomes a rule (step 6); a design choice about the kind (like its stages) is derived by the skill, not asked.

## Steps 2–3 — reuse and terms

Reuse: Domain, Capability, Functionality (the product tree, `product-os.yaml`); Persona; Decision; the GitHub issue type "Business Intent" (#539, #606) is the same concept as this kind. Clash avoided: ICE (`ice.yaml`) also says "intent". Terms from the questions: business intent, outcome, who asked, why, proof it is met, evidence, snapshot, work type (Feature, Story, Bug, Chore, Spike), value, part of the product, change / add / remove, clash, person stepped in, stage.

## Step 4 — kinds (agreed one at a time)

- **Business Intent** (id `business-intent`) — agreed 2026-10-08. What a person or the organisation wants: an outcome in their words, with why it matters and how we will know it is met. Read by a person first. The same thing as the GitHub "Business Intent" issue type. Kapil: "intent is business intent"; **ICE is the agentic intent, and ICE is built from the Business Intent** — a strong relationship, not a clash.
- Open for step 6: are work items (Feature, Story, Bug…) and ICE the same thing, or does a piece of work carry an ICE?
- **Evidence** — agreed 2026-10-08. What a business intent was drawn from: today a prototype (a file or a deployed site), later a conversation or a document; kept as it was when read, with a snapshot. Read by both. Not the intent — one way to build it, never copied into it (IDD Principle 1). Its own kind because one intent can have several pieces of evidence, and one piece can show more than one intent.

## Step 5 — properties

- **Business Intent** — agreed 2026-10-08: Title, Outcome, Why, Asked by, Proof it is met, Must not (optional), Stage, Confirmed by and when. Evidence, work, and the product parts it touches are separate kinds connected to it, not stored in it; no agent working fields (those live in the ICE built from it).
- Kapil asked (2026-10-08): how does the Business Intent connect to ICE, and can ICE — already well defined in `ice.yaml` — be built into this ontology now, connected to it. → ICE added as a third kind in this run.
- **ICE (the agentic intent)** — agreed 2026-10-08 as the third kind of this run, reusing `ice.yaml` as is: part of the product (capability or function), goals / limits / failures, context (personas, systems, scope), outcomes, quality and compliance needs — plus one new property, **Built from**: the business intent(s) it serves. The link is a relationship recorded on the ICE side (ICE → Business Intent, many to many); the Business Intent never points down. Written when the ICE is built (`/vision` seeds, `/understand` fills, `/shape` writes function-level).
- **Source** (renamed from "Evidence", 2026-10-08) — Garura already uses "Evidence" for a play's run record (glossary), so the kind is named **Source**: what a business intent was drawn from. Properties agreed: Kind; Read on; Snapshot (screenshots/images for a deployed site, a copy of the file for a file — kept even if the link or file goes away; saved through Garura's existing evidence method, at the play's close, under `{product_base}_evidence/intent/<timestamp>/`); What it shows; Given by (the git user who ran it, e.g. `Kapil Viren Ahuja <kapil@howtoarchitect.io>`). "Where" dropped — the snapshot is what is kept.
- Q5 reworded to match: "What was this intent drawn from (its source), and what did it show at the time?"

## Step 6 — relationships, rules, states

- **Relationships agreed 2026-10-08:** Source —shows→ Business Intent (many↔many, on the Source); ICE —built from→ Business Intent (many↔many, on the ICE); Business Intent —touches→ Domain / Capability / Function, each marked change / add / remove (on the Business Intent — the one downward link: a fact about what the intent needs, not work done for it); Work —serves→ Business Intent (many↔many, on the Work; type Feature / Story / Bug / Chore / Spike); Business Intent —clashes with→ Business Intent (worked out from "touches", not stored). Work, Domain, Capability, Function listed as not yet defined.
- **Business Intent stages agreed 2026-10-08:** proposed → (the person who asked confirms) → confirmed → (its proof holds) → met; proposed or confirmed → dropped (a person drops it, with a reason).
- **Business Intent rules agreed 2026-10-08:** (1) a destination — work, ICE and sources point at it; it points only at the product parts it touches; (2) met by its proof, never by its work finishing; (3) no ICE built and no work started from a proposed intent — only from a confirmed one; (4) a source is never copied into it; (5) written for a business reader, in plain words; (6) only a person confirms or drops it.
- **The flow (Kapil, 2026-10-08):** a person gives an intent → it becomes a Business Intent in the ontology and a "Business Intent" issue in the tracker → plays break it into work agents know (Feature, Story, Chore, Bug, Spike), each carrying the ICE its agent works on (the agent's intent) → agents finish work, the ontology updates, and the Business Intent is updated with what was done → finished, the Business Intent links to the value it got through the tracker's finished issues.
- **Added, agreed:** Business Intent —tracked as→ Tracker Issue (one to one); Work —carries→ ICE; Business Intent property "What was done" (what was delivered and its value, with links to the finished issues), updated as work finishes. Work and ICE are separate and linked: work is the trackable piece; its ICE is what the agent works on.
