# Feature: Specify intents

## What it does
What a person gives becomes the right business intents, at the depth the product owner chooses, each confirmed by them.

Status: built, except reading existing intents and writing attribution.

## Agent intent (ICE)
- Goal: What a person gives becomes the right business intents, at the depth the product owner chooses, each confirmed by them.
- Limit: One need is one intent, and it can hold several features. Transitional parts aren't intents.
- Limit: It writes business intents and their sources only.
- Fails if: An intent is confirmed without the person's typed word, or a part that matters wasn't considered.
- Context: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: what was given, the existing intents, the depth preference.
- Checked by: A person sees every part considered, each as an intent or with the reason it isn't one.
