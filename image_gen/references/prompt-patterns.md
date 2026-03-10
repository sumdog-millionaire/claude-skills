# Prompt Patterns Reference

Detailed prompt templates and examples for each image type and visual style. Read the main SKILL.md first for provider selection, defaults, and workflow.

---

## Icon Prompts

### Single icon (generate_image)

**Template:**
```
Flat filled icon representing [concept]: [2-3 specific visual details],
[colour with hex code] on transparent background, clean minimal design,
[domain] icon style, solid shapes, no outlines, no text, no gradients
```

**Examples:**

Pain / time pressure:
```
Flat filled icon representing time pressure: a clock face with hands at 
11:55 and a small warning triangle, white (#FFFFFF) on transparent background,
clean minimal design, business compliance icon style, solid shapes, 
no outlines, no text, no gradients
```

Solution / AI analysis:
```
Flat filled icon representing AI document analysis: a magnifying glass 
overlapping a document page with three highlighted rows, white (#FFFFFF) 
on transparent background, clean minimal design, technology icon style,
solid shapes, no outlines, no text, no gradients
```

Value / speed:
```
Flat filled icon representing speed and efficiency: a lightning bolt 
overlapping a circular arrow, white (#FFFFFF) on transparent background,
clean minimal design, business performance icon style, solid shapes,
no outlines, no text, no gradients
```

### Tool parameters for single icons:
```
provider: "openai"
background: "transparent"
aspect_ratio: "square"
quality: "low" (drafts) or "medium" (finals)
output_format: "png"
category: "icons"
```

---

### Icon sheet (generate_icon_sheet)

**Template:**
```
[count] flat filled icons for [context]: [concept 1 with brief visual], 
[concept 2 with brief visual], [concept 3 with brief visual], ...,
[colour constraint], minimal detail, solid shapes, consistent weight and 
style across all icons, professional [domain] style, no text labels,
no outlines, no gradients
```

**Example — compliance inspection pain points (6 icons):**
```
6 flat filled icons for regulatory compliance problems: clock with warning 
symbol, tall stack of paper documents, magnifying glass with question mark,
pound sterling coin with downward arrow, person overwhelmed at desk,
broken chain link — white icons on transparent background, single consistent 
style, minimal detail, solid shapes, no text, no outlines
```

**Example — solution capabilities (4 icons):**
```
4 flat filled icons for AI document processing: cloud with upward arrow 
for upload, brain circuit for AI analysis, checklist with magnifying glass 
for review, document with ribbon seal for final report — white icons on 
transparent background, consistent flat style, solid shapes, no text
```

### Tool parameters for icon sheets:
```
provider: "openai"
count: 6 (default) or as needed
style: "flat filled solid shapes, single colour, minimal detail, no outlines, professional business style"
category: "icons/sheets"
```

### Ensuring consistency across a sheet
- Describe all icons in one prompt rather than generating individually
- Use the same visual weight language for each: "minimal detail, solid shapes"
- Specify "consistent weight and style across all icons"
- If individual icons from separate calls look inconsistent, regenerate as a single sheet

---

## Vector (SVG) Prompts

### Simple icon vectors (generate_vector)

**Template:**
```
Simple flat vector icon: [concept with visual description], [colour],
minimal geometric shapes, clean edges, suitable for SVG editing,
no gradients, no shadows, no text, [domain] style
```

**Example:**
```
Simple flat vector icon: a shield with a checkmark inside, dark green 
(#0A4D1C), minimal geometric shapes, clean edges, suitable for SVG 
editing, no gradients, no shadows, no text, compliance technology style
```

### Diagram vectors

**Template:**
```
Clean flat vector diagram: [diagram type] showing [concept], [colour palette],
simple geometric shapes, professional infographic style, clean connecting lines,
no text labels, no shadows, no photorealistic elements
```

**Example:**
```
Clean flat vector diagram: hub and spoke with central hexagon connected 
to 5 satellite circles by thin lines, dark green centre (#0A4D1C) with 
teal (#0C7C6B) satellites, simple geometric shapes, professional 
infographic style, clean connecting lines, no text labels
```

### Tool parameters for vectors:
```
quality: "standard" (drafts) or "pro" (finals)
category: "vectors"
style: "flat minimal, clean geometric, no gradients" (or user-specified)
```

### SVG prompt tips
- Keep descriptions simpler than raster prompts — complexity creates messy vectors
- Specify "geometric shapes" to encourage clean paths
- Always include "no gradients, no shadows" — these are hard to edit in SVGs
- Recraft handles flat colour areas well but struggles with intricate detail

