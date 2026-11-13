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


def make_model(tmp, features=("ft-pick", "ft-remind", "ft-pay"), extra_slices=(), states=None):
    """A clinic model: one slice for bi-340, its features, their capabilities and pages. Each
    feature is Unplanned unless `states` ({feature: status, or None for no status}) says else."""
    root = os.path.join(tmp, "model")
    caps = [
        {"id": "cap-booking", "domain": "dom-clinic", "intents": ["bi-340"],
         "doc": "clinic/booking/capability.md", "depends_on": []},
        {"id": "cap-payment", "domain": "dom-clinic", "intents": ["bi-340"],
         "doc": "clinic/payment/capability.md", "depends_on": []},
        {"id": "cap-waitlist", "domain": "dom-clinic", "intents": ["bi-999"],
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
    states = dict(states or {})
    for f in feats:
        status = states.get(f["id"], "Unplanned")
        if status is not None:
            f["status"] = status
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
            "record": os.path.join(working, "tracker-record.json"),
            "request": os.path.join(working, "planned-request.json"),
            "state_check": os.path.join(working, "state-check.json")}


def gather(root, p, intent="bi-340"):
    return run("gather_plan.py", "--root", root, "--spine", os.path.join(root, "_spine.yaml"),
               "--intent", intent, "--plans", p["plans"], "--out", p["gather"])


def feature_draft(fid):
    return {"feature": fid, "title": f"The patient can {fid[3:]}",
            "scope_of_work": {"goals": [f"The patient can {fid[3:]} on a phone."],
                              "limits": ["Only open slots are used."],
                              "expectations": ["The patient sees a confirmation."]},
            "context_guidance": {"read": "the opening hours", "never_read": "health records",
                                 "persona": "the patient on a phone",
                                 "in_out": "in: open slots; out: moving a booking"}}


def make_drafts(p):
    """One epic for the plan and one draft for each ready feature, once (as the skill writes)."""
    si = read_json(os.path.join(p["working"], "skill-input.json"))
    out = {"epic": {"title": "A patient books a free slot online",
                    "delivers": "A patient books a slot and gets a reminder."},
           "features": [feature_draft(f["id"]) for f in si["features"]]}
    write(p["drafts"], out)
    return out


def link_model_part(root, request):
    """What the link-model-part skill does for the request (stands in for it in the tests): each
    part's feature gets its status, and its metadata.updated_by the request's `by`."""
    spine = yaml.safe_load(read(os.path.join(root, "_spine.yaml")))
    want = {x["id"]: x["status"] for x in request.get("parts") or []}
    for f in spine["features"]:
        if f["id"] in want:
            f["status"] = want[f["id"]]
            f.setdefault("metadata", {})["updated_by"] = request["by"]
    write(os.path.join(root, "_spine.yaml"), spine)


def flow(root, p, decision="yes"):
    """gather → find → drafts → approval → write → plan → checks → Planned → state check.
    Returns the exit codes."""
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
        codes["check_tracker"] = run("check_tracker.py", "--record", p["record"], "--work-items", p["items"],
                                     "--tracker-file", p["tracker"],
                                     "--out", os.path.join(p["working"], "tracker-check.json"))[0]
        codes["request"] = run("planned_request.py", "--work-items", p["items"], "--record", p["record"],
                               "--plan-write", os.path.join(p["working"], "plan-write.json"),
                               "--approval", p["approval"], "--plan-id", "340", "--out", p["request"])[0]
        if codes["request"] == 0:
            link_model_part(root, read_json(p["request"]))
        codes["check_states"] = run("check_states.py", "--before", os.path.join(p["working"], "spine-before.yaml"),
                                    "--spine", os.path.join(root, "_spine.yaml"), "--work-items", p["items"],
                                    "--request", p["request"], "--out", p["state_check"])[0]
    return codes


def write_items(p, out=None):
    return run("write_work_items.py", "--work-items", p["items"], "--drafts", p["drafts"],
               "--gather", p["gather"], "--approval", p["approval"], "--plan-id", "340",
               "--tracker-file", p["tracker"], "--out", out or p["record"])[0]


def empty_tracker(p, issues=()):
    write(p["tracker"], {"issues": list(issues)})


def issue(number, title, type_, body="", state="open", reason=None, subs=(), labels=()):
    """One issue of the file tracker."""
    it = {"number": number, "title": title, "type": type_, "labels": list(labels), "state": state,
          "body": body, "sub_issues": list(subs)}
    if reason:
        it["state_reason"] = reason
    return it


def full_body(fid):
    return (f"Represents: {fid}\n\n## Scope of work\n\nGoals:\n- x\n\n## Context guidance\n\n"
            "- Read: y\n")


def main():
    print("plan_common.py")
    with tempfile.TemporaryDirectory() as tmp:
        path = write(os.path.join(tmp, "t.json"), {"issues": [
            issue(1, "Pick a slot", "Feature", "Represents: ft-pick\n"),
            issue(2, "Pick a slot, again", "Feature", "Represents: ft-pick-two\n"),
            issue(3, "Pick a slot story", "Story", "Represents: ft-pick\n"),
            issue(4, "Old group", "Feature", "Stories of ft-pick and more.\n"),
            issue(5, "Pick a free slot", "Story", "", state="closed", reason="completed"),
            issue(6, "Pick a free slot later", "Story", "", state="closed", reason="not_planned"),
            issue(7, "Represents line not exact", "Feature", "  Represents: ft-pick and more\n")]})
        tr = pc.FileTracker(path)
        check("the file tracker's search finds a phrase in the text, open or closed",
              tr.search("Represents: ft-pick", fields=("body",)) == [1, 2, 3, 7])
        check("feature_issues keeps only type Feature with the exact line (ADR 068)",
              [i["number"] for i in pc.feature_issues(tr, "ft-pick")] == [1])
        tr.close(1)
        check("the file tracker closes an issue as completed", pc.finished(tr.get(1)))
        tr.reopen(1)
        check("the file tracker opens a closed issue again", tr.get(1)["state"] == "open")
    check("feature_state reads each of the five states",
          all(pc.feature_state({"status": s}) == (s, False) for s in pc.STATES))
    check("feature_state reads no status, or a value outside the five, as Unplanned with no state (ADR 070)",
          pc.feature_state({}) == ("Unplanned", True) and pc.feature_state({"status": "proposed"}) == ("Unplanned", True)
          and pc.feature_state(None) == ("Unplanned", True))
    check("the plan takes in a reopened Feature issue and one closed by hand, never a Completed or "
          "Dropped feature",
          pc.map_pairs([{"feature": "a", "action": "reopen", "issue": 3},
                        {"feature": "d", "action": "closed-by-hand", "issue": 4},
                        {"feature": "b", "action": "completed", "issue": None},
                        {"feature": "c", "action": "dropped", "issue": None}]) == [("a", 3), ("d", 4)])
    body = pc.with_map("Plan: 1", [("ft-a", 2), ("ft-b", 3)], {"ft-b": 9})
    check("a held_by map line names the epic that holds it, and reads back",
          "- ft-b → #3 (under Epic #9)" in body and pc.read_map(body) == {"ft-a": 2, "ft-b": 3}
          and pc.read_map(body, held=True) == {"ft-b": 9})
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
            if verb == "list-issues":
                return {"exit_code": 0, "stdout": '[{"number": 7}, {"number": 3}]', "stderr": ""}
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
    host.close(41)
    host.reopen(41)
    check("every other write is an adapter verb",
          [c[0] for c in calls[1:]] == ["set-issue-type", "edit-issue-body", "remove-label",
                                         "attach-sub-issue", "remove-sub-issue", "close-issue",
                                         "reopen-issue"])
    check("a close is as completed", calls[6][1] == {"issue_number": "41", "reason": "completed"})
    check("an issue opens again through the adapter's reopen-issue verb", calls[7][1] == {"issue_number": "41"})
    found = host.search("Represents: ft-a", fields=("body",))
    check("the host search is the adapter's list-issues verb, open and closed, in the text",
          found == [3, 7] and calls[8][0] == "list-issues"
          and calls[8][1]["query"] == '"Represents: ft-a" in:body' and calls[8][1]["state"] == "all")
    check("a sub-issue is attached with replace_parent, so it leaves any other parent (#1025)",
          calls[4][1].get("replace_parent") == "true")
    import platform_adapter as pa
    with_flag = pa._gh("attach-sub-issue", {"parent_number": "40", "child_number": "41",
                                            "replace_parent": "true"}, ("o", "n"))[0]
    without = pa._gh("attach-sub-issue", {"parent_number": "40", "child_number": "41"}, ("o", "n"))[0]
    check("the adapter sends replace_parent only when asked",
          with_flag[-2:] == ["-F", "replace_parent=true"] and "replace_parent=true" not in without)
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "t.json")
        write(path, {"issues": [{"number": 1, "title": "BI", "type": None, "labels": [], "state": "open",
                                 "body": "", "sub_issues": [5]},
                                {"number": 2, "title": "Epic", "type": "Epic", "labels": [], "state": "open",
                                 "body": "", "sub_issues": []},
                                {"number": 5, "title": "S", "type": "Story", "labels": [], "state": "open",
                                 "body": ""}]})
        ft = pc.open_tracker(path)
        ft.add_sub(2, 5)
        data = {i["number"]: i for i in read_json(path)["issues"]}
        check("the file tracker moves a sub-issue: it leaves its old parent",
              data[2]["sub_issues"] == [5] and data[1]["sub_issues"] == [])
        check("the file tracker reports an issue's parent", ft.get(5)["parent"]["number"] == 2)
    check("a parent in another repository is read with its repository (#1025)",
          pc._parent({"number": 1, "title": "Product", "url": "https://github.com/acme/intents/issues/1"})
          == {"number": 1, "title": "Product", "repo": "acme/intents"} and pc._parent(None) is None)
    with tempfile.TemporaryDirectory() as tmp:
        root = make_model(tmp)
        check("the fixture model loads", os.path.isfile(os.path.join(root, "_spine.yaml")))
    return finish()


if __name__ == "__main__":
    sys.exit(main())
