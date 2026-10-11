# Installing what this skill runs

Read this when a command in `SKILL.md` fails because something is missing — the venv, `uv`,
`ffmpeg` — or on the first run on a new machine. Everything here is checked once and then never
again, so do the whole page rather than the one line that failed.

**Processing only local recordings that already have a transcript (a Teams meeting and its Word
export)?** Skip sections 1, 3 and 4 below entirely — `parse_teams_transcript.py` is plain Python with
no dependency, so it needs neither `uv` nor the venv nor the 1.5 GB Whisper model. Only section 2,
`ffmpeg`, is still needed, for reading the screen.

Four things run outside the conversation, and each is installed differently:

| What | Used by | Where it comes from |
|---|---|---|
| `uv` | every step — it runs `yt-dlp` and builds the venv | one installer, below |
| `ffmpeg` and `ffprobe` | step 4, reading the screen | the OS package manager |
| the venv (`faster-whisper`, `av`) | step 3, transcribing | `uv`, from `requirements.txt` |
| the Whisper model `distil-large-v3` | step 3 | downloads itself on the first transcription |

## 1. `uv`

Check: `uv --version`. If that prints a version, skip to ffmpeg.

- **Windows** (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"` — or `winget install astral-sh.uv`
- **macOS**: `brew install uv` — or `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Linux**: `curl -LsSf https://astral.sh/uv/install.sh | sh`

Open a new shell afterwards so it is on the path. `uv` fetches Python 3.13 itself when the venv is
built, so no separate Python install is needed, whatever the machine already has.

## 2. `ffmpeg`

Check: `ffmpeg -version` and `ffprobe -version`. Both ship together.

- **Windows**: `winget install Gyan.FFmpeg`, then open a new shell
- **macOS**: `brew install ffmpeg`
- **Linux** (Debian/Ubuntu): `sudo apt install ffmpeg`

Only frame extraction needs it. Transcription decodes audio through `av`, which is inside the venv.

## 3. The venv

Built once, in the skill's own folder, so it never collides with a project's environment:

```bash
uv venv --python 3.13 ~/.claude/skills/video-digest/.venv
uv pip install --python ~/.claude/skills/video-digest/.venv \
  -r ~/.claude/skills/video-digest/requirements.txt
```

The interpreter lands in a different place per OS, and every command in `SKILL.md` that says
`<venv-python>` means this path:

- **Windows**: `~/.claude/skills/video-digest/.venv/Scripts/python.exe`
- **macOS and Linux**: `~/.claude/skills/video-digest/.venv/bin/python`

Check it: `<venv-python> -c "import faster_whisper, av; print('ok')"`.

`requirements.txt` pins `av` to 17.x. Version 18 ships DLLs that Windows Application Control
policies block on some corporate machines, and the failure ("DLL load failed ... blocked by an
Application Control policy") appears at import time, three layers below anything the transcription
script reports. 17 works everywhere. Leave the pin unless you have tested 18 on the machine in
question.

## 4. The Whisper model

The first transcription downloads `distil-large-v3` — roughly 1.5 GB — into the Hugging Face cache
(`~/.cache/huggingface/hub` on macOS and Linux, `%USERPROFILE%\.cache\huggingface\hub` on Windows)
and reuses it afterwards. Say so before the first run on a new machine: a silent multi-minute
download looks like a hang. No account or token is needed; the model is public.

## What is deliberately not installed

- **No cookies or accounts for yt-dlp.** `SKILL.md`'s "When it fails" section says why: the tool's
  own documentation warns an account used with it can be banned.
- **No GPU build.** `transcribe.py` runs on CPU at int8, about three times faster than realtime, and a
  GPU build is a second set of drivers to go wrong for a gain nobody notices on a three-minute clip.
