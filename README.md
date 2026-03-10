# Claude Code Skills

Personal skills library for [Claude Code](https://claude.ai/claude-code). These are installed at `~/.claude/skills/` and available across all projects.

## Skills

### `marketing_materials/`
Design system for branded one-pagers, pitch decks, and professional documents. Includes:
- **Component library** — 33 reusable HTML/SVG components across 8 categories (backgrounds, callouts, CTAs, decorative, process flows, section dividers, layouts, stat displays)
- **Brand guidelines** — colours, fonts, tone, logo assets
- **Format references** — one-pager and deck templates

### `image_gen/`
Prompt engineering patterns for the corporate-imgen MCP. Covers icon generation, hero images, SVG vectors, and brand colour integration.

## Usage

These skills are triggered automatically by Claude Code when relevant tasks are detected (e.g. creating a one-pager, generating images). They can also be invoked manually via `/marketing_materials` or `/image_gen`.

## Structure

```
skills/
├── image_gen/
│   ├── SKILL.md
│   └── references/
│       └── prompt-patterns.md
└── marketing_materials/
    ├── SKILL.md
    ├── brand/
    │   ├── brand_guidelines.md
    │   └── assets/
    ├── components/
    │   ├── catalogue.md
    │   ├── backgrounds/
    │   ├── callouts/
    │   ├── cta_blocks/
    │   ├── decorative/
    │   ├── process_flows/
    │   ├── section_dividers/
    │   ├── section_layouts/
    │   └── stat_displays/
    └── references/
        ├── one-pager.md
        └── deck.md
```
