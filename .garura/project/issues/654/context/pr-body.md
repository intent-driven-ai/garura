## What this decides

How Garura's memory works, so that agents work only from memory and a drive can make its own decisions. Kapil set the model on 2026-10-18; this records it.

- **ADR 035 — agents work only from memory.** Three tiers: **Phoenix memory** (global, the superset, in its own git repository until Griffin exists), **Garura memory** (the project's own long-term memory: the subset of Phoenix memory it pulled, plus its product model, intents, decisions and answers), and **short-term memory** per issue. A lookup goes short-term → Garura → Phoenix and stops at the first tier that answers; it never blocks a play. Agents find and update memory only through **one command-line tool** that searches the way Claude Code does, on folders now and on Griffin later. Nothing comes from the model or the web without a **memory update** a person approves, written to memory first. Every decision names its memory. Every Garura install carries the tool and a memory guide. Accepted by Kapil, who named the project tier "Garura memory" so it is not confused with the memory Claude Code and Codex keep.
- **What it replaces.** ADR 015 in part (the R1–R4 lookup and its fallback to the model). It amends ADR 034, 009, 016, 017 and 032; each carries a forward pointer.
- **The work is filed.** Stories #655 to #664 under Feature #653, one per item of the feature plan (`.garura/project/issues/653/specs/plan.md`, moved here from #613's folder).

Nothing is built: decision records, plans and run records only.

Closes #654

## Self-review

Rules: base `standards/rules/self-review.md` (no project override). Findings that stop the raise: **none**. Full review: `.garura/project/issues/654/context/self-review.md`.

**Scope**
- [PASS] Matches the issue: the decision is an accepted ADR, and the stories are filed.
- [REVIEW] Size: about 30 files, +1,230 lines, no code. Most of it is `/adr` run records (about 630 lines), the story texts (186) and plans; the decision to read is ADR 035 (167 lines).
- [PASS] Only `docs/adr/` and `.garura/` change; nothing under `core/` or `.claude/`.

**Quality**
- [PASS] No merge conflicts; no secrets; every JSON and YAML file parses.
- [PASS] ADR 035 has every section, reads Accepted, and is in the index; the forward pointers cite sections that exist.
- [PASS] Commits are conventional, one concern each, and name #654.

**For the reviewer (non-blocking)**
- The ADR scope check ran right after the record commit (a malformed command skipped it before), on the snapshot taken before that commit, and passed (`8b650262`).
- ADR 009 had no Status line; the tool added one reading "(not recorded)" above its own "## Status" section.
- ADR 035's "Work This Creates" says no story was filed yet; they were filed afterwards in this change (#655–#664). An accepted ADR is not edited.
- Some files ADR 035 lists under Affects have no story of their own yet: `CLAUDE.md`, `docs/components/memory.md`, the memory keys in `.garura/core/config.yaml`, drive-contract rule 4, the glossary's install rows, and the locked `knowledge/_DESIGN.md`. Proposed to Kapil to add them to the stories.
- Two commit subjects run past 72 characters.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
