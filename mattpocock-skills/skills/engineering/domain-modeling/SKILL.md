---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a GLOSSARY.md, recording or editing an ADR, or deciding whether a design rule is an ADR or a DDR (design decision record) for the project's design decision register.
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline: challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. (Merely *reading* `GLOSSARY.md` for vocabulary is not this skill: that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

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
`docs/ddr/register.csv`, tagged with layer and aspect, weighted by priority and risk, marked built or
not per surface, dated, and carrying an explicit status of `proposed`, `in-research`, `accepted`,
`rejected`, `deferred` or `superseded`.

When such a rule crystallises, hand it to the `design-decision` skill rather than writing it here. It
routes the rule to the register, a measured value to the project's values file and a term back to
`GLOSSARY.md`, and it makes sure every `proposed`, `in-research` or `deferred` row names the tracker
issue that will settle it. The row format and vocabularies are in [DDR-FORMAT.md](./DDR-FORMAT.md).
A decision that passes the ADR test gets the ADR, and a one-line pointer row in the register; never
two full write-ups.

The register's location is the project's to declare, under "Design decisions" in its `CLAUDE.md`. If
no register is declared, ask before creating one, as with `docs/adr/`.
