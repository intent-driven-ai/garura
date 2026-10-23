# Need — #826

## In the product owner's words

"idd principles need to hold true. what changes does it bring and what it breaks. we cant break the principle"

## The need

Ontology v9 breaks the IDD routing table (`docs/philosophy/idd-principles.md`, "How ICE routes under the barrier" and "The Routing Table"). The table says: the builder never receives failure conditions, recovery conditions or the evals; the eval author receives all of ICE; the validator receives the recovery conditions.

In v9 a Story's scope of work says "what must never happen", and the builder reads the Story. So failure conditions reach the builder. v9 also gives the recovery conditions no place.

The fix (agreed direction, #826):
- The Story keeps only the goal, the constraints and the expectations (success scenarios). It never carries failure conditions or recovery conditions.
- The plan play writes each story's failure conditions and recovery conditions into the slice's hidden eval folder `.garura/project/plans/<plan-id>/evals/<slice>/`. A builder never reads that folder.
- The eval play reads the epic, the stories, that hidden file and the usage guide. So the eval gets all of the ICE, as the plan play interpreted it once. It still never reads the ICE directly.
- The routing table stays true, word for word.

Issue: #826 (plan 788, under #794).

## Sources

- docs/philosophy/idd-principles.md
- core/components/memory/standards/schemas/product-os/ontology.md (v9)
- .garura/project/issues/816/context/edit-ontology/draft-questions.md (Q28, Q29, Q31 as agreed)

## Review round 1 (PR #827)

The product owner, at the review: "fix the findinga and yes add encrypt". The fixes, in this change:
- M2: the ICE section says "only a Story reads it"; the plan play also reads it, when it makes a Story and the hidden file. (This adds ICE to Touches.)
- M4: the recovery rule covers stories too (`standards/rules/expectation-generation.md`, new section).
- M5: the running eval reads only the recovery parts of the hidden file.
- M6: the Story says "limits" where the ICE says "limits" (one word for one thing).
- Two old lines carry a real first name; it becomes "the product owner".

## Touches

Story
Slice
Plan
ICE
