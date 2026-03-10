---
name: marketing-materials
description: "Document design system for creating branded presentations, one-pagers, pitch decks, and professional marketing materials. Use this skill whenever creating ANY client-facing document — including slide decks (.pptx), one-pagers, pitch materials, PDFs, HTML documents, or Gamma presentations. Also trigger when the user mentions 'deck', 'one-pager', 'pitch', 'brand guidelines', 'Sumplexity deck', 'Sumplexity one-pager', 'CLC pitch', or asks to create client-facing or marketing documents. This skill defines the narrative structure, layout patterns, and quality gates — it works alongside output-format skills (pptx, pdf, etc.). Brand-specific identity (colours, fonts, tone, audiences) lives in brand/brand_guidelines.md. Always read this skill FIRST for design direction, then read the brand guidelines and the relevant output-format skill for technical execution."
---

# Document Design System

This skill covers design methodology, narrative structure, layout patterns, and quality gates for creating professional documents. It is format-agnostic — it works with PPTX, Gamma, HTML, PDF, or any other output format.

Brand identity, colours, typography, audience adaptation, and boilerplate content live in a separate file so they can be updated independently. Read [brand/brand_guidelines.md](brand/brand_guidelines.md) for all brand-specific details.

After reading this skill and the brand guidelines, read the relevant output-format skill (pptx, pdf, etc.) for technical implementation.

## Workflow

### Pre-flight Checks
Before creating any document, verify these are available:
1. **Playwright MCP** — required for visual preview and PDF generation. Run `browser_navigate` to confirm it's working. If not available, inform the user and help them set it up.
2. **Brand guidelines** — read [brand/brand_guidelines.md](brand/brand_guidelines.md) for logo assets, colours, typography, tone, and audience guidance.
3. **Component library** — run `python components/build_catalogue.py` to auto-generate the catalogue, then read `components/catalogue.md` to see available design patterns.

### Execution Steps
1. **Read this skill** for design methodology, narrative, and quality gates
2. **Read [brand/brand_guidelines.md](brand/brand_guidelines.md)** for brand identity, colours, audiences, and tone
3. **Determine document type** — one-pager or deck (see below)
4. **Determine audience** — adapt depth and emphasis (see Audience Adaptation in brand guidelines)
5. **Ask the user about design preferences** (see User Preference Discovery below)
6. **Read the detailed reference file** for the document type:
   - **One-pagers**: Read [references/one-pager.md](references/one-pager.md)
   - **Decks**: Read [references/deck.md](references/deck.md)
7. **Browse the component library** — read `components/catalogue.md` for visual inspiration
8. **Create the document** as HTML with inline CSS
9. **Preview with Playwright** — navigate to the HTML file and take a screenshot
10. **Run quality gates** (see Quality Gates below) — fix any issues
11. **Export to PDF** via Playwright's `page.pdf()` for one-pagers (see PDF Export below)
12. **If generating images**, read the image generation skill for prompt engineering

### User Preference Discovery
Before starting design work, ask the user:
- **Do you have a visual style preference?** (e.g. "chevron flow", "hexagonal", "editorial", "dark/light split", or "surprise me")
- **Any specific colours or elements to emphasise or avoid?**
- **Is there a reference design you'd like to draw from?** (point them to the component library if unsure)

If the user says "surprise me" or doesn't have preferences, use creative licence — pick 2-3 components from the library and remix them into something fresh. The component library is inspiration, not a template. Combine elements in new ways, invent new patterns, and push beyond what's been done before.

---

## Narrative Structure

All documents follow **Problem → Pain → Solution → Proof → CTA**. This isn't optional — it's the core persuasion architecture.

### Titles Tell the Story — The Narrative Arc

This is the single most important design requirement. Section titles must be **complete, grammatically correct sentences** that read as a continuous narrative when read in sequence. A busy CEO who only reads the titles should understand the full argument.

**Bad (topic labels):** "The Problem" / "Our Solution" / "Key Benefits"
**Bad (too compressed):** "Growing faster" / "Amplify don't replace" / "Already started"

