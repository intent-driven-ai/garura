#!/usr/bin/env python3
"""Tests for the memory system an install lays (#660, ADR 035 §8), and its reversal.

Run: python3 test_install.py. Each test installs into a throwaway folder, with shared memory,
the Codex home and Phoenix memory's place all in throwaway folders too, so nothing on the
machine is touched.
"""

import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "core", "components", "plays", "uninstall-garura", "scripts"))
import install  # noqa: E402
import memory_system  # noqa: E402
import uninstall  # noqa: E402
from adapters import codex  # noqa: E402


def git(repo, *args):
    subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True)


class Installed(unittest.TestCase):
    def setUp(self):
        self.work = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.work, ignore_errors=True)
        self.target = os.path.join(self.work, "shop")
        self.place = os.path.join(self.work, "machine", "phoenix-memory")
        self.source = os.path.join(self.work, "phoenix-source")
        os.makedirs(os.path.join(self.source, "knowledge", "domains"))
        with open(os.path.join(self.source, "knowledge", "domains", "user-management.md"), "w") as fh:
            fh.write("# User management\n- Password reset — the floor; any credential login.\n")
        git(self.source, "init", "-q", "-b", "main")
        # Demo address: sample data for this throwaway repository, not personal data.
        git(self.source, "config", "user.email", "t@example.com")
        git(self.source, "config", "user.name", "test")
        git(self.source, "add", "-A")
        git(self.source, "commit", "-q", "-m", "seed")
        old_home = codex.CODEX_HOME
        codex.CODEX_HOME = os.path.join(self.work, "codex-home")
        self.addCleanup(setattr, codex, "CODEX_HOME", old_home)

    def install(self, tool="claude"):
        with contextlib.redirect_stdout(io.StringIO()):
            return install.install(ROOT, self.target, tool, False, True, os.path.join(self.work, "shared-memory"),
                                   scope="harness", phoenix_place=self.place, phoenix_source=self.source)

    def tool(self, *args):
        env = {k: v for k, v in os.environ.items() if not k.startswith("MEMORY_")}
        run = subprocess.run(["python3", memory_system.TOOL_CALL, *args], capture_output=True, text=True,
                             env=env, cwd=self.target)
        return json.loads(run.stdout.splitlines()[0])

    def path(self, *parts):
        return os.path.join(self.target, *parts)


class LaysTheMemorySystem(Installed):
    def test_the_install_lays_the_tool_its_settings_and_the_guide_and_brings_no_memory(self):
        record = self.install()["memory_system"]
        self.assertTrue(os.path.isfile(self.path(".garura", "tools", "memory", "memory.py")))
        self.assertTrue(os.path.isfile(self.path(".garura", "tools", "memory", "contract", "v4.json")))
        self.assertFalse(os.path.exists(self.path(".garura", "tools", "memory", "test_memory.py")))
        self.assertFalse(os.path.exists(self.path(".garura", "tools", "memory", "contract", "samples")))
        self.assertTrue(os.path.isdir(self.path(".garura", "project", "issues")))
        with open(self.path(".claude", "rules", "garura-memory.md")) as fh:
            guide = fh.read()
        self.assertIn("python3 .garura/tools/memory/memory.py search", guide)
        self.assertNotIn("{tool}", guide)
        self.assertEqual((record["guide"], record["agents_md_block"]), (".claude/rules/garura-memory.md", None))
        self.assertTrue(record["check"]["ok"], record["check"])
        self.assertEqual(record["check"]["tiers"], {"short-term": True, "garura": True, "phoenix": False})
        self.assertIn("not on this machine yet", " ".join(record["check"]["messages"]))
        self.assertFalse(os.path.exists(self.place))  # the install brings no memory

    def test_an_agent_finds_memory_through_the_installed_tool_and_phoenix_arrives_on_first_use(self):
        self.install()
        a = self.tool("search", "--issue", "1", "--pattern", "password reset", "--ignore-case")
        self.assertEqual((a["ok"], a["answered_by"]), (True, "phoenix"))
        self.assertTrue(os.path.isdir(os.path.join(self.place, ".git")))
        self.assertTrue(self.tool("health")["tiers"][2]["reachable"])

    def test_the_tools_own_files_are_not_memory(self):
        self.install()
        a = self.tool("search", "--pattern", "Garura memory", "--tier", "garura")
        self.assertEqual(a["hits"], [])

    def test_codex_keeps_the_projects_own_agents_md_and_adds_one_block(self):
        os.makedirs(self.target)
        with open(self.path("AGENTS.md"), "w") as fh:
            fh.write("# Our own rules\nKeep it simple.\n")
        self.install("codex")
        self.install("codex")  # a re-install replaces the block, never adds a second
        with open(self.path("AGENTS.md")) as fh:
            text = fh.read()
        self.assertTrue(text.startswith("# Our own rules\nKeep it simple.\n"))
        self.assertEqual(text.count(memory_system.BLOCK_START), 1)
        self.assertIn("python3 .garura/tools/memory/memory.py search", text)
        self.assertFalse(os.path.exists(self.path(".claude", "rules")))

    def test_a_reinstall_keeps_settings_a_person_edited(self):
        self.install()
        settings = self.path(".garura", "tools", "memory", "settings.json")
        with open(settings) as fh:
            edited = json.load(fh)
        edited["phoenix_ref"] = "main"
        with open(settings, "w") as fh:
            json.dump(edited, fh)
        self.install()
        with open(settings) as fh:
            self.assertEqual(json.load(fh)["phoenix_ref"], "main")


