#!/usr/bin/env python3
"""test_shape_slice_scripts.py — the intent page (C1), the fills (C8), the question record
(C2–C5, C10), the slice check (C11) and the checkpoint record (C12) of /shape-slice (#795).

    python3 core/components/plays/shape-slice/scripts/test_shape_slice_scripts.py
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


def run(script, *args):
    p = subprocess.run([sys.executable, os.path.join(HERE, script), *args],
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
            json.dump(data, fh)
        else:
            yaml.safe_dump(data, fh, sort_keys=False)
    return path


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


DRAFT = {"id": "bi-340", "issue": 340, "title": "Patients book their own appointments online",
         "outcome": "A patient books a visit with no phone call.", "why": "The desk is busy.",
         "asked_by": "the clinic manager", "proof": ["Half of the bookings are online for a month."],
         "must_not": "Change how the clinic bills."}


def test_intent_page(tmp):
    root = os.path.join(tmp, "po")
    d = write(os.path.join(tmp, "draft.json"), DRAFT)
    code, out, _ = run("write_intent_page.py", "--root", root, "--intent", "bi-340", "--date", "2026-10-23")
    check("intent page: missing page and no draft exits 3, nothing written",
          code == 3 and not os.path.exists(os.path.join(root, "intents")))
    code, out, _ = run("write_intent_page.py", "--root", root, "--intent", "bi-340", "--draft", d,
                       "--date", "2026-10-23")
    page = os.path.join(root, "intents", "bi-340.md")
    check("intent page: written when the model has none", code == 0 and out["written"] is True)
    text = read(page) if os.path.isfile(page) else ""
    check("intent page: has the ontology's parts",
          all(p in text for p in ("**Outcome:**", "**Why:**", "**Asked by:**", "**Proof it is met:**",
                                  "**Must not:**", "**Stage:** proposed", "**Tracker:** #340")))
    check("intent page: says it was written from the issue", "from issue #340" in text)
    code, out, _ = run("write_intent_page.py", "--root", root, "--intent", "bi-340", "--draft", d,
                       "--date", "2026-10-24")
    check("intent page: never overwritten", code == 0 and out["written"] is False and read(page) == text)
    bad = write(os.path.join(tmp, "bad.json"), dict(DRAFT, why=""))
    code, out, _ = run("write_intent_page.py", "--root", os.path.join(tmp, "po2"), "--intent", "bi-340",
                       "--draft", bad, "--date", "2026-10-23")
    check("intent page: a missing part is refused, nothing written",
          code == 2 and not os.path.exists(os.path.join(tmp, "po2")))
    mism = write(os.path.join(tmp, "mism.json"), dict(DRAFT, id="bi-341"))
    code, _, _ = run("write_intent_page.py", "--root", os.path.join(tmp, "po2"), "--intent", "bi-340",
                     "--draft", mism, "--date", "2026-10-23")
    check("intent page: an id that does not match the issue is refused", code == 2)
    return root


def test_fills(tmp, root):
    spine = write(os.path.join(root, "_spine.yaml"),
                  {"domains": [{"id": "dm-care", "slug": "care"}],
                   "capabilities": [{"id": "cap-booking", "slug": "booking", "domain": "dm-care"}],
                   "features": [{"id": "ft-1", "capability": "cap-booking"}], "ices": [], "slices": []})
    for doc in ("notify/domain.md", "notify/reminders/capability.md",
                "notify/reminders/features/send-reminder/feature.md",
                "notify/reminders/features/send-reminder/ice.md"):
        write(os.path.join(root, doc), "# page\n")
    fills = {"domains": [{"id": "dm-notify", "slug": "notify", "one_line": "Messages to people.",
                          "doc": "notify/domain.md"}],
             "capabilities": [{"id": "cap-reminders", "slug": "reminders", "domain": "dm-notify",
                               "one_line": "Reminders before a visit.",
                               "doc": "notify/reminders/capability.md"}],
             "features": [{"id": "ft-send-reminder", "slug": "send-reminder", "capability": "cap-reminders",
                           "one_line": "Send a reminder.",
                           "doc": "notify/reminders/features/send-reminder/feature.md"}],
             "ices": [{"id": "ice-send-reminder", "for": "ft-send-reminder", "for_kind": "feature",
                       "doc": "notify/reminders/features/send-reminder/ice.md"}]}
    page_before = read(os.path.join(root, "intents", "bi-340.md"))

    bad = write(os.path.join(tmp, "bad-fills.json"),
                dict(fills, features=[dict(fills["features"][0], capability="cap-none")]))
    spine_before = read(spine)
    code, out, _ = run("persist_fills.py", "--root", root, "--spine", spine, "--fills", bad,
                       "--intent", "bi-340")
    check("fills: an unknown parent is refused, nothing written",
          code == 2 and read(spine) == spine_before
          and read(os.path.join(root, "intents", "bi-340.md")) == page_before)
    dup = write(os.path.join(tmp, "dup.json"),
                {"features": [{"id": "ft-1", "slug": "x", "capability": "cap-booking", "one_line": "x",
                               "doc": "notify/domain.md"}]})
    code, _, _ = run("persist_fills.py", "--root", root, "--spine", spine, "--fills", dup,
                     "--intent", "bi-340")
    check("fills: an id already in the model is refused (fills only add)", code == 2)
    nodoc = write(os.path.join(tmp, "nodoc.json"),
                  {"domains": [{"id": "dm-x", "slug": "x", "one_line": "x", "doc": "x/domain.md"}]})
    code, _, _ = run("persist_fills.py", "--root", root, "--spine", spine, "--fills", nodoc,
                     "--intent", "bi-340")
    check("fills: a page not on disk is refused", code == 2)

    good = write(os.path.join(tmp, "fills.json"), fills)
    code, out, _ = run("persist_fills.py", "--root", root, "--spine", spine, "--fills", good,
                       "--intent", "bi-340")
    s = yaml.safe_load(read(spine))
    cap = next(c for c in s["capabilities"] if c["id"] == "cap-reminders")
    check("fills: written (exit 0)", code == 0 and out["ok"] is True)
    check("fills: each new part is marked to be deepened",
          cap["status"] == "proposed" and cap["detail"] == "directional" and cap["metadata"]["deepen"] is True)
    check("fills: the new parts serve the intent", cap["intents"] == ["bi-340"])
    check("fills: the ICE entry is added", any(i["id"] == "ice-send-reminder" for i in s["ices"]))
    check("fills: the result's allow list names each page and the intent page",
          "product-os/notify/reminders/capability.md" in out["allow"]
          and "product-os/intents/bi-340.md" in out["allow"])
    page = read(os.path.join(root, "intents", "bi-340.md"))
    check("fills: the intent page's Touches list names the new domain and capability",
          "(domain) — adds" in page and "(capability) — adds" in page)

    noices = write(os.path.join(tmp, "po3", "_spine.yaml"), {"features": []})
    code, _, _ = run("persist_fills.py", "--root", os.path.join(tmp, "po3"), "--spine", noices,
                     "--fills", good, "--intent", "bi-340")
    check("fills: an ICE on a model with no ices list is refused", code == 2)
    empty = write(os.path.join(tmp, "empty.json"), {})
    code, out, _ = run("persist_fills.py", "--root", root, "--spine", spine, "--fills", empty,
                       "--intent", "bi-340")
    check("fills: nothing to fill writes nothing", code == 0 and out["allow"] == [])


def test_questions(tmp):
    rec = os.path.join(tmp, "ctx", "grounding-questions.md")
    ex = {"why": "The slice is built for it.", "examples": ["a clinic: the booking screen",
                                                             "a shop: the checkout page"]}
    qs = [dict(ex, id="Q-surface-1", blocking=True, question="Which screen does the patient test?",
               proposed_answer="the booking screen", basis={"kind": "model", "ref": "ux.md L4"}),
          dict(ex, id="Q-scope-1", blocking=False, question="Is a reminder in scope?",
               proposed_answer="yes", basis=None),
          dict(ex, id="Q-scale-1", blocking=False, question="How many bookings a day?",
               assume="about 200 a day"),
          dict(ex, id="Q-known-1", blocking=False, question="Who books?", settled=True,
               proposed_answer="the patient", basis={"kind": "memory", "ref": "domains/care.md L3"})]
    qpath = write(os.path.join(tmp, "q.json"), qs)
    checked = os.path.join(tmp, "q-checked.json")
    code, out, _ = run("record_questions.py", "proposals", "--questions", qpath, "--out", checked)
    data = json.loads(read(checked))
    check("proposals: an answer with no named basis is stripped", out["stripped"] == ["Q-scope-1"]
          and data["questions"][1]["proposed_answer"] is None)
    check("proposals: a backed answer is kept", data["questions"][0]["proposed_answer"] == "the booking screen")
    check("proposals: the count of questions with no proposed answer is right",
          code == 0 and out["no_proposed_answer"] == 2)
    check("proposals: a gap the model or memory answers is settled, never asked",
          out["settled"] == ["Q-known-1"] and all(q["id"] != "Q-known-1" for q in data["questions"]))
    badq = write(os.path.join(tmp, "badq.json"),
                 [{"id": "Q-two-1", "blocking": False, "question": "Who books and who pays?",
                   "why": "x", "examples": ["a", "b"]},
                  {"id": "Q-thin-1", "blocking": False, "question": "Who pays?", "examples": ["a"]}])
    code, out, _ = run("record_questions.py", "proposals", "--questions", badq,
                       "--out", os.path.join(tmp, "badq-out.json"))
    check("proposals: a question that asks two things, or lacks why or two examples, fails (exit 1)",
          code == 1 and set(out["shape_problems"]) == {"Q-two-1", "Q-thin-1"})

    split = write(os.path.join(tmp, "split.json"),
                  {"asked": data["questions"][:2], "assumptions": data["questions"][2:], "over_budget": False})
    code, out, _ = run("record_questions.py", "add", "--record", rec, "--issue", "795", "--split", split,
                       "--at", "2026-10-23T10:00:00Z", "--run", "shape-slice-1")
    check("add: asked questions and assumptions are recorded",
          code == 0 and out["added"] == ["Q-surface-1", "Q-scope-1", "Q-scale-1"])
    code, out, _ = run("record_questions.py", "check", "--record", rec, "--split", split)
    check("check: every asked question and assumption is in the record", code == 0 and out["ok"] is True)
    check("check: the asked ones are still unanswered", out["unanswered"] == ["Q-surface-1", "Q-scope-1"])

    ans = write(os.path.join(tmp, "answers.json"), [{"id": "Q-surface-1", "answer": "the booking screen"}])
    code, _, _ = run("record_questions.py", "answer", "--record", rec, "--answers", ans,
                     "--at", "2026-10-23T10:05:00Z", "--run", "shape-slice-1")
    check("answer: the answer is written", code == 0 and "user_answer: the booking screen" in read(rec))

    open_path = os.path.join(tmp, "open.json")
    code, out, _ = run("record_questions.py", "filter", "--record", rec, "--questions", qpath,
                       "--out", open_path)
    still = [q["id"] for q in json.loads(read(open_path))["open"]]
    check("filter: an answered question is never asked again", code == 0 and "Q-surface-1" not in still
          and out["dropped"] == 1)

    size = len(read(rec))
    code, out, _ = run("record_questions.py", "add", "--record", rec, "--issue", "795", "--split", split,
                       "--at", "2026-10-23T11:00:00Z", "--run", "shape-slice-2")
    check("add: the record only grows; an id already there is kept", code == 0 and out["added"] == []
          and len(read(rec)) == size)

    gap = write(os.path.join(tmp, "gap.json"),
                {"asked": [], "assumptions": [{"id": "Q-x-1", "blocking": False, "question": "?"}]})
    code, _, err = run("record_questions.py", "add", "--record", rec, "--issue", "795", "--split", gap,
                       "--at", "t", "--run", "r")
    check("add: a gap left open with no written assumption is refused", code == 2 and "assumption" in err)

    bad = write(os.path.join(tmp, "bad-ans.json"), [{"id": "Q-scale-1", "answer": "x"}])
    code, _, _ = run("record_questions.py", "answer", "--record", rec, "--answers", bad, "--at", "t",
                     "--run", "r")
    check("answer: an assumption is not answered as if it was asked", code == 2)

    miss = write(os.path.join(tmp, "miss.json"), {"asked": [{"id": "Q-new-1", "blocking": True}],
                                                  "assumptions": []})
    code, out, _ = run("record_questions.py", "check", "--record", rec, "--split", miss)
    check("check: a question missing from the record fails (exit 1)", code == 1 and out["missing"] == ["Q-new-1"])


def test_slice_check(tmp):
    root = os.path.join(tmp, "sc")
    entry = {"id": "sl-a", "slug": "a", "feature_refs": ["ft-1"], "vertical": "the booking screen",
             "intents": ["bi-340"], "record": "slices/sl-a.yaml"}
    spine = write(os.path.join(root, "_spine.yaml"), {"slices": [entry]})
    write(os.path.join(root, "intents", "bi-340.md"), "# Patients book online\n")
    write(os.path.join(root, "slices", "sl-a.yaml"),
          {"slice": {"id": "sl-a", "surface": {"name": "the booking screen", "persona_ref": "patient"}}})
    out_path = os.path.join(tmp, "slice-check.json")
    code, _, _ = run("slice_check.py", "--root", root, "--spine", spine, "--slice-id", "sl-a",
                     "--intent", "bi-340", "--out", out_path)
    rep = json.loads(read(out_path))
    check("slice check: a good slice reads valid", code == 0 and rep["valid"] is True)
    write(spine, {"slices": [dict(entry, status="proposed")]})
    code, _, _ = run("slice_check.py", "--root", root, "--spine", spine, "--slice-id", "sl-a",
                     "--intent", "bi-340", "--out", out_path)
    check("slice check: an old field on the spine entry is not valid",
          code == 1 and json.loads(read(out_path))["valid"] is False)
    write(spine, {"slices": [{k: v for k, v in entry.items() if k != "record"}]})
    code, _, _ = run("slice_check.py", "--root", root, "--spine", spine, "--slice-id", "sl-a",
                     "--intent", "bi-340", "--out", out_path)
    check("slice check: a spine entry with no record pointer is not valid", code == 1)
    write(spine, {"slices": [entry]})
    write(os.path.join(root, "slices", "sl-a.yaml"),
          {"slice": {"id": "sl-a", "surface": {"name": "the booking screen"}}})
    code, _, _ = run("slice_check.py", "--root", root, "--spine", spine, "--slice-id", "sl-a",
                     "--intent", "bi-340", "--out", out_path)
    check("slice check: a surface with no tester is not valid", code == 1)
    write(os.path.join(root, "slices", "sl-a.yaml"),
          {"slice": {"id": "sl-a", "surface": {"name": "the booking screen", "persona_ref": "patient"}}})
    write(spine, {"slices": [dict(entry, intents=["bi-999"])]})
    code, _, _ = run("slice_check.py", "--root", root, "--spine", spine, "--slice-id", "sl-a",
                     "--intent", "bi-999", "--out", out_path)
    rep = json.loads(read(out_path))
    check("slice check: a served intent with no page fails the linter",
          code == 1 and rep["lint"]["ok"] is False)


def test_approval(tmp):
    out = os.path.join(tmp, "approval.json")
    code, _, _ = run("record_approval.py", "--decision", "change", "--reply", "drop the reminder",
                     "--at", "t1", "--out", out)
    code2, _, _ = run("record_approval.py", "--decision", "yes", "--reply", "yes", "--at", "t2", "--out", out)
    rec = json.loads(read(out))
    check("approval: the latest answer is on top", code == 0 and code2 == 0 and rec["decision"] == "yes")
    check("approval: a change before it is kept in history",
          rec["history"] and rec["history"][0]["decision"] == "change")
    code, _, _ = run("record_approval.py", "--decision", "yes", "--reply", " ", "--at", "t3",
                     "--out", os.path.join(tmp, "a2.json"))
    check("approval: an empty reply is refused", code == 2 and not os.path.exists(os.path.join(tmp, "a2.json")))


def main():
    with tempfile.TemporaryDirectory() as tmp:
        root = test_intent_page(tmp)
        test_fills(tmp, root)
        test_questions(tmp)
        test_slice_check(tmp)
        test_approval(tmp)
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
