---
name: ingest-meeting
description: Turn a meeting transcript into the project's records. It saves a dated meeting note in `docs/meetings/`, extracts every candidate decision, term, ADR, ticket and open question with a verbatim quote and timestamp, checks each against the glossary, the ADRs, the DDR register and the tracker, then settles them with the user in one grilling round before writing anything. Use it whenever the user supplies or pastes a meeting transcript, call notes, Teams or Zoom captions, or a digest of a recorded meeting and wants decisions, actions, tickets, ADRs, DDRs or glossary terms out of it, or says "process this meeting", "ingest this call", "what came out of this meeting" or "write up the meeting". Use it after a video digest when its findings should become project records.
---

# Ingest meeting

A meeting produces decisions, words, work and questions, and all four are lost if they live only in
a transcript nobody reopens. This skill moves each one to its home, with the evidence that justifies
it, and moves nothing the user has not agreed.

A meeting is not a decision-maker. People in a call suggest, lean and agree in passing; the user
decides what the project records. So a candidate is never written straight from the transcript: it
is quoted, classified, checked against what is already recorded, and put to the user first.

## Before you start

- **A recording, not a transcript:** if a `video-digest` skill is available, call the Skill tool
  with "video-digest" first and work from the transcript and report it produces. Otherwise ask the
  user for the transcript.
- **The meeting's start date and time:** take them from the transcript or its file metadata. If
  neither gives them, ask, and do not write the note until you have them. Never use the time you are
  processing it.
- **The meetings folder** is `docs/meetings/`, unless the project's `docs/agents/domain.md` names
  another place. If it already holds a note for this meeting, ask whether to continue that one.

## 1. Read the records

Call the Skill tool with "domain-modeling". It reads the glossary, the ADRs and the DDR register, so
every candidate is named in the project's words and checked against what was already decided.

## 2. Read the whole transcript

Read every turn. Do not skim to the parts that sound important: a decision is often agreed in a
throwaway line after the discussion that produced it.

Transcription software mishears names and project terms. Use the participant list and the glossary
to spot likely mishearings, and list each in the note's caveats as a guess ("'Wren' at 14:02 is
probably 'REN', the glossary term"). Never correct the transcript itself.

## 3. Extract the candidates

Every candidate gets a number, a short title, one class, a verbatim quote with its speaker and
timestamp, and a recommendation.

| Class | It is | Its home if accepted |
|---|---|---|
| DDR | A choice among several approaches, reversible | The register, via `design-decision` |
| ADR | A choice that is hard to reverse, surprising later and a real trade-off | `docs/adr/`, via `domain-modeling` |
| Term | A word the meeting defined, sharpened or used against the glossary | The glossary, via `domain-modeling` |
| Ticket | Work someone has to do | The tracker |
| Question | Something unknown, or a question for someone outside the meeting | The tracker, as the project's guidance says |
| Conflict | Something said that contradicts a recorded decision or term | Raised with the user; never resolved silently |

Hold the evidence to these rules, because a record that overstates the meeting is worse than none:

- **Decided, proposed or discussed.** Mark a candidate *decided* only when the transcript shows a
  clear outcome (agreed, rejected, postponed). A preference or suggestion is *proposed*; a topic
  without an outcome is *discussed*. Keep the speaker's strength: "we could" is not "we will".
- **Quote the agreement, not the first mention.** The timestamp is where the outcome was reached.
- **Owners and dates.** Name an owner only where someone accepted the task in the transcript; the
  person who raised it is not its owner. Otherwise write "owner not set" and add a question. Convert
  a relative date ("next Friday") against the meeting date; if the reference is unclear, keep the
  speaker's words and flag it. Never supply an owner, date or priority the meeting did not give.
- **Check what exists.** Search the register, the ADRs and the glossary for each candidate's nouns,
  and the tracker for open issues covering it. A candidate already recorded becomes a pointer; one
  that contradicts a record becomes a Conflict; an action already ticketed becomes a comment on that
  issue, not a new ticket.

Leave out small talk, logistics and anything with no consequence for the project. Do not copy
credentials, private links or personal data the meeting does not need.

## 4. Save the note and check the quotes

Write the note to `<meetings folder>/YYYY-MM-DD-HHMM-<slug>.md`, using the meeting's start time and
a short lowercase slug of its topic. Use [NOTE-FORMAT.md](./NOTE-FORMAT.md). The full transcript goes
at the end, because the quote check reads it there: copy the transcript file to the note's path, then
add the note above it. When a video digest ran, link its report and frames rather than copying them.
If no transcript exists, only a summary, say so in the note and to the user: the quotes cannot be
checked.

Then run the quote check:

```bash
python <this skill>/scripts/check_quotes.py <note>
```

It fails any quote line whose words or timestamp are not in the note's transcript. A model can write
a plausible quote nobody said; this check is what catches it. Re-anchor or drop each failure, then
run it again until it passes.

## 5. One round with the user

Call the Skill tool with "grilling" and put every candidate to the user in one round, in its format,
naming the note's item number in each question. For a ticket or question, show the title and a
one-line body, so "yes" approves the exact write. Conflicts come first, because their answers can change the rest.

A decision agreed in the meeting is still recorded as `proposed` unless the user accepts it in this
round: the meeting suggested it, the user decides it.

## 6. Write what was accepted

- DDRs: call the Skill tool with "design-decision", citing the note's path in the row's `why` or
  `tracker_issue` as the project's register expects.
- ADRs and terms: through `domain-modeling`, already loaded.
- Tickets, questions and comments: follow the project's tracker guidance in
  `docs/agents/issue-tracker.md`, with the note's path and the quote's timestamp in each body.

Write nothing the user declined, and nothing they were not shown.

## 7. Close the note

Fill the note's Outcome section: each candidate's number with the record, issue or comment it became,
or "declined" or "deferred". Report the same to the user in plain words, never by identifier alone.

## What this skill does not do

It does not decide, and it does not act on a candidate the user has not seen. It does not rewrite
the transcript, assign work the meeting did not assign, or turn a meeting's mood into a record.
