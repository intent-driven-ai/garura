#!/usr/bin/env python3
"""
feature_ice.py — reach the product model from an /update-plan session (#1002).

    python3 feature_ice.py find --root <model dir> --spine <spine> (--ref <id|slug|title> | --story <n>) \
        [--plans-dir <plans>] --out <found.json> [--collect <model-found.json>]
    python3 feature_ice.py copy --root <model dir> --spine <spine> --intents-dir <intents> \
        --feature <id> --working <working> --out <feature-ice.json>
    python3 feature_ice.py body --draft <story-draft-<i>.json> --record <feature-ice.json> --plan <id> \
        --out <story-body.md>
    python3 feature_ice.py mark --draft <draft-entries.json> --at <i> (--found <found.json> |
        --record <feature-ice.json> | --body <story-body.md> --story-draft <story-draft-<i>.json>)

`find` looks a feature up in the model index: by its id, its slug or its page title (`--ref`),
or as the feature whose story is issue n (`--story`): the feature that names that issue in the
model index, or the one a plan file's item for issue n `represents`. It writes {found, feature, one_line,
capability, ice_pages: [feature page, capability page], story}. `found: false` when nothing
matches, and `matches` when a name fits more than one feature (the person names one).
`--collect` also adds the record to a running list ({found: [...]}) that the `model` screen shows.

`copy` runs the ICE ready check (check_ice_workable.py, beside this script) on the feature's ICE
and its capability's ICE. When both are ready it writes one clean copy, `<working>/ice/<id>.md`,
holding both ICE with every "Fails if" block taken out (plan_common.py, shared with /shape-plan),
and `<working>/story-input.json` for the story writer (author-work-items, story mode): {mode:
"story", feature: {id, one_line, clean_ice}}. It names no ICE page. The record: {feature, ready,
reason, clean_ice, ice_pages}. A feature whose ICE is not ready gets no copy: the story then
takes the person's words, and the list says why.

`body` checks the story the writer drafted, the same way /shape-plan checks its drafts (a title,
the three parts of the scope of work, the four Context lines, and no line of a "Fails if" block,
the words "Fails if" or a recovery phrase), and writes the issue's body in /shape-plan's layout.
Exit 0 written; 1 the draft breaks a rule (problems printed, nothing written); 2 bad input.

`mark` writes a step's result onto entry i of the session's draft (draft-entries.json): `--found`
names the feature on the entry (`feature`), or, when no feature or more than one matches, takes
`feature_ref` off the entry and adds a question in its four parts, so nothing is guessed;
`--record` of a feature whose ICE is not ready sets `no_ice` (the reason; the story keeps the
person's words); `--body` with the writer's draft sets the entry's `body` to the checked story
body, its title (unless the person gave one) and `from_ice: true`.
"""

import argparse
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_common as pc  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
GUIDANCE = ("read", "never_read", "persona", "in_out")
SCOPE = ("goals", "limits", "expectations")


def load_spine(path):
    spine = pc.read_yaml(path, "the spine")
    if not isinstance(spine, dict):
        raise pc.Refused("the spine must be a YAML mapping")
    return spine


def pages_of(spine, f):
    cap = pc.entry(spine, "capabilities", f.get("capability")) if f.get("capability") else None
    return cap, [p for p in (pc.ice_page(spine, f), pc.ice_page(spine, cap)) if p]


def represented_by(plans_dir, story):
    """The feature ids that plan items for issue `story` represent."""
    out = []
    if not plans_dir or not os.path.isdir(plans_dir):
        return out
    for name in sorted(os.listdir(plans_dir)):
        if not name.endswith(".yaml"):
            continue
        try:
            plan = pc.read_yaml(os.path.join(plans_dir, name), "a plan file")
        except pc.Refused:
            continue
        stack = list((plan or {}).get("tree") or []) if isinstance(plan, dict) else []
        while stack:
            n = stack.pop()
            if isinstance(n, dict):
                if str(n.get("issue")) == str(story) and n.get("represents"):
                    out.append(n["represents"])
                stack += n.get("children") or []
    return out


