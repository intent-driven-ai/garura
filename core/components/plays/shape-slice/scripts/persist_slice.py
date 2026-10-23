#!/usr/bin/env python3
"""
persist_slice.py — write the slice /shape-slice shaped into the live product model (C6, C7, C9).

    python3 persist_slice.py --root <product-os dir> --spine <_spine.yaml> --slice <slice.json> \
        [--out <persist-slice.json>]

slice.json:
    {"id": "...", "slug": "...", "feature_refs": ["...", ...], "vertical": "...",
     "intents": ["bi-..."], "surface": {"name": "...", "persona_ref": "...", ...}}

It writes two things and nothing else:
  - the spine `slices` entry, keyed by id, with exactly: id, slug, feature_refs, vertical,
    intents, record. No status, order, effort, depends_on or domain_ref (ontology v10).
    `record` points to the slice record, relative to the product-os folder:
    `slices/<id>.yaml`.
  - the slice record at <root>/slices/<id>.yaml, which holds the one surface with its
    persona_ref (the person who tests the slice).

When the slice id is already in the spine, it adds each new intent to that entry's `intents`
(order kept, no duplicates) and makes no second entry; it adds the `record` pointer if the
entry has none; the record file is written only if it is missing. A slice already in the spine with other features or another vertical is refused.

It refuses with exit 2 and a plain message, and writes nothing, when: the vertical or the
surface name is missing; the surface has no persona_ref; `surface` is a list of more than
one; an id, slug, feature list or intent list is missing; or a feature is not in the spine.
Every check runs before the first write. It calls the model_names guard (#807) on the spine.
Reads and writes files on disk only; no git, no network.

Exit 0 written (or nothing new to write), 2 refused or usage error.
"""

import argparse
import json
import os
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("persist_slice.py: PyYAML is required (pip install pyyaml).\n")
    sys.exit(2)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import model_names  # noqa: E402  (stamped from create-play/references)

SPINE_FIELDS = ("id", "slug", "feature_refs", "vertical", "intents")


def record_rel(slice_id):
    """The slice record's path, relative to the product-os folder."""
    return f"slices/{slice_id}.yaml"


class Refused(Exception):
    """The slice cannot be written; the message says why, in plain words."""


def _text(value):
    return isinstance(value, str) and value.strip() != ""


def _list_of_text(value):
    return isinstance(value, list) and value and all(_text(v) for v in value)


def one_surface(surface):
    if isinstance(surface, list):
        if len(surface) > 1:
            raise Refused(f"the slice names {len(surface)} surfaces; a slice has exactly one "
                          "surface that one person tests end to end")
        surface = surface[0] if surface else None
    if not isinstance(surface, dict) or not _text(surface.get("name")):
        raise Refused("the slice names no surface; a slice needs the one screen or surface a "
                      "person tests end to end")
    if not _text(surface.get("persona_ref")):
        raise Refused("the surface names no persona_ref; a slice needs the person who tests it")
    return surface


def check_slice(sl, spine):
    if not isinstance(sl, dict):
        raise Refused("slice.json must hold one JSON object")
    for key in ("id", "slug"):
        if not _text(sl.get(key)):
            raise Refused(f"the slice has no {key}")
    if not _text(sl.get("vertical")):
        raise Refused("the slice has no vertical; the vertical is the name of its one surface")
    surface = one_surface(sl.get("surface"))
    if not _list_of_text(sl.get("feature_refs")):
        raise Refused("the slice names no features; a slice holds one or more, in build order")
    if not _list_of_text(sl.get("intents")):
        raise Refused("the slice names no business intent it serves")
    known = {f.get("id") for f in (spine.get("features") or []) if isinstance(f, dict)}
    missing = [f for f in sl["feature_refs"] if f not in known]
    if missing:
        raise Refused("these features are not in the spine: " + ", ".join(missing)
                      + " — add them to the model first (C8)")
    return surface


