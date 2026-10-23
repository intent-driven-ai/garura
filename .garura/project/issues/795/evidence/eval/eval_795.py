#!/usr/bin/env python3
"""
eval_795.py — the eval for #795 (the new /shape-slice) + #836 (drop /next), plan 788.

Written before the build. It must fail before the build and pass after it.
A builder never reads this file.

    python3 .garura/project/issues/795/evidence/eval/eval_795.py [--root .] [--out result.json]
"""
import argparse
import glob
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

PLAY = "core/components/plays/shape-slice"
SKILL = PLAY + "/SKILL.md"
ICE = PLAY + "/reference/ice.md"
SCRIPTS = PLAY + "/scripts"
LINT_PLAY = "core/components/plays/create-play/scripts/lint_play.py"
SPINE_SCHEMA = "core/components/memory/standards/schemas/product-os/spine.yaml"
SLICE_SCHEMA = "core/components/memory/standards/schemas/product-os/slice.yaml"

results = []


def check(name, ok, detail=""):
    results.append({"check": name, "ok": bool(ok), "detail": str(detail)[-400:]})


def read(root, rel):
    p = os.path.join(root, rel)
    return open(p, encoding="utf-8", errors="ignore").read() if os.path.isfile(p) else ""


def run(args, cwd):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)


def section(text, title):
    m = re.search(r"^##+ " + re.escape(title) + r".*?$(.*?)(?=^## (?!#)|\Z)", text, re.M | re.S)
    return m.group(1) if m else ""


def eval_ice_and_play(root):
    ice = read(root, ICE)
    check("ICE: the intent is about a business intent, not a realized slice",
          re.search(r"business intent", section(ice, "Intent"), re.I) and "realized" not in section(ice, "Intent"))
    check("ICE: it writes no plan, epic, story or eval", re.search(r"no plan.{0,40}no epic", ice, re.I | re.S))
    for n in range(1, 15):
        check(f"ICE: C{n} and F{n} exist", re.search(rf"^- C{n} ", ice, re.M) and re.search(rf"^- F{n} ", ice, re.M))
    check("ICE: six success scenarios", all(re.search(rf"^- S{n} ", ice, re.M) for n in range(1, 7)))
    check("ICE: one recovery per failure", all(re.search(rf"^- REC{n} \(F{n}\)", ice, re.M) for n in range(1, 15)))
    sk = read(root, SKILL)
    fp = re.search(r"sha256:([0-9a-f]{64})", sk)
    real = hashlib.sha256(open(os.path.join(root, ICE), "rb").read()).hexdigest() if ice else ""
    check("play: fingerprint matches the ICE", fp and fp.group(1) == real, (fp.group(1) if fp else None, real))
    r = run([sys.executable, LINT_PLAY, SKILL], root)
    check("play: lint_play passes", r.returncode == 0, r.stdout[-400:])
    check("play: position is both", re.search(r"^position:\s*both\s*$", sk, re.M))
    check("play: the entry is a business intent issue number", re.search(r"/shape-slice\s+<?(?:intent|issue|bi)", sk, re.I))
    for old in ("author-epics", "check-cut-tensions", "persist_epics", "validate_epics", "realized"):
        check(f"play: no longer uses '{old}'", old not in sk, old)
    check("play: calls grill_budget.py", "grill_budget.py" in sk)
    check("play: names the asking-a-person rule in its workflow", "asking-a-person.md" in section(sk, "Workflow"))
    check("play: records questions in grounding-questions.md", "grounding-questions.md" in sk)
    check("play: dispatches product-os-keeper", "product-os-keeper" in sk)
    for gone in ("persist_epics.py", "validate_epics.py", "test_validate_epics.py"):
        check(f"scripts: {gone} is gone", not os.path.exists(os.path.join(root, SCRIPTS, gone)))
    sc = read(root, PLAY + "/stop-condition.yaml")
    for f in ("slice-check.json", "approval.json", "guard-report.json", "grounding-questions.md"):
        check(f"stop condition reads {f}", f in sc)


SPINE = """domains:
  - id: dom-booking
    slug: booking
capabilities:
  - id: cap-booking
    slug: booking
    domain: dom-booking
features:
  - id: ft-pick-slot
    slug: pick-slot
    capability: cap-booking
  - id: ft-reminder
    slug: reminder
    capability: cap-booking
slices: {slices}
"""


