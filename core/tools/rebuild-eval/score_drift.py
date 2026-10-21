#!/usr/bin/env python3
"""score_drift.py — how much of the prototype came back, and whose fault the rest is.

    python3 score_drift.py --inventory <run>/inventory.json --compare <run>/compare.json \
        --check <run>/check.json [--review <run>/review.json] [--manifest <run>/brief-manifest.json] \
        --out-json <run>/report.json --out-md <run>/report.md

Each prototype behaviour counts 1 when met, ½ when partly met, 0 when missing:

- **kept** — (met + ½ partial) ÷ behaviours: what the rebuild brought back. **drift** = 1 − kept.
- **brief covers** — how much the brief describes, whatever the builder did: a met behaviour
  and one the compare found in the brief count 1; a partial one not in the brief counts ½.
  This is the drive's own number: a low *kept* with a high *brief covers* is the builder's
  fault, not the drive's.
- **missing / partial**, each split: not in the brief (the drive's fault) or in the brief (the
  builder's).
- **extras** — what the rebuild does that the prototype does not: said in the brief (the
  drive invented it) or the builder's own.
- The same numbers by screen; and the static check and the review beside them.

Exit 0 written; 2 an input cannot be read or the compare does not answer every behaviour once.
Standard library only. No LLM.
"""
import argparse
import json
import sys


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def pct(x):
    return round(100 * x, 1)


def score(inventory, compare):
    behaviours = inventory.get("behaviours") or []
    if not behaviours:
        raise ValueError("the inventory holds no behaviour")
    ids = [b["id"] for b in behaviours]
    if compare.get("could_not_open"):
        results = {i: {"verdict": "missing", "in_brief": None} for i in ids}
    else:
        results = {}
        for r in compare.get("results") or []:
            if r.get("id") in results:
                raise ValueError(f"behaviour {r['id']} has two results")
            results[r.get("id")] = r
        lost = [i for i in ids if i not in results]
        unknown = [i for i in results if i not in set(ids)]
        if lost or unknown:
            raise ValueError(f"the compare must answer every behaviour once (no result: {lost[:10]}; "
                             f"not in the inventory: {unknown[:10]})")
        for i, r in results.items():
            if r.get("verdict") not in ("met", "partial", "missing"):
                raise ValueError(f"behaviour {i}: verdict must be met, partial or missing")

    def tally(subset):
        n = len(subset)
        c = {"behaviours": n, "met": 0, "partial": 0, "missing": 0,
             "partial_in_brief": 0, "partial_not_in_brief": 0,
             "missing_in_brief": 0, "missing_not_in_brief": 0}
        covers = 0.0
        for i in subset:
            r = results[i]
            v = r["verdict"]
            c[v] += 1
            if v == "met":
                covers += 1
            else:
                key = f"{v}_{'in_brief' if r.get('in_brief') else 'not_in_brief'}"
                c[key] += 1
                if r.get("in_brief"):
                    covers += 1
                elif v == "partial":
                    covers += 0.5
        kept = (c["met"] + 0.5 * c["partial"]) / n if n else 0.0
        c.update({"kept_pct": pct(kept), "drift_pct": pct(1 - kept),
                  "brief_covers_pct": pct(covers / n if n else 0.0)})
        return c

    screens = {s["id"]: s.get("name", s["id"]) for s in inventory.get("screens") or []}
    by_screen = {}
    for b in behaviours:
        by_screen.setdefault(b.get("screen") or "?", []).append(b["id"])
    extras = compare.get("extras") or []
    return {
        "could_not_open": bool(compare.get("could_not_open")),
        "overall": tally(ids),
        "by_screen": [{"screen": s, "name": screens.get(s, s), **tally(v)} for s, v in by_screen.items()],
        "extras": {"total": len(extras), "in_brief": sum(1 for e in extras if e.get("in_brief")),
                   "builder_own": sum(1 for e in extras if not e.get("in_brief"))},
        "missing_not_in_brief": [{"id": i, "does": b.get("does"), "sees": b.get("sees"),
                                  "screen": screens.get(b.get("screen"), b.get("screen"))}
                                 for b in behaviours for i in [b["id"]]
                                 if results[i]["verdict"] != "met" and not results[i].get("in_brief")],
    }


def summarise_review(review):
    if not review:
        return None
    tests = {}
    for it in review.get("intents") or []:
        for t, v in (it.get("tests") or {}).items():
            tests.setdefault(t, {"pass": 0, "fail": 0})
            tests[t]["pass" if v == "pass" else "fail"] += 1

    def verdicts(items):
        out = {}
        for it in items or []:
            out[it.get("verdict")] = out.get(it.get("verdict"), 0) + 1
        return out

    domains = review.get("domains")
    if domains is None and review.get("domain"):
        domains = [review["domain"]]
    return {"intent_tests": tests, "domains": domains or [],
            "capabilities": verdicts(review.get("capabilities")),
            "functionalities": verdicts(review.get("functionalities")),
            "missed_behaviours": len(review.get("missed_behaviours") or [])}


