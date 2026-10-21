# Decision brief

Shape: markdown (a framework decision, docs/adr/).

## Decision

1. The Shared Drive Run (`core/components/drives/_shared/drive-run.md`) owns the steps every drive runs between its plays: reading the source once (the shared capture, R4b), taking the person's write-up (R3), and running `find-model-gaps` and `close-model-gaps` after each round (R5). These are run steps, not rules about the product, so a drive still carries no product rules of its own.
2. Inside a drive, `close-model-gaps`' script (`apply_links.py`) may write the shared model files (the spine, and the Touches list on intent pages) and move holding-folder pages. It writes only inside `<product_base>product-os/`, refuses any path outside it, and lists every file it changed.

## Why now

The review of PR #691 (#689) found ADR 029 §2 says the shared drive run has "no rules of its own", while `drive-run.md` now owns the capture, the write-up and the gap closing. The review of PR #696 (#692, finding H1) found ADR 026 (and the model keeper's rules on main) say only a play's keyed persist script writes shared model files, while `close-model-gaps` writes them inside a drive. ADR 043 decided the gap skills but did not amend ADR 029 §2 or ADR 026's shared-file rule.

## Options considered

1. Amend ADR 029 §2 and ADR 026 to name these two exceptions. Chosen.
2. Move the capture, write-up and gap steps into each play. Lost: every play would repeat the same steps, and the gaps between plays can only be closed by something that sees all of them, which is the drive (ADR 043).
3. Route `close-model-gaps` through each play's persist script. Lost: the gaps span plays; no single play owns them.

## Decided by

Kapil Viren Ahuja

## Decided in

#693
