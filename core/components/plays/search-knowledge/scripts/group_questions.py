#!/usr/bin/env python3
"""group_questions.py — merge a loop's open questions into what is actually being asked (/search-knowledge).

A loop's round can leave dozens of open questions that are a few questions asked again: the
same business proof once per intent and once per play, the same speed target once per
capability (#613: 82 questions, the proof asked 15 times, speed 11, who may approve 8). This
script gathers every open question of the round and makes a first, mechanical grouping; the
knowledge-builder agent then confirms, splits or joins groups by judgment.

Sources (the loop contract's places, ADR 039 — all in the issue's short-term memory):
  <review_dir>/open-<play>.json        {"play", "questions": [{"id", "ask", "about", ...}]}
  the issue's memory updates still `waiting` — asked of the memory tool (`updates`), never read
  from their files

Grouping: a question's **topic** is the first topic rule its words match (speed, proof,
compliance, who may act, …); questions with the same topic form one group. A question no rule
matches is grouped with others whose words overlap enough (Jaccard ≥ 0.5 on its content
words), else it stands alone.

    python3 group_questions.py --review-dir <review_dir> --issue <issue> \
        --memory-tool .garura/core/tools/memory/memory.py --out <working>/question-groups.json

Writes `{"questions": n, "groups": [{"id", "topic", "members": [ids], "asks": [...],
"about": [...], "from": [plays]}]}`. Exit 0 written; 2 an input cannot be read. Standard
library only.
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys

WAITING = ("waiting", "pending")
# topic rules: the first that matches a question's words names its topic (order matters)
TOPICS = [
    ("proof", r"\b(how will (you|we) know|proof|measure of success|is it met|works for the business|benefit)\b"),
    ("speed", r"\b(how (fast|quickly)|speed|latency|respond(s)? within|performance|seconds?)\b"),
    ("compliance", r"\b(gdpr|soc ?2|hipaa|compliance|regime|regulat\w*|retention|legal)\b"),
    ("who-may-act", r"\b(who may|who can|permission\w*|identity|identified|sign[- ]?in|roles?|allowed to)\b"),
    ("who-asks", r"\b(who (asks|wants|is asking)|asked by|requested by)\b"),
    ("why", r"\b(why does it matter|why it matters|matter to the business)\b"),
    ("placement", r"\b(knowledge base|which (area|domain)|live under|own area|domain it sits)\b"),
    ("visibility", r"\b(who (may|can) see|visible to|hidden from)\b"),
    ("concurrency", r"\b(second person|same time|at once|while the first|two people)\b"),
    ("undo", r"\b(reopen|undo|change (a|an|the) .{0,20}after|revert)\b"),
]
STOP = set("a an the of to and or for in on at is are be by it its this that what which when how "
           "who whom do does did with as from can may must should would will there their them "
           "they you your we our i not no so if into than then any each".split())


def topic_of(text):
    low = text.lower()
    for name, pattern in TOPICS:
        if re.search(pattern, low):
            return name
    return None


def words(text):
    return {w for w in re.findall(r"[a-z][a-z'-]+", text.lower()) if w not in STOP and len(w) > 2}


def waiting_updates(tool, issue):
    """The issue's memory updates still waiting, from the memory tool (`updates`)."""
    out = subprocess.run([sys.executable, tool, "updates", "--status", "waiting"],
                         capture_output=True, text=True, check=False)
    answer = json.loads(out.stdout.strip().splitlines()[-1]) if out.stdout.strip() else {}
    if not answer.get("ok"):
        raise ValueError(f"memory tool: {answer.get('message') or out.stderr.strip() or 'no answer'}")
    return [u for u in answer.get("updates") or [] if str(u.get("issue")) == str(issue)]


def gather(review_dir, updates):
    qs = []
    for path in sorted(glob.glob(os.path.join(review_dir, "open-*.json"))):
        with open(path, encoding="utf-8") as fh:
            doc = json.load(fh)
        play = doc.get("play") or os.path.basename(path)[5:-5]
        for q in doc.get("questions") or []:
            qs.append({"id": str(q.get("id")), "ask": str(q.get("ask") or ""),
                       "about": str(q.get("about") or ""), "from": play})
    for mu in updates:
        if str(mu.get("status", "waiting")).lower() in WAITING:
            qs.append({"id": str(mu.get("id")), "ask": str(mu.get("missing") or ""),
                       "about": "memory update", "from": "memory-update"})
    return qs


def group(qs):
    groups = {}
    loose = []
    for q in qs:
        t = topic_of(q["ask"])
        if t:
            groups.setdefault(t, []).append(q)
        else:
            loose.append(q)
    clusters = []
    for q in loose:
        w = words(q["ask"])
        for c in clusters:
            cw = c["words"]
            if w and cw and len(w & cw) / len(w | cw) >= 0.5:
                c["members"].append(q)
                c["words"] |= w
                break
        else:
            clusters.append({"members": [q], "words": set(w)})
    out = []
    for t, members in groups.items():
        out.append((t, members))
    for n, c in enumerate(clusters, 1):
        out.append((None, c["members"]))
    result = []
    for n, (t, members) in enumerate(out, 1):
        result.append({"id": f"g{n:02d}", "topic": t or "other",
                       "members": [m["id"] for m in members],
                       "asks": [m["ask"] for m in members],
                       "about": sorted({m["about"] for m in members if m["about"]}),
                       "from": sorted({m["from"] for m in members})})
    result.sort(key=lambda g: (-len(g["members"]), g["id"]))
    return result


def main(argv=None):
    ap = argparse.ArgumentParser(description="Group a loop's open questions.")
    ap.add_argument("--review-dir", required=True)
    ap.add_argument("--issue", required=True)
    ap.add_argument("--memory-tool", default=".garura/core/tools/memory/memory.py")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        qs = gather(args.review_dir, waiting_updates(args.memory_tool, args.issue))
    except (OSError, ValueError) as exc:
        sys.stderr.write(f"group_questions.py: cannot read an input: {exc}\n")
        return 2
    groups = group(qs)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump({"questions": len(qs), "groups": groups}, fh, indent=2)
    print(json.dumps({"questions": len(qs), "groups": len(groups),
                      "largest": [(g["topic"], len(g["members"])) for g in groups[:6]]}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
