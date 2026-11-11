Read on each tool's own pages on 2026-11-10, for BI-9 (Orchestration). Each fact names the page it came from.

# An ADR in the same change as its work

- Shopware's own rule: every code change needed to carry out the decision is added to the same merge request as the ADR, and the merge request is labelled ADR. https://developer.shopware.com/docs/resources/references/adr/2020-06-25-implement-architecture-decision-records.html
- UK Government Digital Service: decisions are kept in version control beside the application; on GitHub a proposed ADR can be a draft pull request, and the pull request's status stands for the decision's status until it is accepted. https://gds-way.digital.cabinet-office.gov.uk/standards/architecture-decisions.html
- AWS Prescriptive Guidance: an ADR starts Proposed, is reviewed and becomes Accepted or Rejected; an accepted ADR is not changed, and a new ADR supersedes it; a code reviewer checks a change against the ADRs and links the one it breaks. https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html