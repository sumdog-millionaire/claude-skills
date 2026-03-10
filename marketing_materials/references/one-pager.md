# One-Pager Layout Reference

Detailed layout patterns for one-pagers. Read the main SKILL.md first for narrative structure and quality gates, and `brand/brand_guidelines.md` for colours, typography, and tone.

## Output Format: HTML → PDF

One-pagers are created as **HTML with inline CSS**, previewed via Playwright MCP, then exported to PDF. This is the only workflow — it gives pixel-perfect control over clip-paths, gradients, SVG backgrounds, and every CSS feature.

### Page Setup (required in every one-pager)
```css
@page { size: A4 portrait; margin: 0; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.page {
    width: 210mm;
    height: 297mm;        /* MUST be height, not min-height */
    overflow: hidden;      /* MUST be hidden to enforce single page */
    position: relative;
    font-family: 'Public Sans', Calibri, sans-serif;
}
```

Include Google Fonts in the head:
```html
<link href="https://fonts.googleapis.com/css2?family=Public+Sans:ital,wght@0,400;0,600;0,700;0,800;1,400;1,700&display=swap" rel="stylesheet">
```

### CSS Variables (include in every one-pager)
Copy the CSS variables block from `brand/brand_guidelines.md` into every one-pager's `:root`.

---

## Execution Workflow

1. **Draft titles first** — write all section titles and read them in sequence. Do they tell a coherent story? Fix them before touching any layout.
2. **Choose a layout approach** — browse `components/catalogue.md` (auto-generated — run `python components/build_catalogue.py` first), pick 2-3 components, decide how to combine them.
3. **Build the HTML** — write the full page as a single HTML file with inline CSS. Embed the logo as a base64 data URI or file path.
4. **Preview with Playwright** — `browser_navigate` to the file, `browser_take_screenshot` to inspect.
5. **Run quality gates** — check all items in the Quality Gates section of SKILL.md.
6. **Iterate** — fix issues, re-preview, repeat until all gates pass.
7. **Export to PDF** via Playwright's `page.pdf()`.

---

## Layout Architecture

### What Works (learned from 30+ iterations)

These patterns consistently scored well in user reviews:

| Pattern | Why it works | Component reference |
|---------|-------------|-------------------|
| **Chevron section dividers** | Create flow between sections — "goes from one place into the next" | `section_dividers/chevron_divider.html` |
| **Hexagonal stat cards** | Strong visual identity, memorable, distinctive | `stat_displays/hex_stats.html` |
| **Subtle background textures** | Add richness without distraction (hex tiles at 2-3% opacity, dot grids, radial washes) | `backgrounds/` |
| **Colour-coded sections** | Each narrative beat has its own background tint and accent colour | All section layouts |
| **Bridge/connector text** | Italic transition text between sections maintains narrative flow | `callouts/connector_pills.html` |
| **Multiple shape types** | Mixing circles, hexagons, chevrons, and cards prevents "all rectangles" monotony | Combine from multiple categories |
| **Dark/light split** | Dramatic contrast creates hierarchy — dark for stats/hero, light for detail | `section_layouts/split_contrast.html` |
| **Progress/loading bars** | Inventive data visualisation for comparative stats | `stat_displays/progress_bars.html` |
| **Flowing ribbon** | Creates a journey metaphor — distinctive and memorable | `section_layouts/flowing_ribbon.html` |
| **Full-height accent bar** | Continuous branding strip, subtle but effective | `decorative/accent_bar.html` |

### What Fails (never do these)

| Anti-pattern | Consequence |
|-------------|------------|
| `min-height: 297mm` on page | Content overflows to a second page |
| Absolute positioning with fixed `top` values | Text overlaps when content length changes |
| `margin-top: auto` to push CTA down | Creates huge empty gap when content is short |
| Text inside circles < 160px | Unreadable |
| Font sizes < 7px | Unreadable in print |
| Stat numbers > 32pt on one-pager | Wastes space, looks unbalanced |
| Single shape type throughout | Boring — "all rectangles", "very boring" |
| Emojis | "I hate the emojis. Never use emojis." |
| Ombre gradient backgrounds | "Dreadful" |
| Neon colours on dark backgrounds | "Very ugly and overwhelming" |

