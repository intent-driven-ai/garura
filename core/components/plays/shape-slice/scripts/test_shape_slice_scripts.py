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
                "notify/reminders/send-reminder/feature.md",
                "notify/reminders/send-reminder/ice.md"):
        write(os.path.join(root, doc), "# page\n")
    fills = {"domains": [{"id": "dm-notify", "slug": "notify", "one_line": "Messages to people.",
                          "doc": "notify/domain.md"}],
             "capabilities": [{"id": "cap-reminders", "slug": "reminders", "domain": "dm-notify",
                               "one_line": "Reminders before a visit.",
                               "doc": "notify/reminders/capability.md"}],
             "features": [{"id": "ft-send-reminder", "slug": "send-reminder", "capability": "cap-reminders",
                           "one_line": "Send a reminder.",
                           "doc": "notify/reminders/send-reminder/feature.md"}],
             "ices": [{"id": "ice-send-reminder", "for": "ft-send-reminder", "for_kind": "feature",
                       "doc": "notify/reminders/send-reminder/ice.md"}]}
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
    check("check: every asked question and assumption is in the record", out["missing"] == [])
    check("check: asked questions with no answer fail (exit 1)",
          code == 1 and out["ok"] is False and out["unanswered"] == ["Q-surface-1", "Q-scope-1"])

    ans = write(os.path.join(tmp, "answers.json"), [{"id": "Q-surface-1", "answer": "the booking screen"}])
    code, _, _ = run("record_questions.py", "answer", "--record", rec, "--answers", ans,
                     "--at", "2026-10-23T10:05:00Z", "--run", "shape-slice-1")
    check("answer: the answer is written", code == 0 and "user_answer: the booking screen" in read(rec))
    code, out, _ = run("record_questions.py", "check", "--record", rec, "--split", split)
    check("check: one asked question still unanswered keeps it failing",
          code == 1 and out["unanswered"] == ["Q-scope-1"])
    size = len(read(rec))
    empty_ans = write(os.path.join(tmp, "empty-ans.json"), [{"id": "Q-scope-1", "answer": "  "}])
    code, _, err = run("record_questions.py", "answer", "--record", rec, "--answers", empty_ans,
                       "--at", "t", "--run", "r")
    check("answer: an answer with no text is refused, nothing written",
          code == 2 and "no text" in err and len(read(rec)) == size)
    ans2 = write(os.path.join(tmp, "answers2.json"), [{"id": "Q-scope-1", "answer": "no, later"}])
    run("record_questions.py", "answer", "--record", rec, "--answers", ans2, "--at", "t", "--run", "r")
    code, out, _ = run("record_questions.py", "check", "--record", rec, "--split", split)
    check("check: every asked question answered reads ok (exit 0)", code == 0 and out["ok"] is True)

    open_path = os.path.join(tmp, "open.json")
    code, out, _ = run("record_questions.py", "filter", "--record", rec, "--questions", qpath,
                       "--out", open_path)
    still = [q["id"] for q in json.loads(read(open_path))["open"]]
    check("filter: an answered question is never asked again", code == 0 and "Q-surface-1" not in still
          and out["dropped"] == 2)
    later = write(os.path.join(tmp, "later.json"),
                  [dict(ex, id="Q-screen-9", blocking=False,
                        question="  which SCREEN does the patient test  "),
                   dict(ex, id="Q-scope-1", blocking=False, question="Who pays for a visit?"),
                   dict(ex, id="Q-scale-1", blocking=False, question="How many bookings a day?")])
    code, out, _ = run("record_questions.py", "filter", "--record", rec, "--questions", later,
                       "--out", open_path)
    data_open = json.loads(read(open_path))
    ids = [q["id"] for q in data_open["open"]]
    check("filter: the same question under a new id is answered (matched by its text)",
          "Q-screen-9" not in ids and any(f["id"] == "Q-surface-1" for f in data_open["answered"]))
    check("filter: a different question that reuses an answered id is kept, under a new id",
          "Q-scope-1-2" in ids and out["renamed"] == {"Q-scope-1": "Q-scope-1-2"})
    check("filter: an open assumption with the same text keeps its id", "Q-scale-1" in ids)
    list_path = os.path.join(tmp, "open-list.json")
    code, out, _ = run("record_questions.py", "open-list", "--open", open_path, "--out", list_path)
    check("open-list: writes the open list as a JSON list",
          code == 0 and [q["id"] for q in json.loads(read(list_path))] == ids)
    code, _, _ = run("record_questions.py", "open-list", "--open", qpath, "--out", list_path)
    check("open-list: a file with no open list is refused", code == 2)

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


