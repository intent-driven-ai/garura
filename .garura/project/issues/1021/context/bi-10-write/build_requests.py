"""Build every request for BI-10's write from the six capabilities' drafts.

Run from the repo root after the six drafts pass their check. Writes, beside this file:
- approved/<model path>/ice.md: each thin ICE draft without its Thin line (the page writer never writes it);
- approved-request.json: every page, word for word, for enrich-grounding's approved mode;
- lines-request.json: the one named line on another intent's page that names an old capability;
- link-request.json: the six capabilities, their new features, the nine old features' one-lines, every ICE;
- remove-request.json: bi-734 repointed to bi-10 on the three old capabilities and their nine features, and the
  three merged into Standards;
- intent-draft.json: BI-10's page as it is, with its Touches list;
- one-lines.json: each part's one-line, for the person to read.
"""
import json, os, re, shutil

HERE = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))
ISSUE = ".garura/project/issues/1021/context"
MODEL = ".garura/product/product-os"
S = "software-delivery-planning"
RUNS = [(1, "standards"), (2, "build-your-own-harness"), (3, "structure"), (4, "settings"), (5, "memory"),
        (6, "model-routing")]
INTENTS = {"model-routing": ["bi-10", "bi-7"]}
OLD = ["fn-736", "fn-737", "fn-738", "fn-740", "fn-741", "fn-743", "fn-744", "fn-745", "fn-746"]
OLD_CAPS = ["cap-735", "cap-739", "cap-742"]
THIN = "Thin: proposed from the person's words; deepen with `/discover-capabilities`."
BY = "product-os-keeper (reorganise business intents, #1021)"
SOURCE = (f"{ISSUE}/capabilities.md, section Standards, structure, settings and memory: the product owner's words of "
          "2026-11-11, \"continue as most of this is based on built. please proceed with creae pages and ICE as per the "
          "process and standards and consider them approved. show me only when you are ready for commit and cp\"")
