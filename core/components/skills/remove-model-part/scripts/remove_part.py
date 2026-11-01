#!/usr/bin/env python3
"""
remove_part.py — take parts out of the product model, once a person has approved it (remove-model-part).

The model never loses a part by accident: a removal names the person who approved it, and it
goes through only when nothing is left that still names the part. This script does the spine
and the files; it writes no page words. The page skill fixes the words first, and a survivor's
page is the page skill's work too.

    python3 remove_part.py --request <working>/remove-request.json --product-base <product_base> \
        --out <working>/remove-report.json

remove-request.json:
    {"by": "<the play or run that asks>",
     "approved_by": "<the person who approved it>",
     "repoint": [{"id": "cap-2", "kind": "capability", "intents": {"bi-1": "bi-3"}},
                 {"id": "cap-3", "kind": "capability", "intents": {"bi-2": null}}],
     "remove": [{"kind": "intent", "id": "bi-1"},
                {"kind": "capability", "id": "cap-4", "into": "cap-3"},
                {"kind": "slice", "id": "sl-old"}]}

`repoint` and `remove` are each optional, but at least one must hold an item. The work is done on
a copy of the spine, in this order: repoints, capability merges, slice removals, intent removals.
Every check then runs, and only then is the first file changed.

- repoint: kind is domain, capability, feature or slice, and the id must be in the spine under
  it. The part must name each old intent. The new one takes the old one's place in the list,
  order kept, no duplicates; null drops the old one. Each new intent must have a page at
  intents/<id>.md and must not be one this request removes.
- remove an intent: its page intents/<id>.md goes, and it must be there. Refused while any
  domain, capability, feature or slice in the changed spine still names it.
- merge a capability (`into` is required; a capability is never simply removed): `into` must be
  in the spine, must differ from the id and must not be removed in this request.
    Features whose capability is the id move to `into`. Other capabilities or features
    identified by the id are now identified by `into`, or by nothing when that would be itself.
    Every depends_on list that holds the id holds `into` instead, no duplicates, never itself.
    The survivor gains the intents it lacks, in order, and the decisions; its metadata.merged_from
    gains {id, issue, one_line}, so the issue number stays on record. Non-empty nfr_needs or
    compliance_needs are listed in the report under needs_to_review, and never copied.
    Its page goes, and its folder when that is then empty. Refused when the folder holds any
    other file, or when the spine has an `ices` list with an entry for it.
- remove a slice: its entry goes from `slices`, and its record file (`record`, else
  slices/<id>.yaml) when it is there. Nothing under the plans folder is touched.
- mentions: every id being removed must no longer appear as a whole word in any .md or .yaml file
  under the model, other than the files being deleted and _spine.yaml. In the changed spine data
  it may appear only inside metadata.merged_from. Comments in the spine do not count.

Refused too: no approved_by, an unknown kind, the same id removed twice, an id not in the spine,
an id or a page path that leaves the model folder. All or nothing: one bad item refuses the whole
request. When a write or a delete fails part way, every file is put back as it was. The spine is
written through spine_text.dump and safe_write.atomic_write. No git, no network.

remove-report.json: by, approved_by, repointed, removed, merged [{id, into}], moved_features,
needs_to_review, changed and deleted (relative to the product base), layout_kept.

Exit 0 done, 2 refused (stderr says why, naming the part or the line) and nothing written.
"""

import argparse
import copy
import json
import os
import re
import stat
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import model_names  # noqa: E402  (stamped beside this script)
import safe_write  # noqa: E402  (stamped beside this script)
import spine_text  # noqa: E402  (stamped beside this script)

KINDS = {"domain": "domains", "capability": "capabilities", "feature": "features", "slice": "slices"}
SINGULAR = {key: kind for kind, key in KINDS.items()}
REMOVABLE = ("intent", "capability", "slice")
INTENT_ID = re.compile(r"[a-z0-9][a-z0-9-]*")
MODEL = "product-os"


class Refused(Exception):
    pass


class NotPutBack(Exception):
    """A write or delete failed, and some files could not be put back either."""


