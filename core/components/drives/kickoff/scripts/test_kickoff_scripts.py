#!/usr/bin/env python3
"""Tests for Kickoff's own scripts: the prototype check and the person's decisions."""
import contextlib
import http.server
import io
import json
import os
import shutil
import sys
import tempfile
import threading
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_prototype  # noqa: E402
import record_confirmation  # noqa: E402


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


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802 — the server's own name
        self.send_response(200 if self.path == "/" else 404)
        self.end_headers()

    def log_message(self, *args):
        pass


class Prototype(Work):
    def run_it(self, *args):
        return quiet(check_prototype.main, [*args, "--timeout", "3", "--out", self.p("proto.json")])

    def test_a_link_that_answers_runs(self):
        server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.shutdown)
        url = f"http://127.0.0.1:{server.server_address[1]}"
        self.assertEqual(self.run_it("--prototype", url + "/"), 0)
        self.assertEqual(self.run_it("--prototype", url + "/missing"), 2)

    def test_a_link_nothing_answers_halts(self):
        self.assertEqual(self.run_it("--prototype", "http://127.0.0.1:9/"), 2)

    def test_no_prototype_halts(self):
        self.assertEqual(self.run_it("--prototype", ""), 2)
        self.assertEqual(self.run_it("--prototype", self.p("nowhere")), 2)

    def test_a_folder_needs_files_and_the_persons_word_on_how_it_starts(self):
        os.makedirs(self.p("app"))
        self.assertEqual(self.run_it("--prototype", self.p("app"), "--start", "npm start"), 2)  # empty
        self.write("app/index.html", "<h1>shop</h1>")
        self.assertEqual(self.run_it("--prototype", self.p("app")), 2)  # no word on how it starts
        self.assertEqual(self.run_it("--prototype", self.p("app"), "--start", "open index.html"), 0)


class Confirmation(Work):
    def setUp(self):
        super().setUp()
        self.page = self.write("intents/fewer-lost-carts.md",
                               "# Fewer lost carts\n\n**Stage:** proposed — saved inside a drive\n")
        self.write("intents/faster-checkout.md", "# Faster checkout\n\n**Stage:** proposed\n")
        self.manifest = self.write("intent-manifest.json", json.dumps({"intents": [
            {"id": "fewer-lost-carts", "path": self.p("intents/fewer-lost-carts.md")},
            {"id": "faster-checkout", "path": self.p("intents/faster-checkout.md")}]}))

    def run_it(self, replies):
        path = self.write("replies.json", json.dumps(replies))
        return quiet(record_confirmation.main, ["--manifest", self.manifest, "--replies", path,
                                                "--by", "a person", "--at", "2026-10-20",
                                                "--out", self.p("confirmation.yaml")])

    def test_every_intent_decided_in_the_persons_words(self):
        code = self.run_it({"fewer-lost-carts": "confirm — this is the one",
                            "faster-checkout": "drop, not now"})
        self.assertEqual(code, 0)
        with open(self.p("confirmation.yaml")) as fh:
            text = fh.read()
        self.assertIn("by: person", text)
        self.assertIn("decision: confirmed", text)
        self.assertIn("decision: dropped", text)
        self.assertIn('"drop, not now"', text)
        with open(self.page) as fh:
            self.assertIn("**Stage:** proposed", fh.read())  # the model is untouched

    def test_an_intent_without_a_reply_is_refused(self):
        self.assertEqual(self.run_it({"fewer-lost-carts": "confirm"}), 2)
        self.assertFalse(os.path.exists(self.p("confirmation.yaml")))

    def test_a_reply_that_is_not_confirm_or_drop_is_refused(self):
        self.assertEqual(self.run_it({"fewer-lost-carts": "maybe", "faster-checkout": "confirm"}), 2)

    def test_a_reply_for_an_intent_not_saved_is_refused(self):
        self.assertEqual(self.run_it({"fewer-lost-carts": "confirm", "faster-checkout": "confirm",
                                      "other": "drop"}), 2)

    def test_an_intent_the_drive_changed_is_refused(self):
        self.write("intents/faster-checkout.md", "# Faster checkout\n\n**Stage:** confirmed\n")
        self.assertEqual(self.run_it({"fewer-lost-carts": "confirm", "faster-checkout": "confirm"}), 2)


if __name__ == "__main__":
    unittest.main()
