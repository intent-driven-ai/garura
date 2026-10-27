# Structured Failure Format

How an agent reports a failure to its caller. Each agent that uses this format points to this
file. The agent's own file says where the failure goes and which error types it uses.

This file is not memory. The install lays it in the installed shared folder, at
`.claude/skills/_shared/failure-format.md`.

## When to use it

Use it when an obstacle is outside your domain, or when two attempts to recover failed. Return
the structured failure to the caller. Never return a raw error.

## The shape

```yaml
failure:
  what_failed: "{operation that failed}"
  why: "{root cause — specific, e.g. 'file not found', not 'error occurred'}"
  domain_assessment:
    within_my_domain: false
    responsible_domain: "{implementation | design | repository | project | infrastructure}"
    suggested_agent: "{agent name, if known}"
  context:
    intent_received: "{the intent passed by the caller}"
    constraint_violated: "{if applicable}"
    self_recovery_attempted: true|false
    self_recovery_details: "{what was tried, so the caller does not retry it}"
  suggested_fix: "{what you think would resolve this}"
```

## Recovery

- Make at most two attempts to recover from one obstacle.
- When the caller retries you after a failure, use the earlier failure and any fix that was
  applied. Do not repeat the approach that failed.
- When you fail again on the same obstacle, escalate at once.
