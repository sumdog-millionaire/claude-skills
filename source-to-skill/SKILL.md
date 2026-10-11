---
name: source-to-skill
description: Learn from a video and do something with it — downloads it, transcribes it, reads what is on screen, researches whatever it names, briefs the user, then asks what they want before writing anything — a new Claude Code skill or agent, changes made right now to the project they are in (a CLAUDE.md rule, a README shape, a tool installed, a technique adopted), or just the notes. Use whenever the user pastes a video link (youtube.com, youtu.be, instagram.com/reel, instagram.com/p, tiktok.com, loom.com, x.com, or any other video URL) with any hint they want to learn from it, capture it, or act on it. Trigger on "turn this into a skill", "reel this", "skill this video", "learn this tutorial", "make an agent from this video", "what does this video teach", "apply this to my project", "what can we take from this", "do what this video says", or a bare video link with little explanation. Use it even when they say "agent" rather than "skill", and even when they want no skill at all.
---

# Source to Skill

Turn a video someone saved into something they actually use — a skill, a change made to their project
today, or the notes.

Two things make this work, and both are easy to skip.

**A video is a pointer, not a lesson.** Thirty seconds of someone talking is a signpost towards a
tool, a technique or a repo. The value is in what it points at, so the transcript is where the work
starts, never where it ends.

**Most of a video is not spoken.** Creators put the names, the URLs and the commands on screen and
say "this one" out loud. A real example: a video whose audio said *"choose your preferred primitive
library, here two"*, *"go to this website"*, and *"install this AI skill"* had RadixUI, BaseUI,
ui.shadcn.com and a full install command on screen. Transcribed alone it teaches nothing. Read
properly it is a complete setup guide.

## The rule that governs everything here

**Nothing is written until the user has decided what to write.** No SKILL.md, no agent file, no
directory, no edit to a file they already have. Their objection to how this normally goes is that a
model reads some input and disappears to build something nobody agreed to. Fetching, transcribing,
reading the screen and researching are all fine unprompted — they are read-only and take a couple of
minutes. Creating or changing files is not.

The research is unprompted, not unannounced. Before the first fetch, say in a line what is about to
happen — download, transcribe, read the screen, chase what it names — and that the questions come
once you know what the video holds. A couple of minutes of silent tool calls looks like the thing
they object to, even when it is not.

This applies to what gets built too, which is why every generated skill opens by asking how it
should run. See "What every generated skill must do".

## The second rule: you do not write skills, skill-creator does

**Load the `skill-creator` skill before creating or editing any skill or agent file, and let it do
the writing.** Not "usually", not "when the skill is complicated" — every time, including a one-line
change to a skill that already exists.

Two reasons, and the second is the one that bites. Skill-creator holds the current conventions:
frontmatter fields, how a description has to be written for the skill to actually trigger,
progressive disclosure, when to split into `references/`, the writing style that works on a model.
Those move, and a file written from memory drifts from them one edit at a time. And this skill's
whole job is research — transcribing, reading frames, chasing what a video named. Research context
is a poor state to author from: by the time you reach step 7 you are full of one video's specifics,
which is exactly when a skill comes out overfitted to the example that produced it.

So: research here, hand over there. If you find yourself about to open an editor on a `SKILL.md`
without having loaded skill-creator in this conversation, stop and load it.

## Workflow

Work in `~/source-to-skill-runs/<video-id>--<slug>/`, where the id is whatever the platform's URL
carries and the slug is two to four words of readable title. The id is what makes the folder unique
and dedupable; the slug is what makes `ls` mean anything a month later. Keep everything you fetch: it
is small, it is the only copy that survives the post being taken down, and re-fetching spends another
request against a rate limit. As you learn things, write them into `findings.md` in that folder
rather than holding them in the conversation — the conversation may be rewound, the folder will not.

### 0. Check whether this has been run before

Before fetching anything, take the id out of the URL and look for it:

```bash
ls -d ~/source-to-skill-runs/<video-id>--* 2>/dev/null
```

A hit means the download, the transcription and the frame reading are already done and cost nothing
to reuse — read that folder's `findings.md`, which opens with the source and closes with the verdict.
Say what the run was and what came out of it, then ask whether they want those findings or a fresh
pass; do not silently re-fetch. Re-running is sometimes right — the skill it produced was wrong, or
they want a different part of the video — but it should be their choice rather than three minutes of
unnoticed rework.

An id with no folder is a first run. An id with a folder but no `findings.md` is an abandoned run —
reuse what it downloaded and carry on from there.

### 1. Fetch metadata

```bash
uvx --from "yt-dlp[default,curl-cffi]" yt-dlp --skip-download --dump-json "<URL>" > meta.json
```

The `curl-cffi` extra is not optional. Since June 2026 Instagram rejects requests without a browser
fingerprint, and plain `yt-dlp` fails with "attempting impersonation, but no impersonate target is
available". Let yt-dlp pick the fingerprint — do not pass `--impersonate` or a custom `--user-agent`,
both of which make things worse.

Read `description` (the caption — often carries links the video never says aloud), `uploader`,
`channel` (the @handle), `duration`, `like_count`, `comment_count`, `timestamp`.

**Open `findings.md` now, with the source block, before you have any findings.** `meta.json` holds
all of this, but it is a megabyte of machine output — nobody opens it to remember what a folder was,
and a run that stops early otherwise leaves nothing readable behind at all:

```markdown
# <title>

- **Source**: <full URL>
- **Creator**: <uploader> (<@handle>)
- **Posted**: <date> · <duration> · <likes> likes · <comments> comments
- **Also promotes**: <paid course, newsletter, product — where the video is selling something>
```

### 2. Download the video

```bash
uvx --from "yt-dlp[default,curl-cffi]" yt-dlp -f "best[ext=mp4]/best" -o "video.%(ext)s" "<URL>"
```

### 3. Get the transcript

**Captions first**, where the platform has them:

```bash
uvx --from "yt-dlp[default,curl-cffi]" yt-dlp --skip-download \
  --write-subs --write-auto-subs --sub-langs "en" --convert-subs srt \
  -o "captions" "<URL>"
```

They arrive in seconds however long the video is, and they carry the timestamps everything after
this depends on. Keep `--sub-langs` as bare `en`: a wildcard like `en.*` also matches YouTube's
machine-translated tracks (`en-de`, `en-es`, and a hundred more), and asking for all of them earns
an HTTP 429 before it finishes.

**Where there are none**, transcribe the downloaded file:

```bash
<venv-python> ~/.claude/skills/source-to-skill/scripts/transcribe.py video.mp4
```

`<venv-python>` is the skill's own interpreter: `~/.claude/skills/source-to-skill/.venv/Scripts/python.exe`
on Windows, `~/.claude/skills/source-to-skill/.venv/bin/python` on macOS and Linux. If it is not
there, or `uv` or `ffmpeg` is missing, read `references/install.md` and do the whole page — it is a
one-time setup, and on a fresh machine the first transcription also downloads the model, which is
worth saying before it starts.

Runs locally, costs nothing, roughly three times faster than realtime. Writes `transcript.txt` with
`[MM:SS]` timestamps on every line.

Either way, those timestamps are what let you jump from a spoken moment to the picture that was on
screen at the time.

Expect ordinary errors on technical vocabulary from either source. Meaning survives them; do not
rerun on a heavier model to chase individual words. **Where a name matters, the screen decides it,
not the audio** — a repo heard as "CloudWatch" was `bradautomates/claude-video`, and "GitHub Studio"
was Google AI Studio.

### 4. Read the screen

```bash
<venv-python> ~/.claude/skills/source-to-skill/scripts/extract_frames.py video.mp4
```

This one shells out to `ffmpeg` and `ffprobe`; if either is missing, `references/install.md` has
the install per OS.