**Good (continuous narrative — each title continues the story):**
1. "Regulatory caseloads aren't just growing, they're evolving — and faster than the teams that handle them"
2. "...which demands a concurrent rise in both throughput and attention to detail"
3. "...with AI-powered tools built around CLC workflows — bespoke, traceable, human-led"
4. "A team that has done this before — and has already started"

**Rules:**
- Titles must be grammatically complete — never truncated or awkward
- Each title should logically flow from the previous one
- Use ellipsis continuation ("...which") between titles where it strengthens the narrative thread
- For decks: one title per slide, the full sentence works well at larger font sizes
- For one-pagers: if space is tight, the titles can be shorter but must still read as a coherent sequence — never sacrifice grammar for space. Adjust the layout to accommodate the titles, not the other way round.
- Draft the full title set first, read them in sequence to check they tell a story, then design the layout around them

### The Five Beats

Each beat has a narrative colour defined in the brand guidelines. Use those colours for section markers, stat numbers, icons, and tinted backgrounds.

| Beat | Purpose | Title pattern |
|------|---------|--------------|
| **Problem** | Establish context and urgency | State the situation the reader recognises |
| **Pain** | Quantify the cost of inaction | Lead with a number or consequence |
| **Solution** | Show the path forward | "We do X so you can Y" |
| **Proof** | Evidence and value | Specific outcomes and capabilities |
| **CTA** | Drive next step | Direct, confident ask |

---

## Document Types

### One-Pager
A single portrait page (A4) that conveys the full narrative arc at scannable density. The reader should grasp the value proposition in under 60 seconds.

**Read [references/one-pager.md](references/one-pager.md) for detailed layout patterns, component library usage, and quality gates.**

**Output format: HTML → PDF via Playwright.** One-pagers are created as HTML with inline CSS, previewed via Playwright MCP, then exported to PDF using `page.pdf()`. This gives pixel-perfect control over clip-paths, gradients, SVG backgrounds, and every CSS feature. The PDF is what gets sent to clients.

Key principles:
- Portrait A4 (210mm × 297mm), fixed height, `overflow: hidden`
- All five narrative beats on one page — no information loss
- Browse `components/catalogue.md` and pick 2-3 components to remix creatively
- Section titles must form a narrative arc (see Titles Tell the Story above)
- Logo must appear (top bar + optionally in proof section)
- Visual variety — use different shapes per section (not all rectangles)
- Subtle background textures (dot grid, hex tile, radial washes)
- Clear section splitting with visual connectors between sections
- Brand-coloured top bar with logo
- No emojis. Ever.

### Deck (Slide Presentation)
Multi-slide presentation (16:9) following one-thing-per-slide discipline. Each slide delivers a single message with visual evidence.

**Read [references/deck.md](references/deck.md) for detailed slide types, layouts, and sequencing.**

Key principles:
- 16:9 aspect ratio
- One message per slide — the title IS the message
- Dark backgrounds for title + CTA slides; white for content slides
- Accent colour bar (4px) at top of each content slide, matching the narrative beat
- Stats displayed as large numbers with small labels below
- Insight/implication boxes at bottom of data slides
- Logo (icon variant) in corner of every slide
- Brand line (2px) at bottom of content slides

---

## Visual Elements

### Icons
Use icons inside coloured circles for visual anchoring. Style should be more illustrative and energetic than the UI system — think PwC-style circular icon badges rather than minimal line icons.

- Circle diameter: 28-36px (one-pagers), 44-60px (slides)
- Circle colour: section accent colour (from brand guidelines)
- Icon colour: white
- Icon stroke: 2px, round caps and joins
- Style: clean line icons, but with slightly more visual weight than standard Feather/Lucide icons

If the image generation MCP is available, use it to generate custom icon sets that are more visually distinctive. Prompt for "flat icon, white on [colour] circle, [description], minimal, professional" style.

