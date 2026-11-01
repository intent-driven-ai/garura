#!/usr/bin/env python3
"""
write_page.py — write a business intent's page from its draft, new or rewritten (author-intent-page).

It decides no words: every word comes from the draft, and the stage is confirmed only when the
caller names the person who confirmed it.

    python3 write_page.py --draft <working>/intent-draft.json --product-base <product_base> \
        --date <YYYY-MM-DD> --out <working>/intent-page.json \
        [--rewrite] [--stage proposed|confirmed] [--confirmed-by "<who>"]

intent-draft.json:
    {"id": "bi-<issue>", "issue": <issue>, "title": "...", "outcome": "...", "why": "...",
     "asked_by": "<a persona>", "proof": ["...", ...], "must_not": "..." (optional),
     "rules": ["...", ...] (optional), "serves": "#12" (optional), "identified_by": "..." (optional)}

The page is <product_base>/product-os/intents/<id>.md, in this order, a blank line between each:
the title, Outcome, Why, Asked by, Proof it is met, Must not, Rules, Serves and Identified by
(the last four when the draft has them), then the stage line with the Tracker line right under it.

A new page ends with "**What was done:** (nothing yet)", and a page already there refuses unless
--rewrite is given. A rewrite needs the page to be there. It keeps the old page's Touches block and
What-was-done block byte for byte and replaces everything else; each block runs from its line to the
next line that starts with ** or the end. An old page with no What-was-done block gets the new
page's line.

Refused, nothing written: a required part empty (title, outcome, why, asked by, a proof line); an id
that is not bi-<digits> or not bi-<issue>; a part that holds a line break (it could write a stage line
of its own); --stage confirmed with nobody in --confirmed-by; a date not in the form YYYY-MM-DD.

intent-page.json: id, page (relative to the product base), written, rewrite, stage, kept.
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
NOTHING_YET = "**What was done:** (nothing yet)"
KEPT_BLOCKS = (("Touches", "**Touches:**"), ("What was done", "**What was done:**"))


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


def render(draft, stage, kept_blocks):
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
    return "\n\n".join(parts + kept_blocks) + "\n"


def page_path(product_base, pid):
    root = os.path.realpath(os.path.join(product_base, MODEL))
    page = os.path.join(root, "intents", f"{pid}.md")
    if not os.path.realpath(page).startswith(root + os.sep):
        raise Refused(f"the page of {pid} leaves the model folder")
    return page


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
        page = page_path(a.product_base, draft["id"])
        there = os.path.lexists(page)
        if there and not a.rewrite:
            raise Refused(f"the page of {draft['id']} is already there; only --rewrite changes it")
        if a.rewrite and not there:
            raise Refused(f"--rewrite needs a page, and {draft['id']} has none")
        kept, kept_blocks = [], []
        if a.rewrite:
            with open(page, encoding="utf-8", newline="") as fh:
                old = fh.read()
            old_lines = old.splitlines(keepends=True)
            for name, header in KEPT_BLOCKS:
                found = block(old_lines, header)
                if found is not None:
                    kept.append(name)
                    kept_blocks.append(found)
        if "What was done" not in kept:
            kept_blocks.append(NOTHING_YET)
        text = render(draft, stage, kept_blocks)
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
