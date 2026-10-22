#!/usr/bin/env python3
"""eval_807.py — the hidden eval suite for #807 (Functionality → Feature on disk; the delivery
plays renamed; ADR 048; the ontology leftovers). Written from the approved design BEFORE the
build, and never given to the build. It must fail before the build and pass after it.

    python3 .garura/project/issues/807/evidence/eval/eval_807.py [--skip-tests]

Exit 0 when every check passes, 1 when any fails. Read only (it runs the repo's own checks).
"""
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 6))
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
RESULTS = []


def check(cid, name, ok, detail=""):
    RESULTS.append((cid, name, bool(ok), detail))


def run(*cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def read(p):
    try:
        with open(p, encoding="utf-8") as fh:
            return fh.read()
    except (OSError, UnicodeDecodeError):
        return None


PLAYS = {"shape-features": "shape-slice", "build-feature": "build-epic",
         "validate-feature": "validate-epic", "release-feature": "release-epic"}
SKILLS = {"author-features": "author-epics"}
P = "core/components/plays"
SK = "core/components/skills"

# E1 — the rename map and the old-name check
rmap = read("core/components/memory/standards/rules/rename-map.yaml") or ""
check("E1a", "rename map holds the five new entries",
      all(re.search(rf"^\s+{o}:\s+{n}\s*$", rmap, re.M) for o, n in {**PLAYS, **SKILLS}.items()))
rc, out = run(sys.executable, "core/tools/naming/check_old_names.py")
check("E1b", "check_old_names.py finds no old component name", rc == 0, out.strip().splitlines()[-1:] if rc else "")

# E2 — the renamed plays and skill exist, the old ones do not
for o, n in PLAYS.items():
    s = read(f"{P}/{n}/SKILL.md") or ""
    check("E2", f"play {n} exists with name: {n}; {o} is gone",
          re.search(rf"^name:\s*{n}\s*$", s, re.M) and not os.path.exists(f"{P}/{o}"))
for o, n in SKILLS.items():
    s = read(f"{SK}/{n}/SKILL.md") or ""
    check("E2", f"skill {n} exists with name: {n}; {o} is gone",
          re.search(rf"^name:\s*{n}\s*$", s, re.M) and not os.path.exists(f"{SK}/{o}"))

# E3 — no "functionality" left, except the allowed history lines
ALLOW_LINE = re.compile(r"(renam|formerly|was called|the old functionality|old name|was functionality|"
                        r"→\s*feature|functionality\s*→|functionalit\w*\s*(->|→))", re.I)
SKIP_DIR = {".git", "node_modules", "__pycache__"}
SKIP_PREFIX = ("docs/adr/0", ".garura/product/scope", ".garura/product/specification",
               ".garura/product/research", ".garura/product/_evidence",
               "core/components/memory/standards/rules/rename-map.yaml",
               "core/tools/naming/", ".garura/project", ".garura/core")
roots = ["core", "docs", "CLAUDE.md", ".garura/user-provided", ".garura/product"]
ALLOWED = {ln.split(" ")[0] for ln in (read(os.path.join(HERE, "allowed-hits.txt")) or "").splitlines()
           if ln.strip() and not ln.startswith("#")}
IGNORED = set(subprocess.run(["git", "ls-files", "--others", "--ignored", "--exclude-standard", "--directory"],
                             capture_output=True, text=True).stdout.split())
left = []
for r in roots:
    paths = [r] if os.path.isfile(r) else [os.path.join(d, f) for d, ds, fs in os.walk(r)
                                          for f in fs if not (set(d.split(os.sep)) & SKIP_DIR)]
    for p in paths:
        if p.startswith(SKIP_PREFIX):
            continue
        if any(p.startswith(ig.rstrip("/") + "/") or p == ig for ig in IGNORED):
            continue
        t = read(p)
        if t is None:
            continue
        in_log = False
        for i, ln in enumerate(t.splitlines(), 1):
            if p.endswith("product-os/ontology.md"):
                if ln.startswith("## Log"):
                    in_log = True
                if in_log:
                    continue
            if re.search(r"functionalit", ln, re.I) and not ALLOW_LINE.search(ln) and f"{p}:{i}" not in ALLOWED:
                left.append(f"{p}:{i}")
    for d, ds, fs in (os.walk(r) if os.path.isdir(r) else []):
        for x in ds + fs:
            full = os.path.join(d, x)
            if re.search(r"functionalit", x, re.I) and not full.startswith(SKIP_PREFIX):
                left.append(f"{full} (path)")
check("E3", "no 'functionality' left outside history lines and skipped records", not left,
      f"{len(left)} left, e.g. {left[:6]}")

# E4 — the spine schema
sp = read("core/components/memory/standards/schemas/product-os/spine.yaml") or ""
check("E4", "spine schema has features: and feature_refs, no functionalities:",
      re.search(r"^features:", sp, re.M) and "feature_refs" in sp and not re.search(r"^functionalities:", sp, re.M))

# E5 — the grounding template
g = "core/components/memory/standards/schemas/product-os/grounding"
ft = read(f"{g}/feature.md") or ""
check("E5", "grounding template feature.md exists with a Feature: H1, functionality.md is gone",
      re.search(r"^# Feature:", ft, re.M) and not os.path.exists(f"{g}/functionality.md"))

# E6 — Garura's own model
pm = ".garura/product/product-os"
fdirs = sorted(os.listdir(f"{pm}/features")) if os.path.isdir(f"{pm}/features") else []
pages_ok = fdirs and all((read(f"{pm}/features/{d}/feature.md") or "").lstrip().startswith("# Feature:") for d in fdirs)
check("E6a", "Garura's model has features/<id>/feature.md pages (21), each with a Feature: H1, ids kept",
      len(fdirs) == 21 and pages_ok and all(d.startswith("fn-") for d in fdirs), f"{len(fdirs)} folders")
check("E6b", "no functionalities/ folder in Garura's model", not os.path.exists(f"{pm}/functionalities"))
spine = read(f"{pm}/_spine.yaml") or ""
docs = re.findall(r"doc:\s*(features/\S+/feature\.md)", spine)
check("E6c", "Garura's spine lists the 21 features and every doc pointer exists",
      re.search(r"^features:", spine, re.M) and len(docs) == 21 and all(os.path.isfile(f"{pm}/{d}") for d in docs),
      f"{len(docs)} pointers")

# E7 — stamped copies stay identical
import hashlib


def same(glob_paths):
    hs = {hashlib.sha256(open(x, "rb").read()).hexdigest() for x in glob_paths if os.path.isfile(x)}
    return len(hs) == 1


lg = [os.path.join(P, d, "scripts/lint_grounding.py") for d in os.listdir(P) if os.path.isfile(os.path.join(P, d, "scripts/lint_grounding.py"))]
check("E7a", "the 12 lint_grounding.py copies are identical", len(lg) == 12 and same(lg), f"{len(lg)} copies")
it = [os.path.join(dp, "intent_touches.py") for dp, ds, fs in os.walk("core/components") if "intent_touches.py" in fs]
check("E7b", "the intent_touches.py copies are identical", len(it) >= 5 and same(it), f"{len(it)} copies")
ci = [os.path.join(dp, "check_ice_workable.py") for dp, ds, fs in os.walk("core/components") if "check_ice_workable.py" in fs]
check("E7c", "the check_ice_workable.py copies are identical", len(ci) == 2 and same(ci))
crs = [os.path.join(P, d, "scripts/check_ready_slice.py") for d in os.listdir(P) if d.startswith("shape-") and d.endswith("-lens")
       and os.path.isfile(os.path.join(P, d, "scripts/check_ready_slice.py"))]
check("E7d", "the lens check_ready_slice.py copies are identical", len(crs) == 7 and same(crs), f"{len(crs)} copies")

# E8 — the test suites
TESTS = ["core/components/plays/discover-domains/scripts/test_lint_grounding.py",
         "core/components/plays/discover-domains/scripts/test_lint_ice.py",
         "core/components/plays/discover-domains/scripts/test_vision_scripts.py",
         "core/components/plays/create-play/references/test_check_ice_workable.py",
         "core/components/plays/create-play/references/test_intent_touches.py",
         "core/components/plays/discover-capabilities/scripts/test_check_sources.py",
         "core/components/plays/discover-capabilities/scripts/test_persist_understand.py",
         "core/components/plays/discover-intent/scripts/test_intent_scripts.py",
         "core/components/plays/next/scripts/test_derive_candidates.py",
         "core/components/plays/shape-slice/scripts/test_validate_epics.py",
         "core/components/skills/find-model-gaps/scripts/test_find_gaps.py",
         "core/components/skills/link-model-gaps/scripts/test_apply_links.py",
         "core/tools/rebuild-eval/test_rebuild_eval.py",
         "core/components/skills/author-decision/scripts/test_adr.py",
         "core/components/plays/record-decision/scripts/test_apply_adr.py",
         "core/components/plays/install-garura/scripts/test_install.py",
         "core/tools/naming/test_naming_tools.py"]
if "--skip-tests" not in sys.argv:
    for t in TESTS:
        if not os.path.isfile(t):
            check("E8", f"test suite {t}", False, "missing")
            continue
        rc, out = run(sys.executable, t)
        check("E8", f"test suite {os.path.basename(t)}", rc == 0, out.strip().splitlines()[-1:] if rc else "")

# E9 — lint_play: every play that passed before still passes (renamed plays by their new name)
base = {}
for ln in (read(os.path.join(HERE, "baseline-lint-play.txt")) or "").splitlines():
    parts = ln.split()
    if len(parts) >= 3:
        base[PLAYS.get(parts[0], parts[0])] = parts[2]
bad = []
for play, verdict in base.items():
    if verdict != "PASS":
        continue
    rc, out = run(sys.executable, "core/components/plays/create-play/scripts/lint_play.py", f"{P}/{play}/SKILL.md")
    if "VERDICT: PASS" not in out:
        bad.append(play)
check("E9", "lint_play passes on every play that passed before", not bad, f"now failing: {bad}")

# E10 — component linter: no new error
rc, out = run("node", "core/tools/lint-components/index.js", "--target", "core/components")
m = re.search(r'"errors":\s*(\d+)', out)
check("E10", "component linter shows no new error (baseline 121)", m and int(m.group(1)) <= 121, m.group(1) if m else out[-200:])

# E11 — grounding linter on Garura's model: same result
rc, out = run(sys.executable, f"{P}/discover-domains/scripts/lint_grounding.py", "--root", pm, "--spine", f"{pm}/_spine.yaml")
try:
    import json
    d = json.loads(out[out.find("{"):])
    ne, nw = len(d["errors"]), len(d["warnings"])
except Exception:
    ne, nw = -1, -1
check("E11", "grounding linter gives Garura's model the same counts as before (70 errors, 9 warnings)",
      (ne, nw) == (70, 9), f"now {ne} errors, {nw} warnings")

# E12 — ADR 048
adrs = [f for f in os.listdir("docs/adr") if f.startswith("048-")]
a = read(f"docs/adr/{adrs[0]}") if adrs else ""
check("E12a", "ADR 048 exists and is Accepted", a and re.search(r"\*\*Status:\*\*\s*Accepted", a))
check("E12b", "ADR 048 amends 019, 024, 028, 031, 043 and 047",
      a and all(re.search(rf"ADR 0?{n}\b", a) for n in ("19", "24", "28", "31", "43", "47")))
ptr = [n for n in ("019", "024", "028", "031", "043", "047")
       for f in os.listdir("docs/adr") if f.startswith(n + "-") and "048" not in (read(f"docs/adr/{f}") or "").split("\n## ")[0]]
check("E12c", "each amended ADR carries a forward pointer to 048 in its head", not ptr, f"missing: {ptr}")
check("E12d", "the ADR index has a 048 row", "048" in (read("docs/adr/_index.md") or ""))

# E13 — the ontology's leftovers and the template
o = read("core/components/memory/standards/schemas/product-os/ontology.md") or ""
check("E13a", "the ontology has no 'until the rename' notes outside its log", not re.search(r"until the rename", o.split("\n## Log", 1)[0], re.I))
src = o.split("### Source", 1)[1].split("\n### ", 1)[0] if "### Source" in o else ""
check("E13b", "the Source kind has a Layer line and an In the tracker as line",
      "**Layer:**" in src and "**In the tracker as:**" in src)
tpl = read("core/components/memory/standards/templates/product-ontology.md") or ""
check("E13c", "the ontology template defines the Layer and In the tracker as lines",
      "Layer" in tpl and "In the tracker as" in tpl)

# E14 — the glossary
gl = read("core/grounding/glossary.md") or ""
check("E14", "the glossary has a Feature entry and Slice/Epic follow v7",
      re.search(r"\bFeature\b", gl) and re.search(r"\bSlice\b", gl) and re.search(r"\bEpic\b", gl)
      and not re.search(r"^\|\s*\*?\*?Functionality\b", gl, re.M))

passed = sum(1 for r in RESULTS if r[2])
for cid, name, ok, detail in RESULTS:
    print(f"  [{'PASS' if ok else 'FAIL'}] {cid} {name}" + (f" — {detail}" if (detail and not ok) else ""))
print(f"\n{passed} passed, {len(RESULTS) - passed} failed")
sys.exit(0 if passed == len(RESULTS) else 1)
