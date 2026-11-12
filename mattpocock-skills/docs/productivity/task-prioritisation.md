## What it does

`task-prioritisation` builds one local page that lists every open issue in your tracker and every issue completed in the last seven days. Status reads only Open, In progress or Complete, and priority only High, Medium or Low, each coloured red, amber or green, and the columns sort, filter and resize the way a spreadsheet's do. It is the screen you share on a prioritisation call: what each person is on, what they finished, and what comes next.

The table shows the tracker exactly as it is, and is only ever rebuilt from it. On the call you change priority, owner and the committed queue on the page and press Save changes, which downloads one changes file. When you say the review is done, the agent applies that file to the tracker and rebuilds the table, so the page never drifts from it.

Graduate turns every open row of your stakeholder's feedback sheet that has an owner and no issue yet into one, assigned to that owner, and writes each issue's link back into its rows. The agent proposes groups of rows that share a theme and belong in one issue, shows you the plan, and creates nothing until you agree. Whether a row is a data problem or a fix to build is settled when its issue is investigated. The skill also checks that your project's `CLAUDE.md` tells every agent to build only queued issues, and proposes that section if it is missing.

## When to reach for it

Type `/task-prioritisation`, or the agent reaches for it on its own when you ask to refresh or open the table, before a prioritisation or triage session, or for a weekly roundup of what is in progress, what was finished and what comes next.

| The situation | Reach for |
| --- | --- |
| The team walks through open and recently finished work to choose what comes next | `/task-prioritisation` |
| Raw issues need moving through triage roles one by one | [triage](https://aihero.dev/skills-triage) |
| A decision needs one person's answer, asynchronously | [to-questionnaire](https://aihero.dev/skills-to-questionnaire) |

## Prerequisites

The project declares its tracker in `docs/agents/task-prioritisation.json`: where the table is written, the tracker's link prefix, the label that marks committed work, and how the tracker's statuses and priorities map onto the table's three words each. When the file is missing, the agent proposes one from what your tracker holds and writes it once you agree. On Linear, the config also names the project and the project's `.env` holds a personal API key as `LINEAR_API_KEY`, so a script fetches every issue and no agent copies them. For graduate, the feedback sheet needs a status column, which the config names along with the sheet's other columns and the statuses that count as closed. The scripts need Python with `python-dotenv`, and `openpyxl` for graduate, and the output folder must be ignored by git.

## The walk-through

The page is built for a call: the default view sorts by priority, finished work shows its completion date and one tick hides it, another tick narrows the view to the committed queue, and a click opens a line's full title. A status or priority your tracker uses that the config has no word for stops the build and names it, so it is agreed once rather than shown wrongly on screen.

## It's working if

- The call starts from the table, not from scrolling the tracker.
- Every red line on screen is one somebody can name an owner for by the end of the call.
- After you say the review is done, the tracker shows the priorities and owners you set on the call, without anyone retyping them.

## Where it fits

A reach-for-it-anytime standalone, run before each prioritisation call and for a weekly roundup. It reads what [triage](https://aihero.dev/skills-triage) and [to-tickets](https://aihero.dev/skills-to-tickets) put in the tracker, and [ask-matt](https://aihero.dev/skills-ask-matt) maps the rest of the set.
