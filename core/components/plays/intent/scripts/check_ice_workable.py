#!/usr/bin/env python3
"""check_ice_workable.py — may a play work on this ICE? (ontology v3, #612)

An ICE lives inline in its capability's or functionality's grounding doc; the node's spine
entry names, in `intents`, the business intents it is built from. The ICE is WORKABLE only
when at least one of those intents is confirmed — its page under `product-os/intents/<id>.md`
reads `**Stage:** confirmed`. An ICE with no intent, or only proposed or dropped ones, is
kept as written but no play plans, breaks down or builds from it. Writing is never blocked;
this check stops work, not writes.

Canonical copy for play-creator: a play that works on ICE (plans, breaks down or builds
from it) copies this script unchanged and calls it before that work.

    python3 check_ice_workable.py --spine <product-os>/_spine.yaml \
        --intents-dir <product-os>/intents [--node <capability or functionality id>] \
        [--out <path.json>]

Without --node it reports every capability and functionality. With --node, exit 0 when
that node's ICE is workable, 1 when it is not, 2 when the node is unknown or an input is
unreadable. No git, no network, no LLM.
"""
import argparse
import json
import os
import re
import sys

import yaml

STAGE = re.compile(r"^\*\*Stage:\*\*\s*([a-z]+)", re.MULTILINE | re.IGNORECASE)


def stage_of(intents_dir, iid):
    """The intent's stage from its page, or None when the page does not exist."""
    path = os.path.join(intents_dir, f"{iid}.md")
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as fh:
        m = STAGE.search(fh.read())
    return m.group(1).lower() if m else "unknown"


def assess(entry, kind, intents_dir):
    named = [str(i) for i in (entry.get("intents") or []) if str(i).strip()]
    stages = {i: stage_of(intents_dir, i) for i in named}
    confirmed = [i for i, st in stages.items() if st == "confirmed"]
    if confirmed:
        reason = f"built from confirmed business intent(s): {', '.join(confirmed)}"
    elif not named:
        reason = "built from no business intent — kept, not worked on"
    else:
        reason = "no confirmed business intent (" + ", ".join(
            f"{i}: {st or 'missing'}" for i, st in stages.items()) + ") — kept, not worked on"
    return {"id": entry.get("id"), "kind": kind, "intents": stages,
            "workable": bool(confirmed), "reason": reason}


def check(spine, intents_dir):
    nodes = []
    for section, kind in (("capabilities", "capability"), ("functionalities", "functionality")):
        for entry in spine.get(section) or []:
            if isinstance(entry, dict):
                nodes.append(assess(entry, kind, intents_dir))
    return nodes


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--spine", required=True)
    ap.add_argument("--intents-dir", required=True)
    ap.add_argument("--node")
    ap.add_argument("--out")
    args = ap.parse_args(argv)
    try:
        with open(args.spine, encoding="utf-8") as fh:
            spine = yaml.safe_load(fh) or {}
        if not isinstance(spine, dict):
            raise ValueError("the spine is not a mapping")
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(json.dumps({"error": f"cannot read the spine: {exc}"}))
        return 2
    nodes = check(spine, args.intents_dir)
    if args.node:
        match = [n for n in nodes if n["id"] == args.node]
        report = match[0] if match else {"error": f"no capability or functionality `{args.node}`"}
    else:
        report = {"nodes": nodes, "workable": sum(n["workable"] for n in nodes),
                  "not_workable": sum(not n["workable"] for n in nodes)}
    out = json.dumps(report, indent=2)
    print(out)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(out + "\n")
    if args.node:
        return 2 if "error" in report else (0 if report["workable"] else 1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
