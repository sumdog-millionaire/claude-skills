# DDR Format

A DDR (design decision record) is one row in the project's design decision register, held as a CSV
at `docs/ddr/register.csv`. It is the counterpart of an ADR for decisions that fail the ADR test,
at the granularity an engineer would otherwise get wrong ("the section heading pins level with its
sibling", "prompt construction never makes calls", "retries use the stdlib, not a library").

A DDR and an ADR record the same kind of thing and carry the same fields, so there is only one
format to learn. They differ in one test, and it is not breadth:

> **An ADR is a decision you would pay to undo. A DDR is one you would just change.**

Breadth describes what tends to end up in each set; it does not decide the awkward cases. A narrow,
specific choice can be irreversible and belongs in an ADR ("published quotes are reached by a public
unguessable link"). A decision as wide as a whole visual language can be reversed in an afternoon
and belongs in a row. Route on the cost of undoing it.

The register is one file because its value is in being filtered: every decision at a given priority,
every unbuilt `must`, everything waiting on one tracker issue, in one sort. Prose files cannot do
that, so nothing about a DDR lives outside its row. Where a decision needs a page of argument, it
has failed the reversibility test and wants an ADR instead.

The project names the register under "Design decisions" in its `CLAUDE.md` (or `AGENTS.md`), and may
name a different path. Create the folder lazily, on the user's go, when the first DDR is needed.

## Columns

Seventeen, in this order. **Every field is double-quoted, always, with no exceptions**, so that a
cell containing a comma, a quote or a newline can never shift the columns, and so an exact-match
edit to one row is safe to make without reading the rest.

| Column | Values and shape |
|---|---|
| `id` | `D1`, `D2`, … unique and never reused, kept across status changes |
| `status` | `proposed`, `in-research`, `accepted`, `rejected`, `deferred`, `superseded` |
| `layer` | Where the code that realises the rule lives, one value from the layer list |
| `aspect` | What kind of rule it is, one value from the aspect list |
| `priority` | `must`, `should`, `could` — how vital the feature is |
| `risk` | `high`, `medium`, `low` — the cost of building it wrong |
| `built_prototype` | `yes`, `partial`, `no` |
| `built_production` | `yes`, `partial`, `no` |
| `decided` | The date of the decision, ISO `YYYY-MM-DD` |
| `decision` | The rule: one or two plain present-tense sentences, no implementation detail beyond what the rule needs |
| `why` | The observation or trade-off that produced it, one or two sentences |
| `alternatives` | What was seriously considered and rejected, and why. Empty when there was no real alternative — do not invent one |
| `tracker_issue` | Where the discussion happened, by identifier (`AI-134`); semicolon-separated if several |
| `settled_by` | The tracker issue that will settle a `proposed`, `in-research` or `deferred` row. Empty on settled rows |
| `supersedes` | Semicolon-separated ids this row replaces |
| `superseded_by` | The one id that replaced this row |
| `adrs` | Related ADRs, semicolon-separated (`ADR-0007;ADR-0008`) |

Semicolons separate list values rather than commas, so a list reads clearly in a cell and splits in
one call.

There is deliberately no `consequences` column: in practice almost no row has non-obvious downstream
effects worth recording, and a column that is empty on 95% of rows costs every reader something and
tempts a retrospective audit into inventing content. A decision with real consequences to record is
usually one that wanted an ADR.

There is no detail file. A row is the whole record.

## Layer and aspect

Two independent lists in two columns. The layer is where the code that realises the rule lives; the
aspect is what kind of rule it is. Because they are independent, cross-cutting concerns pair with
any layer: `frontend` + `security`, `backend` + `security`, `system` + `security`.

| Layer | Meaning |
|---|---|
| `frontend` | What the user sees and does |
| `backend` | Services, pipelines, business logic |
| `data` | Schemas, contracts, storage, what is collected and what is never selected |
| `infra` | Deployment, CI, networking, logging, operations |
| `architecture` | Cross-module structure below the ADR bar: ownership, seams, naming |
| `content` | Wording that is neither screen nor pipeline: regulatory, brand, copy sources |
| `system` | A rule that binds every layer |

Aspects: `layout`, `interaction`, `motion`, `visual`, `copy`, `imagery`, `accessibility`,
`performance`, `security`, `dependency`, `structure`, `rules`, `pipeline` (how data is transformed
on its way through), `integration`, `regulatory`, `brand`, `process` (how the work itself is done,
usually `system` + `process`).

A swappable library choice is `backend` + `dependency`; one that carries lock-in is an ADR. A rule
that genuinely lives in two layers is two rows, or `system`. A value outside these lists means ask
the user, not invent one; the project's register README is the vocabulary and a project may extend
it there.

## Priority and risk

Two separate columns, because they differ often: a low-priority feature can be high-risk if it
touches money, and a must-have can be low-risk.

| Priority | Meaning |
|---|---|
| `must` | The product is not acceptable without it |
| `should` | Expected; its absence would be flagged and negotiated |
| `could` | Wanted if capacity allows |

| Risk | Meaning, as the cost of building it wrong |
|---|---|
| `high` | A defect that blocks acceptance: accuracy, money, regulation, security, a client-stated requirement |
| `medium` | A visible deviation the client would flag but ship |
| `low` | A preference a reasonable engineer could vary without harm |

Risk sets how much care implementation gets; `high` rows are the ones carried into acceptance checks
and handover documentation.

## Built

Two columns, `built_prototype` and `built_production`, because projects often build the same rule
twice and skip some in the prototype altogether. The two are independent: every combination is
ordinary, and nothing moves from one to the other. There is no "not applicable" value — a rule
scoped to one surface says so in its `decision` text, and the other column simply reads `no`.

| Value | Meaning |
|---|---|
| `no` | Not built on that surface |
| `partial` | Built, wholly or in part, and not yet checked by the user against the rule. The most an agent may write, at the moment of the implementing edit |
| `yes` | The user has seen the built result, checked it against the rule and signed it off. Flipped only on their explicit word, with "signed off <surface> <date>" added to `why` |

The gap between `partial` and `yes` is the point: a rule the agent believes it built is not the same
as a rule the user has confirmed is built right, and treating them alike is how things get built
badly. Production means the application that ships to users. Collection scripts, data pulls, design
files and anything under a prototype or discovery folder are not production, however finished they
look; until the application exists, every production column is `no`. Built is implementation, not
acceptance: only `status` says whether a rule is agreed, and `yes` on a `proposed` row means a
suggestion was prototyped, nothing more.

Keep it honest by flipping it in the same change as the implementing edit, and by having that code
carry a comment with the id so `grep D99` finds the implementation and the validator can audit the
column. File paths do not go in the register; they rot.

## Status

| Status | Meaning |
|---|---|
| `proposed` | An option awaiting the user's decision; not a build instruction |
| `in-research` | The point matters but a fact must be found first; a named tracker issue owns the investigation and the row becomes `proposed` or `accepted` when it closes |
| `accepted` | An agreed rule, including one not yet built or tested |
| `rejected` | Declined; keep the reason so it is not proposed again without new evidence |
| `deferred` | The decision itself is postponed, not merely its implementation |
| `superseded` | Replaced by the successor named in `superseded_by` |

A `proposed`, `in-research` or `deferred` row names the tracker issue that will settle it in
`settled_by`, and that issue names the DDR back. A row nobody owns is a decision nobody will make.

## Supersession

Supersession is data, not formatting. Keep the old row's id, set its `status` to `superseded` and its
`superseded_by` to the new id; the new row lists the old one in `supersedes`. Leave the old
`decision` text as it was written, so the record still says what was once agreed. Do not strike text
through or fold "superseded by" wording into the prose: nothing renders it, and a filter on
`superseded_by` finds in one pass what a text search never will.

When only part of a row is replaced, the surviving clauses are the reason to write a new row for the
replaced part rather than retiring the whole one. Keep each row to a single rule and the case mostly
disappears.

## Numbering

Read the register immediately before writing, take the highest existing `id` number plus one, and
append the row at the end of the file. A failed exact-match edit means another session wrote first:
reread and reconcile, never overwrite the newer file.

## Validation

A register nothing renders as a table needs a check that nothing drifts. The project keeps a
validator (by convention `scripts/ddr/check.py`) that fails loudly on: a duplicate or missing id, a
`status`, `layer`, `aspect`, `priority`, `risk` or built value outside its vocabulary, a
`superseded_by` or `supersedes` pointing at an id that does not exist, a `superseded` row with no
`superseded_by`, a `proposed`, `in-research` or `deferred` row with no `settled_by`, a malformed
`decided` date, and a row whose field count is wrong. Run it after any edit to the register.

It also warns, without failing, on a `decision` cell over 600 characters. A rule that long is
usually several rules sharing one id, and wants splitting into separate rows by the user.

## What goes elsewhere

- A measured value (16px, a hex colour, a duration) goes in the project's values file, such as
  `DESIGN.md`, citing the id. The row states the rule, not the number.
- A term goes in `GLOSSARY.md`.
- A decision you would pay to undo gets an ADR; the row becomes a one-line pointer with the ADR
  named in `adrs`.
