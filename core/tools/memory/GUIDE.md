# Memory: how every agent finds it and uses it

Read this before you decide anything. Memory is what you decide from. You find it only
through the memory tool, run from the project's root folder. Never read a memory file by its
path. Only agents call the tool: a play asks its agents for what it needs, and a skill reads
only what its agent puts in short-term memory. The working files your own play hands you for this run are not a memory lookup: read
them directly. Never answer from what you already know, and never from the web, without a
memory update a person approved.

## The three tiers

- **Short-term memory** — the current issue's own folder: its plan, specs and context, the
  questions asked of a person and the answers. A lookup reads only the issue you work on,
  never another issue. Every memory write goes here.
- **Garura memory** — this project's own memory, in two folders the tool reads in this
  order: `core/memory`, then the product model (`product`). It holds what was built for this
  project from the part of Phoenix memory it needs, and what people promoted.
- **Phoenix memory** — the global memory. It holds everything. There is one copy on each
  machine (`~/.phoenix/core/memory`), and the tool downloads it the first time a command
  needs it.

A new project starts with no memory of its own. A play run after the install, `initialize`,
will set it up from Phoenix memory; it is not built yet. Until then, lookups go up to Phoenix
memory.

## Find memory

```
python3 {tool} search --issue 12 --pattern "password reset" --ignore-case
python3 {tool} find   --issue 12 --glob "**/user-management.md"
python3 {tool} read   --issue 12 --tier phoenix --path knowledge/domains/user-management.md --start 60 --end 64
```

- Give the issue you work on (`--issue`). With no issue, the lookup starts at Garura memory.
- A lookup goes short-term, then Garura, then Phoenix memory, and stops at the first tier
  that answers. `answered_by` names that tier.
- To go up a tier, ask that tier: `--tier garura` or `--tier phoenix`. To see every tier,
  add `--every-tier`.
- The tool never copies a file from Phoenix memory. Reading one writes nothing.
- Each answer is one line of JSON. `"ok": false` is an error: read its message. The error
  `tier_missing` means a tier cannot be reached. Say so. It never means "nothing found".

## When no tier answers: raise a memory update

Do not guess. Draft the answer as a memory update, and a person approves or rejects it:

```
python3 {tool} propose --request '{"issue": 12, "missing": "How long a reset link lasts",
  "target_tier": "short-term", "target_path": "12/context/answers/reset-link.md",
  "draft": "A reset link expires after one hour.", "draft_source": "web",
  "sources": [], "requested_by": "<your agent name> (<your play>)"}'
```

- `draft_source` says where the draft came from: `person`, `web`, `model` or `memory`.
- An update always goes to the issue's short-term memory, and it is used only after a person
  approves it and it is applied. Until then no lookup finds it.
- Your work goes on while the update waits, unless you cannot go on without it. Then add
  `"blocking": true` and stop.

## Name what you decided from: the trace

Every decision keeps its trace: the question, the answer, and each step you took — what you
looked for, what you found, and the memory lines that said so. Take the tier, path, lines
and fingerprint from the `read` answer.

```
python3 {tool} cite --request '{"issue": 12, "play": "<your play>",
  "question": "Which way back in must a password sign-in offer?", "answer": "Password reset.",
  "decided_by": "<your agent name>",
  "trace": [{"asked": "account recovery for a password sign-in", "found": "password reset is the floor",
             "source": {"tier": "phoenix", "path": "knowledge/domains/user-management.md",
                        "start": 62, "end": 62, "fingerprint": "<from the read answer>"}}]}'
python3 {tool} citations --issue 12 --check
```

`cite` refuses a source that is gone or changed. `citations --check` names every decision
whose source no longer says what it said.

## What you never do

- Never write to Garura memory or Phoenix memory yourself. Every memory write goes to the
  issue's short-term memory, and a person's answer to a question goes there too. Moving it up
  to Garura memory or Phoenix memory is a promotion a person makes on purpose, outside your
  work. A new memory made anywhere else breaks the guardrail.
- Never decide from another issue's short-term memory, from a waiting memory update, or
  from an earlier decision record.
