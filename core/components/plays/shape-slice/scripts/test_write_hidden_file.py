#!/usr/bin/env python3
"""test_write_hidden_file.py — the slice's hidden file of /shape-slice (C15, F15, D6).

    python3 core/components/plays/shape-slice/scripts/test_write_hidden_file.py
"""
import json
import os
import subprocess
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
PASSED = 0
FAILED = 0
THIN = ("Thin: proposed by `/shape-slice` from the person's answers; deepen with "
        "`/discover-capabilities`.")


def check(name, cond):
    global PASSED, FAILED
    if cond:
        PASSED += 1
        print(f"  [PASS] {name}")
    else:
        FAILED += 1
        print(f"  [FAIL] {name}")


def run(*args):
    p = subprocess.run([sys.executable, os.path.join(HERE, "write_hidden_file.py"), *args],
                       capture_output=True, text=True)
    return p.returncode, p.stderr


def write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        if isinstance(data, str):
            fh.write(data)
        elif path.endswith(".json"):
            json.dump(data, fh)
        else:
            yaml.safe_dump(data, fh, sort_keys=False)
    return path


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def page(kind, name, fails, thin=False):
    ice = "".join(f"- Fails if: {f}\n" for f in fails)
    return (f"# {kind}: {name}\n\n## What it does\nText.\n\n" + (THIN + "\n\n" if thin else "")
            + "## Agent intent (ICE)\n- Goal: a patient books a visit with no call.\n" + ice)


def model(tmp):
    root = os.path.join(tmp, "po")
    write(os.path.join(root, "care/booking/capability.md"),
          page("Capability", "Booking", ["a visit is booked with no patient name."]))
    write(os.path.join(root, "care/booking/pick-slot/feature.md"),
          page("Feature", "Pick a free slot", ["a slot is booked twice.", "a past slot is offered."],
               thin=True))
    write(os.path.join(root, "care/booking/remind/feature.md"), page("Feature", "Send a reminder", []))
    spine = {"domains": [{"id": "dm-care", "slug": "care", "doc": "care/domain.md"}],
             "capabilities": [{"id": "cap-booking", "slug": "booking", "domain": "dm-care",
                               "doc": "care/booking/capability.md"}],
             "features": [{"id": "ft-pick", "slug": "pick", "capability": "cap-booking",
                           "doc": "care/booking/pick-slot/feature.md", "metadata": {"thin": True}},
                          {"id": "ft-remind", "slug": "remind", "capability": "cap-booking",
                           "doc": "care/booking/remind/feature.md"}],
             "slices": [{"id": "sl-self-booking", "slug": "self-booking",
                         "feature_refs": ["ft-pick", "ft-remind"], "vertical": "the booking screen",
                         "intents": ["bi-340"], "record": "slices/sl-self-booking.yaml"}]}
    return root, write(os.path.join(root, "_spine.yaml"), spine), spine


REC = {"when": "two bookings sit on one slot.", "way_back": "keep the first booking and free the second.",
       "who_fixes": "the builder can fix this alone"}


def recoveries(lines, override=None):
    out = []
    for e in lines["entries"]:
        rs = [dict(REC, line=ln["id"]) for ln in e["lines"]]
        out.append({"feature": e["feature"], "recoveries": rs})
    if override:
        override(out)
    return {"entries": out}


