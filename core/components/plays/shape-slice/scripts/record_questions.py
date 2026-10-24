#!/usr/bin/env python3
"""
record_questions.py — the question record of /shape-slice (C5, C10; standards/rules/user-questions.md).

Every question the run asks a person, and every gap it leaves as an assumption, is kept in
the issue's short-term memory, in {stm_base}<issue>/context/grounding-questions.md. The file
only grows. A question answered there is a fact and is never asked again.

The file is Markdown with one fenced YAML block that holds `questions:`, one entry each:
    id, kind (asked | assumption), blocking, asked_at, topic, question, proposed_answer,
    basis, pipeline_source, pipeline_guess, impact_if_unknown, user_decision, user_answer,
    resolved_at, resolved_by_run

    python3 record_questions.py proposals --questions <q.json> --out <q-checked.json>
    python3 record_questions.py filter    --record <md> --questions <q-checked.json> --out <open.json>
    python3 record_questions.py open-list --open <open.json> --out <open-list.json>
    python3 record_questions.py early     --split <split.json> --early-out <early-split.json> --rest-out <brief-split.json>
    python3 record_questions.py add       --record <md> --issue <n> --split <split.json> --at <ts> --run <run id>
    python3 record_questions.py answers   --reply <reply.md> --split <split.json> --out <answers.json>
    python3 record_questions.py answer    --record <md> --answers <answers.json> --at <ts> --run <run id>
    python3 record_questions.py brief     --brief <brief.md> --split <split.json> [--early]
    python3 record_questions.py check     --record <md> --split <split.json>

A question (q.json is a JSON list, or the object `proposals` writes) has: id, blocking (true/false), question, and may have
topic, why, examples, proposed_answer, basis {kind: model|memory|person, ref}, assume.

  proposals — three checks before anything is shown. (1) A gap the model or memory already
              answers (`settled: true`, with a named basis) is moved to `settled` and never
              asked (C2). (2) The cardinal rule (C10): a proposed answer with no named basis is
              STRIPPED (set to null, never replaced). (3) The shape the rule for asking a person
              gives (C3): each question asks one thing (no " and " in it, one "?"), stands
              alone (no word that points to other text, such as "above" or "the previous",
              and five words or more), has a "why" and at least two examples. This is the
              floor a script can test; the person at the checkpoint judges the rest. Prints {questions, settled, no_proposed_answer,
              stripped, shape_problems}; exit 1 when a question breaks the shape.
  filter    — drops each question already answered in the record (C5). --questions takes a
              JSON list, or the object `proposals` writes ({questions, settled, ...}): it reads
              its `questions`. A question counts as
              answered when its question text, normalized (lower case, punctuation and extra
              spaces removed), matches an answered entry's — not by id alone. A question whose
              id is already in the record for a DIFFERENT question is kept, under a new id
              (<id>-2, <id>-3, ...), so it is asked and recorded on its own; prints
              {open, answered, dropped, renamed}.
  open-list — writes the `open` list of filter's output as a JSON list, the file
              grill_budget.py split reads (Step 4).
  answers   — builds answers.json from the person's reply, saved word for word in a file
              (Step 5). An answer starts on a line that names a question's id or its number
              in the asked order ("Q-surface-1: ...", "2. ...", "- **Q-scope-1** — ..."); the
              lines after it, up to the next one, belong to it. A reply to exactly one asked
              question may be plain text. A bare "skip" or "defer" (at most with "it", "for
              now" or "later") is recorded with decision deferred. A reply that starts with
              "skip" or "defer" and says more ("Skip the dashboard, use the CLI") is not
              guessed: it is listed in `unclear`, gets no answer, and is asked again. When the
              first line of the reply that is not empty is a bare "yes", each asked question the
              reply does not answer by its id is recorded as {"id", "answer": "yes — accepted as
              proposed", "decision": "accepted"}. Prints {answers, unanswered, unclear, unknown}.
  early     — splits the asked questions of grill_budget.py's split in two. A question is
              asked before the slice is shaped (`early-split.json`) only when it blocks the
              slice, has no proposed answer, and is not about the surface or the tester (topic
              `surface` or `tester`): the run proposes the surface and the tester itself. Every
              other asked question waits for the one brief (`brief-split.json`). Both files have
              the split's shape ({asked, assumptions}); the assumptions go with the brief.
  add       — writes grill_budget.py's split: each asked question as kind asked, each one not
              asked as kind assumption (its `assume` text, else its proposed answer, is the
              assumption). An assumption with no text is refused: a gap left open must have a
              written assumption (C4). An id already in the record is kept as it is.
  answer    — writes the person's answers ([{id, decision, answer}]) onto asked entries. An
              answer with no text is refused (exit 2, nothing written): an empty answer is not
              an answer. An answer with no decision is deferred when its text is a bare
              "skip" or "defer", else in scope.
  brief     — checks the brief shown to the person before it is sent. The opening is the text
              before the first Markdown heading: two or three sentences that say what the person
              decides (it may name a question id). The brief has the H2 headings What you run,
              Who tests it, Features, Hidden file, Left out, Assumptions, Model check and
              Questions; each asked question of the split sits under ## Questions as ### <id>,
              with the parts **Question**, **Answer**, **Why it matters** and **Example**. With
              --early (the questions asked before the slice is shaped) only the opening and
              ## Questions are needed. Prints {ok, problems}; each problem names the heading or
              part that is missing. This is a floor a script can test; the person's read of the
              brief is the full test. Exit 1 on problems.
  check     — every asked and assumption id of the split is in the record, and every asked
              question has an answer that is not empty; a blocking question that is deferred
              has no answer yet. Exit 1 when any of this fails.

Exit 0 done, 1 a check failed (proposals: a question's shape; brief: its shape; check: a
missing entry or an asked question with no answer),
2 usage error or refusal. Files on disk only.
"""

