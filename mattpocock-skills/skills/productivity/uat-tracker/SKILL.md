---
name: uat-tracker
description: Work your share of a client's UAT feedback sheet. Plan your open rows into investigation groups, raise a tracker issue per group, then fix one group per rewind and write each row's status and response back to the sheet.
disable-model-invocation: true
---

# UAT tracker

During user-acceptance testing the client's testers log feedback as rows in a shared spreadsheet, each with a priority and an owner. This skill is how one owner works their share: their open rows become a **worklist** of investigation groups, each group gets one tracker issue, and the groups are worked one per rewind until every row is closed with a response the testers can read.

The sheet is the client's and other people edit it while you work. Read it fresh every time, and let the bundled script be its only writer.

The work is a series of sessions around one **rewind point**, set at the end of planning:

| Session | What it does | Ends with |
| --- | --- | --- |
| Plan | Reads the sheet and agrees the worklist with the user | The rewind point |
| Issues | Raises a tracker issue per group | A rewind to the point |
| Work | Works one group, or several once few remain | A commit and a rewind to the point |

Everything read before the rewind point stays in context for every later session, so planning stays light and the deep research happens inside each group's own session. A session ends by calling the Skill tool with "prepare-rewind"; the user rewinds to the rewind point and resumes with carry-on-rewind.

## The sheet script

`scripts/sheet.py` reads and writes the sheet. The skill is Windows only: run the script from the project root with Excel desktop open and a Python that has `openpyxl` and `pywin32`:

| Command | What it does |
| --- | --- |
| `new <config> <workbook> [--legacy]` | Builds an empty sheet from the config: UID in column A, frozen, grey and locked, the config's columns plus Date, Tester, Type, Reference and Links, dropdowns from its statuses, priorities and owners, a How to use tab and a Names tab. `--legacy` adds "Same issue in legacy?" for a project replacing an old system; ask the user which applies. Refuses if the file exists |
| `rows <config> <workbook> [--open]` | Prints every row as one JSON line: its sheet `row`, UID (`id`), feedback, status, response, priority, owner and issue. `--open` leaves out closed rows |
| `ids <config> <workbook> [--dry-run]` | Gives each row that has feedback and no UID the next one: the config's prefix and one more than the largest number in the column, such as `ID_148`, never reused |
| `add <config> <workbook> --type TYPE --feedback TEXT [--feedback TEXT] [--dry-run]` | Adds one row per feedback text after the last row, dated today, with the type (Bug, Feature request or Question), and gives each its UID. For rows the user agreed in a grilling; testers add their own in Excel |
| `write <config> <workbook> --id UID [--id UID] [--status S] [--priority P] [--owner CODE] [--response TEXT --by INITIALS] [--issue URL] [--dry-run]` | Sets status, priority and owner, adds a response line, links an issue, on each row named by its UID. Priority and owner must be values the config lists |

Name rows by UID everywhere: the `row` number moves whenever someone sorts the sheet, and the UID never does.

Testers edit the sheet while you work, so the script never saves the file itself: replacing the whole file loses whichever edits the cloud copy does not keep. Every command except `new` works through the running Excel, which merges a cell change with co-authors as a person's typing does. It opens the workbook there, or uses it if the user has it open, and refuses a different file of the same name, such as a downloaded copy. A write refuses a cloud workbook with AutoSave off, backs the workbook up to the config's `output_dir` through Excel, prints every cell it sets, sets them, saves, and reads each one back. A response goes on top of the cell as `- 16 Nov, AB - <text>`, newest first, with earlier entries kept below; the script adds the date and initials. Run each write with `--dry-run` first: it prints every cell it would set and sets none. Check that list, then run the same command without it. `new` builds a file nobody has open, so it writes it directly.

A response is one line: what was found and the next step. Anything longer goes in the issue, or in a message drafted for the user to send.

## Set up

When the project has no `docs/agents/uat-tracker.json`, read [CONFIG-FORMAT.md](CONFIG-FORMAT.md), propose the file, and write it on the user's yes.

- **A new sheet.** Agree the owners, priorities and status words with the user, write the config, then run `new` to build the sheet from it. The user puts it where the testers can reach it and adds the testers on its Names tab. Starting from `new` means the sheet always has every column the script reads.
- **An existing sheet.** Take the config from its header row and its owner and priority values.

Either way, ask the user what each priority means for this project and record it in the config. A level is set by how much a problem hurts what the product is for, not by its kind: a low-resolution image can be serious on a luxury brochure and minor on an internal tool. Offer these as a starting point:

| Priority | Meaning | Such as |
| --- | --- | --- |
| 1 | Wrong or broken: information is incorrect, or something does not work | A wrong total, a failing button |
| 2 | Seriously harms the experience the product exists to give | A blurred hero image on a sales page, a form that is hard to complete |
| 3 | A minor imperfection | Alignment slightly off, a slow page load |

A request or question takes the priority of the problem it solves.

