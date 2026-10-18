#!/usr/bin/env python3
"""
citations.py — decision records: every decision names the memory it came from (contract
version 4, ADR 035 §6).

cite records a decision in the issue's short-term memory — the question, the answer, who
decided, the play, and its trace: the steps the agent took, in order, each with what it looked
for, what it found, and the memory lines that said so (tier, file, lines, fingerprint). It reads
each source first, to make sure it still says what the fingerprint says, and keeps the exact
text, the version and the lines around it. citations lists an issue's records and, with check,
reads every step's source again: no trace, a source that is gone, and a source whose text
changed are each a problem, named by its step.

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
TAKEN = re.compile(r'"citation_id":\s*"cite-(\d{8})-(\d{3,})"')
AROUND = 3  # lines kept before and after each source, so a person sees it in its place
TIER_NAMES = {"short-term": "Short-term memory", "garura": "Garura memory", "phoenix": "Phoenix memory"}


def fingerprint(text):
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def split_lines(text):
    lines = text.split("\n")
    if lines and lines[-1] == "" and text.endswith("\n"):
        lines.pop()
    return lines


def lines_of(text, start, end):
    """The text of lines start..end (1-based, inclusive), or None when they are outside the file."""
    lines = split_lines(text)
    if start < 1 or end < start or end > len(lines):
        return None
    return "\n".join(lines[start - 1:end])


def around(text, start, end):
    """Lines start..end with up to AROUND lines before and after, within the file."""
    lines = split_lines(text)
    first, last = max(1, start - AROUND), min(len(lines), end + AROUND)
    return {"start": first, "end": last, "text": "\n".join(lines[first - 1:last])}


class CitationStore:
    def __init__(self, short_term_root, citations_file):
        self.root, self.file = short_term_root, citations_file.strip("/")

    def path(self, issue):
        return os.path.join(self.root, str(issue), self.file)

    def records(self, issue):
        path = self.path(issue)
        if not os.path.isfile(path):
            return []
        found = []
        with open(path, encoding="utf-8") as fh:
            for n, line in enumerate(fh, 1):
                if not line.strip():
                    continue
                try:
                    found.append(json.loads(line))
                except ValueError:
                    raise Refusal("unreadable", f"Short-term memory {issue}/{self.file} line {n} is not a whole "
                                  "decision record (a write cut off, or a hand edit). Fix or remove that line.",
                                  "short-term") from None
        return found

    def next_id(self):
        """The next id of the day, across every issue. It reads only the ids, so one issue's
        unreadable line never stops a decision in another."""
        day = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d")
        taken = []
        for issue in os.listdir(self.root):
            path = self.path(issue)
            if issue.isdigit() and os.path.isfile(path):
                with open(path, encoding="utf-8") as fh:
                    taken += [int(n) for d, n in TAKEN.findall(fh.read()) if d == day]
        return f"cite-{day}-{max(taken, default=0) + 1:03d}"

    def source_problem(self, engine, source):
        """(None, None, text now, lines around now) when the source still says what its
        fingerprint says; else (problem, detail, text now or None, lines around now or None)."""
        text = engine.read(source["tier"], source["path"])
        one = source["start"] == source["end"]
        span = f"line {source['start']}" if one else f"lines {source['start']}–{source['end']}"
        where = f"{TIER_NAMES.get(source['tier'], source['tier'])} {source['path']} {span}"
        if text is None:
            return "source_missing", f"{where}: the file is not there.", None, None
        chunk = lines_of(text, source["start"], source["end"])
        if chunk is None:
            return "source_missing", f"{where}: {'that line is' if one else 'those lines are'} not there.", None, None
        near = around(text, source["start"], source["end"])
        if fingerprint(chunk) != source["fingerprint"]:
            return "source_changed", f"{where} no longer {'says' if one else 'say'} what the decision rested on.", chunk, near
        return None, None, chunk, near

    def cite(self, request, engine, updates):
        issue = request["issue"]
        self.records(issue)  # never append after an unreadable line
        trace = []
        for step in request["trace"]:
            source = step["source"]
            if source["tier"] == "short-term" and not source["path"].startswith(f"{issue}/"):
                raise Refusal("bad_request", f"Short-term path {source['path']} is outside issue {issue}.",
                              "short-term")
            problem, detail, text, near = self.source_problem(engine, source)
            if problem:
                code = "not_found" if problem == "source_missing" else "changed"
                raise Refusal(code, detail + " Nothing was recorded.", source["tier"])
            # the exact text the agent read, from which version of memory, and the lines around it
            trace.append({"asked": step["asked"], "found": step["found"],
                          "source": source | {"text": text, "version": engine.version(source["tier"]), "around": near}})
        if request.get("from_update"):
            update = next((u for u in updates.list() if u["id"] == request["from_update"]), None)
            if update is None:
                raise Refusal("not_found", f"No memory update {request['from_update']}.", "short-term")
            if update["status"] != "applied":
                raise Refusal("not_approved", f"Memory update {update['id']} is {update['status']}: only an "
                              "applied update can be what a decision rests on.", "short-term")
            if not any(st["source"]["tier"] == "short-term" and st["source"]["path"] == update["target_path"]
                       for st in request["trace"]):
                raise Refusal("bad_request", f"A decision from memory update {update['id']} names its written "
                              f"file, {update['target_path']}, as the source of a step.", "short-term")
        record = {
            "citation_id": self.next_id(), "issue": issue, "play": request.get("play"),
            "question": request["question"], "answer": request["answer"], "decided_by": request["decided_by"],
            "decided_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "trace": trace, "from_update": request.get("from_update"),
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
                if not r.get("trace"):
                    problems.append({"citation_id": r["citation_id"], "problem": "no_source", "step": None,
                                     "source": None, "detail": "The decision names no memory.", "now": None,
                                     "now_around": None})
                for n, step in enumerate(r.get("trace") or [], 1):
                    problem, detail, now, near = self.source_problem(engine, step["source"])
                    if problem:
                        problems.append({"citation_id": r["citation_id"], "problem": problem, "step": n,
                                         "source": step["source"], "detail": detail, "now": now, "now_around": near})
        return records, problems
