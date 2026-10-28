#!/usr/bin/env python3
"""Tests for the Shared Loop Run's scripts (create-loop/references)."""
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
import check_knowledge as ck  # noqa: E402
import check_play_done  # noqa: E402
import commit_run_files  # noqa: E402
import group_questions as gq  # noqa: E402
import prepare_check  # noqa: E402
import record_check  # noqa: E402
import record_review as rr  # noqa: E402
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


class LoopPreflight(Work):
    def setUp(self):
        super().setUp()
        self.config = self.write("config.yaml", CONFIG)
        self.write("skills/intent/SKILL.md", "runs check_loop_contract.py first\n")
        self.write("skills/vision/SKILL.md", "runs check_loop_contract.py first\n")
        self.write("skills/shape-thing/SKILL.md", "no contract here\n")
        for skill in ("find-answers-in-sources", "author-knowledge-page", "propose-answers",
                      "author-knowledge-brief"):
            self.write(f"skills/{skill}/SKILL.md", "a skill\n")

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

    def test_a_missing_knowledge_skill_halts(self):
        os.remove(self.p("skills", "author-knowledge-brief", "SKILL.md"))
        self.assertEqual(self.run_it("intent,vision"), 2)
        facts = self.read_json("pre.json")
        self.assertEqual(facts["knowledge_missing"], ["author-knowledge-brief"])
        self.assertEqual(facts["missing"], [])

    def test_no_knowledge_play_is_looked_for(self):
        self.assertEqual(self.run_it("intent,vision"), 0)
        self.assertEqual(self.read_json("pre.json")["missing"], [])
        self.assertFalse(os.path.exists(self.p("skills", "search-knowledge")))

    def test_a_missing_play_halts(self):
        self.assertEqual(self.run_it("intent,understand"), 2)
        self.assertEqual(self.read_json("pre.json")["missing"], ["understand"])

    def test_a_play_that_checks_no_contract_halts(self):
        self.assertEqual(self.run_it("intent,shape-thing"), 2)
        self.assertEqual(self.read_json("pre.json")["no_contract"], ["shape-thing"])

    def test_defaults_when_the_config_names_no_loop_but_the_checker_model_is_asked_for(self):
        cfg = self.write("bare.yaml", "stm:\n  base-path: x/\n")
        self.assertEqual(self.run_it("intent", cfg), 2)
        facts = self.read_json("pre.json")
        self.assertEqual((facts["runner"], facts["checker"]["kind"]), ("subagent", "subagent"))
        self.assertTrue(facts["evidence_record"])
        self.assertTrue(any("checker.model" in p for p in facts["problems"]))

    def test_an_old_drives_block_halts_and_names_the_rename(self):
        cfg = self.write("old.yaml", "stm:\n  base-path: x/\ndrives:\n  kickoff:\n    runner: subagent\n")
        self.assertEqual(self.run_it("intent", cfg), 2)
        self.assertTrue(any("old `drives:` block" in p and "ADR 045" in p
                            for p in self.read_json("pre.json")["problems"]))

    def test_an_unknown_runner_halts(self):
        cfg = self.write("odd.yaml", CONFIG.replace("runner: subagent", "runner: telepathy"))
        self.assertEqual(self.run_it("intent", cfg), 2)


