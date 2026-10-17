---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

Implement the work described by the user in the spec or tickets.

## 1. Load the context

First, before anything else, call the Skill tool with "grilling", "domain-modeling" and "design-decision". Every question to the user follows `grilling`'s format.

If the user passes a ticket reference, fetch it from the issue tracker with its comments and blocking links, and state its title. If the user passes a scope instead (a label, a milestone, a parent issue), take its **frontier**: the open ticket in that scope whose blockers are all done, because the order of work lives in the tracker's blocking links and nowhere else. If the reference is ambiguous, or the frontier holds more than one ticket or none, ask.

The glossary, ADR folder and design decision register sit at their defaults (`GLOSSARY.md`, `docs/adr/`, `docs/ddr/register.csv`) unless the project's `docs/agents/domain.md` names another place. Read every ADR and DDR the ticket cites, plus those whose nouns (module, element, data field) the ticket touches. Find the existing code to reuse or extend, with `file:line`.

## 2. Explain, then decide whether to grill

Explain the ticket in plain terms: what it is for, what it covers, each binding ADR and DDR in one line, and the reuse targets. Do not assume the user remembers the ticket.

List every choice the build needs that the ticket, ADRs, DDRs, glossary and code do not already settle: data shapes, names, file locations, edge cases, error behaviour, scope cuts and the seams to test.

- **Nothing open:** say "This ticket is detailed enough to build as written" and why, ask how involved the user wants to be, then go to step 3.
- **Anything open:** ask the whole list in one round, with how involved the user wants to be. If unsure whether a point is settled, it is not: ask. Never resolve an open point with an assumption.

Record each answer before the edit that implements it. Most become DDRs; one that passes the ADR test becomes an ADR with a pointer row in the register.

## 3. Set the rewind point

The user may rewind the session (`prepare-rewind`, then `carry-on-rewind`) to save tokens, so split the work at a common point.

- Steps 1 and 2 are the exploration. Finish them, every agent and check included, before any build work.
- Once the answers are in, name the **rewind point** to the user: the last message before the build starts, quoted by its first words. The user rewinds to it and sends `carry-on-rewind` in its place.
- Everything above the point must stay true for the whole session. Never set it where the explored facts are expected to change between rewinds, because the rewound context would then contradict the repository.
- Split the build into mechanical parts (A, B, C), one per rewind, each ending in a commit, so a handover carries only what that part built and decided.

## 4. Build

Call the Skill tool with "tdd" at the seams agreed in step 2.

Run typechecking regularly, single test files regularly, and the full test suite once at the end. If a new open point appears mid-build, stop and ask.

Once done, call the Skill tool with "code-review" to review the work.

Commit your work to the current branch.
