## What it does

`task-prioritisation` builds one local page that lists every open issue in your tracker beside every row of a stakeholder's feedback sheet that no open issue covers yet. Status reads only Open, In progress or Complete, and priority only High, Medium or Low, each coloured red, amber or green, and the columns sort, filter and resize the way a spreadsheet's do. It is the screen you share on a prioritisation call.

The table shows the tracker and the sheet exactly as they are, and is only ever rebuilt from them. On the call you change priority, owner and the committed queue on the page and press Save changes, which downloads one changes file. When you say the review is done, the agent applies that file: issue changes to the tracker, changes to uncovered sheet rows to the sheet. Then it rebuilds the table, so the page never drifts from either source.

## When to reach for it

Type `/task-prioritisation`, or the agent reaches for it on its own when you ask to refresh or open the table, before a prioritisation or triage session with a stakeholder, or for a weekly roundup of what is in progress and what comes next.

| The situation | Reach for |
| --- | --- |
| You and a stakeholder walk through feedback and open work to choose what comes next | `/task-prioritisation` |
| Raw issues need moving through triage roles one by one | [triage](https://aihero.dev/skills-triage) |
| A decision needs one person's answer, asynchronously | [to-questionnaire](https://aihero.dev/skills-to-questionnaire) |

## Prerequisites

The project declares its tracker and sheet in `docs/agents/task-prioritisation.json`: where the table is written, the tracker's link prefix, the label that marks committed work, how the tracker's statuses and priorities map onto the table's three words each, and which column of the sheet holds which field. When the file is missing, the agent proposes one from what your tracker and sheet hold and writes it once you agree. On Linear, the config also names the project and the project's `.env` holds a personal API key as `LINEAR_API_KEY`, so a script fetches the issues and no agent copies them. The scripts need Python with `openpyxl` and `python-dotenv`, and the output folder must be ignored by git, because a feedback sheet can carry personal data.

## The walk-through

The page is built for a call: the default view sorts by priority with completed work hidden, one tick narrows it to the committed queue, and a click opens a row's full feedback and the response already sent. A value your tracker or sheet uses that the config has no word for stops the build and names it, so a new status is agreed once rather than shown wrongly on screen.

## It's working if

- The call starts from the table, not from scrolling the sheet and the tracker in turn.
- Every red line on screen is one somebody can name an owner for by the end of the call.
- After you say the review is done, the tracker shows the priorities and owners you set on the call, without anyone retyping them.

## Where it fits

A reach-for-it-anytime standalone, run before each prioritisation call and for a weekly roundup. It reads what [triage](https://aihero.dev/skills-triage) and [to-tickets](https://aihero.dev/skills-to-tickets) put in the tracker, and [ask-matt](https://aihero.dev/skills-ask-matt) maps the rest of the set.
