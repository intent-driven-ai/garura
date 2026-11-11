## Intent
- Goal: Each type of issue Garura files has one agreed meaning in one line, with the tracker it lives in and how an issue of that type is marked, kept in one list that Initialize's brief shows word for word, so the person who sets up a project's tracker sees what each type is for before any type is made.
- Limit: The list says what each type means and how it is marked; it makes no type in a tracker and records no stand-in.
- Limit: A Business Intent never reads as a work item, and the tracker's type Feature never reads as a feature of the product model.
- Limit: A type is marked by the tracker's type field, never by a prefix in a title.
- Fails if: Initialize's brief shows a type Garura files with no meaning, or with words that are not the list's.
- Fails if: One type is given two meanings by the parts that say what it is.
- Fails if: A type Garura files is missing from the list, or is shown with the wrong tracker.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the kinds and how each shows in the tracker in the ontology, the table of the way of working on what each type is and when it is filed, the types Initialize lists, the types each of the project's trackers has with their own descriptions, and the settings that name the intents tracker and the work tracker.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who reads Initialize's brief and says yes before any type is made in the team's tracker.
- Scope: In: one meaning for each type Garura files, the tracker each lives in, how each is marked, and the list that Initialize's brief shows. Out: making the types and the stand-ins, marking each item when a play files it, what each kind is in the ontology, where a setting or a memory shelf lives, and the one tool that knows the tracker.

## Expectation
- Scenario: A school's team keeps its business intents in one tracker and its work in another. Initialize's brief lists Business Intent for the first, and Epic, Story, Bug, Chore and Spike for the second, each with its line from the list: a Bug is a defect under the story that brought it in, and a missing feature is a Story. On a bank's tracker with a fixed list of types, the brief shows the same lines beside each proposed stand-in.
- Done means: Someone other than the one who wrote the list compares Initialize's brief with the list, and finds each type Garura files there, with the list's words and with the tracker that holds it, and no type given a second meaning.
