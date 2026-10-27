# ADR 048, Decision 1 (committed on plan/788/base: docs/adr/048-the-product-model-and-the-work-are-two-layers.md)


- The **product layer** is the model: Business Intent, Source, Domain, Capability (with its ICE), Feature (with its ICE; the old Functionality), Slice and ICE.
- The **work layer** is tracker issues labelled `work-item`: Epic, Story, Spike, Chore and Bug.
- Only the Business Intent is a product-layer tracker issue, labelled `product`. Domain, Capability, Feature, Slice, Source and ICE are never tracker issues. In the tracker, a Story stands for a Feature and an Epic stands for a Slice.
- The **Plan** is a file. It is the thread between the two layers.

