# Compare: does the rebuild do what the prototype does?

Someone built a product from a written brief, without seeing the prototype. You check how much
of the prototype came back.

- `{inventory}` — every behaviour of the prototype: what a person does and sees, with the
  screen and the quote.
- `{rebuild}` — the rebuilt product. Use it with the walker, one step at a time:

  ```
  python3 {walker} --source {rebuild} --steps <work>/<journey>.steps.json \
      --out-dir <work>/walk --name <journey>-NN --session <journey>
  python3 {walker} --session <journey> --stop
  ```

  The steps file holds the steps so far, the last one being the one to take now
  (`{{"do": "click", "target": "<words on the control>"}}`, `type`, `press`, `back`). Work in
  `{work}`.
- `{brief}` — the brief it was built from. Read it only to say why something is missing.

For every behaviour in the inventory, try it on the rebuild. Words, layout and design may
differ; judge whether a person can do the same thing and see the same result.

- `met` — a person can do it and sees the same result.
- `partial` — it is there but a part is missing or works differently (say which part).
- `missing` — a person cannot do it or does not see it.

For each `partial` or `missing`, say whether the brief describes it: `in_brief: true` with the
file and its words, or `false`.

Then use the rebuild freely and list what it does that the prototype does not (`extras`), each
with `in_brief` the same way.

Write `{out}`, one JSON object:

```json
{{
  "results": [{{"id": "b001", "verdict": "met | partial | missing", "seen": "<what you saw>",
               "capture": "<walk capture name>", "in_brief": true, "brief_ref": "<file: words>",
               "why": "<for partial or missing: what differs>"}}],
  "extras": [{{"what": "<what the rebuild does>", "screen": "<where>", "in_brief": false,
              "brief_ref": null}}],
  "could_not_open": false
}}
```

Every inventory behaviour gets exactly one result. If the rebuild does not open, write
`"could_not_open": true` and no results.

Your last message is only: `compare written: <met> met, <partial> partial, <missing> missing, <extras> extras`.
