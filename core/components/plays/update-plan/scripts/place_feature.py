#!/usr/bin/env python3
"""place_feature.py — place each new feature of a draft by fixed rules (C11, C9).

    python3 place_feature.py --draft <draft-entries.json> --plan-file <plans>/<id>.yaml \
        --spine <product_base>product-os/_spine.yaml --plan <id> [--suggestion <routing-result.json>]

For each `new-feature` entry of the draft it fills in, and writes back into the draft:
  - `capability`: the one the entry names (the person said it) when it is in the spine; else the
    spine capability whose `issue` is the issue of the entry's parent in the plan, or of an item
    above it (a feature item and its capability share an issue number); else none — and a
    question goes into the draft's `questions` ("Which capability does it belong under?"),
    with the placement skill's suggestion when --suggestion names one;
  - `slice`: the spine slices whose `intents` hold `bi-<id>`: none → null (a slice is owed);
    one → that slice, shown to the person at the confirm screen; several → none, and a question
    names them;
  - `feature`: `fn-<issue>` when the story exists, else `fn-<slug of the title>`, never one the
    spine has;
  - `one_line`: the title, as the person gave it.
No ICE is drafted here: the page skill writes the thin ICE at the landing, from the person's
words. The script makes no judgment: what it cannot settle by a rule becomes a question for
the person. Exit 0 written; 2 bad input. Reads the plan file and the spine only.
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


def place(entry, plan, spine, plan_id, suggestion):
    questions = []
    entry.setdefault("capability", None)
    entry.setdefault("slice", None)
    caps = {c.get("id"): c for c in spine.get("capabilities") or []}
    by_issue = {str(c.get("issue")): c.get("id") for c in caps.values() if c.get("issue") is not None}
    title = entry.get("title") or ""
    if entry.get("capability") and entry["capability"] not in caps:
        questions.append(f"'{entry['capability']}' is not a capability in the model. Which capability "
                         f"does '{title}' belong under?")
        entry["capability"] = None
    if not entry.get("capability"):
        for issue in chain(plan, entry.get("parent")):
            if issue in by_issue:
                entry["capability"] = by_issue[issue]
                break
    if not entry.get("capability") and not questions:
        hint = f" The placement skill suggests: {suggestion}." if suggestion else ""
        questions.append(f"Which capability does '{title}' belong under? Its parent in the plan names "
                         f"none.{hint}")
    intent = f"bi-{plan_id}"
    slices = [s.get("id") for s in spine.get("slices") or [] if intent in (s.get("intents") or [])]
    if entry.get("slice") and entry["slice"] not in slices:
        entry["slice"] = None
    if not entry.get("slice"):
        if len(slices) == 1:
            entry["slice"] = slices[0]
        elif len(slices) > 1:
            questions.append(f"Which slice does '{title}' join: " + ", ".join(slices) + "?")
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
    for entry in draft.get("entries") or []:
        if entry.get("op") == "new-feature":
            draft.setdefault("questions", []).extend(place(entry, plan, spine, args.plan, suggestion))
    ps.write_json(args.draft, draft)
    return 0


if __name__ == "__main__":
    sys.exit(main())
