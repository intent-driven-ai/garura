#!/usr/bin/env python3
"""
eval_813.py — the eval for the grouped change #813 + #809 (plan 788, finishes #792).

Written before the build. It must fail before the build and pass after it.
A builder never reads this file.

    python3 .garura/project/issues/813/evidence/eval/eval_813.py [--root .] [--out result.json]

Exit 0 when every check passes, 1 when one fails.
"""
import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

PRE_807 = "f4137dc6"  # Garura's own model just before #807
MIGRATE = "core/components/plays/install-garura/scripts/migrate_model.py"
INSTALL = "core/components/plays/install-garura/scripts/install.py"
GUARD_MAIN = "core/components/plays/create-play/references/model_names.py"
SHARED = "core/tools/lint-components/lib/rules/shared-scripts.js"
LINT_GROUNDING = "core/components/plays/discover-domains/scripts/lint_grounding.py"

results = []


def check(name, ok, detail=""):
    results.append({"check": name, "ok": bool(ok), "detail": str(detail)[-400:]})


def run(args, cwd):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)


def exists(root, rel):
    return os.path.exists(os.path.join(root, rel))


def read(root, rel):
    p = os.path.join(root, rel)
    return open(p, encoding="utf-8", errors="ignore").read() if os.path.isfile(p) else ""


SLICE_RECORD = """slice:
  id: slice-self-booking
  functionalities:
    - functionality_ref: fn-1
      order: 1
"""


def make_old_project(root, tmp):
    """A git project holding a pre-#807 product model, plus a slice, an ICE and a nested page."""
    proj = os.path.join(tmp, "proj")
    os.makedirs(proj)
    arch = subprocess.run(["git", "archive", PRE_807, ".garura/product/product-os"], cwd=root, capture_output=True)
    if arch.returncode != 0:
        raise RuntimeError("git archive failed: " + arch.stderr.decode()[-200:])
    subprocess.run(["tar", "-x"], cwd=proj, input=arch.stdout, check=True)
    po = os.path.join(proj, ".garura/product/product-os")
    spine_p = os.path.join(po, "_spine.yaml")
    spine = open(spine_p).read()
    spine += """slices:
  - id: slice-self-booking
    slug: self-booking
    functionality_refs: [fn-1]
    record: work/slices/self-booking.yaml
ices:
  - id: ice-fn-1
    for_kind: functionality
    for: fn-1
    doc: ices/ice-fn-1.md
"""
    open(spine_p, "w").write(spine)
    os.makedirs(os.path.join(po, "work/slices"), exist_ok=True)
    open(os.path.join(po, "work/slices/self-booking.yaml"), "w").write(SLICE_RECORD)
    os.makedirs(os.path.join(po, "work/board/move-a-card"), exist_ok=True)
    open(os.path.join(po, "work/board/move-a-card/functionality.md"), "w").write("# Functionality: Move a card\n\nA person moves a card.\n")
    for c in (["git", "init", "-q"], ["git", "add", "-A"],
              ["git", "-c", "user.name=eval", "-c", "user.email=eval@example.com", "commit", "-qm", "old model"]):
        subprocess.run(c, cwd=proj, check=True)
    return proj, po


def commits(proj):
    return int(run(["git", "rev-list", "--count", "HEAD"], proj).stdout.strip() or 0)


def old_left(po):
    left = []
    for dp, ds, fs in os.walk(po):
        for d in ds:
            if d == "functionalities":
                left.append(os.path.relpath(os.path.join(dp, d), po))
        for f in fs:
            p = os.path.join(dp, f)
            if f == "functionality.md":
                left.append(os.path.relpath(p, po))
                continue
            if f.endswith((".yaml", ".yml", ".md")):
                t = open(p, encoding="utf-8", errors="ignore").read()
                if re.search(r"^\s*functionalities\s*:|functionality_refs?\b|for_kind:\s*functionality\b", t, re.M):
                    left.append(os.path.relpath(p, po) + " (key)")
                if f.endswith(".md") and re.search(r"^# Functionality:|^## Functionalities\s*$", t, re.M):
                    left.append(os.path.relpath(p, po) + " (heading)")
    return left


