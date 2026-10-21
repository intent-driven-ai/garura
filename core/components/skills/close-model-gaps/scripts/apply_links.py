#!/usr/bin/env python3
"""apply_links.py — close the gaps the model itself can close (close-model-gaps, ADR 043).

Reads `gaps.json` (find-model-gaps' agreed result) and applies, in this order, what needs no
new content:

1. **Merge agreed duplicates** (`duplicates[]` with `agreed: true`): keep one entry, move the
   other's `intents` onto it, point its children at it, remove its spine entry and its page,
   and point every intent page's link to its page at the kept page.
2. **Attribute** (`links_to_make[]` with `field: domain | capability`): set a capability's
   `domain` or a functionality's `capability`. A node whose page is in a holding folder
   (`capabilities/<id>/`, `functionalities/<id>/`) moves — its whole folder, byte for byte —
   under its parent's folder; the spine `doc` of it and of everything inside follows, and the
   links to it on intent pages follow.
3. **Link to intents** (`links_to_make[]` with `field: intents`): add the intent ids to the
   node's spine `intents`, and the node to each intent page's Touches list (both sides).

It never writes an intent's content, never writes a new capability or functionality page,
and deletes nothing but a merged duplicate. It writes only inside `<product_base>product-os/`:
every path is checked before it is written, moved or removed, and a link that would reach
outside is skipped, not applied. The report lists every file it changed (`changed`). What needs a play — the `work[]` list — is copied
to the report for the drive.

    python3 apply_links.py --gaps <working>/gaps.json --product-base <product_base> \
        --out <working>/close-report.json

Exit 0 written (with or without skips); 2 an input cannot be read. Standard library + PyYAML.
"""
import argparse
import json
import os
import shutil
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import intent_touches as it  # noqa: E402

SECTIONS = {"domain": "domains", "capability": "capabilities", "functionality": "functionalities"}
HOLDING = {"capability": "capabilities", "functionality": "functionalities"}


class OutOfScope(ValueError):
    """A write that would land outside the product model."""


class Model:
    def __init__(self, base):
        self.root = os.path.join(base, "product-os")
        self.changed = set()
        self.spine_path = os.path.join(self.root, "_spine.yaml")
        with open(self.spine_path, encoding="utf-8") as fh:
            self.spine = yaml.safe_load(fh) or {}
        self.intents_dir = os.path.join(self.root, "intents")

    def guard(self, path):
        """The path, once it is known to sit inside the product model; recorded as changed."""
        root = os.path.realpath(self.root)
        real = os.path.realpath(path)
        if real != root and not real.startswith(root + os.sep):
            raise OutOfScope(f"{os.path.relpath(path, self.root)} is outside the product model")
        self.changed.add(os.path.relpath(real, root).replace(os.sep, "/"))
        return path

    def entries(self, kind):
        return [e for e in self.spine.get(SECTIONS[kind]) or [] if isinstance(e, dict)]

    def get(self, kind, nid):
        return next((e for e in self.entries(kind) if e.get("id") == nid), None)

    def intent_pages(self):
        if not os.path.isdir(self.intents_dir):
            return []
        return [os.path.join(self.intents_dir, n) for n in sorted(os.listdir(self.intents_dir)) if n.endswith(".md")]

    def relink_intents(self, old_doc, new_doc):
        for page in self.intent_pages():
            with open(page, encoding="utf-8") as fh:
                text = fh.read()
            old = it.rel(page, os.path.join(self.root, old_doc))
            new = it.rel(page, os.path.join(self.root, new_doc))
            text2, n = it.relink(text, old, new)
            if n:
                entries, seen = [], set()
                for e in it.read(text2):
                    if e["link"] not in seen:
                        seen.add(e["link"])
                        entries.append(e)
                lines = text2.splitlines()
                found = it._block(lines)
                if found:
                    lines[found[0]:found[1]] = it.render(entries)
                    text2 = "\n".join(lines) + "\n"
                with open(self.guard(page), "w", encoding="utf-8") as fh:
                    fh.write(text2)

    def save(self):
        with open(self.guard(self.spine_path), "w", encoding="utf-8") as fh:
            yaml.safe_dump(self.spine, fh, sort_keys=False, allow_unicode=True)


def in_holding(kind, doc):
    return str(doc or "").startswith(HOLDING.get(kind, "\0") + "/")


def move_dirs(m, entry, parent_doc):
    """(old folder, new folder) of a holding-folder node, both checked to sit in the model."""
    old_dir = os.path.dirname(entry["doc"])
    new_dir = os.path.join(os.path.dirname(parent_doc), entry.get("slug") or entry["id"])
    m.guard(os.path.join(m.root, old_dir))
    m.guard(os.path.join(m.root, new_dir))
    return old_dir, new_dir


def move_under(m, kind, entry, parent_doc, report):
    """Move a holding-folder node's folder under its parent's folder; repoint docs and links."""
    old_dir, new_dir = move_dirs(m, entry, parent_doc)
    if os.path.exists(os.path.join(m.root, new_dir)):
        report["skipped"].append({"id": entry["id"], "why": f"{new_dir} already exists; the page was not moved"})
        return
    os.makedirs(os.path.dirname(os.path.join(m.root, new_dir)), exist_ok=True)
    shutil.move(os.path.join(m.root, old_dir), os.path.join(m.root, new_dir))
    for k in ("capability", "functionality"):
        for e in m.entries(k):
            doc = str(e.get("doc") or "")
            if doc == old_dir or doc.startswith(old_dir + "/"):
                new_doc = new_dir + doc[len(old_dir):]
                m.relink_intents(doc, new_doc)
                e["doc"] = new_doc
    report["applied"].append({"move": entry["id"], "from": old_dir, "to": new_dir})


