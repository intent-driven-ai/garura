# Functionality: "Needs" and "identified by" link capabilities and functionalities

## What it does
a capability or functionality can need, and be identified by, another capability or functionality — any mix. Never on work (feature, story, spike, chore, bug). The spine field is still `depends_on`; renaming it to `needs` across the files that use it (53 today) is part of this story.

## Agent intent (ICE)
- Goal: Anyone can see what a node needs and what led us to find it.
- Limit: Links sit only on capabilities and functionalities.
- Fails if: a need or identified-by link points at work, or at a node that does not exist.
- Checked by: the spine linter rejects a link to a story and accepts capability → functionality.
