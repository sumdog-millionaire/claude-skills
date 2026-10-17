## What it does

`design-decision` writes down the choices that fall below the ADR bar. Wherever there were several ways to build something and the project locks one, it becomes a **DDR** (design decision record): one row in `docs/ddr/register.csv`, numbered, dated and given a status, tagged by layer, area, sub-area and project part, and weighted by priority and risk.

The test that separates the two records is cost, not size. **An ADR is a decision you would pay to undo. A DDR is one you would just change.** A narrow choice can be irreversible and want an ADR; a whole visual language can be reversed in an afternoon and want a row. If there was only one sensible way, there is nothing to record.

The register is a CSV because its value is in being filtered: every unbuilt `must`, every `high` risk row, everything in one area, in one sort.

## When to reach for it

It runs underneath a grilling more often than on its own. [grill-with-docs](https://aihero.dev/skills-grill-with-docs) and [wayfinder](https://aihero.dev/skills-wayfinder) load it beside [domain-modeling](https://aihero.dev/skills-domain-modeling), and it writes a row the moment a question closes with a choice. Type `/design-decision` directly when a review round, a client or a product owner settles something that needs writing down before it is built.

| The situation | The move |
| --- | --- |
| "The section heading pins level with its sibling" was agreed in a call | `design-decision`: a row, written before the edit that builds it |
| You chose a package, a module boundary or a logging rule | `design-decision`: a row naming the alternatives that lost |
| The choice would cost real money or time to undo | [domain-modeling](https://aihero.dev/skills-domain-modeling): an ADR, plus a one-line pointer row |
| A new word settled | [domain-modeling](https://aihero.dev/skills-domain-modeling): the glossary |
| An action, an experiment or a check | The issue tracker, not a record |

## Prerequisites

[setup-matt-pocock-skills](https://aihero.dev/skills-setup-matt-pocock-skills) sets the project up: the register at `docs/ddr/register.csv`, the project's own parts in `docs/ddr/project_taxonomy.json` beside it, and the tracker. A record kept away from its default path is named in `docs/agents/domain.md`. Without a register, the skill asks before creating one.

## How a row is kept honest

- **Status** is explicit on every row: `proposed`, `in-research`, `accepted`, `rejected`, `deferred` or `superseded`. Only the user's word promotes a proposal; a built experiment does not.
- **Built** is two columns, one for the prototype and one for production. An agent may write `partial` at the implementing edit; only the user writes `yes`, after checking the result.
- **An undecided row names the tracker issue that will settle it**, and the issue names the row back.
- **Supersession is data**: the old row keeps its words and points at its successor.
- **The records check** (`domain-modeling/scripts/check_records.py`) refuses a malformed row or ADR. In a project with `docs/agents/records.json` on `main`, the plugin's hooks run it and keep the records on `main` for every branch.

## It's working if

- A choice made in conversation is a row before the code that builds it exists.
- Every new row names the alternatives that lost.
- A filter on the register answers "what is still unbuilt and must ship?" in one pass.
- It refuses to write a row for a choice nobody had to make.

## Where it fits

`design-decision` is a **model-invoked reference** that runs underneath grilling, like domain-modeling. It is the lower half of the decision record, beside [domain-modeling](https://aihero.dev/skills-domain-modeling), which owns the glossary and the ADRs. [implement](https://aihero.dev/skills-implement) reads the rows a ticket cites, and [to-tickets](https://aihero.dev/skills-to-tickets) and [triage](https://aihero.dev/skills-triage) name them under a ticket's Decisions heading. [ask-matt](https://aihero.dev/skills-ask-matt) routes the whole set.
