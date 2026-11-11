# The config file

`docs/agents/task-prioritisation.json` tells the build script where the table goes, how the tracker's words map onto the table's, and where each field sits in the feedback sheet. Every key is required.

```json
{
  "output_dir": "data/task_prioritisation",
  "issue_url_prefix": "https://tracker.example.com/issue/",
  "queue_label": "committed",
  "issue_status": {"Backlog": "Open", "Todo": "Open", "In Progress": "In progress", "In Review": "In progress", "Done": "Complete"},
  "issue_priority": {"Urgent": "High", "High": "High", "Medium": "Medium", "Low": "Low", "No priority": null},
  "sheet": {
    "tab": "Feedback",
    "first_row": 2,
    "columns": {"feedback": 3, "status": 4, "response": 5, "priority": 6, "owner": 7, "issue": 8},
    "status": {"": "Open", "Open": "Open", "In progress": "In progress", "Closed": "Complete"},
    "priority": {"": null, "1": "High", "2": "Medium", "3": "Low"},
    "owner": {"": null, "AB": "Alex", "SC": "Sam"}
  }
}
```

| Key | What it holds |
| --- | --- |
| `output_dir` | The folder for `issues.json` and `index.html`, relative to the project root. It must be ignored by git. |
| `issue_url_prefix` | The tracker address an issue's identifier is appended to, so `ENG-134` links to `<prefix>ENG-134`. A sheet cell holding a full issue address is read back to its identifier by removing this prefix. |
| `queue_label` | The tracker label that marks an issue the team has committed to. The table's "Queue only" filter shows these. |
| `issue_status` | Every tracker status an open issue can have, mapped to `Open`, `In progress` or `Complete`. |
| `issue_priority` | Every tracker priority, mapped to `High`, `Medium`, `Low` or `null` for none. |
| `sheet.tab` | The worksheet that holds the feedback rows. |
| `sheet.first_row` | The first row below the headings. A row with an empty feedback cell is skipped. |
| `sheet.columns` | The 1-based column number of each field: the feedback text, its status, the response written back, its priority, its owner, and the linked issue's address. |
| `sheet.status`, `sheet.priority`, `sheet.owner` | Each value the sheet's cells hold, written as text (`""` for an empty cell, `"1"` for the number 1), mapped to the table's word. |

A value missing from any map stops the build with a `KeyError` naming it, so a new status or owner is agreed and added rather than shown wrongly.