The UID column sits first, frozen, so testers can quote a row's UID, and locked, so they cannot type one. `new` builds it that way. An existing sheet without one gets it by hand, because a person changes the layout of a client's sheet and the script only fills cells. Tell the user to:

1. Cut the UID column, or insert a new one headed as the config names it, and insert it at column A with Excel's Insert Cut Cells, which carries the sheet's dropdowns, formats and table with it. A script moving the column would not.
2. Fill the UID cells grey and freeze column A.
3. Give the UID cells a Custom data validation with the formula `=FALSE` and an input message saying it is filled in automatically. Excel then refuses typed entries, while the script, which writes the file directly, and sorting and filtering are unaffected. A paste still gets through; `ids` stops on the duplicate or prefix-less UID that usually leaves.

Sheet protection is the wrong tool here, because Excel will not sort a protected range that holds locked cells.

## Plan

1. **Who and where.** Ask which owner the user is and where the workbook sits on this machine, unless the stream's `rewind-durable` file already records both, and record the answers there. That file sits at the repository root, beside `rewind-status`, named for the stream as `prepare-rewind` describes; create it when it is missing.
2. **Read fresh.** Run `ids` (with `--dry-run` first), then `rows --open`.
3. **Take the user's rows.** A row is open unless its status is the config's closed word, so a blank status is open. The worklist holds the open rows owned by the user's code, plus unowned rows that fit the user's layer as the config describes it, and keeps three lists beside it:
   - **Confirm**: unowned rows whose layer is unclear, to settle in the grilling.
   - **Waiting**: the user's rows whose own part is done and which wait only on another owner's part, and rows at the built status, which wait only on a deploy; each closes once it is live where the testers test.
   - **Others**: each other owner's open row count and their top-priority rows, as a suggestion. A row with halves in two layers sits in the worklist and in its other owner's list.
4. **Order by priority.** Take every row at the top priority, then the next, then the next. Within a priority the order is yours to propose. Raise any row whose priority looks wrong against the config's meanings and say why: the user decides, and only a priority they agree is written, with `write --priority`.
5. **Group for investigation.** Group rows that look like one cause: one issue may cover rows 1, 8 and 22. This is a starting point for investigation, not a build plan. Read the code a row points at, and use at most a couple of subagents.
6. **Grill.** Call the Skill tool with "grilling" and ask as much as the worklist needs, front-loaded: which rows are in, the groups, the order, what waits. Ask in rounds where an answer opens new questions.
7. **Fix the worklist.** Write it in chat as a table: group, row IDs, each row in plain words, priority, any existing issue, and why the rows are grouped. Record it in the `rewind-durable` file. End the message with a line of its own opening `**Rewind point.**`, saying the worklist above holds for the series.

Done when the user has agreed the worklist and the rewind point line is written.

## Issues

The first session after the rewind point. Read [ISSUES.md](ISSUES.md) and follow it.

Done when every group has an issue and `rows` shows each of the group's rows linking it. Then call the Skill tool with "prepare-rewind".

## Work a group

Each later session takes the next group from the worklist in the `rewind-durable` file. Once few rows remain or their causes are plain, offer to take several groups in one session.

1. **Say what the group is about, first.** Your first message on the group, before any tool call that searches, reads code, queries data, opens the group's issue or starts a subagent, tells the user in plain words what each row reports and what goes wrong for the tester, from the worklist alone. A user told what the task is only after the searching cannot steer it. The depth comes later, at step 4.
2. **Flip.** Set the group's rows to the in-progress status.
3. **Investigate.** Read the code, the saved data and how the old system behaved, saying what each step found as it lands. Measure a subagent's inference before recommending on it.
4. **Say the cause.** Explain what happened and why, in depth and in plain words. Before answering a row as cannot-reproduce, check it against the old behaviour yourself. A data problem goes back to the client through the row's response, with no code.
5. **Build.** When the group needs code, call the Skill tool with "implement", handing it the group's issue and the cause from step 4. It explains the fix, grills whatever is still open, records each decision, builds test-first, reviews and commits. The worklist's rewind point stands for the series, so `implement` keeps it and builds the group in one part. A group whose rows are all data problems or answered questions has nothing to build and goes on to step 7.
6. **Ship** as the project's `CLAUDE.md` says: merge, deploy. Report every test failure found, whoever caused it.
7. **Hand over the other halves.** For each part another owner builds, raise a tracker issue or comment on the group's issue, saying what changed and what they need to do, and draft a message for the user to send them.
8. **Answer the rows.** Write each row's response and status. A row moves to the built status once every owner's half is merged, and closes only when every half is live where the testers test; until then it stays in progress with its response. A row answered with no code closes at once.
9. **Close the issue.** When every row in the group is closed, post a short Done / Needed comment on the group's issue and move it to done.
10. **Hand over.** Record in the `rewind-durable` file what the group produced (commits, issues, each row's status), then call the Skill tool with "prepare-rewind".

Done when `rows` reads back each row's status and response as written and the handover is written.