def test_answers(tmp):
    split = write(os.path.join(tmp, "ans-split.json"),
                  {"asked": [{"id": "Q-surface-1", "blocking": True}, {"id": "Q-scope-1", "blocking": False},
                             {"id": "Q-scale-1", "blocking": False}], "assumptions": []})
    reply = write(os.path.join(tmp, "reply.md"),
                  "Q-surface-1: the booking screen\non the phone too\n"
                  "- **Q-scope-1** — skip for now\nQ-other-1: what?\n")
    out_path = os.path.join(tmp, "answers.json")
    code, out, _ = run("record_questions.py", "answers", "--reply", reply, "--split", split,
                       "--out", out_path)
    got = json.loads(read(out_path))
    check("answers: builds answers.json from a reply that names the ids",
          code == 0 and got[0] == {"id": "Q-surface-1", "answer": "the booking screen\non the phone too"})
    check("answers: 'skip' is recorded as deferred, in the person's words",
          got[1] == {"id": "Q-scope-1", "answer": "skip for now", "decision": "deferred"})
    check("answers: a question not answered and an unknown id are reported",
          out["unanswered"] == ["Q-scale-1"] and out["unknown"] == ["Q-other-1"])
    reply2 = write(os.path.join(tmp, "reply2.md"), "1. the booking screen\n3) about 200\n")
    code, out, _ = run("record_questions.py", "answers", "--reply", reply2, "--split", split,
                       "--out", out_path)
    got = json.loads(read(out_path))
    check("answers: numbers map to the asked order",
          [a["id"] for a in got] == ["Q-surface-1", "Q-scale-1"] and got[1]["answer"] == "about 200")
    one = write(os.path.join(tmp, "one-split.json"),
                {"asked": [{"id": "Q-surface-1", "blocking": True}], "assumptions": []})
    reply3 = write(os.path.join(tmp, "reply3.md"), "The booking screen.\n")
    run("record_questions.py", "answers", "--reply", reply3, "--split", one, "--out", out_path)
    check("answers: a plain reply to one asked question is its answer",
          json.loads(read(out_path)) == [{"id": "Q-surface-1", "answer": "The booking screen."}])

    rec = os.path.join(tmp, "ans-ctx", "grounding-questions.md")
    ex = {"why": "x", "examples": ["a", "b"], "question": "Which screen?"}
    sp = write(os.path.join(tmp, "blk-split.json"),
               {"asked": [dict(ex, id="Q-surface-1", blocking=True)], "assumptions": []})
    run("record_questions.py", "add", "--record", rec, "--issue", "1", "--split", sp, "--at", "t", "--run", "r")
    dfr = write(os.path.join(tmp, "dfr.json"), [{"id": "Q-surface-1", "answer": "skip", "decision": "deferred"}])
    run("record_questions.py", "answer", "--record", rec, "--answers", dfr, "--at", "t", "--run", "r")
    code, out, _ = run("record_questions.py", "check", "--record", rec, "--split", sp)
    check("check: a blocking question that is deferred fails (exit 1)",
          code == 1 and out["blocking_deferred"] == ["Q-surface-1"])


def test_fills_paths(tmp):
    root = os.path.join(tmp, "pp")
    spine = write(os.path.join(root, "_spine.yaml"), {"domains": [], "capabilities": [], "features": []})
    write(os.path.join(root, "intents", "bi-1.md"), "# One\n")
    write(os.path.join(tmp, "outside.md"), "# outside\n")
    before = read(spine)
    for label, doc in (("'..'", "../outside.md"), ("an absolute path", os.path.join(tmp, "outside.md"))):
        f = write(os.path.join(tmp, "esc.json"),
                  {"domains": [{"id": "dm-x", "slug": "x", "one_line": "x", "doc": doc}]})
        code, _, err = run("persist_fills.py", "--root", root, "--spine", spine, "--fills", f,
                           "--intent", "bi-1")
        check(f"fills: a doc path with {label} is refused (exit 2), nothing written",
              code == 2 and "leaves the model folder" in err and read(spine) == before)
    os.symlink(tmp, os.path.join(root, "link"))
    f = write(os.path.join(tmp, "esc.json"),
              {"domains": [{"id": "dm-x", "slug": "x", "one_line": "x", "doc": "link/outside.md"}]})
    code, _, err = run("persist_fills.py", "--root", root, "--spine", spine, "--fills", f, "--intent", "bi-1")
    check("fills: a doc path through a symlink that leaves the model is refused",
          code == 2 and "leaves the model folder" in err and read(spine) == before)
    f = write(os.path.join(tmp, "ok.json"), {})
    code, _, _ = run("persist_fills.py", "--root", root, "--spine", spine, "--fills", f,
                     "--intent", "../bi-1")
    check("fills: an intent id that leaves the model folder is refused", code == 2)


def test_fills_undo(tmp):
    root = os.path.join(tmp, "pu")
    spine = write(os.path.join(root, "_spine.yaml"), {"domains": [], "capabilities": [], "features": []})
    page = write(os.path.join(root, "intents", "bi-1.md"), "# One\n\n**Outcome:** x\n")
    write(os.path.join(root, "notify", "domain.md"), "# page\n")
    fills = write(os.path.join(tmp, "u-fills.json"),
                  {"domains": [{"id": "dm-n", "slug": "notify", "one_line": "x", "doc": "notify/domain.md"}]})
    res = os.path.join(tmp, "u-persist.json")
    before = read(page)
    code, out, _ = run("persist_fills.py", "--root", root, "--spine", spine, "--fills", fills,
                       "--intent", "bi-1", "--out", res)
    check("fills: the result names the Touches lines it added",
          code == 0 and out["touches_added"] == ["- [notify](../notify/domain.md) (domain) — adds"]
          and "(domain) — adds" in read(page))
    code, out, _ = run("persist_fills.py", "--undo", res, "--root", root, "--intent", "bi-1")
    check("fills undo: the intent page is put back as it was before the fills",
          code == 0 and read(page) == before and out["how"] == "put back")
    run("persist_fills.py", "--root", root, "--spine", write(spine, {"domains": [], "capabilities": [],
                                                                      "features": []}),
        "--fills", fills, "--intent", "bi-1", "--out", res)
    with open(page, "a", encoding="utf-8") as fh:
        fh.write("\nA line the person added.\n")
    code, out, _ = run("persist_fills.py", "--undo", res, "--root", root, "--intent", "bi-1")
    text = read(page)
    check("fills undo: after a later edit only the added Touches lines are removed",
          code == 0 and "(domain) — adds" not in text and "A line the person added." in text
          and out["how"] == "lines removed")
    check("fills undo: the Touches heading this run made goes too, with no line under it",
          "**Touches:**" not in text)
    write(page, "# One\n\n**Touches:** none yet\n")
    run("persist_fills.py", "--root", root, "--spine", write(spine, {"domains": [], "capabilities": [],
                                                                      "features": []}),
        "--fills", fills, "--intent", "bi-1", "--out", res)
    with open(page, "a", encoding="utf-8") as fh:
        fh.write("\nA line the person added.\n")
    code, out, _ = run("persist_fills.py", "--undo", res, "--root", root, "--intent", "bi-1")
    text = read(page)
    check("fills undo: a page that said **Touches:** none yet keeps that line after a later edit",
          code == 0 and "**Touches:** none yet" in text and "A line the person added." in text
          and "(domain) — adds" not in text and out["how"] == "lines removed")
    free = "- fn-7 and fn-8 (features of cap-x) — moved under cap-x's folder"
    listed = f"# One\n\n**Touches:**\n- [notify](../notify/domain.md) (domain) — adds\n{free}\n"
    write(page, listed)
    run("persist_fills.py", "--root", root, "--spine", write(spine, {"domains": [], "capabilities": [],
                                                                      "features": []}),
        "--fills", fills, "--intent", "bi-1", "--out", res)
    check("fills: a Touches line in a form the scripts cannot read stays on the intent page",
          read(page) == listed and json.loads(read(res))["touches_added"] == [])
    commented = "# The clinic spine. Keep this note.\ndomains:\n  # booking first\n  - id: dm-b\n    slug: b\n"
    write(spine, commented + "capabilities: []\nfeatures: []\n")
    run("persist_fills.py", "--root", root, "--spine", spine, "--fills", fills, "--intent", "bi-1",
        "--out", res)
    text = read(spine)
    check("fills: the spine keeps its comments, and the new domain is added",
          "Keep this note." in text and "# booking first" in text
          and [d["id"] for d in yaml.safe_load(text)["domains"]] == ["dm-b", "dm-n"])


