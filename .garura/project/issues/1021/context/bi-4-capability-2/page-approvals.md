# BI-4 capability 2: the product owner's words and approvals

Business intent BI-4 (Code → Validation). Capability 2: Test security, against the product profile's security level.
His words are kept as given; quotes on pages tidy only the spelling.

## 2026-11-09

- On BI-4's list: "this is code to validate hence this is about testing and it needs to test functionality which are product evals, but it also needs to handle other forms of testing i.e. seecurity and performance and assessibility, ux (responsive) hence all 5 needs to be handled"
- On the list of six and its leans, recorded in .garura/project/issues/1021/context/capabilities.md (Code → Validation): "yes, record it and draft the first one"
- After capability 1 was written: "commit and cp"
- Earlier, on Deployment design (2026-11-07): "Production never gets set on this, not in the path of the project. We are never touching production."
- On the capability page and its ICE (Test security), with the leans the page carries (the review of each change with its security rules stays with Check the code against its standards; the code at rest and the running build, the running build only in the testing environment; the profile's security level and pass bar with each capability's security need, and a secret's value tested for on every product; a finding goes to the developer only when its way back is a code change the builder controls, else to the product owner, and when in doubt a person; the builder knows the level, never the tests, results or verdict; a test takes the testing environment's secret at run time and writes its value nowhere), what a security test must cover left open, and the product owner as the one who gets a finding that changes the architecture: "approved"
- On the feature Test the built code, its settings and its libraries for security weaknesses (fn-test-code-security), its page and its ICE: "approved"
- On the feature Test the running build for security in the testing environment (fn-test-running-security), its page and its ICE: "approved"
- On the feature Give the security verdict, and send each finding to the developer or to a person (fn-send-security-findings), its page and its ICE, with the line on a finding that changes the architecture, the deployment design or an environment settled as the product owner's: "approved"
- On the feature Test security again as the product changes (fn-retest-security), its page and its ICE, and on writing the capability into the model: "approved"
