# CLAUDE.md

This project uses Garura plays. These rules tell Claude Code how to run them here.

## How plays run

A play is a slash command (`/<play>`). Claude Code runs the play, the play hands its
domain work to agents through the Task tool, and the agents use skills to do the work. The
play's results go to the project's short-term memory, under the issue it works on
(`stm.base-path` in `.garura/core/config.yaml`).

- **Agent-first.** Inside a play, hand domain work to the agent the play names. Do not do it
  with tools directly when an agent covers it.
- **Agents gather context; skills do the work.** An agent puts the context a skill needs on
  disk, and the skill produces the result.
- **Explicit approvals.** At a checkpoint, never use `AskUserQuestion`. Show a short summary
  and wait for the person's typed reply.

## Memory

Agents reach memory only through the memory tool (`.garura/core/tools/memory/`), as its
guide says. Never read a memory file by its path.

## Talking to the person

Lead with what the person works on: the product, the feature, the outcome. File paths, ids
and field names go after that, never in the first line.
