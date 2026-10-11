# ui-dev

A Claude Code plugin for designing and building interfaces: web pages and web apps, with the phone
and native surfaces handled by the skills beside the design skill. One design skill routes the work
by what the visitor is there to do, hands motion to Emil Kowalski's skills, drives Google Stitch
through its MCP server, and runs the Impeccable detector quietly after every edit.

This folder is the source. It is part of the skills repository (`sumdog-millionaire/claude-skills`),
which is cloned in place at `~/.claude/skills/`, and Claude Code loads this folder as a plugin on
every session, hooks included. Edit here, then commit and push from `~/.claude/skills/`.

## What is in it

| Path | Holds |
|---|---|
| `skills/ui-dev/` | the design skill: a short body that reads the brief and picks a mode, plus references loaded on demand |
| `skills/animate`, `animate-expo`, `review-animations`, `improve-animations`, `pick-ui-library`, `prototype`, `apple-design`, `write-swift` | Emil Kowalski's skills, vendored; `ui-dev` hands all interface motion to `animate` |
| `skills/extract-static-html`, `upload-to-stitch`, `extract-design-md`, `react-components` | four of Google's Stitch skills, vendored: capture a running screen as one HTML file, post images and HTML to Stitch over REST, read a DESIGN.md out of existing source, turn a Stitch screen into React |
| `skills/ux-playbook/` | how components and screens behave: loading, errors, forms, empty states, success feedback, partial failure, button states, placement, choices, progressive disclosure; `ui-dev` takes it at the brief, the Stitch hand-over, the state pass and verification, and any UX review can load it alone |
| `skills/upstream-review/` | the maintenance skill: walks `upstream.json`, diffs each source since the reviewed commit, proposes adopt, adapt or skip |
| `hooks/`, `scripts/` | the Impeccable detector adapter: a PostToolUse check after every Edit or Write, a deeper pass at the end of a turn |
| `extensions/` | the same adapter for Pi |
| `upstream.json` | every source this plugin took text or files from, with the commit last reviewed |

## Install on a machine

The folder arrives with the skills repository (see the README one level up). Then:

```powershell
cd "$HOME/.claude/skills/ui-dev"
npm ci --omit=dev          # the pinned Impeccable detector binary; Node 22.18 or newer
copy .env.example .env     # then put the Stitch API key in it (used only by the upload script)
```

Restart Claude Code. The plugin appears as `ui-dev@skills-dir`; `/ui-dev:ui-dev` starts design work
and `/ui-dev:upstream-review` runs the maintenance pass.

### Companions, not bundled

`ui-dev` calls these by name when they are installed and says so when they are not:

- **grilling** (Matt Pocock's plugin): resolves the design decisions for a new direction.
- **anti-ai-slop-writing** (`~/.claude/skills`): the writing standard for anything a person reads.

### Stitch

Create an API key in Stitch settings, then:

```powershell
claude mcp add stitch --transport http https://stitch.googleapis.com/mcp --header "X-Goog-Api-Key: <key>" -s user
```

The same key goes in `.env` for the upload script. Nothing here stores it anywhere else.

A Stitch generation takes minutes and the MCP client gives up at about 150 seconds, so set
`MCP_TOOL_TIMEOUT=600000` in Claude Code's environment (the `env` block of `settings.json`) before
using the Stitch route.

## The detector

The hooks run Impeccable's detector (npm `impeccable`, pinned in `package.json`) on every Edit or
Write of a UI file and once more when a turn ends. Clean results are silent; findings reach the agent
with the command to record a narrow exception, and the end-of-turn pass blocks the turn until they
are dealt with. Project settings in `.impeccable/config.json` are respected.

Run it by hand from the project being checked:

```powershell
node "$HOME/.claude/skills/ui-dev/scripts/impeccable.ts" detect frontend/
```

## Keeping up with upstream

`/ui-dev:upstream-review` fetches each repository in `upstream.json`, shows what changed in the
watched paths since the commit last reviewed, and waits for a choice per change. Nothing is
replaced wholesale; vendored copies keep their local edits.

## Attribution

Taste by Leonxlnx (MIT, `LICENSE`), Emil Kowalski's skills (MIT), Impeccable by Paul Bakaus
(Apache 2.0, used as a pinned executable), and Google's Stitch skills (Apache 2.0). Commits reviewed
are in `upstream.json`.
