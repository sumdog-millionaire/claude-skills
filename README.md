# Claude skills

Benedict's skills for [Claude Code](https://claude.com/claude-code). This repository is the global
skills folder itself: it is cloned to `~/.claude/skills/`, and Claude Code loads every skill in it on
every session, in every project.

## What is in it

| Folder | What it does |
|---|---|
| `anti-ai-slop-writing/` | the writing standard for anything a person reads as a finished piece |
| `prepare-rewind/`, `carry-on-rewind/` | write a handover before the conversation is rewound, then resume from it |
| `video-digest/` | turn a recorded meeting or video into a timestamped evidence map of what was said and shown |
| `source-to-skill/` | learn from a video, then build a skill, change the project, or keep the notes |
| `launch-checklist/` | check a website against twenty pre-launch essentials and build the ones approved |
| `marketing_materials/` | the design system for branded decks, one-pagers and documents |
| `image_gen/` | prompt patterns and model choice for image generation |
| `skill-creator/` | Anthropic's skill for writing and testing skills (its own licence is in the folder) |
| `ui-dev/` | a plugin, not a single skill: fifteen skills and a hook for designing and building interfaces. It has its own README. |
| `mattpocock-skills/` | a plugin: Matt Pocock's engineering skills (grilling, implement, to-tickets, triage, tdd and the rest) with Benedict's changes |

A folder with a `SKILL.md` at its top is one skill. A folder with `.claude-plugin/plugin.json` is a
plugin, which Claude Code loads from here in the same way and lists as `<name>@skills-dir`.

## Install on a machine

```powershell
git clone https://github.com/sumdog-millionaire/claude-skills.git "$HOME/.claude/skills"
```

If `~/.claude/skills` already exists, move its contents out first, clone, then move back anything
this repository does not hold. Restart Claude Code afterwards.

Three folders need one more step each:

- `ui-dev/`: `npm ci --omit=dev`, and a Stitch API key in `ui-dev/.env` (see its README).
- `video-digest/` and `source-to-skill/`: a Python environment from each folder's `requirements.txt`.


## Change a skill

Ask the agent to edit the skill where it is installed. The edit is live in the next session. Then,
from `~/.claude/skills/`:

```powershell
git add -A
git commit -m "what changed, and why"
git push
```

On another machine, `git pull` in `~/.claude/skills/` brings the change in.

On a machine that cannot push to this repository (a work account, for example), fork it on GitHub,
clone the fork to `~/.claude/skills/`, push there, and open a pull request back to this repository.

### Take Matt Pocock's updates

`mattpocock-skills/` is Benedict's version of [`mattpocock/skills`](https://github.com/mattpocock/skills),
kept here as a git subtree: an ordinary folder that git can still merge his repository into. Edit it
like any other folder. To take his updates, from `~/.claude/skills/` with nothing uncommitted:

```powershell
git subtree pull --prefix=mattpocock-skills https://github.com/mattpocock/skills.git main --squash
git push
```

Git merges his changes into the folder and keeps the edits made here. Where both changed the same
lines it stops with a conflict to resolve, as any merge does.

## What is not here

`.env` files, `node_modules/`, `.venv/` and `synced/` (the skills Claude syncs from the account) stay
on each machine and are never committed.
