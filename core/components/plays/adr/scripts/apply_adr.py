#!/usr/bin/env python3
"""apply_adr.py — apply the person's decision on a drafted ADR (/adr, #632).

Mechanical, after the draft and the person's word. Uses `adr.py` (copied beside it from the
author-adr skill) for every check and write, so the rules live in one place.

    python3 apply_adr.py --draft <working>/adr-draft.md|.yaml --context <working>/adr-context.yaml \
        --target <docs/adr/NNN-slug.md | <product-os>/<node>/decisions/<id>.yaml> \
        ( --decision <working>/decision.yaml | --proposed ) \
        [--adr-dir docs/adr] [--index docs/adr/_index.md] [--intents-dir <product-os>/intents] \
        --date <date> --working <working>

    python3 apply_adr.py --accept-existing <proposed ADR file> --by "<person>" --date <date> \
        [--adr-dir docs/adr] [--index docs/adr/_index.md] --working <working>

decision.yaml (written by the play from the person's typed reply):
    decision: { verdict: accept | reject, by: person, accepted_by: <name>, reply: <their words> }

What it does, in order — every check runs before the first write, so a stop writes nothing:
  0. the draft must be Proposed, the number must match its file name and be unused, every
     older ADR it names must exist (when accepting now), and the index folder must exist
  1. lint the draft against the template; a problem stops the run (exit 2)
  2. guard: a decision that would change a person's business intent stops the run before
     anything is written (exit 4) — it goes to the person
  3. reject → nothing is written (exit 5)
  4. write the record at --target (never over an existing file)
  5. accept → mark it accepted with the person's name; THEN write each forward pointer on the
     older ADRs the context names (the only edit an older ADR gets); rebuild the index
     proposed (inside a loop) → leave it proposed; pointers wait for acceptance
  6. write adr-manifest.json — what the stop condition reads

`--accept-existing` completes a proposed ADR later (a loop's final review, or by hand): accept,
pointers from the ADR's own Supersedes/Amends lines, index. No git, no network, no LLM.
"""
import argparse
import io
import json
import os
import re
import shutil
import sys
from contextlib import redirect_stdout

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import adr  # noqa: E402


def call(argv):
    """Run an adr.py command; return (exit code, parsed JSON output)."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = adr.main(argv)
    try:
        return code, json.loads(buf.getvalue())
    except ValueError:
        return code, {"raw": buf.getvalue()}


def load_yaml(path):
    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path} is not a mapping")
    return data


def older_targets(context, adr_dir):
    """[(older file, kind, part)] from the agent's judged context."""
    out = []
    for kind, key in (("superseded", "supersedes"), ("amended", "amends")):
        for item in context.get(key) or []:
            ref = str(item.get("adr") or item.get("id") or "").strip()
            part = str(item.get("part") or "full").strip()
            if part.lower() in ("full", "in full"):           # one spelling for a full supersede
                part = "full"
            path = item.get("file")
            if not path and adr_dir and re.fullmatch(r"\d{1,3}", ref):
                hits = [n for n in os.listdir(adr_dir) if n.startswith(f"{int(ref):03d}-")]
                path = os.path.join(adr_dir, hits[0]) if hits else None
            elif not path and adr_dir and os.path.isdir(adr_dir):     # a product decision, by id
                for n in sorted(os.listdir(adr_dir)):
                    if n.endswith((".yaml", ".yml")):
                        try:
                            if str(adr.load_decision(os.path.join(adr_dir, n))[1].get("id")) == ref:
                                path = os.path.join(adr_dir, n)
                                break
                        except adr.Bad:
                            continue
            elif path and adr_dir and not os.path.isabs(path) and not os.path.exists(path):
                path = os.path.join(adr_dir, path)
            out.append((path, kind, part, ref))
    return out


def refs_from_record(path):
    """For --accept-existing: the older ADRs a record names, from its own header or fields."""
    out = []
    if adr.is_yaml(path):
        _, d = adr.load_decision(path)
        for kind, key in (("superseded", "supersedes"), ("amended", "amends")):
            for item in d.get(key) or []:
                out.append({"kind": kind, "ref": str(item.get("id")), "part": item.get("part") or "full"})
        return out
    fields = adr.parse_md(adr.read(path))["fields"]
    for kind, key in (("superseded", "supersedes"), ("amended", "amends")):
        value = fields.get(key, "").strip()
        if not value or value.lower().startswith("none"):
            continue
        for chunk in re.split(r"\s·\s", value):
            m = re.match(r"\s*ADR\s*0*(\d{1,3})\s*(?:\(([^)]*)\)|—\s*(.+))?", chunk)
            if m:
                out.append({"kind": kind, "ref": m.group(1), "part": (m.group(2) or m.group(3) or "full").strip()})
    return out


