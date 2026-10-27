#!/usr/bin/env python3
"""
write_hidden_file.py — the slice's hidden file of failure and recovery conditions (/shape-slice, C15).

Ontology v11 and ADR 052: /shape-slice writes the slice's hidden file when it shapes the
slice, one entry for each feature, from that feature's ICE and its capability's ICE, with
exactly one recovery condition for each "Fails if" line (standards/rules/expectation-generation.md,
"A feature's recovery"). The file is at

    <plans-root>/<plan-id>/evals/<slug>/failure-and-recovery.md

where <plan-id> is the number of the slice's first business intent (bi-340 gives 340) and
<slug> is the slice's slug. The folder is made also when no plan file exists. A builder never
reads this file.

    python3 write_hidden_file.py lines --root <model> --spine <spine> --slice-id <id> \
        --plans-root <plans dir> --out <hidden-lines.json>
    python3 write_hidden_file.py write --lines <hidden-lines.json> \
        --recoveries <hidden-recoveries.json> --plans-root <plans dir> --out <hidden-write.json>
    python3 write_hidden_file.py check --root <model> --spine <spine> --slice-id <id> \
        --plans-root <plans dir> --out <hidden-file.json> [--clear-working <path>]...

  lines — lists, for each feature of the slice, the "Fails if" lines of its ICE and of its
          capability's ICE: from the inline `## Agent intent (ICE)` section of the part's page
          (`- Fails if: ...`), or, when the spine has an `ices` list, from the `## Intent`
          section of the part's ice.md. It says which of the two ICE is thin (`metadata.thin`
          or the Thin line). An entry already in the file with the same lines and thin marks is
          `kept: true` and keeps its ids; a changed entry keeps the ids of its lines that did
          not change. `--redraft <feature id>` (repeatable, from the person's change) marks that
          entry not kept, with its ids, so its recoveries are drafted again. Lines match with case, spacing and a closing full stop not counted. New lines take the next free id (F1, F2, ... unique in the whole file).
          hidden-lines.json:
              {slice, plan_id, path (relative to plans-root),
               entries: [{feature, name, capability, thin: ["feature"|"capability", ...],
                          kept: bool, lines: [{id, from: "feature"|"capability", text}]}]}
  write — takes the agent's hidden-recoveries.json
              {entries: [{feature, recoveries: [{line, when, way_back, who_fixes}]}]}
          and writes the file through safe_write.atomic_write. The recoveries' `vague` list
          (the lines too vague to judge) goes into hidden-write.json as
          `vague: [{feature, count}]`, by feature and with no line id, so the brief can show it. It keeps each kept entry byte for byte,
          writes the others, and drops an entry whose feature left the slice. It refuses with
          exit 2, and writes nothing, when a line has no recovery or two, a recovery names no
          line of its entry, `who_fixes` is not exactly "the builder can fix this alone" or
          "a person must decide", `when` or `way_back` is empty, or the path leaves plans-root.
  check — reads the file back against the two ICE of each feature and writes
              {ok, path, entries: [{feature, capability, thin, lines}],
               counts: {lines, builder_alone, person}, problems}
          Exit 0 when ok, 1 when not ok (for example, a "Fails if" line of the ICE is not in
          the file, or a line has no recovery).
          --clear-working <path> (repeatable): when the check reads ok, delete each named
          working file (hidden-lines.json, hidden-recoveries.json), so no copy of the "Fails
          if" lines or their ids stays outside the evals folder; when it is not ok, keep them.
          A path under plans-root is refused (exit 2, nothing deleted). `cleared` lists what
          was deleted.

File shape: one `## <feature id>: <name>` heading for each feature, then the capability and
the ICE it was written from (and which is thin), `### Failure conditions` with
`- F<n> (from the feature ICE): <text>` or `(from the capability ICE)`, or `- none`, and
`### Recovery` with `- For F<n>` followed by `  - When:`, `  - Way back:` and `  - Who fixes:`.

Reads and writes files on disk only; no git, no network. Exit 2 on a refusal or usage error.
"""

import argparse
import json
import os
import re
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("write_hidden_file.py: PyYAML is required (pip install pyyaml).\n")
    sys.exit(2)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from safe_write import atomic_write  # noqa: E402

FILE = "failure-and-recovery.md"
WHO = ("the builder can fix this alone", "a person must decide")
THIN_LINE = ("Thin: proposed by `/shape-slice` from the person's answers; deepen with "
             "`/discover-capabilities`.")
