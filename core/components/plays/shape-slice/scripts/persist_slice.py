#!/usr/bin/env python3
"""
persist_slice.py — write the slice /shape-slice shaped into the live product model (C6, C7, C9).

    python3 persist_slice.py --root <product-os dir> --spine <_spine.yaml> --slice <slice.json> \
        [--reuse <slice-id> [--pull-in <feature id>]... [--push-out <feature id>]...] \
        [--out <persist-slice.json>]

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

CHANGE A REUSED SLICE (--pull-in / --push-out, with --reuse only): when the slice kept no
longer serves the intent as it is, the run pulls a feature in, or pushes a feature out. A
feature pulled in takes its place in the order of slice.json `feature_refs` (after the
nearest feature before it that the slice keeps); a feature pushed out leaves the slice. The
slice keeps its one surface and its tester, so it stays testable end to end. The result
names `pulled_in` and `pushed_out`. Refused: a pull-in of a feature not in the spine or
already in the slice, a push-out of a feature not in the slice, and a push-out that leaves
the slice with no feature.

A SLICE IN PROGRESS (a spine `epics` entry with its id as `slice_ref` has the status
in_delivery, validated, fix_required or delivered) is never touched: --reuse of it, or a new
slice with its id, is refused. The run shapes a new slice with its own id.

A RECORD WRITTEN BEFORE slice.yaml v2 (no name or outcome, the surface kept under `slice`)
is brought to v2 when the run touches it: its own facts come from its spine entry, a missing
name or outcome from the shaped slice, a surface under `slice` moves to the top level, and a
missing surface part comes from the shaped slice's surface only when that surface is the
slice's own. The result's `upgraded_to_v2` names each field it set. When a part is still
missing, the run is refused and says which part to fill in the record.

The spine is written back with its comments and layout kept (spine_text.py): only the
changed slice entries' lines change.

It refuses with exit 2 and a plain message, and writes nothing, when: the vertical, the
surface name, its id or its user_action is missing; the surface has no persona_ref;
`surface` is a list of more than one; an id, slug, name, outcome, feature list or intent
list is missing; a feature is not in the spine; --reuse names a slice not in the spine; or
an id would place the record outside the model folder ('..', a path, or a symlink that
leaves it). Every check runs before the first write. Each file is written through
safe_write.atomic_write (a temp file, then a move into place), so a stopped run never leaves
half a file. It calls the model_names
guard (#807) on the spine. Reads and writes files on disk only; no git, no network.

Exit 0 written (or nothing new to write), 2 refused or usage error.
"""

import argparse
import copy
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
import spine_text  # noqa: E402
from safe_write import atomic_write  # noqa: E402

SPINE_FIELDS = ("id", "slug", "feature_refs", "vertical", "intents", "record")
IN_PROGRESS = ("in_delivery", "validated", "fix_required", "delivered")
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
    """Write YAML through safe_write.atomic_write."""
    atomic_text(path, yaml.safe_dump(data, sort_keys=False, allow_unicode=True))


def atomic_text(path, text):
    """Write text through safe_write.atomic_write."""
    atomic_write(path, text)


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


def in_progress(spine, sid):
    return any(isinstance(e, dict) and e.get("slice_ref") == sid and e.get("status") in IN_PROGRESS
               for e in (spine.get("epics") or []))


def changed_features(have, shaped, pull_in, push_out, known):
    """The kept slice's features after the pull-ins and push-outs, in build order."""
    out = list(have)
    for f in push_out:
        if f not in out:
            raise Refused(f"--push-out names feature '{f}', which is not in the slice")
        out.remove(f)
    for f in pull_in:
        if f not in known:
            raise Refused(f"--pull-in names feature '{f}', which is not in the spine; add it to "
                          "the model first (C8)")
        if f in out:
            raise Refused(f"--pull-in names feature '{f}', which is already in the slice")
        at = 0
        if f in shaped:
            before = [x for x in shaped[:shaped.index(f)] if x in out]
            at = out.index(before[-1]) + 1 if before else 0
        else:
            at = len(out)
        out.insert(at, f)
    if not out:
        raise Refused("the push-outs leave the slice with no feature; a slice holds one or more "
                      "features that one person tests end to end")
    return out


