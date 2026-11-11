# ICE Rubric

What a good ICE looks like. It holds for every capability and feature, and for a thin ICE as much as a full one. A person, a play or a judge reads an ICE against this table.

An ICE is not a section of a capability or feature page. It has its own page, `ice.md`, in the folder of its part, and its own entry in the model's index. The page has three sections, in this order: Intent, Context and Expectation. The ontology's ICE kind holds the full shape.

| Section | Line | Rule |
|---------|------|------|
| **Intent** | **Goal** | Exactly one. This is not negotiable. Two goals mean two parts: split the part, or move one goal down to a feature. |
| | **Limit** | At least one. A thin ICE has up to three. |
| | **Fails if** | At least one, for what matters most. A thin ICE has up to three. |
| **Context** | **Read** | Says where the context is gathered from, in the fixed order below, and what to look for. |
| | **Never read** | What this part must not read, once that is known. |
| | **Persona** | Who the work is for, once that is known. |
| | **Scope** | What is in and what is out, once that is known. |
| **Expectation** | **Scenario** | Something that can be tried, with a result that can be seen, once that is known. |
| | **Done means** | At least one way to prove the goal, by someone other than the one who did the work. |
| | **Quality need** | A concrete target, when the part has one. |

## Read

Every Read line gathers from the memory layer, in this order:

1. The project's existing memory and its existing implementation.
2. Garura memory.
3. Phoenix memory.
4. If none of them answers, research it and raise a memory update for a person to approve.

Then it names what this part looks for.

## Thin

An ICE is thin because it carries the thin mark, not because it has few lines. The mark is kept in two places that agree: a line that starts "Thin:" at the top of its page, before Intent, and `thin: true` in its index entry.

## What goes wrong

- **Two goals in one line.** "A person can upload a file and share it" is two goals, unless sharing is what the upload is for.
- **A check by the doer.** The one who did the work reviews it first, but that review is never the proof.
- **A plan named on the page.** Plans sit outside the model, so no line names a particular plan.
- **The ICE kept on the part's page.** A person reading the part's page learns what the part is. The ICE says what an agent must make true there, so it has a page of its own.

## Examples

Each Read line below starts with the fixed order above, and shows only what the part looks for.

**Clinic, feature**
- Intent. Goal: A patient gets a reminder before each visit. Limit: It never shares what the visit is for. Fails if: A reminder goes out after the visit.
- Context. Read: the clinic's reminder rules. Persona: a patient on a phone. Scope: text reminders are in; booking a visit is out.
- Expectation. Scenario: A test visit tomorrow gets one reminder today. Done means: A tester who did not build it sees that reminder arrive.

**Shop, capability**
- Intent. Goal: A shopper can check out a cart. Limit: It never stores card numbers. Fails if: An order is taken and no payment is.
- Context. Read: the payment rules. Persona: a shopper with no account. Scope: card and wallet are in; returns are out.
- Expectation. Scenario: A test order goes through by card. Done means: The test order shows up paid in the payment provider's records. Quality need: The payment page loads in under one second.

**Bank, feature**
- Intent. Goal: An applicant can upload their accounts. Limit: Only the applicant and the reviewer can read them. Fails if: A file is lost with no error.
- Context. Read: the bank's rules for keeping documents. Never read: another applicant's files. Persona: a small-business owner applying for a loan. Scope: PDF uploads are in; deciding the loan is out.
- Expectation. Scenario: An applicant uploads one PDF. Done means: A reviewer reads the file back, unchanged.
