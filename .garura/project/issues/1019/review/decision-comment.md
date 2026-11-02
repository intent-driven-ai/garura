**Reviewer verdict (human, gate on): approve**

The product owner typed "approved" after seeing round 2's findings. The gate is on because this repo's settings still name the old play, `review-change` (#772). Review of #1019, round 2, after the changes the product owner asked for. Nothing blocks the merge.

Checks run
- Tests: `remove-model-part` 63, `author-intent-page` 50, `remove-plan` 31, all passing; install 76 passing in round 1, its code unchanged since.
- Acceptance check: 87 of 87 pass.
- Component linter, installed tool, source layout: 37 problems, none in a changed file (there before).
- Standards scan: 0 findings. Its path rules read scripts under `core/components` as prose, so it did not look inside them (#890).

Open findings (0 P1, 1 P2, 6 P3, 7 P4), each with its basis in `review/findings.yaml`
- Carried to the reorganisation change: MEM-5 and F1 (a decision record for the two spine writers named in `direct-model-write.md`), F8, MEM-6 and MEM-7 (that rule's wording), F6 (the new intents' Touches lists).
- Left by the product owner's decision: MEM-1 to MEM-4 (the verb and Phoenix memory, because the verbs change next) and F3 (the Serves line stays plain text for now).
- Left as they are: F4, F5, F7.
