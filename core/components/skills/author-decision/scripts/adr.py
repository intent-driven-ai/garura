#!/usr/bin/env python3
"""adr.py — the mechanical half of managing decision records (ADRs) (#632).

Template: `standards/templates/adr.md` — one set of core fields, two shapes: Markdown for
Garura's ADRs (`docs/adr/NNN-<slug>.md`), YAML for product decisions (`decision.yaml`, with the #632 fields).
Judgment — what a decision really supersedes or changes, and the draft itself — belongs to
the `adr-keeper` agent and the `author-decision` skill. This script only counts, parses, checks
and writes the one field an accepted ADR may gain. No git, no network, no LLM.

    adr.py number   --dir docs/adr                         next free ADR number
    adr.py lint     --adr <NNN-x.md | decision.yaml>       check a record against the template
    adr.py index    --dir docs/adr [--out docs/adr/_index.md]   the ADR index (number, title, status, date)
    adr.py overlaps --adr <new> --dir docs/adr             older ADRs it may supersede or amend (candidates)
    adr.py pointer  --older <file> --newer <file> --kind amended|superseded [--what "<part>"]
    adr.py guard    --adr <file> [--intents-dir <product-os>/intents]
    adr.py accept   --adr <file> --by "<person>" --date <date>   proposed -> accepted, on a person's word

Exit codes: 0 ok · 2 problems found (lint, guard) or refused (pointer) · 3 unreadable input ·
4 guard: the ADR would change a person's business intent — it goes to the person, never applied.
"""
import argparse
import json
import os
import re
import sys

import yaml

STATUSES = {"proposed", "accepted", "superseded", "rejected"}
LEVELS = {"framework", "product", "capability", "feature"}
BI_CHECKS = {"none", "kind", "instance"}
MD_HEADERS = ["Status", "Date", "Level", "Decided in", "Affects", "ICE impact", "Business intent check"]
MD_SECTIONS = ["Context", "Decision", "Consequences", "Alternatives Considered"]
ACCEPTER_SECTION = "For the Person Who Accepts This"   # optional (#920); each point has five parts
ACCEPTER_MD = ["What and where", "What is wrong, or worth knowing", "Why it matters",
               "What this decision does", "What you decide"]
ACCEPTER_YAML = ["point", "what_and_where", "detail", "why_it_matters", "this_decision_does", "you_decide"]
YAML_REQUIRED = ["id", "title", "status", "level", "reason", "alternatives", "affects",
                 "ice_impact", "business_intent_check"]
TITLE = re.compile(r"^#\s+ADR\s+(\d{3})\s*[—:-]\s*(.+?)\s*$", re.MULTILINE)
HEADER = re.compile(r"^\*\*([A-Za-z][A-Za-z ]*):\*\*\s*(.*)$", re.MULTILINE)
NUMBER = re.compile(r"^(?:SUPERSEDED-)?(\d{3})-.+\.md$")
ADR_REF = re.compile(r"\bADR[ -]?0*(\d{1,3})\b")
STOP = set("the a an and or of to in on for is are be it this that with by as from at not no "
           "its their our we they all any each one new old play plays".split())


class Bad(Exception):
    """Unreadable input."""


