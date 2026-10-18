# Kapil's test — #657 memory tool

A fresh project (empty Garura memory) and a clone of Phoenix memory, read at its approved version (`origin/main`). Settings: `memory-settings.json` in the project (short-term `.garura/project/issues`, Garura `.garura`, pulled pieces in `core/memory`).

Health: short-term reachable, garura reachable, phoenix reachable at `5fcd88e05cf6`

## 1. Login story

**Short-term memory for issue 1:** `1/specs/story.md` — "Story: a user signs in to the app with email and password."

- Look up how sign-in works  
  `memory.py search --issue 1 --pattern credential login --fixed`  
  looked in short-term, garura, phoenix → answered by **phoenix**; first result: `phoenix` `knowledge/domains/user-management.md` line 45 ✓
- Use it: read the Authentication part  
  `memory.py read --issue 1 --tier phoenix --path knowledge/domains/user-management.md --start 44 --end 48`  
  read `phoenix` `knowledge/domains/user-management.md` lines 44–48 ✓
- Pulled into Garura memory so far: `knowledge/domains/user-management.md`

## 2. Re-run the login story
- The same lookup again  
  `memory.py search --issue 1 --pattern credential login --fixed`  
  looked in short-term, garura → answered by **garura**; first result: `garura` `core/memory/knowledge/domains/user-management.md` line 45 ✓

## 3. Change-password story

**Short-term memory for issue 2:** `2/specs/story.md` — "Story: a signed-in user changes their password."

- Look up password reset (pulled during the login story)  
  `memory.py search --issue 2 --pattern Password reset --fixed`  
  looked in short-term, garura → answered by **garura**; first result: `garura` `core/memory/knowledge/domains/user-management.md` line 62 ✓
- Look up password strength (not pulled yet)  
  `memory.py search --issue 2 --pattern Password strength validation --fixed`  
  looked in short-term, garura, phoenix → answered by **phoenix**; first result: `phoenix` `standards/rules/kb-extension.md` line 146 ✓
- Use it: read the password strength rule  
  `memory.py read --issue 2 --tier phoenix --path standards/rules/kb-extension.md --start 145 --end 146`  
  read `phoenix` `standards/rules/kb-extension.md` lines 145–146 ✓
- Pulled into Garura memory so far: `knowledge/domains/user-management.md`, `standards/rules/kb-extension.md`

## 4. Project memory removed
- Deleted `.garura/core/memory/` (every pulled piece and the pulled list).
- The login lookup again  
  `memory.py search --issue 1 --pattern credential login --fixed`  
  looked in short-term, garura, phoenix → answered by **phoenix**; first result: `phoenix` `knowledge/domains/user-management.md` line 45 ✓
- Something no tier holds  
  `memory.py search --issue 2 --pattern passkey --ignore-case`  
  looked in short-term, garura, phoenix → answered by **none** (nothing found); first result: nothing ✓
  The empty answer (answered by none, after all three tiers) is the cue to raise a memory update; raising it is #658, and it lands in short-term memory.

## Result
All steps behaved as expected.