### Shapes and Layout Devices
Avoid everything being rectangular grids. Documents should feel dynamic and flowing — think PwC's chevron arrows that point the reader forward, McKinsey's hexagonal frameworks, or EY's circular hub diagrams. The goal is visual momentum: each section should feel like it leads into the next.

**Flowing elements to use:**
- **Chevron / arrow shapes** for process flows — angled shapes that point rightward, each one containing a step. These replace boring numbered lists and create forward momentum.
- **Circular hub diagrams** for showing interconnected concepts — a central circle with radiating spokes or satellite circles.
- **Rounded pill shapes and capsules** for labels, tags, and category markers instead of sharp rectangles.
- **Angled section dividers** — instead of flat horizontal lines between sections, use subtle diagonal or curved dividers.
- **Overlapping circles (Venn-style)** for showing convergence or intersection of ideas.
- **Hexagonal grids** for capability or feature showcases — each hexagon contains an icon + label.
- **Curved connectors** between process steps instead of straight arrows.

**Structural elements (still important):**
- **4px left-edge bars** in section accent colours — these stay. They're the PwC chevron equivalent for vertical sections.
- **Rounded-corner cards** (6-8px radius) with light tint backgrounds — but vary the shapes. Not every card needs to be the same rectangle.
- **Numbered step circles** for process flows (24-28px, accent-coloured) — but consider placing them inside chevrons or connected nodes rather than in a flat row.
- **Gradient line** under top bar (3px) — colours defined in brand guidelines
- **CTA blocks**: Brand primary background with white text and accent highlights

**Layout philosophy:**
- Not every element needs to be axis-aligned. Overlapping shapes, offset cards, and diagonal flows create energy.
- Circles and rounded shapes convey approachability and technology. Rectangles convey rigidity — use them sparingly and always with rounded corners.
- White space is generous but the page should feel full — aim for 85% content density on one-pagers, 60-70% on slides.
- Each section should visually flow into the next. Use shapes that point downward (on one-pagers) or rightward (on slides) to create reading momentum.

### Data Display
- **Stat callouts**: Large number (accent colour) + small label below
- **Comparison grids**: 2×2 or 3-column with icon + title + description
- **Process flows**: Numbered circles connected by arrows
- **Insight boxes**: Light tint background with coloured left border (3px) and bold lead-in

---

## Component Library

A curated library of reusable HTML/CSS design components lives in `components/`. These are extracted from 30+ reviewed designs with user feedback. Component colours are indicative — always apply the colours from `brand/brand_guidelines.md` when building documents.

**Read `components/catalogue.md` for the full index.** Categories:
- `section_dividers/` — chevron, wave, diagonal, hex separator, banner strip
- `stat_displays/` — chevron stats, hex stats, circular badges, progress bars, glass cards
- `process_flows/` — chevron flow, hub-spoke, timeline spine, pipeline
- `backgrounds/` — dot grid, hex tile, radial washes, crosshatch
- `callouts/` — bridge text, connector pills, quote pills, pull quotes
- `section_layouts/` — split contrast, editorial two-column, 2×2 grid, flowing ribbon
- `cta_blocks/` — full-width bar, rounded card
- `decorative/` — accent bar, ambient glows, organic blobs, gradient borders

### How to Use Components
1. Browse the catalogue to see what's available
2. Pick 2-3 components that suit the content and audience
3. **Remix them** — combine elements in new ways, adjust proportions, try new colour combinations within the brand palette
4. **Invent freely** — the library is inspiration, not constraint. If none of the existing patterns fit, create something new. The library should grow over time.
5. Never use a component verbatim without adaptation — every one-pager should feel unique

### Creating New Components
When a design produces a novel pattern the user likes, extract it into the library so future documents can reuse it.

1. **Identify the pattern** — a reusable visual element (layout, stat display, divider, etc.), not a full page
2. **Choose the right category** — place the `.html` file in the matching subdirectory (`stat_displays/`, `section_dividers/`, `backgrounds/`, etc.). If no category fits, create a new subdirectory.
3. **Add the structured comment block** at the top of the file — `build_catalogue.py` parses this to auto-generate the catalogue:
   ```html
   <!--
     Component: [Descriptive Name]
     Source: [Which design it came from, or "original"]
     Feedback: [User feedback quote if available, or brief description of why it works]
     When to use: [Guidance on when this component is a good fit — what content types,
                    layouts, or contexts it suits best]
   -->
   ```
