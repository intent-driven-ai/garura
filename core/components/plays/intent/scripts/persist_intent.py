#!/usr/bin/env python3
"""persist_intent.py — save the Business Intents and link them to their Sources (/intent, #612;
ADR 043). Run by hand it saves the intents the person confirmed; inside a drive (`--proposed`) it
saves every drafted intent as proposed.

/intent writes business intents only (ADR 043): no ICE, no capability, no domain. Run by hand,
the person confirms or drops each business intent first. Inside a drive (`--proposed`) there is
no approval stop: every drafted intent is saved as `proposed`, and the person confirms or drops
it at the drive's final review. Then this writes — the product model is the hand-off; no
separate hand-off file is written:

  - `<product_base>product-os/intents/<id>.md` — one page per confirmed intent (by hand) or per
    drafted intent, stage proposed (in a drive), in plain words, in the shape of the ontology's
    example (title, outcome, why, asked by, proof it is met, must not, stage, confirmed by and
    when, sources). Its Touches list is written later, by the plays that link a part to the
    intent; on a later round a Touches list already on the page is kept.
  - `<snapshot_dir>/source.md` — one Source record per Source (kind, read on, snapshot, what it
    shows, given by) naming every intent it shows: the link written on BOTH sides.
  - `<working>/intent-manifest.json` — the rollup the stop condition reads.

ADDITIVE: an intent page is never overwritten (except, on a later round of the same drive, a page
it saved and that is still proposed). A dropped intent is not saved. Every check runs before the
first write, so a refusal writes nothing. It refuses (exit 2) when: an input is unreadable or of
the wrong shape; both or neither of --confirmation and --proposed are given; (by hand) the
decisions are not the person's own typed replies, any drafted intent has no decision, or none
is confirmed; a saved intent misses a required property; an id is badly shaped (ids become
file names, so only lower-case letters, digits and dashes) or repeated; the draft carries ICE,
domains, capabilities or functionalities (another play writes those kinds); a Source has no
snapshot or no "what it shows"; or an intent page already exists. Only a person confirms (C4) —
by hand here, or at a drive's final review. No git, no network, no LLM.

Inside a drive (C16): a required property the draft leaves empty is saved as **open** when the
draft names a question for it (the drive asks it) — never why, asked by or proof, which the play
drafts itself with their basis (C17); `--drive-run-id` stamps the drive on each
page; `--open-out` writes the open questions for the drive; and on a later round
`--update-proposed` rewrites only pages still proposed that this same drive saved.

    python3 persist_intent.py --draft <working>/intent-draft.yaml \
        ( --confirmation <working>/confirmation.yaml | --proposed --at <date> ) \
        --source-manifest <working>/source-manifest.json [--source-manifest <another> ...] \
        --product-base <product_base> --working <working> \
        [--drive-run-id <id> --open-out <review_dir>/open-intent.json [--update-proposed]]

confirmation.yaml:
    confirmation:
      by: person
      confirmed_by: <git user>
      at: <date>
      decisions:
        - { intent: <id>, decision: confirmed | dropped, reply: <their exact words> }
"""
import argparse
import json
import os
import re
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import intent_touches as touches  # noqa: E402

REQUIRED = ("title", "outcome", "why", "asked_by", "proof")
DRAFTED = ("why", "asked_by", "proof")   # the play drafts these itself, with their basis (C17)
ID_SHAPE = re.compile(r"^[a-z0-9][a-z0-9-]{0,79}$")   # ids become file names: no paths, no dots


class Refused(Exception):
    """A reason to write nothing, in plain words."""


def load_mapping(path, what):
    try:
        with open(path, encoding="utf-8") as fh:
            data = yaml.safe_load(fh) if not path.endswith(".json") else json.load(fh)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        raise Refused(f"cannot read the {what} ({path}): {exc.__class__.__name__}") from exc
    if not isinstance(data, dict):
        raise Refused(f"the {what} ({path}) is not a mapping")
    return data


