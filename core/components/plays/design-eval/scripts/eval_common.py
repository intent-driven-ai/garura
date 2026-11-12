#!/usr/bin/env python3
"""eval_common.py — the parts the /design-eval scripts share.

Not run on its own. The scripts beside it import it for six jobs:

  - Safe writes. `atomic_write` and `write_json` write through a temp file in the same folder,
    then move it into place with os.replace, so a run that stops half way never leaves half a
    file.
  - The tracker, read only. `open_tracker` gives a file tracker (`--tracker-file <json>`, for
    tests and dry runs: {"issues": [{"number", "title", "body", "type"}]}) or the code host,
    reached only through platform_adapter.py's `view-issue` verb. Both have `get(number)`, which
    gives the issue's number, title, body and type (None when the host does not say).
  - A Feature issue's text. `parse_feature_issue` reads the "Scope of work" section that
    /shape-plan writes (the "Goals:", "Limits:" and "Expectations:" lists) and the "Context
    guidance" section; `has_line` finds the exact line `Represents: <feature id>`. `parse_map`
    reads the plan epic's "Feature-to-story map" (`- fn-795 → #795`, or `- fn-795 → #795 (under
    Epic #121)` for a Feature issue that sits under another plan's epic), in its order.
  - A hidden file. `parse_hidden` reads a slice's failure-and-recovery.md: the slice id of its
    first heading, its Surface line, its features in the order of its entries (the slice's build
    order), each feature's failure conditions (`F<n>`) and the text of every recovery line, which
    must never reach an eval.
  - The step library of a surface kind (`standards/schemas/eval/steps-<kind>.yaml`).
    `load_library` turns each sentence into a pattern; `match_step` says which sentence a step
    is, or None.
  - The eval files. `parse_feature_file` reads a feature file (Markdown with Gherkin, the
    `eval-feature.feature.md` template): its tags, its `Feature:` title, its Background, each
    Scenario with its tags, steps and raw text, its Untestable lines and its Lines covered list
    (the text of each Feature issue line a tag covers, as the file recorded it).
    `parse_plan_file` reads the plan file (`eval-plan.md`): one section for each slice.

No judgment is made here: every rule is fixed.
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
RECOVERY_WORDS = ("the builder can fix this alone", "a person must decide", "way back:", "who fixes:")


class Refused(Exception):
    """A refusal or bad input: the script writes nothing and exits 2."""


# ---- files ------------------------------------------------------------------------------

def atomic_write(path, text):
    folder = os.path.dirname(os.path.abspath(path))
    os.makedirs(folder, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=folder, prefix=".tmp-", suffix=os.path.basename(path))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def write_json(path, data):
    atomic_write(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def read_text(path, what):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError as exc:
        raise Refused(f"cannot read {what} at {path}: {exc}")


def read_json(path, what):
    try:
        return json.loads(read_text(path, what))
    except json.JSONDecodeError as exc:
        raise Refused(f"{what} at {path} is not JSON: {exc}")


def read_yaml(path, what):
    if yaml is None:
        raise Refused("PyYAML is needed (pip install pyyaml)")
    try:
        return yaml.safe_load(read_text(path, what))
    except yaml.YAMLError as exc:
        raise Refused(f"{what} at {path} is not YAML: {exc}")


# ---- the tracker, read only ------------------------------------------------------------

class FileTracker:
    def __init__(self, path):
        data = read_json(path, "the tracker file")
        if not isinstance(data, dict) or not isinstance(data.get("issues"), list):
            raise Refused('the tracker file must be {"issues": [...]}')
        self.issues = {int(i["number"]): i for i in data["issues"] if isinstance(i, dict) and "number" in i}

    def get(self, number):
        it = self.issues.get(int(number))
        return {"number": it["number"], "title": it.get("title") or "", "body": it.get("body") or "",
                "type": it.get("type")} if it else None


class HostTracker:
    def __init__(self, config):
        import sys
        sys.path.insert(0, HERE)
        import platform_adapter as pa  # noqa: E402  (copied beside this script)
        self.pa, self.config = pa, config

    def get(self, number):
        res = self.pa.dispatch("view-issue", {"issue_number": str(number)}, config_path=self.config)
        if res["exit_code"] != 0:
            return None
        raw = json.loads(res["stdout"])
        kind = raw.get("issueType")
        return {"number": raw["number"], "title": raw.get("title") or "", "body": raw.get("body") or "",
                "type": (kind.get("name") if isinstance(kind, dict) else kind) or None}


def open_tracker(tracker_file=None, config=".garura/core/config.yaml"):
    return FileTracker(tracker_file) if tracker_file else HostTracker(config)


# ---- a Feature issue, the epic ---------------------------------------------------------

def _section(body, name):
    """The lines of the `## <name>` section of an issue body, up to the next heading of level 1 or 2."""
    out, inside = [], False
    for line in (body or "").splitlines():
        m = re.match(r"^(#{1,6})\s+(.*?)\s*$", line)
        if m and len(m.group(1)) <= 2:
            if inside:
                break
            inside = m.group(2).strip().lower() == name.lower()
            continue
        if inside:
            out.append(line)
    return out


def _bullets(lines):
    """Each `- ` item of a list, with its wrapped lines joined."""
    items = []
    for line in lines:
        if re.match(r"^\s*[-*]\s+", line):
            items.append(re.sub(r"^\s*[-*]\s+", "", line).strip())
        elif items and line.startswith("  ") and line.strip():
            items[-1] += " " + line.strip()
    return items


def parse_feature_issue(body):
    """{goals, limits, expectations, context, has_scope}: the Feature issue's Scope of work lists, in order."""
    scope = _section(body, "Scope of work")
    lists, current = {"goals": [], "limits": [], "expectations": []}, None
    chunk = {"goals": [], "limits": [], "expectations": []}
    for line in scope:
        head = line.strip().rstrip(":").lower()
        if line.strip().endswith(":") and head in lists:
            current = head
            continue
        if current:
            chunk[current].append(line)
    for key in lists:
        lists[key] = _bullets(chunk[key])
    context = _bullets(_section(body, "Context guidance"))
    return dict(lists, context=context, has_scope=bool(scope))


