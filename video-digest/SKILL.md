---
name: video-digest
description: >-
  Digest recorded meetings and videos into a detailed, timestamped evidence map that combines the
  transcript with what appeared on screen, then let the user decide what to do with the findings.
  Use whenever the user supplies a Teams recording or transcript, a local video or meeting folder,
  or a video URL; asks for detailed meeting notes, minutes, decisions, actions, requirements or a
  screen walkthrough; wants information extracted from a recording; or wants a video turned into
  tracker work, project changes, research, a skill or an agent. Use even when they ask only to
  summarise a meeting, because spoken words alone can miss material information shown on screen.
---

# Video Digest

Turn a recording into a durable evidence map before deciding what to do with it.

A transcript and a recording are complementary sources. Speech establishes what participants said
and why. The recording establishes what was visible, including names, URLs, commands, fields,
controls, documents and demonstrated results. Analyse both and link each important visible point to
the clearest relevant frame.

## Before running

Use AskUserQuestion before processing to settle only choices the request has not already answered:

- **Emphasis**: complete meeting record, detailed screen walkthrough, learning and methods, or all of
  these.
- **Destination**: beside the supplied files or in a separate run folder.
- **External research**: source-bound digest only, or verify and expand what the video names.

Every option still produces a detailed evidence map. Emphasis changes where the most detail goes;
it does not permit a thin summary. Do not ask again about a choice the user already made.

Before the first long tool call, say in one line that you will parse or transcribe the recording,
inspect the screen throughout, connect frames to the transcript and then return with the evidence
map and possible next actions.

## Boundaries

The evidence map is the only output approved by starting this skill. Reading, downloading,
transcribing, frame extraction and requested research are preparation for it.

After the evidence map, propose downstream work and ask the user what to do next. Create tracker
items, edit a project, contact services, or create a skill or agent only after the user chooses that
route and approves the specific write. This prevents a recording from silently turning into work
nobody agreed to.

Do not reproduce credentials, card data, private links or unnecessary personal data visible on
screen. Record only what the meeting requires and describe sensitive values without copying them.

## 1. Identify the source

Accept either:

- a folder or explicit pair containing one recording (`.mp4`, `.mov`, `.mkv` or `.webm`) and one
  transcript (`.docx`, `.txt`, `.srt` or `.vtt`); or
- a public video URL.

If several recordings or transcripts are plausible, ask which pair to use. Do not guess.

Use a stable workspace:

- For a supplied meeting folder, leave originals in place and store `transcript.txt`, `frames/`,
  `meeting-analysis/` and `meeting-notes.md` in that folder. Use a separate destination only when the
  user requests one.
- For other local files, use the supplied folder or `~/video-digest-runs/<date-or-id>--<slug>/`.
- For a URL, use `~/video-digest-runs/<video-id>--<slug>/` and keep the metadata, video, captions,
  transcript and frames so a removed post does not erase the source.

Set `<report>` to `meeting-notes.md` for a recorded meeting and `digest.md` for another video. Check
for an existing run with the same stable ID before fetching or processing. If `<report>` exists,
state its outcome and ask whether to reuse it or make a fresh pass. Reuse any complete files from an
abandoned run.

## 2. Prepare the transcript and frames

Read [references/ingest.md](references/ingest.md) and follow the branch for the supplied source.
Completion means the workspace contains `transcript.txt`, `frames/` and `<report>`.
`transcript.txt` must preserve timestamps and speaker names when the source provides them.
`frames/` must cover the whole recording densely enough to account for every substantive visible
change. Open `<report>` with source details before long processing so an interrupted run remains
identifiable.

## 3. Build the evidence map

Read [references/evidence-map.md](references/evidence-map.md) and follow it in full.

Read every transcript turn and inspect the screen across the entire recording. At each substantive
point, connect:

1. what was said;
2. what was shown or demonstrated;
3. why it mattered;
4. whether it created a decision, action, requirement, risk or open question; and
5. the timestamp and clearest supporting frame or frames.

Distinguish stated, shown, demonstrated, inferred and unclear evidence. A pointer resting over a
control does not prove a click; use before-and-after frames when the action matters. Preserve
caveats, disagreement and uncertainty rather than smoothing them into consensus.

Write the complete result to `<report>`. Analyse a short recording in the main agent. For a long
recording, delegate contiguous time ranges as described in the reference, require a durable segment
file from every range, and read every segment before synthesis.

Completion means every second belongs to the analysis, every substantive transcript turn is
accounted for, every material screen event has been inspected, and the report passes the reference's
review checklist.

## 4. Brief the user

Lead with a compact account of what the recording covered, its main decisions and actions, and what
the screen added that the transcript alone did not reveal. State where `<report>` and its frames are stored and name any important uncertainty.

Then use AskUserQuestion to ask what should happen next. Offer only routes supported by the digest,
which may include:

- keep the evidence map as the final output;
- turn selected findings into work in the project's issue tracker;
- make specified project or documentation changes;
- verify or expand named material through external research;
- create or update a skill or agent; or
- prepare another user-named deliverable.

Allow multiple selections when several routes can apply. Do not imply that an action belongs in an
issue tracker merely because it was mentioned in a meeting.

## 5. Carry out the chosen next action

Read [references/next-actions.md](references/next-actions.md) and follow only the selected branch.
Show the concrete proposal before any write outside `digest.md`, then get approval and make exactly
that change.

Finish `<report>` with a one-line **Outcome** recording what happened after analysis, including the
project or tracker when relevant. If the user chooses no next action, use `**Outcome:** Digest only.`
This line makes repeat runs cheap to identify.

## Failures

Report the failed stage and its error, then stop cleanly. Do not retry blindly against rate limits,
guess at transcript structure, substitute a mismatched recording, or continue with partial coverage
while presenting the result as complete. Keep completed intermediate files so a later run can resume.
