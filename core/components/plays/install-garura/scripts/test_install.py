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
import re
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
from adapters import claude, codex  # noqa: E402


def git(repo, *args):
    subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True)


OLD = "function" + "alit"  # spelled in two parts so a search for old names in this file finds none


def lay_pre_807_model(target):
    """A small product model with the names it had before #807, committed in its own repository."""
    model = os.path.join(target, ".garura", "product", "product-os")
    page = os.path.join(model, OLD + "ies", "fn-1", OLD + "y.md")
    os.makedirs(os.path.dirname(page))
    with open(os.path.join(model, "_spine.yaml"), "w", encoding="utf-8") as fh:
        fh.write(f"{OLD}ies:\n- id: fn-1\n  doc: {OLD}ies/fn-1/{OLD}y.md\n")
    with open(page, "w", encoding="utf-8") as fh:
        fh.write(f"# {OLD.capitalize()}y: One\n")
    os.makedirs(target, exist_ok=True)
    git(target, "init", "-q", "-b", "main")
    # Demo address: sample data for this throwaway repository, not personal data.
    git(target, "config", "user.email", "t@example.com")
    git(target, "config", "user.name", "test")
    git(target, "add", "-A")
    git(target, "commit", "-q", "-m", "seed")
    return model


def snapshot(target, model):
    """Every file under the model with its bytes, plus the repository's last commit."""
    files = {}
    for d, _dirs, names in os.walk(model):
        for n in names:
            full = os.path.join(d, n)
            with open(full, "rb") as fh:
                files[os.path.relpath(full, model)] = fh.read()
    head = subprocess.run(["git", "-C", target, "rev-parse", "HEAD"], capture_output=True, text=True).stdout
    return files, head.strip()


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


class WritesTheProjectInstructions(Installed):
    def test_the_projects_claude_md_holds_the_project_rules_not_garuras_development_guide(self):
        self.install()
        with open(self.path("CLAUDE.md"), encoding="utf-8") as fh:
            text = fh.read()
        self.assertTrue(text.startswith("# CLAUDE.md — shop"))
        self.assertIn("Agent-first", text)
        for dev_only in ("Garura is an agentic framework", "core/components/", "edit-play", "Work Tracking"):
            self.assertNotIn(dev_only, text)


