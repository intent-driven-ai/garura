# Approval, #1021's last model work

- 2026-11-11, the product owner saw the plan in .garura/project/issues/1021/context/cleanup/plan.md (eight steps: 25 named lines on 17 pages, the repoints and the slice removed, the five old intent pages removed, the five features moved into Turn intents into agent work and Write the evals, the two emptied capabilities merged, BI-1's and BI-3's Touches, the seven plans deleted with plans/788/ and its evals, and the checks). He replied: "approved"
- Landing #1021 through the change plays is asked for separately.

## Run order changed (2026-11-11), same approved meaning

Step 3 (remove the five old intent pages) was refused, nothing written: the "Build a plan" page
(cap-718) still named bi-788 on line 15. That page is deleted by the merge in step 5, so the steps run
as 1, 2, 4, 5, 3, 6, 7. Every request is unchanged; only the order moved. Steps 1 and 2 ran first, as planned.

## One more line, to break a loop of refusals (2026-11-11), same approved result

The new order was refused too, at the move: the old BI-788 page still linked to fn-728's old page. The
three steps block each other: removing the intents waits on the "Build a plan" page (gone only at the
merge); the move waits on the BI-788 page (gone only with the intents); the merge waits on the BI-788 page
and on the move. So one more named line runs first (lines-request-2.json): on the "Build a plan" page,
"added by /shape-slice for bi-788." becomes "added by /shape-slice.", the pattern already approved for the
domain page. That page is deleted at the merge, so the model ends exactly as approved. The steps then run
in the plan's own order: 3, 4, 5, 6, 7.
