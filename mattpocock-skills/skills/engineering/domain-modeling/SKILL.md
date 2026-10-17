---
name: domain-modeling
description: "Load this first in any project, before you read its code, research it, plan, build or review. It reads the glossary and the decision records. Use it also when a term or a decision is named, disputed or recorded."
---

# Domain Modeling

The domain model is the project's **glossary** (`GLOSSARY.md`), which holds its words, and its decision records (ADRs and DDRs), which hold what was decided and why. Work in a project starts by reading them. Then, as you design, build and sharpen the model actively: challenge terms, invent edge-case scenarios, and write the glossary and decisions down the moment they crystallise.

## Read first

Before you read code, search, plan, or answer a question about the project:

1. Find where the glossary, the ADR folder and the design decision register live. They sit at the defaults in "File structure" below, unless the project's `docs/agents/domain.md` names another place.
2. Read the glossary whole. Each entry names one thing, and its `_Avoid_` line lists the words that mean something else here.
3. Skim the ADR titles, or their index when the folder has one, and open each ADR and DDR that touches the area you are about to work in.

You are done reading when you can name everything your work touches in the glossary's word, and you have read each decision that touches your area. A project with no glossary and no records has nothing to read: proceed, and create them lazily as below.

From then on, the glossary's word is the only word for its thing, in code, tests, tickets and replies. Where your work contradicts a recorded decision, say so before you go further.

## Keep the records on main

A project with `docs/agents/records.json` on `main` keeps the records it lists (glossary, ADRs, the register, the values file) on `main`, so that people on different branches never number or edit them apart. This plugin's hooks run [scripts/sync_records.py](./scripts/sync_records.py) in every project, act only where that file is on `main`, and do it all silently: at session start and before each edit to a record they bring the records to `main`'s latest, and after the edit they run [scripts/check_records.py](./scripts/check_records.py) and push it to `main` through a sync checkout, `<project>-records`, beside the project. `records.json` names `paths` (every record file or folder), `register` and `adrs`. Edit records in the project as usual. Commit the refreshed copies with the branch's work; they merge back without conflict.

When a hook fails, its message names the failure. Recover as follows, then make the edit again:

- **The records check failed:** nothing was pushed and your edit is still in the working copy. Fix the record so the check passes; the next edit to it pushes.
- **A conflict or an unfinished rebase:** another person changed the same lines moments before. In the sync checkout, resolve the conflicted files keeping both sides, renumber your own record to the next free number (and every reference to it, in the working copy too), `git add` them, then `git rebase --continue` and `git push origin HEAD:main` there.
- **A git or network failure** (fetch, push, credentials): say so to the user and stop; records are not edited until the sync works.
- **Anything else:** show the user the message and ask. Never discard a record edit, and never edit records in the sync checkout by hand except to resolve a conflict.

## File structure

Most repos have a single context:

```
/
├── GLOSSARY.md
├── docs/
│   ├── adr/
│   │   ├── 0001-event-sourced-orders.md
│   │   └── 0002-postgres-for-write-model.md
│   └── ddr/
│       └── register.csv              ← the DDR register, one row per decision
└── src/
```

If a `GLOSSARY-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives:

```
/
├── GLOSSARY-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── GLOSSARY.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── GLOSSARY.md
│       └── docs/adr/
```

Create files lazily: only when you have something to write. If no `GLOSSARY.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `GLOSSARY.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account': do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

### Update GLOSSARY.md inline

When a term is resolved, update `GLOSSARY.md` right there. Don't batch these up: capture them as they happen. Use the format in [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md).

`GLOSSARY.md` should be totally devoid of implementation details. Do not treat `GLOSSARY.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).

### Route design rules to DDRs

Most decisions that fail the ADR test are not worthless; they are just small and reversible. A rule
an engineer who never heard the conversation would build wrong ("the section heading pins level with
its sibling", "prompt construction never makes calls", "retries use the stdlib") is lost if it lives
only in a tracker ticket, which closes and buries it. That rule is a **DDR**, a design decision
record: one row in the project's design decision register, a filterable CSV at
`docs/ddr/register.csv`, tagged with layer, area, sub-area and project part, weighted by priority and risk, marked built or
not per surface, dated, and carrying an explicit status of `proposed`, `in-research`, `accepted`,
`rejected`, `deferred` or `superseded`.

When such a rule crystallises, hand it to the `design-decision` skill rather than writing it here. It
routes the decision to the register, a term back to `GLOSSARY.md` and an action or experiment to the
tracker, and it makes sure every `proposed`, `in-research` or `deferred` row names the tracker
issue that will settle it. The row format and vocabularies are in [DDR-FORMAT.md](./DDR-FORMAT.md).
A decision that passes the ADR test gets the ADR, and a one-line pointer row in the register; never
two full write-ups.

The register lives at `docs/ddr/register.csv` unless the project's `docs/agents/domain.md` names
another place. If the project has none, ask before creating one, as with `docs/adr/`.
