#!/usr/bin/env python3
"""check_plan.py — deterministic check of a plan file (#619).

Reads one plan written in the canonical plan format
(memory/standards/templates/plan.md) and reports two things:

  valid  — the plan follows the format: front matter fields, the required
           sections, a "now" item that exists and is marked, and every open
           item explains itself (a What line).
  linked — a plan that names `serves_plan` / `serves_item` points at a parent
           plan that exists and mentions this issue (#619 P9). A business
           intent's plan names no parent.
  done   — the plan is finished: status is `done` (or `dropped`) and no open
           numbered item is left. Finished items live under "### Done".

No git, no network, no LLM. Same file in, same answer out.

Usage:
    python3 check_plan.py --plan <path to plan.md> [--out <report.json>]

Exit codes: 0 valid and done · 1 valid, not done · 2 not valid · 3 unreadable.
"""
import argparse
import json
import os
import re
import sys

REQUIRED_FIELDS = ["plan_for", "kind", "serves", "status", "updated", "now"]
STATUSES = {"active", "done", "dropped"}
KINDS = {"business-intent", "feature", "story", "bug", "spike", "chore", "drive", "play"}
REQUIRED_SECTIONS = [
    "What we are trying to reach",
    "When this plan is done",
    "Where we are now",
    "The plan, in order",
    "Log",
]
ITEM_RE = re.compile(r"^###\s+(\d+)\.\s+(.*)$")
NOW_MARK = re.compile(r"[—-]\s*now\s*$", re.IGNORECASE)


def parse_front_matter(text):
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    fields = {}
    for line in text[3:end].strip().splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            fields[key.strip()] = val.strip().strip('"')
    return fields, text[end + 4:]


def split_items(body):
    """Return the numbered items in 'The plan, in order' with their text."""
    items, current = [], None
    in_plan = False
    for line in body.splitlines():
        if line.startswith("## "):
            in_plan = line[3:].strip() == "The plan, in order"
            if current:
                items.append(current)
                current = None
            continue
        if not in_plan:
            continue
        m = ITEM_RE.match(line)
        if m:
            if current:
                items.append(current)
            current = {"number": int(m.group(1)), "title": m.group(2).strip(), "lines": []}
        elif line.startswith("### "):
            if current:
                items.append(current)
            current = None
        elif current is not None:
            current["lines"].append(line)
    if current:
        items.append(current)
    return items


def check_parent(fields, plan_path, problems):
    """P9: follow serves_plan up one level. Plans live at {stm}/{n}/specs/plan.md."""
    parent, item = fields.get("serves_plan", ""), fields.get("serves_item", "")
    kind = fields.get("kind", "")
    if kind == "business-intent":
        if parent or item:
            problems.append("a business intent's plan serves no parent: drop serves_plan / serves_item")
        return None
    if not parent and not item:
        return None  # allowed while plans are adopted; the skill always writes them
    if not (parent.isdigit() and item.isdigit()):
        problems.append("serves_plan and serves_item must both be numbers")
        return None
    if plan_path is None:
        return None
    stm = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(plan_path))))
    parent_path = os.path.join(stm, parent, "specs", "plan.md")
    if not os.path.isfile(parent_path):
        problems.append(f"serves_plan={parent}: no plan at {parent_path}")
        return parent_path
    if f"#{fields.get('plan_for', '')}" not in open(parent_path, encoding="utf-8").read():
        problems.append(f"the plan for #{parent} does not mention #{fields.get('plan_for')}")
    return parent_path


def check(text, plan_path=None):
    problems = []
    fields, body = parse_front_matter(text)
    if fields is None:
        return {"valid": False, "done": False, "problems": ["no front matter"], "open_items": [], "now": None}

    for f in REQUIRED_FIELDS:
        if not fields.get(f):
            problems.append(f"front matter: missing `{f}`")
    status = fields.get("status", "")
    if status and status not in STATUSES:
        problems.append(f"front matter: status `{status}` is not one of {sorted(STATUSES)}")
    kind = fields.get("kind", "")
    if kind and kind not in KINDS:
        problems.append(f"front matter: kind `{kind}` is not one of {sorted(KINDS)}")

    headings = {l[3:].strip() for l in body.splitlines() if l.startswith("## ")}
    for s in REQUIRED_SECTIONS:
        if s not in headings:
            problems.append(f"missing section: ## {s}")

    items = split_items(body)
    open_items = [i["number"] for i in items]
    marked = [i["number"] for i in items if NOW_MARK.search(i["title"])]

    now = fields.get("now", "")
    if status == "active":
        if not now.isdigit():
            problems.append("front matter: `now` must be an item number while the plan is active")
        elif int(now) not in open_items:
            problems.append(f"front matter: now={now} points at no open item")
        if len(marked) != 1:
            problems.append(f"exactly one item heading must end with '— now' (found {len(marked)})")
        elif now.isdigit() and marked[0] != int(now):
            problems.append(f"front matter now={now} but the '— now' heading is item {marked[0]}")

    for i in items:
        if not any(l.startswith("**What:**") for l in i["lines"]):
            problems.append(f"item {i['number']} has no **What:** line — every item must explain itself")

    parent_path = check_parent(fields, plan_path, problems)

    valid = not problems
    done = valid and status in {"done", "dropped"} and not open_items
    if valid and status in {"done", "dropped"} and open_items:
        problems.append(f"status is `{status}` but items {open_items} are still open")
        valid, done = False, False

    return {"valid": valid, "done": done, "status": status, "now": now or None,
            "open_items": open_items, "serves_plan": parent_path, "problems": problems}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True)
    ap.add_argument("--out")
    args = ap.parse_args()
    try:
        text = open(args.plan, encoding="utf-8").read()
    except OSError as exc:
        print(json.dumps({"error": str(exc)}))
        return 3
    report = check(text, args.plan)
    report["plan"] = args.plan
    out = json.dumps(report, indent=2)
    print(out)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(out + "\n")
    if not report["valid"]:
        return 2
    return 0 if report["done"] else 1


if __name__ == "__main__":
    sys.exit(main())
