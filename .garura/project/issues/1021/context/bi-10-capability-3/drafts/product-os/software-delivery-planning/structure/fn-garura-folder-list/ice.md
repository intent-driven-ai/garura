## Intent
- Goal: A project's `.garura/` holds only what one written list names: the settings file, `engine-state.json`, Garura memory and the laid tools in `core/`; the product model in `product/`; short-term memory, with its five keys for each issue, and the plans in `project/`; and the install record, the defect reports and what people gave at the top. The three written layouts say the same, and a check names every folder or file the list does not hold, so a person and an agent find each thing where the list says.
- Limit: A new folder joins the list only by a decision, and every written layout gains it in the same change.
- Limit: In Garura's own repository, a change to the list or to the folder is built in the install's source, never by hand in the installed copy.
- Limit: What the product model, Garura memory and the settings hold, which parts a review reads, and the way past a gate stay with their owners.
- Fails if: `.garura/` holds a folder or file the list does not name, and the check does not name it.
- Fails if: The written layouts disagree on a folder, or a folder the settings name is on none of them.
- Fails if: A rule names a check of the list that does not exist.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the decision records that set and change the list; the docs and the glossary that draw it; the settings that name its folders; a listing of `.garura/` as it is and what git ignores in it; the scripts that read or write each file in it; and the rules that name a check of the list.
- Never read: any memory file by its path, any ICE page, and any file under a plan's evals folder.
- Persona: the technical lead, who keeps the layout of `.garura/`; and the developer, a person or an AI agent who builds the code, who adds a play that writes into it.
- Scope: In: the one written list of `.garura/`, the layouts that draw it, and the check of the folder against it. Out: what the product model holds, what may enter Garura memory, where other settings files go, which parts a review reads, keeping each run's records with its issue, and the way past the check.

## Expectation
- Scenario: In a clinic's booking app, a play starts to write its records in a new folder at the top of `.garura/`; the check names the folder, and that the list does not hold it. In a harness repository like Garura's, the plans folder joins all three written layouts, and the check passes on it and names the old global ledger, which nothing reads.
- Done means: Someone other than the one who wrote the list reads the three written layouts and lists `.garura/`, and finds one list that the three agree on, every folder and file on the disk either on the list or named by the check, and the check's report the same as what they found.
