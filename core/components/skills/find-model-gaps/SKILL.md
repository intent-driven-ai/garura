---
name: find-model-gaps
description: Find the gaps in the product model — the nodes not yet linked (a capability with no domain, a functionality with no capability, a node that serves no business intent), the same thing written twice, the work still missing (a capability with no functionalities, an intent no capability serves) and the screens of a prototype no node covers — and say, for each, the link to make or the play that does the missing work. Every kind is written on its own (ADR 043), so the model holds loose nodes until they are linked; this skill finds them. Its script counts the candidates; the judgment (is this really a gap, where does this node belong, which play owns the work) is the skill's. Writes gaps.json; never writes the model. Used by the shared drive run after each round, through product-os-keeper; later plays that show or fix the model's gaps can reuse it.
user-invocable: false
model: sonnet
allowed-tools: Read, Write, Glob, Grep, Bash
---

# find-model-gaps

The product model is written in pieces (ADR 043): `/intent` writes business intents,
`/vision` domains, `/understand` capabilities and functionalities, each on its own. A piece is
not ready until it is linked — functionality → capability → domain, and its agent intent to a
confirmed business intent. This skill finds what is not linked yet, what is written twice, and
what is still missing, and says what to do about each.

## Inputs

| Field | Required | Meaning |
|-------|----------|---------|
| `product_base` | yes | The project's product base; the model is under `<product_base>product-os/`. Read only. |
| `journeys` | no | A prototype's `journeys.yaml` (its `main_sections`), from the shared capture. |
| `view_texts` | no | The folder of the capture's view texts (`view-*.txt`). |
| `write_up` | no | The person's short write-up of the prototype (what it is, who uses it, the field and the job, the sample data, the walkthrough). |
| `out` | yes | Where to write `gaps.json`. |

## Procedure

1. **Count the candidates.** Run the script; it reads the spine, the pages and the capture:

   ```bash
   python3 scripts/find_gaps.py --product-base <product_base> \
       [--journeys <journeys.yaml>] [--view-texts <view texts folder>] \
       --out <working>/gap-candidates.json
   ```

   It lists: nodes with no parent (`unattributed`), parents named that do not exist
   (`dangling`), capabilities with no functionality, intents no node serves, nodes that serve
   no intent, empty domains, likely duplicates (titles that match once normalised) and
   screens no page's `## Sources` names (`uncovered`).
2. **Judge each candidate.** Read the pages and their `## Sources`. Clear a candidate that is
   not a gap (two titles that only look alike). Confirm the rest.
3. **Propose each link, with why.** For a loose node, name where it belongs — the capability
   a functionality is part of, the domain a capability sits in, the intents a node serves —
   from what the pages and their sources say, and say why in one plain line. Never invent a
   parent: when no node fits, it is missing work (step 5), not a link.
4. **Agree the duplicates.** For two nodes that are the same thing, name which to keep (the
   one with more content and sources) and mark it `agreed: true` only when the pages and
   their sources show the same screen and the same purpose.
5. **Give each piece of missing work to the play that does it:**
   - a capability with no functionalities → `/understand`;
   - a capability no domain holds, and no domain fits → `/vision`;
   - a screen's need that no business intent names → `/intent`;
   - an intent no capability serves → `/understand`;
   - a screen no capability or functionality covers → `/understand`.
6. **Write `gaps.json`:**

   ```json
   {
     "links_to_make": [{"kind": "capability", "id": "<id>", "field": "domain | capability | intents",
                        "value": "<parent id, or [intent ids]>", "why": "<one plain line>"}],
     "duplicates": [{"kind": "capability", "keep": "<id>", "drop": "<id>", "agreed": true, "why": "…"}],
     "work": [{"play": "/understand", "target": "<id or screen>", "why": "<one plain line>"}],
     "uncovered": [{"what": "main section | view", "name": "…"}],
     "cleared": [{"candidate": "…", "why": "…"}]
   }
   ```

## Rules

- **Read only.** This skill writes `gaps.json` and nothing else. `close-model-gaps` applies it.
- **No link without a basis.** Every link and every merge says why, from the pages, their
  sources, the capture or the write-up.
- **Work goes to the play that owns the kind** (ADR 043): intents to `/intent`, domains to
  `/vision`, capabilities and functionalities to `/understand`.
- **Plain words.** Each `why` is one short sentence a person reads without the model open.
