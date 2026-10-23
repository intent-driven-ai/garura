#!/usr/bin/env python3
"""
persist_seed.py — /discover-domains's deterministic keyed persist, in place on the live model.

Direct-model-write remnant of the old apply_seed.py (ADR 026,
standards/rules/direct-model-write.md). There is NO draft tree: the LLM authoring skill
(author-domains) already wrote or updated the domain grounding docs (`domain.md`) straight
to the live model. This script owns the SHARED files — the spine `_spine.yaml` (with its
`profile` block) and the Touches lists on the business intent pages — and merges the
manifest's spine-delta in place. /discover-domains writes DOMAINS ONLY (ADR 043 part 2): capabilities
and features are /discover-capabilities's, so a delta that adds, updates or places one refuses the
whole run before anything is written.

  - new `domains` entries: added ONLY when their id is absent; an id already present is left
    untouched (recorded as skipped).
  - `updates` to existing domains — ONLY these (C6): raise `detail` (directional → detailed,
    never lower); refresh `one_line`; add to `intents`. Any other field, an unknown id, a
    lowered `detail`, or an update of any other kind refuses the whole run.
  - links both ways (ontology v4): for every intent a domain of this run names in its
    `intents`, the intent page's Touches list names the domain — `adds` when the domain is new
    in this run, `changes` when it was already there (intent_touches.py). A missing intent page
    is a warning, never a stop.
  - the profile block: added ONLY if the live spine has none.

Layer rule: pure file reads/writes from disk inputs; no git/gh/network.

    python3 persist_seed.py --seed-manifest <seed-manifest.yaml> \
        --product-base <product_base> --out-manifest <persist-manifest.json> \
        [--intents <working>/intents.json]

Prints {applied, written[], skipped[], updated[], links[], warnings[], changed{}} JSON
(`applied: true` is the stop-condition gate's persist record, D1/D2). With --intents
(read_intents.py's record), an input intent that no domain names is named in `warnings`.
Exit 0 on success, 2 on usage/parse/containment error (nothing written).
"""

import argparse
import json
import os
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("persist_seed.py: PyYAML is required (pip install pyyaml).\n")
    sys.exit(2)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import model_names  # noqa: E402  (stamped from create-play/references)
import intent_touches as touches  # noqa: E402

SPINE_NAME = "_spine.yaml"
# ADR 043 part 2: /discover-domains writes domains only; every other collection is /discover-capabilities's or later.
NOT_MINE = ("capabilities", "features", "slices", "epics")
UPDATABLE = {"domain": ("detail", "one_line", "intents")}
DETAIL_RANK = {"directional": 0, "detailed": 1}


class Refused(Exception):
    """A reason to write nothing."""