Frames land in `frames/`, named by timestamp (`t00022.5.png` is 22.5 seconds), and the script prints
the moments the picture changed. Two kinds arrive: a frame taken at each of those moments, and a
sweep across the whole video.

Frames are free to make and cost about 800 tokens each to read, so read deliberately, in this order:

1. **The moments the picture changed.** The script lists them. A caption appearing is a picture
   change, so this is where text on screen shows up.
2. **The pointer moments.** Scan the transcript for someone saying *this*, *these*, *here*, *this
   website*, *these two*, *link in bio*, *this command*, *this repo*. Those are the moments the
   meaning is on screen and not in the words. Take the timestamp and read the frame nearest it.
3. **A sweep** for anything the first two missed. On a short video that is a handful of frames. On
   anything past a couple of minutes, skip it — by then the sweep is mostly re-reading a person
   sitting still, and the first two passes have done the work.

If something looks half-caught — a command scrolling, a URL partly covered — read the neighbouring
frames.

Write what the screen gave you into `findings.md`: names, URLs, commands, versions, verbatim, each
with its timestamp.

### 5. Follow what it names

Now research what the video pointed at, since that is where the substance is.

**Check whether it already exists first.** Tools increasingly ship their own skills or plugins. If
the thing the video recommends has an official one, say so and recommend installing that rather than
writing a worse copy of it. Sometimes the right output here is not a new skill at all, and saying so
is more useful than building something redundant.

Otherwise read the real source: the library's documentation, the repo, the site. Use the Context7
MCP for library documentation where it covers the library, and fetch the page otherwise. What you
are after is what the video assumed you already knew — the actual commands, the current API, the
version-specific detail a thirty-second clip cannot carry. **Anything the video named that you could
not verify is a finding**, not something to quietly drop.

Read first and report what you found, rather than asking permission to look — the reading is quick,
and the findings are what make the interview questions worth answering. If it turns into something
large (a whole repo to clone, hours of documentation), stop and ask before spending that.

Add everything to `findings.md`.

### 6. Brief the user, then ask what they want out of it

**Brief first.** They have not read the transcript, have not seen the frames, and may not remember
the video. Tell them: who made it, what it actually teaches, what the screen gave up that the audio
did not, and what your research found. Where the video is thin, say so — "twenty items with no
method behind them" is useful, and sometimes the right answer is not to build. Where an official
skill already exists, lead with that.

**Then ask what they want out of it**, using AskUserQuestion. The same video can be worth any of
these, and more than one at once:

- **A skill or agent** — the video teaches a method they will want again, in other conversations.
- **Changes made now** — the video shows something worth doing to the project they are sitting in:
  a rule for CLAUDE.md, a shape for the README, a tool to install, a technique to adopt in the code,
  a setting to change. Done today, in this conversation.
- **Just the notes** — they wanted to know what it said. `findings.md` already is the notes.

The brief is what makes this answerable — "it gives you an install command, a habit worth a line in
CLAUDE.md, and a technique that would suit a skill" is a question they can answer, and "skill or not?"
asked before the research is a guess about a clip they half remember. That is why the question comes
here and not at the start.

If their request already said which — "skill this", "apply this to the repo", "what does this
teach" — do not ask; go on what they said. A single question is the ceiling here; the interview for
the route they chose is what follows.

**For a skill or agent**, ask only what genuinely changes what gets built:

- **Skill or agent?** A skill teaches a method applied inside a conversation; an agent is dispatched
  to go and do the job. When it could be either, recommend skill — it can be promoted later.
- **What is in scope?** Videos teach several things at once. Which part is worth capturing?
- **When should it trigger?** The phrases they would actually type. This decides whether the skill
  ever fires, so it deserves a real answer rather than a guess from the title.
- **What must it not do?** Cheapest thing to settle up front, most annoying to discover later.
- **Anything needing credentials or installs?** See "Dependencies and credentials" below.

