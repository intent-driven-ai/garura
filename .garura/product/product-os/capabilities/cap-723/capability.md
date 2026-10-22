# Capability: Link the product model

## Benefit hypothesis
- Who it serves: the plan owner, who plans work toward a business intent (a goal a person sets for the product). It also serves the plays that plan or build from the model.
- What we believe: work can start before the model is complete, if the model links its parts by these rules:
  - Each capability links to the business intents it serves. Each functionality links to the capability that holds it.
  - A domain links to its capabilities and business intents only to help people find them. A missing domain never stops work.
  - A capability or functionality can need another capability or functionality. "Needs" means the other one must be done first. Work items (Feature, Story, Spike, Chore, Bug) never need anything.
- How we will know: a ready check gives one answer for each capability and functionality. It reads the links, the needs and the status of each part, and applies the rules above.
  - Ready: it serves a confirmed business intent, and everything it needs is done. The agent intent (ICE) goes forward, and work starts.
  - Partly ready: it is ready, but the check found gaps that do not stop work, such as no domain or an ICE with no context yet. The ICE goes forward, and work starts. The check lists each gap to fix later. (Our proposal: what counts as a gap is not yet agreed.)
  - Not ready: it serves no confirmed business intent, or something it needs is not done. The ICE does not go forward, and work stops until the cause is fixed. The page itself is kept.

## Boundary (In / Out / Never)
- In: the link rules above, written once in the ontology. Every play reads them from there, so all plays agree.
- In: the ready check and its three answers: ready, partly ready and not ready.
- In: the check that each link points at a part that exists. The ready check reads these links, so a link to nothing gives a wrong answer.
- In: search by domain. A person picks a domain and sees its capabilities and business intents. Domains do not decide when work starts, so search is their only job.
- Out: making, showing or changing a plan. The plan capabilities own this (Build a plan, View plans, Manage a plan).
- Out: branches for a plan. Start and land work against a plan owns this.
- Out: writing domain pages and capability pages. The discovery plays do this, and they follow these rules.
- Never: change how model pages are saved. Every play already writes pages that way, and a change would break them. Business intent #722 forbids it.
- Never: stop a write. A rule can stop work, but the page is always kept, so no work that a play found is lost.

## Guiding rules
- One answer for one model. The ready check is a script, not a judgment. The same model always gives the same answer.
- Old pages still pass. A gap in a page made before these rules is a warning, not an error. A new rule must not break an old model.
- Plans need plans only through their parts. A person never sets "plan A needs plan B". The check finds it from the needs of the capabilities and functionalities in each plan.
- Business intents never need each other. One business intent can lead to another ("identified by"). That link is history, not an order of work.

## Functionalities
- Ready without a domain (fn-724): the ready check gives its answer without the domain.
- The ontology (fn-597): the written rules for each kind of part and its links, with examples from more than one field.
- "Needs" and "identified by" (fn-725): the two links between capabilities and functionalities, and the check that each link points at a part that exists.
- Domains for search (fn-726): a search by domain shows its business intents and capabilities. A domain never shows in a plan or in the tracker.

## Sources
- core/components/memory/standards/schemas/product-os/ontology.md (v5): "Nothing is blocked", and the Capability rule "It is ready when it serves a confirmed business intent and nothing it needs is still open. A missing domain never blocks it."
- core/components/memory/standards/schemas/product-os/spine.yaml: "Ready (check_ice_workable.py): a capability serves a confirmed business intent and nothing in its `depends_on` (\"needs\") is open".
- .garura/product/product-os/intents/bi-722.md: "a plan can be built and worked on without first writing a full product model", and "Must not: change how model pages are saved."
- .garura/project/issues/621/specs/plan-design.md: "Domains are not in the tree", and "Business intents are connected, not dependent".
- .garura/project/issues/621/specs/change-list.md: "C4 Link the product model", with F4.1 to F4.4.
- .garura/user-provided/managing-work.md: "Domains live in the product model and link loosely to business intents and capabilities; they are never an issue and never part of a plan."
- GitHub #723: "Link the product model: needs, identified by, and loose domains"; #722, #724, #725, #726 and #597 for its functionalities.
- Shelf: none. No domain shelf holds the product model of a framework itself (routing for #723).

## Agent intent (ICE)
- Goal: The model can be built in any order and still links up.
- Goal: A capability with no domain, serving a confirmed business intent, is reported ready and can be planned and built.
- Goal: Every need and identified-by link names a capability or functionality that exists in the spine.
- Limit: How pages are saved stays the same.
- Limit: Links sit only on capabilities and functionalities, never on work, and a domain is never a level of a plan.
- Fails if: a node waits on a domain before work can start, or a link points at nothing.
- Fails if: a pre-v5 model page that passed before now fails because a domain, an ICE or a link is missing.
- Context: serves the plan owner and the plays that read the model (build-plan, /discover-domains, /discover-capabilities, the Alignment loop); touches the ontology, the spine schema, check_ice_workable.py, lint_grounding.py and check_ontology.py; in are the links and the ready rule, out are plan files, tracker issues and branches.
- Checked by: the ontology check and the spine linter pass on Garura's own model built for #717 and #722.
- Checked by: check_ice_workable.py gives each capability and functionality one answer: ready, partly ready (work goes on, gaps listed) or not ready (work stops). On Garura's own model, cap-723 is partly ready: bi-722 is confirmed and it needs nothing, and its only gap is no domain.
- Quality need: zero links that point at nothing or at work across Garura's own model, checked by the spine linter.
