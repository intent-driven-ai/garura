#!/usr/bin/env python3
"""gather_plan.py — what the plan of one business intent holds (/shape-plan, C1, C2, C5, C9).

    python3 gather_plan.py --root <model dir> --spine <spine> --intent bi-<n> \
        --plans <plans dir> --out <working>/gather.json

It finds every slice whose `intents` lists the business intent, in the order of the spine (the
link "slice serves business intent"); it never picks or orders the slices itself. For each
slice it lists the features (`feature_refs`, in build order), each feature's capability, and the
page of each of the two ICE: the feature's and its capability's.

For each feature it runs the ready check (check_ice_workable.py, beside this script) on both
ICE. A feature is `ready: false`, with a `reason`, when either ICE is not ready, or has no
lines. For each ready feature it writes one clean copy, `<working>/ice/<feature id>.md`, that
holds both ICE with every "Fails if" line taken out. The skill reads only these copies. A clean
copy left from an earlier run for a feature that is not ready now is deleted.

Output:
    {intent, intent_title, plan_id, plan_file,
     slices: [{id, slug, name, outcome,
               features: [{id, name, one_line, capability, ready, reason, ice_pages: [..],
                           clean_ice}]}]}

Exit 0 written; 2 when no slice serves the intent, or an input is wrong (nothing written).
No git, no network.
"""

import argparse
import glob
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_common as pc  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def ready_check(spine_path, intents_dir, node):
    """(ready, reason) from check_ice_workable.py for one ICE."""
    p = subprocess.run([sys.executable, os.path.join(HERE, "check_ice_workable.py"),
                        "--spine", spine_path, "--intents-dir", intents_dir, "--node", node],
                       capture_output=True, text=True)
    try:
        report = json.loads(p.stdout) if p.stdout.strip() else {}
    except json.JSONDecodeError:
        report = {}
    if p.returncode == 0:
        return True, ""
    if p.returncode == 1:
        stops = report.get("stops") or [report.get("reason") or "not ready"]
        return False, "; ".join(str(s) for s in stops)
    return False, "the ready check could not run: " + str(report.get("error") or p.stderr.strip())


def clean_copy(fid, parts):
    """The clean copy's text: both ICE, headings one level down, no "Fails if" line."""
    out = [f"# The two ICE of {fid}", "",
           "Written by gather_plan.py for /shape-plan from the pages named below. "
           "The failure lines are taken out.", ""]
    for label, pid, page, lines in parts:
        out += [f"## {label} ICE — {pid} ({page})", ""]
        for ln in pc.without_fails_if(lines):
            out.append("#" + ln if ln.startswith("#") else ln)
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def gather(args):
    m = re.fullmatch(r"bi-(\d+)", args.intent or "")
    if not m:
        raise pc.Refused(f"the intent must read bi-<issue number>, not {args.intent!r}")
    plan_id = m.group(1)
    spine = pc.read_yaml(args.spine, "the spine")
    if not isinstance(spine, dict):
        raise pc.Refused("the spine must be a YAML mapping")
    working = os.path.dirname(os.path.abspath(args.out))
    intents_dir = os.path.join(args.root, "intents")
    slices = [s for s in spine.get("slices") or []
              if isinstance(s, dict) and args.intent in (s.get("intents") or [])]
    if not slices:
        raise pc.Refused(f"no slice in the spine serves {args.intent}; run /shape-slice {plan_id} first")
    out_slices, ready_ids = [], set()
    for sl in slices:
        record = {}
        if sl.get("record") and os.path.isfile(os.path.join(args.root, sl["record"])):
            rec = pc.read_yaml(os.path.join(args.root, sl["record"]), "the slice record") or {}
            record = (rec.get("slice") or {}) if isinstance(rec, dict) else {}
        features = []
        for fid in sl.get("feature_refs") or []:
            f = pc.entry(spine, "features", fid)
            if f is None:
                features.append({"id": fid, "name": fid, "one_line": "", "capability": None,
                                 "ready": False, "reason": "the feature is not in the spine",
                                 "ice_pages": [], "clean_ice": None})
                continue
            cap = pc.entry(spine, "capabilities", f.get("capability")) if f.get("capability") else None
            f_page, c_page = pc.ice_page(spine, f), pc.ice_page(spine, cap)
            pages = [os.path.join(args.root, p) for p in (f_page, c_page) if p]
            reasons = []
            for label, part in (("feature", f), ("capability", cap)):
                if part is None:
                    reasons.append(f"the {label} is not in the spine")
                    continue
                ok, why = ready_check(args.spine, intents_dir, part["id"])
                if not ok:
                    reasons.append(f"the {label} ICE ({part['id']}) is not ready: {why}")
                lines = pc.ice_lines(args.root, spine, part)
                if lines is None:
                    reasons.append(f"the {label} ICE ({part['id']}) has no page")
                elif not [ln for ln in pc.without_fails_if(lines) if ln.strip()]:
                    reasons.append(f"the {label} ICE ({part['id']}) has no lines")
            item = {"id": fid, "name": pc.page_title(args.root, f.get("doc"), "Feature:") or fid,
                    "one_line": f.get("one_line") or "", "capability": f.get("capability"),
                    "ready": not reasons, "reason": "; ".join(reasons), "ice_pages": pages,
                    "clean_ice": None}
            if not reasons:
                path = os.path.join(working, "ice", f"{fid}.md")
                pc.atomic_write(path, clean_copy(fid, [
                    ("Feature", fid, f_page, pc.ice_lines(args.root, spine, f)),
                    ("Capability", cap["id"], c_page, pc.ice_lines(args.root, spine, cap))]))
                item["clean_ice"] = path
                ready_ids.add(fid)
            features.append(item)
        out_slices.append({"id": sl.get("id"), "slug": sl.get("slug"),
                           "name": record.get("name") or sl.get("slug") or sl.get("id"),
                           "outcome": record.get("outcome") or "", "features": features})
    for old in glob.glob(os.path.join(working, "ice", "*.md")):
        if os.path.splitext(os.path.basename(old))[0] not in ready_ids:
            os.remove(old)
    title = pc.page_title(args.root, os.path.join("intents", f"{args.intent}.md"), "") or f"Plan {plan_id}"
    return {"intent": args.intent, "intent_title": title, "plan_id": plan_id,
            "plan_file": os.path.join(args.plans, f"{plan_id}.yaml"), "slices": out_slices}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Gather the slices and ICE of one business intent's plan.")
    ap.add_argument("--root", required=True)
    ap.add_argument("--spine", required=True)
    ap.add_argument("--intent", required=True)
    ap.add_argument("--plans", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        result = gather(args)
    except pc.Refused as exc:
        sys.stderr.write(f"gather_plan.py: {exc}\n")
        print(json.dumps({"ok": False, "reason": str(exc)}))
        return 2
    pc.write_json(args.out, result)
    print(json.dumps({"ok": True, "out": args.out, "slices": len(result["slices"]),
                      "not_ready": sum(not f["ready"] for s in result["slices"] for f in s["features"])}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
