---
name: task-prioritisation
description: Build the task prioritisation table, one local page listing every open tracker issue and every issue completed in the last week, with status and priority coloured red, amber and green and columns that sort, filter and resize like a spreadsheet; and graduate the feedback rows a stakeholder session marked for building into tracker issues. Use when the user asks to refresh, build or open the task prioritisation table, says their review on it is done, wants the feedback sheet's agreed rows turned into issues, before a prioritisation or triage session, or for a weekly roundup of what each person is working on, what they finished and what comes next.
---

# Task prioritisation

Two sessions share this skill. In the **stakeholder session** the user and the stakeholder walk the feedback sheet and give each row a decision, priority, owner and, for rows with one cause, a shared group; **graduate** then turns the rows marked for building into issues. In the **team review** the team walks the table: every open issue and every issue completed in the last seven days, status reading Open, In progress or Complete and priority High, Medium or Low, each red, amber or green. The user edits priority, owner and the queue on the page and presses Save changes, which downloads one changes file, and **apply** writes it to the tracker.

The project declares its tracker and sheet in `docs/agents/task-prioritisation.json`. When that file does not exist, read [CONFIG-FORMAT.md](CONFIG-FORMAT.md), propose the file to the user from what the tracker and sheet hold, and write it once they agree. The scripts need a Python with `python-dotenv` and, for graduate, `openpyxl`, and run from the project root with `LINEAR_API_KEY` in the project's `.env`.

**On every run, check the queue rule.** If the project's `CLAUDE.md` does not name the config's `queue_label`, read [QUEUED-WORK.md](QUEUED-WORK.md), fill its section for this project, show it to the user and add it to `CLAUDE.md` only on their yes: the file is shared with the team, so it never changes unseen.

## Graduate

Run after the stakeholder session, once the sheet's decision and group cells are filled. Take the workbook's location from `docs/agents/issue-tracker.md`, and ask the user only when it is not there.

1. **Dry run.** Copy the workbook with the shell (`cp`) into `output_dir`, since a shared workbook is often open, and run `python <this skill>/scripts/graduate.py docs/agents/task-prioritisation.json <the copy> --dry-run`. It checks every lookup and prints each issue it would make, or the rows a group joins to an existing issue. Show the user the list. A `KeyError` or `ValueError` names a row to fix in the sheet, such as one to build with no owner: tell the user and stop.
2. **Graduate.** On the user's yes, ask them to close the workbook everywhere, then run the same command on the workbook itself without `--dry-run`. It creates the issues, writes each address into its rows and reads the cells back. A `PermissionError` before any issue is made means someone still holds the file open. Report each issue made and each row linked.

## Refresh and apply

1. **Fetch every issue.** For a Linear project, run `python <this skill>/scripts/fetch_issues.py docs/agents/task-prioritisation.json`. It takes every issue of the config's `linear_project`, open or closed, and writes `issues.json` to `output_dir`. Another tracker needs its own fetch writing the same file: one JSON list of `{"id", "title", "status", "status_type", "completed_at", "assignee", "priority", "milestone", "labels"}`, `null` where there is no value, with Linear's status types (`triage`, `backlog`, `unstarted`, `started`, `completed`, `canceled`, `duplicate`). Done when it prints the count.
2. **Build the table.** Run `python <this skill>/scripts/build_table.py docs/agents/task-prioritisation.json <output_dir>/issues.json`. It keeps open issues and those completed in the last seven days, and drops cancelled and duplicate ones. A `KeyError` names a status or priority the config's maps lack: agree its mapping with the user, add it to the config and run again.
3. **Check and open.** Open `index.html` in `output_dir` and report both scripts' counts.
4. **Apply the review.** When the user says the review is done, take the newest `task-prioritisation-changes*.json` in their Downloads folder (ask where it is if it is not there). Each change names an issue by its `id`, the `field` and its `to` value, where an empty string means none.
   - Update each issue through the tracker: `priority` through the config's `tracker_priority`, `owner` as the assignee, and `queue` by adding the queue label for `"Yes"` or removing it for `"No"`.
   - Move the changes file into `output_dir`, so it is never applied twice, then rebuild the table (steps 1 to 3) and report each change applied. Done when every change in the file is reported as applied.

`output_dir` stays out of git: it holds generated copies of the tracker and the sheet.
