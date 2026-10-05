#!/usr/bin/env python3
"""
derive_candidates.py — the /next decision tree, as code (C6/C8/C9/C13, F2/F6).

A PURE FUNCTION over the scan_model.py snapshot: same snapshot in, same
candidate set out — no clock, no randomness, no file reads beyond the two
arguments. Emits every action that is currently RUNNABLE or BLOCKED (with the
blocker named), plus the model-inconsistency report (the repair lane, C5).

The tree (framed with the user, #434 follow-on; re-read on the spine, #533):

  no model ............................................. /vision
  model files but no spine ............................. inconsistency only
      (model-has-no-spine — nothing is derived from legacy per-node files)
  directional capability or profile directional ........ /understand
  profile set/locked, domain has capabilities, no slices  /shape {domain id}
  slices proposed / unordered .......................... /roadmap
  per planned slice (roadmap order + depends_on cited), two realize tracks
  (standards/rules/pipeline-next.md — track order is a recommendation, not a gate):
      functional track ux -> agentic -> marketing ....... head missing lens play
      non-functional track arch -> quality -> run ....... head missing lens play
      both tracks done, measure.md missing .............. /measure (stamps realized)
  REPAIR: planned slice with all seven lens docs ....... /measure (stamp unfinished)
  REPAIR: slice realized but a lens missing ............ the missing lens play
      (blocks grill/implement on that slice — carries the blocker flag)
  REPAIR: slice carries surface debt ................... re-validate the surface
      (a delivered user-facing epic; withholds further execute epics of the
       slice until the required surface is re-checked — surface-contract.md)
  REPAIR: slice record not in the spine index .......... inconsistency only
  realized slice, no spine epics, no deferrals ......... /grill {slice}
  epics: fix_required .................................. /implement (fix round)
         ready + deps delivered ........................ /implement {epic}
         ready + deps NOT delivered .................... blocked (dep named)
         in_delivery ................................... /validate {epic}
         validated ..................................... /launch {epic}
  realized slice, grilled, all epics delivered/gone .... /learn (learning)
  everything delivered ................................. strategy refresh
      (/shape from deferred when a deferred bucket exists; /roadmap re-plan)

The order (C14, user direction 2026-09-11, #533) — slices are core, so a slice is
finished before the others advance:

  1. repair, anywhere (lowest roadmap order first)
  2. the FOCUS SLICE — the lowest roadmap-order slice with work left (a lens,
     /measure, /grill, or live epics); within it: functional track head →
     non-functional track head → /measure → /grill → epics by order
  3. strategy (understand / shape / roadmap)
  4. every other slice's steps, by roadmap order — shown, flagged parallel lanes
  5. learning, then 6. strategy refresh

Every candidate carries `rank` (1..n), `slice`, `focus`, `parallel_lane` and a
plain-language `why`. The output also holds `entries` (the first 11 — the cap,
C4), `cut_for_cap` (the ids past the cap) and `focus_slice`.

Layer rule: no git/gh/network. Same snapshot in, same ordered list out.

    python3 derive_candidates.py --state <model-state.json> --out <candidates.json>

Exit 0 on success (even with zero candidates), 2 on usage error.
"""

import argparse
import hashlib
import json
import sys

PIPELINE = "standards/rules/pipeline-next.md"
FUNCTIONAL = ["ux", "agentic", "marketing"]
NON_FUNCTIONAL = ["architecture", "quality", "run"]
ALL_LENSES = FUNCTIONAL + NON_FUNCTIONAL + ["measure"]
LENS_PLAY = {"quality": "quality", "ux": "ux", "agentic": "agentic",
             "marketing": "marketing", "architecture": "arch",
             "measure": "measure", "run": "run"}
TRACKS = [("functional", FUNCTIONAL, "lens"),
          ("non-functional", NON_FUNCTIONAL, "foundation")]
CAP = 11  # C4: next-best-action + ranked list, at most 11 entries
SLICE_LANES = {"repair", "lens", "foundation", "grill", "execute", "learning"}
WORK_LANES = {"repair", "lens", "foundation", "grill", "execute"}
TRACK_NAME = {lt: "feature track (ux → agentic → marketing)" for lt in FUNCTIONAL}
TRACK_NAME.update({lt: "technical track (architecture → quality → run)"
                   for lt in NON_FUNCTIONAL})