def summarise_check(check):
    rules = {}
    for f in check.get("findings") or []:
        rules[f["rule"]] = rules.get(f["rule"], 0) + 1
    return {"ok": check.get("ok"), "counts": check.get("counts"), "findings_by_rule": rules}


def markdown(rep):
    o = rep["score"]["overall"]
    lines = ["# Rebuild eval", ""]
    if rep.get("brief"):
        b = rep["brief"]
        lines += [f"The brief held {b['counts']['intents']} intents, {b['counts']['domain']} domain, "
                  f"{b['counts']['capabilities']} capabilities and {b['counts']['functionalities']} "
                  f"functionalities (level: {b['level']}).", ""]
    if rep["score"]["could_not_open"]:
        lines += ["The rebuild did not open. Nothing of the prototype came back.", ""]
    lines += [
        f"Of {o['behaviours']} things a person can do or see on the prototype, the rebuild brought back "
        f"{o['met']} fully and {o['partial']} in part, and {o['missing']} are missing.",
        "",
        f"- Kept: {o['kept_pct']}%. Drift: {o['drift_pct']}%.",
        f"- The brief describes {o['brief_covers_pct']}% of the prototype.",
        f"- Missing and not in the brief (the drive's fault): {o['missing_not_in_brief']}; "
        f"partly there and not in the brief: {o['partial_not_in_brief']}.",
        f"- Missing although the brief says it (the builder's fault): {o['missing_in_brief']}.",
        f"- Added by the rebuild: {rep['score']['extras']['total']} "
        f"({rep['score']['extras']['in_brief']} from the brief, {rep['score']['extras']['builder_own']} "
        f"the builder's own).",
        "", "## By screen", "",
        "| Screen | Behaviours | Kept | Brief covers | Missing, not in brief |",
        "|---|---|---|---|---|",
    ]
    for s in rep["score"]["by_screen"]:
        lines.append(f"| {s['name']} | {s['behaviours']} | {s['kept_pct']}% | {s['brief_covers_pct']}% | "
                     f"{s['missing_not_in_brief']} |")
    c = rep["check"]
    lines += ["", "## Static check", "",
              "Passed." if c["ok"] else "Failed: " + ", ".join(f"{k} ×{v}" for k, v in c["findings_by_rule"].items()) + "."]
    r = rep.get("review")
    if r:
        lines += ["", "## Review of the output", ""]
        for t, v in r["intent_tests"].items():
            lines.append(f"- Intents, {t.replace('_', ' ')}: {v['pass']} pass, {v['fail']} fail.")
        for d in r.get("domains") or []:
            name = (d.get("file") or "").split("/")[0] or "domain"
            lines.append(f"- Domain {name}: {'recognised' if d.get('recognised') else 'not recognised'}"
                         f"{' — the industry calls it ' + d['known_as'] if d.get('known_as') else ''}.")
        lines.append(f"- Capabilities: {r['capabilities']}. Functionalities: {r['functionalities']}.")
        lines.append(f"- Prototype behaviours no functionality covers: {r['missed_behaviours']}.")
    gaps = rep["score"]["missing_not_in_brief"]
    if gaps:
        lines += ["", "## What the brief never said", ""]
        lines += [f"- {g['screen']}: {g['does']} → {g['sees']}" for g in gaps[:40]]
        if len(gaps) > 40:
            lines.append(f"- … and {len(gaps) - 40} more (report.json).")
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Score how much of the prototype the rebuild kept.")
    ap.add_argument("--inventory", required=True)
    ap.add_argument("--compare", required=True)
    ap.add_argument("--check", required=True)
    ap.add_argument("--review")
    ap.add_argument("--manifest")
    ap.add_argument("--out-json", required=True)
    ap.add_argument("--out-md", required=True)
    args = ap.parse_args(argv)
    try:
        rep = {"score": score(load(args.inventory), load(args.compare)),
               "check": summarise_check(load(args.check)),
               "review": summarise_review(load(args.review)) if args.review else None,
               "brief": load(args.manifest) if args.manifest else None}
    except (OSError, ValueError, KeyError) as exc:
        sys.stderr.write(f"score_drift.py: {exc}\n")
        return 2
    if rep["brief"]:
        rep["brief"] = {k: rep["brief"][k] for k in ("level", "counts")}
    with open(args.out_json, "w", encoding="utf-8") as fh:
        json.dump(rep, fh, indent=2)
    md = markdown(rep)
    with open(args.out_md, "w", encoding="utf-8") as fh:
        fh.write(md)
    print(json.dumps({k: rep["score"]["overall"][k] for k in ("behaviours", "kept_pct", "drift_pct", "brief_covers_pct")}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