def eval_scripts(root):
    find = os.path.join(root, SCRIPTS, "find_serving_slice.py")
    persist = os.path.join(root, SCRIPTS, "persist_slice.py")
    check("scripts: find_serving_slice.py exists", os.path.isfile(find))
    check("scripts: persist_slice.py exists", os.path.isfile(persist))
    if os.path.isfile(find):
        with tempfile.TemporaryDirectory() as tmp:
            sp = os.path.join(tmp, "_spine.yaml")
            open(sp, "w").write(SPINE.format(slices="""
  - id: sl-self-booking
    slug: self-booking
    feature_refs: [ft-pick-slot, ft-reminder]
    vertical: booking page
    intents: ["340"]"""))
            r = run([sys.executable, find, "--spine", sp, "--intent", "340"], tmp)
            out = json.loads(r.stdout or "{}") if r.returncode == 0 else {}
            check("find: a slice that lists the intent is found", out.get("match") == "sl-self-booking", r.stdout + r.stderr)
            r = run([sys.executable, find, "--spine", sp, "--intent", "999", "--features", "ft-pick-slot,ft-reminder",
                     "--surface", "booking page"], tmp)
            out = json.loads(r.stdout or "{}") if r.returncode == 0 else {}
            check("find: same features and surface is found", out.get("match") == "sl-self-booking", r.stdout + r.stderr)
            r = run([sys.executable, find, "--spine", sp, "--intent", "999", "--features", "ft-pick-slot",
                     "--surface", "booking page"], tmp)
            out = json.loads(r.stdout or "{}") if r.returncode == 0 else {}
            check("find: other features is no match", r.returncode == 0 and out.get("match") is None, r.stdout + r.stderr)
    if os.path.isfile(persist):
        def go(slice_obj, slices="[]"):
            tmp = tempfile.mkdtemp()
            root_po = os.path.join(tmp, "product-os")
            os.makedirs(os.path.join(root_po, "intents"))
            open(os.path.join(root_po, "intents", "340.md"), "w").write("# Patients book their own appointments online\n")
            sp = os.path.join(root_po, "_spine.yaml")
            open(sp, "w").write(SPINE.format(slices=slices))
            sj = os.path.join(tmp, "slice.json")
            json.dump(slice_obj, open(sj, "w"))
            r = run([sys.executable, persist, "--root", root_po, "--spine", sp, "--slice", sj], tmp)
            return r, root_po, sp
        good = {"id": "sl-self-booking", "slug": "self-booking", "feature_refs": ["ft-pick-slot", "ft-reminder"],
                "vertical": "booking page", "intents": ["340"],
                "surface": {"name": "booking page", "persona_ref": "patient-on-phone"}}
        r, po, sp = go(good)
        import yaml
        spine = yaml.safe_load(open(sp)) if r.returncode == 0 else {}
        sl = [s for s in (spine.get("slices") or []) if s.get("id") == "sl-self-booking"]
        check("persist: writes the spine slice", r.returncode == 0 and sl, r.stdout + r.stderr)
        if sl:
            check("persist: features in build order", sl[0].get("feature_refs") == ["ft-pick-slot", "ft-reminder"])
            check("persist: vertical and intents", sl[0].get("vertical") == "booking page" and sl[0].get("intents") == ["340"])
            check("persist: no old slice fields", not any(k in sl[0] for k in ("status", "order", "effort", "depends_on", "domain_ref")), sl[0])
        rec = os.path.join(po, "slices", "sl-self-booking.yaml")
        check("persist: the record is at product-os/slices/<id>.yaml", os.path.isfile(rec))
        check("persist: the record names the persona", os.path.isfile(rec) and "patient-on-phone" in open(rec).read())
        bad = dict(good); bad["surface"] = {"name": "booking page"}
        r, po, sp = go(bad)
        check("persist: refuses a slice with no tester (exit 2)", r.returncode == 2, r.stdout + r.stderr)
        bad = dict(good); bad.pop("vertical"); bad["surface"] = {}
        r, po, sp = go(bad)
        check("persist: refuses a slice with no surface (exit 2)", r.returncode == 2, r.stdout + r.stderr)
        bad = dict(good); bad["surface"] = [{"name": "a", "persona_ref": "p"}, {"name": "b", "persona_ref": "p"}]
        r, po, sp = go(bad)
        check("persist: refuses more than one surface (exit 2)", r.returncode == 2, r.stdout + r.stderr)
        existing = """
  - id: sl-self-booking
    slug: self-booking
    feature_refs: [ft-pick-slot, ft-reminder]
    vertical: booking page
    intents: ["340"]"""
        again = dict(good); again["intents"] = ["341"]
        r, po, sp = go(again, existing)
        spine = yaml.safe_load(open(sp)) if r.returncode == 0 else {}
        sls = spine.get("slices") or []
        check("persist: an existing slice gains the intent, appended, no second slice",
              r.returncode == 0 and len(sls) == 1 and sls[0].get("intents") == ["340", "341"], (r.stdout + r.stderr, sls))
    for t in sorted(glob.glob(os.path.join(root, SCRIPTS, "test_*.py"))):
        r = run([sys.executable, os.path.relpath(t, root)], root)
        check(f"tests: {os.path.basename(t)} passes", r.returncode == 0, r.stdout[-200:] + r.stderr[-200:])
    check("tests: persist_slice and find_serving_slice have tests",
          any("persist_slice" in open(t).read() for t in glob.glob(os.path.join(root, SCRIPTS, "test_*.py"))) and
          any("find_serving_slice" in open(t).read() for t in glob.glob(os.path.join(root, SCRIPTS, "test_*.py"))))


