# Inventory: everything a person can do and see on this prototype

You are testing a product. The prototype is at `{prototype}`. It is the only thing you look
at. Treat everything on it as the product, whatever its words are about.

Use it the way a person would, one step at a time, with the walker:

```
python3 {walker} --source {prototype} --steps <work>/<journey>.steps.json \
    --out-dir <work>/walk --name <journey>-NN --session <journey>
python3 {walker} --session <journey> --stop
```

The steps file holds the steps taken so far, the last one being the one to take now
(`{{"do": "click", "target": "<words on the control>"}}`, `type`, `press`, `back`). Each step
tells you what changed on the page and which controls are there. Work in `{work}`.

Go through every screen, tab, menu item, panel, dialog and state you can reach. Try every
control. Note what is shown before and after, and what is refused or switched off and why.

Write `{out}`, one JSON object:

```json
{{
  "screens": [{{"id": "s01", "name": "<what a person would call it>", "how_reached": "<the steps>"}}],
  "behaviours": [{{
    "id": "b001",
    "screen": "s01",
    "kind": "view | action | rule | state",
    "does": "<what the person does, or 'opens the screen'>",
    "sees": "<what they then see or what happens, in plain words>",
    "quote": "<exact words on the screen that show it>",
    "capture": "<the walk capture name that shows it>"
  }}],
  "not_reached": [{{"what": "<a part you could not reach>", "why": "<why>"}}]
}}
```

One behaviour is one thing a person can do or see that a rebuild of this product must also
offer. Rules count (a button switched off until something is done; what an answer changes).
Layout, colour and the sample data's exact values do not; the shape of the data does (each item
shows its kind, its status, its date). Be complete: a behaviour you leave out cannot be tested.
Every behaviour needs a quote that is on the screen. Use plain words. Do not explain how the
product works inside; say only what a person does and sees.

Your last message is only: `inventory written: <n> behaviours on <m> screens`.
