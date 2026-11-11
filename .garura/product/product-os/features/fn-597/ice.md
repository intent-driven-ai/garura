## Intent
- Goal: One written map, the ontology, says what a product is made of: each kind with what it is, who reads it, where it lives, its properties, its links, its rules and a real example; the questions it must answer, each with the kinds that answer it and its status; and a log line for each version; it reads valid by its check, and a person and an agent who read it use the same words for the same things.
- Limit: A rule of the map says what holds once the product is aligned; it never stops a write.
- Limit: Only a person confirms or drops a business intent; no rule gives that to an agent.
- Limit: A question is marked answered only when the kinds that answer it are defined.
- Limit: A feature never needs anything and is never identified by anything; its order of work comes from its parent capability and the slices.
- Fails if: The check finds a kind without its parts, a link to a kind that is not defined, or a question with no answer line or status.
- Fails if: A kind that a play writes or a question names is not defined in the map.
- Fails if: A version has no log line, or the map says something a later log line replaced.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the ontology with its front matter, questions, kinds, list of kinds not yet defined and log; the format the check holds; the check's last report; and the product owner's recorded answers on what the map says.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who agrees what the map says; the technical lead and the developer, a person or an AI agent who builds the code, who read a kind before they write or check a part of the model.
- Scope: In: the map's kinds, properties, links, rules, examples, questions, version and log, and its check. Out: changing the map, bringing it to projects, keeping the templates, the index's schema, the structure check and the glossary in step, the kinds for the profile and the decision, and the model's parts and checks.

## Expectation
- Scenario: In a clinic's booking app, an agent that writes the Reminders capability reads the Capability kind, writes the capability's ICE on its own page, and links the capability to the intent it serves, not to a feature. In a bank's payments service, the technical lead reads the Feature kind, keeps the order of Upload documents and Score the application in the slice, and finds no rule that lets one feature need the other.
- Done means: Someone other than the one who wrote the map runs its check and reads it, and finds it valid; finds each of the thirteen kinds with what it is, who reads it, where it lives, its properties, its links, its rules and an example; finds each of the 47 questions with the kinds that answer it and its status; and finds one dated log line for each version, up to the version in its front matter.
