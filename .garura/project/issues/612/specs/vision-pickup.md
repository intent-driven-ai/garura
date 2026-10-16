# Can `/vision` start from what `/intent` saves? — #612, item 7

Checked 2026-10-16 against main at 9e4724db. This is the write-up item 7 asks for. The change itself is a follow-up, not part of #612.

## The answer

No, not yet. `/intent` hands over the right things, and the product model already allows them: a capability with no domain is a warning, not an error, and the spine has an `intents` field. But `/vision` does not read any of it. It starts from a goal typed as text, makes its own capabilities from the KB, and its save step will not touch a capability that already exists. So a `/vision` run after `/intent` today would ignore the intents, could add a second capability for the same thing, and could not attach a domain to the ones `/intent` wrote.

## What `/intent` hands over

- One page per business intent: `product-os/intents/<id>.md` — title, outcome, why, asked by, proof, must not, stage, sources, and the capabilities built from it.
- Per ICE, one proposed capability on the spine: `domain: ""`, `intents: [<intent id>]`, `status: proposed`, `detail: directional`, doc at `product-os/capabilities/<id>/capability.md` (a `## Directional intent` section plus the ICE goals).
- A save record listing each intent with its page and its capability docs, the stage (`confirmed` by hand, `proposed` inside a drive), and the sources.

Source: `core/components/plays/intent/scripts/persist_intent.py` (`capability_entry`, `capability_doc`, `manifest_for`).

## What `/vision` does today

- Takes "a business goal" from the play argument or by asking (pre-flight table; Steps 0–2 contracts pass `goal` as text).
- Step 1: routes the goal to one domain through the KB, then lists candidate capabilities from that domain's KB shelf. It never reads the spine.
- Step 2: writes a domain doc and a directional doc per capability, only where none exists, and lists new spine entries in its seed manifest. The entries carry no `intents`.
- Step 4: `persist_seed.py` adds only entries whose id is absent. An existing entry is "skipped" and left byte-untouched.
- Step 5: the guard lets docs matching `product-os/*/domain.md` and `product-os/*/*/capability.md` be added, never changed or removed.

Sources: `core/components/plays/vision/reference/ice.md` (intent, C5, C6), `core/components/plays/vision/SKILL.md` (pre-flight, Steps 1–5), `core/components/plays/vision/scripts/persist_seed.py` (`merge_spine`).

## The gaps

1. **The input is text, not intents.** Nothing lets `/vision` start from business intents. It needs to take a set of intents — by id, or `/intent`'s save record inside a drive — and draw the goal from the pages (title, outcome, why). A typed goal can stay for a hand run.
2. **It does not see the capabilities `/intent` wrote.** Step 1 should first read the spine entries built from those intents that have no domain, and treat them as candidates that already exist. KB candidates are then matched against them, so the same thing is not added twice (two ICE for one part is drift, ontology v3).
3. **It cannot attach a domain.** Setting `domain` on an existing entry is a change, and `persist_seed.py` never changes an existing entry. It needs one narrow keyed update: set `domain` on a capability only when it is empty, and nothing else. The guard already lets the spine change, so the rule must live in the script, as the add-only rule does today.
4. **The capabilities it adds itself serve no intent.** Its spine entries carry no `intents`. When it starts from intents, every capability it adds should name the intent it serves (D9); without one, the ICE is kept but nothing is built from it.
5. **Grounding skips the existing capabilities.** C5 says every capability is grounded in a KB shelf or has a KB-node proposal, but the seed manifest only covers capabilities `/vision` writes. The ones `/intent` wrote should get the same check — a shelf match or a proposal, recorded in the manifest. No doc edit is needed for this.
6. **Where the doc lives.** `/intent` puts the doc at `capabilities/<id>/capability.md`; `/vision` puts its own at `<domain>/<capability>/capability.md`. Moving it would be a delete plus an add, and the guard treats the old path as add-only, so a move fails. The spine's `doc` pointer works wherever the doc is.
7. **It must not wait for a confirmed intent.** Inside the Kickoff drive the intents stay proposed until the drive's end review (D10). So `/vision` must accept proposed intents and must not stop on the workable check (`check_ice_workable.py`). Attaching a domain is a write, and a write is never blocked (ontology v3).

## Two choices for whoever builds the change

- **Move the doc or leave it (gap 6).** Leave it where `/intent` put it, with the spine pointing at it. That is less to build and nothing breaks. Moving it needs the guard to allow a remove on that one path. Recommended: leave it.
- **Who adds to the ICE ("enrich").** `/vision` writes at CXO level and never details a capability (C3); `/understand` already has `enrich-capability-ice` for that. Recommended: `/vision` attaches the domain and the grounding only and leaves the doc to `/understand`. Doing it in `/vision` would mean changing a doc it did not write, which its guard forbids today.

## Not in this change

- `/vision` running inside a drive without stopping: #614.
- `/understand` and `/shape` linking the ICE they write to an intent: listed in #612's follow-ups.
- Confirming or dropping intents at the Kickoff drive's end review: #613 (ADR 031, D10).

## What this change is

An intent change to `/vision` (its input, C5, C6, Steps 1–5, the persist script), so it goes through `core/components/plays/vision/reference/ice.md` and `/play-editor`. Filed as #637, a Story under #594 (#606 plan, item 4).
