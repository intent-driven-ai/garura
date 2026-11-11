"""Build BI-9's intent draft from its page as it is now, with its first Touches list of 12 lines.

Run from the repo root. Reads the page and the part pages' titles; writes intent-draft.json in this
write folder. Every part but the Touches block is taken from the page word for word.
"""
import json
import os

HERE = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))
MODEL = ".garura/product/product-os"
PAGE = os.path.join(MODEL, "intents", "bi-9.md")
C = "software-delivery-planning/orchestrate-agent-work"

text = open(PAGE, encoding="utf-8").read()
lines = text.split("\n")
title = lines[0][2:]
assert lines[0].startswith("# ")


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

assert not any(l.startswith(("**Rules:**", "**Serves:**", "**Identified by:**", "**Touches:**")) for l in lines)

parts = [("capability", f"{C}/capability.md", "adds")]
parts += [("feature", f"{C}/{fn}/feature.md", "adds") for fn in
          ["fn-go-to-plan-branch", "fn-know-what-next", "fn-remove-plan",
           "fn-choose-next-item", "fn-work-out-waits-on", "fn-pause-plan"]]
parts += [("feature", f"{C}/fn-795/feature.md", "changes")]
parts += [("feature", f"features/{fn}/feature.md", "changes") for fn in ["fn-729", "fn-806", "fn-628", "fn-730"]]
touches = []
for kind, doc, mark in parts:
    head = open(os.path.join(MODEL, doc), encoding="utf-8").readline().rstrip("\n")
    prefix = "# Capability: " if kind == "capability" else "# Feature: "
    assert head.startswith(prefix), doc
    touches.append({"title": head[len(prefix):], "link": f"../{doc}", "kind": kind, "mark": mark})
assert len(touches) == 12

draft = {"id": "bi-9", "issue": 9, "title": title, "outcome": one("Outcome"), "why": one("Why"),
         "asked_by": one("Asked by"), "proof": proof, "must_not": one("Must not"), "touches": touches}
with open(os.path.join(HERE, "intent-draft.json"), "w", encoding="utf-8") as f:
    json.dump(draft, f, indent=2, ensure_ascii=False)
    f.write("\n")
print(json.dumps(draft, indent=2, ensure_ascii=False))
