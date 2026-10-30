#!/usr/bin/env python3
"""
slice_check.py — the model's own checks after /shape-slice wrote the slice (C6, C9, C11, C16).

    python3 slice_check.py baseline --root <product-os dir> --spine <_spine.yaml> \
        --out <lint-before-run.json>
    python3 slice_check.py --root <product-os dir> --spine <_spine.yaml> \
        --slice-id <id> --intent <bi-id> [--baseline <lint-before-run.json>] \
        [--fills <fills.json>] --out <slice-check.json>

`baseline` runs the shared grounding linter once, before the run's first write, and keeps
its errors (paths relative to the model folder).

The check runs the same linter over the whole model (`lint_grounding.py --root --spine`: the
structure and link check, with the old-name guard inside it) and then checks the slices:
  - the slice this run wrote is in the spine and lists the business intent;
  - every spine slice entry holds the six fields id, slug, feature_refs, vertical, intents,
    record (in any order) and no other — no status, order, effort, depends_on or domain_ref —
    with record pointing to slices/<id>.yaml;
  - every spine slice's record at slices/<id>.yaml follows slice.yaml v2:
        slice:   {id, slug, name, outcome, feature_refs, vertical, intents}
        surface: {id, name, persona_ref, user_action}
    each field present and not empty; slice.id, feature_refs, vertical and intents equal to
    the spine entry's; surface.name equal to the vertical. A record with no persona_ref (no
    tester) is not valid;
  - the thin marks of each part of this slice agree (ontology v11, v14). A part is thin when
    `metadata.thin` is true on its spine entry (the `ices` entry, or the part's own entry) or
    the fills (--fills) list it in `thin`; a thin part must have the Thin line on its ICE page,
    and a page with the Thin line must have `metadata.thin: true`. The Thin line is any line
    that starts "Thin:" (new pages get "Thin: proposed from the person's words; deepen with
    `/discover-capabilities`.")
    just before `## Agent intent (ICE)` (or `## Intent` in an ice.md); and a thin ICE has
    Goal, Limit, Fails if, Context and Checked by (an ice.md: Goal, Limit and Fails if under
    Intent, and a line under Context and under Expectation).

THE OWN-PARTS RULE. The slice's own pages are its features, their capabilities, their
domains, their ICE pages and the slice record. `valid` is false when:
  - any of the slice's own pages has a problem, even one the baseline already had (the run
    brings each page it moves or uses up to the current rules);
  - the linter finds an error the baseline did not have;
  - a check of this run's slice above fails.
A lint error in another page that the baseline already had goes in `older_problems`: it is
shown to the person and does not block the run. Without --baseline, every lint error counts.
The same slice checks of every OTHER slice are `warnings`: a slice an earlier run or a hand
edit left wrong is shown to the person, but it does not block this run.

Writes {"valid", "lint", "problems", "older_problems", "warnings"}. Exit 0 valid, 1 not
valid, 2 usage error. Files on disk only; no git, no network.
"""

import argparse
import json
import os
import re
import subprocess
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("slice_check.py: PyYAML is required (pip install pyyaml).\n")
    sys.exit(2)

HERE = os.path.dirname(os.path.abspath(__file__))
SPINE_FIELDS = ["id", "slug", "feature_refs", "vertical", "intents", "record"]
RECORD_SLICE = ["id", "slug", "name", "outcome", "feature_refs", "vertical", "intents"]
RECORD_SURFACE = ["id", "name", "persona_ref", "user_action"]
THIN_LINE = "Thin: proposed from the person's words; deepen with `/discover-capabilities`."  # ontology v14
# Any line that starts "Thin:" just before the ICE is the mark (ontology v14): a page written
# with the line of v11 ("Thin: proposed by `/shape-slice` ...") is still thin.
THIN_ANY = re.compile(r"^\s*Thin:")
INLINE_ICE = "## Agent intent (ICE)"
THIN_LABELS = ("Goal", "Limit", "Fails if", "Context", "Checked by")


