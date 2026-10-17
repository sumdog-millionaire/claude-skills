# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Before exploring, read these

- **`GLOSSARY.md`** at the repo root, or
- **`GLOSSARY-MAP.md`** at the repo root if it exists: it points at one `GLOSSARY.md` per context. Read each one relevant to the topic.
- **`docs/adr/`** and **`docs/ddr/register.csv`**: read the ADRs and DDRs that touch the area you're about to work in. ADRs and DDRs always travel together: wherever you read, respect, cite or flag one, do the same for the other. In multi-context repos, also check `src/<context>/docs/adr/` for context-scoped decisions.
- **The design rulebook** (the values file, such as `DESIGN.md`), when the project has one: setup writes its path here.

If any of these files don't exist, **proceed silently**. Don't flag their absence; don't suggest creating them upfront. The `/domain-modeling` and `/design-decision` skills (reached via `/grill-with-docs` and `/improve-codebase-architecture`) create them lazily when terms or decisions actually get resolved.

## File structure

Single-context repo (most repos):

```
/
├── GLOSSARY.md
├── docs/adr/
│   ├── 0001-event-sourced-orders.md
│   └── 0002-postgres-for-write-model.md
├── docs/ddr/register.csv
└── src/
```

Multi-context repo (presence of `GLOSSARY-MAP.md` at the root):

```
/
├── GLOSSARY-MAP.md
├── docs/adr/                          ← system-wide decisions
└── src/
    ├── ordering/
    │   ├── GLOSSARY.md
    │   └── docs/adr/                  ← context-specific decisions
    └── billing/
        ├── GLOSSARY.md
        └── docs/adr/
```

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, a test name), use the term as defined in `GLOSSARY.md`. Don't drift to synonyms the glossary explicitly avoids.

If the concept you need isn't in the glossary yet, that's a signal: either you're inventing language the project doesn't use (reconsider) or there's a real gap (note it for `/domain-modeling`).

## Flag ADR and DDR conflicts

If your output contradicts an existing ADR or DDR, surface it explicitly rather than silently overriding:

> _Contradicts ADR-0007 (event-sourced orders), but worth reopening because…_
> _Contradicts D132 (prompt construction never makes calls), but worth reopening because…_

## Cite ADRs and DDRs in tracker issues

Every issue or ticket you create names the ADRs and DDRs that bind it, by identifier with a one-line gist each, under a **Decisions** heading. Write "None" when none apply.
