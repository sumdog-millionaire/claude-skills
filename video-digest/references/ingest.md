# Ingesting a recording

Use the branch that matches the source. The target is the same in both cases: a timestamped
`transcript.txt`, frames covering the recording, and an open report containing source details.

Set `<skill-dir>` to `~/.claude/skills/video-digest` and `<workspace>` to the destination agreed with
the user. Use `<workspace>/meeting-notes.md` for a recorded meeting and `<workspace>/digest.md` for
another video. If a required command is missing, read [install.md](install.md).

## Local recording with an existing transcript

This is the normal Teams route. Leave the original recording and transcript where they are.

### 1. Identify the pair

Accept one recording (`.mp4`, `.mov`, `.mkv` or `.webm`) and one transcript (`.docx`, `.txt`, `.srt`
or `.vtt`). If a folder contains more than one plausible pair, ask which files belong together.

Use a date-time embedded in the filename as the stable run ID when available. Check for an existing
run before processing.

### 2. Open the meeting report

Create `<workspace>/meeting-notes.md` with:

```markdown
# <meeting title>

- **Source**: Local recorded meeting
- **Recording**: <original path>
- **Transcript**: <original path>
- **Held**: <date and duration, when supplied>
- **Participants**: <names supplied by the transcript>
```

Do this before frame extraction so an interrupted run remains identifiable.

### 3. Prepare the transcript

For a Teams Word export:

```bash
python <skill-dir>/scripts/parse_teams_transcript.py "<transcript.docx>"
```

The script prints the meeting header and attendee list and writes `transcript.txt` beside the Word
file. Move that generated file into `<workspace>` when the user chose a separate destination.
Preserve the original `.docx`.

For `.txt`, preserve its words and speaker names. If it already contains timestamps, copy it to
`<workspace>/transcript.txt`. For `.srt` or `.vtt`, normalise each caption to:

```text
[MM:SS] Speaker: text
```

Use the caption start time. Keep a speaker only when the source identifies one. Do not silently
invent speakers or correct uncertain names.

### 4. Extract meeting frames

Use dense extraction for recorded meetings because short interactions and screen demonstrations can
matter even when the transcript does not point to them:

```bash
python <skill-dir>/scripts/extract_meeting_frames.py \
  "<recording>" --frames-dir "<workspace>/frames" --interval 3
```

This writes a frame every three seconds, extra frames at larger screen changes and one time-ranged
contact sheet per minute. Three seconds is the default evidence density. Use a shorter interval only
when the user explicitly needs rapid interaction captured and has accepted the extra storage and
analysis cost.

## Public video URL

Keep fetched files in `<workspace>` because a post may later be removed. Do not use account cookies:
platforms may ban accounts used through download tools.

### 1. Fetch metadata

Run from `<workspace>`:

```bash
uvx --from "yt-dlp[default,curl-cffi]" yt-dlp \
  --skip-download --dump-json "<URL>" > meta.json
```

The `curl-cffi` extra supplies the browser fingerprint some platforms require. Let `yt-dlp` choose
it; do not pass a custom user agent or impersonation target.

Read the title, description, uploader, channel, duration, post date, like count and comment count.
The description often contains links or names absent from the speech.

Open `<workspace>/digest.md` before downloading:

```markdown
# <title>

- **Source**: <full URL>
- **Creator**: <uploader> (<handle>)
- **Posted**: <date> · <duration> · <likes> likes · <comments> comments
- **Also promotes**: <paid course, newsletter or product, when stated>
```

### 2. Download the recording

```bash
uvx --from "yt-dlp[default,curl-cffi]" yt-dlp \
  -f "best[ext=mp4]/best" -o "video.%(ext)s" "<URL>"
```

### 3. Obtain the transcript

Try platform captions first:

```bash
uvx --from "yt-dlp[default,curl-cffi]" yt-dlp \
  --skip-download --write-subs --write-auto-subs --sub-langs "en" \
  --convert-subs srt -o "captions" "<URL>"
```

Keep `--sub-langs` as bare `en`; a wildcard can request many machine-translated tracks and trigger a
rate limit. Normalise the resulting caption file into `transcript.txt`, preserving each caption's
start time.

If no captions exist, transcribe the downloaded video:

```bash
<venv-python> <skill-dir>/scripts/transcribe.py "<workspace>/video.mp4"
```

The skill interpreter is:

- Windows: `<skill-dir>/.venv/Scripts/python.exe`
- macOS or Linux: `<skill-dir>/.venv/bin/python`

The first transcription downloads the public `distil-large-v3` model, about 1.5 GB. Tell the user
before that download starts. Ordinary errors on technical vocabulary do not justify a slower second
transcription; resolve important names from the screen and mark remaining uncertainty.

### 4. Extract frames

For a short online video:

```bash
python <skill-dir>/scripts/extract_frames.py \
  "<workspace>/video.mp4" --frames-dir "<workspace>/frames"
```

Read screen-change frames first, then frames nearest transcript references such as “this”, “here”,
“these”, “this command” or “this website”, then sweep the remainder. Open neighbouring frames when a
command, URL or transition is only partly visible.

Use the dense meeting extractor instead when the URL is a full meeting, workshop or demonstration
whose whole screen history matters.

## Completion checks

Before analysis, confirm that:

1. `transcript.txt` spans the recording and preserves available timestamps and speakers.
2. `frames/` spans the recording and includes readable screen changes.
3. The report identifies the original source and generated evidence.
4. The recording duration and transcript coverage are compatible. Record any gap explicitly.

## Failures

- **Rate limit or login redirect**: report it and stop. Do not retry repeatedly or use account
  cookies.
- **Photo post or carousel**: work from the images and caption; state that there is no audio track.
- **Empty or looping transcript**: treat it as music-only and work from the screen and caption.
- **Teams parser finds no speaker turns**: confirm that the input is the `.docx`, then inspect its
  paragraph layout. Teams may have changed its export format; do not guess a new parser pattern.
- **Other failure**: report the stage and error, preserve completed files and stop.