---

## Section Anatomy

The page contains all five narrative beats. The visual treatment of each section should vary — this is where the component library comes in. Below is the structural skeleton; the visual execution should differ every time.

### 1. Top Bar
- Full-width Brand Green background, ~40-48px height
- Left: Logo (embed as base64 or file path from `brand/assets/`) + brand name uppercase, 700 weight, white
- Right: Contextual label (e.g. "Prepared for the CLC") in small white text at 55% opacity
- Below: 3px gradient line (Brand Dark → Brand Green → Teal)

### 2. Hero Section
- Background: Brand Subtle (`#E9F2EB`) or a creative alternative
- Contains the opening title — the first sentence of the narrative arc
- Optional: a subtitle with the core proposition in 1-2 sentences
- This is the hook — it must be compelling and immediately legible

### 3. Problem / Pain Section
- Narrative colour: Deep Navy (context) → Warm Coral (pain)
- Must contain the key stats/data points that establish urgency
- Visual treatment options: stat cards, hex badges, progress bars, circular badges, chevron stat row
- Every stat must come from the source material — never hallucinate numbers

### 4. Transition / Bridge
- Use a connector element between problem and solution
- Options: bridge text with gradient lines, connector pills, chevron divider, wave divider
- Contains the pivot statement — the sentence that turns from problem to solution

### 5. Solution Section
- Narrative colour: Teal
- Must show the process/approach — how Sumplexity solves this
- Visual treatment options: chevron flow, hub-spoke, pipeline, numbered steps
- Include: what it does, how it works (simply), key differentiators

### 6. Proof / Value Section
- Narrative colour: Amber Gold
- Evidence, team credentials, capabilities, differentiators
- Visual treatment options: 2×2 grid, checkmark items, capability cards, timeline
- Must include team background and why Sumplexity is credible

### 7. CTA Block
- Brand Green background, prominent position
- Specific next step (never vague "learn more")
- Contact details (email, website)
- Should feel like a destination, not a footer

### 8. Footer (optional)
- Thin, minimal — website, email, copyright
- Text Muted colour, smallest font (8pt)

---

## Spacing and Page Fill

### The 85% Rule
The page should feel purposefully full. Content density target: ~85%. This means:
- No massive empty blocks at the bottom (the single most common failure)
- No huge dead zones between sections
- But deliberate whitespace for breathing room is good

### How to Achieve Good Page Fill
- Use `display: flex; flex-direction: column` on `.page`
- Give each section `flex-shrink: 0` to prevent compression
- Use a spacer (`flex: 1`) between the last content section and CTA to distribute any remaining space evenly — but if the gap is > 30px, add more content instead
- Test with `border: 1px solid red` on each section during development to see spacing

### Spacing Between Elements
| Between | Gap |
|---------|-----|
| Top bar → gradient line | 0 (flush) |
| Gradient line → hero | 0 (flush) |
| Between sections | 12-18px padding or a divider component |
| Section label → content | 8-10px |
| Within stat card grids | 7-8px gap |
| CTA → footer | 8-10px |

---

## Using the Component Library

### Creative Remix, Not Templates
The component library (`components/`) contains proven design patterns extracted from reviewed designs. The goal is **remixing, not copying**.

When creating a new one-pager:
1. Run `python components/build_catalogue.py` to generate the catalogue
2. Read `catalogue.md` to see all available components with rationale
3. Pick 2-3 components from different categories that suit the content
4. Combine them in a new way — change proportions, swap colours, adjust layouts
5. Add at least one element that isn't from the library — invent something fresh
6. The library should inspire, not constrain

### Expanding the Library
After creating a new one-pager that the user likes, extract any novel patterns and add them to the library:
1. Create a new `.html` file in the appropriate category subdirectory
2. Add a comment block at the top with: Component name, Source, Feedback, When to use
3. Run `build_catalogue.py` to update the catalogue

