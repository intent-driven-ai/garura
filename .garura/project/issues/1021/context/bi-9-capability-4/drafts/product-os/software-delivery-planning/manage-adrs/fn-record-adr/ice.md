## Intent
- Goal: From a decision brief that holds what is decided, why now, the options with why each lost, who decides and where, the decision is drafted as an ADR from the one template, with status proposed, every older ADR it supersedes or amends named with the part after each candidate was read, what it changes named by paths that exist, its effect on agent intent and its business-intent check; the draft passes the template's check before anyone is asked, and the run writes nothing but the record, the pointers and the index.
- Limit: No heading of the brief is filled in for the person, and no reason, option or consequence is made up.
- Limit: No record is written off the template, over a file that exists, or with a number that does not match its file name.
- Limit: A decision that would change a person's business intent is never written; it is shown to the person, by hand and inside a loop.
- Limit: Inside a loop, no issue and no branch are opened.
- Fails if: A record is written without a complete brief, or fails the template's check.
- Fails if: An older ADR the decision supersedes or amends is not named, or is named without its part, or a path under Affects does not exist.
- Fails if: An ADR that changes a person's business intent is written, or the run changes anything other than the record, its pointers, the index and its own records.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the decision brief and who gave it, the ADR template, the ADR folder and the candidates among its older ADRs, the files, rules, schemas, plays and agents the decision changes, the agent intents it changes, the business intent pages, whether the ADR folder and the product model have uncommitted changes, and, inside a loop, the loop's contract.
- Never read: any memory file by its path, and any ICE page.
- Persona: the technical lead or the developer, who records a decision on how the project is built.
- Scope: In: the brief, the template, the candidates and their judgment, what the decision affects, its effect on agent intent, its business-intent check, the draft and its checks, the clean start, writing the record and the scope check. Out: the person's accept, the forward pointers and the index, the points for the person who accepts, recording in a change already open, product decisions in the model, what a design choice says, and opening, reviewing and landing the change.

## Expectation
- Scenario: In a hospital's appointment system, the technical lead records the decision to send reminders through a queue. The candidates list three older ADRs; the agent reads them and names one as amended in the part that said reminders are sent at once, and the other two as not affected. Affects names the two services and the reminder rule, each by a path that exists, and the draft reads proposed and passes the template's check. In a mobile banking app the same day, a drafted decision that would drop a feature a person asked for stops before anything is written, and the product owner is shown the business intent it would change.
- Done means: Someone other than the one who drafted it reads the draft, its gathered context and the check report, and finds the brief complete, the one amended ADR named with its part, every path under Affects present in the repository, the status proposed, the template's check clean, and, for the bank, no ADR in the ADR folder and the business intent named in the run's report.