def inside(root, rel):
    if not isinstance(rel, str) or not rel or os.path.isabs(rel) or ".." in rel.split("/"):
        raise Refused(f"the path {rel!r} leaves the model folder")
    full = os.path.realpath(os.path.join(root, rel))
    if not full.startswith(os.path.realpath(root) + os.sep):
        raise Refused(f"the path {rel!r} leaves the model folder")
    return full


def entries(spine, key):
    value = spine.get(key)
    return [e for e in value if isinstance(e, dict)] if isinstance(value, list) else []


def entry_of(spine, kind, pid):
    return next((e for e in entries(spine, KINDS[kind]) if e.get("id") == pid), None)


def no_repeats(values):
    out = []
    for value in values:
        if value not in out:
            out.append(value)
    return out


def word_of(pid):
    """A part's id as a whole word: a longer id that starts or ends with it does not match."""
    return re.compile(r"(?<![\w-])" + re.escape(pid) + r"(?![\w-])")


def items_of(request, name):
    items = request.get(name)
    if items is None:
        return []
    if not isinstance(items, list) or not all(isinstance(i, dict) for i in items):
        raise Refused(f"`{name}` must be a list of objects")
    return items


def check_request(request):
    """The repoints, the removals and the set of ids being removed."""
    if not isinstance(request, dict):
        raise Refused("the request is not a JSON object")
    who = request.get("approved_by")
    if not isinstance(who, str) or not who.strip():
        raise Refused("the request names no person who approved it (approved_by); nothing is removed without one")
    repoint, remove = items_of(request, "repoint"), items_of(request, "remove")
    if not repoint and not remove:
        raise Refused("the request holds nothing to repoint and nothing to remove")
    removing = set()
    for item in remove:
        kind, pid = item.get("kind"), item.get("id")
        if kind not in REMOVABLE:
            raise Refused(f"{pid!r}: the kind {kind!r} is unknown here; only an intent, a capability or a slice is removed")
        if not isinstance(pid, str) or not pid:
            raise Refused(f"each item to remove needs an id: {item!r}")
        if pid in removing:
            raise Refused(f"{pid} is removed twice in this request")
        if "into" in item and kind != "capability":
            raise Refused(f"{pid}: only a capability merges into another; a {kind} has no `into`")
        removing.add(pid)
    return repoint, remove, removing


def check_new_intent(root, pid, new, removing):
    if not isinstance(new, str) or not INTENT_ID.fullmatch(new):
        raise Refused(f"{pid}: {new!r} is not a business intent id, or it leaves the model folder")
    if new in removing:
        raise Refused(f"{pid}: the new business intent {new} is one this request removes")
    if not os.path.isfile(inside(root, f"intents/{new}.md")):
        raise Refused(f"{pid}: the new business intent {new} has no page at intents/{new}.md")


def repoint_part(root, spine, item, removing):
    pid, kind, pairs = item.get("id"), item.get("kind"), item.get("intents")
    if not isinstance(kind, str) or kind not in KINDS:
        raise Refused(f"{pid!r}: the kind {kind!r} is unknown; a part to repoint is a domain, a capability, "
                      "a feature or a slice")
    entry = entry_of(spine, kind, pid)
    if entry is None:
        raise Refused(f"{pid} is not in the spine as a {kind}")
    if not isinstance(pairs, dict) or not pairs:
        raise Refused(f"{pid}: `intents` must map each old business intent to its new one, or to null")
    named = entry.get("intents") or []
    for old, new in pairs.items():
        if old not in named:
            raise Refused(f"{pid} does not name the business intent {old}")
        if new is not None:
            check_new_intent(root, pid, new, removing)
    entry["intents"] = no_repeats(pairs.get(i, i) for i in named if pairs.get(i, i) is not None)


def pointed_at(value, pid, into, own):
    """`value` (one id, or a list of ids) naming `into` where it named `pid`, never `own`."""
    if value == pid:
        return "" if into == own else into
    if isinstance(value, list) and pid in value:
        return [v for v in no_repeats(into if v == pid else v for v in value) if v != own]
    return value


