#!/usr/bin/env python3
"""persist_intent.py — save the Business Intents and their ICE, and link them to their Sources
(/intent, #612). Run by hand it saves the intents the person confirmed; inside a drive
(`--proposed`) it saves every drafted intent as proposed.

One run drafts two levels from one or more Sources: business intents, and under each the ICE
the sources show. Run by hand, the person confirms or drops each business intent first. Inside
a drive (`--proposed`) there is no approval stop: every drafted intent is saved as `proposed`,
and the person confirms or drops it at the drive's final review — until then its ICE is not
workable. Then this writes — the product model is the hand-off; no separate hand-off file is written:

  - `<product_base>product-os/intents/<id>.md` — one page per confirmed intent (by hand) or per
    drafted intent, stage proposed (in a drive), in plain words,
    in the shape of the ontology's example (title, outcome, why, asked by, proof it is met,
    must not, stage, confirmed by and when, sources, the capabilities built from it).
  - for each ICE built from a saved intent, a PROPOSED CAPABILITY (spine.yaml v2): an entry
    appended to `<product_base>product-os/_spine.yaml` (status proposed, detail directional, no
    domain yet — /vision attaches it — and `intents` naming the business intent), and its
    grounding doc `product-os/capabilities/<id>/capability.md` with the ICE goals inline.
  - `<snapshot_dir>/source.md` — one Source record per Source (kind, read on, snapshot, what it
    shows, given by) naming every intent it shows: the link written on BOTH sides.
  - `<working>/intent-manifest.json` — the rollup the stop condition reads.

ADDITIVE: an intent page, a capability doc or an existing spine entry is never overwritten. A
dropped intent, and the ICE built from it, are not saved. An ICE whose capability is already in
the model is skipped and reported (`ice_skipped`), never merged in. Every check runs before the
first write, so a refusal writes nothing. It refuses (exit 2) when: an input is unreadable or of
the wrong shape; both or neither of --confirmation and --proposed are given; (by hand) the
decisions are not the person's own typed replies, any drafted intent has no decision, or none
is confirmed; a saved intent misses a required property; an id is badly shaped (ids become
file names, so only lower-case letters, digits and dashes) or repeated; an ICE lacks its name,
one-line or directional paragraph; a Source has no snapshot or no "what it shows"; or an
intent page already exists. Only a person confirms (C4) — by hand here, or at a drive's final
review. No git, no network, no LLM.

    python3 persist_intent.py --draft <working>/intent-draft.yaml \
        ( --confirmation <working>/confirmation.yaml | --proposed --at <date> ) \
        --source-manifest <working>/source-manifest.json [--source-manifest <another> ...] \
        --product-base <product_base> --working <working>

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

REQUIRED = ("title", "outcome", "why", "asked_by", "proof")
ID_SHAPE = re.compile(r"^[a-z0-9][a-z0-9-]{0,79}$")   # ids become file names: no paths, no dots


class Refused(Exception):
    """A reason to write nothing, in plain words."""


SPINE = "_spine.yaml"
CAP_DOC = "capabilities/{id}/capability.md"      # relative to product-os; /vision may move it


def capability_entry(c):
    """A proposed capability for one ICE, in the spine.yaml v2 shape. No domain yet — /vision
    attaches it; `intents` names the business intent the ICE is built from (ontology v3)."""
    return {"id": str(c["id"]), "slug": str(c["id"]), "domain": "",
            "intents": [str(c["built_from"])], "status": "proposed", "detail": "directional",
            "one_line": str(c["one_line"]).strip(), "doc": CAP_DOC.format(id=c["id"]),
            "depends_on": [], "decisions": [], "personas": [], "journeys": [],
            "metadata": {"created_by": "/intent", "updated_by": "/intent", "version": 1}}


def capability_doc(c):
    """The capability's grounding doc at the directional stage, its ICE goals written inline."""
    goals = "\n".join(f"- {g}" for g in c.get("goals") or [])
    return (f"# Capability: {c['title']}\n\n## Directional intent\n"
            f"{str(c['directional_intent']).strip()}\n\nGoals:\n{goals}\n")


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
    for i in confirmed:
        for prop in REQUIRED:
            if not str(i.get(prop) or "").strip():
                raise Refused(f"the intent `{i['id']}` is missing `{prop}`")

    shows = {str(s.get("snapshot_dir")): str(s.get("shows") or "").strip()
             for s in (draft.get("sources") or []) if isinstance(s, dict)}
    for s in sources:
        if not s.get("snapshot_saved") or not s.get("snapshot_dir"):
            raise Refused(f"the Source at {s.get('snapshot_dir')} has no saved snapshot")
        if not shows.get(str(s["snapshot_dir"])):
            raise Refused(f"the Source at {s['snapshot_dir']} has no 'what it shows' — re-draft "
                          f"before saving")

    kept = {str(i["id"]) for i in confirmed}
    all_ice = [c for c in (draft.get("ice") or []) if isinstance(c, dict) and c.get("id")]
    check_ids("ICE", [str(c["id"]) for c in all_ice])
    model = os.path.join(args.product_base, "product-os")
    intents_dir = os.path.join(model, "intents")
    ice = [c for c in all_ice if str(c.get("built_from")) in kept]
    for c in ice:
        for prop in ("title", "one_line", "directional_intent"):
            if not str(c.get(prop) or "").strip():
                raise Refused(f"the ICE `{c['id']}` is missing `{prop}` — it becomes a proposed capability")
    spine_path = os.path.join(model, SPINE)
    spine = load_mapping(spine_path, "spine") if os.path.exists(spine_path) else \
        {"domains": [], "capabilities": [], "functionalities": []}
    taken = {str(e.get("id")) for e in spine.get("capabilities") or [] if isinstance(e, dict)}
    work = {"conf": conf, "decisions": decisions, "sources": sources, "shows": shows,
            "confirmed": confirmed, "ice": ice, "intents_dir": intents_dir,
            "spine": spine, "spine_path": spine_path,
            "dropped": [str(i["id"]) for i in intents if str(i["id"]) not in kept],
            "ice_dropped": [str(c["id"]) for c in all_ice if str(c.get("built_from")) not in kept],
            "paths": {str(i["id"]): os.path.join(intents_dir, f"{i['id']}.md") for i in confirmed},
            "ice_paths": {str(c["id"]): os.path.join(model, CAP_DOC.format(id=c["id"])) for c in ice},
            "source_mds": [os.path.join(s["snapshot_dir"], "source.md") for s in sources]}
    # An ICE whose capability is already in the model is skipped and reported, never merged in:
    # an existing entry or doc is never changed (C8), and one clash must not stop the rest.
    # Linking it to the intent is alignment's work.
    work["ice_skipped"] = []
    for c in list(ice):
        cid = str(c["id"])
        why = ("the spine already has this capability" if cid in taken else
               "its capability doc already exists" if os.path.exists(work["ice_paths"][cid]) else None)
        if why:
            work["ice_skipped"].append({"id": cid, "built_from": str(c.get("built_from")), "reason": why})
            ice.remove(c)
            del work["ice_paths"][cid]
    existing = [p for p in work["paths"].values() if os.path.exists(p)]
    if existing:
        raise Refused(f"{', '.join(existing)} already exist — a business intent is never overwritten")
    return work


