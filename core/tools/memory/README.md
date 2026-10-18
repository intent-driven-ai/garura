# Memory tool

The one way agents find memory and update it. Today it works on folders. Later it calls a
server in Griffin. Agents that call it do not change when that happens, because they only ever
talk to this tool, through the contract in `contract/v4.json`.

This folder holds the contract (version 4), sample answers, the check that keeps them in
step, and the tool: `memory.py` (with `pull.py` for Phoenix memory, `updates.py` for memory
updates and `citations.py` for decision records). It answers every command in the contract:
`health`, `find`, `search`, `read`, `pull`, `pulled`, `propose`, `updates`, `decide`, `apply`,
`cite` and `citations`.

## Running the tool

```
python3 memory.py health
python3 memory.py search --issue 657 --pattern "reset link" --ignore-case --max 20
python3 memory.py read --issue 657 --tier phoenix --path knowledge/domains/user-management.md --start 1 --end 5
python3 memory.py find --request '{"issue": 657, "glob": "**/user-management.md"}'
```

Each request field is a flag, or the whole request is one JSON object (`--request`). Each
answer is one JSON object per line. A request the contract does not allow is refused with
`bad_request` before any memory is read.

The tool learns where each tier lives from one source: the JSON file `MEMORY_SETTINGS` names
(places in it are relative to the file), else these environment variables:

| Setting | Environment | What |
|---|---|---|
| `short-term` | `MEMORY_SHORT_TERM_ROOT` | The folder that holds one folder per issue |
| `garura` | `MEMORY_GARURA_ROOT` | Garura memory's folder. If the short-term folder sits inside it, that part is short-term memory, not Garura memory |
| `phoenix` | `MEMORY_PHOENIX_ROOT` | Phoenix memory's git repository |
| `phoenix_ref` | `MEMORY_PHOENIX_REF` | Phoenix memory's approved version (default `origin/main`) |
| `garura_pull_dir` | `MEMORY_GARURA_PULL_DIR` | Where pulled pieces land inside Garura memory (default: its root) |
| `updates_dir` | `MEMORY_UPDATES_DIR` | Where an issue's memory updates are kept, inside its short-term folder (default `review/memory-updates`). A lookup never reads them: a draft is used only once a person approved it and it was applied |
| `citations_file` | `MEMORY_CITATIONS_FILE` | Where an issue's decision records are kept, inside its short-term folder (default `context/citations.jsonl`). A lookup never reads them: an agent never decides from its own earlier decision |
| `engine` | `MEMORY_ENGINE` | `folder`, the only engine built. A server engine is one setting away |

Two rules the folder engine keeps:

- **Phoenix memory is read only at its approved version**, the commit `phoenix_ref` names. A
  change reaches Phoenix memory when a person approves it outside Garura; until then — on a
  branch, or edited on disk — the tool does not read it.
- **Memory that is used is saved.** When an agent reads a file from Phoenix memory, the tool
  pulls it into Garura memory, so the next lookup answers from the project. A search hit alone
  pulls nothing.

`pull.py` holds the Phoenix side (the approved files, `pull`, `pulled`); its own command line
stays for direct use.

## The three tiers

| Tier | What it holds |
|---|---|
| `short-term` | One issue's own memory: its plans, specs and context. A lookup reads only the issue the work is on. |
| `garura` | **Garura memory** — the project's long-term memory. It holds the part of Phoenix memory this project pulled, and what the project makes itself: its product model, intents, decisions and the person's answers. |
| `phoenix` | **Phoenix memory** — the global memory, holding everything. Its own git repository until Griffin serves it. |

The tool learns where each tier lives from its settings, never from a fixed path. A tier with
no setting, or one it cannot reach, is an error (`tier_missing`) — never "nothing found".

## The lookup order

`find` and `search` look in **short-term**, then **Garura**, then **Phoenix** memory, and stop
at the first tier that has an answer. So the lowest tier answers whenever it can, and Phoenix
memory is reached only when the lower tiers have nothing. A lookup never stops a piece of work
because the project has not pulled something yet: the tool goes a level up and finds it.

A lookup names the issue the work is on, when there is one. Short-term memory is read only in that issue's
folder (`<issue>/`), never in another issue's. Otherwise another issue's old notes would answer
first, and Garura and Phoenix memory would never be reached. For example, an agent that searches
for "commit message" must not stop at another issue's old fix notes; it goes on to the commit rule
in Garura memory. A read of another issue's short-term path is refused (`bad_request`), and so
is a glob or path that steps outside its tier (`../613/**`).