def page_and_folders(root, pid, doc, change):
    """Mark the capability's page and folder to go; refuse when its folder holds any other file."""
    if not doc:
        return
    page = inside(root, doc)
    folder = os.path.dirname(page)
    others, folders = [], []
    for here, dirs, files in os.walk(folder, topdown=False):
        names = [os.path.join(here, n) for n in files] + \
                [os.path.join(here, n) for n in dirs if os.path.islink(os.path.join(here, n))]
        others += [p for p in names if p != page]
        folders.append(here)
    if others:
        names = ", ".join(sorted(os.path.relpath(p, root) for p in others))
        raise Refused(f"{pid}: its folder holds other files, so it cannot go: {names}")
    if os.path.isfile(page):
        change["deletes"].append(page)
    change["folders"] += folders


def merge_capability(root, spine, item, removing, change):
    pid, into = item["id"], item.get("into")
    entry = entry_of(spine, "capability", pid)
    if entry is None:
        raise Refused(f"{pid} is not in the spine as a capability")
    if not isinstance(into, str) or not into:
        raise Refused(f"{pid}: a capability is only removed by merging it into another; name that one in `into`")
    if into == pid:
        raise Refused(f"{pid} cannot be merged into itself")
    if into in removing:
        raise Refused(f"{pid}: {into}, the capability it merges into, is removed in this request too")
    survivor = entry_of(spine, "capability", into)
    if survivor is None:
        raise Refused(f"{pid}: {into}, the capability it merges into, is not in the spine")
    if any(i.get("for") == pid for i in entries(spine, "ices")):
        raise Refused(f"{pid} has its own entry in the spine's `ices` list, so it cannot be merged here")
    page_and_folders(root, pid, entry.get("doc"), change)

    spine["capabilities"] = [c for c in spine["capabilities"] if c is not entry]
    for feature in entries(spine, "features"):
        if feature.get("capability") == pid:
            feature["capability"] = into
            change["moved_features"].append(feature.get("id"))
    for part in entries(spine, "capabilities") + entries(spine, "features"):
        if "identified_by" in part:
            part["identified_by"] = pointed_at(part["identified_by"], pid, into, part.get("id"))
    for key in spine:
        for part in entries(spine, key):
            if isinstance(part.get("depends_on"), list):
                part["depends_on"] = pointed_at(part["depends_on"], pid, into, part.get("id"))

    survivor["intents"] = no_repeats((survivor.get("intents") or []) + (entry.get("intents") or []))
    if entry.get("decisions"):
        survivor["decisions"] = no_repeats((survivor.get("decisions") or []) + entry["decisions"])
    if not isinstance(survivor.get("metadata"), dict):
        survivor["metadata"] = {}
    survivor["metadata"].setdefault("merged_from", []).append(
        {"id": pid, "issue": entry.get("issue"), "one_line": entry.get("one_line")})
    needs = {k: entry[k] for k in ("nfr_needs", "compliance_needs") if entry.get(k)}
    if needs:
        change["needs_to_review"].append(dict({"id": pid}, **needs))
    change["merged"].append({"id": pid, "into": into})


def remove_slice(root, spine, item, change):
    pid = item["id"]
    entry = entry_of(spine, "slice", pid)
    if entry is None:
        raise Refused(f"{pid} is not in the spine as a slice")
    record = inside(root, entry.get("record") or f"slices/{pid}.yaml")
    if os.path.isfile(record):
        change["deletes"].append(record)
    spine["slices"] = [s for s in spine["slices"] if s is not entry]


def remove_intent(root, spine, item, change):
    pid = item["id"]
    if not INTENT_ID.fullmatch(pid):
        raise Refused(f"{pid!r} is not a business intent id, or it leaves the model folder")
    page = inside(root, f"intents/{pid}.md")
    if not os.path.isfile(page):
        raise Refused(f"the business intent {pid} has no page at intents/{pid}.md")
    named_by = [f"{kind} {e.get('id')}" for kind, key in KINDS.items() for e in entries(spine, key)
                if pid in (e.get("intents") or [])]
    if named_by:
        raise Refused(f"the business intent {pid} is still named by {', '.join(named_by)}; repoint them first")
    change["deletes"].append(page)


