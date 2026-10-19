# Meeting note format

One file per meeting: `docs/meetings/YYYY-MM-DD-HHMM-<slug>.md`, named for the meeting's start time.

```markdown
---
title: Checkout review with finance
start: 2026-03-16T14:00:00+00:00
participants: [Ana Ruiz, Sam Okafor, Lee Chen]
source: Teams transcript, downloaded .vtt
---

# Checkout review with finance

## Source and coverage

- **Source:** where the transcript came from and how it was obtained; link a video digest report and
  its frames when one exists.
- **Coverage:** the time range the transcript covers, and any gap.
- **Caveats:** likely mishearings, each marked as a guess with its timestamp; masked words; anything
  unclear.

## Summary

Three to six sentences: what the meeting was for and what came out of it.

## Items

### 1. Refunds go to the original payment method (DDR, decided)

> 12:03 Sam Okafor: refunds always go back to the card they paid with, no store credit

Recommendation: accept as a DDR. Owner not set. Due not set.

### 2. Who emails the payment provider about partial refunds (Ticket, proposed)

> 18:40 Lee Chen: someone should ask them whether partial refunds are supported

Recommendation: create a ticket. Owner not set: nobody took it on.

## Outcome

Filled after the round with the user: each item's number and what it became.

- 1. D107, accepted.
- 2. ENG-212, created.

## Transcript

**Ana Ruiz** 00:04 Right, shall we start.
```

## Rules

- **Quote lines** are `> <timestamp> <speaker>: <words>`, one per line, words copied exactly from
  the transcript turn. When the transcript has no timestamps, write `> <speaker>: <words>` and the
  check matches the words anywhere in it. `scripts/check_quotes.py` reads these two forms; a quote in
  any other form is not checked. An item may carry several quote lines.
- **Item headings** are `### <n>. <title> (<class>, <decided | proposed | discussed>)`, numbered in
  transcript order and never renumbered after the round.
- **Timestamps** are offsets into the recording as the transcript prints them. The real start time
  lives only in the front matter.
- **The transcript** is pasted whole under `## Transcript`, as the source gave it, errors included.
