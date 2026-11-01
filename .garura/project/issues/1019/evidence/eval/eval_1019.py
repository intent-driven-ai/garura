#!/usr/bin/env python3
"""Acceptance check for #1019: three skills let an approved reorganisation run.

Black box: it runs each skill's script on a throwaway model and reads what changed on disk.
It reads none of the skills' code. Run from the repo root; prints one JSON result and exits 1
when any check fails. The builder never reads this folder.
"""

import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile

import yaml

ROOT = os.getcwd()
SKILLS = os.path.join(ROOT, "core", "components", "skills")
REMOVE_PART = os.path.join(SKILLS, "remove-model-part", "scripts", "remove_part.py")
WRITE_PAGE = os.path.join(SKILLS, "author-intent-page", "scripts", "write_page.py")
REMOVE_PLANS = os.path.join(SKILLS, "remove-plan", "scripts", "remove_plans.py")
results = []


def check(name, ok, detail=""):
    results.append({"check": name, "ok": bool(ok), "detail": str(detail)[:400]})


def run(script, *args):
    if not os.path.isfile(script):
        return subprocess.CompletedProcess(args, 127, "", f"no script {script}")
    return subprocess.run([sys.executable, script, *args], capture_output=True, text=True, timeout=60)


SPINE = """\
# a comment that must stay
domains:
- id: dom-a
  slug: a
  intents:
  - bi-1
  - bi-2
  status: proposed
  one_line: Domain A
  doc: a/domain.md
capabilities:
- id: cap-1
  slug: cap-1
  domain: dom-a
  intents:
  - bi-1
  status: proposed
  one_line: Keeper
  doc: a/cap-1/capability.md
  depends_on: []
  identified_by: ''
  issue: 10
- id: cap-2
  slug: cap-2
  domain: ''
  intents:
  - bi-1
  status: proposed
  one_line: Merged away
  doc: capabilities/cap-2/capability.md
  depends_on: []
  identified_by: cap-1
  issue: 20
- id: cap-3
  slug: cap-3
  domain: ''
  intents:
  - bi-2
  status: proposed
  one_line: Stays
  doc: capabilities/cap-3/capability.md
  depends_on:
  - cap-2
  identified_by: cap-2
  issue: 30
features:
- id: fn-1
  slug: fn-1
  capability: cap-2
  intents:
  - bi-1
  status: proposed
  one_line: Moves with the merge
  doc: features/fn-1/feature.md
  depends_on: []
  identified_by: ''
  issue: 11
- id: fn-2
  slug: fn-2
  capability: cap-3
  intents:
  - bi-2
  status: proposed
  one_line: Repointed
  doc: features/fn-2/feature.md
  depends_on: []
  identified_by: ''
  issue: 12
slices:
- id: sl-1
  slug: one
  feature_refs:
  - fn-2
  vertical: a screen
  intents:
  - bi-2
  record: slices/sl-1.yaml
"""

PAGES = {
    "intents/bi-1.md": "# One\n\n**Stage:** confirmed\n**Tracker:** #1\n",
    "intents/bi-2.md": "# Two\n\n**Stage:** confirmed\n**Tracker:** #2\n",
    "intents/bi-3.md": "# Three\n\n**Stage:** confirmed\n**Tracker:** #3\n",
    "a/domain.md": "# Domain A\n",
    "a/cap-1/capability.md": "# Capability: Keeper\n",
    "capabilities/cap-2/capability.md": "# Capability: Merged away\n",
    "capabilities/cap-3/capability.md": "# Capability: Stays\n",
    "features/fn-1/feature.md": "# Feature: one\n",
    "features/fn-2/feature.md": "# Feature: two\n",
    "slices/sl-1.yaml": "slice:\n  id: sl-1\n",
}


def model():
    base = tempfile.mkdtemp(prefix="eval1019-")
    root = os.path.join(base, "product-os")
    for rel, text in PAGES.items():
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
    with open(os.path.join(root, "_spine.yaml"), "w", encoding="utf-8") as fh:
        fh.write(SPINE)
    return base


def snapshot(folder):
    out = {}
    for d, _, files in os.walk(folder):
        for f in files:
            p = os.path.join(d, f)
            if os.access(p, os.R_OK):
                with open(p, "rb") as fh:
                    out[os.path.relpath(p, folder)] = fh.read()
            else:
                out[os.path.relpath(p, folder)] = None
    return out


