"""Tests for remove_plans.py: plans go whole or not at all, and no file in a plan's folder is opened."""

import builtins
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "remove_plans.py")
sys.path.insert(0, HERE)
import remove_plans  # noqa: E402

PLAN = """\
# Plan {id} — a comment.
id: {id}
title: Plan number {id}
status: {status}
direction: 1
branch: {branch}  # a comment after the branch
needs_plans: {needs}
tree:
- issue: 1
  kind: epic
  title: An epic
  status: Done
  children:
  - issue: 2
    kind: story
    title: A story
    status: Done
  - issue: 3
    kind: story
    title: Another story
    status: In Progress
    children:
    - issue: 4
      kind: chore
      title: A chore
      status: Done
- issue: 5
  kind: epic
  title: A second epic
  status: Not Started
"""


class RemovePlansCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.parent = os.path.realpath(os.path.join(self.tmp.name, "project"))
        self.plans = os.path.join(self.parent, "plans")
        os.makedirs(self.plans)
        self.req = os.path.join(self.tmp.name, "request.json")
        self.out = os.path.join(self.tmp.name, "working", "report.json")
        self.plan(606)
        self.plan(717)
        self.plan(722)
        self.put("606/evals/eval.sl-1.md", "secret\n")
        self.put("606/evals/eval.fn-1.feature.md", "secret\n")
        self.put("606/guides/guide.md", "words\n")

    def plan(self, pid, status="Done", branch="null", needs="[]"):
        self.put(f"{pid}.yaml", PLAN.format(id=pid, status=status, branch=branch, needs=needs))

    def put(self, rel, text):
        path = os.path.join(self.plans, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)

    def locked(self, rel, mode=0):
        """Take every permission off a path, and give them back after the test if it still stands."""
        path = os.path.join(self.plans, rel)
        os.chmod(path, mode)
        self.addCleanup(lambda: os.path.exists(path) and os.chmod(path, 0o755))

    def tree(self):
        """Names and permissions of everything beside and under the plans folder, by name only."""
        out = {}
        for here, dirs, files in os.walk(self.parent):
            for name in dirs + files:
                path = os.path.join(here, name)
                out[os.path.relpath(path, self.parent)] = stat.S_IMODE(os.lstat(path).st_mode)
        return out

    def run_script(self, body):
        with open(self.req, "w", encoding="utf-8") as fh:
            json.dump(body, fh)
        return subprocess.run([sys.executable, SCRIPT, "--request", self.req, "--plans-dir", self.plans,
                               "--out", self.out], capture_output=True, text=True)

    def done(self, plans, **kw):
        body = {"by": "/test", "approved_by": "the product owner", "plans": plans}
        body.update(kw)
        r = self.run_script(body)
        self.assertEqual(r.returncode, 0, r.stderr)
        with open(self.out, encoding="utf-8") as fh:
            return json.load(fh)

    def assert_refused(self, body, *words):
        before = self.tree()
        r = self.run_script(body)
        self.assertEqual(r.returncode, 2, r.stdout)
        self.assertIn("refused, nothing changed", r.stderr)
        self.assertNotIn("Traceback", r.stderr)
        for word in words:
            self.assertIn(word, r.stderr)
        self.assertEqual(self.tree(), before)
        self.assertFalse(os.path.exists(self.out))


