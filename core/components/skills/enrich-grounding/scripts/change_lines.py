#!/usr/bin/env python3
"""
change_lines.py — change the lines a request names on product-model pages (enrich-grounding, #993).

A play or a person asks the model sub-agent (product-os-keeper) to change some lines of a page —
a domain, capability, feature or intent page — and gives the new words. This script changes
exactly those lines and keeps every other line word for word. It decides nothing about what a
part means: the request names its source (an approved design, or the person's own words).

    python3 change_lines.py --request <working>/lines-request.json --product-base <product_base> \
        --out <working>/lines-report.json

lines-request.json:
    {"by": "<the play or run that asks>",
     "source": "<an approved design, or the person's own words>",
     "pages": [
       {"page": "capabilities/cap-720/capability.md",
        "changes": [
          {"old": "- Goal: ...", "new": "- Goal: ..."},
          {"old": "- Checked by: ...", "new": null},
          {"after": "- Limit: ...", "add": "- Fails if: ..."}]}]}

A single page may also be given as top-level `page` and `changes`.

- `old` is a whole line as it is on the page (trailing spaces and its line ending aside); `new` replaces it, and
  `new: null` removes it. `after` is a whole line on the page; `add` is put on the line below it.
- Every named line must be on its page exactly once, and no line may be named twice. A change
  never writes or removes the Thin line: the thin mark is link-model-part's.
- A page is a `.md` file inside `<product_base>product-os/` that exists; never the spine.

Every check runs before the first write; any failure refuses the whole request (exit 2) and
writes nothing. When a write fails part way — a page or the report, for any reason — every page
already written is put back as it was, and any page that could not be is named (exit 2). Each
line keeps its own line ending, and an `{after, add}` whose line is already there just below its
anchor is not added again, so a rerun changes nothing. Every page is written through
safe_write.atomic_write. Reads and writes files
on disk only; no git, no network. Exit 0 written, 2 refused or bad input.
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import safe_write  # noqa: E402  (stamped beside this script)

OLD_THIN = re.compile(r"^\s*(?:>\s*)?\**Thin(?: ICE)?\**\s*:", re.I)


class Refused(Exception):
    pass


def inside(root, rel):
    if not isinstance(rel, str) or not rel or os.path.isabs(rel) or ".." in rel.split("/"):
        raise Refused(f"the path {rel!r} leaves the model folder")
    full = os.path.realpath(os.path.join(root, rel))
    if not full.startswith(os.path.realpath(root) + os.sep):
        raise Refused(f"the path {rel!r} leaves the model folder")
    return full


LINE = re.compile(r"[^\r\n]*(?:\r\n|\n|\r)|[^\r\n]+\Z")


def split_lines(text):
    """The page's lines, each with its own line ending kept ("" for a last line with none)."""
    return LINE.findall(text)


def body(line):
    return line.rstrip("\r\n")


def ending(line):
    return line[len(body(line)):]


def text_line(value, what, page):
    if not isinstance(value, str) or "\n" in value or "\r" in value or not value.strip():
        raise Refused(f"{page}: {what} must be one non-empty line, got {value!r}")
    if OLD_THIN.match(value):
        raise Refused(f"{page}: {what} is a Thin line; the thin mark is link-model-part's")
    return value.rstrip()


def find_one(lines, wanted, page):
    hits = [i for i, ln in enumerate(lines) if body(ln).rstrip() == wanted]
    if not hits:
        raise Refused(f"{page}: the line {wanted!r} is not on the page")
    if len(hits) > 1:
        raise Refused(f"{page}: the line {wanted!r} is on the page {len(hits)} times")
    return hits[0]


def read_changes(rel, lines, changes):
    """Each change checked against the page: what replaces which line, and what follows which."""
    replace, insert, report = {}, {}, []
    for change in changes:
        if not isinstance(change, dict):
            raise Refused(f"{rel}: a change must be a mapping, got {change!r}")
        if set(change) == {"old", "new"}:
            old = text_line(change["old"], "old", rel)
            new = None if change["new"] is None else text_line(change["new"], "new", rel)
            at = find_one(lines, old, rel)
            if at in replace:
                raise Refused(f"{rel}: the line {old!r} is named twice")
            replace[at] = new
            report.append({"old": old, "new": new})
        elif set(change) == {"after", "add"}:
            after = text_line(change["after"], "after", rel)
            add = text_line(change["add"], "add", rel)
            at = find_one(lines, after, rel)
            insert.setdefault(at, []).append(add)
            report.append({"after": after, "add": add})
        else:
            raise Refused(f"{rel}: a change is {{old, new}} or {{after, add}}, got {sorted(change)}")
    for at in insert:
        if at in replace and replace[at] is None:
            raise Refused(f"{rel}: a line is added after {body(lines[at])!r}, which is removed")
    return replace, insert, report


