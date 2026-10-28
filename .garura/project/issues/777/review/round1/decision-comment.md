Reject (human verdict, by the product owner).

The script recommended approve (no P1 finding). The product owner rejected it so that three findings are fixed before the merge:

1. P2: `product-os-keeper` does not list `author-product-ontology` among its skills, but the new play tells that agent to run it. The first real run (#758) could fail.
2. P3: the skill's Input table does not name the fields the play sends (`stage`, `change`, `problems`).
3. P3: `standards/rules/pipeline-position.md` says meta plays have no position; `edit-ontology` has position both.

**Next:** fix the three findings on this branch and raise the change again.