class LoopStatus(Work):
    """The loop presents its status in one file; a display reads it (run-status.md)."""

    def test_the_first_call_names_the_run_and_later_calls_update_it(self):
        f = self.p("status", "run-discovery.json")
        self.assertEqual(quiet(loop_status.main, ["--file", f, "--name", "discovery", "--issue", "7",
                                                   "--run-id", "discovery-1", "--round", "1",
                                                   "--play", "discover-intent", "--step", "walking the prototype"]), 0)
        first = self.read_json("status/run-discovery.json")
        self.assertEqual((first["state"], first["play"], first["round"]), ("running", "discover-intent", 1))
        self.assertEqual(quiet(loop_status.main, ["--file", f, "--play", "discover-domains", "--step", "seeding"]), 0)
        later = self.read_json("status/run-discovery.json")
        self.assertEqual((later["name"], later["play"], later["round"]), ("discovery", "discover-domains", 1))
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
                                             "--branch", branch, "--play", "discover-domains",
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
        self.assertIn("chore(stm): record discover-domains run files (#7)", self.log())
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
        code = quiet(run_play_headless.main, ["--play", "discover-domains", "--contract", "c.json",
                                              "--out", self.p("run.json")])
        self.assertEqual(code, 0)
        run = self.read_json("run.json")
        self.assertEqual(run["session_id"], "s1")
        self.assertIn("/discover-domains --contract c.json", run["result"])

    def test_it_hands_the_play_its_argument(self):
        code = quiet(run_play_headless.main, ["--play", "discover-intent", "--contract", "c.json", "--argument",
                                              "https://shop.example.com", "--out", self.p("run.json")])
        self.assertEqual(code, 0)
        self.assertIn("/discover-intent --contract c.json https://shop.example.com", self.read_json("run.json")["result"])

    def test_it_resumes_the_same_session_with_the_answer(self):
        answer = self.write("answer.txt", "Shops pay a monthly fee.")
        code = quiet(run_play_headless.main, ["--play", "discover-domains", "--resume", "s1",
                                              "--message-file", answer, "--out", self.p("run.json")])
        self.assertEqual(code, 0)
        self.assertIn("--resume s1", self.read_json("run.json")["result"])

    def test_resume_without_an_answer_is_refused(self):
        self.assertEqual(quiet(run_play_headless.main, ["--play", "discover-domains", "--resume", "s1",
                                                        "--out", self.p("run.json")]), 2)


