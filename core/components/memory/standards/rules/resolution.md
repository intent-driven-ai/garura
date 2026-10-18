# Resolution Protocol

The standard that all participating agents follow when `ltm_context` is
present in their input contract. Defines the four-step resolution order,
authority semantics, trace output requirements, and exemptions.

Referenced by: tech-designer, feature-steward, repo-orchestrator

## Overview

When an agent receives a contract containing `ltm_context`, it resolves
domain questions against a three-layer hierarchy before falling back to
general reasoning. The four steps are:

- **R1** — Identify decision domains
- **R2** — Query project-scoped knowledge (project_base)
- **R3** — Query core-scoped knowledge (core_base)
- **R4** — Flag LLM fallback

If `ltm_context` is absent, the agent skips this entire section and
operates exactly as it did before this protocol existed (INV3).

## R1 — Identify Decision Domains

From the task intent and `ltm_context.query_domains`, determine the
relevant knowledge categories for this invocation.

- Use `query_domains` as the primary domain list
- Supplement with domain categories implied by the task intent
- Produce a list of domain topics that will be checked in R2 and R3

## R2 — Query Project-Scoped Knowledge

For each domain topic from R1, search `ltm_context.project_base` for
matching knowledge files.

**Discovery method:** Read `search_patterns` metadata from candidate files.
Match patterns against the domain topic. This is a keyword/string comparison
only — no LLM calls, no semantic similarity (INV1).

**Authority semantics:**

| Condition | Meaning | Behavior |
|-----------|---------|----------|
| File does not exist | Layer has no opinion | Descend to next layer |
| File exists, no matching section | Layer has no opinion on this topic | Descend to next layer |
| File exists, matching section, DRAFT | Advisory opinion | Use as input, flag `authority: draft`, descend for confirmation |
| File exists, matching section, LOCKED | Authoritative opinion | Use this. Record `authority: locked`. Do NOT descend further. |

**LOCKED determination:** A file is LOCKED when its filename appears in
`ltm_context.locked_artifacts`. All other project-scoped files are DRAFT.

**Conflict:** When a LOCKED and a DRAFT artifact both answer the same domain
question, the LOCKED artifact wins unconditionally. Record override in trace.

## R3 — Query Core-Scoped Knowledge

For domain topics not resolved (or only DRAFT-resolved) in R2, search
`ltm_context.core_base` for matching knowledge files.

**Discovery method:** Check `{core_base}/_index.md` for category listings.
Read `search_patterns` headers from candidate files in matching categories.
Same keyword/string comparison as R2 (INV1).

**Authority semantics:** All core-scoped files are advisory. Record
`resolved_from: "core"`, `authority: "draft"`.

**Project-over-core:** When both R2 (DRAFT) and R3 both answer the same
domain question, the project-scoped (R2) answer is used (INV5).

## R4 — Flag LLM Fallback

For domain topics that produced no answer from R2 or R3, the agent proceeds
with general reasoning and records `resolved_from: "llm"` in the trace.

LLM fallback entries are primary candidates for the `learn` play. Each
fallback is a knowledge gap: the organization lacks persistent knowledge for
this domain question and relies on general reasoning instead.

## Resolution Trace Output

After completing R1-R4, write the resolution trace to STM:

Path: `{stm_base}/{issue}/evidence/{play}/resolution-trace.yaml`

```yaml
resolution_trace:
  - decision: "string — the domain question that was resolved"
    resolved_from: "project | core | llm"
    source: "relative file path, or null if llm"
    section: "section name within the source file, or null"
    authority: "locked | draft | none"
    value: "brief summary of the resolved decision value"
```

Return the path to this file as `resolution_trace_path` in the output
contract's `stm.output` block (per DD10 in tech.yaml).

## Decision Records (ADR 035 §6)

Every decision an agent makes keeps its trace: the steps the agent took, in order. Each step
says what the agent looked for, what it found, and the memory lines that said so — a tier
(short-term, Garura or Phoenix memory), a file, the lines, and the fingerprint of that text. A
sign-in decision, for example, reads the product's profile (who the users are, the surfaces),
then the domain that covers sign-in, then the profile's security level and compliance regimes,
then the knowledge lines those values select. When the answer came from a memory update a
person approved, the update's written file is the source of a step.

The record is made through the memory tool's `cite`: the question, the answer, who decided, the
play, and the trace. The tool reads every source before it records anything, and keeps the
exact text, the version of memory, and the lines around it, so a person sees each step in its
place. `citations --check` reads every step's source again: a decision with no trace, or a step
whose source is gone or changed, is flagged by its step. A drive's review shows these records.

The shape is the memory tool's contract (`cite`, `citations`, version 4). The trace above (R1–R4),
and R4's model fallback, become this trace when the agents move onto the tool (#663).

## Context Isolation Exemptions

The following agents NEVER receive `ltm_context` from any workflow. No
play populates this field for them under any circumstances (INV4):

- **evals-engineer** — Must not see implementation code or prior outputs
- **judge** — Receives only encrypted evals and the codebase

Any play that attempts to pass `ltm_context` to either agent must be
treated as a defect.

## Backward Compatibility

When `ltm_context` is absent from the input contract:
- Skip this entire section
- No trace is produced
- Agent behavior is identical to pre-protocol operation
- No errors, no warnings, no degradation (INV3)

## Staleness Handling

When a file used in R2 or R3 has a `last_validated` field that exceeds
its `staleness_window`, add a `stale: true` flag to that resolution trace
entry. Stale files remain usable — the flag is a signal, not a rejection.