import argparse
import json
import os
import re
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("record_questions.py: PyYAML is required (pip install pyyaml).\n")
    sys.exit(2)

BLOCK = re.compile(r"```yaml\n(.*?)```", re.S)
BASIS_KINDS = ("model", "memory", "person")


class Refused(Exception):
    pass


def load_json(path, what):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        raise Refused(f"cannot read {what} {path}: {exc}")


def read_record(path):
    if not os.path.isfile(path):
        return None, []
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    m = BLOCK.search(text)
    if not m:
        raise Refused(f"{path} has no ```yaml block of questions")
    data = yaml.safe_load(m.group(1)) or {}
    return text, list(data.get("questions") or [])


def write_record(path, text, entries, issue=None):
    block = "```yaml\n" + yaml.safe_dump({"questions": entries}, sort_keys=False,
                                         allow_unicode=True) + "```"
    if text is None:
        text = (f"# Questions — #{issue}\n\nEvery question /shape-slice asked a person, and every "
                "gap it left as an assumption, with the answer. This file only grows "
                "(standards/rules/user-questions.md).\n\n" + block + "\n")
    else:
        text = BLOCK.sub(lambda _m: block, text, count=1)
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def has_answer(entry):
    return isinstance(entry.get("user_answer"), str) and entry["user_answer"].strip() != ""


def answered(entry):
    """An answer is a fact: the person typed text, and did not defer the question."""
    return has_answer(entry) and entry.get("user_decision") != "deferred"


def normalize(text):
    return " ".join(re.sub(r"[^\w\s]", " ", str(text or "").lower()).split())


def check_questions(qs):
    if not isinstance(qs, list):
        raise Refused("the questions file must hold a JSON list")
    for i, q in enumerate(qs):
        if not isinstance(q, dict) or not q.get("id") or not isinstance(q.get("blocking"), bool):
            raise Refused(f"question {i} needs an \"id\" and a true/false \"blocking\"")
    return qs


