#!/usr/bin/env python3
"""
persist_fills.py — put in the spine the parts the slice needs (/shape-slice, C8, C16).

The fill skills already wrote each new part's page, and the edits to each existing part's
page, in the live model. This script writes the shared file and does the mechanical rest:

  - a NEW part (domain, capability, feature, ICE) gets one spine entry, marked to be deepened
    later (status proposed, detail directional where the kind has a detail field,
    metadata.deepen true);
  - an EXISTING part is filled (`updates`): the intent is added to its `intents`, its domain
    (a capability) or its capability (a feature) is set when it has none, and its page may
    hold the agent's edits (`page: true`); what is there is kept;
  - a part marked thin (`thin`) gets `metadata.thin: true` on its spine entry (the `ices`
    entry when the spine has an `ices` list, else the part's own entry), and its page holds
    exactly the one Thin line just before its ICE section;
  - when a fill gives a capability in the holding folder its domain, the capability's folder,
    and the folders of its features in the holding folder, move under the domain's folder;
    the same for a feature in the holding folder that gets its capability. Every link to a
    moved page, and every link inside one, is fixed;
  - each new domain and capability goes on the intent page's Touches list ("— adds"), and
    each filled domain or capability not listed yet ("— changes").

    python3 persist_fills.py --root <product-os dir> --spine <_spine.yaml> \\
        --fills <fills.json> --intent <bi-id> [--out <persist-fills.json>]

fills.json:
    {"domains":      [{"id", "slug", "one_line", "doc"}],
     "capabilities": [{"id", "slug", "domain", "one_line", "doc"}],
     "features":     [{"id", "slug", "capability", "one_line", "doc"}],
     "ices":         [{"id", "for", "for_kind", "doc"}],
     "thin":         ["<part id or ice id>", ...],
     "updates":      [{"id", "kind": "domain|capability|feature", "add_intents": [...],
                       "domain" | "capability": "<id>", "page": true}]}
Every list may be empty or missing. A capability's `domain` and a feature's `capability`
may be left out: the part then waits in its holding folder.

THE FOLDER RULE. A new page must be in its folder, else the fill is refused:
  - a domain page at `<d>/domain.md`;
  - a capability page at `<folder of its domain's page>/<folder>/capability.md`, or in the
    holding folder `capabilities/<id>/capability.md` while it has no domain;
  - a feature page at `<folder of its capability's page>/<folder>/feature.md`, or in the
    holding folder `features/<id>/feature.md` while it has no capability;
  - an ICE page at `<folder of its part's page>/ice.md`.
The parent's page is taken where it is after this run's moves.

It refuses with exit 2, and writes nothing, when: a new id is already in the spine or given
twice; an update names an id that is not in the spine, or a domain or capability other than
the one the part already has; a page is not on disk or is outside its folder; a parent is in
neither the spine nor this fill; an ICE is given but the spine has no `ices` list; a thin part
has no ICE section on its page; a move would land on a file or folder that is there; or the
intent page is missing. It also refuses any path or intent id that leaves the model folder
('..', an absolute path, or a symlink that points outside it). It calls the model_names guard
(#807) on the spine. Every check runs before the first write; the spine and each page are
written through a temp file and os.replace.

The result names what the scoped write guard needs: `allow` (the new paths: new pages and the
places pages moved to), `modify_only` (existing pages this run changed in place), and
`remove_only` (the places pages moved from), each as `product-os/<path>`; plus `written`,
`updated`, `moved` [{id, from, to}] (every part whose page moved, a feature that moved with
its capability's folder included; its page path before and after), `thin`, `relinked`, `touches_added`, `touches_relinked`
and the intent page's text before and after, so a change at the checkpoint can take the
intent page back:

    python3 persist_fills.py --undo <persist-fills.json> --root <product-os dir> --intent <bi-id>

--undo puts the intent page back as it was before the run when no one edited it since; else
it takes out only the lines this run added and puts back the lines it changed. Every line that
was on the page before the run is there after the undo, `**Touches:** none yet` included. The
spine is written back with its comments and layout kept (spine_text.py). Reads and writes files
on disk only; no git, no network. Exit 0 written, undone (or nothing to do), 2 refused or usage
error.
"""

