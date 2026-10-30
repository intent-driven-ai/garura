#!/usr/bin/env python3
"""check_agreement.py — after the landing, the plan file, the tracker and the model agree (C6, C7, C11).

    python3 check_agreement.py --changes <changes.yaml> --plan-before <plan-before.yaml> \
        --plan-file <plans>/<id>.yaml --snapshot-before <snapshot-before.json> \
        --snapshot-after <snapshot-after.json> --github-record <github-record.json> \
        [--model-record <model-record.json> ...] [--spine <_spine.yaml>] \
        [--evals-before <evals-before.json>] [--evals-after <evals-after.json>] \
        --out <agreement.json>
    python3 check_agreement.py hash-evals --plans-dir <plans> --out <evals.json>

For each item the list names (its number from the tracker record for a new one):
  - the plan file's status and the tracker agree: Done is closed as completed, Dropped is closed
    as not planned, every other status is open;
  - the plan file's title is the tracker's title;
  - the item's parent in the plan file is its parent in the tracker (an item at the top of the
    plan has the plan's business intent as its parent);
  - the tracker type is its kind's type, after an add or a kind change;
  - after a text change, the tracker's text is the new text.
Nothing else changed: every node and every top field of the plan file that the list does not name
reads as before (`updated` aside), and every issue of the snapshot that the list does not name
reads as before in the tracker. For a new feature: the model record names its page and its
entry, the spine has the feature with `metadata.thin: true` and its story's issue, its page has
the Thin line, and its story's node stands for it (`features_ok`). The evals folders hash as
before (`evals_unchanged`). The overrides and what is owed are named in the landing's commit
message (commit_plan.py), not here.

Output: {ok, problems: [..], features_ok, evals_unchanged, checked: [..]}.
Exit 0 ok; 1 not ok (written); 2 bad input. Reads only.
"""

import argparse
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_session as ps  # noqa: E402

THIN_PREFIX = "Thin: "


def hash_evals(plans_dir):
    out = {}
    for path in sorted(glob.glob(os.path.join(plans_dir, "*", "evals", "**", "*"), recursive=True)):
        if os.path.isfile(path):
            out[os.path.relpath(path, plans_dir)] = ps.sha256_of(path)
    return out


def node_parent(plan, issue, plan_id):
    node, parent = ps.find(plan, issue)
    if node is None:
        return None, None
    return node, (int(parent["issue"]) if parent else int(plan_id))


