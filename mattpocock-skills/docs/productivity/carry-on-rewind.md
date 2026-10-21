## What it does

`carry-on-rewind` picks the work up after a rewind. You have rewound the conversation to the message where the plan was agreed, so the plan is still in the [context window](https://www.aihero.dev/ai-coding-dictionary/context-window) and everything built after it is not. The skill reads the handover [prepare-rewind](https://aihero.dev/skills-prepare-rewind) wrote, deletes it, reads git to see what was built, lines that up against the plan, and carries on.

It does not re-plan. The plan above it is the reason you rewound to that message, so the skill takes it as settled, takes the handover's locked decisions as settled, and asks you only what neither the handover nor git can answer.

## When to reach for it

Type `/carry-on-rewind` as the message you rewound to, or the agent reaches for it when it finds `rewind-status.md` waiting after a rewind. Reach for it only after a rewind; for a fresh [session](https://www.aihero.dev/ai-coding-dictionary/session) that a handoff file seeds, point the agent at the file instead ([handoff](https://aihero.dev/skills-handoff)).

## Prerequisites

It works best after `/prepare-rewind` has written `rewind-status-<stream>.md` at the repo root, and carries on from git alone if that file is missing. If a `rewind-durable-<stream>.md` is there, it reads that first and never deletes it. The stream name comes from the prepare-rewind script, taken from the session's first message, so two streams of work in one repo never pick up each other's files.

## Four states

It sorts each part of the agreed plan into one of four states, from the commits and the working tree:

| State | What it does |
| --- | --- |
| Done and committed | Leaves it alone |
| Done but uncommitted | Finishes and commits it before anything new |
| Not started | The remaining work |
| Half-applied | Checks it properly: a rename that landed in some files and not others still type-checks and now means the wrong thing |

## It's working if

- Its first reply is two or three lines on where things stand, and then it is working.
- It never asks you to confirm a decision that was in the handover.
- `rewind-status.md` is gone after it runs.

## Where it fits

`carry-on-rewind` is the second half of a pair inside a long build. [prepare-rewind](https://aihero.dev/skills-prepare-rewind) writes the handover before the rewind; this skill reads it after. [implement](https://aihero.dev/skills-implement) names the rewind point both of them work from. [ask-matt](https://aihero.dev/skills-ask-matt) places the pair among the options at a phase boundary.