def find(root, spine, ref=None, story=None, plans_dir=None):
    features = [f for f in spine.get("features") or [] if isinstance(f, dict)]
    if story is not None:
        hits = [f for f in features if str(f.get("issue")) == str(story)]
        if not hits:
            ids = set(represented_by(plans_dir, story))
            hits = [f for f in features if f.get("id") in ids]
    else:
        want = str(ref).strip().lower()
        hits = [f for f in features if want in (str(f.get("id")).lower(), str(f.get("slug")).lower())]
        if not hits:
            hits = [f for f in features
                    if (pc.page_title(root, f.get("doc"), "Feature:") or "").strip().lower() == want]
    if len(hits) != 1:
        return {"found": False, "ref": ref, "story": story,
                "matches": [f.get("id") for f in hits]}
    f = hits[0]
    cap, pages = pages_of(spine, f)
    return {"found": True, "feature": f.get("id"), "one_line": f.get("one_line"),
            "capability": f.get("capability"), "ice_pages": pages, "story": f.get("issue")}


def ready_check(spine_path, intents_dir, node):
    p = subprocess.run([sys.executable, os.path.join(HERE, "check_ice_workable.py"), "--spine", spine_path,
                        "--intents-dir", intents_dir, "--node", node], capture_output=True, text=True)
    if p.returncode == 0:
        return True, ""
    try:
        report = json.loads(p.stdout) if p.stdout.strip() else {}
    except json.JSONDecodeError:
        report = {}
    stops = report.get("stops") or [report.get("reason") or p.stderr.strip() or "not ready"]
    return False, "; ".join(str(s) for s in stops)


def copy(root, spine_path, intents_dir, fid, working):
    spine = load_spine(spine_path)
    f = pc.entry(spine, "features", fid)
    if f is None:
        raise pc.Refused(f"no feature {fid} in the spine")
    cap, pages = pages_of(spine, f)
    rec = {"feature": fid, "ready": False, "reason": "", "clean_ice": None, "ice_pages": pages}
    reasons, parts = [], []
    for label, part in (("feature", f), ("capability", cap)):
        if part is None:
            reasons.append(f"the {label} is not in the spine")
            continue
        ok, why = ready_check(spine_path, intents_dir, part["id"])
        if not ok:
            reasons.append(f"the {label} ICE ({part['id']}) is not ready: {why}")
        lines = pc.ice_lines(root, spine, part)
        if not lines:
            reasons.append(f"the {label} ({part['id']}) has no ICE")
        parts.append((label.capitalize(), part["id"], lines or []))
    clean = os.path.join(working, "ice", f"{fid}.md")
    if reasons:
        rec["reason"] = "; ".join(reasons)
        if os.path.exists(clean):
            os.remove(clean)
        return rec
    os.makedirs(os.path.dirname(clean), exist_ok=True)
    out = [f"# The two ICE of {fid}", "",
           "Written by feature_ice.py for /update-plan. The failure lines are taken out.", ""]
    for label, pid, lines in parts:
        out += [f"## {label} ICE — {pid}", ""]
        for ln in pc.without_fails_if(lines):
            out.append("#" + ln if ln.startswith("#") else ln)
        out.append("")
    with open(clean, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out).rstrip() + "\n")
    rec.update(ready=True, clean_ice=clean)
    pc.write_json(os.path.join(working, "story-input.json"),
                  {"mode": "story", "feature": {"id": fid, "one_line": f.get("one_line"), "clean_ice": clean}})
    return rec


def filled(value):
    if isinstance(value, str):
        return bool(value.strip())
    return isinstance(value, list) and bool(value) and all(isinstance(v, str) and v.strip() for v in value)


def check_story(story, ice_pages, root):
    problems = []
    if not filled(story.get("title")):
        problems.append("the story has no title")
    scope = story.get("scope_of_work") or {}
    problems += [f"the scope of work has no {k}" for k in SCOPE if not filled(scope.get(k))]
    guide = story.get("context_guidance") or {}
    problems += [f"the Context guidance has no '{k}' line" for k in GUIDANCE if not filled(guide.get(k))]
    fails = []
    for rel in ice_pages or []:
        path = os.path.join(root, rel) if root else rel
        if os.path.isfile(path):
            fails += pc.fails_if_texts(pc.read_text(path).splitlines())
    problems += [f"the story text: {r}" for r in pc.forbidden_in(pc.all_text(story), fails)]
    return problems


def body(story, fid, plan_id, pages):
    scope, guide = story.get("scope_of_work") or {}, story.get("context_guidance") or {}
    lines = [f"Represents: {fid}", f"Plan: {plan_id}", "", "## Scope of work", "", "Goals:"]
    lines += [f"- {g}" for g in scope.get("goals") or []]
    lines += ["", "Limits:"] + [f"- {x}" for x in scope.get("limits") or []]
    lines += ["", "Expectations:"] + [f"- {x}" for x in scope.get("expectations") or []]
    lines += ["", "## Context guidance", "", f"- Read: {guide.get('read', '')}",
              f"- Never read: {guide.get('never_read', '')}", f"- Persona: {guide.get('persona', '')}",
              f"- In and out: {guide.get('in_out', '')}", "", "Written from: " + "; ".join(pages)]
    return "\n".join(lines) + "\n"


