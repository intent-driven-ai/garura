# #881 Initialize sets up the tracker's work-item types: Business Intent, Epic, Story, Bug, Chore and Spike

**When a project is initialized, its tracker gets the work-item types Garura files.** Garura files its work as issues of fixed types: Business Intent, Epic, Story, Bug, Chore and Spike. A tracker does not always have them. On 2026-10-25 Garura's own GitHub organization had no Epic type, so `/shape-plan` could not file an Epic as an Epic (#875). Each project hits the same gap the first time a play writes to its tracker.

So `initialize` (this business intent) also sets up the tracker: whatever the project uses — GitHub, Jira, Linear or another tracker — it finds the work-item types the plays need, and makes the ones that are missing.

## Done when

- `initialize` reads which tracker the project uses, and the types that tracker has.
- It lists the types the plays need (Business Intent, Epic, Story, Bug, Chore, Spike), each with its one-line meaning, and says which are missing.
- It makes each missing type only after the person's typed yes, and records what it made.
- Where a tracker cannot make a type, it says so in plain words and names the type it uses in its place; the plays read that mapping.
- GitHub works first. Jira and Linear come through the same adapter, each with its own way to make a type.
- A play that writes to the tracker stops with a plain message when a type it needs is missing, and points to `initialize`.

## Context

- Found in plan 788, while fixing #875: the organization `intent-driven-ai` got the Epic type by hand on 2026-10-25.
- Not planned yet. It is worked when this business intent's plan starts.
