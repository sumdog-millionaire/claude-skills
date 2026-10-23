# Claude skills

Benedict's skills for [Claude Code](https://claude.com/claude-code). This repository is the global
skills folder itself: it is cloned to `~/.claude/skills/`, and Claude Code loads every skill in it on
every session, in every project.

## What is in it

| Folder | What it does |
|---|---|
| `anti-ai-slop-writing/` | the writing standard for anything a person reads as a finished piece |
| `maintain-mattpocock-fork/` | how to edit `mattpocock-skills/` and take Matt Pocock's updates into it |
| `video-digest/` | turn a recorded meeting or video into a timestamped evidence map of what was said and shown |
| `marketing_materials/` | the design system for branded decks, one-pagers and documents |
| `ui-dev/` | a plugin, not a single skill: fifteen skills and a hook for designing and building interfaces. It has its own README. |
| `mattpocock-skills/` | a plugin: Matt Pocock's engineering skills (grilling, implement, to-tickets, triage, tdd and the rest) with Benedict's changes, including the rewind skills `prepare-rewind` and `carry-on-rewind` |

A folder with a `SKILL.md` at its top is one skill. A folder with `.claude-plugin/plugin.json` is a
plugin, which Claude Code loads from here in the same way and lists as `<name>@skills-dir`.

## Install on a machine

Every command in this file runs as written in bash (Linux and macOS) and in PowerShell (Windows).

```
git clone https://github.com/sumdog-millionaire/claude-skills.git "$HOME/.claude/skills"
```

If `~/.claude/skills` already exists, back it up and install in place; this replaces only the folders
this repository holds:

```
cd "$HOME/.claude/skills"
git init -b main
git remote add origin https://github.com/sumdog-millionaire/claude-skills.git
git fetch origin
git checkout -f -B main --track origin/main
```

Restart Claude Code afterwards.

`.gitignore` is an allowlist: it ignores every top-level folder except this repository's own, so a
skill installed on one machine only (`data-model`, the Azure skills) is never committed. To add a
skill to the repository, add a `!/<folder>/` line for it.

Two folders need one more step each:

- `ui-dev/`: `npm ci --omit=dev`, and a Stitch API key in `ui-dev/.env` (see its README).
- `video-digest/`: `uv` and `ffmpeg` on the path. `uv run` builds its Python environment on first use
  (see `video-digest/references/install.md`).


## Change a skill

Ask the agent to edit the skill where it is installed. The edit is live in the next session. Then,
from `~/.claude/skills/`:

```
git add -A
git commit -m "what changed, and why"
git push
```

On another machine, `git pull` in `~/.claude/skills/` brings the change in.

On a machine that cannot push to this repository (a work account, for example), fork it on GitHub,
clone the fork to `~/.claude/skills/`, push there, and open a pull request back to this repository.

### Take Matt Pocock's updates

`mattpocock-skills/` is Benedict's version of [`mattpocock/skills`](https://github.com/mattpocock/skills),
kept here as a git subtree. To take his updates, from `~/.claude/skills/` with nothing uncommitted under
it, run `git subtree pull --prefix=mattpocock-skills https://github.com/mattpocock/skills.git main --squash`.
The `maintain-mattpocock-fork` skill holds the rest: how to edit the fork, how to resolve a pull, and
which differences from his repository are deliberate.

## What is not here

`.env` files, `node_modules/`, `.venv/` and `synced/` (the skills Claude syncs from the account) stay
on each machine and are never committed.
