# Decision brief — every agent decision keeps a trace; the review tool has five sections

Shape: markdown (a framework decision; Garura's own ADR in `docs/adr/`).

## Decision

1. **Every agent decision keeps a trace.** A trace is the steps the agent took, in order. Each
   step says what the agent looked for, what it found, and the memory lines that said so: a
   tier (short-term, Garura or Phoenix memory), a file, the lines, and a fingerprint of that
   text. The record keeps the exact text the agent read, the version of memory it read it
   from, and a few lines around it (up to three before and after), so a person sees each step
   in its place, with the lines the agent used marked. A decision usually rests on several
   steps, not one source: a sign-in decision reads the product's profile (who the users are),
   the domain that covers sign-in, the profile's security level and compliance, and then the
   knowledge lines those values select. A check reads every step's source again and names the
   step whose source changed or is gone; a decision with no trace is flagged. Kapil, 19 Oct:
   "the source should show a few lines before and after and then the part of section which
   influenced should be highlighted. also, i dont think it will be only 1 line that decided.
   it will be multiple. for example your question 'How do shoppers sign in?' this is based on
   a project profile, domain, its security level and then the file where knowledge is put.
   when these decisions are made, this sort of thinking is critical to show.. these are called
   traces".
2. **The review tool has five sections.** Intents | Product | ADRs | Memory | Agent decisions,
   replacing the one "Memory and ADRs" section.
   - **ADRs** — the ADRs a person records with `/adr`, waiting for a person.
   - **Memory** — the memory that exists: mostly Garura memory inside the project, and once an
     issue is picked, that issue's short-term memory; the memory updates waiting for a person
     live here. It has a plain-words search, **Ask memory**, over all three tiers. Underneath
     it is the same memory tool, vectorless, the way Claude Code finds things; only the
     interface is plain words. Mocked only for now.
   - **Agent decisions** — every decision an agent made, with its trace. Named "Agent
     decisions" because "evidence" already names a play's run records.
   Kapil, 18–19 Oct: "intents - product - adr(s) -> these are the adrs that a human puts, using
   /adr - memory -> this is list of memories that exist.. omstly garura memory inside the
   projecdt, and once an issue is selected then its STM. we woudl need a separate search
   interface that works like NLP ... then the agent adrs - we call this evidence, aka
   agent-decisions"; "the tool withing garua is how claude code works. the tool we are building
   which will got into griffin will use nlp, but it will use vectorless search. the same tool
   under both, just that the interface for tool should be nlp ... you can design the interface
   and create some mocks for now. no need to build this whole this now".

## Why now

#659 built both, and its review (PR #676) found the accepted ADRs behind them. ADR 035 §6 says
a decision names "the tier, the file and the lines it rests on" — one source — while the memory
tool's contract version 4 records a trace of steps, with the text, the version and the lines
around. ADR 032 §3 (as amended by ADR 035 and ADR 036), ADR 035 §7 and ADR 036 §7 say the review
tool's third section is "Memory and ADRs", while the review tool's design and mockup now have
five sections. The memory rule's new section ("Every Decision Names Its Memory") goes to Phoenix
memory when #659 lands, so the decision it rests on must be recorded first. Kapil, on the
review: "fix all the items first".

## Options considered

- **Keep one source per decision (ADR 035 §6 as written).** Lost: one or two lines leave no
  context, and a decision rests on several things (Kapil, 19 Oct).
- **Keep the source as file and lines only, without the text around it.** Lost: the person must
  see the lines in their place, with the used part marked, to judge a step.
- **Keep one "Memory and ADRs" section (ADR 036 §7).** Lost: a person's ADRs, the memory that
  exists, and the agents' decisions are three different things to review; Kapil split them.
- **Call the agents' decisions "evidence".** Lost: "evidence" already names a play's run
  records.
- **A search index (vectors) behind Ask memory.** Lost: one memory tool, vectorless, as ADR 035
  §4 decided; only the interface is plain words.

## Decided by

Kapil (the owner), 18 and 19 October 2026.

## Decided in

#659 (every decision names its memory), PR #676 and its review; the #659 plan log
(`.garura/project/issues/659/specs/plan.md`); the review tool's design
(`.garura/project/issues/617/specs/review-tool.md`).
