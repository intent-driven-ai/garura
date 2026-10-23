# Rebuild eval

The test of what a Discovery loop (or one of its plays) produced from a prototype. Two questions:

1. **Is the output right?** Every business intent has its outcome, why, asked by, proof and
   sources. The domain is a real one, found by research, with its sources. Every capability
   and feature names where on the prototype it is seen, and that quote is on the
   prototype.
2. **Can the prototype be rebuilt from it?** A fresh agent, with no sight of the prototype and
   no knowledge of Garura, builds the product from the intents and the model
   alone. Then what the prototype does is tried on what it built. Design, layout and code may
   differ; what a person can do and see may not. What is missing, what is half there and what
   was added is the **drift**.

If the intents and the model do not bring the prototype back, they are not good enough to
build from. That is the bar every change to `/discover-intent`, `/discover-domains` and `/discover-capabilities` is judged by.

## The stages

| Stage | Who | Sees | Writes |
|---|---|---|---|
| `prepare` | script `prepare.py` | the product model folder | `brief/` — the intents and model pages only, local paths and file links taken out |
| `inventory` | an agent (Claude, `prompts/inventory.md`) | the prototype only | `inventory.json` — every thing a person can do on it and what they see, with the quote and screen |
| `check` | script `check_output.py` | `brief/`, the prototype's text and the inventory's captures | `check.json` — the static findings |
| `build` | a fresh, restricted Claude session (`run_builder.py`, `prompts/build.md`) | `brief/` only, in an empty folder | `build/app/index.html` — the rebuilt product |
| `review` | an agent (Claude, `prompts/review.md`) | `brief/`, `inventory.json` | `review.json` — each intent, the domain, each capability and feature judged |
| `compare` | an agent (Claude, `prompts/compare.md`) | `inventory.json`, the rebuild, `brief/` | `compare.json` — each behaviour met, partial or missing, why, and each extra |
| `score` | script `score_drift.py` | `inventory.json`, `compare.json`, `check.json`, `review.json` | `report.json`, `report.md` |

The static check fails what a script can see: a missing field, a proof left open, a domain with
no research source, a feature that does not say where on the prototype it is, or quotes
words the prototype does not have. The review judges what needs judgement: does each intent name
a need the product offers, is "asked by" a persona, is the domain one the world recognises, is
any feature invented or only one panel of a screen.

The inventory is made from the prototype alone, never from the loop's output, so the test is
not marked by the work it tests. It is made once per prototype and reused (`--inventory`).

## Isolation

- **Every agent runs on Sonnet 5.5 at high effort** (`--claude-model`, `--effort`). The plays
  under test run on their own models; only the eval's agents run on Sonnet.
- **The builder** is a new Claude Code session, run `--restricted --strict-mcp-config
  --disable-slash-commands` with file tools only, in a folder that holds only `brief/`: no
  settings files, no MCP servers, no skills, no shell, no files outside the folder. It gets no
  prototype, no Garura files, no instructions but `prompts/build.md`.
- **The brief** carries no path or link to the prototype or to the loop's records;
  `prepare.py` takes them out and lists what it took out (`brief-manifest.json`).
- **The inventory agent** sees the prototype and nothing of the loop.
- **The compare agent** sees the inventory, the rebuild and the brief. It reads the brief only
  to say why a behaviour is missing: not in the brief (the loop's fault) or in the brief but
  not built (the builder's fault).
- The inventory, review and compare agents run from the eval's run folder, so no project instructions load. The
  report records how each agent was run.

## The drift score

Each prototype behaviour counts 1 when met, ½ when partly met, 0 when missing.

- **Kept** = (met + ½ partial) ÷ behaviours. **Drift** = 1 − kept.
- **Missing, not in the brief** — the intents and model never said it: the loop's fault.
- **Missing, in the brief** — the brief said it and the builder did not build it: the builder's
  fault, not counted against the loop's output, but shown.
- **Added** — what the rebuild does that the prototype does not, split the same way (said in
  the brief, or the builder's own).
- The same numbers by screen of the prototype.

The static check is reported beside the score: a model can score well and still have, say, an
invented domain.

## Running it

```
python3 run_eval.py --product-os <project>/.garura/product/product-os \
    --prototype <project>/prototype/argus.html --out <run folder> \
    [--inventory <an earlier inventory.json>] [--stage all|prepare|check|inventory|build|compare|score] \
    [--claude-model claude-sonnet-5-5] [--effort high]
```

Each stage writes into `<run folder>` and can be run again on its own. The agent stages cost
money: the inventory once per prototype, a build and a compare per eval. The scripts alone
(`prepare`, `check`, `score`) cost nothing.

`python3 -m unittest test_rebuild_eval` runs the tests; the agents are stand-ins there.
