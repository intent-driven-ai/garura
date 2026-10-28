#!/usr/bin/env python3
"""
render_brief.py — the one slice-confirmation brief of /shape-slice (C3, C16, C17, C18).

The person gets one brief, not a list of questions. This script builds it from the run's
records, so no part can be left out; the agent writes only the opening (and the question
text, which is already in the split).

    python3 render_brief.py --working <dir> --root <model> --spine <spine> \
        --opening <opening.md> --out <brief.md>
    python3 render_brief.py --early --working <dir> --opening <opening.md> \
        --split <early-split.json> --out <early-brief.md>

It reads from <dir>: slice.json, fills.json, persist-fills.json, persist-slice.json,
slice-check.json, hidden-file.json, split.json, questions-checked.json and gather.json; and,
when it is there, early-split.json (the questions already asked before the slice was shaped,
which the brief does not ask again).

brief.md is the opening, then these H2 sections:
  What you run   — the surface's name and what the tester does on it
  Who tests it   — the surface's persona_ref
  Features       — one block per capability, in build order:
                       ### <capability name> (<cap id>) — <new|filled|reused>
                       Domain: [<domain name>](<link to the domain's page>)
                       <n>. <feature name> (<feature id>) — <new|filled|reused>
                   (n is the place in build order; a part is new when persist-fills.json
                   `written` names it, filled when `updated` names it, else reused); then,
                   when persist-fills.json `one_lines` names any, ### One-lines replaced with
                   each part's id and its old and new spine one-line
  Hidden file    — Place, Fails if lines, The builder can fix alone, A person must decide;
                   and, from hidden-write.json when it is there, each feature with lines too
                   vague to judge; then the line that says how to change a kept line
                   (/shape-slice #<intent> --edit: <your words>)
  Left out       — each slice.json left_out[].what (with its why), or "Nothing is left out."
  Assumptions    — each split.json assumptions[].assume
  Thin ICE       — only when a part is thin: each thin part's id, and /discover-capabilities
  Kept slice     — only when persist-slice.json reads reused: true: each difference word for
                   word; each pulled-in or pushed-out feature; each field a record upgrade set
                   or dropped, in plain words with the field's own word; when the kept slice
                   takes new text (persist-slice.json `replaced`), that its record keeps a
                   history line, and each epic in `out_of_date`, named as out of date
  Model check    — Older problems: <n>, then each older problem and warning, word for word
  Questions      — Questions with no proposed answer: <n>, then each asked question as
                   ### <id> with **Question**, **Answer**, **Why it matters**, **Example**;
                   a question the person already answered (the question record beside <dir>,
                   ../grounding-questions.md) shows their answer as "yours: ..." and is not
                   counted as having no proposed answer;
                   when gather.json has rule_missing, a line that says the rule for asking a
                   person is missing from its shared place and that an install lays it
  Your reply     — yes, change: <what>, or stop; answer a question by its id

--early writes the short brief of Step 5 (the questions asked before the slice is shaped): the
opening, then ## Questions with each question of the split as ### <id> and its **Question**,
**Answer** ("no proposed answer yet" when it has none), **Why it matters** and **Example**;
when gather.json in <dir> has rule_missing, the line that says so; then ## Your reply. In
early mode --root and --spine are not needed. The result passes `record_questions.py brief
--early`.

The brief is written through safe_write.atomic_write.

Prints {"ok": true, "out": <path>}. Exit 0 written, 2 a record is missing or unreadable.
Files on disk only; no git, no network.
"""

import argparse
import json
import os
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("render_brief.py: PyYAML is required (pip install pyyaml).\n")
    sys.exit(2)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from safe_write import atomic_write  # noqa: E402
from record_questions import ACCEPTED, Refused as BadRecord, has_answer, read_record  # noqa: E402

RECORDS = ("slice.json", "fills.json", "persist-fills.json", "persist-slice.json",
           "slice-check.json", "hidden-file.json", "split.json", "questions-checked.json",
           "gather.json")
THIN_WARNING = ("A thin ICE is enough to start, but it can give weak stories and weak checks "
                "later. `/discover-capabilities` can deepen it. Nothing stops, and you do not "
                "need to run it now.")


class Missing(Exception):
    pass


