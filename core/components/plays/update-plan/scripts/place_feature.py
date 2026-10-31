#!/usr/bin/env python3
"""place_feature.py — place each new feature of a draft by fixed rules (C11, C9).

    python3 place_feature.py --draft <draft-entries.json> --plan-file <plans>/<id>.yaml \
        --spine <product_base>product-os/_spine.yaml --plan <id> [--suggestion <routing-result.json>]

For each `new-feature` entry of the draft it fills in, and writes back into the draft:
  - `capability`: the one the entry names (the person said it) when it is in the spine; else the
    spine capability whose `issue` is the issue of the entry's parent in the plan, or of an item
    above it (a feature item and its capability share an issue number); else none — and a
    question asks which capability, with the placement skill's suggestion when --suggestion
    names one;
  - `slice`: the spine slices whose `intents` hold `bi-<id>`: none → null (a slice is owed);
    one → that slice, shown to the person at the confirm screen; several → none, and a question
    names them;
  - `slice_in_progress`: when that slice's epic is past ready (in_delivery, validated,
    fix_required or delivered — the rule /shape-slice uses, ADR 058), each such epic with its
    issue and status; the confirm screen says the slice is in progress and names the epic as out
    of date (ADR 062). Else an empty list;
  - `feature`: `fn-<issue>` when the story exists, else `fn-<slug of the title>`, never one the
    spine has;
  - `one_line`: the title, as the person gave it.
No ICE is drafted here: the page skill writes the thin ICE at the landing, from the person's
words. The script makes no judgment: what it cannot settle by a rule becomes a question for
the person, in the four parts of `_shared/asking-a-person.md` (question, answer, why, examples).
Its questions go in the draft's `placement_questions`, which it owns and replaces on every run,
so a second run (with --suggestion) never repeats a question; the skill's own `questions` are
left as they are. Exit 0 written; 2 bad input. Reads the plan file and the spine only.
"""

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_session as ps  # noqa: E402


def slug(text):
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return "-".join(s.split("-")[:6]) or "feature"


def chain(plan, issue):
    """The issue numbers from the item up to the top of the plan."""
    out, current = [], issue
    while current is not None:
        node, parent = ps.find(plan, current)
        if node is None:
            break
        out.append(str(node.get("issue")))
        current = parent.get("issue") if parent else None
    return out


IN_PROGRESS = ("in_delivery", "validated", "fix_required", "delivered")  # past ready (ADR 058)

EXAMPLES = ["a clinic: 'Send a reminder' goes under the capability that books visits",
            "a shop: 'Save a wish list' goes under the capability that keeps a basket",
            "a bank: 'Freeze a card' goes under the capability that manages cards"]


def ask(question, answer, why):
    return {"question": question, "answer": answer, "why": why, "examples": EXAMPLES}


def place(entry, plan, spine, plan_id, suggestion):
    questions = []
    entry.setdefault("capability", None)
    entry.setdefault("slice", None)
    caps = {c.get("id"): c for c in spine.get("capabilities") or []}
    by_issue = {str(c.get("issue")): c.get("id") for c in caps.values() if c.get("issue") is not None}
    title = entry.get("title") or ""
    named = entry.get("capability")
    if named and named not in caps:
        entry["capability"] = None
    if not entry.get("capability"):
        for issue in chain(plan, entry.get("parent")):
            if issue in by_issue:
                entry["capability"] = by_issue[issue]
                break
    if named and named not in caps:
        found = f" Its parent in the plan points to {entry['capability']}." if entry["capability"] else ""
        questions.append(ask(f"Which capability does the new feature '{title}' belong under?",
                             f"'{named}' is not a capability in the model.{found}",
                             "The feature's page is written under that capability, and the wrong one puts it "
                             "where the people who use that part of the product will not look for it."))
    elif not entry.get("capability"):
        answer = (f"Proposed: {suggestion} (the placement skill's suggestion)." if suggestion
                  else "No answer yet: its parent in the plan names no capability.")
        questions.append(ask(f"Which capability does the new feature '{title}' belong under?", answer,
                             "The feature's page is written under that capability, and nothing lands until "
                             "it has one."))
    intent = f"bi-{plan_id}"
    slices = [s.get("id") for s in spine.get("slices") or [] if intent in (s.get("intents") or [])]
    if entry.get("slice") and entry["slice"] not in slices:
        entry["slice"] = None
    if not entry.get("slice"):
        if len(slices) == 1:
            entry["slice"] = slices[0]
        elif len(slices) > 1:
            questions.append(ask(f"Which slice does the new feature '{title}' join?",
                                 "No answer yet: these slices serve the plan's business intent: "
                                 + ", ".join(slices) + ".",
                                 "The feature is built and tested with that slice; in the wrong one its "
                                 "tester never reaches it."))
    entry["slice_in_progress"] = [
        {"epic": e.get("issue_ref") or e.get("id"), "status": e.get("status")}
        for e in spine.get("epics") or []
        if isinstance(e, dict) and entry.get("slice") and e.get("slice_ref") == entry["slice"]
        and e.get("status") in IN_PROGRESS]
    taken = {f.get("id") for f in spine.get("features") or []}
    feature = f"fn-{entry['issue']}" if entry.get("issue") is not None else f"fn-{slug(title)}"
    base, n = feature, 2
    while feature in taken:
        feature = f"{base}-{n}"
        n += 1
    entry["feature"] = feature
    entry["one_line"] = entry.get("one_line") or title
    entry.pop("ice", None)
    return questions


def main(argv=None):
    ap = argparse.ArgumentParser(description="place each new feature of a draft by fixed rules")
    ap.add_argument("--draft", required=True)
    ap.add_argument("--plan-file", required=True)
    ap.add_argument("--spine", required=True)
    ap.add_argument("--plan", required=True)
    ap.add_argument("--suggestion")
    args = ap.parse_args(argv)
    try:
        draft = ps.read_json(args.draft, "draft-entries.json")
        plan = ps.load_plan(args.plan_file)
        if not os.path.isfile(args.spine):
            raise ps.Refused(f"no model index at {args.spine}")
        spine = ps.yaml.safe_load(ps.read_text(args.spine)) or {}
        suggestion = None
        if args.suggestion and os.path.isfile(args.suggestion):
            route = ps.read_json(args.suggestion, "routing-result.json")
            route = route.get("routing_result", route)
            best = (route.get("placements") or [{}])[0]
            suggestion = best.get("capability")
    except (ps.Refused, ps.yaml.YAMLError) as e:
        print(f"refused: {e}", file=sys.stderr)
        return 2
    asked = []
    for entry in draft.get("entries") or []:
        if entry.get("op") == "new-feature":
            asked += place(entry, plan, spine, args.plan, suggestion)
    draft["placement_questions"] = asked
    ps.write_json(args.draft, draft)
    return 0


if __name__ == "__main__":
    sys.exit(main())