def backed(basis):
    return (isinstance(basis, dict) and basis.get("kind") in BASIS_KINDS
            and str(basis.get("ref") or "").strip() != "")


# Words that point outside the question: it does not stand alone.
POINTERS = re.compile(r"\b(above|below|as before|as said|the previous|the last one|the same as|"
                      r"this one|that one|these ones|those ones)\b", re.I)
DEFER = re.compile(r"^\s*(defer|skip)(\s+(it|this|this one|for now|later|for later))?"
                   r"\s*[.!]*\s*$", re.I)
DEFER_START = re.compile(r"^\s*(defer|skip)\b", re.I)
YES = re.compile(r"^\s*\**yes\**\s*[.!]*\s*$", re.I)
ACCEPTED = "yes \u2014 accepted as proposed"


def is_deferral(text):
    """True only for a bare "skip" or "defer" (with at most "it", "for now" or "later")."""
    return bool(DEFER.match(str(text or "")))


def shape_problems(q):
    """The shape floor a script can test; the reviewer at the checkpoint judges the rest."""
    text = str(q.get("question") or "").strip()
    out = []
    if not text:
        out.append("no question text")
    elif text.count("?") != 1 or " and " in f" {text.lower()} ":
        out.append("asks more than one thing")
    elif POINTERS.search(text) or len(text.split()) < 5:
        out.append("does not stand alone (it points to other text, or is too short to read alone)")
    if not str(q.get("why") or "").strip():
        out.append("no 'why it matters'")
    ex = q.get("examples")
    if not isinstance(ex, list) or len([e for e in ex if str(e).strip()]) < 2:
        out.append("fewer than two examples")
    return out


def cmd_proposals(args):
    all_qs = check_questions(load_json(args.questions, "questions"))
    settled = [q for q in all_qs if q.get("settled") is True and backed(q.get("basis"))]
    qs = [q for q in all_qs if q not in settled]
    stripped = []
    for q in qs:
        if q.get("proposed_answer") not in (None, "") and not backed(q.get("basis")):
            q["proposed_answer"] = None
            q["basis"] = None
            stripped.append(q["id"])
    none = sum(1 for q in qs if q.get("proposed_answer") in (None, ""))
    problems = {q["id"]: shape_problems(q) for q in qs if shape_problems(q)}
    out = {"questions": qs, "settled": settled, "no_proposed_answer": none, "stripped": stripped,
           "shape_problems": problems}
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps({"settled": [q["id"] for q in settled], "no_proposed_answer": none,
                      "stripped": stripped, "shape_problems": problems}, indent=2))
    return 1 if problems else 0


def questions_of(data):
    """The questions of a file: a JSON list, or the object `proposals` writes."""
    if isinstance(data, dict) and isinstance(data.get("questions"), list):
        return data["questions"]
    return data


def cmd_filter(args):
    qs = check_questions(questions_of(load_json(args.questions, "questions")))
    _text, entries = read_record(args.record)
    done = {}
    for e in entries:
        if answered(e) and normalize(e.get("question")):
            done.setdefault(normalize(e.get("question")), e)
    by_id = {e.get("id"): e for e in entries}
    taken = set(by_id) | {q["id"] for q in qs}
    open_qs, facts, renamed = [], [], {}
    for q in qs:
        hit = done.get(normalize(q.get("question")))
        if hit is not None:
            facts.append({"id": hit.get("id"), "asked_as": q["id"],
                          "user_decision": hit.get("user_decision"),
                          "user_answer": hit.get("user_answer")})
            continue
        old = by_id.get(q["id"])
        if old is not None and normalize(old.get("question")) != normalize(q.get("question")):
            n = 2
            while f"{q['id']}-{n}" in taken:
                n += 1
            new_id = f"{q['id']}-{n}"
            taken.add(new_id)
            renamed[q["id"]] = new_id
            q = dict(q, id=new_id)
        open_qs.append(q)
    out = {"open": open_qs, "answered": facts, "dropped": len(qs) - len(open_qs),
           "renamed": renamed}
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps({"open": len(open_qs), "dropped": out["dropped"], "renamed": renamed},
                     indent=2))
    return 0


