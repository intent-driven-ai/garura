# Draft — the kinds (stage: kinds, steps 2 to 4) — #826

You decide one thing now: whether the words below say your answer to Decision 2 correctly. Your answer is that the Story carries the Context guidance, and the context sub-agent of the build play collects the context itself when the play runs. Decision 1 is agreed as recommended, and the kinds below now follow both answers. Three kinds change (Story, Slice, Plan), and no other kind changes.

## Step 2 — Reuse what exists

### What we reuse, with no change

- **The routing table** (`docs/philosophy/idd-principles.md`, "The Routing Table", lines 126–135). It is the test for this change. Each row must stay true.
- **The ICE kind** (ontology v9). Its three parts stay: Intent (Goal, Limit, Fails if), Context (Read, Never read, Persona, Scope), Expectation (Scenario, Done means, Quality need). v9 already says what its Context is: "the rules for the sub-agent that gathers context" (ontology v9, ICE, "What it is" and the Context property). Your answer to Decision 2 uses these words as they are. So the ICE kind does not change.
- **Context crafting** (`CLAUDE.md`, Behavioral Rule 4: "Agents roles are to gather context and put those on files. the actual work are supposed to be done by skills, which agents will call."). The context sub-agent of a build play is this agent. We reuse it. We make no new kind for it.
- **The issue's short-term memory** (`.garura/core/config.yaml`, `stm.base-path`: `.garura/project/issues/`). The context sub-agent puts what it collects in `.garura/project/issues/<issue>/` for the builder. We reuse this place. We make no new place.
- **The Epic kind.** It has no ICE. The eval reads it. Nothing in it names failure conditions. No change.
- **The eval folder of a slice** (v9, Q28): `.garura/project/plans/<plan-id>/evals/<slice>/`. A builder never reads it. We put the hidden file in it.
- **The usage guide** (v9, Q31). No change.
- **The rule for recovery in plays** (Garura memory, `core/memory/standards/rules/expectation-generation.md`, lines 33–41). For each failure condition, exactly one recovery entry; the trigger is the failure as a symptom; the direction is the opposite of the failure, as guidance, never code. Decision 1 (agreed) uses this rule for product ICE.
- **The Symptom-Based Feedback Protocol** (`idd-principles.md`, lines 164–182). Q35 (the handoff plan says what the product does wrong, not which check failed) is this protocol.

### Where the need clashes with what exists

1. **The Story's scope of work says "what must never happen"** (v9, Story, "Scope of work"; the Story examples; Q29's "Answered by"). The builder reads the Story, so the failure conditions reach the builder. Routing table row "Failure conditions": Builder ✗.
2. **The Slice's eval reads only the epic, the stories and the usage guide** (v9, Slice rule; Slice "Eval": "no failure condition they name happens"). When the stories no longer name failure conditions, the eval must also read the hidden file.
3. **The Plan's folder says `evals/` is "written by the eval play"** (v9, Plan, "Folder"). Now the plan play also writes the hidden file into that folder. So the Plan changes, though the need did not name it.
4. **The recovery conditions have no source.** The product ICE's Expectation has no recovery line. Closed by Decision 1 (agreed).
5. **The builder must get "all of Context"** (routing table, row "Context": Builder ✓ (all)). The ICE page also holds the "Fails if" lines, so the builder must not open it. Closed by Decision 2: the Story carries the guidance, the context sub-agent collects the context, and the builder reads the collected context in the issue's short-term memory.
6. **The word "context" means two things.** The ICE's Context part is the guidance (what to read, what never to read, the persona, what is in and out). The context itself is what the sub-agent collects from that guidance (the opening hours, the payment rules). v9 already says the ICE's Context is "the rules for the sub-agent", but the Story kind did not name the two apart. See the terms below.
7. **The word "scope" means two things.** The ICE's Context has a "Scope" line (what is in and out). The Story has a "Scope of work" property. This change does not rename either. The links stage keeps the two words apart. (Proposed for the links stage: the Story holds the Context guidance as its own property, not inside "Scope of work".)

## Step 3 — The terms

Words from the routing table, and the ontology words they mean:

