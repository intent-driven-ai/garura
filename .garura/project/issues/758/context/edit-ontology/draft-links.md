# Draft links — #758 (plan #756), stage links (steps 5, 6)

The sources are the locked model (`locked-model.md`, agreed on 2026-10-22), the two decisions the product owner made at the kinds checkpoint on the same day, and the kinds draft (`draft-kinds.md`). This draft gives the properties, the links and the rules, in the ontology's own table format. It adds nothing, except the items marked **Our proposal**. Each of those is also in the list at the end.

The ontology writes a count as "one" or "many" from the side of "this" kind. The locked model writes N:N, N:1 and 1:1. The rows below use the ontology's words: N:1 seen from the functionality is "one"; seen from the capability it is "many".

## ICE

**What it is:** The agent's intent for one capability or one functionality, in three parts: Intent, Context and Expectation. It has no link to a business intent; it finds its business intents through its part. It answers "can work start here?" with ready, partly ready or not ready.
**Who reads it:** agent

**Lives at — Our proposal**

- **The page.** One page, `ice.md`, in the folder of its part, so the ICE moves with its part:
  - a capability's ICE: `{domain}/{capability}/ice.md`, or `capabilities/{capability}/ice.md` while the capability has no domain;
  - a functionality's ICE: `{domain}/{capability}/{functionality}/ice.md`, or `functionalities/{functionality}/ice.md` while the functionality has no capability.
- **The page shape.** Three sections, in this order: `## Intent` (lines Goal, Limit, Fails if), `## Context` (lines Read, Never read, Persona, Scope), `## Expectation` (lines Scenario, Done means, Quality need). Each line is filled as far as is known.
- **The spine entry.** A new `ices` list in `_spine.yaml`, one entry for each ICE:

```yaml
ices:
  - id: string          # opaque, stable — never changes once assigned
    for: string         # the id of its capability or functionality (exactly one)
    for_kind: string    # capability | functionality
    doc: string         # pointer to its ice.md, relative to the product-os root
    metadata:
      created_by: string
      updated_by: string
      version: integer
```

  The entry holds no business intent ids and no ready answer. The business intents come from its part. The ready answer is worked out by the ready check each time it runs (today `check_ice_workable.py`), and it is never written by hand.

**Properties**

| Property | What it holds | Required |
|----------|---------------|----------|
| Part of the product | The one capability or functionality it is for | yes |
| Intent | The goals (what must be true), the limits, and what counts as failing (fails if) | yes, to be ready |
| Context | The rules for the sub-agent that gathers context: what to read, what never to read, the persona it works for, and the scope (what is in and what is out) | yes, to be ready; empty or thin makes it partly ready |
| Expectation | The scenarios it must pass, what "done" means, and the quality needs (for example speed, security, regimes such as PCI) | yes, to be ready |
| Ready answer | Ready, partly ready or not ready, with the gaps listed — worked out by the ready check, never stored (**Our proposal**: never stored) | no — it is computed |

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| this → other | Capability | one | It is the ICE of one capability … |
| this → other | Functionality | one | … or of one functionality |
| other → this | Work | many | A piece of work carries it — the intent its agent works on |

**Rules**

- Each capability and each functionality has exactly one ICE, and each ICE is for exactly one capability or functionality. Two ICE for one part are drift; the Alignment loop merges them.
- It has no link to a business intent. A capability's ICE finds its business intents through its capability. A functionality's ICE finds them through its parent capability.
- When a second business intent changes a capability, its one ICE is updated to cover both. A second ICE is never made.
- The ready check gives one of three answers. For a functionality's ICE, "its capability" is the parent capability.
  - **Ready:** its capability serves a confirmed business intent, every capability it needs is done, and the ICE has all three parts. Work starts.
  - **Partly ready:** as ready, but with gaps that do not stop work — no domain, no "identified by", a thin part such as an empty Context. Work starts, and the gaps are listed.
  - **Not ready:** no confirmed business intent, or a capability it needs is not done. Work stops, and the page is kept.
- **Our proposal:** a part that is missing from the page counts as an empty part. It is a gap (partly ready), not a stop.
- Writing it is never blocked. Any play may write it or add to it, inside that play's declared write scope, and keeps what is there.

**States**

not ready → partly ready → ready, as the ready check finds them. The answer can go back (for example, a needed capability is reopened).

**Example**