---

## Adapting Content by Audience

The layout structure stays constant. What changes:

| Section | Regulator | Law firm | Investor |
|---------|-----------|----------|----------|
| Hero title | Frame around regulatory capacity and evolving compliance landscape | Frame around speed, efficiency, competitive advantage | Frame around market size and automation opportunity |
| Pain stats | Inspector capacity, document volume, turnaround time, non-compliance rates | Transaction delays, compliance costs, manual hours | Market inefficiency metrics, TAM/SAM |
| Solution flow | Upload → Classify → Review → Report (regulatory workflow) | Integrate → Automate → Monitor → Report | Land → Expand → Platform → Ecosystem |
| Proof items | Evidence traceability, consistency, regulatory alignment, coverage | Time savings, error reduction, client satisfaction | Traction metrics, pipeline, team, moat |
| CTA | "Run a pilot inspection together" / "30 minutes with your team" | "See it in your workflow" | "Let's talk" / "Request pitch deck" |

---

## Common Mistakes to Avoid

- **Generic section labels** ("Our Solution") — titles must be complete narrative sentences
- **Information loss** — every key point from the source material must appear. If space is tight, compress the wording, don't drop content.
- **Too much text** — if any paragraph exceeds 3 lines, cut it
- **Missing CTA** — every one-pager must end with a specific next step
- **Missing logo** — must appear in the top bar at minimum
- **Colour overload** — accent colours for section markers, stats, icons only. Body text stays neutral.
- **Centred body text** — left-align. Only centre titles in the hero and CTA.
- **All-rectangular layout** — every section must include at least one non-rectangular element
- **Weak stat presentation** — stats should be visually distinct (coloured numbers in shaped containers), not buried in text
- **Not testing with Playwright** — always preview visually before declaring done

---

## Learnings from Production Sessions

**Layout pitfalls:**
- Never give `.content-area` `flex: 1` — it expands and pushes the timeline/footer to the bottom with a huge gap. Use `flex-shrink: 0` on content; use `margin-top: auto` on the element that should be pushed down.
- Keep the section divider line, section label, and timeline as **separate sibling elements** — if bundled in one div, they always move together.
- `overflow: hidden` clips silently in PDF export — always check total height visually.

**Hidden bugs:**
- Reduced opacity on text or logos (`opacity: 0.5`, `0.6`) causes off-colour artefacts. Set to `1` on all text/logos; reserve opacity reduction for decorative SVG only.
- Logo on dark background: `filter: brightness(0) invert(1)` — not `brightness(10)`.

**Playwright workflow:**
- Can't open `file://` paths with spaces on Windows — copy the HTML to `/tmp/` and serve with `python -m http.server 8766 -d /tmp`.
- PDF export requires `printBackground: true` and `margin: 0` on all sides.

**Copy patterns:**
- Bold the lead-in only: `<strong>Key claim.</strong> Elaboration unbolded.`
- Most important stat (especially client-specific) goes first in the list.
- Connector pills: one sentence — if it wraps, cut it.
- Footer URL: not bold, website only.

**What users ask for iteratively — anticipate these:**
- Text slightly too small → start font sizes at upper end of range
- Opacity making logos/labels look off → check and set to 1
- Spacing off after content changes → adjust `margin-bottom` on `.section` (working value: `22px`)
- Section label overlapping timeline → check structural separation
- Footer URL is bold → set `font-weight: 400` on CTA contact links
- Soft CTA → use a presumptive close from the start for sales/regulator audiences: "Next Step: [specific action]" bold + underlined, not "We'd welcome 30 minutes..."
- CTA strip div order matters → flex `justify-content: space-between` positions by DOM order; never reorder divs without checking visually
- Soft CTA styling undercuts bold text → remove italic, use 11px+ and full white; `<strong>` then reads correctly
- AI-sounding copy → em-dash pivot + abstract verb ("cannot be replaced — but it can be amplified") is a giveaway. Anchor brand words to something concrete: "AI amplifies the speed", not vague amplification. Two short sentences beat one long dash-joined sentence.