def plan_page(root, entry):
    if not isinstance(entry, dict):
        raise Refused(f"a page entry must be a mapping, got {entry!r}")
    rel = entry.get("page")
    full = inside(root, rel)
    if not rel.endswith(".md"):
        raise Refused(f"{rel}: only a page (.md) can be changed, never the spine")
    if not os.path.isfile(full):
        raise Refused(f"{rel}: the page is not on disk")
    changes = entry.get("changes")
    if not isinstance(changes, list) or not changes:
        raise Refused(f"{rel}: no changes named")
    with open(full, encoding="utf-8", newline="") as fh:
        before = fh.read()
    lines = split_lines(before)
    replace, insert, report = read_changes(rel, lines, changes)
    usual = next((ending(ln) for ln in lines if ending(ln)), "\n")
    out, added = [], 0
    for i, ln in enumerate(lines):
        end = ending(ln)
        if i in replace:
            if replace[i] is not None:
                out.append(replace[i] + end)
        else:
            out.append(ln)
        # An added line already there just below its anchor is not added again: a rerun is a no-op.
        following = {body(x).rstrip() for x in lines[i + 1:i + 1 + len(insert.get(i, []))]}
        for add in insert.get(i, []):
            if add in following:
                continue
            if end:
                out.append(add + end)
            else:  # the anchor is the last line and has no ending: it gets one, the new line none
                out[-1] += usual
                out.append(add)
            added += 1
    after_text = "".join(out)
    try:
        after_text.encode("utf-8")
    except UnicodeEncodeError as err:
        raise Refused(f"{rel}: a new line cannot be written as UTF-8 ({err.reason})")
    kept = len(lines) - len(replace)
    return full, rel, before, after_text, {"page": rel, "changes": report,
                                           "lines_before": len(lines), "lines_after": len(out),
                                           "lines_added": added, "lines_kept": kept}


def put_back(written):
    """Every page already written goes back as it was; the pages that could not are named."""
    lost = []
    for full, before in reversed(written):
        try:
            safe_write.atomic_write(full, before)
        except Exception:  # noqa: BLE001 — every page is tried, and each failure is named
            lost.append(full)
    return lost


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--request", required=True)
    ap.add_argument("--product-base", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    root = os.path.join(a.product_base, "product-os")
    try:
        with open(a.request, encoding="utf-8") as fh:
            request = json.load(fh)
        if not isinstance(request, dict):
            raise Refused("the request must be a mapping")
        if not isinstance(request.get("source"), str) or not request["source"].strip():
            raise Refused("the request names no source (an approved design, or the person's words)")
        pages = request.get("pages")
        if pages is None and "page" in request:
            pages = [{"page": request["page"], "changes": request.get("changes")}]
        if not isinstance(pages, list) or not pages:
            raise Refused("the request names no page")
        planned = [plan_page(root, p) for p in pages]
        if len({p[0] for p in planned}) != len(planned):
            raise Refused("a page is named twice; put all its changes in one entry")
        report = {"by": request.get("by"), "source": request["source"],
                  "pages": [p[4] for p in planned], "changed": [p[1] for p in planned]}
        report_text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
        report_text.encode("utf-8")
    except (Refused, OSError, ValueError) as err:
        print(f"change_lines: refused — {err}", file=sys.stderr)
        return 2
    written = []
    try:
        for full, _rel, before, after_text, _r in planned:
            if after_text != before:
                safe_write.atomic_write(full, after_text)
                written.append((full, before))
        safe_write.atomic_write(a.out, report_text)
    except Exception as err:  # noqa: BLE001 — any failure puts every page back
        lost = put_back(written)
        if lost:
            print(f"change_lines: a write failed ({err}); these pages could not be put back: "
                  f"{', '.join(lost)}", file=sys.stderr)
        else:
            print(f"change_lines: a write failed, every page put back — {err}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
