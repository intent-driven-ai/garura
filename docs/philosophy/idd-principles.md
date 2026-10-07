# IDD Design Principles

> **Scope**: Garura Methodology
> **Status**: Active
> **Last Updated**: 2026-10-07
> **Part of**: [IDD](./intent-driven-development.md) — the eight principles

Governing principles for Intent-Driven Development. Every new intent, play, agent, and skill in any IDD-based system must be evaluated against these principles. If a design violates a principle, it must either be redesigned or the violation must be recorded with explicit rationale.

IDD sits in a narrow band between two failure modes: over-specification (which recreates SDD) and under-specification (which produces non-deterministic prompting). These principles keep systems in that band.

---

## Principle 1: Intents Declare Outcomes, Not Instructions

An intent must describe **what success looks like**, never **how to get there**. The moment an intent prescribes implementation steps, it has become a spec.

**Test:** Can the intent be satisfied by two completely different implementations? If yes, it's an intent. If only one implementation path can satisfy it, it's a spec in disguise.

**Good:**
```
Goal: All API endpoints return consistent error responses
Constraints: Must use existing error codes; must not break current clients
Failure: Any endpoint returns an unstructured error body; any 5xx leaks stack traces
```

**Bad:**
```
Goal: Wrap all controllers with ErrorHandlerMiddleware that catches exceptions and maps them to RFC 7807 responses using the ErrorMapper class
```

The bad example has already made the design decision. There is nothing left for the agent to decide, which defeats the purpose of having agents as autonomous decision-makers.

**Why this matters:** Agents exist to make domain-specific decisions about *how*. If the intent already answers *how*, the agent becomes a typist, not a judge. You lose the adaptive execution that makes IDD superior to SDD.

### Corollary: The Agent Must Be Able to Say No

An intent must leave enough decision space that an agent can legitimately reject an approach or request clarification. In the space defined by the goal, bounded by constraints, and guarded by failure conditions — the agent must have at least two meaningfully different approaches available. If not, the intent is over-constrained.

If agents are just executors, you don't need agents — you need scripts. The entire value proposition of IDD over SDD is that intelligent agents make contextual decisions within bounded problem spaces. Protect that decision space.

### Corollary: Intents Don't Know About Tools

An intent must never reference specific tools, CLIs, MCPs, or APIs. The intent declares what should happen; the agent decides how; the skill knows the tool.

**Test:** If you swapped the entire toolchain (GitHub to GitLab, npm to yarn, Jest to Vitest), would the intent still be valid without any changes? If not, it contains tool coupling.

Intents are stable across toolchain changes. Skills change when tools change. Agents decide which skills to use. If the intent names the tool, this entire abstraction collapses.

---

## Principle 2: Constraints Are Boundaries, Not Preferences

Constraints define the walls of the solution space. Crossing a constraint is always a failure. If crossing it is sometimes acceptable, it is a preference, not a constraint, and it belongs in LTM as a practice — not in the intent.

**Test:** If the system violates this constraint, do you reject the output unconditionally? If the answer is "it depends," it's not a constraint.

**Examples of real constraints:**
- Must not introduce new runtime dependencies
- Must maintain backward compatibility with API v2 clients
- Must not modify files outside the `src/` directory
- Response time must not exceed current p99 by more than 10%

**Examples of preferences masquerading as constraints:**
- Should use TypeScript (preference — what if the project is Java?)
- Should have test coverage above 80% (practice, belongs in LTM quality gates)
- Should follow clean architecture (standard, belongs in LTM practices)

**The trap this prevents:** Constraint lists that grow to 15+ items per intent. When everything is a constraint, nothing is. Agents cannot distinguish real boundaries from nice-to-haves, and the system drifts toward SDD's worst failure mode — an interconnected web of requirements where missing one cascades.

**Relationship to P4 (Compartmented Evaluation):** The Constraint-Failure Classification Rule (P4) provides a precise test for whether something belongs in constraints or failure conditions. If a requirement shapes the builder's design choices, it is a constraint. If it can only be evaluated after the output exists, it is a failure condition. Constraints that fail this test — requirements the builder doesn't need to make design decisions — should be reclassified as failure conditions. This prevents constraint lists from growing unbounded while ensuring the builder has every piece of information it genuinely needs.

---

## Principle 3: Failure Conditions Must Be Observable and Binary

