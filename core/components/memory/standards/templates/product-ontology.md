# Product Ontology Format

Canonical format for the **product ontology** — the agreed map of the kinds of things a product is made of, what each holds, how they connect, and what must always be true. It is written for a person to read first: a kind that people read (a Business Intent) must make sense to a business reader with no other document open.

Built and extended by the `build-product-ontology` skill. Checked by its `check_ontology.py`. The ontology defines kinds; the real things (instances) live in each product's model at the path each kind names.

## Format

````markdown
---
ontology: product
version: {integer — bumped when a kind is added, changed or removed}
updated: {YYYY-MM-DD}
---

# Product Ontology

{Two or three plain sentences: what this ontology is for, and that it grows a kind at a
time.}

## Questions it must answer

Every kind and relationship exists to answer at least one of these. A question no kind
answers yet says so.

- **Q1** — {the question, in plain words}
  **Answered by:** {kinds and relationships, e.g. Business Intent; Work serves Business Intent}
  **Status:** {answered | partly | not yet}

## Kinds

### {Kind name}

**What it is:** {one or two plain sentences}
**Who reads it:** {person | agent | both}
**Lives at:** {where its instances are stored, e.g. `product-os/intents/<id>.md`}

**Properties**

| Property | What it holds | Required |
|----------|---------------|----------|
| {name} | {plain description} | {yes / no} |

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| {this → other / other → this} | {kind} | {one / many} | {plain words} |

(Write "None yet." under the heading when it has none.)

**Rules**

- {what must always be true for this kind}

**States** *(optional)*

{state → state, with what moves it}

**Example**

{A real, filled-in instance, written the way the reader will see it.}

## Not yet defined

Kinds that are named — by a relationship or a question — but not built yet. Each gets one
plain line, so nothing points at an unknown word.

- **{Kind}** — {one line}

## Log

- {YYYY-MM-DD} — {what changed in the ontology, and why}
````
