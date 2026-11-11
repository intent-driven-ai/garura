"""Build link-request-2.json for BI-9 capability 1 from the approved capability page as it is in the model.

Run from the repo root. Reads the capability page; writes link-request-2.json in this write folder.
The capability's one-line is the line under "## Directional intent", word for word. Each feature's
one-line is the text after "(<fn>): " on its line in the page's feature list, word for word, with
only its first letter made a capital.
"""
import json
import os

HERE = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))
MODEL = ".garura/product/product-os"
C = "software-delivery-planning/orchestrate-agent-work"
CAP = "cap-orchestrate-agent-work"
BY = "product-os-keeper (reorganise business intents, #1021)"

lines = open(os.path.join(MODEL, C, "capability.md"), encoding="utf-8").read().split("\n")
i = lines.index("## Directional intent")
cap_line = lines[i + 1]
assert cap_line.startswith("Orchestrate agent work through planning: ")


def one_line(fn):
    found = [l for l in lines if l.startswith("- ") and f" ({fn}): " in l]
    assert len(found) == 1, fn
    text = found[0].split(f" ({fn}): ", 1)[1]
    return text[0].upper() + text[1:]


NEW = ["fn-go-to-plan-branch", "fn-know-what-next", "fn-remove-plan",
       "fn-choose-next-item", "fn-work-out-waits-on", "fn-pause-plan"]
THIN = {"fn-choose-next-item", "fn-work-out-waits-on", "fn-pause-plan"}

parts = [{"id": CAP, "kind": "capability", "mode": "new", "slug": "orchestrate-agent-work",
          "domain": "dom-software-delivery-planning", "intents": ["bi-9"], "one_line": cap_line,
          "doc": f"{C}/capability.md", "identified_by": ""}]
for fn in NEW:
    parts.append({"id": fn, "kind": "feature", "mode": "new", "slug": fn, "capability": CAP,
                  "intents": ["bi-9"], "one_line": one_line(fn), "doc": f"{C}/{fn}/feature.md",
                  "identified_by": ""})
for fn in ["fn-729", "fn-806", "fn-628", "fn-730"]:
    parts.append({"id": fn, "kind": "feature", "mode": "update", "one_line": one_line(fn)})
parts.append({"id": "ice-795", "kind": "ice", "mode": "new", "for": "fn-795",
              "doc": "software-delivery-planning/shape-slice/fn-795/ice.md", "thin": False})
parts.append({"id": "fn-795", "kind": "feature", "mode": "update", "one_line": one_line("fn-795"),
              "capability": CAP, "doc": f"{C}/fn-795/feature.md"})
parts.append({"id": "fn-931", "kind": "feature", "mode": "update", "capability": "cap-turn-intents-into-work"})
parts.append({"id": "ice-orchestrate-agent-work", "kind": "ice", "mode": "new", "for": CAP,
              "doc": f"{C}/ice.md", "thin": False})
for fn in ["fn-729", "fn-806", "fn-628", "fn-730"]:
    parts.append({"id": "ice-" + fn[3:], "kind": "ice", "mode": "new", "for": fn,
                  "doc": f"features/{fn}/ice.md", "thin": False})
for fn in NEW:
    parts.append({"id": "ice-" + fn[3:], "kind": "ice", "mode": "new", "for": fn,
                  "doc": f"{C}/{fn}/ice.md", "thin": fn in THIN})

with open(os.path.join(HERE, "link-request-2.json"), "w", encoding="utf-8") as f:
    json.dump({"by": BY, "parts": parts}, f, indent=2, ensure_ascii=False)
    f.write("\n")
for p in parts:
    print(p["id"], p["mode"], p.get("thin", ""), "|", p.get("one_line", ""))
