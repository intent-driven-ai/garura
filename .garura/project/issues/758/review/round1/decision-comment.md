Reject (human verdict, by the product owner).

The script recommended approve (no P1). The product owner rejected it to fix three points on this branch:

1. **The ready rule for the three parts.** The product owner's words: "ice cant start unless i.c.e are all provided. it can start even if its thin or wrong. that aka correctness and richness is what product owners function and responsibility." So: an ICE with any of Intent, Context or Expectation missing is **not ready**. An ICE with all three present can start, however thin; its correctness and richness are the product owner's call, not the check's.
2. Add pointers to the issues that build what v6 names: #759 (linter), #760 (ready check), #761 (plays write ICE nodes), #765 (move Garura's model).
3. Record in the run's locked model that the product owner later set capability → domain to at most one.

**Next:** fix on this branch, re-raise, review again.
