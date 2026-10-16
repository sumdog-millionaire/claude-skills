---
name: design-decision
description: Record proposed, in-research and accepted decisions that fall below the ADR bar as DDRs (design decision records) - numbered, dated, statused rows tagged by layer, area, sub-area, project part, priority and risk in the project's design decision register, a filterable CSV - before implementation, for prototype and production alike. Use this whenever a choice is settled in conversation where there were several ways to approach it - how something acts, layout, motion, colour, copy placement, disclosure behaviour, a module boundary, a coding style, a package, a logging or data-handling rule - and whenever the user says "record that", "design note", "make that a decision", "D-row", "DDR", "add it to the register", "put this in for prod", or closes a grilling question with a choice. Run it beside domain-modeling in every grilling; also use it when a review round (users, client stakeholders, the product owner) produces accepted changes that need writing down before they are built.
---

# Design decision

A design decision is a choice where **there were several ways to approach something and the project is
locking one**: how something acts, a coding style, a package. "The section heading pins level with its
sibling heading", "prompt construction never makes calls", "retries use the stdlib, not a library".
Losing one means the production build quietly differs from what was agreed. So each becomes a row in
the project's **design decision register**, a CSV. A row is a DDR, a design decision record, with a
`D99` identifier. If there was only one sensible way, there is no decision to record.

> **An ADR is a decision you would pay to undo. A DDR is one you would just change.**

Breadth is not the test. A narrow choice can be irreversible and wants an ADR; a decision as wide as
a whole visual language can be reversed in an afternoon and wants a row.

The register is a CSV because its value is in being filtered: every unbuilt `must`, every `high` risk
row, everything in one area, in one sort. Accepted rules apply to both prototype and production unless
explicitly limited. A built experiment or passing test is not acceptance of a rule.

The columns, tags and weights live in [DDR-FORMAT.md](../domain-modeling/DDR-FORMAT.md), and the
area list in [taxonomy.json](../domain-modeling/taxonomy.json). Read both before writing a row.

## Project declaration

The skill is the method; each project supplies the places. The project's `CLAUDE.md` (or `AGENTS.md`)
names, under a "Design decisions" heading:

- the **register** file that holds the rows, by convention `docs/ddr/register.csv`, with its
  `project_taxonomy.json` beside it;
- the **values file**, the project's design rulebook, such as `DESIGN.md`;
- the **glossary** for terms, such as `GLOSSARY.md`;
- the **ADR folder**, such as `docs/adr/`;
- the **tracker** and where its conventions live, such as Linear via `docs/agents/issue-tracker.md`.

If any of the five is missing, stop and ask the user where it lives before writing anything. Do not
assume a path, and do not create a register without their go.

## Companion skills

- **Explicit invocation:** when the user invokes this skill by name, load both `grilling` and
  `domain-modeling` before recording decisions. Loading them does not require asking questions whose
  answers are already established.
- **Automatic invocation:** normally load both companions too. They may be skipped only when the
  context unambiguously supplies every column of the row with no unresolved choice or terminology
  conflict.

## Decision status

| Status | Meaning |
|---|---|
| `proposed` | A suggestion or option awaiting the user's decision; not a build instruction |
| `in-research` | The user has agreed the point matters but a fact must be found first; a named tracker issue owns the investigation and the row becomes `proposed` or `accepted` when it closes |
| `accepted` | The user has agreed the rule; it may still be unimplemented, blocked or untested |
| `rejected` | The user declined it; retain the reason so it is not proposed again without new evidence |
| `deferred` | The user explicitly postponed the decision, not merely its implementation |
| `superseded` | A later accepted row replaces it; `superseded_by` names that row |

Promote a proposal only on explicit acceptance, recording who accepted it and when. Preserve its id.
Implementation, silence, a meeting suggestion or a recommendation inside an issue cannot promote it.

## 1. Route it

Decide where the thing belongs before writing anything. One place per thing; the others only point.

| It is | Home |
|---|---|
| A decision: several approaches, one locked | A row in the register |
| A decision you would pay to undo | An ADR, via `domain-modeling`, plus a one-line pointer row naming it in `adrs` |
| A term | The glossary, via `domain-modeling` |
| A change to the design rulebook | The values file, and only when the user has set out to change that rulebook |
| An action, an experiment, a verification, a question for someone | The tracker |
| A pointer from code | A comment carrying the DDR id and nothing else |

A value that realises a decision (16px, a hex colour, 0.7s) lives in the code and, where the value is
the decision, in the row's `statement`. It does not go in the values file unless the user is changing
the rulebook. A decision needing a page of argument has failed the reversibility test: it is an ADR,
not a long row. Experiments, dated actions and measurement notes never go in a record; they go in the
tracker.

## 2. Gather the row's parts