class Removes(RemovePlansCase):
    def test_a_plan_file_and_its_folder_go_and_others_stay(self):
        self.done([606])
        self.assertFalse(os.path.exists(os.path.join(self.plans, "606.yaml")))
        self.assertFalse(os.path.exists(os.path.join(self.plans, "606")))
        self.assertTrue(os.path.exists(os.path.join(self.plans, "717.yaml")))

    def test_no_temporary_folder_is_left(self):
        self.done([606])
        self.assertEqual(os.listdir(self.parent), ["plans"])

    def test_the_report_row(self):
        rep = self.done([606])
        self.assertEqual(rep["by"], "/test")
        self.assertEqual(rep["approved_by"], "the product owner")
        self.assertEqual(rep["removed"], [{
            "id": 606, "title": "Plan number 606", "plan_status": "Done",
            "items": {"Done": 3, "In Progress": 1, "Not Started": 1},
            "folder_files": 3, "deleted": ["plans/606.yaml", "plans/606"]}])

    def test_a_plan_with_no_folder_counts_no_files(self):
        rep = self.done([717])
        self.assertEqual(rep["removed"][0]["folder_files"], 0)
        self.assertEqual(rep["removed"][0]["deleted"], ["plans/717.yaml"])

    def test_a_plan_with_no_tree_has_no_items(self):
        self.put("800.yaml", "id: 800\ntitle: Empty\nstatus: Not Started\nbranch: null\n")
        self.assertEqual(self.done([800])["removed"][0]["items"], {})

    def test_several_plans_in_one_request_and_digit_strings(self):
        rep = self.done([606, "717"])
        self.assertEqual([row["id"] for row in rep["removed"]], [606, 717])

    def test_a_plan_named_only_by_another_removed_plan_can_go(self):
        self.plan(800, needs="[717]")
        self.done([717, 800])
        self.assertFalse(os.path.exists(os.path.join(self.plans, "717.yaml")))

    def test_a_file_with_no_permissions_does_not_stop_it(self):
        self.locked("606/evals/eval.sl-1.md")
        rep = self.done([606])
        self.assertEqual(rep["removed"][0]["folder_files"], 3)
        self.assertFalse(os.path.exists(os.path.join(self.plans, "606")))

    def test_a_folder_with_no_permissions_does_not_stop_it(self):
        self.put("606/evals/inner/deep.md", "secret\n")
        self.locked("606/evals/inner")
        self.locked("606/evals")
        self.locked("606", 0o500)
        rep = self.done([606])
        self.assertEqual(rep["removed"][0]["folder_files"], 4)
        self.assertFalse(os.path.exists(os.path.join(self.plans, "606")))
        self.assertEqual(os.listdir(self.parent), ["plans"])

    def test_no_file_under_a_plans_folder_is_ever_opened(self):
        with open(self.req, "w", encoding="utf-8") as fh:
            json.dump({"approved_by": "the product owner", "plans": [606]}, fh)
        real_open, opened = builtins.open, []

        def watching(path, *args, **kw):
            opened.append(str(path))
            return real_open(path, *args, **kw)

        argv = ["remove_plans.py", "--request", self.req, "--plans-dir", self.plans, "--out", self.out]
        with mock.patch.object(sys, "argv", argv), mock.patch.object(builtins, "open", watching):
            self.assertEqual(remove_plans.main(), 0)
        folder = os.path.join(self.plans, "606") + os.sep
        self.assertEqual([p for p in opened if p.startswith(folder) or ".garura-remove-plans-" in p], [])
        self.assertTrue(opened)

    def test_a_link_in_a_folder_is_never_followed(self):
        outside = os.path.join(self.tmp.name, "outside")
        os.makedirs(outside)
        keep = os.path.join(outside, "keep.md")
        with open(keep, "w", encoding="utf-8") as fh:
            fh.write("stays\n")
        os.chmod(keep, 0o400)
        os.symlink(keep, os.path.join(self.plans, "606", "link.md"))
        os.symlink(outside, os.path.join(self.plans, "606", "link-folder"))
        rep = self.done([606])
        self.assertEqual(rep["removed"][0]["folder_files"], 5)
        self.assertTrue(os.path.exists(keep))
        self.assertEqual(stat.S_IMODE(os.stat(keep).st_mode), 0o400)


class Refusals(RemovePlansCase):
    def body(self, plans, who="the product owner"):
        return {"by": "/test", "approved_by": who, "plans": plans}

    def test_no_person(self):
        self.assert_refused({"plans": [606]}, "approved_by")
        self.assert_refused(self.body([606], "  "), "approved_by")

    def test_an_empty_list(self):
        self.assert_refused(self.body([]), "no plans")
        self.assert_refused({"approved_by": "x"}, "no plans")

    def test_an_id_that_is_not_digits(self):
        for bad in ("../606", "606/", "6x", "", -606, 6.5, True, None, [606], "٣"):
            self.assert_refused(self.body([bad]), "digits only")

    def test_one_bad_id_refuses_the_rest(self):
        self.assert_refused(self.body([606, "../717"]), "digits only")

    def test_the_same_plan_twice(self):
        self.assert_refused(self.body([606, "606"]), "606", "twice")

    def test_a_plan_with_no_file(self):
        self.assert_refused(self.body([606, 900]), "900")

    def test_a_folder_with_no_plan_file(self):
        self.put("900/evals/x.md", "secret\n")
        self.assert_refused(self.body([900]), "900")

    def test_a_plan_file_that_is_not_a_mapping(self):
        self.put("900.yaml", "- a\n- list\n")
        self.assert_refused(self.body([900]), "900", "mapping")

    def test_a_plan_file_that_does_not_parse(self):
        self.put("900.yaml", "a: [unclosed\n")
        self.assert_refused(self.body([900]), "900.yaml")

    def test_a_plan_on_a_branch(self):
        self.plan(800, branch="plan/800/base")
        self.assert_refused(self.body([606, 800]), "800", "plan/800/base")

    def test_a_plan_that_stays_and_needs_one_being_removed(self):
        self.plan(800, needs="[606]")
        self.assert_refused(self.body([606]), "800", "606", "needs")

    def test_a_plan_that_stays_and_cannot_be_read(self):
        self.put("800.yaml", "a: [unclosed\n")
        self.assert_refused(self.body([606]), "800.yaml")

    def test_a_file_in_the_folder_that_is_not_a_plan_does_not_matter(self):
        self.put("notes.yaml", "a: [unclosed\n")
        self.put("README.md", "words\n")
        self.done([606])
        self.assertTrue(os.path.exists(os.path.join(self.plans, "notes.yaml")))

    def test_a_request_that_is_not_an_object(self):
        self.assert_refused([606], "not a JSON object")

    def test_no_plans_folder(self):
        self.plans = os.path.join(self.parent, "nowhere")
        r = self.run_script(self.body([606]))
        self.assertEqual(r.returncode, 2)
        self.assertIn("no plans folder", r.stderr)


