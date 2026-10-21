---
name: prepare-rewind
description: Write rewind-status.md before a context rewind, carrying what was built and every decision the rewind would cut. Use it when the user says they are about to rewind, or when the context is filling and the handover should be written while there is still room to write it well.
argument-hint: "The message being rewound to: quote a few words of it"
---

# Prepare a rewind

The user is about to rewind this conversation to save tokens. Your job is to **write
`rewind-status.md` at the top level of the repo**, so the next context picks up without
re-deriving anything.

The user does not paste anything. After rewinding they run `/carry-on-rewind`, which reads that file
and deletes it. So the file IS the handover: if a decision is not in it, it is gone.

## Choose the rewind point before writing anything

The rewind point decides what the handover must carry, so choose it first. It is always one of the
user's messages: rewinding to it drops that message and everything after it, and keeps the context
the agent held just before it.

**Run the script.** It reads the session log your harness keeps and lists every message the user sent
on the live branch, with the context in tokens just before each, and an `R` beside any message that
follows a stated rewind point. From this skill's folder:

```bash
cd scripts && python -m rewind_point --agent <claude|codex|pi|opencode> --repo <repo root> --quote "<phrase>" --limit 200000
```

Pass the agent you are running in. `--quote` is a distinctive phrase copied exactly from one of the
user's recent messages in this conversation, never from a command; it picks this session out from any
other running in the same repo. `--limit` is 200,000 unless the user gives another.

**The script also prints `Stream: <name>`**, taken from the session's first message, which no rewind
removes. Use that name exactly and never make one up: in this skill, `rewind-status.md` and
`rewind-durable.md` mean `rewind-status-<name>.md` and `rewind-durable-<name>.md`, so two streams of
work in one repo never share a file.

**If it prints `REWIND POINT FAILED`, stop.** Tell the user the script broke, quote its error, and ask
them to name the message to rewind to. Do the same if your harness is not one of the four. Never pick a
point by hand in its place.

**Then choose, in this order:**

1. **The user named one** (the invocation argument, a few words of their message): use it. Claude Code
   expands it here: `$ARGUMENTS`. Pi supplies it in the final `User:` line appended to this skill.
2. **A rewind point was stated** (the latest `R`): use it, and never go earlier, because the research
   and grilling sit just above it. If its context is over the limit, tell the user and let them choose.
3. **None was stated:** start from the latest message under the limit. Go earlier only where the
   context above the earlier message still holds the research and the answers the work rests on, and
   say why it is better.

**If the message at the limit falls before that research and grilling finished, stop.** Tell the user
the rewind cannot be made there, and give the two choices with their token counts: rewind to a later
message and save less, or rewind there and answer the grilling again.

Everything from the chosen message on is about to be discarded, so that is the stretch to comb. Err
towards including: a decision restated needlessly costs a line, where one lost costs an argument you
already had.

## What survives without your help: do not restate any of it

- **Global and project context files (`CLAUDE.md` or `AGENTS.md`).** The rewound agent loads the
  same files.
- **Memories.** Same store, same index. If you saved one during this session it survives too. Do
  not repeat its content, though you may say it now exists if the work turns on it.
- **Anything above the chosen rewind point.** The user is rewinding *to* that message, so it stays in
  context. Do not summarise the research, the grilling or the plan agreed there; they kept it
  deliberately.
- **Committed code, and its commit messages.** Name the commits and let them speak.
- **Anything written to disk or the tracker**: tracker issues, records, plan files. Point at them by
  name and say in one line what each holds.

Repeating any of the above wastes the tokens the rewind was for. Be ruthless about it.

## What you must carry across

Walk the conversation from the chosen rewind point and pull out:

1. **What was built.** Which commits, and what each one settled. Two lines each at most: the commit
   message is already on disk and the agent will read it.
2. **Where the work actually stopped.** Green or not, committed or dirty, and what is next in the
   agreed order.
