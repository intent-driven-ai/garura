#!/usr/bin/env python3
"""check_output.py — the static check of a loop's output against its prototype.

    python3 check_output.py --brief <run>/brief --prototype <argus.html> \
        [--prototype-text <captured text>]... --out <run>/check.json

What a script can check without judgement:

- **Intents** — each has its Outcome, Why, Asked by, Proof it is met and Sources, none blank,
  and the proof is not left open (`open`, "the loop asks …", "to be confirmed").
- **Domain** — its page names research sources: at least one web link under a Sources heading
  or field. A domain with none was not found by research.
- **Capabilities and features** — each page says where on the prototype it is seen
  (a `## Seen on the prototype` or `## Source` section, or a `**Source:**` field) with at least
  one quote, and every quote of four characters or more is on the prototype: in the prototype
  file's text, or in a captured text (`--prototype-text`, e.g. a walk's `.txt` files).

Judgement — is the domain a recognised one, is the asked-by a persona, does an intent name a
need the product offers — is the review agent's (`prompts/review.md`).

Writes `{ok, counts, findings: [{level, item, rule, detail}]}`. A `fail` makes `ok` false.
Exit 0 ok; 1 findings fail; 2 an input cannot be read. Standard library only. No git, no LLM.
"""
import argparse
import glob
import html
import json
import os
import re
import sys

INTENT_FIELDS = ("Outcome", "Why", "Asked by", "Proof it is met", "Sources")
OPEN_PROOF = re.compile(r"^\s*(open\b|tbd\b|to be (confirmed|decided)|unknown\b|n/?a\b)|the loop asks", re.I)
FIELD = re.compile(r"^\*\*(.+?):\*\*\s*(.*)$")
SOURCE_HEAD = re.compile(r"^##\s+(seen on the prototype|sources?|where it is seen)\b", re.I)
SOURCE_FIELD = re.compile(r"^\*\*(source|sources|seen on the prototype):\*\*", re.I)
QUOTE = re.compile(r"[\"“]([^\"“”]{4,})[\"”]")   # double quotes only: an apostrophe is not a quote
WEB = re.compile(r"https?://\S+")
QUOTE_MARKS = str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-", " ": " "})


def read(path):
    with open(path, encoding="utf-8", errors="ignore") as fh:
        return fh.read()


def norm(text):
    text = html.unescape(text).translate(QUOTE_MARKS)
    text = re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), text)
    return re.sub(r"\s+", " ", text).strip().lower()


def fields(md):
    """The page's **Field:** values; a field's later list lines join its value."""
    out, key = {}, None
    for line in md.splitlines():
        m = FIELD.match(line)
        if m:
            key = m.group(1).strip()
            out[key] = m.group(2).strip()
        elif key and line.startswith("- "):
            out[key] = (out[key] + "\n" + line).strip()
        elif line.strip() == "":
            continue
        else:
            key = None
    return out


def source_block(md):
    """The text of the page's source section or field, or None when it has none."""
    lines, keep, found = md.splitlines(), [], False
    for i, line in enumerate(lines):
        if SOURCE_HEAD.match(line):
            found = True
            for nxt in lines[i + 1:]:
                if nxt.startswith("## "):
                    break
                keep.append(nxt)
        elif SOURCE_FIELD.match(line):
            found = True
            keep.append(line)
            for nxt in lines[i + 1:]:
                if not nxt.startswith(("- ", "  ")):
                    break
                keep.append(nxt)
    return "\n".join(keep) if found else None


def check(brief, prototype_text):
    findings, counts = [], {"intents": 0, "domain": 0, "capabilities": 0, "features": 0,
                            "quotes": 0, "quotes_found": 0}

    def find(level, item, rule, detail):
        findings.append({"level": level, "item": item, "rule": rule, "detail": detail})

    for path in sorted(glob.glob(os.path.join(brief, "intents", "*.md"))):
        item = os.path.relpath(path, brief)
        counts["intents"] += 1
        f = fields(read(path))
        for name in INTENT_FIELDS:
            if not f.get(name, "").strip():
                find("fail", item, "intent-field", f"no {name}")
        proof = f.get("Proof it is met", "")
        if proof and OPEN_PROOF.search(proof):
            find("fail", item, "intent-proof-open", f"proof is left open: {proof[:120]}")

    for path in sorted(glob.glob(os.path.join(brief, "**", "*.md"), recursive=True)):
        name = os.path.basename(path)
        if name not in ("domain.md", "capability.md", "feature.md"):
            continue
        item = os.path.relpath(path, brief)
        md = read(path)
        block = source_block(md)
        if name == "domain.md":
            counts["domain"] += 1
            if block is None or not WEB.search(block):
                find("fail", item, "domain-research", "the domain names no research source (no web link "
                                                      "under a Sources heading or field)")
            continue
        counts["capabilities" if name == "capability.md" else "features"] += 1
        if block is None:
            find("fail", item, "source-missing", "does not say where on the prototype it is seen")
            continue
        # a line naming a knowledge shelf or a proposal quotes its terms, not the prototype
        screen_lines = [l for l in block.splitlines() if not re.search(r"\b(shelf|proposal)\b", l, re.I)]
        quotes = [q.strip() for q in QUOTE.findall("\n".join(screen_lines))]
        if not quotes and not re.search(r"\b(shelf|proposal)\b", block, re.I):
            find("fail", item, "source-no-quote", "its source quotes nothing from the prototype")
        for q in quotes:
            counts["quotes"] += 1
            if norm(q) in prototype_text:
                counts["quotes_found"] += 1
            else:
                find("fail", item, "source-quote-not-found", f"not on the prototype: \"{q[:120]}\"")
    if not counts["intents"]:
        find("fail", "intents/", "intent-none", "the brief holds no business intent")
    return {"ok": not any(f["level"] == "fail" for f in findings), "counts": counts,
            "findings": findings}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check a loop's output against its prototype.")
    ap.add_argument("--brief", required=True)
    ap.add_argument("--prototype", required=True, help="the prototype file (its text is searched)")
    ap.add_argument("--prototype-text", action="append", default=[],
                    help="a captured text of the prototype, or a folder of .txt captures (repeatable)")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        texts = []
        if os.path.isfile(args.prototype):
            texts.append(read(args.prototype))
        for extra in args.prototype_text:
            paths = ([p for ext in ("txt", "md", "yaml") for p in glob.glob(os.path.join(extra, "**", f"*.{ext}"), recursive=True)]
                     if os.path.isdir(extra) else [extra])
            texts += [read(p) for p in paths]
        if not texts:
            raise OSError("no prototype text to check quotes against")
        if not os.path.isdir(args.brief):
            raise OSError(f"no brief at {args.brief}")
    except OSError as exc:
        sys.stderr.write(f"check_output.py: {exc}\n")
        return 2
    report = check(args.brief, norm("\n".join(texts)))
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    rules = {}
    for f in report["findings"]:
        rules[f["rule"]] = rules.get(f["rule"], 0) + 1
    print(json.dumps({"ok": report["ok"], "counts": report["counts"], "findings_by_rule": rules}))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