def cmd_open_list(args):
    data = load_json(args.open, "filter output")
    if not isinstance(data, dict) or not isinstance(data.get("open"), list):
        raise Refused(f"{args.open} has no `open` list (run filter first)")
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(data["open"], fh, indent=2)
    print(json.dumps({"open": [q.get("id") for q in data["open"]]}, indent=2))
    return 0


SELF_PROPOSED = ("surface", "tester")


def is_early(q):
    """Asked before the slice is shaped: blocking, no proposed answer, not the surface or tester."""
    topic = str(q.get("topic") or "").strip().lower()
    return (q.get("blocking") is True and q.get("proposed_answer") in (None, "")
            and topic not in SELF_PROPOSED)


def cmd_early(args):
    split = load_json(args.split, "split")
    if not isinstance(split, dict):
        raise Refused(f"{args.split} must hold the split object {{asked, assumptions}}")
    asked = list(split.get("asked") or [])
    early = [q for q in asked if is_early(q)]
    rest = [q for q in asked if not is_early(q)]
    for path, data in ((args.early_out, {"asked": early, "assumptions": []}),
                       (args.rest_out, {"asked": rest,
                                        "assumptions": list(split.get("assumptions") or [])})):
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
    print(json.dumps({"early": [q.get("id") for q in early], "brief": [q.get("id") for q in rest]},
                     indent=2))
    return 0


ANSWER_START = re.compile(r"^\s*(?:[-*]\s*)?(?:\*\*)?(?P<key>Q-[\w-]*\w|\d+)(?:\*\*)?"
                          r"\s*(?:[:.)]|\u2014|--?)\s*(?P<text>.*)$")


def cmd_answers(args):
    split = load_json(args.split, "split")
    asked = [q["id"] for q in split.get("asked") or []]
    try:
        with open(args.reply, encoding="utf-8") as fh:
            reply = fh.read()
    except OSError as exc:
        raise Refused(f"cannot read the reply {args.reply}: {exc}")
    found, unknown, current = {}, [], None
    first = next((ln for ln in reply.splitlines() if ln.strip()), "")
    yes = bool(YES.match(first))
    for line in reply.splitlines():
        m = ANSWER_START.match(line)
        key = m.group("key") if m else None
        qid = None
        if key is not None:
            if key.isdigit():
                qid = asked[int(key) - 1] if 1 <= int(key) <= len(asked) else None
            else:
                qid = key
        if qid is not None or (key is not None and not key.isdigit()):
            if qid not in asked:
                unknown.append(key)
                current = None
                continue
            current = qid
            found[current] = [m.group("text")]
        elif current is not None:
            found[current].append(line)
    if not found and len(asked) == 1 and reply.strip() and not yes:
        found[asked[0]] = [reply]
    answers, unclear = [], []
    for qid in asked:
        text = "\n".join(found.get(qid, [])).strip()
        if not text:
            if yes:
                answers.append({"id": qid, "answer": ACCEPTED, "decision": "accepted"})
            continue
        if DEFER_START.match(text) and not is_deferral(text):
            unclear.append(qid)  # "Skip the dashboard, use the CLI": ask again, never guess
            continue
        a = {"id": qid, "answer": text}
        if is_deferral(text):
            a["decision"] = "deferred"
        answers.append(a)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(answers, fh, indent=2)
    got = {a["id"] for a in answers}
    print(json.dumps({"answers": [a["id"] for a in answers],
                      "unanswered": [q for q in asked if q not in got and q not in unclear],
                      "unclear": unclear, "unknown": unknown},
                     indent=2))
    return 0


