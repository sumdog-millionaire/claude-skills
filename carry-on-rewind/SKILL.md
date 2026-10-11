---
name: carry-on-rewind
description: Re-orient after a context rewind and continue the work already agreed
---

# Carry on

The conversation you are reading has been **rewound** to save tokens. Benedict does this once a
chunk of work is done and committed, rewinding to a point where the two of you had just finished
agreeing what to build.

So the plan is **already above you in this conversation** — that is why he rewound to here. Do not go
hunting for it in plan files, and do not re-plan it. Take it as settled.

What is missing is everything that happened *after* that agreement: the work you then did. Some or
all of it is already on disk and committed, and none of it is in your context.

## 0. Read rewind-durable.md whole, and keep it

If `rewind-durable.md` exists at the top level of the repo, read all of it first. It holds the durable
facts for this whole series of rewinds — how Benedict wants the work run, files to always load,
things never to run again — each in his own words. They bind every session. **Never delete it**,
and never reword it; `/prepare-rewind` only appends to it, or edits an entry when he explicitly
changes his mind.

If it looks unrelated to the work above — another ticket, a finished series, nothing in it touching
this task — do not act on it. Stop and ask Benedict whether to delete it and rewind again, saying in
one line why it looks unrelated. Delete it only on his yes.

## 1. Read rewind-status.md next, then delete it

Before git, before anything else: read `rewind-status.md` at the top level of the repo. The
prepare-rewind skill wrote it in the messages that have just been discarded, and it holds the one
thing git cannot —
**every decision taken in that stretch, with its reasoning and its rejected alternatives**.

Read it whole. Then **delete the file** — it is scratch, it goes stale the moment you act on it,
and a second rewind writes a fresh one.

```bash
rm rewind-status.md
```

Treat what it says as settled. Its "DECISIONS LOCKED" list is exactly the set of arguments already
had: do not re-open one, do not re-derive one, and do not ask Benedict to confirm one. Its "FIRST
TASK ON RESUME" is what you do once you have oriented yourself below.

If the file is not there, carry on regardless — it only exists when `/prepare-rewind` ran.

## 2. Find out what you already built

Git is the only record of what happened in the gap, so start there and nowhere else.

```bash
git log --oneline -20
git status
git diff HEAD~1        # go further back to cover every commit since the plan above
```

Read the commit messages properly — they say what changed and why. If the working tree is dirty,
that uncommitted diff is where you stopped mid-task, and it is the most useful thing on screen.

## 3. Line it up against the plan above

Walk the agreed plan and mark each part:

- **Done and committed** — leave it alone. Do not re-do it, do not re-verify it out of habit.
- **Done but uncommitted** — finish it and commit it before starting anything new.
- **Not started** — this is the remaining work.
- **Half-applied** — a rename that landed in some files and not others, a test written but never
  run, a call site missed. The dangerous category: it still type-checks and now means the wrong
  thing. If the diffs suggest one, check it properly.

If the commits genuinely do not tell you what state something is in, use the harness's available
read-only scout agent to look rather than reading half the repo into this context — keeping this
context small is the entire point of the rewind. Use a task scout in Claude or a codebase explorer
in Pi.

## 4. Then carry on

Default to just continuing. Say in two or three lines where things stand and what you are doing
next, then do it.

Ask only what neither `rewind-durable.md`, `rewind-status.md` nor git can answer — something the two of you settled in
the messages that were discarded, that left no trace in the status file, the code or the tickets.
Ask it in prose, with your recommendation. Never ask him to re-confirm a decision the code or the
status file already embodies, and never invent one you cannot find evidence for.
