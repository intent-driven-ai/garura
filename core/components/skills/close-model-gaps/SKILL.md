---
name: close-model-gaps
description: Close the gaps in the product model that the model itself can close, from the gaps.json find-model-gaps wrote — attribute each loose node to its parent (a capability to its domain, a functionality to its capability), moving a holding-folder page under its parent unchanged; link nodes to the business intents they serve on both sides (the spine and the intent page's Touches list); and merge two nodes agreed to be the same thing. It writes no new page and no intent content, and deletes only a merged duplicate. What needs a play — a capability with no functionalities, a screen no node covers — is handed back as the work list for the loop. Its script does all of it mechanically. Used by the shared loop run after find-model-gaps, through product-os-keeper; later plays that fix the model's gaps can reuse it.
user-invocable: false
model: sonnet
allowed-tools: Read, Bash
---

# close-model-gaps

`find-model-gaps` says what is loose, what is twice and what is missing. This skill makes the
links the model can take without new content, and hands the rest back. It is mechanical: the
judgment was made in `gaps.json`.

## Input

| Field | Required | Meaning |
|-------|----------|---------|
| `gaps` | yes | `gaps.json` from `find-model-gaps`. |
| `product_base` | yes | The project's product base; the model is under `<product_base>product-os/`. |
| `out` | yes | Where to write `close-report.json`. |

## Process

1. **Apply what the model can take.** Run the script:

   ```bash
   python3 scripts/apply_links.py --gaps <working>/gaps.json --product-base <product_base> \
       --out <working>/close-report.json
   ```

   In order, it merges each duplicate marked `agreed: true` (keeps one entry, moves the
   other's intents and children onto it, removes the other's entry and page, points intent
   pages at the kept page); sets each `domain` and `capability` link (a page in a holding
   folder moves, byte for byte, under its parent's folder, and every link to it follows);
   and adds each `intents` link on both sides (the spine and the intent page's Touches list,
   through `intent_touches.py`).
2. **Read the report.** `applied` lists what changed; `skipped` lists each link it refused
   and why (a parent not in the spine, a node already under another parent — moving it is
   alignment work); `work_for_plays` is the work list for the loop, unchanged from
   `gaps.json`.
3. **Return the report's path.** The loop runs the plays the work list names in its next
   round.

## Output

`close-report.json`, at `out`: `applied` (each change made), `skipped` (each link refused,
with why, including any that would write outside the product model), `changed` (every file it
touched, relative to `product-os/`) and `work_for_plays` (the work list for the loop,
unchanged from `gaps.json`).

## Rules

- **Only inside the product model.** The script writes, moves and removes only under
  `<product_base>product-os/`. It checks every path first; a link that would reach outside is
  skipped and never half-applied. `changed` in the report lists every file it touched.

- **No new content.** It never writes an intent's words, a new capability page or a new
  functionality page. A page moves unchanged.
- **Delete only a merged duplicate.** Nothing else is removed.
- **Never move a node already under a parent.** Re-placing it is alignment work; the link is
  skipped with why.
- **Both sides of every link.** A node linked to an intent is named on the intent page's
  Touches list, and the intent is in the node's spine `intents`.
