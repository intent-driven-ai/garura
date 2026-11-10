"""Build BI-8's intent draft from its page as it is now, with the nine Touches lines.

Run from the repo root. Reads the page and the approved pages' titles; writes intent-draft.json
in this write folder. Every part but the Touches block is taken from the page word for word.
"""
import json
import os
import re

HERE = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))
MODEL = ".garura/product/product-os"
PAGE = os.path.join(MODEL, "intents", "bi-8.md")
C = "software-delivery-planning/ship-every-change"

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

parts = [("capability", f"{C}/capability.md", "adds"),
         ("feature", "features/fn-731/feature.md", "changes"),
         ("feature", f"{C}/fn-commit-by-concern/feature.md", "adds"),
         ("feature", f"{C}/fn-raise-change/feature.md", "adds"),
         ("feature", "features/fn-673/feature.md", "changes"),
         ("feature", f"{C}/fn-land-plan-with-evidence/feature.md", "adds"),
         ("feature", f"{C}/fn-land-several-issues/feature.md", "adds"),
         ("feature", f"{C}/fn-scan-every-push/feature.md", "adds"),
         ("feature", f"{C}/fn-keep-docs-in-step/feature.md", "adds")]
touches = []
for kind, doc, mark in parts:
    head = open(os.path.join(MODEL, doc), encoding="utf-8").readline().rstrip("\n")
    prefix = "# Capability: " if kind == "capability" else "# Feature: "
    assert head.startswith(prefix), doc
    touches.append({"title": head[len(prefix):], "link": f"../{doc}", "kind": kind, "mark": mark})

draft = {"id": "bi-8", "issue": 8, "title": title, "outcome": one("Outcome"), "why": one("Why"),
         "asked_by": one("Asked by"), "proof": proof, "must_not": one("Must not"), "touches": touches}
with open(os.path.join(HERE, "intent-draft.json"), "w", encoding="utf-8") as f:
    json.dump(draft, f, indent=2, ensure_ascii=False)
    f.write("\n")
print(json.dumps(draft, indent=2, ensure_ascii=False))