def lint(root, spine):
    p = subprocess.run([sys.executable, os.path.join(HERE, "lint_grounding.py"),
                        "--root", root, "--spine", spine], capture_output=True, text=True)
    try:
        report = json.loads(p.stdout)
    except json.JSONDecodeError:
        report = {"ok": False, "errors": [p.stderr.strip() or "the linter gave no report"]}
    if p.returncode == 2:
        report["ok"] = False
        report.setdefault("errors", []).append(p.stderr.strip() or "the linter stopped")
    return report


def relative(root, message):
    """A lint message with the model folder's own path taken out, so two runs compare."""
    for prefix in {root.rstrip("/") + "/", os.path.normpath(root) + os.sep}:
        message = message.replace(prefix, "")
    return message


def lint_errors(root, spine):
    report = lint(root, spine)
    return report, [relative(root, e) for e in report.get("errors") or []]


def _filled(value):
    if isinstance(value, str):
        return value.strip() != ""
    if isinstance(value, list):
        return bool(value)
    return value is not None


def record_problems(root, entry):
    sid = entry.get("id")
    rec_path = os.path.join(root, "slices", f"{sid}.yaml")
    if not os.path.isfile(rec_path):
        return [f"slice '{sid}' has no record at slices/{sid}.yaml"]
    with open(rec_path, encoding="utf-8") as fh:
        rec = yaml.safe_load(fh) or {}
    if not isinstance(rec, dict):
        return [f"slice '{sid}' record is not a YAML mapping"]
    problems = []
    body = rec.get("slice") if isinstance(rec.get("slice"), dict) else {}
    for key in RECORD_SLICE:
        if not _filled(body.get(key)):
            problems.append(f"slice '{sid}' record has no slice.{key}")
    for key in ("id", "feature_refs", "vertical", "intents"):
        if _filled(body.get(key)) and body.get(key) != entry.get(key):
            problems.append(f"slice '{sid}' record slice.{key} is {body.get(key)!r}, not the "
                            f"spine entry's {entry.get(key)!r}")
    surface = rec.get("surface")
    if not isinstance(surface, dict):
        problems.append(f"slice '{sid}' record does not hold exactly one surface (top-level "
                        "`surface`, slice.yaml v2)")
        return problems
    for key in RECORD_SURFACE:
        if not _filled(surface.get(key)):
            what = " (no tester)" if key == "persona_ref" else ""
            problems.append(f"slice '{sid}' record surface has no {key}{what}")
    if _filled(surface.get("name")) and surface.get("name") != entry.get("vertical"):
        problems.append(f"slice '{sid}' surface '{surface.get('name')}' is not its vertical "
                        f"'{entry.get('vertical')}'")
    return problems


def entry_problems(entry):
    sid = entry.get("id")
    problems = []
    keys = list(entry)
    if set(keys) != set(SPINE_FIELDS) or len(keys) != len(SPINE_FIELDS):
        problems.append(f"slice '{sid}' spine entry holds {keys}, not exactly the six fields "
                        f"{SPINE_FIELDS}")
    if entry.get("record") != f"slices/{sid}.yaml":
        problems.append(f"slice '{sid}' record pointer is {entry.get('record')!r}, "
                        f"not 'slices/{sid}.yaml'")
    return problems


def _entry(spine, key, eid):
    return next((e for e in spine.get(key) or [] if isinstance(e, dict) and e.get("id") == eid), None)


def own_parts(spine, entry):
    """[(kind, id, spine entry)] for the slice's features, their capabilities and domains."""
    out, seen = [], set()
    for fid in entry.get("feature_refs") or []:
        for kind, key, eid in (("feature", "features", fid),):
            f = _entry(spine, key, eid)
            if f is None or eid in seen:
                continue
            seen.add(eid)
            out.append((kind, eid, f))
            cap = _entry(spine, "capabilities", f.get("capability")) if f.get("capability") else None
            if cap is not None and cap.get("id") not in seen:
                seen.add(cap.get("id"))
                out.append(("capability", cap.get("id"), cap))
                dom = _entry(spine, "domains", cap.get("domain")) if cap.get("domain") else None
                if dom is not None and dom.get("id") not in seen:
                    seen.add(dom.get("id"))
                    out.append(("domain", dom.get("id"), dom))
    return out


