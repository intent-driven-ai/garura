# Surface Contract

Single source of truth for **what user-facing surface an epic promises**, **how it
is declared**, and **what counts as that surface actually running**. Every gate in
the execute pipeline references this rule instead of re-deciding "what is the
surface" on its own — so the five plays cannot drift apart, the way they did before
this rule existed (ADR 022, #442).

It governs the epic's `surface` block (`schemas/product-os/epic.yaml`) and the
checks `/shape-slice`, `/build-epic`, `/validate-epic` and `/release-epic` run against it.

## The rule

**The surface is declared once, at the cut, and checked — never re-derived.**

`/shape-slice` writes `surface` when it cuts the epic. Every downstream play **reads** the
declared `surface.type`; none of them re-interprets `user_check` or `acceptance`
prose to decide the surface for themselves. Re-deriving the surface downstream is
the failure this rule exists to stop: a play that infers the surface can infer it
wrong, and two plays inferring independently can disagree about what the epic even
promised. A declared field is deterministically checkable; a derived one is not.

A missing `surface` (a legacy epic cut before this rule) is **"unknown," not a
default.** `/build-epic` must have it declared before it builds — never assume
`service_read_model` or any other value. A silent default re-creates the bug.

## The taxonomy

`surface.type` is exactly one of:

| type | user-facing? | what it is |
|------|--------------|------------|
| `web_dashboard` | yes | openable in a browser |
| `server_api` | yes | an HTTP/API endpoint a human or integration calls |
| `cli` | yes | a command-line entry point a human runs |
| `library` | no | importable code, no run surface |
| `service_read_model` | no | an internal service / read model, no user surface |

The two non-user-facing types are legitimate, but must be declared **explicitly** —
they are never what an epic silently decays into. `service_read_model` is precisely
the value the downgrade bug substituted for `web_dashboard`.

## Required runnable evidence — what `/validate-epic` must measure

For each `surface.type`, validation is only complete when it has run the matching
check. A required surface that was not measured is `fix_required`, never
`validated`. "No browser/API probes available" does not waive a check the surface
requires — it fails it.

| type | required runnable check |
|------|-------------------------|
| `web_dashboard` | a real browser check that opens each `must_open` artifact and observes it render |
| `server_api` | an HTTP/API check that calls the declared endpoint and asserts the response |
| `cli` | a command run that executes `human_run_target` and asserts its output |
| `library` | the library's own tests/import — no run surface to open |
| `service_read_model` | the service's own tests — no user surface to open |

## Valid deploy targets — what `/release-epic` must accept

The deploy record's reachable target must match the surface. `/release-epic` rejects a
record whose shape can't satisfy the declared type, before it asks for human
acceptance.

| type | a valid reachable target | NOT valid |
|------|--------------------------|-----------|
| `web_dashboard` | a real local URL, preview URL, or declared server endpoint | a local command (`python3 ...`), a JSON artifact path |
| `server_api` | a reachable HTTP endpoint (local or preview) | a local command, a file path |
| `cli` | the command and the env it runs in | — |
| `library` | n/a (no deploy surface; launch records the package/import) | a URL pretending to be a UI |
| `service_read_model` | n/a (internal; launch records the service entrypoint) | a URL pretending to be a UI |

**Scenario verb preservation.** A HITL scenario must preserve the user verb of the
`must_open` artifact it covers. "Open the Formula reference" cannot be covered by
"run `python3 -m unittest`." A scenario whose verb does not match the surface is a
semantic mismatch and is rejected.

## Downgrade ordering — what `/build-epic` must block

User-facing surfaces rank above non-user-facing ones:

```
web_dashboard ≈ server_api ≈ cli   >   service_read_model ≈ library
```

A generated build spec whose surface is **below** the epic's declared `surface.type`
is a **downgrade** (e.g. a `service_read_model` build spec for a `web_dashboard`
epic). `/build-epic` halts on a downgrade and requires explicit human approval of a
recut — it never silently builds the lower surface. Building the *same or higher*
surface is fine.

**App-shell seeding.** The **first** epic of a slice whose surface is
`web_dashboard`/`server_api` must scaffold the app/server shell (a minimal openable
app), or be recut. A vertical with no shell for later epics to attach to is the seed
of the downgrade — every later epic then has nothing user-facing to extend.

## Surface debt — what it blocks

A `delivered` epic whose required surface was not actually delivered (it shipped a
lower surface than declared, or its required check never ran) leaves the slice in
**surface debt.** The surface repair goes ahead of the next execute epic in that
slice in the plan, so later epics stop inheriting and compounding the downgrade.
(`/next` used to enforce this; it was dropped by ADR 051, and the plan is the work list.)

## How the plays use this rule

- **`/shape-slice`** — declares `surface` at cut (taxonomy above); enforces app-shell
  seeding on the first user-facing epic.
- **`/build-epic`** — reads `surface.type`; blocks a downgraded build spec (ordering
  above); requires a missing surface to be declared before building.
- **`/validate-epic`** — runs the required runnable check for `surface.type`; unmeasured
  required surface ⇒ `fix_required`.
- **`/release-epic`** — validates the deploy target shape and scenario verbs against
  `surface.type`; rejects before HITL.
