#!/usr/bin/env python3
"""check_plan.py — deterministic check of a plan file (#619).

Reads one plan written in the canonical plan format
(memory/standards/templates/work-plan.md) and reports two things:

  valid  — the plan follows the format: front matter fields, the required
           sections, a "now" item that exists and is marked, and every open
           item explains itself (a What line).
  linked — a plan that names `serves_plan` / `serves_item` points at a parent
           plan that exists and names this issue as a whole token (`#619`,
           never a prefix of `#6190`). When the parent's item `serves_item` is
           open, that item must name this issue; when it is finished, the
           Done line numbered `**N.**` must. A business
           intent's plan names no parent (#619 P9).
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


def issue_ref(number):
    """Match '#619' as a whole token — not '#6190', not 'x#619'."""
    return re.compile(rf"(?<![\w#])#{re.escape(str(number))}(?!\d)")


def read_text(path):
    """Read a plan as UTF-8; raise OSError or UnicodeDecodeError when unreadable."""
    with open(path, encoding="utf-8") as fh:
        return fh.read()


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


DONE_NUM_RE = re.compile(r"^\s*-\s*\*\*(\d+)\.\s")


def done_lines(body):
    """The lines under '### Done' inside 'The plan, in order'."""
    out, in_plan, in_done = [], False, False
    for line in body.splitlines():
        if line.startswith("## "):
            in_plan, in_done = line[3:].strip() == "The plan, in order", False
            continue
        if in_plan and line.startswith("### "):
            in_done = line[4:].strip() == "Done"
            continue
        if in_done:
            out.append(line)
    return out


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
    try:
        parent_text = read_text(parent_path)
    except (OSError, UnicodeDecodeError) as exc:
        problems.append(f"serves_plan={parent}: parent plan unreadable ({exc.__class__.__name__})")
        return parent_path
    ref = issue_ref(fields.get("plan_for", ""))
    if not ref.search(parent_text):
        problems.append(f"the plan for #{parent} does not name #{fields.get('plan_for')}")
        return parent_path
    _, parent_body = parse_front_matter(parent_text)
    parent_body = parent_body or ""
    open_item = next((it for it in split_items(parent_body) if it["number"] == int(item)), None)
    if open_item is not None:
        block = open_item["title"] + "\n" + "\n".join(open_item["lines"])
        if not ref.search(block):
            problems.append(f"serves_item={item}: item {item} of the plan for #{parent} "
                            f"does not name #{fields.get('plan_for')}")
    else:
        finished = {int(m.group(1)): line for line in done_lines(parent_body)
                    if (m := DONE_NUM_RE.match(line))}
        if int(item) not in finished:
            problems.append(f"serves_item={item}: the plan for #{parent} has no item {item}, "
                            f"open or finished (finished items keep their number: `**{item}. …**`)")
        elif not ref.search(finished[int(item)]):
            problems.append(f"serves_item={item}: finished item {item} of the plan for #{parent} "
                            f"does not name #{fields.get('plan_for')}")
    return parent_path


def check(text, plan_path=None):
    problems = []
    fields, body = parse_front_matter(text)
    if fields is None:
        return {"valid": False, "done": False, "status": None, "now": None,
                "open_items": [], "serves_plan": None, "problems": ["no front matter"]}

    for f in REQUIRED_FIELDS:
        if not fields.get(f):
            problems.append(f"front matter: missing `{f}`")
    status = fields.get("status", "")
    if status and status not in STATUSES:
        problems.append(f"front matter: status `{status}` is not one of {sorted(STATUSES)}")
    kind = fields.get("kind", "")
    if kind and kind not in KINDS:
        problems.append(f"front matter: kind `{kind}` is not one of {sorted(KINDS)}")

    headings = {line[3:].strip() for line in body.splitlines() if line.startswith("## ")}
    for section in REQUIRED_SECTIONS:
        if section not in headings:
            problems.append(f"missing section: ## {section}")

    items = split_items(body)
    open_items = [it["number"] for it in items]
    marked = [it["number"] for it in items if NOW_MARK.search(it["title"])]

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

    for it in items:
        if not any(line.startswith("**What:**") for line in it["lines"]):
            problems.append(f"item {it['number']} has no **What:** line — every item must explain itself")

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
        text = read_text(args.plan)
    except (OSError, UnicodeDecodeError) as exc:
        print(json.dumps({"error": f"{exc.__class__.__name__}: {exc}", "plan": args.plan}))
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
