#!/usr/bin/env python3
"""plan_common.py — the parts the /shape-plan scripts share.

Not run on its own. The scripts beside it import it for four jobs:

  - Safe writes. `atomic_write` and `write_json` write through a temp file in the same folder,
    then move it into place with os.replace. A run that stops half way never leaves half a
    file.
  - The ICE text of a part. `ice_lines` reads the ICE of a feature or a capability: the inline
    `## Agent intent (ICE)` section of the part's page, or, when the spine has an `ices` list,
    the `## Intent`, `## Context` and `## Expectation` sections of the part's ice.md.
    `fails_if_texts` lists every line of each "Fails if" block (the line itself and every line
    under it: nested bullets, wrapped text) and `without_fails_if` takes each block out.
  - The words that must never reach an epic, a story or a plan file: "Fails if" and the two
    recovery phrases (`forbidden_in`).
  - The tracker. `open_tracker` gives a file tracker (`--tracker-file <json>`, for tests and
    dry runs) or the code host, reached only through platform_adapter.py. Both have the same
    methods: get, create (title, body, type and parent in one write), set_type, set_body,
    remove_labels, add_sub, remove_sub, save.
  - The hash of a file (`sha256_of`), so a yes stays tied to the files the person saw.

The file tracker is a JSON file {"issues": [{"number", "title", "type", "labels": [],
"state", "body", "sub_issues": [numbers]}]}. A new issue takes the next free number. Like a
real tracker, it keeps each write at once: the file is written after every write. A test can
make one write fail: `"fail_at_write": <n>` in the file makes the n-th write of the run fail,
with nothing changed by it.

The code host is reached through the adapter's verbs only: view-issue, create-issue-typed,
set-issue-type, edit-issue-body, remove-label, attach-sub-issue and remove-sub-issue. No
judgment is made here.
"""

import hashlib

import json
import os
import re
import tempfile

try:
    import yaml
except ImportError:  # the scripts say so in plain words
    yaml = None

HERE = os.path.dirname(os.path.abspath(__file__))
RECOVERY_PHRASES = ("the builder can fix this alone", "a person must decide")
EPIC_TYPE, STORY_TYPE = "Feature", "Story"


class Refused(Exception):
    """A refusal or bad input: the script writes nothing and exits 2."""


class TrackerError(Exception):
    """The tracker did not do what it was asked."""


# ---- files ------------------------------------------------------------------------------

