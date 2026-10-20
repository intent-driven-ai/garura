#!/usr/bin/env python3
"""Tests for the Shared Drive Run's scripts (drive-creator/references)."""
import contextlib
import io
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_play_done  # noqa: E402
import commit_run_files  # noqa: E402
import drive_preflight  # noqa: E402
import run_play_headless  # noqa: E402
import write_drive_contract  # noqa: E402

CONFIG = """\
stm:
  base-path: .garura/project/issues/
evidence:
  record: false
  plays:
    kickoff: true
drives:
  kickoff:
    runner: subagent
    checker:
      kind: coding-agent
      model: codex
"""


def quiet(fn, *args):
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return fn(*args)


class Work(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir, ignore_errors=True)

    def p(self, *parts):
        return os.path.join(self.dir, *parts)

    def write(self, rel, text):
        path = self.p(rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        return path

    def read_json(self, rel):
        with open(self.p(rel), encoding="utf-8") as fh:
            return json.load(fh)


class DrivePreflight(Work):
    def setUp(self):
        super().setUp()
        self.config = self.write("config.yaml", CONFIG)
        self.write("skills/intent/SKILL.md", "runs check_drive_contract.py first\n")
        self.write("skills/vision/SKILL.md", "runs check_drive_contract.py first\n")
        self.write("skills/shape/SKILL.md", "no contract here\n")

    def run_it(self, plays, config=None):
        return quiet(drive_preflight.main, ["--config", config or self.config, "--drive", "kickoff",
                                            "--skills-root", self.p("skills"), "--plays", plays,
                                            "--branch", "feature/7-x", "--out", self.p("pre.json")])

    def test_plays_present_and_ready_pass_with_the_drives_settings(self):
        self.assertEqual(self.run_it("intent,vision"), 0)
        facts = self.read_json("pre.json")
        self.assertTrue(facts["plays_ok"])
        self.assertEqual(facts["runner"], "subagent")
        self.assertEqual(facts["checker"], {"kind": "coding-agent", "model": "codex"})
        self.assertTrue(facts["evidence_record"])  # the drive's own switch beats the global off
        self.assertFalse(facts["on_default_branch"])

    def test_a_missing_play_halts(self):
        self.assertEqual(self.run_it("intent,understand"), 2)
        self.assertEqual(self.read_json("pre.json")["missing"], ["understand"])

    def test_a_play_that_checks_no_contract_halts(self):
        self.assertEqual(self.run_it("intent,shape"), 2)
        self.assertEqual(self.read_json("pre.json")["no_contract"], ["shape"])

    def test_defaults_when_the_config_names_no_drive(self):
        cfg = self.write("bare.yaml", "stm:\n  base-path: x/\n")
        self.assertEqual(self.run_it("intent", cfg), 0)
        facts = self.read_json("pre.json")
        self.assertEqual((facts["runner"], facts["checker"]["kind"]), ("subagent", "subagent"))
        self.assertTrue(facts["evidence_record"])

    def test_an_unknown_runner_halts(self):
        cfg = self.write("odd.yaml", CONFIG.replace("runner: subagent", "runner: telepathy"))
        self.assertEqual(self.run_it("intent", cfg), 2)


class WriteContract(Work):
    def run_it(self, *extra):
        return quiet(write_drive_contract.main, [
            "--drive", "kickoff", "--drive-run-id", "kickoff-1", "--branch", "feature/7-x",
            "--issue", "7", "--review-dir", "r/", "--plays", "intent,vision",
            "--out", self.p("c.json"), *extra])

    def test_a_contract_every_play_accepts(self):
        answers = self.write("a.json", json.dumps({"intent": {"who": "owner"}}))
        self.assertEqual(self.run_it("--answers", answers), 0)
        c = self.read_json("c.json")
        self.assertEqual(c["plays"], ["intent", "vision"])
        self.assertEqual(c["answers"]["intent"], {"who": "owner"})
        self.assertEqual(c["issue"], 7)

    def test_answers_for_a_play_the_drive_does_not_run_are_refused(self):
        answers = self.write("a.json", json.dumps({"intnet": {"who": "owner"}}))
        self.assertEqual(self.run_it("--answers", answers), 2)
        self.assertFalse(os.path.exists(self.p("c.json")))

    def test_a_play_block_that_is_not_an_object_is_refused(self):
        inputs = self.write("i.json", json.dumps({"vision": ["not", "an", "object"]}))
        self.assertEqual(self.run_it("--inputs", inputs), 2)


class PlayDone(Work):
    def run_it(self, not_before):
        return quiet(check_play_done.main, ["--verdict", self.p("sc.yaml"), "--not-before",
                                            str(not_before), "--out", self.p("done.json")])

    def test_held_and_fresh_is_done(self):
        self.write("sc.yaml", "stop_condition: held\nclauses: []\n")
        self.assertEqual(self.run_it(time.time() - 60), 0)
        self.assertTrue(self.read_json("done.json")["done"])

    def test_no_verdict_is_not_done(self):
        self.assertEqual(self.run_it(0), 1)

    def test_a_verdict_from_before_the_play_started_is_not_done(self):
        self.write("sc.yaml", "stop_condition: held\n")
        self.assertEqual(self.run_it(time.time() + 60), 1)

    def test_unmet_is_not_done(self):
        self.write("sc.yaml", "stop_condition: unmet\n")
        self.assertEqual(self.run_it(0), 1)

    def test_a_verdict_with_no_answer_cannot_be_read(self):
        self.write("sc.yaml", "something: else\n")
        self.assertEqual(self.run_it(0), 2)


class CommitRunFiles(Work):
    def setUp(self):
        super().setUp()
        self.old = os.getcwd()
        os.chdir(self.dir)
        self.addCleanup(os.chdir, self.old)
        for args in (["init", "-q", "-b", "feature/7-x"],
                     # Demo address: sample data for this throwaway repository, not personal data.
                     ["config", "user.email", "t@example.com"], ["config", "user.name", "test"]):
            subprocess.run(["git", *args], check=True, capture_output=True)
        self.write("README.md", "x\n")
        subprocess.run(["git", "add", "-A"], check=True, capture_output=True)
        subprocess.run(["git", "commit", "-q", "-m", "seed"], check=True, capture_output=True)

    def run_it(self, branch="feature/7-x"):
        return quiet(commit_run_files.main, ["--issue-dir", ".garura/project/issues/7/", "--issue", "7",
                                             "--branch", branch, "--play", "vision",
                                             "--out", self.p("out", "commit.json")])

    def log(self):
        return subprocess.run(["git", "log", "--format=%s"], capture_output=True, text=True).stdout

    def test_the_issue_folder_is_committed_and_the_tree_is_clean(self):
        self.write(".garura/project/issues/7/context/vision/run.json", "{}")
        self.write(".garura/project/issues/7/review/drive/vision.md", "x")
        os.makedirs(self.p("out"))
        with open(self.p(".git", "info", "exclude"), "a") as fh:
            fh.write("out/\n")
        self.assertEqual(self.run_it(), 0)
        self.assertIn("chore(stm): record vision run files (#7)", self.log())
        self.assertTrue(self.read_json("out/commit.json")["committed"])

    def test_nothing_to_commit_is_fine(self):
        with open(self.p(".git", "info", "exclude"), "a") as fh:
            fh.write("out/\n")
        self.assertEqual(self.run_it(), 0)
        self.assertFalse(self.read_json("out/commit.json")["committed"])

    def test_a_change_outside_the_issue_folder_is_left_and_halts(self):
        self.write(".garura/project/issues/7/context/x.json", "{}")
        self.write("product/page.md", "uncommitted model change")
        with open(self.p(".git", "info", "exclude"), "a") as fh:
            fh.write("out/\n")
        self.assertEqual(self.run_it(), 1)
        result = self.read_json("out/commit.json")
        self.assertTrue(result["committed"])
        self.assertEqual(result["leftover"], ["product/page.md"])

    def test_the_wrong_branch_commits_nothing(self):
        self.write(".garura/project/issues/7/context/x.json", "{}")
        self.assertEqual(self.run_it("feature/8-other"), 2)
        self.assertNotIn("record vision", self.log())

    def test_something_already_staged_is_never_swept_in(self):
        self.write("other.txt", "someone else's work")
        subprocess.run(["git", "add", "other.txt"], check=True)
        self.write(".garura/project/issues/7/context/x.json", "{}")
        self.assertEqual(self.run_it(), 2)
        self.assertNotIn("record vision", self.log())


class Headless(Work):
    def setUp(self):
        super().setUp()
        stand_in = self.write("fake-cli", "#!/bin/sh\nprintf '{\"session_id\": \"s1\", "
                              "\"is_error\": false, \"result\": \"%s\"}' \"$*\"\n")
        os.chmod(stand_in, os.stat(stand_in).st_mode | stat.S_IEXEC)
        self.old = run_play_headless.CLI
        run_play_headless.CLI = stand_in
        self.addCleanup(setattr, run_play_headless, "CLI", self.old)

    def test_it_starts_the_play_with_the_contract(self):
        code = quiet(run_play_headless.main, ["--play", "vision", "--contract", "c.json",
                                              "--out", self.p("run.json")])
        self.assertEqual(code, 0)
        run = self.read_json("run.json")
        self.assertEqual(run["session_id"], "s1")
        self.assertIn("/vision --contract c.json", run["result"])

    def test_it_resumes_the_same_session_with_the_answer(self):
        answer = self.write("answer.txt", "Shops pay a monthly fee.")
        code = quiet(run_play_headless.main, ["--play", "vision", "--resume", "s1",
                                              "--message-file", answer, "--out", self.p("run.json")])
        self.assertEqual(code, 0)
        self.assertIn("--resume s1", self.read_json("run.json")["result"])

    def test_resume_without_an_answer_is_refused(self):
        self.assertEqual(quiet(run_play_headless.main, ["--play", "vision", "--resume", "s1",
                                                        "--out", self.p("run.json")]), 2)


if __name__ == "__main__":
    unittest.main()