def eval_813(root):
    check("813: migrate_model.py exists", exists(root, MIGRATE))
    check("813: install.py runs the model migration", "migrate_model" in read(root, INSTALL))
    check("813: the public installer runs the model migration", "migrate_model" in read(root, "installer/install.sh"))
    if not exists(root, MIGRATE):
        return
    with tempfile.TemporaryDirectory() as tmp:
        proj, po = make_old_project(root, tmp)
        before = commits(proj)
        r = run([sys.executable, os.path.join(root, MIGRATE), "--target", proj], proj)
        check("813: the migration exits 0 on an old model", r.returncode == 0, r.stdout + r.stderr)
        try:
            rep = json.loads(r.stdout)
        except ValueError:
            rep = None
        check("813: the migration prints a JSON report", isinstance(rep, dict), r.stdout)
        if isinstance(rep, dict):
            text = json.dumps(rep)
            check("813: the report lists what it moved", "functionalit" in text and "feature" in text, text[:300])
        check("813: no old key, file, folder or heading is left", not old_left(po), old_left(po)[:10])
        spine = open(os.path.join(po, "_spine.yaml")).read()
        check("813: the spine has a features list", re.search(r"^features\s*:", spine, re.M))
        check("813: spine doc pointers name features/…/feature.md", "/feature.md" in spine and "functionality.md" not in spine)
        check("813: slice refs are feature_refs", "feature_refs" in spine)
        check("813: the ICE is for_kind feature", re.search(r"for_kind:\s*feature\b", spine))
        rec = open(os.path.join(po, "work/slices/self-booking.yaml")).read()
        check("813: the slice record uses features / feature_ref", "feature_ref" in rec and "functionalit" not in rec, rec)
        check("813: the nested page is renamed with its H1",
              os.path.isfile(os.path.join(po, "work/board/move-a-card/feature.md"))
              and read(po, "work/board/move-a-card/feature.md").startswith("# Feature: Move a card"))
        check("813: prose is left alone", "A person moves a card." in read(po, "work/board/move-a-card/feature.md"))
        check("813: the migration made exactly one commit", commits(proj) == before + 1, (before, commits(proj)))
        check("813: the tree is clean after the migration", run(["git", "status", "--porcelain"], proj).stdout.strip() == "",
              run(["git", "status", "--porcelain"], proj).stdout)
        again = run([sys.executable, os.path.join(root, MIGRATE), "--target", proj], proj)
        check("813: a second run is a no-op (exit 0, no new commit)", again.returncode == 0 and commits(proj) == before + 1,
              again.stdout + again.stderr)
    with tempfile.TemporaryDirectory() as tmp:
        proj, po = make_old_project(root, tmp)
        sp = os.path.join(po, "_spine.yaml")
        open(sp, "a").write("features: []\n")
        subprocess.run(["git", "-c", "user.name=e", "-c", "user.email=e@e", "commit", "-qam", "both"], cwd=proj)
        r = run([sys.executable, os.path.join(root, MIGRATE), "--target", proj], proj)
        check("813: the migration refuses a model with both old and new keys", r.returncode != 0, r.stdout + r.stderr)
    # The guard: one main copy, kept the same, called where scripts load the model.
    check("813: the guard's main copy exists", exists(root, GUARD_MAIN))
    check("813: the drift check covers the guard", "model_names.py" in read(root, SHARED))
    copies = glob.glob(os.path.join(root, "core/components/**/scripts/model_names.py"), recursive=True)
    main = read(root, GUARD_MAIN)
    check("813: every copy of the guard matches the main copy", copies and all(open(c).read() == main for c in copies),
          [os.path.relpath(c, root) for c in copies if open(c).read() != main])
    missing = []
    for p in glob.glob(os.path.join(root, "core/components/**/scripts/*.py"), recursive=True):
        b = os.path.basename(p)
        if b.startswith("test_") or b in ("model_names.py", "migrate_model.py") or "/references/" in p and b != "lint_grounding.py":
            continue
        t = open(p, encoding="utf-8", errors="ignore").read()
        if "_spine" in t and "safe_load" in t and "model_names" not in t:
            missing.append(os.path.relpath(p, root))
    check("813: every script that loads the spine calls the guard", not missing, missing)
    with tempfile.TemporaryDirectory() as tmp:
        proj, po = make_old_project(root, tmp)
        r = run([sys.executable, os.path.join(root, LINT_GROUNDING), "--root", po, "--spine", os.path.join(po, "_spine.yaml")], proj)
        out = (r.stdout + r.stderr).lower()
        check("813: the spine linter stops on an old model", r.returncode != 0 and "functionalit" in out, out[-300:])
        check("813: the stop message names the upgrade step", "upgrade" in out or "migrate_model" in out, out[-300:])
    tests = glob.glob(os.path.join(root, "core/components/plays/install-garura/scripts/test_*.py"))
    for t in sorted(tests):
        r = run([sys.executable, os.path.relpath(t, root)], root)
        check(f"all: {os.path.relpath(t, root)} passes", r.returncode == 0, r.stdout[-300:] + r.stderr[-300:])
    check("813: a test covers the migration", any("migrate_model" in open(t).read() for t in tests))


