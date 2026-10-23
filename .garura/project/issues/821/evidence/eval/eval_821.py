#!/usr/bin/env python3
"""
eval_821.py — the eval for the grouped change #821 + #825 + #829 (plan 788).

Written before the build. It must fail before the build and pass after it.
A builder never reads this file.

    python3 .garura/project/issues/821/evidence/eval/eval_821.py [--root .] [--out result.json]

Exit 0 when every check passes, 1 when one fails.
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

RULE = "core/components/memory/standards/rules/asking-a-person.md"
EDIT_ONTOLOGY = "core/components/plays/edit-ontology/SKILL.md"
AUTHOR_SKILL = "core/components/skills/author-product-ontology/SKILL.md"
LINTER = "core/tools/lint-components/index.js"
LINT_TESTS = "core/tools/lint-components/test"
TEMPLATES = "core/components/memory/standards/templates"
APPROVAL = TEMPLATES + "/approval-prompt.md"
SPINE_SCHEMA = "core/components/memory/standards/schemas/product-os/spine.yaml"
LINT_GROUNDING = "core/components/plays/discover-domains/scripts/lint_grounding.py"

results = []


def check(name, ok, detail=""):
    results.append({"check": name, "ok": bool(ok), "detail": str(detail)[-400:]})


def read(root, rel):
    p = os.path.join(root, rel)
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def run(root, args):
    return subprocess.run(args, cwd=root, capture_output=True, text=True)


def lint(root, target):
    r = run(root, ["node", LINTER, "--target", target])
    try:
        return json.loads(r.stdout).get("violations", []), r
    except ValueError:
        return None, r


def write_play(base, name, body):
    d = os.path.join(base, "plays", name)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "SKILL.md"), "w") as fh:
        fh.write(body)


ASKING_PLAY = """---
name: {name}
description: Ask the product owner which kinds change, and record the answer.
user-invocable: true
---

# {name}

## Role

You are the orchestrator.

## Workflow

**Step 2 — Checkpoint: the kinds** · Owner: play · Checkpoint (class: standard, **pinned**)
Show the draft to the product owner and ask them to type **yes**, or **change: <what>**.
Wait for the typed answer. Record it verbatim.
{pointer}
"""


def mentions_rule(v):
    return "asking-a-person" in (v.get("rule", "") + " " + v.get("message", "")).lower()


def eval_821(root):
    # The lint check: a play that asks a person must point to the rule.
    with tempfile.TemporaryDirectory() as tmp:
        write_play(tmp, "ask-without-pointer", ASKING_PLAY.format(name="ask-without-pointer", pointer=""))
        write_play(tmp, "ask-with-pointer", ASKING_PLAY.format(
            name="ask-with-pointer",
            pointer="Each question follows `standards/rules/asking-a-person.md`."))
        vs, r = lint(root, tmp)
        if vs is None:
            check("821: linter runs on a fixture target", False, r.stdout + r.stderr)
        else:
            bad = [v for v in vs if "ask-without-pointer" in v.get("file", "") and mentions_rule(v)]
            good = [v for v in vs if "ask-with-pointer" in v.get("file", "") and mentions_rule(v)]
            check("821: a play that asks a person and does not point to the rule fails", bad, vs)
            check("821: the failure is an error", bad and all(v.get("severity") == "error" for v in bad), bad)
            check("821: a play that points to the rule passes that check", not good, good)
    vs, r = lint(root, "core/components")
    if vs is None:
        check("821: linter runs on core/components", False, r.stdout + r.stderr)
    else:
        for name in ("edit-ontology",):
            hits = [v for v in vs if f"/plays/{name}/" in v.get("file", "") and mentions_rule(v)]
            check(f"821: {name} passes the asking-a-person check", not hits, hits)
        hits = [v for v in vs if "/author-product-ontology/" in v.get("file", "") and mentions_rule(v)]
        check("821: author-product-ontology passes the asking-a-person check", not hits, hits)
    # A test for the new check exists and passes.
    tests = sorted(glob.glob(os.path.join(root, LINT_TESTS, "*.test.js")))
    rel = [os.path.relpath(t, root) for t in tests]
    named = [t for t in tests if "asking-a-person" in open(t).read()]
    check("821: a linter test covers the asking-a-person check", named, rel)
    for t in named:
        r = run(root, ["node", os.path.relpath(t, root)])
        check(f"821: {os.path.basename(t)} passes", r.returncode == 0, r.stdout + r.stderr)
    for t in tests:
        if t in named:
            continue
        r = run(root, ["node", os.path.relpath(t, root)])
        check(f"all: {os.path.basename(t)} still passes", r.returncode == 0, r.stdout + r.stderr)
    # The play hands the rule to its agent, and the skill takes it as an input.
    play = read(root, EDIT_ONTOLOGY)
    contracts = re.findall(r"\{\s*\"task\":.*?\"task_id\":\s*\"edit-ontology-(?:scope|kinds|links)\"", play, re.S)
    check("821: edit-ontology has its scope/kinds/links contracts", len(contracts) >= 1, len(contracts))
    check("821: the Step 1 contract hands the rule to the agent",
          contracts and "asking-a-person" in contracts[0], contracts[:1])
    skill = read(root, AUTHOR_SKILL)
    inp = re.search(r"^## Input.*?(?=^## )", skill, re.S | re.M)
    check("821: author-product-ontology lists the rule as an input",
          inp and "asking-a-person" in inp.group(0), (inp.group(0) if inp else "no ## Input")[:300])


def eval_825(root):
    t = read(root, APPROVAL)
    check("825: the approval template exists", bool(t))
    check("825: the approval template has no Tether / Orbit / Vanish",
          not re.search(r"\b(tether|orbit|vanish)", t, re.I), re.findall(r"\b(?:tether|orbit|vanish)\w*", t, re.I))
    for part in ("Question", "Answer", "Why it matters", "Example"):
        check(f"825: the approval template has the part '{part}'", part in t)
    check("825: the approval template points to the asking-a-person rule", "asking-a-person.md" in t)
    left = []
    for p in sorted(glob.glob(os.path.join(root, TEMPLATES, "*.md"))):
        if re.search(r"\b(Tether|Orbit|Vanish)\b", open(p).read()):
            left.append(os.path.basename(p))
    check("825: no template names Tether / Orbit / Vanish", not left, left)
    check("825: the asking-a-person rule still links the approval template", "approval-prompt.md" in read(root, RULE))


SPINE = """domains: []
capabilities: []
features: []
epics: []
slices:
  - id: slice-self-booking
    slug: self-booking
    intents: ["{intent}"]
    feature_refs: []
