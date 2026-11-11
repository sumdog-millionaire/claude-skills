# The config file

`docs/agents/task-prioritisation.json` tells the scripts which tracker project to read, where the table goes, how the tracker's words map onto the table's, and where `graduate.py` finds each field in the feedback sheet. Every key is required, except `linear_project` for a project not on Linear and `sheet` for a project with no feedback sheet.

```json
{
  "output_dir": "data/task_prioritisation",
  "linear_project": "a1b2c3d4e5f6",
  "issue_url_prefix": "https://tracker.example.com/issue/",
  "queue_label": "committed",
  "issue_status": {"Backlog": "Open", "Todo": "Open", "In Progress": "In progress", "In Review": "In progress", "Done": "Complete"},
  "issue_priority": {"Urgent": "High", "High": "High", "Medium": "Medium", "Low": "Low", "No priority": null},
  "tracker_priority": {"High": "High", "Medium": "Medium", "Low": "Low"},
  "sheet": {
    "tab": "Feedback",
    "first_row": 2,
    "columns": {"feedback": 3, "priority": 6, "owner": 7, "issue": 8, "decision": 9, "group": 10},
    "details": {"Date": 1, "Reported by": 2},
    "build": "Build",
    "priority": {"1": "High", "2": "Medium", "3": "Low"},
    "owner": {"AB": "Alex Brown", "SC": "Sam Clarke"}
  }
}
```

| Key | What it holds |
| --- | --- |
| `output_dir` | The folder for `issues.json` and `index.html`, relative to the project root. It must be ignored by git. |
| `linear_project` | The Linear project `fetch_issues.py` reads: its ID, or the short ID at the end of its address (`.../project/checkout-redesign-a1b2c3d4e5f6`). A project on another tracker leaves it out and fetches its issues another way. |
| `issue_url_prefix` | The tracker address an issue's identifier is appended to, so `ENG-134` links to `<prefix>ENG-134`. |
| `queue_label` | The tracker label that marks an issue the team has committed to. The table's queue filter shows these. |
| `issue_status` | Every tracker status of an open or completed issue, mapped to `Open`, `In progress` or `Complete`. Cancelled and duplicate statuses are never shown, so they need no entry. |
| `issue_priority` | Every tracker priority, mapped to `High`, `Medium`, `Low` or `null` for none. |
| `tracker_priority` | The tracker priority to set when the user picks `High`, `Medium` or `Low` on the page. |
| `sheet.tab`, `sheet.first_row` | The worksheet holding the feedback rows, and the first row below its headings. A row with an empty feedback cell is skipped. |
| `sheet.columns` | The 1-based column of each field `graduate.py` reads: the feedback text, its priority, its owner, the linked issue's address (which it writes), the decision, and the group that joins rows into one issue. |
| `sheet.details` | Columns copied into a new issue's body beside each row's feedback, as heading and column number. |
| `sheet.build` | The decision value that sends a row to the tracker. |
| `sheet.priority`, `sheet.owner` | Each value those cells hold, as text (`"1"` for the number 1), mapped to the table's priority word and to the owner's full name in the tracker. A row to build whose value is missing from a map, an empty cell included, stops the run. |

A value missing from either status or priority map stops the build with a `KeyError` naming it, so a new status is agreed and added rather than shown wrongly.