def write_ice(w):
    """Each ICE as a proposed capability: its doc, and its entry appended to the spine."""
    if not w["ice"]:
        return
    for c in w["ice"]:
        path = w["ice_paths"][str(c["id"])]
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(capability_doc(c))
    spine = w["spine"]
    spine.setdefault("capabilities", [])
    spine["capabilities"] = list(spine["capabilities"] or []) + [capability_entry(c) for c in w["ice"]]
    os.makedirs(os.path.dirname(w["spine_path"]), exist_ok=True)
    with open(w["spine_path"], "w", encoding="utf-8") as fh:
        yaml.safe_dump(spine, fh, sort_keys=False, allow_unicode=True, width=100)


def write_intents(w):
    os.makedirs(w["intents_dir"], exist_ok=True)
    for i in w["confirmed"]:
        path = w["paths"][str(i["id"])]
        here = os.path.dirname(path)
        when = w["decisions"][str(i["id"])].get("at") or w["conf"].get("at", "")
        lines = [f"# {i['title']}", "",
                 f"**Outcome:** {i['outcome']}",
                 f"**Why:** {i['why']}",
                 f"**Asked by:** {i['asked_by']}",
                 f"**Proof it is met:** {i['proof']}"]
        if str(i.get("must_not") or "").strip():
            lines.append(f"**Must not:** {i['must_not']}")
        if w["decisions"][str(i["id"])]["decision"] == "proposed":
            lines.append("**Stage:** proposed — saved inside a drive" + (f", {when}" if when else "")
                         + "; the person confirms or drops it at the drive's final review")
        else:
            lines.append(f"**Stage:** confirmed — by {w['conf']['confirmed_by']}, {when}".rstrip(", "))
        lines.append("**Sources:**")
        for s, md in zip(w["sources"], w["source_mds"]):
            lines.append(f"- [{s.get('kind')}, read {s.get('read_on')}]({os.path.relpath(md, here)})")
        mine = [c for c in w["ice"] if str(c.get("built_from")) == str(i["id"])]
        lines.append("**ICE built from it (proposed capabilities, no domain yet):**" + ("" if mine else " none yet"))
        for c in mine:
            rel = os.path.relpath(w["ice_paths"][str(c["id"])], here)
            lines.append(f"- [{c.get('title') or c['id']}]({rel})")
        lines += ["", "**What was done:** (nothing yet)", ""]
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines))


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
    written = list(w["paths"].values()) + list(w["ice_paths"].values()) + w["source_mds"]
    in_spine = {str(e.get("id")) for e in w["spine"].get("capabilities") or [] if isinstance(e, dict)}
    return {
        "intents": [{"id": str(i["id"]), "path": w["paths"][str(i["id"])],
                     "capabilities": [w["ice_paths"][str(c["id"])] for c in w["ice"]
                                      if str(c.get("built_from")) == str(i["id"])]}
                    for i in w["confirmed"]],
        "spine": w["spine_path"] if w["ice"] else None,
        "dropped": w["dropped"],
        "ice_dropped": w["ice_dropped"],
        "ice_skipped": w["ice_skipped"],
        "stage": "proposed" if w["conf"].get("by") == "drive" else "confirmed",
        "confirmed_by": w["conf"]["confirmed_by"] or None,
        "sources": w["source_mds"],
        "decided": True,
        "sources_saved": all(s.get("snapshot_saved") for s in w["sources"]),
        "linked": all(os.path.isfile(p) for p in written)
        and all(str(c["id"]) in in_spine for c in w["ice"]),
    }


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
    args = ap.parse_args(argv)
    try:
        work = plan(args)
    except Refused as why:
        sys.stderr.write(f"persist_intent.py: {why}\n")
        return 2
    write_ice(work)
    write_intents(work)
    write_sources(work)
    manifest = manifest_for(work)
    with open(os.path.join(args.working, "intent-manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
    print(json.dumps(manifest, indent=2))
    return 0 if manifest["linked"] else 2


if __name__ == "__main__":
    sys.exit(main())