"""


def lint_spine(root, script, intent, make_page):
    with tempfile.TemporaryDirectory() as tmp:
        if make_page:
            os.makedirs(os.path.join(tmp, "intents"))
            with open(os.path.join(tmp, "intents", f"{intent}.md"), "w") as fh:
                fh.write("# Patients book their own appointments online\n")
        sp = os.path.join(tmp, "_spine.yaml")
        with open(sp, "w") as fh:
            fh.write(SPINE.format(intent=intent))
        r = run(root, [sys.executable, script, "--root", tmp, "--spine", sp])
        try:
            out = json.loads(r.stdout)
        except ValueError:
            return None, r
        return [e for e in out.get("errors", []) if "self-booking" in e and "intent" in e.lower()], r


def eval_829(root):
    schema = read(root, SPINE_SCHEMA)
    m = re.search(r"^slices:\n(.*?)(?=^\S)", schema, re.S | re.M)
    check("829: the spine schema's slice entry has an intents field",
          m and re.search(r"^\s+intents:", m.group(1), re.M), (m.group(1) if m else "no slices block")[:300])
    errs, r = lint_spine(root, LINT_GROUNDING, "340", make_page=False)
    if errs is None:
        check("829: lint_grounding runs on a fixture spine", False, r.stdout + r.stderr)
    else:
        check("829: a slice naming a business intent that does not exist fails", errs, r.stdout)
    errs, r = lint_spine(root, LINT_GROUNDING, "340", make_page=True)
    check("829: a slice naming a business intent that exists passes",
          errs is not None and not errs, (errs, r.stdout[-300:]))
    copies = sorted(glob.glob(os.path.join(root, "core/components/plays/*/scripts/lint_grounding.py")))
    digests = {hashlib.sha256(open(p, "rb").read()).hexdigest() for p in copies}
    check("829: every copy of lint_grounding.py is the same", len(copies) >= 2 and len(digests) == 1,
          f"{len(copies)} copies, {len(digests)} versions")
    for t in sorted(glob.glob(os.path.join(root, "core/components/plays/*/scripts/test_lint_*.py"))):
        r = run(root, [sys.executable, os.path.relpath(t, root)])
        check(f"all: {os.path.relpath(t, root)} passes", r.returncode == 0, r.stdout + r.stderr)
    named = [t for t in glob.glob(os.path.join(root, "core/components/plays/*/scripts/test_lint_*.py"))
             if re.search(r"slices[\"']?\s*:[\s\S]{0,400}?intents", open(t).read())]
    check("829: a lint_grounding test covers a slice's intents", named)


OLD_WORDS = re.compile(r"\b(Tether|Orbit|Vanish)(e?s)?\b")


def eval_round2(root):
    # HA1: the edit-ontology ICE source carries the asking-a-person flow, and the play is rebuilt from it.
    ice = read(root, "core/components/plays/edit-ontology/reference/ice.md")
    check("HA1: the edit-ontology ICE names the asking-a-person rule", "asking-a-person" in ice)
    play = read(root, EDIT_ONTOLOGY)
    fp = re.search(r"fingerprint \| sha256:([0-9a-f]{64})", play)
    real = hashlib.sha256(open(os.path.join(root, "core/components/plays/edit-ontology/reference/ice.md"), "rb").read()).hexdigest()
    check("HA1: the play's fingerprint matches its ICE", fp and fp.group(1) == real, (fp.group(1) if fp else None, real))
    check("HA1: the rebuilt play still hands the rule to its agent", "asking_rule" in play and "asking-a-person" in play)
    # MC1: no Tether / Orbit / Vanish outside the ADRs (ADRs record past decisions and stay as written).
    left = []
    for base in ("core", "docs"):
        for dp, _d, fs in os.walk(os.path.join(root, base)):
            if "/docs/adr" in dp or "node_modules" in dp or "__pycache__" in dp:
                continue
            for f in fs:
                if f.endswith((".md", ".yaml", ".yml", ".py", ".js", ".json")):
                    p = os.path.join(dp, f)
                    if OLD_WORDS.search(open(p, encoding="utf-8", errors="ignore").read()):
                        left.append(os.path.relpath(p, root))
    for f in ("AGENTS.md", "CLAUDE.md"):
        if OLD_WORDS.search(read(root, f)):
            left.append(f)
    check("MC1: no file outside the ADRs names Tether / Orbit / Vanish", not left, left)
    # HC1: one main copy of lint_grounding.py, and the linter fails a copy that differs from it.
    main_copy = "core/components/plays/create-play/references/lint_grounding.py"
    check("HC1: a main copy of lint_grounding.py exists", os.path.exists(os.path.join(root, main_copy)))
    if os.path.exists(os.path.join(root, main_copy)):
        want = hashlib.sha256(open(os.path.join(root, main_copy), "rb").read()).hexdigest()
        copies = sorted(glob.glob(os.path.join(root, "core/components/plays/*/scripts/lint_grounding.py")))
        off = [os.path.relpath(p, root) for p in copies if hashlib.sha256(open(p, "rb").read()).hexdigest() != want]
        check("HC1: every play's copy matches the main copy", copies and not off, off)
        with tempfile.TemporaryDirectory() as tmp:
            ref = os.path.join(tmp, "plays", "create-play", "references")
            os.makedirs(ref)
            open(os.path.join(ref, "lint_grounding.py"), "w").write("print('main')\n")
            for name, body in (("same-play", "print('main')\n"), ("drift-play", "print('drifted')\n")):
                write_play(tmp, name, ASKING_PLAY.format(name=name, pointer="See `standards/rules/asking-a-person.md`."))
                sd = os.path.join(tmp, "plays", name, "scripts")
                os.makedirs(sd)
                open(os.path.join(sd, "lint_grounding.py"), "w").write(body)
            vs, r = lint(root, tmp)
            if vs is None:
                check("HC1: linter runs on a fixture with copies", False, r.stdout + r.stderr)
            else:
                hit = lambda n: [v for v in vs if f"/plays/{n}/" in v.get("file", "") and "lint_grounding" in (v.get("rule", "") + v.get("message", ""))]
                check("HC1: the linter fails a copy that differs from the main copy", hit("drift-play"), vs)
                check("HC1: the linter passes a copy that matches", not hit("same-play"), hit("same-play"))
    vs, r = lint(root, "core/components")
    if vs is not None:
        stale = [v for v in vs if "lint_grounding" in (v.get("rule", "") + v.get("message", ""))]
        check("HC1: no copy on core/components differs from the main copy", not stale, stale)


def eval_hb2(root):
    # HB2: the check reads only the play's workflow, not its description or its notes, and the
    # pointer counts only where the play works (its workflow), not in a reference list.
    desc_only = """---