def read(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except (OSError, UnicodeDecodeError) as exc:
        raise Bad(f"cannot read {path}: {exc.__class__.__name__}") from exc


def is_yaml(path):
    return path.endswith((".yaml", ".yml"))


def parse_md(text):
    """Title, number, header fields (case-insensitive keys), and ordered H2 section names."""
    m = TITLE.search(text)
    head = text.split("\n## ", 1)[0]
    fields = {k.strip().lower(): v.strip() for k, v in HEADER.findall(head)}
    # "**Decided by:** x · **Decided in:** y" — split a combined line
    for k, v in list(fields.items()):
        for extra_k, extra_v in re.findall(r"\*\*([A-Za-z][A-Za-z ]*):\*\*\s*([^·]*)", v):
            fields[extra_k.strip().lower()] = extra_v.strip()
        fields[k] = v.split(" · **")[0].strip()
    sections = re.findall(r"^## (.+?)\s*$", text, re.MULTILINE)
    return {"number": m.group(1) if m else None, "title": m.group(2) if m else None,
            "fields": fields, "sections": [s.split("(")[0].strip() for s in sections]}


def load_decision(path):
    try:
        data = yaml.safe_load(read(path)) or {}
    except yaml.YAMLError as exc:
        raise Bad(f"{path} is not valid YAML") from exc
    d = data.get("decision") if isinstance(data, dict) else None
    if not isinstance(d, dict):
        raise Bad(f"{path} has no `decision` mapping")
    return data, d


# ---- number / index ------------------------------------------------------------------------

def numbers(adr_dir):
    out = {}
    for name in sorted(os.listdir(adr_dir)):
        m = NUMBER.match(name)
        if m:
            out[int(m.group(1))] = name
    return out


def cmd_number(args):
    taken = numbers(args.dir)
    nxt = (max(taken) + 1) if taken else 1
    print(json.dumps({"next": f"{nxt:03d}", "taken": len(taken)}))
    return 0


def cmd_index(args):
    rows = []
    for n, name in sorted(numbers(args.dir).items()):
        p = parse_md(read(os.path.join(args.dir, name)))
        status = p["fields"].get("status", "")
        status = status.split(" — ")[0].split(" (")[0] or "(not recorded)"
        if name.startswith("SUPERSEDED-"):
            status = "Superseded"
        rows.append((f"{n:03d}", p["title"] or name, status, p["fields"].get("date", "").split(" ")[0], name))
    lines = ["# Architecture Decision Records", "",
             "Generated by `adr.py index` (#632) — do not edit by hand. Each ADR's own **Status:** line",
             "is the source of truth; ADRs written before the template (`standards/templates/adr.md`)",
             "may have no Status line.", "",
             "| ADR | Title | Status | Date |", "|-----|-------|--------|------|"]
    lines += [f"| [{n}]({name}) | {t} | {s} | {d} |" for n, t, s, d, name in rows]
    text = "\n".join(lines) + "\n"
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
    print(json.dumps({"adrs": len(rows), "out": args.out}))
    return 0


# ---- lint ----------------------------------------------------------------------------------

def lint_md(text):
    p = parse_md(text)
    problems = []
    if not p["number"]:
        problems.append("title line must read `# ADR NNN — <title>`")
    f = p["fields"]
    for h in MD_HEADERS:
        if not f.get(h.lower()):
            problems.append(f"missing header line **{h}:**")
    status = f.get("status", "").split(" ")[0].strip("—").lower()
    if f.get("status") and status not in STATUSES:
        problems.append(f"**Status:** must start with one of {sorted(STATUSES)}")
    level = f.get("level", "").split(" ")[0].lower()
    if f.get("level") and level not in LEVELS:
        problems.append(f"**Level:** must be one of {sorted(LEVELS)}")
    bi = f.get("business intent check", "").split(" ")[0].strip("—").lower()
    if f.get("business intent check") and bi not in BI_CHECKS:
        problems.append(f"**Business intent check:** must start with one of {sorted(BI_CHECKS)}")
    if status == "accepted" and not f.get("decided by"):
        problems.append("an accepted ADR names who accepted it (**Decided by:**)")
    order = [s for s in p["sections"] if s in MD_SECTIONS]
    for s in MD_SECTIONS:
        if s not in p["sections"]:
            problems.append(f"missing section ## {s}")
    if order != [s for s in MD_SECTIONS if s in order]:
        problems.append(f"sections out of order — expected {MD_SECTIONS}")
    for s in MD_SECTIONS:
        body = re.search(rf"^## {re.escape(s)}[^\n]*\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
        if body and not body.group(1).strip():
            problems.append(f"section ## {s} is empty")
    problems += lint_accepter_md(text)
    return problems


def lint_accepter_md(text):
    """The optional section for the person who accepts: each ### point carries its five parts."""
    body = re.search(rf"^## {re.escape(ACCEPTER_SECTION)}[^\n]*\n(.*?)(?=^## |\Z)", text,
                     re.MULTILINE | re.DOTALL)
    if not body:
        return []
    points = re.split(r"^### ", body.group(1), flags=re.MULTILINE)[1:]
    if not points:
        return [f"section ## {ACCEPTER_SECTION} has no ### point"]
    problems = []
    for pt in points:
        name = pt.split("\n", 1)[0].strip()
        for part in ACCEPTER_MD:
            m = re.search(rf"^- \*\*{re.escape(part)}:\*\*[ \t]*(\S.*)$", pt, re.MULTILINE)
            if not m:
                problems.append(f"point `{name}` has no **{part}:**")
    return problems


def lint_yaml(d):
    problems = []
    for k in YAML_REQUIRED:
        if d.get(k) in (None, "", []):
            problems.append(f"missing `{k}`")
    for k in ("id", "title", "status", "level", "reason", "ice_impact", "business_intent_check"):
        if d.get(k) is not None and not isinstance(d.get(k), (str, int)):
            problems.append(f"`{k}` must be a single value")
    for k in ("affects", "alternatives", "supersedes", "amends", "amended_by"):
        if d.get(k) is not None and not isinstance(d.get(k), list):
            problems.append(f"`{k}` must be a list")
    meta = d.get("metadata") if isinstance(d.get("metadata"), dict) else {}
    for k in ("date", "decided_in"):
        if not meta.get(k):
            problems.append(f"missing `metadata.{k}`")
    cons = d.get("consequences")
    if not isinstance(cons, dict) or not (cons.get("positive") or cons.get("negative")):
        problems.append("missing `consequences` (positive and/or negative)")
    if problems and any("single value" in p or "must be a list" in p for p in problems):
        return problems
    if d.get("status") and d["status"] not in STATUSES:
        problems.append(f"`status` must be one of {sorted(STATUSES)}")
    if d.get("level") and d["level"] not in LEVELS:
        problems.append(f"`level` must be one of {sorted(LEVELS)}")
    if d.get("level") in ("capability", "feature") and not d.get("node_ref"):
        problems.append("a capability or feature decision names its `node_ref`")
    if d.get("business_intent_check") and d["business_intent_check"] not in BI_CHECKS:
        problems.append(f"`business_intent_check` must be one of {sorted(BI_CHECKS)}")
    if d.get("status") == "accepted" and not meta.get("accepted_by"):
        problems.append("an accepted decision names who accepted it (`metadata.accepted_by`)")
    for a in d.get("alternatives") or []:
        if not isinstance(a, dict) or not a.get("name") or not a.get("why_not"):
            problems.append("each alternative has a `name` and a `why_not`")
            break
    fta = d.get("for_the_accepter")
    if fta is not None:
        if not isinstance(fta, list) or not fta:
            problems.append("`for_the_accepter` must be a list of points")
        else:
            for i, pt in enumerate(fta, 1):
                missing = [k for k in ACCEPTER_YAML
                           if not isinstance(pt, dict) or not str(pt.get(k) or "").strip()]
                if missing:
                    problems.append(f"`for_the_accepter` point {i} has no {', '.join(missing)}")
    return problems


def cmd_lint(args):
    if is_yaml(args.adr):
        _, d = load_decision(args.adr)
        problems = lint_yaml(d)
    else:
        problems = lint_md(read(args.adr))
    print(json.dumps({"adr": args.adr, "valid": not problems, "problems": problems}, indent=2))
    return 0 if not problems else 2


# ---- overlaps ------------------------------------------------------------------------------

def terms(text):
    paths = set(re.findall(r"`([^`\s]+\.(?:md|yaml|yml|py))`", text))
    paths |= set(re.findall(r"`(/[a-z][a-z-]+)`", text))           # play names like `/discover-domains`
    words = {w for w in re.findall(r"[a-z][a-z-]{3,}", text.lower()) if w not in STOP}
    return paths, words


def cmd_overlaps(args):
    new_text = read(args.adr)
    new = parse_md(new_text)
    named = {int(n) for n in ADR_REF.findall(new_text)} - ({int(new["number"])} if new["number"] else set())
    new_paths, new_words = terms(new_text)
    out = []
    for n, name in sorted(numbers(args.dir).items()):
        if new["number"] and n == int(new["number"]):
            continue
        old_text = read(os.path.join(args.dir, name))
        paths, words = terms(old_text)
        shared_paths = sorted(new_paths & paths)
        shared_words = new_words & words
        score = 5 * (n in named) + 2 * len(shared_paths) + len(shared_words) / 40
        if n in named or shared_paths:
            out.append({"adr": f"{n:03d}", "file": name, "named_in_new": n in named,
                        "shared_paths": shared_paths, "shared_terms": len(shared_words),
                        "score": round(score, 2)})
    out.sort(key=lambda r: -r["score"])
    print(json.dumps({"candidates": out[: args.top],
                      "note": "candidates only — the agent judges which are really superseded or amended"},
                     indent=2))
    return 0


# ---- pointer -------------------------------------------------------------------------------

def superseded_in_full_by(path):
    """Who already supersedes this record in full, or None — read-only, for pre-checks."""
    if is_yaml(path):
        _, d = load_decision(path)
        return d.get("superseded_by") if d.get("status") == "superseded" else None
    m = re.search(r"^\*\*Status:\*\*\s*Superseded by \[ADR (\d{3})\]", read(path), re.MULTILINE)
    return m.group(1) if m else None


def cmd_pointer(args):
    if is_yaml(args.older) != is_yaml(args.newer):
        print(json.dumps({"refused": "older and newer must be the same shape"}))
        return 2
    if is_yaml(args.older):
        data, d = load_decision(args.older)
        _, new = load_decision(args.newer)
        if not new.get("id"):
            print(json.dumps({"refused": "the newer decision has no id"}))
            return 2
        full = args.kind == "superseded" and (args.what or "full") == "full"
        if full:
            if d.get("status") == "superseded" and d.get("superseded_by") not in (None, new["id"]):
                print(json.dumps({"refused": f"already superseded in full by {d['superseded_by']} — "
                                             f"supersede that one instead"}))
                return 2
            d["superseded_by"] = new["id"]
            d["status"] = "superseded"
        else:
            # an amendment, or a supersede in part: the YAML shape points back through
            # amended_by, which can hold many (superseded_by is for the one full supersede)
            d["amended_by"] = sorted(set((d.get("amended_by") or []) + [new["id"]]))
        with open(args.older, "w", encoding="utf-8") as fh:
            yaml.safe_dump(data, fh, sort_keys=False, allow_unicode=True)
        print(json.dumps({"older": args.older, "set": args.kind, "by": new["id"]}))
        return 0
    old_text, new_text = read(args.older), read(args.newer)
    new = parse_md(new_text)
    if not new["number"]:
        print(json.dumps({"refused": "the newer ADR has no `# ADR NNN — ...` title"}))
        return 2
    link = f"[ADR {new['number']}]({os.path.basename(args.newer)})"
    if link in old_text:
        print(json.dumps({"older": args.older, "unchanged": "already points to it"}))
        return 0
    what = f": {args.what}" if args.what and args.what != "full" else ""
    phrase = (f"superseded by {link}{what}" if args.kind == "superseded" else
              f"amended in part by {link}{what}")
    status = re.search(r"^\*\*Status:\*\*\s*(.*)$", old_text, re.MULTILINE)
    if status and args.kind == "superseded" and status.group(1).lower().startswith("superseded by"):
        print(json.dumps({"refused": f"already {status.group(1).strip()} — supersede that one instead"}))
        return 2
    if status:
        current = status.group(1).rstrip().rstrip(".")
        if args.kind == "superseded" and (args.what or "full") == "full":
            line = f"**Status:** Superseded by {link}"
        elif " — " in current:
            line = f"**Status:** {current}; and {phrase}"
        else:
            line = f"**Status:** {current} — {phrase}"
        new_old = old_text[:status.start()] + line + old_text[status.end():]
    else:  # an ADR from before the template: add the Status line under its title, nothing else
        title = re.search(r"^# .*$", old_text, re.MULTILINE)
        if not title:
            print(json.dumps({"refused": "the older ADR has no title line"}))
            return 2
        line = f"**Status:** (not recorded) — {phrase}"
        new_old = old_text[:title.end()] + "\n\n" + line + old_text[title.end():]
    with open(args.older, "w", encoding="utf-8") as fh:
        fh.write(new_old)
    print(json.dumps({"older": args.older, "status_line": line.strip()}))
    return 0


# ---- accept ---------------------------------------------------------------------------------

def cmd_accept(args):
    """Move a proposed record to accepted and name who accepted it. Nothing else changes."""
    if not args.by.strip():
        print(json.dumps({"refused": "only a person accepts an ADR — --by names them"}))
        return 2
    if is_yaml(args.adr):
        data, d = load_decision(args.adr)
        if d.get("status") != "proposed":
            print(json.dumps({"refused": f"status is `{d.get('status')}`, not proposed"}))
            return 2
        d["status"] = "accepted"
        meta = d.setdefault("metadata", {})
        meta["accepted_by"] = args.by.strip()
        meta["date"] = args.date
        with open(args.adr, "w", encoding="utf-8") as fh:
            yaml.safe_dump(data, fh, sort_keys=False, allow_unicode=True)
    else:
        text = read(args.adr)
        f = parse_md(text)["fields"]
        if f.get("status", "").split(" ")[0].lower() != "proposed":
            print(json.dumps({"refused": f"status is `{f.get('status')}`, not Proposed"}))
            return 2
        by = args.by.strip()            # replacements are functions: a name like CORP\kapil is text
        text = re.sub(r"^\*\*Status:\*\*.*$", lambda m: "**Status:** Accepted", text, count=1, flags=re.MULTILINE)
        text = re.sub(r"^\*\*Date:\*\*.*$", lambda m: f"**Date:** {args.date}", text, count=1, flags=re.MULTILINE)
        if re.search(r"^\*\*Decided by:\*\*", text, re.MULTILINE):
            text = re.sub(r"^\*\*Decided by:\*\*[^·\n]*", lambda m: f"**Decided by:** {by} ", text, count=1,
                          flags=re.MULTILINE)
        else:
            text = re.sub(r"^(\*\*Level:\*\*.*)$", lambda m: f"{m.group(1)}\n**Decided by:** {by}", text, count=1,
                          flags=re.MULTILINE)
        with open(args.adr, "w", encoding="utf-8") as fh:
            fh.write(text)
    print(json.dumps({"adr": args.adr, "status": "accepted", "by": args.by.strip()}))
    return 0


# ---- business-intent guard -----------------------------------------------------------------

def intent_titles(intents_dir):
    out = {}
    if intents_dir and os.path.isdir(intents_dir):
        for name in sorted(os.listdir(intents_dir)):
            if name.endswith(".md"):
                m = re.search(r"^# (.+)$", read(os.path.join(intents_dir, name)), re.MULTILINE)
                out[name[:-3]] = m.group(1).strip() if m else name[:-3]
    return out


def cmd_guard(args):
    text = read(args.adr)
    if is_yaml(args.adr):
        _, d = load_decision(args.adr)
        declared = str(d.get("business_intent_check") or "").strip().lower()
        raw = d.get("affects") or []
        affects = raw if isinstance(raw, str) else " ".join(str(a) for a in raw)
    else:
        f = parse_md(text)["fields"]
        declared = f.get("business intent check", "").split(" ")[0].strip("—").lower()
        affects = f.get("affects", "")
    touched = []
    if re.search(r"product-os/intents/", affects):
        touched.append("its Affects names a business intent page (product-os/intents/)")
    for iid, title in intent_titles(args.intents_dir).items():
        if re.search(rf"\b{re.escape(iid)}\b", affects) or (len(title) > 12 and title in text):
            touched.append(f"it names the business intent `{iid}`")
    report = {"adr": args.adr, "declared": declared or None, "touches_an_intent": touched}
    if declared not in BI_CHECKS:
        report["problem"] = "no business intent check declared (none | kind | instance)"
        code = 2
    elif declared == "instance" or touched:
        report["verdict"] = ("it would change a person's business intent — ask the person; the ADR "
                             "is never applied to the intent")
        if touched and declared != "instance":
            report["problem"] = f"declared `{declared}`, but {'; '.join(touched)}"
        code = 4
    else:
        report["verdict"] = "no person's business intent changes"
        code = 0
    print(json.dumps(report, indent=2))
    return code


def main(argv=None):
    ap = argparse.ArgumentParser(description="Mechanical checks for decision records (ADRs).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("number")
    s.add_argument("--dir", required=True)
    s = sub.add_parser("lint")
    s.add_argument("--adr", required=True)
    s = sub.add_parser("index")
    s.add_argument("--dir", required=True)
    s.add_argument("--out")
    s = sub.add_parser("overlaps")
    s.add_argument("--adr", required=True)
    s.add_argument("--dir", required=True)
    s.add_argument("--top", type=int, default=10)
    s = sub.add_parser("pointer")
    s.add_argument("--older", required=True)
    s.add_argument("--newer", required=True)
    s.add_argument("--kind", required=True, choices=["amended", "superseded"])
    s.add_argument("--what")
    s = sub.add_parser("accept")
    s.add_argument("--adr", required=True)
    s.add_argument("--by", required=True)
    s.add_argument("--date", required=True)
    s = sub.add_parser("guard")
    s.add_argument("--adr", required=True)
    s.add_argument("--intents-dir")
    args = ap.parse_args(argv)
    try:
        return {"number": cmd_number, "lint": cmd_lint, "index": cmd_index, "overlaps": cmd_overlaps,
                "pointer": cmd_pointer, "guard": cmd_guard, "accept": cmd_accept}[args.cmd](args)
    except (Bad, OSError, UnicodeDecodeError, ValueError, TypeError, AttributeError, KeyError,
            yaml.YAMLError) as exc:
        print(json.dumps({"error": f"unreadable or wrong-shaped input: {exc.__class__.__name__}: {exc}"}))
        return 3


if __name__ == "__main__":
    sys.exit(main())
