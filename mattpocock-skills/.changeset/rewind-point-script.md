---
"mattpocock-skills": minor
---

`prepare-rewind` chooses the rewind point before writing the handover, using a new standard-library script, `scripts/rewind_point/`, that reads the session log of Claude Code, Codex, Pi or opencode and lists each user message with the context in tokens before it. It takes a message the user names, then the point `implement` stated on a line opening `**Rewind point.**`, then the latest message under a token limit (200,000 by default), going earlier only where the context above still holds the research; it stops and offers the user a later message or a repeat grilling when the limit falls before the research finished, and reports a broken script to the user rather than guessing. It also appends to `rewind-durable.md` any fact the research established that the work then changed. `implement` runs further rounds of research and grilling aimed at facts that hold for the session, and states the rewind point on that marker line.
