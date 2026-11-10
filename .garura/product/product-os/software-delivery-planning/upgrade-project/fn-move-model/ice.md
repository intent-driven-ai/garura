## Intent
- Goal: When the new version reads the product model in a new shape, the upgrade shows each key, file name, folder and heading of the project's model it would move, and on the person's yes moves them to the new version's shape as one step that puts everything back when a step fails, with every page's words, every id and every link as they were; on a no, the model stays as it was and the move is named as owed.
- Limit: Only the model's shape moves; the words on its pages, its ids, its business intents and its links never change.
- Limit: Nothing in the model moves before the person has seen each change and said yes.
- Limit: Nothing outside the project's model is changed, and a model folder outside the project is refused.
- Fails if: After the move, a page's words, an id, a business intent or a link is different.
- Fails if: The model moved with no yes on record, or a change was made that the list shown first did not name.
- Fails if: A move that failed part way left the model partly in each shape, or a no left no record of the move owed.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the project's product model and the shape it is in, the moves from that shape to the new version's, the release notes that name each move, and whether the project is a git repository.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who decides whether the model moves.
- Scope: In: showing each key, file, folder and heading to move, the person's yes or no, the move as one step, and the move owed on a no. Out: the model's shape itself and how it is versioned, writing what the model says, the list and the report themselves, and the release notes.

## Expectation
- Scenario: A shop's checkout project made its model before the Feature rename. On the upgrade, the list shows its features folder, its feature pages and their headings to move. The product owner says yes. Afterwards the model is in the new shape, every page says what it said, every id is as it was, and the move is one commit of its own. A clinic's booking app with the same model says no; its model is as it was, the report names the move as owed, and the scripts that read the model name the move it can run later.
- Done means: Someone other than the one who ran the upgrade compares the model's pages, ids and links before and after the move, and finds only keys, file names, folders and headings changed, every one of them on the list shown first, and the yes on record.
