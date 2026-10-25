#!/usr/bin/env python3
"""
grounding_gate.py — the deterministic gate over a grounding-eval judge verdict.

The judge (an LLM, in any of the configured modes) only SCORES and evidences; it does
NOT decide pass/fail. This gate decides — so a judge cannot wave a doc through with a
self-declared overall. A verdict missing a criterion fails CLOSED (a judge that drops a
criterion is not trusted).

See standards/rules/grounding-eval.md for the gate rule, and the judge-grounding skill for
the rubric, the prompt and the verdict shape.

Usage:
    python3 grounding_gate.py --verdict verdict.json
    cat verdict.json | python3 grounding_gate.py
        All-pass, no state: the doc passes iff every one of the five criteria is `pass`
        or `na`. Prints {ok, overall, doc, failures[], missing[]}.

    python3 grounding_gate.py --verdict V --state DIR --doc D --guidance G [--parent P] [--judge J]
        The gate with the judge state. First round (no record for the doc): all-pass, as
        above. Fix round (a record exists): each last failure counts as fixed only when
        its `prior` entry says fixed: true, the doc's text changed since the failing
        verdict, and every quoted fragment of the entry's evidence is found in the doc's
        text now. The gate decides this, not the judge. A criterion that fails only on text
        that did not change since the last verdict (every quoted fragment of its evidence is
        found in the snapshot) is a note, not a failure. Then writes the record. Prints
        {ok, overall, doc, round, failures[], notes[], missing[], fingerprint}.

    python3 grounding_gate.py kept --state DIR --doc D --guidance G [--parent P] [--judge J]
        Prints {kept, fingerprint, reason, notes[]}. Exit 0 when the last verdict passed and
        the doc, its parent, the guidance and the judge skill file have not changed since
        (the play then does not judge this doc again); exit 1 otherwise. `notes` are the
        notes the record holds.

    python3 grounding_gate.py prior --state DIR --doc D
        Prints {round: first|fix, prior_failures[]}, exit 0. The play hands
        prior_failures to the judge in a fix round.

    python3 grounding_gate.py notes --state DIR --out FILE
        Writes {notes: [{doc, id, evidence, fix}]} to FILE: every note held in the state's
        records, passed and kept docs included, for the play to show at its checkpoint.
        Prints the same object, exit 0. A missing state folder gives no notes.

A human summary goes to stderr. Exit 0 when the doc passes, 1 on any fail/missing, 2 on a
usage/parse error.
"""

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile

REQUIRED_CRITERIA = [
    "completeness",
    "self_explanation",
    "discreteness_form",
    "depth_gradient",
    "stranger_test",
]
PASS_VERDICTS = {"pass", "na"}

QUOTE_RE = re.compile(r'"([^"]*)"')
ELLIPSIS_RE = re.compile(r"\.\.\.|…")
SPACE_RE = re.compile(r"\s+")
RECORD_RE = re.compile(r"[0-9a-f]{32}\.json")


class UsageError(Exception):
    """A usage or read error: the gate exits 2."""


# ---------------------------------------------------------------- the judge state


def read_bytes(path, what):
    try:
        with open(path, "rb") as fh:
            return fh.read()
    except OSError as exc:
        raise UsageError(f"cannot read {what} {path}: {exc}")


def fingerprint(doc, guidance, parent=None, judge=None):
    """sha256 of the doc, the parent (empty when none), the guidance and the judge skill
    file (empty when none), in that order. Each part is prefixed by its length, so a byte
    cannot move from one part to another. A stricter judge file ends an old pass."""
    h = hashlib.sha256()
    for part in (
        read_bytes(doc, "doc"),
        read_bytes(parent, "parent") if parent else b"",
        read_bytes(guidance, "guidance"),
        read_bytes(judge, "judge") if judge else b"",
    ):
        h.update(len(part).to_bytes(8, "big"))
        h.update(part)
    return h.hexdigest()


def doc_key(doc):
    return os.path.normpath(doc)


def record_path(state, doc):
    name = hashlib.sha256(doc_key(doc).encode("utf-8")).hexdigest()[:32]
    return os.path.join(state, name + ".json")