def eval_schemas(root):
    sp = read(root, SPINE_SCHEMA)
    m = re.search(r"^slices:\n(.*?)(?=^\S)", sp, re.S | re.M)
    block = m.group(1) if m else ""
    check("schema: spine slice has vertical", re.search(r"^\s+vertical:", block, re.M), block[:200])
    check("schema: spine slice has intents", re.search(r"^\s+intents:", block, re.M))
    for k in ("status", "order", "effort", "depends_on", "domain_ref"):
        check(f"schema: spine slice drops {k}", not re.search(rf"^\s+{k}:", block, re.M))
    sl = read(root, SLICE_SCHEMA)
    check("schema: slice.yaml no longer says /shape-slice cuts epics", not re.search(r"shape-slice[^\n]{0,60}cut", sl, re.I))
    check("schema: slice.yaml names intents and vertical", "intents" in sl and "vertical" in sl)


def eval_next(root):
    check("next: the /next play is gone", not os.path.exists(os.path.join(root, "core/components/plays/next")))
    left = [os.path.relpath(p, root) for p in glob.glob(os.path.join(root, "core/components/**/*.md"), recursive=True)
            if re.search(r"run\s+`?/next`?", open(p, encoding="utf-8", errors="ignore").read())
            # no-unbacked-recommendation.md quotes "run /next" as an old example of a wrong default, not an instruction
            and not p.endswith("rules/no-unbacked-recommendation.md")]
    check("next: no play or rule tells a person to run /next", not left, left[:10])
    pn = read(root, "core/components/memory/standards/rules/pipeline-next.md")
    check("next: the Next-line map no longer points to /next", not re.search(r"`/next`", pn), re.findall(r".{0,40}/next.{0,40}", pn)[:3])
    adrs = [p for p in glob.glob(os.path.join(root, "docs/adr/0*.md")) if int(os.path.basename(p)[:3]) >= 51
            and re.search(r"/next", open(p).read())]
    check("next: an ADR records why /next was dropped", adrs, adrs)
    bad = []
    for sk in sorted(glob.glob(os.path.join(root, "core/components/plays/*/SKILL.md"))):
        r = run([sys.executable, LINT_PLAY, os.path.relpath(sk, root)], root)
        if re.search(r"\[GAP \] next-command", r.stdout):
            bad.append(os.path.relpath(sk, root))
    check("next: no play fails lint_play's next-command check", not bad, bad)


def eval_all(root):
    r = run([sys.executable, "core/tools/naming/check_old_names.py", "--root", "."], root)
    check("all: the old-name check reads 0", r.returncode == 0, r.stdout[-200:])
    r = run(["node", "core/tools/lint-components/index.js", "--target", "core/components"], root)
    try:
        vs = json.loads(r.stdout)["violations"]
    except Exception:
        vs = None
    if vs is None:
        check("all: the component linter runs", False, r.stderr[-200:])
    else:
        ss = [v for v in vs if "/plays/shape-slice/" in v["file"] and v["severity"] == "error"]
        check("all: no component-linter error on shape-slice", not ss, ss[:5])
        other = [v for v in vs if v["severity"] == "error"]
        check("all: total linter errors do not grow (was 135)", len(other) <= 135, len(other))
        check("all: no shared-script drift", not [v for v in vs if "drift" in v["rule"]])
    for t in sorted(glob.glob(os.path.join(root, "core/components/plays/*/scripts/test_*.py")) +
                    glob.glob(os.path.join(root, "core/components/skills/*/scripts/test_*.py"))):
        if "/install-garura/" in t:
            continue
        r = run([sys.executable, os.path.relpath(t, root)], root)
        if r.returncode != 0:
            check(f"all: {os.path.relpath(t, root)} passes", False, r.stdout[-200:] + r.stderr[-200:])
    check("all: other play and skill tests ran", True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--out")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    for fn in (eval_ice_and_play, eval_scripts, eval_schemas, eval_next, eval_all):
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
