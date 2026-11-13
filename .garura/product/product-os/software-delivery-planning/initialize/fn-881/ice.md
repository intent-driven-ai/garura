## Intent
- Goal: After Initialize has listed each needed type with its one-line meaning and said which are missing before it makes anything, each tracker the project uses holds each issue type Garura files there (Business Intent in the intents tracker; Epic, Story, Bug, Chore and Spike in the work tracker), made after the product owner's typed yes, or a stand-in the product owner said yes to, recorded in a mapping that the filing plays read once a later story of Initialize changes them, and each type still missing is named in the brief and the record.
- Limit: Make no type in the tracker and record no stand-in before the product owner's typed yes, and record every type it makes.
- Limit: Reach every tracker only through the adapter, GitHub first, with Jira and Linear through the same adapter and no change to a play; never remove or change a type the tracker already has.
- Fails if: a type is made in the tracker, or a stand-in written to the mapping, without the product owner's typed yes.
- Fails if: a type whose make failed is given a stand-in, or a type the tracker cannot make is left with no proposed stand-in.
- Fails if: a type that is missing and not mapped after the run is not named as still missing in the brief and the record, or the mapping names a type for it that the product owner never said yes to, so a filing play that reads the mapping could file the item as another type.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: which tracker the project's settings name for business intents and for work; the types each tracker has and whether it can make one, read through the adapter; each type's meaning as Track execution in the team's tracker gives it; and any mapping and record from an earlier run.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who says yes before anything is made in the team's tracker.
- Scope: In: reading the trackers and their types, the brief, making each missing type after the yes, proposing and recording stand-ins, the mapping and its record. Out: filing work items, changing the filing plays to read the mapping, what each type means and how a work item is marked, how Jira and Linear each make a type inside the adapter, and moving to another tracker on a later run.

## Expectation
- Scenario: A shop's GitHub organization has no Epic and no Spike type. Initialize's brief lists the six types with their meanings and marks Epic and Spike missing. The product owner types yes for Epic only. The Epic type is made and the record names it; Spike stays missing and unmapped, and the brief and the record name it as still missing. On a bank's tracker with a fixed list of types, each missing type gets a proposed stand-in, written to the mapping only on the yes.
- Done means: Someone other than the one who ran Initialize compares the tracker's type list and the mapping before and after with the replies, and finds nothing made or mapped without a typed yes, every type made named in the record, and every type still missing named as missing.
