#!/usr/bin/env python3
"""
write_page.py — write a business intent's page from its draft, new or rewritten (author-intent-page).

It decides no words: the page holds what the draft holds, and the stage is confirmed only when the
caller names the person who confirmed it.

    python3 write_page.py --draft <working>/intent-draft.json --product-base <product_base> \
        --date <YYYY-MM-DD> --out <working>/intent-page.json \
        [--rewrite] [--stage proposed|confirmed] [--confirmed-by "<who>"]

intent-draft.json:
    {"id": "bi-<issue>", "issue": <issue>, "title": "...", "outcome": "...", "why": "...",
     "asked_by": "<a persona>", "proof": ["...", ...], "must_not": "..." (optional),
     "rules": ["...", ...] (optional), "serves": "#12" (optional), "identified_by": "..." (optional),
     "touches": [{"title": "...", "link": "../care/booking/capability.md",
                  "kind": "domain|capability|feature", "mark": "adds|changes|removes"}] (optional)}

The page is <product_base>/product-os/intents/<id>.md, in this order, a blank line between each:
the title, Outcome, Why, Asked by, Proof it is met, Must not, Rules, Serves and Identified by
(the last four when the draft has them), then the stage line with the Tracker line right under it,
then the Touches block when there is one, then the What-was-done block.

Touches is the page's side of the link between a part and this intent: one line per entry,
"- [<title>](<link>) (<kind>) — <mark>". Each link is relative to the page's own folder and must
lead to a file inside the model.

A new page ends with "**What was done:** (nothing yet)", and a page already there refuses unless
--rewrite is given. A rewrite needs the page to be there. It keeps the old page's What-was-done block
byte for byte, and its Touches block byte for byte too unless the draft gives touches, which replace
it; an empty list gives none. Everything else is replaced. Each block runs from its line to the next
line that starts with ** or the end. An old page with no What-was-done block gets the new page's line.

Refused, nothing written: a required part empty (title, outcome, why, asked by, a proof line); an id
that is not bi-<digits> or not bi-<issue>; a part that holds a line break (it could write a stage line
of its own); a touches entry with a bad kind or mark, an empty title, a title holding a square bracket
or a link holding whitespace or a closing bracket (the line could not be read back), or a link that
leaves the model or leads to no file; --stage confirmed with nobody in --confirmed-by; a date not in
the form YYYY-MM-DD.

intent-page.json: id, page (relative to the product base), written, rewrite, stage, kept (the old
blocks kept as they were; none on a new page, and never a Touches block the draft replaced).
The page and the report go through safe_write.atomic_write. No git, no network.
Exit 0 written, 2 refused.
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import safe_write  # noqa: E402  (stamped beside this script)

MODEL = "product-os"
INTENT_ID = re.compile(r"bi-[0-9]+")
DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
TOUCHES = "**Touches:**"
WHAT_WAS_DONE = "**What was done:**"
NOTHING_YET = f"{WHAT_WAS_DONE} (nothing yet)"
TOUCH_KINDS = ("domain", "capability", "feature")
TOUCH_MARKS = ("adds", "changes", "removes")


class Refused(Exception):
    pass


def words(draft, key):
    """A part of the draft as one line of plain words; empty when it is not there."""
    value = draft.get(key)
    if value is None:
        return ""
    if isinstance(value, (dict, list, bool)):
        raise Refused(f"the draft's {key.replace('_', ' ')} must be plain words")
    text = str(value).strip()
    if "\n" in text or "\r" in text:
        raise Refused(f"the draft's {key.replace('_', ' ')} holds a line break; each part is one line")
    return text


def lines_of(draft, key):
    """A list part of the draft as its non-empty lines; empty when it is not there."""
    value = draft.get(key)
    if value is None:
        return []
    if not isinstance(value, list):
        raise Refused(f"the draft's {key} must be a list of lines")
    out = [words({key: item}, key) for item in value]
    return [line for line in out if line]


def check(draft):
    if not isinstance(draft, dict):
        raise Refused("the draft must be one JSON object")
    pid, issue = draft.get("id"), draft.get("issue")
    if not isinstance(pid, str) or not INTENT_ID.fullmatch(pid):
        raise Refused(f"the id {pid!r} is not bi-<digits>")
    if isinstance(issue, bool) or str(issue) != pid[3:]:
        raise Refused(f"the id {pid} must be bi-<issue> for issue {issue}")
    for key in ("title", "outcome", "why", "asked_by"):
        if not words(draft, key):
            raise Refused(f"the draft has no {key.replace('_', ' ')}")
    if not lines_of(draft, "proof"):
        raise Refused("the draft has no proof it is met")


def stage_line(stage, who, date):
    if stage == "proposed":
        return "**Stage:** proposed"
    if not (who or "").strip():
        raise Refused("--stage confirmed needs the person who confirmed it in --confirmed-by")
    if "\n" in who or "\r" in who:
        raise Refused("--confirmed-by holds a line break")
    return f"**Stage:** confirmed — by {who.strip()}, {date}"


def check_link(title, link, page, root):
    """The link must lead, from the page's own folder, to a file inside the model."""
    if not isinstance(link, str) or not link or ")" in link or any(c.isspace() for c in link):
        raise Refused(f"touches, {title}: the link {link!r} is empty or holds whitespace or a closing bracket")
    target = os.path.realpath(os.path.join(os.path.dirname(page), link))
    if not target.startswith(root + os.sep):
        raise Refused(f"touches, {title}: the link {link} leaves the model folder")
    if not os.path.isfile(target):
        raise Refused(f"touches, {title}: the link {link} leads to no file from the page's own folder")