EPIC_STATUSES = {"ready", "in_delivery", "validated", "fix_required", "delivered"}
# surface-contract.md taxonomy: the user-facing types carry a run surface a human
# can open/call/run; the others do not. A `delivered` epic with a user-facing
# surface is the deterministic signal of surface debt (the model records no
# "delivered surface" field, so a delivered user-facing epic is the weaker-but-real
# signal that surface repair must precede further execute work in that slice).
USER_FACING_SURFACES = {"web_dashboard", "server_api", "cli"}


def cand(cid, play, command, target, lane, status="runnable", blocker=None,
         gates=None, order_hint=0, unblocks=None, repair=False, parallel=False):
    return {"id": cid, "play": play, "command": command, "target": target,
            "lane": lane, "status": status, "blocker": blocker,
            "gates": sorted(g for g in (gates or []) if g),
            "order_hint": order_hint,
            "unblocks": sorted(u for u in (unblocks or []) if u),
            "repair": repair,
            "parallel_lane": parallel}


def domain_folder(d):
    return d.get("slug") or d["id"]


def slice_ref(domain, sl):
    return f"{domain}/{sl['id']}"


def chain_text(chain):
    return "→".join("arch" if lt == "architecture" else lt for lt in chain)


def derive(state):
    candidates, inconsistencies = [], []

    # ---- cold start -----------------------------------------------------
    if not state.get("model_exists"):
        candidates.append(cand(
            "strategy/vision", "vision", "/vision", "(new product)", "strategy",
            gates=["no product model exists under product-os/"],
            unblocks=["the whole strategy pipeline (understand, shape, roadmap)"]))
        return candidates, inconsistencies

    # ---- no spine: report, derive nothing (C13) --------------------------
    if state.get("spine_exists") is False:
        inconsistencies.append({
            "kind": "model-has-no-spine", "target": state.get("root") or "product-os/",
            "detail": "product-os/ holds files but no _spine.yaml — the spine is the index "
                      "of record (ADR 026); nothing is derived from legacy per-node files"})
        return candidates, inconsistencies

    domains = state.get("domains") or []
    profile = state.get("profile") or {}
    profile_state = profile.get("state") or "directional"

    for sid in state.get("orphan_slices") or []:
        inconsistencies.append({
            "kind": "slice-domain-unresolved", "target": str(sid),
            "detail": f"spine slice '{sid}' names a domain_ref that is not in the spine "
                      "domains index — it cannot be placed or realized"})
    for d in domains:
        for sid in d.get("unindexed_slices") or []:
            inconsistencies.append({
                "kind": "slice-not-indexed", "target": f"{domain_folder(d)}/{sid}",
                "detail": f"slice record '{sid}' exists under {domain_folder(d)}/slices/ "
                          "but the spine slices index has no entry — its record status is "
                          "never read; index it through /shape or remove the record"})

    any_slices = any(d.get("slices") for d in domains)
    directional_caps = [c for d in domains for c in d.get("capabilities", [])
                        if c.get("detail") != "detailed"]

    # ---- strategy: understand / shape / roadmap -------------------------
    if profile_state == "directional" or (directional_caps and not any_slices):
        why = [f"profile state is '{profile_state}' (must be set before /shape)"]
        if directional_caps:
            why.append(f"{len(directional_caps)} capability(ies) still directional on the "
                       "spine (not yet detailed by /understand)")
        candidates.append(cand(
            "strategy/understand", "understand", "/understand", "(product)",
            "strategy", gates=why,
            unblocks=["/shape (needs a set profile and detailed capabilities)"]))

    if profile_state in ("set", "locked"):
        for d in domains:
            if d.get("capabilities") and not d.get("slices"):
                candidates.append(cand(
                    f"strategy/shape/{d['id']}", "shape", f"/shape {d['id']}",
                    d["id"], "strategy",
                    gates=[f"profile is '{profile_state}'",
                           f"domain '{d['id']}' has capabilities on the spine but no slices"],
                    unblocks=["/roadmap", "the realize tracks for this domain"]))

    unplanned = [(domain_folder(d), s) for d in domains for s in d.get("slices", [])
                 if s["status"] == "proposed" or (s["status"] not in ("deferred",)
                                                  and s.get("order") is None)]
    if unplanned:
        candidates.append(cand(
            "strategy/roadmap", "roadmap", "/roadmap", "(all slices)", "strategy",
            gates=[f"{len(unplanned)} slice(s) unplanned on the spine (status proposed / "
                   "no order): " + ", ".join(slice_ref(dm, s) for dm, s in unplanned)],
            unblocks=["the realize tracks (lens work runs in roadmap order)"]))

    # ---- per-slice: lenses, repair, grill, epics -------------------------
    all_slices = [(domain_folder(d), s) for d in domains for s in d.get("slices", [])]
    by_id = {s["id"]: s for _, s in all_slices}
    in_flight_orders = sorted(s.get("order") or 0 for _, s in all_slices
                              if s["status"] in ("planned", "realized"))
    first_order = in_flight_orders[0] if in_flight_orders else 0

    learning_targets = []

    for domain, sl in all_slices:
        ref = slice_ref(domain, sl)
        order = sl.get("order") or 0
        if sl["status"] == "deferred":
            continue
        if sl["status"] not in ("proposed", "planned", "realized") and sl["status"]:
            inconsistencies.append({
                "kind": "unknown-slice-status", "target": ref,
                "detail": f"slice status '{sl['status']}' is outside the vocabulary "
                          "(proposed|planned|realized|deferred)"})

        dep_state = []
        for dep in sl.get("depends_on") or []:
            dep_sl = by_id.get(dep)
            if dep_sl is None:
                inconsistencies.append({
                    "kind": "broken-slice-dependency", "target": ref,
                    "detail": f"depends_on '{dep}' does not resolve to any slice"})
            else:
                dep_state.append(f"depends_on {dep} is '{dep_sl['status']}'")

        lenses = sl.get("lenses") or {}
        missing = [lt for lt in ALL_LENSES if not lenses.get(lt)]
        parallel = order > first_order

        # -- repair: realized but incomplete (C5) --
        if sl["status"] == "realized" and missing:
            lens = missing[0]
            inconsistencies.append({
                "kind": "realized-but-lens-missing", "target": ref,
                "detail": f"slice is stamped realized but lens doc(s) missing: "
                          f"{', '.join(missing)} — downstream gates "
                          "(grill/implement) require all seven"})
            candidates.append(cand(
                f"repair/{ref}/{lens}", LENS_PLAY[lens],
                f"/{LENS_PLAY[lens]} {ref}", ref, "repair",
                gates=[f"slice status is 'realized' but the '{lens}' lens doc is absent"],
                order_hint=order, repair=True,
                unblocks=[f"every epic of {ref} (the seven-lens gate)",
                          f"/grill on {ref}" if not sl.get("has_epics") else ""]))
            # the queue behind the broken gate stays VISIBLE (S1/F6): every
            # live epic of this slice is a blocked candidate naming the lens
            epic_by_id = {e["id"]: e for e in sl.get("epics", [])}
            for e in sorted(sl.get("epics", []), key=lambda e: (e.get("order") or 0,
                                                                e["id"])):
                if e["status"] == "delivered":
                    continue
                eref = f"{ref}/{e['id']}"
                dep_note = []
                for dep in e.get("depends_on") or []:
                    dep_e = epic_by_id.get(dep)
                    if dep_e and dep_e["status"] != "delivered":
                        dep_note.append(f"also waits for {dep} "
                                        f"(is '{dep_e['status']}')")
                play_for = {"ready": ("implement", f"/implement --epic {eref}"),
                            "fix_required": ("implement",
                                             f"/implement --epic {eref}"),
                            "in_delivery": ("validate", f"/validate --epic {eref}"),
                            "validated": ("launch", f"/launch --epic {eref}")}
                pl, cmd = play_for.get(e["status"],
                                       ("implement", f"/implement --epic {eref}"))
                candidates.append(cand(
                    f"execute/{eref}", pl, cmd, eref, "execute",
                    status="blocked",
                    blocker=f"slice gate broken: '{', '.join(missing)}' lens "
                            f"missing on {ref} — repair first"
                            + ("; " + "; ".join(dep_note) if dep_note else ""),
                    gates=[f"epic status '{e['status']}', order {e.get('order')}",
                           "the seven-lens gate requires all lens docs present"],
                    order_hint=order))

        # -- planned slice: walk both realize tracks, then /measure --
        if sl["status"] == "planned" and missing:
            heads = []
            for track, chain, lane in TRACKS:
                lens = next((lt for lt in chain if not lenses.get(lt)), None)
                if lens:
                    heads.append((track, chain, lane, lens))
            for i, (track, chain, lane, lens) in enumerate(heads):
                last = lens == chain[-1]
                candidates.append(cand(
                    f"{lane}/{ref}/{lens}", LENS_PLAY[lens],
                    f"/{LENS_PLAY[lens]} {ref}", ref, lane,
                    gates=[f"slice is planned at roadmap order {order}",
                           f"{track} track {chain_text(chain)} ({PIPELINE}): "
                           f"'{lens}' is its first missing lens doc — track order is "
                           "a recommendation, not a readiness gate"] + dep_state,
                    order_hint=order, parallel=parallel or i > 0,
                    unblocks=[f"the next lens in {ref}'s {track} track" if not last
                              else f"/measure on {ref} once both tracks are done"]))
            if not heads:
                # both tracks done, only measure.md missing
                candidates.append(cand(
                    f"foundation/{ref}/measure", "measure", f"/measure {ref}", ref,
                    "foundation",
                    gates=[f"slice is planned at roadmap order {order}",
                           "both realize tracks are done (ux, agentic, marketing, "
                           "architecture, quality, run lens docs present)",
                           f"/measure runs last and stamps the slice realized ({PIPELINE})"]
                          + dep_state,
                    order_hint=order, parallel=parallel,
                    unblocks=[f"/measure's realized stamp on {ref}", f"/grill on {ref}"]))

        if sl["status"] == "planned" and not missing:
            inconsistencies.append({
                "kind": "lenses-complete-but-unstamped", "target": ref,
                "detail": "all seven lens docs exist but the slice is not stamped "
                          "realized — /measure's stamp step did not finish"})
            candidates.append(cand(
                f"repair/{ref}/stamp", "measure", f"/measure {ref}", ref, "repair",
                gates=["all seven lens docs exist", "slice status is still 'planned'",
                       "/measure stamps the slice realized when the seven docs line up"],
                order_hint=order, repair=True,
                unblocks=[f"/grill on {ref}"]))

        # -- realized + complete: grill or execute --
        if sl["status"] == "realized" and not missing:
            if not sl.get("has_epics") and not sl.get("deferrals_exists"):
                candidates.append(cand(
                    f"grill/{ref}", "grill", f"/grill {ref}", ref, "grill",
                    gates=["slice is realized with all seven lens docs",
                           "no epics cut yet (no spine epics for the slice)"] + dep_state,
                    order_hint=order, parallel=parallel,
                    unblocks=["the execute pipeline (implement/validate/launch)"]))
            else:
                epics = sl.get("epics", [])
                live = [e for e in epics if e["status"] != "delivered"]
                if not live:
                    learning_targets.append((domain, sl, order))
                epic_by_id = {e["id"]: e for e in epics}

                # -- surface debt (C11/F8): a delivered epic with a required
                # user-facing surface whose surface-parity check never passed leaves
                # the slice in surface debt. The deterministic signal is the epic's
                # surface_verified stamp on the spine epics index: /validate sets it
                # true only when the required surface was measured and matched
                # (surface-contract.md). While debt is open, the next execute epic in
                # the slice is WITHHELD and a surface-repair action takes priority.
                debt_epics = sorted(
                    (e for e in epics
                     if e["status"] == "delivered"
                     and e.get("surface_type") in USER_FACING_SURFACES
                     and not e.get("surface_verified")),
                    key=lambda e: (e.get("order") or 0, e["id"]))
                surface_debt = bool(debt_epics)
                if surface_debt:
                    debt_ids = [e["id"] for e in debt_epics]
                    inconsistencies.append({
                        "kind": "surface-debt", "target": ref,
                        "detail": "slice carries surface debt: delivered epic(s) "
                                  f"{', '.join(debt_ids)} declare a user-facing "
                                  "surface that may not have been delivered at its "
                                  "declared type (surface-contract.md) — the surface "
                                  "repair takes priority and further execute epics "
                                  "are withheld until it clears"})
                    candidates.append(cand(
                        f"repair/{ref}/surface", "validate",
                        f"/validate --epic {ref}/{debt_ids[0]}", ref, "repair",
                        gates=["slice carries surface debt: delivered user-facing "
                               f"epic(s) {', '.join(debt_ids)} — required surface "
                               "must be re-checked before more epics build on it"],
                        order_hint=order, repair=True,
                        unblocks=[f"every further execute epic of {ref} "
                                  "(withheld while surface debt is open)"]))

                for e in sorted(epics, key=lambda e: (e.get("order") or 0, e["id"])):
                    eref = f"{ref}/{e['id']}"
                    st = e["status"]
                    if st and st not in EPIC_STATUSES:
                        inconsistencies.append({
                            "kind": "unknown-epic-status", "target": eref,
                            "detail": f"epic status '{st}' is outside the vocabulary"})
                        continue
                    undelivered = []
                    for dep in e.get("depends_on") or []:
                        dep_e = epic_by_id.get(dep)
                        if dep_e is None:
                            inconsistencies.append({
                                "kind": "broken-epic-dependency", "target": eref,
                                "detail": f"depends_on '{dep}' does not exist "
                                          "in this slice"})
                        elif dep_e["status"] != "delivered":
                            undelivered.append(f"{dep} (is '{dep_e['status']}')")
                    if st in ("in_delivery", "fix_required") and not e.get("issue_ref"):
                        inconsistencies.append({
                            "kind": "epic-missing-issue-ref", "target": eref,
                            "detail": f"epic is '{st}' but carries no issue_ref"})
                    if surface_debt and st != "delivered":
                        candidates.append(cand(
                            f"execute/{eref}", "implement",
                            f"/implement --epic {eref}", eref, "execute",
                            status="blocked",
                            blocker=f"slice {ref} carries surface debt "
                                    f"(delivered user-facing epic(s) "
                                    f"{', '.join(debt_ids)}) — repair the surface "
                                    "first; further execute epics are withheld",
                            gates=[f"epic status '{st}', order {e.get('order')}",
                                   "surface debt blocks further execute work "
                                   "(surface-contract.md)"],
                            order_hint=order, parallel=parallel))
                        continue
                    if st == "ready":
                        if undelivered:
                            candidates.append(cand(
                                f"execute/{eref}", "implement",
                                f"/implement --epic {eref}", eref, "execute",
                                status="blocked",
                                blocker="waits for dependency epic(s): "
                                        + ", ".join(undelivered),
                                gates=[f"epic order {e.get('order')}",
                                       "deps must be 'delivered' "
                                       "(check_ready_epic gate)"],
                                order_hint=order, parallel=parallel))
                        else:
                            candidates.append(cand(
                                f"execute/{eref}", "implement",
                                f"/implement --epic {eref}", eref, "execute",
                                gates=["epic status 'ready'",
                                       "all depends_on delivered",
                                       "slice realized with seven lens docs"],
                                order_hint=order, parallel=parallel,
                                unblocks=[x["id"] for x in epics
                                          if e["id"] in (x.get("depends_on") or [])]))
                    elif st == "fix_required":
                        candidates.append(cand(
                            f"execute/{eref}/fix", "implement",
                            f"/implement --epic {eref}", eref, "execute",
                            gates=["epic status 'fix_required' — the fix round "
                                   "(re-admits /implement with the validate "
                                   "fix report)"],
                            order_hint=order,
                            unblocks=[f"/validate then /launch on {e['id']}"]))
                    elif st == "in_delivery":
                        candidates.append(cand(
                            f"execute/{eref}/validate", "validate",
                            f"/validate --epic {eref}", eref, "execute",
                            gates=["epic status 'in_delivery' "
                                   "(its /validate gate also requires "
                                   "/implement's verdict to hold)"],
                            order_hint=order,
                            unblocks=[f"/launch on {e['id']}"]))
                    elif st == "validated":
                        candidates.append(cand(
                            f"execute/{eref}/launch", "launch",
                            f"/launch --epic {eref}", eref, "execute",
                            gates=["epic status 'validated' — /launch's hard "
                                   "precondition"],
                            order_hint=order,
                            unblocks=["delivery (epic merges and leaves the model)"]))

    # ---- learning + strategy refresh -------------------------------------
    for domain, sl, order in learning_targets:
        ref = slice_ref(domain, sl)
        candidates.append(cand(
            f"learning/{ref}", "learn", "/learn", ref, "learning",
            gates=[f"{ref} is grilled and every epic is delivered/cleared"],
            order_hint=order,
            unblocks=["the KB and product LTM (skipping learning piles up "
                      "corrections later)"]))

    live_work = [c for c in candidates
                 if c["lane"] in ("strategy", "lens", "foundation", "grill",
                                  "execute", "repair")]
    if not live_work and any_slices:
        deferred_domains = [d["id"] for d in domains
                            if d.get("deferred") and
                            (d["deferred"].get("functionalities"))]
        for dom in deferred_domains:
            candidates.append(cand(
                f"refresh/shape/{dom}", "shape", f"/shape {dom}", dom, "refresh",
                gates=["all in-flight work is delivered",
                       f"domain '{dom}' holds a deferred bucket — parked "
                       "functionality ready to be re-shaped"],
                unblocks=["the next round of slices"]))
        candidates.append(cand(
            "refresh/roadmap", "roadmap", "/roadmap", "(all slices)", "refresh",
            gates=["all in-flight work is delivered — re-plan from here"],
            unblocks=["the next build cycle"]))

    return order_candidates(candidates), inconsistencies


