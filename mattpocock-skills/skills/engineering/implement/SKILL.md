---
name: implement
description: "Carry a tracker issue, or the next free ticket in a scope, to done."
disable-model-invocation: true
---

Carry a tracker issue, or the next free ticket in a scope, to done.

## 1. Load the context

First, before anything else, call the Skill tool three times, for "grilling", "domain-modeling" and "design-decision". Every question to the user follows `grilling`'s format.

If the user passes a ticket reference, fetch it from the issue tracker with its comments and blocking links, and state its title. If the user passes a scope instead (a label, a milestone, a parent issue), take its **frontier**: the open ticket in that scope whose blockers are all done, because the order of work lives in the tracker's blocking links and nowhere else. If the reference is ambiguous, or the frontier holds more than one ticket or none, ask.

The glossary, ADR folder and design decision register sit at their defaults (`GLOSSARY.md`, `docs/adr/`, `docs/ddr/register.csv`) unless the project's `docs/agents/domain.md` names another place. Read every ADR and DDR the ticket cites, plus those whose nouns (module, element, data field) the ticket touches. Find the existing code to reuse or extend, with `file:line`.

## 2. Explain, then decide whether to grill

Explain the ticket in plain terms: what it is for, what it covers, each binding ADR and DDR in one line, and the reuse targets. Do not assume the user remembers the ticket.

List every choice the build needs that the ticket, ADRs, DDRs, glossary and code do not already settle: data shapes, names, file locations, edge cases, error behaviour, scope cuts and the seams to test. Holdouts are on unless the user opts out for this ticket.

- **Nothing open:** say "This ticket is detailed enough to build as written" and why, ask how involved the user wants to be, then go to step 3.
- **Anything open:** ask the whole list in one round, with how involved the user wants to be. If unsure whether a point is settled, it is not: ask. Never resolve an open point with an assumption.
- **Answers that open more:** run further rounds of research and grilling until nothing is open, each round finished, every agent and check included, before its questions go out. Aim every round at facts that will hold for the whole session, because they sit above the rewind point.

Record each answer before the edit that implements it. Most become DDRs; one that passes the ADR test becomes an ADR in `docs/adr/`.

## 3. Set the rewind point

The user may rewind the session to save tokens, running `/prepare-rewind` before the rewind and `/carry-on-rewind` after it, so split the work at a common point.

- Steps 1 and 2 are the exploration. Finish them, every agent and check included, before any build work.
- Once the answers are in, state the **rewind point** in your last message before the build starts, on a line of its own that opens with `**Rewind point.**`, followed by a sentence saying the research and grilling above it hold for the session. `prepare-rewind` finds that line in the session log, so never write it anywhere else. Before a rewind the user runs `/prepare-rewind`, rewinds to their own message that follows yours, and sends `/carry-on-rewind` in its place, so your message stays.
- Everything above the point must stay true for the whole session. Never set it where the explored facts are expected to change between rewinds, because the rewound context would then contradict the repository. If one changes anyway, `prepare-rewind` records the change in `rewind-durable.md`.
- Split the build into mechanical parts (A, B, C), one per rewind, each ending in a commit, so a handover carries only what that part built and decided.

## 4. Build

Call the Skill tool with "tdd" and run its holdout loop at the seams agreed in step 2, unless the user opted out of holdouts.

Run typechecking regularly and the full test suite once at the end. If a new open point appears mid-build, stop and ask.

Once done, call the Skill tool with "code-review" to review the work. Then show the user what was built; once they confirm it meets the intent, have the tester promote the holdouts.

Commit your work to the current branch.
