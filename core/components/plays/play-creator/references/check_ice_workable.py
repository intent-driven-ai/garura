#!/usr/bin/env python3
"""check_ice_workable.py — may a play work on this ICE? (ontology v5, #724)

An ICE lives inline in its capability's or functionality's grounding doc; the node's spine
entry names, in `intents`, the business intents it is built from. The ICE is WORKABLE only
when at least one of those intents is confirmed — its page under `product-os/intents/<id>.md`
reads `**Stage:** confirmed`, or `met` (a met intent was confirmed first and its proof now
holds; work that keeps it met is still wanted). An ICE with no intent, or only proposed or
dropped ones, is kept as written but no play plans, breaks down or builds from it.

Ontology v5 (#724): a missing domain no longer blocks. A capability is ready when it serves
a confirmed business intent and nothing it needs is open; a functionality is ready when it
names a capability that is ready (its own confirmed intent, or its capability's) and nothing
it needs is open. A capability with no domain gets a warning, never a block. "Needs" is the
spine's `depends_on` list (capabilities or functionalities). Whether a need is still open
comes from `--done`: a file listing the ids of done nodes (YAML or JSON list). Without it,
needs are listed but not judged. Writing is never blocked; this check stops work, not writes.

Canonical copy for play-creator: a play that works on ICE (plans, breaks down or builds
from it) copies this script unchanged and calls it before that work.

    python3 check_ice_workable.py --spine <product-os>/_spine.yaml \
        --intents-dir <product-os>/intents [--node <capability or functionality id>] \
        [--done <done-ids.yaml>] [--out <path.json>]

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

WORKABLE_STAGES = {"confirmed", "met"}
STAGE = re.compile(r"^\*\*Stage:\*\*\s*([a-z]+)", re.MULTILINE | re.IGNORECASE)


def stage_of(intents_dir, iid):
    """The intent's stage from its page, or None when the page does not exist."""
    path = os.path.join(intents_dir, f"{iid}.md")
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as fh:
        m = STAGE.search(fh.read())
    return m.group(1).lower() if m else "unknown"


def domain_warning(cap, spine):
    """v5: a missing domain is a warning, never a block. Returns the warning or ''."""
    domains = {d.get("id") for d in spine.get("domains") or [] if isinstance(d, dict)}
    if not cap.get("domain"):
        return f"capability `{cap.get('id')}` has no domain yet"
    if cap.get("domain") not in domains:
        return f"domain `{cap.get('domain')}` is not in the spine"
    return ""


def intent_state(entry, intents_dir):
    named = [str(i) for i in (entry.get("intents") or []) if str(i).strip()]
    stages = {i: stage_of(intents_dir, i) for i in named}
    confirmed = [i for i, st in stages.items() if st in WORKABLE_STAGES]
    return stages, confirmed


def open_needs(entry, done):
    """The needs not yet done, or None when no done list was given."""
    needs = [str(n) for n in (entry.get("depends_on") or []) if str(n).strip()]
    if done is None:
        return needs, None
    return needs, [n for n in needs if n not in done]


def assess(entry, kind, intents_dir, spine=None, done=None):
    spine = spine or {}
    caps = {c.get("id"): c for c in spine.get("capabilities") or [] if isinstance(c, dict)}
    stages, confirmed = intent_state(entry, intents_dir)
    reasons, warnings = [], []
    needs, still_open = open_needs(entry, done)
    cap_ok = True
    if kind == "capability":
        cap = entry
        has_intent = bool(confirmed)
    else:
        cap_ok = False
        cap = caps.get(entry.get("capability")) if entry.get("capability") else None
        cap_report = assess(cap, "capability", intents_dir, spine, done) if cap else None
        _, cap_confirmed = intent_state(cap, intents_dir) if cap else ({}, [])
        has_intent = bool(confirmed or cap_confirmed)
        if not entry.get("capability"):
            reasons.append("no capability yet")
        elif cap is None:
            reasons.append(f"its capability `{entry.get('capability')}` is not in the spine")
        elif not cap_report["workable"]:
            reasons.append(f"its capability `{cap.get('id')}` is not ready")
        else:
            cap_ok = True
    if has_intent:
        reasons.insert(0, f"built from confirmed business intent(s): {', '.join(confirmed) or 'through its capability'}")
    elif not stages:
        reasons.append("built from no business intent")
    else:
        reasons.append("no confirmed business intent (" + ", ".join(
            f"{i}: {st or 'missing'}" for i, st in stages.items()) + ")")
    if still_open:
        reasons.append("blocked: needs " + ", ".join(still_open))
    if cap is not None:
        w = domain_warning(cap, spine)
        if w:
            warnings.append(w)
    workable = has_intent and cap_ok and not still_open
    return {"id": entry.get("id"), "kind": kind, "intents": stages, "needs": needs,
            "needs_open": still_open, "blocked": bool(still_open) if still_open is not None else None,
            "warnings": warnings, "workable": workable,
            "reason": "; ".join(reasons) + ("" if workable else " — kept, not ready")}


def check(spine, intents_dir, done=None):
    nodes = []
    for section, kind in (("capabilities", "capability"), ("functionalities", "functionality")):
        for entry in spine.get(section) or []:
            if isinstance(entry, dict):
                nodes.append(assess(entry, kind, intents_dir, spine, done))
    return nodes


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--spine", required=True)
    ap.add_argument("--intents-dir", required=True)
    ap.add_argument("--node")
    ap.add_argument("--done")
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
    done = None
    if args.done:
        try:
            with open(args.done, encoding="utf-8") as fh:
                done = {str(x) for x in (yaml.safe_load(fh) or [])}
        except (OSError, yaml.YAMLError, TypeError) as exc:
            print(json.dumps({"error": f"cannot read the done list: {exc}"}))
            return 2
    nodes = check(spine, args.intents_dir, done)
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