def load(path):
    if not os.path.isfile(path):
        return {}
    try:
        with open(path, encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
        model_names.check_model(data, path)
    except (OSError, yaml.YAMLError) as exc:
        raise Refused(f"cannot read {path}: {exc.__class__.__name__}") from exc
    if not isinstance(data, dict):
        raise Refused(f"{path} is not a mapping")
    return data


def by_id(live, key):
    return {str(e.get("id")): e for e in live.get(key) or [] if isinstance(e, dict)}


def merge_new(delta, live, rec):
    """Add new domain entries whose id is absent; never modify an existing one."""
    live_list = live.setdefault("domains", []) if delta.get("domains") else live.get("domains")
    have = {e.get("id") for e in live_list or [] if isinstance(e, dict)}
    for e in delta.get("domains") or []:
        eid = e.get("id")
        tag = f"spine:domain:{eid}"
        if eid in have:
            rec["skipped"].append(tag)
        else:
            live_list.append(e)
            have.add(eid)
            rec["written"].append(tag)
            rec["new"].add(("domain", str(eid)))
            rec["changed"].setdefault("domains", []).append(eid)
    if delta.get("profile"):
        if live.get("profile"):
            rec["skipped"].append("spine:profile")
        else:
            live["profile"] = delta["profile"]
            rec["written"].append("spine:profile")
            rec["changed"]["profile"] = True


def check_scope(delta):
    """Refuse a delta that writes anything but domains and the profile (ADR 043 part 2)."""
    for key in NOT_MINE:
        if delta.get(key):
            raise Refused(f"the delta adds `{key}` — /discover-domains writes domains only; capabilities and "
                          f"features are /discover-capabilities's (ADR 043)")


def check_updates(updates, live):
    """Refuse the run, before any write, if an update is outside the named ones."""
    for u in updates:
        kind, uid = u.get("kind"), str(u.get("id"))
        if kind not in UPDATABLE:
            raise Refused(f"update of kind `{kind}` — /discover-domains updates domain entries only (ADR 043)")
        extra = sorted(set(u) - {"kind", "id"} - set(UPDATABLE[kind]))
        if extra:
            raise Refused(f"update of {kind} `{uid}` touches {', '.join(extra)} — not a named update")
        entry = by_id(live, "domains").get(uid)
        if entry is None:
            raise Refused(f"update names {kind} `{uid}`, which is not in the spine")
        if "detail" in u:
            old, new = DETAIL_RANK.get(entry.get("detail"), 0), DETAIL_RANK.get(u["detail"])
            if new is None:
                raise Refused(f"{kind} `{uid}`: detail `{u['detail']}` is not directional or detailed")
            if new < old:
                raise Refused(f"{kind} `{uid}`: detail may be raised, never lowered")


def apply_updates(updates, live, rec):
    for u in updates:
        uid = str(u["id"])
        entry = by_id(live, "domains")[uid]
        fields = []
        if "detail" in u and u["detail"] != entry.get("detail"):
            entry["detail"] = u["detail"]
            fields.append("detail")
        if str(u.get("one_line") or "").strip() and u["one_line"] != entry.get("one_line"):
            entry["one_line"] = u["one_line"]
            fields.append("one_line")
        if add_intents(entry, u.get("intents")):
            fields.append("intents")
        if fields:
            rec["updated"].append({"kind": "domain", "id": uid, "fields": fields})
            rec["touched"].add(("domain", uid))


def add_intents(entry, ids):
    have = [str(x) for x in entry.get("intents") or []]
    new = [str(x) for x in ids or [] if str(x) not in have]
    if new:
        entry["intents"] = have + new
    return bool(new)


def write_touches(live, root, rec):
    """Each intent page a domain of this run names: list the domain in its Touches list."""
    titles = {}
    by_intent = {}
    for e in live.get("domains") or []:
        if isinstance(e, dict) and ("domain", str(e.get("id"))) in rec["touched"] | rec["new"]:
            for iid in e.get("intents") or []:
                by_intent.setdefault(str(iid), []).append(e)
    for iid in sorted(by_intent):
        page = os.path.join(root, "intents", f"{iid}.md")
        if not os.path.isfile(page):
            rec["warnings"].append(f"intent `{iid}` has no page — its Touches list was not written")
            continue
        with open(page, encoding="utf-8") as fh:
            text = before = fh.read()
        entries = []
        for e in by_intent[iid]:
            mark = "adds" if ("domain", str(e.get("id"))) in rec["new"] else "changes"
            entries.append(touches.entry(title_of(root, e, "domain", titles),
                                         touches.rel(page, os.path.join(root, e["doc"])), "domain", mark))
            rec["links"].append({"intent": iid, "kind": "domain", "id": str(e.get("id")), "mark": mark})
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


def unlinked(live, intents_path, rec):
    """An input intent that no domain names is a warning, never a stop."""
    if not intents_path or not os.path.isfile(intents_path):
        return
    with open(intents_path, encoding="utf-8") as fh:
        wanted = [i["id"] for i in (json.load(fh).get("intents") or []) if i.get("accepted")]
    named = {str(x) for d in live.get("domains") or [] if isinstance(d, dict) for x in d.get("intents") or []}
    for iid in wanted:
        if str(iid) not in named:
            rec["warnings"].append(f"intent `{iid}` is named by no domain yet")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Keyed in-place persist for /discover-domains — domains only (ADR 026, ADR 043).")
    ap.add_argument("--seed-manifest", required=True,
                    help="seed-manifest.yaml written by author-domains (carries the spine-delta)")
    ap.add_argument("--product-base", required=True, help="product.base-path from config")
    ap.add_argument("--out-manifest", required=True)
    ap.add_argument("--intents", help="read_intents.py's record, to name input intents no domain names")
    args = ap.parse_args(argv)

    if not os.path.isfile(args.seed_manifest):
        sys.stderr.write(f"persist_seed.py: missing seed manifest {args.seed_manifest}\n")
        return 2

    try:
        man = load(args.seed_manifest)
    except Refused as why:
        sys.stderr.write(f"persist_seed.py: {why} — nothing written\n")
        return 2
    seed = man.get("seed", man) if isinstance(man, dict) else {}
    delta = seed.get("spine_delta") or seed.get("spine") or {}
    updates = [u for u in (delta.get("updates") or []) if isinstance(u, dict)] if isinstance(delta, dict) else []
    if not isinstance(delta, dict) or not any(delta.get(k) for k in ("domains",) + NOT_MINE) \
            and not delta.get("profile") and not updates:
        sys.stderr.write("persist_seed.py: seed manifest carries no spine_delta to persist\n")
        return 2

    root = os.path.join(args.product_base, "product-os")
    live_spine_path = os.path.join(root, SPINE_NAME)
    try:
        live = load(live_spine_path)
    except Refused as why:
        sys.stderr.write(f"persist_seed.py: {why} — nothing written\n")
        return 2

    rec = {"written": [], "skipped": [], "updated": [], "links": [], "warnings": [],
           "intent_pages": [], "changed": {}, "new": set(), "touched": set()}
    try:
        check_scope(delta)
        check_updates(updates, live)
    except Refused as why:
        sys.stderr.write(f"persist_seed.py: {why} — nothing written\n")
        return 2
    merge_new(delta, live, rec)
    apply_updates(updates, live, rec)
    unlinked(live, args.intents, rec)

    os.makedirs(root, exist_ok=True)
    with open(live_spine_path, "w", encoding="utf-8") as fh:
        yaml.safe_dump(live, fh, sort_keys=False, allow_unicode=True)
    write_touches(live, root, rec)

    manifest = {"applied": True,
                "written": sorted(rec["written"]),
                "skipped": sorted(rec["skipped"]),
                "updated": rec["updated"],
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