def slice_of(c):
    """The domain/slice ref a slice-scoped candidate belongs to; None otherwise."""
    if c["lane"] not in SLICE_LANES:
        return None
    parts = c["target"].split("/")
    return "/".join(parts[:2]) if len(parts) >= 2 else None


def step_rank(c):
    """Within one slice: repair → feature track → technical track → /measure →
    /grill → epics (generation order keeps epics in their own order)."""
    if c["lane"] == "repair":
        return 0
    if c["lane"] == "lens":
        return 1
    if c["lane"] == "foundation":
        return 3 if c["play"] == "measure" else 2
    if c["lane"] == "grill":
        return 4
    return 5


def order_candidates(candidates):
    """Apply the finish-the-slice-first order (C14) and stamp rank, focus,
    parallel_lane and why. Pure and deterministic."""
    for seq, c in enumerate(candidates):
        c["_seq"] = seq
        c["slice"] = slice_of(c)
    work = [c for c in candidates if c["slice"] and c["lane"] in WORK_LANES]
    focus = (min(work, key=lambda c: (c["order_hint"], c["slice"]))["slice"]
             if work else None)

    def key(c):
        if c["lane"] == "repair":
            return (0, c["order_hint"], c["slice"] or "", 0, c["_seq"])
        if c["slice"] == focus and c["lane"] in WORK_LANES:
            return (1, 0, "", step_rank(c), c["_seq"])
        if c["lane"] == "strategy":
            return (2, 0, "", 0, c["_seq"])
        if c["lane"] in WORK_LANES:
            return (3, c["order_hint"], c["slice"] or "", step_rank(c), c["_seq"])
        if c["lane"] == "learning":
            return (4, c["order_hint"], c["slice"] or "", 0, c["_seq"])
        return (5, 0, "", 0, c["_seq"])

    candidates.sort(key=key)
    for i, c in enumerate(candidates, 1):
        del c["_seq"]
        c["rank"] = i
        c["focus"] = bool(focus) and c["slice"] == focus
        c["parallel_lane"] = (c["slice"] is not None and c["slice"] != focus
                              and c["lane"] in WORK_LANES)
        c["why"] = why_for(c, focus)
    return candidates


