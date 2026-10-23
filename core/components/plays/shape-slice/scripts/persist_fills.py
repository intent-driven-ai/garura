#!/usr/bin/env python3
"""
persist_fills.py — add to the spine the parts the slice needs and the model lacked (/shape-slice, C8).

The fill skills already wrote each new part's page in the live model. This script writes the
shared file: one spine entry for each new domain, capability, feature and ICE, marked to be
deepened later (status proposed, detail directional where the kind has a detail field,
metadata.deepen true). It also links each new domain and capability to the business intent
on the intent page's Touches list (marked "adds"), so both sides of the link are written.

    python3 persist_fills.py --root <product-os dir> --spine <_spine.yaml> \
        --fills <fills.json> --intent <bi-id> [--out <persist-fills.json>]

fills.json:
    {"domains":      [{"id", "slug", "one_line", "doc"}],
     "capabilities": [{"id", "slug", "domain", "one_line", "doc"}],
     "features":     [{"id", "slug", "capability", "one_line", "doc"}],
     "ices":         [{"id", "for", "for_kind", "doc"}]}
Every list may be empty or missing.

ADDITIVE ONLY. It refuses with exit 2, and writes nothing, when: an id is already in the
spine or given twice; a page (doc) is not on disk; a parent (a capability's domain, a
feature's capability, an ICE's part) is in neither the spine nor this fill; an ICE is given
but the spine has no `ices` list (that model keeps the ICE inside the part's page); or the
intent page is missing. It calls the model_names guard (#807) on the spine.

It also refuses (exit 2, nothing written) any doc path or intent id that leaves the model
folder: '..', an absolute path, or a symlink that points outside it. The spine and the intent
page are written through a temp file and os.replace.

The result names `allow`: the model paths this run may change for the fills, for the scoped
write guard. It also keeps `touches_added` (the Touches lines it added to the intent page)
and the page's text before and after, so a change at the checkpoint can take them back:

    python3 persist_fills.py --undo <persist-fills.json> --root <product-os dir> --intent <bi-id>

--undo removes the Touches lines this run added and nothing else: when the page is as this
run left it, it is put back exactly as it was before; when someone edited it since, only the
added lines are taken out (and the Touches heading too, when this run made it and no line is
left under it). The spine is written back with its comments and layout kept (spine_text.py).
Reads and writes files on disk only; no git, no network.
Exit 0 written, undone (or nothing to do), 2 refused or usage error.
"""

import argparse
import copy
import json
import os
import sys
import tempfile

try:
    import yaml
except ImportError:
    sys.stderr.write("persist_fills.py: PyYAML is required (pip install pyyaml).\n")
    sys.exit(2)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import intent_touches as touches  # noqa: E402  (stamped from create-play/references)
import model_names  # noqa: E402  (stamped from create-play/references)
import spine_text  # noqa: E402

KINDS = (  # (fills key, spine key, touches kind, parent field, parent spine key)
    ("domains", "domains", "domain", None, None),
    ("capabilities", "capabilities", "capability", "domain", "domains"),
    ("features", "features", "feature", "capability", "capabilities"),
)
MARK = {"created_by": "/shape-slice", "deepen": True}


class Refused(Exception):
    """The fills cannot be written; the message says why."""


def inside(root, rel, what):
    """The path of `rel` under `root`; refused when it leaves the model folder."""
    if not isinstance(rel, str) or not rel.strip() or os.path.isabs(rel) \
            or ".." in rel.replace("\\", "/").split("/"):
        raise Refused(f"{what} '{rel}' leaves the model folder; give a path inside it")
    real_root = os.path.realpath(root)
    target = os.path.realpath(os.path.join(root, rel))
    if target != real_root and not target.startswith(real_root + os.sep):
        raise Refused(f"{what} '{rel}' leaves the model folder (through a link); "
                      "give a path inside it")
    return os.path.join(root, rel)


def intent_page(root, intent):
    if not isinstance(intent, str) or not intent.strip() or "/" in intent or "\\" in intent \
            or intent.startswith("."):
        raise Refused(f"the intent id '{intent}' is not a plain name")
    return inside(root, f"intents/{intent}.md", "the intent page")


