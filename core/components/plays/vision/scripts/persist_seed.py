#!/usr/bin/env python3
"""
persist_seed.py — /vision's deterministic keyed persist, in place on the live model.

Direct-model-write remnant of the old apply_seed.py (ADR 026,
standards/rules/direct-model-write.md). There is NO draft tree: the LLM authoring skill
(author-vision-seed) already wrote or updated the per-node grounding docs (domain.md,
capability.md) straight to the live model. This script owns the SHARED files and every page
move — the spine `_spine.yaml` (with its `profile` block) and the Touches lists on the
business intent pages — and merges the manifest's spine-delta in place:

  - new entries (domains / capabilities / functionalities / slices / epics): added ONLY when
    their id is absent; an id already present is left untouched (recorded as skipped).
  - `updates` to existing domains and capabilities — ONLY these (#637, C6): set an empty
    `domain`; raise `detail` (directional → detailed, never lower); refresh `one_line`; add to
    `intents`. Any other field, an unknown id, or a lowered `detail` refuses the whole run
    before anything is written. Setting a domain that differs from one already set is not
    applied — moving between domains is alignment work — and is recorded as a warning.
  - placing: a capability that gains a domain while its page sits in the holding folder
    (`capabilities/<id>/capability.md`) has the page moved byte-identical to
    `<domain-slug>/<capability-slug>/capability.md`, its `doc` repointed, and every link to
    the old page on the intent pages pointed at the new one.
  - links both ways (ontology v4): a domain gains the `intents` of every capability under it
    that this run wrote, updated or placed; and for every intent linked to a part this run,
    the intent page's Touches list names the part — `adds` when the part is new in this run,
    `changes` when it was already there (intent_touches.py). A missing intent page is a
    warning, never a stop.
  - the profile block: added ONLY if the live spine has none.

Layer rule: pure file reads/writes from disk inputs; no git/gh/network.

    python3 persist_seed.py --seed-manifest <seed-manifest.yaml> \
        --product-base <product_base> --out-manifest <persist-manifest.json> \
        [--intents <working>/intents.json]

Prints {applied, written[], skipped[], updated[], placed[], links[], warnings[], changed{}}
JSON (`applied: true` is the stop-condition gate's persist record, D1/D2). With --intents
(read_intents.py's record), a capability built from an input intent that still has no domain
is named in `warnings`. Exit 0 on success, 2 on usage/parse/containment error (nothing
written).
"""

import argparse
import hashlib
import json
import os
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("persist_seed.py: PyYAML is required (pip install pyyaml).\n")
    sys.exit(2)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import intent_touches as touches  # noqa: E402

SPINE_NAME = "_spine.yaml"
HOLDING = "capabilities/"
# id-keyed collections merged additively, with their singular tag for the manifest.
ID_LISTS = {
    "domains": "domain",
    "capabilities": "capability",
    "functionalities": "functionality",
    "slices": "slice",
    "epics": "epic",
}
UPDATABLE = {"domain": ("detail", "one_line", "intents"),
             "capability": ("domain", "detail", "one_line", "intents")}
DETAIL_RANK = {"directional": 0, "detailed": 1}


class Refused(Exception):
    """A reason to write nothing."""


