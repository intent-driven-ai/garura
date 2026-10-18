#!/usr/bin/env python3
"""
citations.py — decision records: every decision names the memory it came from (contract
version 4, ADR 035 §6).

cite records a decision in the issue's short-term memory — the question, the answer, who
decided, the play, and its sources (tier, file, lines, fingerprint) — after reading each source
to make sure it still says what the fingerprint says. citations lists an issue's records and,
with check, reads every source again: no source, a source that is gone, and a source whose text
changed are each a problem.

Records are kept one per line in <short-term root>/<issue>/<citations_file>. A lookup never
returns them: an agent never decides from its own earlier decision. Standard library only.
"""

import datetime
import hashlib
import json
import os
import re

from pull import Refusal

ID = re.compile(r"^cite-(\d{8})-(\d{3,})$")


def fingerprint(text):
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def lines_of(text, start, end):
    """The text of lines start..end (1-based, inclusive), or None when they are outside the file."""
    lines = text.split("\n")
    if lines and lines[-1] == "" and text.endswith("\n"):
        lines.pop()
    if start < 1 or end < start or end > len(lines):
        return None
    return "\n".join(lines[start - 1:end])


class CitationStore:
    def __init__(self, short_term_root, citations_file):
        self.root, self.file = short_term_root, citations_file.strip("/")

    def path(self, issue):
        return os.path.join(self.root, str(issue), self.file)

    def records(self, issue):
        path = self.path(issue)
        if not os.path.isfile(path):
            return []
        with open(path, encoding="utf-8") as fh:
            return [json.loads(line) for line in fh if line.strip()]

    def next_id(self):
        day = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d")
        taken = []
        for issue in os.listdir(self.root):
            if issue.isdigit():
                taken += [int(m.group(2)) for r in self.records(issue)
                          if (m := ID.match(str(r.get("citation_id", "")))) and m.group(1) == day]
        return f"cite-{day}-{max(taken, default=0) + 1:03d}"

    def source_problem(self, engine, source):
        """(None, text now) when the source still says what its fingerprint says;
        else (problem, detail, text now or None)."""
        text = engine.read(source["tier"], source["path"])
        where = f"{source['tier']} memory {source['path']} lines {source['start']}–{source['end']}"
        if text is None:
            return "source_missing", f"{where}: the file is not there.", None
        chunk = lines_of(text, source["start"], source["end"])
        if chunk is None:
            return "source_missing", f"{where}: those lines are not there.", None
        if fingerprint(chunk) != source["fingerprint"]:
            return "source_changed", f"{where} no longer say what the decision rested on.", chunk
        return None, None, chunk

    def cite(self, request, engine, updates):
        issue = request["issue"]
        cited = []
        for source in request["sources"]:
            if source["tier"] == "short-term" and not source["path"].startswith(f"{issue}/"):
                raise Refusal("bad_request", f"Short-term path {source['path']} is outside issue {issue}.",
                              "short-term")
            problem, detail, text = self.source_problem(engine, source)
            if problem:
                code = "not_found" if problem == "source_missing" else "changed"
                raise Refusal(code, detail + " Nothing was recorded.", source["tier"])
            # the exact text the agent read, and from which version of memory
            cited.append(source | {"text": text, "version": engine.version(source["tier"])})
        if request.get("from_update"):
            update = next((u for u in updates.list() if u["id"] == request["from_update"]), None)
            if update is None:
                raise Refusal("not_found", f"No memory update {request['from_update']}.", "short-term")
            if update["status"] != "applied":
                raise Refusal("not_approved", f"Memory update {update['id']} is {update['status']}: only an "
                              "applied update can be what a decision rests on.", "short-term")
            if not any(s["tier"] == "short-term" and s["path"] == update["target_path"] for s in request["sources"]):
                raise Refusal("bad_request", f"A decision from memory update {update['id']} names its written "
                              f"file, {update['target_path']}, as a source.", "short-term")
        record = {
            "citation_id": self.next_id(), "issue": issue, "play": request.get("play"),
            "question": request["question"], "answer": request["answer"], "decided_by": request["decided_by"],
            "decided_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "sources": cited, "from_update": request.get("from_update"),
        }
        path = self.path(issue)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        return record["citation_id"], {"tier": "short-term", "path": f"{issue}/{self.file}"}

    def citations(self, request, engine):
        records = [r for r in self.records(request["issue"])
                   if not request.get("play") or r.get("play") == request["play"]]
        problems = []
        if request.get("check"):
            for r in records:
                if not r.get("sources"):
                    problems.append({"citation_id": r["citation_id"], "problem": "no_source", "source": None,
                                     "detail": "The decision names no memory.", "now": None})
                for source in r.get("sources", []):
                    problem, detail, now = self.source_problem(engine, source)
                    if problem:
                        problems.append({"citation_id": r["citation_id"], "problem": problem, "source": source,
                                         "detail": detail, "now": now})
        return records, problems