def has_line(body, line):
    """True when the body has this exact line (spaces at the ends not counted)."""
    return any(ln.strip() == line for ln in (body or "").splitlines())


MAP_LINE = re.compile(r"^\s*[-*]\s*(?P<feature>[\w.-]+)\s*(?:→|->)\s*#(?P<issue>\d+)"
                      r"(?:\s*\((?:under|held by)\s+(?:[Ee]pic\s+)?#(?P<held>\d+)\))?\s*$")


def parse_map(body):
    """The plan epic's feature-to-story map, in its order: [{feature, issue, held_by}], where
    held_by is the other plan's epic that holds the Feature issue, or None."""
    return [{"feature": m["feature"], "issue": int(m["issue"]), "held_by": int(m["held"]) if m["held"] else None}
            for m in (MAP_LINE.match(ln) for ln in _section(body, "Feature-to-story map")) if m]


# ---- the hidden file --------------------------------------------------------------------

HIDDEN_ENTRY = re.compile(r"^##\s+(?P<feature>[\w.-]+):")
FAILURE = re.compile(r"^\s*-\s*(?P<id>F\d+)\b[^:]*:\s*(?P<text>.+)$")


def parse_hidden(text):
    """{slice_id, surface, features: [feature id, in the order of the entries], failures: {feature: [{id, text}]},
    recovery_lines: [...]}."""
    first = next((ln for ln in text.splitlines() if ln.startswith("# ")), "")
    m = re.search(r"slice\s+([\w.-]+)", first)
    m2 = re.search(r"Surface:\s*([^.;\n]+)", text)
    surface = m2.group(1).strip() if m2 else None
    failures, recovery, feature, part = {}, [], None, None
    for line in text.splitlines():
        e = HIDDEN_ENTRY.match(line)
        if e:
            feature, part = e["feature"], None
            failures.setdefault(feature, [])
            continue
        if line.startswith("### "):
            part = line[4:].strip().lower()
            continue
        if feature and part == "failure conditions":
            f = FAILURE.match(line)
            if f:
                failures[feature].append({"id": f["id"], "text": f["text"].strip()})
        elif feature and part == "recovery":
            r = re.match(r"^\s*-\s*(When|Way back|Who fixes):\s*(.+)$", line)
            if r and r.group(1) != "Who fixes":
                recovery.append(r.group(2).strip())
    return {"slice_id": m.group(1) if m else None, "surface": surface, "features": list(failures),
            "failures": failures, "recovery_lines": recovery}


