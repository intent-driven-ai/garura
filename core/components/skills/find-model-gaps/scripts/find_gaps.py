#!/usr/bin/env python3
"""find_gaps.py — the countable gaps in the product model (find-model-gaps, ADR 043).

Every kind is written on its own (ADR 043), so the model holds loose nodes until they are
linked. This script finds the candidates a script can count; the agent then confirms or
clears each one and decides the links and the work.

    python3 find_gaps.py --product-base <product_base> \
        [--journeys <journeys.yaml>] [--view-texts <folder of view .txt>] --out <working>/gap-candidates.json

It reports:
- `unattributed` — capabilities with no domain, functionalities with no capability;
- `dangling` — a parent named that is not in the spine;
- `no_functionalities` — capabilities that have no functionality;
- `intents_unserved` — intent pages no capability or functionality names in `intents`;
- `serves_no_intent` — capabilities and functionalities whose `intents` is empty;
- `one_way` — a link to a business intent held on one side only: a node's `intents` names the
  intent but the intent page's Touches list does not name the node (`missing: touches`), or
  the Touches list names the node but its `intents` does not name the intent
  (`missing: intents`). A link is made only when both sides hold it;
- `domains_empty` — domains no capability names;
- `duplicates` — nodes of one kind whose titles match once normalised;
- `uncovered` — with `--journeys`, main sections no page's `## Sources` names; with
  `--view-texts`, captured views no page's quoted source words appear in.

Exit 0 written (gaps or not); 2 an input cannot be read. Standard library + PyYAML. No LLM.
"""
import argparse
import glob
import json
import os
import re
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import intent_touches  # noqa: E402  (stamped from create-play/references)

QUOTE = re.compile(r"[\"“]([^\"“”]{4,})[\"”]")
MARKS = str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-", " ": " "})
STOP = {"a", "an", "the", "and", "or", "of", "to", "for", "in", "on", "with", "its", "it", "my"}
TITLE = re.compile(r"^#\s*(?:Theme|Capability|Functionality):\s*(.+)$", re.M)


def norm(text):
    return re.sub(r"\s+", " ", str(text).translate(MARKS)).strip().lower()


def key(title):
    """A title reduced to its words, for spotting the same thing named twice."""
    words = re.findall(r"[a-z0-9]+", norm(title))
    return " ".join(sorted(w for w in words if w not in STOP))


def read(path):
    with open(path, encoding="utf-8", errors="ignore") as fh:
        return fh.read()


def sources_of(text):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == "## Sources":
            out = []
            for nxt in lines[i + 1:]:
                if nxt.startswith("## "):
                    break
                if nxt.strip():
                    out.append(nxt.strip())
            return out
    return []


def entries(spine, section):
    return [e for e in spine.get(section) or [] if isinstance(e, dict) and e.get("id")]


def one_way(model, intent_pages, groups):
    """Intent links held on one side only: the spine's `intents` against each intent page's Touches."""
    by_doc, claims = {}, set()
    for kind, group in groups:
        for e in group:
            if e.get("doc"):
                by_doc[os.path.normpath(os.path.join(model, str(e["doc"])))] = (kind, e["id"])
            claims |= {(kind, e["id"], str(i)) for i in e.get("intents") or [] if str(i).strip()}
    touched = set()
    for page in intent_pages:
        intent = os.path.splitext(os.path.basename(page))[0]
        for t in intent_touches.read(read(page)):
            node = by_doc.get(os.path.normpath(os.path.join(os.path.dirname(page), t["link"])))
            if node:
                touched.add((node[0], node[1], intent))
    pages = {os.path.splitext(os.path.basename(p))[0] for p in intent_pages}
    out = [{"kind": k, "id": i, "intent": n, "missing": "touches"}
           for k, i, n in sorted(claims - touched) if n in pages]
    out += [{"kind": k, "id": i, "intent": n, "missing": "intents"}
            for k, i, n in sorted(touched - claims)]
    return out


