#!/usr/bin/env python3
"""test_trace_check.py — the trace check of the decisions the slice rests on (/shape-slice, D5).

The #844 shape: 14 records, 7 problems on 5 of them; the 9 records the slice rests on are live.

    python3 core/components/plays/shape-slice/scripts/test_trace_check.py
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PASSED = 0
FAILED = 0


def check(name, cond):
    global PASSED, FAILED
    if cond:
        PASSED += 1
        print(f"  [PASS] {name}")
    else:
        FAILED += 1
        print(f"  [FAIL] {name}")


def run(*args):
    p = subprocess.run([sys.executable, os.path.join(HERE, "trace_check.py"), *args],
                       capture_output=True, text=True)
    return p.returncode


def write(path, data):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh)
    return path


def cid(n):
    return f"cite-20261024-{n:03d}"


def main():
    with tempfile.TemporaryDirectory() as tmp:
        records = [{"citation_id": cid(n)} for n in range(1, 15)]
        stale = [1, 1, 2, 3, 3, 4, 8]  # 7 problems on 5 records
        answer = {"ok": True, "command": "citations", "records": records,
                  "problems": [{"citation_id": cid(n), "problem": "source_changed"} for n in stale]}
        check_p = write(os.path.join(tmp, "citations-check.json"), answer)
        live = [cid(n) for n in range(1, 15) if n not in {1, 2, 3, 4, 8}]
        live_p = write(os.path.join(tmp, "citations-live.json"), {"live": live})
        out = os.path.join(tmp, "trace-check.json")
        code = run("--issue", "844", "--live", live_p, "--check", check_p, "--out", out)
        res = json.load(open(out, encoding="utf-8"))
        check("trace: no problem when every live record still holds (exit 0)",
              code == 0 and res["ok"] and res["problems"] == [] and len(res["live"]) == 9)
        check("trace: the other five records are listed apart as not live",
              sorted(res["not_live"]) == sorted(cid(n) for n in (1, 2, 3, 4, 8)))
        live_p = write(os.path.join(tmp, "live2.json"), {"live": live + [cid(8)]})
        code = run("--issue", "844", "--live", live_p, "--check", check_p, "--out", out)
        res = json.load(open(out, encoding="utf-8"))
        check("trace: a live record whose source changed is a problem (exit 1)",
              code == 1 and [p["citation_id"] for p in res["problems"]] == [cid(8)])
        live_p = write(os.path.join(tmp, "live3.json"), {"live": live + ["cite-20261024-099"]})
        code = run("--issue", "844", "--live", live_p, "--check", check_p, "--out", out)
        res = json.load(open(out, encoding="utf-8"))
        check("trace: a live id with no record is a problem (not_recorded)",
              code == 1 and res["problems"] == [{"citation_id": "cite-20261024-099",
                                                 "problem": "not_recorded"}])
        bad = write(os.path.join(tmp, "bad.json"), {"live": "x"})
        check("trace: a live file of the wrong shape stops it (exit 2)",
              run("--issue", "844", "--live", bad, "--check", check_p, "--out", out) == 2)
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
