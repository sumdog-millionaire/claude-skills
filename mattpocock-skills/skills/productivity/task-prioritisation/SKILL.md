---
name: task-prioritisation
description: Build the task prioritisation table, one local page listing every open tracker issue and every issue completed in the last week, with status and priority coloured red, amber and green and columns that sort, filter and resize like a spreadsheet. Use when the user asks to refresh, build or open the task prioritisation table, says their review on it is done, before a prioritisation or triage session, or for a weekly roundup of what each person is working on, what they finished and what comes next.
---

# Task prioritisation

The table holds every open issue in the project's tracker and every issue completed in the last seven days, so a team can see on one screen what each person is working on, what they finished and what comes next. Status reads Open, In progress or Complete and priority High, Medium or Low, each red, amber or green. In the session the user edits priority, owner and the queue on the page and presses Save changes, which downloads one changes file; when they say the review is done, step 4 applies it to the tracker.

The project declares its tracker in `docs/agents/task-prioritisation.json`. When that file does not exist, read [CONFIG-FORMAT.md](CONFIG-FORMAT.md), propose the file to the user from what the tracker holds, and write it once they agree.

The scripts need a Python with `python-dotenv`, and run from the project root.

1. **Fetch every issue.** For a Linear project, run `python <this skill>/scripts/fetch_issues.py docs/agents/task-prioritisation.json`. It reads `LINEAR_API_KEY` from the project's `.env`, takes every issue of the config's `linear_project`, open or closed, and writes `issues.json` to `output_dir`. Another tracker needs its own fetch writing the same file: one JSON list of `{"id", "title", "status", "status_type", "completed_at", "assignee", "priority", "milestone", "labels"}`, `null` where there is no value, with Linear's status types (`triage`, `backlog`, `unstarted`, `started`, `completed`, `canceled`, `duplicate`). Done when it prints the count.
2. **Build the table.** Run `python <this skill>/scripts/build_table.py docs/agents/task-prioritisation.json <output_dir>/issues.json`. It keeps open issues and those completed in the last seven days, and drops cancelled and duplicate ones. A `KeyError` names a status or priority the config's maps lack: agree its mapping with the user, add it to the config and run again.
3. **Check and open.** Open `index.html` in `output_dir` and report both scripts' counts.
4. **Apply the review.** When the user says the review is done, take the newest `task-prioritisation-changes*.json` in their Downloads folder (ask where it is if it is not there). Each change names an issue by its `id`, the `field` and its `to` value, where an empty string means none.
   - Update each issue through the tracker: `priority` through the config's `tracker_priority`, `owner` as the assignee, and `queue` by adding the queue label for `"Yes"` or removing it for `"No"`.
   - Move the changes file into `output_dir`, so it is never applied twice, then rebuild the table (steps 1 to 3) and report each change applied. Done when every change in the file is reported as applied.

`output_dir` stays out of git: it holds generated copies of the tracker.
