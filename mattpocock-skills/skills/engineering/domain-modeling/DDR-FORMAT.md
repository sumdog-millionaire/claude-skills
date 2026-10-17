# DDR Format

A DDR (design decision record) is one row in the project's design decision register, held as a CSV
at `docs/ddr/register.csv`. It records a choice where **there were several ways to approach something
and the project is locking one**: how something acts, a coding style, a package. If there was only one
sensible way, there is nothing to record.

A DDR and an ADR record the same kind of thing and carry the same tags, so there is one vocabulary to
learn. They differ in one test, and it is not breadth:

> **An ADR is a decision you would pay to undo. A DDR is one you would just change.**

A narrow choice can be irreversible and belongs in an ADR ("shared documents are reached by a public
unguessable link"). A decision as wide as a whole visual language can be reversed in an afternoon and
belongs in a row. Route on the cost of undoing it.

The register is one file because its value is in being filtered: every decision in one area, every
unbuilt `must`, everything waiting on one tracker issue, in one sort. Nothing about a DDR lives
outside its row. A decision that needs a page of argument wants an ADR instead.

The register holds DDRs only. An ADR is written in `docs/adr/` and carries the same tags in its front
matter ([ADR-FORMAT.md](./ADR-FORMAT.md)), so one filter over the register and the ADR folder reads
both. A row names the ADRs it relates to in `adrs`.

## Columns

Nineteen, in this order. **Every field is double-quoted, always**, so a cell containing a comma, a
quote or a newline can never shift the columns.

| Column | Values and shape |
|---|---|
| `id` | `D1`, `D2`, … unique and never reused, kept across status changes |
| `status` | `proposed`, `in-research`, `accepted`, `rejected`, `deferred`, `superseded` |
| `layer` | Where the code that realises the rule lives, one value from the layer list |
| `area` | One of the eight areas in [taxonomy.json](./taxonomy.json) |
| `sub_area` | One sub-area of that area, from the same file |
| `project_taxonomy` | The project's own parts the row touches, semicolon-separated, from `project_taxonomy.json`; empty when it touches none in particular |
| `priority` | `must`, `should`, `could`: how vital the feature is |
| `risk` | `high`, `medium`, `low`: the cost of building it wrong |
| `built_prototype` | `yes`, `partial`, `no` |
| `built_production` | `yes`, `partial`, `no` |
| `decided` | The date of the decision, ISO `YYYY-MM-DD` |
| `statement` | The rule: one or two plain present-tense sentences, no implementation detail beyond what the rule needs |
| `why` | The observation or trade-off that produced it, one or two sentences |
| `alternatives` | The other approaches seriously considered, and why each lost. Required |
| `tracker_issue` | Where the discussion happened, by identifier (`ENG-134`); semicolon-separated if several |
| `settled_by` | The tracker issue that will settle a `proposed`, `in-research` or `deferred` row. Empty on settled rows |
| `supersedes` | Semicolon-separated ids this row replaces |
| `superseded_by` | The one id that replaced this row |
| `adrs` | Related ADRs, semicolon-separated (`ADR-0007;ADR-0008`) |

Semicolons separate list values, so a list reads clearly in a cell and splits in one call.

`alternatives` is required because it is what makes a row a decision: an empty one means either the
row is not a DDR or the reasoning was lost. Rows decided before 17 October 2026 are exempt and are
not back-filled.

There is no `consequences` column: a decision with real consequences to record usually wants an ADR.
There is no detail file. A row is the whole record.

## Tags

Three independent tags.

- **`layer`**: where the code lives.
- **`area` and `sub_area`**: what kind of decision it is. The same for every project, fixed in
  [taxonomy.json](./taxonomy.json), with a definition and a boundary example for each sub-area. When
  two sub-areas seem to fit, the boundary examples decide; when none fits, ask the user rather than
  stretch one.
- **`project_taxonomy`**: which of the project's own parts it touches.

| Layer | Meaning |
|---|---|
| `frontend` | What the user sees and does |
| `backend` | Services, pipelines, business logic |
| `data` | Schemas, contracts, storage, what is collected and what is never selected |
| `infra` | Deployment, CI, networking, logging, operations |
| `architecture` | Cross-module structure below the ADR bar: ownership, seams, naming |
| `content` | Wording that is neither screen nor pipeline: regulatory, brand, copy sources |
| `system` | A rule that binds every layer |

A rule that genuinely lives in two layers is two rows, or `system`.

### The project taxonomy

`project_taxonomy.json` sits beside the register: a JSON object from each part's name to a one-line
definition, naming the few big parts the project is built from as its people talk about them
(`"checkout": "The pages a customer pays through"`). It is not a second cut of the area list. The setup skill
writes the first version with the user. Afterwards an agent may propose adding, renaming or retiring
a part, and asks before changing the file; retiring one means retagging its rows in the same change.

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
| `high` | A defect that blocks acceptance: accuracy, money, regulation, security, a stakeholder's stated requirement |
| `medium` | A visible deviation a stakeholder would flag but ship |
| `low` | A preference a reasonable engineer could vary without harm |

## Built

`built_prototype` and `built_production` are independent; every combination is ordinary. There is no
"not applicable": a rule scoped to one surface says so in its `statement`, and the other column reads
`no`.

| Value | Meaning |
|---|---|
| `no` | Not built on that surface |
| `partial` | Built, wholly or in part, and not yet checked by the user. The most an agent may write, at the implementing edit |
| `yes` | The user has checked the built result against the rule and signed it off, with "signed off <surface> <date>" in `why` |

Production means the application that ships to users. Scripts, data pulls, design files and anything
under a prototype or discovery folder are not production. Built is not acceptance: only `status` says
whether a rule is agreed. The implementing code carries a comment with the id, so `grep D99` finds it.
File paths do not go in the register; they rot.

## Status

| Status | Meaning |
|---|---|
| `proposed` | An option awaiting the user's decision; not a build instruction |
| `in-research` | The point matters but a fact must be found first; a named tracker issue owns the investigation |
| `accepted` | An agreed rule, including one not yet built or tested |
| `rejected` | Declined; keep the reason so it is not proposed again without new evidence |
| `deferred` | The decision itself is postponed, not merely its implementation |
| `superseded` | Replaced by the successor named in `superseded_by` |

A `proposed`, `in-research` or `deferred` row names the tracker issue that will settle it in
`settled_by`, and that issue names the DDR back.

## Supersession

Keep the old row's id, set its `status` to `superseded` and its `superseded_by` to the new id; the new
row lists the old one in `supersedes`. Leave the old `statement` as written. Do not strike text through
or fold "superseded by" wording into the prose. When only part of a row is replaced, write a new row
for the replaced part rather than retiring the whole one.

## Numbering

Read the register immediately before writing, take the highest existing number plus one, and append
at the end of the file. A failed exact-match edit means another session wrote first: reread and
reconcile, never overwrite the newer file.

## Validation

[scripts/check_records.py](./scripts/check_records.py) ships with this skill and is the only check;
projects keep no validator of their own. The sync hook runs it before any record edit reaches `main`.
By hand, from the project root:

```bash
python <skill>/scripts/check_records.py docs/ddr/register.csv docs/adr
```

It fails on: wrong columns, a duplicate id, a value outside a vocabulary or the taxonomy, a sub-area
under the wrong area, an unknown project taxonomy part, a required column left empty (including
`alternatives` on a new decision), a supersession or settling reference pointing at nothing, an `adrs`
entry naming no ADR, a malformed date, and ADR front matter that breaks the same rules. It warns on a
`statement` over 600 characters, which is usually several rules sharing one id.
