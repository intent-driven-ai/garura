#!/usr/bin/env python3
"""plan_session.py — the parts the /update-plan scripts share (#730).

Not run on its own. The scripts beside it import it for:

  - the plan's rules: the item kinds a plan may hold, the parent each kind may sit under, the
    tracker type of each kind, the item statuses and plan statuses (from the plan-view template);
  - reading a plan file and walking its tree (`load_plan`, `walk`, `find`, `parent_of`,
    `descendants`);
  - the two templates' settings blocks (`load_block`);
  - safe writes (`write_json`, `write_text`: a temp file, then a move) and `sha256_of`;
  - the session's list (`load_list`, `save_list`), kept in changes.yaml.
No git, no network, no judgment.
"""

import hashlib
import json
import os
import re

import yaml

# The item kinds a plan may hold (#917), and where each may sit. None is the plan itself.
KINDS = ("epic", "feature", "story", "spike", "chore", "bug")
PARENTS = {
    "epic": (None,),
    "feature": ("epic",),
    "story": ("epic", "feature"),
    "spike": ("story",),
    "chore": ("story",),
    "bug": ("story",),
}
TYPES = {"epic": "Epic", "feature": "Feature", "story": "Story", "spike": "Spike",
         "chore": "Chore", "bug": "Bug"}
CLOSED = {"Done": "completed", "Dropped": "not planned"}
REASON_OF = {"completed": "COMPLETED", "not planned": "NOT_PLANNED"}
# The tracker reasons each close reason covers: a duplicate is closed as not planned (#1007).
COVERS = {"completed": ("COMPLETED", None), "not planned": ("NOT_PLANNED", "DUPLICATE")}


def closed_as(now, reason):
    """True when the tracker already holds the issue closed for `reason` ("completed" or "not planned")."""
    return bool(now) and now.get("state") == "CLOSED" and now.get("state_reason") in COVERS[reason]


class Refused(Exception):
    pass


def load_block(path, name):
    """The settings block that opens with ```yaml <name> in a template."""
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError as e:
        raise Refused(f"cannot read the template {path}: {e.strerror}")
    m = re.search(rf"^```yaml {re.escape(name)}\s*\n(.*?)^```", text, re.S | re.M)
    if not m:
        raise Refused(f"{path} has no ```yaml {name} block")
    return yaml.safe_load(m.group(1)) or {}


def statuses(view):
    """(item statuses in order, {name: mark}, plan statuses, directions) from plan-view."""
    items = [s["name"] for s in view["statuses"]]
    marks = {s["name"]: s["mark"] for s in view["statuses"]}
    return items, marks, list(view["list"]["plan_statuses"]), dict(view["list"]["directions"])


def read_text(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return fh.read()


def load_plan(path):
    try:
        data = yaml.safe_load(read_text(path)) or {}
    except (OSError, yaml.YAMLError) as e:
        raise Refused(f"cannot read the plan file {path}: {e}")
    if not isinstance(data, dict) or "tree" not in data:
        raise Refused(f"{path} is not a plan file (no tree)")
    return data


def walk(nodes, parent=None):
    """Each node with its parent node (None at the top)."""
    for n in nodes or []:
        yield n, parent
        yield from walk(n.get("children"), n)


def find(plan, issue):
    for n, p in walk(plan.get("tree")):
        if str(n.get("issue")) == str(issue):
            return n, p
    return None, None


def descendants(node):
    return [n for n, _ in walk(node.get("children"))]


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


def write_text(path, text):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    os.replace(tmp, path)


def write_json(path, data):
    write_text(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def read_json(path, what):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError) as e:
        raise Refused(f"cannot read {what} ({path}): {e}")


def model_records(paths):
    """The model records of one landing read as one (HF-12): Step 8 writes model-record.json and
    Step 9's story naming writes its own record, so neither replaces the other. Parts are joined
    by feature (a later record's fields win), files are joined with no repeat. A path that is
    given but not on disk is refused: a missing record is never read as an empty one."""
    parts, files = {}, []
    for path in paths or []:
        rec = read_json(path, "the model record")
        if not isinstance(rec, dict) or not isinstance(rec.get("parts") or [], list) \
                or not isinstance(rec.get("files") or [], list):
            raise Refused(f"{path} is not a model record ({{parts: [...], files: [...]}})")
        for p in rec.get("parts") or []:
            if not isinstance(p, dict):
                raise Refused(f"{path}: a part is not an object")
            parts.setdefault(p.get("feature"), {}).update(p)
        for f in rec.get("files") or []:
            if not isinstance(f, str):
                raise Refused(f"{path}: a file is not a path")
            if f and f not in files:
                files.append(f)
    return {"parts": list(parts.values()), "files": files}


def load_list(path):
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def save_list(path, data):
    write_text(path, yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=10 ** 9))


def owed_of(changes):
    """What the landing leaves owed, for each new feature: its slice or its hidden-file entry
    (/shape-slice), and its eval scenarios (/shape-eval). The play never writes the evals folder."""
    owed = []
    for e in changes.get("entries") or []:
        if e.get("op") != "new-feature":
            continue
        title = e.get("title")
        if e.get("slice"):
            owed.append(f"the hidden-file entry for '{title}' (/shape-slice)")
        else:
            owed.append(f"a slice for '{title}' (/shape-slice)")
        owed.append(f"eval scenarios for '{title}' (/shape-eval)")
    return owed