def load(working, name, optional=False):
    path = os.path.join(working, name)
    if not os.path.isfile(path):
        if optional:
            return None
        raise Missing(f"the record {name} is not in {working}")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _entry(spine, key, eid):
    return next((e for e in spine.get(key) or [] if isinstance(e, dict) and e.get("id") == eid), None)


def page_name(root, part, prefix):
    if part is None:
        return None
    path = os.path.join(root, part.get("doc") or "")
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as fh:
            for ln in fh:
                if ln.startswith("# " + prefix):
                    return ln[len("# " + prefix):].strip()
    return part.get("slug") or part.get("id")


def mark(pid, written, updated):
    if pid in written:
        return "new"
    if pid in updated:
        return "filled"
    return "reused"


def surface_of(sl):
    s = sl.get("surface")
    if isinstance(s, list):
        s = s[0] if s else {}
    return s if isinstance(s, dict) else {}


def features_section(root, spine, sl, pf, out_dir):
    written = {i for ids in (pf.get("written") or {}).values() for i in ids}
    updated = set(pf.get("updated") or [])
    groups, order = {}, []
    for n, fid in enumerate(sl.get("feature_refs") or [], 1):
        f = _entry(spine, "features", fid) or {"id": fid}
        cap_id = f.get("capability") or None
        if cap_id not in groups:
            groups[cap_id] = []
            order.append(cap_id)
        groups[cap_id].append((n, f))
    out = []
    for cap_id in order:
        cap = _entry(spine, "capabilities", cap_id) if cap_id else None
        if cap is None:
            out.append("### No capability yet — the features wait in the holding folder")
        else:
            out.append(f"### {page_name(root, cap, 'Capability:')} ({cap_id}) — "
                       f"{mark(cap_id, written, updated)}")
            dom = _entry(spine, "domains", cap.get("domain")) if cap.get("domain") else None
            if dom is None:
                out.append("Domain: none yet — the capability waits in the holding folder")
            else:
                link = os.path.relpath(os.path.join(root, dom.get("doc") or ""), out_dir)
                out.append(f"Domain: [{page_name(root, dom, 'Theme:')}]({link.replace(os.sep, '/')})"
                           f" — {mark(dom.get('id'), written, updated)}")
        out.append("")
        for n, f in groups[cap_id]:
            out.append(f"{n}. {page_name(root, f, 'Feature:')} ({f.get('id')}) — "
                       f"{mark(f.get('id'), written, updated)}")
        out.append("")
    return out


def thin_parts(spine, sl, fills, hidden):
    ids = list(fills.get("thin") or [])
    wanted = set(sl.get("feature_refs") or [])
    for f in sl.get("feature_refs") or []:
        e = _entry(spine, "features", f)
        if e and e.get("capability"):
            wanted.add(e["capability"])
    for key in ("capabilities", "features", "ices"):
        for e in spine.get(key) or []:
            if isinstance(e, dict) and (e.get("metadata") or {}).get("thin"):
                pid = e.get("for") if key == "ices" else e.get("id")
                if pid in wanted:
                    ids.append(pid)
    for entry in hidden.get("entries") or []:
        for kind in entry.get("thin") or []:
            ids.append(entry["feature"] if kind == "feature" else entry.get("capability"))
    return [i for i in dict.fromkeys(ids) if i]


def kept_section(root, ps):
    out = [f"- {d}" for d in ps.get("differences") or []]
    out += [f"- This run pulls feature {f} into the kept slice, in its place in build order."
            for f in ps.get("pulled_in") or []]
    out += [f"- This run pushes feature {f} out of the kept slice." for f in ps.get("pushed_out") or []]
    rec = {}
    rec_path = os.path.join(root, ps.get("record") or "")
    if ps.get("record") and os.path.isfile(rec_path):
        with open(rec_path, encoding="utf-8") as fh:
            rec = yaml.safe_load(fh) or {}
    for field in ps.get("upgraded_to_v2") or []:
        if field.startswith("surface (moved"):
            out.append("- The kept slice's record held its surface inside the slice part; this run "
                       "moved the surface to its own part.")
            continue
        part, _, word = field.partition(".")
        value = (rec.get(part) or {}).get(word) if isinstance(rec.get(part), dict) else None
        shown = f" '{value}'" if isinstance(value, str) else (f" {value}" if value else "")
        out.append(f"- The kept slice's record had no {word}; it now has the {word}{shown}.")
    if ps.get("replaced"):
        words = {"slice.name": "name", "slice.outcome": "outcome", "surface.user_action": "tester's action"}
        parts = ", ".join(words.get(r, r) for r in ps["replaced"])
        out.append(f"- The kept slice takes the new {parts}; its record keeps a history line for it.")
        for e in ps.get("out_of_date") or []:
            out.append(f"- Out of date (named, not changed): epic {e.get('id')} ({e.get('status')}); "
                       "its stories were written from the old text.")
    for field in ps.get("dropped_fields") or []:
        out.append(f"- The kept slice's spine entry had the old field {field}; this run removed it, "
                   "because a slice entry has six fields only.")
    return out or ["- The kept slice is as it was; this run only adds the intent to it."]


