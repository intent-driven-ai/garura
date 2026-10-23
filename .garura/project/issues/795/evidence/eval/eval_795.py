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


def eval_followups(root):
    # Product owner's yes on the open items (2026-10-23).
    import yaml
    persist = os.path.join(root, SCRIPTS, "persist_slice.py")
    if os.path.isfile(persist):
        tmp = tempfile.mkdtemp()
        po = os.path.join(tmp, "product-os"); os.makedirs(os.path.join(po, "intents"))
        open(os.path.join(po, "intents", "340.md"), "w").write("# x\n")
        sp = os.path.join(po, "_spine.yaml"); open(sp, "w").write(SPINE.format(slices="[]"))
        sj = os.path.join(tmp, "s.json")
        json.dump({"id": "sl-a", "slug": "a", "feature_refs": ["ft-pick-slot"], "vertical": "page", "intents": ["340"],
                   "surface": {"name": "page", "persona_ref": "p"}}, open(sj, "w"))
        r = run([sys.executable, persist, "--root", po, "--spine", sp, "--slice", sj], tmp)
        sl = [x for x in (yaml.safe_load(open(sp)).get("slices") or []) if x.get("id") == "sl-a"] if r.returncode == 0 else []
        check("follow-up: the spine slice carries its record pointer", sl and sl[0].get("record") == "slices/sl-a.yaml", (sl, r.stderr[-200:]))
    pn = read(root, "core/components/memory/standards/rules/pipeline-next.md")
    m = re.search(r"^\s*shape-slice:[^\n]*$", pn, re.M)
    check("follow-up: the Next-line map no longer sends shape-slice to build-epic",
          m and "build-epic" not in m.group(0) and "cut into" not in pn, m.group(0) if m else "")
    for src in ("complete-discovery", "discover-capabilities"):
        mm = re.search(r"^\s*%s:[^\n]*$" % src, pn, re.M)
        check(f"follow-up: after {src}, the Next line names /shape-slice (ADR 049), not the old chain",
              mm and "command: shape-slice" in mm.group(0), mm.group(0) if mm else "")
    check("follow-up: no Next entry sends a person to /shape-slice for a realized slice",
          not re.search(r"command:\s*shape-slice[^\n]*realized", pn), re.findall(r".{0,60}command:\s*shape-slice[^\n]*realized.{0,40}", pn))
    ag = read(root, "core/components/agents/product-os-keeper.md")
    for sk in ("author-epics", "check-cut-tensions", "rank-actions"):
        check(f"follow-up: product-os-keeper no longer lists {sk}", sk not in ag)
        check(f"follow-up: the {sk} skill is deleted", not os.path.exists(os.path.join(root, "core/components/skills", sk)))
    check("follow-up: the work-intelligence shelf is deleted",
          not os.path.exists(os.path.join(root, "core/components/memory/knowledge/work-intelligence")))
    check("follow-up: docs/command-chain.html is deleted", not os.path.exists(os.path.join(root, "docs/command-chain.html")))
    live = []
    for p in glob.glob(os.path.join(root, "core/**/*.*"), recursive=True) + [os.path.join(root, f) for f in ("CLAUDE.md", "AGENTS.md")]:
        if not os.path.isfile(p) or "rename-map.yaml" in p or "node_modules" in p:
            continue
        t = open(p, encoding="utf-8", errors="ignore").read()
        if re.search(r"^deprecated:\s*true", t, re.M):
            continue
        for n in ("rank-actions", "author-epics", "check-cut-tensions", "work-intelligence", "command-chain.html"):
            if n in t:
                live.append(f"{os.path.relpath(p, root)}: {n}")
    check("follow-up: no live file names a deleted part", not live, live[:10])
    ice = read(root, ICE)
    check("follow-up: the ICE's D4 check uses path:", re.search(r"D4[^\n]*\n\s*check:[^\n]*\bpath:", ice))
    n = len(glob.glob(os.path.join(root, "docs/adr/0*.md")))
    check("follow-up: CLAUDE.md states the right ADR count", re.search(r"\b%d ADRs\b" % n, read(root, "CLAUDE.md")), n)