def test_slice_check(tmp):
    root = os.path.join(tmp, "sc")
    entry = {"id": "sl-a", "slug": "a", "feature_refs": ["ft-1"], "vertical": "the booking screen",
             "intents": ["bi-340"], "record": "slices/sl-a.yaml"}
    spine = write(os.path.join(root, "_spine.yaml"), {"slices": [entry]})
    write(os.path.join(root, "intents", "bi-340.md"), "# Patients book online\n")
    write(os.path.join(root, "slices", "sl-a.yaml"), RECORD)
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
    write(spine, {"slices": [{k: entry[k] for k in reversed(list(entry))}]})
    code, _, _ = run("slice_check.py", "--root", root, "--spine", spine, "--slice-id", "sl-a",
                     "--intent", "bi-340", "--out", out_path)
    check("slice check: the six fields in another order read valid", code == 0)
    write(spine, {"slices": [entry]})
    no_tester = {"slice": RECORD["slice"], "surface": {k: v for k, v in RECORD["surface"].items()
                                                       if k != "persona_ref"}}
    write(os.path.join(root, "slices", "sl-a.yaml"), no_tester)
    code, _, _ = run("slice_check.py", "--root", root, "--spine", spine, "--slice-id", "sl-a",
                     "--intent", "bi-340", "--out", out_path)
    rep = json.loads(read(out_path))
    check("slice check: a record with no persona_ref is not valid",
          code == 1 and rep["valid"] is False and any("persona_ref" in p for p in rep["problems"]))
    for field in ("name", "outcome", "intents", "slug"):
        bad = {"slice": {k: v for k, v in RECORD["slice"].items() if k != field},
               "surface": RECORD["surface"]}
        write(os.path.join(root, "slices", "sl-a.yaml"), bad)
        code, _, _ = run("slice_check.py", "--root", root, "--spine", spine, "--slice-id", "sl-a",
                         "--intent", "bi-340", "--out", out_path)
        check(f"slice check: a record with no slice.{field} is not valid", code == 1)
    old = {"slice": dict(RECORD["slice"], surface=RECORD["surface"])}
    write(os.path.join(root, "slices", "sl-a.yaml"), old)
    code, _, _ = run("slice_check.py", "--root", root, "--spine", spine, "--slice-id", "sl-a",
                     "--intent", "bi-340", "--out", out_path)
    check("slice check: a surface nested under slice (not slice.yaml v2) is not valid", code == 1)
    write(os.path.join(root, "slices", "sl-a.yaml"), RECORD)
    other = {"id": "sl-b", "slug": "b", "feature_refs": ["ft-1"], "vertical": "the booking screen",
             "intents": ["bi-340"], "record": "slices/sl-b.yaml"}
    write(os.path.join(root, "slices", "sl-b.yaml"),
          {"slice": dict(RECORD["slice"], id="sl-b", slug="b"),
           "surface": {k: v for k, v in RECORD["surface"].items() if k != "persona_ref"}})
    write(spine, {"slices": [entry, other]})
    code, _, _ = run("slice_check.py", "--root", root, "--spine", spine, "--slice-id", "sl-a",
                     "--intent", "bi-340", "--out", out_path)
    rep = json.loads(read(out_path))
    check("slice check: every other spine slice's record is checked, as a warning (it does "
          "not block this run)",
          not any("sl-b" in p for p in rep["problems"])
          and any("sl-b" in p and "persona_ref" in p for p in rep["warnings"]))
    write(spine, {"slices": [entry]})
    write(spine, {"slices": [dict(entry, intents=["bi-999"])]})
    code, _, _ = run("slice_check.py", "--root", root, "--spine", spine, "--slice-id", "sl-a",
                     "--intent", "bi-999", "--out", out_path)
    rep = json.loads(read(out_path))
    check("slice check: a served intent with no page fails the linter",
          code == 1 and rep["lint"]["ok"] is False)



THIN = ("Thin: proposed by `/shape-slice` from the person's answers; deepen with "
        "`/discover-capabilities`.")
ICE = ("## Agent intent (ICE)\n- Goal: a patient books a free visit with no phone call.\n"
       "- Limit: never book a slot that a doctor has closed for the day.\n"
       "- Fails if: a slot is booked twice by two patients at once.\n"
       "- Context: the patient uses the booking screen on a phone or a laptop.\n"
       "- Checked by: a patient books a slot and sees it in the list of visits.\n")


def feature_page(name, drop=None, thin=False, ice=ICE):
    sections = {"What it does": "A patient picks a free slot and books a visit with no phone call to the desk.",
                "Inputs / Outputs": "- In: the free slots of each doctor for the next two weeks.",
                "Rules & behavior": "- A slot that is booked is not shown to the next patient.",
                "Acceptance criteria": "- Given a free slot, when a patient books it, then it is gone.",
                "Out of scope": "- Paying for a visit, which the clinic does at the desk."}
    body = "".join(f"## {h}\n{t}\n\n" for h, t in sections.items() if h != drop)
    return f"# Feature: {name}\n\n{body}" + (THIN + "\n\n" if thin else "") + ice


