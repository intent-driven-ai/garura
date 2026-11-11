"""Build every request for BI-11's write from the two capabilities' drafts.

Run from the repo root after the six drafts pass their check. Writes, beside this file:
- approved/<model path>/ice.md: each thin ICE draft without its Thin line (the page writer never writes it);
- approved-request.json: every page, word for word, for enrich-grounding's approved mode;
- lines-request.json: (none needed: no page outside the drafts names the old capability);
- link-request.json: the two capabilities, their new features, the four old features' one-lines (fn-597 filed under Define), every ICE;
- remove-request.json: bi-722 repointed to bi-11 on the old capability and its four features, and it merged
  into Manage the model;
- intent-draft.json: BI-11's page as it is, with its Touches list;
- one-lines.json: each part's one-line, for the person to read.
"""
import json, os, re, shutil

HERE = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))
ISSUE = ".garura/project/issues/1021/context"
MODEL = ".garura/product/product-os"
S = "software-delivery-planning"
RUNS = [(1, "define-product"), (2, "manage-model")]
INTENTS = {}
OLD = ["fn-597", "fn-724", "fn-725", "fn-726"]
REFILE = {"fn-597": "cap-define-product"}  # filed before the merge, which files the others under Manage the model
OLD_CAPS = ["cap-723"]
THIN = "Thin: proposed from the person's words; deepen with `/discover-capabilities`."
BY = "product-os-keeper (reorganise business intents, #1021)"
SOURCE = (f"{ISSUE}/capabilities.md, section Product model, and the product owner's words of "
          "2026-11-11 on BI-11's review, \"i want to review A as most of this is built at least as skills\"; recorded in "
          ".garura/project/issues/1021/context/bi-11-write/approval.md")
OVERRIDES = {
 "fn-change-ontology": "/edit-ontology changes only the kinds one need touches, with the product owner's typed yes at three points, ends only when the map reads valid, and lands through the change plays.",
 "fn-readers-in-step": "Each part that describes or checks the model's shape follows the map's current version.",
 "fn-change-part": "A part changes only from words a person approved: named lines, a whole page, an intent page, its one-line, its intents or its parent, by one edit standard.",
 "fn-take-part-out": "A part is taken out only on a person's named approval: an old intent repointed, an intent page removed, a capability merged or a slice removed.",
 "fn-725": "Each link follows the ontology's rules, is kept on both sides, and points at a part that exists.",
 "fn-724": "The ready check says for each part whether work can start, ready, partly ready or not ready, with its gaps, and the same model always gives the same answer.",
 "fn-check-model": "The structure check reads the model's pages and index for their shape and links on every change, as findings, never a stop."
}  # one-line overrides by part id: what each part does, in one sentence, with no status
ITEM = re.compile(r"^- (.+?) \((fn-[a-z0-9-]+)\): (.+)$")
STATUS_TAIL = re.compile(r"\s*(?:[;,]\s*|\.\s+)(?:it is )?(?:not built|built in part|planned|built)\b[^.;]*\.?\s*$", re.I)


def ice_id(pid):
    return "ice-" + (pid[3:] if pid.startswith("fn-") else pid[4:])


def one_line(text):
    t = text.strip()
    for _ in range(3):
        t2 = STATUS_TAIL.sub("", t)
        if t2 == t:
            break
        t = t2
    t = t.rstrip(" .;,")
    return t[0].upper() + t[1:] + "."