GONE = [
    ".garura/product/scope", ".garura/product/specification", ".garura/product/_checkpoints/specify-product",
    ".garura/product/_evidence/specify-product", ".garura/product/user-provided/grounding-questions.md",
    ".garura/product/research/agentic-methodology.md", ".garura/product/research/ai-governance.md",
    ".garura/product/research/engineering-experience.md", ".garura/product/research/engineering-observability.md",
    ".garura/product/research/work-intelligence.md",
    "core/components/memory/standards/schemas/intent-epic.yaml",
    "core/components/memory/standards/schemas/mvp-recommendation.yaml",
    "core/components/memory/standards/rules/features.md", "core/components/memory/standards/rules/feature-catalog.md",
    "core/components/memory/standards/rules/epics.md", "core/components/memory/standards/rules/scenarios.md",
    "core/components/memory/standards/rules/design.md", "core/components/memory/standards/rules/architecture.md",
    "core/components/memory/standards/templates/feature-tree-output.md",
    "core/components/skills/infer-features", "core/components/skills/infer-feature-catalog",
    "core/components/skills/author-feature-catalog", "core/components/skills/author-product-spec",
    "core/components/skills/derive-capability-selection", "core/components/skills/derive-design-patterns",
    "core/components/skills/derive-logical-architecture", "core/components/skills/derive-nfr-spec",
    "core/components/skills/derive-physical-architecture", "core/components/skills/derive-quality-vision",
    "core/components/skills/derive-systems-inventory", "core/components/skills/derive-tech-stack",
    "core/components/agents/feature-steward.md", "core/components/agents/epic-expectation-crafter.md",
    "core/components/agents/product-keeper.md", "core/components/agents/market-analyst.md",
]
KEPT = ["core/components/skills/derive-blast-radius/SKILL.md", ".garura/product/user-provided/project-brief.md"]
DELETED_NAMES = ["intent-epic.yaml", "mvp-recommendation.yaml", "feature-catalog.md", "feature-tree-output.md",
                 "infer-features", "infer-feature-catalog", "author-feature-catalog", "author-product-spec",
                 "derive-capability-selection", "derive-design-patterns", "derive-logical-architecture",
                 "derive-nfr-spec", "derive-physical-architecture", "derive-quality-vision",
                 "derive-systems-inventory", "derive-tech-stack", "feature-steward", "epic-expectation-crafter",
                 "product-keeper", "market-analyst"]


