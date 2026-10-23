#!/usr/bin/env python3
"""
persist_slice.py — write the slice /shape-slice shaped into the live product model (C6, C7, C9).

    python3 persist_slice.py --root <product-os dir> --spine <_spine.yaml> --slice <slice.json> \
        [--reuse <slice-id>] [--out <persist-slice.json>]

slice.json:
    {"id": "...", "slug": "...", "name": "...", "outcome": "...",
     "feature_refs": ["...", ...], "vertical": "...", "intents": ["bi-..."],
     "surface": {"id": "...", "name": "...", "persona_ref": "...", "user_action": "..."}}

It writes two things and nothing else:
  - the spine `slices` entry, keyed by id, with exactly six fields: id, slug, feature_refs,
    vertical, intents, record. No status, order, effort, depends_on or domain_ref (ontology
    v10). `record` points to the slice record, relative to the product-os folder:
    `slices/<id>.yaml`.
  - the slice record at <root>/slices/<id>.yaml (slice.yaml v2):
        slice:   {id, slug, name, outcome, feature_refs, vertical, intents}
        surface: {id, name, persona_ref, user_action}
    The surface's persona_ref is the person who tests the slice.

A NEW slice (no --reuse): when the id is already in the spine with the same features and
vertical, the run adds each new intent to that entry and to its record (order kept, no
duplicates) and makes no second entry. The same id with other features or another vertical
is refused: a slice that serves the intent is reused with --reuse, never overwritten.

REUSE (--reuse <slice-id>, C7): the slice <slice-id> already serves the intent
(find_serving_slice.py found it). The run adds the shaped slice's intents to that slice's
spine entry and to its record (appended, no duplicates). It keeps that slice's feature_refs,
vertical and surface as they are, and makes no second slice. The result's `differences`
lists, in plain words, how the new shape differs from the slice it reuses, so the person
sees it at the checkpoint. An older entry with fields ontology v10 removed (status, order,
effort, depends_on, domain_ref) is written back with the six fields only; the result names
the fields it dropped.

It refuses with exit 2 and a plain message, and writes nothing, when: the vertical, the
surface name, its id or its user_action is missing; the surface has no persona_ref;
`surface` is a list of more than one; an id, slug, name, outcome, feature list or intent
list is missing; a feature is not in the spine; --reuse names a slice not in the spine; or
an id would place the record outside the model folder ('..', a path, or a symlink that
leaves it). Every check runs before the first write. Each file is written through a temp
file and os.replace, so a stopped run never leaves half a file. It calls the model_names
guard (#807) on the spine. Reads and writes files on disk only; no git, no network.

Exit 0 written (or nothing new to write), 2 refused or usage error.
"""

import argparse
import json
import os
import sys
import tempfile

try:
    import yaml
except ImportError:
    sys.stderr.write("persist_slice.py: PyYAML is required (pip install pyyaml).\n")
    sys.exit(2)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import model_names  # noqa: E402  (stamped from create-play/references)

SPINE_FIELDS = ("id", "slug", "feature_refs", "vertical", "intents", "record")
RECORD_SLICE = ("id", "slug", "name", "outcome", "feature_refs", "vertical", "intents")
RECORD_SURFACE = ("id", "name", "persona_ref", "user_action")


def record_rel(slice_id):
    """The slice record's path, relative to the product-os folder."""
    return f"slices/{slice_id}.yaml"


class Refused(Exception):
    """The slice cannot be written; the message says why, in plain words."""


def _text(value):
    return isinstance(value, str) and value.strip() != ""


def _list_of_text(value):
    return isinstance(value, list) and value and all(_text(v) for v in value)


def inside(root, rel, what):
    """The absolute path of `rel` under `root`; refused when it leaves the model folder."""
    if not _text(rel) or os.path.isabs(rel) or ".." in rel.replace("\\", "/").split("/"):
        raise Refused(f"{what} '{rel}' leaves the model folder; give a path inside it")
    real_root = os.path.realpath(root)
    target = os.path.realpath(os.path.join(root, rel))
    if target != real_root and not target.startswith(real_root + os.sep):
        raise Refused(f"{what} '{rel}' leaves the model folder (through a link); "
                      "give a path inside it")
    return os.path.join(root, rel)