def load(path):
    if not os.path.isfile(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def by_id(live, key):
    return {str(e.get("id")): e for e in live.get(key) or [] if isinstance(e, dict)}


def merge_new(delta, live, rec):
    """Add new entries whose id is absent; never modify an existing one."""
    for key, singular in ID_LISTS.items():
        entries = delta.get(key) or []
        if not entries:
            continue
        live_list = live.setdefault(key, [])
        have = {e.get("id") for e in live_list if isinstance(e, dict)}
        for e in entries:
            eid = e.get("id")
            tag = f"spine:{singular}:{eid}"
            if eid in have:
                rec["skipped"].append(tag)
            else:
                live_list.append(e)
                have.add(eid)
                rec["written"].append(tag)
                rec["new"].add((singular, str(eid)))
                rec["changed"].setdefault(key, []).append(eid)
    if delta.get("profile"):
        if live.get("profile"):
            rec["skipped"].append("spine:profile")
        else:
            live["profile"] = delta["profile"]
            rec["written"].append("spine:profile")
            rec["changed"]["profile"] = True


def check_updates(updates, live):
    """Refuse the run, before any write, if an update is outside the named ones."""
    for u in updates:
        kind, uid = u.get("kind"), str(u.get("id"))
        if kind not in UPDATABLE:
            raise Refused(f"update of kind `{kind}` — only domain and capability entries may be updated")
        extra = sorted(set(u) - {"kind", "id"} - set(UPDATABLE[kind]))
        if extra:
            raise Refused(f"update of {kind} `{uid}` touches {', '.join(extra)} — not a named update")
        entry = by_id(live, {"domain": "domains", "capability": "capabilities"}[kind]).get(uid)
        if entry is None:
            raise Refused(f"update names {kind} `{uid}`, which is not in the spine")
        if "detail" in u:
            old, new = DETAIL_RANK.get(entry.get("detail"), 0), DETAIL_RANK.get(u["detail"])
            if new is None:
                raise Refused(f"{kind} `{uid}`: detail `{u['detail']}` is not directional or detailed")
            if kind == "capability" and u["detail"] == "detailed":
                raise Refused(f"capability `{uid}`: /vision never details a capability (C3)")
            if new < old:
                raise Refused(f"{kind} `{uid}`: detail may be raised, never lowered")


def apply_updates(updates, live, rec):
    for u in updates:
        kind, uid = u["kind"], str(u["id"])
        entry = by_id(live, {"domain": "domains", "capability": "capabilities"}[kind])[uid]
        fields = []
        if u.get("domain"):
            have = str(entry.get("domain") or "")
            if not have:
                entry["domain"] = str(u["domain"])
                fields.append("domain")
            elif have != str(u["domain"]):
                rec["warnings"].append(f"capability `{uid}` is under `{have}`; /vision suggested "
                                       f"`{u['domain']}` — moving it is alignment work, left as is")
        if "detail" in u and u["detail"] != entry.get("detail"):
            entry["detail"] = u["detail"]
            fields.append("detail")
        if str(u.get("one_line") or "").strip() and u["one_line"] != entry.get("one_line"):
            entry["one_line"] = u["one_line"]
            fields.append("one_line")
        if add_intents(entry, u.get("intents")):
            fields.append("intents")
        if fields:
            rec["updated"].append({"kind": kind, "id": uid, "fields": fields})
            rec["touched"].add((kind, uid))


def add_intents(entry, ids):
    have = [str(x) for x in entry.get("intents") or []]
    new = [str(x) for x in ids or [] if str(x) not in have]
    if new:
        entry["intents"] = have + new
    return bool(new)


def place(live, root, rec):
    """Move each holding-folder capability that now has a domain into its domain's folder."""
    domains = by_id(live, "domains")
    plan = []
    for c in live.get("capabilities") or []:
        if not isinstance(c, dict) or not c.get("domain") or not str(c.get("doc", "")).startswith(HOLDING):
            continue
        d = domains.get(str(c["domain"]))
        if d is None:
            rec["warnings"].append(f"capability `{c.get('id')}` names domain `{c['domain']}`, which is not "
                                   f"in the spine — its page stays in the holding folder")
            continue
        new_doc = f"{d.get('slug') or d.get('id')}/{c.get('slug') or c.get('id')}/capability.md"
        old_abs, new_abs = os.path.join(root, c["doc"]), os.path.join(root, new_doc)
        if not os.path.isfile(old_abs):
            rec["warnings"].append(f"capability `{c.get('id')}`: its page {c['doc']} is missing — not moved")
            continue
        if os.path.exists(new_abs):
            raise Refused(f"cannot place `{c.get('id')}`: {new_doc} already exists")
        plan.append((c, old_abs, new_abs, new_doc))
    return plan


def do_place(plan, root, rec):
    for c, old_abs, new_abs, new_doc in plan:
        before = sha(old_abs)
        os.makedirs(os.path.dirname(new_abs), exist_ok=True)
        os.rename(old_abs, new_abs)
        for folder in (os.path.dirname(old_abs), os.path.dirname(os.path.dirname(old_abs))):
            try:
                os.rmdir(folder)           # only an empty holding folder goes
            except OSError:
                break
        rec["placed"].append({"id": str(c["id"]), "from": c["doc"], "to": new_doc,
                              "unchanged": sha(new_abs) == before})
        rec["moves"][c["doc"]] = new_doc
        c["doc"] = new_doc
        rec["touched"].add(("capability", str(c["id"])))


def link_domains(live, rec):
    """A domain gains the intents of the capabilities under it that this run touched."""
    domains = by_id(live, "domains")
    for c in live.get("capabilities") or []:
        if not isinstance(c, dict):
            continue
        cid = str(c.get("id"))
        if ("capability", cid) not in rec["touched"] | rec["new"]:
            continue
        d = domains.get(str(c.get("domain") or ""))
        if d is not None and add_intents(d, c.get("intents")):
            did = str(d["id"])
            if ("domain", did) not in rec["new"]:
                rec["updated"].append({"kind": "domain", "id": did, "fields": ["intents"]})
            rec["touched"].add(("domain", did))


def write_touches(live, root, rec):
    """Each intent page: relink moved pages, and list every part this run linked to it."""
    parts = []
    titles = {}
    for key, kind in (("domains", "domain"), ("capabilities", "capability")):
        for e in live.get(key) or []:
            if isinstance(e, dict) and (kind, str(e.get("id"))) in rec["touched"] | rec["new"]:
                parts.append((kind, e))
    by_intent = {}
    for kind, e in parts:
        for iid in e.get("intents") or []:
            by_intent.setdefault(str(iid), []).append((kind, e))
    pages = set(by_intent)
    pages |= {os.path.splitext(f)[0] for f in os.listdir(os.path.join(root, "intents"))} \
        if rec["moves"] and os.path.isdir(os.path.join(root, "intents")) else set()
    for iid in sorted(pages):
        page = os.path.join(root, "intents", f"{iid}.md")
        if not os.path.isfile(page):
            if iid in by_intent:
                rec["warnings"].append(f"intent `{iid}` has no page — its Touches list was not written")
            continue
        with open(page, encoding="utf-8") as fh:
            text = before = fh.read()
        for old, new in rec["moves"].items():
            text, _n = touches.relink(text, touches.rel(page, os.path.join(root, old)),
                                      touches.rel(page, os.path.join(root, new)))
        entries = []
        for kind, e in by_intent.get(iid, []):
            mark = "adds" if (kind, str(e.get("id"))) in rec["new"] else "changes"
            entries.append(touches.entry(title_of(root, e, kind, titles), touches.rel(page, os.path.join(root, e["doc"])),
                                         kind, mark))
            rec["links"].append({"intent": iid, "kind": kind, "id": str(e.get("id")), "mark": mark})
        # domains before capabilities, so the list reads from the top of the tree down
        entries.sort(key=lambda x: x["kind"] != "domain")
        if entries:
            text = touches.upsert(text, entries)
        if text != before:
            with open(page, "w", encoding="utf-8") as fh:
                fh.write(text)
            rec["intent_pages"].append(f"intents/{iid}.md")


def title_of(root, e, kind, cache):
    """A part's name from its page's H1 (`# Theme: X` / `# Capability: X`), else its id."""
    key = (kind, str(e.get("id")))
    if key not in cache:
        title = ""
        path = os.path.join(root, str(e.get("doc") or ""))
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as fh:
                first = fh.readline().strip()
            title = first.split(":", 1)[1].strip() if first.startswith("# ") and ":" in first else ""
        cache[key] = title or str(e.get("id"))
    return cache[key]


def unplaced(live, intents_path, rec):
    if not intents_path or not os.path.isfile(intents_path):
        return
    with open(intents_path, encoding="utf-8") as fh:
        wanted = {i["id"] for i in (json.load(fh).get("intents") or []) if i.get("accepted")}
    for c in live.get("capabilities") or []:
        if isinstance(c, dict) and not c.get("domain") and wanted & {str(x) for x in c.get("intents") or []}:
            rec["warnings"].append(f"capability `{c.get('id')}` is built from an input intent and still "
                                   f"has no domain")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Keyed in-place persist for /vision (ADR 026, #637).")
    ap.add_argument("--seed-manifest", required=True,
                    help="seed-manifest.yaml written by author-vision-seed (carries the spine-delta)")
    ap.add_argument("--product-base", required=True, help="product.base-path from config")
    ap.add_argument("--out-manifest", required=True)
    ap.add_argument("--intents", help="read_intents.py's record, to name capabilities left unplaced")
    args = ap.parse_args(argv)

    if not os.path.isfile(args.seed_manifest):
        sys.stderr.write(f"persist_seed.py: missing seed manifest {args.seed_manifest}\n")
        return 2

    man = load(args.seed_manifest)
    seed = man.get("seed", man) if isinstance(man, dict) else {}
    delta = seed.get("spine_delta") or seed.get("spine") or {}
    updates = [u for u in (delta.get("updates") or []) if isinstance(u, dict)] if isinstance(delta, dict) else []
    if not isinstance(delta, dict) or not any(delta.get(k) for k in ID_LISTS) \
            and not delta.get("profile") and not updates:
        sys.stderr.write("persist_seed.py: seed manifest carries no spine_delta to persist\n")
        return 2

    root = os.path.join(args.product_base, "product-os")
    live_spine_path = os.path.join(root, SPINE_NAME)
    live = load(live_spine_path)

    rec = {"written": [], "skipped": [], "updated": [], "placed": [], "links": [], "warnings": [],
           "intent_pages": [], "changed": {}, "new": set(), "touched": set(), "moves": {}}
    try:
        check_updates(updates, live)
        merge_new(delta, live, rec)
        apply_updates(updates, live, rec)
        plan = place(live, root, rec)
    except Refused as why:
        sys.stderr.write(f"persist_seed.py: {why} — nothing written\n")
        return 2
    do_place(plan, root, rec)
    link_domains(live, rec)
    unplaced(live, args.intents, rec)

    os.makedirs(root, exist_ok=True)
    with open(live_spine_path, "w", encoding="utf-8") as fh:
        yaml.safe_dump(live, fh, sort_keys=False, allow_unicode=True)
    write_touches(live, root, rec)

    manifest = {"applied": True,
                "written": sorted(rec["written"]),
                "skipped": sorted(rec["skipped"]),
                "updated": rec["updated"],
                "placed": rec["placed"],
                "links": rec["links"],
                "intent_pages": rec["intent_pages"],
                "warnings": rec["warnings"],
                "changed": rec["changed"]}
    with open(args.out_manifest, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
