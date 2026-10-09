#!/usr/bin/env python3
"""check_intent.py — deterministic check of a two-level intent draft (/intent, #612).

Reads the draft the authoring skill wrote (`intent-draft.yaml`: `intents`, `ice`, `sources`,
`coverage`, `questions`), and optionally the sources' text and the person's answers record.
Reports, for every business intent:

  - every required property of the ontology's Business Intent kind is present and non-empty
    (title, outcome, why, asked_by, proof); must_not is optional          (C2 / F2)
  - every filled property records where it came from: `source` or `person` — never empty,
    never `agent`                                                         (C5 / F5)
  - outcome, not build: title / outcome / proof copy no run of 8 or more words from the
    source, and carry no code-like text (markup, braces, file paths)    (C3 / F3)
  - plain words: no property is a bare label (fewer than 3 words), apart from asked_by (C2)
  - it has at least one ICE built from it, unless the person stated it   (C12)

for every ICE (each becomes a proposed capability):

  - an id, a title, a one-line descriptor, a directional paragraph, and at least one goal;
    built from an existing intent                                         (C12 / F12)
  - its goals copy no run from the source, carry no code-like text, are no bare labels (C3)

and for the draft as a whole:

  - unique, file-name-safe ids; every Source has a plain "what it shows"; with
    --source-manifest, every manifest's snapshot is summarised            (C6)
  - the coverage map: every part names an existing ICE; every ICE is mapped from a part
    — nothing left out, nothing from nothing                              (C12 / F12)
  - every question carries 1–3 example answers                            (C13 / F13)
  - no question is left unanswered                                        (C5)
  - with --answers: every recorded answer lists the examples it was offered, and a reply
    that equals an offered example is marked `picked: true`; an answer the person gave
    unprompted is marked `volunteered: true` and needs no examples       (C13 / F13)

What the person must still answer is reported once per intent ("needs the person"), not once
per gap and again per question. Whether separate things were merged, or an intent restates the
source, is judgment — the agent checks it; this script checks only what can be counted.
No git, no network, no LLM. Same input, same answer.

    python3 check_intent.py --draft <working>/intent-draft.yaml \
        [--source-text <file> ...] [--source-manifest <manifest.json> ...] \
        [--answers <working>/answers.yaml] [--out <working>/intent-check.json]

The report's `person_only` is true when every problem left is something only the person can
answer. Exit 0 clean · 2 problems found · 3 unreadable input.
"""
import argparse
import json
import re
import sys

import yaml

REQUIRED = ["title", "outcome", "why", "asked_by", "proof"]
PROSE = ["title", "outcome", "why", "proof", "must_not"]
COPY_RUN = 8
MAX_EXAMPLES = 3
ID_SHAPE = re.compile(r"^[a-z0-9][a-z0-9-]{0,79}$")   # ids become file names: no paths, no dots
CODE_LIKE = re.compile(r"(<[a-zA-Z/][^>]*>|[{}]|\b\w+\(\)|(?:\.{0,2}/)?[\w.-]+/[\w./-]+\.\w{1,5}\b)")


def words(text):
    return re.findall(r"[a-z0-9']+", str(text).lower())


def copied_run(text, source_words, n=COPY_RUN):
    """The first run of n words in text that also appears in the source, else None."""
    tw = words(text)
    grams = {" ".join(source_words[i:i + n]) for i in range(len(source_words) - n + 1)}
    for i in range(len(tw) - n + 1):
        g = " ".join(tw[i:i + n])
        if g in grams:
            return g
    return None


def plain_text(label, text, src_words, other):
    """Outcome-not-build and plain-words checks shared by intent properties and ICE goals."""
    if src_words and text:
        run = copied_run(text, src_words)
        if run:
            other.append(f"{label} copies the source (\"{run}\") — state the outcome, not the source")
    if CODE_LIKE.search(text):
        other.append(f"{label} carries code-like text — write it in plain words")


def as_list(value):
    return value if isinstance(value, list) else []


def as_map(value):
    return value if isinstance(value, dict) else {}


def check_ids(kind, ids, other):
    if not all(ids):
        other.append(f"a {kind} has no `id`")
    bad = [i for i in ids if i and not ID_SHAPE.match(i)]
    if bad:
        other.append(f"{kind} ids must be lower-case letters, digits and dashes (they become file "
                     f"names): {', '.join(bad)}")
    dupes = sorted({i for i in ids if i and ids.count(i) > 1})
    if dupes:
        other.append(f"{kind} ids are not unique: {', '.join(dupes)}")


