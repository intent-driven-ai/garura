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
    appended to `<product_base>product-os/_spine.yaml` (status proposed, detail directional,
    `intents` naming the business intent) and its grounding doc with the ICE in its
    `## Agent intent (ICE)` section. When the draft names the ICE's domain (ontology v4: only
    when the source, the person or the model shows it) the doc goes under that domain —
    `<domain>/<id>/capability.md` — and a domain not yet in the model is added as a light,
    directional domain entry and page (`<domain>/domain.md`); a domain already in the model
    only gains the intent in its `intents`. With no domain, or one that cannot be used, the
    doc waits in the holding folder `capabilities/<id>/capability.md` with `domain` empty —
    /vision places it — and the reason is recorded in `warnings`.
  - on each intent page, the Touches list (intent_touches.py): every capability and domain
    the intent reaches, marked `adds` (written by this run) or `changes` (already there).
  - `<snapshot_dir>/source.md` — one Source record per Source (kind, read on, snapshot, what it
    shows, given by) naming every intent it shows: the link written on BOTH sides.
  - `<working>/intent-manifest.json` — the rollup the stop condition reads.

ADDITIVE: an intent page, a capability or domain doc, or an existing spine entry is never
overwritten (the one update: an existing domain's `intents` gains the intent). A
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

Inside a drive (C16): a required property the draft leaves empty is saved as **open** when the
draft names a question for it (the drive asks it); `--drive-run-id` stamps the drive on each
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
ID_SHAPE = re.compile(r"^[a-z0-9][a-z0-9-]{0,79}$")   # ids become file names: no paths, no dots


class Refused(Exception):
    """A reason to write nothing, in plain words."""


SPINE = "_spine.yaml"
HOLDING_DOC = "capabilities/{id}/capability.md"  # relative to product-os; /vision places it
CAP_DOC = "{domain}/{id}/capability.md"
DOMAIN_DOC = "{id}/domain.md"
RESERVED = ("capabilities", "intents")           # product-os folders that are not domains


def as_list(v):
    return [x for x in (v if isinstance(v, list) else [v] if v else []) if str(x).strip()]


def capability_entry(c, domain, doc):
    """A proposed capability for one ICE, in the spine.yaml v2 shape: under `domain` when known,
    else empty — /vision places it; `intents` names the business intent its ICE is built from."""
    return {"id": str(c["id"]), "slug": str(c["id"]), "domain": domain,
            "intents": [str(c["built_from"])], "status": "proposed", "detail": "directional",
            "one_line": str(c["one_line"]).strip(), "doc": doc,
            "depends_on": [], "decisions": [], "personas": [], "journeys": [],
            "metadata": {"created_by": "/intent", "updated_by": "/intent", "version": 1}}


def capability_doc(c):
    """The capability's grounding doc at the directional stage, its ICE in the named section."""
    ice = [f"- Goal: {g}" for g in as_list(c.get("goals"))]
    ice += [f"- Limit: {x}" for x in as_list(c.get("limits"))]
    ice += [f"- Fails if: {x}" for x in as_list(c.get("fails_if"))]
    return (f"# Capability: {c['title']}\n\n## Directional intent\n"
            f"{str(c['directional_intent']).strip()}\n\n## Agent intent (ICE)\n" + "\n".join(ice) + "\n")


def domain_entry(d, intents):
    """A light (directional) domain for a domain the source, the person or the model showed."""
    return {"id": str(d["id"]), "slug": str(d["id"]), "status": "proposed", "detail": "directional",
            "one_line": str(d["one_line"]).strip(), "doc": DOMAIN_DOC.format(id=d["id"]),
            "intents": sorted(intents), "decisions": [],
            "metadata": {"created_by": "/intent", "updated_by": "/intent", "version": 1}}


def domain_doc(d):
    return f"# Theme: {d['title']}\n\n## Intent\n{str(d['intent']).strip()}\n"


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
        if not as_list(c.get("goals")):
            raise Refused(f"the ICE `{c['id']}` has no goal — its agent intent starts with what must be true")
    spine_path = os.path.join(model, SPINE)
    spine = load_mapping(spine_path, "spine") if os.path.exists(spine_path) else \
        {"domains": [], "capabilities": [], "functionalities": []}
    taken = {str(e.get("id")) for e in spine.get("capabilities") or [] if isinstance(e, dict)}
    drafted = {str(d.get("id")): d for d in (draft.get("domains") or []) if isinstance(d, dict)}
    check_ids("domain", list(drafted))
    in_model = {str(d.get("id")): d for d in spine.get("domains") or [] if isinstance(d, dict)}
    work = {"conf": conf, "decisions": decisions, "sources": sources, "shows": shows, "drafted": drafted,
            "confirmed": confirmed, "ice": ice, "intents_dir": intents_dir, "model": model,
            "spine": spine, "spine_path": spine_path, "warnings": [],
            "new_domains": {}, "old_domains": {}, "placed": {},
            "dropped": [str(i["id"]) for i in intents if str(i["id"]) not in kept],
            "ice_dropped": [str(c["id"]) for c in all_ice if str(c.get("built_from")) not in kept],
            "paths": {str(i["id"]): os.path.join(intents_dir, f"{i['id']}.md") for i in confirmed},
            "source_mds": [os.path.join(s["snapshot_dir"], "source.md") for s in sources]}
    for c in ice:
        work["placed"][str(c["id"])] = place(c, drafted, in_model, model, work)
    work["ice_paths"] = {cid: os.path.join(model, doc) for cid, (_d, doc) in work["placed"].items()}
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
            del work["placed"][cid]
    # A domain is written or linked only for the ICE that are actually saved under it.
    used = {}
    for c in ice:
        dom = work["placed"][str(c["id"])][0]
        if dom:
            used.setdefault(dom, set()).add(str(c["built_from"]))
    work["new_domains"] = {k: v for k, v in used.items() if k not in in_model}
    work["old_domains"] = {k: v for k, v in used.items() if k in in_model}
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


def place(c, drafted, in_model, model, work):
    """(domain id, doc path) for one ICE: under its domain when the draft names one that can be
    used, else the holding folder — with the reason in `warnings`. Never a refusal."""
    cid, dom = str(c["id"]), str(c.get("domain") or "").strip()
    holding = ("", HOLDING_DOC.format(id=cid))
    if not dom:
        return holding
    if dom in in_model:
        slug = str(in_model[dom].get("slug") or dom)
        return dom, CAP_DOC.format(domain=slug, id=cid)
    d = drafted.get(dom)
    why = None
    if d is None:
        why = f"its domain `{dom}` is neither in the draft's domains nor in the model"
    elif dom in RESERVED:
        why = f"`{dom}` is a folder the model keeps for itself"
    elif not all(str(d.get(k) or "").strip() for k in ("title", "one_line", "intent")):
        why = f"its domain `{dom}` lacks a title, one-line or intent"
    elif os.path.exists(os.path.join(model, DOMAIN_DOC.format(id=dom))):
        why = f"a page for domain `{dom}` exists but the spine does not list it"
    if why:
        work["warnings"].append(f"ICE `{cid}` waits in the holding folder: {why}")
        return holding
    work.setdefault("drafted_domains", {})[dom] = d
    return dom, CAP_DOC.format(domain=dom, id=cid)


def write_ice(w):
    """Each ICE as a proposed capability (doc + spine entry); new domains as light pages; the
    intents added to the domains already in the model."""
    if not w["ice"]:
        return
    spine = w["spine"]
    for dom, intents in w["new_domains"].items():
        d = w["drafted_domains"][dom]
        path = os.path.join(w["model"], DOMAIN_DOC.format(id=dom))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(domain_doc(d))
        spine["domains"] = list(spine.get("domains") or []) + [domain_entry(d, intents)]
    for e in spine.get("domains") or []:
        if isinstance(e, dict) and str(e.get("id")) in w["old_domains"]:
            have = [str(x) for x in e.get("intents") or []]
            e["intents"] = have + sorted(set(w["old_domains"][str(e["id"])]) - set(have))
    for c in w["ice"]:
        path = w["ice_paths"][str(c["id"])]
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(capability_doc(c))
    spine["capabilities"] = list(spine.get("capabilities") or []) + [
        capability_entry(c, *w["placed"][str(c["id"])]) for c in w["ice"]]
    os.makedirs(os.path.dirname(w["spine_path"]), exist_ok=True)
    with open(w["spine_path"], "w", encoding="utf-8") as fh:
        yaml.safe_dump(spine, fh, sort_keys=False, allow_unicode=True, width=100)


def domain_title(w, dom, doc):
    """The domain's name: from the draft, else its page's `# Theme:` line, else its id."""
    title = str((w["drafted"].get(dom) or {}).get("title") or "").strip()
    if not title and os.path.isfile(doc):
        with open(doc, encoding="utf-8") as fh:
            first = fh.readline().strip()
        title = first[len("# Theme:"):].strip() if first.startswith("# Theme:") else ""
    return title or dom


def touched(w, iid, page):
    """The Touches entries for one intent: its capabilities (adds) and their domains."""
    out, seen = [], set()
    docs = {str(e.get("id")): str(e.get("doc")) for e in w["spine"].get("domains") or [] if isinstance(e, dict)}
    for c in w["ice"]:
        if str(c.get("built_from")) != iid:
            continue
        dom, doc = w["placed"][str(c["id"])]
        if dom and dom not in seen:
            seen.add(dom)
            doc_d = os.path.join(w["model"], docs[dom])
            out.append(touches.entry(domain_title(w, dom, doc_d), touches.rel(page, doc_d), "domain",
                                     "adds" if dom in w["new_domains"] else "changes"))
        out.append(touches.entry(c.get("title") or c["id"], touches.rel(page, os.path.join(w["model"], doc)),
                                 "capability", "adds"))
    return out


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
        text = touches.upsert("\n".join(lines), touched(w, str(i["id"]), path))
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


def both_ways(w):
    """Every part an intent touches names the intent in the spine, and the intent page lists it."""
    by_id = {(k, str(e.get("id"))): e for k in ("domains", "capabilities")
             for e in w["spine"].get(k) or [] if isinstance(e, dict)}
    for i in w["confirmed"]:
        iid, page = str(i["id"]), w["paths"][str(i["id"])]
        with open(page, encoding="utf-8") as fh:
            listed = {e["link"] for e in touches.read(fh.read())}
        for c in w["ice"]:
            if str(c.get("built_from")) != iid:
                continue
            dom, doc = w["placed"][str(c["id"])]
            parts = [("capabilities", str(c["id"]), doc)]
            if dom:
                parts.append(("domains", dom, str(by_id.get(("domains", dom), {}).get("doc"))))
            for kind, pid, pdoc in parts:
                if iid not in [str(x) for x in by_id.get((kind, pid), {}).get("intents") or []]:
                    return False
                if touches.rel(page, os.path.join(w["model"], pdoc)) not in listed:
                    return False
    return True


def manifest_for(w):
    written = list(w["paths"].values()) + list(w["ice_paths"].values()) + w["source_mds"]
    in_spine = {str(e.get("id")) for e in w["spine"].get("capabilities") or [] if isinstance(e, dict)}
    return {
        "intents": [{"id": str(i["id"]), "path": w["paths"][str(i["id"])],
                     "capabilities": [w["ice_paths"][str(c["id"])] for c in w["ice"]
                                      if str(c.get("built_from")) == str(i["id"])]}
                    for i in w["confirmed"]],
        "spine": w["spine_path"] if w["ice"] else None,
        "domains_added": sorted(w["new_domains"]),
        "domains_linked": sorted(w["old_domains"]),
        "in_holding_folder": sorted(cid for cid, (dom, _doc) in w["placed"].items() if not dom),
        "warnings": w["warnings"],
        "dropped": w["dropped"],
        "ice_dropped": w["ice_dropped"],
        "ice_skipped": w["ice_skipped"],
        "stage": "proposed" if w["conf"].get("by") == "drive" else "confirmed",
        "confirmed_by": w["conf"]["confirmed_by"] or None,
        "sources": w["source_mds"],
        "decided": True,
        "sources_saved": all(s.get("snapshot_saved") for s in w["sources"]),
        "linked": all(os.path.isfile(p) for p in written)
        and all(str(c["id"]) in in_spine for c in w["ice"]) and both_ways(w),
    }


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
    write_ice(work)
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
