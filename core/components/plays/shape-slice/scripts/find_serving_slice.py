#!/usr/bin/env python3
"""
find_serving_slice.py — does a slice already serve this business intent? (/shape-slice, C7)

A slice already serves the intent when either:
  1. its spine entry lists the intent in `intents`, or
  2. (only when --features and --surface are both given) it has the same `feature_refs`
     (the same features, in the same order) and the same `vertical` (the one surface).

The first match in the spine's `slices` order wins; a match by rule 1 wins over rule 2.

    python3 find_serving_slice.py --spine <_spine.yaml> --intent <id> \
        [--features a,b,c] [--surface <name>] [--reuse-into <slice.json>]

With --reuse-into and a match, the slice.json the run shaped takes the matched slice's id and
slug, so the write adds the intent to that slice and makes no new one (C7, REC7).

Prints one JSON object: {"match": "<slice id>" | null, "reason": "..."}. Exit 0 on a
result (match or none), 2 on a usage or read error. Reads files on disk only; no git, no
network. Calls the model_names guard (#807) on the spine it loads.
"""

import argparse
import json
import os
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("find_serving_slice.py: PyYAML is required (pip install pyyaml).\n")
    sys.exit(2)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import model_names  # noqa: E402  (stamped from create-play/references)


def load_spine(path):
    with open(path, encoding="utf-8") as fh:
        spine = yaml.safe_load(fh) or {}
    if not isinstance(spine, dict):
        raise ValueError("the spine must be a YAML mapping")
    return model_names.check_spine(spine, path)


def find(spine, intent, features=None, surface=None):
    slices = [s for s in (spine.get("slices") or []) if isinstance(s, dict)]
    for s in slices:
        if intent in (s.get("intents") or []):
            return {"match": s.get("id"),
                    "reason": f"slice '{s.get('id')}' already lists business intent '{intent}'"}
    if features is not None and surface is not None:
        for s in slices:
            if list(s.get("feature_refs") or []) == features and s.get("vertical") == surface:
                return {"match": s.get("id"),
                        "reason": f"slice '{s.get('id')}' has the same features in the same order "
                                  f"and the same surface '{surface}'"}
    if features is not None and surface is not None:
        reason = (f"no slice lists business intent '{intent}', and none has the same features "
                  f"and the surface '{surface}'")
    else:
        reason = f"no slice lists business intent '{intent}'"
    return {"match": None, "reason": reason}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Find a slice that already serves a business intent.")
    ap.add_argument("--spine", required=True)
    ap.add_argument("--intent", required=True)
    ap.add_argument("--features", help="comma-separated feature ids, in build order")
    ap.add_argument("--surface", help="the one surface (the slice's vertical)")
    ap.add_argument("--reuse-into", help="on a match, give this slice.json the match's id and slug")
    args = ap.parse_args(argv)
    if (args.features is None) != (args.surface is None):
        sys.stderr.write("find_serving_slice.py: give --features and --surface together, or neither\n")
        return 2
    features = None
    if args.features is not None:
        features = [f.strip() for f in args.features.split(",") if f.strip()]
        if not features:
            sys.stderr.write("find_serving_slice.py: --features names no feature\n")
            return 2
    try:
        spine = load_spine(args.spine)
    except (OSError, yaml.YAMLError, ValueError) as exc:
        sys.stderr.write(f"find_serving_slice.py: cannot read the spine {args.spine}: {exc}\n")
        return 2
    result = find(spine, args.intent, features, args.surface)
    if args.reuse_into and result["match"]:
        try:
            with open(args.reuse_into, encoding="utf-8") as fh:
                shaped = json.load(fh)
            hit = next(s for s in spine.get("slices") or [] if s.get("id") == result["match"])
            shaped["id"], shaped["slug"] = hit["id"], hit.get("slug", shaped.get("slug"))
            with open(args.reuse_into, "w", encoding="utf-8") as fh:
                json.dump(shaped, fh, indent=2)
            result["reused_into"] = args.reuse_into
        except (OSError, json.JSONDecodeError, AttributeError) as exc:
            sys.stderr.write(f"find_serving_slice.py: cannot update {args.reuse_into}: {exc}\n")
            return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