OVERRIDES = {
 "fn-build-from-ice": "Each play and loop is compiled from its ICE source and records its fingerprint, so a check can tell when the compiled part no longer matches its ICE.",
 "fn-standard-per-kind": "Each kind of part, play, loop, sub-agent, skill, script, shared file and tool, has a written standard that says what it is and what it does.",
 "fn-736": "Every part is named by one rule: plain words, the verb first, one meaning per verb, never a coding tool's own command, with five roles owning the verbs.",
 "fn-743": "The harness plays and the loop carry the standard's names, and move to each new name the standard sets.",
 "fn-744": "The change, plan, knowledge and record plays carry the standard's names, and move to each new name the standard sets.",
 "fn-745": "The lifecycle and lens plays carry the standard's names, and move to each new name the standard sets.",
 "fn-746": "Every skill carries a verb from the skill verb list, and moves to each new name the standard sets.",
 "fn-740": "The component linter, the play linter, the loop linter and the old-name check fail every part that breaks a written rule.",
 "fn-rules-for-every-part": "Each rule every part follows, such as asking a person and staying on scope, is written once and binds every part without the part naming it.",
 "fn-build-play": "/create-play builds a play from its ICE: it works out its scripts, skills and sub-agents, adds the change plays and the shared close, records the fingerprint and runs the play linter until clean.",
 "fn-change-play": "/edit-play changes a play through its ICE first, compiles it again with a new fingerprint and runs the play linter, so the play always matches its intent.",
 "fn-build-loop": "/create-loop builds a loop from its ICE as its own values and a pointer to the shared loop run, with its Done means, settings and fingerprint, and runs the loop linter until clean.",
 "fn-change-loop": "/edit-loop changes a loop through its ICE first, on the person's typed approval, carries the change through and runs the loop linter, which fails a loop whose ICE changed since it was built.",
 "fn-add-gate": "The builders place a play's checkpoint where its workflow puts it, with its class, and pinning or unpinning it is a change to the play's intent through /edit-play.",
 "fn-harness-in-own-repo": "A team installs Garura's builders in its own repository and builds its own plays and loops there, reading a written architecture of what each part may do.",
 "fn-source-layout": "Garura's own repository keeps each kind of part in one known folder, each tool in the tools folder and the settings in one file, so a developer knows where a part goes.",
 "fn-one-settings-file": "Every setting Garura's plays, scripts and loops read is in one settings file, written once in Garura's source and laid by the install as each project's own copy.",
 "fn-setting-names-reader": "A list names, for every setting, what it means and the play or tool that reads it, and a check fails a setting no one reads.",
 "fn-settings-folder": "Every settings file other than the one settings file goes into one settings folder beside it, starting with the learned policy.",
 "fn-checkpoint-settings": "Each checkpoint is turned on or off by a setting for its play, its kind of risk or the default, a conditional one passes once the learned policy allows it, and no setting reaches a pinned one.",
 "fn-evidence-setting": "One setting, with a switch for each play, decides whether a play writes its evidence file at its end, and the report a person reads is always shown.",
 "fn-find-memory": "An agent finds what it needs with one memory tool, which looks in short-term, then Garura, then Phoenix memory, stops at the first tier that answers, and names where each answer came from.",
 "fn-person-decides-update": "When no tier answers, an agent drafts the answer as a memory update, and only a person approves or rejects it, one at a time, with their exact reply on record.",
 "fn-keep-decision-trace": "Each decision an agent makes keeps its trace, each step resting on memory lines with their fingerprint, and a check names the step whose source changed or is gone.",
 "fn-read-through-tool": "Every agent reads memory through the tool by one shared protocol, and the component linter fails a part that skips it or names a memory folder.",
 "fn-phoenix-in-step": "A change to a memory page in Garura's source reaches Phoenix memory in the same release, a check names every page where the two differ, and each release has a version and its notes.",
 "fn-bring-phoenix": "The memory tool downloads Phoenix memory the first time a command needs it and reads it at its approved version, and one Phoenix install per machine keeps it current.",
 "fn-check-memory": "A page that is out of date, or whose source changed, is named before an agent uses it, and each change to a project's memory shows in the review of its change.",
 "fn-decide-inside-memory": "Everything agents decide from sits inside memory: the machine-wide copy is retired, Claude Code's own memory is held to a guardrail, and the engine's rules stay in Phoenix memory.",
 "fn-tier-by-rule": "Each part's maker names in its source the tier and the effort its job needs, by one written rule, and a project may change a part's tier in its own settings.",
 "fn-step-on-set-model": "A step whose model a setting names, such as the check of a finished loop or the judge of a model page, runs on that model and not on the session's own."
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
    drafts = f"{ISSUE}/bi-10-capability-{n}/drafts/product-os"
    cdir = f"{drafts}/{S}/{slug}"
    cap = f"cap-{slug}"
    intents = INTENTS.get(slug, ["bi-10"])
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
            parts.append({"id": fid, "kind": "feature", "mode": "update", "one_line": lines_out[fid]})
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
                                       "intents": {"bi-734": "bi-10"}} for i in OLD_CAPS + OLD],
                          "remove": [{"kind": "capability", "id": c, "into": "cap-standards"} for c in OLD_CAPS]})
old725 = ("- Given Garura's own model (#717, #722, #734) after the rename, when the linter and the ready check run, then "
          "cap-742 still needs cap-739, and fn-727 still needs fn-724, with no value lost.")
assert old725 in open(f"{MODEL}/features/fn-725/feature.md", encoding="utf-8").read().split("\n")
w("lines-request.json", {"by": BY, "source": SOURCE + "; the three old capabilities merge into Standards, so this line names "
                         "the features whose need is kept",
                         "pages": [{"page": "features/fn-725/feature.md", "changes": [
                             {"old": old725, "new": old725.replace("cap-742 still needs cap-739", "fn-743 still needs fn-741")}]}]})

# BI-10's page as it is, with its Touches list
lines = open(f"{MODEL}/intents/bi-10.md", encoding="utf-8").read().split("\n")
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
w("intent-draft.json", {"id": "bi-10", "issue": 10, "title": lines[0][2:], "outcome": one("Outcome"), "why": one("Why"),
                        "asked_by": one("Asked by"), "proof": proof, "must_not": one("Must not"), "touches": tl})
w("one-lines.json", lines_out)
print(json.dumps({"pages": len(pages), "parts": len([p for p in parts if p["kind"] != "ice"]),
                  "ice": len([p for p in parts if p["kind"] == "ice"]),
                  "thin_ice": len([p for p in parts if p["kind"] == "ice" and p["thin"]]), "touches": len(tl)}))
