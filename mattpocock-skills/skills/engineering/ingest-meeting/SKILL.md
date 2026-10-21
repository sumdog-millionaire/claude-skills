---
name: ingest-meeting
description: Turn a meeting transcript into the project's records. It saves a dated meeting note in `docs/meetings/`, extracts every candidate decision, term, ADR, ticket and open question with a verbatim quote and timestamp, checks each against the glossary, the ADRs, the DDR register and the tracker, then settles them with the user in a grilling, conflicts first, before writing anything. Use it whenever the user supplies or pastes a meeting transcript, call notes, Teams or Zoom captions, or a digest of a recorded meeting and wants decisions, actions, tickets, ADRs, DDRs or glossary terms out of it, or says "process this meeting", "ingest this call", "what came out of this meeting" or "write up the meeting". Use it after a video digest when its findings should become project records.
---

# Ingest meeting

A meeting suggests; the user decides. Move each decision, term, action and question from the
transcript to its home, and write nothing the user has not seen and accepted.

1. **Get the transcript.** For a recording, call the Skill tool with "video-digest" first if it is
   installed. Take the meeting's start date and time from the transcript or its metadata, and ask if
   neither gives them.
2. **Read the records.** Call the Skill tool with "domain-modeling".
3. **List the candidates.** Read every turn. Each candidate is a DDR, an ADR, a glossary term, a
   ticket, a question, or a conflict with a recorded decision. Give it a number, a verbatim quote with
   its speaker taken from where the outcome was reached, and whether the meeting decided, proposed or
   only discussed it. Name an owner or date only where the meeting gave one. Search the records and
   the tracker: a candidate already recorded becomes a pointer, and an action already ticketed becomes
   a comment on that issue. Note likely mishearings of names and terms as guesses.
4. **Save the note** at `docs/meetings/YYYY-MM-DD-HHMM-<slug>.md`, or where `docs/agents/domain.md`
   names, in [NOTE-FORMAT.md](./NOTE-FORMAT.md), with the transcript at the end. Run
   `python <this skill>/scripts/check_quotes.py <note>` and fix every quote it fails. If the
   transcript came as a loose file elsewhere in the project, the note is its renamed, moved home:
   once the note holds the whole transcript, delete the loose file. Before ingesting a loose file,
   check `docs/meetings/` for a note already holding its transcript; if one does, delete the loose
   file and do not ingest it again.
5. **Grill the user.** Call the Skill tool with "grilling" and put every candidate to the user in its
   format, conflicts first, naming the note's item number. A ticket or comment shows its title and a
   one-line body, so "yes" approves that exact write. A decision the meeting agreed stays `proposed`
   unless the user accepts it.
6. **Write what was accepted.** Call the Skill tool with "design-decision" for DDRs; ADRs and terms
   go through `domain-modeling`; tickets and comments follow the project's tracker guidance. Cite the
   note's path in each. Fill the note's Outcome section, and tell the user in plain words what each
   candidate became.