3. **Every decision taken.** This is the whole point of the command. Design choices, rejected
   alternatives *and why they lost*, judgement calls you made and flagged, things the user ruled out
   in passing. A decision restated without its reasoning gets re-litigated, so give each one a
   sentence of why.
4. **Preferences and corrections the user gave in this session**: how they want you to work, what
   they pushed back on. Skip any that went into memory, which survives; keep the rest.
5. **What is owed.** A record not yet written, a test not yet added, a decision the user has not
   signed off on. Say plainly that it is outstanding.

## Durable facts go to rewind-durable.md, not here

Some learnings matter to every session in this series of rewinds, not just the next one: how the
user wants the work run, a file to always load, a command never to run again, a rule they set for
the whole ticket. Carried in `rewind-status.md`, such an instruction is rewritten by a fresh agent at
every rewind and drifts. So it goes in `rewind-durable.md` at the repo root instead, which
`/carry-on-rewind` reads whole on every resume and never deletes.

- **The test:** would every future session in this series go wrong without it? If yes, `rewind-durable.md`.
  If it matters only to the next session, `rewind-status.md`. If it matters beyond this repo or
  ticket, memory.
- **A researched fact that changed.** The research above the rewind point is meant to hold for the whole
  session. Where the work changed something it established (a file moved, a field renamed, a finding
  overturned), append a dated entry naming what the research said and what is true now, because the
  rewound context still says the old thing. If the change is large enough that the rewound context would
  mislead, tell the user the rewind point is out of date and recommend researching afresh.
- **Append only.** Add each new durable fact as one dated bullet, quoting the user's own words where
  they gave the instruction. Never reword, tidy or summarise an existing entry: copying, not
  regenerating, is what stops the drift.
- **Edit an entry only when the user explicitly changes their mind** about it. Then change that entry
  and date the change; do not add a second, contradicting entry.
- Do not restate anything already in `rewind-durable.md` in `rewind-status.md`.
- Create it if it does not exist, and make sure `.gitignore` holds the pattern `rewind-durable-*.md`.
- **When the whole task is done** (the ticket or series of rewinds is finished, not just this
  stretch), ask the user whether to delete `rewind-durable.md`. Never delete it without their yes.

## Shape of the file

Write it with the Write tool to `rewind-status.md` at the repo root, never anywhere else, and
never as a fenced block in your reply. Make sure `.gitignore` holds the pattern `rewind-status-*.md`:
the file is scratch that must never reach a commit.

Address it to the next agent, not to the user. Structure it roughly:

- One paragraph of state: what is done, what is committed, what is green.
- **DECISIONS LOCKED: do not re-open, do not re-derive**, as a numbered list, each with its reasoning
  and its rejected alternative where there was one.
- **FIRST TASK ON RESUME**, named explicitly, so the agent does not start by asking what to do next.

**Keep it short.** The next agent reads the codebase, the commits and the tracker issues for itself;
this file exists only for what none of those hold. A screen or so is right; two is the ceiling.
Density comes from cutting what survives elsewhere, never from cutting a decision's reasoning.

## Then

Say in one or two lines what you have carried across, what you appended to `rewind-durable.md`, and what
you have deliberately left out because it survives on its own. Confirm the file is written and tell the
user they can rewind and run the carry-on command: `/carry-on-rewind` in Claude Code or
`/skill:carry-on-rewind` in Pi.

Tell the user exactly where to rewind to: the message chosen above, with its number in the script's
table and the context it keeps. A rewind menu lists only the user's messages, and they send the
carry-on command in place of the chosen one. Name it by its first words, beside the agent message just
above it, in this order: *I said "<first words of the agent's message>", then you said "<first words of
the user's message>". Rewind to your message (number N, keeping about X tokens) and send
`/carry-on-rewind` in its place.* Quote both exactly as written, typos included, so the user can find
theirs in the menu.

If anything is genuinely at risk of being lost that belongs somewhere permanent (a design decision
with no record, an agreement with no tracker issue), say so and offer to write it down properly first.
`rewind-status.md` is deleted the moment it is read, so it is a worse home for a decision than a
record or a tracker issue is.
