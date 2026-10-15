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

What it does, in order, and only in this order:
  1. lint the draft against the template; a problem stops the run (exit 2)
  2. guard: a decision that would change a person's business intent stops the run before
     anything is written (exit 4) — it goes to the person
  3. reject → nothing is written (exit 5)
  4. write the record at --target (never over an existing file)
  5. accept → mark it accepted with the person's name; THEN write each forward pointer on the
     older ADRs the context names (the only edit an older ADR gets); rebuild the index
     proposed (inside a drive) → leave it proposed; pointers wait for acceptance
  6. write adr-manifest.json — what the stop condition reads

`--accept-existing` completes a proposed ADR later (a drive's final review, or by hand): accept,
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
        for chunk in re.split(r"\s·\s", fields.get(key, "")):
            m = re.search(r"ADR\s*0*(\d{1,3})\s*(?:\(([^)]*)\)|—\s*(.+))?", chunk)
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

    if args.accept_existing:                    # complete a proposed ADR later
        path = args.accept_existing
        code, out = call(["lint", "--adr", path])
        manifest.update(path=path, lint_ok=code == 0)
        if code != 0:
            manifest["problem"] = out.get("problems")
            return finish(args.working, manifest, 2)
        if not (args.by or "").strip():
            manifest["problem"] = "only a person accepts an ADR — --by names them"
            return finish(args.working, manifest, 2)
        olders = []
        for r in refs_from_record(path):
            olders += older_targets({("supersedes" if r["kind"] == "superseded" else "amends"):
                                     [{"adr": r["ref"], "part": r["part"]}]},
                                    args.adr_dir or os.path.dirname(path))
        ok = accept_and_link(path, args.by.strip(), args.date, olders,
                             args.adr_dir or os.path.dirname(path), args.index, manifest)
        manifest["decided"] = ok
        return finish(args.working, manifest, 0 if ok and manifest["linked"] else 2)

    for need in ("draft", "context", "target"):
        if not getattr(args, need):
            manifest["problem"] = f"--{need} is required"
            return finish(args.working, manifest, 2)
    if bool(args.proposed) == bool(args.decision):
        manifest["problem"] = "pass exactly one of --decision (by hand) or --proposed (inside a drive)"
        return finish(args.working, manifest, 2)
    try:
        context = load_yaml(args.context)
        verdict = None if args.proposed else load_yaml(args.decision).get("decision") or {}
    except (OSError, ValueError, yaml.YAMLError) as exc:
        manifest["problem"] = f"cannot read an input: {exc}"
        return finish(args.working, manifest, 3)
    manifest.update(target=args.target, shape="yaml" if adr.is_yaml(args.target) else "markdown")

    code, out = call(["lint", "--adr", args.draft])                       # 1. template
    manifest["lint_ok"] = code == 0
    if code != 0:
        manifest["problem"] = out.get("problems") or out
        return finish(args.working, manifest, 2)
    guard = ["guard", "--adr", args.draft] + (["--intents-dir", args.intents_dir] if args.intents_dir else [])
    code, out = call(guard)                                                # 2. business intent
    manifest["guard"] = out
    if code == 4:
        manifest["business_intent"] = True
        manifest["problem"] = "the decision would change a person's business intent — ask the person"
        return finish(args.working, manifest, 4)
    if code != 0:
        manifest["problem"] = out.get("problem") or out
        return finish(args.working, manifest, 2)
    if verdict is not None:                                                # 3. the person's word
        if verdict.get("by") != "person" or not str(verdict.get("reply") or "").strip():
            manifest["problem"] = "the decision must be the person's own typed reply (by: person, reply)"
            return finish(args.working, manifest, 2)
        if verdict.get("verdict") == "reject":
            manifest.update(rejected=True, problem="the person rejected the ADR — nothing is written")
            return finish(args.working, manifest, 5)
        if verdict.get("verdict") != "accept" or not str(verdict.get("accepted_by") or "").strip():
            manifest["problem"] = "verdict must be accept (with accepted_by) or reject"
            return finish(args.working, manifest, 2)
    if os.path.exists(args.target):                                        # 4. write, never over
        manifest["problem"] = f"{args.target} already exists — a record is never overwritten"
        return finish(args.working, manifest, 2)
    os.makedirs(os.path.dirname(args.target) or ".", exist_ok=True)
    shutil.copyfile(args.draft, args.target)
    olders = older_targets(context, args.adr_dir)
    manifest["olders"] = [{"adr": r, "file": p, "kind": k, "part": pt} for p, k, pt, r in olders]
    if args.proposed:                                                      # 5. drive: proposed
        manifest.update(status="proposed", pointers_deferred=True, decided=True, linked=True)
        return finish(args.working, manifest, 0)
    ok = accept_and_link(args.target, str(verdict["accepted_by"]).strip(), args.date, olders,
                         args.adr_dir, args.index, manifest)
    manifest["decided"] = ok
    return finish(args.working, manifest, 0 if ok and manifest["linked"] else 2)


if __name__ == "__main__":
    sys.exit(main())
