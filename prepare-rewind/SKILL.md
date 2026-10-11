---
name: prepare-rewind
description: Write rewind-status.md — what was built, and every decision the rewind would cut
argument-hint: [the message being rewound to — quote a few words of it]
---

# /prepare-rewind — hand the rewound context everything it is about to lose

Benedict is about to rewind this conversation to save tokens. Your job is to **write
`rewind-status.md` at the top level of the repo**, so the next context picks up without
re-deriving anything.

He does not paste anything. After rewinding he runs `/carry-on-rewind`, which reads that file
and deletes it. So the file IS the handover — if a decision is not in it, it is gone.

The rewind point is the invocation argument — a few words of the message he is going back to,
**if he names one**. Claude expands it below; Pi supplies it in the final `User:` line appended to
this skill.

Claude argument: `$ARGUMENTS`

Everything after that message is about to be discarded, so that is the stretch to comb.

**He often will not name one. Do not ask.** Cover the whole session instead: every decision taken
and where the work stands. Err towards including — a decision restated needlessly costs a line,
where one lost costs an argument you already had.

## What survives without your help — do not restate any of it

- **Global and project context files (`CLAUDE.md` or `AGENTS.md`).** The rewound agent loads the
  same files.
- **Memories.** Same store, same index. If you saved one during this session it survives too — do
  not repeat its content, though you may say it now exists if the work turns on it.
- **Anything above a named rewind point.** He is rewinding *to* that message, so it stays in
  context. Do not summarise the plan he agreed there; he kept it deliberately. With no point named,
  assume nothing survives and cover the session.
- **Committed code, and its commit messages.** Name the commits and let them speak.
- **Anything written to disk** — Linear tickets, records, plan files. Point at them by name and say
  in one line what each holds.

Repeating any of the above wastes the tokens the rewind was for. Be ruthless about it.

## What you must carry across

Walk the conversation — from the rewind point where he named one, otherwise the whole of it — and
pull out:

1. **What was built.** Which commits, and what each one settled. Two lines each at most — the commit
   message is already on disk and the agent will read it.
2. **Where the work actually stopped.** Green or not, committed or dirty, and what is next in the
   agreed order.
3. **Every decision taken.** This is the whole point of the command. Design choices, rejected
   alternatives *and why they lost*, judgement calls you made and flagged, things he ruled out in
   passing. A decision restated without its reasoning gets re-litigated, so give each one a sentence
   of why.
4. **Preferences and corrections he gave in this session** — how he wants you to work, what he
   pushed back on. Skip any that went into memory, which survives; keep the rest.
5. **What is owed.** A record not yet written, a test not yet added, a decision he has not signed off
   on. Say plainly that it is outstanding.

## Durable facts go to rewind-durable.md, not here

Some learnings matter to every session in this series of rewinds, not just the next one: how
Benedict wants the work run, a file to always load, a command never to run again, a rule he set for
the whole ticket. Carried in `rewind-status.md`, such an instruction is rewritten by a fresh agent at
every rewind and drifts. So it goes in `rewind-durable.md` at the repo root instead, which
`/carry-on-rewind` reads whole on every resume and never deletes.

- **The test:** would every future session in this series go wrong without it? If yes, `rewind-durable.md`.
  If it matters only to the next session, `rewind-status.md`. If it matters beyond this repo or
  ticket, memory.
- **Append only.** Add each new durable fact as one dated bullet, quoting Benedict's own words where
  he gave the instruction. Never reword, tidy or summarise an existing entry: copying, not
  regenerating, is what stops the drift.
- **Edit an entry only when he explicitly changes his mind** about it. Then change that entry and
  date the change; do not add a second, contradicting entry.
- Do not restate anything already in `rewind-durable.md` in `rewind-status.md`.
- Create it if it does not exist, and add it to `.gitignore`.
- **When the whole task is done** (the ticket or series of rewinds is finished, not just this
  stretch), ask Benedict whether to delete `rewind-durable.md`. Never delete it without his yes.

## Shape of the file

Write it with the Write tool to `rewind-status.md` at the repo root — never anywhere else, and
never as a fenced block in your reply. Add it to `.gitignore` if it is not already there: it is
scratch that must never reach a commit.

Address it to the next agent, not to Benedict. Structure it roughly:

- One paragraph of state: what is done, what is committed, what is green.
- **DECISIONS LOCKED — do not re-open, do not re-derive**, as a numbered list, each with its reasoning
  and its rejected alternative where there was one.
- **FIRST TASK ON RESUME**, named explicitly, so the agent does not start by asking what to do next.

**Keep it short.** The next agent reads the codebase, the commits and the tickets for itself; this
file exists only for what none of those hold. A screen or so is right; two is the ceiling. Density
comes from cutting what survives elsewhere, never from cutting a decision's reasoning.

## Then

Say in one or two lines what you have carried across, what you appended to `rewind-durable.md`, and what
you have deliberately left out because it survives on its own. Confirm the file is written and tell him he can rewind and run the carry-on command:
`/carry-on-rewind` in Claude or `/skill:carry-on-rewind` in Pi.

If anything is genuinely at risk of being lost that belongs somewhere permanent — a design decision
with no record, an agreement with no ticket — say so and offer to write it down properly first.
`rewind-status.md` is deleted the moment it is read, so it is a worse home for a decision than a
record or a ticket is.
