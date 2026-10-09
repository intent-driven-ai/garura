# Follow-up draft — a skill that manages ADRs

**Asked by:** Kapil, 2026-10-09, while ADR 031 was being written for #612:
"we need a skill that manages adrs... adr format, write it, approve it and also to check if
this adr invalidates any older ones. and impact of AINT... ADRs ideally should not impact bint"

Not filed in the tracker yet (no tracker write was asked for). Its own issue, branch and change,
after PR #631.

## What it must do

1. **Format.** One canonical ADR format (today each ADR follows the last one by hand: Status,
   Date, Decided in, Amends / Supersedes, Affects, Related; Context, Decision, Consequences,
   Alternatives, Work This Creates, References).
2. **Write.** Draft an ADR from a decision and its sources, in that format.
3. **Approve.** A person approves it; it moves Proposed → Accepted only on their word.
4. **Check what it invalidates.** Read every older ADR and say which ones it supersedes or
   amends, in part or in full — and update their status lines so the older ADRs point forward.
5. **Check its impact on agent intent (AInt / ICE).** Say which ICE, rules, plays and schemas
   the decision changes.
6. **Guard business intent.** An ADR should not change a business intent. If it does, flag it to
   the person instead of applying it, because only a person changes what they want.

## Seen while writing ADR 031 (input for the design)

- Finding the older ADRs a new one amends took a manual search (ADR 029 §6, ADR 027, ADR 026);
  the review of PR #631 caught the gaps (MEM-3, MEM-4, F4), not the author.
- ADR 031 itself changes the *kinds* Business Intent and ICE — framework doctrine — but no
  person's business intent. The check in step 6 must tell those two apart.
- Likely shape: a skill (format + write + the two checks as a script where they are mechanical:
  status-line cross-references, ADR numbering), with the approval as a play checkpoint.
