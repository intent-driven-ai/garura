# Functionality: Rebuild the product model as an ontology

## What it does
The ontology (the product model rules) defines every kind a plan uses — Business Intent, Capability, Functionality, Work and Plan — with needs, identified by, loose domains and the ready rule, and examples from more than one domain.

## Agent intent (ICE)
- Goal: every kind a plan uses is defined in the ontology, with examples from more than one domain.
- Limit: one kind at a time, through build-product-ontology, with Kapil.
- Fails if: a kind a plan uses is still under "Not yet defined".
- Checked by: check_ontology.py passes, and Q7 is marked answered.
