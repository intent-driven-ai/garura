#!/usr/bin/env python3
"""
link_part.py — put a part's page into the product model's spine (link-model-part, #979).

The page skill (`enrich-grounding`) already wrote or changed each part's page. This script does
the shared part no page skill does: the part's entry in the spine (`_spine.yaml`, the model's
index of every part) and, for a thin capability or feature, the thin mark — `metadata.thin: true`
on its entry and exactly one Thin line on its page, just before its ICE — the one line the ontology fixes. A domain carries no ICE,
so it is never thin.

    python3 link_part.py --request <working>/link-request.json --product-base <product_base> \
        --out <working>/link-report.json

link-request.json:
    {"by": "<the play or run that asks>",
     "parts": [
       {"id": "dom-care", "kind": "domain", "mode": "new", "slug": "care", "intents": ["bi-1"],
        "one_line": "...", "doc": "care/domain.md"},
       {"id": "cap-booking", "kind": "capability", "mode": "new", "slug": "booking",
        "domain": "dom-care", "intents": ["bi-1"], "one_line": "...",
        "doc": "care/booking/capability.md", "issue": 12, "identified_by": "", "thin": true},
       {"id": "fn-806", "kind": "feature", "mode": "new", "slug": "fn-806", "capability": "cap-719",
        "intents": ["bi-717"], "one_line": "...", "doc": "features/fn-806/feature.md",
        "issue": 806, "identified_by": "", "thin": true},
       {"id": "fn-628", "kind": "feature", "mode": "update", "one_line": "...", "add_intents": [],
        "thin": true}]}

`features` in place of `parts` is read as a list of features (kind feature), as before.

- mode `new`: the id must not be in the spine; its parent (a capability's domain, a feature's
  capability), when given, must be; its page must be on disk, in its folder:
    domain      `<folder>/domain.md`, one folder under the model root;
    capability  the holding folder `capabilities/<id>/capability.md`, or
                `<folder of its domain's page>/<folder>/capability.md`;
    feature     the holding folder `features/<id>/feature.md`, or
                `<folder of its capability's page>/<folder>/feature.md`.
  The entry gets status proposed (and detail directional for a domain or capability), its
  empty lists, and metadata {created_by, deepen: true, thin when thin}.
- mode `update`: the id must be in the spine under its kind. `one_line` replaces its one-line,
  `add_intents` are added to its intents, `issue` names its issue when it names none yet, `thin:
  true` sets the thin mark, and metadata.updated_by is set. Every other field is kept.
- kind `slice`, mode `update` only (a slice is shaped by /shape-slice): `add_features` are added
  to its `feature_refs`, in their order, at the end or right after the feature named by `after`;
  a feature already there is not added twice, and each must be in the spine (#931).

Every check runs before the first write; any failure refuses the whole request (exit 2) and
writes nothing. When a write itself fails part way, every file already written is put back as
it was, so the spine and the pages never disagree (exit 2). Paths that leave the model folder are refused. Every intent a part names must
have its page. The spine keeps its comments and layout (spine_text.py); every file is written
through safe_write.atomic_write. Reads and writes files on disk only; no git, no network.
Exit 0 written, 2 refused or bad input.
"""

import argparse
import copy
import json
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import model_names  # noqa: E402  (stamped beside this script)
import safe_write  # noqa: E402  (stamped beside this script)
import spine_text  # noqa: E402  (stamped beside this script)

KINDS = {"domain": "domains", "capability": "capabilities", "feature": "features", "slice": "slices"}
PARENT = {"capability": "domain", "feature": "capability"}
HOLDING = {"capability": "capabilities", "feature": "features"}
PAGE = {"domain": "domain.md", "capability": "capability.md", "feature": "feature.md"}
ICE_HEADINGS = ("## Agent intent (ICE)", "## Intent")
OLD_THIN = re.compile(r"^\s*(?:>\s*)?\**Thin(?: ICE)?\**\s*:", re.I)
NEW_KEYS = ("id", "slug", "intents", "one_line", "doc")
NOT_A_DOMAIN_FOLDER = {"capabilities", "features", "intents"}


class Refused(Exception):
    pass


# The one Thin line the ontology fixes (ontology v14); any line that starts "Thin:" just before
# the ICE counts as the mark, and marking a page again replaces an older line with this one.
THIN_LINE = "Thin: proposed from the person's words; deepen with `/discover-capabilities`."