4. **Make it self-contained** — single HTML file with inline CSS, Google Fonts link, and CSS variables in `:root`. No external dependencies. The file should render standalone in a browser as a demo.
5. **Run `python components/build_catalogue.py`** to regenerate `catalogue.md`

---

## Quality Gates (Playwright)

After creating a one-pager or any HTML-based document, run these checks using Playwright MCP before declaring done:

### Visual Inspection Checklist
Use `browser_navigate` to open the HTML file, then `browser_take_screenshot` to capture it. Inspect for:

1. **No huge empty blocks** — the page should feel purposefully full (~85% content density). Small whitespace for breathing room is good; massive empty zones at the bottom or between sections is a critical failure. If content doesn't fill the page, add more detail or adjust spacing.
2. **No overlapping text** — all text must be readable without any overlap from transforms, absolute positioning, or text inside small shapes. Zoom in on dense areas.
3. **Fits single A4 page** — use `height: 297mm; overflow: hidden` on the page container. Nothing should be cut off at the bottom.
4. **All source content present** — cross-check against the source material. Every key point, stat, and section must be represented. Information loss is a critical failure.
5. **No emojis** — scan the entire document. Zero tolerance.
6. **Logo present** — logo must appear in the top bar. Optionally also in the proof/team section.
7. **Titles read as narrative** — read just the section titles in sequence. Do they tell a coherent story? Would a CEO skimming only titles understand the argument?
8. **Branding correct** — correct font, brand colours, gradient accent line under top bar (check against brand guidelines).
9. **Section splitting clear** — each section should be visually distinct with clear boundaries (colour-coded borders, background tints, divider shapes).
10. **Stat numbers not oversized** — numbers should stand out but not dominate. On one-pagers, 20-28pt is right; avoid going larger.

### PDF Export
Once quality gates pass, export to PDF via Playwright:
```javascript
await page.pdf({
  path: 'output.pdf',
  format: 'A4',
  printBackground: true,
  margin: { top: '0', right: '0', bottom: '0', left: '0' }
});
```
This uses Chromium's built-in print-to-PDF engine (Skia), which renders CSS exactly as designed — clip-paths, gradients, backdrop-filter, SVGs, everything.

Take a screenshot of the PDF too and verify it matches the HTML preview.

---

## Critical Anti-Patterns

These are learned from 30+ design iterations. Never do these:

| Anti-pattern | Why it fails |
|-------------|-------------|
| **Emojis** | Universally hated. Destroys professionalism. Zero tolerance. |
| **Ombre/gradient colour backgrounds** | Look cheap and dated. Subtle gradients on small elements are fine; full-section ombre is not. |
| **Overwhelming dark mode** | Dark backgrounds with neon accents are too aggressive for corporate pitch documents. Dark/light split (like v8_split_contrast) can work when done sparingly. |
| **All rectangles** | Boring. Every design must include non-rectangular elements (circles, chevrons, hexagons, curves). |
| **Giant stat numbers (>32pt on one-pager)** | Numbers already stand out as numericals. Making them enormous wastes space and looks unbalanced. |
| **Topic-label titles** ("The Problem", "Our Solution") | Generic and uninformative. Titles must be complete sentences that tell the story. |
| **Hallucinated content** | Never invent stats, claims, or details not in the source material. |
| **Absolute positioning with fixed px values** | Fragile — breaks when content length changes. Prefer flexbox/grid with fixed page height. |
| **Text inside shapes smaller than 160px** | Text becomes unreadable inside small circles, hexagons, etc. |
| **Font sizes below 7px** | Unreadable in print. Minimum body text: 9px. Minimum labels: 7px. |
| **`min-height` instead of `height` on page** | Allows content to overflow beyond one page. Always use `height: 297mm; overflow: hidden`. |
| **Centre-only alignment** | Full page of centred content feels monotonous. Left-align body text, vary alignment across sections. |
| **Uniform border-radius everywhere** | When every element has the same rounded corners, the page looks auto-generated. Vary radii by element type — or mix rounded with sharp where appropriate. |
| **Equal spacing throughout** | AI tends to space everything identically. Professional design uses tight grouping within related elements and generous gaps between sections — unequal on purpose. |
| **Decorative icons restating their label** | A lightbulb next to "Innovation" or a shield next to "Security" adds nothing. Icons should be specific and informative, or removed. |
| **Identical card structures repeated** | Same icon-title-description pattern for every item looks templated. Vary presentation: some items as stat callouts, some as icon rows, some as inline text with bold leads. |