| Routing table word | Ontology word | Where it is |
|--------------------|---------------|-------------|
| Goal (Intent) | Goal | ICE, Intent part; in the Story |
| Constraints (Intent) | Limit | ICE, Intent part; in the Story |
| Failure conditions (Intent) | Fails if | ICE, Intent part; in the hidden file, never in the Story |
| Context | Context guidance, and the context the sub-agent collects | see the two rows below |
| Success scenarios (Expectation) | Scenario, Done means, Quality need | ICE, Expectation part; in the Story |
| Recovery (Expectation) | Recovery condition (the plan play writes one for each "Fails if" line) | in the hidden file, never in the Story |
| Eval author | the eval play, when it builds the eval | Slice, "Eval" |
| Validator | the eval, when it runs on the built slice | Slice, "Eval" |
| Encrypted evals | the slice's eval, in the eval folder a builder never reads | Slice, "Eval" |
| Recovery handoff plan | the handoff plan (Q35) | the eval's output when it finds a failure |
| Builder | the agent that builds a story | reads the Story and the collected context |

The two meanings of "context":

| Term | What it is | Who writes it | Where it is | Who reads it |
|------|-----------|---------------|-------------|--------------|
| **Context guidance** | The four Context lines of the story's two ICE: what to read, what never to read, the persona, what is in and what is out. It says where to look. It holds no facts. | The plan play, from the two ICE, when it makes the Story | In the Story | The context sub-agent; the eval |
| **Context** (the context itself) | What the sub-agent found by following the guidance: the facts, rules and files the builder needs, for the persona, inside the scope | The context sub-agent of the build play, when the build play runs (CLAUDE.md, Rule 4: agents gather context and put it on files) | In the issue's short-term memory, `.garura/project/issues/<issue>/` | The builder |

**Who collects the context:** the context sub-agent of the build play — the agent that does context crafting. It reads the Story's Context guidance, never the ICE page. It collects the context at run time, not when the Story is made, so the context is fresh for each run. It puts what it collected in the issue's short-term memory. The builder reads it there.

