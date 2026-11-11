"""Build the approved-pages request and the link request for BI-9 capability 2.

Run from the repo root after make_thin_copies.py. Writes approved-request.json and link-request.json
in this write folder. The one-lines are the ones the product owner approved (plan.md).
"""
import json
import os

HERE = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))
ISSUE = ".garura/project/issues/1021/context/bi-9-capability-2"
C = "software-delivery-planning/run-plays-as-loops"
DRAFTS = f"{ISSUE}/drafts/product-os/{C}"
CAP = "cap-run-plays-as-loops"
BY = "product-os-keeper (reorganise business intents, #1021)"
FEATURES = ["fn-run-loop", "fn-check-loop-result", "fn-brief-open-points", "fn-show-run-status",
            "fn-loop-per-transition", "fn-start-loop-on-trigger", "fn-run-plays-side-by-side"]
THIN = {"fn-start-loop-on-trigger", "fn-run-plays-side-by-side"}
LINES = {
    CAP: "Run plays as loops: A person gives one goal, and a loop runs its plays until the goal is met.",
    "fn-run-loop": "Every loop takes the same steps: a check before anything opens, one change, questions first, its plays in rounds decided done, again or ask, then the checker and the landing.",
    "fn-check-loop-result": "A model or coding agent that did not run the loop judges every criterion from the loop's outputs only, and a reject halts the loop before any pull request.",
    "fn-brief-open-points": "When a round closes nothing new or the round limit is reached, the loop closes what it can, then briefs the person once with proposed answers; they reply or type stop.",
    "fn-show-run-status": "While a loop runs, one status file always says its state, round, play and step in plain words, so a person can see what a long run is doing.",
    "fn-loop-per-transition": "Each of the six transitions between phases has one loop of its own, named for the two phases it joins, that runs that transition's plays.",
    "fn-start-loop-on-trigger": "A loop is started by a person, a schedule or a hook, as the loop says, and keeps one record across rounds that tells the next round what was tried.",
    "fn-run-plays-side-by-side": "A round's plays run at the same time when all five conditions of the scoped-write rule hold, and in turn when they do not, with the same result.",
}

pages = [{"page": f"{C}/capability.md", "from": f"{DRAFTS}/capability.md"},
         {"page": f"{C}/ice.md", "from": f"{DRAFTS}/ice.md"}]
for fn in FEATURES:
    pages.append({"page": f"{C}/{fn}/feature.md", "from": f"{DRAFTS}/{fn}/feature.md"})
    src = f"{HERE}/approved/{fn}/ice.md" if fn in THIN else f"{DRAFTS}/{fn}/ice.md"
    pages.append({"page": f"{C}/{fn}/ice.md", "from": src})
for p in pages:
    assert os.path.isfile(p["from"]), p["from"]
approved = {"by": BY, "approved_by": "the product owner", "source": f"{ISSUE}/page-approvals.md",
            "pages": pages}

parts = [{"id": CAP, "kind": "capability", "mode": "new", "slug": "run-plays-as-loops",
          "domain": "dom-software-delivery-planning", "intents": ["bi-9"], "one_line": LINES[CAP],
          "doc": f"{C}/capability.md", "identified_by": ""}]
for fn in FEATURES:
    parts.append({"id": fn, "kind": "feature", "mode": "new", "slug": fn, "capability": CAP,
                  "intents": ["bi-9"], "one_line": LINES[fn], "doc": f"{C}/{fn}/feature.md",
                  "identified_by": ""})
parts.append({"id": "ice-run-plays-as-loops", "kind": "ice", "mode": "new", "for": CAP,
              "doc": f"{C}/ice.md", "thin": False})
for fn in FEATURES:
    parts.append({"id": "ice-" + fn[3:], "kind": "ice", "mode": "new", "for": fn,
                  "doc": f"{C}/{fn}/ice.md", "thin": fn in THIN})
link = {"by": BY + "; the write plan and one-lines approved by the product owner", "parts": parts}

for name, data in (("approved-request.json", approved), ("link-request.json", link)):
    with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
print(len(pages), "pages;", len(parts), "link parts")
