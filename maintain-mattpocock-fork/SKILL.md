---
name: maintain-mattpocock-fork
description: How to change the mattpocock-skills fork and how to take Matt Pocock's updates into it. Use it when editing anything under mattpocock-skills/ (a skill, a docs page, a README, the plugin manifest, the records scripts or hooks), or taking Matt Pocock's updates, or resolving a conflict from a subtree pull.
---

# Maintain the mattpocock-skills fork

`~/.claude/skills/mattpocock-skills/` is a fork of [`mattpocock/skills`](https://github.com/mattpocock/skills),
kept as a git subtree inside the `~/.claude/skills` repository. It ships as a plugin to any project, so
two things hold at once: it follows upstream's rules as if it were upstream, and it carries a small set
of deliberate additions. Everything below serves one of those two.

## The one rule: nothing project-specific

The fork carries only project-agnostic material. Nothing in it names the user, a client, one
project's paths, one project's dates or examples, or one tracker as *the* tracker. A skill may tell an
agent how to set up a local project (where the register goes, what `docs/agents/domain.md` holds), but
the project's own content (its taxonomy, its records, its rules) lives in that project, never here.
Examples are invented and generic: an invoice, a checkout, `ENG-134`. Upstream's own text naming
Linear as one tracker among several is fine; leave upstream text alone.

Before finishing any change, grep the fork for the user's name, client and product names, absolute
paths, and real ticket identifiers, and make each hit generic.

## Editing the fork

Read upstream's guides first and follow them in everything you write. They live in the fork itself:

- `mattpocock-skills/CLAUDE.md`: buckets, what a promoted skill must have, no em dashes.
- `mattpocock-skills/.agents/writing-docs.md`: the docs page template and its "Done when" list.
- `mattpocock-skills/.agents/invocation.md`: user-invoked versus model-invoked, and how one skill
  calls another.
- `mattpocock-skills/.agents/install-block.md`: the only install wording allowed.

Write in plain English, keep the UK spelling the fork already uses, and use no em dashes and no
spaced hyphens as dashes: rewrite the sentence with a comma, colon, full stop or brackets.

### What every shipped skill has

A skill in `skills/engineering/` or `skills/productivity/` is shipped, and each one has all of:

| Part | Where |
| --- | --- |
| The skill | `skills/<bucket>/<name>/SKILL.md` |
| Codex metadata, matching its invocation | `skills/<bucket>/<name>/agents/openai.yaml` |
| A docs page | `docs/<bucket>/<name>.md`, in the bucket's folder |
| A manifest entry | the `skills` list in `.claude-plugin/plugin.json` |
| Two README entries | the top-level `README.md` and `skills/<bucket>/README.md`, under User-invoked or Model-invoked, in the order the list already uses |
| A place in the router | `skills/engineering/ask-matt/SKILL.md`, if a user can reach it |

A user-invoked skill carries `disable-model-invocation: true` in its front matter and
`policy.allow_implicit_invocation: false` in its `openai.yaml`; a model-invoked one carries neither.

### How skills call each other

An operative step calls the Skill tool by name, one call per skill: `call the Skill tool twice, for
"grilling" and "domain-modeling"`. Never a `../other-skill/FILE.md` link and never a bare `/name` left
for the model to read as a command. A user-invoked skill cannot be called by another skill, so a step
that needs one tells the user to run it (`tell the user to run /prepare-rewind`).

### Every change

1. **Make the change** in the skill.
2. **Re-sync the docs page** of every skill whose behaviour changed, in the same change, following
   `writing-docs.md`. A new skill gets a new page; a renamed one moves its page.
3. **Update the listings**: `plugin.json`, both READMEs and `ask-matt` when a skill is added, renamed,
   removed or changes how it fits the flows. Run `claude plugin validate . --strict` from
   `mattpocock-skills/` after touching a manifest.
4. **Write or widen a changeset** in `.changeset/`: front matter `"mattpocock-skills": patch` (or
   `minor` for a new skill or behaviour), then one paragraph naming what changed. A fork addition
   that is still growing widens its existing changeset (`add-design-decision-ddr.md`) rather than
   adding a second.
5. **Run the checks** after touching anything under `skills/engineering/domain-modeling/scripts/`,
   `taxonomy.json` or the record formats:
   - from a project that keeps records:
     `python ~/.claude/skills/mattpocock-skills/skills/engineering/domain-modeling/scripts/check_records.py docs/ddr/register.csv docs/adr`
   - `python ~/.claude/skills/mattpocock-skills/skills/engineering/domain-modeling/scripts/test_sync_records.py`
6. **Commit from `~/.claude/skills/`**, staging only the paths you changed, with a message that says
   what changed and why.

## Taking Matt Pocock's updates

From `~/.claude/skills/`, with nothing uncommitted under `mattpocock-skills/`:

```bash
git subtree pull --prefix=mattpocock-skills https://github.com/mattpocock/skills.git main --squash
```

The pull works out what upstream changed from the last squash commit's `git-subtree-split:` line, so
that line must name a commit in upstream's repository. Never squash in a copy from any other fork,
however close: a split commit upstream never had makes the pull read upstream as deleting every fork
edit. That happened once, and commit `5dec628` re-anchored the fork on upstream's `f3fc563` to fix it.
Merge upstream's repository and only upstream's.

On a conflict, keep the fork's additions (listed below) and take upstream's text everywhere else.
Where upstream rewrote a passage the fork had amended, take upstream's new passage and re-apply the
fork's amendment to it, rather than keeping the fork's old copy of upstream.

Then:

1. Re-sync the docs page of every skill either side changed, so each page matches its skill.
2. Check every upstream skill the pull added or renamed has its full set of parts (the table above).
3. Widen the fork's changeset if the merge changed what the fork adds.
4. Run the checks above.
5. Commit and `git push`.

## What the fork deliberately adds

These differences from upstream are wanted. Keep them through every pull, and do not report them as
drift:

- **The `design-decision` skill and the DDR register**: decisions below the ADR bar as rows in
  `docs/ddr/register.csv`, with `DDR-FORMAT.md` and `taxonomy.json` in `domain-modeling`. The register
  holds DDRs only; ADRs carry the same tags in their front matter.
- **The records check and the sync hooks**: `domain-modeling/scripts/check_records.py`,
  `sync_records.py` and its test, and `hooks/hooks.json`, which keep a project's records on `main`.
- **Required ADR front matter** (`status`, `date`, `area`, `sub_area`, `project_taxonomy`) in
  `ADR-FORMAT.md`, which the check reads.
- **`domain-modeling` loads first** in any project and reads the glossary and records before code
  (its description, its "Read first" section, and the matching passage in `.agents/invocation.md`).
- **The rewritten `implement` skill**: carry a tracker issue, or the next free ticket in a scope, to
  done; explain and grill first; set a rewind point.
- **The triage sweep** (`/triage sweep`) and the "Keeping the tracker true" sections in the
  tracker templates.
- **Decisions sections** in tickets, specs and agent briefs, naming each binding ADR and DDR.
- **The rewind skills**, `prepare-rewind` and `carry-on-rewind`, in `skills/productivity/`, both
  model-invoked.
- **`grill-with-docs` is model-invoked**, where upstream makes it user-invoked.
- **Fixed default record places**, named in `docs/agents/domain.md` only when a project moves one.
- **DDRs named beside ADRs** throughout upstream's skills (grill-with-docs, to-tickets, to-spec,
  triage, wayfinder, tdd, diagnosing-bugs, improve-codebase-architecture, handoff).
