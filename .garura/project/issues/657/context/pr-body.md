## What this delivers

**The memory tool can find memory.** `core/tools/memory/memory.py` is the one entry agents will call: `health`, `find`, `search`, `read`, `pull` and `pulled`. A lookup goes short-term memory (the issue's own folder only) → Garura memory (the project's `.garura/`) → Phoenix memory, and stops at the first tier that answers. It searches the way Claude Code does (find files, git grep their text, read exact lines), and every result names its tier, file, lines and fingerprint.

**Phoenix memory is read only at its approved version** — the commit `phoenix_ref` names (default `origin/main`). A change on a branch, or edited on disk, is not read. Kapil, 2026-10-18: "unless memory is approved (outside) the reader cant use that phoenix memory".

**Memory that is used is saved.** When a file is read from Phoenix memory, the tool pulls it into Garura memory, so the next lookup answers from the project. A search hit alone pulls nothing. Kapil: "the file is pulled when needed.. once the memory is used, then it saved in garura / proejct memory."

**Contract version 2** (`core/tools/memory/contract/v2.json`; version 1 kept as it was): a lookup of Garura or Phoenix memory works without an issue (it goes Garura → Phoenix), and a glob, like a path, never steps outside its tier (`../613/**` is refused).

**Kapil's test passes on a fresh project** with a copy of Phoenix memory: login story answered by Phoenix memory and saved; the re-run answered by Garura memory; change-password answered partly by Garura memory and partly by Phoenix memory; with project memory removed, the lookup goes up to Phoenix memory again, and a question no tier answers gives the empty answer — the cue for a memory update (#658). Record: `.garura/project/issues/657/evidence/kapil-test.md`.

Also: five finished plans that stayed active after their merges are closed out (#617, #632, #654, #655, #656).

Closes #657

## Where the issue text no longer matches

| Issue says | What happened |
|---|---|
| The tool writes approved updates to their tier | Not here. Kapil, 2026-10-18: memory updates land in short-term memory only (#658); `learn` and `promote` plays move memory up |
| It pulls a piece when it finds it in Phoenix memory | It pulls when the file is read (used), on Kapil's word |
| Every lookup names its issue | Version 2: a lookup of Garura or Phoenix memory works without one (the issue's own done-when) |
| Pointing it at Griffin is one setting | The `engine` setting exists; only the folder engine is built |

No agent calls the tool yet. Kapil kept the order: agents move onto it in #661, after #658–#660.

## Not in this change

- Memory updates, citations, the install (#658, #659, #660); moving agents onto the tool (#661, #663).
- Amending ADR 035 and ADR 036 for these decisions (its own `/adr` change).
- The no-client-names rule in project memory (#672); the merge play's plan check (#673).

## Self-review

Rules: `standards/rules/self-review.md` from Phoenix memory (Garura memory has no copy). Blocking: **0**. Notes: 12, full review in `.garura/project/issues/657/context/self-review.md`.

Checks run: `test_memory.py` 33 (36 after the fixes below), `test_pull.py` 12, `test_check_contract.py` 49; the contract check (22 samples, 23 broken samples, boundary) passes; ruff clean; both plans valid; Kapil's test passes; merges cleanly with main; no secret, home-folder, client or company text.

Fixed after the self-review: every command-line failure now answers in JSON (pull with no paths, Garura memory that cannot be written, an unknown tier, unreadable `--request`); stale "version 1" wording; the tests no longer leave temp folders; the test record matches its runner. The rest of the notes are placed in the #657 plan, "After this story".

🤖 Generated with [Claude Code](https://claude.com/claude-code)
