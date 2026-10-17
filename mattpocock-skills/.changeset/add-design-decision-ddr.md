---
"mattpocock-skills": minor
---

Add the `design-decision` skill and DDRs (design decision records). A DDR is one row in `docs/ddr/register.csv`, a filterable register, for a decision that fails the ADR test but would still be built wrong by an engineer who never heard the conversation: statused (proposed, in-research, accepted, rejected, deferred, superseded), tagged by layer, area, sub-area and project part, weighted by priority and risk, dated, and written before the edit that implements it. An undecided row names the tracker issue that settles it, and the issue names the row back. `domain-modeling` gains a "Route design rules to DDRs" section and a `DDR-FORMAT.md` beside `ADR-FORMAT.md`; `grill-with-docs` loads `design-decision` as its third companion.
