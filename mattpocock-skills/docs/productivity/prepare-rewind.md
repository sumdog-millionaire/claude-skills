## What it does

`prepare-rewind` writes the **handover** for a rewind. You are about to rewind the conversation to an earlier message to save tokens, and everything after that message is about to leave the [context window](https://www.aihero.dev/ai-coding-dictionary/context-window). The skill combs that stretch and writes `rewind-status.md` at the repo root: what was built, where the work stopped, and every decision taken, each with its reasoning and the alternative that lost.

It carries only what nothing else holds. The rewound agent still loads `CLAUDE.md`, memory, the commits and the tracker, and still has every message above the rewind point, so the file names those and never restates them. What it keeps in full is the reasoning behind each decision, because a decision without its why gets argued again.

## When to reach for it

Type `/prepare-rewind`, or the agent reaches for it on its own when you say you are about to rewind or its context is filling. Pass a few words of the message you are rewinding to; with none, it chooses one before writing anything, as below.

| The situation | Reach for |
| --- | --- |
| A part of a build is committed and the context is filling, and your [harness](https://www.aihero.dev/ai-coding-dictionary/harness) can rewind to an earlier message | `/prepare-rewind`, then rewind, then [carry-on-rewind](https://aihero.dev/skills-carry-on-rewind) |
| The work has to travel to another harness, directory or person | [handoff](https://aihero.dev/skills-handoff) |
| The harness cannot rewind | `/compact` |

## Prerequisites

It writes two files at the repo root and adds both to `.gitignore`: `rewind-status.md`, read once and deleted on resume, and `rewind-durable.md`, which holds the facts every session in a series of rewinds needs (how you want the work run, a command never to run again) and is only ever appended to. When the work changes something the research above the rewind point established, it appends that too, because the rewound context still says the old thing.

## Locked decisions

The file's centre is a **DECISIONS LOCKED** list. Each entry is a decision from the discarded stretch, with the reason it was taken and the option it beat. The next agent treats the list as settled and does not ask you to confirm any of it. The file ends with a **FIRST TASK ON RESUME**, so the next agent starts working instead of asking what to do.

## Where to rewind to

The rewind point decides what the handover must carry, so the skill chooses it first. A script in `scripts/rewind_point/` reads the session log your harness already keeps (Claude Code, Codex, Pi or opencode) and lists each of your messages with the context in [tokens](https://www.aihero.dev/ai-coding-dictionary/token) just before it. It needs only Python's standard library.

- A message you name wins.
- Otherwise it takes the rewind point [implement](https://aihero.dev/skills-implement) stated, a line opening `**Rewind point.**`, and never goes earlier, because the research and grilling sit just above it.
- Otherwise it starts from your latest message under 200,000 tokens, and goes earlier only when the context above still holds the research the work rests on.
- If that message falls before the research and grilling finished, it stops and offers two choices with their token counts: rewind later and save less, or rewind there and answer the grilling again.

If the script breaks, it prints `REWIND POINT FAILED` with the error, and the agent tells you and asks you to name the message rather than guessing one.

A rewind menu shows only your messages, so the skill names the one to pick by its first words, beside the agent's message just above it: *I said "...", then you said "...". Rewind to your message (number N, keeping about X tokens) and send `/carry-on-rewind` in its place.* Rewinding to that message drops it, and keeps the agent's message above it.

## It's working if

- The file fits on a screen, and names commits and tracker issues rather than copying them.
- You find the message to rewind to in the menu on the first look.
- After the rewind, the agent never re-asks a question you had already answered.
- A rule you gave for the whole task still holds three rewinds later, worded as you said it.

## Where it fits

`prepare-rewind` is the first half of a pair, and the pair is a step inside a long build: [implement](https://aihero.dev/skills-implement) names the rewind point and splits the build into parts that each end in a commit, and this skill runs at the end of each part. Its other half is [carry-on-rewind](https://aihero.dev/skills-carry-on-rewind), which reads the file after the rewind. [ask-matt](https://aihero.dev/skills-ask-matt) places both among the options at a phase boundary.