New nouns: **context guidance**, **the hidden file** (the failure and recovery conditions of a slice's stories), **recovery condition**, **handoff plan**.
Verbs: the plan play **writes** the context guidance into the Story; the context sub-agent **collects** the context and **puts** it in the issue's short-term memory; the builder **reads** it there; the plan play **writes** the hidden file; the eval **reads** the hidden file; the eval **writes** the handoff plan; the builder **gets** the handoff plan.

Not new kinds: the context sub-agent is an agent of a play, as the plan play is a play; the collected context is a file of one run in the issue's short-term memory; the hidden file is a part of the Slice's eval. The hidden file's proposed name: `.garura/project/plans/<plan-id>/evals/<slug>/failure-and-recovery.md`. The links stage sets its properties.

## Step 4 — The kinds

### Story (changes)

**What changes:** It holds the goal, the constraints, the Context guidance and the expectations (the scenarios, what "done" means, and the quality needs) of its two ICE. The Context guidance is the four Context lines of its two ICE: what to read, what never to read, the persona, what is in and what is out. The Story does not hold the context itself: when the build play runs, its context sub-agent reads the guidance, collects the context and puts it in the issue's short-term memory for the builder. The Story never holds a failure condition or a recovery condition. Its examples lose "no slot is booked twice", "no card is charged twice" and "no decision goes out without a score".
**Why:** The builder reads the Story and the collected context, and never the ICE page, so it never sees a "Fails if" line. It still gets all of Context, through the sub-agent, as the routing table says. The context is collected when the work runs, so it is not stale when the work starts.
**What stays:** It represents one feature, sits in one epic, and is written by the plan play from its two ICE. Who reads it: both.
**Log line:** Story — it holds the goal, the constraints, the Context guidance (the four Context lines) and the expectations of its two ICE, and never a failure condition or a recovery condition; it does not hold the context itself, which the build play's context sub-agent collects from the guidance at run time and puts in the issue's short-term memory for the builder, so the builder gets all of Context and never opens an ICE page (routing table, #826); "what must never happen" goes from its scope of work and its examples.

### Slice (changes)

**What changes:** Its eval reads four things: its epic, the stories in that epic, the hidden file `failure-and-recovery.md` in its eval folder, and its usage guide. The hidden file lists each story of the slice with its failure conditions and its recovery conditions. The plan play writes it; the eval play reads it to build the eval; the eval reads its recovery conditions when it runs, and writes a handoff plan that says what the product does wrong, never which check failed. Its "Eval" property says "no failure condition in the hidden file happens", in place of "no failure condition they name happens". "Lives at" names the hidden file. The eval gets Context from the stories' Context guidance (routing table, Validator ✓ Context).
**Why:** When the stories no longer name failure conditions, the eval needs another place to find them. The hidden file is in the eval folder, which a builder never reads.
**What stays:** One eval and one usage guide, in its home plan's folder. A builder never reads the eval folder. The eval never reads the ICE or the code.
**Log line:** Slice — its eval reads its epic, its stories, the hidden file `evals/<slug>/failure-and-recovery.md` (each story's failure conditions and recovery conditions, written by the plan play) and its usage guide; it tests that no failure condition in the hidden file happens, and when one does, it writes a handoff plan that says what the product does wrong and never names the condition (#826).

### Plan (changes — not named in the need)

**What changes:** Its "Folder" property says that the plan play writes the hidden file `failure-and-recovery.md` in `evals/<slug>/`, the eval play writes the eval beside it, and the build writes the guide in `guides/`. Its "What it is" says that, when it creates the stories of an epic, it also writes the slice's hidden file, from the same two ICE of each story: for each "Fails if" line, exactly one recovery condition, by the rule in `standards/rules/expectation-generation.md` (Decision 1). It interprets each ICE once.
**Why:** v9 says the evals folder is "written by the eval play". Now the plan play writes into it too.
**What stays:** One plan for each business intent. Its three actions, in their order. The plan play is not a builder: it reads all of the ICE and splits it, so no builder reads the evals folder.
**Log line:** Plan — when it creates a slice's epic and stories, the plan play also writes the slice's hidden file `evals/<slug>/failure-and-recovery.md` from the same two ICE of each story, with exactly one recovery condition for each "Fails if" line, so each ICE is interpreted once; its folder's `evals/` holds that file and the eval (#826).

### Kinds that do not change

This change touches no kind beyond the Story, the Slice and the Plan.

- **ICE — no change.** Its parts stay. Its Context is already "the rules for the sub-agent that gathers context" (v9). Its rule "No work item carries it. Only a Story reads it" stays true: the plan play reads it and writes the Story and the hidden file; the context sub-agent reads the Story's guidance, not the ICE; the hidden file is not a work item.
- **Epic — no change.** It names no failure condition. The eval reads it, as in v9.
- **Bug, Spike, Chore — no change.** They are children of a Story and carry no ICE part. How the handoff plan reaches the builder (for example, as a Bug under the story) is not part of this need.
- **Business Intent, Source, Domain, Capability, Feature — no change.**

### The combined log line (version 9 to 10)

- 2026-10-23 — v10 (#826, plan #788, with the product owner): the routing table of `idd-principles.md` holds word for word. A Story holds the goal, the constraints, the Context guidance and the expectations of its two ICE, and never a failure condition or a recovery condition. The Story does not hold the context itself: the build play's context sub-agent reads the guidance, collects the context at run time and puts it in the issue's short-term memory, so the builder gets all of Context and never opens an ICE page. The plan play writes each story's failure conditions, and one recovery condition for each, into the slice's hidden file `.garura/project/plans/<plan-id>/evals/<slug>/failure-and-recovery.md`, from the same two ICE, so each ICE is interpreted once; the Plan's folder says so. The Slice's eval reads its epic, its stories, the hidden file and its usage guide, tests that no failure condition in the hidden file happens, and when one does, writes a handoff plan that says what the product does wrong and never names the condition. The ICE does not change. Q26 and Q29 change; Q32–Q35 are added. Dropped: "a story's scope of work says what must never happen".

## Decisions

### Decision 1 — Where the recovery conditions come from (AGREED)

**Question:** When the plan play writes a slice's hidden file, where does it take each story's recovery conditions from?
**Answer (agreed):** The plan play makes them. For each "Fails if" line of the story's two ICE, it writes exactly one recovery condition, by the rule plays already use (`standards/rules/expectation-generation.md`): what the eval sees when it fails, and the way back to a good state, as guidance, never as code. It also marks each one: the builder can fix it alone, or a person must decide. The ICE does not change.
**Why it matters:** The eval needs a recovery condition for each failure, to tell the builder how to get back to a good state. If no part of the model says where they come from, they are not written, or each play makes them a different way.
**Example:**
- Clinic. ICE of "Pick a free slot" says: Fails if a slot is booked twice. The plan play writes "When a slot has two bookings: keep the first, free the second, tell the second patient. The builder can fix this alone."
- Shop. ICE of "Guest checkout" says: Fails if a card is charged twice. The plan play writes "When a card has two charges for one order: refund the second. A person must decide, because money goes out."
- Bank. ICE of "Score the application" says: Fails if a decision goes out without a score. The plan play writes "When a decision has no score: hold the decision until the score exists. The builder can fix this alone."

### Decision 2 — How the builder gets all of Context (your answer — please confirm the words)

**Question:** The routing table gives the builder "all of Context". Where does the builder get it, when it must never open the ICE page (the page also holds the "Fails if" lines)?
**Answer (the product owner's):** The Story carries the Context guidance: the four Context lines of its two ICE (what to read, what never to read, the persona, what is in and what is out). The Story does not carry the context itself. When the build play runs, its context sub-agent — the agent that does context crafting — reads the guidance in the Story, collects the context, and puts it in the issue's short-term memory. The builder reads the Story and that collected context. It never opens an ICE page, so it never sees a "Fails if" line. The ICE does not change.
**Why it matters:** If the builder does not get the context, it invents its own, which the routing table forbids. If it gets the context by opening the ICE page, it sees the failure conditions, and the barrier breaks. If the plan play wrote the context itself into the Story, the context could be old by the time the work starts.
**Example:**
- Clinic. Story #342 "Pick a free slot" holds the guidance "Read: the clinic's opening hours. Never read: patient health records. Persona: the patient on a phone. In: open slots; out: moving a booking." When the build play runs, the sub-agent reads the clinic's opening hours, does not open health records, and puts the hours and the slot rules in `.garura/project/issues/342/`. The builder reads them there.
- Shop. Story #122 "Guest checkout" (Capability Checkout) holds the guidance "Read: the payment rules. Never read: saved card data. Persona: the guest shopper on mobile. In: card and wallet; out: saved addresses." The sub-agent collects the payment rules into `.garura/project/issues/122/`. The builder reads them there.
- Bank. Story #55 "Score the application" (Capability "Credit decision") holds the guidance "Read: the lending policy. Never read: other customers' accounts. Persona: the credit officer. In: the documents sent; out: credit bureau data." The sub-agent collects the lending policy into `.garura/project/issues/55/`. The builder reads it there.

**Please confirm:** Do these words say your answer correctly?

## Points for the links stage (not decisions)

- Story property (proposed): the Context guidance is its own property ("Context guidance", required), not inside "Scope of work", so "Scope" (the ICE Context line) and "Scope of work" (the Story property) stay apart.
- Story rules: "a story never holds a failure condition or a recovery condition"; "a story holds the Context guidance, never the context itself"; "the context sub-agent reads the guidance in the story, never the ICE page".
- Plan rule: "the plan play writes the slice's hidden file from the same two ICE as each story, one recovery condition for each 'Fails if' line".
- Slice rule: the eval reads four things; the hidden file is in the eval folder; the handoff plan names what is wrong, never the condition.
- Drift: when an ICE changes after the story is made, the story's Context guidance and the hidden file are drift too, as the story's scope of work already is (v9 Story rule).
- The hidden file, when two plans hold a slice: it is in the home plan's folder only, as the eval is; when the slice gains a feature, its new story's conditions join the file.
- Fix at the write stage (the agreed questions draft named two capabilities wrongly): Q26 and Q34 say "Checkout" in place of "Payments" for Feature "Guest checkout", and "Credit decision" in place of "Lending" for Story "Score the application" ("Lending" is a domain, and a domain has no ICE). These are the v9 names; the meaning of the questions does not change.
- Q26 and Q32 gain the Context guidance at the write stage: the story holds the goal, the constraints, the Context guidance and the expectations, and the builder also sees the context the sub-agent collected.
