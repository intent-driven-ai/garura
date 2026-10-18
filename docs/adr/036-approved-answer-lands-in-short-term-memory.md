# ADR 036 — An Approved Researched Answer Lands in the Current Issue's Short-Term Memory, and Memory and ADRs Are Reviewed in the Review Tool

**Status:** Accepted — amended in part by [ADR 037](037-agent-decisions-keep-a-trace-and-the-review-tool-has-five-sections.md): §7 "Memory and ADRs are reviewed in the review tool": the one Memory and ADRs section is replaced by three — ADRs (the ADRs a person records with /adr, waiting for a person); Memory (the memory that exists: mostly Garura memory, and an issue's short-term memory once one is picked; the memory updates waiting for a person; and Ask memory, a plain-words search over all three tiers on the same vectorless memory tool, mocked only for now); and Agent decisions (every decision an agent made, with its trace); and with it §8's lines on ADR 035 §7 and ADR 032 §3. Where the brief is silent, §7 stands: the reviews happen in the review tool, on the Catch up cards, and a person approves by typing until the sections exist
**Date:** 2026-10-18
**Level:** framework
**Decided by:** Kapil Viren Ahuja
**Decided in:** #667 (spike: where an approved memory update lands and where memory and ADRs are reviewed), under Feature #653 and business intent #606; from Kapil's answers of 18 October during #655 (PR #666)
**Amends:** ADR 035 — §1 short-term memory is the current issue's folder only, and every lookup names its issue; §5 an approved researched answer is written to the issue's short-term memory, never straight to Garura or Phoenix memory, and moving it up is a promotion, its own memory update a person approves outside the work, while a person's own answer to a question goes to Garura memory; §7 the review tool's third section is Memory and ADRs, where every memory review and ADR review happens, on the Catch up cards (and with it §9's line on ADR 032 §3); and Negative / Risks, "Not decided here": its first two questions are settled — learned checkpoint answers are not memory, and a play's own working files stay direct (ADR 011) · ADR 034 — §2 "What counts as memory": the learned checkpoint answers come off the list; they stay a checkpoint tool, which holds only "approved or not" for a kind of change and cannot answer a question; a person's answers to questions are kept in Garura memory · ADR 032 — §3 "Two review tools", as amended by ADR 035: the third section is Memory and ADRs, not Memory; it also shows the ADRs waiting for a person, and every memory review and ADR review happens there, on the same Catch up cards as Intents and Product (#644)
**Affects:** `core/tools/memory/contract/v1.json` (already follows parts 1 to 6; its lookup rule and its propose command cite ADR 035 §3 and §5 for rules this ADR now records; no rule changes), `core/tools/memory/README.md` (already follows parts 1 to 6, in "The lookup order", "When no tier answers" and "What is not memory"; no rule changes), `.garura/project/issues/653/specs/plan.md` (item 5, #658, still writes the approved update to Garura or Phoenix memory; item 11, #664, waits on this amendment and an `/adr` intent change), `.garura/project/issues/654/specs/stories.yaml` (the filed texts of stories #658 and #664: the update written to Garura or Phoenix memory, and "a Memory view" that approves memory updates only), `.garura/project/issues/617/specs/review-tool.md` (§4 "What the person sees": the Intents and Product switch gains a third section, Memory and ADRs, and Catch up covers memory updates and ADRs), the `/adr` play's ICE source `core/components/plays/adr/reference/ice.md` (C6: the pinned accept, typed today by hand, and the accept at a drive's final review) and its compiled `core/components/plays/adr/SKILL.md` (Step 3, recompiled through `/play-editor`, never hand-edited), and three things not built yet: the memory tool (#657), memory updates (#658) and the memory review (#664) in the review tool (#641–#644)
**ICE impact:** The `/adr` play's agent intent changes once the review tool's Memory and ADRs section exists: C6's pinned accept, typed today when run by hand, and the accept at a drive's final review move onto a card in that section, through its ICE source and `/play-editor`. Until then C6 stands as written. The agent intents of the plays whose agents read memory change as they move onto the memory tool (#653 plan items 8 and 10), each through its ICE source and `/play-editor`: every lookup names the issue, and short-term memory is that issue only; a researched draft is proposed to the issue's short-term memory and used only after a person approves it; a person's own answer goes to Garura memory. For `/intent` (C4, C5, Step 3), `/vision` (C11) and `/understand` (C13), the "memory update the person approves" that ADR 035 named lands in the issue's short-term memory. Parts 5 and 6 change no agent intent: no play reads learned checkpoint answers as memory today, and a play's step-to-step files already stay direct. The ICE kind does not change.
**Business intent check:** none — a framework decision on where an approved memory update is written, what short-term memory covers, and where a person reviews memory and ADRs; no person's business intent changes, and the Business Intent kind's rules stand: only a person confirms or drops one (ADR 031)
**Related:** ADR 011 (STM as inter-skill transport), ADR 008 (issue-centric STM), ADR 033 (approval in the product model), ADR 031 (business intent and ICE), #653, #655 (PR #666), #657, #658, #664, #641–#644 (the review tool; Catch up is #644), #606

## Context

ADR 035, accepted on 18 October, set Garura's memory system. Memory has three tiers: short-term memory, Garura memory and Phoenix memory. Agents read them in that order through one memory tool. Nothing from the model or the web is used until a person approves a memory update.

The memory tool's contract was built next (#655, PR #666, merged on 18 October). The design review of PR #666 raised its first major finding (TIC-1): ADR 035 §5, as written, disagrees with the contract's rule for researched drafts. Kapil answered on 18 October. The contract already follows his answers:

- every lookup names its issue;
- an update may target short-term memory;
- a draft from the web or the model must target short-term memory.

ADR 035 on main says otherwise in three places:

- §5 says the approved update is written to Garura or Phoenix memory.
- §7 names only a Memory view.
- "Not decided here" still lists the two questions settled on #655.

ADR 034 §2 still counts learned checkpoint answers as memory.

The memory tool (#657), memory updates (#658) and the memory review (#664) are built next. They must build the rules Kapil set, not the old text. This ADR records those rules.

## Decision

### 1. Short-term memory is the current issue only

- Every lookup names its issue. Short-term memory is that issue's folder, never another issue's.
- Garura memory and Phoenix memory are read in full by every issue.
- The order does not change: short-term memory, then Garura memory, then Phoenix memory, stopping at the first tier that answers.
- Research is allowed only after all three have nothing.

Kapil: "When a short-term memory is looked up, it is looked up only in the current issue, not the other issues. That is critical. If it reads everything, then the point of LTM and Phoenix memory is useless. It reads only in the current issue that it is working on." And: "the agents start by looking in short-term memory. If they don't find it, they go to the project memory, which is also known as the Garura memory. When they don't find that, then they go to find the Phoenix memory, which is the global memory. Only after that do they go and do research and find everything else."

### 2. An approved researched answer lands in the issue's short-term memory

- When no tier answers, the agent researches. The web or the model may draft the answer.
- A person reviews it and approves it.
- The approved answer is written to the issue's short-term memory. The work then decides from memory.
- A draft from the web or the model never goes straight to Garura or Phoenix memory.

Kapil: "it still needs to get the answer, which it gets from either research algorithms or whatnot. That is then reviewed by the human, and it needs to be approved. That information goes into STM, the local memory."

### 3. Promotion happens outside the work

Moving an answer from short-term memory up to Garura or Phoenix memory is a **promotion**. It happens outside the piece of work, as its own memory update that a person approves.

Kapil: "The promotion from STM to Garuda memory and long-term memory happens outside, so I think that is fine."

### 4. A person's own answer goes into Garura memory

When a person answers a question, the answer goes into Garura memory. So no one is asked the same thing twice.

### 5. Learned checkpoint answers are not memory

The record of past checkpoint approvals stays a checkpoint tool. It holds only "approved or not" for a kind of change. It cannot answer a question.

### 6. A play's own working files stay direct

The files a play hands from one of its steps to the next, inside one run (ADR 011), are read and written directly. Only memory lookups go through the memory tool. The tool can still find those files later, as short-term memory.

Kapil settled parts 4 to 6 on #655's two questions: "approve, A, A".

### 7. Memory and ADRs are reviewed in the review tool

- The review tool gets a third section, **Memory and ADRs**, next to Intents and Product.
- It shows short-term, Garura and Phoenix memory, the memory updates waiting for a person, the ADRs waiting for a person, and which memory each decision came from.
- Every memory review and ADR review happens there, with the same Catch up cards as intents and product (#644): one card per change, swipe right to accept, swipe left to leave for later.
- Until the tool has this section, a person approves by typing, as today. That includes the `/adr` play's pinned accept.

Kapil: "There needs to be a third section of memory and ADRs in it, where it should be showing the STM, LTM, and Phoenix memory allowed. Any reviews that happen happen there, and the same card sweeping next method should be used."

### 8. What this changes in older records

- **ADR 035 §1** — short-term memory is the current issue's folder only. Every lookup names its issue.
- **ADR 035 §5** — the approved update is written to the issue's short-term memory, not to Garura or Phoenix memory. Moving it up is a promotion, outside the work. A person's own answer goes to Garura memory. The rest of §5 stands, including approval by typing until the review exists.
- **ADR 035 §7** — the Memory view becomes the Memory and ADRs section, and every memory and ADR review happens there. §9's line on ADR 032 §3 changes with it.
- **ADR 035, "Not decided here"** — its first two questions are settled by parts 5 and 6. The other two stay open.
- **ADR 034 §2** — the learned checkpoint answers come off the list of memory. §6's line that they do not answer a pinned checkpoint stands.
- **ADR 032 §3** — the third section is Memory and ADRs, not Memory. This is a judgment call: ADR 035 already points 032 §3 to a Memory view, so a direct pointer lets a reader of 032 see the current name without a second hop.

### 9. What this does not change

- The lookup order (ADR 035 §3).
- Nothing from the model or the web is used before a person approves it (ADR 035 §5).
- A play's step-to-step files are read and written directly (ADR 011).
- Short-term memory stays per issue (ADR 008).
- Only a person accepts an ADR. Only where the person does it moves.
- Only a person confirms or drops a business intent (ADR 031).

## Consequences

### Positive

- Garura and Phoenix memory hold only promoted content. They stay small and clean.
- No draft from the model or the web drives the work before a person approves it.
- A lookup never stops at another issue's old notes. Garura and Phoenix memory are reached when the issue has nothing.
- The contract merged in PR #666 and the ADRs now say the same thing. The memory tool, memory updates and the memory review build from one set of rules.
- A person reviews intents, product, memory and ADRs in one tool, with one card method.
- A person is not asked the same question twice.

### Negative / Risks

- **An approved answer stays in its issue until it is promoted.** Another issue does not find it before then, so the same question can be researched and approved again.
- **Two approvals for something every project needs:** once in the issue, and once at promotion. More work waits for a person.
- **Promotion is a separate step.** If no one promotes an answer, it never reaches Garura or Phoenix memory.
- **Until the review tool has the section, every approval is typed.** That includes the `/adr` play's pinned accept.
- **Plans, stories and a play must change:** #653 plan item 5 and story #658 still write the update to Garura or Phoenix memory; item 11 and story #664 name a Memory view only; `/adr`'s accept moves through its ICE source and `/play-editor`.
- **Not decided here:**
  - whether a product decision (a `decision.yaml` record, also an ADR) waiting for a person is reviewed in Memory and ADRs or stays under Decisions in the Product view (ADR 032 §2; the review tool plan, §4). Read literally, "every ADR review happens there" would move it;
  - who writes the approval when a person swipes right on a memory update or an ADR (ADR 033 §6: the review tool writes nothing to the model; only the review step writes approval);
  - still open from ADR 035: whether the rest of a drive goes on while one memory update waits, and where in `.garura/` Garura memory lives (#656).

## Alternatives Considered

**Where an approved researched answer lands**

- **The agent writes it to short-term memory alone; a person checks it only at promotion.** Lost: short-term memory is read first, so the agent's next lookup would find its own draft and use it at once. A guess from the model would drive the work with no person in between, which ADR 035 §5 forbids.
- **ADR 035 as written: straight to Garura or Phoenix memory after approval.** Lost: Kapil wants the answer in the issue's short-term memory first ("That information goes into STM, the local memory"), and only promoted content in Garura and Phoenix memory, which keeps them small and clean.

**What short-term memory covers**

- **Every issue's folder.** Lost: another issue's old notes would answer first and stop the lookup, so Garura and Phoenix memory would never be reached. For example, an agent searching for "commit message" would stop at old fix notes in another issue and miss the commit rule.

**Where memory and ADRs are reviewed**

- **A separate memory page, or typed approval in the terminal for good.** Lost: Kapil wants every review in the one tool, with the same card method. Typing stays only until the section exists.

**Learned checkpoint answers**

- **The memory tool reads them too.** Lost: that record holds only "approved or not" for a kind of change; it cannot answer a question.

**A play's own working files**

- **Every read and write goes through the tool.** Lost: it adds a step to every script and gains nothing; the tool can still find those files later as short-term memory.

## Work This Creates

None is filed yet; they are filed only when Kapil asks.

1. Update #653 plan item 5 and story #658: the approved researched answer lands in the issue's short-term memory, and promotion is its own memory update.
2. Update item 11 and story #664: the section is Memory and ADRs, with ADR reviews and the Catch up cards.
3. Change `/adr`'s C6 through its ICE source and `/play-editor` once the section exists.
4. Add the third section to the review tool plan (`.garura/project/issues/617/specs/review-tool.md`, §4).

## References

- `.garura/project/issues/655/specs/plan.md` — item 1 ("approve, A, A") and the log of Kapil's answers to the PR #666 review
- `.garura/project/issues/655/review/design-findings-tool-interface-contract.yaml` — TIC-1
- `.garura/project/issues/653/specs/plan.md` — items 5 and 11, and the log
- `.garura/project/issues/617/specs/review-tool.md` — §4, the Catch up cards
- `core/tools/memory/contract/v1.json` and `core/tools/memory/README.md` — the memory tool's contract, version 1
- `core/components/memory/standards/rules/product.md` — rule 12, where a person's answers to questions are kept
- ADR 035 — agents work only from memory; ADR 034 — plays answer from memory inside a drive; ADR 032 — drive review of outcomes; ADR 011 — STM as inter-skill transport; ADR 033 — approval in the product model
