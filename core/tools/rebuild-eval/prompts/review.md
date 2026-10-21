# Review: are the intents and the model right for this product?

- `{brief}` — business intents (`intents/`) and a product model (a domain, its capabilities,
  their functionalities) written from a prototype.
- `{inventory}` — what the prototype offers: its screens and every behaviour a person can do
  and see there, with quotes.

Judge the brief against the product the inventory describes. Be strict and plain.

**Each business intent** — pass or fail on each test, with one line of why:

- `need_the_product_offers` — it names a need the product meets for its user, which a screen
  or area of the inventory serves (say which). Not the process behind the screens.
- `outcome` — it says what the person can do or see when the need is met.
- `asked_by_persona` — "asked by" is a persona with its role in the domain (for example "a
  product owner who defines what a product must do"), not a step in a process.
- `why_business` — "why" is the business reason the product is needed.
- `proof_measurable` — "proof it is met" is a result someone can measure, with a number or a
  clear yes/no.
- `product_words` — it is written in the words of the product's domain, as its users talk,
  not in the words of the machinery that made the brief.

**The domain** — is it a domain the world recognises (as an industry or a known product
category would name it)? Give that name. Do its sources support it? If it is a name made up
for this product, say `recognised: false`. A domain is a field the industry identifies itself
with — a product category or market vendors, analysts and buyers name; a principle, practice,
regulation or quality (for example human oversight) is not a domain. The brief may hold several
domains: judge each one.

**Each capability** — `ok` (a known capability of the domain, or one the inventory clearly
shows), `invented` (neither), or `misplaced` (it belongs to another domain).

**Each functionality** — list the inventory behaviours it covers. `ok` when it covers at least
one; `invented` when it covers none; `panel` when it is only one part of a screen made into a
functionality of its own. Then list the inventory behaviours no functionality covers.

Write `{out}`, one JSON object:

```json
{{
  "intents": [{{"file": "intents/<f>.md", "tests": {{"need_the_product_offers": "pass", "outcome": "pass",
               "asked_by_persona": "fail", "why_business": "pass", "proof_measurable": "fail",
               "product_words": "pass"}}, "why": {{"<test>": "<one line>"}}}}],
  "domains": [{{"file": "<path>", "recognised": false, "known_as": "<the name the industry uses>",
               "sources_support": false, "why": "<one line>"}}],
  "capabilities": [{{"file": "<path>", "verdict": "ok | invented | misplaced", "why": "<one line>"}}],
  "functionalities": [{{"file": "<path>", "behaviours": ["b001"], "verdict": "ok | invented | panel",
                       "why": "<one line>"}}],
  "missed_behaviours": ["b0xx"]
}}
```

Your last message is only: `review written`.
