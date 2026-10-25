---
ontology: product
version: 4
updated: 2026-10-18
---

# Product Ontology

The agreed map of what a product is made of in Garura: the kinds of things, what each holds, how they connect, and what must always be true. A person and an agent reading it use the same words for the same things. It grows one kind at a time, through the `build-product-ontology` skill; this first version defines the Business Intent — the person's side — and connects it to ICE, the agent's side.

How it flows: a person gives an intent → it becomes a **Business Intent** here and a "Business Intent" issue in the tracker → plays break it into **Work** agents know (Feature, Story, Chore, Bug, Spike), each carrying the **ICE** its agent works on → as work finishes, the Business Intent is updated with what was done → when it is done, the Business Intent links to the value it got through the tracker's finished issues.

**Who writes, and what the rules mean.** No play owns a kind. Any play may write the intents, ICE or other kinds it finds — from a prototype, while shaping, or in the middle of implementation — and the parts may come in any order. A play still writes only inside its own declared write scope (`standards/rules/direct-model-write.md`); a play's scope is widened on purpose, in that play, never by this sentence. The rules below say what holds once the product is **aligned**; they never stop a write. Drift between them is found and fixed by the Alignment drive. What a rule can stop is work, never a write: an ICE with no confirmed business intent is kept, but nothing is built from it. One thing is never left to alignment: only a person confirms or drops a business intent.