# ---- the step library -------------------------------------------------------------------

VALUE = r'(?:"[^"]*"|\[[^\]]+\])'
NAME = r'\[[^\]]+\]'


def _pattern(sentence):
    out, pos = "", 0
    for m in re.finditer(r"\{(value|name|n)\}", sentence):
        out += re.escape(sentence[pos:m.start()])
        out += {"value": VALUE, "name": NAME, "n": r"\d+"}[m.group(1)]
        pos = m.end()
    return re.compile("^" + out + re.escape(sentence[pos:]) + "$")


def load_library(path):
    data = read_yaml(path, "the step library")
    if not isinstance(data, dict) or not data.get("kind") or not isinstance(data.get("steps"), list):
        raise Refused(f"{path} is not a step library (kind and steps are needed)")
    steps = [{"id": s["id"], "keyword": s["keyword"], "text": s["text"], "re": _pattern(s["text"])}
             for s in data["steps"]]
    return {"kind": data["kind"], "matches": [m.lower() for m in data.get("matches") or []], "steps": steps}


def kind_of(surface, libraries):
    """The library whose `matches` names the surface, or None."""
    s = (surface or "").lower()
    for lib in libraries:
        if any(m in s for m in lib["matches"]) or lib["kind"] in s:
            return lib
    return None


def match_step(keyword, text, library):
    """The library sentence a step is (keyword already resolved for And / But), or None."""
    return next((s for s in library["steps"] if s["keyword"] == keyword and s["re"].match(text)), None)


def names_in(text):
    return re.findall(r"\[([^\]]+)\]", text)


# ---- the eval files ---------------------------------------------------------------------

TAG_LINE = re.compile(r"^\s*(`@[\w.-]+`\s*)+$")
KEYWORD = re.compile(r"^#+\s*(?P<kw>Feature|Business Need|Ability|Background|Rule|Scenario|Example)\s*:\s*(?P<title>.*)$")
STEP = re.compile(r"^\s*[-*]\s+(?P<kw>Given|When|Then|And|But)\s+(?P<text>.+?)\s*$")
COVERED = re.compile(r"^\s*[-*]\s*`@(?P<tag>[\w.-]+)`\s*:\s*(?P<text>.+)$")
UNTESTABLE = re.compile(r"^\s*[-*]\s*(?P<tags>(?:`@[\w.-]+`\s*)+):\s*(?P<reason>.+)$")


def tags_of(line):
    return re.findall(r"`@([\w.-]+)`", line)


def parse_feature_file(text):
    """{top_tags, feature, background, scenarios: [{tags, title, steps: [(kw, text)], raw}], untestable,
    lines_covered: {tag: the Feature issue line's text as the file recorded it}, errors}."""
    lines = text.splitlines()
    res = {"top_tags": [], "feature": None, "background": [], "scenarios": [], "untestable": [],
           "lines_covered": {}, "errors": []}
    pending, block, current, section = [], None, None, None
    for i, line in enumerate(lines):
        if TAG_LINE.match(line):
            pending = tags_of(line)
            block = [line]
            continue
        k = KEYWORD.match(line)
        if k:
            kw = k["kw"]
            if kw in ("Feature", "Business Need", "Ability"):
                if res["feature"] is not None:
                    res["errors"].append("more than one Feature: in the file")
                res["feature"], res["top_tags"] = k["title"].strip(), pending
                current, section = None, "feature"
            elif kw == "Background":
                current, section = None, "background"
            elif kw in ("Scenario", "Example"):
                current = {"tags": pending, "title": k["title"].strip(), "steps": [],
                           "raw": (block or []) + [line]}
                res["scenarios"].append(current)
                section = "scenario"
            else:  # Rule: allowed, groups scenarios
                current, section = None, "rule"
            pending, block = [], None
            continue
        if re.match(r"^#+\s*Untestable\s*$", line):
            current, section, pending, block = None, "untestable", [], None
            continue
        if re.match(r"^#+\s*Lines covered\s*$", line):
            current, section, pending, block = None, "covered", [], None
            continue
        if re.match(r"^#+\s", line):
            current, section, pending, block = None, "prose", [], None
            continue
        s = STEP.match(line)
        if s and section in ("scenario", "background"):
            target = current["steps"] if section == "scenario" else res["background"]
            target.append((s["kw"], s["text"]))
            if current is not None:
                current["raw"].append(line)
            continue
        if section == "covered":
            c = COVERED.match(line)
            if c:
                res["lines_covered"][c["tag"]] = c["text"].strip()
            continue
        if section == "untestable":
            u = UNTESTABLE.match(line)
            if u:
                res["untestable"].append({"tags": tags_of(u["tags"]), "reason": u["reason"].strip()})
            continue
        if current is not None and section == "scenario":
            current["raw"].append(line)
    for sc in res["scenarios"]:
        while sc["raw"] and not sc["raw"][-1].strip():
            sc["raw"].pop()
        sc["raw"] = "\n".join(sc["raw"])
    return res