def merge(m, d, report):
    kind, keep_id, drop_id = d.get("kind"), d.get("keep"), d.get("drop")
    keep, drop = (m.get(kind, keep_id), m.get(kind, drop_id)) if kind in SECTIONS else (None, None)
    if not keep or not drop or keep_id == drop_id:
        report["skipped"].append({"duplicate": [keep_id, drop_id], "why": "not two known nodes of one kind"})
        return
    for doc in (drop.get("doc"), keep.get("doc")):
        if doc:
            m.guard(os.path.join(m.root, doc))
    keep["intents"] = sorted(set(keep.get("intents") or []) | set(drop.get("intents") or []))
    child = {"domain": ("capability", "domain"), "capability": ("functionality", "capability")}.get(kind)
    if child:
        for e in m.entries(child[0]):
            if e.get(child[1]) == drop_id:
                e[child[1]] = keep_id
    if drop.get("doc") and keep.get("doc"):
        m.relink_intents(drop["doc"], keep["doc"])
        page = m.guard(os.path.join(m.root, drop["doc"]))
        if os.path.isfile(page):
            os.remove(page)
            folder = os.path.dirname(page)
            if os.path.isdir(folder) and not os.listdir(folder):
                os.rmdir(folder)
    m.spine[SECTIONS[kind]] = [e for e in m.entries(kind) if e.get("id") != drop_id]
    report["applied"].append({"merged": drop_id, "into": keep_id, "kind": kind})


def attribute(m, link, report):
    kind, nid, field, value = link.get("kind"), link.get("id"), link.get("field"), link.get("value")
    parent_kind = {"capability": "domain", "functionality": "capability"}.get(kind)
    entry = m.get(kind, nid) if kind in SECTIONS else None
    if not entry or field != parent_kind:
        report["skipped"].append({"id": nid, "why": f"cannot set `{field}` on a {kind or 'unknown node'}"})
        return
    parent = m.get(parent_kind, value)
    if not parent:
        report["skipped"].append({"id": nid, "why": f"{parent_kind} `{value}` is not in the spine"})
        return
    if entry.get(field) and entry.get(field) != value:
        report["skipped"].append({"id": nid, "why": f"already under `{entry[field]}`; moving it is alignment work"})
        return
    moves = in_holding(kind, entry.get("doc")) and parent.get("doc") and not in_holding(parent_kind, parent.get("doc"))
    if moves:
        move_dirs(m, entry, parent["doc"])
    entry[field] = value
    report["applied"].append({"attributed": nid, field: value})
    if moves:
        move_under(m, kind, entry, parent["doc"], report)


def link_intents(m, link, report):
    kind, nid = link.get("kind"), link.get("id")
    entry = m.get(kind, nid) if kind in SECTIONS else None
    ids = link.get("value") if isinstance(link.get("value"), list) else [link.get("value")]
    if not entry:
        report["skipped"].append({"id": nid, "why": "not in the spine"})
        return
    for iid in [str(i) for i in ids if i]:
        page = os.path.join(m.intents_dir, f"{iid}.md")
        if not os.path.isfile(page):
            report["skipped"].append({"id": nid, "intent": iid, "why": "no intent page"})
            continue
        m.guard(page)
        entry["intents"] = sorted(set(entry.get("intents") or []) | {iid})
        if entry.get("doc"):
            with open(os.path.join(m.root, entry["doc"]), encoding="utf-8", errors="ignore") as fh:
                first = fh.readline()
            title = first.split(":", 1)[1].strip() if ":" in first else nid
            with open(page, encoding="utf-8") as fh:
                text = fh.read()
            text = it.upsert(text, [it.entry(title, it.rel(page, os.path.join(m.root, entry["doc"])), kind,
                                             link.get("mark") or "adds")])
            with open(m.guard(page), "w", encoding="utf-8") as fh:
                fh.write(text)
        report["applied"].append({"linked": nid, "intent": iid})


def apply(gaps, base):
    m = Model(base)
    report = {"applied": [], "skipped": [], "work_for_plays": list(gaps.get("work") or [])}
    def guarded(fn, item):
        try:
            fn(m, item, report)
        except OutOfScope as exc:
            report["skipped"].append({"id": item.get("id") or item.get("drop"), "why": str(exc)})

    for d in gaps.get("duplicates") or []:
        if d.get("agreed"):
            guarded(merge, d)
    links = gaps.get("links_to_make") or []
    order = {"domain": 0, "capability": 1}
    for link in sorted([l for l in links if l.get("field") in order], key=lambda l: order[l["field"]]):
        guarded(attribute, link)
    for link in links:
        if link.get("field") == "intents":
            guarded(link_intents, link)
        elif link.get("field") not in order:
            report["skipped"].append({"id": link.get("id"), "why": f"unknown field `{link.get('field')}`"})
    m.save()
    report["changed"] = sorted(m.changed)
    return report


def main(argv=None):
    ap = argparse.ArgumentParser(description="Close the gaps the model itself can close.")
    ap.add_argument("--gaps", required=True)
    ap.add_argument("--product-base", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        with open(args.gaps, encoding="utf-8") as fh:
            gaps = json.load(fh)
        report = apply(gaps, args.product_base)
    except (OSError, ValueError, yaml.YAMLError, it.Bad) as exc:
        sys.stderr.write(f"apply_links.py: {exc}\n")
        return 2
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print(json.dumps({k: len(v) for k, v in report.items()}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
