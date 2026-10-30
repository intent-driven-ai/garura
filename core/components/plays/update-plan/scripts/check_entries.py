#!/usr/bin/env python3
"""check_entries.py — check each drafted entry against the plan's rules before it joins the list (C3, C4, C8).

    python3 check_entries.py --draft <draft-entries.json> --plan-file <plans>/<id>.yaml \
        --snapshot <snapshot.json> --changes <changes.yaml> --view-template <plan-view.md> \
        --out <checked.json>

For each entry of the draft (author-plan-changes) it fills in what the draft leaves out — the
old value from the plan file and the tracker, the item's kind and parent — and decides, by fixed
rules only:

  - `problem` and `fix`: the entry breaks a rule, and what works instead. The rules: a kind the
    plan may hold (epic, feature, story, spike, chore, bug); a parent of the right kind (an epic
    at the top; a feature under an epic; a story under an epic or a feature; a spike, a chore or
    a bug under a story); a status the plan knows; an item that is in the plan (or, for `add`,
    is not); an issue the tracker has; no labels on an issue that joins the plan; a parent that
    is not the item itself or under it; a title that is not empty; one story for each feature in
    an epic. `fix` names up to three open items of a kind that works, near the parent asked for.
  - `big` and `big_why`: dropping an epic, moving a feature, a new feature (a model change), or
    closing an item with open work under it (work the list or the draft closes counts as closed). A big entry is shown and confirmed first.
  - `already`: the entry changes nothing (the item already reads so); it is not added.
  - `where`: what the landing will write — on GitHub (close as completed, close as not
    planned, reopen, a new issue, parent, title, text, type) and in the model (thin page, index,
    slice).
An issue the snapshot does not hold is listed in `unknown_issues`: the play has it read and runs
the check again. No status or direction is ever added that the draft does not name (no roll-ups).

Output: {"entries": [...], "questions": [...], "unknown_issues": [...]}.
Exit 0 written; 2 bad input (nothing written). No git, no network.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_session as ps  # noqa: E402


def a(kind):
    return ("an " if kind and kind[0] in "aeiou" else "a ") + str(kind)


def open_status(status):
    return status not in ps.CLOSED


def near(plan, parent_issue, kinds, skip, pending=None):
    """Open items of the given kinds near the parent asked for: its own line, then its children."""
    out = []
    node, _ = ps.find(plan, parent_issue) if parent_issue is not None else (None, None)
    pool = []
    if node is not None:
        chain, at = [], node
        while at is not None:
            chain.append(at)
            at = ps.find(plan, at.get("issue"))[1]
        pool = chain + ps.descendants(node)
    else:
        pool = [n for n, _ in ps.walk(plan.get("tree"))]
    for n in pool:
        status = (pending or {}).get(str(n.get("issue")), n.get("status"))
        if n.get("kind") in kinds and open_status(status) and n.get("issue") not in skip:
            if all(o["issue"] != n.get("issue") for o in out):
                out.append({"issue": n.get("issue"), "title": n.get("title")})
        if len(out) == 3:
            break
    return out


def fix_text(cands, kinds):
    if not cands:
        return "put it under " + " or ".join(a(k) for k in kinds if k) if any(kinds) else "put it at the top"
    return "put it under " + " or ".join(f"#{c['issue']} ({c['title']})" for c in cands)


def check(entry, plan, snap, items, plan_statuses, directions, listed, pending):
    e = dict(entry)
    e.update({"problem": None, "fix": None, "big": False, "big_why": None, "already": False,
              "status_now": "Not Started", "where": {"github": [], "model": []}})
    op = e.get("op")
    issues = snap.get("issues") or {}
    unknown = []

    def tracker(n):
        if n is None:
            return None
        got = issues.get(str(n))
        if got is None:
            unknown.append(int(n))
        return got

    def broke(problem, fix=None):
        if e["problem"] is None:
            e["problem"], e["fix"] = problem, fix

    def parent_rule(kind, parent_issue, skip=()):
        allowed = ps.PARENTS.get(kind, ())
        if parent_issue is None:
            pkind = None
        else:
            pnode, _ = ps.find(plan, parent_issue)
            pkind = pnode.get("kind") if pnode is not None else ("new" if str(parent_issue) in listed else None)
            if pnode is None and pkind is None:
                broke(f"#{parent_issue} is not in this plan", "name a parent that is in the plan")
                return
            if pkind == "new":
                pkind = listed[str(parent_issue)]
        if pkind not in allowed:
            where = "at the top of the plan" if pkind is None else f"under {a(pkind)}"
            want = " or ".join("the top of the plan" if k is None else a(k) for k in allowed)
            broke(f"{a(kind)} does not sit {where}; it sits under {want}",
                  fix_text(near(plan, parent_issue, [k for k in allowed if k], skip, pending), allowed))

    if op in ("status", "move", "retitle", "text", "kind"):
        node, parent = ps.find(plan, e.get("issue"))
        if node is None:
            broke(f"#{e.get('issue')} is not in this plan", "add it first, with its parent")
            return e, unknown
        e["title"], e["kind"], e["status_now"] = node.get("title"), node.get("kind"), node.get("status")
        now = tracker(e["issue"])
    if op == "status":
        e["from"] = node.get("status")
        if e.get("to") not in items:
            broke(f"'{e.get('to')}' is not a status of an item", "use one of: " + ", ".join(items))
        elif e["to"] == e["from"]:
            e["already"] = True
        else:
            if e["to"] in ps.CLOSED:
                want = ps.REASON_OF[ps.CLOSED[e["to"]]]
                if not now or now["state"] != "CLOSED" or now.get("state_reason") != want:
                    e["where"]["github"].append("close-completed" if e["to"] == "Done" else "close-not-planned")
                open_under = [d for d in ps.descendants(node)
                              if open_status(pending.get(str(d.get("issue")), d.get("status")))]
                if node.get("kind") == "epic" and e["to"] == "Dropped":
                    e["big"], e["big_why"] = True, "it drops an epic"
                elif open_under:
                    e["big"] = True
                    e["big_why"] = "open work stays under it: " + ", ".join(f"#{d.get('issue')}" for d in open_under[:5])
            elif now and now["state"] == "CLOSED":
                e["where"]["github"].append("reopen")
    elif op == "add":
        kind = e.get("kind")
        if kind not in ps.KINDS:
            broke(f"'{kind}' is not a kind a plan holds", "use one of: " + ", ".join(ps.KINDS))
        if e.get("issue") is not None:
            if ps.find(plan, e["issue"])[0] is not None:
                broke(f"#{e['issue']} is already in this plan", "move it instead")
            now = tracker(e["issue"])
            if now:
                e["title"] = now["title"]
                if now.get("labels"):
                    broke(f"#{e['issue']} has labels ({', '.join(now['labels'])}); an item in a plan has none",
                          "take the labels off first")
                if now.get("type") != ps.TYPES.get(kind):
                    e["where"]["github"].append("type")
                if str(now.get("parent")) != str(e.get("parent")):
                    e["where"]["github"].append("parent")
        else:
            if not (e.get("title") or "").strip():
                broke("a new item needs a title", "give its title")
            e["where"]["github"].append("create")
        if kind in ps.KINDS:
            parent_rule(kind, e.get("parent"))
    elif op == "move":
        e["from"] = parent.get("issue") if parent else None
        to = e.get("to")
        if str(to) == str(e["issue"]) or any(str(d.get("issue")) == str(to) for d in ps.descendants(node)):
            broke(f"#{e['issue']} cannot sit under itself or under its own work", None)
        elif str(to) == str(e["from"]):
            e["already"] = True
        else:
            parent_rule(node.get("kind"), to, skip=(e["issue"],))
            e["where"]["github"].append("parent")
            if node.get("kind") == "feature":
                e["big"], e["big_why"] = True, "it moves a feature to another place in the plan"
    elif op == "retitle":
        e["from"] = node.get("title")
        if not (e.get("to") or "").strip():
            broke("a title cannot be empty", "give the new title")
        elif e["to"] == e["from"] and (not now or now["title"] == e["to"]):
            e["already"] = True
        else:
            e["where"]["github"].append("title")
    elif op == "text":
        if not (e.get("body") or "").strip():
            broke("the new text is empty", "give the new text")
        elif now and now["body"] == e["body"]:
            e["already"] = True
        else:
            e["where"]["github"].append("body")
    elif op == "kind":
        e["from"] = node.get("kind")
        if e.get("to") not in ps.KINDS:
            broke(f"'{e.get('to')}' is not a kind a plan holds", "use one of: " + ", ".join(ps.KINDS))
        elif e["to"] == e["from"]:
            e["already"] = True
        else:
            parent_rule(e["to"], parent.get("issue") if parent else None, skip=(e["issue"],))
            for d in node.get("children") or []:
                if e["to"] not in ps.PARENTS.get(d.get("kind"), ()):
                    broke(f"#{d.get('issue')} ({a(d.get('kind'))}) could not sit under {a(e['to'])}", None)
            e["where"]["github"].append("type")
    elif op == "new-feature":
        e["kind"] = "story"
        e["big"], e["big_why"] = True, "it adds a feature to the product model"
        if not (e.get("title") or "").strip():
            broke("a new feature needs a title", "give its title")
        if e.get("issue") is not None:
            node, _ = ps.find(plan, e["issue"])
            now = tracker(e["issue"])
            if node is not None and node.get("represents"):
                broke(f"#{e['issue']} already stands for {node.get('represents')}", None)
            e["where"]["github"].append("body")
            if node is None or (now and str(now.get("parent")) != str(e.get("parent"))):
                e["where"]["github"].append("parent")
        else:
            e["where"]["github"].append("create")
        parent_rule("story", e.get("parent"))
        feature = e.get("feature")
        epic = e.get("parent")
        if feature and epic is not None:
            pnode, _ = ps.find(plan, epic)
            if pnode is not None and any(d.get("represents") == feature for d in ps.descendants(pnode)):
                broke(f"{feature} already has a story under #{epic}; one story for each feature", None)
        e["where"]["model"] = ["model-page", "model-index"] + (["model-slice"] if e.get("slice") else [])
    elif op == "plan-status":
        e["from"] = plan.get("status")
        if e.get("to") not in plan_statuses:
            broke(f"'{e.get('to')}' is not a status of a plan", "use one of: " + ", ".join(plan_statuses))
        elif e["to"] == e["from"]:
            e["already"] = True
    elif op == "plan-direction":
        e["from"] = plan.get("direction")
        to = e.get("to")
        if to is not None and to not in directions:
            broke(f"'{to}' is not a direction", "use 1, 2, 3 or none")
        elif to == e["from"]:
            e["already"] = True
    elif op not in ("status", "move", "retitle", "text", "kind"):
        broke(f"'{op}' is not a change a session makes", None)
    return e, unknown


def main(argv=None):
    ap = argparse.ArgumentParser(description="check drafted entries against the plan's rules")
    ap.add_argument("--draft", required=True)
    ap.add_argument("--plan-file", required=True)
    ap.add_argument("--snapshot", required=True)
    ap.add_argument("--changes", required=True)
    ap.add_argument("--view-template", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        draft = ps.read_json(args.draft, "draft-entries.json")
        plan = ps.load_plan(args.plan_file)
        snap = ps.read_json(args.snapshot, "snapshot.json")
        items, _, plan_statuses, directions = ps.statuses(ps.load_block(args.view_template, "plan-view"))
        current = ps.load_list(args.changes) or {}
    except ps.Refused as e:
        print(f"refused: {e}", file=sys.stderr)
        return 2
    # Items the list already adds can be parents of later entries ("new" until they land).
    listed = {}
    for ent in current.get("entries") or []:
        if ent.get("op") in ("add", "new-feature") and ent.get("issue") is not None:
            listed[str(ent["issue"])] = ent.get("kind")
        if ent.get("op") in ("add", "new-feature") and ent.get("issue") is None:
            listed[f"@{ent.get('n')}"] = ent.get("kind")
    # The statuses the list and this draft set: closing an item whose open work the same list
    # closes is not "closing with open work under it".
    pending = {}
    for ent in (current.get("entries") or []) + (draft.get("entries") or []):
        if ent.get("op") == "status" and ent.get("issue") is not None:
            pending[str(ent["issue"])] = ent.get("to")
    out, unknown = [], []
    for entry in draft.get("entries") or []:
        e, miss = check(entry, plan, snap, items, plan_statuses, directions, listed, pending)
        out.append(e)
        unknown += [m for m in miss if m not in unknown]
    ps.write_json(args.out, {"instruction": draft.get("instruction"), "entries": out,
                             "questions": draft.get("questions") or [], "unknown_issues": unknown})
    return 0


if __name__ == "__main__":
    sys.exit(main())
