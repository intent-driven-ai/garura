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

The result names `allow`: the model paths this run may change for the fills, for the scoped
write guard. Reads and writes files on disk only; no git, no network.
Exit 0 written (or nothing to write), 2 refused or usage error.
"""

import argparse
import json
import os
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("persist_fills.py: PyYAML is required (pip install pyyaml).\n")
    sys.exit(2)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import intent_touches as touches  # noqa: E402  (stamped from create-play/references)
import model_names  # noqa: E402  (stamped from create-play/references)

KINDS = (  # (fills key, spine key, touches kind, parent field, parent spine key)
    ("domains", "domains", "domain", None, None),
    ("capabilities", "capabilities", "capability", "domain", "domains"),
    ("features", "features", "feature", "capability", "capabilities"),
)
MARK = {"created_by": "/shape-slice", "deepen": True}


class Refused(Exception):
    """The fills cannot be written; the message says why."""


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
            if not os.path.isfile(os.path.join(root, e["doc"])):
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
        if not os.path.isfile(os.path.join(root, e["doc"])):
            raise Refused(f"the page for '{eid}' is not on disk at '{e['doc']}'")
        ices.append({"id": eid, "for": e["for"], "for_kind": e["for_kind"], "doc": e["doc"],
                     "metadata": dict(MARK)})
    entries["ices"] = ices
    page = os.path.join(root, "intents", f"{intent}.md")
    if any(entries.values()) and not os.path.isfile(page):
        raise Refused(f"the intent page intents/{intent}.md is missing; write it first (C1)")
    return entries, page


def main(argv=None):
    ap = argparse.ArgumentParser(description="Add the parts the slice needs to the spine.")
    ap.add_argument("--root", required=True)
    ap.add_argument("--spine", required=True)
    ap.add_argument("--fills", required=True)
    ap.add_argument("--intent", required=True)
    ap.add_argument("--out")
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
    if any(entries.values()):
        for key, items in entries.items():
            if items:
                spine.setdefault(key, [])
                if spine[key] is None:
                    spine[key] = []
                spine[key].extend(items)
                allow += [f"product-os/{e['doc']}" for e in items]
        with open(args.spine, "w", encoding="utf-8") as fh:
            yaml.safe_dump(spine, fh, sort_keys=False, allow_unicode=True)
        links = []
        for key, kind in (("domains", "domain"), ("capabilities", "capability")):
            for e in entries[key]:
                links.append(touches.entry(e["slug"], touches.rel(page, os.path.join(args.root, e["doc"])),
                                           kind, "adds"))
        if links:
            with open(page, encoding="utf-8") as fh:
                text = fh.read()
            with open(page, "w", encoding="utf-8") as fh:
                fh.write(touches.upsert(text, links))
        allow.append(f"product-os/intents/{args.intent}.md")
    return finish({"ok": True, "written": written, "allow": allow}, 0)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