A failure condition must describe something that can be **detected programmatically or by inspection** and evaluated as **true or false**. Under compartmented evaluation (P4), failure conditions are **validator-only instruments** — they are routed exclusively to the validator agent and never shown to the builder. Subjective, gradient, or aspirational failure conditions are not failure conditions — they are quality preferences.

**Test:** Can a validator agent determine whether this failure condition has been triggered without asking a human for an opinion? If not, it's not a failure condition.

**Second test (P4 alignment):** Can this failure condition be evaluated from builder output alone, without knowing the goal or constraints that shaped the builder's decisions? If the validator needs to understand the builder's intent to evaluate the condition, it is not a proper failure condition — it may be a constraint in disguise.

**Observable and binary:**
- The generated code does not compile
- Tests fail or test coverage drops below the project's configured threshold
- The PR description is empty
- The commit message does not follow conventional commit format
- The API contract (OpenAPI spec) has changed without a version bump

**Not observable or not binary:**
- The code is "not clean" (subjective)
- The design is "too complex" (gradient — complex relative to what?)
- Performance is "acceptable" (unmeasured)
- The solution is "not elegant" (aesthetic judgment)

**Why this matters:** Failure conditions are the mechanism for catching bad outputs *during* execution, before they reach a checkpoint. This only works if the system can actually evaluate them. An unobservable failure condition is worse than no failure condition at all — it creates false confidence that problems will be caught.

---

## Principle 4: Builders and Validators Must Not Share Context

When an agent builds a solution and the same agent (or a peer with the same context) validates it, a fundamental conflict arises: the builder optimizes for passing the specific checks it knows about, rather than genuinely solving the problem. This is Goodhart's Law applied to agentic verification — when the measure becomes the target, it ceases to be a good measure.

The fix is an **information barrier**: the builder and validator operate with deliberately different context windows.

### How ICE routes under the barrier

The barrier is **applied proportionally, not always** — it earns its keep on judgment-heavy work (the heavy lifting of coding, where many valid outputs exist) and is skipped for mechanical, single-output tasks, which just run the validator as a plain regression check (see "When Compartmented Evaluation Applies" under Principle 4). When it is on:

Evals are the verification instrument, built by a **separate agent** that reads all of ICE and compiles them from **failure conditions + success scenarios**. Those evals are then **encrypted** — locked away from the builder, so it cannot optimize to the test.

| Who | Receives | Never receives |
|-----|----------|----------------|
| **Builder** | goal, constraints, all of Context, success scenarios; and the validator's recovery handoff plan when a fix is routed back to it | failure conditions, recovery conditions, the evals |
| **Eval author** (separate agent) | all of ICE | builder output |
| **Validator** | the implementation, the decrypted evals, Context, the recovery conditions | — |

The builder marches toward the goal, follows the constraints it knows, uses all the context it was handed, invents no context of its own, and keeps working until it has succeeded. The validator sees the implementation and validates it against the evals — evals written so that every success scenario is met and no failure condition occurs. Everything that must be tested has to live within the validator's context.

The success scenarios are the part of the spec the builder *does* see — it needs the target to know when to stop. When the barrier is on, it holds anyway, because the evals themselves and the failure conditions stay hidden and encrypted. The builder knows where the finish line is; it does not get to see the judges' scorecards.

### The Routing Table

Evals are compiled by a separate agent from failure conditions + scenarios + success, then encrypted. The builder never sees them.

| ICE element | Builder | Eval author | Validator |
|-------------|---------|-------------|-----------|
| **Goal** (Intent) | ✓ | ✓ | ✗ |
| **Constraints** (Intent) | ✓ | ✓ | ✗ |
| **Failure conditions** (Intent) | ✗ | ✓ | via evals |
| **Context** | ✓ (all) | ✓ | ✓ |
| **Success scenarios** (Expectation) | ✓ | ✓ | via evals |
| **Recovery** (Expectation) | only the resulting handoff plan | — | ✓ (builds the recovery handoff plan) |
| **Encrypted evals** | ✗ never | produces | ✓ (decrypts) |
| **Implementation** | produces | ✗ | ✓ |

The builder works from **goal + constraints + all of Context + success scenarios** — it knows what to achieve, the boundaries, the surround, and the finish line, but not the evals or the failure conditions.