Ask what this particular video makes uncertain. Two well-chosen questions beat four obvious ones.

**For changes made now**, the user steers and you make it concrete. Ask what they want done, in their
words, and let it be as large or as small as they say — a one-line rule and a new library wired
through the codebase are both legitimate answers, and the size is theirs to set, not yours to trim.
Then look at whatever that answer needs looked at, and nothing more: a CLAUDE.md rule needs the
current CLAUDE.md read so the proposal fits what is already there and does not contradict it; a
README change needs the README; adopting a library needs the code it would touch. Reading the repo
is in service of a request that needs it, not a step of its own — "make this a skill" needs none
of it, and reading a project uninvited is its own kind of running off.

Come back with the proposal spelled out — each file it would touch and what would change in it,
in enough detail that a "yes" means something. For a small change that is the edit itself,
described; for a large one it is a plan they can argue with. Get the yes before touching anything,
and where the proposal has a real fork in it, put the fork to them rather than picking.

### 7. Do what they chose

**A skill or agent: hand to skill-creator.** Load the `skill-creator` skill — this is the "second
rule" above, and it is not optional — and give it `findings.md`, the transcript, the caption, the
handle, the link, and the interview answers. Tell it the scoping interview is done so it does not
repeat it.

Write nothing yourself. If the answer turned out to be "this is not worth a skill", that is a valid
end to a run: say so, index it as such, and stop. Do not write a thin skill to have produced
something.

skill-creator will offer to build an evaluation harness and benchmark the new skill. That is
genuinely useful but much longer work — ask whether the user wants it rather than starting it.

**Changes made now: make them, as agreed.** Do exactly the proposal they said yes to — the file
they were shown, the change they were shown. Where doing it turns up something the proposal did not
foresee (the README section already exists under another name, the install fails, the library
needs a version the project cannot take), stop and say so rather than improvising around it: a
change they did not see is a change they did not agree to. If the project has its own way of
working — a CLAUDE.md, a contributing guide, a test suite — the change follows it, and the change is
proved the way that project proves things before it is called done.

**Just the notes: stop here.** Tidy `findings.md` so it reads top to bottom — source, what it
teaches, what the screen gave, what the research found — and say where it is. Nothing else is
produced.

**Both a skill and changes:** the changes first, then the skill. Making the change is the quickest
way to find out what the video left out, and a skill written after that is written from something
that has worked once rather than from the transcript.

### 8. Close the run, then report

Finish `findings.md` with a one-line **Verdict**: what came of this, in the plainest terms. "No skill
— an official one already exists." "Folded one idea into `ui-development`." "Built `x`." "Added the
commit-message rule to `~/code/foo/CLAUDE.md`." "Notes only." "Not worth building."

That line is what step 0 reads when the same video turns up again, and the "not worth building" ones
matter most — without them only successes leave a trace, and the same dead end gets researched twice.
It lives in the run's own file because that file is being written anyway; a separate register of runs
would be a second copy of what the folder already says, and it would go stale the first time one was
renamed. A change made to a project names the project, because the run folder is shared across every
project the user has and "added a rule to CLAUDE.md" is otherwise unplaceable a month later.

Then report. For a skill: where it landed, what triggers it, what it needs installed or configured,
and where the run folder is. Suggest testing it once while the video is fresh — that is when they can
still tell whether it caught the point. For changes made now: each file touched and how it was proved.
In both cases, anything the video named that you could not verify, so it is not mistaken for settled.

## What every generated skill must do

Every skill or agent produced here opens by asking the user how it should run, using
AskUserQuestion, before producing anything. This exists because their complaint about generated
tooling is that it runs off and builds something nobody agreed to.

Judgement matters more than compliance. Ask about choices that genuinely change the output — scope,
destination, depth, format, tone — and leave out anything with an obvious default. A skill that
interrogates someone about trivia is worse than one that just ran. One or two real questions is
usually right; if a skill has nothing worth asking, say so during the interview rather than
inventing questions to satisfy the rule.

