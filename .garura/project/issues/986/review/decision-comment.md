Harness verdict (gate off per gates.plays.check-change): approve

No blocking finding. test_plan green (17); /list-plans' check passes on the real plans (7 plans, all listed, in order, as set, same twice, no plan file changed). This is a recorded harness verdict, not a human review.

**Findings — {'P4': 5, 'P3': 1}**

P3:
- **H-1** (harness) The compiled description now says 'its number and business intent, its direction on the line under', but the ICE Intent paragraph (reference/ice.md line 9) still reads 'with the plan's direction, its number and business 

P4:
- **F-1** (code-and-tests) The listing() docstring has a line of 152 characters because the new text was joined onto the old line; the rest of the file keeps lines near 100 to 120. Wrap it onto two lines.
- **H-2** (harness) SKILL.md 'Compiled From' and the compiled_by row now cite #986, but the ICE 'Stories' line (line 64) lists #729, #806 and #983 only. The compiled file names a story the ICE source does not.
- **H-3** (harness) The check now also requires a blank line between the icon line (or heading) and the Status row, and rows at the left edge. The ICE (S6, C10) and SE-7 say only 'the icon line, and the Status row'; the blank line and left-
- **F-001** (memory) The list example ends the second card (#722) after the Status row, with no ellipsis. The tool always prints Branch and Waits on for every card (and the prose says Waits on is always shown), so the example reads as if a c
- **F-002** (memory) README line 10 still describes a card as "its direction (⏵, ⏵⏵, ⏵⏵⏵), number and title", which reads as the icon coming first. The template now puts the number and title first and the icon on its own line below. The READ

**Routing:** approve → `/merge-change` lands this on `plan/717/base`; then plan 717 to main (squashed), the template promotion and the reinstall. Follow-up: `/list-plans`' intent sentence and its story list (#986) through `/edit-play`; the README's card line; the template's second example card.
