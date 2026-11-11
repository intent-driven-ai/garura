"""Build the approved-pages request and the link request for BI-9 capability 3.

Run from the repo root after make_thin_copies.py. Writes approved-request.json and link-request.json
in this write folder. The one-lines are the ones the product owner approved (plan.md).
"""
import json
import os

HERE = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))
ISSUE = ".garura/project/issues/1021/context/bi-9-capability-3"
C = "software-delivery-planning/track-execution"
DRAFTS = f"{ISSUE}/drafts/product-os/{C}"
CAP = "cap-track-execution"
BY = "product-os-keeper (reorganise business intents, #1021)"
FEATURES = ["fn-mark-item-type", "fn-status-follows-issue", "fn-land-tracker-writes-once",
            "fn-see-issues-worth-attention", "fn-record-defect-under-story", "fn-one-tool-knows-tracker",
            "fn-link-work-across-trackers", "fn-say-what-each-type-means"]
THIN = {"fn-one-tool-knows-tracker", "fn-link-work-across-trackers", "fn-say-what-each-type-means"}
LINES = {
    CAP: "Track execution in the team's tracker: The product's execution is tracked in the tracker Garura connects to, for completion status and the backlog.",
    "fn-mark-item-type": "Every work item a play files or takes into a plan gets its kind's type and a parent of the right kind by a real link, with no label and no type in its title.",
    "fn-status-follows-issue": "When a work item's own issue closes, its item in the plan file reads Done or Dropped, and nothing is worked out from the items under it.",
    "fn-land-tracker-writes-once": "The tracker writes of an approved session are made one by one and recorded as made, so a run after a stop goes on from its record and never makes an issue twice.",
    "fn-see-issues-worth-attention": "One of three fixed modes cuts the work tracker's issues to at most ten, each with a reason, its kind and a play only where a fixed table names one.",
    "fn-record-defect-under-story": "A defect is recorded as an issue of type Bug under the story whose work brought it in, with its severity as its first line and a text that never names the test.",
    "fn-one-tool-knows-tracker": "One tool reads the settings and reaches the trackers they name, so no play, skill or sub-agent names a tracker, and a team changes its tracker by a setting.",
    "fn-link-work-across-trackers": "Each piece of work hangs under the business intent it serves by the tracker's own parent and child link, also when the intents live in another tracker.",
    "fn-say-what-each-type-means": "One agreed list gives each type Garura files its one-line meaning, its tracker and how it is marked, and Initialize's brief shows it word for word.",
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

parts = [{"id": CAP, "kind": "capability", "mode": "new", "slug": "track-execution",
          "domain": "dom-software-delivery-planning", "intents": ["bi-9"], "one_line": LINES[CAP],
          "doc": f"{C}/capability.md", "identified_by": ""}]
for fn in FEATURES:
    parts.append({"id": fn, "kind": "feature", "mode": "new", "slug": fn, "capability": CAP,
                  "intents": ["bi-9"], "one_line": LINES[fn], "doc": f"{C}/{fn}/feature.md",
                  "identified_by": ""})
parts.append({"id": "ice-track-execution", "kind": "ice", "mode": "new", "for": CAP,
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