def check(args):
    changes = ps.load_list(args.changes) or {}
    plan_id = str(changes.get("plan"))
    before = ps.load_plan(args.plan_before)
    after = ps.load_plan(args.plan_file)
    snap0 = ps.read_json(args.snapshot_before, "the snapshot before")
    snap1 = ps.read_json(args.snapshot_after, "the snapshot after")
    rec = ps.read_json(args.github_record, "the tracker record") if os.path.isfile(args.github_record) else {"done": {}}
    problems = []
    numbers = {}
    for e in changes.get("entries") or []:
        made = (rec.get("done") or {}).get(f"{e['n']}-create")
        numbers[e["n"]] = made["result"] if made else e.get("issue")
    named = {str(numbers[e["n"]]) for e in changes.get("entries") or [] if numbers.get(e["n"]) is not None}
    issues1 = snap1.get("issues") or {}

    for e in changes.get("entries") or []:
        n = numbers.get(e["n"])
        if n is None:
            continue
        node, parent = node_parent(after, n, plan_id)
        if node is None:
            problems.append(f"#{n} (entry {e['n']}) is not in the plan file")
            continue
        now = issues1.get(str(n))
        if now is None:
            problems.append(f"#{n} was not read back from the tracker")
            continue
        status = node.get("status")
        if status in ps.CLOSED:
            want = ps.REASON_OF[ps.CLOSED[status]]
            if now["state"] != "CLOSED" or now.get("state_reason") != want:
                problems.append(f"#{n} is {status} in the plan file but {now['state'].lower()}"
                                f" ({now.get('state_reason') or 'no reason'}) in the tracker")
        elif now["state"] != "OPEN":
            problems.append(f"#{n} is {status} in the plan file but closed in the tracker")
        if now["title"] != node.get("title"):
            problems.append(f"#{n}'s title differs: plan file '{node.get('title')}', tracker '{now['title']}'")
        if e["op"] in ("add", "move", "new-feature") and str(now.get("parent")) != str(parent):
            problems.append(f"#{n}'s parent is #{parent} in the plan file but #{now.get('parent')} in the tracker")
        if e["op"] in ("add", "kind") and now.get("type") != ps.TYPES.get(node.get("kind")):
            problems.append(f"#{n} is a {node.get('kind')} in the plan file but type {now.get('type')} in the tracker")
        if e["op"] == "text" and now.get("body") != e.get("body"):
            problems.append(f"#{n}'s text is not the approved text")

    # Nothing else changed: the plan file.
    before_nodes = {str(nd.get("issue")): nd for nd, _ in ps.walk(before.get("tree"))}
    after_nodes = {str(nd.get("issue")): nd for nd, _ in ps.walk(after.get("tree"))}

    def flat(nd):
        return {k: v for k, v in nd.items() if k != "children"}

    for issue, nd in before_nodes.items():
        if issue in named:
            continue
        if issue not in after_nodes:
            problems.append(f"#{issue} left the plan file, but the list does not name it")
        elif flat(nd) != flat(after_nodes[issue]):
            problems.append(f"#{issue} changed in the plan file, but the list does not name it")
    for issue in after_nodes:
        if issue not in before_nodes and issue not in named:
            problems.append(f"#{issue} joined the plan file, but the list does not name it")
    plan_ops = {e["op"] for e in changes.get("entries") or []}
    for key in set(before) | set(after):
        if key in ("tree", "updated"):
            continue
        if key == "status" and "plan-status" in plan_ops or key == "direction" and "plan-direction" in plan_ops:
            continue
        if before.get(key) != after.get(key):
            problems.append(f"the plan's '{key}' changed, but the list does not name it")
    # Nothing else changed: the tracker.
    for issue, was in (snap0.get("issues") or {}).items():
        if issue in named:
            continue
        now = issues1.get(issue)
        keys = ("title", "state", "state_reason", "type", "body", "parent")
        if now is not None and any(was.get(k) != now.get(k) for k in keys):
            problems.append(f"#{issue} changed in the tracker, but the list does not name it")

    features = [e for e in changes.get("entries") or [] if e["op"] == "new-feature"]
    features_ok = True
    if features:
        model = ps.model_records(args.model_record)
        spine = ps.yaml.safe_load(ps.read_text(args.spine)) if args.spine else {}
        by_id = {f.get("id"): f for f in (spine or {}).get("features") or []}
        for e in features:
            f = by_id.get(e["feature"])
            node, _ = ps.find(after, numbers.get(e["n"]))
            page = os.path.join(os.path.dirname(args.spine), f["doc"]) if f and f.get("doc") else None
            ok = (f is not None and (f.get("metadata") or {}).get("thin") is True
                  and page and os.path.isfile(page)
                  and any(ln.startswith(THIN_PREFIX) for ln in ps.read_text(page).splitlines())
                  and str(f.get("issue")) == str(numbers.get(e["n"]))
                  and node is not None and node.get("represents") == e["feature"]
                  and e["feature"] in [p.get("feature") for p in model.get("parts") or []])
            if not ok:
                features_ok = False
                problems.append(f"the new feature {e['feature']} is not whole: its page, its thin marks, "
                                "its entry or its story is missing")
    evals_unchanged = True
    if args.evals_before and args.evals_after:
        evals_unchanged = ps.read_json(args.evals_before, "evals before") == ps.read_json(args.evals_after, "evals after")
        if not evals_unchanged:
            problems.append("the evals folder changed")
    return {"ok": not problems, "problems": problems, "features_ok": features_ok, "evals_unchanged": evals_unchanged,
            "checked": sorted(int(i) for i in named)}


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if argv and argv[0] == "hash-evals":
        ap = argparse.ArgumentParser()
        ap.add_argument("cmd")
        ap.add_argument("--plans-dir", required=True)
        ap.add_argument("--out", required=True)
        a = ap.parse_args(argv)
        ps.write_json(a.out, hash_evals(a.plans_dir))
        return 0
    ap = argparse.ArgumentParser(description="check the plan file, the tracker and the model agree")
    for name in ("--changes", "--plan-before", "--plan-file", "--snapshot-before", "--snapshot-after",
                 "--github-record", "--out"):
        ap.add_argument(name, required=True)
    ap.add_argument("--model-record", action="append", default=[])
    for name in ("--spine", "--evals-before", "--evals-after"):
        ap.add_argument(name)
    args = ap.parse_args(argv)
    try:
        out = check(args)
    except (ps.Refused, KeyError, TypeError) as e:
        print(f"refused: {e}", file=sys.stderr)
        return 2
    ps.write_json(args.out, out)
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
