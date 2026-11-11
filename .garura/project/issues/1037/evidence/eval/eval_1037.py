#!/usr/bin/env python3
"""Acceptance check: the model's index tool clears a thin mark, moves a feature to another
capability, and moves a part's page (#1037).

Written before the build, so it fails until the three updates exist. Run from the repo root:

    python3 <this file>

E1  `thin: false` takes a part's thin mark off its index entry and its page together, and the
    part can then take an ICE of its own in the same request.
E2  `capability: <id>` files a feature under another capability that is in the index, or that the
    same request adds; it is refused for a capability not in the index, and on a capability.
E3  `doc: <new path>` moves a part's page and the ice.md beside it to the new folder, moves the
    ICE's index entry with it, removes the empty old folder, and keeps the spine's comment.
E4  The move is refused, and the model stays byte for byte as it was, when: the old folder holds
    another file; a page names the old path (written from the model's root, or as a link
    relative to the page); the new path is outside the part's allowed folders, already holds a
    file, or leaves the model. `thin: false` on a domain is refused too.
E5  What was there stays: an ICE for a part that still carries the thin mark is refused.
"""

import json
import os
import subprocess
import sys
import tempfile

import yaml

ROOT = os.getcwd()
INDEX_SCRIPT = os.path.join(ROOT, "core/components/skills/link-model-part/scripts/link_part.py")

SPINE = """\
# The spine: a comment that must stay.
domains:
- id: dom-work
  slug: work
  intents:
  - bi-1
  status: proposed
  detail: directional
  one_line: Getting work done
  doc: work/domain.md
capabilities:
- id: cap-1
  slug: cap-1
  domain: ''
  intents:
  - bi-1
  status: proposed
  one_line: Plan the work
  doc: capabilities/cap-1/capability.md
- id: cap-2
  slug: run-work
  domain: dom-work
  intents:
  - bi-1
  status: proposed
  one_line: Run the work
  doc: work/run-work/capability.md
features:
- id: fn-a
  slug: fn-a
  capability: cap-1
  intents:
  - bi-1
  status: proposed
  one_line: See every plan
  doc: capabilities/cap-1/fn-a/feature.md
  depends_on: []
  identified_by: ''
  metadata:
    thin: true
- id: fn-b
  slug: fn-b
  capability: cap-1
  intents:
  - bi-1
  status: proposed
  one_line: Pause a plan
  doc: features/fn-b/feature.md
  depends_on: []
  identified_by: ''
slices: []
"""

THIN = "Thin: proposed from the person's words; deepen with `/discover-capabilities`."

OLD_THIN_PAGE = f"""\
# Feature: See every plan

## What it does
Old words.

{THIN}

## Agent intent (ICE)
- Goal: See every plan.
"""

NEW_PAGE = """\
# Feature: See every plan

## What it does
Every plan as a card, from the plan files alone.

## Out of scope
- One plan as a tree. Another feature does it.
"""

ICE = """\
## Intent
- Goal: Anyone sees every plan at once.
- Limit: It reads only the plan files.
- Fails if: A plan is missing.

## Context
- Read: the plan files.
- Persona: the product owner.

## Expectation
- Scenario: Three plans show as three cards.
- Done means: Someone who did not build it counts three cards.
"""

results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))


class Model:
    def __init__(self, spine=SPINE):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = self.tmp.name + "/"
        self.root = os.path.join(self.base, "product-os")
        self.work = os.path.join(self.tmp.name, "work")
        os.makedirs(self.work)
        self.put("_spine.yaml", spine)
        self.put("intents/bi-1.md", "# People get their work done\n")
        self.put("work/domain.md", "# Theme: Getting work done\n")
        self.put("capabilities/cap-1/capability.md", "# Capability: Plan the work\n")
        self.put("work/run-work/capability.md", "# Capability: Run the work\n")
        self.put("capabilities/cap-1/fn-a/feature.md", OLD_THIN_PAGE)
        self.put("features/fn-b/feature.md", "# Feature: Pause a plan\n\n## What it does\nPause.\n")

    def put(self, rel, text):
        path = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)

    def read(self, rel):
        with open(os.path.join(self.root, rel), encoding="utf-8") as fh:
            return fh.read()

    def exists(self, rel):
        return os.path.exists(os.path.join(self.root, rel))

    def spine(self):
        return yaml.safe_load(self.read("_spine.yaml"))

    def entry(self, kind, pid):
        return next((e for e in self.spine().get(kind) or [] if e.get("id") == pid), {})

    def snapshot(self):
        out = {}
        for d, dirs, files in os.walk(self.root):
            for x in dirs:
                out[os.path.relpath(os.path.join(d, x), self.root) + "/"] = b""
            for f in files:
                p = os.path.join(d, f)
                with open(p, "rb") as fh:
                    out[os.path.relpath(p, self.root)] = fh.read()
        return out

    def run(self, parts):
        req = os.path.join(self.work, "request.json")
        out = os.path.join(self.work, "report.json")
        with open(req, "w", encoding="utf-8") as fh:
            json.dump({"by": "the acceptance check", "parts": parts}, fh)
        if os.path.exists(out):
            os.remove(out)
        p = subprocess.run([sys.executable, INDEX_SCRIPT, "--request", req, "--product-base", self.base,
                            "--out", out], capture_output=True, text=True)
        return p.returncode, p.stderr


