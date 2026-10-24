#!/usr/bin/env python3
"""
write_intent_page.py — write a business intent's page when the model has none (/shape-slice, C1).

The run reads the intent from the product model. When the model has no page for it, the run
drafts one from the issue (author-business-intent) and this script writes it, in the shape of
the ontology's Business Intent: title, outcome, why, asked by, proof it is met, must not,
stage (proposed — only a person confirms it), and the tracker issue. It never overwrites a
page: when the page is there it writes nothing and says so.

    python3 write_intent_page.py --root <product-os dir> --intent <bi-id> --date <YYYY-MM-DD> \
        [--draft <intent-draft.json>] [--out <intent-page.json>]

Run it first with no --draft: when the page is there it reports written false (exit 0);
when it is missing it exits 3, and the run drafts the page and runs it again with --draft.

intent-draft.json:
    {"id": "bi-<issue>", "issue": <issue>, "title": "...", "outcome": "...", "why": "...",
     "asked_by": "<a persona>", "proof": ["...", ...], "must_not": "..." (optional)}

Prints {"ok", "written", "page", "reason"}. Exit 0 written or already there, 2 refused (a
required part is missing, or the id does not match the issue or --intent), 3 the page is
missing and no draft was given. Files on disk only.
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from safe_write import atomic_write  # noqa: E402

REQUIRED = ("title", "outcome", "why", "asked_by")


class Refused(Exception):
    pass


def render(d, date):
    lines = [f"# {d['title'].strip()}", "",
             f"**Outcome:** {d['outcome'].strip()}", "",
             f"**Why:** {d['why'].strip()}", "",
             f"**Asked by:** {d['asked_by'].strip()}", "",
             "**Proof it is met:**"]
    lines += [f"- {p.strip()}" for p in d["proof"]]
    lines.append("")
    if str(d.get("must_not") or "").strip():
        lines += [f"**Must not:** {d['must_not'].strip()}", ""]
    lines += [f"Written by /shape-slice from issue #{d['issue']} on {date}, because the product "
              "model had no page for it. A person confirms it.", "",
              "**Stage:** proposed",
              f"**Tracker:** #{d['issue']}", "",
              "**What was done:** (nothing yet)"]
    return "\n".join(lines) + "\n"


def check(d):
    if not isinstance(d, dict):
        raise Refused("the draft must be one JSON object")
    for key in REQUIRED:
        if not str(d.get(key) or "").strip():
            raise Refused(f"the draft has no {key.replace('_', ' ')}")
    proof = d.get("proof")
    if not isinstance(proof, list) or not [p for p in proof if str(p).strip()]:
        raise Refused("the draft has no proof it is met")
    if not re.fullmatch(r"bi-\d+", str(d.get("id") or "")) or str(d.get("issue")) != d["id"][3:]:
        raise Refused(f"the id '{d.get('id')}' must be bi-<issue> for issue {d.get('issue')}")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Write a missing business intent page.")
    ap.add_argument("--root", required=True)
    ap.add_argument("--intent", required=True, help="the business intent id, bi-<issue>")
    ap.add_argument("--draft")
    ap.add_argument("--date", required=True)
    ap.add_argument("--out")
    args = ap.parse_args(argv)

    def finish(result, code):
        text = json.dumps(result, indent=2)
        print(text)
        if args.out:
            atomic_write(args.out, text + "\n")
        return code

    page = os.path.join(args.root, "intents", f"{args.intent}.md")
    rel = f"intents/{args.intent}.md"
    if os.path.isfile(page):
        return finish({"ok": True, "written": False, "page": rel,
                       "reason": "the model already has a page for this intent"}, 0)
    if not args.draft:
        return finish({"ok": False, "written": False, "page": rel,
                       "reason": "the model has no page for this intent; draft one from the issue"}, 3)
    try:
        with open(args.draft, encoding="utf-8") as fh:
            d = json.load(fh)
        check(d)
        if d["id"] != args.intent:
            raise Refused(f"the draft is for '{d['id']}', not '{args.intent}'")
    except Refused as exc:
        return finish({"ok": False, "written": False, "reason": str(exc)}, 2)
    except (OSError, json.JSONDecodeError) as exc:
        return finish({"ok": False, "written": False, "reason": f"cannot read the draft: {exc}"}, 2)
    atomic_write(page, render(d, args.date))
    return finish({"ok": True, "written": True, "page": rel,
                   "reason": f"the model had no page; written from issue #{d['issue']}"}, 0)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
