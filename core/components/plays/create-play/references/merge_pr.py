#!/usr/bin/env python3
"""
merge_pr.py — merge-change Step 3 as a script (#484).

Merges the PR, switches to main and pulls, deletes the feature branch (local +
remote), finalizes merge-gate.json's two Done-means booleans — and then COMMITS
the run records on main itself (#491): the play's C6 always required that
commit, but as prose it got skipped and left merge-gate.json littering the tree.
The script that writes the record commits it, on BOTH paths (fresh merge and the
already-merged no-op) — and then PUSHES the records commit (#493): the pinned
Confirm Merge approval already put the human on the outward act, so the
bookkeeping push rides on that authorization, no second ask. A failed push is
reported visibly (records_pushed: false) with the push left owed — never silent.
Zero judgment — a fixed sequence gated on the mergeable read.

Plans (#673): --base is the target resolve_target.py gave — the plan branch for an
issue in a plan, main otherwise. Before merging, the PR's own base must equal it
(`on_target`), or nothing is merged. With --close-issue (an issue in a plan), the
issue is closed after the merge, because the code host closes issues only on main;
with --plans-dir and --plan-id, its capability is closed too once every issue under
it is closed.

    python3 merge_pr.py --config .garura/core/config.yaml \
        --branch <feature-branch> --base main \
        --gate <merge-gate.json> \
        [--issue N --records-dir <review/>]   # enables the records self-commit

The records self-commit runs only when BOTH --issue and --records-dir are given
(the compiled play always passes them; tests may omit). The printed result
carries `records_committed: true|false|null` (null = self-commit not requested)
and `records_pushed: true|false|null` (null = no commit to push / not requested)
so a leftover or an unpushed record is a visible state, never silent.

Idempotent: if the PR is already merged (gate.already_merged), it is a clean
no-op — no second merge is attempted; the records commit still runs.

Exit 0 merged or clean no-op; 1 on a merge/verify failure.
"""

import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import platform_adapter as pa  # noqa: E402

# The installed plan tool that sets one item's status from its own issue (#1007).
PLAN_TOOL = ".garura/core/tools/plan/plan_status.py"


def _git(*args, check=False):
    proc = subprocess.run(["git", *args], capture_output=True, text=True)
    if check and proc.returncode != 0:
        sys.stderr.write(f"merge_pr.py: git {' '.join(args)} failed: {proc.stderr}\n")
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def _branch_gone(branch):
    rc_l, out_l, _ = _git("branch", "--list", branch)
    local_gone = not out_l.strip()
    rc_r, out_r, _ = _git("ls-remote", "--heads", "origin", branch)
    remote_gone = not out_r.strip()
    return local_gone and remote_gone


def _commit_records(gate_path, records_dir, issue, plan_file=None):
    """Stage the gate file + the records dir (+ the plan file whose item was marked Done)
    and commit (#491). No push. Returns True when the records are committed (including
    'nothing to commit' — already clean counts as committed), False when the commit failed."""
    _git("add", gate_path)
    if records_dir and os.path.isdir(records_dir):
        _git("add", records_dir)
    if plan_file and os.path.isfile(plan_file):
        _git("add", plan_file)
    rc, out, err = _git("diff", "--cached", "--quiet")
    if rc == 0:
        return True  # nothing staged — records already committed, tree clean
    rc, _, err = _git("commit", "-m",
                      f"chore(stm): record merge-change run records (#{issue})")
    if rc != 0:
        sys.stderr.write(f"merge_pr.py: records commit failed: {err}\n")
        return False
    return True


def _pr_base(config, pr_number):
    """The PR's base branch on the host, or None when it cannot be read."""
    view = pa.dispatch("view-pr", {"pr_number": pr_number}, config_path=config)
    if view["exit_code"] == 0 and view["stdout"].strip():
        try:
            return json.loads(view["stdout"]).get("baseRefName")
        except ValueError:
            return None
    return None


def _close_landed(ns):
    """Close an issue that landed on its plan branch (and its capability once every issue
    under it is closed). An issue already closed is left as it is, so a re-run is safe."""
    closed = []
    if not ns.close_issue:
        return closed
    import resolve_target as rt
    if rt.tracker_state(str(ns.close_issue), ns.config, None) != "CLOSED":
        res = pa.dispatch("close-issue", {"issue_number": ns.close_issue,
                                          "comment": f"Landed on {ns.base} (merge-change)."},
                          config_path=ns.config)
        if res["exit_code"] == 0:
            closed.append(str(ns.close_issue))
    if ns.plans_dir and ns.plan_id:
        closed += _close_finished_capability(ns, str(ns.close_issue))
    return closed


def _mark_done(ns):
    """Set the landed issue's item Done in its plan file (#1007): an item's status follows
    its own issue. Only that item changes; nothing rolls up. Returns the tool's record, or
    None when the issue sits in no plan."""
    if not (ns.close_issue and ns.plans_dir and ns.plan_id):
        return None
    res = subprocess.run([sys.executable, ns.plan_tool, "--plans-dir", ns.plans_dir,
                          "--plan", str(ns.plan_id), "--issue", str(ns.close_issue),
                          "--status", "Done"], capture_output=True, text=True)
    if res.returncode != 0:
        return {"error": res.stderr.strip() or f"exit {res.returncode}"}
    return json.loads(res.stdout)