FAILS_IF = re.compile(r"^\s*[-*]\s+Fails if:\s*(?P<text>\S.*?)\s*$")
HEAD = re.compile(r"^## (?P<feature>[^:\s]+): (?P<name>.*?)\s*$")
FLINE = re.compile(r"^- (?P<id>F\d+) \(from the (?P<from>feature|capability) ICE\): (?P<text>.*?)\s*$")
FOR = re.compile(r"^- For (?P<id>F\d+)\s*$")
PART = re.compile(r"^\s+- (?P<key>When|Way back|Who fixes):\s*(?P<text>.*?)\s*$")
WRITTEN_FROM = re.compile(r"^- Written from: (?P<text>.*)$")
OLD_THIN = re.compile(r"^- Thin: (?P<text>.*)$")  # the form written by hand before this script


def same_text(text):
    """A line's text for matching: case, spacing and a closing full stop do not count."""
    return " ".join(str(text).split()).rstrip(".").lower()


class Refused(Exception):
    """Nothing is written; the message says why."""


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _entry(spine, key, eid):
    return next((e for e in spine.get(key) or [] if isinstance(e, dict) and e.get("id") == eid), None)


def load_spine(path):
    spine = yaml.safe_load(_read(path)) or {}
    if not isinstance(spine, dict):
        raise Refused("the spine must be a YAML mapping")
    return spine


def plan_id_of(sl):
    intents = sl.get("intents") or []
    m = re.fullmatch(r"bi-(\d+)", str(intents[0])) if intents else None
    if not m:
        raise Refused(f"slice '{sl.get('id')}' has no first business intent of the form bi-<number>; "
                      "the home plan's id is that number")
    return m.group(1)


def inside(root, rel, what):
    real_root = os.path.realpath(root)
    if os.path.isabs(rel) or ".." in rel.replace("\\", "/").split("/"):
        raise Refused(f"{what} '{rel}' leaves the plans folder")
    target = os.path.realpath(os.path.join(root, rel))
    if not target.startswith(real_root + os.sep):
        raise Refused(f"{what} '{rel}' leaves the plans folder")
    return os.path.join(root, rel)


