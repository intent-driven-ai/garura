"""Build the approved-pages request and the link request for BI-9 capability 4.

Run from the repo root after make_thin_copies.py. Writes approved-request.json and link-request.json
in this write folder. The one-lines are the ones the product owner approved (plan.md).
"""
import json
import os

HERE = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))
ISSUE = ".garura/project/issues/1021/context/bi-9-capability-4"
C = "software-delivery-planning/manage-adrs"
DRAFTS = f"{ISSUE}/drafts/product-os/{C}"
CAP = "cap-manage-adrs"
BY = "product-os-keeper (reorganise business intents, #1021)"
FEATURES = ["fn-record-adr", "fn-accept-adr", "fn-keep-adrs-linked", "fn-show-accepter-findings",
            "fn-adr-in-its-change", "fn-keep-adrs-to-build", "fn-take-design-choices"]
THIN = {"fn-adr-in-its-change", "fn-keep-adrs-to-build", "fn-take-design-choices"}
LINES = {
    CAP: "Manage ADRs: Decisions on how the project is built are recorded closely as they're made, so agents can coordinate many pieces from them.",
    "fn-record-adr": "From a decision brief, a decision is drafted as an ADR from the one template, naming each older ADR it supersedes or amends with the part, and what it changes by real paths.",
    "fn-accept-adr": "An ADR becomes accepted only on a person's typed word: by hand at a pinned checkpoint, or later for an ADR a loop saved as proposed.",
    "fn-keep-adrs-linked": "Once an ADR is accepted, each older ADR it changes gains one forward pointer, its only edit, and the index of ADRs is rebuilt from the ADR folder.",
    "fn-show-accepter-findings": "Each point found while an ADR was drafted that the brief did not ask about is written with its five parts and shown to the person before they accept.",
    "fn-adr-in-its-change": "Run on the branch of a change that is already open, the decision play records the ADR in that change, so a decision lands with the work it decides.",
    "fn-keep-adrs-to-build": "Every ADR is reviewed, and what is about what the product model holds moves into the model, so ADRs hold only how the project is built.",
    "fn-take-design-choices": "Each design choice a person confirmed in Spec → Design reaches the decision play as a decision brief and is recorded as an ADR, and an update supersedes the older one.",
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

parts = [{"id": CAP, "kind": "capability", "mode": "new", "slug": "manage-adrs",
          "domain": "dom-software-delivery-planning", "intents": ["bi-9"], "one_line": LINES[CAP],
          "doc": f"{C}/capability.md", "identified_by": ""}]
for fn in FEATURES:
    parts.append({"id": fn, "kind": "feature", "mode": "new", "slug": fn, "capability": CAP,
                  "intents": ["bi-9"], "one_line": LINES[fn], "doc": f"{C}/{fn}/feature.md",
                  "identified_by": ""})
parts.append({"id": "ice-manage-adrs", "kind": "ice", "mode": "new", "for": CAP,
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