def question_block(q, entry=None):
    ans = q.get("proposed_answer")
    examples = [str(e) for e in q.get("examples") or [] if str(e).strip()]
    if entry is not None and has_answer(entry) and entry["user_answer"] != ACCEPTED:
        answer = "yours: " + " ".join(str(entry["user_answer"]).split())
    elif entry is not None and has_answer(entry):
        answer = f"proposed: {ans} (you accepted it)"
    else:
        answer = 'proposed: ' + str(ans) if ans not in (None, '') else 'no proposed answer yet'
    return [f"### {q['id']}", "",
            f"**Question** {q.get('question') or ''}", "",
            f"**Answer** {answer}",
            "", f"**Why it matters** {q.get('why') or ''}", "",
            "**Example** " + " ".join(f"({chr(97 + i)}) {e}" for i, e in enumerate(examples)), ""]


def recorded(working):
    """The question record beside the working folder ({issue}/context/grounding-questions.md),
    by id: a brief shown again after a change shows each answer the person already gave."""
    path = os.path.join(os.path.dirname(os.path.normpath(working)), "grounding-questions.md")
    try:
        _text, entries = read_record(path)
    except (BadRecord, OSError, ValueError):  # unreadable: show the questions as the split has them
        return {}
    return {e.get("id"): e for e in entries if isinstance(e, dict)}


def rule_missing_lines(gather):
    missing = (gather or {}).get("rule_missing")
    if not isinstance(missing, dict):
        return []
    path = missing.get("path") or "_shared/asking-a-person.md"
    return [f"The rule for asking a person is missing: there is no {path} beside the "
            "installed skills. This brief follows the floor the play states. An install of "
            "Garura lays the rule.", ""]


def render_early(working, split, opening):
    """The short brief of Step 5: the opening, then each early question with its four parts."""
    gather = load(working, "gather.json", optional=True) or {}
    lines = [opening.strip(), "", "## Questions", ""]
    lines += rule_missing_lines(gather)
    for q in split.get("asked") or []:
        lines += question_block(q)
    lines += ["## Your reply", "",
              "Answer each question by its id (for example `Q-scope-1: ...`). The run shapes the "
              "slice after your answers and shows it to you in one brief.", ""]
    return "\n".join(lines).rstrip("\n") + "\n"


