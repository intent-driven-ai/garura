# Capability: Manage a plan

## Directional intent
update, edit and delete plans, and keep the plan file and its tracker issues in step. Orchestration only.

## Agent intent (ICE)
- Goal: After any change, the plan file and the tracker agree.
- Limit: It never cuts or merges a branch and never changes code — that is the implementation plays' work.
- Fails if: a change lands in the plan file and not in the tracker, or the other way round.
- Checked by: a compare of the plan file with the tracker finds no difference after each change.