def eval_809(root):
    still = [p for p in GONE if exists(root, p)]
    check("809: every retired item is gone", not still, still)
    for k in KEPT:
        check(f"809: {k} is kept", exists(root, k))
    # Rule 12 survives as its own rule; the rest of product.md is gone.
    rules = glob.glob(os.path.join(root, "core/components/memory/standards/rules/*.md"))
    r12 = [p for p in rules if "grounding-questions.md" in open(p).read() and "Rule 12" in open(p).read()
           and not p.endswith("/product.md")]
    check("809: Rule 12 (questions are first-class) has its own rule file", r12, [os.path.basename(p) for p in rules][:50])
    pm = read(root, "core/components/memory/standards/rules/product.md")
    check("809: the rest of rules/product.md is gone", not re.search(r"^## Rule (1|2|3|11|13|15)\b", pm, re.M))
    # The two learnings move into memory standards.
    for old in (".garura/product/research/arch.md", ".garura/product/research/standards/play-orchestration.md"):
        body = subprocess.run(["git", "show", "e0990229:" + old], cwd=root, capture_output=True, text=True).stdout
        lines = [l.strip() for l in body.splitlines() if len(l.strip()) > 40 and not l.startswith("#")][:3]
        hits = [h for h in glob.glob(os.path.join(root, "core/components/memory/**/*.md"), recursive=True)
                if lines and all(l in open(h).read() for l in lines)]
        check(f"809: {os.path.basename(old)} moved into memory", hits and not exists(root, old), (hits, lines[:1]))
    # No index row, rename-map entry or live component still names a deleted part.
    idx = "".join(read(root, p) for p in ("core/components/memory/standards/_index.md",
                                          "core/components/memory/standards/rules/_index.md",
                                          "core/components/memory/standards/schemas/_index.md",
                                          "core/components/memory/standards/templates/_index.md"))
    check("809: the memory indexes name no deleted file",
          not [n for n in DELETED_NAMES if n in idx] and not re.search(r"\b(features|epics|scenarios|design|architecture)\.md\b", idx),
          [n for n in DELETED_NAMES if n in idx])
    rm = read(root, "core/components/memory/standards/rules/rename-map.yaml")
    check("809: rename-map.yaml maps nothing onto a deleted part", not [n for n in DELETED_NAMES if re.search(r":\s*" + re.escape(n) + r"\s*$", rm, re.M)],
          [n for n in DELETED_NAMES if re.search(r":\s*" + re.escape(n) + r"\s*$", rm, re.M)])
    live = []
    for p in glob.glob(os.path.join(root, "core/components/**/*.md"), recursive=True) + \
            glob.glob(os.path.join(root, "core/components/**/*.py"), recursive=True) + \
            glob.glob(os.path.join(root, "core/components/**/*.yaml"), recursive=True):
        t = open(p, encoding="utf-8", errors="ignore").read()
        if re.search(r"^deprecated:\s*true", t, re.M) or "rename-map.yaml" in p:
            continue
        for n in DELETED_NAMES:
            if re.search(r"(?<![\w-])" + re.escape(n) + r"(?![\w-])", t):
                live.append(f"{os.path.relpath(p, root)}: {n}")
    check("809: no live part names a deleted part", not live, live[:15])
    # The decision record.
    adrs = [p for p in glob.glob(os.path.join(root, "docs/adr/0*.md")) if re.search(r"intent.?epic", open(p).read(), re.I)
            and int(os.path.basename(p)[:3]) >= 50]
    check("809: an ADR records the retirement", adrs, adrs)
    check("809: ADR 017 points forward to it", adrs and os.path.basename(adrs[0])[:3] in read(root, "docs/adr/017-folder-whitelist.md"))
    a035 = glob.glob(os.path.join(root, "docs/adr/035-*.md"))
    check("809: ADR 035 points forward to it", adrs and a035 and os.path.basename(adrs[0])[:3] in open(a035[0]).read())


def eval_all(root):
    r = run([sys.executable, "core/tools/naming/check_old_names.py", "--root", "."], root)
    check("all: the old-name check reads 0", r.returncode == 0, r.stdout[-300:])
    for t in sorted(glob.glob(os.path.join(root, "core/tools/lint-components/test/*.test.js"))):
        r = run(["node", os.path.relpath(t, root)], root)
        check(f"all: {os.path.basename(t)} passes", r.returncode == 0, r.stdout[-200:] + r.stderr[-200:])
    r = run(["node", "core/tools/lint-components/index.js", "--target", "core/components"], root)
    try:
        vs = json.loads(r.stdout)["violations"]
    except Exception:
        vs = None
    if vs is None:
        check("all: the component linter runs", False, r.stderr[-300:])
    else:
        other = [v for v in vs if v["severity"] == "error" and not v["rule"].startswith("asking-a-person")]
        check("all: no component-linter error beyond the 121 old ones", len(other) <= 121, len(other))
        drift = [v for v in vs if "drift" in v["rule"]]
        check("all: no shared-script drift", not drift, drift[:5])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--out")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    for fn in (eval_813, eval_809, eval_all):
        try:
            fn(root)
        except Exception as e:  # a crash is a failed check, never a pass
            check("%s ran" % fn.__name__, False, repr(e))
    failed = [r for r in results if not r["ok"]]
    report = {"passed": len(results) - len(failed), "failed": len(failed), "results": results}
    if a.out:
        with open(a.out, "w") as fh:
            json.dump(report, fh, indent=2)
    for r in results:
        print(("PASS " if r["ok"] else "FAIL ") + r["check"])
    print("%d passed, %d failed" % (report["passed"], report["failed"]))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
