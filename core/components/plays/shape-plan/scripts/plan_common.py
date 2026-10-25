#!/usr/bin/env python3
"""plan_common.py — the parts the /shape-plan scripts share.

Not run on its own. The scripts beside it import it for four jobs:

  - Safe writes. `atomic_write` and `write_json` write through a temp file in the same folder,
    then move it into place with os.replace. A run that stops half way never leaves half a
    file.
  - The ICE text of a part. `ice_lines` reads the ICE of a feature or a capability: the inline
    `## Agent intent (ICE)` section of the part's page, or, when the spine has an `ices` list,
    the `## Intent`, `## Context` and `## Expectation` sections of the part's ice.md.
    `fails_if_texts` lists its "Fails if" lines and `without_fails_if` takes them out.
  - The words that must never reach an epic, a story or a plan file: "Fails if" and the two
    recovery phrases (`forbidden_in`).
  - The tracker. `open_tracker` gives a file tracker (`--tracker-file <json>`, for tests and
    dry runs) or the code host, reached through platform_adapter.py. Both have the same
    methods: get, create, set_type, set_body, remove_labels, add_sub, remove_sub, save.

The file tracker is a JSON file {"issues": [{"number", "title", "type", "labels": [],
"state", "body", "sub_issues": [numbers]}]}. A new issue takes the next free number. Its
changes are written to the file only by save(), so a run that fails half way changes nothing.

The code host is GitHub only. The adapter gives view-issue, create-issue and
attach-sub-issue. It has no verb to set the issue type, change the body, take off a label or
take off a sub-issue, so those four run as fixed gh commands on the repository the adapter
names. No judgment is made here.
"""

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
        if n and n in low:
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


def fails_if_texts(lines):
    """The text of each "Fails if" line."""
    out = []
    for ln in lines or []:
        m = FAILS_BULLET.match(ln)
        if m and m.group("text"):
            out.append(m.group("text"))
    return out


def without_fails_if(lines):
    """The lines with every "Fails if" line, its wrapped lines and a "Fails if" block taken out.
    Any other line that still names the words is taken out too."""
    out, skip_deeper, skip_block = [], None, None
    for ln in lines or []:
        indent = len(ln) - len(ln.lstrip())
        if skip_block is not None:
            hm = HEADING.match(ln.lstrip())
            if skip_block == "label":
                # a bold "Fails if" label: its list goes on while the lines are list items or blank
                if not ln.strip() or ln.lstrip().startswith(("- ", "* ")) or indent > 0:
                    continue
                skip_block = None
            elif hm and len(hm.group(1)) <= skip_block:
                skip_block = None
            else:
                continue
        if skip_deeper is not None:
            if ln.strip() and indent > skip_deeper and not ln.lstrip().startswith(("- ", "* ")):
                continue
            skip_deeper = None
        if FAILS_BULLET.match(ln):
            skip_deeper = indent
            continue
        if FAILS_HEAD.match(ln):
            hm = HEADING.match(ln.lstrip())
            skip_block = len(hm.group(1)) if hm else "label"
            continue
        if "fails if" in ln.lower():
            continue
        out.append(ln)
    return out


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


# ---- the tracker ------------------------------------------------------------------------

def _issue(raw):
    return {"number": int(raw["number"]), "title": raw.get("title") or "",
            "type": raw.get("type"), "labels": list(raw.get("labels") or []),
            "state": (raw.get("state") or "open").lower(), "body": raw.get("body") or "",
            "sub_issues": [int(n) for n in raw.get("sub_issues") or []]}


