#!/usr/bin/env python3
"""test_grill_budget.py — the /shape-slice grilling tier and question split (#817).

    python3 core/components/plays/shape-slice/scripts/test_grill_budget.py
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "grill_budget.py")

PASSED = 0
FAILED = 0


def check(name, cond):
    global PASSED, FAILED
    if cond:
        PASSED += 1
        print(f"  [PASS] {name}")
    else:
        FAILED += 1
        print(f"  [FAIL] {name}")


def run(*args):
    p = subprocess.run([sys.executable, SCRIPT, *args], capture_output=True, text=True)
    out = json.loads(p.stdout) if p.returncode == 0 and p.stdout.strip() else None
    return p.returncode, out, p.stderr


def write(root, name, text):
    path = os.path.join(root, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


def questions(root, name, flags):
    items = [{"id": f"q{i}", "blocking": b, "text": f"question {i}"} for i, b in enumerate(flags)]
    return write(root, name, json.dumps(items)), items


def main():
    with tempfile.TemporaryDirectory() as root:
        for tier, budget in (("xs", 5), ("s", 12), ("m", 25), ("l", 45), ("xl", 70)):
            cfg = write(root, f"{tier}.yaml", f"shape-slice:\n  grill-tier: {tier}\n")
            code, out, _ = run("tier", "--config", cfg)
            check(f"tier {tier} gives budget {budget}", code == 0 and out == {"tier": tier, "budget": budget})

        cfg = write(root, "no-section.yaml", "craft-ice:\n  hitl: true\n")
        code, out, _ = run("tier", "--config", cfg)
        check("no shape-slice section gives tier m, 25", code == 0 and out == {"tier": "m", "budget": 25})
        cfg = write(root, "no-key.yaml", "shape-slice:\n  other: 1\n")
        code, out, _ = run("tier", "--config", cfg)
        check("no grill-tier key gives tier m, 25", code == 0 and out == {"tier": "m", "budget": 25})

        cfg = write(root, "bad.yaml", "shape-slice:\n  grill-tier: huge\n")
        code, out, err = run("tier", "--config", cfg)
        check("an unknown tier exits 2", code == 2 and out is None)
        check("the error names the allowed values", all(t in err for t in ("xs", "s", "m", "l", "xl")))

        flags = [False, True, False, True, False, False, True]
        path, items = questions(root, "mixed.json", flags)
        code, out, _ = run("split", "--questions", path, "--budget", "5")
        asked_ids = [q["id"] for q in out["asked"]] if out else []
        check("split keeps every blocking question",
              code == 0 and all(q["id"] in asked_ids for q in items if q["blocking"]))
        check("split never asks more than the budget when the blocking ones fit", len(asked_ids) == 5)
        check("non-blocking questions fill the budget in their given order",
              asked_ids == ["q0", "q1", "q2", "q3", "q6"])
        check("each question not asked is in assumptions",
              out is not None and [q["id"] for q in out["assumptions"]] == ["q4", "q5"])
        check("other fields are kept", out is not None and out["asked"][0]["text"] == "question 0")
        check("over_budget is false when the blocking ones fit", out is not None and out["over_budget"] is False)

        path, items = questions(root, "over.json", [True, False, True, True, False])
        code, out, _ = run("split", "--questions", path, "--budget", "2")
        check("blocking over budget: every blocking question is still asked",
              code == 0 and [q["id"] for q in out["asked"]] == ["q0", "q2", "q3"])
        check("blocking over budget: over_budget is true", out is not None and out["over_budget"] is True)
        check("blocking over budget: the rest are assumptions",
              out is not None and [q["id"] for q in out["assumptions"]] == ["q1", "q4"])

        path = write(root, "broken.json", json.dumps([{"id": "q0"}]))
        code, _, _ = run("split", "--questions", path, "--budget", "3")
        check("a question with no blocking flag exits 2", code == 2)
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
