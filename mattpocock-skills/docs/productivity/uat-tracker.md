## What it does

`uat-tracker` is how one owner works their share of a client's user-acceptance testing sheet: the spreadsheet where testers log feedback rows, each with a priority and an owner. It turns your open rows into a worklist of groups, raises one tracker issue per group, then works the groups through to fixes, writing each row's status and a one-line, dated response back so the testers can see where things stand.

The sheet stays the client's. Other people edit it while you work, so the skill reads it fresh every time and writes to it only through a bundled script. The script changes cells through the Excel open on your machine, so its edits merge with the testers' as a person's typing does, instead of saving over the file and losing theirs. It backs the sheet up, prints every cell it will set, adds responses newest first without touching earlier ones, and reads each cell back. Planning is kept deliberately light, because everything read before the rewind point is carried into every later session's [context window](https://www.aihero.dev/ai-coding-dictionary/context-window).

## When to reach for it

You invoke this by typing `/uat-tracker`, and the agent won't reach for it on its own. Reach for it when testing has produced a feedback sheet and you want to work through the rows that are yours.

| The situation | Reach for |
| --- | --- |
| Your rows of a client's UAT feedback sheet need planning, raising as issues and fixing | `/uat-tracker` |
| The team walks through every open tracker issue to choose what comes next | [task-prioritisation](https://aihero.dev/skills-task-prioritisation) |
| Raw tracker issues need moving through triage roles one by one | [triage](https://aihero.dev/skills-triage) |

## Prerequisites

The project describes its sheet in `docs/agents/uat-tracker.json`: the tab, each column's header, the status words, each priority value and what it means for the project, every owner's code, name, initials and layer, and the tracker project and queue label. When it is missing, the agent proposes one, from the sheet's header row when the sheet exists, and writes it once you agree. A new project can start from the script's `new` command, which builds an empty sheet from that file with every column the script reads. The sheet needs an ID column first, frozen and locked against typing; `new` builds it that way, and an existing sheet gets it by hand once. The script numbers new rows itself. The skill is Windows only: the script needs Excel desktop open and Python with `openpyxl` and `pywin32`, and its output folder, which holds backups of the sheet, must be ignored by git.

## The worklist and the rewind point

The series runs around one rewind point. The plan session reads the sheet, takes your open rows (yours by owner code, plus unowned rows that fit your layer), orders them by the sheet's priority column, proposes a new priority for any row that looks wrong against the agreed meanings and writes the ones you accept, groups the ones that look like one cause for investigation, and grills you on the lot. It ends by writing the worklist in chat and setting the rewind point. The next session raises the issues; each one after works one group, or several once few remain, and ends in a commit and a rewind back to that same point. Each group's session opens by telling you, in plain words, what each tester asked for, before the agent searches or reads any code, so you can steer the investigation; the detailed cause follows once it is found. A script the agent writes to investigate goes in the project's scripts folder under the topic it touches, named for what it shows rather than for a group or row. The groups are a starting point for investigation rather than a build plan: deep research happens inside each group's session, where it is discarded by the next rewind, not before the point, where it would be carried forever.

## Common questions

**Why does the sheet need an ID column?**
Row numbers move whenever someone filters or sorts the sheet, and feedback text can repeat. An ID the script writes once, one more than the largest already there, never moves and never repeats, and nobody has to type it.

**Can a response @-mention someone so they get a notification?**
No. A mention notifies only when a signed-in person posts it as a comment in Excel; text written into a cell does nothing. A response that needs someone's attention gets a message drafted for you to send.

## It's working if

- Testers read a short, dated answer on every row they raised, newest on top.
- Each group has one issue, and every row in it links that issue.
- Sessions after the first start from the worklist without re-reading the sheet's history or re-asking what was agreed.
- A row moves to built once every owner's part of it is merged, and closes only once every part is live where the testers test.

## Where it fits

A series-long workflow for the testing phase of a project, run once per series of sessions. Once a group's cause is known, its fix goes to [implement](https://aihero.dev/skills-implement), which explains it, grills what is open, builds it test-first, reviews and commits, keeping the worklist's rewind point; `uat-tracker` keeps the sheet, the issues and the handovers. The series leans on [prepare-rewind](https://aihero.dev/skills-prepare-rewind) and [carry-on-rewind](https://aihero.dev/skills-carry-on-rewind) to move between sessions, and [ask-matt](https://aihero.dev/skills-ask-matt) maps the rest of the set.
