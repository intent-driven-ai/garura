# Need (#846, plan 788)

The product owner's words, from the /shape-slice run for #788 (#844, decisions 6 and 7):

- "No, the shape plan is only going to write a plan. It cannot write failure and recovery conditions. That has to be part of the shape slice. The shape slice has to do that. The plan only builds a plan, and then set up your stories, epics, and whatnot. That responsibility is clear."
- "option C: Shapeslice writes the entry from whatever I suggest. … Setting up a new capability should mean that, at a bare minimum, a thin ICE has to be proposed by Shapeslice itself… the user is not forced to change… We should warn them that they should go back, but we should not force them to go back."
- "thin ICE - makes sense even in real world. when working on thin ice, you can fall into deep water and die. this is the warning :) not literally though"

What changes, in plain words:
1. /shape-slice writes the slice's hidden file (failure-and-recovery.md) when it shapes the slice: one entry for each feature of the slice, from that feature's ICE and its capability's ICE, with exactly one recovery condition for each "Fails if" line.
2. The plan play (/shape-plan) writes only the plan file, the epic and the stories. It writes nothing in the evals folder. The epic keeps the map from each feature to its story, so the eval play can join the hidden file's entries to the stories.
3. When the slice needs a capability or a feature that has no ICE, /shape-slice proposes a thin ICE itself (a goal, its limits and a few "Fails if" lines), marks it as thin, and warns the person; it never forces them back to a discovery play.

Issue: #846 (sub-issue of #788). Closes finding M1 on PR #845.

## Touches
Slice
Plan
Epic
Story
ICE
