# Feature: Specify from a video

## What it does
What a video shows is captured, so intents can trace to moments in it.

Status: to build.

## Agent intent (ICE)
- Goal: What a video shows is captured, so intents can trace to moments in it.
- Limit: The video is kept as given.
- Fails if: Its contents are guessed, or a part that matters wasn't read.
- Context: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the video, any notes given with it.
- Checked by: Validate the attribution.