The validator works from **the implementation + the decrypted evals + Context + the recovery conditions** — the evals encode every scenario, success, and failure condition, so it checks against them without needing the raw Intent, and the recovery conditions let it turn failures into a directional recovery handoff plan that either loops back to the builder for an autonomous fix or escalates to a human. Everything that must be tested has to live within the validator's context.

When the barrier is on, it holds because the **evals are encrypted and the failure conditions stay hidden from the builder** — the builder cannot teach to a test it cannot see, even though it knows the success target it is aiming at.

### The Constraint-Failure Classification Rule

The partition between constraints and failure conditions is not arbitrary — it follows a single decision rule:

> **"Would knowing this change how the builder writes code? Yes → constraint. No → failure condition."**

If a requirement shapes the builder's design choices (API compatibility, dependency restrictions, performance budgets), it is a **constraint** — the builder needs it to make good decisions. If a requirement can only be evaluated after the output exists (compilation success, test coverage, security scan results), it is a **failure condition** — giving it to the builder only invites teaching-to-the-test.

| Requirement | Classification | Reasoning |
|-------------|---------------|-----------|
| "Must not introduce new runtime dependencies" | Constraint | Shapes which libraries the builder considers |
| "Must maintain backward compatibility with API v2" | Constraint | Shapes interface design decisions |
| "Response time must not exceed current p99 by more than 10%" | Constraint | Shapes algorithmic and architectural choices |
| "The generated code must compile" | Failure condition | Builder should try to write compilable code regardless — knowing this is a check doesn't help |
| "Test coverage must not drop below threshold" | Failure condition | Evaluable only after code exists; giving it to builder invites coverage gaming |
| "No secrets in source code" | Failure condition | Binary check on output; builder should follow secure coding practices from LTM |
| "PR description must not be empty" | Failure condition | Evaluable only from output artifact |
| "Must not modify files outside src/" | Constraint | Directly shapes which files the builder touches |

**Misclassification is always worse in one direction:** Putting a failure condition into constraints drowns the builder in prescriptive rules and reduces its decision space (drift toward SDD). Putting a constraint into failure conditions deprives the builder of information it needs to make good design decisions. When in doubt, ask: "Does the builder need this to make a *design choice*, or is it something we check *after the fact*?"

### Symptom-Based Feedback Protocol

When the validator finds issues, it reports **symptoms**, not **condition IDs**.

**Correct (symptom-based):**
```
"The output contains a hardcoded database connection string at line 47."
"The function processBatch() does not handle the case where the input array is empty."
"Two API endpoints return different error response formats."
```

**Incorrect (condition-based):**
```
"Failed check FC-3: No secrets in source code."
"Violation of failure condition #2: test coverage below threshold."
"FC-7 triggered: API contract changed without version bump."
```

Symptom-based feedback tells the builder *what the output does wrong* without revealing *which specific condition was violated*. This preserves the barrier: the builder fixes the actual problem rather than reverse-engineering which check to pass.

### Convergence Protocol

The builder-validator loop must converge. Unbounded iteration is both wasteful and a signal that the intent is poorly formed.

| Parameter | Default | Rationale |
|-----------|---------|-----------|
| **Max iterations** | 3 | If 3 cycles don't converge, the problem is upstream |
| **Escalation trigger** | 3 failures on same symptom | Repeating symptom = structural misunderstanding, not fixable by iteration |
| **Escalation action** | Drop barrier; present full intent to human | Human sees everything and makes the judgment call |
| **Hard ceiling** | 5 iterations | Absolute maximum before mandatory human intervention |

**Escalation drops the barrier**: When the system escalates to a human, the human receives the complete intent (goal + constraints + failure conditions), all builder outputs, and all validator feedback. The information barrier exists for agents, not for humans.

### When Compartmented Evaluation Applies

The barrier adds value when the builder must make **judgment calls** — creative, architectural, or design decisions where knowing the test criteria could bias the approach. It adds no value for **mechanical operations** where the output is deterministic.

| Intent Type | Barrier? | Reasoning |
|-------------|----------|-----------|
| Build a feature from intent | ✓ Yes | Builder makes design decisions; knowing failure checks would bias them |
| Fix a bug from RCA | ✓ Yes | Builder chooses a fix strategy; knowing validator checks would narrow exploration |
| Design a technical architecture | ✓ Yes | Designer makes structural decisions that should not be test-shaped |
| Commit code | ✗ No | Mechanical operation — no judgment calls, deterministic output |
| Create a branch | ✗ No | Mechanical — deterministic |
| Generate documentation from code | ✗ No | Descriptive, not creative — output is determined by input |
| Run a security audit | ✗ No | Audit IS validation — the agent is already in the validator role |