def with_ice_a(m, page=NEW_PAGE):
    """fn-a with a page that has no Thin line, its ice.md beside it, no thin mark, and its ICE entry."""
    m.put("capabilities/cap-1/fn-a/feature.md", page)
    m.put("capabilities/cap-1/fn-a/ice.md", ICE)
    spine = SPINE.replace("  metadata:\n    thin: true\n", "")
    spine = spine.replace("slices: []\n", "slices: []\nices:\n- id: ice-a\n  for: fn-a\n  for_kind: feature\n"
                          "  doc: capabilities/cap-1/fn-a/ice.md\n")
    m.put("_spine.yaml", spine)


# E1: thin: false, then the part's ICE in the same request
m = Model()
m.put("capabilities/cap-1/fn-a/feature.md", NEW_PAGE)
m.put("capabilities/cap-1/fn-a/ice.md", ICE)
code, err = m.run([{"id": "fn-a", "kind": "feature", "mode": "update", "thin": False},
                   {"id": "ice-a", "kind": "ice", "mode": "new", "for": "fn-a",
                    "doc": "capabilities/cap-1/fn-a/ice.md"}])
check("E1 thin: false and the part's ICE are accepted together", code == 0, err.strip()[:200])
if code == 0:
    a = m.entry("features", "fn-a")
    check("E1 the entry carries no thin mark", not (a.get("metadata") or {}).get("thin"))
    check("E1 the entry keeps its other fields", a.get("capability") == "cap-1" and a.get("one_line") == "See every plan"
          and a.get("doc") == "capabilities/cap-1/fn-a/feature.md")
    check("E1 the ICE entry is there", any(e.get("id") == "ice-a" and e.get("for") == "fn-a"
                                         for e in m.spine().get("ices") or []))
    check("E1 the page is as written", m.read("capabilities/cap-1/fn-a/feature.md") == NEW_PAGE)

m = Model()
code, err = m.run([{"id": "fn-a", "kind": "feature", "mode": "update", "thin": False}])
check("E1 thin: false on a page that still holds its Thin line", code == 0, err.strip()[:200])
if code == 0:
    page = m.read("capabilities/cap-1/fn-a/feature.md")
    check("E1 the Thin line is gone from the page", THIN not in page and not any(
        ln.startswith("Thin:") for ln in page.splitlines()))
    check("E1 every other line of the page is kept",
          [ln for ln in page.splitlines() if ln.strip()] ==
          [ln for ln in OLD_THIN_PAGE.splitlines() if ln.strip() and ln != THIN])
    check("E1 the entry carries no thin mark", not (m.entry("features", "fn-a").get("metadata") or {}).get("thin"))

# E2: capability: <id>
m = Model()
code, err = m.run([{"id": "fn-b", "kind": "feature", "mode": "update", "capability": "cap-2"}])
check("E2 a feature is filed under another capability", code == 0 and m.entry("features", "fn-b").get("capability") == "cap-2",
      err.strip()[:200])
if code == 0:
    check("E2 its page does not move", m.entry("features", "fn-b").get("doc") == "features/fn-b/feature.md"
          and m.exists("features/fn-b/feature.md"))

m = Model()
m.put("work/new-cap/capability.md", "# Capability: A new one\n")
code, err = m.run([{"id": "cap-3", "kind": "capability", "mode": "new", "slug": "new-cap", "domain": "dom-work",
                    "intents": ["bi-1"], "one_line": "A new one", "doc": "work/new-cap/capability.md",
                    "identified_by": ""},
                   {"id": "fn-b", "kind": "feature", "mode": "update", "capability": "cap-3"}])
check("E2 a feature is filed under a capability the same request adds",
      code == 0 and m.entry("features", "fn-b").get("capability") == "cap-3", err.strip()[:200])

