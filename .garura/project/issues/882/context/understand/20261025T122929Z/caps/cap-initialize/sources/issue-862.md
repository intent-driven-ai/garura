# #862 A project gets only the memory and the review rules that fit it: initialize asks after the install

**Hypothesis:** We believe a project needs only the part of Phoenix memory that fits it. Today an install copies all of the memory, and every review runs every rule, so a project that has no database, no front end or no permissions still gets those standards and those findings. We believe that when a project answers a short set of questions after the install, it gets the memory and the review rules that fit it, and nothing else.

**We will know it is true when:**
- after the install, one play (`initialize`) asks the person a short set of questions built from Phoenix memory: the domains, the kinds of features, the technology standards, the tools and frameworks, the surfaces (web, mobile, CLI, API), and whether there is a database, personal data, permissions or a running service;
- each question has choices and a proposed answer with its source;
- the answers set up the project's Garura memory from only the part of Phoenix memory it needs, and the profile records them;
- a review in that project runs only the rule groups that fit it (for Garura itself: no front end, no back-end service, no database, no running service), and the review record names the groups it skipped;
- a project can run `initialize` again when it changes.

**Rules**
1. The install brings no memory of its own; `initialize` builds the project's memory after it (recorded with the #653 plan, ADR 038, ADR 039).
2. Every part reads memory only through the memory tool.
3. The answers are the person's; a proposed answer always names its source.

**Out of scope:**
- Moving the memory tool's home to Phoenix, and removing `~/.garura/core/memory`: later, once the memory tool is fully live.
- Installed parts reading the source tree (#860).

**Identified by:** #860 (the review of PR #858 ran database, permission and front-end rules on Garura's own tool files).

Recorded with the product owner, 2026-10-25.