import argparse
import copy
import json
import os
import re
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
KIND_KEY = {"domain": "domains", "capability": "capabilities", "feature": "features"}
PARENT = {"capability": ("domain", "domains"), "feature": ("capability", "capabilities")}
HOLDING = {"capability": "capabilities", "feature": "features"}
MARK = {"created_by": "/shape-slice", "deepen": True}
THIN_LINE = ("Thin: proposed by `/shape-slice` from the person's answers; deepen with "
             "`/discover-capabilities`.")
OLD_THIN = re.compile(r"^\s*(?:>\s*)?\**Thin(?: ICE)?\**\s*:", re.I)
INLINE_ICE = "## Agent intent (ICE)"
PAGE_ICE = "## Intent"
LINK = re.compile(r"\]\(([^)\s]+)\)")


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
    os.makedirs(folder, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".persist-fills-", suffix=".tmp", dir=folder)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _ids(spine, key):
    return {e.get("id") for e in (spine.get(key) or []) if isinstance(e, dict)}


def _entry(spine, key, eid):
    return next((e for e in (spine.get(key) or []) if isinstance(e, dict) and e.get("id") == eid),
                None)


def _norm(path):
    return os.path.normpath(path).replace(os.sep, "/")


def _empty(value):
    return value in (None, "", [])


class Plan:
    """Every write of the run, worked out before the first one."""

    def __init__(self, root, spine, fills, intent):
        self.root, self.spine, self.fills, self.intent = root, spine, fills, intent
        self.new = {"domains": [], "capabilities": [], "features": [], "ices": []}
        self.changed = {}        # (spine key, id) -> the entry as it will be
        self.updated = []        # ids filled by `updates`
        self.folder_moves = []   # (id, kind, old folder, new folder)
        self.moved_parts = []    # {id, from, to}: every part whose page moved (its doc)
        self.file_moves = {}     # old file -> new file, relative to the model
        self.thin = []
        self.page_edits = {}     # relative path -> new text (thin line)
        self.filled_pages = []   # relative paths of existing pages the agent edited
        self.touch_entries = []  # (kind, id, doc, mark)

    # -- lookups that see this run's changes --
    def entry(self, key, eid):
        if (key, eid) in self.changed:
            return self.changed[(key, eid)]
        new = next((e for e in self.new.get(key, []) if e["id"] == eid), None)
        return new or _entry(self.spine, key, eid)

    def doc_after(self, key, eid):
        e = self.entry(key, eid)
        return e.get("doc") if e else None

    def change(self, key, eid):
        if (key, eid) not in self.changed:
            self.changed[(key, eid)] = copy.deepcopy(_entry(self.spine, key, eid))
        return self.changed[(key, eid)]


def _moved_path(p, rel):
    return p.file_moves.get(rel, rel)