def check_questions(questions, other):
    """Open questions per intent; every question must carry example answers (C13)."""
    open_q = {}
    for q in questions:
        if not str(q.get("answer") or "").strip():
            open_q.setdefault(str(q.get("intent") or "all"), []).append(q)
        examples = [e for e in as_list(q.get("examples")) if str(e).strip()]
        if not 1 <= len(examples) <= MAX_EXAMPLES:
            other.append(f"[{q.get('intent') or 'all'}] question \"{q.get('ask', '')}\" needs 1 to "
                         f"{MAX_EXAMPLES} example answers")
    return open_q


def check_intents(intents, open_q, src_words, person, other):
    for intent in intents:
        iid = intent.get("id") or "?"
        missing = [p for p in REQUIRED if not str(intent.get(p) or "").strip()]
        asks = len(open_q.get(str(iid), []))
        if missing or asks:
            gaps = (f"`{'`, `'.join(missing)}` missing" if missing else "") + \
                   ("; " if missing and asks else "") + (f"{asks} open question(s)" if asks else "")
            person.append(f"[{iid}] needs the person: {gaps}")
        prov = as_map(intent.get("provenance"))
        for prop in REQUIRED + ["must_not"]:
            if str(intent.get(prop) or "").strip():
                where = str(prov.get(prop) or "").strip().lower()
                if where not in {"source", "person"}:
                    other.append(f"[{iid}] `{prop}` has provenance `{where or 'none'}` — it must come "
                                 f"from the source or the person, never be invented")
        for prop in ("title", "outcome", "proof"):
            plain_text(f"[{iid}] `{prop}`", str(intent.get(prop) or ""), src_words, other)
        for prop in PROSE:
            text = str(intent.get(prop) or "").strip()
            if text and len(words(text)) < 3:
                other.append(f"[{iid}] `{prop}` is a bare label (\"{text}\") — explain it in a plain sentence")


def check_ice(ice, ids, intents, src_words, other):
    served = set()
    for c in ice:
        cid = c.get("id") or "?"
        if not str(c.get("title") or "").strip():
            other.append(f"ICE [{cid}] has no title")
        for prop in ("one_line", "directional_intent"):
            text = str(c.get(prop) or "").strip()
            if not text:
                other.append(f"ICE [{cid}] has no `{prop}` — it becomes a proposed capability")
            elif len(words(text)) < 3:
                other.append(f"ICE [{cid}] `{prop}` is a bare label (\"{text}\") — explain it")
            else:
                plain_text(f"ICE [{cid}] `{prop}`", text, src_words, other)
        goals = [g for g in as_list(c.get("goals")) if str(g).strip()]
        if not goals:
            other.append(f"ICE [{cid}] has no goals")
        for g in goals:
            plain_text(f"ICE [{cid}] goal", str(g), src_words, other)
            if len(words(g)) < 3:
                other.append(f"ICE [{cid}] goal \"{g}\" is a bare label — explain it in a plain sentence")
        target = str(c.get("built_from") or "").strip()
        if target not in ids:
            other.append(f"ICE [{cid}] is built from no business intent (`{target or 'none'}`)")
        else:
            served.add(target)
    stated = {str(i.get("id") or "").strip() for i in intents
              if str(as_map(i.get("provenance")).get("outcome") or "").strip().lower() == "person"}
    for iid in ids:
        if iid and iid not in served and iid not in stated:
            other.append(f"[{iid}] has no ICE under it — an intent the source shows needs at least "
                         f"one ICE; only an intent the person stated may have none yet")


def check_sources(sources, snapshot_dirs, other):
    shown = {str(s.get("snapshot_dir") or ""): str(s.get("shows") or "").strip() for s in sources}
    if not sources:
        other.append("draft has no `sources` — say in plain words what each source shows")
    for d, shows in shown.items():
        if not shows:
            other.append(f"source `{d}` has no 'what it shows'")
    for d in snapshot_dirs:
        if d not in shown:
            other.append(f"source `{d}` is not summarised in the draft's `sources`")