def own_names(spine, entry, parts):
    """The doc paths and spine names that mark a lint error as one of the slice's own."""
    docs, names = set(), set()
    ices = {i.get("for"): i for i in spine.get("ices") or [] if isinstance(i, dict)}
    for kind, eid, e in parts:
        if e.get("doc"):
            docs.add(os.path.normpath(e["doc"]))
        names.add(f"spine {kind} '{eid}'")
        names.add(f"'{eid}' has two ICE")
        ice = ices.get(eid)
        if ice is not None:
            if ice.get("doc"):
                docs.add(os.path.normpath(ice["doc"]))
            names.add(f"spine ice '{ice.get('id')}'")
    sid = entry.get("id")
    docs.add(f"slices/{sid}.yaml")
    names.add(f"spine slice '{sid}'")
    return docs, names


def is_own(message, docs, names):
    return any(n in message for n in names) or any(
        message.startswith(d + ":") or f"'{d}'" in message for d in docs)


def section(text, heading):
    lines = text.splitlines()
    at = next((i for i, ln in enumerate(lines) if ln.strip() == heading), None)
    if at is None:
        return None, None
    end = next((i for i in range(at + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return at, lines[at + 1:end]


def thin_problems(root, spine, parts, listed=()):
    """Thin marks: a part is thin when its spine metadata says so (the ICE entry or the part's
    own entry) or the fills list it; a thin part needs the Thin line on its ICE page, and a page
    with the Thin line needs metadata.thin on the spine."""
    out = []
    ices = {i.get("for"): i for i in spine.get("ices") or [] if isinstance(i, dict)}
    for kind, eid, e in parts:
        if kind == "domain":
            continue
        ice = ices.get(eid)
        holder = ice if "ices" in spine else e
        marked = [x for x in (holder, e) if x is not None and (x.get("metadata") or {}).get("thin")]
        thin = bool(marked) or eid in listed
        path = os.path.join(root, holder["doc"]) if holder is not None and holder.get("doc") else None
        if path is None or not os.path.isfile(path):
            if thin:
                out.append(f"thin mark drift on {kind} '{eid}': it is marked thin, but it has no ICE "
                           "page to hold the Thin line; write the thin ICE and its Thin line")
            continue
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        heading = "## Intent" if "ices" in spine else INLINE_ICE
        at, body = section(text, heading)
        lines = text.splitlines()
        before = next((ln.strip() for ln in reversed(lines[:at]) if ln.strip()), "") if at else ""
        line = bool(THIN_ANY.match(before))
        meta = bool((holder.get("metadata") or {}).get("thin"))
        if thin and not line:
            out.append(f"thin mark drift on {kind} '{eid}': it is marked thin "
                       f"({'listed in the fills' if not marked else 'metadata.thin'}), but the Thin "
                       f"line is not just before '{heading}' on '{holder['doc']}'; write the Thin line")
        elif line and not meta:
            out.append(f"thin mark drift on {kind} '{eid}': the Thin line is on '{holder['doc']}', "
                       "but its spine entry has no metadata.thin: true; set both or neither")
        elif any(THIN_ANY.match(ln) for ln in lines) and not line:
            out.append(f"thin mark drift on {kind} '{eid}': metadata.thin is {meta}, and the Thin "
                       f"line {'is' if line else 'is not'} just before '{heading}' on "
                       f"'{holder['doc']}'; set both or neither")
        if thin or line:
            if "ices" in spine:
                labels = {m.split(":")[0].strip("-* ").strip() for m in body or [] if ":" in m}
                missing = [x for x in ("Goal", "Limit", "Fails if") if x not in labels]
                for part in ("## Context", "## Expectation"):
                    _a, b = section(text, part)
                    if not b or not any(x.strip() for x in b):
                        missing.append(part[3:])
            else:
                labels = {m.group(1) for m in (re.match(r"^\s*[-*]\s+([^:]{1,30}):", x)
                                               for x in body or []) if m}
                missing = [x for x in THIN_LABELS if x not in labels]
            if missing:
                out.append(f"thin ICE of {kind} '{eid}' lacks {', '.join(missing)} — a thin ICE "
                           "has a goal, a limit, a Fails if line, a context line and a check")
    return out


def slice_problems(root, spine_path, sid, intent):
    """(problems, warnings): problems of this run's slice; warnings for every other slice."""
    with open(spine_path, encoding="utf-8") as fh:
        spine = yaml.safe_load(fh) or {}
    entries = [s for s in spine.get("slices") or [] if isinstance(s, dict)]
    entry = next((s for s in entries if s.get("id") == sid), None)
    if entry is None:
        return [f"slice '{sid}' is not in the spine"], []
    problems, warnings = [], []
    if intent not in (entry.get("intents") or []):
        problems.append(f"slice '{sid}' does not list business intent '{intent}'")
    for e in entries:
        found = entry_problems(e) + record_problems(root, e)
        (problems if e is entry else warnings).extend(found)
    return problems, warnings


def check(root, spine_path, sid, intent, baseline, listed=()):
    report, errors = lint_errors(root, spine_path)
    with open(spine_path, encoding="utf-8") as fh:
        spine = yaml.safe_load(fh) or {}
    try:
        problems, warnings = slice_problems(root, spine_path, sid, intent)
    except (OSError, yaml.YAMLError) as exc:
        problems, warnings = [f"cannot read the slice: {exc}"], []
    entry = _entry(spine, "slices", sid) or {"id": sid}
    parts = own_parts(spine, entry)
    docs, names = own_names(spine, entry, parts)
    before = set(baseline) if baseline is not None else set()
    older = []
    for e in errors:
        if is_own(e, docs, names):
            problems.append(e)
        elif baseline is not None and e in before:
            older.append(e)
        else:
            problems.append(f"new problem: {e}" if baseline is not None else e)
    problems += thin_problems(root, spine, parts, listed)
    return {"valid": not problems, "lint": report, "problems": problems,
            "older_problems": older, "warnings": warnings}


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv[:1] == ["baseline"]:
        ap = argparse.ArgumentParser(description="Take the model check once before the first write.")
        ap.add_argument("--root", required=True)
        ap.add_argument("--spine", required=True)
        ap.add_argument("--out", required=True)
        args = ap.parse_args(argv[1:])
        if not os.path.isfile(args.spine):
            sys.stderr.write(f"slice_check.py: spine not found: {args.spine}\n")
            return 2
        report, errors = lint_errors(args.root, args.spine)
        result = {"errors": errors, "warnings": report.get("warnings") or []}
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2)
        print(json.dumps({"errors": len(errors)}, indent=2))
        return 0
    ap = argparse.ArgumentParser(description="Check the model after the slice is written.")
    ap.add_argument("--root", required=True)
    ap.add_argument("--spine", required=True)
    ap.add_argument("--slice-id", required=True)
    ap.add_argument("--intent", required=True)
    ap.add_argument("--baseline", help="lint-before-run.json from `baseline`")
    ap.add_argument("--fills", help="fills.json: a part in its `thin` list counts as thin")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    if not os.path.isfile(args.spine):
        sys.stderr.write(f"slice_check.py: spine not found: {args.spine}\n")
        return 2
    baseline = None
    if args.baseline:
        try:
            with open(args.baseline, encoding="utf-8") as fh:
                baseline = list(json.load(fh).get("errors") or [])
        except (OSError, json.JSONDecodeError, AttributeError) as exc:
            sys.stderr.write(f"slice_check.py: cannot read the baseline {args.baseline}: {exc}\n")
            return 2
    listed = ()
    if args.fills:
        try:
            with open(args.fills, encoding="utf-8") as fh:
                listed = tuple((json.load(fh) or {}).get("thin") or ())
        except (OSError, json.JSONDecodeError, AttributeError) as exc:
            sys.stderr.write(f"slice_check.py: cannot read the fills {args.fills}: {exc}\n")
            return 2
    result = check(args.root, args.spine, args.slice_id, args.intent, baseline, listed)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)
    print(json.dumps({"valid": result["valid"],
                      "lint_errors": len(result["lint"].get("errors") or []),
                      "problems": result["problems"], "older_problems": len(result["older_problems"]),
                      "warnings": result["warnings"]}, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