def places(value, path, word):
    """Each place under `value` that holds the word, skipping metadata.merged_from."""
    if isinstance(value, dict):
        for key, inner in value.items():
            here = f"{path}.{key}" if path else str(key)
            if key == "merged_from" and path.split(".")[-1] == "metadata":
                continue
            if word.search(str(key)):
                yield here
            yield from places(inner, here, word)
    elif isinstance(value, list):
        for inner in value:
            yield from places(inner, path, word)
    elif isinstance(value, str) and word.search(value):
        yield path


def left_in_spine(spine, pid):
    """Where the changed spine data still names the id, each named by its part."""
    word = word_of(pid)
    out = []
    for key, value in spine.items():
        if isinstance(value, list):
            for item in value:
                has_id = isinstance(item, dict) and item.get("id")
                label = f"{SINGULAR.get(key, key)} {item['id']}" if has_id else key
                out += [f"{label} ({field})" if field else label for field in places(item, "", word)]
        else:
            out += list(places(value, key, word))
    return no_repeats(out)


def left_in_files(root, ids, deleting):
    """Each path:line under the model that still names an id being removed."""
    skip = set(deleting) | {os.path.join(root, "_spine.yaml")}
    words = [(pid, word_of(pid)) for pid in sorted(ids)]
    out = []
    for here, dirs, files in os.walk(root):
        dirs.sort()
        for name in sorted(files):
            path = os.path.join(here, name)
            if not name.endswith((".md", ".yaml")) or path in skip:
                continue
            with open(path, encoding="utf-8", errors="replace") as fh:
                for number, line in enumerate(fh, 1):
                    out += [f"{os.path.relpath(path, root)}:{number} names {pid}"
                            for pid, word in words if word.search(line)]
    return out


def plan(root, spine, request):
    """The changed spine and what changes: every check runs here, before any file is touched."""
    repoint, remove, removing = check_request(request)
    new_spine = copy.deepcopy(spine)
    change = {"moved_features": [], "merged": [], "needs_to_review": [], "deletes": [], "folders": []}
    for item in repoint:
        repoint_part(root, new_spine, item, removing)
    for item in remove:
        if item["kind"] == "capability":
            merge_capability(root, new_spine, item, removing, change)
    for item in remove:
        if item["kind"] == "slice":
            remove_slice(root, new_spine, item, change)
    for item in remove:
        if item["kind"] == "intent":
            remove_intent(root, new_spine, item, change)
    left = [f"{pid} in {place}" for pid in sorted(removing) for place in left_in_spine(new_spine, pid)]
    if left:
        raise Refused("the spine still names a part being removed: " + "; ".join(left))
    lines = left_in_files(root, removing, change["deletes"])
    if lines:
        raise Refused("pages still name a part being removed; have the page skill fix these words first: "
                      + "; ".join(lines))
    change["repointed"] = no_repeats(item["id"] for item in repoint)
    change["removed"] = [item["id"] for item in remove]
    return new_spine, change


def cut_gone_items(old_text, old, new):
    """The text and data of the old spine without the items the new one dropped.

    spine_text.dump rewrites a whole list when it got shorter, and the comments inside it go with
    it. With the dropped items cut first, dump sees lists of the same length and changes only the
    items that changed. When the layout does not allow a clean cut, dump gets the spine as it was."""
    lines = old_text.splitlines()
    blocks = spine_text._blocks(lines)
    cut = copy.deepcopy(old)
    order = sorted((k for k in old if k in blocks), key=lambda k: blocks[k][0], reverse=True)
    for key in order:
        was, now = old[key], new.get(key)
        if not (isinstance(was, list) and isinstance(now, list) and now and len(now) < len(was)):
            continue
        found = spine_text._items(lines, *blocks[key])
        if found is None or len(found[1]) != len(was):
            return old_text, old
        kept_ids = {e.get("id") for e in now if isinstance(e, dict)}
        for (first, stop), item in reversed(list(zip(found[1], was))):
            if isinstance(item, dict) and item.get("id") not in kept_ids:
                del lines[first:stop]
        cut[key] = [e for e in was if not isinstance(e, dict) or e.get("id") in kept_ids]
    text = "\n".join(lines) + "\n"
    try:
        same = yaml.safe_load(text) == cut
    except yaml.YAMLError:
        same = False
    return (text, cut) if same else (old_text, old)


