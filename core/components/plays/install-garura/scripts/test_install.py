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
import tarfile
import tempfile
import unittest
from unittest import mock

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

    def test_a_reinstall_that_stops_part_way_keeps_the_tool_and_its_settings(self):
        self.install()
        settings = self.path(".garura", "tools", "memory", "settings.json")
        with open(settings, "w") as fh:
            fh.write('{"edited": true}\n')
        with mock.patch.object(memory_system.shutil, "copytree", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                memory_system.lay(ROOT, self.target, "claude", self.place, self.source, info=lambda m: None)
        self.assertTrue(os.path.isfile(self.path(".garura", "tools", "memory", "memory.py")))
        with open(settings) as fh:
            self.assertEqual(json.load(fh), {"edited": True})
        self.assertFalse(os.path.exists(self.path(".garura", "tools", "memory.new")))  # no half copy left

    def test_bad_input_exits_2_not_like_a_failed_check(self):
        os.makedirs(self.target)
        for source, tool in ((self.work, "claude"), (ROOT, "vim")):
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as stop:
                memory_system.lay(source, self.target, tool, info=lambda m: None)
            self.assertEqual(stop.exception.code, 2)

    def test_a_stray_end_marker_before_the_block_does_not_stop_the_block_being_replaced(self):
        text = f"# Ours\n{memory_system.BLOCK_END}\n\n{memory_system.BLOCK_START}\nold\n{memory_system.BLOCK_END}\n"
        self.assertEqual(memory_system.strip_block(text), f"# Ours\n{memory_system.BLOCK_END}\n")


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

    def test_an_old_python_fails_and_names_the_version_needed(self):
        self.install()
        with mock.patch.object(memory_system, "NEEDS_PYTHON", (99, 0)):
            report = memory_system.check(self.target, info=lambda m: None)
        self.assertFalse(report["ok"])
        self.assertIn("needs Python 99.0 or newer", " ".join(report["messages"]))

    def test_a_tool_that_answers_not_ok_in_another_shape_fails_with_a_message(self):
        self.install()
        with open(self.path(".garura", "tools", "memory", "memory.py"), "w") as fh:
            fh.write('print(\'{"ok": false}\')\n')
        report = memory_system.check(self.target, info=lambda m: None)
        self.assertFalse(report["ok"])
        self.assertIn("the memory tool answered not ok", " ".join(report["messages"]))

    def test_an_answer_the_check_cannot_read_fails_with_a_message(self):
        self.install()
        for answer in ('[1]', '{"ok": true, "tiers": [1]}'):
            with open(self.path(".garura", "tools", "memory", "memory.py"), "w") as fh:
                fh.write(f"print('{answer}')\n")
            report = memory_system.check(self.target, info=lambda m: None)
            self.assertFalse(report["ok"])
            self.assertIn("cannot read", " ".join(report["messages"]))

    def test_a_source_that_does_not_answer_is_noted_and_does_not_fail(self):
        self.source = os.path.join(self.work, "no-such-repository")
        record = self.install()["memory_system"]["check"]
        self.assertTrue(record["ok"])
        self.assertIn("does not answer from here now", " ".join(record["messages"]))

    def test_a_source_that_answers_is_not_noted(self):
        record = self.install()["memory_system"]["check"]
        self.assertNotIn("NOTE", " ".join(record["messages"]))

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

    def test_a_dry_run_leaves_the_memory_system_in_place(self):
        with contextlib.redirect_stdout(io.StringIO()):
            install.main(["--target", self.target, "--scope", "harness", "--quiet",
                          "--memory-dest", os.path.join(self.work, "shared-memory"),
                          "--phoenix-place", self.place, "--phoenix-source", self.source])
            uninstall.uninstall(self.target, purge=False, quiet=True, dry=True)
        self.assertTrue(os.path.isfile(self.path(".garura", "tools", "memory", "memory.py")))
        self.assertTrue(os.path.isfile(self.path(".claude", "rules", "garura-memory.md")))

    def test_uninstall_removes_a_half_copy_a_stopped_reinstall_left(self):
        with contextlib.redirect_stdout(io.StringIO()):
            install.main(["--target", self.target, "--scope", "harness", "--quiet",
                          "--memory-dest", os.path.join(self.work, "shared-memory"),
                          "--phoenix-place", self.place, "--phoenix-source", self.source])
        os.makedirs(self.path(".garura", "tools", "memory.new"))
        uninstall.uninstall(self.target, purge=False, quiet=True, dry=False)
        self.assertFalse(os.path.exists(self.path(".garura", "tools")))

    def test_an_agents_md_that_holds_only_the_block_is_removed(self):
        os.makedirs(self.target)
        memory_system.put_block(self.path("AGENTS.md"), "the guide")
        removed = []
        self.assertTrue(uninstall.rm_block(self.path("AGENTS.md"), removed, dry=False))
        self.assertFalse(os.path.exists(self.path("AGENTS.md")))

    def test_both_scripts_use_the_same_block_markers(self):
        self.assertEqual((uninstall.BLOCK_START, uninstall.BLOCK_END),
                         (memory_system.BLOCK_START, memory_system.BLOCK_END))


FAKE_CURL = """#!/bin/sh
# Serves the installer a local Garura in place of GitHub: the archive, and a commit id.
out=""; url=""
while [ $# -gt 0 ]; do
  case "$1" in -o) out="$2"; shift 2 ;; -*) shift ;; *) url="$1"; shift ;; esac
done
case "$url" in
  *archive*) cp "$GARURA_TEST_ARCHIVE" "$out" ;;
  *commits/main*) echo '{"sha": "0123456789abcdef"}' ;;
  *) exit 22 ;;
esac
"""


class PublicInstaller(unittest.TestCase):
    """installer/install.sh, run whole, with a local Garura served in place of the download."""

    def setUp(self):
        self.work = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.work, ignore_errors=True)
        self.target = os.path.join(self.work, "shop")
        os.makedirs(self.target)
        self.bin = os.path.join(self.work, "bin")
        os.makedirs(self.bin)
        with open(os.path.join(self.bin, "curl"), "w") as fh:
            fh.write(FAKE_CURL)
        os.chmod(os.path.join(self.bin, "curl"), 0o755)

    def archive(self, change=None):
        """A copy of this Garura as a release archive; `change` edits the copy first."""
        copy = os.path.join(self.work, "garura-main")
        shutil.rmtree(copy, ignore_errors=True)
        shutil.copytree(os.path.join(ROOT, "core"), os.path.join(copy, "core"),
                        ignore=shutil.ignore_patterns("play-reviewer", "node_modules", "__pycache__"))
        os.makedirs(os.path.join(copy, ".garura", "core"))
        shutil.copy(os.path.join(ROOT, ".garura", "core", "config.yaml"), os.path.join(copy, ".garura", "core"))
        shutil.copy(os.path.join(ROOT, "CLAUDE.md"), copy)
        if change:
            change(copy)
        path = os.path.join(self.work, "garura.tar.gz")
        with tarfile.open(path, "w:gz") as tar:
            tar.add(copy, arcname="garura-main")
        return path

    def run_installer(self, archive):
        # Phoenix memory's default source is answered by a local repository: no network, no keychain
        home = os.path.join(self.work, "home")
        source = os.path.join(self.work, "phoenix-source")
        if not os.path.isdir(source):
            os.makedirs(home)
            git(self.work, "init", "-q", "--bare", source)
            with open(os.path.join(home, ".gitconfig"), "w") as fh:
                fh.write(f'[url "{source}"]\n\tinsteadOf = {memory_system.PHOENIX_SOURCE}\n')
        env = dict(os.environ, PATH=self.bin + os.pathsep + os.environ["PATH"], GARURA_TEST_ARCHIVE=archive,
                   HOME=home, GIT_CONFIG_NOSYSTEM="1")
        env = {k: v for k, v in env.items() if not k.startswith("MEMORY_")}
        return subprocess.run(["bash", os.path.join(ROOT, "installer", "install.sh"), "--version", "main"],
                              cwd=self.target, env=env, capture_output=True, text=True)

    def path(self, *parts):
        return os.path.join(self.target, *parts)

    def test_it_lays_the_memory_system_and_records_the_version(self):
        run = self.run_installer(self.archive())
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertTrue(os.path.isfile(self.path(".garura", "tools", "memory", "memory.py")))
        self.assertTrue(os.path.isfile(self.path(".garura", "tools", "memory", "settings.json")))
        self.assertTrue(os.path.isfile(self.path(".claude", "rules", "garura-memory.md")))
        self.assertIn("Short-term memory: reached.", run.stdout)
        self.assertFalse(os.path.exists(os.path.join(self.work, "home", ".garura", "phoenix-memory")))
        with open(self.path(".garura", "core", "garura-version")) as fh:
            self.assertEqual(fh.read().strip(), "main@01234567")

    def test_a_failed_check_exits_1_after_the_version_is_recorded(self):
        def broken(copy):
            with open(os.path.join(copy, "core", "tools", "memory", "memory.py"), "w") as fh:
                fh.write("this is not python\n")
        run = self.run_installer(self.archive(broken))
        self.assertEqual(run.returncode, 1)
        self.assertIn("the memory check failed", run.stderr)
        self.assertTrue(os.path.isfile(self.path(".garura", "core", "garura-version")))

    def test_an_upgrade_keeps_settings_a_person_edited(self):
        archive = self.archive()
        self.assertEqual(self.run_installer(archive).returncode, 0)
        settings = self.path(".garura", "tools", "memory", "settings.json")
        with open(settings) as fh:
            edited = dict(json.load(fh), phoenix_ref="main")
        with open(settings, "w") as fh:
            json.dump(edited, fh)
        run = self.run_installer(archive)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("upgraded", run.stdout)
        with open(settings) as fh:
            self.assertEqual(json.load(fh)["phoenix_ref"], "main")

    def test_a_release_without_the_memory_system_installs_as_before(self):
        def older(copy):
            os.remove(os.path.join(copy, "core", "components", "plays", "install-garura", "scripts", "memory_system.py"))
        run = self.run_installer(self.archive(older))
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("no memory system; skipped", run.stdout)
        self.assertFalse(os.path.exists(self.path(".garura", "tools")))


if __name__ == "__main__":
    unittest.main(verbosity=1)