Use the conversation and dated source records, not inferred intent from code. Capture unresolved
options as `proposed` rather than losing them or choosing for the user. Never invent a reason or a
source to fill a cell.

- **`status`**, with prototype-only, production-only or provisional limits stated in the `statement`.
- **`layer`**, **`area`**, **`sub_area`** and **`project_taxonomy`**: where the code lives, what kind of
  decision it is (from `taxonomy.json`, using its boundary examples when two seem to fit) and which of
  the project's parts it touches (from `project_taxonomy.json`, several allowed, empty when none in
  particular). A value outside the lists means ask, not invent. If the project taxonomy seems to be
  missing a part, propose the addition to the user rather than stretching an existing one.
- **`priority`** and **`risk`**. Priority is how vital the feature is; risk is the cost of building it
  wrong and sets how much care implementation gets. Weigh them separately.
- **`built_prototype`** and **`built_production`**, each `yes`, `partial` or `no`. A new row is
  normally `no` and `no`. After the implementing edit, flip that surface to `partial` in the same change
  and give the code a comment carrying the id. `yes` is the user's alone, with "signed off <surface>
  <date>" added to `why`.
- **`decided`**, the date in ISO form.
- **`statement`**, the rule in one or two plain present-tense sentences. One rule per row: past about
  600 characters it is several rules and wants splitting.
- **`why`**, the observation or trade-off that produced it, in one or two sentences. A rule hiding in
  `why` belongs in the `statement` or its own row.
- **`alternatives`**, required: the other approaches seriously considered and why each lost. If there
  were none, it is not a DDR.
- **`tracker_issue`**, where the discussion happened, by identifier.
- **`settled_by`**, for every `proposed`, `in-research` or `deferred` row: the tracker issue that will
  settle it. If none exists one is created (step 5) before the row is written.
- **`supersedes`**, **`superseded_by`** and **`adrs`**, ids only.

## 3. Check the register first

Filter the register for the nouns in the rule and for its area and project part. Three outcomes:

- **Already recorded**: say so, cite the id, write nothing.
- **Accepted replacement conflicts with a row**: supersede it. A proposal does not replace an accepted
  rule. Set the old row's `status` to `superseded` and its `superseded_by` to the new id, leave its
  `statement` as written, and list it in the new row's `supersedes`.
- **New**: write it.

Also check the project's `CLAUDE.md` and ADR folder. Flag an unresolved conflict with those to the
user rather than silently changing them.

## 4. Number and write

Read the register immediately before writing; preserve newer decisions from other sessions. The next
number is the highest existing id plus one. Append the row at the end of the file, columns in the
order given in DDR-FORMAT.md, **every field double-quoted**.

A proposed row names its proposer and proposal date. Record acceptance or rejection with its date when
it happens. The records check runs from the sync hook on every register edit and stops a bad row
reaching `main`; fix what it names and edit again.

Write the row **before** the edit that implements it: the user steers the record, not just the code.
Keep the row's wording the same as the code comment and the tracker comment, so one search finds all
three.

## 5. The tracker

- Offer a one-line tracker comment on the issue citing the id ("Recorded as D107: …"). Writing to the
  tracker is an external step: state what will be posted and wait for the user's go unless they have
  already asked for the tracker update in this conversation.
- For a `proposed`, `in-research` or `deferred` row with no settling issue, search the project's issues
  first and reuse an open issue whose done-when covers the point. Otherwise draft one: title, the open
  question, the options with the recommendation and its date, the id, and a done-when that names the
  decision. Show the draft and wait for the user's go. The link runs both ways: `settled_by` carries the
  identifier and the issue body names the DDR ("Register: D132").

## 6. Report

Report the id(s) with each described in plain words, its status, tags, priority and risk, and what was
superseded. Never report a row by its id alone.

**Example**

Conversation: the user rejects the fade beneath a pinned section heading and asks for the heading to
be solid from the header's edge so released cards are never seen again.

Row written (line wrapped here; it is one line in the file):

```csv
"D99","accepted","frontend","presentation","layout","quote-ui","should","medium","partial","no",
"2026-09-16","The pinned section heading sits at the header's bottom edge, level with its sibling
heading, with a solid background from the header to the docked card top; a released card passes
behind it and is not seen again.","Cards had reappeared above the label through a 16px gap.","A fade
beneath the heading was tried and rejected as fogging.","AI-134","","D62","",""
```

Report: "D99, the pinned section heading sits solid at the header's edge: accepted, presentation /
layout, quote UI, should / medium, built partial in the prototype; supersedes D62, the earlier fade."

## What this skill does not do

It does not make the decision. Record options as `proposed`, then use `grilling` beside
`domain-modeling` when the user wants to settle them. It does not write ADRs or glossary entries
itself, or turn a prototype into a production-readiness claim.