def entry_for(q, kind, at, run):
    assume = q.get("assume") or q.get("proposed_answer")
    if kind == "assumption" and not str(assume or "").strip():
        raise Refused(f"gap '{q['id']}' is not asked but has no written assumption")
    return {"id": q["id"], "kind": kind, "blocking": q["blocking"], "asked_at": at,
            "topic": q.get("topic"), "question": q.get("question"),
            "proposed_answer": q.get("proposed_answer"), "basis": q.get("basis"),
            "pipeline_source": f"/shape-slice {run}",
            "pipeline_guess": assume if kind == "assumption" else q.get("proposed_answer"),
            "impact_if_unknown": q.get("why"),
            "user_decision": None, "user_answer": None, "resolved_at": None, "resolved_by_run": None}


def cmd_add(args):
    split = load_json(args.split, "split")
    text, entries = read_record(args.record)
    have = {e.get("id") for e in entries}
    new = []
    for kind, key in (("asked", "asked"), ("assumption", "assumptions")):
        for q in split.get(key) or []:
            if q["id"] not in have:
                new.append(entry_for(q, kind, args.at, args.run))
    write_record(args.record, text, entries + new, args.issue)
    print(json.dumps({"added": [e["id"] for e in new], "kept": len(entries)}, indent=2))
    return 0


def cmd_answer(args):
    answers = load_json(args.answers, "answers")
    text, entries = read_record(args.record)
    if text is None:
        raise Refused(f"no record at {args.record}")
    by_id = {e.get("id"): e for e in entries}
    if not isinstance(answers, list):
        raise Refused("the answers file must hold a JSON list")
    for a in answers:
        e = by_id.get(a.get("id"))
        if e is None or e.get("kind") != "asked":
            raise Refused(f"'{a.get('id')}' is not an asked question in the record")
        if not isinstance(a.get("answer"), str) or not a["answer"].strip():
            raise Refused(f"the answer to '{a.get('id')}' has no text; an empty answer is not "
                          "an answer — ask the question again")
    for a in answers:
        e = by_id[a["id"]]
        e["user_decision"] = a.get("decision") or (
            "deferred" if is_deferral(a.get("answer")) else "in_scope")
        e["user_answer"] = a.get("answer")
        e["resolved_at"] = args.at
        e["resolved_by_run"] = args.run
    write_record(args.record, text, entries)
    print(json.dumps({"answered": [a["id"] for a in answers]}, indent=2))
    return 0


QUESTION_PARTS = ("Question", "Answer", "Why it matters", "Example")
BRIEF_HEADINGS = ("What you run", "Who tests it", "Features", "Hidden file", "Left out",
                  "Assumptions", "Model check", "Questions")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")


def brief_problems(text, asked, early=False):
    """The brief the person reads, checked against the floor of the rule for asking a person."""
    problems = []
    lines = text.splitlines()
    first = next((i for i, ln in enumerate(lines) if HEADING.match(ln)), len(lines))
    opening = " ".join(ln.strip() for ln in lines[:first] if ln.strip())
    sentences = [x for x in re.split(r"(?<=[.!?])\s+", opening) if x.strip()]
    if not opening:
        problems.append("no opening before the first heading")
    elif not 2 <= len(sentences) <= 3:
        problems.append(f"the opening has {len(sentences)} sentences, not two or three")
    if opening and not re.search(r"\bdecid", opening, re.I):
        problems.append("the opening does not say what the person decides")
    h2 = {}
    for i, ln in enumerate(lines):
        m = HEADING.match(ln)
        if m and len(m.group(1)) == 2:
            h2.setdefault(m.group(2), i)
    for name in (("Questions",) if early else BRIEF_HEADINGS):
        if name not in h2:
            problems.append(f"no '## {name}' heading")
    if "Questions" not in h2:
        for q in asked:
            problems.append(f"'{q}' is not under '## Questions'")
        return problems
    start = h2["Questions"] + 1
    end = next((i for i in range(start, len(lines)) if (m := HEADING.match(lines[i]))
                and len(m.group(1)) <= 2), len(lines))
    blocks, current = {}, None
    for ln in lines[start:end]:
        m = HEADING.match(ln)
        if m and len(m.group(1)) == 3:
            current = m.group(2).strip()
            blocks.setdefault(current, [])
        elif current is not None:
            blocks[current].append(ln)
    for q in asked:
        if q not in blocks:
            problems.append(f"'{q}' has no '### {q}' heading under '## Questions'")
            continue
        part = "\n".join(blocks[q])
        for name in QUESTION_PARTS:
            if not re.search(r"\*\*" + re.escape(name) + r"\b", part):
                problems.append(f"'### {q}' has no **{name}** part")
    return problems


