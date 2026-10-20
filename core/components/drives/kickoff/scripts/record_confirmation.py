#!/usr/bin/env python3
"""record_confirmation.py — keep the person's typed confirm or drop for each intent (C7).

Until the review tool (Argus) exists, Kickoff ends at the pull request: the person types
**confirm** or **drop** for each intent `/intent` saved as proposed, and the drive keeps their
exact words in the issue's short-term memory (Kapil, 2026-10-20, "2"). The drive never changes
an intent in the model: the intents stay `proposed` until Argus's review step writes the
approval (ADR 033, #650). This script writes the record and proves that:

- every intent `/intent` saved (its `intent-manifest.json`) has one decision, and no other;
- each decision is `confirm` or `drop`, with the person's own non-empty words;
- every intent page still reads `Stage: proposed` — the drive changed none (F7).

    python3 record_confirmation.py --manifest <intent run>/intent-manifest.json \
        --replies <working>/replies.json --by "<git user>" --at <date> \
        --out <working>/confirmation.yaml

`replies.json`: `{"<intent id>": "<the person's exact words>"}` — the words start with
`confirm` or `drop`. Exit 0 written; 2 refused — nothing written. Standard library only.
"""
import argparse
import json
import os
import re
import sys


class Refused(Exception):
    """Why the record cannot be written, in plain words."""


def decision_of(words):
    first = (words or "").strip().split(None, 1)
    head = first[0].lower().rstrip(".,:;!") if first else ""
    return {"confirm": "confirmed", "confirmed": "confirmed",
            "drop": "dropped", "dropped": "dropped"}.get(head)


def stage_of(path):
    with open(path, encoding="utf-8") as fh:
        m = re.search(r"(?m)^\*\*Stage:\*\*\s*(\w+)", fh.read())
    return m.group(1).lower() if m else None


def build(manifest, replies):
    intents = manifest.get("intents") or []
    if not intents:
        raise Refused("/intent saved no intents — there is nothing to decide")
    ids = [i["id"] for i in intents]
    stray = sorted(set(replies) - set(ids))
    if stray:
        raise Refused(f"replies name intents /intent did not save: {', '.join(stray)}")
    decisions = []
    for intent in intents:
        words = replies.get(intent["id"])
        if not (words and str(words).strip()):
            raise Refused(f"no reply from the person for {intent['id']}")
        decision = decision_of(str(words))
        if decision is None:
            raise Refused(f"the reply for {intent['id']} must start with confirm or drop")
        if os.path.isfile(intent["path"]) and stage_of(intent["path"]) != "proposed":
            raise Refused(f"{intent['id']}'s page no longer reads proposed — the drive must not "
                          f"change an intent's state (F7)")
        decisions.append({"intent": intent["id"], "decision": decision, "reply": str(words).strip()})
    return decisions


def as_yaml(by, at, decisions):
    q = json.dumps
    lines = ["by: person", f"confirmed_by: {q(by)}", f"at: {q(at)}",
             "applied_to_model: false   # Argus's review step writes the approval (#650)",
             "decisions:"]
    for d in decisions:
        lines += [f"  - intent: {q(d['intent'])}", f"    decision: {d['decision']}",
                  f"    reply: {q(d['reply'])}"]
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Record the person's decision on each intent.")
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--replies", required=True)
    ap.add_argument("--by", required=True)
    ap.add_argument("--at", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        with open(args.manifest, encoding="utf-8") as fh:
            manifest = json.load(fh)
        with open(args.replies, encoding="utf-8") as fh:
            replies = json.load(fh)
        if not isinstance(replies, dict):
            raise Refused("replies.json must map each intent id to the person's words")
        if not args.by.strip():
            raise Refused("the person's name is missing")
        decisions = build(manifest, replies)
    except (OSError, ValueError, KeyError, Refused) as why:
        msg = why if isinstance(why, Refused) else f"cannot read an input: {why.__class__.__name__}"
        sys.stderr.write(f"record_confirmation.py: {msg} — nothing written\n")
        return 2
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(as_yaml(args.by, args.at, decisions))
    print(json.dumps({"decisions": len(decisions),
                      "confirmed": sum(d["decision"] == "confirmed" for d in decisions)}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
