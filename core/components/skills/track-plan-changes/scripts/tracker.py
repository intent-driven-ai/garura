#!/usr/bin/env python3
"""tracker.py — the tracker a plan session reads and writes (track-plan-changes, #730).

Not run on its own. `open_tracker(config, tracker_file)` gives one of two trackers with the same
methods:

  - the file tracker (`--tracker-file <json>`), for tests and the test run of /update-plan: a JSON
    file {"issues": [{"number", "title", "type", "labels": [], "state": "OPEN"|"CLOSED",
    "state_reason": null|"COMPLETED"|"NOT_PLANNED", "body", "parent": null|number,
    "sub_issues": [numbers]}]}. Each write is kept at once (the file is written after every
    write), as a real tracker would. `"fail_at_write": <n>` makes the n-th write of the run fail,
    with nothing changed by it;
  - the code host, reached only through platform_adapter.py's verbs (copied beside this file):
    view-issue, close-issue, reopen-issue, edit-issue-title, edit-issue-body, set-issue-type,
    create-issue-typed, attach-sub-issue and remove-sub-issue.

Methods: get(number) -> issue dict, or None when the tracker has no such issue (any other failed
read raises TrackerError, never None); close(number, reason); reopen(number);
set_title(number, title); set_body(number, body); set_type(number, type); create(title, body,
type, parent) -> number; attach(parent, child); detach(parent, child); find_marked(text) -> the
numbers of issues whose text holds that exact line (a create's marker), so a run again finds
the issue an earlier run made.
An issue dict: {number, title, type, labels, state, state_reason, body, parent, sub_issues}.
No judgment is made here.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


class TrackerError(Exception):
    pass


def _issue(d):
    return {"number": int(d["number"]), "title": d.get("title") or "", "type": d.get("type"),
            "labels": list(d.get("labels") or []), "state": (d.get("state") or "OPEN").upper(),
            "state_reason": (d.get("state_reason") or None) and str(d["state_reason"]).upper(),
            "body": d.get("body") or "", "parent": d.get("parent"),
            "sub_issues": [int(n) for n in d.get("sub_issues") or []]}


class FileTracker:
    def __init__(self, path):
        self.path = path
        with open(path, encoding="utf-8") as fh:
            self.data = json.load(fh)
        self.writes = 0

    def _find(self, number):
        for d in self.data.get("issues", []):
            if int(d["number"]) == int(number):
                return d
        return None

    def _write(self):
        self.writes += 1
        if self.data.get("fail_at_write") == self.writes:
            raise TrackerError(f"write {self.writes} failed (fail_at_write)")

    def _save(self):
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(self.data, fh, indent=2)
            fh.write("\n")
        os.replace(tmp, self.path)

    def _need(self, number):
        d = self._find(number)
        if d is None:
            raise TrackerError(f"issue #{number} is not in the tracker")
        return d

    def get(self, number):
        d = self._find(number)
        if d is None:
            return None
        parent = d.get("parent")
        if parent is None:
            for p in self.data.get("issues", []):
                if int(number) in [int(n) for n in p.get("sub_issues") or []]:
                    parent = int(p["number"])
        return _issue({**d, "parent": parent})

    def close(self, number, reason):
        d = self._need(number)
        self._write()
        d["state"], d["state_reason"] = "CLOSED", "NOT_PLANNED" if reason == "not planned" else "COMPLETED"
        self._save()

    def reopen(self, number):
        d = self._need(number)
        self._write()
        d["state"], d["state_reason"] = "OPEN", "REOPENED"
        self._save()

    def set_title(self, number, title):
        d = self._need(number)
        self._write()
        d["title"] = title
        self._save()

    def set_body(self, number, body):
        d = self._need(number)
        self._write()
        d["body"] = body
        self._save()

    def set_type(self, number, type_):
        d = self._need(number)
        self._write()
        d["type"] = type_
        self._save()

    def create(self, title, body, type_, parent=None):
        self._write()
        issues = self.data.setdefault("issues", [])
        number = max([int(d["number"]) for d in issues] + [0]) + 1
        issues.append({"number": number, "title": title, "type": type_, "labels": [], "state": "OPEN",
                       "state_reason": None, "body": body, "parent": None, "sub_issues": []})
        if parent is not None:
            self._need(parent).setdefault("sub_issues", []).append(number)
        self._save()
        return number

    def find_marked(self, text):
        return [int(d["number"]) for d in self.data.get("issues", []) if text in (d.get("body") or "")]

    def attach(self, parent, child):
        p = self._need(parent)
        self._need(child)
        self._write()
        for d in self.data.get("issues", []):
            if int(child) in [int(n) for n in d.get("sub_issues") or []]:
                d["sub_issues"] = [n for n in d["sub_issues"] if int(n) != int(child)]
        p.setdefault("sub_issues", []).append(int(child))
        self._need(child)["parent"] = None
        self._save()

    def detach(self, parent, child):
        p = self._need(parent)
        self._write()
        p["sub_issues"] = [n for n in p.get("sub_issues") or [] if int(n) != int(child)]
        self._save()


class HostTracker:
    """The code host, reached only through platform_adapter.py's verbs."""

    def __init__(self, config):
        sys.path.insert(0, HERE)
        import platform_adapter as pa  # noqa: E402  (copied beside this script)
        self.pa, self.config = pa, config

    def _adapter(self, verb, args):
        res = self.pa.dispatch(verb, args, config_path=self.config)
        if res["exit_code"] != 0:
            raise TrackerError(f"{verb} failed: {(res['stderr'] or res['stdout']).strip()}")
        return res

    def get(self, number):
        res = self.pa.dispatch("view-issue", {"issue_number": str(number)}, config_path=self.config)
        if res["exit_code"] != 0:
            why = (res["stderr"] or res["stdout"]).strip()
            if "could not resolve to an issue" in why.lower():
                return None  # the tracker has no such issue
            raise TrackerError(f"view-issue #{number} failed: {why}")
        if not res.get("tree_available", True):
            raise TrackerError("the tracker cannot show issue types and parents "
                               "(on GitHub, gh 2.94.0 or later is needed)")
        raw = json.loads(res["stdout"])
        subs = raw.get("subIssues") or []
        if isinstance(subs, dict):
            subs = subs.get("nodes") or []
        itype = raw.get("issueType") or {}
        parent = raw.get("parent") or {}
        return _issue({"number": raw["number"], "title": raw.get("title"),
                       "type": itype.get("name") if isinstance(itype, dict) else itype,
                       "labels": [lb.get("name") for lb in raw.get("labels") or []],
                       "state": raw.get("state"), "state_reason": raw.get("stateReason"),
                       "body": raw.get("body"),
                       "parent": parent.get("number") if isinstance(parent, dict) else parent,
                       "sub_issues": [s.get("number") for s in subs if isinstance(s, dict)]})

    def close(self, number, reason):
        self._adapter("close-issue", {"issue_number": str(number), "reason": reason})

    def reopen(self, number):
        self._adapter("reopen-issue", {"issue_number": str(number)})

    def set_title(self, number, title):
        self._adapter("edit-issue-title", {"issue_number": str(number), "title": title})

    def set_body(self, number, body):
        self._adapter("edit-issue-body", {"issue_number": str(number), "body": body})

    def set_type(self, number, type_):
        self._adapter("set-issue-type", {"issue_number": str(number), "issue_type": type_})

    def create(self, title, body, type_, parent=None):
        args = {"title": title, "body": body, "issue_type": type_}
        if parent is not None:
            args["parent_number"] = str(parent)
        number = self._adapter("create-issue-typed", args)["stdout"].strip()
        if not number.isdigit():
            raise TrackerError(f"create-issue-typed gave no issue number: {number!r}")
        return int(number)

    def find_marked(self, text):
        res = self._adapter("list-issues", {"query": f'"{text}" in:body', "state": "all", "limit": 10})
        try:
            hits = json.loads(res["stdout"] or "[]")
        except ValueError:
            raise TrackerError("list-issues gave no JSON")
        found = []
        for hit in hits:
            issue = self.get(hit.get("number"))
            if issue and text in issue["body"]:
                found.append(issue["number"])
        return found

    def attach(self, parent, child):
        self._adapter("attach-sub-issue", {"parent_number": str(parent), "child_number": str(child)})

    def detach(self, parent, child):
        self._adapter("remove-sub-issue", {"parent_number": str(parent), "child_number": str(child)})


def open_tracker(config, tracker_file=None):
    return FileTracker(tracker_file) if tracker_file else HostTracker(config)
