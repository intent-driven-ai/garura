# Draft questions — #758 (plan #756), stage scope

The need: the agent intent (ICE) becomes its own kind of node. Each ICE has its own page and its own spine entry. There is one ICE for each pair of one business intent and one capability or functionality. An ICE is built from one business intent and is for one capability or functionality. A business intent connects to its ICE nodes, not to capabilities.

The ontology has Q1 to Q7. The questions below are new. Each question says which existing question it touches. The product owner confirms or changes each question, one at a time.

- **Q8** — Given a capability or functionality, which ICE are for it, and which business intent is each ICE built from?
  **Example:** A bank has the capability "Credit decision". The lending manager wants "Small businesses get a loan decision in one day". The compliance officer wants "Every declined loan shows the reason to the applicant". The lending manager asks: "Which agent intents are on Credit decision, and whose intent is each one?" The answer is two ICE, one for each business intent.
  **Touches:** Q7 (the plan now reaches a node through its ICE). It changes the ICE rule "one part of the product has one ICE": a part now has one ICE for each business intent it serves.
  **Status:** not yet

- **Q9** — Given a business intent, which ICE were built from it, and which capability or functionality is each one for?
  **Example:** An online shop has the intent "Shoppers can check out without making an account". The head of growth asks: "Which agent intents came from my intent?" The answer is one ICE for the capability Checkout and one ICE for the functionality Guest checkout.
  **Touches:** Q2 (the parts an intent touches are now found through its ICE) and Q7 (its plan). It changes the Business Intent link: the intent connects to ICE nodes, not to capabilities.
  **Status:** not yet

- **Q10** — When two ICE are for the same capability or functionality, do their goals or limits go against each other, and does a person see that before work starts?
  **Example:** A clinic has the functionality "Send a reminder". One ICE, from "Patients miss fewer appointments", has the goal "send an SMS the day before". A second ICE, from "We contact patients only with their consent", has the limit "send no message to a patient who did not agree". The practice manager asks: "Do these two agree, or must I choose?"
  **Touches:** Q3 (today a clash is found between business intents; with this need it is also found between two ICE on one part).
  **Status:** not yet

- **Q11** — Given an ICE, what does the agent get told when it gathers context: what to read, what never to read, which persona it works for, and what is in and out of scope?
  **Example:** A bank's ICE for "Upload documents" says: read the loan application rules; never read other customers' files; work for the small-business applicant; ID and accounts are in scope, tax returns are out. The product owner asks: "What will the agent read for this, and what is it kept away from?"
  **Touches:** none directly. It is new: today Context is one line inside a page; here it is the set of rules handed to the context sub-agent.
  **Status:** not yet

- **Q12** — Given an ICE, how will we know the agent's work for it is done: which scenarios it must pass, what "done" means, and which quality needs it must meet?
  **Example:** An online shop's ICE for "Guest checkout" says: a guest pays by card on mobile in under two minutes; done means that scenario and a wallet scenario pass; the page loads in under one second. The head of growth asks: "When can I call this part finished?"
  **Touches:** Q6 (Q6 asks if the business intent is met by its proof; Q12 asks if one ICE is done by its expectation; an ICE can be done while its intent is not yet met).
  **Status:** not yet

- **Q13** — Given an ICE, is it ready for an agent to work on, and if not, what is missing?
  **Example:** A clinic's ICE for "Booking" is built from "Patients book their own appointments online". That intent is still proposed, so the ICE is not ready. The practice manager asks: "Why has no work started on booking?" The answer: the intent is not confirmed yet.
  **Touches:** Q1 and Q4 (work now carries one ICE, so the work an intent needs and the work agents finished alone are found through its ICE). It moves the ready rule from the node to the ICE.
  **Status:** not yet

## Left out, on purpose

These look like questions but are not. They go to later steps.

- "Can a person read the ICE page with no other page open?" — a quality bar. It becomes a rule at step 6.
- "Must an ICE have all three parts before work starts?" — a design choice about the kind. It is worked out at step 6 from the sources and shown to the product owner.
- "Where does the ICE page live, and what does its spine entry hold?" — a design choice. It is decided at steps 4 and 5.
