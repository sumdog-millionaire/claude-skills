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

A project with `docs/agents/records.json` on `main` keeps the records it lists (glossary, ADRs, the register, the values file) on `main`, so branches share one source. This plugin's hooks run [scripts/sync_records.py](./scripts/sync_records.py) in every project, act only where that file is on `main`, and do it all silently: at the start of each turn they fetch `main` and refresh the local records, and when the turn ends they run [scripts/check_records.py](./scripts/check_records.py) and push the turn's record edits to `main` in one commit, through a sync checkout, a git worktree at `.git/records-sync` inside the project, so nothing appears beside it. A turn the user interrupts does not push; its edits are preserved for the next turn. Only your own changes reach `main`. A register row whose id `main` lacks is appended. A row or file you changed, meaning it differs from both your branch's commit and the copy the hook last gave you (kept in `.git/records-base`), replaces `main`'s only while `main` still holds the copy you started from. The hook never deletes a row or a file. The turn-start refresh replaces only the files that hold no change of yours. If someone pushes first, the hook fetches and merges again once. `records.json` names `paths` (every record file or folder), `register` and `adrs`. Edit records in the project as usual and commit the refreshed copies with the branch's work. Only the configured records are synchronised, not the whole branch.

When a hook fails, its message names the failure. A failed turn-start refresh never blocks the user's prompt: its message reaches you as context instead. Recover as follows; the hooks retry at the next turn boundary:

- **The records check failed:** nothing was pushed and your edit is still in the working copy. Fix the record so the check passes; the push runs again when the turn ends.
- **Main changed a record after you started from it:** the message names the row ids or files. Nothing was pushed and your working copy is intact. Compare your copy with `main`'s, keep both changes in your working copy, renumber a new row of yours if its id is taken (and every reference to it), and save; the push runs again when the turn ends.
- **An unfinished rebase left by an earlier version of the hook:** run `git rebase --abort` in the sync checkout.
- **A git or network failure** (fetch, push, credentials, a lock file): tell the user, investigate the cause and report what you found; edit no record until the sync works.
- **Anything else:** show the user the message and ask. Never discard a record edit, and never edit records in the sync checkout by hand.

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

An ADR records what the product is and why, or a choice you would pay to undo. Offer one in two cases.

**A decision about the product as a whole**: its purpose, who it is for, what it stands for, a concept
everything else rests on. This is an ADR however cheaply its words could change, and it never goes in
the design decision register, which holds rules for how things are built.

**A decision on how to build**, when all three are true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

If a build decision misses any of the three, skip the ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).

### Route design rules to DDRs

Most build decisions that fail the ADR test are not worthless; they are just small and reversible. A rule
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
A decision that passes the ADR test gets an ADR in `docs/adr/`, with its tags in the front matter,
and no row: the register holds DDRs only, and a filter reads both. A DDR row may name related ADRs in
its `adrs` column.

The register lives at `docs/ddr/register.csv` unless the project's `docs/agents/domain.md` names
another place. If the project has none, ask before creating one.