CAP_PAGE = ("# Capability: Booking\n\n## Directional intent\nPatients book, move and cancel "
            "their visits without a phone call to the clinic desk, at any hour of the day.\n")
DOM_PAGE = ("# Theme: Patient care\n\n## Intent\nThe clinic serves its patients well: they get a "
            "visit when they need one, and they know what happens next.\n")


def test_fills_v11(tmp):
    root = os.path.join(tmp, "v11")
    write(os.path.join(root, "care", "domain.md"), DOM_PAGE)
    write(os.path.join(root, "capabilities", "cap-x", "capability.md"),
          CAP_PAGE + "\nSee [the slot feature](../../features/fn-a/feature.md).\n")
    write(os.path.join(root, "features", "fn-a", "feature.md"),
          feature_page("Pick a slot") + "\nServes [the intent](../../intents/bi-1.md).\n")
    write(os.path.join(root, "capabilities", "cap-x", "fn-c", "feature.md"), feature_page("Move a visit"))
    write(os.path.join(root, "intents", "bi-1.md"), "# Patients book online\n\n**Touches:** none yet\n")
    spine = write(os.path.join(root, "_spine.yaml"),
                  {"domains": [{"id": "dm-care", "slug": "care", "one_line": "x", "doc": "care/domain.md"}],
                   "capabilities": [{"id": "cap-x", "slug": "cap-x", "domain": "", "intents": [],
                                     "one_line": "x", "doc": "capabilities/cap-x/capability.md"}],
                   "features": [{"id": "fn-a", "slug": "fn-a", "capability": "cap-x", "one_line": "x",
                                 "doc": "features/fn-a/feature.md"},
                                {"id": "fn-c", "slug": "fn-c", "capability": "cap-x", "one_line": "x",
                                 "doc": "capabilities/cap-x/fn-c/feature.md"}],
                   "slices": []})
    # a new feature page is written where it belongs: under the capability's folder after the move
    write(os.path.join(root, "care", "cap-x", "fn-b", "feature.md"),
          feature_page("Send a reminder").replace(ICE, "> Thin ICE: proposed by /shape-slice.\n\n" + ICE))
    fills = {"updates": [{"id": "cap-x", "kind": "capability", "add_intents": ["bi-1"],
                          "domain": "dm-care", "page": True}],
             "features": [{"id": "fn-b", "slug": "fn-b", "capability": "cap-x", "one_line": "Send a reminder.",
                           "doc": "care/cap-x/fn-b/feature.md"}],
             "thin": ["fn-b"]}
    f = write(os.path.join(tmp, "v11-fills.json"), fills)
    res = os.path.join(tmp, "v11-persist.json")
    code, out, err = run("persist_fills.py", "--root", root, "--spine", spine, "--fills", f,
                         "--intent", "bi-1", "--out", res)
    s = yaml.safe_load(read(spine))
    cap = next(c for c in s["capabilities"] if c["id"] == "cap-x")
    fa = next(x for x in s["features"] if x["id"] == "fn-a")
    fb = next(x for x in s["features"] if x["id"] == "fn-b")
    check("fills v11: an existing capability is filled (exit 0): it gains the intent and the domain",
          code == 0 and cap["intents"] == ["bi-1"] and cap["domain"] == "dm-care"
          and out["updated"] == ["cap-x"])
    check("fills v11: the capability's page and its feature's page move under the domain folder",
          cap["doc"] == "care/cap-x/capability.md" and fa["doc"] == "care/cap-x/fn-a/feature.md"
          and os.path.isfile(os.path.join(root, "care/cap-x/fn-a/feature.md"))
          and not os.path.exists(os.path.join(root, "capabilities", "cap-x"))
          and not os.path.exists(os.path.join(root, "features", "fn-a")))
    check("fills v11: moved names every part whose page moved, a feature inside the capability's "
          "folder too",
          {m["id"] for m in out["moved"]} == {"cap-x", "fn-a", "fn-c"}
          and {"id": "fn-c", "from": "capabilities/cap-x/fn-c/feature.md",
               "to": "care/cap-x/fn-c/feature.md"} in out["moved"])
    check("fills v11: the result names the moves and the old paths for the guard",
          {m["id"] for m in out["moved"]} == {"cap-x", "fn-a", "fn-c"}
          and "product-os/capabilities/cap-x/capability.md" in out["remove_only"]
          and "product-os/care/cap-x/fn-a/feature.md" in out["allow"])
    check("fills v11: every link to a moved page, and inside one, is fixed",
          "](fn-a/feature.md)" in read(os.path.join(root, "care/cap-x/capability.md"))
          and "](../../../intents/bi-1.md)" in read(os.path.join(root, "care/cap-x/fn-a/feature.md")))
    page = read(os.path.join(root, "intents", "bi-1.md"))
    check("fills v11: the filled capability is on the Touches list, marked changes",
          "[cap-x](../care/cap-x/capability.md) (capability) — changes" in page)
    fb_page = read(os.path.join(root, "care/cap-x/fn-b/feature.md"))
    check("fills v11: a thin part gets metadata.thin and exactly one Thin line before its ICE",
          fb["metadata"]["thin"] is True and fb_page.count(THIN) == 1
          and "> Thin ICE" not in fb_page and (THIN + "\n\n## Agent intent (ICE)") in fb_page)
    code, out2, _ = run("persist_fills.py", "--undo", res, "--root", root, "--intent", "bi-1")
    check("fills v11 undo: the page is put back with its **Touches:** none yet line",
          code == 0 and "**Touches:** none yet" in read(os.path.join(root, "intents", "bi-1.md")))

    root2 = os.path.join(tmp, "v11b")
    write(os.path.join(root2, "care", "domain.md"), DOM_PAGE)
    write(os.path.join(root2, "capabilities", "cap-y", "capability.md"), CAP_PAGE)
    write(os.path.join(root2, "intents", "bi-1.md"), "# One\n")
    sp2 = write(os.path.join(root2, "_spine.yaml"),
                {"domains": [{"id": "dm-care", "slug": "care", "one_line": "x", "doc": "care/domain.md"}],
                 "capabilities": [{"id": "cap-z", "slug": "z", "domain": "dm-care", "one_line": "x",
                                   "doc": "care/z/capability.md"}], "features": []})
    before = read(sp2)
    f = write(os.path.join(tmp, "v11b.json"),
              {"capabilities": [{"id": "cap-y", "slug": "y", "domain": "dm-care", "one_line": "x",
                                 "doc": "capabilities/cap-y/capability.md"}]})
    code, _, err = run("persist_fills.py", "--root", root2, "--spine", sp2, "--fills", f, "--intent", "bi-1")
    check("fills v11: a new capability with a domain but a page in the holding folder is refused",
          code == 2 and "outside its folder" in err and read(sp2) == before)
    f = write(os.path.join(tmp, "v11c.json"),
              {"updates": [{"id": "cap-z", "kind": "capability", "domain": "dm-other"}]})
    code, _, err = run("persist_fills.py", "--root", root2, "--spine", sp2, "--fills", f, "--intent", "bi-1")
    check("fills v11: an update never changes a domain the part already has", code == 2
          and "already has domain" in err)
    f = write(os.path.join(tmp, "v11d.json"), {"updates": [{"id": "cap-none", "kind": "capability"}]})
    code, _, err = run("persist_fills.py", "--root", root2, "--spine", sp2, "--fills", f, "--intent", "bi-1")
    check("fills v11: an update of a part not in the spine is refused", code == 2 and "not in the spine" in err)


