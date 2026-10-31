#!/usr/bin/env python3
"""
plan.py — the plan tool: prints the plans from the plan files alone (#719).

    python3 plan.py list  --template T [--plans-dir D]
    python3 plan.py show  --template T [--plans-dir D] --plan ID
    python3 plan.py graph --template T [--plans-dir D] [--repo R]

A plan's file is `<plans-dir>/<id>.yaml`: its ID is its business intent's issue number, and its
`tree` holds every node under it, each with its `issue`, `kind`, `title`, `status` and
`children`. The tool reads only those files (and, for `graph`, git), never the tracker, and
makes no model call: the same files print the same way every time.

Every mark and every line comes from the template (`standards/templates/plan-view.md`), from its
fenced block that opens with ```yaml plan-view. A change to how a view looks is made there,
never here.

Output goes to stdout. Exit: 0 = printed, 1 = the plan asked for does not exist, 2 = bad input
(a template with no settings block, a plan file that cannot be read, a plan with no title, a
node that is not a mapping or has no issue, title or status, a status the template does not
know, a --repo that is not a folder). When git is not installed, every plan shows as on main
and the graph's counts read ?.
"""

import argparse
import glob
import os
import re
import subprocess
import sys

import yaml

DEFAULT_PLANS = os.path.join(".garura", "project", "plans")
BLOCK = re.compile(r"^```yaml plan-view\s*\n(.*?)^```", re.S | re.M)


class BadInput(Exception):
    pass


def load_template(path):
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError as e:
        raise BadInput(f"cannot read the template {path}: {e.strerror}")
    m = BLOCK.search(text)
    if not m:
        raise BadInput(f"{path} has no ```yaml plan-view block")
    t = yaml.safe_load(m.group(1)) or {}
    for key in ("statuses", "tree", "list", "graph"):
        if key not in t:
            raise BadInput(f"the template's settings have no '{key}'")
    t["by_name"] = {s["name"]: s for s in t["statuses"]}
    return t


def plan_id(path):
    return os.path.splitext(os.path.basename(path))[0]


def load_plans(plans_dir, template):
    """Every plan file, in the order of the plan numbers."""
    paths = [p for p in glob.glob(os.path.join(plans_dir, "*.yaml"))
             if os.path.basename(p) != "index.yaml"]
    paths.sort(key=lambda p: (int(plan_id(p)) if plan_id(p).isdigit() else float("inf"), plan_id(p)))
    plans = []
    for path in paths:
        try:
            with open(path, encoding="utf-8") as fh:
                plan = yaml.safe_load(fh) or {}
        except (OSError, yaml.YAMLError) as e:
            raise BadInput(f"cannot read {path}: {e}")
        if not isinstance(plan, dict):
            raise BadInput(f"{path} is not a mapping")
        plan.setdefault("id", plan_id(path))
        if not plan.get("title"):
            raise BadInput(f"{path} has no title")
        check_shape(plan.get("tree"), path)
        if plan.get("status") not in template["list"]["plan_statuses"]:
            raise BadInput(f"{path}: the plan status {plan.get('status')!r} is not one the template knows")
        if plan.get("direction") not in (None, *template["list"]["directions"]):
            raise BadInput(f"{path}: the direction {plan.get('direction')!r} is not 1, 2, 3 or empty")
        for node in walk(plan.get("tree")):
            missing = [k for k in ("issue", "title", "status") if not node.get(k)]
            if missing:
                raise BadInput(f"{path}: a node ({node.get('issue', 'no issue')}) has no {', '.join(missing)}")
            if node.get("status") not in template["by_name"]:
                raise BadInput(f"{path}: #{node.get('issue')} has the status {node.get('status')!r}, "
                               f"which the template does not know")
        plans.append(plan)
    return plans


def check_shape(nodes, path):
    """Every tree level is a list and every node a mapping, before anything reads a field."""
    if nodes is None:
        return
    if not isinstance(nodes, list):
        raise BadInput(f"{path}: a tree or a children list is not a list")
    for node in nodes:
        if not isinstance(node, dict):
            raise BadInput(f"{path}: a node is not a mapping: {node!r}")
        check_shape(node.get("children"), path)