def plan(spine, sl, root):
    """Work out the write. Returns (action, entry, added_intents, record_needed, add_pointer)."""
    slices = spine.get("slices") or []
    if not isinstance(slices, list):
        raise Refused("the spine's `slices` is not a list")
    existing = next((s for s in slices if isinstance(s, dict) and s.get("id") == sl["id"]), None)
    record_path = os.path.join(root, record_rel(sl["id"]))
    if existing is None:
        entry = {k: sl[k] for k in SPINE_FIELDS}
        entry["feature_refs"] = list(sl["feature_refs"])
        entry["intents"] = list(dict.fromkeys(sl["intents"]))
        entry["record"] = record_rel(sl["id"])
        return "created", entry, entry["intents"], True, False
    if list(existing.get("feature_refs") or []) != list(sl["feature_refs"]) \
            or existing.get("vertical") != sl["vertical"]:
        raise Refused(f"slice '{sl['id']}' is already in the spine with other features or another "
                      "surface; give the new slice its own id")
    have = list(existing.get("intents") or [])
    added = [i for i in dict.fromkeys(sl["intents"]) if i not in have]
    add_pointer = not _text(existing.get("record"))
    action = "updated" if (added or add_pointer) else "unchanged"
    return action, existing, added, not os.path.isfile(record_path), add_pointer


def write(spine_path, spine, root, sl, surface, action, entry, added, record_needed,
          add_pointer):
    if action == "created":
        spine.setdefault("slices", [])
        if spine["slices"] is None:
            spine["slices"] = []
        spine["slices"].append(entry)
    else:
        if added:
            entry["intents"] = list(entry.get("intents") or []) + added
        if add_pointer:
            entry["record"] = record_rel(sl["id"])
    if action != "unchanged":
        with open(spine_path, "w", encoding="utf-8") as fh:
            yaml.safe_dump(spine, fh, sort_keys=False, allow_unicode=True)
    rel = record_rel(sl["id"])
    if record_needed:
        os.makedirs(os.path.join(root, "slices"), exist_ok=True)
        record = {"slice": {"id": sl["id"], "slug": sl["slug"],
                            "feature_refs": list(sl["feature_refs"]),
                            "vertical": sl["vertical"], "surface": dict(surface)}}
        with open(os.path.join(root, rel), "w", encoding="utf-8") as fh:
            yaml.safe_dump(record, fh, sort_keys=False, allow_unicode=True)
    return rel


def main(argv=None):
    ap = argparse.ArgumentParser(description="Write the shaped slice into the product model.")
    ap.add_argument("--root", required=True, help="the product-os folder")
    ap.add_argument("--spine", required=True)
    ap.add_argument("--slice", required=True, help="slice.json")
    ap.add_argument("--out", help="also write the result JSON here")
    args = ap.parse_args(argv)

    def finish(result, code):
        text = json.dumps(result, indent=2)
        print(text)
        if args.out:
            with open(args.out, "w", encoding="utf-8") as fh:
                fh.write(text + "\n")
        return code

    try:
        with open(args.spine, encoding="utf-8") as fh:
            spine = yaml.safe_load(fh) or {}
        if not isinstance(spine, dict):
            raise Refused("the spine must be a YAML mapping")
        model_names.check_spine(spine, args.spine)
        with open(args.slice, encoding="utf-8") as fh:
            sl = json.load(fh)
        surface = check_slice(sl, spine)
        action, entry, added, record_needed, add_pointer = plan(spine, sl, args.root)
    except Refused as exc:
        sys.stderr.write(f"persist_slice.py: not written — {exc}\n")
        return finish({"ok": False, "refused": str(exc)}, 2)
    except (OSError, yaml.YAMLError, json.JSONDecodeError) as exc:
        sys.stderr.write(f"persist_slice.py: cannot read an input: {exc}\n")
        return finish({"ok": False, "refused": f"cannot read an input: {exc}"}, 2)

    rel = write(args.spine, spine, args.root, sl, surface, action, entry, added, record_needed,
                add_pointer)
    return finish({"ok": True, "action": action, "id": sl["id"], "added_intents": added,
                   "record": rel, "record_written": record_needed}, 0)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