def check_coverage(coverage, ice_ids, other):
    if not coverage:
        other.append("draft has no `coverage` map — map every part of what the sources show to "
                     "the ICE it serves")
        return
    mapped = set()
    for c in coverage:
        part = str(c.get("part") or "").strip()
        target = str(c.get("ice") or "").strip()
        if not part:
            other.append("a coverage entry names no part of the source")
        elif target not in ice_ids:
            other.append(f"part \"{part}\" maps to no ICE (`{target or 'none'}`) — nothing may be left out")
        else:
            mapped.add(target)
    for cid in ice_ids:
        if cid and cid not in mapped:
            other.append(f"ICE [{cid}] is mapped from no part of the source")


def check_answers(answers, other):
    for a in as_list(as_map(answers).get("answers")):
        if not isinstance(a, dict) or a.get("volunteered") is True:
            continue                     # said unprompted — no question, so no examples
        offered = [str(e).strip() for e in as_list(a.get("offered")) if str(e).strip()]
        about = a.get("about", "?")
        if not offered:
            other.append(f"answer about {about} lists no examples it was offered")
        reply = " ".join(words(a.get("reply", "")))
        if reply and any(reply == " ".join(words(e)) for e in offered) and a.get("picked") is not True:
            other.append(f"answer about {about} equals an offered example but is not marked picked")


def entries(draft, key):
    return [x for x in as_list(draft.get(key)) if isinstance(x, dict)]


def check(draft, source_text="", snapshot_dirs=(), answers=None):
    person, other = [], []
    intents = draft.get("intents") if isinstance(draft, dict) else None
    if not isinstance(intents, list) or not intents or not all(isinstance(i, dict) for i in intents):
        return {"clean": False, "person_only": False, "intents": 0, "ice": 0,
                "problems": ["draft has no `intents` list — at least one business intent is required"]}
    src_words = words(source_text)
    ids = [str(i.get("id") or "").strip() for i in intents]
    check_ids("business intent", ids, other)
    open_q = check_questions(entries(draft, "questions"), other)
    check_intents(intents, open_q, src_words, person, other)
    for who, qs in open_q.items():
        if who not in ids:
            person.append(f"[{who}] needs the person: {len(qs)} open question(s)")
    ice = entries(draft, "ice")
    ice_ids = [str(c.get("id") or "").strip() for c in ice]
    check_ids("ICE", ice_ids, other)
    check_ice(ice, ids, intents, src_words, other)
    check_sources(entries(draft, "sources"), snapshot_dirs, other)
    check_coverage(entries(draft, "coverage"), ice_ids, other)
    check_answers(answers, other)
    problems = person + other
    return {"clean": not problems, "person_only": bool(person) and not other,
            "intents": len(intents), "ice": len(ice), "problems": problems}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--draft", required=True)
    ap.add_argument("--source-text", action="append", default=[],
                    help="a source's readable text (repeatable: one per snapshot file)")
    ap.add_argument("--source-manifest", action="append", default=[],
                    help="a Source manifest whose snapshot must be summarised (repeatable)")
    ap.add_argument("--answers", help="the person's answers record (answers.yaml)")
    ap.add_argument("--out")
    args = ap.parse_args(argv)
    try:
        with open(args.draft, encoding="utf-8") as fh:
            draft = yaml.safe_load(fh) or {}
        texts = []
        for path in args.source_text:
            with open(path, encoding="utf-8", errors="replace") as fh:
                texts.append(fh.read())
        dirs = []
        for path in args.source_manifest:
            with open(path, encoding="utf-8") as fh:
                dirs.append(json.load(fh)["snapshot_dir"])
        answers = None
        if args.answers:
            with open(args.answers, encoding="utf-8") as fh:
                answers = yaml.safe_load(fh) or {}
        if not isinstance(draft, dict) or (answers is not None and not isinstance(answers, dict)):
            raise ValueError("the draft and the answers record must each be a mapping")
    except (OSError, UnicodeDecodeError, KeyError, ValueError, yaml.YAMLError) as exc:
        print(json.dumps({"error": f"{exc.__class__.__name__}: {exc}"}))
        return 3
    report = check(draft, "\n\n".join(texts), dirs, answers)
    out = json.dumps(report, indent=2)
    print(out)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(out + "\n")
    return 0 if report["clean"] else 2


if __name__ == "__main__":
    sys.exit(main())