parts, pages, touches, lines_out = [], [], [], {}
old_seen = []
for n, slug in RUNS:
    drafts = f"{ISSUE}/bi-11-capability-{n}/drafts/product-os"
    cdir = f"{drafts}/{S}/{slug}"
    cap = f"cap-{slug}"
    intents = INTENTS.get(slug, ["bi-11"])
    cap_text = open(f"{cdir}/capability.md", encoding="utf-8").read()
    di = cap_text.split("## Directional intent", 1)[1].split("\n### ", 1)[0]
    first = [l for l in di.split("\n") if l.strip()][0]
    title = cap_text.split("\n", 1)[0][len("# Capability: "):]
    assert first.startswith(title + ": "), (slug, first[:80])
    lines_out[cap] = OVERRIDES.get(cap, first.strip())
    feats = [(m.group(2), m.group(3)) for m in (ITEM.match(l) for l in di.split("\n")) if m]
    assert feats, slug
    parts.append({"id": cap, "kind": "capability", "mode": "new", "slug": slug, "domain": "dom-software-delivery-planning",
                  "intents": intents, "one_line": lines_out[cap], "doc": f"{S}/{slug}/capability.md", "identified_by": ""})
    touches.append(("capability", f"{S}/{slug}/capability.md", "adds"))
    rels = [(cap, f"{S}/{slug}", f"{cdir}")]
    for fid, desc in feats:
        if fid in OLD:
            rels.append((fid, f"features/{fid}", f"{drafts}/features/{fid}"))
            lines_out[fid] = OVERRIDES.get(fid, one_line(desc))
            upd = {"id": fid, "kind": "feature", "mode": "update", "one_line": lines_out[fid]}
            if fid in REFILE:
                upd["capability"] = REFILE[fid]
            parts.append(upd)
            touches.append(("feature", f"features/{fid}/feature.md", "changes"))
            old_seen.append(fid)
        else:
            rels.append((fid, f"{S}/{slug}/{fid}", f"{cdir}/{fid}"))
            lines_out[fid] = OVERRIDES.get(fid, one_line(desc))
            parts.append({"id": fid, "kind": "feature", "mode": "new", "slug": fid, "capability": cap, "intents": intents,
                          "one_line": lines_out[fid], "doc": f"{S}/{slug}/{fid}/feature.md", "identified_by": ""})
            touches.append(("feature", f"{S}/{slug}/{fid}/feature.md", "adds"))
    for pid, mdir, ddir in rels:
        page = "capability.md" if pid.startswith("cap-") else "feature.md"
        assert os.path.isfile(f"{ddir}/{page}") and os.path.isfile(f"{ddir}/ice.md"), ddir
        pages.append({"page": f"{mdir}/{page}", "from": f"{ddir}/{page}"})
        data = open(f"{ddir}/ice.md", "rb").read()
        thin = data.split(b"\n", 1)[0].decode() == THIN
        src = f"{ddir}/ice.md"
        if thin:
            first_line, blank, rest = data.split(b"\n", 2)
            assert blank == b"" and THIN.encode() not in rest
            src = f"{HERE}/approved/{mdir}/ice.md"
            os.makedirs(os.path.dirname(src), exist_ok=True)
            open(src, "wb").write(rest)
        pages.append({"page": f"{mdir}/ice.md", "from": src})
        parts.append({"id": ice_id(pid), "kind": "ice", "mode": "new", "for": pid, "doc": f"{mdir}/ice.md", "thin": thin})
assert sorted(old_seen) == sorted(OLD), old_seen
for x in lines_out.values():
    assert not x.lower().startswith("not built"), x

# the parts first, then their ICE, so every ICE names a part already in the request
parts = [p for p in parts if p["kind"] != "ice"] + [p for p in parts if p["kind"] == "ice"]
w = lambda name, obj: json.dump(obj, open(os.path.join(HERE, name), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
w("approved-request.json", {"by": BY, "approved_by": "the product owner", "source": SOURCE, "pages": pages})
w("link-request.json", {"by": BY + "; pages and one-lines taken as approved by the product owner", "parts": parts})
w("remove-request.json", {"by": BY, "approved_by": "the product owner", "source": SOURCE,
                          "repoint": [{"id": i, "kind": "capability" if i.startswith("cap-") else "feature",
                                       "intents": {"bi-722": "bi-11"}} for i in OLD_CAPS + OLD],
                          "remove": [{"kind": "capability", "id": c, "into": "cap-manage-model"} for c in OLD_CAPS]})
# BI-11's page as it is, with its Touches list
lines = open(f"{MODEL}/intents/bi-11.md", encoding="utf-8").read().split("\n")
one = lambda label: [l for l in lines if l.startswith(f"**{label}:** ")][0][len(f"**{label}:** "):]
i = lines.index("**Proof it is met:**")
proof = []
for l in lines[i + 1:]:
    if not l.startswith("- "):
        break
    proof.append(l[2:])
assert not any(l.startswith(("**Rules:**", "**Serves:**", "**Identified by:**", "**Touches:**")) for l in lines)
tl = []
for kind, doc, mark in touches:
    src = next(p["from"] for p in pages if p["page"] == doc)
    head = open(src, encoding="utf-8").readline().rstrip("\n")
    prefix = "# Capability: " if kind == "capability" else "# Feature: "
    assert head.startswith(prefix), doc
    tl.append({"title": head[len(prefix):], "link": f"../{doc}", "kind": kind, "mark": mark})
w("intent-draft.json", {"id": "bi-11", "issue": 11, "title": lines[0][2:], "outcome": one("Outcome"), "why": one("Why"),
                        "asked_by": one("Asked by"), "proof": proof, "must_not": one("Must not"), "touches": tl})
w("one-lines.json", lines_out)
print(json.dumps({"pages": len(pages), "parts": len([p for p in parts if p["kind"] != "ice"]),
                  "ice": len([p for p in parts if p["kind"] == "ice"]),
                  "thin_ice": len([p for p in parts if p["kind"] == "ice" and p["thin"]]), "touches": len(tl)}))
