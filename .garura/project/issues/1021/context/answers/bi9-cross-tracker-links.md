Read on each tool's own pages on 2026-11-10, for BI-9 (Orchestration). Each fact names the page it came from.

# Linking work across trackers

- GitHub sub-issues: a parent issue can take an existing issue from another repository as a sub-issue; a parent holds up to 100 sub-issues, nested up to eight levels; projects can group and filter by parent and show sub-issue progress. The docs do not say whether the other repository may be in another organization. https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues
- Jira links a work item to GitHub through its key (for example JRA-123, in capitals) written in a branch name, a commit message or a pull request title; Jira then shows the branches, commits, pull requests and deployments on the work item. https://support.atlassian.com/jira-software-cloud/docs/reference-issues-in-your-development-work/ and https://support.atlassian.com/jira-cloud-administration/docs/use-the-github-for-jira-app/

So there are two kinds of link: a real parent and child link inside one platform, and a key written in the work that an integration reads.