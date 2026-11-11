---
name: task-prioritisation
description: Build the task prioritisation table, one local page listing every open tracker issue beside the rows of a stakeholder's feedback sheet, with status and priority coloured red, amber and green and columns that sort, filter and resize like a spreadsheet. Use when the user asks to refresh, build or open the task prioritisation table, says their review on it is done, before a prioritisation or triage session with a stakeholder, or for a weekly roundup of what is being worked on and what comes next.
---

# Task prioritisation

The table holds every open issue in the project's tracker, and every row of the feedback sheet that no open issue covers, so a team can walk through what to work on next on one screen. Status reads Open, In progress or Complete and priority High, Medium or Low, each red, amber or green. In the session the user edits priority, owner and the queue on the page and presses Save changes, which downloads one changes file; when they say the review is done, step 5 applies it to the tracker and the sheet.

The project declares its tracker and sheet in `docs/agents/task-prioritisation.json`. When that file does not exist, read [CONFIG-FORMAT.md](CONFIG-FORMAT.md), propose the file to the user from what the tracker and the sheet hold, and write it once they agree.

The scripts need a Python with `openpyxl` and `python-dotenv`, and run from the project root.

1. **Fetch the open issues.** For a Linear project, run `python <this skill>/scripts/fetch_issues.py docs/agents/task-prioritisation.json`. It reads `LINEAR_API_KEY` from the project's `.env`, takes every issue of the config's `linear_project` whose status is not completed, cancelled or duplicate, and writes `issues.json` to `output_dir`. Another tracker needs its own fetch writing the same file: one JSON list of `{"id", "title", "status", "assignee", "priority", "milestone", "labels"}`, `null` where there is no value. Done when it prints the count.
2. **Build the table.** Copy the feedback workbook with the shell (`cp`) to `sheet.xlsx` in `output_dir`: a shared workbook is often open during a session, and the shell can copy it when Python cannot open it. Take the workbook's location from `docs/agents/issue-tracker.md`, and ask the user only when it is not there. Then run:

   ```bash
   python <this skill>/scripts/build_table.py docs/agents/task-prioritisation.json <output_dir>/sheet.xlsx <output_dir>/issues.json
   ```

   A `KeyError` names a status, priority or owner the config's maps lack: agree its mapping with the user, add it to the config and run again.
3. **Check and open.** Done when the script's issue count equals the number of issues fetched. Open `index.html` in `output_dir` and report both counts.
4. **Apply the review.** When the user says the review is done, take the newest `task-prioritisation-changes*.json` in their Downloads folder (ask where it is if it is not there). Each change names an issue (`"kind": "issue"`, with its `id`) or a sheet row (`"kind": "row"`, with its `row`), the `field` and its `to` value, where an empty string means none.
   - For each issue change, update the issue through the tracker: `priority` through the config's `tracker_priority`, `owner` as the assignee, and `queue` by adding the queue label for `"Yes"` or removing it for `"No"`.
   - Run `python <this skill>/scripts/apply_sheet_changes.py docs/agents/task-prioritisation.json "<feedback workbook>" "<changes file>"` for the sheet-row changes; it writes each into its cell and reads it back. A `PermissionError` means someone holds the workbook open: ask the user to close it, then run again.
   - Move the changes file into `output_dir`, so it is never applied twice, then rebuild the table (steps 1 to 3) and report each change applied. Done when every change in the file is reported as applied.

`output_dir` stays out of git, because a feedback sheet can carry personal data.
