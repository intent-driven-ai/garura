#!/usr/bin/env python3
"""check_ontology_change.py — what an edit-ontology run changed in the ontology (#777).

Compares the ontology before the run with the ontology after it, and checks three things:
  scope   — only the kinds the need touches changed (C1/F1)
  version — the version is up by one, `updated` is the run's date, one new log line (C6/F6)
  names   — no real person's name appears in the changed text (C4/F4)

    python3 check_ontology_change.py --before <base copy> --after <ontology.md> \
        --allow-kind ICE [--allow-kind Capability ...] --date 2026-10-22 \
        [--forbid-name <name> ...] --out <change-check.json>

The questions, the "Not yet defined" list, the version, the date and the log may always
change. Exit 0 when all three checks pass, 1 when one fails, 2 on bad input.
"""
import argparse
import json
import re
import sys


def parse(text):
    """version, updated, kinds {name: body}, log lines."""
    fm = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    meta = {}
    if fm:
        for line in fm.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
    sections = re.split(r"^## ", text, flags=re.M)
    kinds, log = {}, []
    for sec in sections:
        title, _, body = sec.partition("\n")
        if title.strip() == "Kinds":
            for part in re.split(r"^### ", body, flags=re.M)[1:]:
                name, _, kbody = part.partition("\n")
                kinds[name.strip()] = kbody.strip()
        elif title.strip() == "Log":
            log = [ln for ln in body.splitlines() if ln.startswith("- ")]
    return meta.get("version"), meta.get("updated"), kinds, log


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--before", required=True)
    ap.add_argument("--after", required=True)
    ap.add_argument("--allow-kind", action="append", default=[])
    ap.add_argument("--date", required=True)
    ap.add_argument("--forbid-name", action="append", default=[])
    ap.add_argument("--out", required=True)
    ns = ap.parse_args(argv)
    try:
        before = open(ns.before, encoding="utf-8").read()
        after = open(ns.after, encoding="utf-8").read()
    except OSError as e:
        sys.stderr.write(f"check_ontology_change.py: {e}\n")
        sys.exit(2)

    v0, _, k0, log0 = parse(before)
    v1, d1, k1, log1 = parse(after)
    changed = sorted(n for n in set(k0) | set(k1) if k0.get(n) != k1.get(n))
    out_of_scope = [n for n in changed if n not in ns.allow_kind]
    new_log = [ln for ln in log1 if ln not in log0]
    try:
        bumped = int(v1) == int(v0) + 1
    except (TypeError, ValueError):
        bumped = False
    changed_text = "\n".join(k1.get(n, "") for n in changed) + "\n" + "\n".join(new_log)
    found = sorted({n for n in ns.forbid_name if n and re.search(rf"\b{re.escape(n)}\b", changed_text, re.I)})

    report = {
        "changed_kinds": changed, "allowed_kinds": sorted(ns.allow_kind), "out_of_scope": out_of_scope,
        "scope_ok": not out_of_scope,
        "version_before": v0, "version_after": v1, "updated": d1, "date": ns.date,
        "new_log_lines": len(new_log),
        "version_ok": bumped and d1 == ns.date and len(new_log) == 1,
        "names_found": found, "names_ok": not found,
    }
    with open(ns.out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print(json.dumps(report, indent=2))
    sys.exit(0 if report["scope_ok"] and report["version_ok"] and report["names_ok"] else 1)


if __name__ == "__main__":
    main()