def walk(nodes):
    for node in nodes or []:
        yield node
        yield from walk(node.get("children"))


def shown(node, template):
    return template["by_name"][node["status"]]["shown"]


def visible(node, template):
    return shown(node, template) or any(visible(c, template) for c in node.get("children") or [])


def finished_children(node, template):
    """A shown node whose children are all Done or Dropped prints them too, so a person can decide on it (#1005)."""
    children = node.get("children") or []
    return shown(node, template) and children and not any(shown(c, template) for c in children)


def tree_lines(nodes, template, prefix="", keep_all=False):
    lines = []
    keep = [n for n in nodes or [] if keep_all or visible(n, template)]
    for i, node in enumerate(keep):
        last = i == len(keep) - 1
        mark = template["by_name"][node["status"]]["mark"]
        text = template["tree"]["line"].format(mark=mark, issue=node["issue"], title=node["title"])
        lines.append(prefix + ("└─ " if last else "├─ ") + text)
        child_prefix = prefix + ("   " if last else "│  ")
        lines += tree_lines(node.get("children"), template, child_prefix, finished_children(node, template))
    return lines


def printed(nodes, template, keep_all=False):
    """Every node the tree prints, by the same rules as tree_lines."""
    for node in nodes or []:
        if keep_all or visible(node, template):
            yield node
            yield from printed(node.get("children"), template, finished_children(node, template))


def hidden_counts(nodes, template):
    seen = {id(n) for n in printed(nodes, template)}
    counts = {}
    for node in walk(nodes):
        if id(node) not in seen:
            counts[node["status"]] = counts.get(node["status"], 0) + 1
    return counts


def one_tree(plan, template):
    t = template["tree"]
    lines = [t["root"].format(issue=plan["id"], title=plan["title"])]
    lines += tree_lines(plan.get("tree"), template)
    counts = hidden_counts(plan.get("tree"), template)
    if counts:
        order = [s["name"] for s in template["statuses"] if s["name"] in counts]
        lines.append(t["hidden"].format(counts=t["hidden_join"].join(f"{counts[s]} {s}" for s in order)))
    return lines


def show(plans, plan, template, plans_dir):
    t = template["tree"]
    by_id = {str(p["id"]): p for p in plans}
    if str(plan) not in by_id:
        return 1, [t["no_plan"].format(plan=plan, dir=plans_dir)]
    legend = t["legend_join"].join(f"{s['mark']} {s['name']}" for s in template["statuses"])
    target = by_id[str(plan)]
    lines = [legend, ""] + one_tree(target, template)
    for needed in target.get("needs_plans") or []:
        lines.append("")
        if str(needed) in by_id:
            lines.append(t["needs"].format(plan=target["id"], needed=needed))
            lines += one_tree(by_id[str(needed)], template)
        else:
            lines.append(t["no_plan"].format(plan=needed, dir=plans_dir))
    return 0, lines


def plan_branch(plan, repo):
    """The plan's branch: the one its file names, else plan/<id>/base when git has it."""
    if plan.get("branch"):
        return plan["branch"]
    name = f"plan/{plan['id']}/base"
    return name if ref_of(name, repo) else None


def git(args, repo):
    """Run git in `repo`; None when git is not installed or cannot run there."""
    try:
        return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None


def ref_of(branch, repo):
    for ref in (branch, f"origin/{branch}"):
        r = git(["rev-parse", "--verify", "--quiet", ref], repo)
        if r is not None and r.returncode == 0:
            return ref
    return None