**Rule of thumb:** If the intent's goal can be satisfied by only one possible output, the barrier adds overhead without benefit. If multiple valid outputs exist and the builder must choose among them, the barrier prevents the builder from optimizing for the validator's specific checks rather than the actual goal.

**Why this matters:** Without compartmented evaluation, every generation-verification loop in IDD is vulnerable to Goodhart's Law. The builder doesn't need to be "trying" to game the checks — LLMs naturally pattern-match toward satisfying visible criteria. The information barrier ensures that the builder optimizes for the *goal* (which it can see) while the validator independently evaluates against *failure conditions* (which only it can see). This is the same principle as separation of duties in financial controls and monitor-command in safety-critical systems, adapted for AI agent verification.

---

## Principle 5: Each Intent Is Self-Contained; Cross-Cutting Concerns Live in LTM

An intent must not depend on another intent's internal state. If two intents need to share knowledge, that knowledge belongs in LTM (practices, standards, quality gates) or STM (issue-specific artifacts), not in the intent itself.

**Test:** Can this intent execute correctly if every other intent in the system is deleted? If not, you have a hidden dependency.

**Correct separation:**
```
LTM (practices/logging.md):     "All services use structured JSON logging via the project logger"
LTM (quality-gates/security.md): "No secrets in source; all credentials via environment variables"

Intent (for a new endpoint):
  Goal: Add a /users/export endpoint that returns CSV
  Constraints: Must authenticate via existing auth middleware
  Failure: Endpoint accessible without valid token; response not valid CSV
```

The logging and security concerns are not in the intent. They are in LTM, where they apply to all work implicitly. The intent focuses only on what is unique to this specific piece of work.

**The trap this prevents:** LTM bloat. When cross-cutting concerns accumulate in LTM unchecked, LTM becomes a shadow spec. Guard against this by applying the same discipline to LTM entries: each practice must be independently valuable, not dependent on other practices to make sense.

**LTM hygiene rule:** If LTM exceeds 20 practice files, audit for overlap, contradiction, and redundancy. Merge or remove entries. LTM should grow logarithmically with project complexity, not linearly.

---

## Principle 6: Intents Scale Horizontally, Not Vertically

When a goal is too large for a single execution step, the answer is to decompose into multiple intents — not to make the intent more detailed. Vertical scaling (adding more detail to one intent) recreates SDD. Horizontal scaling (more intents, each small and focused) preserves IDD.

**Test:** Can the goal of this intent be expressed in one sentence without conjunctions? If you need "and" to describe the goal, it's likely two intents.

**Horizontal (correct):**
```
Intent 1: Goal — Identify the root cause of the payment timeout
Intent 2: Goal — Design a fix that addresses the root cause
Intent 3: Goal — Implement the designed fix
Intent 4: Goal — Validate the fix resolves the original issue
```

**Vertical (drift toward SDD):**
```
Intent: Goal — Identify the root cause of the payment timeout, design a fix considering database connection pooling and retry logic, implement the fix using the circuit breaker pattern, and validate it resolves timeouts under load
```

The vertical version has made design decisions (connection pooling, circuit breaker) before any agent has analyzed anything. It has also chained four activities into one, making the checkpoint model meaningless.

---

## Principle 7: Verify Understanding Before Execution

Before an agent begins work on an intent, it must be able to restate the goal, constraints, and failure conditions in the context of the current codebase. If the agent's restatement reveals ambiguity, the system must checkpoint for clarification — not guess.

**Test:** Could two reasonable agents interpret this intent differently given the same codebase? If yes, the intent is ambiguous and must either be tightened or force a verification checkpoint.

**What verification looks like:**
```
Intent received:
  Goal: Refactor the payment module for better testability
  Constraints: Must not change public API signatures
  Failure: Any existing test fails after refactoring

Agent restatement (before work begins):
  "The payment module (src/payments/) has 3 classes with direct database calls
   in constructor methods, making unit testing impossible without a live DB.
   I will extract dependencies to allow injection. Public method signatures
   on PaymentService, RefundHandler, and InvoiceGenerator will not change.
   I will verify by running the existing 47 tests in payments.test.ts."
```

