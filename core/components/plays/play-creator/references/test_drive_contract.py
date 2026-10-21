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
    if rc != 0:
        return rc, None
    with open(out) as fh:
        return rc, json.load(fh)


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
                 ("an issue that is not a number", ["--branch", BRANCH, "--contract", contract(tmp, issue="613")], "positive issue number"),
                 ("answers that are not keyed by play", ["--branch", BRANCH, "--contract", contract(tmp, answers=["x"])], "keyed by play"),
                 ("an issue that is true or false", ["--branch", BRANCH, "--contract", contract(tmp, issue=True)], "positive issue number"),
                 ("an issue that is zero", ["--branch", BRANCH, "--contract", contract(tmp, issue=0)], "positive issue number"),
                 ("a review_dir that is not text", ["--branch", BRANCH, "--contract", contract(tmp, review_dir=["a"])], "non-empty text"))
        for label, args, why in cases:
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                rc = run(tmp, *args)[0]
            check(f"{label} is refused (exit 2) for that reason", rc == 2 and why in err.getvalue())
        nul = contract(tmp, inputs=None)
        with open(nul) as fh:
            c = json.load(fh)
        c["inputs"] = None
        with open(nul, "w") as fh:
            json.dump(c, fh)
        rc, r = run(tmp, "--branch", BRANCH, "--contract", nul)
        check("a null optional `inputs` is read as none", rc == 0 and r["inputs"] == {})
        lst = os.path.join(tmp, "list.json")
        with open(lst, "w") as fh:
            fh.write("[1, 2]")
        check("a contract that is a list is refused", run(tmp, "--branch", BRANCH, "--contract", lst)[0] == 2)
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
        rec = {}
        if os.path.isfile(rec_path):
            with open(rec_path) as fh:
                rec = json.load(fh)
        check("the review record is written for the drive, undecided",
              rc == 0 and rec.get("decided") is False and rec.get("drive_run_id") == "kickoff-1"
              and rec.get("attachments") == {"guard": guard})
        with open(os.path.join(r["review_dir"], "vision-20261017-120000.md")) as a, open(summary) as b:
            check("the summary is kept exactly as it would have been shown", a.read() == b.read())
        check("a missing attached file writes nothing",
              wdr.main(["--run", os.path.join(tmp, "run.json"), "--summary", summary,
                        "--attach", "x=/nope", "--ts", "t2"]) == 2
              and not os.path.exists(os.path.join(r["review_dir"], "vision-t2.json")))
        runp = os.path.join(tmp, "run.json")
        check("a missing summary writes nothing",
              wdr.main(["--run", runp, "--summary", "/nope.md", "--ts", "t4"]) == 2)
        for ts in ("../x", "", ".hidden"):
            check(f"a timestamp like `{ts}` is refused",
                  wdr.main(["--run", runp, "--summary", summary, "--ts", ts]) == 2)
        check("re-running with the same timestamp rewrites the same record",
              wdr.main(["--run", runp, "--summary", summary, "--ts", "20261017-120000"]) == 0
              and len([f for f in os.listdir(r["review_dir"]) if f.startswith("vision-20261017-120000")]) == 2)
        with open(runp) as fh:
            broken = json.load(fh)
        del broken["drive_run_id"]
        brokenp = os.path.join(tmp, "broken-run.json")
        with open(brokenp, "w") as fh:
            json.dump(broken, fh)
        check("a run record lacking a field writes nothing",
              wdr.main(["--run", brokenp, "--summary", summary, "--ts", "t5"]) == 2
              and not os.path.exists(os.path.join(r["review_dir"], "vision-t5.md")))
        with open(brokenp, "w") as fh:
            json.dump(dict(broken, drive_run_id="k", in_drive="false"), fh)
        check("in_drive as the text 'false' is not a drive run",
              wdr.main(["--run", brokenp, "--summary", summary, "--ts", "t6"]) == 2)
        citations = os.path.join(tmp, "citations.json")
        with open(citations, "w") as fh:
            json.dump({"ok": True, "contract_version": "4", "command": "citations", "records": [
                {"citation_id": "cite-20261019-001", "issue": 613, "play": "/vision", "question": "Guest checkout?",
                 "answer": "Yes.", "decided_by": "product-os-keeper (/vision)", "decided_at": "2026-10-19T09:00:00Z",
                 "trace": [{"asked": "What has the product model decided?", "found": "Guest checkout at launch.",
                            "source": {"tier": "garura", "path": "product-os/checkout/checkout/capability.md",
                                       "start": 12, "end": 12, "fingerprint": "sha256:" + "0" * 64}}],
                 "from_update": None}],
                "problems": []}, fh)
        rc = wdr.main(["--run", runp, "--summary", summary, "--decisions", citations, "--ts", "t7"])
        with open(os.path.join(r["review_dir"], "vision-t7.json")) as fh:
            rec7 = json.load(fh)
        check("the review record carries each decision and its trace",
              rc == 0 and [d["question"] for d in rec7["decisions"]] == ["Guest checkout?"]
              and rec7["decisions"][0]["trace"][0]["source"]["tier"] == "garura" and rec7["decision_problems"] == [])
        with open(citations) as fh:
            good = json.load(fh)
        v5 = os.path.join(tmp, "citations-v5.json")
        with open(v5, "w") as fh:
            json.dump(dict(good, contract_version="5"), fh)
        check("a citations answer from contract v5 (the current tool) is written too",
              wdr.main(["--run", runp, "--summary", summary, "--decisions", v5, "--ts", "t10"]) == 0)
        bare = os.path.join(tmp, "citations-bare.json")
        with open(bare, "w") as fh:
            json.dump(dict(good, records=[dict(good["records"][0], play="vision")]), fh)
        check("a decision recorded as `vision` (no slash) is this play's too",
              wdr.main(["--run", runp, "--summary", summary, "--decisions", bare, "--ts", "t11"]) == 0)
        for name, bad in (("another play", dict(good, records=[dict(good["records"][0], play="/understand")])),
                          ("another play, no slash", dict(good, records=[dict(good["records"][0], play="understand")])),
                          ("another issue", dict(good, records=[dict(good["records"][0], issue=999)])),
                          ("records that are not a list", dict(good, records="oops")),
                          ("a record that is not an object", dict(good, records=[1])),
                          ("an older contract", dict(good, contract_version="3"))):
            wrong = os.path.join(tmp, "wrong.json")
            with open(wrong, "w") as fh:
                json.dump(bad, fh)
            check(f"a citations answer with {name} writes nothing",
                  wdr.main(["--run", runp, "--summary", summary, "--decisions", wrong, "--ts", "t9"]) == 2)
        not_citations = os.path.join(tmp, "not-citations.json")
        with open(not_citations, "w") as fh:
            fh.write('{"ok": true, "command": "search"}')
        check("a decisions file that is not a citations answer writes nothing",
              wdr.main(["--run", runp, "--summary", summary, "--decisions", not_citations, "--ts", "t8"]) == 2
              and not os.path.exists(os.path.join(r["review_dir"], "vision-t8.json")))
        before = sorted(os.listdir(r["review_dir"]))
        run(tmp, "--branch", "main")
        check("a run by hand writes no drive record",
              wdr.main(["--run", runp, "--summary", summary, "--ts", "t3"]) == 2
              and sorted(os.listdir(r["review_dir"])) == before)


def test_every_copy_is_identical():
    for name in ("check_drive_contract.py", "write_drive_review.py"):
        with open(os.path.join(HERE, name), "rb") as fh:
            mine = fh.read()
        copies = glob.glob(os.path.join(REPO, "core", "components", "plays", "*", "scripts", name))
        different = []
        for c in copies:
            with open(c, "rb") as fh:
                if fh.read() != mine:
                    different.append(c)
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
