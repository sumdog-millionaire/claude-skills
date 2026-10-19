## What it does

`ingest-meeting` turns a meeting transcript into the project's records: DDRs, ADRs, glossary terms, tickets and open questions, each carrying the quote and timestamp that justify it, plus a dated meeting note in `docs/meetings/` that keeps the transcript and links every record it produced.

A meeting is not a decision-maker, so nothing goes straight from the transcript into a record. Every candidate is quoted, classed as decided, proposed or discussed, checked against what is already recorded, and put to you in one grilling round. A decision everyone agreed in the call is still written as `proposed` unless you accept it.

## When to reach for it

Type `/ingest-meeting`, or the agent reaches for it automatically when you hand it a transcript and want what came out of the meeting recorded. For a recording rather than a transcript, it runs a video digest first where one is installed.

| You have | Use |
| --- | --- |
| A transcript, and want decisions and work recorded | `ingest-meeting` |
| A plan in your head to stress-test, with no meeting behind it | [grill-with-docs](https://aihero.dev/skills-grill-with-docs) |
| A spec to split into build tickets | [to-tickets](https://aihero.dev/skills-to-tickets) |

## Prerequisites

The project needs the records set up by [setup-matt-pocock-skills](https://aihero.dev/skills-setup-matt-pocock-skills): a glossary, an ADR folder, a DDR register and a tracker. The skill writes meeting notes to `docs/meetings/`, or wherever `docs/agents/domain.md` names.

## Quoted, then agreed

Every candidate carries a **verbatim quote** with its speaker and timestamp, taken from where the outcome was reached rather than where the topic first came up. A bundled script then checks each quote against the transcript, because a model can write a plausible line nobody said. Owners and dates appear only where someone in the meeting accepted them; otherwise the note says "owner not set" and a question goes on the list.

Candidates that clash with a recorded decision come first in the round, because their answers can change the rest.

## Common questions

**Does it create tickets for every action mentioned?**
No. It searches the tracker first: an action already ticketed becomes a comment on that issue, and nothing is created until you say yes to its title and body in the round.

**Why is a decision the client clearly agreed still `proposed`?**
The register records what the project decided, and you are the one who decides it. Saying yes in the round promotes it in the same step.

## It's working if

- Every item in the meeting note has a quote you can find in its transcript.
- The round with you is a single numbered list, and nothing appears in the register or tracker that you did not see in it.
- The note's Outcome section links every record and issue the meeting produced.

## Where it fits

`ingest-meeting` is a **reach-for-it-anytime standalone** that feeds the records. It loads [domain-modeling](https://aihero.dev/skills-domain-modeling) to read what is already decided, [grilling](https://aihero.dev/skills-grilling) to run the round, and [design-decision](https://aihero.dev/skills-design-decision) to write the rows. [ask-matt](https://aihero.dev/skills-ask-matt) routes the whole set.
