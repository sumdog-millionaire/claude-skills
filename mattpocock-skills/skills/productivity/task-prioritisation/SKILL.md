---
name: task-prioritisation
description: Build the task prioritisation table, one local page listing every open tracker issue beside the rows of a stakeholder's feedback sheet, with status and priority coloured red, amber and green and columns that sort, filter and resize like a spreadsheet. Use when the user asks to refresh, build or open the task prioritisation table, before a prioritisation or triage session with a stakeholder, or for a weekly roundup of what is being worked on and what comes next.
---

# Task prioritisation

The table holds every open issue in the project's tracker, and every row of the feedback sheet that no open issue covers, so a team can walk through what to work on next on one screen. Status reads Open, In progress or Complete and priority High, Medium or Low, each red, amber or green. The table is read-only: decisions taken in a session go to the tracker and the sheet, and the table is rebuilt.

The project declares its tracker and sheet in `docs/agents/task-prioritisation.json`. When that file does not exist, read [CONFIG-FORMAT.md](CONFIG-FORMAT.md), propose the file to the user from what the tracker and the sheet hold, and write it once they agree.

1. **Fetch the open issues.** Read every open issue through the project's tracker, as `docs/agents/issue-tracker.md` says, following every page of results. Keep each issue's identifier, title, status, assignee, priority name, milestone name and labels. Done when every page is read.
2. **Save them.** Write them as one JSON list to `issues.json` in the config's `output_dir`, each as `{"id", "title", "status", "assignee", "priority", "milestone", "labels"}`, with `null` where the tracker gives no value.
3. **Build the table.** From the project root, with a Python that has `openpyxl`, run:

   ```bash
   python <this skill>/scripts/build_table.py docs/agents/task-prioritisation.json "<feedback workbook>" <output_dir>/issues.json
   ```

   Ask the user for the workbook's local path when it is not known. A `KeyError` names a status, priority or owner the config's maps lack: agree its mapping with the user, add it to the config and run again. A `PermissionError` means someone holds the workbook open: ask the user to close it.
4. **Check and open.** Done when the script's issue count equals the number of issues fetched. Open `index.html` in `output_dir` and report both counts.

`output_dir` stays out of git, because a feedback sheet can carry personal data.
