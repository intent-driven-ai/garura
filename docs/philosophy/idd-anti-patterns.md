# IDD Anti-Patterns

> **Scope**: Garura Methodology
> **Status**: Active
> **Last Updated**: 2026-10-07
> **Part of**: [IDD](./intent-driven-development.md) — how IDD fails

Each anti-pattern below is a way an intent-driven system drifts out of the band the [eight principles](./idd-principles.md) keep it in: toward spec-driven over-specification, or toward unstructured prompting. Each one names the symptom you will see first.

---

## Anti-Pattern 1: The Spec Intent
An intent that is so detailed it leaves no decision space for the agent. Usually has 10+ constraints, prescribes implementation patterns, and has failure conditions that implicitly define the solution.

**Symptom:** Agents always produce identical outputs regardless of context.

## Anti-Pattern 2: The Wish Intent
An intent with a vague goal ("make it better"), no real constraints, and subjective failure conditions. The agent has unlimited decision space but no way to know when it's done.

**Symptom:** Checkpoints always require human intervention because the agent can't self-evaluate.

## Anti-Pattern 3: The Leaky Intent
An intent that works only because of implicit knowledge not captured in the intent, constraints, failure conditions, or LTM. The agent produces correct output because the LLM has seen similar patterns, not because the intent is well-defined.

**Symptom:** Works with one LLM provider, breaks when you switch models or versions.

## Anti-Pattern 4: The Shadow Spec (LTM Bloat)
Cross-cutting concerns, standards, and practices accumulate in LTM until the combined weight of LTM + intent effectively recreates a full specification document. Individual intents look clean, but they're only interpretable in the context of dozens of LTM files.

**Symptom:** Onboarding a new project requires reading all of LTM before any intent makes sense.

## Anti-Pattern 5: The Chain Lock
A composed workflow where each step's success depends on the previous step producing output in a very specific format. The intents are nominally independent, but practically they form a rigid pipeline where changing one breaks the chain.

**Symptom:** Modifying one step requires updating every downstream step in the chain.

## Anti-Pattern 6: The Barrier Leak
The builder has access to failure conditions — either because they were embedded in the goal text, because the validator's feedback included condition identifiers instead of symptoms, or because the same agent plays both roles. The builder optimizes for passing specific checks rather than solving the actual problem.

**Symptom:** Builder outputs pass all failure conditions but miss the actual intent. Code that technically satisfies every check but doesn't solve the real problem. Validator feedback includes phrases like "FC-3 violated" instead of describing what the output does wrong.

## Anti-Pattern 7: The Constraint Overload
Failure conditions have been misclassified as constraints, drowning the builder in prescriptive rules that reduce its decision space to near-zero. The intent looks like it has many constraints and few failure conditions, but most "constraints" are actually output-evaluation criteria that the builder doesn't need for design decisions.

**Symptom:** Constraint list exceeds 8+ items per intent. Builder always produces nearly identical outputs regardless of context. Removing half the "constraints" wouldn't change the builder's approach — they were evaluation criteria, not design-shaping boundaries.

---

## Related Documentation

- [IDD](./intent-driven-development.md): the paradigm
- [IDD design principles](./idd-principles.md): the principles each anti-pattern breaks
- [Decision checklist](./idd-decision-checklist.md): the checks that catch these before an intent is added

---

**Author**: Kapil Viren Ahuja
**Version**: 1.0.0
**Last Updated**: 2026-10-07
**Status**: Active
