# ICE Rubric

What a good ICE looks like. It holds for every capability and feature, and for a thin ICE as much as a full one. A person, a play or a judge reads a page against this table.

| Part | Rule |
|------|------|
| **Goal** | Exactly one. This is not negotiable. Two goals mean two parts: split the part, or move one goal down to a feature. |
| **Limit** | At least one. A thin ICE has up to three. |
| **Fails if** | At least one, for what matters most. A thin ICE has up to three. |
| **Context** | Says where the context is gathered from, in the fixed order below, and what to look for. |
| **Checked by** | At least one way to prove the goal, by someone other than the one who did the work. |

## Context

Every Context line gathers from the memory layer, in this order:

1. The project's existing memory and its existing implementation.
2. Garura memory.
3. Phoenix memory.
4. If none of them answers, research it and raise a memory update for a person to approve.

Then it names what this part looks for.

## What goes wrong

- **Two goals in one line.** "A person can upload a file and share it" is two goals, unless sharing is what the upload is for.
- **A check by the doer.** The one who did the work reviews it first, but that review is never the check.
- **A plan named on the page.** Plans sit outside the model, so no line names a particular plan.

## Examples

- **Clinic, feature.** Goal: A patient gets a reminder before each visit. Limit: It never shares what the visit is for. Fails if: A reminder goes out after the visit. Checked by: A test visit tomorrow gets one reminder today.
- **Shop, capability.** Goal: A shopper can check out a cart. Limit: It never stores card numbers. Fails if: An order is taken and no payment is. Checked by: A test order shows up paid.
- **Bank, feature.** Goal: An applicant can upload their accounts. Limit: Only the applicant and the reviewer can read them. Fails if: A file is lost with no error. Checked by: An uploaded file can be read back unchanged.