def why_for(c, focus):
    """One plain-language sentence for the candidate — templated, never inferred (C3)."""
    lane, tail, play = c["lane"], c["id"].split("/")[-1], c["play"]
    name = c["slice"].split("/")[-1] if c["slice"] else ""
    if c["id"] == "strategy/vision":
        why = "There is no product model yet, so the first step is writing the product vision."
    elif c["id"] == "strategy/understand":
        why = ("The product profile or some capabilities are still rough, so they need "
               "detailing before slices can be cut.")
    elif lane == "strategy" and play == "shape":
        why = (f"Domain {c['target']} has detailed capabilities but no slices yet, so it "
               "needs cutting into slices.")
    elif c["id"] == "strategy/roadmap":
        why = ("Some slices have no build order yet, so the roadmap needs planning before "
               "more realize work.")
    elif lane == "repair" and tail == "stamp":
        why = (f"All seven lenses exist on {name} but it was never marked realized, so "
               "/measure needs to finish its stamp.")
    elif lane == "repair" and tail == "surface":
        why = (f"An epic already delivered on {name} may not have shipped the surface it "
               "promised, so recheck it before more epics build on it.")
    elif lane == "repair":
        why = (f"{name} is marked realized but its {tail} lens is missing, so add it before "
               "any epic on the slice is built.")
    elif lane in ("lens", "foundation") and play == "measure":
        why = (f"Both realize tracks are done on {name}; /measure runs last and marks the "
               "slice realized.")
    elif lane in ("lens", "foundation"):
        why = f"{name} still needs its {tail} lens, the next step in its {TRACK_NAME[tail]}."
    elif lane == "grill":
        why = (f"{name} is realized with all seven lenses, so it is ready to be cut into "
               "buildable epics.")
    elif lane == "execute":
        epic = c["target"].split("/")[-1]
        if c["status"] == "blocked":
            why = f"Epic {epic} on {name} cannot start yet: {c['blocker']}."
        elif tail == "fix":
            why = f"Epic {epic} on {name} failed validation, so it needs its fix round."
        elif tail == "validate":
            why = f"Epic {epic} on {name} is built, so it needs independent validation next."
        elif tail == "launch":
            why = f"Epic {epic} on {name} passed validation, so it is ready to land."
        else:
            why = (f"Epic {epic} on {name} is ready and everything it depends on is "
                   "delivered, so it can be built now.")
    elif lane == "learning":
        why = (f"Every epic on {name} is delivered, so capture what was learned before the "
               "next cycle.")
    elif lane == "refresh" and play == "shape":
        why = (f"All work is delivered and domain {c['target']} has parked functionality "
               "ready to shape into new slices.")
    else:
        why = "All in-flight work is delivered, so plan the next build cycle on the roadmap."
    if c["parallel_lane"]:
        why += f" It can run in parallel, but {focus.split('/')[-1]} is the slice to finish first."
    elif c["focus"] and lane != "repair":
        why += " This moves forward the slice being finished first."
    return why


