#!/usr/bin/env python3
"""Tests for the rebuild eval's scripts. The agents (Claude sessions) are stand-ins here."""
import contextlib
import io
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_output as co  # noqa: E402
import prepare as pr  # noqa: E402
import run_builder as rb  # noqa: E402
import score_drift as sd  # noqa: E402

INTENT = """# Able to see the product intents as business needs

**Outcome:** A product owner opens Intents and sees each business intent with its agent intents under it.
**Why:** A coding agent wrote them; someone must review and approve them before work starts.
**Asked by:** A product owner who defines what a product must do
**Proof it is met:** 90% or more of the intents are approved without change
**Sources:**
- [prototype — file](../../../project/issues/1/evidence/source.md)

**Touches:**
- [Reviewing](../review/domain.md) (domain) — adds
"""
DOMAIN = """# Theme: Review and approval

## Intent
Review work before it is used.

## Sources
- https://example.org/approval-workflows
"""
FUNC = """# Functionality: Finish a review

## What it does
Sends every answer back at once.

## Seen on the prototype
- Catch up view, the finish button: "Finish review"
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
            fh.write(text if isinstance(text, str) else json.dumps(text))
        return path

    def model(self, intent=INTENT, domain=DOMAIN, func=FUNC):
        self.write("pos/intents/see-intents.md", intent)
        self.write("pos/review/domain.md", domain)
        self.write("pos/review/catch-up/capability.md", "# Capability: Catch up\n\n## Seen on the prototype\n"
                                                         "- \"Catch up\"\n")
        self.write("pos/review/catch-up/finish/functionality.md", func)
        self.write("pos/_spine.yaml", "domains: []\n")
        self.write("pos/notes.txt", "not part of the model")
        self.write("proto/argus.html", "<button>Catch up</button><button>Finish review</button>"
                                       "<p>Agents work only on approved pieces.</p>")


class Prepare(Work):
    def test_the_brief_holds_the_model_without_local_links_paths_or_the_prototype_name(self):
        self.model(intent=INTENT + "\nRead from /Users/someone/x/argus.html and .garura/project/issues/1/a.md\n")
        m = pr.prepare(self.p("pos"), self.p("run", "brief"), ["argus.html"])
        text = open(self.p("run", "brief", "intents", "see-intents.md")).read()
        self.assertNotIn("](", text)
        self.assertNotIn("/Users/", text)
        self.assertNotIn(".garura/", text)
        self.assertNotIn("argus.html", text)
        self.assertIn("prototype — file", text)
        self.assertEqual(m["level"], "functionalities")
        self.assertEqual(m["counts"], {"intents": 1, "domain": 1, "capabilities": 1, "functionalities": 1})
        self.assertFalse(os.path.exists(self.p("run", "brief", "notes.txt")))
        self.assertTrue(m["removed"])

    def test_web_links_stay(self):
        self.model()
        pr.prepare(self.p("pos"), self.p("run", "brief"), [])
        self.assertIn("https://example.org/approval-workflows", open(self.p("run", "brief", "review", "domain.md")).read())

    def test_intents_only_is_its_own_level_and_no_intents_is_an_error(self):
        self.write("a/intents/x.md", INTENT)
        self.assertEqual(pr.prepare(self.p("a"), self.p("b"), [])["level"], "intents")
        self.write("c/review/domain.md", DOMAIN)
        with self.assertRaises(OSError):
            pr.prepare(self.p("c"), self.p("d"), [])


class CheckOutput(Work):
    def run_check(self, **kw):
        self.model(**kw)
        pr.prepare(self.p("pos"), self.p("run", "brief"), [])
        proto = co.norm(open(self.p("proto", "argus.html")).read())
        return co.check(self.p("run", "brief"), proto)

    def rules(self, report):
        return {f["rule"] for f in report["findings"]}

    def test_a_complete_model_with_sources_on_the_prototype_passes(self):
        r = self.run_check()
        self.assertTrue(r["ok"], r["findings"])
        self.assertEqual(r["counts"]["quotes_found"], 2)

    def test_a_proof_left_open_fails(self):
        r = self.run_check(intent=INTENT.replace("90% or more of the intents are approved without change",
                                                 "open — the drive asks this"))
        self.assertIn("intent-proof-open", self.rules(r))

    def test_a_missing_intent_field_fails(self):
        r = self.run_check(intent=INTENT.replace("**Asked by:** A product owner who defines what a product must do\n", ""))
        self.assertIn("intent-field", self.rules(r))

    def test_a_domain_without_research_sources_fails(self):
        r = self.run_check(domain="# Theme: Drive review\n\n## Intent\nMade up.\n")
        self.assertIn("domain-research", self.rules(r))

    def test_a_functionality_without_a_source_fails(self):
        r = self.run_check(func="# Functionality: Build-from vs waiting split\n\n## What it does\nA split.\n")
        self.assertIn("source-missing", self.rules(r))

    def test_a_quote_the_prototype_does_not_have_fails(self):
        r = self.run_check(func=FUNC.replace('"Finish review"', '"Build-from vs waiting split"'))
        self.assertIn("source-quote-not-found", self.rules(r))

    def test_curly_quotes_and_spacing_still_match(self):
        r = self.run_check(func=FUNC.replace('"Finish review"', "“Agents work only on  approved pieces.”"))
        self.assertTrue(r["ok"], r["findings"])


INVENTORY = {"screens": [{"id": "s1", "name": "Intents"}, {"id": "s2", "name": "Catch up"}],
             "behaviours": [{"id": "b1", "screen": "s1", "does": "opens Intents", "sees": "the list"},
                            {"id": "b2", "screen": "s1", "does": "opens an intent", "sees": "five sections"},
                            {"id": "b3", "screen": "s2", "does": "presses Finish", "sees": "a summary"},
                            {"id": "b4", "screen": "s2", "does": "undoes", "sees": "the card reopens"}]}
COMPARE = {"results": [{"id": "b1", "verdict": "met"},
                       {"id": "b2", "verdict": "partial", "in_brief": False},
                       {"id": "b3", "verdict": "missing", "in_brief": True},
                       {"id": "b4", "verdict": "missing", "in_brief": False}],
           "extras": [{"what": "a search box", "in_brief": True}, {"what": "dark mode", "in_brief": False}]}


class Score(unittest.TestCase):
    def test_kept_drift_and_brief_covers(self):
        s = sd.score(INVENTORY, COMPARE)["overall"]
        self.assertEqual((s["met"], s["partial"], s["missing"]), (1, 1, 2))
        self.assertEqual(s["kept_pct"], 37.5)      # (1 + 0.5) / 4
        self.assertEqual(s["drift_pct"], 62.5)
        self.assertEqual(s["brief_covers_pct"], 62.5)  # b1 1 + b2 0.5 + b3 1 + b4 0
        self.assertEqual(s["missing_not_in_brief"], 1)
        self.assertEqual(s["missing_in_brief"], 1)

    def test_by_screen_and_extras(self):
        s = sd.score(INVENTORY, COMPARE)
        by = {x["name"]: x for x in s["by_screen"]}
        self.assertEqual(by["Intents"]["kept_pct"], 75.0)
        self.assertEqual(by["Catch up"]["kept_pct"], 0.0)
        self.assertEqual(s["extras"], {"total": 2, "in_brief": 1, "builder_own": 1})
        self.assertEqual([g["id"] for g in s["missing_not_in_brief"]], ["b2", "b4"])

    def test_every_behaviour_needs_exactly_one_result(self):
        with self.assertRaises(ValueError):
            sd.score(INVENTORY, {"results": COMPARE["results"][:3]})
        with self.assertRaises(ValueError):
            sd.score(INVENTORY, {"results": COMPARE["results"] + [{"id": "b1", "verdict": "met"}]})

    def test_a_rebuild_that_does_not_open_keeps_nothing(self):
        s = sd.score(INVENTORY, {"could_not_open": True})
        self.assertTrue(s["could_not_open"])
        self.assertEqual(s["overall"]["kept_pct"], 0.0)


STAND_IN_CLAUDE = """#!/usr/bin/env python3
import json, os, re, sys
text = sys.argv[sys.argv.index("-p") + 1]
if text.startswith("# Build this product"):  # the builder: log what it was given, build the app
    cd = os.getcwd()
    open(os.environ["STAND_IN_LOG"], "w").write(json.dumps({"args": sys.argv[1:], "files": sorted(
        os.path.relpath(os.path.join(r, f), cd) for r, _, fs in os.walk(cd) for f in fs)}))
    if os.environ.get("STAND_IN_BUILD", "1") == "1":
        open(os.path.join(cd, "app", "index.html"), "w").write("<button>Finish review</button>")
    print(json.dumps({"total_cost_usd": 0.02, "num_turns": 3, "result": "built: app/index.html"}))
    sys.exit(0)
