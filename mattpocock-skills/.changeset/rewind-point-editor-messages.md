---
"mattpocock-skills": patch
---

The rewind point script reads a Claude Code session run from an editor extension, which stores each typed message as text blocks rather than one string, so it no longer finds no messages there and fails to match the quote. A terminal session's string messages read as before, and tool results and harness notes are still left out; `scripts/test_rewind_point.py` covers both shapes.
