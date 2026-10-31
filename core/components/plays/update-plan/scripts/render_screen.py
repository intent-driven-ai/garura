#!/usr/bin/env python3
"""render_screen.py — print one screen of the session from the plan-update template (C10).

    python3 render_screen.py --screen <name> --template <plan-update.md> --view-template <plan-view.md> \
        --work <working folder> [--at 1,2] [--out <screen.txt>]

Screens and what each reads from the working folder:
  found, not_found   plan.json
  stopped, on_branch branch.json (on_branch adds the cut note when the branch was cut)
  taken              changes.yaml and taken.json: one line for each entry just added
  break, confirm     checked.json: the entries at --at (their place in it); confirm adds, for a new
                     feature, the thin-ICE warning and its slice in progress with the epic out of date
  question           checked.json: the questions at --at (all when --at is empty), in four parts
  list, empty        changes.yaml and --plan-file: the plan before and after the list (only the
                     touched items and the items above them), then what changed, one line each
  rejected           nothing (it asks what to change)
  aborted            branch.json (and whether the session cut the branch)
  resume             changes.yaml
  landed             commit.json, github-record.json, model-record.json, plan-write.json,
                     agreement.json, branch.json and changes.yaml
Every word comes from the template's settings block; the marks come from plan-view. The screen is
printed and, with --out, written. Exit 0 printed; 2 bad input (a missing record or setting).
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_session as ps  # noqa: E402


class Screens:
    def __init__(self, t, view, work, plan_file=None):
        self.t, self.work, self.plan_file = t, work, plan_file
        _, self.marks, _, self.icons = ps.statuses(view)

    def rec(self, name):
        path = os.path.join(self.work, name)
        if name.endswith(".yaml"):
            got = ps.load_list(path)
        else:
            got = ps.read_json(path, name) if os.path.isfile(path) else None
        if got is None:
            raise ps.Refused(f"{name} is not in the working folder")
        return got

    def opt(self, name):
        try:
            return self.rec(name)
        except ps.Refused:
            return None

    def ref(self, issue):
        if issue is None:
            return self.t["new_ref"]
        s = str(issue)
        return f"new {s[1:]}" if s.startswith("@") else f"#{s}"

    def what(self, e):
        w = self.t["what"].get(e["op"], "")
        frm, to = e.get("from"), e.get("to")
        if e["op"] == "move":
            return w.format(**{"from": frm, "to": str(to).lstrip("#")})
        return w.format(**{"from": frm, "to": to, "parent": str(e.get("parent")).lstrip("#")})

    def where(self, e):
        parts = []
        gh = [self.t["where"][k].format(type=ps.TYPES.get(e.get("kind"), "")) for k in e["where"]["github"]]
        md = [self.t["where"][k] for k in e["where"].get("model") or []]
        if md:
            parts.append(self.t["where_model"].format(items=self.t["where_join"].join(md)))
        if gh:
            parts.append(self.t["where_github"].format(items=self.t["where_join"].join(gh)))
        return self.t["where_sides_join"].join(parts)

    def row(self, e, n=None):
        mark = self.marks.get(e["to"] if e["op"] == "status" else e.get("status_now") or "Not Started", "")
        title = e.get("title") or ""
        width = self.t["title_width"]
        if len(title) > width:
            title = title[:width - 1] + self.t["title_cut"]
        issue = e.get("issue")
        lines = [self.t["row"].format(n=n if n is not None else e.get("n", ""), mark=mark, ref=self.ref(issue),
                                      title=title, what=self.what(e), where=self.where(e)).rstrip()]
        if e.get("override"):
            lines.append(self.t["under_line"].format(kind="override", text=e["override"]))
        if e.get("from_ice"):
            lines.append(self.t["under_line"].format(kind="model", text=self.t["from_ice_note"].format(
                feature=e.get("feature", ""))))
        if e.get("no_ice"):
            lines.append(self.t["under_line"].format(kind="model", text=self.t["no_ice_note"].format(
                feature=e.get("feature", ""), reason=e["no_ice"])))
        if e["op"] == "new-feature":
            for owed in ps.owed_of({"entries": [e]}):
                lines.append(self.t["under_line"].format(kind="owed", text=owed))
        return lines

    def plan_row(self, entries):
        changes = self.plan_changes(entries)
        return [self.t["plan_row"].format(changes=changes)] if changes else []

    def plan_changes(self, entries):
        bits = []
        for e in entries:
            if e["op"] == "plan-status":
                bits.append(self.t["plan_change"].format(field="Status", **{"from": e.get("from"), "to": e["to"]}))
            elif e["op"] == "plan-direction":
                def icon(v):
                    return self.icons.get(v, "none") if v is not None else "none"
                bits.append(self.t["plan_change"].format(field="Direction", **{"from": icon(e.get("from")),
                                                                              "to": icon(e["to"])}))
        return self.t["plan_join"].join(bits)

    # --- the screens ---

    def found(self, _):
        p = self.rec("plan.json")
        return self.t["found"].format(plan=p["plan"], title=p.get("title"), matched=p.get("matched", ""),
                                      where=p.get("where", ""))

    def not_found(self, _):
        p = self.rec("plan.json")
        cands = [self.t["candidate_line"].format(plan=c["plan"], title=c["title"]) for c in p.get("candidates") or []]
        return self.t["not_found"].format(description=p.get("asked", ""),
                                          candidates="\n".join(cands) or self.t["no_candidates"])

    def stopped(self, _):
        b = self.rec("branch.json")
        files = "\n".join(self.t["file_line"].format(file=f) for f in b.get("files") or [])
        return self.t["stopped"].format(branch=b.get("start_branch") or "this branch", files=files, plan=b["plan"])

    def on_branch(self, _):
        b = self.rec("branch.json")
        back = self.t["back_note"].format(back_to=b["back_to"]) if b.get("back_to") else ""
        text = self.t["on_branch"].format(plan=b["plan"], plan_branch=b["plan_branch"], back=back)
        if b.get("action") == "cut":
            text = self.t["cut_note"].format(plan=b["plan"], plan_branch=b["plan_branch"],
                                             commit=(b.get("main_commit") or "")[:7]) + "\n" + text
        return text

    def taken(self, _):
        ch, tk = self.rec("changes.yaml"), self.rec("taken.json")
        out = []
        for e in ch.get("entries") or []:
            if e["n"] in tk.get("taken") or []:
                if e["op"] in ("plan-status", "plan-direction"):
                    out.append(self.t["taken_plan"].format(changes=self.plan_changes([e])))
                else:
                    rows = self.row(e)
                    out.append(self.t["taken"].format(row=rows[0].strip()))
                    out += rows[1:]
        checked = self.opt("checked.json") or {}
        for left in tk.get("left") or []:
            if left.get("why") == "already so":
                e = (checked.get("entries") or [])[left["at"] - 1]
                what = e.get("to") if e["op"] != "plan-direction" else self.icons.get(e.get("to"), "none")
                out.append(self.t["already"].format(ref=self.ref(e.get("issue")) if e.get("issue") else "the plan",
                                                    what=f"is {what}" if e["op"] in ("status", "plan-status", "plan-direction") else "reads so"))
        return "\n".join(out)

    def picked(self, at):
        ch = self.rec("checked.json")["entries"]
        return [(i, ch[i - 1]) for i in at if 0 < i <= len(ch)]

    def break_(self, at):
        out = []
        for _, e in self.picked(at):
            parent = e.get("to") if e["op"] == "move" else e.get("parent")
            out.append(self.t["break"].format(ref=self.ref(e.get("issue")), title=e.get("title") or "",
                                              parent=self.ref(parent) if parent is not None else "the plan",
                                              problem=e["problem"], fix=e.get("fix") or "—"))
        return "\n\n".join(out)

    def confirm(self, at):
        out = []
        for i, e in self.picked(at):
            text = self.t["confirm"].format(row="\n".join(self.row(e, n=i)), why=e.get("big_why") or "")
            if e["op"] == "new-feature":
                notes = [self.t["thin_warning"]]
                busy = e.get("slice_in_progress") or []
                if busy:
                    epics = self.t["epic_join"].join(self.t["epic_line"].format(epic=self.ref(b.get("epic"))
                                                                                if str(b.get("epic")).isdigit()
                                                                                else b.get("epic"),
                                                                                status=b.get("status"))
                                                     for b in busy)
                    notes.append(self.t["slice_in_progress"].format(slice=e.get("slice"), epics=epics))
                head, _, ask = text.rpartition("\n")
                text = "\n".join([head] + notes + [ask])
            out.append(text)
        return "\n\n".join(out)

    def question(self, at):
        qs = self.rec("checked.json").get("questions") or []
        picked = [qs[i - 1] for i in at if 0 < i <= len(qs)] if at else qs
        out = []
        for q in picked:
            if not isinstance(q, dict):
                q = {"question": str(q)}
            examples = "\n".join(self.t["example_line"].format(example=x) for x in q.get("examples") or [])
            out.append(self.t["question"].format(question=q.get("question") or "",
                                                 answer=q.get("answer") or self.t["none"],
                                                 why=q.get("why") or self.t["none"],
                                                 examples=examples or self.t["example_line"].format(example=self.t["none"])))
        return "\n\n".join(out)

    def tree(self, plan, keep):
        """The plan's tree, only the touched items and the items above them, like /show-plan."""
        def walk(nodes, prefix):
            shown = [n for n in nodes or [] if str(n.get("issue")) in keep]
            out = []
            for i, n in enumerate(shown):
                last = i == len(shown) - 1
                ref = self.t["new_ref"] if str(n.get("issue")).startswith("@") else f"#{n.get('issue')}"
                line = self.t["tree_line"].format(mark=self.marks.get(n.get("status"), ""), ref=ref,
                                                  title=n.get("title") or "")
                out.append(prefix + (self.t["tree_last"] if last else self.t["tree_mid"]) + line)
                out += walk(n.get("children"), prefix + (self.t["tree_space"] if last else self.t["tree_pipe"]))
            return out
        return walk(plan.get("tree"), "")

    def change_text(self, e, after):
        c = self.t["change"]
        ref = self.ref(e.get("issue")) if e.get("issue") is not None else self.t["new_ref"]

        def where(v):
            return self.ref(v) if v is not None else "the top of the plan"
        if e["op"] == "status":
            text = c["status"][e["to"]].format(ref=ref)
        elif e["op"] == "add":
            key = "add_new" if e.get("issue") is None else "add_existing"
            text = c[key].format(ref=ref, kind=e.get("kind"), title=e.get("title"), parent=where(e.get("parent")))
        elif e["op"] == "new-feature" and e.get("issue") is not None:
            text = c["feature-of-story"].format(ref=ref, title=e.get("title"))
        elif e["op"] == "new-feature":
            text = c["new-feature"].format(title=e.get("title"), parent=where(e.get("parent")))
        elif e["op"] == "move":
            text = c["move"].format(ref=ref, to=where(e.get("to")))
        elif e["op"] == "plan-direction":
            to = e.get("to")
            text = c["plan-direction"].format(to=self.icons.get(to, self.t["no_direction"]) if to is not None
                                              else self.t["no_direction"])
        else:
            text = c[e["op"]].format(ref=ref, to=e.get("to"), summary=e.get("summary") or "")
        if e.get("override"):
            text += self.t["override_note"].format(override=e["override"])
        return text

    def list(self, _):
        ch = self.rec("changes.yaml")
        entries = ch.get("entries") or []
        if not entries:
            return self.t["empty"]
        if not self.plan_file:
            raise ps.Refused("the list screen needs --plan-file")
        import write_plan_changes as wpc
        before = ps.load_plan(self.plan_file)
        numbers = {}
        for e in entries:
            if e["op"] in ("add", "new-feature") and e.get("issue") is None:
                numbers[e["n"]] = numbers[f"@{e['n']}"] = f"@{e['n']}"
        after = wpc.data_apply(before, ch, numbers)
        touched = set()
        for e in entries:
            for v in (numbers.get(e["n"], e.get("issue")), e.get("parent"), e.get("to") if e["op"] == "move" else None,
                      e.get("from") if e["op"] == "move" else None):
                if v is not None:
                    touched.add(str(numbers.get(v, v)))

        def keep(plan):
            out = set()
            for node, _ in ps.walk(plan.get("tree")):
                if str(node.get("issue")) in touched:
                    at = node
                    while at is not None:
                        out.add(str(at.get("issue")))
                        at = ps.find(plan, at.get("issue"))[1]
            return out

        def direction(v):
            return self.icons.get(v, self.t["no_direction"]) if v is not None else self.t["no_direction"]
        out = [self.t["list_head"].format(plan=ch["plan"], title=ch.get("title")), ""]
        out.append(self.t["before_head"].format(status=before.get("status"), direction=direction(before.get("direction"))))
        out += self.tree(before, keep(before))
        out += ["", self.t["after_head"].format(status=after.get("status"), direction=direction(after.get("direction")))]
        out += self.tree(after, keep(after))
        out += ["", self.t["changed_head"]]
        out += [self.t["change_line"].format(n=e["n"], text=self.change_text(e, after)) for e in entries]
        out += ["", self.t["ask"]]
        return "\n".join(out)

    def empty(self, _):
        return self.t["empty"]

    def rejected(self, _):
        return self.t["rejected"]

    def aborted(self, _):
        b = self.rec("branch.json")
        undo = self.t["aborted_undo"].format(plan=b["plan"]) if b.get("action") == "cut" else ""
        return self.t["aborted"].format(undo=undo, back_to=b.get("back_to") or b.get("start_branch"))

    def resume(self, _):
        ch = self.rec("changes.yaml")
        return self.t["resume"].format(count=len(ch.get("entries") or []), at=ch.get("started"), plan=ch["plan"])

    def landed(self, _):
        ch, commit = self.rec("changes.yaml"), self.rec("commit.json")
        gh, model = self.opt("github-record.json") or {}, self.opt("model-record.json") or {}
        agree, branch = self.opt("agreement.json") or {}, self.opt("branch.json") or {}
        none = self.t["none"]
        counts = {}
        for d in (gh.get("done") or {}).values():
            if d.get("how") != "already":
                counts[d["op"]] = counts.get(d["op"], 0) + 1
        order = list(self.t["landed_counts"])
        github = self.t["landed_join"].join(self.t["landed_counts"][k].format(n=counts[k])
                                            for k in order if counts.get(k)) or none
        parts = model.get("parts") or []
        model_text = self.t["landed_model"].format(n=len(parts)) if parts else none
        plan_changes = self.t["landed_plan"].format(n=len(ch.get("entries") or []))
        check = self.t["check_ok"] if agree.get("ok") else "; ".join(agree.get("problems") or []) or none
        owed = ps.owed_of(ch)
        owed_text = self.t["landed_owed"].format(owed=self.t["owed_join"].join(owed)) if owed else ""
        back = self.t["landed_back"].format(back_to=branch["back_to"]) if branch.get("back_to") \
            else self.t["landed_stay"].format(plan_branch=ch.get("plan_branch"))
        return self.t["landed"].format(plan_branch=ch.get("plan_branch"), commit=(commit.get("commit") or "")[:7],
                                       model=model_text, github=github, plan_changes=plan_changes,
                                       check=check, owed=owed_text, back=back)


    def model(self, _):
        """The answer to a lookup in the product model (#1002): model-found.json, one record per ask."""
        out = []
        for r in self.rec("model-found.json").get("found") or []:
            ref = r.get("ref") or (f"#{r['story']}" if r.get("story") else "")
            if r.get("found"):
                pages = self.t["model_join"].join(r.get("ice_pages") or [])
                key = "model_found" if r.get("story") else "model_feature"
                out.append(self.t[key].format(story=r.get("story") or "", feature=r["feature"],
                                              one_line=r.get("one_line") or "", pages=pages))
            elif r.get("matches"):
                out.append(self.t["model_many"].format(ref=ref, matches=self.t["model_join"].join(r["matches"])))
            else:
                out.append(self.t["model_not_found"].format(ref=ref))
        return "\n".join(out)


SCREENS = {"found", "not_found", "stopped", "on_branch", "taken", "break", "confirm", "list", "empty",
           "rejected", "aborted", "resume", "landed", "question", "model"}


def main(argv=None):
    ap = argparse.ArgumentParser(description="print one screen of an /update-plan session")
    ap.add_argument("--screen", required=True, choices=sorted(SCREENS))
    ap.add_argument("--template", required=True)
    ap.add_argument("--view-template", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--at", default="")
    ap.add_argument("--plan-file", help="the plan file (the list screen draws it before and after)")
    ap.add_argument("--out")
    args = ap.parse_args(argv)
    try:
        s = Screens(ps.load_block(args.template, "plan-update"), ps.load_block(args.view_template, "plan-view"),
                    args.work, args.plan_file)
        at = [int(x) for x in args.at.split(",") if x.strip()]
        fn = getattr(s, "break_" if args.screen == "break" else args.screen)
        text = fn(at)
    except (ps.Refused, KeyError) as e:
        print(f"refused: {e}", file=sys.stderr)
        return 2
    if args.out:
        ps.write_text(args.out, text + "\n")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
