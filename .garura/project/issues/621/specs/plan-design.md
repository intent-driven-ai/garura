# Plan design — #621 (working note, not locked)

Built with Kapil on 2026-10-21, before any ADR. When it is agreed, it goes through `/adr` (it amends ADR 030), and the #621 stories are rewritten to match.

## What a plan is

- A plan exists to meet one business intent. The business intent is its root.
- It is not Claude Code's or Codex's plan mode. It follows how the product works.
- It is a cache. A script reads it, so agents need not re-read every issue and work folder (cost: on 2026-10-21 the #606 tree took 20 plan files and about 30 GitHub reads).
- A one-off fix builds no plan. It joins the tree that already exists, under a functionality.
- Many plans are active at the same time, for many people.

## Agreed

- **Where:** `.garura/project/plans/` — one YAML file per business intent with the whole tree, plus one index of every plan. (Adds a folder to the `.garura/` whitelist; the ADR allows it.)
- **Format:** YAML is the source. The tree a person reads is printed from it by a script, the same way every time.
- **Levels:** the product path — Business Intent → Capability → Functionality. Domains are not a level (see below). Garura builds itself this way from now on (Kapil). The Feature → Story path for Garura's own work goes.
- **Tracker:** every node maps to an issue in the team's tracker (GitHub, Jira, Azure, Linear, custom), through the platform adapter.
- **Defects:** a defect always sits under a functionality, so the tree shows an intent delivered with defects — also after the intent is met.

## Where the agent intent (ICE) sits

From the ontology (`core/components/memory/standards/schemas/product-os/ontology.md`, kind ICE):

- An ICE is not its own level. It is the agent's intent **for one capability or one functionality**, kept as the last section (`## Agent intent (ICE)`) of that node's page in the product model — for example `capabilities/harness-steering/capability.md`. That page is the ICE's home; the issue copies it.
- An ICE is built from one or more business intents (many to many).
- A piece of Work (Feature, Story, Chore, Bug, Spike) carries an ICE; one ICE may need many pieces of work.

So in the tree, each capability and functionality node carries its ICE. The ICE is *what must be true*; the issue is *the work order to make it true*. They are not the same thing.

The plan tree (agreed with Kapil, 2026-10-21):

```
Business Intent                  ── issue: Business Intent
└─ Capability + its ICE          ── issue: Feature
   └─ Functionality + its ICE    ── issue: Story
      ├─ Spike / Chore           ── issue, when the work needs one
      └─ Bug                     ── issue, always under a functionality
```

**Domains are not in the tree.** They live in the product model and set which areas the product covers. They have no issue. A business intent is linked to its domains loosely, through the model; a capability may name a domain, but the plan does not need it.

A capability that serves two business intents shows in both plans (Kapil: "100%").

## What goes into each issue (proposed)

- **Business Intent** — the intent in the person's words, why it matters, how we know it is met, and a link to its plan. It also reports open defects under it (see Defects below).
- **Feature (a capability)** — the capability in one line, its ICE (goal, limit, fails if, checked by — as far as known), the business intent(s) it serves, and a link to its model page.
- **Story (a functionality)** — the same, for one functionality, plus "seen on" when a prototype shows it.
- **Spike / Chore** — the question to settle or the job to do, and the functionality or capability it serves.
- **Bug** — what is wrong, how to see it, and the functionality it sits under.

The issue is the work order; the model page is the source of the ICE. `manage-plan` keeps the two the same.

## Three plays (names come later — Kapil, 2026-10-21)

1. **build-plan** — reads the business intent and the product model, builds the whole tree, writes the YAML, and creates or links an issue for every node.
2. **view-plans** — lists every plan, and shows one plan as the GOAL / DONE / NOW / NEXT / WAIT tree, from the YAML alone (no tracker reads, no inference).
3. **manage-plan** — update, edit, delete. It changes the YAML **and** the tracker together (new issues, closed issues, moved parents), so they never drift. It is orchestration only: it never touches branches or code. Branches are cut and merged by the implementation plays (start-change, merge-change) — Kapil, 2026-10-21.

Names are set later, with the naming standard (Kapil). Known clash: a skill is already called `manage-plan`.

## No dependency on the product model (Kapil, 2026-10-21)

A person can build a plan, create its issues and build from it **without** a full product model first. The model is created on the fly: build-plan writes light nodes (a capability or functionality with a goal-only ICE) in the holding folders the ontology already allows (ADR 043), and the links to domains are made later.

**What changes in the product model (linking only; how pages are saved stays the same):**

- Today the spine is a tree `domain → capability → functionality`, and every node already lists the business intents it serves (`intents`). The link from a business intent to its capabilities exists.
- Today's ready rule: an ICE is ready only when its node is linked all the way up to a domain that exists — a capability must name a domain, a functionality must name a capability that names a domain — and its business intent is confirmed. Until then "no play plans, breaks down or builds from it". The check is `check_ice_workable.py` (in `plays/intent/scripts/` and `plays/play-creator/references/`), and the rule is written in the ontology (kind ICE) and the spine schema (tree rules, ADR 043).
- New ready rule: a capability is ready when it serves a confirmed business intent. A functionality is ready when it names a ready capability. A missing domain is a warning for alignment, never a block.
- Plays to update: `/vision` (places capabilities in domains — it becomes a link it adds, not a gate) and `/understand` (details capabilities and functionalities — it no longer waits for a domain). The ontology, the spine schema and the check change with them.

Two different things (Kapil): the **product model reports** on a business intent (what is met, what has open defects); the **plan implements** it. A plan is not the report.

## Branches (Kapil, 2026-10-21, second pass — replaces "one branch per plan")

- A business intent is for tracking. It is captured and delivered, never built: agents cannot work on it, because it holds no ICE. It gets no branch.
- Agents work only on what holds an ICE: a capability or a functionality.
- When a capability is ready, it gets its own branch, cut from main.
- Each functionality (and each spike, chore or bug under it) gets a branch cut from its capability's branch, and merges back into it.
- The capability branch merges into main when its issue is done; the merge stops while any issue under it is open. Main is where releases come from.
- At start-change, the capability branch takes in the latest main.
- A capability serving two business intents has one branch, so no plan "owns" it; the clash in the first pass goes away.

## Settled with Kapil (2026-10-21)

1. **Main moving under a plan branch:** the plan branch takes in the latest main at start-change, each time an issue branch is cut from it.
2. **A bug after a plan is done:** a one-off. No plan, and a closed plan is never reopened. The bug sits under its functionality, so the business intent reports it as an open defect (through the product model, not the plan).
3. **A capability serving two business intents:** it shows in both plans.
4. **Garura's own model:** not built up front. The no-dependency rule above covers it — the #606 test builds only light nodes on the fly.
5. **Domains:** out of the tree; in the model; loosely linked to the business intent. The ready rule drops the domain (above).

## The litmus test: Garura's own work on this tree (proposed, 2026-10-21)

Kapil: two business intents, and #597 becomes a story under one of them. Storage and linking may be rewritten later; this is the test.

```
BI-A  People plan work toward a business intent, and pick it up across days and people
├─ Capability: Build a plan
│  ├─ Functionality: build the tree from a business intent and the model
│  └─ Functionality: create or link an issue for every node
├─ Capability: View plans
│  ├─ Functionality: list every plan
│  └─ Functionality: show one plan as a tree            (was #628)
└─ Capability: Manage a plan
   ├─ Functionality: update, edit, delete — plan and tracker together
   ├─ Functionality: a capability branch cannot land while an issue under it is open   (was #673)
   └─ Functionality: branches per capability, take in main at start-change

BI-B  A product model can be managed
└─ Capability: Link the product model
   └─ Functionality: a node is ready without a domain (the ready-rule change)
      └─ Story: #597, reworded to this
```

Open: #621 (a Feature today) — becomes BI-A, or closes as replaced by a new BI-A issue. #622–#627 (plays use the plan instead of a task list) — re-decide once the three plays exist; they may become a fourth capability under BI-A.

## Latest (Kapil, 2026-10-21, third pass — replaces the separate plan issue)

- A plan is linked to one business intent, and **the business intent's issue number is the plan's ID**. No separate plan issue.
- Plans can be linked: one plan can depend on another, or one can drive others. The links between business intents live in the ontology (one leads to another, one depends on another).
- So the test above becomes two or more plans (BI-A and BI-B), linked to each other, each handled on its own.
- The test tree above is still a proposal. Nothing is filed: the issues #702–#716 filed by mistake were withdrawn, and #621, #622–#628, #673 and #597 are back as they were.

## Branch dependency between plans (Kapil, 2026-10-21)

When plan A depends on plan B:
- A cannot merge into main until B is done. Before A merges, B has either merged into A's branch or already merged into main.
- B, if it does not depend on A, merges straight into main.
- **No loops:** if A depends on B and B depends on A, they are one plan — merge them into one.
- Plan branches are only merged, never rewritten, so a dependent plan can always take in the other's work.
- "Drives" is a looser link; only "depends on" sets a merge order.

## Dependencies live in the product model (Kapil, 2026-10-21)

Dependencies sit only at the lower levels: a capability on a capability, a functionality on a functionality, and a feature, story or spike on another.

**Business intents are connected, not dependent** (Kapil, 2026-10-21). One business intent can lead to another — while building one, we find a feature that must change in another — but neither waits on the other. The ontology is a graph of connections at that level, not a dependency chain.

What the ontology needs (proposed):
- Define **Work** — today named but not defined — as five kinds: Feature (the work order for a capability), Story (for a functionality), Spike, Chore and Bug (each under a functionality).
- A **depends on** link between capabilities, between functionalities, and between pieces of work.
- A **led to** (connected) link between business intents — no merge order, no waiting.
- A plan's dependency is **worked out** from the lower links, not set by hand: if anything in plan A depends on something in plan B, plan A depends on plan B.

Kapil: "If we can put stories, spikes, and features into it, I think our product ontology is pretty much sorted."

## Open points

6. How #621, #622–#628 and #673 move into the test tree (above).
7. Whether to file BI-A and BI-B and their capabilities and functionalities now, as the first use of the tree.