class FileTracker:
    """A tracker kept in a JSON file. Changes reach the file only on save()."""

    def __init__(self, path):
        self.path = path
        data = read_json(path, "the tracker file")
        if not isinstance(data, dict) or not isinstance(data.get("issues"), list):
            raise Refused('the tracker file must be {"issues": [...]}')
        self.issues = {}
        for raw in data["issues"]:
            if not isinstance(raw, dict) or "number" not in raw:
                raise Refused("each issue in the tracker file needs a number")
            self.issues[int(raw["number"])] = _issue(raw)

    def get(self, number):
        it = self.issues.get(int(number))
        return json.loads(json.dumps(it)) if it else None

    def _must(self, number):
        it = self.issues.get(int(number))
        if it is None:
            raise TrackerError(f"the tracker has no issue #{number}")
        return it

    def create(self, title, body, type_):
        number = max(self.issues, default=0) + 1
        self.issues[number] = _issue({"number": number, "title": title, "type": type_,
                                      "labels": [], "state": "open", "body": body})
        return number

    def set_type(self, number, type_):
        self._must(number)["type"] = type_

    def set_body(self, number, body):
        self._must(number)["body"] = body

    def remove_labels(self, number, labels):
        it = self._must(number)
        it["labels"] = [lb for lb in it["labels"] if lb not in labels]

    def add_sub(self, parent, child):
        self._must(child)
        subs = self._must(parent)["sub_issues"]
        if int(child) not in subs:
            subs.append(int(child))

    def remove_sub(self, parent, child):
        it = self._must(parent)
        it["sub_issues"] = [n for n in it["sub_issues"] if n != int(child)]

    def save(self):
        write_json(self.path, {"issues": [self.issues[n] for n in sorted(self.issues)]})


class HostTracker:
    """The code host (GitHub), reached through platform_adapter.py."""

    def __init__(self, config):
        import sys
        sys.path.insert(0, HERE)
        import platform_adapter as pa  # noqa: E402  (copied beside this script)
        self.pa, self.config = pa, config
        if pa.resolve_platform(config) != pa.GITHUB:
            raise Refused("the code host is not GitHub; /shape-plan writes work items on GitHub only. "
                          "Give --tracker-file for a dry run")
        self.owner, self.name = pa.resolve_repo(config)
        if not self.owner or not self.name:
            raise Refused("the config names no repository (host owner and name)")
        self.repo = f"{self.owner}/{self.name}"

    def _adapter(self, verb, args):
        res = self.pa.dispatch(verb, args, config_path=self.config)
        if res["exit_code"] != 0:
            raise TrackerError(f"{verb} failed: {res['stderr'].strip() or res['stdout'].strip()}")
        return res

    def _gh(self, *argv):
        rc, out, err = self.pa._run(["gh", *argv])
        if rc != 0:
            raise TrackerError(f"gh {argv[0]} failed: {err.strip() or out.strip()}")
        return out

    def get(self, number):
        try:
            res = self._adapter("view-issue", {"issue_number": str(number)})
        except TrackerError:
            return None
        if not res.get("tree_available"):
            raise Refused("the tracker cannot show the issue type and sub-issues (gh 2.94.0 or later is needed)")
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

    def create(self, title, body, type_):
        res = self._adapter("create-issue", {"title": title, "body": body})
        m = re.search(r"/issues/(\d+)", res["stdout"])
        if not m:
            raise TrackerError(f"create-issue gave no issue number: {res['stdout'].strip()}")
        number = int(m.group(1))
        self.set_type(number, type_)
        return number

    def set_type(self, number, type_):
        self._gh("api", "-X", "PATCH", f"repos/{self.repo}/issues/{number}", "-f", f"type={type_}")

    def set_body(self, number, body):
        self._gh("api", "-X", "PATCH", f"repos/{self.repo}/issues/{number}", "-f", f"body={body}")

    def remove_labels(self, number, labels):
        for label in labels:
            self._gh("issue", "edit", str(number), "-R", self.repo, "--remove-label", label)

    def add_sub(self, parent, child):
        self._adapter("attach-sub-issue", {"parent_number": str(parent), "child_number": str(child)})

    def remove_sub(self, parent, child):
        child_id = self._gh("api", f"repos/{self.repo}/issues/{child}", "--jq", ".id").strip()
        self._gh("api", "-X", "DELETE", f"repos/{self.repo}/issues/{parent}/sub_issue",
                 "-F", f"sub_issue_id={child_id}")

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
