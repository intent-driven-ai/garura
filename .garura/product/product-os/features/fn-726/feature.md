# Feature: Domains link to business intents and capabilities, outside the plan tree

## What it does
A domain lists the business intents and capabilities in it. Thus a person can ask, "Which business intents serve the commerce domain?" Domains are never in a plan or in the tracker.
- A domain is a large area of the product. The model keeps it only for finding things.
- The spine is the file that lists each node and its links. In the spine, the `intents` of a domain name the business intents that touch it. Each capability in the domain names it in its own `domain` field. Together, these two links answer a search by domain.
- The link is loose. A capability can have no domain. A new or changed domain never changes whether something is ready (a play can plan or build from it), or what a plan holds.
- It also keeps domains out of the places where work is ordered. No plan file has a domain level, and nobody files a tracker issue for a domain.
- When it runs: the search runs on request, when a person or a play asks for a domain.
- The keep-out check is part of the spine linter (lint_grounding.py --spine). It runs each time that linter runs, over the spine, the domain pages and the plan files. Our default — the sources do not say which check holds the keep-out rule.

## Inputs / Outputs
- In: the spine. For each domain, it reads the `id` and the `intents`. For each capability, it reads the `domain`.
- In: the business intent pages. The Touches list on each page names the domains that the intent touches. Each name has the mark adds, changes or removes.
- The search lists the intent under the domain for each mark, and shows the mark beside it. Thus a reader sees how the intent touches the area.
- In: the plan files (`.garura/project/plans/*.yaml`). For each node in the `tree` of a plan (and its `children`), it reads the `kind` and the `issue` number.
- In: the spine entry of each domain, which it checks for an `issue` field. The check never reads the tracker itself.
- In: the page of each domain (the `doc` that its spine entry names) and its spine entry. The check reads them to see if the domain has an Agent intent (ICE), the short agent intent of a node.
- Out: for a domain id, the search gives the business intents that touch it and the capabilities in it, each with its page link. Through those capabilities, it also gives their features.
- Out: each listed intent shows its Touches mark (adds, changes or removes). A link that only one side holds has the flag "one-sided".
- Out: some capabilities name a `domain` id that the spine does not hold. The search lists each one under that id, with the mark "not in the spine".
- Out: the check gives an error when a plan file has a node of kind domain, or when a domain links to a tracker issue.
- Out: the check gives an error when a domain page has an `## Agent intent (ICE)` section. It also gives an error when the spine entry of a domain has an ICE field.
- Out: the check gives a warning for alignment for each link that only one side holds.
- Out: the check gives a warning for alignment for each capability whose `domain` names an id that the spine does not hold. The warning names the capability and the id.

## Rules & behavior
- Both sides keep the link. When the Touches list of an intent names a domain, the spine `intents` of that domain names the intent, and the reverse. A play that writes one side also writes the other side. Thus a search from the intent and a search from the domain always give the same answer.
- A link that the check finds on one side only gives a warning for alignment, never an error. It never stops a write, because the parent capability has the rule that nothing is blocked. The Alignment loop writes the missing side.
- The search still returns a one-sided link from the side that holds it, with the mark "one-sided". Our default — the sources say a play writes both sides but not what happens when one is missing.
- The check finds a domain linked to a tracker issue from files only, never from the tracker. It looks for two things.
- First, a domain entry in the spine that has an `issue` field. Garura's spine puts this field on capability and feature entries, for example `issue: 723` on cap-723.
- Second, a node in a plan file whose `kind` is domain. A plan node always holds an `issue`, and names its kind but no node id, so the check reads the kind.
- Either one is an error that names the domain (its spine id, or the title of the plan node) and the issue number. Our default — the sources say a domain has no issue but not how the check sees one.
- A capability names one domain at most. A domain lists its capabilities only through those capability entries, so there is one place to change.
- A domain that no capability names and no intent touches is still a valid domain. The search returns it with empty lists.
- A domain id that a capability names but the spine does not hold gives a warning for alignment, never a block (see fn-724). The search shows it as "not in the spine".
- A domain is never a level of a plan tree, never a tracker issue, and never has an ICE. Each of these is an error, because domains set which areas the product covers, not which work is done.
- Garura's own model has no domains yet (`domains: []`). Thus the search returns nothing and the check passes. This is the expected state until /discover-domains adds domains.
- The search reads only files and changes nothing, so it can run at any time.

## Acceptance criteria
- Given a test model with a commerce domain that two business intents touch and three capabilities name, when a search for that domain runs, then it lists exactly those two intents and three capabilities with their page links.
- Given a business intent whose Touches list names a domain that does not name it back in `intents`, when the check runs, then it warns, names the intent and the domain, and still passes.
- Given a business intent whose Touches list names a domain that does not name it back in `intents`, when a search for that domain runs, then the intent is listed with its Touches mark and the flag "one-sided".
- Given a capability whose `domain` names an id that the spine does not hold, when a search for that id runs, then the capability is listed with the mark "not in the spine". When the check runs, then it warns, names the capability and the id, and still passes with no error.
- Given a spine where a domain entry has an `issue` field, or a plan file with a node of kind domain that holds an issue number, when the check runs, then it fails with an error that names the domain and the issue number.
- Given a plan file with a node whose kind is domain, when the check runs, then it fails with an error that names the plan and the node.
- Given a domain whose page has an `## Agent intent (ICE)` section, or whose spine entry has an ICE field, when the check runs, then it fails with an error that names the domain and where the ICE was found.
- Given Garura's own model with no domains, when the search and the check run, then the search returns nothing and the check passes.
- Given a capability with an empty domain, when the ready check runs on it, then the missing domain does not change its readiness.

## Out of scope
- Writing domain pages and adding a domain to the spine. /discover-domains owns that.
- Deciding readiness. fn-724 owns it, and a domain has no part in it.
- The needs and identified-by links. fn-725 owns those.
- Showing plans. View plans (cap-719) shows the plan tree, which has no domain level.

## Sources
- core/components/memory/standards/schemas/product-os/ontology.md (v5), kind Business Intent: "It touches a domain … A loose link, for finding things; a domain is never part of its plan".
- Ontology, "Not yet defined", Domain: "It is for finding things: never part of a plan, never a tracker issue."
- .garura/project/issues/621/specs/plan-design.md: "Domains are not in the tree. They live in the product model … They have no issue."
- .garura/user-provided/managing-work.md: "they are never an issue and never part of a plan."
- .garura/product/product-os/_spine.yaml: "domains: []".
- GitHub #726: "Domains link to business intents and capabilities, outside the plan tree".
- Shelf: none. No domain shelf holds the product model of a framework itself (routing for #723).

## Agent intent (ICE)
- Goal: A search by domain finds its business intents and capabilities.
- Goal: Every domain link is kept on both sides — the intent's Touches list and the domain's spine `intents`.
- Limit: A domain never gets an issue and is never a level of a plan.
- Limit: A domain never changes whether a capability or feature is ready.
- Fails if: a domain appears in a plan file or the tracker.
- Fails if: the search by domain misses an intent or capability linked to it, or lists one that is not.
- Context: serves the plan owner asking which work sits in an area, /discover-domains and the Alignment loop; touches the spine's domains and capabilities, the intent pages' Touches lists and the plan files; in are the lookup and the keep-out check, out are writing domains and readiness.
- Checked by: a query for a domain in a test model lists its business intents and capabilities.
- Checked by: a check over every plan file finds no domain node, and passes on Garura's own plans 717, 722 and 734.