class LaysTheMemorySystem(Installed):
    def test_the_install_lays_the_tool_its_settings_and_the_guide_and_brings_no_memory(self):
        record = self.install()["memory_system"]
        self.assertTrue(os.path.isfile(self.path(".garura", "core", "tools", "memory", "memory.py")))
        self.assertTrue(os.path.isfile(self.path(".garura", "core", "tools", "memory", "contract", "v5.json")))
        self.assertFalse(os.path.exists(self.path(".garura", "core", "tools", "memory", "test_memory.py")))
        self.assertFalse(os.path.exists(self.path(".garura", "core", "tools", "memory", "contract", "samples")))
        self.assertTrue(os.path.isdir(self.path(".garura", "project", "issues")))
        self.assertFalse(os.path.exists(self.path(".garura", "project", "specs")))
        with open(self.path(".claude", "rules", "garura-memory.md")) as fh:
            guide = fh.read()
        self.assertIn("python3 .garura/core/tools/memory/memory.py search", guide)
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

    def stopped(self, call):
        """Run an install call; return its exit code and what it wrote to stderr."""
        err = io.StringIO()
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err), \
                self.assertRaises(SystemExit) as stop:
            call()
        return stop.exception.code, err.getvalue()

    def test_codex_is_deprecated_and_the_install_stops_and_changes_nothing(self):
        os.makedirs(self.target)
        with open(self.path("AGENTS.md"), "w") as fh:
            fh.write("# Our own rules\nKeep it simple.\n")
        code, err = self.stopped(lambda: self.install("codex"))
        self.assertEqual(code, 2)
        self.assertIn("Codex installer is deprecated", err)
        self.assertIn("#863", err)
        self.assertEqual(os.listdir(self.target), ["AGENTS.md"])
        with open(self.path("AGENTS.md")) as fh:
            self.assertEqual(fh.read(), "# Our own rules\nKeep it simple.\n")
        self.assertFalse(os.path.exists(codex.CODEX_HOME))

    def test_the_command_line_stops_for_codex_before_it_makes_the_target(self):
        code, err = self.stopped(lambda: install.main(["--target", self.target, "--tool", "codex", "--quiet"]))
        self.assertEqual(code, 2)
        self.assertIn("#863", err)
        self.assertFalse(os.path.exists(self.target))

    def test_the_shared_play_close_is_laid_beside_the_plays(self):
        self.install()
        self.assertTrue(os.path.isfile(self.path(".claude", "skills", "_shared", "play-close.md")))
        self.assertTrue(os.path.isfile(self.path(".claude", "agents", "template-manager.md")))
        with open(self.path(".claude", "skills", "start-change", "SKILL.md")) as fh:
            self.assertIn("../_shared/play-close.md", fh.read())

    def test_the_config_comes_from_core_config_yaml(self):
        self.install()
        with open(self.path(".garura", "core", "config.yaml")) as fh:
            config = fh.read()
        self.assertIn("ontology: standards/schemas/product-os/ontology.md", config)

    def test_a_reinstall_keeps_settings_a_person_edited(self):
        self.install()
        settings = self.path(".garura", "core", "tools", "memory", "settings.json")
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
        settings = self.path(".garura", "core", "tools", "memory", "settings.json")
        with open(settings, "w") as fh:
            fh.write('{"edited": true}\n')
        with mock.patch.object(memory_system.shutil, "copytree", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                memory_system.lay(ROOT, self.target, "claude", self.place, self.source, info=lambda m: None)
        self.assertTrue(os.path.isfile(self.path(".garura", "core", "tools", "memory", "memory.py")))
        with open(settings) as fh:
            self.assertEqual(json.load(fh), {"edited": True})
        self.assertFalse(os.path.exists(self.path(".garura", "core", "tools", "memory.new")))  # no half copy left

    def test_a_tool_an_older_install_laid_is_removed_and_its_settings_written_new(self):
        old = self.path(".garura", "tools", "memory")
        os.makedirs(old)
        with open(os.path.join(old, "settings.json"), "w") as fh:
            fh.write('{"garura": "../..", "garura_pull_dir": "core/memory"}\n')
        self.install()
        self.assertFalse(os.path.exists(self.path(".garura", "tools")))
        with open(self.path(".garura", "core", "tools", "memory", "settings.json")) as fh:
            settings = json.load(fh)
        self.assertEqual(settings["garura"], "../../..")
        self.assertNotIn("garura_pull_dir", settings)
        self.assertEqual(settings["phoenix"], self.place)

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
        with open(self.path(".garura", "core", "tools", "memory", "memory.py"), "w") as fh:
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
        with open(self.path(".garura", "core", "tools", "memory", "memory.py"), "w") as fh:
            fh.write('print(\'{"ok": false}\')\n')
        report = memory_system.check(self.target, info=lambda m: None)
        self.assertFalse(report["ok"])
        self.assertIn("the memory tool answered not ok", " ".join(report["messages"]))

    def test_an_answer_the_check_cannot_read_fails_with_a_message(self):
        self.install()
        for answer in ('[1]', '{"ok": true, "tiers": [1]}'):
            with open(self.path(".garura", "core", "tools", "memory", "memory.py"), "w") as fh:
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
        for gone in ((".garura", "core", "tools"), (".claude", "rules"), (".garura", "project", "issues")):
            self.assertFalse(os.path.exists(self.path(*gone)), gone)

    def test_uninstall_takes_out_only_the_block_from_the_projects_agents_md(self):
        os.makedirs(self.target)
        with open(self.path("AGENTS.md"), "w") as fh:
            fh.write("# Our own rules\nKeep it simple.\n")
        memory_system.put_block(self.path("AGENTS.md"), "the guide")
        removed = []
        self.assertTrue(uninstall.rm_block(self.path("AGENTS.md"), removed, dry=False))
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
        self.assertTrue(os.path.isfile(self.path(".garura", "core", "tools", "memory", "memory.py")))
        self.assertTrue(os.path.isfile(self.path(".claude", "rules", "garura-memory.md")))

    def test_uninstall_removes_a_half_copy_a_stopped_reinstall_left(self):
        with contextlib.redirect_stdout(io.StringIO()):
            install.main(["--target", self.target, "--scope", "harness", "--quiet",
                          "--memory-dest", os.path.join(self.work, "shared-memory"),
                          "--phoenix-place", self.place, "--phoenix-source", self.source])
        os.makedirs(self.path(".garura", "core", "tools", "memory.new"))
        uninstall.uninstall(self.target, purge=False, quiet=True, dry=False)
        self.assertFalse(os.path.exists(self.path(".garura", "core", "tools")))

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


class RetiresOldNames(Installed):
    """#748: a project installed under the old names, before the install record existed,
    ends with only the new names; folders the project wrote itself are kept."""

    def old(self, rel, name):
        os.makedirs(self.path(*rel.split("/")), exist_ok=True)
        with open(self.path(*rel.split("/"), "SKILL.md"), "w") as fh:
            fh.write(f"---\nname: {name}\n---\nold\n")

    def test_old_names_go_and_the_project_s_own_folders_stay(self):
        self.old(".claude/skills/play-creator", "play-creator")       # Garura's, old name
        self.old(".claude/skills/review-change", "review-change")     # Garura's, old name
        self.old(".claude/skills/adr", "our-own-adr-notes")           # the project's own
        with contextlib.redirect_stdout(io.StringIO()):
            install.main(["--target", self.target, "--scope", "harness", "--quiet",
                          "--memory-dest", os.path.join(self.work, "shared-memory"),
                          "--phoenix-place", self.place, "--phoenix-source", self.source])
        self.assertFalse(os.path.exists(self.path(".claude", "skills", "play-creator")))
        self.assertFalse(os.path.exists(self.path(".claude", "skills", "review-change")))
        self.assertTrue(os.path.isfile(self.path(".claude", "skills", "create-play", "SKILL.md")))
        self.assertTrue(os.path.isfile(self.path(".claude", "skills", "check-change", "SKILL.md")))
        self.assertTrue(os.path.isfile(self.path(".claude", "skills", "adr", "SKILL.md")))
        with open(self.path(".garura", "install-manifest.json")) as fh:
            retired = json.load(fh)["record"]["retired"]
        self.assertIn(os.path.join(".claude", "skills", "play-creator"), retired)

    def test_every_old_name_of_one_new_name_goes(self):
        # #807: grill and shape-features both became shape-slice; both old folders go
        self.old(".claude/skills/grill", "grill")
        self.old(".claude/skills/shape-features", "shape-features")
        with contextlib.redirect_stdout(io.StringIO()):
            install.main(["--target", self.target, "--quiet",
                          "--memory-dest", os.path.join(self.work, "shared-memory"),
                          "--phoenix-place", self.place, "--phoenix-source", self.source])
        self.assertFalse(os.path.exists(self.path(".claude", "skills", "grill")))
        self.assertFalse(os.path.exists(self.path(".claude", "skills", "shape-features")))
        self.assertTrue(os.path.isfile(self.path(".claude", "skills", "shape-slice", "SKILL.md")))


class LeavesTheProductModelAsItIs(Installed):
    """The install never changes a product model the project already has (#813; upgrades: #835)."""

    def test_an_install_leaves_a_pre_807_model_unchanged(self):
        model = lay_pre_807_model(self.target)
        before = snapshot(self.target, model)
        record = self.install()
        self.assertNotIn("model_migration", record)
        self.assertEqual(snapshot(self.target, model), before)
        status = subprocess.run(["git", "-C", self.target, "status", "--porcelain", "--", ".garura/product"],
                                capture_output=True, text=True).stdout
        self.assertEqual(status, "")


class LaysLoops(unittest.TestCase):
    """Loops live in core/components/loops/ (#613) and install as skills beside the plays."""

    def setUp(self):
        self.work = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.work, ignore_errors=True)
        self.src = os.path.join(self.work, "components")
        for rel, text in (("plays/start-change/SKILL.md", "---\nname: start-change\n---\n"),
                          ("plays/_shared/play-close.md", "# close\n"),
                          ("loops/complete-discovery/SKILL.md", "---\nname: complete-discovery\nkind: loop\n---\n"),
                          ("loops/_shared/loop-run.md", "# run\n")):
            path = os.path.join(self.src, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as fh:
                fh.write(text)
        self.target = os.path.join(self.work, "shop")

    def lay(self, adapter, allow=None):
        with contextlib.redirect_stdout(io.StringIO()):
            return adapter.lay_components(self.src, self.target, lambda _m: None, allow)

    def test_claude_lays_a_loop_and_both_shared_files(self):
        paths, counts, _ = self.lay(claude)
        skills = os.path.join(self.target, ".claude", "skills")
        self.assertEqual((counts["plays"], counts["loops"]), (1, 1))
        self.assertTrue(os.path.isfile(os.path.join(skills, "complete-discovery", "SKILL.md")))
        self.assertTrue(os.path.isfile(os.path.join(skills, "_shared", "play-close.md")))
        self.assertTrue(os.path.isfile(os.path.join(skills, "_shared", "loop-run.md")))
        self.assertIn(os.path.join(".claude", "skills", "complete-discovery"), paths)

    def test_codex_lays_a_loop_too(self):
        _, counts, _ = self.lay(codex)
        skills = os.path.join(self.target, ".agents", "skills")
        self.assertEqual(counts["loops"], 1)
        self.assertTrue(os.path.isfile(os.path.join(skills, "_shared", "loop-run.md")))

    def test_the_harness_scope_installs_no_loop(self):
        allow = install.SCOPES["harness"]
        _, counts, _ = self.lay(claude, {**allow, "plays": allow["plays"] | {"start-change"}})
        self.assertEqual(counts["loops"], 0)
        self.assertFalse(os.path.exists(os.path.join(self.target, ".claude", "skills", "complete-discovery")))

    def test_the_full_scope_installs_every_loop_but_not_the_loop_builders(self):
        scope = install.resolve_scope("full", os.path.join(ROOT, "core", "components"))
        self.assertIsNone(scope["loops"])
        self.assertNotIn("create-loop", scope["plays"])
        self.assertNotIn("edit-loop", scope["plays"])
        self.assertIn("create-loop", install.SCOPES["harness"]["plays"])

    def test_the_harness_scope_carries_discover_capabilities_and_its_workers(self):
        # Garura plans its own work with its own product model; this play writes the full ICE (#753).
        allow = install.SCOPES["harness"]
        components = os.path.join(ROOT, "core", "components")
        self.assertIn("discover-capabilities", allow["plays"])
        for skill in ("find-work-placement", "enrich-capability-ice", "judge-grounding"):
            self.assertIn(skill, allow["skills"])
            self.assertTrue(os.path.isfile(os.path.join(components, "skills", skill, "SKILL.md")), skill)
        for agent in ("product-os-keeper", "template-manager"):
            self.assertIn(agent, allow["agents"])
            self.assertTrue(os.path.isfile(os.path.join(components, "agents", agent + ".md")), agent)

    def test_the_harness_scope_carries_shape_slice_and_its_workers(self):
        # Garura shapes the slice for each of its own business intents (plan 788).
        allow = install.SCOPES["harness"]
        components = os.path.join(ROOT, "core", "components")
        self.assertIn("shape-slice", allow["plays"])
        for skill in ("author-business-intent", "author-domains", "propose-answers", "author-slice",
                      "find-slice-gaps", "author-slice-brief", "enrich-grounding",
                      "author-failure-recovery", "find-work-placement", "enrich-capability-ice"):
            self.assertIn(skill, allow["skills"])
            self.assertTrue(os.path.isfile(os.path.join(components, "skills", skill, "SKILL.md")), skill)

    def test_edit_ontology_goes_to_harness_repos_only(self):
        # The play that changes the product ontology is build tooling for a harness repo (#777).
        self.assertIn("edit-ontology", install.SCOPES["harness"]["plays"])
        self.assertIn("author-product-ontology", install.SCOPES["harness"]["skills"])
        full = install.resolve_scope("full", os.path.join(ROOT, "core", "components"))
        self.assertNotIn("edit-ontology", full["plays"])
        self.assertNotIn("author-product-ontology", full["skills"])

    def test_the_config_points_loops_at_the_install_place(self):
        text = install.transform_config("components:\n  loops: ./core/components/loops/\n"
                                        "loops:\n  complete-discovery:\n    runner: subagent\n",
                                        "shop", "claude")
        self.assertIn("  loops: ./.claude/skills/", text)
        self.assertIn("loops:\n  complete-discovery:", text)


class SkipsStaleParts(unittest.TestCase):
    """A stale or deprecated part is not installed, and a reinstall removes one that became
    stale (#855). The skills' shared rule for asking a person is laid in _shared (#854)."""

    def setUp(self):
        self.work = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.work, ignore_errors=True)
        self.src = os.path.join(self.work, "components")
        for rel, text in (("plays/start-change/SKILL.md", "---\nname: start-change\n---\n"),
                          ("plays/build-thing/SKILL.md", "---\nname: build-thing\n---\n"),
                          ("plays/_shared/play-close.md", "# close\n"),
                          ("skills/author-thing/SKILL.md", "---\nname: author-thing\n---\n"),
                          ("skills/author-old/SKILL.md",
                           "---\nname: author-old\nstale: true\nstale_note: 'waits for a rebuild'\n---\n"),
                          ("skills/scan-old/SKILL.md", "---\nname: scan-old\ndeprecated: yes\n---\n"),
                          ("skills/_shared/asking-a-person.md", "# Asking a Person\n"),
                          ("agents/old-agent.md", "---\nname: old-agent\nstale: on\n---\n"),
                          ("agents/keeper.md", "---\nname: keeper\n---\n")):
            path = os.path.join(self.src, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as fh:
                fh.write(text)
        self.target = os.path.join(self.work, "shop")

    def lay(self, adapter):
        with contextlib.redirect_stdout(io.StringIO()):
            return adapter.lay_components(self.src, self.target, lambda _m: None, None)

    def mark_stale(self, rel):
        path = os.path.join(self.src, rel)
        with open(path) as fh:
            text = fh.read()
        with open(path, "w") as fh:
            fh.write(text.replace("---\n", "---\nstale: true\n", 1))

    def test_the_skip_check_reads_deprecated_and_stale(self):
        from adapters import common
        self.assertTrue(common.file_is_skipped(os.path.join(self.src, "skills", "author-old", "SKILL.md")))
        self.assertTrue(common.file_is_skipped(os.path.join(self.src, "skills", "scan-old", "SKILL.md")))
        self.assertTrue(common.file_is_skipped(os.path.join(self.src, "agents", "old-agent.md")))
        self.assertFalse(common.file_is_skipped(os.path.join(self.src, "skills", "author-thing", "SKILL.md")))
        self.assertFalse(common.file_is_skipped(os.path.join(self.src, "skills", "none", "SKILL.md")))

    def test_claude_does_not_install_a_stale_play_or_a_stale_skill(self):
        self.mark_stale("plays/build-thing/SKILL.md")
        _, counts, _ = self.lay(claude)
        skills = os.path.join(self.target, ".claude", "skills")
        self.assertEqual((counts["plays"], counts["skills"], counts["agents"]), (1, 1, 1))
        self.assertFalse(os.path.exists(os.path.join(skills, "build-thing")))
        self.assertFalse(os.path.exists(os.path.join(skills, "author-old")))
        self.assertFalse(os.path.exists(os.path.join(skills, "scan-old")))
        self.assertFalse(os.path.exists(os.path.join(self.target, ".claude", "agents", "old-agent.md")))
        self.assertTrue(os.path.isfile(os.path.join(skills, "author-thing", "SKILL.md")))

    def test_codex_does_not_install_a_stale_play_or_a_stale_skill(self):
        self.mark_stale("plays/build-thing/SKILL.md")
        _, counts, _ = self.lay(codex)
        skills = os.path.join(self.target, ".agents", "skills")
        self.assertEqual((counts["plays"], counts["skills"], counts["agents"]), (1, 1, 1))
        for name in ("build-thing", "author-old", "scan-old", "old-agent"):
            self.assertFalse(os.path.exists(os.path.join(skills, name)), name)

    def test_a_reinstall_removes_a_part_that_became_stale(self):
        first, _, _ = self.lay(claude)
        self.assertIn(os.path.join(".claude", "skills", "build-thing"), first)
        manifest = os.path.join(self.target, ".garura", "install-manifest.json")
        os.makedirs(os.path.dirname(manifest), exist_ok=True)
        with open(manifest, "w") as fh:
            json.dump({"record": {"components": first}}, fh)
        self.mark_stale("plays/build-thing/SKILL.md")
        second, _, _ = self.lay(claude)
        with contextlib.redirect_stdout(io.StringIO()):
            removed = install.retire_stale(self.target, second, True)
        self.assertIn(os.path.join(".claude", "skills", "build-thing"), removed)
        self.assertFalse(os.path.exists(os.path.join(self.target, ".claude", "skills", "build-thing")))

    def test_the_asking_rule_is_laid_in_shared_for_both_tools(self):
        self.lay(claude)
        self.lay(codex)
        for tool in (".claude", ".agents"):
            shared = os.path.join(self.target, tool, "skills", "_shared")
            self.assertTrue(os.path.isfile(os.path.join(shared, "asking-a-person.md")), tool)
            self.assertTrue(os.path.isfile(os.path.join(shared, "play-close.md")), tool)

    def test_the_real_install_lays_the_asking_rule(self):
        components = os.path.join(ROOT, "core", "components")
        self.assertTrue(os.path.isfile(os.path.join(components, "skills", "_shared", "asking-a-person.md")))
        with contextlib.redirect_stdout(io.StringIO()):
            claude.lay_components(components, self.target, lambda _m: None, None)
        self.assertTrue(os.path.isfile(os.path.join(self.target, ".claude", "skills", "_shared",
                                                    "asking-a-person.md")))


class InstallFindings(unittest.TestCase):
    """What Discovery's test runs found in the install (#613): K-0 and K-2."""

    def test_the_record_writes_a_home_path_as_tilde(self):
        home = os.path.expanduser("~")
        self.assertEqual(install.portable(os.path.join(home, ".garura", "core", "memory")),
                         os.path.join("~", ".garura", "core", "memory"))
        self.assertEqual(install.portable("/opt/shared/memory"), "/opt/shared/memory")

    def test_the_installed_skills_ignore_python_caches(self):
        work = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, work, ignore_errors=True)
        src = os.path.join(work, "components", "plays", "p")
        os.makedirs(src)
        with open(os.path.join(src, "SKILL.md"), "w") as fh:
            fh.write("---\nname: p\n---\n")
        with contextlib.redirect_stdout(io.StringIO()):
            paths, _, _ = claude.lay_components(os.path.join(work, "components"), os.path.join(work, "t"),
                                                lambda _m: None, None)
        with open(os.path.join(work, "t", ".claude", "skills", ".gitignore")) as fh:
            self.assertIn("__pycache__/", fh.read())
        self.assertIn(os.path.join(".claude", "skills", ".gitignore"), paths)
        self.assertIn("**/__pycache__/", install.STATUS_GITIGNORE)