The restatement converts the abstract intent into a concrete plan anchored to real code. If the agent cannot produce this restatement, it doesn't understand the intent well enough to proceed.

**Barrier-aware restatement (when P4 applies):**

The builder's restatement must confirm it is working from goal + constraints only:
```
Builder restatement:
  "Working from: goal (refactor payment module for testability)
   + constraints (must not change public API signatures).
   I do not have visibility into failure conditions.
   My approach: extract dependencies to allow injection in 3 classes."
```

The validator's restatement must confirm it is working from failure conditions + builder output only:
```
Validator restatement:
  "Evaluating against: failure conditions for payment module refactoring.
   I have the builder's output (modified src/payments/ files).
   I do not have visibility into the original goal or constraints.
   My evaluation: run existing test suite, check for API signature changes."
```

These restatements serve as runtime verification that the information barrier is intact. If either agent's restatement references information it should not have, the barrier has been compromised.

**Why this matters:** "Clearly understood" is the most dangerous phrase in IDD. An LLM can pattern-match to something close enough and proceed with confidence down the wrong path. Forced restatement surfaces misunderstandings *before* work begins, when correction is free — not after three agent calls, when it's expensive.

**When to skip:** Intents with purely mechanical goals (commit code, create branch, open PR) where the action is unambiguous. The verification principle applies to intents where the agent must make judgment calls about *what* the codebase needs.

---

## Principle 8: Feedback Is Continuous, Failure Is Cheap

Design intents so that failures are detected as early as possible, checkpoints are meaningful, and intent health is measured over time. This principle unifies three concerns: fail-fast design, checkpoint justification, and outcome measurement.

### Fail-Fast

Front-load risky decisions. Put analysis before design, design before build. Make the first intent in any chain produce a verifiable artifact that a human can validate before expensive work begins.

**Test:** If this intent fails, how many subsequent steps have already executed? If more than zero, consider whether the failure condition could have been checked earlier.

### Justify Every Checkpoint

The checkpoint is where human judgment enters the system. An intent that always auto-approves is either too trivial to be an intent or has failure conditions that are too lenient. An intent that never auto-approves has constraints that are too tight or failure conditions that can't be evaluated programmatically.

**Test:** Over time, does this intent's checkpoint get approved ~70-90% of the time? If it's 100%, the checkpoint is a rubber stamp. If it's under 50%, the intent is poorly defined.

### Measure Intent Health

A successful outcome (code shipped, PR merged) does not mean the intent was well-designed. Track these signals per intent over time:

| Signal | Healthy | Unhealthy | What It Means |
|--------|---------|-----------|---------------|
| Checkpoint approval rate | 70-90% | <50% or 100% | Intent clarity or checkpoint value |
| Agent skill selection variance | 2-4 different skill paths | Always the same path | Intent is too prescriptive or agent is stuck |
| Constraint violation frequency | Rare | Frequent | Constraints unclear or contradictory |
| Failure condition trigger rate | Occasional | Never triggered | Failure conditions may be too lenient |
| Downstream rework | Rare | Frequent rejections in later steps | Early intents not catching problems |
| LTM dependency count | 0-3 practices referenced | 10+ practices needed | Intent is underspecified, leaning on LTM as a crutch |
| Builder-validator alignment rate | >80% converge within 2 iterations | <50% require 3+ iterations | Barrier partition quality or intent clarity |
| Rework cycles per intent | 1-2 cycles | 3+ cycles | Intent may be ambiguous or barrier may be misconfigured |

**Why this matters:** IDD's advantage over SDD is adaptability. But adaptability without feedback is drift. These signals tell you whether your intents are staying in the productive middle ground or drifting toward either over-specification or chaos.

---

## Related Documentation

- [IDD](./intent-driven-development.md): the paradigm, and PCAM, the design of the tool that drives ICE
- [Intent](./intent.md): what an intent is, and the decision space it gives an agent
- [Anti-patterns](./idd-anti-patterns.md): how IDD fails when these principles are broken
- [Decision checklist](./idd-decision-checklist.md): the principles as checks to run before adding an intent

---

**Author**: Kapil Viren Ahuja
**Version**: 1.0.0
**Last Updated**: 2026-10-07
**Status**: Active