def _close_finished_capability(ns, issue):
    """Close the capability over `issue` when every issue under it is closed (#673)."""
    import resolve_target as rt
    try:
        plan = rt.load_plan(ns.plans_dir, ns.plan_id)
    except (OSError, ValueError):
        return []
    for cap in plan.get("tree") or []:
        kids = [str(i) for i in rt.work_issues(cap.get("children"))]
        if issue in kids and cap.get("issue") is not None:
            if rt.tracker_state(str(cap["issue"]), ns.config, None) == "CLOSED":
                return []
            if all(rt.tracker_state(i, ns.config, None) == "CLOSED" for i in kids):
                res = pa.dispatch("close-issue", {"issue_number": cap["issue"],
                                                  "comment": "Every issue under it has landed."},
                                  config_path=ns.config)
                return [str(cap["issue"])] if res["exit_code"] == 0 else []
    return []


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=".garura/core/config.yaml")
    ap.add_argument("--branch", required=True)
    ap.add_argument("--base", default="main")
    ap.add_argument("--gate", required=True)
    ap.add_argument("--issue", default=None)
    ap.add_argument("--records-dir", default=None)
    ap.add_argument("--close-issue", default=None)
    ap.add_argument("--plans-dir", default=None)
    ap.add_argument("--plan-id", default=None)
    ap.add_argument("--plan-tool", default=PLAN_TOOL)
    ns = ap.parse_args(argv)
    plan_file = (os.path.join(ns.plans_dir, f"{ns.plan_id}.yaml")
                 if ns.plans_dir and ns.plan_id else None)

    with open(ns.gate, encoding="utf-8") as fh:
        gate = json.load(fh)
    pr_number = str(gate.get("pr_number") or "")
    want_records = bool(ns.issue and ns.records_dir)

    def finalize(pr_merged, branch_deleted, extra=None):
        """Write the final gate file, run the records self-commit (#491) and the
        records push (#493) when requested, and print the result with
        records_committed + records_pushed."""
        gate["pr_merged"] = pr_merged
        gate["branch_deleted"] = branch_deleted
        if extra:
            gate.update(extra)
            if extra.get("status") in {"merged", "already_merged"}:
                gate.pop("error", None)
        with open(ns.gate, "w", encoding="utf-8") as fh:
            json.dump(gate, fh, indent=2)
        committed = (_commit_records(ns.gate, ns.records_dir, ns.issue, plan_file)
                     if want_records else None)
        pushed = None
        if committed is True:
            # #493: the pinned merge approval covers this push — no second ask.
            # Soft-fail: a failed push is reported, the push stays owed, and the
            # merge outcome still decides the exit code.
            rc, _, perr = _git("push", "origin", ns.base)
            pushed = rc == 0
            if not pushed:
                sys.stderr.write(f"merge_pr.py: records push failed (left owed): "
                                 f"{perr}\n")
        print(json.dumps({**gate, "records_committed": committed,
                          "records_pushed": pushed}, indent=2))
        return committed

    # Clean no-op: already merged (C5/F5). Confirm the branch is gone; don't
    # re-merge. The records self-commit still runs — the no-op path is exactly
    # where leftovers were observed (#491).
    if gate.get("already_merged"):
        base = _pr_base(ns.config, pr_number) if pr_number else None
        if base == ns.base:
            # A first run may have merged and stopped before closing the issue: close it now.
            gate["issues_closed"] = _close_landed(ns)
            gate["plan_marked"] = _mark_done(ns)
        committed = finalize(True, _branch_gone(ns.branch),
                             {"status": "already_merged", "on_target": base == ns.base})
        sys.exit(0 if committed in (True, None) else 1)

    if not pr_number:
        sys.stderr.write("merge_pr.py: no pr_number in gate — cannot merge\n")
        sys.exit(1)

    # The PR must land where its branch belongs (#673): its base equals the target.
    pr_base = _pr_base(ns.config, pr_number)
    gate["on_target"] = pr_base == ns.base
    if not gate["on_target"]:
        finalize(False, False, {"status": "wrong_target",
                                "error": f"PR base is {pr_base!r}, but this branch lands on {ns.base!r}"})
        sys.exit(1)

    # Merge via the adapter (repository default strategy).
    res = pa.dispatch("merge-pr", {"pr_number": pr_number}, config_path=ns.config)
    if res["exit_code"] != 0:
        finalize(False, False, {"status": "merge_failed", "error": res["stderr"]})
        sys.exit(1)

    # Switch to base + pull latest.
    _git("checkout", ns.base, check=True)
    _git("pull", "--ff-only", "origin", ns.base)

    # Delete the feature branch — local (safe delete) then remote (best-effort).
    _git("branch", "-D", ns.branch)
    _git("push", "origin", "--delete", ns.branch)  # some hosts auto-delete → no-op

    branch_deleted = _branch_gone(ns.branch)

    # An issue in a plan lands on its plan branch, where the host does not close it.
    gate["issues_closed"] = _close_landed(ns)
    gate["plan_marked"] = _mark_done(ns)
    # Verify we landed on updated base.
    _, cur, _ = _git("branch", "--show-current")
    on_base = cur == ns.base
    committed = finalize(True, branch_deleted,
                         {"status": "merged", "on_base": on_base,
                          "merge_sha": None})
    ok = branch_deleted and on_base and committed in (True, None)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