def main():
    with tempfile.TemporaryDirectory() as tmp:
        root, spine, data = model(tmp)
        plans = os.path.join(tmp, "plans")
        lines_p = os.path.join(tmp, "hidden-lines.json")
        code, _ = run("lines", "--root", root, "--spine", spine, "--slice-id", "sl-self-booking",
                      "--plans-root", plans, "--out", lines_p)
        lines = json.loads(read(lines_p))
        check("lines: the home plan is the first intent's number, and the path is its evals folder",
              code == 0 and lines["plan_id"] == "340"
              and lines["path"] == "340/evals/self-booking/failure-and-recovery.md")
        pick, remind = lines["entries"]
        check("lines: each feature has the lines of its ICE and of its capability's ICE",
              [ln["from"] for ln in pick["lines"]] == ["feature", "feature", "capability"]
              and [ln["id"] for ln in pick["lines"]] == ["F1", "F2", "F3"])
        check("lines: ids are unique in the whole file",
              [ln["id"] for ln in remind["lines"]] == ["F4"])
        check("lines: a thin feature ICE is named thin", pick["thin"] == ["feature"]
              and remind["thin"] == [])
        check("lines: nothing is kept when no file exists", not pick["kept"] and not remind["kept"])

        rec_p = write(os.path.join(tmp, "rec-missing.json"),
                      recoveries(lines, lambda out: out[0]["recoveries"].pop()))
        out_p = os.path.join(tmp, "hidden-write.json")
        code, err = run("write", "--lines", lines_p, "--recoveries", rec_p, "--plans-root", plans,
                        "--out", out_p)
        hidden = os.path.join(plans, lines["path"])
        check("write: a line with no recovery is refused (exit 2), nothing written",
              code == 2 and "no recovery" in err and not os.path.exists(hidden))
        rec_p = write(os.path.join(tmp, "rec-two.json"),
                      recoveries(lines, lambda out: out[0]["recoveries"].append(dict(REC, line="F1"))))
        code, err = run("write", "--lines", lines_p, "--recoveries", rec_p, "--plans-root", plans,
                        "--out", out_p)
        check("write: a line with two recoveries is refused", code == 2 and "two recoveries" in err)
        rec_p = write(os.path.join(tmp, "rec-who.json"),
                      recoveries(lines, lambda out: out[0]["recoveries"][0].update(who_fixes="the team")))
        code, err = run("write", "--lines", lines_p, "--recoveries", rec_p, "--plans-root", plans,
                        "--out", out_p)
        check("write: any other 'who fixes' text is refused", code == 2 and "who fixes" in err)
        bad_lines = write(os.path.join(tmp, "bad-lines.json"), dict(lines, path="../outside.md"))
        code, err = run("write", "--lines", bad_lines, "--recoveries", rec_p, "--plans-root", plans,
                        "--out", out_p)
        check("write: a path outside plans-root is refused", code == 2 and "leaves" in err)

        person = lambda out: out[0]["recoveries"][0].update(who_fixes="a person must decide")  # noqa: E731
        rec_p = write(os.path.join(tmp, "rec.json"), dict(recoveries(lines, person), vague=["F1"]))
        code, _ = run("write", "--lines", lines_p, "--recoveries", rec_p, "--plans-root", plans,
                      "--out", out_p)
        text = read(hidden) if os.path.isfile(hidden) else ""
        check("write: a vague line is counted by feature, with no line id",
              json.loads(read(out_p))["vague"] == [{"feature": "ft-pick", "count": 1}])
        check("write: the folder is made and the file written, with no plan file",
              code == 0 and os.path.isfile(hidden) and not os.path.exists(os.path.join(plans, "340.yaml")))
        check("write: one heading per feature, the failure lines and one recovery each",
              "## ft-pick: Pick a free slot" in text and "## ft-remind: Send a reminder" in text
              and "- F1 (from the feature ICE): a slot is booked twice." in text
              and "- F3 (from the capability ICE): a visit is booked with no patient name." in text
              and text.count("- For F") == 4 and "  - Who fixes: a person must decide" in text)
        check("write: the entry says which ICE is thin",
              "the feature ICE (thin) and the capability ICE" in text)
        check("write: a feature with no line of its own still gets its capability's line",
              "- F4 (from the capability ICE)" in text)

        res_p = os.path.join(tmp, "hidden-file.json")
        code, _ = run("check", "--root", root, "--spine", spine, "--slice-id", "sl-self-booking",
                      "--plans-root", plans, "--out", res_p)
        res = json.loads(read(res_p))
        check("check: the file reads ok, with the counts by who fixes",
              code == 0 and res["ok"] and res["counts"] == {"lines": 4, "builder_alone": 3, "person": 1}
              and [e["feature"] for e in res["entries"]] == ["ft-pick", "ft-remind"])

        # the slice gains a feature: its entry is added, the others are kept byte for byte
        write(os.path.join(root, "care/booking/cancel/feature.md"),
              page("Feature", "Cancel a visit", ["a visit is cancelled with no notice to the doctor."]))
        data["features"].append({"id": "ft-cancel", "slug": "cancel", "capability": "cap-booking",
                                 "doc": "care/booking/cancel/feature.md"})
        data["slices"][0]["feature_refs"].append("ft-cancel")
        write(spine, data)
        before = text
        run("lines", "--root", root, "--spine", spine, "--slice-id", "sl-self-booking",
            "--plans-root", plans, "--out", lines_p)
        lines = json.loads(read(lines_p))
        check("lines: the entries already in the file are kept, the new one is not",
              [e["kept"] for e in lines["entries"]] == [True, True, False]
              and [ln["id"] for ln in lines["entries"][2]["lines"]] == ["F5", "F6"])
        rec_p = write(os.path.join(tmp, "rec2.json"), recoveries(lines))
        code, _ = run("write", "--lines", lines_p, "--recoveries", rec_p, "--plans-root", plans,
                      "--out", out_p)
        after = read(hidden)
        old_block = before[before.index("## ft-pick"):before.index("## ft-remind")]
        check("write: a kept entry stays byte for byte, and the new entry is added",
              code == 0 and old_block in after and "## ft-cancel: Cancel a visit" in after)
        code, _ = run("check", "--root", root, "--spine", spine, "--slice-id", "sl-self-booking",
                      "--plans-root", plans, "--out", res_p)
        check("check: ok after the new entry", code == 0)
        code, _ = run("check", "--root", root, "--spine", spine, "--slice-id", "sl-self-booking",
                      "--plans-root", plans, "--out", res_p, "--lines", lines_p)
        res = json.loads(read(res_p))
        check("check --lines: each kept entry reads byte for byte as it was",
              code == 0 and res["kept_unchanged"] == ["ft-pick", "ft-remind"])
        write(hidden, after.replace("the builder can fix this alone", "a person must decide", 1))
        code, _ = run("check", "--root", root, "--spine", spine, "--slice-id", "sl-self-booking",
                      "--plans-root", plans, "--out", res_p, "--lines", lines_p)
        res = json.loads(read(res_p))
        check("check --lines: a kept entry that changed without an approved edit is a problem (exit 1)",
              code == 1 and any("kept entry" in p for p in res["problems"]))
        write(hidden, after)
        code, err = run("check", "--root", root, "--spine", spine, "--slice-id", "sl-self-booking",
                        "--plans-root", plans, "--out", res_p, "--clear-working", lines_p,
                        "--clear-working", hidden)
        check("check --clear-working: a path under plans-root is refused (exit 2), nothing deleted",
              code == 2 and "plans folder" in err and os.path.isfile(lines_p)
              and os.path.isfile(hidden))
        code, _ = run("check", "--root", root, "--spine", spine, "--slice-id", "sl-self-booking",
                      "--plans-root", plans, "--out", res_p, "--clear-working", lines_p,
                      "--clear-working", rec_p)
        res = json.loads(read(res_p))
        check("check --clear-working: when ok, each named working file is deleted",
              code == 0 and not os.path.exists(lines_p) and not os.path.exists(rec_p)
              and sorted(res["cleared"]) == sorted([lines_p, rec_p]) and os.path.isfile(hidden))

        # an ICE line the file does not hold fails the check
        write(os.path.join(root, "care/booking/remind/feature.md"),
              page("Feature", "Send a reminder", ["a reminder goes to the wrong phone."]))
        keep_p = write(os.path.join(tmp, "hidden-recoveries.json"), {"entries": []})
        code, _ = run("check", "--root", root, "--spine", spine, "--slice-id", "sl-self-booking",
                      "--plans-root", plans, "--out", res_p, "--clear-working", keep_p)
        res = json.loads(read(res_p))
        check("check: a \"Fails if\" line of the ICE that is not in the file fails (exit 1)",
              code == 1 and res["ok"] is False
              and any("wrong phone" in p for p in res["problems"]))
        check("check --clear-working: when not ok, the working files are kept",
              os.path.isfile(keep_p) and res["cleared"] == [])
        os.remove(hidden)
        code, _ = run("check", "--root", root, "--spine", spine, "--slice-id", "sl-self-booking",
                      "--plans-root", plans, "--out", res_p)
        check("check: a missing file fails", code == 1 and "missing" in json.dumps(json.loads(read(res_p))))

        # the ices model reads the lines from ice.md
        root2 = os.path.join(tmp, "po2")
        write(os.path.join(root2, "care/booking/capability.md"), "# Capability: Booking\n")
        write(os.path.join(root2, "care/booking/ice.md"),
              "## Intent\n- Goal: x x x x x\n- Fails if: a booking has no doctor.\n\n## Context\n- x\n")
        write(os.path.join(root2, "care/booking/pick/feature.md"), "# Feature: Pick\n")
        write(os.path.join(root2, "care/booking/pick/ice.md"),
              THIN + "\n\n## Intent\n- Fails if: a slot is booked twice.\n")
        spine2 = write(os.path.join(root2, "_spine.yaml"),
                       {"capabilities": [{"id": "cap-b", "doc": "care/booking/capability.md"}],
                        "features": [{"id": "ft-p", "capability": "cap-b",
                                      "doc": "care/booking/pick/feature.md"}],
                        "ices": [{"id": "ice-b", "for": "cap-b", "for_kind": "capability",
                                  "doc": "care/booking/ice.md"},
                                 {"id": "ice-p", "for": "ft-p", "for_kind": "feature",
                                  "doc": "care/booking/pick/ice.md", "metadata": {"thin": True}}],
                        "slices": [{"id": "sl-x", "slug": "x", "feature_refs": ["ft-p"],
                                    "intents": ["bi-12"]}]})
        run("lines", "--root", root2, "--spine", spine2, "--slice-id", "sl-x", "--plans-root", plans,
            "--out", lines_p)
        lines = json.loads(read(lines_p))
        e = lines["entries"][0]
        check("lines: with an ices list the lines come from each ice.md's Intent",
              [ln["text"] for ln in e["lines"]] == ["a slot is booked twice.", "a booking has no doctor."]
              and e["thin"] == ["feature"] and lines["path"] == "12/evals/x/failure-and-recovery.md")
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