def inside(root, rel):
    if not rel or os.path.isabs(rel) or ".." in rel.split("/"):
        raise Refused(f"the path {rel!r} leaves the model folder")
    full = os.path.realpath(os.path.join(root, rel))
    if not full.startswith(os.path.realpath(root) + os.sep):
        raise Refused(f"the path {rel!r} leaves the model folder")
    return full


def with_thin_line(text, line):
    """The page with exactly one Thin line, just before its ICE heading; None when it has none."""
    lines = [ln for ln in text.splitlines() if not OLD_THIN.match(ln)]
    at = next((i for i, ln in enumerate(lines) if ln.strip() in ICE_HEADINGS), None)
    if at is None:
        return None
    before = lines[:at]
    while before and not before[-1].strip():
        before.pop()
    return "\n".join(before + ([""] if before else []) + [line, ""] + lines[at:]).rstrip("\n") + "\n"


def allowed_docs(kind, pid, doc, parent_entry):
    if kind == "domain":
        folder = os.path.dirname(doc)
        ok = "/" not in folder and folder and folder not in NOT_A_DOMAIN_FOLDER
        return {doc} if ok and doc == f"{folder}/domain.md" else set()
    allowed = {f"{HOLDING[kind]}/{pid}/{PAGE[kind]}"}
    if parent_entry:
        parent_dir = os.path.dirname(parent_entry.get("doc", ""))
        allowed.add(f"{parent_dir}/{os.path.basename(os.path.dirname(doc))}/{PAGE[kind]}")
    return allowed


def new_entry(kind, p, by):
    e = {"id": p["id"], "slug": p["slug"]}
    if kind in PARENT:
        e[PARENT[kind]] = p.get(PARENT[kind], "")
    e["intents"] = list(p["intents"])
    e["status"] = "proposed"
    if kind in ("domain", "capability"):
        e["detail"] = "directional"
    e["one_line"] = p["one_line"]
    e["doc"] = p["doc"].strip("/")
    if kind != "domain":
        e["depends_on"] = []
        e["identified_by"] = p.get("identified_by", "")
    e["decisions"] = []
    if p.get("issue") is not None:
        e["issue"] = p["issue"]
    e["metadata"] = {"created_by": by, "deepen": True}
    return e


