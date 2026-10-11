---
name: design-decision
description: Record proposed, in-research and accepted decisions that fall below the ADR bar as DDRs (design decision records) - numbered, dated, statused rows tagged by layer, aspect, priority and risk in the project's design decision register, a filterable CSV - before implementation, for prototype and production alike. Use this whenever a rule is settled in conversation that an engineer would otherwise get wrong, however small - layout, alignment, motion, colour, copy placement, disclosure behaviour, a module boundary, a swappable library, a logging or data-handling rule - and whenever the user says "record that", "design note", "make that a decision", "D-row", "DDR", "add it to the register", "put this in for prod", or closes a grilling question with a choice. Run it beside domain-modeling in every grilling; also use it when a review round (users, client stakeholders, the product owner) produces accepted changes that need writing down before they are built.
---

# Design decision

A design decision is any rule an engineer building the same thing from the same inputs would
otherwise get wrong: "the section heading pins level with its sibling heading", "prompt construction
never makes calls", "retries use the stdlib, not a library". These rules are too small and too
reversible for an ADR, yet losing one means the production build quietly differs from what was
agreed. So each becomes a row in the project's **design decision register**, a CSV. A row is a DDR, a
design decision record: the counterpart of an ADR (architecture decision record) for everything below
the ADR bar, with a `D99` identifier.

A DDR carries the same fields an ADR does, so there is one format to learn, and the two differ in one
test:

> **An ADR is a decision you would pay to undo. A DDR is one you would just change.**

Breadth is not the test. A narrow, specific choice can be irreversible and wants an ADR; a decision
as wide as a whole visual language can be reversed in an afternoon and wants a row.

The register is a CSV because its value is in being filtered: every unbuilt `must`, every `high` risk
row, everything waiting on one tracker issue, in one sort. Accepted rules apply to both prototype and
production unless explicitly limited. The tracker tracks delivery; a built experiment or passing test
is not acceptance of a rule.

The columns, vocabularies and weights live in
[DDR-FORMAT.md](../domain-modeling/DDR-FORMAT.md). Read it before writing a row.

## Project declaration

The skill is the method; each project supplies the places. The project's `CLAUDE.md` (or `AGENTS.md`)
names, under a "Design decisions" heading:

- the **register** file that holds the rows, by convention `docs/ddr/register.csv`;
- the **values file** for measured values (tokens, components, motion constants), such as `DESIGN.md`;
- the **glossary** for terms, such as `GLOSSARY.md`;
- the **ADR folder**, such as `docs/adr/`;
- the **tracker** and where its conventions live, such as Linear via `docs/agents/issue-tracker.md`.

If any of the five is missing, stop and ask the user where it lives before writing anything. Do not
assume a path, and do not create a register without their go. When a project has no register yet,
offer to create `docs/ddr/register.csv` with the columns in DDR-FORMAT.md, and wait for the answer.

## Companion skills

- **Explicit invocation:** when the user invokes this skill by name, load both `grilling` and
  `domain-modeling` before recording decisions. Use grilling for unresolved choices and
  domain-modeling for terminology and ADR routing. Loading them does not require asking questions
  whose answers are already established.
- **Automatic invocation:** normally load both companions too. They may be skipped only when the
  available context unambiguously supplies every column of the row with no unresolved choice or
  terminology conflict. If uncertain, load both.

## Decision status

The proposed/accepted lifecycle that ADRs use, with an explicit `status` on every row:

| Status | Meaning |
|---|---|
| `proposed` | A suggestion or option awaiting the user's decision; not a build instruction |
| `in-research` | The user has agreed the point matters but a fact must be found before they can decide; a named tracker issue owns the investigation and the row becomes `proposed` or `accepted` when it closes |
| `accepted` | The user has agreed the rule; it may still be unimplemented, blocked or untested |
| `rejected` | The user declined it; retain the reason so it is not proposed again without new evidence |
| `deferred` | The user explicitly postponed the decision, not merely its implementation |
| `superseded` | A later accepted row replaces it; `superseded_by` names that row |