out = re.search(r"Write `([^`]+\\.json)`", text).group(1)
data = {"inventory.json": json.loads(%(inv)r), "compare.json": json.loads(%(cmp)r),
        "review.json": {"intents": [], "domains": [{"recognised": True, "known_as": "Approval workflow"}],
                        "capabilities": [], "functionalities": [], "missed_behaviours": []}}
open(out, "w").write(json.dumps(data[out.rsplit("/", 1)[-1]]))
print(json.dumps({"total_cost_usd": 0.01, "num_turns": 1, "result": "done"}))
""" % {"inv": json.dumps(INVENTORY), "cmp": json.dumps(COMPARE)}


class Agents(Work):
    def stand_in(self, name, body):
        path = self.p(name)
        with open(path, "w") as fh:
            fh.write(body)
        os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)
        return path

    def test_the_builder_is_a_restricted_sonnet_session_on_the_brief_alone(self):
        self.model()
        pr.prepare(self.p("pos"), self.p("run", "brief"), [])
        os.environ["STAND_IN_LOG"] = self.p("builder.json")
        old = rb.CLI
        rb.CLI = self.stand_in("claude", STAND_IN_CLAUDE)
        try:
            rc = quiet(rb.main, ["--brief", self.p("run", "brief"), "--build-dir", self.p("run", "build"),
                                 "--prompt", os.path.join(HERE, "prompts", "build.md"), "--out", self.p("run", "b.json")])
        finally:
            rb.CLI = old
        self.assertEqual(rc, 0)
        seen = json.load(open(self.p("builder.json")))
        for flag in ("--restricted", "--strict-mcp-config", "--disable-slash-commands"):
            self.assertIn(flag, seen["args"])
        args = seen["args"]
        self.assertEqual(args[args.index("--model") + 1], "claude-sonnet-5-5")
        self.assertEqual(args[args.index("--effort") + 1], "high")
        self.assertNotIn("Bash", args[args.index("--tools") + 1])
        self.assertEqual(json.load(open(self.p("run", "b.json")))["cost_usd"], 0.02)
        self.assertTrue(all(f.startswith("brief" + os.sep) for f in seen["files"]), seen["files"])
        self.assertFalse(any("argus" in f for f in seen["files"]))

    def test_the_builder_refuses_a_build_folder_inside_a_git_tree(self):
        os.makedirs(self.p("repo", ".git"))
        self.write("brief/intents/x.md", INTENT)
        rc = quiet(rb.main, ["--brief", self.p("brief"), "--build-dir", self.p("repo", "run", "build"),
                             "--prompt", os.path.join(HERE, "prompts", "build.md"), "--out", self.p("b.json")])
        self.assertEqual(rc, 2)

    def test_no_app_built_is_exit_1(self):
        self.write("brief/intents/x.md", INTENT)
        os.environ["STAND_IN_LOG"] = self.p("builder.json")
        os.environ["STAND_IN_BUILD"] = "0"
        old = rb.CLI
        rb.CLI = self.stand_in("claude", STAND_IN_CLAUDE)
        try:
            rc = quiet(rb.main, ["--brief", self.p("brief"), "--build-dir", self.p("run", "build"),
                                 "--prompt", os.path.join(HERE, "prompts", "build.md"), "--out", self.p("b.json")])
        finally:
            rb.CLI = old
            os.environ["STAND_IN_BUILD"] = "1"
        self.assertEqual(rc, 1)

    def test_the_whole_eval_runs_end_to_end_with_stand_ins(self):
        self.model()
        env = dict(os.environ, STAND_IN_LOG=self.p("builder.json"),
                   REBUILD_EVAL_CLAUDE_CLI=self.stand_in("claude", STAND_IN_CLAUDE))
        run = subprocess.run([sys.executable, os.path.join(HERE, "run_eval.py"), "--product-os", self.p("pos"),
                              "--prototype", self.p("proto", "argus.html"), "--out", self.p("run")],
                             capture_output=True, text=True, env=env)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        report = json.load(open(self.p("run", "report.json")))
        self.assertEqual(report["score"]["overall"]["kept_pct"], 37.5)
        self.assertTrue(report["check"]["ok"])
        self.assertEqual(report["review"]["domains"][0]["known_as"], "Approval workflow")
        md = open(self.p("run", "report.md")).read()
        self.assertIn("Kept: 37.5%", md)
        log = json.load(open(self.p("run", "run.json")))
        self.assertEqual(list(log["stages"]), ["prepare", "inventory", "check", "build", "review", "compare", "score"])
        self.assertEqual(log["stages"]["inventory"]["cost_usd"], 0.01)
        cmd = log["stages"]["review"]["command"]
        self.assertEqual(cmd[cmd.index("--effort") + 1], "high")
        self.assertEqual(cmd[cmd.index("--model") + 1], "claude-sonnet-5-5")


if __name__ == "__main__":
    unittest.main()
