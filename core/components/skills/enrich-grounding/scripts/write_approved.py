#!/usr/bin/env python3
"""
write_approved.py — write product-model pages from text a person approved, word for word
(enrich-grounding, #1031).

A person reviews a page's text before it reaches the model: a domain, capability or feature
page, or an ICE page (ontology v15: an ICE has its own page, `ice.md`, beside its part's page,
with three sections, Intent, Context and Expectation). This script copies each approved text to
its page exactly as it is. It decides nothing and composes nothing.

    python3 write_approved.py --request <working>/approved-request.json \
        --product-base <product_base> --out <working>/approved-report.json

approved-request.json:
    {"by": "<the play or run that asks>",
     "approved_by": "<the person who approved the text>",
     "source": "<where the approval is recorded>",
     "pages": [
       {"page": "<domain>/<capability>/<feature>/feature.md", "from": "<path to the approved text>"},
       {"page": "<domain>/<capability>/<feature>/ice.md", "from": "<path to the approved text>"}]}

- `page` is a path inside `<product_base>product-os/`, named domain.md, capability.md,
  feature.md or ice.md. An intent page is author-intent-page's; the spine is never a page.
- A capability page starts "# Capability:", a feature page "# Feature:". A part's page holds no
  ICE section ("## Agent intent (ICE)"): the ICE has its own page.
- An ICE page has "## Intent", "## Context" and "## Expectation", in that order, none empty. Its
  folder holds its part's page (capability.md or feature.md), on disk or in the same request.
- No text holds a Thin line, and no page that carries one on disk is replaced: the thin mark is
  link-model-part's.
- `approved_by` names the person. No page is named twice.

Every check runs before the first write; any failure refuses the whole request (exit 2) and
writes nothing. When a write fails part way, every page already written is put back as it was,
and a page that was new is removed (exit 2). Every page is written through
safe_write.atomic_write. Reads and writes files on disk only; no git, no network.
Exit 0 written, 2 refused or bad input.
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import safe_write  # noqa: E402  (stamped beside this script)

PAGES = {"domain.md", "capability.md", "feature.md", "ice.md"}
TITLES = {"capability.md": "# Capability:", "feature.md": "# Feature:"}
PART_PAGES = ("capability.md", "feature.md")
ICE_PARTS = ("Intent", "Context", "Expectation")
INLINE_ICE = "## Agent intent (ICE)"
THIN = re.compile(r"^\s*(?:>\s*)?\**Thin(?: ICE)?\**\s*:", re.I)


class Refused(Exception):
    pass


def inside(root, rel):
    if not isinstance(rel, str) or not rel or os.path.isabs(rel) or ".." in rel.split("/"):
        raise Refused(f"the path {rel!r} leaves the model folder")
    full = os.path.realpath(os.path.join(root, rel))
    if not full.startswith(os.path.realpath(root) + os.sep):
        raise Refused(f"the path {rel!r} leaves the model folder")
    return full


def sections(text):
    """[(heading, body)] for each '## ' heading outside a code fence, in order."""
    out, cur, fence = [], None, False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            fence = not fence
        if not fence and line.startswith("## "):
            cur = [line[3:].strip(), []]
            out.append(cur)
        elif cur is not None:
            cur[1].append(line)
    return [(h, "\n".join(b)) for h, b in out]


def check_text(rel, name, text):
    if not text.strip():
        raise Refused(f"{rel}: the approved text is empty")
    if any(THIN.match(ln) for ln in text.splitlines()):
        raise Refused(f"{rel}: the approved text holds a Thin line; the thin mark is link-model-part's")
    if name in TITLES and not text.lstrip().startswith(TITLES[name]):
        raise Refused(f"{rel}: a {name[:-3]} page starts with {TITLES[name]!r}")
    if name != "ice.md" and any(ln.strip() == INLINE_ICE for ln in text.splitlines()):
        raise Refused(f"{rel}: a part's page holds no ICE section; the ICE has its own page, ice.md")
    if name == "ice.md":
        found = sections(text)
        heads = [h for h, _ in found]
        missing = [p for p in ICE_PARTS if p not in heads]
        if missing:
            raise Refused(f"{rel}: an ICE page has Intent, Context and Expectation; it lacks {', '.join(missing)}")
        if [h for h in heads if h in ICE_PARTS] != list(ICE_PARTS):
            raise Refused(f"{rel}: an ICE page has Intent, Context and Expectation, in that order")
        for h, body in found:
            if h in ICE_PARTS and not body.strip():
                raise Refused(f"{rel}: its {h} section is empty")


def plan(root, request):
    if not isinstance(request, dict):
        raise Refused("the request is not a JSON object")
    if not isinstance(request.get("approved_by"), str) or not request["approved_by"].strip():
        raise Refused("`approved_by` must name the person who approved the text")
    pages = request.get("pages")
    if not isinstance(pages, list) or not pages or not all(isinstance(p, dict) for p in pages):
        raise Refused("`pages` must be a non-empty list of objects")
    writes, seen = [], set()
    for p in pages:
        rel = p.get("page")
        full = inside(root, rel)
        name = os.path.basename(rel)
        if name not in PAGES:
            raise Refused(f"{rel}: only a domain, capability, feature or ICE page is written here")
        if rel.split("/")[0] == "intents":
            raise Refused(f"{rel}: an intent page is author-intent-page's")
        if full in seen:
            raise Refused(f"{rel} is named twice")
        seen.add(full)
        src = p.get("from")
        if not isinstance(src, str) or not os.path.isfile(src):
            raise Refused(f"{rel}: the approved text {src!r} is not a file")
        with open(src, encoding="utf-8") as fh:
            text = fh.read()
        check_text(rel, name, text)
        if os.path.isfile(full):
            with open(full, encoding="utf-8") as fh:
                if any(THIN.match(ln) for ln in fh.read().splitlines()):
                    raise Refused(f"{rel}: the page on disk is thin; its thin mark is link-model-part's, "
                                  f"so it is not replaced here")
        writes.append((full, rel, name, text))
    for full, rel, name, _ in writes:
        if name != "ice.md":
            continue
        folder = os.path.dirname(full)
        part = [n for n in PART_PAGES
                if os.path.isfile(os.path.join(folder, n)) or os.path.join(folder, n) in seen]
        if not part:
            raise Refused(f"{rel}: its folder holds no capability or feature page; an ICE sits beside its part")
    return writes


def write_all(writes):
    """Write every page; when one write fails, put back each page already written and raise."""
    done = []
    try:
        for full, _rel, _name, text in writes:
            old = None
            if os.path.exists(full):
                with open(full, encoding="utf-8") as fh:
                    old = fh.read()
            safe_write.atomic_write(full, text)
            done.append((full, old))
    except OSError:
        for full, old in reversed(done):
            if old is None:
                os.remove(full)
            else:
                safe_write.atomic_write(full, old)
        raise


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
        writes = plan(root, request)
        actions = [(rel, "replaced" if os.path.exists(full) else "created") for full, rel, _, _ in writes]
    except (Refused, OSError, ValueError, json.JSONDecodeError, UnicodeDecodeError) as e:
        sys.stderr.write(f"write_approved.py: refused, nothing written: {e}\n")
        return 2
    try:
        write_all(writes)
    except OSError as e:
        sys.stderr.write(f"write_approved.py: a write failed, every page is back as it was: {e}\n")
        return 2
    report = {"written": [{"page": rel, "action": act} for rel, act in actions],
              "approved_by": request["approved_by"], "source": request.get("source", ""),
              "by": request.get("by", "")}
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print(json.dumps(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