def eval_round1(root):
    # Review round 1 of PR #840 (the product owner rejected; fix all findings).
    import yaml
    P = os.path.join(root, SCRIPTS)
    persist, check_s, rq, ra = (os.path.join(P, f) for f in ("persist_slice.py", "slice_check.py", "record_questions.py", "record_approval.py"))
    def model(slices="[]"):
        tmp = tempfile.mkdtemp(); po = os.path.join(tmp, "product-os")
        os.makedirs(os.path.join(po, "intents")); os.makedirs(os.path.join(po, "slices"))
        for i in ("340", "341"):
            open(os.path.join(po, "intents", i + ".md"), "w").write("# x\n")
        sp = os.path.join(po, "_spine.yaml"); open(sp, "w").write(SPINE.format(slices=slices))
        return tmp, po, sp
    full = {"id": "sl-a", "slug": "a", "name": "Self-booking", "outcome": "A patient books a free slot",
            "feature_refs": ["ft-pick-slot"], "vertical": "page", "intents": ["340"],
            "surface": {"id": "booking-page", "name": "page", "persona_ref": "patient", "user_action": "books a slot"}}
    # P2 reuse: an existing slice that serves the intent is reused even when the new shape differs.
    existing = """
  - id: sl-a
    slug: a
    feature_refs: [ft-pick-slot]
    vertical: page
    intents: ["340"]
    record: slices/sl-a.yaml"""
    tmp, po, sp = model(existing)
    open(os.path.join(po, "slices", "sl-a.yaml"), "w").write(yaml.safe_dump({"slice": {"id": "sl-a", "slug": "a", "intents": ["340"]}}))
    shaped = dict(full); shaped["feature_refs"] = ["ft-pick-slot", "ft-reminder"]; shaped["vertical"] = "page2"; shaped["intents"] = ["341"]
    sj = os.path.join(tmp, "s.json"); json.dump(shaped, open(sj, "w"))
    r = run([sys.executable, persist, "--root", po, "--spine", sp, "--slice", sj, "--reuse", "sl-a"], tmp)
    sls = (yaml.safe_load(open(sp)) or {}).get("slices") or []
    check("round1: reuse of a serving slice works when the new shape differs (exit 0, one slice)", r.returncode == 0 and len(sls) == 1, (r.returncode, r.stderr[-300:]))
    if sls:
        check("round1: the reused slice keeps its features and surface", sls[0].get("feature_refs") == ["ft-pick-slot"] and sls[0].get("vertical") == "page", sls[0])
        check("round1: the reused slice gains the intent, appended", sls[0].get("intents") == ["340", "341"], sls[0])
    check("round1: the run reports how the new shape differs from the reused slice", re.search(r"differ", r.stdout, re.I), r.stdout[-300:])
    rec = os.path.join(po, "slices", "sl-a.yaml")
    check("round1: the reused slice's record gains the intent", os.path.isfile(rec) and "341" in open(rec).read())
    # P2 record matches slice.yaml v2, and the slice check tests the record.
    tmp, po, sp = model()
    sj = os.path.join(tmp, "s.json"); json.dump(full, open(sj, "w"))
    r = run([sys.executable, persist, "--root", po, "--spine", sp, "--slice", sj], tmp)
    rec = os.path.join(po, "slices", "sl-a.yaml")
    recd = yaml.safe_load(open(rec)) if os.path.isfile(rec) else {}
    sl, su = (recd or {}).get("slice") or {}, (recd or {}).get("surface") or (recd or {}).get("slice", {}).get("surface") or {}
    for k in ("name", "outcome", "intents"):
        check(f"round1: the record holds slice.{k}", k in sl, recd)
    for k in ("id", "persona_ref", "user_action"):
        check(f"round1: the record holds surface.{k}", k in su, recd)
    schema = read(root, SLICE_SCHEMA)
    for k in ("name", "outcome", "intents", "persona_ref", "user_action"):
        check(f"round1: slice.yaml describes {k}", k in schema)
    out = os.path.join(tmp, "check.json")
    r = run([sys.executable, check_s, "--root", po, "--spine", sp, "--out", out], tmp)
    ok_good = os.path.isfile(out) and json.load(open(out)).get("valid") is True
    if os.path.isfile(rec):
        d = yaml.safe_load(open(rec)); (d.get("surface") or d["slice"].get("surface") or {}).pop("persona_ref", None)
        open(rec, "w").write(yaml.safe_dump(d))
    r2 = run([sys.executable, check_s, "--root", po, "--spine", sp, "--out", out], tmp)
    ok_bad = os.path.isfile(out) and json.load(open(out)).get("valid") is False
    check("round1: the slice check passes a good record and fails one with no tester", ok_good and ok_bad, (r.stdout[-200:], r2.stdout[-200:]))
    # P4 ids and paths stay inside the model.
    tmp, po, sp = model()
    bad = dict(full); bad["id"] = "../../etc/x"
    sj = os.path.join(tmp, "s.json"); json.dump(bad, open(sj, "w"))
    r = run([sys.executable, persist, "--root", po, "--spine", sp, "--slice", sj], tmp)
    check("round1: persist_slice refuses an id that leaves the model (exit 2)", r.returncode == 2, (r.returncode, r.stderr[-200:]))
    check("round1: persist_slice writes the spine safely (temp file + replace)", "os.replace" in read(root, SCRIPTS + "/persist_slice.py"))
    check("round1: persist_fills refuses paths that leave the model", re.search(r"\.\.|outside|relpath|commonpath", read(root, SCRIPTS + "/persist_fills.py")))
    # P3 the question record.
    src = read(root, SCRIPTS + "/record_questions.py")
    check("round1: record_questions has subcommands for the open list and the answers", re.search(r"open-list|open_list", src) and re.search(r"answers", src))
    tmp = tempfile.mkdtemp()
    recq = os.path.join(tmp, "grounding-questions.md")
    help_ = run([sys.executable, rq, "--help"], tmp).stdout + run([sys.executable, rq, "check", "--help"], tmp).stdout
    check("round1: record_questions check is documented", "check" in help_, help_[-300:])
    check("round1: record_questions matches an answered question by its text, not only its id",
          re.search(r"normali[sz]|lower\(\)|casefold|question text|same question", src, re.I))
    check("round1: record_questions check fails on an unanswered asked question",
          re.search(r"unanswered", src) and re.search(r"(sys\.exit\(1\)|return 1|exit 1)", src))
    # P3 a script gate before the commit; memory trace; pointers.
    check("round1: record_approval has a verify step that fails unless the decision is yes",
          re.search(r"verify", read(root, SCRIPTS + "/record_approval.py")))
    sk = read(root, SKILL)
    check("round1: the play runs the approval verify before it commits", re.search(r"record_approval\.py verify", sk))
    check("round1: the play keeps a memory trace for its decisions (memory.py cite)", "memory.py cite" in sk or "memory.py\" cite" in sk or re.search(r"memory\.py[^\n]{0,40}cite", sk))
    check("round1: the play points to #838 for the author-slice skill", "#838" in sk)
    check("round1: the play's text no longer says the spine entry has exactly 5 fields", not re.search(r"exactly (5|five) fields", sk, re.I))
    check("round1: the play counts template-manager as a utility agent", re.search(r"utility_agents \| [1-9]", sk) and "template-manager" in sk)
    check("round1: a 'change' undoes this run's intent-page edits (Touches lines)", re.search(r"change[^\n]{0,200}(Touches|intent page)", sk, re.I | re.S))
    # Memory and rule files.
    sp_schema = read(root, SPINE_SCHEMA)
    check("round1: spine.yaml marks the domain slices/ folders as the older chain", re.search(r"older chain|old chain", sp_schema, re.I))
    pn = read(root, "core/components/memory/standards/rules/pipeline-next.md")
    check("round1: the Next map says which shape loop is live", re.search(r"(older|old) chain", pn, re.I))
    check("round1: the cardinal-rule table lists shape-slice", "shape-slice" in read(root, "core/components/memory/standards/rules/no-unbacked-recommendation.md"))
    uq = read(root, "core/components/memory/standards/rules/user-questions.md")
    check("round1: user-questions.md lists the fields the play adds", all(k in uq for k in ("blocking", "proposed_answer", "basis")))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--out")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    for fn in (eval_ice_and_play, eval_scripts, eval_schemas, eval_next, eval_followups, eval_round1, eval_all):
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
