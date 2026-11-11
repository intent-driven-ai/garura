## Intent
- Goal: Every kind of part, each tool, the memory source and the one settings file has one known place in Garura's source: the parts in their kind's folder under `core/components/`, each whole with its scripts and reference files inside it; the blocks they share in their kind's `_shared/` folder; the tools in `core/tools/<name>/`; and the settings in `core/config.yaml`; each named in the settings and in one written layout, so a developer knows where a part goes and the install knows where to take it from.
- Limit: A change is made in the source; nothing in an installed copy is edited to make one.
- Limit: A part keeps its scripts and reference files inside its own folder, so it is laid whole.
- Limit: What each kind of part is, what each setting means and what the memory source holds stay with Standards, Settings and Memory.
- Fails if: A part, a tool or a shared block sits outside the folder of its kind, or a part's script sits outside the part's own folder.
- Fails if: The written layout leaves out a folder or a tool of the source, or names one that is not there.
- Fails if: A change is made by editing an installed copy instead of the source.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the folders under `core/` and what each holds; the settings that name the source folders; the install's adapters and what they take from each folder; the tools the install never lays; the written layouts in `CLAUDE.md` and the harness standard; and the issues that plan the tools component and the harness layout.
- Never read: any memory file by its path, and any ICE page.
- Persona: the developer, a person or an AI agent who builds the code, who adds a part or a tool to Garura's source; and the technical lead, who keeps the layout.
- Scope: In: the folder of each kind of part, the shared blocks, the tools folder, the memory source, the settings file's source, and the written layout of the source. Out: what each kind of part is and how it is built, what each setting means, what the memory source holds, where each part lands once installed, and building parts in a team's own repository.

## Expectation
- Scenario: In a harness repository like Garura's, a developer adds a skill and a tool. The skill goes in `core/components/skills/<name>/` with its script inside it, the tool goes in `core/tools/<name>/`, and the written layout names both. In a game studio's build harness that keeps the same layout, a new loop goes in the loops folder, and the steps every loop shares go in the loops' shared folder.
- Done means: Someone other than the one who added them lists the source folders and reads the written layout, and finds every part in its kind's folder with its scripts inside it, every tool in the tools folder, every folder and tool of the source named in the layout, and nothing in an installed copy edited by hand.
