#!/usr/bin/env python3
"""Tests for lint_loop.py: the worked example passes; each kind of broken loop fails."""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
LINT = os.path.join(HERE, "..", "scripts", "lint_loop.py")
EXAMPLE = os.path.join(HERE, "compiled-loop-example")
SHARED_RUN = os.path.join(HERE, "..", "..", "..", "loops", "_shared", "loop-run.md")


class LintLoop(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        comp = os.path.join(self.root, "components")
        for play, text in (("intent", "runs check_loop_contract.py first; reads the statement\n"),
                           ("vision", "runs check_loop_contract.py first; reads the goal\n"),
                           ("shape", "no contract here\n")):
            os.makedirs(os.path.join(comp, "plays", play))
            with open(os.path.join(comp, "plays", play, "SKILL.md"), "w") as fh:
                fh.write(text)
        os.makedirs(os.path.join(comp, "loops", "_shared"))
        shutil.copy(SHARED_RUN, os.path.join(comp, "loops", "_shared", "loop-run.md"))
        self.loop = os.path.join(comp, "loops", "sample-loop")
        shutil.copytree(EXAMPLE, self.loop)
        self.skill = os.path.join(self.loop, "SKILL.md")

    def edit(self, old, new):
        with open(self.skill) as fh:
            text = fh.read()
        self.assertIn(old, text)
        with open(self.skill, "w") as fh:
            fh.write(text.replace(old, new))

    def lint(self):
        run = subprocess.run([sys.executable, LINT, self.skill], capture_output=True, text=True)
        return run.returncode, run.stdout

    def gaps(self):
        return [line for line in self.lint()[1].splitlines() if "[GAP" in line]

    def test_the_worked_example_passes(self):
        code, out = self.lint()
        self.assertEqual(code, 0, out)

    def test_a_missing_play_fails(self):
        self.edit("plays=intent,vision", "plays=intent,ghost")
        self.assertTrue(any("ghost: no such play" in g for g in self.gaps()))

    def test_a_play_that_cannot_run_in_a_loop_fails(self):
        self.edit("plays=intent,vision", "plays=intent,shape")
        self.assertTrue(any("shape: cannot run inside a loop" in g for g in self.gaps()))

    def test_a_missing_anchor_fails(self):
        self.edit("# --- end Shared Loop Run ---\n", "")
        self.assertTrue(any("shared loop run" in g for g in self.gaps()))

    def test_a_step_that_does_work_itself_fails(self):
        self.edit("Owner: loop · Depends on: Step 1", "Owner: `product-os-keeper` · Depends on: Step 1")
        self.assertTrue(any("product-os-keeper" in g for g in self.gaps()))

    def test_a_loop_without_kind_fails(self):
        self.edit("kind: loop\n", "")
        self.assertTrue(any("kind: loop" in g for g in self.gaps()))

    def test_a_config_key_for_another_loop_fails(self):
        self.edit("runner_key=loops.sample-loop.runner", "runner_key=loops.discovery.runner")
        self.assertTrue(any("config keys" in g for g in self.gaps()))

    def test_a_missing_script_fails(self):
        os.remove(os.path.join(self.loop, "scripts", "commit_run_files.py"))
        self.assertTrue(any("commit_run_files.py" in g for g in self.gaps()))

    def test_a_failure_with_no_step_eval_fails(self):
        self.edit("**SE-4 (F4/C4):**", "**SE-4 (C4):**")
        self.assertTrue(any("F4" in g for g in self.gaps()))

    def test_a_loop_with_no_done_means_fails(self):
        ice = os.path.join(self.loop, "reference", "ice.md")
        with open(ice) as fh:
            text = fh.read()
        with open(ice, "w") as fh:
            fh.write(text.replace("### Done means", "### Done"))
        self.assertTrue(any("done means" in g for g in self.gaps()))


class LintLoopMore(LintLoop):
    """The checks the /loop-creator trial asked for: end=, fingerprint, stamped copies, config."""

    CONFIG = ("evidence:\n  record: false\n  plays:\n    sample-loop: true\n"
              "loops:\n  sample-loop:\n    runner: subagent\n    checker:\n      kind: subagent\n")

    def config(self, text):
        with open(os.path.join(self.root, "config.yaml"), "w") as fh:
            fh.write(text)

    def test_a_loop_with_no_end_fails(self):
        self.edit("end=commit-change, propose-change, review-change, merge-change (merge pinned)\n", "")
        self.assertTrue(any("end=" in g for g in self.gaps()))

    def test_an_ice_changed_after_the_build_fails(self):
        with open(os.path.join(self.loop, "reference", "ice.md"), "a") as fh:
            fh.write("\nA late edit.\n")
        self.assertTrue(any("fingerprint matches" in g for g in self.gaps()))

    def test_an_edited_stamped_script_fails_when_its_source_is_there(self):
        plays = os.path.join(self.root, "components", "plays")
        shutil.copytree(HERE, os.path.join(plays, "loop-creator", "references"))
        shutil.copytree(os.path.join(HERE, "..", "..", "play-creator", "references"),
                        os.path.join(plays, "play-creator", "references"))
        self.assertEqual(self.lint()[0], 0, self.lint()[1])
        with open(os.path.join(self.loop, "scripts", "check_play_done.py"), "a") as fh:
            fh.write("# edited\n")
        self.assertTrue(any("check_play_done.py" in g for g in self.gaps()))

    def test_the_config_must_set_the_loop(self):
        self.config(self.CONFIG)
        self.assertEqual(self.lint()[0], 0, self.lint()[1])
        self.config(self.CONFIG.replace("    sample-loop: true\n", ""))
        self.assertTrue(any("evidence.plays.sample-loop" in g for g in self.gaps()))
        self.config(self.CONFIG.replace("      kind: subagent\n", ""))
        self.assertTrue(any("checker.kind" in g for g in self.gaps()))


class LintLoopHalfDone(LintLoop):
    """The /loop-editor trial's findings: a half-done edit and an input no play reads fail."""

    def test_a_play_added_to_plays_alone_fails(self):
        with open(os.path.join(self.root, "components", "plays", "shape", "SKILL.md"), "w") as fh:
            fh.write("runs check_loop_contract.py first\n")
        self.edit("plays=intent,vision", "plays=intent,vision,shape")
        gaps = self.gaps()
        self.assertTrue(any("no step owned by: shape" in g for g in gaps), gaps)
        self.assertTrue(any("shape-done.json" in g for g in gaps), gaps)

    def test_an_argument_is_handed_on_the_command_line_not_read_from_the_contract(self):
        self.edit("Run R4 with the statement as `inputs.intent.statement`.",
                  "Run R4 with the statement as `inputs.intent.statement` and `inputs.intent.argument`.")
        self.assertFalse(any("inputs.intent.argument" in g for g in self.gaps()))

    def test_an_input_the_play_never_reads_fails(self):
        self.edit("Run R4 with the statement as `inputs.intent.statement`.",
                  "Run R4 with the statement as `inputs.intent.statement` and `inputs.intent.mood`.")
        self.assertTrue(any("inputs.intent.mood" in g for g in self.gaps()))


class CopiesMatch(unittest.TestCase):
    """Stamped copies are copies: the example's scripts and the editor's linter match their source."""

    def same(self, a, b):
        with open(a, "rb") as fa, open(b, "rb") as fb:
            self.assertEqual(fa.read(), fb.read(), f"{b} differs from {a}")

    def test_the_examples_scripts_match_their_canonical_copies(self):
        play_refs = os.path.join(HERE, "..", "..", "play-creator", "references")
        for name in [n for n in os.listdir(os.path.join(EXAMPLE, "scripts")) if n.endswith(".py")]:
            source = os.path.join(HERE, name)
            if not os.path.isfile(source):
                source = os.path.join(play_refs, name)
            self.same(source, os.path.join(EXAMPLE, "scripts", name))

    def test_the_editors_linter_matches_the_creators(self):
        self.same(LINT, os.path.join(HERE, "..", "..", "loop-editor", "scripts", "lint_loop.py"))


if __name__ == "__main__":
    unittest.main()
