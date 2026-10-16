#!/usr/bin/env python3
"""test_drive_contract.py — tests for the shared drive-contract checker and review-record writer.

Every play's stamped copy of check_drive_contract.py and write_drive_review.py must be
identical to the canonical one here.

    python3 test_drive_contract.py
"""
import contextlib
import glob
import io
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_drive_contract as cdc  # noqa: E402
import write_drive_review as wdr  # noqa: E402

REPO = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", ".."))
PASSED = 0
FAILED = 0
BRANCH = "feature/613-kickoff"


def check(name, cond):
    global PASSED, FAILED
    if cond:
        PASSED += 1
        print(f"  [PASS] {name}")
    else:
        FAILED += 1
        print(f"  [FAIL] {name}")
        if os.environ.get("PYTEST_CURRENT_TEST"):
            raise AssertionError(name)


def contract(tmp, **change):
    c = {"drive_run_id": "kickoff-1", "drive": "kickoff", "branch": BRANCH, "issue": 613,
         "review_dir": os.path.join(tmp, "review", "drive"),
         "inputs": {"vision": {"intents": ["grow-online-sales"]}},
         "answers": {"vision": {"goal": "Sell online without sign-up friction."}}}
    c.update(change)
    for k in [k for k, v in change.items() if v is None]:
        del c[k]
    path = os.path.join(tmp, f"contract-{len(os.listdir(tmp))}.json")
    with open(path, "w") as fh:
        json.dump(c, fh)
    return path


def run(tmp, *args):
    out = os.path.join(tmp, "run.json")
    rc = cdc.main(["--play", "vision", "--out", out, *args])
    return rc, (json.load(open(out)) if rc == 0 else None)


def test_checker():
    with tempfile.TemporaryDirectory() as tmp:
        rc, r = run(tmp, "--branch", "main")
        check("with no contract the run is by hand", rc == 0 and r["in_drive"] is False)
        rc, r = run(tmp, "--branch", BRANCH, "--contract", contract(tmp))
        check("a valid contract on its branch starts a drive run",
              rc == 0 and r["in_drive"] and r["drive_run_id"] == "kickoff-1" and r["issue"] == 613)
        check("the run carries only this play's inputs and answers",
              r["inputs"] == {"intents": ["grow-online-sales"]} and r["answers"]["goal"].startswith("Sell"))
        cases = (("the wrong branch", ["--branch", "main", "--contract", contract(tmp)], "switch to it first"),
                 ("a missing field", ["--branch", BRANCH, "--contract", contract(tmp, review_dir=None)], "missing review_dir"),
                 ("an issue that is not a number", ["--branch", BRANCH, "--contract", contract(tmp, issue="613")], "must be a number"),
                 ("answers that are not keyed by play", ["--branch", BRANCH, "--contract", contract(tmp, answers=["x"])], "keyed by play"))
        for label, args, why in cases:
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                rc = run(tmp, *args)[0]
            check(f"{label} is refused (exit 2) for that reason", rc == 2 and why in err.getvalue())
        bad = os.path.join(tmp, "bad.json")
        with open(bad, "w") as fh:
            fh.write("{not json")
        check("a contract that is not JSON is refused", run(tmp, "--branch", BRANCH, "--contract", bad)[0] == 2)


def test_review_writer():
    with tempfile.TemporaryDirectory() as tmp:
        _, r = run(tmp, "--branch", BRANCH, "--contract", contract(tmp))
        summary = os.path.join(tmp, "checkpoint.md")
        with open(summary, "w") as fh:
            fh.write("# Proposed seed\nThe domain, the capabilities and the profile.\n")
        guard = os.path.join(tmp, "guard-report.json")
        with open(guard, "w") as fh:
            fh.write('{"ok": true}')
        rc = wdr.main(["--run", os.path.join(tmp, "run.json"), "--summary", summary,
                       "--attach", f"guard={guard}", "--ts", "20261017-120000"])
        rec_path = os.path.join(r["review_dir"], "vision-20261017-120000.json")
        rec = json.load(open(rec_path)) if os.path.isfile(rec_path) else {}
        check("the review record is written for the drive, undecided",
              rc == 0 and rec.get("decided") is False and rec.get("drive_run_id") == "kickoff-1"
              and rec.get("attachments") == {"guard": guard})
        check("the summary is kept exactly as it would have been shown",
              open(os.path.join(r["review_dir"], "vision-20261017-120000.md")).read() == open(summary).read())
        check("a missing attached file writes nothing",
              wdr.main(["--run", os.path.join(tmp, "run.json"), "--summary", summary,
                        "--attach", "x=/nope", "--ts", "t2"]) == 2
              and not os.path.exists(os.path.join(r["review_dir"], "vision-t2.json")))
        run(tmp, "--branch", "main")
        check("a run by hand writes no drive record",
              wdr.main(["--run", os.path.join(tmp, "run.json"), "--summary", summary, "--ts", "t3"]) == 2)


def test_every_copy_is_identical():
    for name in ("check_drive_contract.py", "write_drive_review.py"):
        mine = open(os.path.join(HERE, name), "rb").read()
        copies = glob.glob(os.path.join(REPO, "core", "components", "plays", "*", "scripts", name))
        different = [c for c in copies if open(c, "rb").read() != mine]
        check(f"every play's {name} is identical to the canonical one ({len(copies)} copies)",
              copies and not different)


def main():
    for test in (test_checker, test_review_writer, test_every_copy_is_identical):
        print(test.__name__)
        test()
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