def check_ids(kind, ids):
    bad = [i for i in ids if not ID_SHAPE.match(i)]
    if bad:
        raise Refused(f"{kind} ids must be lower-case letters, digits and dashes: {', '.join(bad)}")
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        raise Refused(f"{kind} ids are not unique: {', '.join(dupes)}")


def read_decisions(conf, ids):
    """The person's decision per drafted intent; refuses unless every one is the person's own."""
    if conf.get("by") != "person" or not str(conf.get("confirmed_by") or "").strip():
        raise Refused("decisions must be the person's own (by: person, confirmed_by) — an agent "
                      "never confirms or drops an intent")
    decisions = {}
    for d in conf.get("decisions") or []:
        if not isinstance(d, dict):
            continue
        if d.get("decision") not in ("confirmed", "dropped"):
            raise Refused(f"decision for `{d.get('intent')}` must be confirmed or dropped")
        if not str(d.get("reply") or "").strip():
            raise Refused(f"decision for `{d.get('intent')}` has no typed reply from the person")
        decisions[str(d.get("intent"))] = d
    unknown = sorted(set(decisions) - set(ids))
    if unknown:
        raise Refused(f"decisions name intents the draft does not have: {', '.join(unknown)}")
    undecided = [i for i in ids if i not in decisions]
    if undecided:
        raise Refused(f"the person has not decided: {', '.join(undecided)} — every drafted "
                      f"intent is confirmed or dropped")
    return decisions


def plan(args):
    """Read and check every input; return what to write. Nothing is written here."""
    if bool(args.proposed) == bool(args.confirmation):
        raise Refused("pass exactly one of --confirmation (run by hand: the person's decisions) "
                      "or --proposed (inside a drive)")
    for p in [args.draft] + ([] if args.proposed else [args.confirmation]) + args.source_manifest:
        if not os.path.isfile(p):
            raise Refused(f"missing input {p}")
    draft = load_mapping(args.draft, "draft")
    if args.proposed:
        conf = {"by": "drive", "confirmed_by": "", "at": args.at or ""}
    else:
        conf = load_mapping(args.confirmation, "confirmation").get("confirmation")
        if not isinstance(conf, dict):
            raise Refused("the confirmation has no `confirmation` mapping")
    sources = [load_mapping(p, "source manifest") for p in args.source_manifest]
    intents = [i for i in (draft.get("intents") or []) if isinstance(i, dict)]
    if not intents:
        raise Refused("the draft has no intents")
    ids = [str(i.get("id") or "") for i in intents]
    check_ids("business intent", ids)
    if args.proposed:   # inside a drive: no approval stop; the drive's final review confirms
        decisions = {i: {"decision": "proposed"} for i in ids}
    else:
        decisions = read_decisions(conf, ids)
    confirmed = [i for i in intents if decisions[str(i["id"])]["decision"] in ("confirmed", "proposed")]
    if not confirmed:
        raise Refused("the person confirmed no intent — nothing is saved")
    questions = [q for q in (draft.get("questions") or []) if isinstance(q, dict)]
    for i in confirmed:
        for prop in REQUIRED:
            if not str(i.get(prop) or "").strip():
                asked = [q for q in questions if str(q.get("intent")) in (str(i["id"]), "all")]
                if prop in DRAFTED:
                    raise Refused(f"the intent `{i['id']}` is missing `{prop}` — the play drafts it "
                                  f"itself, with its basis; it is never left open")
                if not (args.proposed and asked and prop != "title"):
                    raise Refused(f"the intent `{i['id']}` is missing `{prop}`" +
                                  (" — inside a drive a gap is saved only when the draft names its "
                                   "question for the drive" if args.proposed else ""))

    shows = {str(s.get("snapshot_dir")): str(s.get("shows") or "").strip()
             for s in (draft.get("sources") or []) if isinstance(s, dict)}
    for s in sources:
        if not s.get("snapshot_saved") or not s.get("snapshot_dir"):
            raise Refused(f"the Source at {s.get('snapshot_dir')} has no saved snapshot")
        if not shows.get(str(s["snapshot_dir"])):
            raise Refused(f"the Source at {s['snapshot_dir']} has no 'what it shows' — re-draft "
                          f"before saving")

    for key in ("ice", "domains", "capabilities", "functionalities"):
        if draft.get(key):
            raise Refused(f"the draft carries `{key}` — /intent writes business intents only "
                          f"(ADR 043); another play writes that kind")
    kept = {str(i["id"]) for i in confirmed}
    model = os.path.join(args.product_base, "product-os")
    intents_dir = os.path.join(model, "intents")
    work = {"conf": conf, "decisions": decisions, "sources": sources, "shows": shows,
            "confirmed": confirmed, "intents_dir": intents_dir, "model": model,
            "dropped": [str(i["id"]) for i in intents if str(i["id"]) not in kept],
            "paths": {str(i["id"]): os.path.join(intents_dir, f"{i['id']}.md") for i in confirmed},
            "source_mds": [os.path.join(s["snapshot_dir"], "source.md") for s in sources]}
    work["questions"] = questions
    work["drive_run_id"] = args.drive_run_id or ""
    work["updated"] = []
    existing = [p for p in work["paths"].values() if os.path.exists(p)]
    if existing and args.update_proposed and args.drive_run_id:
        foreign = [p for p in existing if not saved_by_this_drive(p, args.drive_run_id)]
        if foreign:
            raise Refused(f"{', '.join(foreign)} were not saved by this drive "
                          f"({args.drive_run_id}) — only an intent this drive saved is updated")
        work["updated"] = existing
    elif existing:
        raise Refused(f"{', '.join(existing)} already exist — a business intent is never overwritten")
    return work