def test_slice_check_v11(tmp):
    root = os.path.join(tmp, "scv")
    write(os.path.join(root, "care", "domain.md"), DOM_PAGE)
    write(os.path.join(root, "care", "booking", "capability.md"), CAP_PAGE)
    write(os.path.join(root, "care", "booking", "fn-old", "feature.md"),
          feature_page("Old one", drop="Out of scope"))
    write(os.path.join(root, "intents", "bi-340.md"), "# Patients book online\n")
    base_spine = {"domains": [{"id": "dm-care", "slug": "care", "one_line": "x", "doc": "care/domain.md",
                               "detail": "directional"}],
                  "capabilities": [{"id": "cap-b", "slug": "booking", "domain": "dm-care", "one_line": "x",
                                    "detail": "directional", "doc": "care/booking/capability.md"}],
                  "features": [{"id": "fn-old", "slug": "fn-old", "capability": "cap-b", "one_line": "x",
                                "doc": "care/booking/fn-old/feature.md"}],
                  "slices": []}
    spine = write(os.path.join(root, "_spine.yaml"), base_spine)
    base = os.path.join(tmp, "lint-before-run.json")
    code, _, _ = run("slice_check.py", "baseline", "--root", root, "--spine", spine, "--out", base)
    held = json.loads(read(base))["errors"]
    check("slice check baseline: the older error is kept, with its path in the model",
          code == 0 and any(e.startswith("care/booking/fn-old/feature.md:") for e in held))
    write(os.path.join(root, "care", "booking", "fn-new", "feature.md"), feature_page("New one"))
    entry = {"id": "sl-a", "slug": "a", "feature_refs": ["fn-new"], "vertical": "the booking screen",
             "intents": ["bi-340"], "record": "slices/sl-a.yaml"}
    sp = dict(base_spine, features=base_spine["features"] + [
        {"id": "fn-new", "slug": "fn-new", "capability": "cap-b", "one_line": "x",
         "doc": "care/booking/fn-new/feature.md"}], slices=[entry])
    write(spine, sp)
    write(os.path.join(root, "slices", "sl-a.yaml"), dict(RECORD, slice=dict(RECORD["slice"], feature_refs=["fn-new"])))
    out_path = os.path.join(tmp, "scv.json")
    args = ("--root", root, "--spine", spine, "--slice-id", "sl-a", "--intent", "bi-340",
            "--baseline", base, "--out", out_path)
    code, _, _ = run("slice_check.py", *args)
    rep = json.loads(read(out_path))
    check("slice check: an older error in a page the slice does not use is a warning, not a stop",
          code == 0 and rep["valid"] is True and len(rep["older_problems"]) == 1
          and "fn-old" in rep["older_problems"][0])
    write(os.path.join(root, "care", "booking", "fn-new", "feature.md"),
          feature_page("New one", drop="Rules & behavior"))
    code, _, _ = run("slice_check.py", *args)
    rep = json.loads(read(out_path))
    check("slice check: a problem in the slice's own page stops it",
          code == 1 and any("fn-new" in p for p in rep["problems"]))
    write(os.path.join(root, "care", "booking", "fn-new", "feature.md"), feature_page("New one"))
    write(spine, dict(sp, slices=[dict(entry, feature_refs=["fn-new", "fn-old"])]))
    write(os.path.join(root, "slices", "sl-a.yaml"),
          dict(RECORD, slice=dict(RECORD["slice"], feature_refs=["fn-new", "fn-old"])))
    code, _, _ = run("slice_check.py", *args)
    rep = json.loads(read(out_path))
    check("slice check: an older problem in a page the slice now uses stops it (the run fixes it)",
          code == 1 and any("fn-old" in p for p in rep["problems"]) and rep["older_problems"] == [])
    write(spine, sp)
    write(os.path.join(root, "slices", "sl-a.yaml"), dict(RECORD, slice=dict(RECORD["slice"], feature_refs=["fn-new"])))
    write(os.path.join(root, "care", "orphan", "capability.md"), CAP_PAGE)
    code, _, _ = run("slice_check.py", *args)
    rep = json.loads(read(out_path))
    check("slice check: a new error the baseline did not have stops it",
          code == 1 and any(p.startswith("new problem:") and "orphan" in p for p in rep["problems"]))
    os.remove(os.path.join(root, "care", "orphan", "capability.md"))
    thin_sp = dict(sp, features=[dict(f, metadata={"thin": True}) if f["id"] == "fn-new" else f
                                 for f in sp["features"]])
    write(spine, thin_sp)
    code, _, _ = run("slice_check.py", *args)
    rep = json.loads(read(out_path))
    check("slice check: metadata.thin with no Thin line is thin mark drift",
          code == 1 and any("thin mark drift" in p for p in rep["problems"]))
    write(spine, sp)
    fills_thin = write(os.path.join(tmp, "scv-fills.json"), {"thin": ["fn-new"]})
    code, _, _ = run("slice_check.py", *args, "--fills", fills_thin)
    rep = json.loads(read(out_path))
    check("slice check: a part listed thin in the fills with no Thin line on its page is a thin problem",
          code == 1 and any("thin mark drift" in p and "fn-new" in p and "listed in the fills" in p
                            for p in rep["problems"]))
    ices_sp = dict(thin_sp, ices=[])
    write(spine, ices_sp)
    code, _, _ = run("slice_check.py", *args)
    rep = json.loads(read(out_path))
    check("slice check: a thin part with no ICE page for its Thin line is a thin problem",
          code == 1 and any("no ICE page" in p and "fn-new" in p for p in rep["problems"]))
    write(spine, thin_sp)
    write(os.path.join(root, "care", "booking", "fn-new", "feature.md"), feature_page("New one", thin=True))
    code, _, _ = run("slice_check.py", *args)
    check("slice check: both thin marks, with the minimum lines, read valid", code == 0)
    write(spine, sp)
    code, _, _ = run("slice_check.py", *args)
    rep = json.loads(read(out_path))
    check("slice check: a Thin line with no metadata.thin on the spine is a thin problem",
          code == 1 and any("no metadata.thin" in p for p in rep["problems"]))
    write(spine, thin_sp)
    no_limit = ICE.replace("- Limit: never book a slot that a doctor has closed for the day.\n", "")
    write(os.path.join(root, "care", "booking", "fn-new", "feature.md"),
          feature_page("New one", thin=True, ice=no_limit))
    code, _, _ = run("slice_check.py", *args)
    rep = json.loads(read(out_path))
    check("slice check: a thin ICE with no Limit fails", code == 1
          and any("lacks Limit" in p for p in rep["problems"]))


