# Intent

> **Scope**: Garura Methodology
> **Status**: Active
> **Last Updated**: 2026-10-05
> **Used by**: [IDD](./intent-driven-development.md) (the principles), [IDSD](./idsd.md) (the dual-intent system), [Garura](./garura-reference-implementation.md) (the reference implementation)

Intent is the one idea everything else in this framework is built on. IDD gives the principles for working from intent, IDSD keeps two intents true across the lifecycle, and Garura runs it. This document says only what an intent is: the decisions it lets an agent make, how it differs from a spec, and what one looks like.

## What an Intent Is

An intent states **why** the work exists and **what outcome** it must reach, in business language, at a level above any specification. It never says how. Because it says nothing about implementation, it stays stable when requirements, tools, or code change; only what is generated from it adapts.

Every well-formed intent has exactly three elements:

| Element | What it captures | Why only a human can write it |
|---------|------------------|-------------------------------|
| **Intent** (the goal) | The positive space: the outcome we want | It is the root input; everything else derives from it |
| **Constraints** | The boundaries the solution must respect | Business decisions, compliance, risk tolerance |
| **Failure conditions** | The halt signals: when to stop | Risk appetite is a human judgment; an agent cannot infer when "enough is enough" |

Success is not a fourth element. Success scenarios are *generated* from the intent and its context, then approved by a human (the Expectation layer of [ICE](./idsd.md#ice-the-idsd-model)). Writing them into the intent by hand would do the specifier's work for it, which is the spec-driven pattern this framework rejects.

## The Decision Space

An intent is the smallest thing an agent needs to decide its next step without asking. With the three elements it can answer four questions:

| Question | Answered from | Answer |
|----------|---------------|--------|
| Am I moving toward the goal? | The goal | Continue |
| Am I within the constraints? | The constraints | Continue |
| Have I reached success? | The success scenarios generated from the goal | Stop when they hold |
| Have I tripped a failure condition? | The failure conditions | Halt |

Under compartmented evaluation, the builder sees the goal and constraints, while a separate validator holds the failure conditions and the success checks ([IDD Principle 4](./idd-principles.md#principle-4-builders-and-validators-must-not-share-context)).

**Quality test.** If you cannot tell from the intent whether it has been achieved, the intent is poorly formed. Fix it upstream by sharpening the intent, not downstream by bolting on success criteria.

## Intent Is Not a Spec

| | Specification | Intent |
|---|---------------|--------|
| **Says** | How to build it: APIs, schemas, files | Why, and what outcome |
| **Language** | Technical | Business |
| **Stability** | Changes with every requirement shift | Survives requirement and implementation changes |
| **Who writes it** | A human writes and maintains it | A human writes it; the system generates the spec from it |
| **Size** | Often hundreds of lines | Three short elements |

In spec-driven work the spec is the input a human writes. In intent-driven work the spec is an intermediate the system generates from intent and memory. The information is the same; who owns it is not.

## Examples

**A spec** (implementation-level, brittle):

```
Build a REST endpoint at /api/users with GET/POST methods.
Validate email with regex pattern X.
Return 201 on success with JSON body { id, email, created_at }.
Use PostgreSQL schema: users(id UUID PK, email VARCHAR(255) UNIQUE, ...).
File: src/controllers/userController.ts
```

**The same work as an intent** (outcome-level, stable):

```
Intent:             Users can register and manage their profiles.
Constraints:        Must support SSO. Must comply with GDPR. Must work with the existing identity provider.
Failure conditions: Registration fails silently. PII is logged to stdout. User data persists after a deletion request.
```

**An intent about how the work is done** has the same shape. This is the kind IDSD calls SDLC intent:

```
Intent:             Build one ready epic to done, test-first.
Constraints:        The builder never sees the evals.
Failure conditions: Done is claimed while a check is red.
```

The first kind says what to build; the second says how a step of the lifecycle operates. Keeping the two apart is what [IDSD](./idsd.md#the-dual-intent-system) is about.

## Related Documentation

- [IDSD](./idsd.md): the dual-intent system, ICE, and the loop that keeps intent true
- [IDD](./intent-driven-development.md): the eight principles, and PCAM, the design of the tool that drives ICE
- [Garura](./garura-reference-implementation.md): where each intent lives in the reference implementation

---

**Author**: Kapil Viren Ahuja
**Version**: 1.0.0
**Last Updated**: 2026-10-05
**Status**: Active