class MovesBack(RemovePlansCase):
    def blocked_out(self):
        blocker = os.path.join(self.tmp.name, "a-file")
        with open(blocker, "w", encoding="utf-8") as fh:
            fh.write("x")
        self.out = os.path.join(blocker, "report.json")

    def test_a_report_that_cannot_be_written_moves_everything_back(self):
        self.blocked_out()
        before = self.tree()
        r = self.run_script({"approved_by": "x", "plans": [606, 717]})
        self.assertEqual(r.returncode, 2)
        self.assertIn("everything is back", r.stderr)
        self.assertEqual(self.tree(), before)

    def test_permissions_are_put_back_as_they_were(self):
        self.put("606/evals/inner/deep.md", "secret\n")
        self.locked("606/evals/eval.sl-1.md", 0)
        self.locked("606/evals/inner", 0)
        self.locked("606", 0o500)
        before = self.tree()
        self.assertEqual(before["plans/606"], 0o500)
        self.assertEqual(before["plans/606/evals/eval.sl-1.md"], 0)
        self.assertEqual(before["plans/606/evals/inner"], 0)
        self.blocked_out()
        r = self.run_script({"approved_by": "x", "plans": [606]})
        self.assertEqual(r.returncode, 2)
        self.assertEqual(self.tree(), before)

    def test_a_delete_that_fails_moves_everything_back_and_takes_the_report_back(self):
        before = self.tree()
        with open(self.req, "w", encoding="utf-8") as fh:
            json.dump({"approved_by": "x", "plans": [606]}, fh)
        argv = ["remove_plans.py", "--request", self.req, "--plans-dir", self.plans, "--out", self.out]
        with mock.patch.object(sys, "argv", argv), \
                mock.patch.object(remove_plans.shutil, "rmtree", side_effect=OSError("stuck")), \
                mock.patch.object(sys, "stderr"):
            self.assertEqual(remove_plans.main(), 2)
        self.assertEqual(self.tree(), before)
        self.assertFalse(os.path.exists(self.out))

    def test_a_report_that_was_there_before_is_put_back(self):
        os.makedirs(os.path.dirname(self.out))
        with open(self.out, "w", encoding="utf-8") as fh:
            fh.write("an older report\n")
        with open(self.req, "w", encoding="utf-8") as fh:
            json.dump({"approved_by": "x", "plans": [606]}, fh)
        argv = ["remove_plans.py", "--request", self.req, "--plans-dir", self.plans, "--out", self.out]
        with mock.patch.object(sys, "argv", argv), \
                mock.patch.object(remove_plans.shutil, "rmtree", side_effect=OSError("stuck")), \
                mock.patch.object(sys, "stderr"):
            self.assertEqual(remove_plans.main(), 2)
        with open(self.out, encoding="utf-8") as fh:
            self.assertEqual(fh.read(), "an older report\n")

    def test_a_move_that_fails_part_way_moves_the_first_back(self):
        before = self.tree()
        real, calls = os.rename, []

        def flaky(source, target):
            calls.append(source)
            if len(calls) == 3:
                raise OSError("stuck")
            real(source, target)

        with mock.patch.object(os, "rename", flaky):
            with self.assertRaises(OSError):
                remove_plans.remove(self.plans, {"606": {}, "717": {}}, self.out, "x", "y")
        self.assertEqual(self.tree(), before)
        self.assertFalse(os.path.exists(self.out))


if __name__ == "__main__":
    unittest.main()
