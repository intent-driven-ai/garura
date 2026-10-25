#!/usr/bin/env python3
"""test_support.py — the fixtures the /shape-plan tests share, and the tests of plan_common.py.

    python3 test_support.py

A fixture is a small product model in a temp folder (a clinic: patients book their own
appointments), a plans folder and a tracker file. No network, no real tracker.
"""
import json
import os
import subprocess
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import plan_common as pc  # noqa: E402

RESULTS = {"passed": 0, "failed": 0}


def check(name, cond):
    if cond:
        RESULTS["passed"] += 1
        print(f"  [PASS] {name}")
    else:
        RESULTS["failed"] += 1
        print(f"  [FAIL] {name}")


def finish():
    print(f"{RESULTS['passed']} passed, {RESULTS['failed']} failed")
    return 1 if RESULTS["failed"] else 0


def run(script, *args):
    p = subprocess.run([sys.executable, os.path.join(HERE, script), *[str(a) for a in args]],
                       capture_output=True, text=True)
    try:
        out = json.loads(p.stdout) if p.stdout.strip() else None
    except json.JSONDecodeError:
        out = None
    return p.returncode, out, p.stderr


def write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        if isinstance(data, str):
            fh.write(data)
        elif path.endswith(".json"):
            json.dump(data, fh, indent=2)
        else:
            yaml.safe_dump(data, fh, sort_keys=False)
    return path


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def read_json(path):
    return json.loads(read(path))


FAILS = {
    "ft-pick": "two patients get the same slot",
    "ft-remind": "a reminder goes to the wrong patient",
    "ft-pay": "a card is charged twice",
    "ft-cancel": "a cancelled slot stays booked",
    "ft-wait": "a patient waits with no slot offered",
    "cap-booking": "a booking is lost",
    "cap-payment": "money is taken with no booking",
    "cap-waitlist": "the waiting list loses a patient",
}


def page(kind, pid, name):
    return (f"# {kind}: {name}\n\n## What it does\n{name}.\n\n## Agent intent (ICE)\n"
            f"- Goal: {name} works for the patient.\n"
            f"- Limit: only open slots are used.\n"
            f"- Fails if: {FAILS[pid]}.\n"
            f"  The line goes on here.\n"
            f"- Context: serves the patient on a phone; read the opening hours; never read health records; in: open slots, out: moving a booking.\n"
            f"- Checked by: a patient books a slot on a phone.\n")


def make_model(tmp, features=("ft-pick", "ft-remind", "ft-pay"), extra_slices=()):
    """A clinic model: one slice for bi-340, its features, their capabilities and pages."""
    root = os.path.join(tmp, "model")
    caps = [
        {"id": "cap-booking", "domain": "dom-clinic", "intents": ["bi-340"], "status": "proposed",
         "doc": "clinic/booking/capability.md", "depends_on": []},
        {"id": "cap-payment", "domain": "dom-clinic", "intents": ["bi-340"], "status": "proposed",
         "doc": "clinic/payment/capability.md", "depends_on": []},
        {"id": "cap-waitlist", "domain": "dom-clinic", "intents": ["bi-999"], "status": "proposed",
         "doc": "clinic/waitlist/capability.md", "depends_on": []},
    ]
    feats = [
        {"id": "ft-pick", "capability": "cap-booking", "doc": "clinic/booking/ft-pick/feature.md",
         "one_line": "A patient picks a free slot."},
        {"id": "ft-remind", "capability": "cap-booking", "doc": "clinic/booking/ft-remind/feature.md",
         "one_line": "A patient gets a reminder."},
        {"id": "ft-pay", "capability": "cap-payment", "doc": "clinic/payment/ft-pay/feature.md",
         "one_line": "A patient pays the booking fee."},
        {"id": "ft-cancel", "capability": "cap-booking", "doc": "clinic/booking/ft-cancel/feature.md",
         "one_line": "A patient cancels online."},
        {"id": "ft-wait", "capability": "cap-waitlist", "doc": "clinic/waitlist/ft-wait/feature.md",
         "one_line": "A patient joins the waiting list."},
    ]
    names = {"ft-pick": "Pick a free slot", "ft-remind": "Send a reminder", "ft-pay": "Pay the fee",
             "ft-cancel": "Cancel online", "ft-wait": "Join the waiting list",
             "cap-booking": "Booking", "cap-payment": "Payment", "cap-waitlist": "Waiting list"}
    for c in caps:
        write(os.path.join(root, c["doc"]), page("Capability", c["id"], names[c["id"]]))
    for f in feats:
        write(os.path.join(root, f["doc"]), page("Feature", f["id"], names[f["id"]]))
    slices = [{"id": "sl-self-booking", "slug": "self-booking", "feature_refs": list(features),
               "vertical": "the booking page", "intents": ["bi-340"],
               "record": "slices/sl-self-booking.yaml"}]
    slices += list(extra_slices)
    spine = {"domains": [{"id": "dom-clinic"}], "capabilities": caps, "features": feats,
             "slices": slices}
    write(os.path.join(root, "_spine.yaml"), spine)
    write(os.path.join(root, "slices", "sl-self-booking.yaml"),
          {"slice": {"id": "sl-self-booking", "name": "Self-booking",
                     "outcome": "A patient books a free slot online and gets a reminder."}})
    write(os.path.join(root, "intents", "bi-340.md"),
          "# Patients book their own appointments online\n\n**Stage:** confirmed\n")
    write(os.path.join(root, "intents", "bi-999.md"), "# Someone else's need\n\n**Stage:** proposed\n")
    return root