> **Shop — ICE of "Guest checkout"** (a functionality in Checkout). Checkout serves "Shoppers can check out without an account" (confirmed). Checkout needs Cart, which is done.
> **Intent:** Goal — a shopper with no account pays from start to finish. Limit — returns do not change. Fails if — a guest is asked to sign up before paying.
> **Context:** Read — the payment rules. Never read — saved card data. Persona — the guest shopper on mobile. Scope — card and wallet in; saved addresses out.
> **Expectation:** Scenario — a guest pays by card in under two minutes. Done means — that scenario and a wallet scenario pass. Quality need — the page loads in under one second.
> **Ready answer:** ready.
>
> **Clinic — ICE of "Booking"** (a capability, no domain yet). Booking serves "Patients book their own appointments online" (confirmed). It needs nothing.
> **Intent:** Goal — a patient books, moves and cancels an appointment without a call.
> **Context:** (empty)
> **Expectation:** Scenario — a patient moves an appointment in three steps.
> **Ready answer:** partly ready — gaps: no domain, Context is empty.
>
> **Bank — ICE of "Credit decision"**. Credit decision serves "Small businesses get a loan decision in one day" (confirmed), and needs "Loan application", which is not done.
> **Ready answer:** not ready — Loan application is not done. The page is kept.

## Business Intent

**Property changes**

