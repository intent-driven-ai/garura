# Feature: Specify from a deployed site

## What it does
A person gives a link to a deployed site. A browser with no window opens the link and finds each view by itself. A view is what a prototype shows after a click, such as the content of a tab. The browser clicks each control on the first screen, then each new control those views add, and saves each new view as a full-page picture and its visible text. A later step can then read the site as it was, even after the site is gone.

Status: built.

## Inputs / Outputs
- In: the link, and who gave it.
- In: any more pages of the same site to capture, and any named controls to click on the first page. Both are optional.
- Out: for the first page, a full-page picture, its visible text and its page code.
- Out: for each new view, a full-page picture and its visible text.
- Out: the capture record, with the kind "prototype — deployed site" and how many views were found and kept, whether the size limit was reached, and each view not reached with why.

## Rules & behavior
- A control is a button, a tab, a menu item, a link, a toggle or another marked element that a person can see and use.
- The browser loads the page again before each try and repeats the clicks. So each view starts from a known state.
- A view is new when its visible text differs from each view already kept. A control that shows a repeat counts as found and is not kept again.
- The size limit is 40 views beyond the first screen, or 160 clicks. Each control the browser did not try then goes on the record as not reached, with the limit as the reason.
- A click that fails goes on the record as not reached, with the error, and the browser goes on to the next control. The person hears which views were not reached.
- The browser does not click a control with any of these words: accept, approve, reject, drop, send back, delete, remove, edit, comment, finish, submit, undo, save, reset, log out, sign out, point, upload, pay, buy. This is a list of words, so a button such as "Create" or "Confirm" is clicked. The test also finds these words inside longer words, so a tab named "Payments" or "Appointments" is skipped. The record does not list the controls it skipped.
- The browser does not follow mail, phone or script links, or full links outside the folder of the page it was given. It follows relative links. Two gaps remain. A button that moves to another site by script is not tested. And when the given link is only the site's name with no final slash, such as https://example.com, every https link gets through.
- A named control is clicked with no word test. A named control that cannot be found fails the capture.
- A link that cannot be opened fails the capture. When the browser tool is not installed, the capture also fails, and it says how to install the tool.

## Acceptance criteria
- Given a first screen with three controls that each open a different view, when the site is captured, then the run keeps four pictures and four texts, and the record reads four kept.
- Given a control that reads "Delete", when the site is captured, then the browser does not click it.
- Given a site reached by a link with a path, such as https://example.com/app/, and a control that links to another site, when the site is captured, then the browser does not follow that link.
- Given a control that fails when clicked, when the site is captured, then the record lists that view as not reached, with why, and the other views are kept.
- Given a site with more than 40 views, when it is captured, then the run keeps 40 views beyond the first screen, and the record lists the rest as not reached.
- Given a link that cannot be opened, when the capture runs, then it fails, and the record says why and that nothing was saved.

## Out of scope
- Views deeper than two clicks. A journey reaches them when a person needs them: Specify from a prototype's journeys (fn-specify-from-journeys).
- Taking a step that changes data. Only a journey may do this, on a site the person cleared.
- Starting a local app before the capture. Specify from a project folder (fn-specify-from-folder) does this.
- Saying what the site shows in plain words. Specify intents (fn-specify-intents) does this.

## Sources
- The product owner approved this page and its ICE on 2026-11-06.
- core/components/plays/discover-intent/reference/ice.md: "up to two clicks deep", "a view it could not reach is recorded with why"
- core/components/plays/discover-intent/SKILL.md: "It never clicks a control that answers or changes data", "the person was told which"
- core/components/plays/discover-intent/scripts/capture_source.py: "Controls that answer or change data rather than show a view: never clicked while exploring.", "MAX_VIEWS = 40", "MAX_CLICKS = 160", "the exploration limit was reached", "a named control that cannot be found is a failure, not a skip"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "screenshots and images for a site"