def main(argv=None):
    ap = argparse.ArgumentParser(description="/next decision tree over the model snapshot.")
    ap.add_argument("--state", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)

    with open(args.state, encoding="utf-8") as fh:
        state = json.load(fh)

    candidates, inconsistencies = derive(state)
    payload_for_hash = json.dumps(
        {"candidates": candidates, "inconsistencies": inconsistencies},
        sort_keys=True)
    focus = next((c["slice"] for c in candidates if c["focus"]), None)
    out = {
        "derived_from_model_hash": state.get("model_hash"),
        "focus_slice": focus,
        "candidates": candidates,
        "entries": candidates[:CAP],
        "cut_for_cap": [c["id"] for c in candidates[CAP:]],
        "inconsistencies": inconsistencies,
        "derivation_hash": "sha256:" + hashlib.sha256(
            payload_for_hash.encode("utf-8")).hexdigest(),
    }
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
    print(json.dumps({"ok": True,
                      "focus_slice": focus,
                      "candidates": len(candidates),
                      "entries": len(out["entries"]),
                      "runnable": sum(1 for c in candidates
                                      if c["status"] == "runnable"),
                      "blocked": sum(1 for c in candidates
                                     if c["status"] == "blocked"),
                      "inconsistencies": len(inconsistencies),
                      "derivation_hash": out["derivation_hash"],
                      "out": args.out}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
