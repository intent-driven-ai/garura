#!/usr/bin/env python3
"""
updates.py — memory updates, kept in the issue's short-term memory (contract version 5).

A memory update is raised when no tier answers. It waits for a person. A person approves or
rejects it, one at a time, in the review tool. An approved update is written to the issue's
own short-term memory. Every update lands in short-term memory; moving memory up is the
/learn-memory and /promote-memory plays, not this file.

Each update is one JSON file: <short-term root>/<issue>/<updates_dir>/<id>.json, holding the
update as the contract shapes it, plus the fingerprint its target had when it was proposed
(so apply can tell when the target changed since). Standard library only.
"""

import datetime
import hashlib
import json
import os
import re

from pull import Refusal

ID = re.compile(r"^mu-(\d{8})-(\d{3,})$")


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fingerprint(data):
    return "sha256:" + hashlib.sha256(data).hexdigest()


class UpdateStore:
    def __init__(self, short_term_root, updates_dir):
        self.root, self.dir = short_term_root, updates_dir.strip("/")

    # where things are
    def folder(self, issue):
        return os.path.join(self.root, str(issue), self.dir)

    def records(self):
        """(path, record) for every update in short-term memory, oldest id first."""
        found = []
        for issue in sorted(os.listdir(self.root)):
            folder = self.folder(issue)
            if not issue.isdigit() or not os.path.isdir(folder):
                continue
            for name in sorted(os.listdir(folder)):
                if ID.match(name[:-5]) and name.endswith(".json"):
                    path = os.path.join(folder, name)
                    with open(path, encoding="utf-8") as fh:
                        found.append((path, json.load(fh)))
        return sorted(found, key=lambda pr: pr[1]["update"]["id"])

    def find(self, uid):
        for path, record in self.records():
            if record["update"]["id"] == uid:
                return path, record
        raise Refusal("not_found", f"No memory update {uid}.", "short-term")

    def save(self, path, record):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(record, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        os.replace(tmp, path)

    def target(self, update):
        return os.path.join(self.root, update["target_path"])

    def target_fingerprint(self, update):
        path = self.target(update)
        if not os.path.isfile(path):
            return None
        with open(path, "rb") as fh:
            return fingerprint(fh.read())

    def next_id(self):
        day = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d")
        taken = [int(m.group(2)) for _, r in self.records()
                 if (m := ID.match(r["update"]["id"])) and m.group(1) == day]
        return f"mu-{day}-{max(taken, default=0) + 1:03d}"

    # the four commands
    def propose(self, request):
        issue, target = request["issue"], request["target_path"]
        if not target.startswith(f"{issue}/"):
            raise Refusal("bad_request", f"An update to short-term memory goes in its own issue: {target} "
                          f"is outside issue {issue}.", "short-term")
        if target.startswith(f"{issue}/{self.dir}/") or target == f"{issue}/{self.dir}":
            raise Refusal("bad_request", f"{target} is where memory updates are kept, not where an answer "
                          "is written.", "short-term")
        update = {
            "id": self.next_id(), "status": "waiting", "issue": issue, "missing": request["missing"],
            "target_tier": "short-term", "target_path": target, "draft": request["draft"],
            "draft_source": request["draft_source"], "sources": request["sources"],
            "requested_by": request["requested_by"], "requested_at": now(),
            "decided_by": None, "reply": None, "decided_at": None, "applied_version": None,
            "blocking": request.get("blocking", False), "decided_in": None,
        }
        record = {"update": update, "target_fingerprint_at_propose": self.target_fingerprint(update)}
        self.save(os.path.join(self.folder(issue), update["id"] + ".json"), record)
        return update

    def list(self, status=None):
        return [r["update"] for _, r in self.records() if status is None or r["update"]["status"] == status]

    def decide(self, request):
        path, record = self.find(request["id"])
        update = record["update"]
        if update["status"] != "waiting":
            raise Refusal("wrong_state", f"Memory update {update['id']} is {update['status']}, not waiting: "
                          "a person decides an update once.", "short-term")
        update.update({"status": "approved" if request["verdict"] == "approve" else "rejected",
                       "decided_by": request["by"], "reply": request["reply"], "decided_at": now(),
                       "decided_in": request["decided_in"]})
        self.save(path, record)
        return update

    def apply(self, request):
        path, record = self.find(request["id"])
        update = record["update"]
        if update["status"] == "applied":
            raise Refusal("wrong_state", f"Memory update {update['id']} is already applied.", "short-term")
        if update["status"] != "approved":
            raise Refusal("not_approved", f"Memory update {update['id']} is {update['status']}: only an update "
                          "a person approved is written.", "short-term")
        if self.target_fingerprint(update) != record["target_fingerprint_at_propose"]:
            raise Refusal("changed", f"{update['target_path']} changed after the update was proposed; propose "
                          "again from the current text.", "short-term")
        data = update["draft"].encode("utf-8")
        target = self.target(update)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "wb") as fh:
            fh.write(data)
        update["status"] = "applied"
        self.save(path, record)
        written = {"tier": "short-term", "path": update["target_path"], "version": None,
                   "fingerprint": fingerprint(data)}
        return update, written