def set_slice(root, slice_id, features):
    spine = yaml.safe_load(read(os.path.join(root, "_spine.yaml")))
    for s in spine["slices"]:
        if s["id"] == slice_id:
            s["feature_refs"] = list(features)
    write(os.path.join(root, "_spine.yaml"), spine)


def paths(tmp):
    working = os.path.join(tmp, "working")
    os.makedirs(working, exist_ok=True)
    return {"working": working, "plans": os.path.join(tmp, "plans"),
            "plan_file": os.path.join(tmp, "plans", "340.yaml"),
            "tracker": os.path.join(tmp, "tracker.json"),
            "gather": os.path.join(working, "gather.json"),
            "items": os.path.join(working, "work-items.json"),
            "drafts": os.path.join(working, "drafts.json"),
            "approval": os.path.join(working, "approval.json"),
            "brief": os.path.join(working, "brief.md"),
            "record": os.path.join(working, "tracker-record.json")}


def gather(root, p, intent="bi-340"):
    return run("gather_plan.py", "--root", root, "--spine", os.path.join(root, "_spine.yaml"),
               "--intent", intent, "--plans", p["plans"], "--out", p["gather"])


def story_draft(fid, pages):
    return {"feature": fid, "title": f"The patient can {fid[3:]}",
            "scope_of_work": {"goals": [f"The patient can {fid[3:]} on a phone."],
                              "limits": ["Only open slots are used."],
                              "expectations": ["The patient sees a confirmation."]},
            "context_guidance": {"read": "the opening hours", "never_read": "health records",
                                 "persona": "the patient on a phone",
                                 "in_out": "in: open slots; out: moving a booking"},
            "written_from": pages}


def make_drafts(p):
    g = read_json(p["gather"])
    out = {"slices": []}
    for sl in g["slices"]:
        out["slices"].append({
            "slice": sl["id"],
            "epic": {"title": "A patient books a free slot online", "delivers": "A patient books a slot and gets a reminder."},
            "stories": [story_draft(f["id"], f["ice_pages"]) for f in sl["features"] if f["ready"]]})
    write(p["drafts"], out)
    return out


def flow(root, p, decision="yes"):
    """gather → find → drafts → approval → write → plan → checks. Returns the exit codes."""
    codes = {}
    codes["gather"] = gather(root, p)[0]
    codes["find"] = run("find_work_items.py", "--gather", p["gather"], "--plan-file", p["plan_file"],
                        "--tracker-file", p["tracker"], "--out", p["items"])[0]
    make_drafts(p)
    codes["drafts"] = run("check_drafts.py", "--drafts", p["drafts"], "--gather", p["gather"],
                          "--out", os.path.join(p["working"], "drafts-check.json"))[0]
    codes["brief"] = run("render_brief.py", "--gather", p["gather"], "--work-items", p["items"],
                         "--drafts", p["drafts"], "--out", p["brief"])[0]
    codes["approval"] = run("record_approval.py", "--decision", decision, "--reply", decision,
                            "--at", "2026-10-25T10:00:00Z", "--brief", p["brief"], "--work-items", p["items"],
                            "--drafts", p["drafts"], "--out", p["approval"])[0]
    codes["write"] = write_items(p)
    if codes["write"] in (0, 1):
        codes["plan"] = run("write_plan_file.py", "--plan-file", p["plan_file"], "--gather", p["gather"],
                            "--record", p["record"], "--out", os.path.join(p["working"], "plan-write.json"))[0]
    if codes["write"] == 0:
        codes["check_plan"] = run("check_plan.py", "--plan-file", p["plan_file"], "--gather", p["gather"],
                                  "--record", p["record"], "--out", os.path.join(p["working"], "plan-check.json"))[0]
        codes["check_tracker"] = run("check_tracker.py", "--record", p["record"], "--tracker-file", p["tracker"],
                                     "--out", os.path.join(p["working"], "tracker-check.json"))[0]
    return codes


def write_items(p, out=None):
    return run("write_work_items.py", "--work-items", p["items"], "--drafts", p["drafts"],
               "--gather", p["gather"], "--approval", p["approval"], "--plan-id", "340",
               "--tracker-file", p["tracker"], "--out", out or p["record"])[0]


def empty_tracker(p, issues=()):
    write(p["tracker"], {"issues": list(issues)})


