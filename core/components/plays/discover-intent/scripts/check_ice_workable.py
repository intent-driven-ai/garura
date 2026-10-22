#!/usr/bin/env python3
"""check_ice_workable.py — may a play work on this ICE? (ontology v6, #760; v5, #724)

Ontology v6 (ADR 047 §6, #760): when the spine has an `ices` list, the check reads each ICE
node — its `ices` entry and its ice.md — and gives one of three answers, computed each run
and never stored. "Its capability" is the capability itself, or a feature's parent.
  - ready: its capability serves a confirmed business intent, every capability it needs is
    done, and the ICE has all three parts (Intent, Context, Expectation). Work starts.
  - partly_ready: as ready, with gaps outside the parts — no domain, no identified_by. Work
    starts; the gaps are listed.
  - not_ready: a part is missing or empty, no confirmed business intent reaches it, a needed
    capability is not done, a feature has no parent, or a part has no ICE. Work stops.
A feature's own `intents` and `depends_on` are not read (v6: it finds its business
intents through its parent and never needs anything). Richness (which lines each part fills,
light | full) is reported, never a stop. The ICE's own approval is not a condition (§8).
Each answer keeps `workable` (true unless not_ready) for older callers. A spine with no
`ices` list keeps the v5 rule below, written in the same three answers.

The v5 rule (#724):

An ICE lives inline in its capability's or feature's grounding doc; the node's spine
entry names, in `intents`, the business intents it is built from. The ICE is WORKABLE only
when at least one of those intents is confirmed — its page under `product-os/intents/<id>.md`
reads `**Stage:** confirmed`, or `met` (a met intent was confirmed first and its proof now
holds; work that keeps it met is still wanted). An ICE with no intent, or only proposed or
dropped ones, is kept as written but no play plans, breaks down or builds from it.

Ontology v5 (#724): a missing domain no longer blocks. A capability is ready when it serves
a confirmed business intent and nothing it needs is open; a feature is ready when it
names a capability that is ready (its own confirmed intent, or its capability's) and nothing
it needs is open. A capability with no domain gets a warning, never a block. "Needs" is the
spine's `depends_on` list (capabilities or features). Whether a need is still open
comes from `--done`: a file listing the ids of done nodes (YAML or JSON list). Without it,
needs are listed but not judged. Writing is never blocked; this check stops work, not writes.

Canonical copy for create-play: a play that works on ICE (plans, breaks down or builds
from it) copies this script unchanged and calls it before that work.

    python3 check_ice_workable.py --spine <product-os>/_spine.yaml \
        --intents-dir <product-os>/intents [--node <capability or feature id>] \
        [--done <done-ids.yaml>] [--out <path.json>]

Without --node it reports every capability and feature (v6: every ICE, and every part
with none), with counts of each answer. --node takes an ICE id or its part's id: exit 0 when
ready or partly ready, 1 when not ready, 2 when the node is unknown or an input is unreadable. No git, no network, no LLM.
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
    for section, kind in (("capabilities", "capability"), ("features", "feature")):
        for entry in spine.get(section) or []:
            if isinstance(entry, dict):
                nodes.append(assess(entry, kind, intents_dir, spine, done))
    return nodes


# ---- Ontology v6 (ADR 047 §6, #760): the ready check reads each ICE node ----------------

ICE_PARTS = {"Intent": ("Goal", "Limit", "Fails if"),
             "Context": ("Read", "Never read", "Persona", "Scope"),
             "Expectation": ("Scenario", "Done means", "Quality need")}
LINE = re.compile(r"^\s*[-*]\s*\*\*([^*:]+?):?\*\*:?\s*(.*)$")


def read_parts(path):
    """{part: {line label: text}} for the three ICE sections of an ice.md, or None if unreadable."""
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        return None
    parts, cur, in_fence = {}, None, False
    for raw in text.splitlines():
        if raw.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if raw.startswith("## "):
            head = raw[3:].strip()
            cur = head if head in ICE_PARTS else None
            if cur:
                parts.setdefault(cur, {"_text": []})
            continue
        if cur and raw.strip():
            parts[cur]["_text"].append(raw)
            m = LINE.match(raw)
            if m and m.group(2).strip():
                parts[cur][m.group(1).strip()] = m.group(2).strip()
    return parts


def richness(parts):
    """Which lines each part fills: reported, never a stop (ADR 047). light | full."""
    missing = {p: [ln for ln in lines if ln not in parts.get(p, {})] for p, lines in ICE_PARTS.items()}
    level = "full" if not any(missing.values()) else "light"
    return {"level": level, "missing": missing}


def assess_ice(ice, part, kind, spine, root, intents_dir, done):
    """One ICE (or a part with none) → ready | partly_ready | not_ready, with stops and gaps."""
    caps = {c.get("id"): c for c in spine.get("capabilities") or [] if isinstance(c, dict)}
    stops, gaps, rich = [], [], None
    if ice is None:
        stops.append(f"{kind} `{part.get('id')}` has no ICE")
    else:
        parts = read_parts(os.path.join(root, ice.get("doc") or ""))
        if parts is None:
            stops.append(f"its ICE page `{ice.get('doc')}` cannot be read")
        else:
            for p in ICE_PARTS:
                if p not in parts:
                    stops.append(f"the ICE has no {p}")
                elif not parts[p]["_text"]:
                    stops.append(f"the ICE's {p} is empty")
            rich = richness(parts)
    # its capability: the part itself, or a feature's parent
    if kind == "capability":
        cap = part
    else:
        cap = caps.get(part.get("capability")) if part.get("capability") else None
        if not part.get("capability"):
            stops.append("the feature has no parent capability yet")
        elif cap is None:
            stops.append(f"its capability `{part.get('capability')}` is not in the spine")
    stages, confirmed, needs, still_open = {}, [], [], None
    if cap is not None:
        stages, confirmed = intent_state(cap, intents_dir)
        if not confirmed:
            stops.append("no confirmed business intent reaches it" + (
                " (" + ", ".join(f"{i}: {st or 'missing'}" for i, st in stages.items()) + ")" if stages else ""))
        cap_needs = [n for n in (cap.get("depends_on") or []) if str(n) in caps]
        needs, still_open = open_needs({"depends_on": cap_needs}, done)
        if still_open:
            stops.append("a capability it needs is not done: " + ", ".join(still_open))
        w = domain_warning(cap, spine)
        if w:
            gaps.append(w)
        if not cap.get("identified_by"):
            gaps.append(f"capability `{cap.get('id')}` has no identified by")
    answer = "not_ready" if stops else ("partly_ready" if gaps else "ready")
    return {"id": ice.get("id") if ice else None, "for": part.get("id"), "for_kind": kind, "answer": answer,
            "stops": stops, "gaps": gaps, "intents": stages, "needs": needs, "needs_open": still_open,
            "richness": rich, "workable": answer != "not_ready"}


def check_ices(spine, root, intents_dir, done=None):
    by_part = {}
    for ice in spine.get("ices") or []:
        if isinstance(ice, dict) and ice.get("for"):
            by_part.setdefault(ice["for"], ice)
    out = []
    for section, kind in (("capabilities", "capability"), ("features", "feature")):
        for part in spine.get(section) or []:
            if isinstance(part, dict):
                out.append(assess_ice(by_part.get(part.get("id")), part, kind, spine, root, intents_dir, done))
    return out


def v5_answer(node):
    """A spine with no `ices` list keeps the v5 rule, written in the three answers."""
    answer = "not_ready" if not node["workable"] else ("partly_ready" if node["warnings"] else "ready")
    return dict(node, answer=answer, **{"for": node["id"], "for_kind": node["kind"],
                                        "stops": [] if node["workable"] else [node["reason"]],
                                        "gaps": node["warnings"]})


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
    if spine.get("ices") is not None:
        root = os.path.dirname(os.path.abspath(args.spine))
        nodes = check_ices(spine, root, args.intents_dir, done)
    else:
        nodes = [v5_answer(n) for n in check(spine, args.intents_dir, done)]
    if args.node:
        match = [n for n in nodes if args.node in (n["id"], n["for"])]
        report = match[0] if match else {"error": f"no ICE, capability or feature `{args.node}`"}
    else:
        counts = {a: sum(n["answer"] == a for n in nodes) for a in ("ready", "partly_ready", "not_ready")}
        report = {"nodes": nodes, "counts": counts, "workable": sum(n["workable"] for n in nodes),
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
