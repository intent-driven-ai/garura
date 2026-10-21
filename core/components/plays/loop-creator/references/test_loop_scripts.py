#!/usr/bin/env python3
"""Tests for the Shared Loop Run's scripts (loop-creator/references)."""
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
import prepare_check  # noqa: E402
import record_check  # noqa: E402
import round_state  # noqa: E402
import run_checker_codex  # noqa: E402
import loop_preflight  # noqa: E402
import loop_status  # noqa: E402
import run_play_headless  # noqa: E402
import write_loop_contract  # noqa: E402

CONFIG = """\
stm:
  base-path: .garura/project/issues/
evidence:
  record: false
  plays:
    discovery: true
loops:
  discovery:
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
        self.write("skills/intent/SKILL.md", "runs check_loop_contract.py first\n")
        self.write("skills/vision/SKILL.md", "runs check_loop_contract.py first\n")
        self.write("skills/shape/SKILL.md", "no contract here\n")
        for member in ("search-knowledge", "build-knowledge", "review-knowledge"):
            self.write(f"skills/{member}/SKILL.md", "runs check_loop_contract.py first\n")

    def run_it(self, plays, config=None):
        return quiet(loop_preflight.main, ["--config", config or self.config, "--loop", "discovery",
                                            "--skills-root", self.p("skills"), "--plays", plays,
                                            "--branch", "feature/7-x", "--out", self.p("pre.json")])

    def test_plays_present_and_ready_pass_with_the_loops_settings(self):
        self.assertEqual(self.run_it("intent,vision"), 0)
        facts = self.read_json("pre.json")
        self.assertTrue(facts["plays_ok"])
        self.assertEqual(facts["runner"], "subagent")
        self.assertEqual(facts["checker"], {"kind": "coding-agent", "model": "codex"})
        self.assertTrue(facts["evidence_record"])  # the loop's own switch beats the global off
        self.assertFalse(facts["on_default_branch"])

    def test_a_missing_member_play_halts(self):
        os.remove(self.p("skills", "review-knowledge", "SKILL.md"))
        self.assertEqual(self.run_it("intent,vision"), 2)
        self.assertEqual(self.read_json("pre.json")["missing"], ["review-knowledge"])

    def test_a_missing_play_halts(self):
        self.assertEqual(self.run_it("intent,understand"), 2)
        self.assertEqual(self.read_json("pre.json")["missing"], ["understand"])

    def test_a_play_that_checks_no_contract_halts(self):
        self.assertEqual(self.run_it("intent,shape"), 2)
        self.assertEqual(self.read_json("pre.json")["no_contract"], ["shape"])

    def test_defaults_when_the_config_names_no_loop_but_the_checker_model_is_asked_for(self):
        cfg = self.write("bare.yaml", "stm:\n  base-path: x/\n")
        self.assertEqual(self.run_it("intent", cfg), 2)
        facts = self.read_json("pre.json")
        self.assertEqual((facts["runner"], facts["checker"]["kind"]), ("subagent", "subagent"))
        self.assertTrue(facts["evidence_record"])
        self.assertTrue(any("checker.model" in p for p in facts["problems"]))

    def test_an_unknown_runner_halts(self):
        cfg = self.write("odd.yaml", CONFIG.replace("runner: subagent", "runner: telepathy"))
        self.assertEqual(self.run_it("intent", cfg), 2)


class DriveStatus(Work):
    """The loop presents its status in one file; a display reads it (run-status.md)."""

    def test_the_first_call_names_the_run_and_later_calls_update_it(self):
        f = self.p("status", "run-discovery.json")
        self.assertEqual(quiet(loop_status.main, ["--file", f, "--name", "discovery", "--issue", "7",
                                                   "--run-id", "discovery-1", "--round", "1",
                                                   "--play", "intent", "--step", "walking the prototype"]), 0)
        first = self.read_json("status/run-discovery.json")
        self.assertEqual((first["state"], first["play"], first["round"]), ("running", "intent", 1))
        self.assertEqual(quiet(loop_status.main, ["--file", f, "--play", "vision", "--step", "seeding"]), 0)
        later = self.read_json("status/run-discovery.json")
        self.assertEqual((later["name"], later["play"], later["round"]), ("discovery", "vision", 1))
        self.assertEqual(later["started_at"], first["started_at"])
        self.assertEqual([n for n in os.listdir(self.p("status")) if n.startswith(".")], [])

    def test_a_first_call_without_the_run_is_refused(self):
        self.assertEqual(quiet(loop_status.main, ["--file", self.p("s.json"), "--step", "x"]), 2)

    def test_an_unknown_state_is_refused(self):
        with self.assertRaises(SystemExit):
            quiet(loop_status.main, ["--file", self.p("s.json"), "--name", "k", "--run-id", "k-1",
                                      "--state", "sleeping"])


class WriteContract(Work):
    def run_it(self, *extra):
        return quiet(write_loop_contract.main, [
            "--loop", "discovery", "--loop-run-id", "discovery-1", "--branch", "feature/7-x",
            "--issue", "7", "--review-dir", "r/", "--plays", "intent,vision",
            "--out", self.p("c.json"), *extra])

    def test_a_contract_every_play_accepts(self):
        answers = self.write("a.json", json.dumps({"intent": {"who": "owner"}}))
        self.assertEqual(self.run_it("--answers", answers), 0)
        c = self.read_json("c.json")
        self.assertEqual(c["plays"], ["intent", "vision"])
        self.assertEqual(c["answers"]["intent"], {"who": "owner"})
        self.assertEqual(c["issue"], 7)

    def test_the_round_is_carried(self):
        self.assertEqual(self.run_it("--round", "2"), 0)
        self.assertEqual(self.read_json("c.json")["round"], 2)

    def test_answers_for_a_play_the_loop_does_not_run_are_refused(self):
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


class GitWork(Work):
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


class CommitRunFiles(GitWork):
    def run_it(self, branch="feature/7-x"):
        return quiet(commit_run_files.main, ["--issue-dir", ".garura/project/issues/7/", "--issue", "7",
                                             "--branch", branch, "--play", "vision",
                                             "--out", self.p("out", "commit.json")])

    def log(self):
        return subprocess.run(["git", "log", "--format=%s"], capture_output=True, text=True).stdout

    def test_the_issue_folder_is_committed_and_the_tree_is_clean(self):
        self.write(".garura/project/issues/7/context/vision/run.json", "{}")
        self.write(".garura/project/issues/7/review/loop/vision.md", "x")
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

    def test_the_round_commits_the_model_with_the_run_files(self):
        self.write(".garura/project/issues/7/context/discovery/gaps.json", "{}")
        self.write("product/product-os/_spine.yaml", "domains: []\n")
        with open(self.p(".git", "info", "exclude"), "a") as fh:
            fh.write("out/\n")
        code = quiet(commit_run_files.main, ["--issue-dir", ".garura/project/issues/7/", "--issue", "7",
                                             "--branch", "feature/7-x", "--play", "round-1",
                                             "--also", "product/product-os", "--out", self.p("out", "commit.json")])
        self.assertEqual(code, 0)
        self.assertIn("chore(stm): record round-1 round (#7)", self.log())
        self.assertEqual(self.read_json("out/commit.json")["leftover"], [])

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

    def test_it_hands_the_play_its_argument(self):
        code = quiet(run_play_headless.main, ["--play", "intent", "--contract", "c.json", "--argument",
                                              "https://shop.example.com", "--out", self.p("run.json")])
        self.assertEqual(code, 0)
        self.assertIn("/intent --contract c.json https://shop.example.com", self.read_json("run.json")["result"])

    def test_it_resumes_the_same_session_with_the_answer(self):
        answer = self.write("answer.txt", "Shops pay a monthly fee.")
        code = quiet(run_play_headless.main, ["--play", "vision", "--resume", "s1",
                                              "--message-file", answer, "--out", self.p("run.json")])
        self.assertEqual(code, 0)
        self.assertIn("--resume s1", self.read_json("run.json")["result"])

    def test_resume_without_an_answer_is_refused(self):
        self.assertEqual(quiet(run_play_headless.main, ["--play", "vision", "--resume", "s1",
                                                        "--out", self.p("run.json")]), 2)


class RoundState(GitWork):
    """After a round: done, again, or ask (the loop loops; a question is the loop's)."""

    def setUp(self):
        super().setUp()
        self.write("product/model.md", "v1\n")
        subprocess.run(["git", "add", "-A"], check=True, capture_output=True)
        subprocess.run(["git", "commit", "-q", "-m", "model"], check=True, capture_output=True)
        os.makedirs(self.p("rev"), exist_ok=True)
        os.makedirs(self.p("issue", "review", "memory-updates"), exist_ok=True)

    def open_q(self, *ids):
        self.write("rev/open-intent.json", json.dumps({"play": "intent", "questions": [
            {"id": i, "ask": f"question {i}", "for_person": True} for i in ids]}))

    def decide(self, rnd, max_rounds=3, report=None, gaps=None):
        extra = []
        if report is not None:
            self.write(f"work/close-report-{rnd}.json", json.dumps(report))
            extra += ["--close-report", f"work/close-report-{rnd}.json"]
        if gaps is not None:
            self.write(f"work/gaps-{rnd}.json", json.dumps(gaps))
            extra += ["--gaps", f"work/gaps-{rnd}.json"]
        quiet(round_state.main, ["--round", str(rnd), "--max-rounds", str(max_rounds), "--working", "work",
                                 "--review-dir", "rev", "--issue-dir", "issue", "--model-path", "product",
                                 *extra, "--out", f"work/round-{rnd}.json"])
        return self.read_json(f"work/round-{rnd}.json")

    def commit_model(self, text):
        self.write("product/model.md", text)
        subprocess.run(["git", "commit", "-qam", "model moved"], check=True, capture_output=True)

    def test_no_open_question_is_done(self):
        self.assertEqual(self.decide(1)["decision"], "done")

    def test_a_round_that_moved_goes_again(self):
        self.open_q("who", "proof")
        self.assertEqual(self.decide(1)["decision"], "again")
        self.commit_model("v2\n")
        self.open_q("proof")
        self.assertEqual(self.decide(2)["decision"], "again")

    def test_a_round_that_moved_nothing_asks_the_person(self):
        self.open_q("who")
        self.decide(1)
        self.assertEqual(self.decide(2)["decision"], "ask")

    def test_the_round_limit_asks(self):
        self.open_q("who")
        self.decide(1)
        self.commit_model("v2\n")
        self.assertEqual(self.decide(2, max_rounds=2)["decision"], "ask")

    def test_work_left_for_a_play_goes_again_on_exactly_that_work(self):
        rec = self.decide(1, report={"work_for_plays": [{"play": "/understand", "target": "cap-board"}]})
        self.assertEqual(rec["decision"], "again")
        self.assertEqual(rec["next"], {"/understand": ["cap-board"]})
        self.assertEqual(rec["gaps_left"], 1)

    def test_an_uncovered_screen_is_not_done(self):
        rec = self.decide(1, gaps={"uncovered": [{"what": "main section", "name": "Reports"}]}, report={})
        self.assertNotEqual(rec["decision"], "done")

    def test_closed_gaps_and_no_question_is_done(self):
        rec = self.decide(1, gaps={"work": [], "uncovered": []}, report={"work_for_plays": []})
        self.assertEqual(rec["decision"], "done")

    def test_the_same_gaps_twice_asks_the_person(self):
        report = {"work_for_plays": [{"play": "/vision", "target": "cap-x"}]}
        self.decide(1, report=report)
        self.assertEqual(self.decide(2, report=report)["decision"], "ask")

    def test_a_pending_memory_update_is_an_open_question(self):
        self.write("issue/review/memory-updates/mu-1.json", json.dumps({"update": {
            "id": "mu-1", "status": "waiting", "missing": "how long is a cart kept?"}}))
        self.write("issue/review/memory-updates/mu-2.json", json.dumps({"update": {"id": "mu-2", "status": "applied"}}))
        rec = self.decide(1)
        self.assertEqual([q["id"] for q in rec["open"]], ["mu-1"])
        self.assertEqual(self.read_json("work/rounds.json")["open_left"], 1)


ICE = """# ICE — t

## Intent

**Goal:** turn a statement into a seeded domain.

### Constraints

- C1 — One issue and one branch.
- C2 — Questions first.

### Failure conditions

- F1 — Wrote outside the issue.

## Expectation

### Done means

- D1 — the contract exists.
"""


class PrepareCheck(GitWork):
    def setUp(self):
        super().setUp()
        self.base = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        self.write("product/domain.md", "# Shop\n")
        self.write(".garura/project/issues/7/review/loop/vision-1.md", "review record")
        self.write(".garura/project/issues/7/context/run.json", "{}")
        self.write("work/answers.json", "{}")
        self.write("work/intent-done.json", '{"done": true}')
        subprocess.run(["git", "add", "-A"], check=True, capture_output=True)
        subprocess.run(["git", "commit", "-q", "-m", "loop"], check=True, capture_output=True)
        self.ice = self.write("ice.md", ICE)

    def test_the_bundle_holds_the_criteria_and_the_outputs_only(self):
        code = quiet(prepare_check.main, ["--ice", self.ice, "--issue", "7", "--issue-dir",
                                          ".garura/project/issues/7/", "--working", "work",
                                          "--base", self.base, "--memory-tool", "none.py",
                                          "--out-dir", "work/check"])
        self.assertEqual(code, 0)
        m = self.read_json("work/check/manifest.json")
        self.assertEqual(m["criteria_ids"], ["G", "C1", "C2", "D1"])
        with open(self.p("work/check/change.diff")) as fh:
            diff = fh.read()
        self.assertIn("product/domain.md", diff)
        self.assertNotIn("issues/7/", diff)  # the loop's own run records are not the change
        self.assertTrue(os.path.isfile(self.p("work/check/review/vision-1.md")))
        self.assertTrue(os.path.isfile(self.p("work/check/done/intent-done.json")))
        self.assertIn("decision-trace check", m["missing"])
        self.assertIn("answers-sources.json", m["missing"])

    def test_an_ice_with_no_goal_is_nothing_to_judge(self):
        ice = self.write("bad.md", "# ICE\n\n## Intent\n\nno goal\n")
        self.assertEqual(quiet(prepare_check.main, ["--ice", ice, "--issue", "7", "--issue-dir", "x/",
                                                    "--working", "work", "--base", self.base,
                                                    "--out-dir", "work/check"]), 2)


class RecordCheck(Work):
    def setUp(self):
        super().setUp()
        self.manifest = self.write("manifest.json", json.dumps({"criteria_ids": ["G", "C1"]}))

    def run_it(self, verdict):
        path = self.write("verdict.json", json.dumps(verdict))
        return quiet(record_check.main, ["--verdict", path, "--manifest", self.manifest, "--kind",
                                         "subagent", "--model", "sonnet", "--out", self.p("check.yaml")])

    def crit(self, g="pass", c1="pass"):
        return [{"id": "G", "result": g, "evidence": "change.diff: adds the domain"},
                {"id": "C1", "result": c1, "evidence": "change.diff: all under issues/7/"}]

    def test_a_pass_is_recorded(self):
        self.assertEqual(self.run_it({"verdict": "pass", "criteria": self.crit(), "reasons": []}), 0)
        with open(self.p("check.yaml")) as fh:
            text = fh.read()
        self.assertIn("verdict: pass", text)
        self.assertIn("model: \"sonnet\"", text)

    def test_a_reject_is_recorded_and_halts(self):
        v = {"verdict": "reject", "criteria": self.crit(c1="fail"), "reasons": ["C1: writes outside"]}
        self.assertEqual(self.run_it(v), 1)
        with open(self.p("check.yaml")) as fh:
            self.assertIn('failed: ["C1"]', fh.read())

    def test_a_pass_with_a_failed_criterion_is_never_a_pass(self):
        self.assertEqual(self.run_it({"verdict": "pass", "criteria": self.crit(c1="fail"), "reasons": []}), 2)
        self.assertFalse(os.path.exists(self.p("check.yaml")))

    def test_a_criterion_not_judged_is_never_a_pass(self):
        self.assertEqual(self.run_it({"verdict": "pass", "criteria": self.crit()[:1], "reasons": []}), 2)

    def test_a_reject_without_reasons_is_refused(self):
        self.assertEqual(self.run_it({"verdict": "reject", "criteria": self.crit(g="fail"), "reasons": []}), 2)

    def test_no_evidence_is_refused(self):
        crit = self.crit()
        crit[0]["evidence"] = " "
        self.assertEqual(self.run_it({"verdict": "pass", "criteria": crit, "reasons": []}), 2)


class CodexChecker(Work):
    def setUp(self):
        super().setUp()
        skill_dir = os.path.join(HERE, "..", "..", "..", "skills", "judge-loop-result")
        self.skill = os.path.join(skill_dir, "SKILL.md")
        # a stand-in Codex: records its arguments and stdin, writes the verdict to -o's path
        stand_in = self.write("fake-codex", "#!/bin/sh\n"
                              "echo \"$@\" > \"$(dirname \"$0\")/args.txt\"\n"
                              "cat > \"$(dirname \"$0\")/prompt.txt\"\n"
                              "while [ $# -gt 0 ]; do [ \"$1\" = --output-last-message ] && out=$2; shift; done\n"
                              "printf '{\"verdict\": \"pass\"}' > \"$out\"\n")
        os.chmod(stand_in, os.stat(stand_in).st_mode | stat.S_IEXEC)
        self.old = run_checker_codex.CLI
        run_checker_codex.CLI = stand_in
        self.addCleanup(setattr, run_checker_codex, "CLI", self.old)
        os.makedirs(self.p("check"))

    def test_codex_runs_read_only_on_the_bundle_with_the_schema(self):
        code = quiet(run_checker_codex.main, ["--bundle", self.p("check"), "--skill", self.skill,
                                              "--model", "gpt-5", "--out", self.p("check", "verdict.json")])
        self.assertEqual(code, 0)
        with open(self.p("args.txt")) as fh:
            args = fh.read()
        for part in ("exec", "--sandbox read-only", f"--cd {self.p('check')}", "verdict.schema.json",
                     "--model gpt-5"):
            self.assertIn(part, args)
        with open(self.p("prompt.txt")) as fh:
            prompt = fh.read()
        self.assertIn("No evidence, no pass.", prompt)
        self.assertNotIn("user-invocable", prompt)  # the skill's frontmatter is not the prompt

    def test_no_answer_is_an_error(self):
        broken = self.write("silent-codex", "#!/bin/sh\nexit 1\n")
        os.chmod(broken, os.stat(broken).st_mode | stat.S_IEXEC)
        run_checker_codex.CLI = broken
        self.assertEqual(quiet(run_checker_codex.main, ["--bundle", self.p("check"), "--skill", self.skill,
                                                        "--out", self.p("check", "verdict.json")]), 2)


if __name__ == "__main__":
    unittest.main()