def test_questions_v11(tmp):
    ex = {"why": "The slice is built for it.", "examples": ["a clinic: a booking screen", "a shop: a cart"]}
    qs = [dict(ex, id="Q-surface-1", topic="surface", blocking=True,
               question="Which screen does the patient test the booking on?"),
          dict(ex, id="Q-pay-1", topic="payment", blocking=True,
               question="Who pays for a visit the patient misses?"),
          dict(ex, id="Q-scope-1", topic="scope", blocking=False,
               question="Is a reminder in scope for the first slice?", proposed_answer="yes",
               basis={"kind": "model", "ref": "intents/bi-340.md L4"})]
    qpath = write(os.path.join(tmp, "v11-q.json"), qs)
    checked = os.path.join(tmp, "v11-qc.json")
    run("record_questions.py", "proposals", "--questions", qpath, "--out", checked)
    rec = os.path.join(tmp, "v11-ctx", "grounding-questions.md")
    code, out, _ = run("record_questions.py", "filter", "--record", rec, "--questions", checked,
                       "--out", os.path.join(tmp, "v11-open.json"))
    check("filter: reads the proposals output (its questions) with no file made by hand",
          code == 0 and out["open"] == 3)
    split = write(os.path.join(tmp, "v11-split.json"), {"asked": qs, "assumptions": []})
    early, rest = os.path.join(tmp, "v11-early.json"), os.path.join(tmp, "v11-rest.json")
    code, out, _ = run("record_questions.py", "early", "--split", split, "--early-out", early,
                       "--rest-out", rest)
    check("early: only a blocking gap with no proposed answer is asked first, never the surface",
          code == 0 and out["early"] == ["Q-pay-1"] and out["brief"] == ["Q-surface-1", "Q-scope-1"])
    reply = write(os.path.join(tmp, "v11-reply.md"), "yes\nQ-surface-1: the booking screen on a phone\n")
    ans = os.path.join(tmp, "v11-answers.json")
    code, out, _ = run("record_questions.py", "answers", "--reply", reply, "--split", rest, "--out", ans)
    got = {a["id"]: a for a in json.loads(read(ans))}
    check("answers: a plain yes accepts each question the reply does not answer by its id",
          code == 0 and got["Q-scope-1"] == {"id": "Q-scope-1", "answer": "yes — accepted as proposed",
                                             "decision": "accepted"}
          and got["Q-surface-1"]["answer"] == "the booking screen on a phone")
    one = write(os.path.join(tmp, "v11-one.json"), {"asked": [qs[2]], "assumptions": []})
    reply = write(os.path.join(tmp, "v11-reply2.md"), "yes\n")
    run("record_questions.py", "answers", "--reply", reply, "--split", one, "--out", ans)
    check("answers: a bare yes to one question is an acceptance, not its answer text",
          json.loads(read(ans))[0]["decision"] == "accepted")
    msg = write(os.path.join(tmp, "v11-early.md"),
                "You decide who pays for a missed visit, in Q-pay-1. We shape the slice after your answer.\n\n"
                "## Questions\n\n### Q-pay-1\n**Question** Who pays?\n**Answer** no proposed answer yet\n"
                "**Why it matters** x\n**Example** a clinic; a shop\n")
    code, out, _ = run("record_questions.py", "brief", "--brief", msg, "--split", early, "--early")
    check("brief --early: an opening that names a question id, and the four parts, pass",
          code == 0 and out["ok"] is True)
    code, out, _ = run("record_questions.py", "brief", "--brief", msg, "--split", early)
    check("brief: the full brief needs each section heading, and names the missing ones",
          code == 1 and "no '## Hidden file' heading" in out["problems"])


