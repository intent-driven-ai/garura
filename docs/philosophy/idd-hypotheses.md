# IDD Hypotheses

> **Scope**: Garura Methodology
> **Status**: Active
> **Last Updated**: 2026-10-07
> **Part of**: [IDD](./intent-driven-development.md) — the bets IDD makes

IDD rests on three testable hypotheses. These are not proven — they are the bets the paradigm makes. If any is falsified, the paradigm must adapt.

## H1: Memory-Driven Intent Self-Generation

**Hypothesis**: A system that accumulates enough structured intent→outcome pairs in LTM can eventually generate well-formed intents from observed production patterns, reducing human involvement from "author all intents" to "approve or refine generated intents."

**Preconditions**: Rich LTM with contextual metadata. Production monitoring integration. Pattern correlation capability. Well-defined governance for generated vs human-authored intents.

**Current state**: The accumulation mechanism (STM→LTM promotion) is designed. The generation mechanism is not. This hypothesis cannot be tested until steps 1-3 of the [memory path to intent self-generation](./intent-driven-development.md#memory-as-foundation-for-intent-self-generation) are operational and producing a critical mass of intent→outcome data.

**Falsification signal**: If systems with rich LTM consistently generate intents that humans reject >80% of the time, the hypothesis is falsified — memory accumulation does not lead to generation capability.

## H2: Hypothesis Layer Above Intents

**Hypothesis**: There exists a useful abstraction above intents — a "purpose" or "hypothesis" layer that connects business hypotheses to the intents that test them. Example: "We hypothesize that adding social login will increase registration by 30%" → generates intents for implementation, measurement, and evaluation.

**Why it matters**: Intents describe WHAT to build. Hypotheses describe WHY to build it. If the system can track hypothesis→intent→outcome chains, it can learn which types of business bets succeed and which fail — informing future hypothesis generation.

**Current state**: Not designed. Conceptual only. IDD currently treats intent as the highest abstraction layer. Whether a hypothesis layer adds genuine value or unnecessary ceremony is an open question.

**Falsification signal**: If adding a hypothesis layer increases authorship burden without improving intent quality or outcome prediction, the abstraction is not useful.

## H3: Cross-Domain Applicability

**Hypothesis**: The IDD paradigm — intent triples, constraints vs failure conditions, compartmented evaluation, memory architecture — applies beyond software development. Initial domains: UX design, supply chain management, agentic system design.

**Current state**: Preliminary exploration in UX contexts shows the intent triple (goal + constraints + failure conditions) transfers naturally. Failure conditions for UX are harder to make binary and observable (P3 challenge). No exploration in other domains.

**Falsification signal**: If adapting IDD to a non-software domain requires modifying more than 2 of the [8 principles](./idd-principles.md), the paradigm is software-specific, not universal.

---

## Related Documentation

- [IDD](./intent-driven-development.md): the paradigm these hypotheses underpin
- [IDD design principles](./idd-principles.md): the principles H3 tests for portability

---

**Author**: Kapil Viren Ahuja
**Version**: 1.0.0
**Last Updated**: 2026-10-07
**Status**: Active