def section(text, heading):
    lines = text.splitlines()
    at = next((i for i, ln in enumerate(lines) if ln.strip() == heading), None)
    if at is None:
        return []
    end = next((i for i in range(at + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return lines[at + 1:end]


def ice_of(root, spine, part):
    """(page text or None, thin) of a capability's or feature's ICE."""
    if part is None:
        return None, False
    if "ices" in spine:
        ice = next((i for i in spine.get("ices") or [] if isinstance(i, dict)
                    and i.get("for") == part.get("id")), None)
        holder, heading = ice, "## Intent"
    else:
        holder, heading = part, "## Agent intent (ICE)"
    if holder is None or not holder.get("doc"):
        return None, False
    path = os.path.join(root, holder["doc"])
    text = _read(path) if os.path.isfile(path) else ""
    thin = bool((holder.get("metadata") or {}).get("thin")) or THIN_LINE in text
    lines = [m.group("text") for m in (FAILS_IF.match(x) for x in section(text, heading)) if m]
    return lines, thin


def page_name(root, part, prefix):
    path = os.path.join(root, part.get("doc") or "")
    if os.path.isfile(path):
        for ln in _read(path).splitlines():
            if ln.startswith("# " + prefix):
                return ln[len("# " + prefix):].strip()
    return part.get("slug") or part.get("id")


def wanted(root, spine, slice_id):
    """The slice, its plan id, the file's path and, per feature, its ICE lines and thin marks."""
    sl = _entry(spine, "slices", slice_id)
    if sl is None:
        raise Refused(f"slice '{slice_id}' is not in the spine")
    if not sl.get("slug"):
        raise Refused(f"slice '{slice_id}' has no slug")
    plan_id = plan_id_of(sl)
    rel = f"{plan_id}/evals/{sl['slug']}/{FILE}"
    out = []
    for fid in sl.get("feature_refs") or []:
        f = _entry(spine, "features", fid)
        if f is None:
            raise Refused(f"feature '{fid}' of slice '{slice_id}' is not in the spine")
        cap = _entry(spine, "capabilities", f.get("capability")) if f.get("capability") else None
        f_lines, f_thin = ice_of(root, spine, f)
        c_lines, c_thin = ice_of(root, spine, cap)
        lines = [("feature", t) for t in f_lines or []] + [("capability", t) for t in c_lines or []]
        thin = (["feature"] if f_thin else []) + (["capability"] if c_thin else [])
        out.append({"feature": fid, "name": page_name(root, f, "Feature:"),
                    "capability": cap.get("id") if cap else None, "thin": thin, "lines": lines})
    return sl, plan_id, rel, out


def parse(text):
    """(preamble, [block]) of a hidden file; each block keeps its text byte for byte."""
    preamble, blocks, current = [], [], None
    for ln in text.splitlines(keepends=True):
        if HEAD.match(ln.rstrip("\n")):
            current = {"lines": [ln]}
            blocks.append(current)
        elif current is None:
            preamble.append(ln)
        else:
            current["lines"].append(ln)
    for b in blocks:
        b["text"] = "".join(b["lines"])
        m = HEAD.match(b["lines"][0].rstrip("\n"))
        b["feature"], b["name"] = m.group("feature"), m.group("name")
        b["failures"], b["recoveries"], b["thin"] = [], {}, []
        rec = None
        for ln in b["lines"][1:]:
            s = ln.rstrip("\n")
            fm, rm, pm, wm = FLINE.match(s), FOR.match(s), PART.match(s), WRITTEN_FROM.match(s)
            if fm:
                b["failures"].append({"id": fm.group("id"), "from": fm.group("from"),
                                      "text": fm.group("text")})
            elif rm:
                rec = {}
                b["recoveries"].setdefault(rm.group("id"), []).append(rec)
            elif pm and rec is not None:
                rec[pm.group("key")] = pm.group("text")
            elif wm:
                t = wm.group("text")
                b["thin"] = [k for k in ("feature", "capability") if f"the {k} ICE (thin)" in t]
            elif OLD_THIN.match(s) and not b["thin"]:
                t = OLD_THIN.match(s).group("text").lower()
                b["thin"] = ["feature", "capability"] if t.startswith("both") else \
                    [k for k in ("feature", "capability") if k in t]
    return "".join(preamble), blocks


def cmd_lines(args):
    spine = load_spine(args.spine)
    sl, plan_id, rel, want = wanted(args.root, spine, args.slice_id)
    path = inside(args.plans_root, rel, "the hidden file")
    blocks = parse(_read(path))[1] if os.path.isfile(path) else []
    by_feature = {b["feature"]: b for b in blocks}
    used = {int(f["id"][1:]) for b in blocks for f in b["failures"]}
    nxt = max(used, default=0)
    redraft = set(getattr(args, "redraft", None) or [])
    unknown = redraft - {w["feature"] for w in want}
    if unknown:
        raise Refused(f"--redraft names {', '.join(sorted(unknown))}, which is not a feature of the slice")
    entries = []
    for w in want:
        old = by_feature.get(w["feature"])
        old_ids = {(f["from"], same_text(f["text"])): f["id"] for f in (old["failures"] if old else [])}
        want_keys = [(frm, same_text(text)) for frm, text in w["lines"]]
        same = old is not None and sorted(old_ids) == sorted(want_keys) \
            and len(old["failures"]) == len(w["lines"]) and sorted(old["thin"]) == sorted(w["thin"]) \
            and w["feature"] not in redraft
        lines = []
        for frm, text in w["lines"]:
            lid = old_ids.get((frm, same_text(text)))
            if lid is None:
                nxt += 1
                lid = f"F{nxt}"
            lines.append({"id": lid, "from": frm, "text": text})
        entries.append({"feature": w["feature"], "name": w["name"], "capability": w["capability"],
                        "thin": w["thin"], "kept": bool(same), "lines": lines})
    out = {"slice": sl["id"], "plan_id": plan_id, "path": rel, "entries": entries}
    atomic_write(args.out, json.dumps(out, indent=2))
    print(json.dumps({"path": rel, "entries": [{"feature": e["feature"], "kept": e["kept"],
                                                "lines": len(e["lines"])} for e in entries]},
                     indent=2))
    return 0


def written_from(entry):
    f = "the feature ICE" + (" (thin)" if "feature" in entry["thin"] else "")
    if entry.get("capability"):
        c = "the capability ICE" + (" (thin)" if "capability" in entry["thin"] else "")
        return f"{f} and {c}"
    return f"{f} (the feature has no capability yet)"


def render(entry, recs):
    out = [f"## {entry['feature']}: {entry['name']}", "",
           f"- Capability: {entry.get('capability') or 'none yet'}",
           f"- Written from: {written_from(entry)}."]
    for kind in entry["thin"]:
        out.append(f"- Thin ICE: the {kind} ICE is thin, so its recovery may be weak until "
                   "`/discover-capabilities` deepens it.")
    out += ["", "### Failure conditions", ""]
    out += [f"- {ln['id']} (from the {ln['from']} ICE): {ln['text']}" for ln in entry["lines"]] \
        or ["- none"]
    out += ["", "### Recovery", ""]
    if not entry["lines"]:
        out.append("- none")
    for ln in entry["lines"]:
        r = recs[ln["id"]]
        out += [f"- For {ln['id']}", f"  - When: {r['when'].strip()}",
                f"  - Way back: {r['way_back'].strip()}", f"  - Who fixes: {r['who_fixes']}"]
    return "\n".join(out) + "\n"


def cmd_write(args):
    lines = json.loads(_read(args.lines))
    recov = json.loads(_read(args.recoveries))
    path = inside(args.plans_root, lines.get("path") or "", "the hidden file")
    by_feature = {}
    for e in (recov.get("entries") if isinstance(recov, dict) else None) or []:
        by_feature.setdefault(e.get("feature"), []).extend(e.get("recoveries") or [])
    preamble, blocks = parse(_read(path)) if os.path.isfile(path) else ("", [])
    old = {b["feature"]: b for b in blocks}
    parts, written, kept = [], [], []
    for e in lines.get("entries") or []:
        if e.get("kept"):
            if e["feature"] not in old:
                raise Refused(f"the entry for '{e['feature']}' is marked kept but is not in the file")
            parts.append(old[e["feature"]]["text"])
            kept.append(e["feature"])
            continue
        ids = [ln["id"] for ln in e["lines"]]
        recs = {}
        for r in by_feature.get(e["feature"], []):
            if r.get("line") not in ids:
                raise Refused(f"a recovery for '{e['feature']}' names line '{r.get('line')}', which "
                              "is not one of its lines")
            if r["line"] in recs:
                raise Refused(f"line {r['line']} of '{e['feature']}' has two recoveries; a line has "
                              "exactly one")
            if r.get("who_fixes") not in WHO:
                raise Refused(f"line {r['line']} of '{e['feature']}' says who fixes it as "
                              f"'{r.get('who_fixes')}'; write exactly '{WHO[0]}' or '{WHO[1]}'")
            for key in ("when", "way_back"):
                if not str(r.get(key) or "").strip():
                    raise Refused(f"line {r['line']} of '{e['feature']}' has no {key}")
            recs[r["line"]] = r
        missing = [i for i in ids if i not in recs]
        if missing:
            raise Refused(f"line {', '.join(missing)} of '{e['feature']}' has no recovery; each "
                          "\"Fails if\" line has exactly one")
        parts.append(render(e, recs))
        written.append(e["feature"])
    dropped = [f for f in old if f not in {e["feature"] for e in lines.get("entries") or []}]
    if not preamble:
        preamble = (f"# Failure and recovery: slice {lines.get('slice')}\n\n"
                    "Written by `/shape-slice` from each feature's ICE and its capability's ICE: one "
                    "recovery for each \"Fails if\" line. A builder never reads this file.\n\n")
    text = preamble
    for part in parts:
        if not text.endswith("\n\n"):
            text += "\n" if text.endswith("\n") else "\n\n"
        text += part
    atomic_write(path, text)
    vague_ids = set((recov.get("vague") if isinstance(recov, dict) else None) or [])
    vague = [{"feature": e["feature"],
              "count": sum(1 for ln in e.get("lines") or [] if ln.get("id") in vague_ids)}
             for e in lines.get("entries") or [] if e["feature"] in written]
    out = {"ok": True, "path": lines.get("path"), "written": written, "kept": kept,
           "dropped": dropped, "vague": [v for v in vague if v["count"]]}
    atomic_write(args.out, json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
    return 0


def working_files(plans_root, paths):
    """The working copies --clear-working names. A path under the plans folder is refused."""
    real_root = os.path.realpath(plans_root)
    for p in paths:
        real = os.path.realpath(p)
        if real == real_root or real.startswith(real_root + os.sep):
            raise Refused(f"--clear-working '{p}' is under the plans folder; it clears only "
                          "working files, never the hidden file or its folder")
    return paths


def cmd_check(args):
    clear = working_files(args.plans_root, args.clear_working or [])
    spine = load_spine(args.spine)
    _sl, _plan, rel, want = wanted(args.root, spine, args.slice_id)
    path = inside(args.plans_root, rel, "the hidden file")
    problems, entries = [], []
    counts = {"lines": 0, "builder_alone": 0, "person": 0}
    blocks = []
    if not os.path.isfile(path):
        problems.append(f"the hidden file is missing at {rel}")
    else:
        blocks = parse(_read(path))[1]
    by_feature = {}
    for b in blocks:
        if b["feature"] in by_feature:
            problems.append(f"'{b['feature']}' has two entries")
        by_feature[b["feature"]] = b
    seen_ids = {}
    for b in blocks:
        for f in b["failures"]:
            if f["id"] in seen_ids:
                problems.append(f"{f['id']} is used twice (in '{seen_ids[f['id']]}' and '{b['feature']}')")
            seen_ids[f["id"]] = b["feature"]
    for w in want:
        b = by_feature.get(w["feature"])
        entries.append({"feature": w["feature"], "capability": w["capability"], "thin": w["thin"],
                        "lines": len(w["lines"])})
        if b is None:
            if blocks or os.path.isfile(path):
                problems.append(f"no entry for feature '{w['feature']}'")
            continue
        have = [(f["from"], f["text"]) for f in b["failures"]]
        have_keys = [(frm, same_text(t)) for frm, t in have]
        want_keys = [(frm, same_text(t)) for frm, t in w["lines"]]
        for line, key in zip(w["lines"], want_keys):
            if key not in have_keys:
                problems.append(f"'{w['feature']}': the {line[0]} ICE line \"{line[1]}\" is not in "
                                "the file")
        for line, key in zip(have, have_keys):
            if key not in want_keys:
                problems.append(f"'{w['feature']}': the line \"{line[1]}\" is in no ICE of the feature")
        if sorted(b["thin"]) != sorted(w["thin"]):
            problems.append(f"'{w['feature']}': the entry says the thin ICE are {b['thin'] or 'none'}, "
                            f"but they are {w['thin'] or 'none'}")
        for f in b["failures"]:
            recs = b["recoveries"].get(f["id"], [])
            if len(recs) != 1:
                problems.append(f"'{w['feature']}': {f['id']} has {len(recs)} recoveries, not one")
                continue
            r = recs[0]
            if not r.get("When") or not r.get("Way back"):
                problems.append(f"'{w['feature']}': the recovery of {f['id']} has no When or Way back")
            if r.get("Who fixes") not in WHO:
                problems.append(f"'{w['feature']}': the recovery of {f['id']} says who fixes it as "
                                f"'{r.get('Who fixes')}'")
            counts["lines"] += 1
            if r.get("Who fixes") == WHO[0]:
                counts["builder_alone"] += 1
            elif r.get("Who fixes") == WHO[1]:
                counts["person"] += 1
        for rid in b["recoveries"]:
            if rid not in {f["id"] for f in b["failures"]}:
                problems.append(f"'{w['feature']}': a recovery is for {rid}, which is not one of its lines")
    for f in by_feature:
        if f not in {w["feature"] for w in want}:
            problems.append(f"the file has an entry for '{f}', which is not a feature of the slice")
    cleared = []
    if not problems:
        for p in clear:
            if os.path.isfile(p):
                os.remove(p)
                cleared.append(p)
    out = {"ok": not problems, "path": rel, "entries": entries, "counts": counts,
           "problems": problems, "cleared": cleared}
    atomic_write(args.out, json.dumps(out, indent=2))
    print(json.dumps({"ok": out["ok"], "counts": counts, "problems": problems,
                      "cleared": cleared}, indent=2))
    return 0 if out["ok"] else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="The slice's hidden file of failure and recovery conditions.")
    sub = ap.add_subparsers(dest="command", required=True)
    for name in ("lines", "check"):
        p = sub.add_parser(name)
        p.add_argument("--root", required=True)
        p.add_argument("--spine", required=True)
        p.add_argument("--slice-id", required=True)
        p.add_argument("--plans-root", required=True)
        p.add_argument("--out", required=True)
        if name == "lines":
            p.add_argument("--redraft", action="append", default=[],
                           help="a feature whose entry is drafted again; repeatable")
        if name == "check":
            p.add_argument("--clear-working", action="append", default=[],
                           help="a working file to delete when the check reads ok; repeatable")
    w = sub.add_parser("write")
    w.add_argument("--lines", required=True)
    w.add_argument("--recoveries", required=True)
    w.add_argument("--plans-root", required=True)
    w.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        return {"lines": cmd_lines, "write": cmd_write, "check": cmd_check}[args.command](args)
    except Refused as exc:
        sys.stderr.write(f"write_hidden_file.py: not written — {exc}\n")
        if getattr(args, "out", None) and args.command == "write":
            atomic_write(args.out, json.dumps({"ok": False, "refused": str(exc)}, indent=2))
        return 2
    except (OSError, ValueError, yaml.YAMLError) as exc:
        sys.stderr.write(f"write_hidden_file.py: cannot read an input: {exc}\n")
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