def remove_part(base, request):
    req = os.path.join(base, "req.json")
    out = os.path.join(base, "report.json")
    with open(req, "w", encoding="utf-8") as fh:
        json.dump(request, fh)
    if os.path.exists(out):
        os.remove(out)
    return run(REMOVE_PART, "--request", req, "--product-base", base, "--out", out)


def spine_of(base):
    with open(os.path.join(base, "product-os", "_spine.yaml"), encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def by_id(entries):
    return {e["id"]: e for e in entries}


def check_refusal(name, request, must_name=None, setup=None):
    base = model()
    if setup:
        setup(base)
    before = snapshot(os.path.join(base, "product-os"))
    r = remove_part(base, request)
    after = snapshot(os.path.join(base, "product-os"))
    check(f"{name}: refused with exit 2", r.returncode == 2, f"exit {r.returncode}: {r.stderr[-200:]}")
    check(f"{name}: every file left as it was", before == after)
    if must_name:
        check(f"{name}: the refusal names {must_name}", must_name in (r.stderr + r.stdout), r.stderr[-300:])
    shutil.rmtree(base)


APPROVED = {"by": "eval", "approved_by": "the product owner"}

# --- remove-model-part: repoint, then remove an intent
base = model()
r = remove_part(base, {**APPROVED,
                       "repoint": [{"id": "dom-a", "kind": "domain", "intents": {"bi-2": "bi-3"}},
                                   {"id": "cap-3", "kind": "capability", "intents": {"bi-2": "bi-3"}},
                                   {"id": "fn-2", "kind": "feature", "intents": {"bi-2": "bi-3"}},
                                   {"id": "sl-1", "kind": "slice", "intents": {"bi-2": "bi-3"}}],
                       "remove": [{"kind": "intent", "id": "bi-2"}]})
check("remove intent: runs", r.returncode == 0, r.stderr[-300:])
s = spine_of(base) if r.returncode == 0 else {"domains": [], "capabilities": [], "features": [], "slices": []}
check("remove intent: its page is gone", not os.path.exists(os.path.join(base, "product-os/intents/bi-2.md")))
check("remove intent: other intent pages stay", os.path.exists(os.path.join(base, "product-os/intents/bi-1.md")))
check("repoint: in place and in order", by_id(s["domains"]).get("dom-a", {}).get("intents") == ["bi-1", "bi-3"],
      by_id(s["domains"]).get("dom-a"))
check("repoint: capability, feature and slice follow",
      by_id(s["capabilities"]).get("cap-3", {}).get("intents") == ["bi-3"]
      and by_id(s["features"]).get("fn-2", {}).get("intents") == ["bi-3"]
      and by_id(s["slices"]).get("sl-1", {}).get("intents") == ["bi-3"])
with open(os.path.join(base, "product-os/_spine.yaml"), encoding="utf-8") as fh:
    check("the spine keeps its comments", "# a comment that must stay" in fh.read())
check("the report is written", os.path.isfile(os.path.join(base, "report.json")))
shutil.rmtree(base)

# --- remove-model-part: two parts that shared an intent can go different ways
base = model()
r = remove_part(base, {**APPROVED,
                       "repoint": [{"id": "cap-1", "kind": "capability", "intents": {"bi-1": "bi-2"}},
                                   {"id": "cap-2", "kind": "capability", "intents": {"bi-1": "bi-3"}},
                                   {"id": "fn-1", "kind": "feature", "intents": {"bi-1": "bi-3"}},
                                   {"id": "dom-a", "kind": "domain", "intents": {"bi-1": None}}],
                       "remove": [{"kind": "intent", "id": "bi-1"}]})
s = spine_of(base) if r.returncode == 0 else None
check("repoint: per part, and null drops the intent",
      r.returncode == 0 and by_id(s["capabilities"])["cap-1"]["intents"] == ["bi-2"]
      and by_id(s["capabilities"])["cap-2"]["intents"] == ["bi-3"]
      and by_id(s["domains"])["dom-a"]["intents"] == ["bi-2"], r.stderr[-300:])
shutil.rmtree(base)

# --- remove-model-part: merge a capability
base = model()
r = remove_part(base, {**APPROVED, "remove": [{"kind": "capability", "id": "cap-2", "into": "cap-1"}]})
check("merge: runs", r.returncode == 0, r.stderr[-300:])
s = spine_of(base) if r.returncode == 0 else {"capabilities": [], "features": []}
caps = by_id(s["capabilities"])
check("merge: the capability is gone from the spine", "cap-2" not in caps and "cap-1" in caps)
check("merge: its page and empty folder are gone", not os.path.exists(os.path.join(base, "product-os/capabilities/cap-2")))
check("merge: its features move to the survivor", by_id(s["features"]).get("fn-1", {}).get("capability") == "cap-1")
check("merge: links to it follow",
      caps.get("cap-3", {}).get("identified_by") == "cap-1" and caps.get("cap-3", {}).get("depends_on") == ["cap-1"],
      caps.get("cap-3"))
check("merge: its issue number stays on record", "20" in json.dumps(caps.get("cap-1", {}).get("metadata", {})),
      caps.get("cap-1"))
shutil.rmtree(base)

# --- remove-model-part: remove a slice
base = model()
r = remove_part(base, {**APPROVED, "remove": [{"kind": "slice", "id": "sl-1"}]})
s = spine_of(base) if r.returncode == 0 else {"slices": [1]}
check("slice: entry and record are gone",
      r.returncode == 0 and s["slices"] == [] and not os.path.exists(os.path.join(base, "product-os/slices/sl-1.yaml")),
      r.stderr[-300:])
shutil.rmtree(base)

# --- remove-model-part: refusals


def mention(base):
    with open(os.path.join(base, "product-os/features/fn-2/feature.md"), "a", encoding="utf-8") as fh:
        fh.write("Written for bi-3 on the way.\n")


check_refusal("no approval", {"by": "eval", "remove": [{"kind": "slice", "id": "sl-1"}]})
check_refusal("intent still named", {**APPROVED, "remove": [{"kind": "intent", "id": "bi-1"}]}, must_name="cap-1")
check_refusal("a page still mentions it", {**APPROVED, "remove": [{"kind": "intent", "id": "bi-3"}]},
              must_name="fn-2/feature.md", setup=mention)
check_refusal("repoint to an intent with no page",
              {**APPROVED, "repoint": [{"id": "cap-3", "kind": "capability", "intents": {"bi-2": "bi-9"}}]},
              must_name="bi-9")
check_refusal("repoint a part that does not name the intent",
              {**APPROVED, "repoint": [{"id": "cap-3", "kind": "capability", "intents": {"bi-1": "bi-3"}}]})
check_refusal("merge into itself", {**APPROVED, "remove": [{"kind": "capability", "id": "cap-2", "into": "cap-2"}]})
check_refusal("merge with no survivor", {**APPROVED, "remove": [{"kind": "capability", "id": "cap-2"}]})
check_refusal("merge into a missing part", {**APPROVED, "remove": [{"kind": "capability", "id": "cap-2", "into": "cap-9"}]})
check_refusal("one bad item refuses all",
              {**APPROVED, "remove": [{"kind": "slice", "id": "sl-1"}, {"kind": "slice", "id": "sl-9"}]})
check_refusal("a path that leaves the model",
              {**APPROVED, "remove": [{"kind": "intent", "id": "../../secret"}]})

# --- author-intent-page
DRAFT = {"id": "bi-40", "issue": 40, "title": "People get the thing", "outcome": "They get it.",
         "why": "They need it.", "asked_by": "the product owner", "proof": ["They got it."],
         "must_not": "Break it."}


def write_page(base, draft, *flags):
    path = os.path.join(base, "draft.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(draft, fh)
    return run(WRITE_PAGE, "--draft", path, "--product-base", base, "--date", "2026-11-02",
               "--out", os.path.join(base, "page.json"), *flags)


base = model()
page = os.path.join(base, "product-os/intents/bi-40.md")
r = write_page(base, DRAFT)
check("page: a new page is written", r.returncode == 0 and os.path.isfile(page), r.stderr[-300:])
text = open(page, encoding="utf-8").read() if os.path.isfile(page) else ""
for part in ("# People get the thing", "**Outcome:** They get it.", "**Why:** They need it.",
             "**Asked by:** the product owner", "They got it.", "**Must not:** Break it.",
             "**Stage:** proposed", "**Tracker:** #40"):
    check(f"page: holds {part}", part in text, text[:200])
before = snapshot(os.path.join(base, "product-os"))
r = write_page(base, dict(DRAFT, title="Other"))
check("page: never overwrites without rewrite", r.returncode == 2 and before == snapshot(os.path.join(base, "product-os")),
      r.returncode)
with open(page, "a", encoding="utf-8") as fh:
    fh.write("\n**Touches:**\n- [Keeper](../a/cap-1/capability.md) (capability) — adds\n\n**What was done:** shipped it\n")
r = write_page(base, dict(DRAFT, title="New words", outcome="New outcome."), "--rewrite", "--stage", "confirmed",
               "--confirmed-by", "the product owner")
text = open(page, encoding="utf-8").read()
check("page: rewrite changes the words", r.returncode == 0 and "# New words" in text and "New outcome." in text
      and "They get it." not in text, r.stderr[-300:])
check("page: rewrite keeps Touches and what was done",
      "- [Keeper](../a/cap-1/capability.md) (capability) — adds" in text and "shipped it" in text)
check("page: confirmed names who and when", "**Stage:** confirmed — by the product owner, 2026-11-02" in text, text[-300:])
before = snapshot(os.path.join(base, "product-os"))
for name, draft, flags in (
        ("no proof", dict(DRAFT, id="bi-41", issue=41, proof=[]), []),
        ("no why", dict(DRAFT, id="bi-41", issue=41, why=""), []),
        ("id does not match issue", dict(DRAFT, id="bi-41", issue=42), []),
        ("id leaves the folder", dict(DRAFT, id="../bi-41", issue=41), []),
        ("rewrite of a page that is not there", dict(DRAFT, id="bi-41", issue=41), ["--rewrite"]),
        ("confirmed with no person", dict(DRAFT, id="bi-41", issue=41), ["--stage", "confirmed"])):
    r = write_page(base, draft, *flags)
    check(f"page refused: {name}", r.returncode == 2 and before == snapshot(os.path.join(base, "product-os")),
          f"exit {r.returncode}")
shutil.rmtree(base)

# --- remove-plan


def plans():
    base = tempfile.mkdtemp(prefix="eval1019plans-")
    d = os.path.join(base, "plans")
    os.makedirs(os.path.join(d, "2", "evals", "sl"))
    secret = os.path.join(d, "2", "evals", "sl", "eval.md")
    with open(secret, "w", encoding="utf-8") as fh:
        fh.write("hidden\n")
    os.chmod(secret, 0)
    plan = {
        "1": {"id": 1, "title": "One", "status": "Paused", "branch": None, "needs_plans": [2],
              "tree": [{"issue": 5, "kind": "epic", "title": "E", "status": "Done", "children": []}]},
        "2": {"id": 2, "title": "Two", "status": "Paused", "branch": None, "needs_plans": [],
              "tree": [{"issue": 6, "kind": "epic", "title": "E", "status": "In Progress", "children": [
                  {"issue": 7, "kind": "story", "title": "S", "status": "Done"}]}]},
        "3": {"id": 3, "title": "Three", "status": "In Progress", "branch": "plan/3/base", "needs_plans": [],
              "tree": []},
    }
    for pid, data in plan.items():
        with open(os.path.join(d, f"{pid}.yaml"), "w", encoding="utf-8") as fh:
            yaml.safe_dump(data, fh)
    return base, d


def remove_plans(base, d, request):
    req = os.path.join(base, "req.json")
    with open(req, "w", encoding="utf-8") as fh:
        json.dump(request, fh)
    return run(REMOVE_PLANS, "--request", req, "--plans-dir", d, "--out", os.path.join(base, "report.json"))


base, d = plans()
r = remove_plans(base, d, {**APPROVED, "plans": [1, 2]})
check("plans: removes the files and the folder",
      r.returncode == 0 and not os.path.exists(os.path.join(d, "1.yaml")) and not os.path.exists(os.path.join(d, "2.yaml"))
      and not os.path.exists(os.path.join(d, "2")), r.stderr[-300:])
check("plans: leaves the others", os.path.exists(os.path.join(d, "3.yaml")))
rep = {}
if os.path.isfile(os.path.join(base, "report.json")):
    rep = json.load(open(os.path.join(base, "report.json"), encoding="utf-8"))
check("plans: the report counts what left", '"Done"' in json.dumps(rep) and "1" in json.dumps(rep), rep)
check("plans: works without being able to read the evals folder's files", r.returncode == 0)
shutil.rmtree(base, ignore_errors=True)

for name, request, must in (
        ("no approval", {"by": "eval", "plans": [1]}, None),
        ("a plan on a live branch", {**APPROVED, "plans": [3]}, "plan/3/base"),
        ("a plan another remaining plan needs", {**APPROVED, "plans": [2]}, "1"),
        ("one bad plan refuses all", {**APPROVED, "plans": [1, 2, 9]}, "9"),
        ("a path that leaves the folder", {**APPROVED, "plans": ["../x"]}, None)):
    base, d = plans()
    before = snapshot(d)
    r = remove_plans(base, d, request)
    check(f"plans refused: {name}", r.returncode == 2 and before == snapshot(d), f"exit {r.returncode}")
    if must:
        check(f"plans refused: {name} names {must}", must in r.stderr + r.stdout, r.stderr[-200:])
    os.chmod(os.path.join(d, "2", "evals", "sl", "eval.md"), stat.S_IRUSR | stat.S_IWUSR)
    shutil.rmtree(base, ignore_errors=True)

# --- the skills are wired in
for skill in ("remove-model-part", "author-intent-page", "remove-plan"):
    check(f"{skill}: has its SKILL.md", os.path.isfile(os.path.join(SKILLS, skill, "SKILL.md")))
    tests = os.path.join(SKILLS, skill, "scripts")
    has = os.path.isdir(tests) and any(f.startswith("test_") for f in os.listdir(tests))
    check(f"{skill}: has tests", has)
    if has:
        t = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", tests, "-p", "test_*.py"],
                           capture_output=True, text=True, timeout=240)
        check(f"{skill}: its tests pass", t.returncode == 0, t.stderr[-300:])

with open("core/components/memory/standards/rules/naming.yaml", encoding="utf-8") as fh:
    naming = yaml.safe_load(fh)
check("naming: remove is a skill verb with a meaning", bool(naming["skill"]["verbs"].get("remove")))
with open("core/components/memory/standards/rules/naming.md", encoding="utf-8") as fh:
    check("naming: the rules for people list remove", "`remove`" in fh.read())
with open("core/components/agents/product-os-keeper.md", encoding="utf-8") as fh:
    keeper = fh.read()
check("product-os-keeper lists its two skills", "`remove-model-part`" in keeper and "`author-intent-page`" in keeper)
with open("core/components/agents/project-orchestrator.md", encoding="utf-8") as fh:
    check("project-orchestrator lists its skill", "`remove-plan`" in fh.read())
with open("core/components/plays/install-garura/scripts/install.py", encoding="utf-8") as fh:
    install = fh.read()
for skill in ("remove-model-part", "author-intent-page", "remove-plan"):
    check(f"a harness install lays {skill}", f'"{skill}"' in install)

out = tempfile.mktemp(suffix=".json")
lint = subprocess.run(f"node core/tools/lint-components/index.js --target core/components --output json > {out}",
                      shell=True, capture_output=True, text=True, timeout=240)
try:
    data = json.load(open(out, encoding="utf-8"))
    text = json.dumps(data)
    check("lint: it inspected components", '"skills"' in text or len(text) > 1000, text[:200])
    rows = data.get("violations") or data.get("errors") or []
    mine = [v for v in rows if any(s in json.dumps(v) for s in ("remove-model-part", "author-intent-page", "remove-plan"))
            and str(v.get("severity", "error")) == "error"]
    check("lint: no error for the three skills", not mine, mine[:3])
except (OSError, ValueError) as exc:
    check("lint: its output can be read", False, exc)

failed = [r for r in results if not r["ok"]]
print(json.dumps({"passed": len(results) - len(failed), "failed": len(failed), "results": results}, indent=2,
                 ensure_ascii=False))
sys.exit(1 if failed else 0)