def saved_by_this_drive(path, drive_run_id):
    """True when the page is still proposed and its stage line names this drive's run."""
    with open(path, encoding="utf-8") as fh:
        stage = next((ln for ln in fh if ln.startswith("**Stage:**")), "")
    return "proposed" in stage and f"drive {drive_run_id}" in stage


def write_intents(w):
    os.makedirs(w["intents_dir"], exist_ok=True)
    for i in w["confirmed"]:
        path = w["paths"][str(i["id"])]
        here = os.path.dirname(path)
        when = w["decisions"][str(i["id"])].get("at") or w["conf"].get("at", "")
        def prop_text(prop):
            text = str(i.get(prop) or "").strip()
            return text or "open — the drive asks this; nothing is filled in until it is answered"
        lines = [f"# {i['title']}", "",
                 f"**Outcome:** {prop_text('outcome')}",
                 f"**Why:** {prop_text('why')}",
                 f"**Asked by:** {prop_text('asked_by')}",
                 f"**Proof it is met:** {prop_text('proof')}"]
        if str(i.get("must_not") or "").strip():
            lines.append(f"**Must not:** {i['must_not']}")
        if w["decisions"][str(i["id"])]["decision"] == "proposed":
            drive = f" (drive {w['drive_run_id']})" if w.get("drive_run_id") else ""
            lines.append("**Stage:** proposed — saved inside a drive" + drive + (f", {when}" if when else "")
                         + "; the person confirms or drops it at the drive's final review")
        else:
            lines.append(f"**Stage:** confirmed — by {w['conf']['confirmed_by']}, {when}".rstrip(", "))
        lines.append("**Sources:**")
        for s, md in zip(w["sources"], w["source_mds"]):
            lines.append(f"- [{s.get('kind')}, read {s.get('read_on')}]({os.path.relpath(md, here)})")
        lines += ["", "**What was done:** (nothing yet)", ""]
        text = "\n".join(lines) + "\n"
        if os.path.isfile(path):   # a later round: keep the Touches list other plays wrote
            with open(path, encoding="utf-8") as fh:
                kept_touches = touches.read(fh.read())
            if kept_touches:
                text = touches.upsert(text, kept_touches)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)