def atomic_write(path, text):
    folder = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(prefix=".persist-fills-", suffix=".tmp", dir=folder)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def _ids(spine, key):
    return {e.get("id") for e in (spine.get(key) or []) if isinstance(e, dict)}


def plan(root, spine, fills, intent):
    seen = set()
    for key in ("domains", "capabilities", "features", "ices"):
        seen |= _ids(spine, key)
    given = set()
    entries = {}
    for fkey, skey, _kind, parent, pkey in KINDS:
        out = []
        for e in fills.get(fkey) or []:
            if not isinstance(e, dict):
                raise Refused(f"an entry in {fkey} is not an object")
            eid = e.get("id")
            for field in ("id", "slug", "one_line", "doc"):
                if not e.get(field):
                    raise Refused(f"{fkey} entry '{eid}' has no {field}")
            if eid in seen or eid in given:
                raise Refused(f"'{eid}' is already in the model or given twice; a fill only adds")
            given.add(eid)
            if not os.path.isfile(inside(root, e["doc"], f"the page for '{eid}'")):
                raise Refused(f"the page for '{eid}' is not on disk at '{e['doc']}'")
            new = {"id": eid, "slug": e["slug"]}
            if parent:
                pref = e.get(parent)
                known = _ids(spine, pkey) | {x.get("id") for x in (fills.get(pkey) or [])}
                if not pref or pref not in known:
                    raise Refused(f"{fkey} entry '{eid}' names {parent} '{pref}', which is in "
                                  "neither the model nor this fill")
                new[parent] = pref
            new["intents"] = [intent]
            new["status"] = "proposed"
            if fkey in ("domains", "capabilities"):
                new["detail"] = "directional"
            new["one_line"] = e["one_line"]
            new["doc"] = e["doc"]
            new["metadata"] = dict(MARK)
            out.append(new)
        entries[skey] = out
    ices = []
    for e in fills.get("ices") or []:
        if "ices" not in spine:
            raise Refused("this model keeps each ICE inside its part's page (the spine has no "
                          "`ices` list); write the ICE there, not as its own entry")
        eid = e.get("id")
        for field in ("id", "for", "for_kind", "doc"):
            if not e.get(field):
                raise Refused(f"ice entry '{eid}' has no {field}")
        if eid in seen or eid in given:
            raise Refused(f"'{eid}' is already in the model or given twice; a fill only adds")
        given.add(eid)
        pkey = {"capability": "capabilities", "feature": "features"}.get(e["for_kind"])
        if pkey is None:
            raise Refused(f"ice entry '{eid}' has for_kind '{e['for_kind']}'; "
                          "it must be capability or feature")
        if e["for"] not in _ids(spine, pkey) | {x["id"] for x in entries[pkey]}:
            raise Refused(f"ice entry '{eid}' is for '{e['for']}', which is not a {e['for_kind']} "
                          "in the model or this fill")
        if not os.path.isfile(inside(root, e["doc"], f"the page for '{eid}'")):
            raise Refused(f"the page for '{eid}' is not on disk at '{e['doc']}'")
        ices.append({"id": eid, "for": e["for"], "for_kind": e["for_kind"], "doc": e["doc"],
                     "metadata": dict(MARK)})
    entries["ices"] = ices
    page = intent_page(root, intent)
    if any(entries.values()) and not os.path.isfile(page):
        raise Refused(f"the intent page intents/{intent}.md is missing; write it first (C1)")
    return entries, page


