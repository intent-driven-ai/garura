# Eval step libraries

One step library for each surface kind of the slices a plan's eval covers (ADR 069): every sentence an eval step may use, each one
exact action or check that a runner does with no agent. The rules of an eval: `standards/rules/eval-format.md`.

## Contents

| Path | Surface kind | Consumers |
|------|--------------|-----------|
| `steps-command-line.yaml` | command line, including a Claude Code play run in a test project | `/design-eval`, `author-slice-eval`, the eval runner (later) |

A library for the browser page, the mobile app and the backend endpoint is added when a slice first needs it.
