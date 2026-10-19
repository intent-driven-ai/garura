# #660 — the memory system on a fresh project

Run on 2026-10-19 from branch `feature/660-install-carries-memory` (after `d2e84523`).
`<work>` is a throwaway folder; nothing on the machine's own memory was touched. Phoenix
memory's place for each test was an empty folder under `<work>`; its source was the real
default, `https://github.com/intent-driven-ai/phoenix-memory.git`.

## 1. Claude Code: a fresh project, installed with no memory

```
python3 core/components/plays/install-garura/scripts/install.py --target <work>/shop --tool claude \
  --memory-dest <work>/shared-memory --phoenix-place <work>/machine/phoenix-memory
```

The install's own words (the end of its output):

```
  memory tool: .garura/tools/memory (settings written)
  memory guide: .claude/rules/garura-memory.md
  Short-term memory: reached.
  Garura memory: reached.
  Phoenix memory: not on this machine yet. The tool downloads it to <work>/machine/phoenix-memory the first time it is needed.
done — installed 13 agent(s) and 77 skill/play(s) into <work>/shop for claude
```

Exit 0. Phoenix memory's place after the install: **not there** — the install brought no memory.

## 2. A real sub-agent in that project finds a piece of memory

In `<work>/shop`, a headless Claude Code session (`claude -p`, version 2.1.303) was asked to
dispatch one general-purpose sub-agent with this task, and nothing else: "In this project,
which way back in must a password sign-in offer? Decide it from memory, and name the memory
lines your answer rests on." The prompt did not name the tool, the guide or any path. The
session was allowed only the Agent tool, Read, and `python3 .garura/tools/memory/memory.py`.

What the sub-agent did, in order (from the session's stream):

1. `python3 .garura/tools/memory/memory.py search --pattern "password" --ignore-case --every-tier`
   — looked in Garura, then Phoenix memory; answered by Phoenix memory. This first command
   downloaded Phoenix memory from GitHub to its place.
2. `read --tier phoenix --path knowledge/domains/user-management.md --start 58 --end 75`
3. `read --tier phoenix --path knowledge/domains/user-management.md --start 61 --end 62` —
   "Account Recovery — include with any credential-based auth. / Password reset — the floor;
   any credential login." Version `ad3afb587…`.
4. `cite` — recorded the decision with its trace: `cite-20261019-001`, stored in short-term
   memory.

Its answer: "A password sign-in must offer password reset as its way back in. Memory calls it
'the floor' ... The answer rests on one file, lines 61 and 62 of the global (Phoenix) memory
file `knowledge/domains/user-management.md` ... Memory in this project (Garura memory) had
nothing of its own on this. The answer came from Phoenix memory, and reading it saved a copy
into the project's memory."

Phoenix memory's place after the run: **downloaded** (a git repository at version `ad3afb5`).

So the sub-agent learned the tool and the rules from the guide alone
(`.claude/rules/garura-memory.md`), used only the tool, named its source lines, and kept the
trace.

## 3. Codex: a fresh project that already has its own AGENTS.md

The project's `AGENTS.md` held two lines: `# Our shop` and `Keep answers short.`

```
CODEX_HOME=<work>/codex-home python3 core/components/plays/install-garura/scripts/install.py \
  --target <work>/shop-codex --tool codex --memory-dest <work>/shared-memory \
  --phoenix-place <work>/machine2/phoenix-memory
```

Exit 0, the same check lines as in step 1. `AGENTS.md` kept its two lines and gained one
marked block holding the guide. No Codex agent was run.

## 4. Uninstall

`uninstall.py --target` on both projects:

- Claude Code project: the tool, its settings and `.claude/rules/` are gone. Left: the
  project's own memory and work — the piece the sub-agent's read saved into Garura memory
  (`.garura/core/memory/…/user-management.md`, `pulled.json`), its decision record in
  short-term memory, and `CLAUDE.md` (an install never removes it).
- Codex project: `AGENTS.md` is back to its own two lines; `AGENTS.md.new` is gone.

## Not run here

- The public installer (`installer/install.sh`) downloads a published release, so its new
  step can only run after a release carries it. Checked instead: its syntax (`bash -n`), and
  the script it calls, run the same way (`memory_system.py --target … --tool claude`).
- A Codex agent. Not checked: whether Codex's sandbox lets the tool download Phoenix memory
  on first use.
