# Decision brief — #660

Shape: markdown (a framework decision), `docs/adr/`.

## Decision

The Garura install brings no memory into a project. It lays the memory tool, its settings and the memory guide, and checks that the tool runs and reaches the project's short-term and Garura memory.

Phoenix memory reaches a machine the first time the memory tool needs it. The tool downloads it whole, from the source its settings name (today a git repository; later a server address), to one place on the machine (default `~/.garura/phoenix-memory`). The download never blocks on a password and stops after a time limit; when it fails, the lookup is refused with Phoenix memory named. The install does not fail when Phoenix memory is not on the machine yet; it reports it, and notes when the source does not answer.

A project's own Garura memory is set up after the install by a new play, `initialize` (not designed or built yet). It reads Phoenix memory and asks the person questions built from it — which domains, which functionalities, which technology standards, tools and frameworks — each with choices to pick from. Until it runs, lookups go up to Phoenix memory.

The memory tool lives inside the project, at `.garura/tools/memory/`, with its settings (`settings.json`) beside it. The tool's own folder is never answered as Garura memory. This adds `tools/` to the `.garura/` folder whitelist.

Kapil, 2026-10-19 (on #660): "install finishes without any memory." "Today, when the tool runs for the first time after installation, it downloads the memory and puts it into a global source. It could go into the global .cloud, or it could go into the user's home base or something that the tool knows about. It's a local configuration. Eventually, this tool is going to point to a URL. After the installation is finished, we then run a play. This play is not designed yet, and that play is going to ask questions. That will read the Phoenix memory and will start setting up the project's memory. This is going to be a question about which domains, which functionalities, what kind of technology standards, tools, frameworks, or what have you. The question here will be generated based on the Phoenix memory that it already has, because we're not pulling something random. It has to give choices, and the user has to pick one of those. That's a new play which we have to build." And: "After install, let's call this whole thing `initialize`." On where the tool lives, he chose "a.1": the tool in the project at `.garura/tools/memory/`, with its settings beside it, hidden from Garura memory lookups.

Earlier, on #656 (2026-10-18), Kapil already ruled that the installer pulls nothing and that set-up plays fill a project's first memory; the #653 plan records "ADR 035 §2 still needs its amendment (its own /adr change)".

## Why now

#660 builds this (PR #677). Its review (round 1) found the code contradicts accepted ADR 035: §2 says "At install, a project pulls a starting set: Garura's rulebook and the memory guide", and its Alternatives list "A project pulls nothing at install; every piece on first need" as rejected. It also found `.garura/tools/` is not in ADR 017's `.garura/` whitelist. Kapil chose to record the decision before #677 merges, so the record and the code land together.

## Options considered

- **A starting set pulled at install (ADR 035 §2 as written).** Lost: Kapil decided the install finishes without any memory; what a project needs is chosen by the person in `initialize`, from choices built from Phoenix memory, not pulled blind at install.
- **The installer fills Phoenix memory on the machine at install.** Lost: the install should not carry or fetch memory; the tool fetches it when it first needs it, from a source it knows (later a URL).
- **The memory tool outside the project (machine-global, beside Phoenix memory).** Lost: Kapil chose "a.1", the tool inside the project with its settings beside it, so each project carries the version it was installed with.
- **The install fails when Phoenix memory cannot be reached.** Lost: a lookup never blocks a play (ADR 035 §3), and Phoenix memory arrives on first use; the install reports it and notes an unreachable source instead.

## Decided by

Kapil Viren Ahuja (owner), 2026-10-19.

## Decided in

#660 — the plan's item 1 (answers a.1, b.1, c), `.garura/project/issues/660/specs/plan.md`; earlier on #656 (installer pulls nothing), recorded in `.garura/project/issues/653/specs/plan.md` item 3.
