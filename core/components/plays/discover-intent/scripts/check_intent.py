#!/usr/bin/env python3
"""check_intent.py — deterministic check of a business intent draft (/discover-intent, #612; ADR 043).

Reads the draft the authoring skill wrote (`intent-draft.yaml`: `intents`, `sources`,
`coverage`, `questions`), and optionally the sources' text and the person's answers record.
/discover-intent writes business intents only (ADR 043): a draft that carries `ice`, `domains`,
`capabilities` or `features` is a problem — another play writes those kinds.
Reports, for every business intent:

  - every required property of the ontology's Business Intent kind is present and non-empty
    (title, outcome, why, asked_by, proof); must_not is optional          (C2 / F2)
  - every filled property records where it came from: `source`, `journey`, `memory`, `model`,
    `person`, or `proposed` — never empty, never `agent`; a `proposed` property (why, asked by,
    proof: the play's own draft) names its basis in `basis.<property>`   (C5 / F5, C17)
  - why, asked by and proof are never left open or asked: they are drafted, with their basis;
    a proof reads as a measurable result, not `open` / `to be confirmed`; no question asks
    for them                                                              (C17 / F17)
  - outcome, not build: title / outcome / proof copy no run of 8 or more words from the
    source, and carry no code-like text (markup, braces, file paths)    (C3 / F3)
  - plain words: no property is a bare label (fewer than 3 words), apart from asked_by (C2)

and for the draft as a whole:

  - unique, file-name-safe ids; every Source has a plain "what it shows"; with
    --source-manifest, every manifest's snapshot is summarised            (C6)
  - the coverage map: every part names an existing business intent; every intent the source
    shows is mapped from a part — nothing left out, nothing from nothing  (C12 / F12)
  - one kind: no `ice`, `domains`, `capabilities` or `features`   (C8 / F8, ADR 043)
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

# where a property may come from (C5): never the model alone
PROVENANCE = {"source", "journey", "memory", "model", "person", "proposed"}
DRAFTED = ("why", "asked_by", "proof")      # the play drafts these itself, with their basis (C17)
OPEN_TEXT = re.compile(r"^\s*(open\b|tbd\b|to be (confirmed|decided|agreed)|unknown\b|n/?a\b)|the loop asks", re.I)
ASKS_DRAFTED = re.compile(r"how (will|would|do) (we|you) know|why does (it|this) matter|who (wants|asked)", re.I)
REQUIRED = ["title", "outcome", "why", "asked_by", "proof"]
PROSE = ["title", "outcome", "why", "proof", "must_not"]
COPY_RUN = 8
MAX_EXAMPLES = 3
ID_SHAPE = re.compile(r"^[a-z0-9][a-z0-9-]{0,79}$")   # ids become file names: no paths, no dots
CODE_LIKE = re.compile(r"(<[a-zA-Z/][^>]*>|[{}]|\b\w+\(\)|(?:\.{0,2}/)?[\w.-]+/[\w./-]+\.\w{1,5}\b)")

import os  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import model_names  # noqa: E402  (stamped from create-play/references)


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
    """Outcome-not-build and plain-words checks for intent properties."""
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
        unanswered = not str(q.get("answer") or "").strip()
        if unanswered and (str(q.get("property") or "").strip() in DRAFTED
                           or ASKS_DRAFTED.search(str(q.get("ask") or ""))):
            other.append(f"[{q.get('intent') or 'all'}] question \"{q.get('ask', '')}\" asks for why, "
                         f"asked by or proof — draft it with its basis instead of asking (C17)")
            continue
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
        for p in DRAFTED:
            text = str(intent.get(p) or "").strip()
            if p in missing:
                other.append(f"[{iid}] `{p}` is empty — draft it yourself with its basis (provenance "
                             f"`proposed`); it is never left open (C17)")
            elif OPEN_TEXT.search(text):
                other.append(f"[{iid}] `{p}` is left open (\"{text[:60]}\") — draft it with its basis (C17)")
        missing = [p for p in missing if p not in DRAFTED]
        asks = len(open_q.get(str(iid), []))
        if missing or asks:
            gaps = (f"`{'`, `'.join(missing)}` missing" if missing else "") + \
                   ("; " if missing and asks else "") + (f"{asks} open question(s)" if asks else "")
            person.append(f"[{iid}] needs the person: {gaps}")
        prov = as_map(intent.get("provenance"))
        for prop in REQUIRED + ["must_not"]:
            if str(intent.get(prop) or "").strip():
                where = str(prov.get(prop) or "").strip().lower()
                if where not in PROVENANCE:
                    other.append(f"[{iid}] `{prop}` has provenance `{where or 'none'}` — it must come "
                                 f"from the source, its journeys, memory, the product model or the "
                                 f"person, or be the play's own proposal with its basis, never be "
                                 f"invented")
                elif where == "proposed" and prop not in DRAFTED:
                    other.append(f"[{iid}] `{prop}` is marked proposed — only why, asked by and proof "
                                 f"are the play's own draft; `{prop}` comes from what the source shows")
                elif where == "proposed" and not str(as_map(intent.get("basis")).get(prop) or "").strip():
                    other.append(f"[{iid}] `{prop}` is proposed with no basis — say what it rests on "
                                 f"(`basis.{prop}`)")
        for prop in ("title", "outcome", "proof"):
            plain_text(f"[{iid}] `{prop}`", str(intent.get(prop) or ""), src_words, other)
        for prop in PROSE:
            text = str(intent.get(prop) or "").strip()
            if text and len(words(text)) < 3:
                other.append(f"[{iid}] `{prop}` is a bare label (\"{text}\") — explain it in a plain sentence")


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


def check_coverage(coverage, ids, intents, other):
    """Every part of the source maps to a business intent; every intent the source shows is mapped."""
    if not coverage:
        other.append("draft has no `coverage` map — map every part of what the sources show to "
                     "the business intent it serves")
        return
    mapped = set()
    for c in coverage:
        part = str(c.get("part") or "").strip()
        target = str(c.get("intent") or "").strip()
        if not part:
            other.append("a coverage entry names no part of the source")
        elif target not in ids:
            other.append(f"part \"{part}\" maps to no business intent (`{target or 'none'}`) — nothing "
                         f"may be left out")
        else:
            mapped.add(target)
    stated = {str(i.get("id") or "").strip() for i in intents
              if str(as_map(i.get("provenance")).get("outcome") or "").strip().lower() == "person"}
    for iid in ids:
        if iid and iid not in mapped and iid not in stated:
            other.append(f"[{iid}] is mapped from no part of the source — only an intent the person "
                         f"stated may have none")


def check_one_kind(draft, other):
    """ADR 043: /discover-intent writes business intents only — never ICE, capabilities or domains."""
    for key in ("ice", "domains", "capabilities", "features"):
        if draft.get(key):
            other.append(f"the draft carries `{key}` — /discover-intent writes business intents only (ADR 043); "
                         f"another play writes that kind")


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
        return {"clean": False, "person_only": False, "intents": 0,
                "problems": ["draft has no `intents` list — at least one business intent is required"]}
    src_words = words(source_text)
    ids = [str(i.get("id") or "").strip() for i in intents]
    check_ids("business intent", ids, other)
    open_q = check_questions(entries(draft, "questions"), other)
    check_intents(intents, open_q, src_words, person, other)
    for who, qs in open_q.items():
        if who not in ids:
            person.append(f"[{who}] needs the person: {len(qs)} open question(s)")
    check_one_kind(draft, other)
    check_sources(entries(draft, "sources"), snapshot_dirs, other)
    check_coverage(entries(draft, "coverage"), ids, intents, other)
    check_answers(answers, other)
    problems = person + other
    return {"clean": not problems, "person_only": bool(person) and not other,
            "intents": len(intents), "problems": problems}


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
        model_names.check_model(draft, args.draft)
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