def find(model, journeys=None, view_texts=None):
    spine_path = os.path.join(model, "_spine.yaml")
    spine = yaml.safe_load(read(spine_path)) if os.path.isfile(spine_path) else {}
    spine = spine or {}
    doms, caps, funcs = entries(spine, "domains"), entries(spine, "capabilities"), entries(spine, "functionalities")
    dom_ids, cap_ids = {d["id"] for d in doms}, {c["id"] for c in caps}
    out = {"unattributed": [], "dangling": [], "no_functionalities": [], "intents_unserved": [],
           "serves_no_intent": [], "one_way": [], "domains_empty": [], "duplicates": [], "uncovered": []}

    for c in caps:
        if not c.get("domain"):
            out["unattributed"].append({"kind": "capability", "id": c["id"], "missing": "domain"})
        elif c["domain"] not in dom_ids:
            out["dangling"].append({"kind": "capability", "id": c["id"], "names": c["domain"], "field": "domain"})
    for f in funcs:
        if not f.get("capability"):
            out["unattributed"].append({"kind": "functionality", "id": f["id"], "missing": "capability"})
        elif f["capability"] not in cap_ids:
            out["dangling"].append({"kind": "functionality", "id": f["id"], "names": f["capability"],
                                    "field": "capability"})
    with_funcs = {f.get("capability") for f in funcs}
    out["no_functionalities"] = [{"id": c["id"]} for c in caps if c["id"] not in with_funcs]
    with_caps = {c.get("domain") for c in caps}
    out["domains_empty"] = [{"id": d["id"]} for d in doms if d["id"] not in with_caps]

    served = set()
    for kind, group in (("capability", caps), ("functionality", funcs)):
        for e in group:
            ids = [str(i) for i in e.get("intents") or [] if str(i).strip()]
            served |= set(ids)
            if not ids:
                out["serves_no_intent"].append({"kind": kind, "id": e["id"]})
    intent_pages = sorted(glob.glob(os.path.join(model, "intents", "*.md")))
    out["intents_unserved"] = [{"id": os.path.splitext(os.path.basename(p))[0]} for p in intent_pages
                               if os.path.splitext(os.path.basename(p))[0] not in served]
    out["one_way"] = one_way(model, intent_pages, (("domain", doms), ("capability", caps),
                                                   ("functionality", funcs)))

    pages = {}
    for kind, group in (("domain", doms), ("capability", caps), ("functionality", funcs)):
        for e in group:
            path = os.path.join(model, str(e.get("doc") or ""))
            text = read(path) if e.get("doc") and os.path.isfile(path) else ""
            m = TITLE.search(text)
            pages[(kind, e["id"])] = {"title": m.group(1).strip() if m else e.get("one_line") or e["id"],
                                      "sources": sources_of(text)}
    for kind, group in (("domain", doms), ("capability", caps), ("functionality", funcs)):
        seen = {}
        for e in group:
            k = key(pages[(kind, e["id"])]["title"]) or key(e["id"].replace("-", " "))
            seen.setdefault(k, []).append(e["id"])
        for k, ids in seen.items():
            if k and len(ids) > 1:
                out["duplicates"].append({"kind": kind, "ids": ids, "match": k})

    all_sources = "\n".join(line for p in pages.values() for line in p["sources"])
    if journeys:
        for sec in journeys.get("main_sections") or []:
            if norm(sec) not in norm(all_sources):
                out["uncovered"].append({"what": "main section", "name": str(sec)})
    if view_texts:
        quotes = [norm(q) for q in QUOTE.findall(all_sources)]
        for path in sorted(glob.glob(os.path.join(view_texts, "**", "view-*.txt"), recursive=True)):
            text = norm(read(path))
            if not any(q and q in text for q in quotes):
                out["uncovered"].append({"what": "view", "name": os.path.splitext(os.path.basename(path))[0]})

    out["counts"] = {k: len(v) for k, v in out.items() if isinstance(v, list)}
    out["counts"].update(domains=len(doms), capabilities=len(caps), functionalities=len(funcs),
                         intents=len(intent_pages))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Find the countable gaps in the product model.")
    ap.add_argument("--product-base", required=True)
    ap.add_argument("--journeys")
    ap.add_argument("--view-texts")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        journeys = yaml.safe_load(read(args.journeys)) if args.journeys else None
        report = find(os.path.join(args.product_base, "product-os"), journeys or None, args.view_texts)
    except (OSError, yaml.YAMLError, AttributeError) as exc:
        sys.stderr.write(f"find_gaps.py: cannot read an input: {exc}\n")
        return 2
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print(json.dumps(report["counts"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
