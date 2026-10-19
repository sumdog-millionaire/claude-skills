---
"mattpocock-skills": minor
---

Add the `ingest-meeting` skill, which turns a meeting transcript into the project's records. It saves a dated note in `docs/meetings/` (or where `docs/agents/domain.md` names), extracts every candidate DDR, ADR, glossary term, ticket, question and conflict with a verbatim quote and timestamp, checks the quotes against the transcript with a bundled script, checks each candidate against the glossary, records and tracker, and settles them with the user in one grilling round before `domain-modeling` and `design-decision` write anything. A decision agreed in the meeting stays `proposed` until the user accepts it. It is model-invoked, so a video digest can hand over to it.
