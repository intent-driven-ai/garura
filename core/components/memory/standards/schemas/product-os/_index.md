# Product-OS Schemas — v1

The persistent data model for the ProductOS Command Model. These schemas define
the three things ProductOS keeps forever — structure, intent, decisions — plus
the two delivery artifacts that ride on top.

| Schema | Keeps | Lifecycle |
|--------|-------|-----------|
| `ontology.md` | the product ontology — the agreed, human-readable map of the kinds of things a product is made of (v4: Business Intent, Source, ICE — the ICE in its named page section, intents linked both ways), how they connect and their rules; built with `author-product-ontology` | permanent |
| `product-os.yaml` | the Domain → Capability → Feature tree, personas, journeys | permanent |
| `ice.yaml` | Intent / Context / Expectations on a node (the build unit at feature level) | permanent |
| `decision.yaml` | decision records (ADRs) at any level — with the core fields of `templates/adr.md` added in #632 (supersedes, amends, affects, ICE impact, business-intent check) and, since #930, `for_the_accepter`: the points for the person who accepts the record, each with its six parts | permanent |
| `lens/` (one file per type) | the 5 realize lenses (ux, architecture, run, quality, agentic) | permanent |
| `slice.yaml` | a vertical product increment — features, taken from any capabilities, bundled into an increment a person can test end to end; written by /shape-slice | permanent |
| `epic.yaml` | a vertical slice of a feature — the delivery/issue grain | permanent (stamped `delivered` on merge, kept) |
| `product-profile.yaml` | the NFR + shape posture of a product; the vocabulary the KB matches conditions against | permanent |

Two "vertical slice" terms, deliberately distinct: a **slice** (`slice.yaml`) is the
product-increment level — whole features bundled into a usable increment, from
/shape-slice. An **epic** (`epic.yaml`) is the engineering grain — one
feature cut end-to-end through its components, from /shape-slice inside a chosen slice.

Storage tiers (see `product-os.yaml` storage layout):
- **Permanent** (product-os): structure, ICE, decisions, the 5 lenses, and epics — epics
  are stamped `delivered` on merge and kept in place as the as-delivered record (ADR 019).
- **STM only**: stories, tests, build detail produced by /build-epic.

Schema evolution is parked for v1: a dedicated schema-evolution play will own it
later, and it implies migrating existing records to the new shape.

Created under issue #434 (Realign Garura to the ProductOS Command Model), Phase B.
