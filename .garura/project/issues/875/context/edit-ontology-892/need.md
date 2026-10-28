# Need — #892 (under #875, plan 788)

The product owner, 2026-10-25, on the PR #891 review: "fix mediums", "go for those together as chore".

Review finding MEM-2: the ontology's Q20 answer ("Given a tracker issue, which kind is it?") mixes two ideas. It says the issue type names the kind, and also that the issue is found by its plan file's `represents` mark. For an issue outside a plan file it is unclear which one answers the question.

The fix the product owner saw before saying go: the issue type names the kind; the `represents` mark is how a play finds which Epic stands for a slice and which Story for a feature. Proposed Answered-by line:

> the issue type names the kind: type Epic is an Epic and type Story is a Story, each with no label (rules R1, R2); label `product` is a Business Intent; label `work-item` with its kind is a Spike, a Chore or a Bug. Which Epic stands for a slice, and which Story for a feature, is found by the plan file's `represents` mark, never by type or title (rule R3).

Only Q20's Answered-by line changes. No kind, property, link or rule changes. The ontology stays at version 12 (this lands in the same pull request as v12, #891), and the v12 log line stays as written.

Issue: #892. Branch: plan/788/875-epic-issue-type (already open; lands with #875).

## Touches
None. Q20 is a question, not a kind. (The change check compares against the plan base, v11, so the Epic and Story changes of v12 in the same pull request show there too.)