def mark(draft_path, at, found=None, record=None, body_path=None, story_draft=None):
    with open(draft_path, encoding="utf-8") as fh:
        draft = json.load(fh)
    entries = draft.get("entries") or []
    if not 0 <= at < len(entries):
        raise pc.Refused(f"the draft has no entry {at}")
    e = entries[at]
    if found is not None:
        if found.get("found"):
            e["feature"] = found["feature"]
        else:
            ref = e.pop("feature_ref", None)
            many = found.get("matches") or []
            draft.setdefault("questions", []).append({
                "question": (f"Which feature did you mean by '{ref}'?" if many
                             else f"No feature in the model matches '{ref}'. Which feature is it?"),
                "answer": (f"One of {', '.join(many)}." if many
                           else "None found; give its id (fn-...) or the title of its page."),
                "why": "The story is drafted from that feature's ICE; a wrong feature gives a wrong story.",
                "examples": ["fn-818", "the feature's page title, for example 'Pick a free slot'"]})
    if record is not None and not record.get("ready"):
        e["no_ice"] = record.get("reason") or "the feature has no ready ICE"
    if body_path is not None:
        if not story_draft:
            raise pc.Refused("--body needs --story-draft (the story the body was written from)")
        with open(body_path, encoding="utf-8") as fh:
            e["body"] = fh.read()
        with open(story_draft, encoding="utf-8") as fh:
            story = (json.load(fh).get("stories") or [{}])[0]
        if not e.get("title"):
            e["title"] = story.get("title")
        e["from_ice"] = True
        e.pop("no_ice", None)
    pc.write_json(draft_path, draft)
    return e


def main(argv=None):
    ap = argparse.ArgumentParser(description="reach the product model from an /update-plan session")
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("find")
    f.add_argument("--root", required=True)
    f.add_argument("--spine", required=True)
    g = f.add_mutually_exclusive_group(required=True)
    g.add_argument("--ref")
    g.add_argument("--story")
    f.add_argument("--plans-dir")
    f.add_argument("--out", required=True)
    f.add_argument("--collect")
    c = sub.add_parser("copy")
    for a in ("--root", "--spine", "--intents-dir", "--feature", "--working", "--out"):
        c.add_argument(a, required=True)
    b = sub.add_parser("body")
    for a in ("--draft", "--record", "--plan", "--out"):
        b.add_argument(a, required=True)
    b.add_argument("--root", default="")
    m = sub.add_parser("mark")
    m.add_argument("--draft", required=True)
    m.add_argument("--at", type=int, required=True)
    m.add_argument("--found")
    m.add_argument("--record")
    m.add_argument("--body")
    m.add_argument("--story-draft")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "mark":
            def read(p):
                with open(p, encoding="utf-8") as fh:
                    return json.load(fh)
            e = mark(args.draft, args.at, read(args.found) if args.found else None,
                     read(args.record) if args.record else None, args.body, args.story_draft)
            print(json.dumps({k: e.get(k) for k in ("feature", "from_ice", "no_ice", "title")}))
            return 0
        if args.cmd == "find":
            rec = find(args.root, load_spine(args.spine), args.ref, args.story, args.plans_dir)
            pc.write_json(args.out, rec)
            if args.collect:
                got = {"found": []}
                if os.path.isfile(args.collect):
                    with open(args.collect, encoding="utf-8") as fh:
                        got = json.load(fh)
                got.setdefault("found", []).append(rec)
                pc.write_json(args.collect, got)
            return 0
        if args.cmd == "copy":
            pc.write_json(args.out, copy(args.root, args.spine, args.intents_dir, args.feature, args.working))
            return 0
        with open(args.draft, encoding="utf-8") as fh:
            draft = json.load(fh)
        with open(args.record, encoding="utf-8") as fh:
            rec = json.load(fh)
        story = (draft.get("stories") or [{}])[0]
        problems = check_story(story, rec.get("ice_pages"), args.root)
        if problems:
            print(json.dumps({"ok": False, "problems": problems}, indent=2))
            return 1
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(body(story, rec["feature"], args.plan, rec.get("ice_pages") or []))
        print(json.dumps({"ok": True, "problems": [], "title": story.get("title")}))
        return 0
    except (pc.Refused, OSError, ValueError) as e:
        print(f"refused: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
