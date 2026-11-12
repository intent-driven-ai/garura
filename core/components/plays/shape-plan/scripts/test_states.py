#!/usr/bin/env python3
"""test_states.py — planned_request.py writes the Planned request only after the yes, the
tracker writes and the plan file; check_states.py lets the model change in nothing but the
features' status (C8, C18, D6).

    python3 test_states.py
"""
import os
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from test_support import (check, empty_tracker, finish, flow, make_model, paths, read,  # noqa: E402
                          read_json, run, write)


def request(p, out, plan_write=None, approval=None, record=None):
    return run("planned_request.py", "--work-items", p["items"], "--record", record or p["record"],
               "--plan-write", plan_write or os.path.join(p["working"], "plan-write.json"),
               "--approval", approval or p["approval"], "--plan-id", "340", "--out", out)


def verdict(root, p, req=None):
    out = os.path.join(p["working"], "state-check-2.json")
    args = ["--before", os.path.join(p["working"], "spine-before.yaml"),
            "--spine", os.path.join(root, "_spine.yaml"), "--work-items", p["items"], "--out", out]
    if req:
        args += ["--request", req]
    code, _, _ = run("check_states.py", *args)
    return code, read_json(out) if os.path.isfile(out) else None


def edit_spine(root, fn):
    path = os.path.join(root, "_spine.yaml")
    spine = yaml.safe_load(read(path))
    fn(spine)
    write(path, spine)


def feature(spine, fid):
    return next(f for f in spine["features"] if f["id"] == fid)


def main():
    print("planned_request.py and check_states.py")
    with tempfile.TemporaryDirectory() as tmp:
        root = make_model(tmp, states={"ft-pay": "In progress"})
        p = paths(tmp)
        empty_tracker(p)
        codes = flow(root, p)
        check("the flow writes the request and the state check reads ok",
              codes["request"] == 0 and codes["check_states"] == 0)
        req = read_json(p["request"])
        check("the request holds only the Unplanned features taken in, each a feature set to Planned",
              req["by"] == "shape-plan (#340)"
              and [x["id"] for x in req["parts"]] == ["ft-pick", "ft-remind"]
              and all(x == {"id": x["id"], "kind": "feature", "mode": "update", "status": "Planned"}
                      for x in req["parts"]))
        check("the skill's stamp on a feature it updated is allowed",
              feature(yaml.safe_load(read(os.path.join(root, "_spine.yaml"))), "ft-pick")["metadata"]["updated_by"]
              == "shape-plan (#340)")

        out = os.path.join(tmp, "req.json")
        write(os.path.join(tmp, "no.json"), dict(read_json(p["approval"]), decision="stop"))
        code, _, _ = request(p, out, approval=os.path.join(tmp, "no.json"))
        check("no yes: refused, nothing written", code == 2 and not os.path.exists(out))
        write(os.path.join(tmp, "rec.json"), dict(read_json(p["record"]), ok=False))
        code, _, _ = request(p, out, record=os.path.join(tmp, "rec.json"))
        check("the tracker writes did not all land: refused, nothing written",
              code == 2 and not os.path.exists(out))
        write(os.path.join(tmp, "pw.json"), {"ok": False})
        code, _, _ = request(p, out, plan_write=os.path.join(tmp, "pw.json"))
        check("the plan file was not written: refused, nothing written", code == 2 and not os.path.exists(out))
        write(os.path.join(tmp, "rec.json"), dict(read_json(p["record"]), map={}))
        code, _, _ = request(p, out, record=os.path.join(tmp, "rec.json"))
        check("a feature to set Planned that is not in the plan: refused", code == 2 and not os.path.exists(out))

        good = read(os.path.join(root, "_spine.yaml"))
        edit_spine(root, lambda s: feature(s, "ft-cancel").update(status="Planned"))
        code, res = verdict(root, p, p["request"])
        check("another feature's status moved: not ok",
              code == 1 and any("ft-cancel" in x for x in res["problems"]))
        write(os.path.join(root, "_spine.yaml"), good)
        edit_spine(root, lambda s: feature(s, "ft-pay").update(status="Planned"))
        code, res = verdict(root, p, p["request"])
        check("an In progress feature taken in lost its state: not ok",
              code == 1 and any("ft-pay" in x and "keep its state" in x for x in res["problems"]))
        write(os.path.join(root, "_spine.yaml"), good)
        edit_spine(root, lambda s: feature(s, "ft-pick").update(one_line="Changed."))
        code, res = verdict(root, p, p["request"])
        check("another field of a feature changed: not ok",
              code == 1 and any("more than the features' status" in x for x in res["problems"]))
        write(os.path.join(root, "_spine.yaml"), good)
        edit_spine(root, lambda s: s["capabilities"][0].update(one_line="Changed."))
        code, res = verdict(root, p, p["request"])
        check("another part of the model changed: not ok",
              code == 1 and any("capabilities" in x for x in res["problems"]))
        write(os.path.join(root, "_spine.yaml"), good)
        edit_spine(root, lambda s: feature(s, "ft-remind").update(status="Unplanned"))
        code, res = verdict(root, p, p["request"])
        check("an Unplanned feature taken in that does not read Planned: not ok",
              code == 1 and any("ft-remind" in x and "not Planned" in x for x in res["problems"]))
        write(os.path.join(root, "_spine.yaml"), good)
        write(os.path.join(tmp, "req2.json"), dict(req, parts=req["parts"][:1]))
        code, res = verdict(root, p, os.path.join(tmp, "req2.json"))
        check("a request that does not ask for each change the brief showed: not ok",
              code == 1 and any("the brief showed" in x for x in res["problems"]))
        write(os.path.join(tmp, "req3.json"), dict(req, parts=[dict(req["parts"][0], one_line="x"), req["parts"][1]]))
        code, res = verdict(root, p, os.path.join(tmp, "req3.json"))
        check("a request part that asks for more than the status: not ok",
              code == 1 and any("nothing else" in x for x in res["problems"]))
        code, res = verdict(root, p, p["request"])
        check("the spine as the skill left it: ok", code == 0 and res["planned"] == ["ft-pick", "ft-remind"])
    return finish()


if __name__ == "__main__":
    sys.exit(main())