def write_pointers(new_path, olders):
    written, missing = [], []
    for path, kind, part, ref in olders:
        if not path or not os.path.exists(path):
            missing.append(ref or str(path))
            continue
        code, out = call(["pointer", "--older", path, "--newer", new_path, "--kind", kind,
                          "--what", "full" if kind == "superseded" and part == "full" else part])
        (written if code == 0 else missing).append(os.path.basename(path))
    return written, missing


def finish(working, manifest, code):
    with open(os.path.join(working, "adr-manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
    print(json.dumps(manifest, indent=2))
    return code


def accept_and_link(path, by, date, olders, adr_dir, index, manifest):
    code, out = call(["accept", "--adr", path, "--by", by, "--date", date])
    if code != 0:
        manifest["problem"] = out.get("refused", "accept failed")
        return False
    written, missing = write_pointers(path, olders)
    manifest.update(status="accepted", accepted_by=by, pointers_written=written,
                    pointers_missing=missing, linked=not missing)
    if not adr.is_yaml(path) and adr_dir and index:
        call(["index", "--dir", adr_dir, "--out", index])
        listed = os.path.basename(path) in open(index, encoding="utf-8").read()
        manifest["index_ok"] = listed
    return True


class Stop(Exception):
    """A reason to write nothing: (exit code, message)."""


def draft_status(path):
    if adr.is_yaml(path):
        return str(adr.load_decision(path)[1].get("status") or "").lower()
    return adr.parse_md(adr.read(path))["fields"].get("status", "").split(" ")[0].lower()


def resolve_olders(olders, new_ref):
    """Every older ADR must exist, and none it supersedes in full may already be superseded in
    full by another record — checked before anything is written, so a refused pointer can never
    leave a record accepted with a link missing."""
    missing = [ref or str(path) for path, _, _, ref in olders if not path or not os.path.exists(path)]
    if missing:
        raise Stop(2, f"older ADRs named but not found: {', '.join(missing)} — nothing is written")
    for path, kind, part, ref in olders:
        if kind == "superseded" and part == "full":
            by = adr.superseded_in_full_by(path)
            if by and str(by).lstrip("0") != str(new_ref).lstrip("0"):
                raise Stop(2, f"{os.path.basename(path)} is already superseded in full by {by} — "
                              f"supersede that one instead; nothing is written")


def record_ref(path):
    """The record's own number (Markdown) or id (YAML)."""
    if adr.is_yaml(path):
        return str(adr.load_decision(path)[1].get("id") or "")
    return adr.parse_md(adr.read(path))["number"] or ""


def check_number(target, draft, adr_dir):
    """A Markdown ADR's number matches its file name and is not taken by another file (F5)."""
    if adr.is_yaml(target):
        return
    num = adr.parse_md(adr.read(draft))["number"]
    m = re.match(r"^(\d{3})-", os.path.basename(target))
    if not num or not m or m.group(1) != num:
        raise Stop(2, f"the ADR number ({num}) does not match the file name {os.path.basename(target)}")
    if adr_dir and os.path.isdir(adr_dir):
        taken = adr.numbers(adr_dir)
        if int(num) in taken and taken[int(num)] != os.path.basename(target):
            raise Stop(2, f"ADR {num} is already taken by {taken[int(num)]}")


def plan_new(args, manifest):
    """Read and check every input for a new record. Writes nothing. Records each check that
    passes in the manifest, so a stopped run still shows what held (SCE-2, SCE-5)."""
    for need in ("draft", "context", "target"):
        if not getattr(args, need):
            raise Stop(2, f"--{need} is required")
    if bool(args.proposed) == bool(args.decision):
        raise Stop(2, "pass exactly one of --decision (by hand) or --proposed (inside a loop)")
    if not adr.is_yaml(args.target) and not args.adr_dir:
        raise Stop(2, "--adr-dir is required for a Markdown ADR")
    try:
        context = load_yaml(args.context)
        verdict = None if args.proposed else load_yaml(args.decision).get("decision") or {}
    except (OSError, ValueError, yaml.YAMLError) as exc:
        raise Stop(3, f"cannot read an input: {exc}") from exc
    if not isinstance(context, dict):
        raise Stop(3, "the context is not a mapping")
    code, out = call(["lint", "--adr", args.draft])                       # 1. template
    if code != 0:
        raise Stop(2, out.get("problems") or out)
    manifest["lint_ok"] = True
    if draft_status(args.draft) != "proposed":                            # only a person accepts
        raise Stop(2, "the draft must be Proposed — only a person's word makes it accepted")
    guard = ["guard", "--adr", args.draft] + (["--intents-dir", args.intents_dir] if args.intents_dir else [])
    code, out = call(guard)                                                # 2. business intent
    manifest["guard"] = out
    if code == 4:
        raise Stop(4, "the decision would change a person's business intent — ask the person")
    if code != 0:
        raise Stop(2, out.get("problem") or out)
    if verdict is not None:                                                # 3. the person's word
        if verdict.get("by") != "person" or not str(verdict.get("reply") or "").strip():
            raise Stop(2, "the decision must be the person's own typed reply (by: person, reply)")
        if verdict.get("verdict") == "reject":
            raise Stop(5, "the person rejected the ADR — nothing is written")
        if verdict.get("verdict") != "accept" or not str(verdict.get("accepted_by") or "").strip():
            raise Stop(2, "verdict must be accept (with accepted_by) or reject")
    if os.path.exists(args.target):
        raise Stop(2, f"{args.target} already exists — a record is never overwritten")
    check_number(args.target, args.draft, args.adr_dir)
    olders = older_targets(context, args.adr_dir)
    if verdict is not None:            # pointers are written now, so their targets must be sound now
        resolve_olders(olders, record_ref(args.draft))
    index_dir = os.path.dirname(args.index) if args.index else None
    if index_dir and os.path.normpath(index_dir) not in {
            os.path.normpath(os.path.dirname(args.target) or "."),
            os.path.normpath(args.adr_dir or os.path.dirname(args.target) or ".")} \
            and not os.path.isdir(index_dir):
        raise Stop(2, f"the index folder for {args.index} does not exist")
    return verdict, olders


def run_new(args, manifest):
    verdict, olders = plan_new(args, manifest)
    manifest["olders"] = [{"adr": r, "file": p, "kind": k, "part": pt} for p, k, pt, r in olders]
    os.makedirs(os.path.dirname(args.target) or ".", exist_ok=True)       # 4. write
    shutil.copyfile(args.draft, args.target)
    if verdict is None:                                                    # 5. loop: proposed
        manifest.update(status="proposed", pointers_deferred=True, decided=True, linked=True)
        return 0
    ok = accept_and_link(args.target, str(verdict["accepted_by"]).strip(), args.date, olders,
                         args.adr_dir, args.index, manifest)
    manifest["decided"] = ok
    return 0 if ok and manifest["linked"] else 2


def run_accept_existing(args, manifest):
    path = args.accept_existing
    manifest["path"] = path
    code, out = call(["lint", "--adr", path])
    if code != 0:
        raise Stop(2, out.get("problems") or out)
    manifest["lint_ok"] = True
    if not (args.by or "").strip():
        raise Stop(2, "only a person accepts an ADR — --by names them")
    if draft_status(path) != "proposed":
        raise Stop(2, "only a proposed ADR can be accepted")
    adr_dir = args.adr_dir or os.path.dirname(path)
    olders = []
    for r in refs_from_record(path):
        key = "supersedes" if r["kind"] == "superseded" else "amends"
        olders += older_targets({key: [{"adr": r["ref"], "id": r["ref"], "part": r["part"]}]}, adr_dir)
    resolve_olders(olders, record_ref(path))                               # before accepting (F4)
    ok = accept_and_link(path, args.by.strip(), args.date, olders, adr_dir, args.index, manifest)
    manifest["decided"] = ok
    return 0 if ok and manifest["linked"] else 2


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--draft")
    ap.add_argument("--context")
    ap.add_argument("--target")
    ap.add_argument("--decision")
    ap.add_argument("--proposed", action="store_true")
    ap.add_argument("--accept-existing")
    ap.add_argument("--by")
    ap.add_argument("--adr-dir")
    ap.add_argument("--index")
    ap.add_argument("--intents-dir")
    ap.add_argument("--date", required=True)
    ap.add_argument("--working", required=True)
    args = ap.parse_args(argv)
    os.makedirs(args.working, exist_ok=True)
    manifest = {"decided": False, "lint_ok": False, "linked": False}
    if not args.accept_existing:
        manifest.update(target=args.target, shape="yaml" if adr.is_yaml(args.target or "") else "markdown")
    try:
        code = run_accept_existing(args, manifest) if args.accept_existing else run_new(args, manifest)
    except Stop as stop:
        code, why = stop.args
        manifest["problem"] = why
        if code == 4:
            manifest["business_intent"] = True
        if code == 5:
            manifest["rejected"] = True
    except (adr.Bad, OSError, ValueError, TypeError, AttributeError, yaml.YAMLError) as exc:
        code = 3
        manifest["problem"] = f"unreadable or wrong-shaped input: {exc}"
    return finish(args.working, manifest, code)


if __name__ == "__main__":
    sys.exit(main())