def plan_updates(p, seen_new):
    for u in p.fills.get("updates") or []:
        if not isinstance(u, dict):
            raise Refused("an entry in updates is not an object")
        eid, kind = u.get("id"), u.get("kind")
        if kind not in KIND_KEY:
            raise Refused(f"update '{eid}' has kind '{kind}'; it must be domain, capability or feature")
        key = KIND_KEY[kind]
        if _entry(p.spine, key, eid) is None:
            raise Refused(f"update '{eid}' names a {kind} that is not in the spine; a new part goes "
                          f"in `{key}`, not in `updates`")
        if eid in seen_new or eid in p.updated:
            raise Refused(f"'{eid}' is given twice in this fill")
        p.updated.append(eid)
        e = p.change(key, eid)
        add = u.get("add_intents") or []
        if not isinstance(add, list) or not all(isinstance(i, str) and i for i in add):
            raise Refused(f"update '{eid}' has add_intents that is not a list of intent ids")
        have = list(e.get("intents") or [])
        e["intents"] = have + [i for i in dict.fromkeys(add) if i not in have]
        if kind in PARENT:
            field, pkey = PARENT[kind]
            given = u.get(field)
            if not _empty(given):
                if not _empty(e.get(field)) and e.get(field) != given:
                    raise Refused(f"{kind} '{eid}' already has {field} '{e.get(field)}'; a fill keeps "
                                  f"what is there and does not change it to '{given}'")
                known = _ids(p.spine, pkey) | {x.get("id") for x in (p.fills.get(pkey) or [])
                                               if isinstance(x, dict)}
                if given not in known:
                    raise Refused(f"update '{eid}' names {field} '{given}', which is in neither the "
                                  "model nor this fill")
                e[field] = given
        if u.get("page") is True:
            doc = e.get("doc")
            if not doc or not os.path.isfile(inside(p.root, doc, f"the page for '{eid}'")):
                raise Refused(f"update '{eid}' says its page was edited, but no page is at '{doc}'")
            p.filled_pages.append(_norm(doc))
        if kind in ("domain", "capability"):
            p.touch_entries.append((kind, eid, key, "changes"))


def in_holding(doc, kind, eid):
    parts = _norm(doc or "").split("/")
    return len(parts) >= 2 and parts[0] == HOLDING[kind]


def plan_moves(p):
    """A capability (or feature) in the holding folder that now has its parent moves under it."""
    def move_folder(eid, kind, key, parent_doc):
        e = p.entry(key, eid)
        doc = _norm(e.get("doc") or "")
        if not doc or not in_holding(doc, kind, eid):
            return
        old = os.path.dirname(doc)
        new = _norm(os.path.join(os.path.dirname(parent_doc), os.path.basename(old)))
        if old == new:
            return
        inside(p.root, new, f"the new folder of '{eid}'")
        if not os.path.isdir(inside(p.root, old, f"the folder of '{eid}'")):
            raise Refused(f"the page of '{eid}' is not on disk at '{doc}'")
        p.folder_moves.append((eid, kind, old, new))
        for dirpath, _dirs, files in os.walk(os.path.join(p.root, old)):
            for fn in files:
                full = _norm(os.path.relpath(os.path.join(dirpath, fn), p.root))
                dest = new + full[len(old):]
                if os.path.exists(os.path.join(p.root, dest)):
                    raise Refused(f"'{eid}' would move '{full}' to '{dest}', but a file is there "
                                  "already")
                p.file_moves[full] = dest

    for (key, eid), e in list(p.changed.items()):
        if key == "capabilities" and not _empty(e.get("domain")):
            ddoc = p.doc_after("domains", e["domain"])
            if ddoc:
                move_folder(eid, "capability", key, ddoc)
    moved_caps = {eid for eid, kind, _o, _n in p.folder_moves if kind == "capability"}
    for f in p.spine.get("features") or []:
        if not isinstance(f, dict):
            continue
        cur = p.entry("features", f.get("id"))
        cap = cur.get("capability")
        if _empty(cap) or not in_holding(cur.get("doc"), "feature", f.get("id")):
            continue
        gained = _empty(f.get("capability")) and f.get("id") in p.updated
        cdoc = p.doc_after("capabilities", cap)
        if cdoc and (cap in moved_caps or gained):
            move_folder(f.get("id"), "feature", "features", _moved_path(p, _norm(cdoc)))
    # every spine entry whose page moved gets its new doc
    for key in ("domains", "capabilities", "features", "ices"):
        for e in p.spine.get(key) or []:
            if not isinstance(e, dict):
                continue
            doc = _norm(e.get("doc") or "")
            if doc in p.file_moves:
                p.change(key, e.get("id"))["doc"] = p.file_moves[doc]
                p.moved_parts.append({"id": e.get("id"), "from": doc, "to": p.file_moves[doc]})


