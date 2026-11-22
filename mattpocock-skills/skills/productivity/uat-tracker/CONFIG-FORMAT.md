# docs/agents/uat-tracker.json

The project's description of its UAT feedback sheet. It is committed and shared with the team, so it names every owner and never says which one the current user is: the plan session asks, and the stream's `rewind-durable` file records the answer.

```json
{
  "workbook": "Shared drive: UAT/Feedback.xlsx",
  "output_dir": ".uat-tracker",
  "id_prefix": "ID_",
  "sheet": {
    "tab": "Feedback Log",
    "columns": {
      "id": "UID",
      "date": "Date",
      "tester": "Tester",
      "type": "Type",
      "reference": "Reference",
      "feedback": "Feedback",
      "legacy": "Same issue in legacy?",
      "links": "Links",
      "status": "Status",
      "response": "Response",
      "priority": "Priority",
      "owner": "Assigned to",
      "issue": "Tracker issue"
    }
  },
  "release_notes": { "tab": "Change log", "columns": { "released": "Released", "level": "Major or minor", "change": "Change", "uids": "Feedback UID" } },
  "statuses": { "open": "Open", "in_progress": "In progress", "built": "Built", "closed": "Closed" },
  "priorities": {
    "1": "Wrong or broken: information is incorrect, or something does not work, such as a wrong total or a failing pay button",
    "2": "Seriously harms the shopper's experience, such as a blurred product photo or a form that is hard to complete",
    "3": "A minor imperfection, such as alignment slightly off or a slow page load"
  },
  "owners": {
    "AE": { "name": "Alex Example", "layer": "front end: pages, layout, styling" },
    "SE": { "name": "Sam Example", "layer": "back end: data, rules, everything not front end" }
  },
  "tracker": { "project": "Checkout rebuild", "queue_label": "uat-queue" }
}
```

| Key | Meaning |
| --- | --- |
| `workbook` | Where the team keeps the sheet, as people would find it. Each user's absolute path differs, so the plan session asks for it and records it in the `rewind-durable` file. |
| `output_dir` | A folder in the project for backups and copies. Add it to `.gitignore`: it holds copies of the client's sheet. |
| `id_prefix` | The text before each row's number in its UID cell, so `"ID_"` gives `ID_1`, `ID_2`. An empty string gives bare numbers. A UID cell without it stops the script. |
| `sheet.tab` | The worksheet holding the rows. |
| `sheet.columns` | Each column's header text, exactly as the header row reads, trailing spaces included. The script finds the header row as the first row holding all of them, so columns may move. `reference` holds the record a row is about, such as a booking or order number, and `links` holds links to screenshots. `legacy` is present only for a project replacing an old system: then `new` builds the column and `add` requires its answer. |
| `release_notes` | The change log tab each release's changes go on, and its four headers, in the order they show: when the release went live, Major or Minor, the change in plain words, and the sheet UIDs it answers. `release` adds the tab when the sheet lacks it and keeps it a table filtered to Major. |
| `statuses` | The words the sheet's Status column uses for open, in progress, built and closed. Built means the fix is merged but not yet live where the testers test; closed means live there, or no further action. A blank status counts as open. |
| `priorities` | Each value the Priority column uses, most urgent first, as text, with what it means for this project. A level is set by how much the problem hurts what the product is for, so the same kind of problem can sit at different levels in different projects; the user agrees the meanings at set up. Compare a cell's value as text, since a typed 1 reads back as a number. |
| `owners` | Each owner, keyed by their first and last initials, which are also their code in the sheet and sign their responses, with their name and their layer in words, which decides the unowned rows that fall to them. A team that is not one person gets a short code, such as `SD`. A row with several owners holds their codes comma-separated in alphabetical order, such as `AS, BS`. |
| `tracker` | The project issues are raised in, and the label that marks them as queued work. |