- **Our proposal:** add **Rules** — the business rules the person says the outcome must keep — not required. The locked model's "hypothesis" is the Outcome, the Why and the Proof it is met, and its "boundaries" is Must not. No property is renamed.
- **Touches** names domains and capabilities, each marked adds, changes or removes. It no longer names functionalities.

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| other → this | Source | many | A source shows what is wanted |
| other → this | Capability | many | A capability serves it |
| this → other | Capability | many | It has a capability — marked change, add or remove on its Touches list; the capability's spine `intents` holds the other side |
| this → other | Business Intent | many | It was **identified by** another business intent — building one led us to find this one. A connection, never a dependency: neither waits on the other |
| this → other | Domain | many | It touches a domain — a loose link, for search only; never in a plan, never a stop (the domain's spine `intents` holds the other side) |
| this → other | Tracker Issue | one | It is tracked as one "Business Intent" issue in the team's tracker |
| other → this | Plan | one | Its plan holds the work that meets it; the plan's ID is this intent's issue number |

Rows removed from version 5: "an ICE is built from it", "a piece of work serves it", and "it touches a functionality". The row "it was identified by another business intent" stays (the product owner's decision).

**Rules**

- It is a destination: sources and capabilities point at it. It points only at its tracker issue, its capabilities, the business intents it was identified by and, loosely, its domains.
- It holds no ICE, and Garura never works on it directly. Agents work on the ICE of its capabilities and of their functionalities.
- Each capability it has is linked both ways: the capability's spine entry names it in `intents`, and its Touches list names the capability with the mark. A play that makes one side writes the other.
- It is met by its proof, never because its work is finished.
- Work starts only from an ICE that is ready or partly ready. An ICE whose capability serves no confirmed business intent is kept, not worked on, and is drift for alignment, never a blocked write.
- A source is never copied into it; the source shows the intent, it is not the intent.
- It is written for a business reader, in plain words.
- Only a person confirms or drops it; an agent never does.
- Two intents that touch the same capability in opposite ways are a clash, shown to a person before work starts.
- Business intents never need one another. They may be identified by one another — a connection, never a dependency; neither waits on the other. Plan files use it: for example, #722 is identified by #717.

## Capability

**Property changes**

- **ICE** replaces "Agent intent (ICE)": its one ICE, on the ICE's own page — required to be ready.
- **Serves** stays: the business intents it serves (spine `intents`) — at least one, confirmed, for its ICE to be ready.
- **Needs** names other capabilities only (spine `depends_on`, to be renamed `needs` under #725).
- **Identified by** names other capabilities only, and may name more than one.
- **Domain** is the one domain it sits in (spine `domain`, kept as a single field) — at most one, and may be missing. The page lives under that domain's folder, or in the holding folder `capabilities/` while it has none.

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| this → other | Business Intent | many | It serves a business intent |
| other → this | Functionality | many | A functionality has it as its one parent |
| other → this | ICE | one | Its one ICE — the agent's intent for it |
| this → other | Capability | many | It **needs** another capability: the other must be done first |
| this → other | Capability | many | It was **identified by** another capability: the other led us to find it |
| this → other | Domain | one | It sits in at most one domain; a domain has one or more capabilities. May be missing — a gap, never a stop |

Rows removed from version 5: "it needs a functionality", "it was identified by a functionality", and "it is tracked as one Feature" (work now reaches it through its ICE; see Work).

**Rules**

- It has exactly one ICE. The ICE is on its own page, never a section of the capability page.
- It serves one or more business intents. When it serves more than one, its one ICE covers all of them, and it shows in each of their plans.
- A capability's "needs" and "identified by" name other capabilities only — never a functionality, a business intent or work.
- While a capability it needs is not done, its ICE and the ICE of each of its functionalities are not ready.
- It sits in at most one domain. A domain has one or more capabilities.
- A missing domain or a missing "identified by" never stops work; it is a gap, and its ICE is partly ready. A capability with no domain waits in the holding folder until it names one.

## Functionality

**Property changes**

- **ICE** replaces "Agent intent (ICE)": its one ICE, on the ICE's own page — required to be ready.
- **Capability** is its one parent capability.
- **Serves**, **Needs** and **Identified by** are removed. Its business intents and its order of work come from its parent capability.

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| this → other | Capability | one | It has exactly one parent capability |
| other → this | ICE | one | Its one ICE — the agent's intent for it |

Rows removed from version 5: "it serves a business intent", "it needs a capability", "it needs another functionality", "it was identified by a capability or a functionality", and "it is tracked as one Story" (work now reaches it through its ICE; see Work).

**Rules**

- It has exactly one parent capability. Until it names one it waits in the holding folder, and its ICE is not ready, because no confirmed business intent reaches it.
- It has exactly one ICE, on its own page, never a section of the functionality page.
- It never needs anything and is never identified by anything. Its order of work comes from its parent capability.
- Its business intents are the ones its parent capability serves.
- Garura's own model: fn-727 → fn-724 is not allowed; it becomes cap-718 → cap-723 (the move is #765).

## Work

**Property changes**

- **ICE** replaces "Node": the one ICE it carries, and through it the capability or functionality it is for — required.
- **ICE copy** stays: a copy of that ICE on the issue, for the agent doing the work — Feature and Story.

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| this → other | ICE | one | It carries one ICE; an ICE can have many pieces of work |
| this → other | Tracker Issue | one | It is one issue in the tracker |

Rows removed from version 5: "a Feature tracks a capability", "a Story tracks a functionality; a Spike, Chore or Bug sits under one", and "it serves a business intent, through its node". Each is now found through its ICE.

**Rules**

- Work never needs anything and is never identified by anything.
- It reaches its part and its business intents through its ICE.
- A Story builds one functionality and carries that functionality's ICE. One functionality has exactly one Story.
- Spikes, Bugs and Chores sit under a functionality and carry its ICE. A Bug always sits under a functionality.
- **Our proposal:** a Feature carries its capability's ICE. One capability has one Feature.
- In the tracker, work follows the plan's parent order: Business Intent → Feature → Story → Spike, Chore or Bug.

## Not yet defined — the change to one line

- **Domain** — a big area of the product. Its page is light (directional) or full (detailed); it holds no ICE. It has one or more capabilities, and each capability sits in at most one domain. It links loosely to business intents, many to many, for search only. It is never in a plan, never a tracker issue, and never stops work.

## What this means outside the ontology (for later changes, not this one)

- `spine.yaml`: a new `ices` list (**Our proposal**, above). On functionalities, `intents`, `depends_on` and `identified_by` lose their meaning. On capabilities, `depends_on` and `identified_by` name capabilities only, and `identified_by` becomes a list. The capability's single `domain` field and the folder layout stay as they are.
- The page templates `grounding/capability.md` and `grounding/functionality.md` lose the `## Agent intent (ICE)` section. A new template is needed for `ice.md`.
- The ready check (`check_ice_workable.py`) gives three answers and lists the gaps.
- The glossary entry "ICE (ProductOS)" changes: one for each part, its own page, no business intent link, three ready answers.

## Question for the product owner

Do these links and rules say the right thing — and do you agree with where the ICE page lives and what its spine entry holds?

## Differences from the locked model

1. **Our proposal** — where the ICE lives: `ice.md` in the folder of its part (holding folders included), with three sections `## Intent`, `## Context`, `## Expectation` and named lines in each.
2. **Our proposal** — the ICE spine entry: a new `ices` list with `id`, `for`, `for_kind`, `doc` and `metadata`; no business intent ids and no ready answer in it.
3. **Our proposal** — the ready answer is computed by the ready check each time, never stored.
4. **Our proposal** — a part that is missing from the ICE page counts as an empty part: a gap (partly ready), not a stop.
5. **Our proposal** — Business Intent gains an optional Rules property; "hypothesis" and "boundaries" map onto the properties that exist; nothing is renamed.
6. **Our proposal** — the Feature stays and carries its capability's ICE; one capability has one Feature.

**The product owner's decisions (kinds checkpoint, 2026-10-22):**

- A capability has at most one domain, and a domain has one or more capabilities. The product owner's words: "capability cant be many to many with domain. domain can have 1 more or more capability. and capability can have only 1 domain." This replaces the N:N row for Domain and Capability in the locked table. A capability with no domain yet is a gap, never a stop. The spine's single `domain` field and the folder layout stay as they are. The link between a domain and a business intent stays loose and N:N, for search only.
- Business intents are still identified by one another — a connection, never a dependency (agreed 2026-10-21; plan files use it, for example #722 is identified by #717). Between the parts of the product, only a capability needs or is identified by another capability; a functionality has neither.

**Reading we made (not an addition; please check it):**

- A functionality has no direct link to a business intent, so the Touches list names domains and capabilities only.