def cmd_brief(args):
    split = load_json(args.split, "split")
    asked = [q["id"] for q in split.get("asked") or []]
    try:
        with open(args.brief, encoding="utf-8") as fh:
            text = fh.read()
    except OSError as exc:
        raise Refused(f"cannot read the brief {args.brief}: {exc}")
    problems = brief_problems(text, asked, early=args.early)
    print(json.dumps({"ok": not problems, "problems": problems}, indent=2))
    return 1 if problems else 0


def cmd_check(args):
    split = load_json(args.split, "split")
    _text, entries = read_record(args.record)
    have = {e.get("id"): e for e in entries}
    missing = [q["id"] for key in ("asked", "assumptions") for q in split.get(key) or []
               if q["id"] not in have]
    open_asked = [q["id"] for q in split.get("asked") or []
                  if q["id"] in have and not has_answer(have[q["id"]])]
    blocking_deferred = [q["id"] for q in split.get("asked") or []
                         if q["id"] in have and has_answer(have[q["id"]])
                         and have[q["id"]].get("blocking") is True
                         and have[q["id"]].get("user_decision") == "deferred"]
    ok = not missing and not open_asked and not blocking_deferred
    print(json.dumps({"ok": ok, "missing": missing, "unanswered": open_asked,
                      "blocking_deferred": blocking_deferred}, indent=2))
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="The /shape-slice question record.")
    sub = ap.add_subparsers(dest="command", required=True)
    p = sub.add_parser("proposals")
    p.add_argument("--questions", required=True)
    p.add_argument("--out", required=True)
    f = sub.add_parser("filter")
    f.add_argument("--record", required=True)
    f.add_argument("--questions", required=True)
    f.add_argument("--out", required=True)
    a = sub.add_parser("add")
    a.add_argument("--record", required=True)
    a.add_argument("--issue", required=True)
    a.add_argument("--split", required=True)
    a.add_argument("--at", required=True)
    a.add_argument("--run", required=True)
    o = sub.add_parser("open-list")
    o.add_argument("--open", required=True)
    o.add_argument("--out", required=True)
    w = sub.add_parser("answers")
    w.add_argument("--reply", required=True)
    w.add_argument("--split", required=True)
    w.add_argument("--out", required=True)
    r = sub.add_parser("answer")
    r.add_argument("--record", required=True)
    r.add_argument("--answers", required=True)
    r.add_argument("--at", required=True)
    r.add_argument("--run", required=True)
    c = sub.add_parser("check")
    c.add_argument("--record", required=True)
    c.add_argument("--split", required=True)
    b = sub.add_parser("brief")
    b.add_argument("--brief", required=True)
    b.add_argument("--split", required=True)
    b.add_argument("--early", action="store_true",
                   help="the questions asked before the slice is shaped: opening and Questions only")
    e = sub.add_parser("early")
    e.add_argument("--split", required=True)
    e.add_argument("--early-out", required=True)
    e.add_argument("--rest-out", required=True)
    args = ap.parse_args(argv)
    try:
        return {"proposals": cmd_proposals, "filter": cmd_filter, "open-list": cmd_open_list,
                "answers": cmd_answers, "add": cmd_add, "answer": cmd_answer,
                "brief": cmd_brief, "early": cmd_early, "check": cmd_check}[args.command](args)
    except Refused as exc:
        sys.stderr.write(f"record_questions.py: {exc}\n")
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