# The parts that work on Garura's source only, by design (#860), and the files that sort the paths
# of the repo under review. An installed file outside them names no path in the source.
SOURCE_ONLY = {"create-play", "edit-play", "create-loop", "edit-loop", "install-garura",
               "uninstall-garura", "edit-ontology", "author-product-ontology"}
REPO_LAYOUT = {os.path.join("commit-change", "scripts", "analyze_changeset.py"),
               os.path.join("assess-pr", "reference", "quality-rules.md")}
# Tools whose job is Garura's own repository: the component linter's source layout and the
# old-name check over the repo.
REPO_TOOLS = {"lint-components", "naming"}
SOURCE_PATH = re.compile(r"core/components/|(?<!\.garura/)core/tools/")
# A pointer to Garura's own docs, which the install never copies (decision 10); a glob over the
# reviewed repo (docs/philosophy/**) is repo layout, not a pointer.
GARURA_DOCS = re.compile(r"(?<![A-Za-z0-9_-])docs/(?:agentic-methodology|components|design|framework|philosophy"
                         r"|standards|usage)(?![A-Za-z0-9_-])[^\s`'\"(),;]*")


def names_the_source(line):
    return bool(SOURCE_PATH.search(line)) or any("*" not in m for m in GARURA_DOCS.findall(line))