def atomic_write(path, text):
    """Write `text` to `path` through a temp file in the same folder, then os.replace it."""
    folder = os.path.dirname(os.path.abspath(path))
    os.makedirs(folder, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".shape-plan-", suffix=".tmp", dir=folder)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def sha256_of(path):
    """The sha256 of a file's bytes, or None when it cannot be read."""
    try:
        with open(path, "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return None


def write_json(path, obj):
    atomic_write(path, json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def read_text(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def read_json(path, what):
    try:
        return json.loads(read_text(path))
    except (OSError, json.JSONDecodeError) as exc:
        raise Refused(f"cannot read {what} at {path}: {exc}")


def read_yaml(path, what):
    if yaml is None:
        raise Refused("PyYAML is needed (pip install pyyaml)")
    try:
        return yaml.safe_load(read_text(path))
    except (OSError, yaml.YAMLError) as exc:
        raise Refused(f"cannot read {what} at {path}: {exc}")


# ---- text -------------------------------------------------------------------------------

def norm(text):
    """Text for matching: case, spacing and a closing full stop do not count."""
    return " ".join(str(text).split()).rstrip(".").lower()


def forbidden_in(text, fails_lines=()):
    """What in `text` must never reach an epic, a story or a plan file, as plain reasons."""
    found = []
    low = norm(text)
    if "fails if" in low:
        found.append('it holds the words "Fails if"')
    for phrase in RECOVERY_PHRASES:
        if phrase in low:
            found.append(f'it holds the recovery phrase "{phrase}"')
    for line in fails_lines:
        n = norm(line)
        if len(n.split()) >= 2 and n in low:
            found.append(f'it holds a failure line of its ICE: "{line}"')
    return found


def all_text(value):
    """Every string inside a JSON value, joined, so one check reads all of it."""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return "\n".join(all_text(v) for v in value.values())
    if isinstance(value, list):
        return "\n".join(all_text(v) for v in value)
    return ""


# ---- the ICE of a part ------------------------------------------------------------------

FAILS_BULLET = re.compile(r"^(?P<lead>\s*)[-*]\s+(?:\*\*)?Fails if:?(?:\*\*)?:?\s*(?P<text>.*?)\s*$",
                          re.IGNORECASE)
NEW_ITEM = re.compile(r"^\s*(?:[-*+]\s|\d+[.)]\s|#|\*\*|>|```)")
FAILS_HEAD = re.compile(r"^\s*(?:#+\s*|\*\*)Fails if\b", re.IGNORECASE)
HEADING = re.compile(r"^(#+)\s")
ICE_PARTS = ("## Intent", "## Context", "## Expectation")


def entry(spine, key, eid):
    return next((e for e in spine.get(key) or [] if isinstance(e, dict) and e.get("id") == eid), None)


def _section(lines, heading):
    at = next((i for i, ln in enumerate(lines) if ln.strip() == heading), None)
    if at is None:
        return None
    end = next((i for i in range(at + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return lines[at + 1:end]


def ice_page(spine, part):
    """The page (relative to the model folder) that holds the part's ICE, or None."""
    if part is None:
        return None
    if "ices" in spine:
        ice = next((i for i in spine.get("ices") or [] if isinstance(i, dict)
                    and i.get("for") == part.get("id")), None)
        return ice.get("doc") if ice else None
    return part.get("doc")


def ice_lines(root, spine, part):
    """The lines of the part's ICE (a list, maybe empty), or None when its page is missing."""
    rel = ice_page(spine, part)
    if not rel:
        return None
    path = os.path.join(root, rel)
    if not os.path.isfile(path):
        return None
    lines = read_text(path).splitlines()
    if "ices" in spine:
        out = []
        for head in ICE_PARTS:
            body = _section(lines, head)
            if body is not None:
                out.append(head)
                out.extend(body)
        return out
    body = _section(lines, "## Agent intent (ICE)")
    return body if body is not None else []


def _split(lines):
    """(kept lines, blocks): each block is the lines of one "Fails if" line, label or heading,
    with every line under it — deeper lines, nested bullets, wrapped text."""
    kept, blocks, cur = [], [], None
    for ln in lines or []:
        indent = len(ln) - len(ln.lstrip())
        if cur is not None:
            kind, depth, seen_blank = cur["kind"], cur["depth"], cur["blank"]
            if not ln.strip():
                cur["blank"] = True
                continue
            if kind == "heading":
                hm = HEADING.match(ln.lstrip())
                if not (hm and len(hm.group(1)) <= depth):
                    cur["lines"].append(ln)
                    continue
            elif indent > depth:
                cur["lines"].append(ln)
                continue
            elif kind == "label" and not seen_blank and ln.lstrip().startswith(("- ", "* ", "+ ")):
                cur["lines"].append(ln)
                continue
            elif not seen_blank and not NEW_ITEM.match(ln):
                cur["lines"].append(ln)  # wrapped text that goes on from the line above
                continue
            blocks.append(cur["lines"])
            cur = None
        if FAILS_BULLET.match(ln):
            cur = {"kind": "bullet", "depth": indent, "blank": False, "lines": [ln]}
            continue
        if FAILS_HEAD.match(ln):
            hm = HEADING.match(ln.lstrip())
            cur = {"kind": "heading" if hm else "label", "depth": len(hm.group(1)) if hm else indent,
                   "blank": False, "lines": [ln]}
            continue
        if "fails if" in ln.lower():
            blocks.append([ln])
            continue
        kept.append(ln)
    if cur is not None:
        blocks.append(cur["lines"])
    return kept, blocks


def _text_of(line):
    m = FAILS_BULLET.match(line)
    if m:
        return m.group("text")
    text = re.sub(r"^\s*(?:[-*+]\s+|\d+[.)]\s+|#+\s*)", "", line).strip()
    return re.sub(r"^(?:\*\*)?Fails if:?(?:\*\*)?:?\s*", "", text, flags=re.IGNORECASE).strip()


def fails_if_texts(lines):
    """The text of every line of every "Fails if" block, children included."""
    return [t for block in _split(lines)[1] for t in (_text_of(ln) for ln in block) if t]


def without_fails_if(lines):
    """The lines with every "Fails if" block taken out: the line, label or heading and every
    line under it. Any other line that still names the words is taken out too."""
    return _split(lines)[0]


def page_title(root, rel, prefix):
    path = os.path.join(root, rel or "")
    if rel and os.path.isfile(path):
        for ln in read_text(path).splitlines():
            if ln.startswith("# "):
                head = ln[2:].strip()
                return head[len(prefix):].strip() if head.startswith(prefix) else head
    return None


# ---- the approval -----------------------------------------------------------------------

def approval_is_yes(path):
    """(ok, decision, reason): ok only when the file reads decision yes with a typed reply."""
    try:
        rec = json.loads(read_text(path))
    except (OSError, json.JSONDecodeError):
        return False, None, "no approval is recorded"
    decision = rec.get("decision") if isinstance(rec, dict) else None
    reply = rec.get("reply") if isinstance(rec, dict) else None
    if decision != "yes":
        return False, decision, f"the decision is {decision!r}, not yes"
    if not isinstance(reply, str) or not reply.strip():
        return False, decision, "the reply is empty"
    return True, decision, "the person typed yes"


def approval_matches(path, work_items, drafts):
    """(ok, reason): ok only when the brief, work-items.json and drafts.json are still the
    files the person saw when they typed their answer (their sha256 is the one recorded)."""
    try:
        files = json.loads(read_text(path)).get("files") or {}
    except (OSError, json.JSONDecodeError, AttributeError):
        return False, "no approval is recorded"
    want = {"brief": (files.get("brief") or {}).get("path"), "work_items": work_items, "drafts": drafts}
    for key, file_path in want.items():
        seen = (files.get(key) or {}).get("sha256")
        if not seen:
            return False, f"the approval does not record which {key.replace('_', '-')} the person saw"
        if not file_path or sha256_of(file_path) != seen:
            return False, (f"{key.replace('_', '-')} ({file_path}) is not the file the person saw; "
                           "show the brief again")
    return True, "the files are the ones the person saw"


# ---- the tracker ------------------------------------------------------------------------

def _issue(raw):
    return {"number": int(raw["number"]), "title": raw.get("title") or "",
            "type": raw.get("type"), "labels": list(raw.get("labels") or []),
            "state": (raw.get("state") or "open").lower(), "body": raw.get("body") or "",
            "sub_issues": [int(n) for n in raw.get("sub_issues") or []]}


class FileTracker:
    """A tracker kept in a JSON file. Like a real tracker, each write is kept at once."""

    def __init__(self, path):
        self.path = path
        data = read_json(path, "the tracker file")
        if not isinstance(data, dict) or not isinstance(data.get("issues"), list):
            raise Refused('the tracker file must be {"issues": [...]}')
        self.fail_at = data.get("fail_at_write")
        self.writes = 0
        self.issues = {}
        for raw in data["issues"]:
            if not isinstance(raw, dict) or "number" not in raw:
                raise Refused("each issue in the tracker file needs a number")
            self.issues[int(raw["number"])] = _issue(raw)

    def get(self, number):
        it = self.issues.get(int(number)) if number is not None else None
        return json.loads(json.dumps(it)) if it else None

    def _must(self, number):
        it = self.issues.get(int(number))
        if it is None:
            raise TrackerError(f"the tracker has no issue #{number}")
        return it

    def _write(self, what):
        self.writes += 1
        if self.fail_at is not None and self.writes == int(self.fail_at):
            raise TrackerError(f"the tracker did not take write {self.writes} ({what})")

    def _keep(self):
        data = {"issues": [self.issues[n] for n in sorted(self.issues)]}
        if self.fail_at is not None:
            data["fail_at_write"] = self.fail_at
        write_json(self.path, data)

    def create(self, title, body, type_, parent=None):
        self._write("make an issue")
        if parent is not None:
            self._must(parent)
        number = max(self.issues, default=0) + 1
        self.issues[number] = _issue({"number": number, "title": title, "type": type_,
                                      "labels": [], "state": "open", "body": body})
        if parent is not None:
            self.issues[int(parent)]["sub_issues"].append(number)
        self._keep()
        return number

    def set_type(self, number, type_):
        self._write("set the type")
        self._must(number)["type"] = type_
        self._keep()

    def set_body(self, number, body):
        self._write("change the body")
        self._must(number)["body"] = body
        self._keep()

    def remove_labels(self, number, labels):
        self._write("take off labels")
        it = self._must(number)
        it["labels"] = [lb for lb in it["labels"] if lb not in labels]
        self._keep()

    def add_sub(self, parent, child):
        self._write("add a sub-issue")
        self._must(child)
        subs = self._must(parent)["sub_issues"]
        if int(child) not in subs:
            subs.append(int(child))
        self._keep()

    def remove_sub(self, parent, child):
        self._write("take off a sub-issue")
        it = self._must(parent)
        it["sub_issues"] = [n for n in it["sub_issues"] if n != int(child)]
        self._keep()

    def save(self):
        return None


class HostTracker:
    """The code host, reached only through platform_adapter.py's verbs."""

    def __init__(self, config):
        import sys
        sys.path.insert(0, HERE)
        import platform_adapter as pa  # noqa: E402  (copied beside this script)
        self.pa, self.config = pa, config

    def _adapter(self, verb, args):
        res = self.pa.dispatch(verb, args, config_path=self.config)
        if res["exit_code"] != 0:
            raise TrackerError(f"{verb} failed: {res['stderr'].strip() or res['stdout'].strip()}")
        return res

    def get(self, number):
        if number is None:
            return None
        try:
            res = self._adapter("view-issue", {"issue_number": str(number)})
        except TrackerError:
            return None
        if not res.get("tree_available"):
            raise Refused("the tracker cannot show the issue type and sub-issues "
                          "(on GitHub, gh 2.94.0 or later is needed)")
        raw = json.loads(res["stdout"])
        subs = raw.get("subIssues") or []
        if isinstance(subs, dict):
            subs = subs.get("nodes") or []
        itype = raw.get("issueType") or {}
        return _issue({"number": raw["number"], "title": raw.get("title"),
                       "type": itype.get("name") if isinstance(itype, dict) else itype,
                       "labels": [lb.get("name") for lb in raw.get("labels") or []],
                       "state": raw.get("state"), "body": raw.get("body"),
                       "sub_issues": [s.get("number") for s in subs if isinstance(s, dict)]})

    def create(self, title, body, type_, parent=None):
        args = {"title": title, "body": body, "issue_type": type_}
        if parent is not None:
            args["parent_number"] = str(parent)
        res = self._adapter("create-issue-typed", args)
        number = res["stdout"].strip()
        if not number.isdigit():
            raise TrackerError(f"create-issue-typed gave no issue number: {number!r}")
        return int(number)

    def set_type(self, number, type_):
        self._adapter("set-issue-type", {"issue_number": str(number), "issue_type": type_})

    def set_body(self, number, body):
        self._adapter("edit-issue-body", {"issue_number": str(number), "body": body})

    def remove_labels(self, number, labels):
        for label in labels:
            self._adapter("remove-label", {"issue_number": str(number), "label": label})

    def add_sub(self, parent, child):
        self._adapter("attach-sub-issue", {"parent_number": str(parent), "child_number": str(child)})

    def remove_sub(self, parent, child):
        self._adapter("remove-sub-issue", {"parent_number": str(parent), "child_number": str(child)})

    def save(self):
        return None


def open_tracker(tracker_file=None, config=".garura/core/config.yaml"):
    return FileTracker(tracker_file) if tracker_file else HostTracker(config)


# ---- issue bodies -----------------------------------------------------------------------

def has_heading(body, name):
    return re.search(rf"(?im)^#{{1,6}}\s*{re.escape(name)}\s*$", body or "") is not None


def has_line(body, line):
    return any(ln.strip() == line for ln in (body or "").splitlines())


def lines_kept(old, new):
    """True when every line of `old` is in `new`, in the same order."""
    it = iter((new or "").splitlines())
    return all(any(ln == x for x in it) for ln in (old or "").splitlines())


# ---- the plan file's tree ---------------------------------------------------------------

def load_plan(path):
    """The plan file as a mapping, or None when there is no plan file."""
    if not os.path.isfile(path):
        return None
    plan = read_yaml(path, "the plan file")
    if not isinstance(plan, dict):
        raise Refused("the plan file must be a YAML mapping")
    return plan


def walk(nodes):
    """Every node of a tree, at any depth."""
    for node in nodes or []:
        if isinstance(node, dict):
            yield node
            yield from walk(node.get("children"))


def marked(nodes, represents):
    """The nodes, at any depth, whose `represents` is the given id."""
    return [n for n in walk(nodes) if str(n.get("represents") or "") == str(represents)]


def children(node):
    return [c for c in node.get("children") or [] if isinstance(c, dict)]


# ---- the epic's feature-to-story map ----------------------------------------------------

MAP_HEADING = "Feature-to-story map"
MAP_LINE = re.compile(r"^\s*[-*]\s+(?P<feature>\S+)\s+→\s+#(?P<issue>\d+)\s*$")


def _map_span(lines):
    """(start, end) of the map section's lines (heading included), or None."""
    at = next((i for i, ln in enumerate(lines)
               if re.match(rf"^(#{{1,6}})\s*{re.escape(MAP_HEADING)}\s*$", ln, re.IGNORECASE)), None)
    if at is None:
        return None
    level = len(re.match(r"^(#+)", lines[at]).group(1))
    end = next((i for i in range(at + 1, len(lines))
                if re.match(r"^(#+)\s", lines[i]) and len(re.match(r"^(#+)", lines[i]).group(1)) <= level),
               len(lines))
    return at, end


def read_map(body):
    """{feature: issue} from the epic's map section, or None when it has no map section."""
    lines = (body or "").splitlines()
    span = _map_span(lines)
    if span is None:
        return None
    out = {}
    for ln in lines[span[0] + 1:span[1]]:
        m = MAP_LINE.match(ln)
        if m:
            out[m.group("feature")] = int(m.group("issue"))
    return out


def map_lines(pairs):
    """The map section's text: the heading, then one line "<feature> → #<story>" each."""
    return [f"## {MAP_HEADING}", ""] + [f"- {f} → #{n}" for f, n in pairs]


def with_map(body, pairs):
    """The body with its map section written again; every other line stays where it is."""
    lines = (body or "").splitlines()
    new = map_lines(pairs)
    span = _map_span(lines)
    if span is None:
        while lines and not lines[-1].strip():
            lines.pop()
        lines = lines + ([""] if lines else []) + new
    else:
        tail = lines[span[1]:]
        lines = lines[:span[0]] + new + ([""] if tail else []) + tail
    return "\n".join(lines).rstrip() + "\n"


def map_pairs(slice_items, made=None):
    """[(feature, story issue)] in the slice's order: each feature that has a story, made in
    this run (`made`: {feature: issue}) or there before. A moved-out story is not in it."""
    made = made or {}
    out = []
    for st in slice_items.get("stories") or []:
        issue = made.get(st.get("feature")) or st.get("issue")
        if issue is not None:
            out.append((st.get("feature"), int(issue)))
    return out
