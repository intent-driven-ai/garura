# Decisions — #795 (product owner, 2026-10-23)

Q1 — The input is a business intent issue number, but the issue is only the entry point. The run finds that business intent in the product model and works from the model's current state of it. If the model has no page for it, the run writes the page from the issue and says so; it does not stop.
Q2 — Until #796 builds the one checkpoint for the shaping loop, /shape-slice writes the slice and its link to the live model, shows it at a typed checkpoint (yes / change / stop), and commits only after yes. Stop undoes the write.
Q3 — Every run fills the product model. When the slice needs a domain, capability, feature or ICE the model lacks, the run adds it at the depth it knows and marks it for a later play to deepen. Nothing waits; nothing is skipped.
Q4 — The tester is the surface's persona_ref in the slice record; the spine slice has `vertical`, the name of that one surface.
Q5 — A slice already serves the intent when it lists the intent in `intents`, or has the same features and the same surface; then the run adds the intent to it instead of making a new slice.
Q6 — The old /shape-slice is gone. Build the new one fresh with /create-play, reading the old play only for parts worth keeping (grill_budget.py, guards, end sequence). Dependents change in the same change: spine.yaml and slice.yaml follow the new slice.
Q7 — A slice links to capabilities, and through them to every domain it touches. It has no domain home: it lives in the spine's `slices` list, with its record at product-os/slices/<id>.yaml. A domain view shows every slice that touches it; a slice view shows every domain it touches.
/next — Drop /next now (it read the old chain; the plan is the work list). Remove the play, the "Or run /next" line in the shared close, and the Next-line map's /next pointer; record why in an ADR. Done in this change.
