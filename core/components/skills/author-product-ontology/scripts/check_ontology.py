#!/usr/bin/env python3
"""check_ontology.py — deterministic check of the product ontology document.

Reads the ontology written in the canonical format
(memory/standards/templates/product-ontology.md) and reports whether it holds together:

  - front matter: ontology, version, updated
  - sections: Questions it must answer, Kinds, Not yet defined, Log
  - every question has an id (Qn), an "Answered by" line and a Status
    (answered | partly | not yet); a question marked "answered" may only lean on
    kinds that are defined, not on kinds still "not yet defined"
  - every defined kind has: What it is, Who reads it (person | agent | both),
    Lives at, a Properties table with at least one row, Relationships (a table or
    "None yet."), at least one Rule, and an Example
  - every relationship points at a kind that is defined or listed as not yet defined
  - every kind a question names is defined or listed as not yet defined

No git, no network, no LLM. Same file in, same answer out.

Usage:
    python3 check_ontology.py --ontology <path> [--out <report.json>]

Exit codes: 0 valid · 2 not valid · 3 unreadable.
"""
import argparse
import json
import re
import sys

REQUIRED_FIELDS = ["ontology", "version", "updated"]
REQUIRED_SECTIONS = ["Questions it must answer", "Kinds", "Not yet defined", "Log"]
READERS = {"person", "agent", "both"}
STATUSES = {"answered", "partly", "not yet"}
Q_RE = re.compile(r"^-\s+\*\*(Q\d+)\*\*\s+[—-]\s+(.+)$")


def read_text(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def front_matter(text):
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    fields = {}
    for line in text[3:end].strip().splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            fields[key.strip()] = val.strip()
    return fields, text[end + 4:]


def sections(body):
    """Split into {## heading: text}."""
    out, current, buf = {}, None, []
    for line in body.splitlines():
        if line.startswith("## "):
            if current is not None:
                out[current] = "\n".join(buf)
            current, buf = line[3:].strip(), []
        elif current is not None:
            buf.append(line)
    if current is not None:
        out[current] = "\n".join(buf)
    return out


def kinds(kinds_text):
    """Split the Kinds section into {kind name: text}."""
    out, current, buf = {}, None, []
    for line in kinds_text.splitlines():
        if line.startswith("### "):
            if current is not None:
                out[current] = "\n".join(buf)
            current, buf = line[4:].strip(), []
        elif current is not None:
            buf.append(line)
    if current is not None:
        out[current] = "\n".join(buf)
    return out


def table_rows(block, heading):
    """Data rows of the markdown table right after **heading** (blank lines allowed between).

    Returns None when the heading is missing, [] when no table follows it."""
    m = re.search(rf"\*\*{re.escape(heading)}\*\*", block)
    if not m:
        return None
    rows = []
    for line in block[m.end():].splitlines()[1:]:
        if not line.strip() and not rows:
            continue
        if not line.startswith("|"):
            break
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in cells):
            continue
        rows.append(cells)
    return rows[1:]  # drop the header row


def bullets_after(block, heading):
    """Bullets right after **heading** (blank lines allowed before the first)."""
    m = re.search(rf"\*\*{re.escape(heading)}\*\*", block)
    if not m:
        return None
    items = []
    for line in block[m.end():].splitlines()[1:]:
        if not line.strip() and not items:
            continue
        if not line.startswith("- "):
            break
        items.append(line[2:].strip())
    return items


def field(block, name):
    m = re.search(rf"^\*\*{re.escape(name)}:\*\*\s*(.+)$", block, re.M)
    return m.group(1).strip() if m else ""


def not_yet_kinds(text):
    return {m.group(1).strip() for m in re.finditer(r"^-\s+\*\*(.+?)\*\*\s+[—-]", text, re.M)}