def safe_id(value, what):
    if not _text(value) or "/" in value or "\\" in value or value in (".", "..") \
            or value.startswith("."):
        raise Refused(f"{what} '{value}' is not a plain name; it would place a file outside "
                      "the model folder")
    return value


def atomic_dump(path, data):
    """Write YAML through a temp file in the same folder, then os.replace it into place."""
    folder = os.path.dirname(os.path.abspath(path))
    os.makedirs(folder, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".persist-slice-", suffix=".tmp", dir=folder)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            yaml.safe_dump(data, fh, sort_keys=False, allow_unicode=True)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


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
    for key in ("id", "user_action"):
        if not _text(surface.get(key)):
            raise Refused(f"the surface has no {key}; the slice record needs the surface's id "
                          "and what the person does on it (slice.yaml v2)")
    return surface


def check_slice(sl, spine, root):
    if not isinstance(sl, dict):
        raise Refused("slice.json must hold one JSON object")
    for key in ("id", "slug", "name", "outcome"):
        if not _text(sl.get(key)):
            raise Refused(f"the slice has no {key}")
    safe_id(sl["id"], "the slice id")
    inside(root, record_rel(sl["id"]), "the slice record")
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


def load_record(path):
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as fh:
        rec = yaml.safe_load(fh) or {}
    if not isinstance(rec, dict):
        raise Refused(f"the slice record {path} is not a YAML mapping")
    return rec


def new_record(sl, surface, intents):
    return {"slice": {"id": sl["id"], "slug": sl["slug"], "name": sl["name"],
                      "outcome": sl["outcome"], "feature_refs": list(sl["feature_refs"]),
                      "vertical": sl["vertical"], "intents": list(intents)},
            "surface": {k: surface.get(k) for k in RECORD_SURFACE}}


def record_surface(rec):
    """The surface of a record: top-level (v2), or under `slice` (written before v2)."""
    if not isinstance(rec, dict):
        return None
    s = rec.get("surface")
    if isinstance(s, dict):
        return s
    s = (rec.get("slice") or {}).get("surface")
    return s if isinstance(s, dict) else None


def differences(existing, rec, sl, surface):
    out = []
    have_f, new_f = list(existing.get("feature_refs") or []), list(sl["feature_refs"])
    if have_f != new_f:
        only_new = [f for f in new_f if f not in have_f]
        only_have = [f for f in have_f if f not in new_f]
        parts = []
        if only_new:
            parts.append("the new shape adds " + ", ".join(only_new))
        if only_have:
            parts.append("the new shape leaves out " + ", ".join(only_have))
        if not parts:
            parts.append("the new shape has the same features in another order")
        out.append(f"features differ: the slice keeps {have_f}; " + "; ".join(parts))
    if existing.get("vertical") != sl["vertical"]:
        out.append(f"surface differs: the slice keeps '{existing.get('vertical')}'; "
                   f"the new shape names '{sl['vertical']}'")
    have_s = record_surface(rec) or {}
    if have_s and have_s.get("persona_ref") != surface.get("persona_ref"):
        out.append(f"tester differs: the slice keeps '{have_s.get('persona_ref')}'; "
                   f"the new shape names '{surface.get('persona_ref')}'")
    return out