Promote a proposal only on explicit acceptance, recording who accepted it and when. Preserve its id.
Implementation, silence, a meeting suggestion or a recommendation inside an issue cannot promote it.
An accepted provisional default remains accepted but names what can change.

## 1. Route it

Decide where the thing belongs before writing anything. One place per decision; the others only point.

| It is | Home | Test |
|---|---|---|
| A rule about what is built, shown or done, that you would just change | Row in the register | Would someone build it differently without it? |
| A measured value realising a rule (16px, a hex colour, 0.7s, `grayscale(1)`) | The values file | Is it a number or a code, not a rule? The row states the rule; the values file carries the value |
| A term | The glossary, via `domain-modeling` | Is it vocabulary, not a choice? |
| A decision you would pay to undo | ADR in the ADR folder, via `domain-modeling`; the row becomes gist plus the ADR named in `adrs` | Would undoing it cost real money or time? |

Most decisions are rows. When one also qualifies as an ADR, write the ADR and leave a one-line
pointer row naming it; never two full write-ups. A decision needing a page of argument has failed the
reversibility test: it is an ADR, not a long row.

## 2. Gather the row's parts

Use the conversation and dated source records, not inferred intent from code. Capture unresolved
options as `proposed` rather than losing them or choosing for the user. If a reason or source is
missing during a retrospective audit, say it was not recorded and leave the column empty; never
invent one to fill a cell. Ask only where the missing information prevents an accurate rule or
acceptance status. The decision remains the user's.

- **`status`**, with prototype-only, production-only or provisional limits stated in the `decision`
  text. Keep implementation and verification status in the tracker.
- **`layer`** and **`aspect`**, one value each from the two independent vocabularies in DDR-FORMAT.md.
  The layer is where the code that realises the rule lives; the aspect is what kind of rule it is, so
  cross-cutting concerns pair with any layer (`backend` + `security`, `frontend` + `security`). A rule
  in two layers is two rows, or `system`. A value outside the vocabulary means ask, not invent.
- **`priority`** and **`risk`**. Priority is how vital the feature is (`must`, `should`, `could`); risk
  is the cost of building it wrong (`high`, `medium`, `low`) and sets how much care implementation
  gets. They differ often, so weigh them separately.
- **`built_prototype`** and **`built_production`**, each `yes`, `partial` or `no`, independent. A new
  row is normally `no` and `no`; a rule scoped to one surface says so in its text. After the
  implementing edit, flip that column to `partial` in the same change and give the code a comment
  carrying the id so the column can be audited by grep. `yes` is the user's alone: write it only when
  they have checked the built result against the rule and said so, and add "signed off <surface>
  <date>" to `why`. Built is not acceptance.
- **`decided`**, the date in ISO form.
- **`decision`**, the rule in one or two plain present-tense sentences, no implementation detail
  beyond what the rule needs ("pins at the header's bottom edge", not `position: sticky; top: 72px`).
  One rule per row: if it runs past about 600 characters it is several rules and wants splitting.
- **`why`**, the observation or trade-off that produced it, in one or two sentences.
- **`alternatives`**, what was seriously considered and rejected, and why. Empty when there was no
  real alternative.
- **`tracker_issue`**, where the discussion happened, by identifier (`AI-134`). Recommendations inside
  the tracker carry a date because they go stale.
- **`settled_by`**, for every `proposed`, `in-research` or `deferred` row: the tracker issue that will
  look into the point and settle it. A row with no issue to settle it is a decision nobody owns, so if
  none exists one is created (step 5) before the row is written. The register records the rule; the
  issue carries the investigation and the answer.
- **`supersedes`** and **`superseded_by`**, ids only.
- **`adrs`**, any related ADR by identifier.

## 3. Check the register first