RECORD = {"slice": {"id": "sl-a", "slug": "a", "name": "Self booking",
                    "outcome": "A patient books a visit.", "feature_refs": ["ft-1"],
                    "vertical": "the booking screen", "intents": ["bi-340"]},
          "surface": {"id": "sf-booking", "name": "the booking screen", "persona_ref": "patient",
                      "user_action": "books a free slot"}}


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
    code, res, _ = run("record_approval.py", "verify", "--file", out)
    check("approval verify: a recorded yes lets the commit go (exit 0)", code == 0 and res["ok"] is True)
    for decision in ("change", "stop"):
        p = os.path.join(tmp, f"a-{decision}.json")
        run("record_approval.py", "--decision", decision, "--reply", decision, "--at", "t", "--out", p)
        code, res, _ = run("record_approval.py", "verify", "--file", p)
        check(f"approval verify: {decision} blocks the commit (exit 1)", code == 1 and res["ok"] is False)
    code, _, _ = run("record_approval.py", "verify", "--file", os.path.join(tmp, "none.json"))
    check("approval verify: no approval file blocks the commit (exit 2)", code == 2)


def test_round2(tmp):
    one = write(os.path.join(tmp, "r2-split.json"),
                {"asked": [{"id": "Q-surface-1", "blocking": False}], "assumptions": []})
    out_path = os.path.join(tmp, "r2-answers.json")
    reply = write(os.path.join(tmp, "r2-reply.md"), "Skip the dashboard, use the CLI\n")
    code, out, _ = run("record_questions.py", "answers", "--reply", reply, "--split", one,
                       "--out", out_path)
    check("answers: a reply that starts with 'skip' and says more is unclear, not deferred",
          code == 0 and json.loads(read(out_path)) == [] and out["unclear"] == ["Q-surface-1"]
          and out["unanswered"] == [])
    rec = os.path.join(tmp, "r2-ctx", "grounding-questions.md")
    sp = write(os.path.join(tmp, "r2-q.json"),
               {"asked": [{"id": "Q-surface-1", "blocking": False, "question": "Which screen?"}],
                "assumptions": []})
    run("record_questions.py", "add", "--record", rec, "--issue", "1", "--split", sp, "--at", "t", "--run", "r")
    bare = write(os.path.join(tmp, "r2-bare.json"), [{"id": "Q-surface-1", "answer": "skip"}])
    run("record_questions.py", "answer", "--record", rec, "--answers", bare, "--at", "t", "--run", "r")
    check("answer: a bare 'skip' with no decision is recorded as deferred",
          "user_decision: deferred" in read(rec))
    qs = write(os.path.join(tmp, "r2-shape.json"),
               [{"id": "Q-a-1", "blocking": False, "question": "Which of the options above do you pick?",
                 "why": "x", "examples": ["a", "b"]}])
    code, out, _ = run("record_questions.py", "proposals", "--questions", qs,
                       "--out", os.path.join(tmp, "r2-shape-out.json"))
    check("proposals: a question that points to other text does not stand alone (exit 1)",
          code == 1 and "stand alone" in json.dumps(out["shape_problems"]))
    good = ("You decide where a patient tests the booking. Each question has a proposed answer.\n\n"
            + "".join(f"## {h}\n- x\n\n" for h in ("What you run", "Who tests it", "Features",
                                                     "Hidden file", "Left out", "Assumptions",
                                                     "Model check"))
            + "## Questions\n\n### Q-surface-1\n**Question** Which surface does a patient test the booking on?\n"
            "**Answer** proposed: the booking screen\n**Why it matters** A slice has one surface.\n"
            "**Example** A clinic: a web page. A bank: a phone app.\n")
    msg = write(os.path.join(tmp, "r2-msg.md"), good)
    code, out, _ = run("record_questions.py", "brief", "--brief", msg, "--split", one)
    check("brief: an opening, the headings and the four parts pass (exit 0)",
          code == 0 and out["ok"] is True)
    write(msg, good.replace("You decide where a patient tests the booking. ", "Here we go. "))
    code, out, _ = run("record_questions.py", "brief", "--brief", msg, "--split", one)
    check("brief: an opening that does not say what the person decides fails (exit 1)",
          code == 1 and any("decides" in p for p in out["problems"]))
    write(msg, good.replace("**Example** A clinic: a web page. A bank: a phone app.\n", ""))
    code, out, _ = run("record_questions.py", "brief", "--brief", msg, "--split", one)
    check("brief: a question with no Example part fails (exit 1)",
          code == 1 and any("Example" in p for p in out["problems"]))


def test_merge_proposals(tmp):
    """propose-answers output goes into the questions by script, never by an agent (Round 2)."""
    base = {"why": "The slice is built for it.", "examples": ["a clinic: a booking screen", "a shop: a cart"]}
    qs = [dict(base, id="Q-pay-1", blocking=True, topic="payment",
               question="Which way does a patient pay for a booking?"),
          dict(base, id="Q-time-1", blocking=False, topic="time",
               question="How long does a patient keep a free slot?"),
          dict(base, id="Q-size-1", blocking=False, topic="size",
               question="How many bookings does the clinic take each day?"),
          dict(base, id="Q-name-1", blocking=False, topic="name",
               question="Which name does the booking screen show first?")]
    qpath = write(os.path.join(tmp, "merge", "questions.json"), qs)
    props = write(os.path.join(tmp, "merge", "proposals.json"), {"proposals": [
        {"group": "Q-pay-1", "closed_by": "proposal", "answer": "by card at the desk",
         "basis": {"kind": "model", "ref": "care/booking/capability.md:12-14"}, "context": "x"},
        {"group": "Q-time-1", "closed_by": "settled", "why": "the model sets ten minutes",
         "basis": {"kind": "memory", "ref": "knowledge/domains/care.md:40"}},
        {"group": "Q-size-1", "closed_by": "proposal", "answer": "about fifty",
         "basis": {"kind": "web", "ref": "a blog post"}, "context": "x"},
        {"group": "Q-name-1", "closed_by": "proposal", "answer": "the doctor's name",
         "basis": {"kind": "person", "ref": ""}, "context": "x"}]})
    code, out, _ = run("record_questions.py", "merge-proposals", "--questions", qpath,
                       "--proposals", props, "--out", qpath)
    got = {q["id"]: q for q in json.loads(read(qpath))}
    check("merge-proposals: a backed proposal sets proposed_answer and basis {kind, ref}",
          code == 0 and got["Q-pay-1"]["proposed_answer"] == "by card at the desk"
          and got["Q-pay-1"]["basis"] == {"kind": "model", "ref": "care/booking/capability.md:12-14"})
    check("merge-proposals: closed_by settled sets settled and settled_basis",
          got["Q-time-1"]["settled"] is True
          and got["Q-time-1"]["settled_basis"] == {"kind": "memory", "ref": "knowledge/domains/care.md:40"})
    check("merge-proposals: another basis kind or an empty ref leaves no proposed answer",
          got["Q-size-1"]["proposed_answer"] is None and got["Q-size-1"]["basis"] is None
          and got["Q-name-1"]["proposed_answer"] is None)
    check("merge-proposals: it counts the questions with no proposed answer",
          out["no_proposed_answer"] == 2 and out["proposed"] == ["Q-pay-1"]
          and out["settled"] == ["Q-time-1"])
    checked = os.path.join(tmp, "merge", "checked.json")
    run("record_questions.py", "proposals", "--questions", qpath, "--out", checked)
    data = json.loads(read(checked))
    check("merge-proposals then proposals: a settled gap with a settled_basis is never asked",
          [q["id"] for q in data["settled"]] == ["Q-time-1"]
          and "Q-time-1" not in [q["id"] for q in data["questions"]])
    before = read(qpath)
    bad = write(os.path.join(tmp, "merge", "bad.json"), {"proposals": [
        {"group": "Q-none-9", "closed_by": "proposal", "answer": "x",
         "basis": {"kind": "model", "ref": "a.md:1"}}]})
    code, _, err = run("record_questions.py", "merge-proposals", "--questions", qpath,
                       "--proposals", bad, "--out", qpath)
    check("merge-proposals: a proposal for an id that is not a question is refused, nothing written",
          code == 2 and "Q-none-9" in err and read(qpath) == before)