def plan(spine, sl, surface, root, reuse, pull_in=(), push_out=()):
    """Work out every write before the first one. Returns a dict that `write` applies."""
    slices = spine.get("slices") or []
    if not isinstance(slices, list):
        raise Refused("the spine's `slices` is not a list")
    sid = reuse or sl["id"]
    if (pull_in or push_out) and not reuse:
        raise Refused("--pull-in and --push-out change a reused slice; give --reuse <slice id>")
    if reuse:
        safe_id(reuse, "the slice to reuse")
    if in_progress(spine, sid):
        raise Refused(f"slice '{sid}' is in progress (its epic is past ready), so the run does not "
                      "touch it; shape a new slice with its own id")
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
                "rec_path": rec_path, "differences": [], "dropped": [], "spine_changed": True,
                "upgraded": [], "pulled_in": [], "pushed_out": []}
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
    known = {f.get("id") for f in (spine.get("features") or []) if isinstance(f, dict)}
    old_features = list(existing.get("feature_refs") or [])
    features = changed_features(old_features, list(sl["feature_refs"]), list(pull_in),
                                list(push_out), known) if (pull_in or push_out) else old_features
    entry["feature_refs"] = features
    kept_view = dict(existing, feature_refs=features)
    dropped = [k for k in existing if k not in SPINE_FIELDS]
    rec = load_record(rec_path)
    diffs = differences(kept_view, rec, sl, surface) if reuse else []
    if rec is None:
        rec_surface = surface if surface.get("name") == existing.get("vertical") else None
        if rec_surface is None:
            raise Refused(f"slice '{sid}' has no record at {record_rel(sid)}, and the new shape's "
                          "surface is not that slice's surface, so the record cannot be written")
        base = dict(sl, id=sid, slug=existing.get("slug") or sl["slug"],
                    feature_refs=features or sl["feature_refs"],
                    vertical=existing.get("vertical"))
        rec_new = new_record(base, rec_surface, intents)
        rec_changed = True
    else:
        rec_new = copy.deepcopy(rec)
        upgraded = to_v2(rec_new, sid, existing, sl, surface)
        body = rec_new["slice"]
        rec_intents = list(body.get("intents") or [])
        body["intents"] = rec_intents + [i for i in intents if i not in rec_intents]
        if features != old_features:
            body["feature_refs"] = list(features)
        rec_changed = rec_new != rec
    if rec is None:
        upgraded = []
    spine_changed = bool(added) or bool(dropped) or existing.get("record") != record_rel(sid) \
        or list(existing) != list(SPINE_FIELDS) or features != old_features
    action = "updated" if (spine_changed or rec_changed) else "unchanged"
    return {"action": action, "id": sid, "entry": entry, "new_entry": False, "existing": existing,
            "added": added, "record": rec_new if rec_changed else None, "rec_path": rec_path,
            "differences": diffs, "dropped": dropped, "spine_changed": spine_changed,
            "upgraded": upgraded, "pulled_in": [f for f in features if f not in old_features],
            "pushed_out": [f for f in old_features if f not in features]}