class TheCheck(Installed):
    def test_no_short_term_folder_fails_and_names_short_term_memory(self):
        self.install()
        os.rmdir(self.path(".garura", "project", "issues"))
        report = memory_system.check(self.target, info=lambda m: None)
        self.assertFalse(report["ok"])
        self.assertIn("Short-term memory cannot be reached", " ".join(report["messages"]))

    def test_a_tool_that_cannot_run_fails(self):
        self.install()
        with open(self.path(".garura", "tools", "memory", "memory.py"), "w") as fh:
            fh.write("this is not python\n")
        report = memory_system.check(self.target, info=lambda m: None)
        self.assertFalse(report["ok"])
        self.assertIn("did not run", " ".join(report["messages"]))

    def test_a_failed_check_makes_the_install_exit_1_after_writing_the_manifest(self):
        old = memory_system.check
        memory_system.check = lambda target, info=print: {"ok": False, "messages": ["FAIL: test"], "tiers": {}}
        self.addCleanup(setattr, memory_system, "check", old)
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as stop:
                install.main(["--target", self.target, "--scope", "harness", "--quiet",
                              "--memory-dest", os.path.join(self.work, "shared-memory"),
                              "--phoenix-place", self.place, "--phoenix-source", self.source])
        self.assertEqual(stop.exception.code, 1)
        self.assertTrue(os.path.isfile(self.path(".garura", "install-manifest.json")))


class Uninstall(Installed):
    def run_main(self, tool):
        with contextlib.redirect_stdout(io.StringIO()):
            install.main(["--target", self.target, "--tool", tool, "--scope", "harness", "--quiet",
                          "--memory-dest", os.path.join(self.work, "shared-memory"),
                          "--phoenix-place", self.place, "--phoenix-source", self.source])
            uninstall.uninstall(self.target, purge=False, quiet=True, dry=False)

    def test_uninstall_removes_the_tool_and_the_guide(self):
        self.run_main("claude")
        for gone in ((".garura", "tools"), (".claude", "rules"), (".garura", "project", "issues")):
            self.assertFalse(os.path.exists(self.path(*gone)), gone)

    def test_uninstall_takes_out_only_the_block_from_the_projects_agents_md(self):
        os.makedirs(self.target)
        with open(self.path("AGENTS.md"), "w") as fh:
            fh.write("# Our own rules\nKeep it simple.\n")
        self.run_main("codex")
        with open(self.path("AGENTS.md")) as fh:
            self.assertEqual(fh.read(), "# Our own rules\nKeep it simple.\n")

    def test_short_term_memory_with_work_in_it_is_kept(self):
        with contextlib.redirect_stdout(io.StringIO()):
            install.main(["--target", self.target, "--scope", "harness", "--quiet",
                          "--memory-dest", os.path.join(self.work, "shared-memory"),
                          "--phoenix-place", self.place, "--phoenix-source", self.source])
        os.makedirs(self.path(".garura", "project", "issues", "1", "specs"))
        with open(self.path(".garura", "project", "issues", "1", "specs", "plan.md"), "w") as fh:
            fh.write("the person's work\n")
        uninstall.uninstall(self.target, purge=False, quiet=True, dry=False)
        self.assertTrue(os.path.isfile(self.path(".garura", "project", "issues", "1", "specs", "plan.md")))

    def test_both_scripts_use_the_same_block_markers(self):
        self.assertEqual((uninstall.BLOCK_START, uninstall.BLOCK_END),
                         (memory_system.BLOCK_START, memory_system.BLOCK_END))


if __name__ == "__main__":
    unittest.main(verbosity=1)