def touches_block(draft, page, root):
    """The Touches block the draft gives, one line per entry; None when it gives none."""
    entries = draft.get("touches")
    if entries is None or entries == []:
        return None
    if not isinstance(entries, list):
        raise Refused("the draft's touches must be a list of entries")
    lines = [TOUCHES]
    for entry in entries:
        if not isinstance(entry, dict):
            raise Refused(f"each entry of the draft's touches must be an object: {entry!r}")
        title, link, kind, mark = (entry.get(k) for k in ("title", "link", "kind", "mark"))
        if not isinstance(title, str) or not title.strip():
            raise Refused(f"a touches entry has an empty title: {entry!r}")
        title = title.strip()
        if set(title) & set("[]\r\n"):
            raise Refused(f"touches: the title {title!r} holds a square bracket or a line break")
        if kind not in TOUCH_KINDS:
            raise Refused(f"touches, {title}: the kind {kind!r} is not domain, capability or feature")
        if mark not in TOUCH_MARKS:
            raise Refused(f"touches, {title}: the mark {mark!r} is not adds, changes or removes")
        check_link(title, link, page, root)
        lines.append(f"- [{title}]({link}) ({kind}) — {mark}")
    return "\n".join(lines)


def block(lines, header):
    """The block from the line that starts with `header` to the next ** line or the end, without
    the blank lines after it; None when the page has no such line."""
    start = next((i for i, line in enumerate(lines) if line.startswith(header)), None)
    if start is None:
        return None
    end = start + 1
    while end < len(lines) and not lines[end].startswith("**"):
        end += 1
    kept = lines[start:end]
    while not kept[-1].strip():
        kept.pop()
    return "".join(kept).rstrip("\r\n")


def render(draft, stage, last_blocks):
    parts = [f"# {words(draft, 'title')}",
             f"**Outcome:** {words(draft, 'outcome')}",
             f"**Why:** {words(draft, 'why')}",
             f"**Asked by:** {words(draft, 'asked_by')}",
             "\n".join(["**Proof it is met:**"] + [f"- {p}" for p in lines_of(draft, "proof")])]
    if words(draft, "must_not"):
        parts.append(f"**Must not:** {words(draft, 'must_not')}")
    if lines_of(draft, "rules"):
        parts.append("\n".join(["**Rules:**"] + [f"- {r}" for r in lines_of(draft, "rules")]))
    if words(draft, "serves"):
        parts.append(f"**Serves:** {words(draft, 'serves')}")
    if words(draft, "identified_by"):
        parts.append(f"**Identified by:** {words(draft, 'identified_by')}")
    parts.append(f"{stage}\n**Tracker:** #{draft['issue']}")
    return "\n\n".join(parts + last_blocks) + "\n"


def page_path(root, pid):
    page = os.path.join(root, "intents", f"{pid}.md")
    if not os.path.realpath(page).startswith(root + os.sep):
        raise Refused(f"the page of {pid} leaves the model folder")
    return page


def last_blocks_of(old_text, new_touches):
    """The blocks that end the page, and the names of the old ones kept as they were."""
    old_lines = old_text.splitlines(keepends=True)
    kept, blocks = [], []
    old_touches = block(old_lines, TOUCHES)
    if new_touches is not None:
        blocks.append(new_touches)
    elif old_touches is not None:
        kept.append("Touches")
        blocks.append(old_touches)
    old_done = block(old_lines, WHAT_WAS_DONE)
    if old_done is not None:
        kept.append("What was done")
    blocks.append(NOTHING_YET if old_done is None else old_done)
    return blocks, kept


def main(argv=None):
    ap = argparse.ArgumentParser(description="Write a business intent's page from its draft.")
    ap.add_argument("--draft", required=True)
    ap.add_argument("--product-base", required=True)
    ap.add_argument("--date", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--rewrite", action="store_true")
    ap.add_argument("--stage", choices=("proposed", "confirmed"), default="proposed")
    ap.add_argument("--confirmed-by")
    a = ap.parse_args(argv)
    old = None
    try:
        with open(a.draft, encoding="utf-8") as fh:
            draft = json.load(fh)
        check(draft)
        if not DATE.fullmatch(a.date):
            raise Refused(f"the date {a.date!r} is not in the form YYYY-MM-DD")
        stage = stage_line(a.stage, a.confirmed_by, a.date)
        root = os.path.realpath(os.path.join(a.product_base, MODEL))
        page = page_path(root, draft["id"])
        there = os.path.lexists(page)
        if there and not a.rewrite:
            raise Refused(f"the page of {draft['id']} is already there; only --rewrite changes it")
        if a.rewrite and not there:
            raise Refused(f"--rewrite needs a page, and {draft['id']} has none")
        new_touches = touches_block(draft, page, root)
        if a.rewrite:
            with open(page, encoding="utf-8", newline="") as fh:
                old = fh.read()
        last_blocks, kept = last_blocks_of(old or "", new_touches)
        text = render(draft, stage, last_blocks)
    except (Refused, OSError, ValueError) as err:
        sys.stderr.write(f"write_page.py: refused, nothing written: {err}\n")
        return 2

    report = {"id": draft["id"], "page": os.path.join(MODEL, "intents", f"{draft['id']}.md"),
              "written": True, "rewrite": a.rewrite, "stage": a.stage, "kept": kept}
    try:
        safe_write.atomic_write(page, text)
        try:
            safe_write.atomic_write(a.out, json.dumps(report, indent=2) + "\n")
        except OSError:
            if old is None:
                os.remove(page)
            else:
                safe_write.atomic_write(page, old)
            raise
    except OSError as err:
        sys.stderr.write(f"write_page.py: refused, nothing written: {err}\n")
        return 2
    print(json.dumps(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
