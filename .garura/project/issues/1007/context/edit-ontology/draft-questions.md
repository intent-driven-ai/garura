# Questions the ontology must answer — #1007 (an item's status in a plan follows its own issue)

You decide whether the list of questions stays as it is for this change. If you say yes, the
next step changes only the one rule in the Plan kind. If you name a question to add or change,
this step is done again with your words.

**No question changes.**

Why: no question asks who sets the status of an item in a plan. The two questions on status ask
about the plan's own Status (Q41) and its Direction (Q42). A person still sets both, and nothing
works them out, so their words and answers stay. The two questions that list "each work item's
state" (Q7 and Q23) still get the same answer: the plan file holds that state. Only the rule on
who may change it is new: an item's status now follows its own issue (closed as completed is
Done, closed as not planned is Dropped), and there are still no roll-ups.
