# IDD Decision Checklist: Before Adding a New Intent

> **Scope**: Garura Methodology
> **Status**: Active
> **Last Updated**: 2026-10-07
> **Part of**: [IDD](./intent-driven-development.md) — the principles as checks

Run this checklist when you design a new intent-based workflow, or change an existing one. Each check turns one of the [eight IDD principles](./idd-principles.md) into a question you can answer before any work runs. A check that fails is cheap to fix now and expensive to fix after the agents have built on it.

The fourteen checks fall into five groups: the goal, the constraints, the failure conditions, the shape of the intent, and the feedback around it.

## Quick Reference

| # | Question | Principle | Pass Condition |
|---|----------|-----------|----------------|
| 1 | Does the goal describe an outcome, not an implementation? | P1 | Two different implementations could satisfy it |
| 2 | Does the agent have meaningful choices to make? | P1 | At least two valid approaches exist |
| 3 | Is the intent free of tool/technology references? | P1 | Survives a complete toolchain swap |
| 4 | Is every constraint a hard boundary you'd reject on? | P2 | No "should" or "prefer" language |
| 5 | Can every failure condition be evaluated without human opinion? | P3 | A validator agent can check it |
| 6 | Is every constraint something the builder needs to make design choices? | P4 | Passes the Classification Rule: "Would knowing this change how the builder writes code?" |
| 7 | Are failure conditions evaluable from builder output alone? | P4 | Validator can check without knowing goal or constraints |
| 8 | Is validator feedback symptom-based, not condition-based? | P4 | Feedback describes what output does wrong, not which condition ID failed |
| 9 | Does the intent work without knowledge of other intents? | P5 | Delete all other intents — does this one still make sense? |
| 10 | Can you state the goal in one sentence without "and"? | P6 | If not, decompose into multiple intents |
| 11 | Can the agent restate this intent in concrete codebase terms? | P7 | Restatement surfaces no ambiguity or forces clarification |
| 12 | Is this the earliest point this failure could be detected? | P8 | No cheaper place to catch this error |
| 13 | Will the checkpoint add value (not rubber stamp)? | P8 | Expected approval rate 70-90% |
| 14 | Can you measure this intent's health over time? | P8 | At least 3 signals from the health table are trackable |

---

## The Goal (P1)

### 1. Does the goal describe an outcome, not an implementation?

The goal says what must be true when the work is done. It never says how to get there. Once a goal names a class, a pattern or a file, it has already made the design decision, and the agent has nothing left to decide.

**How to check:** Imagine two engineers solving it in two different ways. If both solutions would satisfy the goal, it is an outcome. If only one would, it is a spec written as a goal.

**If it fails:** Remove the "how" from the goal. If that "how" is a real limit, move it to the constraints. If it is a team habit, move it to LTM.

### 2. Does the agent have meaningful choices to make?