def to_v2(rec, sid, existing, sl, surface):
    """Bring a record written before slice.yaml v2 to v2, in place; return the fields it set.

    The slice's own facts come from its spine entry (id, slug, features, vertical). A missing
    name or outcome comes from the shaped slice, which serves the same intent. A surface kept
    under `slice` moves to the top level; a missing surface part comes from the shaped
    slice's surface only when that surface is the slice's own (same name as its vertical).
    Refused when a part is still missing: the person fills it in the record, then runs again."""
    set_ = []
    body = rec.get("slice")
    if not isinstance(body, dict):
        body = {}
        rec["slice"] = body
    for key, value in (("id", sid), ("slug", existing.get("slug")),
                       ("name", sl.get("name")), ("outcome", sl.get("outcome")),
                       ("feature_refs", list(existing.get("feature_refs") or [])),
                       ("vertical", existing.get("vertical")),
                       ("intents", list(existing.get("intents") or []))):
        if body.get(key) in (None, "", []):
            body[key] = value
            set_.append(f"slice.{key}")
    top = rec.get("surface")
    nested = body.pop("surface", None)
    if not isinstance(top, dict):
        top = dict(nested) if isinstance(nested, dict) else {}
        if nested is not None or top:
            set_.append("surface (moved from slice.surface)")
    own = surface if surface.get("name") == existing.get("vertical") else {}
    for key in RECORD_SURFACE:
        if not _text(top.get(key)) and _text(own.get(key)):
            top[key] = own[key]
            set_.append(f"surface.{key}")
    missing = [k for k in RECORD_SURFACE if not _text(top.get(k))]
    if missing:
        raise Refused(f"slice '{sid}' has a record written before slice.yaml v2, and it cannot "
                      f"be brought to v2: its surface has no {', '.join(missing)}, and the new "
                      f"shape's surface is not that slice's surface '{existing.get('vertical')}'. "
                      f"Fill those parts in {record_rel(sid)}, then run again")
    rec["surface"] = {k: top.get(k) for k in RECORD_SURFACE} | {k: v for k, v in top.items()
                                                                if k not in RECORD_SURFACE}
    return set_


def write(spine_path, spine, p, old_text, old_spine):
    if p["new_entry"]:
        if spine.get("slices") is None:
            spine["slices"] = []
        spine["slices"].append(p["entry"])
    elif p["spine_changed"]:
        spine["slices"] = [p["entry"] if s is p["existing"] else s for s in spine["slices"]]
    if p["spine_changed"]:
        text, _kept = spine_text.dump(old_text, old_spine, spine)
        atomic_text(spine_path, text)
    if p["record"] is not None:
        atomic_dump(p["rec_path"], p["record"])


def main(argv=None):
    ap = argparse.ArgumentParser(description="Write the shaped slice into the product model.")
    ap.add_argument("--root", required=True, help="the product-os folder")
    ap.add_argument("--spine", required=True)
    ap.add_argument("--slice", required=True, help="slice.json")
    ap.add_argument("--reuse", help="the id of the slice that already serves the intent (C7)")
    ap.add_argument("--pull-in", action="append", default=[],
                    help="with --reuse: a feature the kept slice takes in; repeatable")
    ap.add_argument("--push-out", action="append", default=[],
                    help="with --reuse: a feature the kept slice gives up; repeatable")
    ap.add_argument("--out", help="also write the result JSON here")
    args = ap.parse_args(argv)

    def finish(result, code):
        text = json.dumps(result, indent=2)
        print(text)
        if args.out:
            atomic_write(args.out, text + "\n")
        return code

    try:
        with open(args.spine, encoding="utf-8") as fh:
            old_text = fh.read()
        spine = yaml.safe_load(old_text) or {}
        if not isinstance(spine, dict):
            raise Refused("the spine must be a YAML mapping")
        old_spine = copy.deepcopy(spine)
        model_names.check_spine(spine, args.spine)
        with open(args.slice, encoding="utf-8") as fh:
            sl = json.load(fh)
        surface = check_slice(sl, spine, args.root)
        p = plan(spine, sl, surface, args.root, args.reuse, args.pull_in, args.push_out)
    except Refused as exc:
        sys.stderr.write(f"persist_slice.py: not written — {exc}\n")
        return finish({"ok": False, "refused": str(exc)}, 2)
    except (OSError, yaml.YAMLError, json.JSONDecodeError) as exc:
        sys.stderr.write(f"persist_slice.py: cannot read an input: {exc}\n")
        return finish({"ok": False, "refused": f"cannot read an input: {exc}"}, 2)

    write(args.spine, spine, p, old_text, old_spine)
    result = {"ok": True, "action": p["action"], "id": p["id"], "reused": bool(args.reuse),
              "added_intents": p["added"], "record": record_rel(p["id"]),
              "record_written": p["record"] is not None, "differences": p["differences"],
              "dropped_fields": p["dropped"], "upgraded_to_v2": p["upgraded"],
              "pulled_in": p["pulled_in"], "pushed_out": p["pushed_out"]}
    return finish(result, 0)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
