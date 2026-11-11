"""Build BI-9's intent draft from its page as it is now, with 6 Touches lines added for Give every gate a way past.

Run from the repo root. Reads the page and the approved drafts' titles; writes intent-draft.json in
this write folder. Every part but the Touches block is taken from the page word for word, and the 37
Touches lines already there are kept as they are, in their order, before the 6 new ones.
"""
import json
import os
import re

HERE = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))
MODEL = ".garura/product/product-os"
PAGE = os.path.join(MODEL, "intents", "bi-9.md")
C = "software-delivery-planning/give-every-gate-a-way-past"
DRAFTS = f".garura/project/issues/1021/context/bi-9-capability-5/drafts/product-os/{C}"
FEATURES = ["fn-way-past-every-gate", "fn-keep-what-is-owed", "fn-record-every-skip", "fn-guardrail-way-past",
            "fn-pinned-yes"]
TOUCH = re.compile(r"^- \[(.+)\]\((.+)\) \((capability|feature|domain)\) — (adds|changes|removes)$")

lines = open(PAGE, encoding="utf-8").read().split("\n")
assert lines[0].startswith("# ")
title = lines[0][2:]


def one(label):
    found = [l for l in lines if l.startswith(f"**{label}:** ")]
    assert len(found) == 1, label
    return found[0][len(f"**{label}:** "):]


i = lines.index("**Proof it is met:**")
proof = []
for l in lines[i + 1:]:
    if not l.startswith("- "):
        break
    proof.append(l[2:])
assert not any(l.startswith(("**Rules:**", "**Serves:**", "**Identified by:**")) for l in lines)

t = lines.index("**Touches:**")
touches = []
for l in lines[t + 1:]:
    if not l.startswith("- "):
        break
    m = TOUCH.match(l)
    assert m, l
    touches.append({"title": m.group(1), "link": m.group(2), "kind": m.group(3), "mark": m.group(4)})
assert len(touches) == 37, len(touches)

new = [("capability", "capability.md")] + [("feature", f"{fn}/feature.md") for fn in FEATURES]
for kind, rel in new:
    head = open(os.path.join(DRAFTS, rel), encoding="utf-8").readline().rstrip("\n")
    prefix = "# Capability: " if kind == "capability" else "# Feature: "
    assert head.startswith(prefix), rel
    touches.append({"title": head[len(prefix):], "link": f"../{C}/{rel}", "kind": kind, "mark": "adds"})
assert len(touches) == 43

draft = {"id": "bi-9", "issue": 9, "title": title, "outcome": one("Outcome"), "why": one("Why"),
         "asked_by": one("Asked by"), "proof": proof, "must_not": one("Must not"), "touches": touches}
with open(os.path.join(HERE, "intent-draft.json"), "w", encoding="utf-8") as f:
    json.dump(draft, f, indent=2, ensure_ascii=False)
    f.write("\n")
print(len(touches), "touches;", [x["title"] for x in touches[12:]])
