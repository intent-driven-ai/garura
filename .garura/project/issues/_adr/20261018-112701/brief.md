# Decision brief — where an approved memory update lands, and where memory and ADRs are reviewed

Shape: markdown (a framework decision; Garura's own ADR in `docs/adr/`).

## Decision

1. **Short-term memory is the current issue only.** Every lookup names its issue. Short-term
   memory is that issue's folder, never another issue's. Garura memory and Phoenix memory are
   read in full by every issue. The order does not change: short-term memory, then Garura
   memory, then Phoenix memory, stopping at the first tier that answers. Research is allowed
   only after all three have nothing.
2. **An approved researched answer lands in the issue's short-term memory.** When no tier
   answers, the agent researches (the web or the model may draft the answer). A person reviews
   it and approves it. The approved answer is written to the issue's short-term memory, and the
   work then decides from memory. A draft from the web or the model never goes straight to
   Garura or Phoenix memory.
3. **Promotion happens outside the work.** Moving an answer from short-term memory up to Garura
   or Phoenix memory is a promotion. It happens outside the piece of work, as its own memory
   update that a person approves.
4. **A person's own answer to a question goes into Garura memory**, so no one is asked the same
   thing twice (Kapil's "A" on #655).
5. **Learned checkpoint answers are not memory.** The record of past checkpoint approvals stays a
   checkpoint tool. It holds only "approved or not" for a kind of change and cannot answer a
   question.
6. **A play's own working files stay direct.** The files a play hands from one of its steps to
   the next inside one run (ADR 011) are read and written directly. Only memory lookups go
   through the memory tool, which can still find those files later as short-term memory.
7. **Memory and ADRs are reviewed in the review tool.** The review tool gets a third section,
   **Memory and ADRs**, next to Intents and Product. It shows short-term, Garura and Phoenix
   memory, the memory updates waiting for a person, the ADRs waiting for a person, and which
   memory each decision came from. Every memory review and ADR review happens there, with the
   same Catch up cards as intents and product (#644): one card per change, swipe right to
   accept, swipe left to leave for later. Until the tool has this section, a person approves by
   typing, as today (including the `/adr` play's pinned accept).

## Why now

The memory tool's contract (#655, PR #666, merged on 18 October) already follows points 1 to 6:
every lookup names its issue, an update may target short-term memory, and a draft from the web
or the model must target short-term memory. ADR 035 on main says otherwise in three places:
§5 says the approved update is written to Garura or Phoenix memory; §7 names only a Memory view;
and "Not decided here" still lists the two questions settled on #655. ADR 034 §2 still counts
learned checkpoint answers as memory. The memory tool (#657), memory updates (#658) and the
memory review (#664) are built next. They must build the rules Kapil set, not the old text. The
design review of PR #666 raised this as its first major finding (TIC-1).

## Options considered

**Where an approved researched answer lands**
- **A — chosen:** a person approves it before it is written; it is written to the issue's
  short-term memory; promotion to Garura or Phoenix memory happens outside the work.
- **B — the agent writes it to short-term memory alone; a person checks it only at promotion.**
  Lost: short-term memory is read first, so the agent's next lookup would find its own draft and
  use it at once. A guess from the model would drive the work with no person in between, which
  ADR 035 §5 forbids.
- **C — ADR 035 as written: straight to Garura or Phoenix memory after approval.** Lost: Kapil
  wants the answer in the issue's short-term memory first ("That information goes into STM, the
  local memory"), and only promoted content in Garura and Phoenix memory, which keeps them small
  and clean.

**What short-term memory covers**
- **A — chosen:** the current issue only.
- **B — every issue's folder.** Lost: another issue's old notes would answer first and stop the
  lookup, so Garura and Phoenix memory would never be reached. For example, an agent searching
  for "commit message" would stop at old fix notes in another issue and miss the commit rule.

**Where memory and ADRs are reviewed**
- **A — chosen:** the review tool's Memory and ADRs section, with the Catch up cards.
- **B — a separate memory page, or typed approval in the terminal for good.** Lost: Kapil wants
  every review in the one tool, with the same card method. Typing stays only until the section
  exists.

**Learned checkpoint answers**
- **A — chosen:** not memory.
- **B — the memory tool reads them too.** Lost: that record holds only "approved or not" for a
  kind of change; it cannot answer a question.

**A play's own working files**
- **A — chosen:** read and written directly.
- **B — every read and write goes through the tool.** Lost: it adds a step to every script and
  gains nothing; the tool can still find those files later as short-term memory.

## Decided by

Kapil Viren Ahuja.

## Decided in

#667 (this spike, under Feature #653 and business intent #606), from Kapil's answers on 18
October during #655 (PR #666). His words:

- "it still needs to get the answer, which it gets from either research algorithms or whatnot.
  That is then reviewed by the human, and it needs to be approved. That information goes into
  STM, the local memory."
- "The promotion from STM to Garuda memory and long-term memory happens outside, so I think that
  is fine."
- "When a short-term memory is looked up, it is looked up only in the current issue, not the
  other issues. That is critical. If it reads everything, then the point of LTM and Phoenix
  memory is useless. It reads only in the current issue that it is working on."
- "the agents start by looking in short-term memory. If they don't find it, they go to the
  project memory, which is also known as the Garura memory. When they don't find that, then they
  go to find the Phoenix memory, which is the global memory. Only after that do they go and do
  research and find everything else."
- "There needs to be a third section of memory and ADRs in it, where it should be showing the
  STM, LTM, and Phoenix memory allowed. Any reviews that happen happen there, and the same card
  sweeping next method should be used."
- On #655's two questions: "approve, A, A".