Include a section like this in the generated skill:

```markdown
## Before running

Ask the user how this run should go, using AskUserQuestion, before producing anything:

- <the choice that most changes the output, with 2-4 concrete options>
- <a second, only if it genuinely matters>

If the user already answered these in their request, do not ask again — proceed on what they said.
```

That last line matters. Asking something they have already told you reads as not having listened.

## Dependencies and credentials

Most skills worth having depend on something. Three kinds, and they rot differently:

**Knowledge** — docs or a repo that matter for what they teach. Read them once now and distil into
`references/` inside the skill. Do not keep a live clone: it goes stale and nobody notices.

**Tools** — something the skill actually runs. Record the install command in the skill, have it
check the tool is present on first use, and install if missing. The Python environment this skill
builds for itself is the pattern.

**Services** — anything needing a key. Keys go in **`~/.claude/.env`**, one file shared by every
skill, and the skill names the variables it needs and reads them from there at runtime.

Never put a key inside the skill's own folder, and never write one into SKILL.md or `references/`.
Two reasons, both concrete: skills get packaged and shared — skill-creator has a script that zips a
skill folder into a shareable file, and a key inside it ships with it. And anything in the skill's
markdown is read into the conversation, so it lands in context and in logs, whereas a key loaded by
a script at runtime never appears.

If a required variable is missing, the skill should say which one and where to put it, rather than
failing with a cryptic authentication error from three layers down.

## Sharing this skill

When the user wants to give this skill to someone, package it with skill-creator's script, which
validates the frontmatter and zips the folder into a single `.skill` file:

```bash
cd ~/.claude/skills/skill-creator
PYTHONUTF8=1 python -m scripts.package_skill ~/.claude/skills/source-to-skill ~/Desktop
```

`PYTHONUTF8=1` is for Windows, where the console defaults to an encoding that cannot print the
script's emoji and it crashes before packaging anything; elsewhere it changes nothing. The script
also validates the frontmatter first, and its ceiling for the description is 1024 characters —
an edit to the description gets checked here whether or not anyone meant it to be.

The archive must not contain `.venv`. It is a quarter of a gigabyte of compiled libraries for one
OS, and it is rebuilt on the recipient's machine from `requirements.txt` in a minute — the
"Tools" pattern above. The packager skips it; if a listing of the archive shows `.venv` anyway, the
packager is an older copy, and the fix is adding `".venv"` to its `EXCLUDE_DIRS` rather than
shipping the file. What ships is `SKILL.md`, `requirements.txt`, `scripts/` and `references/` — a
few kilobytes.

Tell the recipient four things: unzip it into `~/.claude/skills/source-to-skill/` (a `.skill` file
is a zip with a different extension); install `skill-creator` beside it if they do not have it,
because the skill-making route loads it and is dead without it — it is Anthropic's, from their
public skills repository, and packaging its folder the same way gives them a copy; install `uv` and
`ffmpeg` if they have neither (the skill will point them at `references/install.md` the first time
it needs them); and paste a video link. Nothing in the folder is tied to the sender's machine, and
no keys are inside it — see "Dependencies and credentials" for why none ever should be.

## When it fails

**Rate limited, or redirected to a login page.** Instagram limits anonymous fetching per IP address
and it clears in roughly a day. Say that plainly and stop. Do not reach for cookies: yt-dlp's own
documentation warns that using an account with it risks that account being banned permanently, and
Instagram is specifically known to detect and act on it. A day's wait is cheaper than an account,
and public posts do not need a login.

**A photo post or carousel.** No audio track, but the frames still hold everything — read the images
and the caption, and say that is what you did.

**A transcript that is empty or one phrase looping.** Music-only. Say so and work from the screen
and the caption, which for this kind of video is usually where the content was anyway.

**Anything else.** Report which step failed and what it said, then stop cleanly. Do not retry
blindly against a rate limit — that is how a temporary block becomes a longer one.
