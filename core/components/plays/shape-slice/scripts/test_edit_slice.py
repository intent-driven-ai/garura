#!/usr/bin/env python3
"""test_edit_slice.py — the edit path of /shape-slice (C20, F20, S11): only what the person
named changes, with a history line, and any other change is caught.

    python3 core/components/plays/shape-slice/scripts/test_edit_slice.py
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


def check(name, cond):
    global PASSED, FAILED
    if cond:
        PASSED += 1
        print(f"  [PASS] {name}")
    else:
        FAILED += 1
        print(f"  [FAIL] {name}")


def run(*args):
    p = subprocess.run([sys.executable, os.path.join(HERE, "edit_slice.py"), *args],
                       capture_output=True, text=True)
    try:
        out = json.loads(p.stdout) if p.stdout.strip() else None
    except json.JSONDecodeError:
        out = None
    return p.returncode, out, p.stderr


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


SPINE = """# the spine
features:
# the booking features
- id: ft-pick
  slug: pick
  one_line: Pick a free slot.
  doc: care/pick/feature.md
- id: ft-remind
  slug: remind
  one_line: Send a reminder.
  doc: care/remind/feature.md
slices:
- id: sl-self
  slug: self
  feature_refs: [ft-pick, ft-remind]
  vertical: the booking screen
  intents: [bi-340]
  record: slices/sl-self.yaml
"""

RECORD = """slice:
  id: sl-self
  slug: self
  name: Self booking
  outcome: A patient books a visit.
  feature_refs:
  - ft-pick
  - ft-remind
surface:
  id: sf-booking
  name: the booking screen
  persona_ref: patient
  user_action: books a free slot
"""

HIDDEN = """# Failure and recovery: slice sl-self

Slice: Self booking.

## ft-pick: Pick a free slot

### Failure conditions

- F1 (from the feature ICE): two patients get one slot.
- F2 (from the feature ICE): a slot in the past is shown.

### Recovery

- For F1
  - When: two bookings hold one slot
  - Way back: book each slot once
  - Who fixes: the builder can fix this alone
- For F2
  - When: a past slot is shown
  - Way back: show only slots to come
  - Who fixes: the builder can fix this alone

## ft-remind: Send a reminder

### Failure conditions

- F3 (from the feature ICE): no reminder is sent.

### Recovery

- For F3
  - When: no reminder is sent a day before
  - Way back: send each reminder a day before
  - Who fixes: the builder can fix this alone
