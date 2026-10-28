# GitHub Verb Translations

Normative reference for the `platform-adapter` skill when `platform=github`. One section per verb — each section contains the exact `gh` command with parameter substitution tokens. The adapter reads this file to resolve the CLI command for the requested verb.

## view-pr

Fetch PR metadata (JSON):

```bash
gh pr view {pr_number} --json number,title,body,state,author,headRefName,baseRefName,files,changedFiles,commits,mergeable,url
```

Note: field `baseRefName` contains the target branch name.

## diff-pr

Fetch PR unified diff:

```bash
gh pr diff {pr_number}
```

## pr-files

List every changed file of a PR with its patch, one JSON object a line, page by page (the host lists up to 3000 files; `diff-pr` stops at 300):

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/files --paginate --jq '.[] | @json'
```

## compare-diff

The plain diff between two branches, three-dot (from where `head` left `base`), with no file limit. It is the first try for a PR whose one diff `diff-pr` refuses (over 300 files); `pr-files` (at most 3000 files) is the second. For a PR from a fork, `head` is `{owner}:{branch}`:

```bash
gh api repos/{owner}/{repo}/compare/{base}...{head} -H "Accept: application/vnd.github.diff"
```

## comment-pr

Post a comment on a PR:

```bash
gh pr comment {pr_number} --body "{body}"
```

## request-changes

Request changes on a PR (blocks merge):

```bash
gh pr review {pr_number} --request-changes --body "{body}"
```

## add-reviewer

Add a reviewer to a PR:

```bash
gh pr edit {pr_number} --add-reviewer {reviewer}
```

## create-pr

Create a pull request:

```bash
gh pr create \
  --title "{title}" \
  --body "{body}" \
  --base "{base}" \
  [--draft] \
  [--label "{label}"] \
  [--assignee "{assignee}"]
```

## merge-pr

Merge a pull request (uses repository default strategy):

```bash
gh pr merge {pr_number}
```

## view-issue

Fetch issue details (JSON):

```bash
gh issue view {issue_number} --json number,title,labels,state,body,url,closedAt,issueType,parent,subIssues,subIssuesSummary
```

Note: close date is in the `closedAt` field. The last four fields are the issue's place in the work tree: `issueType` (its type, e.g. Feature, Story), `parent` (the parent issue, or null), `subIssues` (its child issues, each with number, title and state) and `subIssuesSummary` (counts: total, completed, percent completed).

**Version gate.** The four tree fields need gh **2.94.0 or newer**; an older gh rejects the whole call, not just those fields. So check `gh --version` first. On an older gh, run the same command with the base fields only — `number,title,labels,state,body,url,closedAt` — and report `tree_available: false`, so callers know the type, parent and children are unknown, not empty. The bundled `platform_adapter.py` does exactly this.

## create-issue

Create a new issue:

```bash
gh issue create \
  --title "{title}" \
  --body "{body}" \
  --label "{labels}" \
  --assignee "@me"
```

## list-issues

List open issues matching a search query:

```bash
gh issue list \
  --state {state} \
  --search "{query}" \
  --json {fields} \
  --limit {limit}
```

`{fields}` is optional. When the caller does not pass it, substitute the default
`number,title,updatedAt,labels,state` — existing callers are unchanged. A caller
that needs more (e.g. `/list-focus-issues` selecting by assignee, age, or close date) passes
its own comma-separated `gh` JSON field list, such as
`number,title,url,state,createdAt,updatedAt,closedAt,labels,assignees`.

## close-issue

Close an issue:

```bash
gh issue close {issue_number} --reason {reason}
```

With optional comment:

```bash
gh issue close {issue_number} --reason {reason} --comment "{comment}"
```

## comment-issue

Post a comment on an issue:

```bash
gh issue comment {issue_number} --body "{body}"
```

## add-label

Add labels to an issue or PR:

```bash
gh issue edit {number} --add-label "{labels}"
```

For a PR:

```bash
gh pr edit {pr_number} --add-label "{labels}"
```

## attach-sub-issue

Attach a child issue as a sub-issue of a parent (GitHub-specific feature):

```bash
# Step 1: Get child issue's internal numeric ID (NOT the issue number)
CHILD_ID=$(gh api /repos/{owner}/{repo}/issues/{child_number} --jq '.id')

# Step 2: Attach as sub-issue
gh api /repos/{owner}/{repo}/issues/{parent_number}/sub_issues \
  -X POST -F sub_issue_id="$CHILD_ID"
```

Derive `{owner}/{repo}` from:

```bash
gh repo view --json nameWithOwner --jq '.nameWithOwner'
```

## view-user

Get the current authenticated user's login:

```bash
gh api user --jq '.login'
```

## update-comment

Update an existing comment in place (e.g., to update a review-pr marker comment):

```bash
gh api repos/{owner}/{repo}/issues/comments/{comment_id} \
  -X PATCH \
  -f body="{body}"
```

Derive `{owner}/{repo}` from:

```bash
gh repo view --json nameWithOwner --jq '.nameWithOwner'
```

## create-issue-typed

Create an issue with its title, body, issue type and parent in one call (GitHub only). First read the repository's id and its issue types, then create the issue with the type's id and, when there is a parent, the parent's node id. Stdout is the new issue's number.

```bash
gh api graphql -H "GraphQL-Features: issue_types,sub_issues" \
  -f query='query($owner:String!,$name:String!){repository(owner:$owner,name:$name){id issueTypes(first:50){nodes{id name}}}}' \
  -f owner={owner} -f name={repo}

gh api graphql -H "GraphQL-Features: issue_types,sub_issues" \
  -f query='mutation($repo:ID!,$title:String!,$body:String,$type:ID,$parent:ID){createIssue(input:{repositoryId:$repo,title:$title,body:$body,issueTypeId:$type,parentIssueId:$parent}){issue{number url}}}' \
  -f repo={repo_id} -f title="{title}" -f body="{body}" -f type={type_id} [-f parent={parent_node_id}]
```

An `issue_type` the repository does not have stops with exit 1, and nothing is made.

## set-issue-type

Set an issue's type (GitHub only):

```bash
gh api -X PATCH repos/{owner}/{repo}/issues/{issue_number} -f type="{issue_type}"
```

## edit-issue-body

Replace an issue's body (GitHub only):

```bash
gh api -X PATCH repos/{owner}/{repo}/issues/{issue_number} -f body="{body}"
```

## remove-label

Take one label off an issue (GitHub only):

```bash
gh issue edit {issue_number} --remove-label "{label}"
```

## remove-sub-issue

Take a child issue off its parent (GitHub only). Like `attach-sub-issue`, it needs the child's internal numeric id first:

```bash
CHILD_ID=$(gh api /repos/{owner}/{repo}/issues/{child_number} --jq '.id')
gh api /repos/{owner}/{repo}/issues/{parent_number}/sub_issue -X DELETE -F sub_issue_id="$CHILD_ID"
```