A lookup with no issue has no short-term memory: it goes Garura, then Phoenix memory. This lets
work look things up before its issue exists. Asking for short-term memory without an issue is
refused (`bad_request`).

- `tier` asks one tier only.
- `every_tier` looks in all three and does not stop at the first answer. `answered_by` is then
  the first tier in the lookup order that has a result. Asking for `tier` and `every_tier`
  together is an error (`bad_request`).

A lookup never skips a tier. If it reaches a tier with no setting, or one it cannot reach, it
fails with `tier_missing`. "Never stops a piece of work" means a piece the project has not
pulled is found a level up — not that a tier may be passed over.

An empty answer — `answered_by: null`, no hits — means no tier it looked in holds it (with no
issue, short-term memory is not looked in). That is the cue to raise a memory update. Agents never fill the gap from the model or the web on their own.

## The commands

Every request is a JSON object. On the command line its fields are the flags (`search --pattern
"checkout" --max 20`); on a server they are the request body. Every answer is a JSON object
with `ok`, `contract_version` and `command`.

**Finding memory**

| Command | What it does |
|---|---|
| `health` | Reports each tier: reachable or not, folder or server, and its version. The install check calls this. |
| `find` | Finds files by name pattern, in the lookup order. |
| `search` | Searches the text of files, in the lookup order, and returns each hit with its tier, file and line. |
| `read` | Reads exact lines of one file and returns them with a fingerprint of the text. |
| `cite` | Records a decision and its trace in the issue's short-term memory: the question, the answer, who decided, the play, and the steps the agent took, in order — each with what it looked for, what it found, and its source (tier, file, lines, fingerprint). It reads every source first: one that is gone is `not_found`, one whose text changed is `changed`. The record keeps each source's exact text, the memory version, and up to 3 lines around it. A decision from an approved memory update names it (`from_update`), and the update's written file is the source of a step. |
| `citations` | Lists an issue's decision records (optionally one play's). With `--check`, reads every step's source again: a record with no trace (`no_source`), a source that is gone (`source_missing`), and a source whose text changed (`source_changed`, with the lines now and the lines around them) are each a problem, named by its step. |

**Updating memory**

| Command | What it does |
|---|---|
| `pull` | Copies one piece of Phoenix memory into Garura memory and records the version it came from. It never writes over a different Garura file (`would_overwrite`). |
| `pulled` | Lists what Garura memory pulled, and whether Phoenix memory has moved on since. |
| `propose` | Raises a memory update in the issue's short-term memory: what is missing, a drafted entry, where the draft came from (`person`, `web`, `model` or `memory`), and whether it blocks the work. Nothing in it is used until a person approves it. |
| `updates` | Lists memory updates, optionally only those with one status. |
| `decide` | Records a person's word on a waiting update: approve or reject, who, their exact reply, and where they decided (the review tool). Only a person decides, one update at a time. |
| `apply` | Writes an approved update to the issue's short-term memory. An update no one approved is refused (`not_approved`). |

A memory update moves through `waiting` → `approved` or `rejected` → `applied`.

## When no tier answers

1. The agent finds the answer by research — the web or the model may draft it — and raises it
   with `propose`, in the issue's short-term memory. Every update lands there ("STM - always
   STM"), whatever drafted it. It says whether it blocks the work: the rest of the work goes
   on unless it does.
2. A person approves or rejects it, one update at a time, in the review tool (`decide`). Until
   that tool is built, a local prototype page stands in. Nothing in it is used before that.
3. The approved answer is written to the issue's own short-term memory (`apply`). The work then
   decides from memory, and cites it.
4. Moving memory up is not this tool's job: `/learn-memory` learns from short-term memory into
   Garura memory, and `/promote-memory` sends Garura memory to Phoenix memory for an approval
   outside Garura.

## What every answer carries

- **Every piece of text** the tool returns — from `read`, a `search` hit, a trace step's source —
  carries its tier, file, lines and fingerprint. A file list from `find` carries tier, file and
  version. `pull` names the tier it wrote to.
- **Paths** are relative to the tier's root, use forward slashes, never start with a slash and
  never contain `..`.
- **Fingerprint** — `sha256:` and 64 hex characters, taken over the exact text returned or
  cited. When a file changes, an old citation's fingerprint no longer matches, so a stale
  answer can be seen.
- **Version** — for Phoenix memory, the repository's commit. For the other tiers it may be
  empty.

## How a request reads

- `glob` is shell-style: `*` within one folder, `**` at any depth, `?` one character.
- `pattern` is an extended regular expression, as `grep -E` reads it — or plain text when
  `fixed` is true.