def check(text):
    problems = []
    fm, body = front_matter(text)
    if fm is None:
        return {"valid": False, "problems": ["no front matter"], "kinds": [], "questions": []}
    for f in REQUIRED_FIELDS:
        if not fm.get(f):
            problems.append(f"front matter: missing `{f}`")
    if fm.get("version") and not fm["version"].isdigit():
        problems.append("front matter: version must be a whole number")

    secs = sections(body)
    for s in REQUIRED_SECTIONS:
        if s not in secs:
            problems.append(f"missing section: ## {s}")

    defined = kinds(secs.get("Kinds", ""))
    pending = not_yet_kinds(secs.get("Not yet defined", ""))
    known = set(defined) | pending
    for k in set(defined) & pending:
        problems.append(f"kind `{k}` is both defined and listed as not yet defined")

    for name, block in defined.items():
        if not field(block, "What it is"):
            problems.append(f"{name}: no **What it is:** line")
        reader = field(block, "Who reads it").lower()
        if reader not in READERS:
            problems.append(f"{name}: **Who reads it:** must be person, agent or both")
        if not field(block, "Lives at"):
            problems.append(f"{name}: no **Lives at:** line")
        props = table_rows(block, "Properties")
        if not props:
            problems.append(f"{name}: needs a Properties table with at least one row")
        if "**Relationships**" not in block:
            problems.append(f"{name}: no **Relationships** heading")
        else:
            rels = table_rows(block, "Relationships") or []
            if not rels and "None yet." not in block.split("**Relationships**", 1)[1].split("**", 1)[0]:
                problems.append(f"{name}: Relationships needs a table or 'None yet.'")
            for row in rels:
                other = row[1] if len(row) > 1 else ""
                if other and other not in known:
                    problems.append(f"{name}: relationship points at unknown kind `{other}` — "
                                    f"define it or list it under Not yet defined")
        rules = bullets_after(block, "Rules")
        if not rules:
            problems.append(f"{name}: needs at least one rule under **Rules**")
        ex = block.split("**Example**", 1)
        if len(ex) < 2 or not ex[1].strip():
            problems.append(f"{name}: needs an **Example**")

    questions = []
    lines = secs.get("Questions it must answer", "").splitlines()
    for i, line in enumerate(lines):
        m = Q_RE.match(line)
        if not m:
            continue
        qid = m.group(1)
        rest = "\n".join(lines[i + 1:i + 4])
        answered_by = re.search(r"\*\*Answered by:\*\*\s*(.+)", rest)
        status = re.search(r"\*\*Status:\*\*\s*(.+)", rest)
        st = status.group(1).strip().lower() if status else ""
        questions.append({"id": qid, "status": st})
        if not answered_by:
            problems.append(f"{qid}: no **Answered by:** line")
        if st not in STATUSES:
            problems.append(f"{qid}: **Status:** must be answered, partly or not yet")
        if answered_by:
            named = [k for k in known if re.search(rf"\b{re.escape(k)}\b", answered_by.group(1))]
            if not named and st != "not yet":
                problems.append(f"{qid}: **Answered by:** names no known kind")
            if st == "answered" and any(k in pending for k in named):
                problems.append(f"{qid}: marked answered but leans on a kind not yet defined")
    if not questions:
        problems.append("no questions — the ontology must say what it answers")

    return {"valid": not problems, "kinds": sorted(defined), "not_yet_defined": sorted(pending),
            "questions": questions, "problems": problems}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ontology", required=True)
    ap.add_argument("--out")
    args = ap.parse_args()
    try:
        text = read_text(args.ontology)
    except (OSError, UnicodeDecodeError) as exc:
        print(json.dumps({"error": f"{exc.__class__.__name__}: {exc}", "ontology": args.ontology}))
        return 3
    report = check(text)
    report["ontology"] = args.ontology
    out = json.dumps(report, indent=2)
    print(out)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(out + "\n")
    return 0 if report["valid"] else 2


if __name__ == "__main__":
    sys.exit(main())
