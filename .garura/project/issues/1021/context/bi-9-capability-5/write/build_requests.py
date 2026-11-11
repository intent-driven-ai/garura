"""Build the approved-pages request and the link request for BI-9 capability 5.

Run from the repo root after make_thin_copies.py. Writes approved-request.json and link-request.json
in this write folder. The one-lines are the ones the product owner approved (plan.md).
"""
import json
import os

HERE = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))
ISSUE = ".garura/project/issues/1021/context/bi-9-capability-5"
C = "software-delivery-planning/give-every-gate-a-way-past"
DRAFTS = f"{ISSUE}/drafts/product-os/{C}"
CAP = "cap-give-every-gate-a-way-past"
BY = "product-os-keeper (reorganise business intents, #1021)"
FEATURES = ["fn-way-past-every-gate", "fn-keep-what-is-owed", "fn-record-every-skip", "fn-guardrail-way-past",
            "fn-pinned-yes"]
THIN = {"fn-way-past-every-gate", "fn-keep-what-is-owed", "fn-record-every-skip", "fn-guardrail-way-past",
            "fn-pinned-yes"}
LINES = {
    CAP: "Give every gate a way past: No gate stops a person; each has a way past it, and using it records what is owed where a later play finds it.",
    "fn-way-past-every-gate": "Every gate a play declares names its kind, its way past and what using it records, and the person sees the way past at the gate.",
    "fn-keep-what-is-owed": "Each use of a way past writes one owed entry in the issue folder of the work that made it, and a tool reads every issue's entries back as one list.",
    "fn-record-every-skip": "A checkpoint the settings turn off writes one record in its issue's folder, naming the setting that skipped it, whatever the evidence setting says.",
    "fn-guardrail-way-past": "One list of the guardrails names, for each, the shortcut it guards, the play that owns that work and its way past, and each pass is recorded as owed.",
    "fn-pinned-yes": "One list names every pinned yes, such as the merge onto main, with why it is pinned, where it is asked and what happens to it inside a loop.",
}

pages = [{"page": f"{C}/capability.md", "from": f"{DRAFTS}/capability.md"},
         {"page": f"{C}/ice.md", "from": f"{HERE}/approved/ice.md"}]
for fn in FEATURES:
    pages.append({"page": f"{C}/{fn}/feature.md", "from": f"{DRAFTS}/{fn}/feature.md"})
    src = f"{HERE}/approved/{fn}/ice.md" if fn in THIN else f"{DRAFTS}/{fn}/ice.md"
    pages.append({"page": f"{C}/{fn}/ice.md", "from": src})
for p in pages:
    assert os.path.isfile(p["from"]), p["from"]
approved = {"by": BY, "approved_by": "the product owner", "source": f"{ISSUE}/page-approvals.md",
            "pages": pages}

parts = [{"id": CAP, "kind": "capability", "mode": "new", "slug": "give-every-gate-a-way-past",
          "domain": "dom-software-delivery-planning", "intents": ["bi-9"], "one_line": LINES[CAP],
          "doc": f"{C}/capability.md", "identified_by": ""}]
for fn in FEATURES:
    parts.append({"id": fn, "kind": "feature", "mode": "new", "slug": fn, "capability": CAP,
                  "intents": ["bi-9"], "one_line": LINES[fn], "doc": f"{C}/{fn}/feature.md",
                  "identified_by": ""})
parts.append({"id": "ice-give-every-gate-a-way-past", "kind": "ice", "mode": "new", "for": CAP,
              "doc": f"{C}/ice.md", "thin": True})
for fn in FEATURES:
    parts.append({"id": "ice-" + fn[3:], "kind": "ice", "mode": "new", "for": fn,
                  "doc": f"{C}/{fn}/ice.md", "thin": fn in THIN})
link = {"by": BY + "; the write plan and one-lines approved by the product owner", "parts": parts}

for name, data in (("approved-request.json", approved), ("link-request.json", link)):
    with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
print(len(pages), "pages;", len(parts), "link parts")