def expected_folder(p, kind, e):
    """(prefix, why) the new page must sit in, by the folder rule."""
    if kind == "domain":
        return None
    field, pkey = PARENT[kind]
    parent = e.get(field)
    if _empty(parent):
        return f"{HOLDING[kind]}/{e['id']}/"
    pdoc = p.doc_after(pkey, parent)
    if not pdoc:
        return None
    base = os.path.dirname(_norm(pdoc))
    return (base + "/") if base else ""


def check_folder(p, kind, e):
    doc = _norm(e["doc"])
    name = {"domain": "domain.md", "capability": "capability.md", "feature": "feature.md"}[kind]
    parts = doc.split("/")
    if kind == "domain":
        if len(parts) != 2 or parts[1] != name:
            raise Refused(f"the page for '{e['id']}' is at '{doc}', outside its folder; a domain page "
                          f"is at '<domain folder>/{name}'")
        return
    prefix = expected_folder(p, kind, e)
    if prefix is None:
        return
    rest = doc[len(prefix):] if doc.startswith(prefix) else None
    holding = prefix.startswith(HOLDING[kind] + "/")
    ok = rest is not None and (rest == name if holding else
                               (len(rest.split("/")) == 2 and rest.split("/")[1] == name))
    if not ok:
        want = prefix + name if holding else f"{prefix}<folder>/{name}"
        raise Refused(f"the page for '{e['id']}' is at '{doc}', outside its folder; put it at '{want}'")


def plan_new(p, seen, given):
    for fkey, skey, kind, parent, pkey in KINDS:
        for e in p.fills.get(fkey) or []:
            if not isinstance(e, dict):
                raise Refused(f"an entry in {fkey} is not an object")
            eid = e.get("id")
            for field in ("id", "slug", "one_line", "doc"):
                if not e.get(field):
                    raise Refused(f"{fkey} entry '{eid}' has no {field}")
            if eid in seen or eid in given or eid in p.updated:
                raise Refused(f"'{eid}' is already in the model or given twice; a new part is not "
                              "in the spine (fill an existing part with `updates`)")
            given.add(eid)
            if not os.path.isfile(inside(p.root, e["doc"], f"the page for '{eid}'")):
                raise Refused(f"the page for '{eid}' is not on disk at '{e['doc']}'")
            new = {"id": eid, "slug": e["slug"]}
            if parent:
                pref = e.get(parent)
                if not _empty(pref):
                    known = _ids(p.spine, pkey) | {x.get("id") for x in (p.fills.get(pkey) or [])
                                                   if isinstance(x, dict)}
                    if pref not in known:
                        raise Refused(f"{fkey} entry '{eid}' names {parent} '{pref}', which is in "
                                      "neither the model nor this fill")
                    new[parent] = pref
                else:
                    new[parent] = ""
            new["intents"] = [p.intent]
            new["status"] = "proposed"
            if fkey in ("domains", "capabilities"):
                new["detail"] = "directional"
            new["one_line"] = e["one_line"]
            new["doc"] = _norm(e["doc"])
            new["metadata"] = dict(MARK)
            p.new[skey].append(new)


def plan_places(p, seen, given):
    """The folder rule for each new page, and the new ICE entries, after this run's moves."""
    for fkey, skey, kind, _parent, _pkey in KINDS:
        for e in p.new[skey]:
            check_folder(p, kind, e)
            if kind in ("domain", "capability"):
                p.touch_entries.append((kind, e["id"], skey, "adds"))
    for e in p.fills.get("ices") or []:
        if "ices" not in p.spine:
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
        if p.entry(pkey, e["for"]) is None:
            raise Refused(f"ice entry '{eid}' is for '{e['for']}', which is not a {e['for_kind']} "
                          "in the model or this fill")
        if not os.path.isfile(inside(p.root, e["doc"], f"the page for '{eid}'")):
            raise Refused(f"the page for '{eid}' is not on disk at '{e['doc']}'")
        want = _norm(os.path.join(os.path.dirname(_norm(p.doc_after(pkey, e["for"]))), "ice.md"))
        if _norm(e["doc"]) != want:
            raise Refused(f"the ICE page '{eid}' is at '{e['doc']}', outside its folder; put it at "
                          f"'{want}'")
        p.new["ices"].append({"id": eid, "for": e["for"], "for_kind": e["for_kind"],
                              "doc": _norm(e["doc"]), "metadata": dict(MARK)})