---

## Conceptual / Hero Image Prompts

Style-specific templates. **Ask the user which style before using these.**

### Style 1: Flat Illustration
Clean, vector-style illustrations. Think Stripe, Linear, or Notion marketing pages.

**Template:**
```
Flat illustration, [scene description], [colour palette with hex codes],
clean vector art style, smooth shapes, subtle shadows only, modern tech 
aesthetic, [composition notes], no text, no UI elements, no watermarks,
for [intended use]
```

**Example:**
```
Flat illustration, a regulatory inspector reviewing digital documents on 
a large screen while AI highlights key passages, dark green (#0A4D1C) and 
teal (#0C7C6B) colour palette with white and light grey accents, clean 
vector art style, smooth shapes, subtle shadows only, modern tech aesthetic,
centred composition with negative space on the right for text overlay,
no text, no UI elements, for a presentation title slide background
```

### Style 2: Abstract Geometric
Shapes, gradients, and patterns. Good for backgrounds and mood-setting.

**Template:**
```
Abstract geometric composition, [description of shapes and arrangement],
[colour palette with hex codes], smooth gradients, overlapping transparent 
shapes, modern minimalist style, [composition notes], no text, no icons,
no figurative elements, for [intended use]
```

**Example:**
```
Abstract geometric composition, overlapping circles and angular shapes 
suggesting data flow and analysis, dark green (#0A4D1C) to teal (#0C7C6B) 
gradient with amber (#C8952E) accent shapes, smooth gradients, overlapping 
transparent shapes, modern minimalist style, weight towards the left side 
with open space on the right, no text, for a slide deck title background
```

### Style 3: Isometric
3D-ish technical diagrams. Good for process explanations and technical concepts.

**Template:**
```
Isometric illustration, [scene/object description], [colour palette], 
clean isometric perspective, flat shading, no realistic textures, 
modern technical diagram style, [composition notes], no text labels,
no people, for [intended use]
```

**Example:**
```
Isometric illustration, a conveyor belt of documents being fed into a 
glowing analysis machine that outputs organised report folders, dark green 
and teal colour palette, clean isometric perspective, flat shading, 
no realistic textures, modern technical diagram style, centred composition,
no text labels, for a solution overview slide
```

### Style 4: Photorealistic
Stock-photo quality but AI-generated. Use sparingly — real photography often looks better.

**Template:**
```
Professional photograph, [scene description], [lighting and mood],
[colour temperature], sharp focus, shallow depth of field, high quality,
editorial style, [composition notes], no text, no watermarks,
for [intended use]
```

**Example:**
```
Professional photograph, close-up of a legal professional reviewing 
documents at a modern desk with a laptop showing data analytics, 
warm natural lighting from a window, neutral colour temperature, 
sharp focus on the documents, shallow depth of field, high quality, 
editorial style, rule of thirds composition with space for text overlay 
on the left, no text, no watermarks, for a one-pager hero image
```

### Style 5: Minimal Line Art
Simple outlines with accent colour fills. Clean and distinctive.

**Template:**
```
Minimal line art illustration, [subject description], thin [colour] outlines 
on white/transparent background, selective [accent colour] fills on key 
elements, clean hand-drawn style but precise, generous negative space,
no shading, no gradients, for [intended use]
```

**Example:**
```
Minimal line art illustration, a stack of documents being transformed into 
a clean organised report with a small star/sparkle, thin dark green (#0A4D1C) 
outlines on transparent background, selective teal (#0C7C6B) fills on the 
final report, clean precise line style, generous negative space, no shading, 
no gradients, for presentation section divider
```

---

## Troubleshooting

| Problem | Likely cause | Fix |
|---------|-------------|-----|
| Icons have unwanted text/labels | Models default to adding text | Add "no text, no labels, no words, no letters" explicitly |
| Icons look inconsistent | Generated individually | Regenerate as an icon sheet for consistency |
| SVG is too complex / messy paths | Prompt too detailed | Simplify description, add "geometric shapes, clean edges" |
| Colours don't match brand | Missing hex codes | Always include exact hex codes, not just colour names |
| Image too busy / cluttered | Over-described | Cut description to essentials, add "minimal", "clean", "negative space" |
| Wrong aspect ratio | Defaulted to square | Explicitly set aspect_ratio based on intended use |
| Background not transparent | Forgot parameter | Set `background: "transparent"` — only works with OpenAI provider |
| Photorealistic looks AI-generated | Quality too low / prompt too generic | Use `quality: "high"`, add specific lighting and composition details |