Filter the register for the nouns in the rule (the element, the module, the data field). Three
outcomes:

- **Already recorded**: say so, cite the id, write nothing.
- **Accepted replacement conflicts with a row**: supersede it. A proposal does not replace an accepted
  rule. Set the old row's `status` to `superseded` and its `superseded_by` to the new id, leave its
  `decision` text as written, and list it in the new row's `supersedes`. Supersession is data: do not
  strike text through or fold "superseded by" wording into the prose.
- **New**: write it.

Also check the project's `CLAUDE.md` and ADR folder. Record an unresolved conflict as `proposed` or as
an explicit production gate; flag it to the user rather than silently changing those constraints. A
prototype exception is not a production exemption. A broad review is a filter over the register, not a
second copy of its rules; include unimplemented decisions and rejected alternatives.

## 4. Number and write

Read the register immediately before writing; preserve newer decisions from other sessions. The next
number is the highest existing id plus one. Append the row at the end of the file. Seventeen columns
in the order given in DDR-FORMAT.md, **every field double-quoted without exception**, so a comma or a
newline inside a cell can never shift the columns. Keep existing ids when changing status.

A proposed row names its proposer and proposal date, not an invented approver. Record acceptance or
rejection with its date when it happens. Run the project's validator (by convention
`scripts/ddr/check.py`) after editing: it catches a duplicate id, a value outside a vocabulary, a
successor pointing at nothing and a settling issue that is missing. A failed exact-match edit means
reread and reconcile, not overwrite the newer file.

Write the row **before** the edit that implements it, with the same standing as explaining an edit
before making it: the user steers the record, not just the code. Keep the row's wording the same as
the code comment and the tracker comment that follow it, so one search finds all three. After the
implementing edit, flip that surface's built column to `partial` in the same change; `yes` waits for
the user's sign-off.

## 5. Values and the tracker

- If the decision fixes a value, put the value in the values file in the section that owns it
  (spacing, colour, motion, components) and cite the id there.
- Offer a one-line tracker comment on the issue citing the id ("Recorded as D107: …"). Writing to the
  tracker is an external step: state what will be posted and wait for the user's go unless they have
  already asked for the tracker update in this conversation.
- For a `proposed`, `in-research` or `deferred` row with no settling issue, search the project's issues
  first with the rule's nouns and reuse an open issue whose done-when covers the point. Otherwise
  draft one: title, the open question, the options with the recommendation and its date, the id, and a
  done-when that names the decision. Label it per the project's tracker conventions. Show the draft
  and wait for the user's go before creating it. The link runs both ways: `settled_by` carries the
  identifier and the issue body names the DDR ("Register: D132"), added once the id exists.

## 6. Report

Report the id(s), status, layer, aspect, priority and risk, where any values went and what was
superseded. In a retrospective pass, distinguish accepted rules, proposals and unresolved production
gates from implementation work.

**Example**

Conversation: the user rejects the fade beneath a pinned section heading and asks for the heading to
be solid from the header's edge so released cards are never seen again.

Row written (line wrapped here; it is one line in the file):

```csv
"D99","accepted","frontend","interaction","should","medium","partial","no","2026-09-16",
"The pinned section heading sits at the header's bottom edge, level with its sibling heading, with a
solid background from the header to the docked card top; a released card passes behind it and is not
seen again.","Cards had reappeared above the label through a 16px gap.","A fade beneath the heading
was tried and rejected as fogging.","AI-134","","D62","","ADR-0007"
```

Report: "D99 written, frontend/interaction, should/medium, built partial in the prototype and no in
production pending sign-off; no value change; supersedes D62, whose row is now marked superseded."

## What this skill does not do

It does not make the decision. Record options as `proposed`, then use `grilling` beside
`domain-modeling` when the user wants to settle them; do not implement them as accepted. It does not
write ADRs or glossary entries itself, or turn a prototype into a production-readiness claim.
