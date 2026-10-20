# .garura/ — the installed copy

This folder is the **installed copy** of Garura in this repository. It is what an install
laid here. It is **not the working copy**. The working copy — the source you edit — is
`core/` (and `installer/`).

- Never edit, add or delete anything under `.garura/core/` (config, memory, tools) to make a
  change. Make the change in `core/`. It reaches `.garura/` only when Kapil asks for an
  install.
- Never clear, move or un-ignore the installed memory copy (`.garura/core/memory/`) or the
  installed memory tool, even when an ADR says how a project's `.garura/` should look. An ADR
  about `.garura/` is built in the install's source, not by hand here.
- Plays still write their run records here as usual: short-term memory under
  `.garura/project/issues/<issue>/`, and the product model's records. That is normal work, not
  a change to the installed copy.