name: {name}
description: Land one epic on a person's typed approval at the gate.
user-invocable: true
---

# {name}

## Workflow

**Step 1 — Merge** · Owner: play (script)
Run the merge script. This play has no checkpoint of its own.
"""
    pointer_in_refs = ASKING_PLAY.format(name="{name}", pointer="") + """
## References

- `standards/rules/asking-a-person.md`
"""
    with tempfile.TemporaryDirectory() as tmp:
        write_play(tmp, "desc-only", desc_only.format(name="desc-only"))
        write_play(tmp, "pointer-in-refs", pointer_in_refs.replace("{name}", "pointer-in-refs"))
        write_play(tmp, "pointer-in-workflow", ASKING_PLAY.format(
            name="pointer-in-workflow", pointer="Each question follows `standards/rules/asking-a-person.md`."))
        vs, r = lint(root, tmp)
        if vs is None:
            check("HB2: linter runs on the fixtures", False, r.stdout + r.stderr)
            return
        hit = lambda n: [v for v in vs if f"/plays/{n}/" in v.get("file", "") and mentions_rule(v)]
        check("HB2: a play that asks no one in its workflow is not flagged (description only)", not hit("desc-only"), hit("desc-only"))
        check("HB2: a pointer only in a reference list does not pass", hit("pointer-in-refs"), vs)
        check("HB2: a pointer in the workflow passes", not hit("pointer-in-workflow"), hit("pointer-in-workflow"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--out")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    for fn in (eval_821, eval_825, eval_829, eval_round2, eval_hb2):
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
