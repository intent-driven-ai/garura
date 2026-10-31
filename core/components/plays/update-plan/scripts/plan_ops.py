#!/usr/bin/env python3
"""plan_ops.py — turn the approved list into the tracker writes and the model parts (C6, C7, C11).

    python3 plan_ops.py --changes <changes.yaml> --plan-file <plans>/<id>.yaml \
        --snapshot <snapshot.json> --out-github <github-ops.json> --out-model <model-ops.json>

A fixed rule for each entry, in the list's order (n):

  status Done / Dropped   close as completed / as not planned (when the tracker does not read so)
  status, from Done or Dropped to an open status        reopen (when the tracker reads closed)
  add (an issue that exists)   parent (to its plan parent), type (to its kind's type), when they differ
  add (a new issue)            create: title, text, the kind's type, the plan parent
  move                         parent
  retitle                      title
  text                         body
  kind                         type
  new-feature                  create the story (or, for a story that exists, body + parent), and one
                               model part in model-ops.json
  plan-status, plan-direction  nothing in the tracker (the plan file only)

An item at the top of the plan (an epic) has the plan's business intent as its parent in the
tracker. A parent that is a new item of the list is written "@<n>-create", the id of the op that
makes it. Every op carries `entry` (its n). Exit 0 written; 2 bad input. No git, no network.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_session as ps  # noqa: E402

REPRESENTS = "Represents: {feature}"


def parent_ref(value, plan_id, new_ids):
    if value is None:
        return int(plan_id)
    if isinstance(value, str) and value.startswith("@"):
        return new_ids[value]
    return int(value)


def story_body(entry, plan_id):
    lines = [entry.get("body") or entry.get("description") or "", "",
             REPRESENTS.format(feature=entry["feature"]), f"Plan: {plan_id}"]
    return "\n".join(lines).strip() + "\n"


def build(changes, plan, snap):
    plan_id = str(changes.get("plan") or plan.get("id"))
    issues = snap.get("issues") or {}
    gh, model = [], []
    new_ids = {}
    for e in changes.get("entries") or []:
        n, op = e["n"], e["op"]
        now = issues.get(str(e.get("issue"))) if e.get("issue") is not None else None

        def add(kind, **kw):
            gh.append({"id": f"{n}-{kind}", "entry": n, "op": kind, **kw})

        if op == "status":
            to = e["to"]
            if to in ps.CLOSED:
                reason = ps.CLOSED[to]
                if not ps.closed_as(now, reason):
                    add("close", issue=e["issue"], reason=reason)
            elif now and now["state"] == "CLOSED":
                add("reopen", issue=e["issue"])
        elif op == "add":
            parent = parent_ref(e.get("parent"), plan_id, new_ids)
            if e.get("issue") is None:
                add("create", title=e["title"], body=e.get("body") or "", type=ps.TYPES[e["kind"]], parent=parent)
                new_ids[f"@{n}"] = f"@{n}-create"
            else:
                if not now or now.get("type") != ps.TYPES[e["kind"]]:
                    add("type", issue=e["issue"], type=ps.TYPES[e["kind"]])
                if not now or str(now.get("parent")) != str(parent):
                    add("parent", issue=e["issue"], to=parent, **{"from": now.get("parent") if now else None})
        elif op == "move":
            add("parent", issue=e["issue"], to=parent_ref(e["to"], plan_id, new_ids), **{"from": e.get("from")})
        elif op == "retitle":
            add("title", issue=e["issue"], title=e["to"])
        elif op == "text":
            add("body", issue=e["issue"], body=e["body"])
        elif op == "kind":
            add("type", issue=e["issue"], type=ps.TYPES[e["to"]])
        elif op == "new-feature":
            parent = parent_ref(e.get("parent"), plan_id, new_ids)
            if e.get("issue") is None:
                add("create", title=e["title"], body=story_body(e, plan_id), type="Story", parent=parent)
                story = f"@{n}-create"
                new_ids[f"@{n}"] = story
            else:
                body = (now or {}).get("body") or ""
                line = REPRESENTS.format(feature=e["feature"])
                if line not in body:
                    add("body", issue=e["issue"], body=body.rstrip("\n") + "\n\n" + line + "\n")
                if not now or str(now.get("parent")) != str(parent):
                    add("parent", issue=e["issue"], to=parent, **{"from": now.get("parent") if now else None})
                story = e["issue"]
            model.append({"entry": n, "feature": e["feature"], "title": e["title"],
                          "capability": e.get("capability"), "slice": e.get("slice"),
                          "intent": f"bi-{plan_id}", "story": story, "identified_by": e.get("identified_by"),
                          "one_line": e.get("one_line") or e["title"], "ice": e.get("ice") or {},
                          "description": e.get("description")})
    return gh, model


def main(argv=None):
    ap = argparse.ArgumentParser(description="the tracker writes and model parts of the approved list")
    ap.add_argument("--changes", required=True)
    ap.add_argument("--plan-file", required=True)
    ap.add_argument("--snapshot", required=True)
    ap.add_argument("--out-github", required=True)
    ap.add_argument("--out-model", required=True)
    args = ap.parse_args(argv)
    try:
        changes = ps.load_list(args.changes)
        if not changes:
            raise ps.Refused("there is no list")
        plan = ps.load_plan(args.plan_file)
        snap = ps.read_json(args.snapshot, "snapshot.json")
        gh, model = build(changes, plan, snap)
    except (ps.Refused, KeyError) as e:
        print(f"refused: {e}", file=sys.stderr)
        return 2
    ps.write_json(args.out_github, {"plan": changes.get("plan"), "ops": gh})
    ps.write_json(args.out_model, {"plan": changes.get("plan"), "parts": model})
    return 0


if __name__ == "__main__":
    sys.exit(main())