def thin_page_text(text, heading):
    """The page with exactly one Thin line, just before its ICE heading; None when it has none."""
    lines = text.splitlines()
    kept = [ln for ln in lines if not OLD_THIN.match(ln) and ln.strip() != THIN_LINE]
    at = next((i for i, ln in enumerate(kept) if ln.strip() == heading), None)
    if at is None:
        return None
    before = kept[:at]
    while before and not before[-1].strip():
        before.pop()
    before = before + ([""] if before else []) + [THIN_LINE, ""]
    return "\n".join(before + kept[at:]).rstrip("\n") + "\n"


def plan_thin(p):
    ices_model = "ices" in p.spine
    for tid in p.fills.get("thin") or []:
        target_key, target = None, None
        if ices_model:
            ice = p.entry("ices", tid)
            if ice is None:
                part = p.entry("capabilities", tid) or p.entry("features", tid)
                if part is not None:
                    ice = next((x for x in list(p.spine.get("ices") or []) + p.new["ices"]
                                if isinstance(x, dict) and x.get("for") == tid), None)
                    ice = p.entry("ices", ice["id"]) if ice else None
            if ice is None:
                raise Refused(f"'{tid}' is marked thin, but it has no ICE in the `ices` list")
            target_key, target, heading = "ices", ice, PAGE_ICE
        else:
            for key in ("capabilities", "features"):
                if p.entry(key, tid) is not None:
                    target_key, target = key, p.entry(key, tid)
            if target is None:
                raise Refused(f"'{tid}' is marked thin, but it is not a capability or feature in "
                              "the model or this fill")
            heading = INLINE_ICE
        if target in p.new[target_key]:
            entry = target
        else:
            entry = p.change(target_key, target["id"])
        meta = dict(entry.get("metadata") or {})
        meta["thin"] = True
        entry["metadata"] = meta
        doc = _norm(entry["doc"])
        src = next((old for old, new in p.file_moves.items() if new == doc), doc)
        text = _read(inside(p.root, src, f"the page of '{tid}'"))
        new_text = thin_page_text(text, heading)
        if new_text is None:
            raise Refused(f"'{tid}' is marked thin, but its page '{doc}' has no '{heading}' "
                          "section; write the thin ICE there first")
        if new_text != text:
            p.page_edits[doc] = new_text
        p.thin.append(tid)


def build(root, spine, fills, intent):
    p = Plan(root, spine, fills, intent)
    seen = set()
    for key in ("domains", "capabilities", "features", "ices"):
        seen |= _ids(spine, key)
    news = {e.get("id") for k in ("domains", "capabilities", "features", "ices")
            for e in (fills.get(k) or []) if isinstance(e, dict)}
    given = set()
    plan_updates(p, news)
    plan_new(p, seen, given)
    plan_moves(p)
    plan_places(p, seen, given)
    plan_thin(p)
    page = intent_page(root, intent)
    if (any(p.new.values()) or p.changed) and not os.path.isfile(page):
        raise Refused(f"the intent page intents/{intent}.md is missing; write it first (C1)")
    return p, page


