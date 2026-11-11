## Intent
- Goal: While a loop runs, one status file for the run, in the issue's status folder, always holds the run's state (running, asking, checking, landing, done or halted), its round, the play that runs and its step in plain words, and when the run started and when the file was last updated; the loop updates it at every step and at each play's start and end, writes it whole, keeps it out of git, never shows it itself, and a display, once built, reads it and shows a line about once a minute without writing it.
- Limit: The file holds no secret, no file content and no person's answers, only what the run is doing.
- Limit: A reader never sees half a file, and a broken file is replaced, never trusted.
- Limit: The loop never shows the status itself, and a display never writes the file or controls the run.
- Fails if: During a run the file reads a step, play or state that is not what the run is doing, or is not updated when a play starts or ends.
- Fails if: The status file is committed, or holds a secret, file content or a person's answer.
- Fails if: A display, or anything but the loop's script, writes the file or changes how the run goes.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the run-status rule, the Shared Loop Run's status lines, the status script, the loop's name, issue and run id, the steps of the run, the folder rule that keeps status files out of git, and the coding tool the team works in.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who gave the loop its goal and follows a long run without asking; and the developer, a person or an AI agent who builds the code, who checks where a run stopped.
- Scope: In: the status file, its fields and states, when it is updated, how it is written, and the display that reads it once built. Out: what each step of the run does, laying the display into a project, the run's evidence, and seeing plans.

## Expectation
- Scenario: In a clinic's booking app, the Discovery loop runs for an hour. Its status file reads running, round one, the intents play, then the domains play, as each starts; it reads asking while the product owner reads the brief, checking while the checker runs, landing during the end, and done at the close. In a bank's payments service, a loop started outside an interactive session halts overnight, and the file reads halted with the time it stopped.
- Done means: Someone other than the one who ran the loop reads the status file during and after each run and the issue's commits, and finds for the clinic each state in its turn with the play and step that ran then, a start time and a newer update time, no secret, file content or answer in it, and no status file among the commits; and for the bank a file reading halted with the time of its last update.
