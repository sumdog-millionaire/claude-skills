# Building the evidence map

The evidence map is a detailed account of what happened, what appeared on screen and what each point
means. It is not a transcript summary with decorative screenshots. Every substantive part of the
recording must be traceable through timestamps, and every frame must support a specific visible fact
or demonstrated action.

## Evidence categories

Keep these categories distinct:

- **Stated**: a participant or presenter said it. Attribute the speaker and timestamp.
- **Shown**: it was visible in a frame. Link the clearest frame.
- **Demonstrated**: before-and-after frames support an action and result. Link both when the change
  matters.
- **Inferred**: the conclusion follows from context but was not stated or shown. Label it.
- **Unclear**: the transcript or screen does not support a reliable reading. Preserve the uncertainty.

A suggestion is not a decision. A question is not an action. A rough date is not a commitment. A
pointer resting over a control does not prove a click.

## Analyse the whole recording

1. Read the transcript from start to finish.
2. Review the contact sheets chronologically for a meeting, or the scene changes and sweep for a
   short video.
3. At every substantive transcript turn, inspect the nearest frame and any relevant neighbouring
   frames. Pay particular attention to deictic phrases such as “this”, “here”, “these”, “that field”,
   “this command” and “this screen”, where speech depends on the picture.
4. At every material screen change, check the surrounding transcript even when nobody explicitly
   describes it.
5. Extract a better-aligned frame when the available samples do not show the initial state, action or
   result clearly:

   ```bash
   python <skill-dir>/scripts/extract_meeting_frames.py \
     "<recording>" --frames-dir "<workspace>/frames" \
     --at "HH:MM:SS.s" --at "HH:MM:SS.s"
   ```

6. Record what happened, why it mattered, its evidence category, and any decision, action,
   requirement, risk, dependency or open question it created.
7. Account for short asides, disagreement, corrections, transitions and closing commitments. Detail
   comes from coverage, not repetition.

## Frame references

Link the clearest individual frame relative to `<report>`:

```markdown
[Frame 00:13:12](frames/t00792.0.jpg)
[Frame 01:02:14.6](frames/change_t03734.6.jpg)
```

Use the actual filename produced by the extractor. Prefer a precise requested or change frame over a
coarse regular sample. Use contact sheets for analysis, not as final evidence when an individual
frame is available.

Put each frame link beside the information it proves. When a point depends on several visible
states, link the small set of frames needed to establish the sequence.

## Long recordings and delegation

Use the main agent when the recording and its evidence fit comfortably in context; 30 minutes is the
normal ceiling. For a longer or unusually dense recording, delegate contiguous 20–30 minute ranges.
Every range must leave a durable analysis file because chat responses are not evidence artefacts.

1. Divide the recording into contiguous, non-overlapping ranges with explicit start and end times.
   Every second must belong to exactly one range.
2. Give each reviewer the complete transcript, frame folder, assigned range, evidence categories,
   report requirements and a bound output path:

   ```text
   <workspace>/meeting-analysis/segments/<start>-<end>.md
   ```

3. Require each segment to contain:

   ```markdown
   # Evidence map — <start>-<end>

   ## Coverage and evidence
   ## Detailed chronological record
   ## Screen evidence and demonstrations
   ## Decisions and agreed directions
   ## Actions
   ## Open questions
   ## Requirements and implications
   ## Systems, fields and artefacts shown
   ## Risks, constraints and uncertainties
   ```

4. Each reviewer reads every transcript turn and every overlapping contact sheet, opens individual
   frames around each material screen state, extracts exact frames when needed and writes its segment
   file before completing.
5. Rerun any missing or thin range. Do not ask another reviewer to fill it from memory.
6. Read every complete segment file in full before writing `<report>`. Write the top-level synthesis
   first, then append every complete segment report in chronological order, demoting headings only as
   needed to fit the parent document. This preserves all detail while giving the reader a useful
   summary and extracted tables at the front.
7. Keep segment files after synthesis as recoverable analysis evidence.
8. Validate the stitched result and write `<workspace>/meeting-analysis/final-acceptance.md`. Record:
   - every segment file and time range;
   - transcript and recording coverage from first substantive turn to close;
   - report line and character counts;
   - frame-link count and whether every target exists;
   - whether every segment appears in full in the stitched report;
   - any independent review attempted and its actual result; and
   - corrections made during the parent's direct acceptance pass.

Delegation is complete only when every second belongs to one segment, every segment file exists and
has been read, `<report>` contains every segment in full, and the acceptance record reaches an
explicit verdict.

## Report structure

Use this structure unless the user requested a destination format with equivalent coverage:

```markdown
# <title>

## Source and coverage
- Source, date, duration and participants or creator
- Recording, transcript and frame locations
- Frame interval and any evidence gaps

## Executive account
A compact account of the recording's purpose, what happened, what was established and what remains
unresolved.

## Outcomes at a glance
### Decisions
### Actions
### Open questions
### Principal findings

## Detailed chronological evidence map
### 00:00-<time> — <topic>
- **Information:** What was raised, explained, challenged, corrected or agreed.
- **Screen evidence:** What was visible or demonstrated, with the relevant frame or frame sequence.
- **Significance:** Why the point mattered and what followed from it.
- **Status:** Decision, action, requirement, risk, dependency, question or contextual information.

## Detailed screen walkthrough
### <system, document or demonstration>
1. `<timestamp>` — What the participant opened, selected, entered, changed or reviewed.
   - **Visible result:** ...
   - **Significance:** ...
   - **Evidence:** [Frame ...](frames/...)

## Decisions and agreements
| Time | Decision or agreement | Owner or participants | Evidence | Qualification |

## Actions and follow-ups
| Owner | Action | Timing | Dependency | Evidence |

## Open questions and unresolved decisions
| Question | Why it matters | Proposed owner | Next step | Evidence |

## Requirements and implications
### Functional requirements
### Content and data requirements
### User experience requirements
### Security, privacy and legal requirements
### Integration and operational requirements

## Risks, constraints and assumptions

## Systems, fields and artefacts shown
Record each named system, page, control, field, document, command, URL or data source and what the
recording established about it.

## Uncertainties and evidence limits

## Appendix: timestamp index
A dense topic index covering every substantive part of the recording.

# Full detailed record by time range
For delegated analysis, include every complete segment report here in chronological order.

## Outcome
Added after the user chooses what to do with the evidence map.
```

For an educational or instructional video, retain the same evidence standard but adapt meeting-only
labels: use presenter instead of participant, claims or recommendations instead of decisions, and
steps or techniques instead of actions. Do not invent meeting governance around a tutorial.

## Review before delivery

Confirm that:

1. The chronological map covers the entire recording, including side discussions and the close.
2. Every substantive transcript turn appears in the map or is explicitly marked immaterial.
3. Every material screen change was inspected.
4. Each described selection, edit, navigation or result is supported by the frames.
5. Frame links resolve from `<report>` and match their stated timestamps.
6. Decisions, proposals, preferences, questions and actions remain distinct.
7. Actions have an owner only when the source names one; unassigned work remains unassigned.
8. Disagreement, uncertainty and caveats remain visible.
9. Sensitive details are described only as far as the recording requires and are not copied.
10. The executive account and extracted tables agree with the detailed chronology.