for why, part in {
    "a capability not in the index": {"id": "fn-b", "kind": "feature", "mode": "update", "capability": "cap-none"},
    "a capability key on a capability": {"id": "cap-1", "kind": "capability", "mode": "update", "capability": "cap-2"},
}.items():
    m = Model()
    before = m.snapshot()
    code, err = m.run([part])
    check(f"E2 refused: {why}", code == 2 and m.snapshot() == before, f"exit {code}: {err.strip()[:160]}")

# E3: doc: <new path>
m = Model()
with_ice_a(m)
code, err = m.run([{"id": "fn-a", "kind": "feature", "mode": "update", "capability": "cap-2",
                    "doc": "work/run-work/fn-a/feature.md"}])
check("E3 a feature's page moves with its new capability", code == 0, err.strip()[:200])
if code == 0:
    a = m.entry("features", "fn-a")
    ice = next((e for e in m.spine().get("ices") or [] if e.get("id") == "ice-a"), {})
    check("E3 the entry names the new page and capability", a.get("doc") == "work/run-work/fn-a/feature.md"
          and a.get("capability") == "cap-2")
    check("E3 the page moved word for word", m.exists("work/run-work/fn-a/feature.md")
          and m.read("work/run-work/fn-a/feature.md") == NEW_PAGE)
    check("E3 the ICE page moved beside it", m.exists("work/run-work/fn-a/ice.md")
          and m.read("work/run-work/fn-a/ice.md") == ICE)
    check("E3 the ICE entry names the moved page", ice.get("doc") == "work/run-work/fn-a/ice.md")
    check("E3 the old folder is gone", not m.exists("capabilities/cap-1/fn-a"))
    check("E3 the spine keeps its comment", m.read("_spine.yaml").startswith("# The spine: a comment that must stay."))

m = Model()
with_ice_a(m)
code, err = m.run([{"id": "fn-a", "kind": "feature", "mode": "update", "doc": "features/fn-a/feature.md"}])
check("E3 a feature's page moves to the holding folder", code == 0 and m.exists("features/fn-a/feature.md")
      and m.exists("features/fn-a/ice.md") and not m.exists("capabilities/cap-1/fn-a"), err.strip()[:200])

# E4: refusals, nothing changes
def refusal(why, setup, part):
    m = Model()
    with_ice_a(m)
    setup(m)
    before = m.snapshot()
    code, err = m.run([part])
    check(f"E4 refused: {why}", code == 2 and m.snapshot() == before, f"exit {code}: {err.strip()[:160]}")


MOVE = {"id": "fn-a", "kind": "feature", "mode": "update", "doc": "features/fn-a/feature.md"}
refusal("the old folder holds another file", lambda m: m.put("capabilities/cap-1/fn-a/notes.md", "notes\n"), MOVE)
refusal("a page names the old path from the model's root",
        lambda m: m.put("intents/bi-1.md", "# People get their work done\n\n- [See every plan]"
                                           "(../capabilities/cap-1/fn-a/feature.md) (feature) — adds\n"), MOVE)
refusal("a page links to the old path relative to itself",
        lambda m: m.put("capabilities/cap-1/capability.md", "# Capability: Plan the work\n\n"
                                                             "- [See every plan](fn-a/feature.md)\n"), MOVE)
refusal("the new path is outside the part's allowed folders", lambda m: None,
        dict(MOVE, doc="elsewhere/fn-a/feature.md"))
refusal("the new path already holds a file", lambda m: m.put("features/fn-a/feature.md", "# Feature: Taken\n"), MOVE)
refusal("the new path leaves the model", lambda m: None, dict(MOVE, doc="../outside/fn-a/feature.md"))

m = Model()
before = m.snapshot()
code, err = m.run([{"id": "dom-work", "kind": "domain", "mode": "update", "thin": False}])
check("E4 refused: thin: false on a domain", code == 2 and m.snapshot() == before, f"exit {code}: {err.strip()[:160]}")

# E5: an ICE for a part that still carries the thin mark is refused
m = Model()
m.put("capabilities/cap-1/fn-a/ice.md", ICE)
before = m.snapshot()
code, err = m.run([{"id": "ice-a", "kind": "ice", "mode": "new", "for": "fn-a",
                    "doc": "capabilities/cap-1/fn-a/ice.md"}])
check("E5 refused: an ICE for a part still marked thin", code == 2 and m.snapshot() == before,
      f"exit {code}: {err.strip()[:160]}")

failed = [r for r in results if not r[1]]
for name, ok, detail in results:
    print(("PASS " if ok else "FAIL ") + name + (f"  ({detail})" if detail and not ok else ""))
print(f"\n{len(results) - len(failed)} of {len(results)} checks pass")
sys.exit(1 if failed else 0)