def load_record(state, doc):
    """The record for the doc, or None when there is none. A record that cannot be read is
    treated as none: the doc then gets a first round, the strictest one."""
    path = record_path(state, doc)
    if not os.path.isfile(path):
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            rec = json.load(fh)
    except (OSError, ValueError) as exc:
        sys.stderr.write(f"grounding_gate.py: record {path} unreadable ({exc}); treated as none\n")
        return None
    return rec if isinstance(rec, dict) else None


def write_json(path, data):
    """Write through a temp file and a rename, so a reader never sees half a file."""
    folder = os.path.dirname(os.path.abspath(path))
    os.makedirs(folder, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=folder, prefix=".tmp-", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def write_record(state, doc, rec):
    write_json(record_path(state, doc), rec)


def item(i, evidence, fix):
    return {"id": i, "evidence": evidence or "", "fix": fix or ""}


# ---------------------------------------------------------------- notes


def collapse(text):
    return SPACE_RE.sub(" ", text).strip()


def quotes_found(evidence, text):
    """True when the evidence quotes at least one fragment and every fragment is found in
    the text. A fragment is split on '...' and '…'; each part must be found. Runs of
    whitespace count as one space."""
    parts = []
    for fragment in QUOTE_RE.findall(evidence or ""):
        parts += [collapse(p) for p in ELLIPSIS_RE.split(fragment)]
    parts = [p for p in parts if p]
    if not parts:
        return False
    whole = collapse(text)
    return all(p in whole for p in parts)


def on_unchanged_text(evidence, snapshot):
    """A new point rests on text that did not change: every quote is in the snapshot."""
    return quotes_found(evidence, snapshot)


def why_not_fixed(entry, snapshot, now):
    """None when the gate counts a prior failure as fixed, else the reason in plain words.
    All three must hold: the judge says fixed, the doc changed since the failing verdict,
    and every quote of the entry's evidence is on the page now."""
    if entry.get("fixed") is not True:
        return ""
    if collapse(snapshot) == collapse(now):
        return "marked fixed, but the doc did not change since the verdict that failed"
    if not quotes_found(entry.get("evidence"), now):
        return "marked fixed, but its evidence quotes no text found on the page now"
    return None


# ---------------------------------------------------------------- the gate


def read_verdict(path):
    try:
        raw = open(path, encoding="utf-8").read() if path else sys.stdin.read()
        verdict = json.loads(raw)
    except (OSError, ValueError) as exc:
        raise UsageError(f"cannot read/parse verdict: {exc}")
    if not isinstance(verdict, dict):
        raise UsageError("cannot read/parse verdict: not a JSON object")
    return verdict


def criteria_by_id(verdict):
    return {c.get("id"): c for c in (verdict.get("criteria") or []) if isinstance(c, dict)}


def gate_plain(verdict):
    """All-pass, no state: the old use, unchanged."""
    doc = verdict.get("doc", "<unknown>")
    by_id = criteria_by_id(verdict)

    missing = [cid for cid in REQUIRED_CRITERIA if cid not in by_id]
    failures = []
    for cid in REQUIRED_CRITERIA:
        c = by_id.get(cid)
        if c is None:
            continue  # reported as missing
        if c.get("verdict") not in PASS_VERDICTS:
            failures.append({
                "id": cid,
                "verdict": c.get("verdict"),
                "evidence": c.get("evidence", ""),
                "fix": c.get("fix", ""),
            })

    ok = not missing and not failures
    return {
        "ok": ok,
        "overall": "pass" if ok else "fail",
        "doc": doc,
        "failures": failures,
        "missing": missing,
    }


def gate_with_state(verdict, args):
    fp = fingerprint(args.doc, args.guidance, args.parent, args.judge)
    snapshot_now = read_bytes(args.doc, "doc").decode("utf-8", errors="replace")
    rec = load_record(args.state, args.doc)
    by_id = criteria_by_id(verdict)
    missing = [cid for cid in REQUIRED_CRITERIA if cid not in by_id]
    failures, notes = [], []

    if rec is None:
        rnd = "first"
        for cid in REQUIRED_CRITERIA:
            c = by_id.get(cid)
            if c is not None and c.get("verdict") not in PASS_VERDICTS:
                failures.append(item(cid, c.get("evidence"), c.get("fix")))
    else:
        rnd = "fix"
        snapshot = rec.get("snapshot") or ""
        # Each last failure must be answered by one prior entry, and the gate checks the
        # fix: the judge says fixed, the page changed, and the quote is on the page now.
        entries = [e for e in (verdict.get("prior") or []) if isinstance(e, dict)]
        used = set()
        for last in [f for f in (rec.get("failures") or []) if isinstance(f, dict)]:
            lid = last.get("id")
            idx = next((k for k, e in enumerate(entries) if k not in used and e.get("id") == lid), None)
            if idx is None:
                failures.append(item(
                    lid,
                    "no prior entry for this failure; it fails closed. Last evidence: "
                    + (last.get("evidence") or ""),
                    last.get("fix"),
                ))
                continue
            used.add(idx)
            entry = entries[idx]
            reason = why_not_fixed(entry, snapshot, snapshot_now)
            if reason is None:
                continue
            evidence = entry.get("evidence") or ""
            if reason:
                evidence = f"{reason}. Judge evidence: {evidence}"
            failures.append(item(lid, evidence, last.get("fix")))
        # A new point is a note only when it rests on text that did not change.
        for cid in REQUIRED_CRITERIA:
            c = by_id.get(cid)
            if c is None or c.get("verdict") in PASS_VERDICTS:
                continue
            point = item(cid, c.get("evidence"), c.get("fix"))
            (notes if on_unchanged_text(c.get("evidence"), snapshot) else failures).append(point)

    ok = not missing and not failures
    write_record(args.state, args.doc, {
        "doc": doc_key(args.doc),
        "fingerprint": fp,
        "passed": ok,
        "failures": failures,
        "snapshot": snapshot_now,
        "notes": notes,
    })
    return {
        "ok": ok,
        "overall": "pass" if ok else "fail",
        "doc": verdict.get("doc", args.doc),
        "round": rnd,
        "failures": failures,
        "notes": notes,
        "missing": missing,
        "fingerprint": fp,
    }


def summarize(result):
    doc = result["doc"]
    if result["ok"]:
        sys.stderr.write(f"PASS — {doc} cleared all five criteria.\n")
    else:
        sys.stderr.write(f"FAIL — {doc}\n")
        for cid in result["missing"]:
            sys.stderr.write(f"  missing criterion: {cid} (verdict failed closed)\n")
        for f in result["failures"]:
            if "verdict" in f:
                sys.stderr.write(f"  {f['id']} = {f['verdict']}\n")
            else:
                sys.stderr.write(f"  {f['id']} = fail\n")
            if f["evidence"]:
                sys.stderr.write(f"    evidence: {f['evidence']}\n")
            if f["fix"]:
                sys.stderr.write(f"    fix:      {f['fix']}\n")
    for n in result.get("notes") or []:
        sys.stderr.write(f"  note (text did not change, does not block): {n['id']}\n")
        if n["evidence"]:
            sys.stderr.write(f"    evidence: {n['evidence']}\n")


def run_gate(argv):
    ap = argparse.ArgumentParser(description="Gate a grounding-eval judge verdict.")
    ap.add_argument("--verdict", help="verdict JSON file (default: stdin)")
    ap.add_argument("--state", help="judge state folder (turns on the kept pass and the fix round)")
    ap.add_argument("--doc", help="the judged doc (with --state)")
    ap.add_argument("--guidance", help="the guidance the judge was given (with --state)")
    ap.add_argument("--parent", help="the parent doc the judge was given, if any (with --state)")
    ap.add_argument("--judge", help="the judge skill file, whose text joins the fingerprint (with --state)")
    args = ap.parse_args(argv)

    if args.state is None and (args.doc or args.guidance or args.parent or args.judge):
        raise UsageError("--doc, --guidance, --parent and --judge need --state")
    if args.state is not None and not (args.doc and args.guidance):
        raise UsageError("--state needs --doc and --guidance")

    verdict = read_verdict(args.verdict)
    result = gate_plain(verdict) if args.state is None else gate_with_state(verdict, args)
    print(json.dumps(result, indent=2))
    summarize(result)
    return 0 if result["ok"] else 1


# ---------------------------------------------------------------- kept, prior and notes


def run_kept(argv):
    ap = argparse.ArgumentParser(prog="grounding_gate.py kept",
                                 description="Is the last pass of this doc still good?")
    ap.add_argument("--state", required=True)
    ap.add_argument("--doc", required=True)
    ap.add_argument("--guidance", required=True)
    ap.add_argument("--parent")
    ap.add_argument("--judge")
    args = ap.parse_args(argv)

    fp = fingerprint(args.doc, args.guidance, args.parent, args.judge)
    rec = load_record(args.state, args.doc)
    if rec is None:
        kept, reason = False, "the doc has not been judged yet"
    elif rec.get("passed") is not True:
        kept, reason = False, "the last verdict did not pass"
    elif rec.get("fingerprint") != fp:
        kept, reason = False, ("the doc, its parent, the guidance or the judge changed "
                               "since the last pass")
    else:
        kept, reason = True, "the last verdict passed and nothing it judged has changed"
    notes = [item(n.get("id"), n.get("evidence"), n.get("fix"))
             for n in ((rec or {}).get("notes") or []) if isinstance(n, dict)]
    print(json.dumps({"kept": kept, "fingerprint": fp, "reason": reason, "notes": notes},
                     indent=2))
    sys.stderr.write(("KEPT — " if kept else "NOT KEPT — ") + f"{args.doc}: {reason}\n")
    return 0 if kept else 1


def run_prior(argv):
    ap = argparse.ArgumentParser(prog="grounding_gate.py prior",
                                 description="Which round is next, and what failed last time?")
    ap.add_argument("--state", required=True)
    ap.add_argument("--doc", required=True)
    args = ap.parse_args(argv)

    rec = load_record(args.state, args.doc)
    if rec is None:
        out = {"round": "first", "prior_failures": []}
    else:
        out = {
            "round": "fix",
            "prior_failures": [
                item(f.get("id"), f.get("evidence"), f.get("fix"))
                for f in (rec.get("failures") or []) if isinstance(f, dict)
            ],
        }
    print(json.dumps(out, indent=2))
    return 0


def run_notes(argv):
    ap = argparse.ArgumentParser(prog="grounding_gate.py notes",
                                 description="Collect every note the judge state holds.")
    ap.add_argument("--state", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)

    records = []
    if os.path.isdir(args.state):
        for name in sorted(os.listdir(args.state)):
            if not RECORD_RE.fullmatch(name):
                continue  # not a record (a temp file, or a notes file kept here)
            path = os.path.join(args.state, name)
            try:
                with open(path, encoding="utf-8") as fh:
                    rec = json.load(fh)
            except (OSError, ValueError) as exc:
                sys.stderr.write(f"grounding_gate.py: record {path} unreadable ({exc}); skipped\n")
                continue
            if isinstance(rec, dict):
                records.append(rec)
    notes = []
    for rec in sorted(records, key=lambda r: str(r.get("doc", ""))):
        for n in rec.get("notes") or []:
            if isinstance(n, dict):
                notes.append({"doc": rec.get("doc", ""), **item(n.get("id"), n.get("evidence"),
                                                               n.get("fix"))})
    out = {"notes": notes}
    write_json(args.out, out)
    print(json.dumps(out, indent=2))
    sys.stderr.write(f"NOTES — {len(notes)} note(s) written to {args.out}\n")
    return 0


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    try:
        if argv and argv[0] == "kept":
            return run_kept(argv[1:])
        if argv and argv[0] == "prior":
            return run_prior(argv[1:])
        if argv and argv[0] == "notes":
            return run_notes(argv[1:])
        return run_gate(argv)
    except UsageError as exc:
        sys.stderr.write(f"grounding_gate.py: {exc}\n")
        return 2
    except SystemExit as exc:  # argparse usage error
        return 2 if exc.code else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