class RoundState(GitWork):
    """After a round: done, again, or ask (the loop loops; a question is the loop's)."""

    def setUp(self):
        super().setUp()
        self.write("product/model.md", "v1\n")
        subprocess.run(["git", "add", "-A"], check=True, capture_output=True)
        subprocess.run(["git", "commit", "-q", "-m", "model"], check=True, capture_output=True)
        os.makedirs(self.p("rev"), exist_ok=True)
        self.tool = stub_tool(self, [])

    def open_q(self, *ids):
        self.write("rev/open-discover-intent.json", json.dumps({"play": "discover-intent", "questions": [
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
                                 "--review-dir", "rev", "--issue", "7", "--memory-tool", self.tool,
                                 "--model-path", "product",
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
        rec = self.decide(1, report={"work_for_plays": [{"play": "/discover-capabilities", "target": "cap-board"}]})
        self.assertEqual(rec["decision"], "again")
        self.assertEqual(rec["next"], {"/discover-capabilities": ["cap-board"]})
        self.assertEqual(rec["gaps_left"], 1)

    def test_an_uncovered_screen_is_not_done(self):
        rec = self.decide(1, gaps={"uncovered": [{"what": "main section", "name": "Reports"}]}, report={})
        self.assertNotEqual(rec["decision"], "done")

    def test_closed_gaps_and_no_question_is_done(self):
        rec = self.decide(1, gaps={"work": [], "uncovered": []}, report={"work_for_plays": []})
        self.assertEqual(rec["decision"], "done")

    def test_the_same_gaps_twice_asks_the_person(self):
        report = {"work_for_plays": [{"play": "/discover-domains", "target": "cap-x"}]}
        self.decide(1, report=report)
        self.assertEqual(self.decide(2, report=report)["decision"], "ask")

    def test_a_waiting_memory_update_the_tool_lists_is_an_open_question(self):
        self.tool = stub_tool(self, [
            {"id": "mu-1", "issue": 7, "status": "waiting", "missing": "how long is a cart kept?"},
            {"id": "mu-2", "issue": 7, "status": "applied"},
            {"id": "mu-3", "issue": 8, "status": "waiting", "missing": "another issue's"}])
        rec = self.decide(1)
        self.assertEqual([q["id"] for q in rec["open"]], ["mu-1"])
        self.assertEqual(self.read_json("work/rounds.json")["open_left"], 1)

    def test_an_update_file_on_disk_is_not_read(self):
        self.write("issue/review/memory-updates/mu-9.json", json.dumps({"update": {
            "id": "mu-9", "status": "waiting", "missing": "read by path"}}))
        self.assertEqual(self.decide(1)["open"], [])

    def test_a_memory_tool_error_stops_the_round(self):
        self.tool = self.write("bad.py", "import json\nprint(json.dumps({'ok': False, 'message': 'tier_missing'}))\n")
        rc = quiet(round_state.main, ["--round", "1", "--working", "work", "--review-dir", "rev",
                                      "--issue", "7", "--memory-tool", self.tool, "--model-path", "product",
                                      "--out", "work/round-1.json"])
        self.assertEqual(rc, 2)


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
        self.write("work/discover-intent-done.json", '{"done": true}')
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
        self.assertTrue(os.path.isfile(self.p("work/check/done/discover-intent-done.json")))
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


# --- The knowledge step (R5c, R5b; ADR 059) ---

def stub_tool(work, updates):
    """A stand-in memory tool that answers `updates --status waiting` with these updates."""
    return work.write("memory.py", "import json, sys\nU = " + json.dumps(updates) + "\n"
                      "print(json.dumps({'ok': True, 'command': 'updates', 'updates': "
                      "[u for u in U if u['status'] == sys.argv[sys.argv.index('--status') + 1]]}))\n")


class GroupQuestions(Work):
    def setUp(self):
        super().setUp()
        self.write("issue/review/loop/open-intent.json", json.dumps({"play": "discover-intent", "questions": [
            {"id": "i1", "ask": "How will you know signing off a loop works?", "about": "sign-off"},
            {"id": "i2", "ask": "Why does it matter to the business?", "about": "sign-off"}]}))
        self.write("issue/review/loop/open-understand.json", json.dumps({"play": "discover-capabilities", "questions": [
            {"id": "u1", "ask": "How will you know answering every change works?", "about": "answer"},
            {"id": "u2", "ask": "How quickly must a card open?", "about": "answer"},
            {"id": "u3", "ask": "How fast must a comment show?", "about": "comment"},
            {"id": "u4", "ask": "Does GDPR apply to the review record?", "about": "answer"},
            {"id": "u5", "ask": "Must commenting on an area work without a mouse pointer drag?", "about": "c"}]}))
        self.write("work/round-2.json", json.dumps({"round": 2, "decision": "ask", "open": [
            {"from": "discover-intent", "id": "i1", "ask": "How will you know signing off a loop works?"},
            {"from": "memory-update", "id": "mu-1", "ask": "Speed bar for review pages", "for_person": True}]}))

    def groups(self):
        rc = quiet(gq.main, ["--review-dir", self.p("issue/review/loop"),
                             "--round-record", self.p("work/round-2.json"), "--out", self.p("g.json")])
        self.assertEqual(rc, 0)
        return self.read_json("g.json")

    def test_the_same_question_from_several_plays_is_one_group(self):
        by_topic = {g["topic"]: g for g in self.groups()["groups"]}
        self.assertEqual(sorted(by_topic["proof"]["members"]), ["i1", "u1"])
        self.assertEqual(by_topic["proof"]["from"], ["discover-capabilities", "discover-intent"])
        self.assertEqual(sorted(by_topic["speed"]["members"]), ["mu-1", "u2", "u3"])
        self.assertEqual(by_topic["compliance"]["members"], ["u4"])

    def test_waiting_updates_come_from_the_round_record_only(self):
        ids = [m for g in self.groups()["groups"] for m in g["members"]]
        self.assertIn("mu-1", ids)
        self.assertEqual(ids.count("i1"), 1)  # a play's question is read from its open file once

    def test_it_never_calls_the_memory_tool(self):
        with open(gq.__file__, encoding="utf-8") as fh:
            text = fh.read()
        self.assertNotIn("subprocess", text)
        self.assertNotIn("memory.py", text.split('"""', 2)[2])

    def test_every_question_lands_in_exactly_one_group(self):
        d = self.groups()
        ids = [m for g in d["groups"] for m in g["members"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(ids), d["questions"])

    def test_a_round_record_with_no_open_list_stops_the_grouping(self):
        bad = self.write("work/round-3.json", json.dumps({"round": 3}))
        rc = quiet(gq.main, ["--review-dir", self.p("issue/review/loop"),
                             "--round-record", bad, "--out", self.p("g.json")])
        self.assertEqual(rc, 2)


GROUPS = {"groups": [{"id": "g1", "members": ["q1", "q2"]}, {"id": "g2", "members": ["q3"]},
                     {"id": "g3", "members": ["q4"]}]}
SEARCH = {"groups": [
    {"id": "g1", "members": ["q1", "q2"], "ask": "Does Later reach Garura?", "found": "answered",
     "closed_by": "source", "answer": "No; Later keeps the card unread.",
     "evidence": [{"file": "argus.html", "where": "line 997", "quote": "Later · keep unread"}]},
    {"id": "g2", "members": ["q3"], "ask": "Is a sent-back decision kept?", "found": "partly",
     "closed_by": "memory", "answer": "Kept beside the new one.", "trace": "cite-12",
     "missing": "for how long"},
    {"id": "g3", "members": ["q4"], "ask": "How will you know reviews work?", "found": "open",
     "missing": "the business measure", "not_shown": "no-screen"}]}


def copy(data):
    return json.loads(json.dumps(data))


class CheckKnowledgeSearch(unittest.TestCase):
    def test_a_complete_search_is_clean_and_counts_what_is_left(self):
        gaps, counts = ck.check_search(SEARCH, GROUPS)
        self.assertEqual(gaps, [])
        self.assertEqual(counts["left_for_build"], 2)
        self.assertEqual(counts["questions"], 4)

    def test_a_source_answer_without_a_quote_fails(self):
        bad = copy(SEARCH)
        bad["groups"][0]["evidence"] = [{"file": "argus.html", "quote": ""}]
        self.assertTrue(any("quote" in g for g in ck.check_search(bad, GROUPS)[0]))

    def test_a_memory_answer_without_its_trace_fails(self):
        bad = copy(SEARCH)
        bad["groups"][1]["trace"] = ""
        self.assertTrue(any("trace" in g for g in ck.check_search(bad, GROUPS)[0]))

    def test_an_open_group_says_what_is_missing_and_why(self):
        bad = copy(SEARCH)
        bad["groups"][2]["missing"] = ""
        bad["groups"][2]["not_shown"] = None
        gaps = ck.check_search(bad, GROUPS)[0]
        self.assertTrue(any("missing" in g for g in gaps))
        self.assertTrue(any("should-show" in g for g in gaps))

    def test_a_question_left_out_or_in_two_groups_fails(self):
        bad = copy(SEARCH)
        bad["groups"][0]["members"] = ["q1"]
        bad["groups"][2]["members"] = ["q4", "q3"]
        gaps = ck.check_search(bad, GROUPS)[0]
        self.assertTrue(any("q2 is in 0 groups" in g for g in gaps))
        self.assertTrue(any("q3 is in 2 groups" in g for g in gaps))


B_SEARCH = {"groups": [
    {"id": "s1", "found": "answered"},
    {"id": "s2", "found": "open", "not_shown": "no-screen"},
    {"id": "s3", "found": "partly"},
    {"id": "s4", "found": "open", "not_shown": "should-show"},
    {"id": "s5", "found": "open", "not_shown": "no-screen"}]}
B_GOOD = {"groups": [
    {"id": "b1", "from": ["s2"], "ask": "How fast must a card open?", "closed_by": "update",
     "update": "mu-9", "for_project_memory": True},
    {"id": "b2", "from": ["s3"], "ask": "Who decides on a run?", "closed_by": "proposal",
     "proposal": {"answer": "The person who asked decides on their run.",
                  "basis": "argus.html shows one reviewer answering every card",
                  "context": "The prototype never shows a second person."}},
    {"id": "b3", "from": ["s4"], "ask": "What if memory finds nothing?",
     "closed_by": "prototype-feedback", "feedback": "Show an empty answer state in Ask memory"},
    {"id": "b4", "from": ["s5"], "ask": "Does Argus earn money?", "closed_by": "settled",
     "why": "Argus is an internal tool; the prototype has no pricing or customers.",
     "basis": "argus.html: no pricing, plan or customer screen in any of the 36 views"}]}


class CheckKnowledgeBuild(unittest.TestCase):
    waiting = {"mu-9"}

    def test_a_complete_build_is_clean(self):
        gaps, counts = ck.check_build(B_SEARCH, B_GOOD, self.waiting)
        self.assertEqual(gaps, [])
        self.assertEqual(counts["left_by_search"], 4)
        self.assertEqual(counts["closed"]["proposal"], 1)

    def test_a_proposal_needs_its_basis_and_context(self):
        bad = copy(B_GOOD)
        bad["groups"][1]["proposal"]["context"] = ""
        self.assertTrue(any("context" in g for g in ck.check_build(B_SEARCH, bad, self.waiting)[0]))

    def test_an_update_the_memory_tool_does_not_list_as_waiting_fails(self):
        bad = copy(B_GOOD)
        bad["groups"][0]["update"] = "mu-404"
        self.assertTrue(any("mu-404" in g for g in ck.check_build(B_SEARCH, bad, self.waiting)[0]))

    def test_a_screen_the_prototype_should_show_is_feedback(self):
        bad = copy(B_GOOD)
        bad["groups"][2]["closed_by"] = "proposal"
        bad["groups"][2]["proposal"] = {"answer": "x", "basis": "y", "context": "z"}
        self.assertTrue(any("prototype feedback" in g for g in ck.check_build(B_SEARCH, bad, self.waiting)[0]))

    def test_an_answered_search_group_is_not_built_again_and_none_is_left_out(self):
        bad = copy(B_GOOD)
        bad["groups"][3]["from"] = ["s1"]
        gaps = ck.check_build(B_SEARCH, bad, self.waiting)[0]
        self.assertTrue(any("already answered" in g for g in gaps))
        self.assertTrue(any("s5 is in 0 build groups" in g for g in gaps))

    def test_settled_says_why_and_what_it_rests_on(self):
        bad = copy(B_GOOD)
        bad["groups"][3]["why"] = ""
        bad["groups"][3]["basis"] = ""
        gaps = ck.check_build(B_SEARCH, bad, self.waiting)[0]
        self.assertTrue(any("settles" in g for g in gaps))
        self.assertTrue(any("basis" in g for g in gaps))


BUILD = {"groups": [
    {"id": "b1", "closed_by": "update", "update": "mu-9"},
    {"id": "b2", "closed_by": "proposal"},
    {"id": "b3", "closed_by": "proposal"},
    {"id": "b4", "closed_by": "prototype-feedback"},
    {"id": "b5", "closed_by": "settled"}]}
BRIEF = {"understood": "Argus is the review tool for the agents' work.",
         "built": "6 business intents, one domain, 12 capabilities.",
         "gaps": [{"id": "G1", "theme": "Who decides", "context": "The prototype shows one reviewer.",
                   "proposal": "The person who asked decides on their run.", "from": ["b2", "b3"]}],
         "settled": [{"from": ["b5"], "what": "How Argus earns money", "why": "It is an internal tool."}],
         "pages": [{"update": "mu-9", "what": "Speed bar for Ask memory", "sources": ["nngroup response times"],
                    "recommend": "approve"}],
         "prototype_notes": {"count": 1, "where": "build.json"}}
MD = "## What we understood\n...\n## What we built\n...\n## Where the gaps are\n- G1 Who decides\n"


class CheckKnowledgeBrief(unittest.TestCase):
    def test_a_complete_brief_is_clean(self):
        problems, counts = ck.check_brief(BRIEF, MD, BUILD, 7)
        self.assertEqual(problems, [])
        self.assertEqual(counts["gaps"], 1)

    def test_a_gap_without_a_proposal_or_with_a_question_fails(self):
        bad = copy(BRIEF)
        bad["gaps"][0]["proposal"] = "Who should decide?"
        self.assertTrue(any("question" in p for p in ck.check_brief(bad, MD, BUILD, 7)[0]))
        bad["gaps"][0]["context"] = ""
        self.assertTrue(any("context" in p for p in ck.check_brief(bad, MD, BUILD, 7)[0]))

    def test_too_many_gaps_fail(self):
        bad = copy(BRIEF)
        bad["gaps"] = [dict(BRIEF["gaps"][0], id=f"G{i}", **{"from": []}) for i in range(1, 10)]
        bad["gaps"][0]["from"] = ["b2", "b3"]
        md = MD + "".join(f"G{i}\n" for i in range(1, 10))
        self.assertTrue(any("at most 7" in p for p in ck.check_brief(bad, md, BUILD, 7)[0]))

    def test_every_proposal_page_and_note_is_carried(self):
        bad = copy(BRIEF)
        bad["gaps"][0]["from"] = ["b2"]
        bad["pages"] = []
        bad["prototype_notes"]["count"] = 0
        problems = ck.check_brief(bad, MD, BUILD, 7)[0]
        self.assertTrue(any("b3 is in 0 gaps" in p for p in problems))
        self.assertTrue(any("mu-9" in p for p in problems))
        self.assertTrue(any("prototype notes" in p for p in problems))

    def test_settled_points_and_page_sources_are_shown(self):
        bad = copy(BRIEF)
        bad["settled"] = []
        bad["pages"][0]["sources"] = []
        problems = ck.check_brief(bad, MD, BUILD, 7)[0]
        self.assertTrue(any("b5 is shown 0 times" in p for p in problems))
        self.assertTrue(any("sources" in p for p in problems))

    def test_a_waiting_update_the_build_did_not_name_is_still_listed(self):
        problems = ck.check_brief(BRIEF, MD, BUILD, 7, waiting={"mu-9", "mu-12"})[0]
        self.assertTrue(any("mu-12" in p for p in problems))

    def test_the_markdown_carries_the_headings_and_gaps(self):
        problems = ck.check_brief(BRIEF, "nothing here", BUILD, 7)[0]
        self.assertTrue(any("What we understood" in p for p in problems))
        self.assertTrue(any("G1: not named" in p for p in problems))

    def test_a_brief_md_that_is_not_the_renderers_output_fails(self):
        self.assertEqual(ck.check_brief(BRIEF, MD, BUILD, 7, rendered=MD + "\n")[0], [])
        problems = ck.check_brief(BRIEF, MD + "Written beside the data.\n", BUILD, 7, rendered=MD)[0]
        self.assertTrue(any("renderer" in p for p in problems))


class CheckKnowledgeMain(Work):
    def run_main(self, build=B_GOOD):
        self.write("groups.json", json.dumps({"groups": [{"id": "x", "members": ["q1"]}]}))
        self.write("search.json", json.dumps({"groups": [
            {"id": "s2", "members": ["q1"], "ask": "How fast must a card open?", "found": "open",
             "missing": "the speed bar", "not_shown": "no-screen"}]}))
        self.write("build.json", json.dumps(build))
        brief = {"understood": "u", "built": "b", "gaps": [], "settled": [],
                 "pages": [{"update": "mu-9", "what": "Speed bar", "sources": ["nngroup"], "recommend": "approve"}],
                 "prototype_notes": {"count": 0, "where": "build.json"}}
        self.write("brief.json", json.dumps(brief))
        self.write("brief.md", MD)
        renderer = self.write("render.py", "import sys\nopen(sys.argv[sys.argv.index('--out') + 1], 'w')"
                              f".write({MD!r})\n")
        tool = stub_tool(self, [{"id": "mu-9", "issue": 7, "status": "waiting"}])
        return quiet(ck.main, ["--groups", self.p("groups.json"), "--search", self.p("search.json"),
                               "--build", self.p("build.json"), "--brief", self.p("brief.json"),
                               "--brief-md", self.p("brief.md"), "--issue", "7", "--memory-tool", tool,
                               "--renderer", renderer, "--out", self.p("check.json")])

    def test_one_run_checks_the_search_the_build_and_the_brief(self):
        build = {"groups": [{"id": "b1", "from": ["s2"], "ask": "How fast must a card open?",
                             "closed_by": "update", "update": "mu-9"}]}
        self.assertEqual(self.run_main(build), 0)
        report = self.read_json("check.json")
        self.assertTrue(report["ok"])
        self.assertEqual(set(report), {"ok", "search", "build", "brief"})

    def test_a_gap_in_one_part_fails_the_whole_check_and_names_its_part(self):
        build = {"groups": [{"id": "b1", "from": ["s2"], "ask": "How fast must a card open?",
                             "closed_by": "update", "update": "mu-404"}]}
        self.assertEqual(self.run_main(build), 1)
        report = self.read_json("check.json")
        self.assertFalse(report["ok"])
        self.assertTrue(any("mu-404" in g for g in report["build"]["gaps"]))
        self.assertEqual(report["search"]["gaps"], [])

    def test_a_memory_tool_error_is_an_unreadable_input(self):
        self.write("x.json", "{}")
        bad = self.write("bad.py", "import json\nprint(json.dumps({'ok': False, 'message': 'tier_missing'}))\n")
        args = ["--groups", self.p("x.json"), "--search", self.p("x.json"), "--build", self.p("x.json"),
                "--brief", self.p("x.json"), "--brief-md", self.p("x.json"), "--issue", "7",
                "--memory-tool", bad, "--renderer", bad, "--out", self.p("check.json")]
        self.assertEqual(quiet(ck.main, args), 2)


class RecordReview(Work):
    def run_record(self, reply):
        search = {"groups": [{"id": "s1", "members": ["intent-q7"]}, {"id": "s2", "members": ["understand-q2"]}]}
        build = {"groups": [{"id": "b2", "from": ["s1"]}, {"id": "b3", "from": ["s2"]}]}
        for name, data in (("brief.json", BRIEF), ("review.json", reply), ("build.json", build),
                           ("search.json", search),
                           ("loop/open-intent.json", {"play": "discover-intent", "questions": [{"id": "intent-q7"}]}),
                           ("loop/open-understand.json", {"play": "discover-capabilities", "questions": [{"id": "understand-q2"}]})):
            self.write(name, json.dumps(data))
        rc = quiet(rr.main, ["--brief", self.p("brief.json"), "--reply", self.p("review.json"),
                             "--build", self.p("build.json"), "--search", self.p("search.json"),
                             "--review-dir", self.p("loop"),
                             "--issue-dir", self.p("issue"), "--round", "3", "--out", self.p("rec.json")])
        return rc, self.read_json("rec.json")

    def test_yes_takes_every_proposal_and_recommendation(self):
        rc, rec = self.run_record({"words": "yes", "gaps": {"G1": "accept"}, "pages": {"mu-9": "approve"}})
        self.assertEqual(rc, 0)
        with open(rec["written"]) as fh:
            written = json.load(fh)
        self.assertEqual(written["gaps"][0]["answer"], BRIEF["gaps"][0]["proposal"])
        self.assertEqual(written["gaps"][0]["from"], "person")
        self.assertEqual(written["gaps"][0]["proposed_by"], "knowledge-builder")
        self.assertEqual(rec["page_decisions"][0]["decision"], "approve")

    def test_the_answer_reaches_each_play_by_its_question_id(self):
        rc, rec = self.run_record({"words": "yes", "gaps": {"G1": "accept"}, "pages": {"mu-9": "approve"}})
        with open(rec["written"]) as fh:
            mapped = json.load(fh)["answers"]
        self.assertEqual(mapped["discover-intent"]["intent-q7"], BRIEF["gaps"][0]["proposal"])
        self.assertEqual(mapped["discover-capabilities"]["understand-q2"], BRIEF["gaps"][0]["proposal"])
        self.assertEqual(rec["questions_answered"], 2)

    def test_a_correction_is_the_persons_own_answer(self):
        rc, rec = self.run_record({"words": "G1: the owner decides", "gaps": {"G1": {"answer": "The owner decides."}},
                                   "pages": {"mu-9": "reject"}})
        self.assertEqual(rc, 0)
        with open(rec["written"]) as fh:
            self.assertFalse(json.load(fh)["gaps"][0]["accepted_proposal"])

    def test_an_undecided_gap_or_page_records_nothing(self):
        rc, rec = self.run_record({"words": "yes", "gaps": {}, "pages": {}})
        self.assertEqual(rc, 1)
        self.assertNotIn("written", rec)
        self.assertFalse(os.path.exists(self.p("issue", "review", "loop", "person-answers-round-3.json")))


if __name__ == "__main__":
    unittest.main()