---

## Creative Variation

Every document should feel like it belongs to the same brand family, but no two should look identical. The brand system is flexible — it's not a template.

### What stays constant (brand anchors)
- Typeface and weight hierarchy (from brand guidelines)
- Colour palette and narrative colour mapping (from brand guidelines)
- Logo placement and treatment (from brand guidelines)
- Narrative structure (Problem → Pain → Solution → Proof → CTA)
- Tone and voice (from brand guidelines)

### What can vary (creative licence)
- **Section layout patterns** — the Pain section doesn't always have to be a 3-column card grid. Try: a single large stat with supporting text, a horizontal bar chart, an icon-row list, a comparison table, or a full-width callout with a background texture.
- **Shape language emphasis** — one document leans on circles and radial layouts; another features chevrons and angular momentum; a third uses flowing curves. All use the brand's shape vocabulary, but the mix changes.
- **Background treatment** — clean white with subtle grain; light tinted sections; dark-background hero with light content below. Vary between documents.
- **Visual density** — information-dense, data-heavy layouts for regulators/analysts; spacious, narrative layouts with fewer elements given more room for executives/partners.
- **Accent colour weighting** — one document features teal prominently (solution-focused pitch) while another leads with coral (problem-awareness piece). The palette is the same; the emphasis shifts.

### How to vary systematically
When told "surprise me" or when making autonomous creative decisions, make three micro-decisions before designing:
1. **Hero treatment** — what makes the top of this document distinctive? (Texture choice, layout split, typographic scale)
2. **Dominant shape** — which shape from the brand vocabulary leads this document? (Circles, chevrons, hexagons, pills, curves)
3. **Density stance** — spacious-and-narrative or dense-and-data-rich?

These three choices cascade through the rest of the layout and prevent two documents from looking like copies of each other.

---

## Format-Specific Notes

This skill defines WHAT to design. The output-format skill defines HOW to build it.

| Output format | Approach | Notes |
|--------------|----------|-------|
| HTML → PDF | **Preferred for one-pagers.** Create as HTML with inline CSS, preview with Playwright, export via `page.pdf()`. Full CSS fidelity. | Use Google Fonts for the brand typeface. `@page { size: A4; margin: 0; }` |
| PPTX | Read the PPTX skill. Use for editable slide decks where recipients need to modify content. | Visual fidelity is lower than HTML — simpler shapes, no clip-paths or backdrop-filter. |
| Gamma | Gamma MCP (`generate` tool). Good for quick drafts. | Pass design direction as theme/style guidance in the prompt. Limited visual control. |

When using Gamma, translate the brand system into Gamma's theme parameters: specify colours, font preferences, and tone in the generation prompt. Gamma won't have pixel-perfect control, so focus on getting the narrative structure, colour palette, and tone right.

---

## Learnings Protocol

After completing a document, offer: *"Would you like me to update my reference docs with anything we learned in this session?"*

If yes, decide where it belongs:
- **One-pager specific** (HTML layout, Playwright quirks, copy patterns) → `references/one-pager.md`
- **Deck specific** (slide structure, PPTX handling) → `references/deck.md`
- **Applies to all formats** (narrative, brand, quality gates) → this file (`SKILL.md`)

Keep entries concise — one line per learning where possible.