def undo(root, intent, result_path):
    """Take back the Touches lines a run added to the intent page (a change at the checkpoint)."""
    with open(result_path, encoding="utf-8") as fh:
        result = json.load(fh)
    page = intent_page(root, intent)
    added = list(result.get("touches_added") or [])
    if not added or not os.path.isfile(page):
        return {"ok": True, "undone": [], "page": f"intents/{intent}.md"}
    with open(page, encoding="utf-8") as fh:
        text = fh.read()
    if result.get("intent_page_after") == text and result.get("intent_page_before") is not None:
        atomic_write(page, result["intent_page_before"])
        return {"ok": True, "undone": added, "page": f"intents/{intent}.md", "how": "put back"}
    gone = set(added)
    lines = [ln for ln in text.splitlines() if ln.strip() not in gone]
    had_list = bool(touches.read(result.get("intent_page_before") or ""))
    if not had_list and not touches.read("\n".join(lines)):
        # The run made the Touches heading; with its lines gone, the heading goes too.
        at = next((i for i, ln in enumerate(lines) if ln.strip().startswith(touches.HEADER)), None)
        if at is not None:
            del lines[at]
            if at < len(lines) and at > 0 and not lines[at].strip() and not lines[at - 1].strip():
                del lines[at]
    atomic_write(page, "\n".join(lines).rstrip("\n") + "\n")
    return {"ok": True, "undone": added, "page": f"intents/{intent}.md", "how": "lines removed"}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Add the parts the slice needs to the spine.")
    ap.add_argument("--root", required=True)
    ap.add_argument("--spine")
    ap.add_argument("--fills")
    ap.add_argument("--intent", required=True)
    ap.add_argument("--out")
    ap.add_argument("--undo", help="a persist-fills.json: take back the Touches lines it added")
    args = ap.parse_args(argv)

    def finish(result, code):
        text = json.dumps(result, indent=2)
        print(text)
        if args.out:
            with open(args.out, "w", encoding="utf-8") as fh:
                fh.write(text + "\n")
        return code

    if args.undo:
        try:
            return finish(undo(args.root, args.intent, args.undo), 0)
        except Refused as exc:
            sys.stderr.write(f"persist_fills.py: not undone — {exc}\n")
            return finish({"ok": False, "refused": str(exc)}, 2)
        except (OSError, json.JSONDecodeError) as exc:
            return finish({"ok": False, "refused": f"cannot read an input: {exc}"}, 2)
    if not args.spine or not args.fills:
        sys.stderr.write("persist_fills.py: give --spine and --fills (or --undo)\n")
        return 2

    try:
        with open(args.spine, encoding="utf-8") as fh:
            old_text = fh.read()
        spine = yaml.safe_load(old_text) or {}
        if not isinstance(spine, dict):
            raise Refused("the spine must be a YAML mapping")
        old_spine = copy.deepcopy(spine)
        model_names.check_spine(spine, args.spine)
        with open(args.fills, encoding="utf-8") as fh:
            fills = json.load(fh) or {}
        if not isinstance(fills, dict):
            raise Refused("fills.json must hold one JSON object")
        entries, page = plan(args.root, spine, fills, args.intent)
    except Refused as exc:
        sys.stderr.write(f"persist_fills.py: not written — {exc}\n")
        return finish({"ok": False, "refused": str(exc)}, 2)
    except (OSError, yaml.YAMLError, json.JSONDecodeError) as exc:
        return finish({"ok": False, "refused": f"cannot read an input: {exc}"}, 2)

    written = {k: [e["id"] for e in v] for k, v in entries.items()}
    allow = []
    result = {"ok": True, "written": written, "allow": allow, "touches_added": [],
              "intent_page_before": None, "intent_page_after": None}
    if any(entries.values()):
        for key, items in entries.items():
            if items:
                spine.setdefault(key, [])
                if spine[key] is None:
                    spine[key] = []
                spine[key].extend(items)
                allow += [f"product-os/{e['doc']}" for e in items]
        atomic_write(args.spine, spine_text.dump(old_text, old_spine, spine)[0])
        links = []
        for key, kind in (("domains", "domain"), ("capabilities", "capability")):
            for e in entries[key]:
                links.append(touches.entry(e["slug"], touches.rel(page, os.path.join(args.root, e["doc"])),
                                           kind, "adds"))
        if links:
            with open(page, encoding="utf-8") as fh:
                text = fh.read()
            listed = {e["link"] for e in touches.read(text)}
            new_text = touches.upsert(text, links)
            atomic_write(page, new_text)
            result["touches_added"] = [line for line in touches.render(
                [e for e in links if e["link"] not in listed])[1:]]
            result["intent_page_before"] = text
            result["intent_page_after"] = new_text
        allow.append(f"product-os/intents/{args.intent}.md")
    return finish(result, 0)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