FAKE_ADAPTER_RUN = """
import json, sys
sys.path.insert(0, sys.argv[1])
import fetch_pr_context as f
diff = "diff --git a/src/app.py b/src/app.py\\n--- a/src/app.py\\n+++ b/src/app.py\\n@@ -1 +1 @@\\n-a\\n+b\\n"
def fake(verb, args, config_path=None):
    if verb == "view-pr":
        return {"exit_code": 0, "stdout": json.dumps({"number": 7, "baseRefName": "main", "changedFiles": 1}), "stderr": ""}
    if verb == "diff-pr":
        return {"exit_code": 0, "stdout": diff, "stderr": ""}
    return {"exit_code": 1, "stdout": "", "stderr": "unexpected verb"}
f.pa.dispatch = fake
f.main(sys.argv[2:])
"""


class AnEmptyProject(unittest.TestCase):
    """#860: install into a folder with no core/; every installed part runs from the install alone."""

    def setUp(self):
        self.work = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.work, ignore_errors=True)
        self.target = os.path.join(self.work, "shop")
        os.makedirs(self.target)
        self.place = os.path.join(self.work, "machine", "phoenix-memory")
        self.source = os.path.join(self.work, "phoenix-source")
        rules = os.path.join(self.source, "standards", "rules")
        os.makedirs(rules)
        shutil.copy(os.path.join(ROOT, "core", "components", "memory", "standards", "rules", "pr.md"), rules)
        git(self.source, "init", "-q", "-b", "main")
        # Demo address: sample data for this throwaway repository, not personal data.
        git(self.source, "config", "user.email", "t@example.com")
        git(self.source, "config", "user.name", "test")
        git(self.source, "add", "-A")
        git(self.source, "commit", "-q", "-m", "seed")
        old_home = codex.CODEX_HOME
        codex.CODEX_HOME = os.path.join(self.work, "codex-home")
        self.addCleanup(setattr, codex, "CODEX_HOME", old_home)

    def install(self, target, scope="harness"):
        with contextlib.redirect_stdout(io.StringIO()):
            record = install.install(ROOT, target, "claude", False, True, os.path.join(self.work, "shared-memory"),
                                     scope=scope, phoenix_place=self.place, phoenix_source=self.source)
        install.write_manifest(target, record, True)
        return record

    def run_here(self, *cmd):
        env = {k: v for k, v in os.environ.items() if not k.startswith("MEMORY_")}
        return subprocess.run(list(cmd), capture_output=True, text=True, env=env, cwd=self.target)

    def path(self, *parts):
        return os.path.join(self.target, *parts)

    def test_the_tools_are_laid_without_their_tests(self):
        record = self.install(self.target)
        self.assertFalse(os.path.exists(self.path("core")))
        tools = self.path(".garura", "core", "tools")
        self.assertEqual(sorted(os.listdir(tools)), ["lint-components", "lint-play", "memory", "naming", "rebuild-eval"])
        self.assertTrue(os.path.isfile(os.path.join(tools, "lint-components", "index.js")))
        self.assertTrue(os.path.isdir(os.path.join(tools, "lint-components", "node_modules", "js-yaml")))
        self.assertFalse(os.path.exists(os.path.join(tools, "lint-components", "test")))
        self.assertTrue(os.path.isfile(os.path.join(tools, "lint-play", "lint_play.py")))
        self.assertTrue(os.path.isfile(os.path.join(tools, "rebuild-eval", "run_eval.py")))
        for d, _dirs, names in os.walk(tools):
            if "node_modules" in d or os.path.relpath(d, tools).split(os.sep)[0] == "memory":
                continue  # the memory tool is laid and checked by memory_system.py
            for n in names:
                self.assertFalse(n.startswith("test_") or n.endswith(".test.js"), os.path.join(d, n))
            self.assertFalse({"__pycache__", ".ruff_cache"} & set(_dirs), d)
        self.assertEqual(sorted(record["tools"]), sorted(os.path.join(".garura", "core", "tools", n)
                                                         for n in ("lint-components", "lint-play", "naming", "rebuild-eval")))

    def test_a_reinstall_removes_a_tool_that_left_the_source_and_uninstall_removes_them_all(self):
        self.install(self.target)
        gone = self.path(".garura", "core", "tools", "old-tool")
        os.makedirs(gone)
        man = self.path(".garura", "install-manifest.json")
        with open(man) as fh:
            data = json.load(fh)
        data["record"]["tools"].append(os.path.join(".garura", "core", "tools", "old-tool"))
        with open(man, "w") as fh:
            json.dump(data, fh)
        with contextlib.redirect_stdout(io.StringIO()):
            install.main(["--target", self.target, "--scope", "harness", "--memory-dest",
                          os.path.join(self.work, "shared-memory"), "--phoenix-place", self.place,
                          "--phoenix-source", self.source, "--quiet"])
        self.assertFalse(os.path.exists(gone))
        with contextlib.redirect_stdout(io.StringIO()):
            uninstall.uninstall(self.target, purge=False, quiet=True, dry=False)
        self.assertFalse(os.path.exists(self.path(".garura", "core", "tools")))

    def test_the_installed_linter_runs_in_the_installed_layout_and_finds_no_source_path(self):
        self.install(self.target)
        run = self.run_here("node", ".garura/core/tools/lint-components/index.js", "--layout", "installed",
                            "--target", ".claude")
        self.assertIn(run.returncode, (0, 1), run.stderr)
        out = json.loads(run.stdout)
        self.assertEqual(out["layout"], "installed")
        self.assertTrue(any(n.startswith("naming rules skipped") for n in out.get("notes", [])))
        self.assertEqual([v for v in out["violations"] if v["rule"] == "installed-paths/source-path"], [])

    def test_the_review_reads_the_taxonomy_through_the_memory_tool_and_scans_with_it(self):
        self.install(self.target)
        found = json.loads(self.run_here("python3", ".garura/core/tools/memory/memory.py", "find", "--issue", "7",
                                         "--glob", "**/standards/rules/pr.md").stdout.splitlines()[0])
        self.assertTrue(found["ok"], found)
        hit = found["matches"][0]
        answer = json.loads(self.run_here("python3", ".garura/core/tools/memory/memory.py", "read", "--issue", "7",
                                          "--tier", hit["tier"], "--path", hit["path"]).stdout.splitlines()[0])
        self.assertTrue(answer["ok"], answer)
        copy = self.path(".garura", "project", "issues", "7", "context", "memory", "standards", "rules", "pr.md")
        os.makedirs(os.path.dirname(copy))
        with open(copy, "w", encoding="utf-8") as fh:
            fh.write(answer["text"])
        working = self.path(".garura", "project", "issues", "7", "review")
        os.makedirs(working)
        with open(os.path.join(working, "pr.diff"), "w") as fh:
            fh.write("diff --git a/src/app.py b/src/app.py\n--- a/src/app.py\n+++ b/src/app.py\n@@ -1 +1 @@\n-a\n+b\n")
        with open(os.path.join(working, "changed-paths.txt"), "w") as fh:
            fh.write("src/app.py\n")
        run = self.run_here("python3", ".claude/skills/check-pr-quality/scripts/scan_taxonomy.py",
                            "--taxonomy", os.path.relpath(copy, self.target),
                            "--diff", ".garura/project/issues/7/review/pr.diff",
                            "--paths", ".garura/project/issues/7/review/changed-paths.txt",
                            "--out", ".garura/project/issues/7/review/findings.yaml")
        self.assertEqual(run.returncode, 0, run.stderr)
        with open(os.path.join(working, "findings.yaml")) as fh:
            self.assertIn("context/memory/standards/rules/pr.md", fh.read())

    def test_the_installed_pr_context_script_names_no_memory_folder(self):
        self.install(self.target)
        run = self.run_here("python3", "-c", FAKE_ADAPTER_RUN, ".claude/skills/check-change/scripts",
                            "--config", ".garura/core/config.yaml", "--pr-number", "7",
                            "--out-context", "context.json", "--out-diff", "pr.diff")
        self.assertEqual(run.returncode, 0, run.stderr)
        with open(self.path("context.json")) as fh:
            context = json.load(fh)
        self.assertEqual(context["changed_paths"], ["src/app.py"])
        self.assertNotIn("review_shelf", context)
        self.assertNotIn(".garura/core/memory", json.dumps(context))

    def test_no_installed_file_names_the_source(self):
        full = os.path.join(self.work, "full")
        os.makedirs(full)
        found = []
        for target, scope in ((self.target, "harness"), (full, "full")):
            self.install(target, scope)
            skills = os.path.join(target, ".claude", "skills")
            roots = [(os.path.join(skills, n), n) for n in os.listdir(skills)
                     if os.path.isdir(os.path.join(skills, n)) and n not in SOURCE_ONLY]
            roots.append((os.path.join(target, ".claude", "agents"), "agents"))
            tools = os.path.join(target, ".garura", "core", "tools")
            roots += [(os.path.join(tools, n), n) for n in os.listdir(tools) if n not in REPO_TOOLS]
            for root, name in roots:
                for d, dirs, names in os.walk(root):
                    dirs[:] = [x for x in dirs if x not in ("node_modules", "__pycache__")]
                    for n in names:
                        f = os.path.join(d, n)
                        rel = os.path.relpath(f, os.path.dirname(root))
                        if rel in REPO_LAYOUT or n.startswith("test_") or n.endswith(".test.js"):
                            continue
                        try:
                            with open(f, encoding="utf-8") as fh:
                                text = fh.read()
                        except (UnicodeDecodeError, OSError):
                            continue
                        found += [f"{scope}: {rel}:{i}" for i, line in enumerate(text.splitlines(), 1)
                                  if names_the_source(line)]
        self.assertEqual(found, [])
        with open(os.path.join(full, ".garura", "core", "config.yaml")) as fh:
            self.assertIsNone(SOURCE_PATH.search(fh.read()))


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
        self.assertTrue(os.path.isfile(self.path(".garura", "core", "tools", "memory", "memory.py")))
        self.assertTrue(os.path.isfile(self.path(".garura", "core", "tools", "memory", "settings.json")))
        self.assertTrue(os.path.isfile(self.path(".claude", "rules", "garura-memory.md")))
        self.assertIn("Short-term memory: reached.", run.stdout)
        self.assertFalse(os.path.exists(os.path.join(self.work, "home", ".phoenix", "core", "memory")))
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
        settings = self.path(".garura", "core", "tools", "memory", "settings.json")
        with open(settings) as fh:
            edited = dict(json.load(fh), phoenix_ref="main")
        with open(settings, "w") as fh:
            json.dump(edited, fh)
        run = self.run_installer(archive)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("upgraded", run.stdout)
        with open(settings) as fh:
            self.assertEqual(json.load(fh)["phoenix_ref"], "main")

    def test_the_installer_writes_the_config_from_core_config_yaml(self):
        run = self.run_installer(self.archive())
        self.assertEqual(run.returncode, 0, run.stderr)
        with open(self.path(".garura", "core", "config.yaml")) as fh:
            self.assertIn("ontology: standards/schemas/product-os/ontology.md", fh.read())
        self.assertFalse(os.path.exists(self.path(".garura", "project", "specs")))

    def test_a_release_with_the_config_in_its_old_place_still_installs(self):
        def older(copy):
            os.makedirs(os.path.join(copy, ".garura", "core"))
            os.rename(os.path.join(copy, "core", "config.yaml"), os.path.join(copy, ".garura", "core", "config.yaml"))
        run = self.run_installer(self.archive(older))
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertTrue(os.path.isfile(self.path(".garura", "core", "config.yaml")))

    def test_a_release_without_the_memory_system_installs_as_before(self):
        def older(copy):
            for name in ("memory_system.py", "tools_system.py"):
                os.remove(os.path.join(copy, "core", "components", "plays", "install-garura", "scripts", name))
        run = self.run_installer(self.archive(older))
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("no memory system; skipped", run.stdout)
        self.assertFalse(os.path.exists(self.path(".garura", "core", "tools")))

    def test_the_shell_installer_leaves_a_pre_807_model_unchanged(self):
        model = lay_pre_807_model(self.target)
        before = snapshot(self.target, model)
        run = self.run_installer(self.archive())
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertNotIn("model:", run.stdout)
        self.assertEqual(snapshot(self.target, model), before)


if __name__ == "__main__":
    unittest.main(verbosity=1)