def fix_links(root, file_moves):
    """Fix every link to a moved page, and every link inside one. Returns {rel path: new text}."""
    if not file_moves:
        return {}
    back = {new: old for old, new in file_moves.items()}
    out = {}
    for dirpath, _dirs, files in os.walk(root):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            here = _norm(os.path.relpath(os.path.join(dirpath, fn), root))
            was = back.get(here, here)
            text = _read(os.path.join(dirpath, fn))

            def repl(m):
                target = m.group(1)
                if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith(("#", "/")):
                    return m.group(0)
                path, _, anchor = target.partition("#")
                if not path:
                    return m.group(0)
                old = _norm(os.path.join(os.path.dirname(was), path))
                new = file_moves.get(old, old)
                if here == was and new == old:
                    return m.group(0)
                link = os.path.relpath(new, os.path.dirname(here) or ".").replace(os.sep, "/")
                return "](" + link + (("#" + anchor) if anchor else "") + ")"

            new_text = LINK.sub(repl, text)
            if new_text != text:
                out[here] = new_text
    return out


def undo(root, intent, result_path):
    """Take back the intent page lines a run added or changed (a change at the checkpoint)."""
    with open(result_path, encoding="utf-8") as fh:
        result = json.load(fh)
    page = intent_page(root, intent)
    added = list(result.get("touches_added") or [])
    relinked = list(result.get("touches_relinked") or [])
    if (not added and not relinked) or not os.path.isfile(page):
        return {"ok": True, "undone": [], "page": f"intents/{intent}.md"}
    text = _read(page)
    if result.get("intent_page_after") == text and result.get("intent_page_before") is not None:
        atomic_write(page, result["intent_page_before"])
        return {"ok": True, "undone": added, "page": f"intents/{intent}.md", "how": "put back"}
    gone = set(added)
    back = {r["after"]: r["before"] for r in relinked if isinstance(r, dict)}
    lines = []
    for ln in text.splitlines():
        if ln.strip() in gone:
            continue
        lines.append(back.get(ln.strip(), ln))
    before = result.get("intent_page_before") or ""
    old_header = next((ln for ln in before.splitlines() if ln.strip().startswith(touches.HEADER)), None)
    at = next((i for i, ln in enumerate(lines) if ln.strip().startswith(touches.HEADER)), None)
    if at is not None and not touches.read("\n".join(lines)):
        if old_header is not None:
            # The page had the heading before the run (for example "none yet"): it keeps it.
            lines[at] = old_header
        else:
            # The run made the Touches heading; with its lines gone, the heading goes too.
            del lines[at]
            if at < len(lines) and at > 0 and not lines[at].strip() and not lines[at - 1].strip():
                del lines[at]
    atomic_write(page, "\n".join(lines).rstrip("\n") + "\n")
    return {"ok": True, "undone": added, "page": f"intents/{intent}.md", "how": "lines removed"}