def plan(root, spine, request):
    if not isinstance(request, dict):
        raise Refused("the request is not a JSON object")
    by = request.get("by") or "a play"
    parts = request.get("parts")
    if parts is None:
        features = request.get("features") or []
        if not isinstance(features, list) or not all(isinstance(f, dict) for f in features):
            raise Refused("`features` must be a list of objects")
        parts = [dict(f, kind="feature") for f in features]
    if not isinstance(parts, list) or not all(isinstance(p, dict) for p in parts):
        raise Refused("`parts` must be a list of objects")
    new_spine = copy.deepcopy(spine)
    index = {kind: {e["id"]: e for e in new_spine.setdefault(key, [])} for kind, key in KINDS.items()}
    before = {kind: set(ids) for kind, ids in index.items()}
    pages, intents, seen = {}, set(), set()
    report = {"written": [], "updated": [], "thin": [], "changed": []}
    for p in parts:
        pid, kind, mode = p.get("id"), p.get("kind"), p.get("mode")
        if not pid or kind not in KINDS or mode not in ("new", "update"):
            raise Refused(f"each part needs an id, a kind (domain, capability, feature or slice) and a "
                          f"mode (new or update): {p!r}")
        if pid in seen:
            raise Refused(f"{pid} is given twice")
        seen.add(pid)
        if kind == "slice":
            if mode != "update" or p.get("thin"):
                raise Refused(f"{pid}: a slice is only updated here (add_features); /shape-slice shapes a slice")
            if pid not in before["slice"]:
                raise Refused(f"{pid} is not in the spine as a slice")
            entry = index["slice"][pid]
            refs = entry.setdefault("feature_refs", [])
            after = p.get("after")
            if after is not None and after not in refs:
                raise Refused(f"{pid}: {after} is not one of its features")
            at = refs.index(after) + 1 if after is not None else len(refs)
            for fid in p.get("add_features") or []:
                if fid not in index["feature"]:
                    raise Refused(f"{pid}: the feature {fid} is not in the spine")
                if fid not in refs:
                    refs.insert(at, fid)
                    at += 1
            report["updated"].append(pid)
            continue
        if p.get("thin") and kind == "domain":
            raise Refused(f"{pid}: a domain carries no ICE, so it cannot be thin")
        if mode == "new":
            if any(pid in ids for ids in before.values()):
                raise Refused(f"{pid} is already in the spine; use mode update")
            missing = [k for k in NEW_KEYS if k not in p]
            if missing:
                raise Refused(f"{pid}: a new {kind} needs {', '.join(missing)}")
            parent_entry = None
            if kind in PARENT and p.get(PARENT[kind]):
                parent_kind = PARENT[kind]
                parent_entry = index[parent_kind].get(p[PARENT[kind]])
                if parent_entry is None:
                    raise Refused(f"{pid}: its {parent_kind} {p[PARENT[kind]]} is not in the spine")
            doc = p["doc"].strip("/")
            if not os.path.isfile(inside(root, doc)):
                raise Refused(f"{pid}: its page {doc} is not on disk; write the page first")
            if doc not in allowed_docs(kind, pid, doc, parent_entry):
                raise Refused(f"{pid}: its page {doc} is outside its folder")
            entry = new_entry(kind, p, by)
            new_spine[KINDS[kind]].append(entry)
            index[kind][pid] = entry
            report["written"].append(pid)
        else:
            if pid not in before[kind]:
                raise Refused(f"{pid} is not in the spine as a {kind}; use mode new")
            entry = index[kind][pid]
            if "one_line" in p:
                entry["one_line"] = p["one_line"]
            if p.get("issue") is not None and kind != "domain":
                if entry.get("issue") not in (None, "", p["issue"]):
                    raise Refused(f"{pid} already names issue {entry['issue']}")
                entry["issue"] = p["issue"]
            for i in p.get("add_intents") or []:
                if i not in entry.setdefault("intents", []):
                    entry["intents"].append(i)
            entry.setdefault("metadata", {})["updated_by"] = by
            report["updated"].append(pid)
        intents.update(entry.get("intents") or [])
        if p.get("thin"):
            page = inside(root, entry["doc"])
            if not os.path.isfile(page):
                raise Refused(f"{pid}: its page {entry['doc']} is not on disk")
            with open(page, encoding="utf-8") as fh:
                text = fh.read()
            new_text = with_thin_line(text, THIN_LINE)
            if new_text is None:
                raise Refused(f"{pid}: its page has no ICE section to mark thin")
            entry.setdefault("metadata", {})["thin"] = True
            if new_text != text:
                pages[page] = new_text
            report["thin"].append(pid)
    for i in sorted(intents):
        if not os.path.isfile(inside(root, f"intents/{i}.md")):
            raise Refused(f"the business intent {i} has no page in the model")
    return new_spine, pages, report


def write_all(writes):
    """Write every (path, text); when one write fails, put back each file already written
    (its old text, or no file when it was new) and raise the error."""
    done = []
    try:
        for path, text in writes:
            old = None
            if os.path.exists(path):
                with open(path, encoding="utf-8") as fh:
                    old = fh.read()
            safe_write.atomic_write(path, text)
            done.append((path, old))
    except OSError:
        for path, old in reversed(done):
            if old is None:
                os.remove(path)
            else:
                safe_write.atomic_write(path, old)
        raise


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--request", required=True)
    ap.add_argument("--product-base", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    root = os.path.join(a.product_base, "product-os")
    spine_path = os.path.join(root, "_spine.yaml")
    try:
        with open(a.request, encoding="utf-8") as fh:
            request = json.load(fh)
        with open(spine_path, encoding="utf-8") as fh:
            old_text = fh.read()
        spine = yaml.safe_load(old_text) or {}
        model_names.check_spine(spine, spine_path)
        new_spine, pages, report = plan(root, spine, request)
        model_names.check_spine(new_spine, spine_path)
    except (Refused, OSError, ValueError, json.JSONDecodeError, yaml.YAMLError) as e:
        sys.stderr.write(f"link_part.py: refused, nothing written: {e}\n")
        return 2
    text, kept = spine_text.dump(old_text, spine, new_spine)
    try:
        write_all([(spine_path, text)] + list(pages.items()))
    except OSError as e:
        sys.stderr.write(f"link_part.py: a write failed, every file is back as it was: {e}\n")
        return 2
    report["changed"].append(os.path.relpath(spine_path, a.product_base))
    for page in pages:
        report["changed"].append(os.path.relpath(page, a.product_base))
    report["layout_kept"] = kept
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print(json.dumps(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
