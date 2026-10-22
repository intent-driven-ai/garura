#!/usr/bin/env python3
"""record_checkpoint.py — record the product owner's answer at an edit-ontology checkpoint (#777).

There are three checkpoints: questions, kinds, links. Each answer is kept in the history,
in order. A checkpoint is agreed when its latest answer is "yes". `all_agreed` is true only
when all three are agreed (C2/F2).

    python3 record_checkpoint.py --decisions <decisions.json> --point questions|kinds|links \
        --verdict yes|change --reply "<the person's exact words>" --draft <the draft that was shown>

Refuses (exit 2) an empty reply, or a draft file that does not exist — an answer is only
recorded for a draft the person was shown.
"""
import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

POINTS = ("questions", "kinds", "links")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--decisions", required=True)
    ap.add_argument("--point", required=True, choices=POINTS)
    ap.add_argument("--verdict", required=True, choices=("yes", "change"))
    ap.add_argument("--reply", required=True)
    ap.add_argument("--draft", required=True)
    ns = ap.parse_args(argv)
    if not ns.reply.strip():
        sys.stderr.write("record_checkpoint.py: the reply is empty — record only the person's own words\n")
        sys.exit(2)
    if not os.path.isfile(ns.draft):
        sys.stderr.write(f"record_checkpoint.py: no draft at {ns.draft} — show the draft before recording an answer\n")
        sys.exit(2)

    data = {"history": []}
    if os.path.isfile(ns.decisions):
        with open(ns.decisions, encoding="utf-8") as fh:
            data = json.load(fh)
    digest = hashlib.sha256(open(ns.draft, "rb").read()).hexdigest()
    data["history"].append({"point": ns.point, "verdict": ns.verdict, "reply": ns.reply,
                            "draft": ns.draft, "draft_sha256": digest,
                            "at": datetime.now(timezone.utc).isoformat(timespec="seconds")})
    latest = {}
    for entry in data["history"]:
        latest[entry["point"]] = entry["verdict"]
    data["agreed"] = {p: latest.get(p) == "yes" for p in POINTS}
    data["all_agreed"] = all(data["agreed"].values())
    with open(ns.decisions, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
    print(json.dumps({"point": ns.point, "verdict": ns.verdict, "all_agreed": data["all_agreed"]}))


if __name__ == "__main__":
    main()