def render(working, root, spine, opening, out_dir=None):
    sl = load(working, "slice.json")
    fills = load(working, "fills.json")
    pf = load(working, "persist-fills.json")
    ps = load(working, "persist-slice.json")
    sc = load(working, "slice-check.json")
    hidden = load(working, "hidden-file.json")
    split = load(working, "split.json")
    qc = load(working, "questions-checked.json")
    gather = load(working, "gather.json")
    early = load(working, "early-split.json", optional=True) or {}
    out_dir = out_dir or working
    surface = surface_of(sl)
    lines = [opening.strip(), ""]
    lines += ["## What you run", "",
              f"- Surface: {surface.get('name') or sl.get('vertical')}",
              f"- What the tester does there: {surface.get('user_action') or 'not given'}", ""]
    lines += ["## Who tests it", "", f"- {surface.get('persona_ref') or 'not given'}", ""]
    lines += ["## Features", ""] + features_section(root, spine, sl, pf, out_dir)
    if pf.get("one_lines"):
        lines += ["### One-lines replaced", ""]
        lines += [f"- {o['id']} ({o['kind']}): was \"{o.get('was') or ''}\"; now \"{o['now']}\""
                  for o in pf["one_lines"]] + [""]
    counts = hidden.get("counts") or {}
    lines += ["## Hidden file", "",
              f"- Place: {hidden.get('path')}",
              f"- Fails if lines: {counts.get('lines', 0)}",
              f"- The builder can fix alone: {counts.get('builder_alone', 0)}",
              f"- A person must decide: {counts.get('person', 0)}"]
    for v in (load(working, "hidden-write.json", optional=True) or {}).get("vague") or []:
        lines.append(f"- Too vague to judge, so a person must decide: {v.get('count')} line(s) of "
                     f"{v.get('feature')}. A clearer \"Fails if\" line gives a clearer recovery.")
    intent = (sl.get("intents") or ["bi-<n>"])[0].replace("bi-", "")
    lines.append(f"- A line the file already kept stays as it is. To change one, run "
                 f"`/shape-slice #{intent} --edit: <what to change, in your own words>`.")
    lines.append("")
    left = sl.get("left_out") or []
    lines += ["## Left out", ""]
    lines += [f"- {x.get('what')}" + (f" — {x['why']}" if x.get("why") else "") for x in left] \
        or ["Nothing is left out."]
    lines.append("")
    assumptions = [a.get("assume") or a.get("proposed_answer") for a in split.get("assumptions") or []]
    lines += ["## Assumptions", ""]
    lines += [f"- {a}" for a in assumptions if a] or ["No assumptions."]
    lines.append("")
    thin = thin_parts(spine, sl, fills, hidden)
    if thin:
        lines += ["## Thin ICE", ""] + [f"- {t}" for t in thin] + ["", THIN_WARNING, ""]
    if ps.get("reused"):
        lines += ["## Kept slice", ""] + kept_section(root, ps) + [""]
    older = sc.get("older_problems") or []
    lines += ["## Model check", "", f"Older problems: {len(older)}", ""]
    lines += [f"- {x}" for x in older + list(sc.get("warnings") or [])]
    lines.append("")
    skip = {q.get("id") for q in early.get("asked") or []}
    asked = [q for q in split.get("asked") or [] if q.get("id") not in skip]
    record = recorded(working)
    yours = [q for q in asked if q.get("proposed_answer") in (None, "")
             and has_answer(record.get(q.get("id")) or {})]
    lines += ["## Questions", "",
              f"Questions with no proposed answer: {max(0, qc.get('no_proposed_answer', 0) - len(yours))}", ""]
    lines += rule_missing_lines(gather)
    if not asked:
        lines += ["No question is open.", ""]
    for q in asked:
        lines += question_block(q, record.get(q.get("id")))
    lines += ["## Your reply", "",
              "Type **yes**, **change: <what>**, or **stop**. Answer any question by its id in the "
              "same reply (for example `Q-scope-1: ...`). A plain yes accepts each proposed answer.",
              ""]
    return "\n".join(lines).rstrip("\n") + "\n"


PART_WORDS = {"slice.name": "the slice's name", "slice.outcome": "the slice's outcome",
              "surface.user_action": "what the tester does", "when": "when it shows",
              "way_back": "the way back", "who_fixes": "who fixes", "one_line": "the one-line"}