def mode_of(path):
    return stat.S_IMODE(os.stat(path).st_mode)


def put_back(undo, spine_path, old_text):
    """Undo each step that was done, last first. Returns the paths it could not put back."""
    stuck, folder_modes = [], []
    for step, path, data, mode in reversed(undo):
        try:
            if step == "spine":
                safe_write.atomic_write(spine_path, old_text)
            elif step == "folder":
                os.makedirs(path, exist_ok=True)
                folder_modes.append((path, mode))
            else:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "wb") as fh:
                    fh.write(data)
                os.chmod(path, mode)
        except OSError:
            stuck.append(path)
    for path, mode in reversed(folder_modes):
        try:
            os.chmod(path, mode)
        except OSError:
            stuck.append(path)
    return stuck


def apply(spine_path, old_text, new_text, deletes, folders, out, report_text):
    """Write the spine, delete the files and folders, write the report: all of it, or none of it."""
    files = []
    for path in deletes:
        with open(path, "rb") as fh:
            files.append((path, fh.read(), mode_of(path)))
    folder_modes = [(path, mode_of(path)) for path in folders]
    undo = []
    try:
        if new_text is not None:
            safe_write.atomic_write(spine_path, new_text)
            undo.append(("spine", spine_path, None, None))
        for path, data, mode in files:
            os.remove(path)
            undo.append(("file", path, data, mode))
        for path, mode in folder_modes:
            os.rmdir(path)
            undo.append(("folder", path, None, mode))
        safe_write.atomic_write(out, report_text)
    except OSError as err:
        stuck = put_back(undo, spine_path, old_text)
        if stuck:
            raise NotPutBack(f"{err}; these could not be put back: {', '.join(stuck)}") from err
        raise


def main():
    ap = argparse.ArgumentParser(description="Take parts out of the product model, on a person's approval.")
    ap.add_argument("--request", required=True)
    ap.add_argument("--product-base", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    root = os.path.realpath(os.path.join(a.product_base, MODEL))
    spine_path = os.path.join(root, "_spine.yaml")
    try:
        with open(a.request, encoding="utf-8") as fh:
            request = json.load(fh)
        with open(spine_path, encoding="utf-8", newline="") as fh:
            old_text = fh.read()
        spine = yaml.safe_load(old_text) or {}
        if not isinstance(spine, dict):
            raise Refused("the spine is not a mapping")
        model_names.check_spine(spine, spine_path)
        new_spine, change = plan(root, spine, request)
        model_names.check_spine(new_spine, spine_path)
    except (Refused, OSError, ValueError, yaml.YAMLError) as err:
        sys.stderr.write(f"remove_part.py: refused, nothing written: {err}\n")
        return 2

    new_text, kept = None, True
    if new_spine != spine:
        cut_text, cut_spine = cut_gone_items(old_text, spine, new_spine)
        new_text, kept = spine_text.dump(cut_text, cut_spine, new_spine)

    def from_base(path):
        return os.path.join(MODEL, os.path.relpath(path, root))

    report = {
        "by": request.get("by") or "a play",
        "approved_by": request["approved_by"],
        "repointed": change["repointed"],
        "removed": change["removed"],
        "merged": change["merged"],
        "moved_features": change["moved_features"],
        "needs_to_review": change["needs_to_review"],
        "changed": [from_base(spine_path)] if new_text is not None else [],
        "deleted": [from_base(p) for p in change["deletes"] + change["folders"]],
        "layout_kept": kept,
    }
    try:
        apply(spine_path, old_text, new_text, change["deletes"], change["folders"], a.out,
              json.dumps(report, indent=2) + "\n")
    except NotPutBack as err:
        sys.stderr.write(f"remove_part.py: a write or delete failed: {err}\n")
        return 2
    except OSError as err:
        sys.stderr.write(f"remove_part.py: a write or delete failed, every file is back as it was: {err}\n")
        return 2
    print(json.dumps(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