def apply(args, spine, old_text, old_spine, p, page):
    root = args.root
    result = {"ok": True, "written": {k: [e["id"] for e in v] for k, v in p.new.items()},
              "updated": list(p.updated), "moved": [], "thin": list(p.thin), "relinked": [],
              "allow": [], "modify_only": [], "remove_only": [], "touches_added": [],
              "touches_relinked": [], "intent_page_before": None, "intent_page_after": None}
    if not any(p.new.values()) and not p.changed:
        return result
    page_rel = f"intents/{args.intent}.md"
    page_before = _read(page)
    # 1. moves, file by file (a new page may already sit in the folder a part moves to)
    for old, new in sorted(p.file_moves.items()):
        dest = os.path.join(root, new)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        os.rename(os.path.join(root, old), dest)
    for eid, _kind, old, new in p.folder_moves:
        for dirpath, _dirs, _files in sorted(os.walk(os.path.join(root, old)), reverse=True):
            if os.path.isdir(dirpath) and not os.listdir(dirpath):
                os.rmdir(dirpath)
    result["moved"] = list(p.moved_parts)
    # 2. the thin line on each thin page (at its new place)
    for rel, text in p.page_edits.items():
        atomic_write(os.path.join(root, rel), text)
    # 3. every link to a moved page, and inside one
    for rel, text in fix_links(root, p.file_moves).items():
        atomic_write(os.path.join(root, rel), text)
        if rel not in p.file_moves.values() and rel != page_rel:
            result["relinked"].append(rel)
    # 4. the spine
    for key, items in p.new.items():
        if items:
            if spine.get(key) is None:
                spine[key] = []
            spine[key].extend(items)
    for (key, eid), entry in p.changed.items():
        spine[key] = [entry if isinstance(e, dict) and e.get("id") == eid else e
                      for e in spine.get(key) or []]
    atomic_write(args.spine, spine_text.dump(old_text, old_spine, spine)[0])
    # 5. the intent page's Touches list
    text = _read(page)
    links = []
    for kind, eid, key, mark in p.touch_entries:
        e = p.entry(key, eid)
        links.append(touches.entry(e.get("slug") or eid,
                                   touches.rel(page, os.path.join(root, e["doc"])), kind, mark))
    listed = {e["link"] for e in touches.read(text)}
    new_text = touches.upsert(text, links) if links else text
    if new_text != text:
        atomic_write(page, new_text)
    after = _read(page)
    before_lines = {ln.strip() for ln in page_before.splitlines()}
    result["touches_added"] = [line for line in touches.render(
        [e for e in links if e["link"] not in listed])[1:]]
    if p.file_moves:
        for ln in page_before.splitlines():
            fixed = fix_line(ln, page_rel, p.file_moves)
            if fixed != ln and fixed.strip() not in before_lines:
                result["touches_relinked"].append({"before": ln.strip(), "after": fixed.strip()})
    result["intent_page_before"] = page_before
    result["intent_page_after"] = after
    # 6. what the guard needs
    new_docs = [e["doc"] for items in p.new.values() for e in items]
    moved_to = sorted(p.file_moves.values())
    result["allow"] = [f"product-os/{d}" for d in new_docs + moved_to] + [f"product-os/{page_rel}"]
    result["remove_only"] = [f"product-os/{d}" for d in sorted(p.file_moves)]
    edited = set(p.filled_pages) | set(p.page_edits) | set(result["relinked"])
    result["modify_only"] = sorted(f"product-os/{d}" for d in edited
                                   if d not in set(new_docs) | set(moved_to) | set(p.file_moves)
                                   and d != page_rel)
    return result


def fix_line(line, page_rel, file_moves):
    def repl(m):
        target = m.group(1)
        path, _, anchor = target.partition("#")
        if not path or re.match(r"^[a-z][a-z0-9+.-]*:", path, re.I):
            return m.group(0)
        old = _norm(os.path.join(os.path.dirname(page_rel), path))
        if old not in file_moves:
            return m.group(0)
        link = os.path.relpath(file_moves[old], os.path.dirname(page_rel)).replace(os.sep, "/")
        return "](" + link + (("#" + anchor) if anchor else "") + ")"
    return LINK.sub(repl, line)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Put in the spine the parts the slice needs.")
    ap.add_argument("--root", required=True)
    ap.add_argument("--spine")
    ap.add_argument("--fills")
    ap.add_argument("--intent", required=True)
    ap.add_argument("--out")
    ap.add_argument("--undo", help="a persist-fills.json: take back the intent page lines it changed")
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
        old_text = _read(args.spine)
        spine = yaml.safe_load(old_text) or {}
        if not isinstance(spine, dict):
            raise Refused("the spine must be a YAML mapping")
        old_spine = copy.deepcopy(spine)
        model_names.check_spine(spine, args.spine)
        with open(args.fills, encoding="utf-8") as fh:
            fills = json.load(fh) or {}
        if not isinstance(fills, dict):
            raise Refused("fills.json must hold one JSON object")
        p, page = build(args.root, spine, fills, args.intent)
    except Refused as exc:
        sys.stderr.write(f"persist_fills.py: not written — {exc}\n")
        return finish({"ok": False, "refused": str(exc)}, 2)
    except (OSError, yaml.YAMLError, json.JSONDecodeError) as exc:
        return finish({"ok": False, "refused": f"cannot read an input: {exc}"}, 2)
    return finish(apply(args, spine, old_text, old_spine, p, page), 0)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
