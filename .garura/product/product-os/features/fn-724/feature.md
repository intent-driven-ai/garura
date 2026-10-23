# Feature: A capability or feature is ready without a domain

## What it does
This is the new ready rule. "Ready" means a play can plan or build from the node. A capability is ready when it serves a confirmed business intent and nothing it needs is open. A feature is ready when its capability is ready and nothing it needs is open. A missing domain is a warning, never a block.
- When it runs: a play is about to plan, break down or build from the ICE of a node. The ICE is the short agent intent of the node. Before it starts, the play runs the ready check (check_ice_workable.py) on that node or on the full model.
- What it reads and gives: it reads the spine (the file that lists each node and its links) and the business intent pages. For each capability and feature, it answers "ready" or "not ready, because …", with any warnings. A domain that is missing, or not yet in the spine, gives only a warning.
- What it replaces: the ADR 043 rule. Under that rule, a node had to link all the way up to a domain that exists before a play could work on it. That rule blocked a plan built directly from a business intent. This feature removes that block.

## Inputs / Outputs
- In: the spine (`product-os/_spine.yaml`). For each capability, it reads `intents`, `domain` and `depends_on` ("needs"). For each feature, it reads `capability`, `intents` and `depends_on`.
- In: the business intent pages (`product-os/intents/<id>.md`). The `**Stage:**` line on each page says proposed, confirmed, met or dropped.
- In (optional): a list of the ids of the nodes that are done (`--done`, YAML or JSON). Without this list, the check shows the needs but does not say if they are open or done.
- In (optional): one node id (`--node`), to check only that node.
- Out: for each node, it gives its kind, the stage of each intent it serves, its needs and which needs are still open. It also gives whether the node is blocked, its warnings, `workable` true or false, and a plain reason. The output is JSON, on the screen or in the `--out` file.
- Out: an exit code when it checks one node. The code is 0 for ready, 1 for not ready, and 2 when the node is unknown or an input cannot be read. Thus a play can stop on the code without reading the JSON.

## Rules & behavior
- A capability is ready when at least one business intent in its `intents` is confirmed or met, and none of its needs is open. A met intent counts, because it was confirmed first. Work that keeps it met is still wanted.
- A feature is ready when its capability is ready and none of its own needs is open. The capability can be ready through its own confirmed intent or through the intent of the feature.
- A capability with an empty `domain`, or with a domain id that is not in the spine, is also ready. The check adds the warning "has no domain yet" or "is not in the spine". It never sets `workable` to false for this reason.
- A node with no intent, or with only proposed or dropped intents, is not ready. The check keeps it exactly as written. The check stops work on it, never the write that made it.
- A missing business intent page counts as not confirmed. Thus a link to an intent that nobody wrote never makes a node ready.
- A need that is not in the done list is open. An open need makes the node blocked and not ready, and the reason names what the node waits for. Without a done list, the check shows the needs, but they do not change the answer.
- A feature whose capability is not in the spine is not ready, because it has no capability to be ready through.
- A feature with no capability yet stays in the holding folder (`features/<id>/`). In this folder, a feature waits until a capability claims it. It is not ready, because a feature is ready only through a capability, and it has none.
- For that feature, the check also gives a warning, so the Alignment loop finds it and attaches it to a capability. The warning and the not-ready answer are separate. The warning asks for the link. The not-ready answer stops work until the link exists.
- The check reads only files. It uses no git, no network and no model call. Thus the same model always gives the same answer.
- The two copies of the script stay the same: the reference copy in create-play and the copy in discover-intent. A play that works on ICE copies the reference with no change. Thus every play gives the same ready answer for the same model.

## Acceptance criteria
- Given a capability with an empty domain that serves a confirmed business intent and needs nothing, when the ready check runs on it, then it is ready (exit 0) and its warnings include "has no domain yet".
- Given a capability whose only business intent is proposed, when the ready check runs on it, then it is not ready (exit 1) and the reason says no confirmed business intent.
- Given a capability that serves a confirmed intent and needs a node that is not in the done list, when the check runs with `--done`, then it is blocked, not ready, and the open need is named.
- Given the same capability and a done list that holds that need, when the check runs, then it is ready.
- Given a feature whose capability is ready and which needs nothing, when the check runs on it, then it is ready, although neither it nor its capability has a domain.
- Given an id that is not in the spine, when the check runs with `--node`, then it exits 2.
- Given Garura's own model on this branch, when the check runs on cap-723, then it reports workable true with the warning "capability `cap-723` has no domain yet".
- Given the fixture tests (test_check_ice_workable.py), when they run, then every case passes: no domain plus a confirmed intent is ready, no confirmed intent is not ready, and an open need is not ready.

## Out of scope
- The check that a need or identified-by link points at a real capability or feature. "Needs" and "identified by" link capabilities and features (fn-725) owns that.
- Writing or fixing the domain link. /discover-domains adds it later, and the Alignment loop flags a missing one. This check only gives a warning.
- Deciding which node to work on next, or in which order. Build a plan (cap-718) and /next do that from the ready answers.
- Changing how pages are saved. The business intent (bi-722) forbids it.

## Sources
- core/components/memory/standards/schemas/product-os/ontology.md (v5), kind ICE: "A missing domain is a warning for alignment, never a block (v5, … 2026-10-21; this replaces the v4 rule that a node must link up to a domain)."
- core/components/plays/create-play/references/check_ice_workable.py: "No git, no network, no LLM", and "exit 0 when that node's ICE is workable, 1 when it is not, 2 when the node is unknown or an input is unreadable."
- .garura/project/issues/621/specs/plan-design.md: "New ready rule: a capability is ready when it serves a confirmed business intent."
- GitHub #724 (closed): "A capability or functionality is ready without a domain".
- Shelf: none. No domain shelf holds the product model of a framework itself (routing for #723).

## Agent intent (ICE)
- Goal: A plan can build from capabilities and features that have no domain yet.
- Goal: The ready answer for a node depends only on its confirmed intents and its open needs.
- Limit: No change to how pages are saved.
- Limit: The check stops work on a node, never the write that created it.
- Fails if: the ready check says "no domain yet" for a node that serves a confirmed business intent.
- Fails if: a node with no confirmed business intent, or with an open need, is reported ready.
- Context: serves the plays that plan or build from ICE (build-plan, /discover-capabilities, /start-change) and the plan owner; touches check_ice_workable.py (both copies), its tests, the spine and the intent pages; in is the ready answer, out are the link-target check and the domain writes.
- Checked by: the ready check's tests: no domain + confirmed intent = ready; no confirmed intent = not ready; an open need = not ready.
- Checked by: running the check on Garura's own model reports cap-723 and its features workable with only a no-domain warning.
- Quality need: the same spine and intent pages always give the same ready answer, with no network or model call.