def listing(plans, template, plans_dir, repo):
    """One card for each plan: number and title, the direction icon on its own line (none when the
    plan has no direction); Status, Branch, Waits on; then each epic with its Progress. Status and Direction are read from the plan file as a person set
    them, never worked out from the work."""
    li = template["list"]
    if not plans:
        return [li["none"].format(dir=plans_dir)]
    by_id = {str(p["id"]): p for p in plans}
    label_width = li["label_width"]
    icons = li["directions"]
    lines = [li["legend_join"].join(f"{icons[k]} {li['direction_names'][k]}" for k in sorted(icons)), ""]

    def row(key, value=""):
        return li["row"].format(label=li["labels"][key].ljust(label_width), value=value).rstrip()

    for plan in plans:
        lines.append(li["plan_rule"])
        lines.append(li["head"].format(plan=plan["id"], title=plan["title"]))
        if plan.get("direction") in icons:
            lines.append(li["direction_line"].format(direction=icons[plan["direction"]]))
        lines.append("")
        lines.append(row("status", plan.get("status") or ""))
        lines.append(row("branch", plan_branch(plan, repo) or "main"))
        waits = li["waits_join"].join(
            li["waits_item"].format(plan=n, title=by_id[str(n)]["title"]) if str(n) in by_id
            else li["waits_item"].format(plan=n, title="").rstrip()
            for n in plan.get("needs_plans") or [])
        lines.append(row("waits", waits))
        epics = [n for n in plan.get("tree") or [] if n.get("kind") == "epic"]
        for i, epic in enumerate(epics):
            lines.append("" if i == 0 else li["epic_rule"])
            nodes = list(walk(epic.get("children")))
            done = sum(1 for n in nodes if n["status"] == "Done")
            dropped = sum(1 for n in nodes if n["status"] == "Dropped")
            mark = template["by_name"][epic["status"]]["mark"]
            lines.append(row("epic", li["epic"].format(mark=mark, issue=epic["issue"], title=epic["title"])))
            progress = li["progress"].format(done=done, open=len(nodes) - done - dropped)
            if dropped:
                progress += li["dropped"].format(dropped=dropped)
            lines.append(row("progress", progress))
        lines.append("")
    return lines[:-1]


def graph(plans, template, repo):
    g = template["graph"]
    lines = [g["main"]]
    branched, on_main = [], []
    for plan in plans:
        branch = plan_branch(plan, repo)
        (branched if branch else on_main).append((plan, branch))
    main = ref_of("main", repo)
    for i, (plan, branch) in enumerate(branched):
        ref = ref_of(branch, repo)
        ahead = behind = "?"
        if ref and main:
            r = git(["rev-list", "--left-right", "--count", f"{main}...{ref}"], repo)
            if r is not None and r.returncode == 0:
                behind, ahead = r.stdout.split()
        flag = g["behind_flag"] if behind not in ("?", "0") else ""
        bar = "└─" if i == len(branched) - 1 else "├─"
        lines.append(g["line"].format(bar=bar, branch=branch, ahead=ahead, behind=behind, flag=flag,
                                      plan=plan["id"], title=plan["title"]))
    if on_main:
        lines.append(g["on_main"].format(plans=", ".join(f"#{p['id']}" for p, _ in on_main)))
    return lines


def main(argv=None):
    ap = argparse.ArgumentParser(description="Print the plans from the plan files alone.")
    ap.add_argument("command", choices=["list", "show", "graph"])
    ap.add_argument("--template", required=True, help="the plan-view template")
    ap.add_argument("--plans-dir", default=DEFAULT_PLANS)
    ap.add_argument("--plan", help="the plan to show (show only)")
    ap.add_argument("--repo", default=".", help="the git repository (graph and branches)")
    args = ap.parse_args(argv)
    try:
        if args.command in ("list", "graph") and not os.path.isdir(args.repo):
            raise BadInput(f"--repo {args.repo} is not a folder")
        template = load_template(args.template)
        plans = load_plans(args.plans_dir, template)
        code = 0
        if args.command == "show":
            if not args.plan:
                raise BadInput("show needs --plan")
            code, lines = show(plans, args.plan, template, args.plans_dir)
        elif args.command == "list":
            lines = listing(plans, template, args.plans_dir, args.repo)
        else:
            lines = graph(plans, template, args.repo)
    except BadInput as e:
        print(f"plan.py: {e}", file=sys.stderr)
        return 2
    print("\n".join(lines))
    return code


if __name__ == "__main__":
    sys.exit(main())