def hidden_names(before):
    """{feature id: (feature name, {F id: failure text})} from the copy of the hidden file."""
    from write_hidden_file import parse
    path = ((before or {}).get("copies") or {}).get("hidden")
    if not path or not os.path.isfile(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        blocks = parse(fh.read())[1]
    return {b["feature"]: (b["name"], {f["id"]: f["text"] for f in b["failures"]}) for b in blocks}


def part_words(change, names=None):
    """A change's part in plain words, with the feature's name and the failure line it is for:
    'the hidden file, feature "Pick a free slot" (ft-pick), the line "two patients get one slot"
    (F1): who fixes'."""
    part, f = str(change.get("part") or ""), change.get("file")
    bits = part.split("/")
    hidden = (names or {}).get("hidden") or {}
    if f == "record":
        return f"the slice record: {PART_WORDS.get(part, part)}"
    if f == "hidden" and len(bits) == 3:
        name, fails = hidden.get(bits[0], (None, {}))
        feature = f"feature \"{name}\" ({bits[0]})" if name else f"feature {bits[0]}"
        line = f"the line \"{fails[bits[1]]}\" ({bits[1]})" if bits[1] in fails else f"line {bits[1]}"
        return f"the hidden file, {feature}, {line}: {PART_WORDS.get(bits[2], bits[2])}"
    if f == "spine" and len(bits) == 2:
        return f"the model index, {bits[0]}: {PART_WORDS.get(bits[1], bits[1])}"
    return f"{f}: {part}"


def render_edit(working, slice_name):
    """The brief of an edit (C20): what the person asked, each change old and new, and each
    record the edit makes out of date (named, not changed). Built from the run's records."""
    lst = load(working, "edit-list.json")
    before = load(working, "edit-before.json")
    names = {"hidden": hidden_names(before)}
    with open(os.path.join(working, "edit-request.md"), encoding="utf-8") as fh:
        request = " ".join(fh.read().split())
    changes = lst.get("changes") or []
    what = "this change" if len(changes) == 1 else f"these {len(changes)} changes"
    lines = [f"You decide whether to make {what} to the slice \"{slice_name}\". "
             "Nothing else in the slice, its hidden file or the model changes. Type yes to make "
             f"{'it' if len(changes) == 1 else 'them'}, change with what to change, or stop to make none.", "",
             "## What you asked", "", f"> {request}", "", "## Changes", ""]
    for i, c in enumerate(changes, 1):
        lines += [f"{i}. {part_words(c, names)}", f"   - was: {c.get('old')}", f"   - now: {c.get('new')}"]
        if c.get("why"):
            lines.append(f"   - why: {c['why']}")
    epics = before.get("epics") or [] if before.get("in_progress") else []
    if epics:
        named = ", ".join(f"{e.get('id')} ({e.get('status')})" for e in epics)
        lines += ["", "## In progress", "",
                  f"This slice is in progress: its epic {named} is past ready. The edit changes it only "
                  "because you approve each change; the work started from it is named below as out of date."]
    lines += ["", "## Out of date (named, not changed)", ""]
    stale = [f"- {o.get('record')}: {o.get('why')}" for o in lst.get("out_of_date") or []]
    listed = " ".join(str(o.get("record")) for o in lst.get("out_of_date") or [])
    stale += [f"- epic {e.get('id')} ({e.get('status')}): work has started from this slice, so what was built "
              "from the old text may need a look." for e in epics if str(e.get("id")) not in listed]
    lines += stale or ["Nothing."]
    if lst.get("not_editable"):
        lines += ["", "## Not changed by an edit", ""]
        lines += [f"- {n.get('what')}: {n.get('why')}" for n in lst["not_editable"]]
    lines += ["", "## Your reply", "", "Type **yes**, **change: <what>**, or **stop**."]
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Render the one slice-confirmation brief.")
    ap.add_argument("--early", action="store_true",
                    help="the short brief of the questions asked before the slice is shaped")
    ap.add_argument("--edit", help="the brief of an edit (C20): the slice's name; reads edit-list.json "
                                   "and edit-request.md from --working")
    ap.add_argument("--working", required=True)
    ap.add_argument("--root", help="the model folder (not needed with --early)")
    ap.add_argument("--spine", help="the spine (not needed with --early)")
    ap.add_argument("--split", help="with --early: early-split.json")
    ap.add_argument("--opening")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    if args.edit:
        try:
            text = render_edit(args.working, args.edit)
        except (Missing, OSError, json.JSONDecodeError) as exc:
            sys.stderr.write(f"render_brief.py: not written — {exc}\n")
            return 2
        atomic_write(args.out, text)
        print(json.dumps({"ok": True, "out": args.out}, indent=2))
        return 0
    if not args.opening:
        sys.stderr.write("render_brief.py: give --opening (or --edit)\n")
        return 2
    if args.early and not args.split:
        sys.stderr.write("render_brief.py: --early needs --split <early-split.json>\n")
        return 2
    if not args.early and (not args.root or not args.spine):
        sys.stderr.write("render_brief.py: give --root and --spine (or --early)\n")
        return 2
    try:
        with open(args.opening, encoding="utf-8") as fh:
            opening = fh.read()
        if args.early:
            with open(args.split, encoding="utf-8") as fh:
                text = render_early(args.working, json.load(fh) or {}, opening)
        else:
            with open(args.spine, encoding="utf-8") as fh:
                spine = yaml.safe_load(fh) or {}
            text = render(args.working, args.root, spine, opening,
                          os.path.dirname(os.path.abspath(args.out)))
    except (Missing, OSError, json.JSONDecodeError, yaml.YAMLError) as exc:
        sys.stderr.write(f"render_brief.py: not written — {exc}\n")
        return 2
    atomic_write(args.out, text)
    print(json.dumps({"ok": True, "out": args.out}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