def plan(spine, sl, surface, root, reuse):
    """Work out every write before the first one. Returns a dict that `write` applies."""
    slices = spine.get("slices") or []
    if not isinstance(slices, list):
        raise Refused("the spine's `slices` is not a list")
    sid = reuse or sl["id"]
    if reuse:
        safe_id(reuse, "the slice to reuse")
    existing = next((s for s in slices if isinstance(s, dict) and s.get("id") == sid), None)
    rec_path = inside(root, record_rel(sid), "the slice record")
    if existing is None:
        if reuse:
            raise Refused(f"--reuse names slice '{reuse}', which is not in the spine")
        entry = {k: sl[k] for k in SPINE_FIELDS if k != "record"}
        entry["feature_refs"] = list(sl["feature_refs"])
        entry["intents"] = list(dict.fromkeys(sl["intents"]))
        entry["record"] = record_rel(sid)
        return {"action": "created", "id": sid, "entry": entry, "new_entry": True,
                "added": entry["intents"], "record": new_record(sl, surface, entry["intents"]),
                "rec_path": rec_path, "differences": [], "dropped": [], "spine_changed": True}
    if not reuse and (list(existing.get("feature_refs") or []) != list(sl["feature_refs"])
                      or existing.get("vertical") != sl["vertical"]):
        raise Refused(f"slice '{sid}' is already in the spine with other features or another "
                      "surface; to add the intent to it run with --reuse "
                      f"{sid}, or give the new slice its own id")
    have = list(existing.get("intents") or [])
    added = [i for i in dict.fromkeys(sl["intents"]) if i not in have]
    intents = have + added
    entry = {k: existing.get(k) for k in SPINE_FIELDS if k != "record"}
    entry["intents"] = intents
    entry["record"] = record_rel(sid)
    dropped = [k for k in existing if k not in SPINE_FIELDS]
    rec = load_record(rec_path)
    diffs = differences(existing, rec, sl, surface) if reuse else []
    if rec is None:
        rec_surface = surface if surface.get("name") == existing.get("vertical") else None
        if rec_surface is None:
            raise Refused(f"slice '{sid}' has no record at {record_rel(sid)}, and the new shape's "
                          "surface is not that slice's surface, so the record cannot be written")
        base = dict(sl, id=sid, slug=existing.get("slug") or sl["slug"],
                    feature_refs=existing.get("feature_refs") or sl["feature_refs"],
                    vertical=existing.get("vertical"))
        rec_new = new_record(base, rec_surface, intents)
        rec_changed = True
    else:
        rec_new = rec
        body = rec_new.get("slice")
        if not isinstance(body, dict):
            body = {}
            rec_new["slice"] = body
        rec_intents = list(body.get("intents") or [])
        merged = rec_intents + [i for i in intents if i not in rec_intents]
        rec_changed = merged != rec_intents
        body["intents"] = merged
    spine_changed = bool(added) or bool(dropped) or existing.get("record") != record_rel(sid) \
        or list(existing) != list(SPINE_FIELDS)
    action = "updated" if (spine_changed or rec_changed) else "unchanged"
    return {"action": action, "id": sid, "entry": entry, "new_entry": False, "existing": existing,
            "added": added, "record": rec_new if rec_changed else None, "rec_path": rec_path,
            "differences": diffs, "dropped": dropped, "spine_changed": spine_changed}


def write(spine_path, spine, p):
    if p["new_entry"]:
        if spine.get("slices") is None:
            spine["slices"] = []
        spine["slices"].append(p["entry"])
    elif p["spine_changed"]:
        spine["slices"] = [p["entry"] if s is p["existing"] else s for s in spine["slices"]]
    if p["spine_changed"]:
        atomic_dump(spine_path, spine)
    if p["record"] is not None:
        atomic_dump(p["rec_path"], p["record"])


def main(argv=None):
    ap = argparse.ArgumentParser(description="Write the shaped slice into the product model.")
    ap.add_argument("--root", required=True, help="the product-os folder")
    ap.add_argument("--spine", required=True)
    ap.add_argument("--slice", required=True, help="slice.json")
    ap.add_argument("--reuse", help="the id of the slice that already serves the intent (C7)")
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
        surface = check_slice(sl, spine, args.root)
        p = plan(spine, sl, surface, args.root, args.reuse)
    except Refused as exc:
        sys.stderr.write(f"persist_slice.py: not written — {exc}\n")
        return finish({"ok": False, "refused": str(exc)}, 2)
    except (OSError, yaml.YAMLError, json.JSONDecodeError) as exc:
        sys.stderr.write(f"persist_slice.py: cannot read an input: {exc}\n")
        return finish({"ok": False, "refused": f"cannot read an input: {exc}"}, 2)

    write(args.spine, spine, p)
    result = {"ok": True, "action": p["action"], "id": p["id"], "reused": bool(args.reuse),
              "added_intents": p["added"], "record": record_rel(p["id"]),
              "record_written": p["record"] is not None, "differences": p["differences"],
              "dropped_fields": p["dropped"]}
    return finish(result, 0)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