- `read` reads from `start` (default the first line) to `end` (default the last). `end` before
  `start` is `bad_request`; lines outside the file are `out_of_range`.

## The answer rules

The check holds every sample to these, beyond its shape:

- A request the contract refuses is answered with `bad_request`, never with an answer: `tier`
  with `every_tier`, a `read` with `end` before `start`, and a `read` of a short-term path
  outside the issue.
- `looked_in` lists the tiers looked in, in the lookup order.
- `answered_by` names a tier only when that tier has a result, and is empty only when nothing was
  found. With `every_tier`, `looked_in` is all three tiers.
- "Nothing found" (`answered_by: null`) only after every tier was looked in — or just the one
  asked for. A shorter `looked_in` with nothing found is a silent skip, and fails.
- Without `every_tier`, the lookup stops at the first tier that answers, and every result comes
  from that tier.
- Every short-term path in an answer starts with `<issue>/`, the issue the request named.
- `read` answers the tier, file and lines asked (from line 1 to the last line when not given).
- A fingerprint is the sha256 of the exact text it travels with.
- A memory update agrees with its status. `waiting` has no decision yet. `approved`, `rejected`
  and `applied` carry the person, their reply and the time. An update applied to Phoenix memory
  carries its commit.
- An update to short-term memory names its issue, and its path is in that issue's folder.
- An update drafted from the web or the model goes to short-term memory.
- `propose` answers `waiting`, with what was asked exactly as given.
- `decide` answers `approve` as `approved` and `reject` as `rejected`, with the person and their
  reply exactly as given.
- `apply` answers only `applied`, and writes to the update's own tier and path.
- `updates` with a status lists only updates with that status.

## Errors

| Code | When |
|---|---|
| `settings_missing` | The tool has no settings at all. |
| `tier_missing` | A tier has no setting or cannot be reached. |
| `bad_request` | The request does not match the contract, or reads a short-term path outside its issue. |
| `not_found` | The file or update named does not exist. |
| `out_of_range` | The lines asked for are outside the file. |
| `not_approved` | `apply` on an update no person approved: it is waiting or was rejected. |
| `wrong_state` | `decide` on an update that is not waiting, or `apply` on one already applied. |
| `changed` | The target changed after the update was proposed, or a source `cite` was given no longer says what its fingerprint says. |
| `would_overwrite` | Garura memory already holds a different file at that path; nothing was overwritten. |
| `unreadable` | An issue's decision records hold a line that is not a whole record (a cut-off write or a hand edit). The answer names the file and line; other issues are not stopped. |

## What is not memory

- **Learned checkpoint answers.** The record of past checkpoint approvals is a checkpoint
  tool, not memory. It holds "approved or not" for a kind of change and cannot answer a
  question. A person's answers to questions are kept in Garura memory instead.
- **A play's own working files.** The files a play hands from one of its steps to the next,
  inside one run, are read and written directly. Only memory lookups go through the tool. The
  tool can still find those files later, as short-term memory.

## Rules for this folder

- Nothing here names a path inside a project or imports code from outside the folder, so the
  folder can move to Griffin as it is.
- Python standard library only, Python 3.10 or newer. No installs.
- The contract changes only by a new version. Version 4 is `contract/v4.json` (#659: `cite`
  records a decision with its trace — steps in order, each source read first and kept with its
  text, version and the lines around it; `citations` lists an issue's decision records and checks
  every step's source again, naming the step; decision records and waiting drafts are never
  found by a lookup). Version 3 (#658: every
  memory update lands in short-term memory, an update says whether it blocks, a person decides
  each one in the review tool, and a used file is never saved over a different Garura file).
  Version 2 (#657: lookups without an issue, globs that never step outside their tier, Phoenix
  memory read only at its approved version, memory that is used is saved) and version 1 are
  kept as they were.

## Checking the contract

From this folder:

```
python3 contract/check_contract.py
python3 contract/test_check_contract.py
python3 test_memory.py
python3 test_pull.py
```

The first checks every sample in `contract/samples/` against the contract's shapes and its
answer rules, checks that every sample in `contract/samples/broken/` fails, and checks the
folder's boundary: no path into a project, the framework's source or a home folder, and no
import from outside the standard library or the folder. It prints a JSON report and exits 0
when all hold. The second tests the check itself. `test_memory.py` tests the tool, and puts
every answer it gives through the same contract check. `test_pull.py` tests the Phoenix side.
All need Python 3.10 or newer.
