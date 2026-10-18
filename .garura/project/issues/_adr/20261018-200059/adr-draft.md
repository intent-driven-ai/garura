# ADR 037 — Every Agent Decision Keeps a Trace of the Memory It Rested On, and the Review Tool Has Five Sections

**Status:** Proposed
**Date:** 2026-10-19
**Level:** framework
**Decided in:** #659 (every decision names its memory), under Feature #653 and business intent #606, with PR #676 and its review; the #659 plan log (`.garura/project/issues/659/specs/plan.md`) and the review tool's design (`.garura/project/issues/617/specs/review-tool.md`, §4 item 7)
**Amends:** ADR 035 — §6 "Every decision names its memory": a decision keeps a trace — the steps the agent took, in order, each with what it looked for, what it found, and the memory lines that said so (a tier, a file, the lines and a fingerprint of that text), kept with the exact text, the version of memory it was read from and up to three lines before and after — not one source; a check reads every step's source again, names the step whose source changed or is gone, and flags a decision with no trace; §7 "A memory review" (a Memory view, made Memory and ADRs by ADR 036): the review tool's sections are Intents, Product, ADRs, Memory and Agent decisions, and which memory each decision came from is shown in Agent decisions, as its trace (and with it §9's line on ADR 032 §3) · ADR 036 — §7 "Memory and ADRs are reviewed in the review tool": the one Memory and ADRs section is replaced by three — ADRs (the ADRs a person records with `/adr`, waiting for a person), Memory (the memory that exists: mostly Garura memory, and an issue's short-term memory once one is picked; the memory updates waiting for a person; and Ask memory, a plain-words search over all three tiers on the same vectorless memory tool, mocked only for now) and Agent decisions (every decision an agent made, with its trace); and with it §8's lines on ADR 035 §7 and ADR 032 §3; where this ADR is silent, §7 stands: the reviews happen in the review tool, on the Catch up cards, and a person approves by typing until the sections exist · ADR 032 — §3 "Two review tools", as amended by ADR 033, ADR 035 and ADR 036: the review tool has five sections — Intents, Product, ADRs, Memory and Agent decisions — in place of a third section called Memory and ADRs; the Intents and Product views, and ADR 033's part of §3 (they show the whole model's approval state when they open), stand
**Affects:** `core/tools/memory/contract/v4.json` (already records the trace: `cite`, `citations` with its check, and the lines around each source; its `cite` summary cites ADR 035 §6 and ADR 034 §4 only), `core/tools/memory/citations.py` (`cite` and `citations`; keeps three lines around each source; its header cites ADR 035 §6 only), `core/tools/memory/memory.py` (wires both commands and where the records are kept), `core/tools/memory/README.md` (describes the trace; no rule changes), `core/tools/memory/contract/check_contract.py` and its samples (`cite.json`, `citations.json`, `citations-check.json` and the broken ones), `core/components/memory/standards/rules/resolution.md` (the new section "Every Decision Names Its Memory", which this ADR is the record for) and its row in `core/components/memory/standards/rules/_index.md`, the Phoenix memory copy `~/.garura/phoenix-memory/standards/rules/resolution.md` (the section lands there with #659), `core/components/plays/play-creator/references/write_drive_review.py` and its identical copies in `core/components/plays/vision/scripts/` and `core/components/plays/understand/scripts/` (the drive review record carries each decision with its trace; optional), `.garura/project/issues/617/specs/review-tool.md` (§4: five sections, Ask memory, Agent decisions with each step's source in its place; story 9) and `.garura/project/issues/617/specs/review-tool-mockup.html` (the five-section switch, the Ask memory mock, 12 real traces), `.garura/project/issues/653/specs/plan.md` (item 11) and `.garura/project/issues/606/specs/plan.md` (item 8, step 2), `.garura/project/issues/654/specs/stories.yaml` (item 11, story #664: still one Memory and ADRs section and one source per decision), the `/adr` play's ICE source `core/components/plays/adr/reference/ice.md` (C6: the accept card sits in ADRs once it exists) and its compiled `core/components/plays/adr/SKILL.md` (recompiled through `/play-editor`, never hand-edited), `core/grounding/glossary.md` (not changed: its Evidence row is why the section is not called evidence; its Resolution trace row is a different, older trace), and things not built yet: the review tool's ADRs, Memory and Agent decisions sections (#664, with #641–#644), Ask memory (mocked only), and the agents' move onto `cite` (#661, #663)
**ICE impact:** The agent intents of the plays whose agents make decisions change as those agents move onto the memory tool (#661: `/intent`, `/vision`, `/understand` and every play's close; #663: every other play), each through its ICE source and `/play-editor`: each decision is recorded with the tool's `cite` as a trace — the steps taken, each with its source — not as one source. No play's ICE changes on this branch: no agent calls `cite` yet, and the drive review record's decisions are optional, so `/vision` and `/understand` run as before. The `/adr` play's C6: once the review tool's ADRs section exists, the accept card ADR 036 placed in Memory and ADRs sits in ADRs; until then C6 stands as written. The ICE kind does not change (Goal, Limit, Fails if, Context, Checked by, Quality need); a decision record is not an ICE.
**Business intent check:** none — a framework decision on how an agent records a decision and how the review tool is laid out; no person's business intent changes, and the Business Intent kind's rules stand: only a person confirms or drops one (ADR 031); the Intents section is unchanged
**Related:** ADR 033 (approval in the product model), ADR 031 (business intent and ICE), ADR 012 (evidence self-commit — why the section is not called evidence), ADR 015 (the older resolution trace), ADR 034 §4 (every answer names its source), #659, PR #676, #653, #661, #663, #664, #641–#644 (the review tool), #606

## Context

ADR 035, accepted on 18 October, says every decision an agent makes names the memory it came from: "the tier, the file and the lines it rests on" (§6). It left the exact shape to the feature plan's item 6, which is #659.

#659 built it (PR #676). While it was being built, Kapil looked at the screen that shows the agents' decisions. On 19 October he found that one or two lines leave no context: a decision rests on several things, one after another. So the memory tool's contract, version 4, now records a **trace** for each decision: the steps the agent took, each with its source, the text it read and the lines around it.

On 18 and 19 October Kapil also split the review tool's third section. ADR 036 had named it "Memory and ADRs". The review tool's design and its mockup on this branch now have five sections.

So the accepted ADRs and what #659 built disagree in two places:

- ADR 035 §6 names one source per decision. Contract version 4 records a trace of steps.
- ADR 032 §3 (as amended by ADR 035 and ADR 036), ADR 035 §7 and ADR 036 §7 name a third section, "Memory and ADRs". The design and the mockup have five sections.

The memory rule's new section, "Every Decision Names Its Memory" (`core/components/memory/standards/rules/resolution.md`), goes to Phoenix memory when #659 lands. The decision it rests on must be recorded first. Kapil, on the review of PR #676: "fix all the items first".

## Decision

### 1. Every agent decision keeps a trace

- A **trace** is the steps the agent took, in order.
- Each step says what the agent looked for, what it found, and the memory lines that said so: a tier (short-term, Garura or Phoenix memory), a file, the lines, and a fingerprint of that text.
- The record keeps the exact text the agent read, the version of memory it read it from, and a few lines around it: up to three before and three after. So a person sees each step in its place, with the lines the agent used marked.

A decision usually rests on several steps, not one source. A sign-in decision, for example, reads the product's profile (who the users are), then the domain that covers sign-in, then the profile's security level and compliance, and then the knowledge lines those values select.

Kapil, 19 October: "the source should show a few lines before and after and then the part of section which influenced should be highlighted. also, i dont think it will be only 1 line that decided. it will be multiple. for example your question 'How do shoppers sign in?' this is based on a project profile, domain, its security level and then the file where knowledge is put. when these decisions are made, this sort of thinking is critical to show.. these are called traces".

### 2. A check reads every step's source again

- The check names the step whose source changed or is gone.
- A decision with no trace is flagged.

### 3. The review tool has five sections

**Intents | Product | ADRs | Memory | Agent decisions.** These replace the one "Memory and ADRs" section.

- **ADRs** — the ADRs a person records with `/adr`, waiting for a person.
- **Memory** — the memory that exists: mostly Garura memory inside the project, and once an issue is picked, that issue's short-term memory. The memory updates waiting for a person live here.
- **Agent decisions** — every decision an agent made, with its trace. It is named "Agent decisions" because "evidence" already names a play's run records.

Intents and Product do not change. Where this ADR is silent, ADR 036 §7 stands: the reviews happen in the review tool, on the Catch up cards, and until the sections exist a person approves by typing, as today.

Kapil, 18–19 October: "intents - product - adr(s) -> these are the adrs that a human puts, using /adr - memory -> this is list of memories that exist.. omstly garura memory inside the projecdt, and once an issue is selected then its STM. we woudl need a separate search interface that works like NLP ... then the agent adrs - we call this evidence, aka agent-decisions".

### 4. Ask memory: plain words on top, the same memory tool underneath

- The Memory section has a plain-words search, **Ask memory**, over all three tiers.
- Underneath it is the same memory tool the agents use: vectorless, finding things the way Claude Code does (ADR 035 §4). Only the interface is plain words.
- It is mocked only for now.

Kapil: "the tool withing garua is how claude code works. the tool we are building which will got into griffin will use nlp, but it will use vectorless search. the same tool under both, just that the interface for tool should be nlp ... you can design the interface and create some mocks for now. no need to build this whole this now".

### 5. What this changes in older records

- **ADR 035 §6** — a decision names its memory as a trace of steps, each with its source, kept with the text, the memory version and the lines around it, not as one source. A check reads every step's source again. This is the shape §6 left to the feature plan's item 6.
- **ADR 035 §7** — the Memory view (Memory and ADRs since ADR 036) becomes three sections: ADRs, Memory and Agent decisions. Which memory each decision came from is shown in Agent decisions, as its trace. §9's line on ADR 032 §3 changes with it.
- **ADR 036 §7** — the one Memory and ADRs section becomes ADRs, Memory and Agent decisions. §8's lines on ADR 035 §7 and ADR 032 §3 change with it. The rest of §7 stands.
- **ADR 032 §3** — the review tool has five sections. This is a judgment call: ADR 032's status line already names "Memory and ADRs", which this decision makes wrong, so a direct pointer saves its reader a second hop, as ADR 036 did. The Intents and Product views, and ADR 033's part of §3, stand.

### 6. What this does not change

- One memory tool finds and updates memory, searching the way Claude Code does, with no index (ADR 035 §4).
- Nothing from the model or the web is used without a memory update a person approved (ADR 035 §5). Every step's source is memory.
- Every answer names its source (ADR 034 §4). A trace is that source, step by step. ADR 034 §4 is reached through ADR 035 §6, as before, so it gets no pointer of its own.
- Only the review step writes approval; the review tool writes nothing to the model (ADR 033 §6).
- Short-term memory stays per issue (ADR 008). Decision records are kept in the issue's own short-term folder, and a lookup never finds them.
- Only a person accepts an ADR. Only a person confirms or drops a business intent (ADR 031).

## Consequences

### Positive

- A person sees what each decision rested on, step by step, in its place, with the lines the agent used marked. They can judge the step, not only a file name.
- A source that changed or is gone is caught and named by its step. A decision with no trace is flagged.
- The accepted ADRs, the contract (version 4) and the review tool's design say the same thing again. The rule's new section can go to Phoenix memory resting on an accepted decision.
- A person's ADRs, the memory that exists, and the agents' decisions are reviewed apart, each in its own section.
- "Evidence" keeps one meaning: a play's run records.
- A person can ask memory in plain words with no second search engine: one memory tool, vectorless, under both.

### Negative / Risks

- **The check sees only recorded decisions.** A decision that was never recorded is not flagged, so recording it is the agent's duty (`resolution.md`).
- **No agent keeps a trace yet.** Until the agents move onto the memory tool (#661, #663), the older rule (R1–R4 and its resolution trace) still governs them. Two kinds of trace sit side by side in `resolution.md` until then.
- **A source is shown as its memory, file and lines.** That is an exception to the review tool's no-file-paths rule, which Kapil asked for because the person must check it (`review-tool.md`, §4).
- **Ask memory and the three sections are a mock.** Until the review tool is built (#664, in the #606 plan), a local prototype stands in for memory approvals, and every other approval is typed.
- **A story must change:** story #664's filed text still describes one Memory and ADRs section and one source per decision.
- **Not decided here:**
  - what a person does on an agent decision. The design has "Looks right, or send back so the agent decides again from memory"; ADR 033 §6 (only the review step writes approval) bears on it;
  - whether the Memory section lists Phoenix memory, or reaches it only through Ask memory. The brief names Garura memory and the picked issue's short-term memory; ADR 036 §7 listed all three tiers;
  - still open from ADR 036: whether a product decision (a `decision.yaml` record) waiting for a person is reviewed in ADRs or under Decisions in the Product view, and who writes the approval when a person accepts a card (ADR 033 §6);
  - whether the glossary gains a row for this trace. Its "Resolution trace" row (ADR 015's older trace) shares the word.

## Alternatives Considered

- **Keep one source per decision (ADR 035 §6 as written).** Lost: one or two lines leave no context, and a decision rests on several things (Kapil, 19 October).
- **Keep the source as a file and lines only, without the text around it.** Lost: the person must see the lines in their place, with the part the agent used marked, to judge a step.
- **Keep one "Memory and ADRs" section (ADR 036 §7).** Lost: a person's ADRs, the memory that exists, and the agents' decisions are three different things to review. Kapil split them.
- **Call the agents' decisions "evidence".** Lost: "evidence" already names a play's run records.
- **A search index (vectors) behind Ask memory.** Lost: one memory tool, vectorless, as ADR 035 §4 decided. Only the interface is plain words.

## Work This Creates

None is filed yet; they are filed only when Kapil asks.

1. Once this ADR is accepted, the rule's new section in `resolution.md`, its row in the rules index, the `cite` summary in contract version 4 and the header of `citations.py` name this ADR beside ADR 035 §6.
2. The rule's new section goes to Phoenix memory when #659 lands (#659 plan, item 6).
3. Story #664 (`.garura/project/issues/654/specs/stories.yaml`, item 11, and its text on the tracker): the three sections, Ask memory as a mock, and each decision shown with its trace.
4. Change `/adr`'s C6 through its ICE source and `/play-editor` once the ADRs section exists (ADR 036's item 3, now naming ADRs).

## References

- `.garura/project/issues/659/specs/plan.md` — items 1e and 2, and the log of 19 October
- `.garura/project/issues/617/specs/review-tool.md` — §4 item 7 and story 9; `.garura/project/issues/617/specs/review-tool-mockup.html`
- `core/tools/memory/contract/v4.json` and `core/tools/memory/citations.py` — `cite` and `citations`, the trace and its check
- `core/components/memory/standards/rules/resolution.md` — "Every Decision Names Its Memory"
- `core/components/plays/play-creator/references/write_drive_review.py` — the drive review record
- `.garura/project/issues/654/specs/stories.yaml` — item 11, story #664
- ADR 035 — agents work only from memory; ADR 036 — an approved researched answer lands in short-term memory; ADR 032 — drive review of outcomes; ADR 034 — plays answer from memory inside a drive; ADR 033 — approval in the product model; ADR 012 — evidence self-commit