An agent is only worth running when it has a real choice to make. If only one approach fits inside the goal, the constraints and the failure conditions, a script would do the same job for less. That is the [corollary to P1](./idd-principles.md#corollary-the-agent-must-be-able-to-say-no): the agent must be able to say no.

**How to check:** Name at least two different approaches that would both pass. If you can name only one, the intent is over-constrained.

**If it fails:** Look for constraints that are really preferences (check 4), and for failure conditions that quietly define the solution.

### 3. Is the intent free of tool and technology references?

The intent says what should happen. The agent decides how. The skill knows the tool. If the intent names GitHub, Jest or a specific API, that layering collapses, and the intent breaks the day the toolchain changes.

**How to check:** Swap the whole toolchain in your head: GitHub to GitLab, Jest to Vitest, npm to yarn. If any word of the intent must change, it has a tool in it.

**If it fails:** Replace the tool name with the outcome the tool was there to give.

## The Constraints (P2, P4)

### 4. Is every constraint a hard boundary you would reject on?

A constraint is a wall. Crossing it is always a failure. If crossing it is fine "in some cases", it is a preference. Preferences belong in LTM as practices, not in the intent.

**How to check:** For each constraint, ask: if the output breaks this, do I reject it every time, with no exceptions? Words like "should", "prefer" or "ideally" mean the answer is no.

**If it fails:** Move the preference to LTM, or delete it.

### 6. Is every constraint something the builder needs to make design choices?

This is the [Constraint-Failure Classification Rule](./idd-principles.md#the-constraint-failure-classification-rule). The builder sees the constraints, so each one must change how the builder works. A requirement that can only be checked after the output exists is a failure condition. If the builder sees it, the builder is tempted to aim at the check instead of at the goal.

**How to check:** For each constraint, ask: would knowing this change how the builder writes the code? Yes means it stays a constraint. No means it is a failure condition.

**If it fails:** Move the item to the failure conditions, which only the validator sees.

## The Failure Conditions (P3, P4)

### 5. Can every failure condition be evaluated without human opinion?

A failure condition is a halt signal. It only works if the system can tell, by itself, whether it fired. "The code is not clean" needs a human to judge it. "The code does not compile" does not.

**How to check:** Could a validator agent decide true or false with no human in the loop? If the answer depends on taste or degree, the condition fails this check.

**If it fails:** Rewrite it as something observable and binary. If you can't, it is a quality preference. Remove it from the intent and leave it to review or to LTM.

### 7. Are failure conditions evaluable from builder output alone?

Under compartmented evaluation, the validator does not see the goal or the constraints. So each failure condition must be checkable from the output alone. If the validator needs to know what the builder was aiming for, the item is probably a constraint in disguise.

**How to check:** Hand the condition and the output to someone who has never seen the goal. Can they decide? If not, the condition leans on hidden context.

**If it fails:** Reword it so the output alone answers it, or move it to the constraints (check 6).

### 8. Is validator feedback symptom-based, not condition-based?

When the validator finds a problem, it says what is wrong with the output: "line 47 holds a hard-coded connection string". It never says which check failed: "FC-3 violated". A check ID lets the builder learn the test and aim at it. A symptom makes it fix the real problem. See the [Symptom-Based Feedback Protocol](./idd-principles.md#symptom-based-feedback-protocol).

**How to check:** Read the validator's feedback template. If it can print a condition ID or a condition name, it fails.

**If it fails:** Change the feedback to describe the output, never the rule.

## The Shape of the Intent (P5, P6, P7)

### 9. Does the intent work without knowledge of other intents?

Each intent must stand alone. If it works only because another intent left something behind, it has a hidden dependency, and it will break when that other intent changes. Shared knowledge goes in LTM. Issue-specific artifacts go in STM.

**How to check:** Delete every other intent in your head. Does this one still make sense, and can it still run?

**If it fails:** Move the shared knowledge into LTM or STM, and refer to it from there.

### 10. Can you state the goal in one sentence without "and"?

A goal that needs "and" is usually two goals. Big work gets split into more intents, not into more detail inside one intent. One large detailed intent turns back into a spec.

**How to check:** Write the goal as one sentence. If you reach for "and", "then" or a semicolon, look again.

**If it fails:** Split it into several intents, each with its own goal, and let each one have its own checkpoint.

### 11. Can the agent restate this intent in concrete codebase terms?

Before it starts, the agent must restate the goal, the constraints and the failure conditions against the real code: which modules, which public interfaces, which tests. If the restatement shows two possible readings, the system must stop and ask, not guess.

**How to check:** Ask whether two reasonable agents, given the same codebase, could read the intent in two different ways. If yes, it is ambiguous.

**If it fails:** Tighten the wording, or add a checkpoint where the agent's restatement is approved before any work.

## The Feedback Around It (P8)

### 12. Is this the earliest point this failure could be detected?

Failures are cheapest when they are caught early. Analysis comes before design, and design comes before build. A failure condition that only fires after three steps have run wastes all three.

**How to check:** For each failure condition, ask how many steps have already run when it can fire. If more than zero, ask whether an earlier step could catch it.

**If it fails:** Move the check earlier, or split off an early intent that produces something a human can check first.

### 13. Will the checkpoint add value, not rubber-stamp?

A checkpoint is where human judgment enters. If it is approved every time, it adds delay and nothing else. If it is rejected most of the time, the intent before it is poorly formed.

**How to check:** Estimate the approval rate. A healthy range is 70–90%. 100% means a rubber stamp. Under 50% means the intent needs work.

**If it fails:** Remove the checkpoint, or fix the intent before it.

### 14. Can you measure this intent's health over time?

A shipped outcome does not prove the intent was well designed. Track the intent across runs: approval rate, rework cycles, how often constraints are broken, and the other signals in the [intent health table](./idd-principles.md#measure-intent-health).

**How to check:** Name at least three signals from that table that you can collect for this intent.

**If it fails:** Add the evidence or logging that lets you track them, before the intent goes live.

---

## Related Documentation

- [IDD](./intent-driven-development.md): the paradigm
- [IDD design principles](./idd-principles.md): the principles behind each check
- [IDD anti-patterns](./idd-anti-patterns.md): what an intent looks like when these checks are skipped
- [Intent Complexity Scoring](./intent-driven-development.md#intent-complexity-scoring-ics): the same checks scored as a balance profile

---

**Author**: Kapil Viren Ahuja
**Version**: 1.0.0
**Last Updated**: 2026-10-07
**Status**: Active
