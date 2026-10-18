# Memory tool

The one way agents find memory and update it. Today it works on folders. Later it calls a
server in Griffin. Agents that call it do not change when that happens, because they only ever
talk to this tool, through the contract in `contract/v1.json`.

This folder holds the contract (version 1), sample answers and the check that keeps them in
step. The tool itself is built against this contract in a later step.

## The three tiers

| Tier | What it holds |
|---|---|
| `short-term` | One issue's own memory: its plans, specs and context. |
| `garura` | **Garura memory** — the project's long-term memory. It holds the part of Phoenix memory this project pulled, and what the project makes itself: its product model, intents, decisions and the person's answers. |
| `phoenix` | **Phoenix memory** — the global memory, holding everything. Its own git repository until Griffin serves it. |

The tool learns where each tier lives from its settings, never from a fixed path. A tier with
no setting, or one it cannot reach, is an error (`tier_missing`) — never "nothing found".

## The lookup order

`find` and `search` look in **short-term**, then **Garura**, then **Phoenix** memory, and stop
at the first tier that has an answer. So the lowest tier answers whenever it can, and Phoenix
memory is reached only when the lower tiers have nothing. A lookup never stops a piece of work
because the project has not pulled something yet: the tool goes a level up and finds it.

- `tier` asks one tier only.
- `every_tier` looks in all three and does not stop at the first answer.

An empty answer — `answered_by: null`, no hits — means no tier holds it. That is the cue to
raise a memory update. Agents never fill the gap from the model or the web on their own.

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
| `cite` | Records a decision and the memory it rests on — tier, file, lines, fingerprint — in the issue's short-term memory. |

**Updating memory**

| Command | What it does |
|---|---|
| `pull` | Copies one piece of Phoenix memory into Garura memory and records the version it came from. |
| `pulled` | Lists what Garura memory pulled, and whether Phoenix memory has moved on since. |
| `propose` | Raises a memory update: what is missing, where it belongs, a drafted entry, and where the draft came from (`person`, `web`, `model` or `memory`). Nothing in it is used until a person approves it. |
| `updates` | Lists memory updates, optionally only those with one status. |
| `decide` | Records a person's word on a waiting update: approve or reject, who, and their exact reply. Only a person decides. |
| `apply` | Writes an approved update to its tier — in Phoenix memory, as a commit. An update no one approved is refused (`not_approved`). |

A memory update moves through `waiting` → `approved` or `rejected` → `applied`.

## What every answer carries

- **Paths** are relative to the tier's root, use forward slashes, never start with a slash and
  never contain `..`.
- **Fingerprint** — `sha256:` and 64 hex characters, taken over the exact text returned or
  cited. When a file changes, an old citation's fingerprint no longer matches, so a stale
  answer can be seen.
- **Version** — for Phoenix memory, the repository's commit. For the other tiers it may be
  empty.

## Errors

| Code | When |
|---|---|
| `settings_missing` | The tool has no settings at all. |
| `tier_missing` | A tier has no setting or cannot be reached. |
| `bad_request` | The request does not match the contract. |
| `not_found` | The file or update named does not exist. |
| `out_of_range` | The lines asked for are outside the file. |
| `not_approved` | `apply` on an update no person approved. |
| `changed` | The target changed after the update was proposed. |

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
- Python standard library only. No installs.
- The contract changes only by a new version. Version 1 is `contract/v1.json`.

## Checking the contract

From this folder:

```
python3 contract/check_contract.py
```

It checks every sample in `contract/samples/` against the contract, checks that every sample
in `contract/samples/broken/` fails, and checks the folder's boundary. It prints a JSON report
and exits 0 when all three hold.
