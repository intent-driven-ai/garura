# Draft kinds — #758 (plan #756), stage kinds (steps 2, 3, 4)

The source of truth is the locked model (`locked-model.md`, checkpoint 1, agreed on 2026-10-22), with the two decisions the product owner made at the kinds checkpoint on the same day (listed at the end). This draft does what they say. It adds nothing, except the items marked **Our proposal**. Each of those is also in the list at the end.

The change in one paragraph: today the agent intent (ICE) is the last section of a capability page or a functionality page. After this change, the ICE is its own kind of node, with its own page and its own spine entry. Each capability and each functionality has exactly one ICE. The ICE has no link to a business intent. Its business intents are found through its part. A business intent holds no ICE, and Garura never works on a business intent directly. Among the parts of the product, "needs" and "identified by" join capabilities only; a functionality has neither. Business intents are still identified by one another. A capability sits in at most one domain, and a domain has one or more capabilities. The ready rule moves to the ICE, and it has three answers: ready, partly ready, not ready.

The new version is 6.

## Step 2 — Reuse what exists

We read the ontology (version 5), the spine schema (`spine.yaml`, version 2), the glossary entry "ICE (ProductOS)", the page templates and `ice.yaml`.

**What we reuse, as it is**

- **Business Intent** — the kind, its page, its stages, its Touches list and its "identified by" link to other business intents. Only its other links and two rules change.
- **Capability** — the kind, its page and its spine entry. The ICE section leaves its page.
- **Functionality** — the kind, its page and its spine entry. The ICE section, its "needs" and its "identified by" leave it.
- **Work** — the five types (Feature, Story, Spike, Chore, Bug) and the ICE copy on the issue. Work now points at one ICE.
- **The three parts of the ICE** — the glossary and `ice.yaml` already name Intent, Context and Expectation. We keep these three names.
- **The ICE labels of version 4** — Goal, Limit, Fails if, Context, Checked by, Quality need. They become the lines inside the three parts.
- **"Writing is never blocked"** (version 3) — kept. A rule can stop work, never a write.
- **The spine field `depends_on`** — kept as the field for "needs" on capabilities. Its rename to `needs` stays with #725.
- **The spine field `domain`** — kept as it is: one domain for each capability. The folder layout (a capability's page under its one domain's folder, or the holding folder `capabilities/` while it has none) stays as it is.

**Where the change clashes with what exists**

1. **The ICE section on a page.** Version 4 says the ICE is the section `## Agent intent (ICE)`, the last section of a capability or functionality page. Version 6 says the ICE has its own page. The old section must go. Pages that have it today are drift for the Alignment loop. They are not an error.
2. **Functionality spine fields.** The functionality spine entry has `intents`, `depends_on` and `identified_by`. In version 6 a functionality never needs anything, is never identified by anything, and finds its business intents through its parent capability. These three fields no longer have a meaning on a functionality.
3. **"Workable" and "ready".** Version 5 puts the ready rule on the node (the capability or functionality). Version 6 puts it on the ICE, with three answers. The glossary word "workable" means the old two-answer rule. The glossary needs a new line (a later change, not this ontology).
4. **"Open" and "done".** Version 5 says "nothing it needs is still open". The locked model says "every capability it needs is done". We use "done".
5. **The word "Context".** In Garura, "context" also names the run folder of a play (`context/`). In this ontology, Context is one part of an ICE only: the rules for the sub-agent that gathers context.
6. **The word "rules".** The locked model says a business intent holds "rules". Each kind in the ontology also has a "Rules" section. These are not the same thing. A business intent's rules are what the person says the outcome must keep. A kind's Rules section is what must always be true for the kind.
7. **Garura's own model.** The link fn-727 → fn-724 ("needs" between two functionalities) is not allowed in version 6. It becomes cap-718 → cap-723. The move is #765, not this change.
8. **The rejected design.** The need (`need.md`) says one ICE for each pair of business intent and part (option 1.B). The locked model replaces this with one ICE for each part (option 1). This draft follows the locked model.
9. **Domain and capability in the locked table.** The locked links table says Domain to Capability is N:N. The product owner changed this at the kinds checkpoint: a capability has at most one domain, and a domain has one or more capabilities. This matches the spine and the folders as they are today, so nothing outside the ontology changes for it.
10. **"Identified by" in the locked model.** The locked model says "needs" and "identified by" join capabilities only. The product owner said this is about the parts of the product: business intents are still identified by one another (agreed 2026-10-21), and plan files use it — for example, #722 is identified by #717.

## Step 3 — List the terms

**Nouns (candidate kinds and properties)**

business intent, hypothesis, boundaries, rules, capability, functionality, ICE, agent intent, Intent, goals, limits, fails if, Context, what to read, what never to read, persona, scope, Expectation, scenarios, done means, quality needs, work, Story, Spike, Bug, Chore, Feature, domain, spine entry, page, ready, partly ready, not ready, gap, confirmed.

**Verbs (candidate relationships)**

