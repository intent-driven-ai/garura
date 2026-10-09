#!/usr/bin/env python3
"""persist_intent.py — save the confirmed Business Intents and their ICE, and link them to their
Sources (/intent, #612).

One run drafts two levels from one or more Sources: business intents, and under each the ICE
the sources show. The person confirms or drops each business intent. Only after that, this
writes — the product model is the hand-off; no separate hand-off file is written:

  - `<product_base>product-os/intents/<id>.md` — one page per CONFIRMED intent, in plain words,
    in the shape of the ontology's example (title, outcome, why, asked by, proof it is met,
    must not, stage, confirmed by and when, sources, its ICE).
  - `<product_base>product-os/ice/<id>.yaml` — one ICE per ICE built from a confirmed intent, in
    the `ice.yaml` shape: goals only, `node_ref` null (not yet placed), `built_from` its intent.
  - `<snapshot_dir>/source.md` — one Source record per Source (kind, read on, snapshot, what it
    shows, given by) naming every intent it shows: the link written on BOTH sides.
  - `<working>/intent-manifest.json` — the rollup the stop condition reads.

ADDITIVE: refuses if any intent page or ICE file already exists. A dropped intent, and the ICE
built from it, are not saved. It refuses (exit 2) and writes nothing when: the decisions are
not the person's own typed replies; any drafted intent has no decision; no intent is
confirmed; a confirmed intent misses a required property; a Source has no snapshot; or an
intent page already exists. Only a person confirms (C4). No git, no network, no LLM.

    python3 persist_intent.py --draft <working>/intent-draft.yaml \
        --confirmation <working>/confirmation.yaml \
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
import sys

import yaml

REQUIRED = ("title", "outcome", "why", "asked_by", "proof")


def ice_record(c, created_at):
    """One ICE in the ice.yaml shape, goals only and not yet placed (ontology v3)."""
    return {"schema": {"name": "ice", "version": 1},
            "ice": {"id": str(c["id"]), "title": str(c.get("title") or ""), "node_ref": None,
                    "built_from": [str(c["built_from"])],
                    "intent": {"goals": [str(g) for g in c.get("goals") or []],
                               "constraints": [], "failures": []},
                    "context": {"persona": [], "systems": [], "scope": []},
                    "expectations": {"outcomes": []},
                    "metadata": {"created_by": "/intent", "updated_by": "/intent",
                                 "created_at": created_at, "version": 1}}}


def load_yaml(path):
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--draft", required=True)
    ap.add_argument("--confirmation", required=True)
    ap.add_argument("--source-manifest", action="append", required=True)
    ap.add_argument("--product-base", required=True)
    ap.add_argument("--working", required=True)
    args = ap.parse_args(argv)

    def refuse(msg):
        sys.stderr.write(f"persist_intent.py: {msg}\n")
        return 2

    for p in [args.draft, args.confirmation] + args.source_manifest:
        if not os.path.isfile(p):
            return refuse(f"missing input {p}")
    draft = load_yaml(args.draft)
    intents = [i for i in (draft.get("intents") or []) if isinstance(i, dict)]
    shows = {str(s.get("snapshot_dir")): str(s.get("shows") or "").strip()
             for s in (draft.get("sources") or []) if isinstance(s, dict)}
    conf = load_yaml(args.confirmation).get("confirmation") or {}
    sources = []
    for p in args.source_manifest:
        with open(p, encoding="utf-8") as fh:
            sources.append(json.load(fh))

    if not intents:
        return refuse("the draft has no intents")
    if conf.get("by") != "person" or not str(conf.get("confirmed_by") or "").strip():
        return refuse("decisions must be the person's own (by: person, confirmed_by) — an agent "
                      "never confirms or drops an intent")
    decisions = {}
    for d in conf.get("decisions") or []:
        if not isinstance(d, dict):
            continue
        if d.get("decision") not in ("confirmed", "dropped"):
            return refuse(f"decision for `{d.get('intent')}` must be confirmed or dropped")
        if not str(d.get("reply") or "").strip():
            return refuse(f"decision for `{d.get('intent')}` has no typed reply from the person")
        decisions[str(d.get("intent"))] = d
    ids = [str(i.get("id") or "") for i in intents]
    unknown = sorted(set(decisions) - set(ids))
    if unknown:
        return refuse(f"decisions name intents the draft does not have: {', '.join(unknown)}")
    undecided = [i for i in ids if i not in decisions]
    if undecided:
        return refuse(f"the person has not decided: {', '.join(undecided)} — every drafted "
                      f"intent is confirmed or dropped")
    confirmed = [i for i in intents if decisions[str(i["id"])]["decision"] == "confirmed"]
    dropped = [str(i["id"]) for i in intents if decisions[str(i["id"])]["decision"] == "dropped"]
    if not confirmed:
        return refuse("the person confirmed no intent — nothing is saved")
    for i in confirmed:
        for prop in REQUIRED:
            if not str(i.get(prop) or "").strip():
                return refuse(f"the intent `{i['id']}` is missing `{prop}`")
    for s in sources:
        if not s.get("snapshot_saved"):
            return refuse(f"the Source at {s.get('snapshot_dir')} has no saved snapshot")

    intents_dir = os.path.join(args.product_base, "product-os", "intents")
    ice_dir = os.path.join(args.product_base, "product-os", "ice")
    paths = {str(i["id"]): os.path.join(intents_dir, f"{i['id']}.md") for i in confirmed}
    kept = {str(i["id"]) for i in confirmed}
    all_ice = [c for c in (draft.get("ice") or []) if isinstance(c, dict) and c.get("id")]
    ice = [c for c in all_ice if str(c.get("built_from")) in kept]
    ice_dropped = [str(c["id"]) for c in all_ice if str(c.get("built_from")) not in kept]
    ice_paths = {str(c["id"]): os.path.join(ice_dir, f"{c['id']}.yaml") for c in ice}
    existing = [p for p in list(paths.values()) + list(ice_paths.values()) if os.path.exists(p)]
    if existing:
        return refuse(f"{', '.join(existing)} already exist — an intent or an ICE is never overwritten")
    os.makedirs(intents_dir, exist_ok=True)
    if ice:
        os.makedirs(ice_dir, exist_ok=True)
    when_all = conf.get("at", "")
    for c in ice:
        with open(ice_paths[str(c["id"])], "w", encoding="utf-8") as fh:
            yaml.safe_dump(ice_record(c, when_all), fh, sort_keys=False, allow_unicode=True)

    source_mds = [os.path.join(s["snapshot_dir"], "source.md") for s in sources]
    for i in confirmed:
        path = paths[str(i["id"])]
        when = decisions[str(i["id"])].get("at") or conf.get("at", "")
        lines = [f"# {i['title']}", "",
                 f"**Outcome:** {i['outcome']}",
                 f"**Why:** {i['why']}",
                 f"**Asked by:** {i['asked_by']}",
                 f"**Proof it is met:** {i['proof']}"]
        if str(i.get("must_not") or "").strip():
            lines.append(f"**Must not:** {i['must_not']}")
        lines.append(f"**Stage:** confirmed — by {conf['confirmed_by']}, {when}".rstrip(", "))
        lines.append("**Sources:**")
        for s, md in zip(sources, source_mds):
            lines.append(f"- [{s.get('kind')}, read {s.get('read_on')}]"
                         f"({os.path.relpath(md, os.path.dirname(path))})")
        mine = [c for c in ice if str(c.get("built_from")) == str(i["id"])]
        lines.append("**ICE built from it:**" + ("" if mine else " none yet"))
        for c in mine:
            rel = os.path.relpath(ice_paths[str(c["id"])], os.path.dirname(path))
            lines.append(f"- [{c.get('title') or c['id']}]({rel})")
        lines += ["", "**What was done:** (nothing yet)", ""]
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines))

    for s, md in zip(sources, source_mds):
        src_lines = ["# Source", "",
                     f"**Kind:** {s.get('kind')}",
                     f"**Read on:** {s.get('read_on')}",
                     f"**Snapshot:** {', '.join(s.get('files', []))}",
                     f"**What it shows:** {shows.get(str(s['snapshot_dir']), '')}",
                     f"**Given by:** {s.get('given_by')}",
                     "**Shows the intents:**"]
        for i in confirmed:
            rel = os.path.relpath(paths[str(i["id"])], s["snapshot_dir"])
            src_lines.append(f"- [{i['title']}]({rel})")
        with open(md, "w", encoding="utf-8") as fh:
            fh.write("\n".join(src_lines) + "\n")

    missing_shows = [s["snapshot_dir"] for s in sources if not shows.get(str(s["snapshot_dir"]))]
    linked = not missing_shows and all(os.path.isfile(m) for m in source_mds) \
        and all(os.path.isfile(p) for p in list(paths.values()) + list(ice_paths.values()))
    manifest = {
        "intents": [{"id": str(i["id"]), "path": paths[str(i["id"])],
                     "ice": [ice_paths[str(c["id"])] for c in ice
                             if str(c.get("built_from")) == str(i["id"])]}
                    for i in confirmed],
        "dropped": dropped,
        "ice_dropped": ice_dropped,
        "confirmed_by": conf["confirmed_by"],
        "sources": source_mds,
        "any_confirmed": True,
        "all_decided": True,
        "confirmed_and_decided": True,
        "sources_saved": all(s.get("snapshot_saved") for s in sources),
        "linked": linked,
    }
    if missing_shows:
        manifest["problem"] = f"no 'what it shows' summary for: {', '.join(missing_shows)}"
    with open(os.path.join(args.working, "intent-manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
    print(json.dumps(manifest, indent=2))
    return 0 if linked else 2


if __name__ == "__main__":
    sys.exit(main())
