# Functionality: Domains link to business intents and capabilities, outside the plan tree

## What it does
a domain lists the business intents and capabilities in it, so "which business intents serve the commerce domain?" can be answered. Domains are never in a plan or the tracker.

## Agent intent (ICE)
- Goal: A search by domain finds its business intents and capabilities.
- Limit: A domain never gets an issue and is never a level of a plan.
- Fails if: a domain appears in a plan file or the tracker.
- Checked by: a query for a domain in a test model lists its business intents and capabilities.