def test_safe_write(tmp):
    sys.path.insert(0, HERE)
    import safe_write
    folder = os.path.join(tmp, "safe", "new", "folder")
    path = os.path.join(folder, "page.md")
    safe_write.atomic_write(path, "first\n")
    check("safe_write: makes the folder and writes the text", read(path) == "first\n")
    safe_write.atomic_write(path, "second\n")
    check("safe_write: replaces the file whole, and leaves no temp file",
          read(path) == "second\n" and os.listdir(folder) == ["page.md"])

    try:
        safe_write.atomic_write(path, 42)  # not text: the write fails part way
    except TypeError:
        pass
    check("safe_write: a failed write keeps the old file and removes its temp file",
          read(path) == "second\n" and os.listdir(folder) == ["page.md"])
    calls = []
    for name in sorted(os.listdir(HERE)):
        if name.endswith(".py") and not name.startswith("test_") and name != "safe_write.py":
            text = read(os.path.join(HERE, name))
            if "os.replace(" in text or "mkstemp(" in text:
                calls.append(name)
    check("safe_write: no other script of the play calls os.replace or tempfile.mkstemp", calls == [])
    users = [n for n in ("persist_fills.py", "persist_slice.py", "write_hidden_file.py",
                         "render_brief.py", "write_intent_page.py")
             if "from safe_write import atomic_write" not in read(os.path.join(HERE, n))]
    check("safe_write: the five writing scripts use it", users == [])


def test_plain_yes(tmp):
    ex = {"why": "x", "examples": ["a clinic: a", "a shop: b"], "blocking": False}
    qs = [dict(ex, id="Q-scope-1", question="Is a reminder in scope?", proposed_answer="yes",
               basis={"kind": "model", "ref": "intents/bi-340.md L4"}),
          dict(ex, id="Q-flag-1", question="Where does the flag show?", proposed_answer=None)]
    sp = write(os.path.join(tmp, "py-split.json"), {"asked": qs, "assumptions": []})
    reply = write(os.path.join(tmp, "py-reply.md"), "yes\n")
    ans = os.path.join(tmp, "py-answers.json")
    code, out, _ = run("record_questions.py", "answers", "--reply", reply, "--split", sp, "--out", ans)
    check("answers: a plain yes accepts only a question that has a proposed answer",
          code == 0 and [a["id"] for a in json.loads(read(ans))] == ["Q-scope-1"]
          and out["unanswered"] == ["Q-flag-1"])
    rec = os.path.join(tmp, "py-ctx", "grounding-questions.md")
    run("record_questions.py", "add", "--record", rec, "--issue", "1", "--split", sp, "--at", "t", "--run", "r")
    run("record_questions.py", "answer", "--record", rec, "--answers", ans, "--at", "t", "--run", "r")
    code, out, _ = run("record_questions.py", "check", "--record", rec, "--split", sp)
    check("check: a question a plain yes could not accept is still open (exit 1)",
          code == 1 and out["unanswered"] == ["Q-flag-1"])
    own = write(os.path.join(tmp, "py-own.json"), [{"id": "Q-flag-1", "answer": "in the run's evidence"}])
    run("record_questions.py", "answer", "--record", rec, "--answers", own, "--at", "t2", "--run", "r")
    again = write(os.path.join(tmp, "py-again.json"),
                  [{"id": "Q-flag-1", "answer": "yes — accepted as proposed", "decision": "accepted"},
                   {"id": "Q-scope-1", "answer": "yes — accepted as proposed", "decision": "accepted"}])
    code, out, _ = run("record_questions.py", "answer", "--record", rec, "--answers", again,
                       "--at", "t3", "--run", "r")
    text = read(rec)
    check("answer: a later plain yes never writes over the person's own answer",
          code == 0 and out["kept"] == ["Q-flag-1"] and out["answered"] == ["Q-scope-1"]
          and "in the run's evidence" in text)


def main():
    with tempfile.TemporaryDirectory() as tmp:
        root = test_intent_page(tmp)
        test_fills(tmp, root)
        test_questions(tmp)
        test_answers(tmp)
        test_fills_paths(tmp)
        test_fills_undo(tmp)
        test_slice_check(tmp)
        test_approval(tmp)
        test_round2(tmp)
        test_fills_v11(tmp)
        test_slice_check_v11(tmp)
        test_questions_v11(tmp)
        test_merge_proposals(tmp)
        test_plain_yes(tmp)
        test_safe_write(tmp)
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