def main():
    print("plan_common.py")
    lines = ["- Goal: a.", "- Fails if: b goes", "  wrong for a long time.", "- Limit: c.",
             "### Fails if", "- d.", "## Context", "**Fails if**", "- e.", "", "Plain line.",
             "- Context: f; the line fails if nothing"]
    kept = pc.without_fails_if(lines)
    check("without_fails_if keeps the other lines", kept[:2] == ["- Goal: a.", "- Limit: c."])
    check("without_fails_if takes out every failure line, block and wrapped line",
          not any("fails if" in ln.lower() for ln in kept) and "  wrong for a long time." not in kept
          and "- d." not in kept and "- e." not in kept)
    check("without_fails_if keeps the line after a bold block", "Plain line." in kept)
    check("fails_if_texts reads each line of each block",
          pc.fails_if_texts(lines)[:4] == ["b goes", "wrong for a long time.", "d.", "e."])
    nested = ["- Goal: a patient books.", "- Fails if:", "  - a card is charged twice", "  - two slots are booked",
              "    and the patient pays for both", "- Fails if: a reminder goes out", "late at night",
              "- Limit: open slots only."]
    check("a nested block: the line and every line under it are taken out",
          pc.without_fails_if(nested) == ["- Goal: a patient books.", "- Limit: open slots only."])
    check("a nested block: every child line is read for the check",
          pc.fails_if_texts(nested) == ["a card is charged twice", "two slots are booked",
                                        "and the patient pays for both", "a reminder goes out", "late at night"])
    check("forbidden_in finds the words, the phrases and a line",
          len(pc.forbidden_in("It Fails If it breaks", ["a card is charged twice"])) == 1
          and pc.forbidden_in("then a person must decide")
          and pc.forbidden_in("when a card is charged twice.", ["A card is charged twice."]))
    check("forbidden_in passes plain text", pc.forbidden_in("A patient books a slot.", ["two bookings"]) == [])
    body = "Intro line.\n\n## Feature-to-story map\n\n- ft-a → #2\n\n## Notes\nKeep me.\n"
    check("read_map reads the map", pc.read_map(body) == {"ft-a": 2})
    new = pc.with_map(body, [("ft-a", 2), ("ft-b", 3)])
    check("with_map writes the map again and keeps the other lines",
          pc.read_map(new) == {"ft-a": 2, "ft-b": 3} and "Keep me." in new and "Intro line." in new)
    check("with_map adds a map to a body that has none",
          pc.read_map(pc.with_map("Only text.", [("ft-a", 2)])) == {"ft-a": 2})
    check("lines_kept sees a kept body", pc.lines_kept("a\nb", "a\nx\nb\nc"))
    check("lines_kept sees a lost line", not pc.lines_kept("a\nb", "a\nc"))
    with tempfile.TemporaryDirectory() as tmp:
        path = write(os.path.join(tmp, "t.json"), {"issues": [{"number": 5, "title": "x"}]})
        tr = pc.FileTracker(path)
        n = tr.create("New", "body", "Story", parent=5)
        check("the file tracker gives the next free number and sets the parent in the same write",
              n == 6 and read_json(path)["issues"][0]["sub_issues"] == [6])
        write(path, dict(read_json(path), fail_at_write=2))
        tr = pc.FileTracker(path)
        tr.set_type(6, "Story")
        try:
            tr.set_body(6, "lost")
            failed = False
        except pc.TrackerError:
            failed = True
        check("fail_at_write makes that write fail and keeps every write before it",
              failed and read_json(path)["issues"][1]["body"] == "body")
    calls = []

    class FakeAdapter:
        @staticmethod
        def dispatch(verb, args, config_path=None):
            calls.append((verb, args))
            if verb == "create-issue-typed":
                return {"exit_code": 0, "stdout": "41\n", "stderr": ""}
            return {"exit_code": 0, "stdout": "{}", "stderr": "", "tree_available": True}

    host = pc.HostTracker.__new__(pc.HostTracker)
    host.pa, host.config = FakeAdapter, "c.yaml"
    check("the host tracker makes an issue with its type and parent in one adapter call",
          host.create("T", "B", "Story", parent=40) == 41 and len(calls) == 1
          and calls[0] == ("create-issue-typed", {"title": "T", "body": "B", "issue_type": "Story",
                                                  "parent_number": "40"}))
    host.set_type(41, "Story")
    host.set_body(41, "x")
    host.remove_labels(41, ["a"])
    host.add_sub(40, 41)
    host.remove_sub(40, 41)
    check("every other write is an adapter verb",
          [c[0] for c in calls[1:]] == ["set-issue-type", "edit-issue-body", "remove-label",
                                         "attach-sub-issue", "remove-sub-issue"])
    with tempfile.TemporaryDirectory() as tmp:
        root = make_model(tmp)
        check("the fixture model loads", os.path.isfile(os.path.join(root, "_spine.yaml")))
    return finish()


if __name__ == "__main__":
    sys.exit(main())