def write_sources(w):
    for s, md in zip(w["sources"], w["source_mds"]):
        lines = ["# Source", "",
                 f"**Kind:** {s.get('kind')}",
                 f"**Read on:** {s.get('read_on')}",
                 f"**Snapshot:** {', '.join(s.get('files', []))}",
                 f"**What it shows:** {w['shows'][str(s['snapshot_dir'])]}",
                 f"**Given by:** {s.get('given_by')}",
                 "**Shows the intents:**"]
        for i in w["confirmed"]:
            lines.append(f"- [{i['title']}]({os.path.relpath(w['paths'][str(i['id'])], s['snapshot_dir'])})")
        with open(md, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")


def manifest_for(w):
    written = list(w["paths"].values()) + w["source_mds"]
    return {
        "intents": [{"id": str(i["id"]), "path": w["paths"][str(i["id"])]} for i in w["confirmed"]],
        "dropped": w["dropped"],
        "stage": "proposed" if w["conf"].get("by") == "drive" else "confirmed",
        "confirmed_by": w["conf"]["confirmed_by"] or None,
        "sources": w["source_mds"],
        "decided": True,
        "sources_saved": all(s.get("snapshot_saved") for s in w["sources"]),
        "linked": all(os.path.isfile(p) for p in written) and sources_name_every_intent(w),
    }


def sources_name_every_intent(w):
    """Both sides: each intent page names every Source, and each Source names every intent."""
    for md in w["source_mds"]:
        with open(md, encoding="utf-8") as fh:
            text = fh.read()
        for i in w["confirmed"]:
            if os.path.relpath(w["paths"][str(i["id"])], os.path.dirname(md)) not in text:
                return False
    for i in w["confirmed"]:
        with open(w["paths"][str(i["id"])], encoding="utf-8") as fh:
            text = fh.read()
        for md in w["source_mds"]:
            if os.path.relpath(md, os.path.dirname(w["paths"][str(i["id"])])) not in text:
                return False
    return True


def write_open(w, path):
    """The questions /intent hands the drive (drive contract, step 5): what each is about, the
    gaps it blocks, whether a person must answer, and its example answers."""
    titles = {str(i["id"]): str(i.get("title") or i["id"]) for i in w["confirmed"]}
    gaps = {str(i["id"]): [p for p in REQUIRED if not str(i.get(p) or "").strip()] for i in w["confirmed"]}
    out = []
    for n, q in enumerate(w["questions"], 1):
        if str(q.get("answer") or "").strip():
            continue
        iid = str(q.get("intent") or "all")
        out.append({"id": f"intent-q{n}", "ask": str(q.get("ask") or ""),
                    "about": "the whole product" if iid == "all" else titles.get(iid, iid),
                    "blocks": [f"{iid}:{g}" for g in gaps.get(iid, [])] if iid != "all" else [],
                    "for_person": bool(q.get("for_person", True)),
                    "examples": list(q.get("examples") or [])})
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"play": "intent", "questions": out}, fh, indent=2)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--draft", required=True)
    ap.add_argument("--confirmation", help="the person's decisions (run by hand)")
    ap.add_argument("--proposed", action="store_true",
                    help="inside a drive: save every drafted intent as proposed, no approval stop")
    ap.add_argument("--at", help="the date, for --proposed")
    ap.add_argument("--source-manifest", action="append", required=True)
    ap.add_argument("--product-base", required=True)
    ap.add_argument("--working", required=True)
    ap.add_argument("--drive-run-id", help="inside a drive: stamped on each page it saves")
    ap.add_argument("--update-proposed", action="store_true",
                    help="a later round of the drive: update the intents this drive saved")
    ap.add_argument("--open-out", help="inside a drive: where to write the open questions for the drive")
    args = ap.parse_args(argv)
    try:
        work = plan(args)
    except Refused as why:
        sys.stderr.write(f"persist_intent.py: {why}\n")
        return 2
    write_intents(work)
    write_sources(work)
    if args.open_out:
        write_open(work, args.open_out)
    manifest = manifest_for(work)
    manifest["updated"] = work["updated"]
    with open(os.path.join(args.working, "intent-manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
    print(json.dumps(manifest, indent=2))
    return 0 if manifest["linked"] else 2


if __name__ == "__main__":
    sys.exit(main())
