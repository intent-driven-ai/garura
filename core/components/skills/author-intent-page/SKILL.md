---
name: author-intent-page
description: Write a business intent's page in the product model from its draft — a new page, or a rewrite of one that is there. The draft starts as the intent-draft.json that author-business-intent writes in one-intent mode, and a caller may add the optional fields rules, serves, identified_by and touches. The page holds what the draft holds, and this skill drafts nothing. Its script writes every part in one fixed order (title, outcome, why, asked by, proof it is met, must not, rules, serves, identified by, stage and tracker, touches, what was done). On a rewrite it keeps the old page's What-was-done block byte for byte, keeps its Touches block too unless the draft gives touches, which replace it, and replaces everything else. It is mechanical. It never overwrites a page unless told to rewrite it, and never confirms by itself; the stage is proposed unless the caller names the person who confirmed it. A required part left empty, an id that is not the issue's, a draft part holding a line break, or a touches entry with a bad kind or mark, an empty title or a link that leads to no file refuses the page and writes nothing. Used through product-os-keeper by any play or run that has a person's approved words for an intent page.
user-invocable: false
model: sonnet
allowed-tools: Read, Bash
---

# author-intent-page

The draft holds the words of a business intent. This skill puts them on the intent's page, in the
one shape every intent page has. The page holds what the draft holds, and this skill drafts nothing:
which words, and whether the person confirmed them, were settled before it runs.

## Input

| Field | Required | Meaning |
|-------|----------|---------|
| `draft` | yes | `intent-draft.json` — see below. |
| `product_base` | yes | The project's product base; the page is `<product_base>product-os/intents/<id>.md`. |
| `date` | yes | Today, as `YYYY-MM-DD`. A confirmed stage line carries it. |
| `out` | yes | Where to write `intent-page.json`. |
| `rewrite` | no | The page is there and is to be rewritten. With no `rewrite`, a page already there refuses; with it, a page not there refuses. |
| `stage` | no | `proposed` (the default) or `confirmed`. |
| `confirmed_by` | for `confirmed` | The person who confirmed it. |

What the draft holds:

- **From `author-business-intent`, in one-intent mode:** `id` (`bi-<issue>`), `issue`, `title`,
  `outcome`, `why`, `asked_by`, `proof` (a list of one line or more), and `must_not` when the statement
  gives a limit. Its `basis` and `other_needs` do not reach the page.
- **Optional fields a caller may add:** that skill does not write these. They are `rules` (a list),
  `serves` (for example `#539`), `identified_by`, and `touches`, a list of
  `{"title", "link", "kind", "mark"}`, where `kind` is domain, capability or feature and `mark` is adds,
  changes or removes.

Each part is one line. A part the draft leaves out is not on the page.

## Process

1. **Run the script:**

   ```bash
   python3 scripts/write_page.py --draft <working>/intent-draft.json \
       --product-base <product_base> --date <YYYY-MM-DD> --out <working>/intent-page.json \
       [--rewrite] [--stage proposed|confirmed] [--confirmed-by "<who>"]
   ```

   Exit 0: written. Exit 2: nothing was written; the error says why.
2. **Return the report's path.**

The page, with a blank line between each part: `# <title>`, `**Outcome:**`, `**Why:**`, `**Asked by:**`,
`**Proof it is met:**` with one `- ` line per proof, then `**Must not:**`, `**Rules:**` with `- ` lines,
`**Serves:**` and `**Identified by:**` when the draft has them, then the stage line with the
`**Tracker:** #<issue>` line right under it, then the Touches block, then the What-was-done block. The
stage line is `**Stage:** proposed` or exactly `**Stage:** confirmed — by <who>, <date>`.

The Touches block is `**Touches:**` followed by one line per entry, in exactly this form:
`- [<title>](<link>) (<kind>) — <mark>`. Each link is relative to the page's own folder, and must lead
to a file inside the model.

A new page ends with `**What was done:** (nothing yet)`. A rewrite keeps the old page's What-was-done
block unchanged. It keeps the old Touches block unchanged too when the draft gives no touches (an
empty list gives none); when the draft gives touches, they replace it. Each block runs from its line
to the next line that starts with `**`, or the end. Everything else on the old page is replaced, and
an old page with no What-was-done block gets the new page's line.

## Output

`intent-page.json`, at `out`: `id`, `page` (relative to the product base), `written`, `rewrite`,
`stage` and `kept` (the old blocks kept as they were: `Touches`, `What was done`; none on a new page,
and never a Touches block the draft replaced). No report is written when the script exits 2.

## Rules

- **It drafts nothing.** The page holds what the draft holds. It does not fix, shorten or fill in a
  part. A required part left empty (title, outcome, why, asked by, a proof line) refuses the page.
- **It never confirms by itself.** Confirmed is written only when the caller passes the person who
  confirmed it; a rewrite with no stage goes back to proposed, whatever the old page said. A draft
  part holding a line break refuses the page, so a draft can never write a stage line of its own.
- **It never overwrites by accident.** A page that is there changes only with `rewrite`.
- **The id is the issue's.** An id that is not `bi-<digits>`, or not `bi-<issue>`, refuses the page.
- **Every Touches line can be followed and read back.** A bad kind or mark, an empty title, a title
  holding a square bracket, a link holding whitespace or a closing bracket, or a link that leaves the
  model or leads to no file refuses the page.
- **One page, no spine.** It writes only this page. A link between a part and an intent is kept on
  both sides: the page's Touches list is written here when the draft gives it, and the spine's side
  is another skill's work.