"""


def setup(tmp):
    root, plans, work = (os.path.join(tmp, n) for n in ("po", "plans", "work"))
    spine = write(os.path.join(root, "_spine.yaml"), SPINE)
    write(os.path.join(root, "slices", "sl-self.yaml"), RECORD)
    hidden = write(os.path.join(plans, "340", "evals", "self", "failure-and-recovery.md"), HIDDEN)
    req = write(os.path.join(work, "edit-request.md"), "F1 and F3 should go to a person.\n")
    before = os.path.join(work, "edit-before.json")
    run("snapshot", "--root", root, "--spine", spine, "--slice-id", "sl-self", "--plans-root", plans,
        "--working", work, "--out", before)
    return root, plans, work, spine, hidden, req, before


def lst(work, changes, name="edit-list.json"):
    return write(os.path.join(work, name), json.dumps({"changes": changes, "out_of_date": []}))


def main():
    with tempfile.TemporaryDirectory() as tmp:
        root, plans, work, spine, hidden, req, before = setup(tmp)
        snap = json.loads(read(before))
        check("snapshot: copies the slice record, the hidden file and the spine",
              sorted(snap["files"]) == ["hidden", "record", "spine"]
              and all(os.path.isfile(p) for p in snap["copies"].values()))
        two = lst(work, [
            {"file": "hidden", "part": "ft-pick/F1/who_fixes", "old": "the builder can fix this alone",
             "new": "a person must decide", "why": "the person asked"},
            {"file": "hidden", "part": "ft-remind/F3/who_fixes", "old": "the builder can fix this alone",
             "new": "a person must decide", "why": "the person asked"}])
        code, out, _ = run("check-list", "--before", before, "--list", two,
                           "--out", os.path.join(work, "lc.json"))
        check("check-list: a list of two who-fixes changes holds (exit 0)", code == 0 and out["ok"])
        code, out, _ = run("apply", "--before", before, "--list", two, "--request", req,
                           "--by", "the product owner", "--at", "2026-10-27",
                           "--out", os.path.join(work, "apply.json"))
        text = read(hidden)
        check("apply: the two named lines change, F2 stays with the builder",
              code == 0 and text.count("Who fixes: a person must decide") == 2
              and text.count("Who fixes: the builder can fix this alone") == 1)
        check("apply: the hidden file holds a history line with the person's words",
              "Edited on 2026-10-27 by the product owner" in text and "F1 and F3 should go to a person." in text)
        rec = yaml.safe_load(read(os.path.join(root, "slices", "sl-self.yaml")))
        check("apply: the slice record holds a history entry, and nothing else of it changed",
              rec["edits"][0]["by"] == "the product owner" and rec["slice"]["name"] == "Self booking"
              and rec["surface"]["user_action"] == "books a free slot")
        check("apply: the spine did not change", read(spine) == SPINE)
        code, out, _ = run("check", "--before", before, "--list", two, "--request", req,
                           "--apply", os.path.join(work, "apply.json"), "--out", os.path.join(work, "check.json"))
        check("check: before and after differ only by the list and the history lines (exit 0)",
              code == 0 and out["ok"] and out["changes"] == 2)
        write(hidden, read(hidden).replace("show only slots to come", "show any slot"))
        code, out, _ = run("check", "--before", before, "--list", two, "--request", req,
                           "--apply", os.path.join(work, "apply.json"), "--out", os.path.join(work, "check.json"))
        check("check: a change that is not on the list is caught (exit 1)",
              code == 1 and "not on the list" in " ".join(out["problems"]))
        lst_json = json.loads(read(two))
        lst_json["not_editable"] = [{"what": "take ft-remind out", "why": "a feature in or out is a reshape"}]
        write(two, json.dumps(lst_json))
        bp = os.path.join(work, "brief.md")
        r = subprocess.run([sys.executable, os.path.join(HERE, "render_brief.py"), "--edit", "Self booking",
                            "--working", work, "--out", bp], capture_output=True, text=True)
        brief = read(bp) if os.path.isfile(bp) else ""
        check("render_brief --edit: the brief shows what was asked, each change old and new",
              r.returncode == 0 and "F1 and F3 should go to a person." in brief
              and "was: the builder can fix this alone" in brief and "now: a person must decide" in brief)
        check("render_brief --edit: each change names its feature, its failure line and why, in words",
              'feature "Pick a free slot" (ft-pick)' in brief
              and 'the line "two patients get one slot." (F1): who fixes' in brief
              and "why: the person asked" in brief)
        check("render_brief --edit: what the words named that an edit does not change is shown",
              "## Not changed by an edit" in brief and "take ft-remind out" in brief)
        r = subprocess.run([sys.executable, os.path.join(HERE, "record_questions.py"), "brief", "--brief", bp,
                            "--edit"], capture_output=True, text=True)
        check("record_questions brief --edit: the edit brief passes its check",
              r.returncode == 0 and json.loads(r.stdout)["ok"])
        rec_md = os.path.join(work, "grounding-questions.md")
        write(os.path.join(work, "reply.md"), "yes\n")
        for _ in range(2):
            r = subprocess.run([sys.executable, os.path.join(HERE, "record_questions.py"), "edit",
                                "--record", rec_md, "--issue", "908", "--request", req,
                                "--reply", os.path.join(work, "reply.md"), "--decision", "yes",
                                "--at", "2026-10-27", "--run", "r1"], capture_output=True, text=True)
        entries = yaml.safe_load(read(rec_md).split("```yaml\n")[1].split("```")[0])["questions"]
        check("record_questions edit: the record holds the edit's question, the words and the reply",
              r.returncode == 0 and [e["id"] for e in entries] == ["Q-edit-1", "Q-edit-2"]
              and "F1 and F3 should go to a person." in entries[0]["question"]
              and entries[0]["user_answer"] == "yes" and entries[0]["user_decision"] == "yes")
        code, out, _ = run("restore", "--before", before, "--out", os.path.join(work, "restore.json"))
        check("restore: every record is as it was before the edit",
              code == 0 and read(hidden) == HIDDEN and read(spine) == SPINE
              and read(os.path.join(root, "slices", "sl-self.yaml")) == RECORD)

    with tempfile.TemporaryDirectory() as tmp:
        root, plans, work, spine, hidden, req, before = setup(tmp)
        by_intent = os.path.join(work, "by-intent.json")
        code, out, _ = run("snapshot", "--root", root, "--spine", spine, "--intent", "bi-340",
                           "--plans-root", plans, "--working", work, "--out", by_intent)
        check("snapshot --intent: finds the one slice the spine links to the intent",
              code == 0 and out["slice"] == "sl-self" and out["in_progress"] is False)
        code, _, err = run("snapshot", "--root", root, "--spine", spine, "--intent", "bi-999",
                           "--plans-root", plans, "--working", work, "--out", by_intent)
        check("snapshot --intent: refuses an intent with no slice (exit 2)", code == 2 and "0 slices" in err)
        rename = lst(work, [
            {"file": "record", "part": "slice.name", "old": "Self booking", "new": "A patient books online",
             "why": "x"},
            {"file": "spine", "part": "ft-pick/one_line", "old": "Pick a free slot.",
             "new": "A patient picks a free slot.", "why": "x"}])
        code, _, _ = run("apply", "--before", before, "--list", rename, "--request", req,
                         "--by", "the product owner", "--at", "2026-10-27", "--out", os.path.join(work, "a.json"))
        sp = read(spine)
        check("apply: a one-line and the slice name change; the spine keeps its comments",
              code == 0 and "A patient picks a free slot." in sp and "# the booking features" in sp
              and yaml.safe_load(read(os.path.join(root, "slices", "sl-self.yaml")))["slice"]["name"]
              == "A patient books online")
        check("apply: the hidden file is untouched when the list names no change to it",
              read(hidden) == HIDDEN)
        code, out, _ = run("check", "--before", before, "--list", rename, "--request", req,
                           "--apply", os.path.join(work, "a.json"), "--out", os.path.join(work, "c.json"))
        check("check: the rename and the one-line pass", code == 0 and out["ok"])

    with tempfile.TemporaryDirectory() as tmp:
        root, plans, work, spine, hidden, req, before = setup(tmp)
        cases = [
            ([{"file": "hidden", "part": "ft-pick/F1/who_fixes", "old": "a person must decide",
               "new": "the builder can fix this alone"}], "old text"),
            ([{"file": "hidden", "part": "ft-pick/F1/who_fixes", "old": "the builder can fix this alone",
               "new": "the builder decides"}], "who fixes must be"),
            ([{"file": "record", "part": "slice.feature_refs", "old": "x", "new": "y"}], "not a part"),
            ([{"file": "eval", "part": "x", "old": "x", "new": "y"}], "not a file"),
            ([{"file": "spine", "part": "ft-none/one_line", "old": "x", "new": "y"}], "not in the spine"),
            ([], "names no change"),
        ]
        for i, (changes, want) in enumerate(cases):
            code, out, _ = run("check-list", "--before", before, "--list", lst(work, changes, f"l{i}.json"),
                               "--out", os.path.join(work, f"lc{i}.json"))
            check(f"check-list refuses: {want}", code == 1 and want in " ".join(out["problems"]))
        code, _, err = run("apply", "--before", before, "--list", os.path.join(work, "l0.json"),
                           "--request", req, "--by", "p", "--at", "d", "--out", os.path.join(work, "x.json"))
        check("apply: a list that does not hold is refused and nothing is written (exit 2)",
              code == 2 and read(hidden) == HIDDEN)
    with tempfile.TemporaryDirectory() as tmp:
        root, plans, work, spine, hidden, req, before = setup(tmp)
        write(spine, SPINE + "epics:\n- id: ep-self\n  slice_ref: sl-self\n  status: in_delivery\n")
        code, out, _ = run("snapshot", "--root", root, "--spine", spine, "--slice-id", "sl-self",
                           "--plans-root", plans, "--working", work, "--out", before)
        check("snapshot: a slice whose epic is past ready is in progress, and an edit may still go on",
              code == 0 and out["in_progress"] is True
              and out["epics"] == [{"id": "ep-self", "status": "in_delivery"}])
        lst(work, [{"file": "record", "part": "slice.name", "old": "Self booking", "new": "Book online",
                    "why": "x"}])
        bp = os.path.join(work, "brief.md")
        subprocess.run([sys.executable, os.path.join(HERE, "render_brief.py"), "--edit", "Self booking",
                        "--working", work, "--out", bp], capture_output=True, text=True)
        brief = read(bp) if os.path.isfile(bp) else ""
        check("render_brief --edit: the brief says the slice is in progress and names its epic",
              "## In progress" in brief and "ep-self (in_delivery)" in brief)
        check("render_brief --edit: the epic is named as out of date even when the list leaves it out",
              "- epic ep-self (in_delivery): work has started" in brief.split("## Out of date")[1])
        r = subprocess.run([sys.executable, os.path.join(HERE, "record_questions.py"), "brief", "--brief", bp,
                            "--edit", "--before", before], capture_output=True, text=True)
        check("record_questions brief --edit: the brief of a slice in progress passes its check",
              r.returncode == 0)
        write(bp, brief.replace("## In progress", "## Note"))
        r = subprocess.run([sys.executable, os.path.join(HERE, "record_questions.py"), "brief", "--brief", bp,
                            "--edit", "--before", before], capture_output=True, text=True)
        check("record_questions brief --edit --before: a brief that hides the slice is in progress fails",
              r.returncode == 1 and "in progress" in r.stdout)
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
