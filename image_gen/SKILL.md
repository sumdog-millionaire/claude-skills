---
name: image-gen
description: "Prompt engineering and model selection for AI image generation via the corporate-imgen MCP. Use this skill whenever generating images — icons, icon sheets, diagrams, illustrations, hero images, backgrounds, or SVG vectors. Trigger whenever you're about to use generate_image, generate_icon_sheet, or generate_vector tools, or when the user asks for visual assets. Also trigger when a brand design system skill (e.g. marketing-materials) references image generation."
---

# Image Generation Skill

Prompt engineering layer for the `corporate-imgen` MCP. This skill tells you what to generate, how to prompt, and which tool/provider to use. See [references/prompt-patterns.md](references/prompt-patterns.md) for ready-to-adapt templates.

## Tool & Provider Selection

| Need | Tool | Provider |
|------|------|----------|
| Icon (transparent bg) | `generate_image` | `openai` |
| Set of related icons | `generate_icon_sheet` | `openai` |
| Icon (SVG, editable) | `generate_vector` | `recraft` |
| Illustration / hero image | `generate_image` | `openai` |
| Editable diagram (SVG) | `generate_vector` | `recraft` |

**OpenAI**: photorealism, complex scenes, transparent backgrounds. Most raster needs.
**Recraft V4**: vectors, clean SVGs, editable paths. Use when output needs to scale or be edited.

## Defaults by Image Type

### Icons
- **Style**: Flat filled, solid colour shapes, no outlines, no gradients, no text/labels
- **Background**: Always `"transparent"`
- **Colour**: Max 2-3 tones of a single hue. If a brand system is active, match the relevant section colour. If not, default to neutral dark grey (`#333333`).
- **Quality**: `"low"` — icons are small in final output. Use `"medium"` only if displayed >200px.
- **Always include hex codes** in prompts — models interpret colour names loosely

### Hero / Conceptual Images
- **Ask the user** about visual style before generating (flat illustration, abstract geometric, isometric, photorealistic, minimal line art)
- **Don't auto-inject brand colours** — these benefit from natural palettes. Only use brand colours if explicitly requested.
- **Quality**: `"medium"` minimum, `"high"` for full-bleed backgrounds
- **Aspect ratio**: Landscape for slides/banners, portrait for one-pager heroes, square for social/unknown

### SVG Vectors
- **Quality**: `"standard"` for most, `"pro"` for complex illustrations
- Flat colour, no gradients, 2-4 colours max, clean geometric forms
- Keep prompts simpler than raster — complexity creates messy vector paths

## Brand Colour Integration

| Image type | Inject brand colours? |
|-----------|----------------------|
| Icons / icon sheets | **Yes** — map to section accent colours |
| Diagrams / frameworks | **Yes** — use brand primary and accents |
| Hero / conceptual images | **No** — natural palettes unless user asks |
| Backgrounds / textures | Only if abstract/geometric behind branded content |

Always include both colour name AND hex code: `Single colour (teal, hex #0C7C6B, tones only)`

## Prompt Principles

1. Lead with style, then content: "Flat illustration: a document being scanned"
2. Specify what you don't want: "No text, no watermarks, no 3D effects"
3. Describe composition and intended use for context
4. One concept per image — generate separately for complex sets
5. Always end with: "No text, no watermarks"

## Before Every Call

- Set `category` for auto-organisation (e.g. `icons`, `backgrounds`, `diagrams`, `vectors`, `project/{name}`)
- Check `list_categories` for existing assets to avoid regenerating
- Match `aspect_ratio` to intended use