serves (capability → business intent), has (business intent → capability; capability → ICE; functionality → ICE; domain → capability), has a parent (functionality → capability), sits in (capability → its one domain), needs (capability → capability), identified by (capability → capability; business intent → business intent), builds (Story → functionality), sits under (Spike, Bug, Chore → functionality), carries (work → ICE), links loosely (domain → business intent), is updated to cover (one ICE → a second business intent).

## Step 4 — Decide the kinds

Five kinds change. No kind is added; the ICE was already a kind. No kind is removed.

### ICE — changed

**What it is after the change.** The ICE is the agent's intent for one capability or one functionality. It has its own page and its own spine entry, and it holds three parts: Intent (goals, limits, fails if), Context (the rules for the sub-agent: what to read, what never to read, the persona, the scope) and Expectation (scenarios, done means, quality needs). It has no link to a business intent; it finds its business intents through its part, and it is the node that answers "can work start here?" with ready, partly ready or not ready.

**Who reads it:** agent.

**It is not** the business intent (the person's intent). It is not the capability or the functionality page (that page says what the part is; the ICE says what an agent must make true there).

**What changes**

- It leaves the capability page and the functionality page. It gets its own page and its own spine entry.
- It holds three named parts. Version 5 held six loose labels.
- Its link to a business intent ("built from") goes. A capability's ICE finds its business intents through the capability. A functionality's ICE finds them through its parent capability.
- Each capability and each functionality has exactly one ICE (1:1). When a second business intent changes a capability, the one ICE is updated to cover both.
- The ready rule moves here, with three answers.

**Log line:** ICE becomes its own node with its own page and spine entry, one for each capability and each functionality, in three parts (Intent, Context, Expectation); it has no link to a business intent, and the ready rule moves to it with three answers (ready, partly ready, not ready).

**Examples**

- Shop: the ICE for the functionality "Guest checkout". Intent: a shopper with no account pays from start to finish. Context: read the payment rules; never read saved card data; work for the guest shopper on mobile; card and wallet are in scope. Expectation: a guest pays by card in under two minutes.
- Clinic: the ICE for the capability "Booking". Intent: a patient books, moves and cancels an appointment without a call. Context: read the clinic's opening hours; never read medical notes; work for the patient. Expectation: a patient moves an appointment in three steps.

### Business Intent — changed

**What it is after the change.** A business intent is what a person or the organisation wants, in their words: the outcome as a hypothesis, the boundaries it must stay inside, the rules it must keep, and the capabilities that serve it. It is the person's interface to the product and it is for tracking; it holds no ICE, and Garura never works on a business intent directly. Agents work on the ICE of its capabilities and of their functionalities.

**Who reads it:** person.

**What changes**

- It holds no ICE, and no ICE points at it. Version 5 had "an ICE is built from it".
- It has one or more capabilities (N:N with Capability). It no longer has a direct link to a functionality. A functionality reaches it through its parent capability.
- It keeps its link "identified by another business intent": a connection, never a dependency, and neither waits on the other. Plan files use it — for example, #722 is identified by #717.
- **Our proposal:** the locked model's words "hypothesis · boundaries · rules" map onto the properties that exist. "Hypothesis" is the Outcome, the Why and the Proof it is met. "Boundaries" is Must not. "Rules" is a new property that is not required: the business rules the person says the outcome must keep. No property is renamed.

**Log line:** Business Intent holds no ICE and is never worked on directly; it has one or more capabilities (N:N), reaches functionalities only through them, gains an optional Rules property, and keeps its "identified by" link to other business intents (a connection, never a dependency).

**Examples**

- Bank: "Small businesses get a loan decision in one day". Boundary: no change to how the bank checks identity. Rule: every declined loan shows its reason. It has the capabilities "Loan application" and "Credit decision".
- Clinic: "Patients book their own appointments online". Boundary: no change to how the clinic bills. It has the capability "Booking". It was identified by "Patients get a reminder before each visit".

### Capability — changed

**What it is after the change.** A capability is something the product can do, in the product's own words, and it serves one or more business intents. It sits in at most one domain, and it has exactly one ICE, on its own page; the capability page no longer holds the ICE section. Among the parts of the product it is the only kind that "needs" another (the other must be done first) or is "identified by" another (the other led us to find it), and it links to those other capabilities only.

**Who reads it:** both.

**What changes**

- The ICE leaves its page. The capability has one ICE (1:1), on the ICE's own page.
- It serves one or more business intents (N:N). This is the only link from the product's parts to a business intent.
- "Needs" and "identified by" join it to other capabilities only (N:N). It no longer needs a functionality or is identified by a functionality. "Identified by" can now name more than one capability.
- It sits in at most one domain (N:1); a domain has one or more capabilities. A capability with no domain yet waits in the holding folder; the missing domain is a gap, never a stop. The spine's single `domain` field and the folder layout stay as they are.
- The ready rule moves to its ICE.
- Garura's own model: fn-727 → fn-724 becomes cap-718 → cap-723 (the move is #765).

**Log line:** Capability has exactly one ICE on its own page (no ICE section on the capability page), serves one or more business intents, sits in at most one domain (a missing domain is a gap, never a stop), and is the only part that needs or is identified by another — always another capability; its ready rule moves to its ICE.

**Examples**

- Shop: "Cart" serves "Shoppers can check out without an account". It sits in the domain Commerce. It is identified by "Checkout". Its ICE is on its own page.
- Bank: "Credit decision" sits in the domain Lending and needs "Loan application", because an applicant must apply before the bank decides.

### Functionality — changed

**What it is after the change.** A functionality is one specific thing a person can do inside a capability, and it has exactly one parent capability. It has exactly one ICE, on its own page. It never needs anything and is never identified by anything; its order of work and its business intents come from its parent capability.

**Who reads it:** both.

**What changes**

- The ICE leaves its page. The functionality has one ICE (1:1), on the ICE's own page.
- It has exactly one parent capability (N:1).
- It loses "needs", "identified by" and its direct link to a business intent ("serves").
- The ready rule moves to its ICE. Its ICE is ready when its parent capability's conditions hold.

**Log line:** Functionality has exactly one parent capability and exactly one ICE on its own page; it never needs anything, is never identified by anything, and takes its order of work and its business intents from its parent capability.

**Examples**

- Clinic: "Send a reminder" in "Booking". It needs nothing. Its work waits until "Booking" can start.
- Bank: "Upload documents" in "Loan application". Its business intent is the one "Loan application" serves.

### Work — changed

**What it is after the change.** Work is a tracked piece of work in the team's tracker: a Feature, a Story, a Spike, a Chore or a Bug. Each piece of work carries one ICE, and an ICE can have many pieces of work. Under a functionality, the Story builds it, and Spikes, Bugs and Chores sit under it.

**Who reads it:** both.

**What changes**

- It points at one ICE (N:1). Version 5 pointed at a capability or a functionality directly.
- It reaches its part and its business intents through its ICE. It no longer has a direct "serves" link to a business intent.
- **Our proposal:** the Feature type stays. The locked model shows work under a functionality only, but it does not remove the Feature. A Feature carries the ICE of its capability.

**Log line:** Work carries one ICE (an ICE can have many pieces of work) and reaches its part and its business intents through it; a Story builds a functionality, and Spikes, Bugs and Chores sit under it.

**Examples**

- Shop: Story #122 carries the ICE of "Guest checkout". Bug #130 "Card fails on mobile" carries the same ICE.
- Clinic: Spike #344 "Which SMS provider?" carries the ICE of "Send a reminder".

### Kinds not changed

Source and Plan do not change. Plan still holds its business intent's capabilities. Domain stays under "Not yet defined"; only its one line changes, to say it has one or more capabilities (each capability sits in at most one domain), and its link to business intents is loose and N:N, for search only.

### Proposed log line for version 6

2026-10-22 — v6 (#758, plan #756, with the product owner): the ICE becomes its own node, with its own page and spine entry, one for each capability and each functionality, in three parts (Intent, Context, Expectation); it has no link to a business intent, and finds them through its part. A business intent holds no ICE and is never worked on directly; business intents are still identified by one another, a connection and never a dependency. Among the parts of the product, "needs" and "identified by" join capabilities only; a functionality has neither. A capability sits in at most one domain and a domain has one or more capabilities; a missing domain is a gap, never a stop; the spine's single `domain` field and the folders stay as they are. The ready rule moves to the ICE, with three answers: ready, partly ready, not ready. Garura's own fn-727 → fn-724 becomes cap-718 → cap-723 (#765). Option 1 (one ICE for each part) replaces option 1.B (one ICE for each pair of business intent and part).

## Question for the product owner

Do these five kinds say the right thing after the change — the ICE, the business intent, the capability, the functionality and the work?

## Differences from the locked model

1. **Our proposal** — Business Intent: "hypothesis" maps to Outcome, Why and Proof it is met; "boundaries" maps to Must not; "rules" is a new property that is not required. No property is renamed.
2. **Our proposal** — Work: the Feature type stays, and it carries its capability's ICE. The locked model does not remove it.

**The product owner's decisions (kinds checkpoint, 2026-10-22):**

- A capability has at most one domain, and a domain has one or more capabilities. The product owner's words: "capability cant be many to many with domain. domain can have 1 more or more capability. and capability can have only 1 domain." This replaces the N:N row for Domain and Capability in the locked table. A capability with no domain yet is a gap, never a stop. The spine's single `domain` field and the folder layout stay as they are. The link between a domain and a business intent stays loose and N:N, for search only.
- Business intents are still identified by one another — a connection, never a dependency (agreed 2026-10-21; plan files use it, for example #722 is identified by #717). The locked model's "needs and identified by join capabilities only" is about the parts of the product: between parts, only capabilities need or are identified by another capability, and a functionality has neither.

**Reading we made (not an addition; please check it):**

- A functionality has no direct link to a business intent. The locked links table has no such row, and it says a functionality's ICE goes through its parent capability. So the business intent's Touches list names domains and capabilities, not functionalities. Q2 is then answered at the capability level.

**Note for the write stage:** the questions Q8 to Q13 in `draft-questions.md` were written for option 1.B (one ICE for each pair). The write stage must write the tests from the locked model and the decisions above, not from that draft.