def resolve_keywords(steps):
    """[(keyword for the library, text, as written)]: And / But take the keyword of the step before."""
    out, last = [], None
    for kw, text in steps:
        real = last if kw in ("And", "But") else kw
        out.append((real, text, kw))
        last = real
    return out


FEATURE_ITEM = re.compile(r"^\s*\d+\.\s*Feature issue #(?P<issue>\d+)\s*\((?P<feature>[\w.-]+)\)\s*—\s*(?P<file>\S+)"
                          r"(?:\s*\(held by epic #(?P<held>\d+)\))?")
OUT_ITEM = re.compile(r"^\s*[-*]\s*Feature issue #(?P<issue>\d+)\s*\((?P<feature>[\w.-]+)\)\s*—\s*(?P<file>\S+?):?\s")


def parse_plan_file(text):
    """{title, has_pass_rule, slices: [{slice, surface_kind, time_limit, features: [(feature, issue, file)],
    held: {feature: epic}}], out_of_plan: [(feature, issue, file)], names}."""
    res = {"title": None, "has_pass_rule": False, "slices": [], "out_of_plan": [], "names": []}
    section, current = None, None
    for line in text.splitlines():
        if line.startswith("# ") and res["title"] is None:
            res["title"] = line[2:].strip()
            continue
        h = re.match(r"^##\s+(.*?)\s*$", line)
        if h:
            head = h.group(1)
            sm = re.match(r"^Slice\s+([\w.-]+)", head)
            if sm:
                section = "slice"
                current = {"slice": sm.group(1), "surface_kind": None, "time_limit": None, "features": [],
                           "held": {}}
                res["slices"].append(current)
            else:
                section, current = head.lower(), None
                if section == "pass rule":
                    res["has_pass_rule"] = True
            continue
        if section == "slice":
            m = re.match(r"^Surface kind:\s*(\S+)", line)
            if m:
                current["surface_kind"] = m.group(1)
            m = re.match(r"^Time limit for each scenario:\s*(\d+)\s*seconds?\s*$", line)
            if m:
                current["time_limit"] = int(m.group(1))
            m = FEATURE_ITEM.match(line)
            if m:
                current["features"].append((m["feature"], int(m["issue"]), m["file"]))
                if m["held"]:
                    current["held"][m["feature"]] = int(m["held"])
        elif section == "out of the plan":
            m = OUT_ITEM.match(line + " ")
            if m:
                res["out_of_plan"].append((m["feature"], int(m["issue"]), m["file"].rstrip(":")))
        elif section == "names":
            m = re.match(r"^\s*[-*]\s*\[([^\]]+)\]", line)
            if m:
                res["names"].append(m.group(1))
    return res


def issue_line(feature, tag):
    """The Feature issue's line a `goal-<k>` or `expectation-<k>` tag points at now, or None."""
    m = re.match(r"^(goal|expectation)-(\d+)$", tag)
    if not m:
        return None
    items = feature.get("goals" if m.group(1) == "goal" else "expectations") or []
    k = int(m.group(2))
    return items[k - 1] if 1 <= k <= len(items) else None


def same_line(a, b):
    return " ".join(str(a or "").split()) == " ".join(str(b or "").split())


def feature_file_name(feature):
    return f"eval.{feature}.feature.md"


def plan_file_name(plan_id):
    return f"eval.{plan_id}.md"
