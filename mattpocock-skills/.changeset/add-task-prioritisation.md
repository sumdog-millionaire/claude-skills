---
"mattpocock-skills": minor
---

Add `task-prioritisation`, a model-invoked productivity skill that builds one local, read-only HTML table of every open tracker issue beside the rows of a stakeholder's feedback sheet that no open issue covers. Status and priority each read three words, coloured red, amber and green, and the columns sort, filter and resize. The project declares its tracker prefix, queue label, word maps and sheet columns in `docs/agents/task-prioritisation.json` (format in `CONFIG-FORMAT.md`), and `scripts/build_table.py` stops on any value the maps lack rather than showing it wrongly. `ask-matt` routes to it for choosing what to work on next with a stakeholder.
