---
name: ui-dev
description: Design and build any interface from brief to verified build, a marketing page, a web app, a docs site, a portfolio, and the phone surface beside them. Reads the brief, picks the mode the visitor is in, works from the brand folder, renders the direction in Google Stitch through its MCP server for the user to iterate, then implements the approved screens, inspecting designs through Stitch's individual-screen screenshots and exported HTML. Use this skill for ANY change to what a person sees on screen, however small, a page, screen, component, layout, list row, tooltip, dropdown, dashboard, settings page, landing page, docs page; anything called dated, cluttered, generic, cleaner, more modern, more polished, better looking or better animated; any brand or brand-folder work; and any mention of Stitch, including how to get a screen into it or use it. Load it before reading the code, even when the user never says the word design. Hands interface motion to animate on the web and animate-expo on React Native.
---

# ui-dev

Brand rules and approved project choices beat every aesthetic rule here, and the absence of a rule
is creative freedom. Accessibility, security and factual accuracy are requirements throughout.

## Inspection method — Benedict's standing instruction

Use Stitch MCP to retrieve each individual screen's screenshot and HTML. Download those exports,
view the screen-only image, and inspect the HTML/CSS for fonts, sizes, spacing, colours, assets and
component fidelity. Whole-project canvas screenshots are not useful evidence. Local reading,
parsing and cropping of the exported files are allowed; no browser is needed.

Do not use Playwright, browser automation, browser-rendered local exports, desktop automation or
whole-window screenshots. This instruction overrides browser-inspection steps in this skill's
references and companions. If a check requires a running browser, report it as not checked rather
than substituting automation or claiming that static HTML proves runtime behaviour.

When matching an existing screen, fetch its latest exports first and treat the user-designated
reference as the visual source of truth. Compare equivalent component roles in HTML; differently
sized screenshots do not establish equal font or margin values. Edit only the target screen,
then fetch it again to verify persistence, preserved content and visual fidelity. If the tool
creates a revision instead of saving in place, report the returned ID; never claim an overwrite.

## Start here

Read [workflow.md](references/workflow.md) first: the stages, the two approval gates, and the routes
through Stitch. A targeted change inside an approved direction skips the gates and Stitch and loads
only the mode file and redesign.md. Otherwise load what the task needs:

| When | Read |
|---|---|
| a brand is named, none exists yet, or the task is onboarding one (no design read) | [brands.md](references/brands.md) |
| the design read picks a mode | [persuade.md](references/persuade.md) (also experience), [operate.md](references/operate.md), or [read.md](references/read.md) |
| a new or materially revised direction | [stitch.md](references/stitch.md) |
| DESIGN.md or PRODUCT.md is read or written | [design-file.md](references/design-file.md) |
| before production edits, and at delivery | [verification.md](references/verification.md) |
| the surface already exists and is being changed | [redesign.md](references/redesign.md) |
| composing a persuade or experience direction | [patterns.md](references/patterns.md) |
| the brief names a visual language (soft, minimalist, brutalist, or a Stitch style word) | [styles.md](references/styles.md) |
| a named design system or aesthetic family is in play, or a new project needs a foundation | [design-systems.md](references/design-systems.md) |
| scroll storytelling: sticky stacks, horizontal pans | [motion.md](references/motion.md) |
| generated images or video, hero backgrounds, sequence scroll | [generated-media.md](references/generated-media.md) |

**Motion is written by `animate`** on the web and `animate-expo` on React Native, which own every
constant, curve and duration and the decision whether a thing animates at all; `apple-design`
supplies the reasoning and physics when the brief asks for that feel; `pick-ui-library` chooses a
component when a task needs one rather than an animation. A surface gets one authored moment of
motion.

**How components and screens behave is `ux-playbook`'s**: loading, errors, forms, empty states,
success feedback, sections that fail on their own, button states, control placement, choices,
progressive disclosure and hard steps. Every operate screen takes it; a screen in any other mode
takes it when it fetches data, submits something or asks the person to choose. workflow.md says
where it enters the route.

**Prose is written or revised with `anti-ai-slop-writing`**, with the brand's voice and market
conventions taking precedence over its default tone. Supplied facts, quotations and protected
text are preserved.

**Companions** in this plugin: `extract-static-html` captures a running screen as one HTML file,
`upload-to-stitch` posts images and HTML to Stitch, `extract-design-md` reads a DESIGN.md out of
existing source, `react-components` turns a Stitch screen into React. When calling them, this
workflow's two gates are the only approval points, and the project's DESIGN.md is `docs/DESIGN.md`
wherever a companion names `.stitch/DESIGN.md`.

**Words for the person.** This skill has working words of its own, and they stay in these files. To the
person, say the thing in plain words, the way someone with no design training would say it:

| The skill's word | Say to the person |
|---|---|
| the design read | what I am taking this to be |
| mode (persuade, operate, read, experience) | what the visitor came to do: to decide, to get a job done, to understand, or to look at the work |
| dials, and a number for each | how symmetrical the layout is, how much movement, how tightly packed, each in words |
| surface | the page, or the screen |
| direction | the proposed look |
| subscreen | one part of the screen |
| state inventory | what each screen shows while loading, when empty, and when it fails |
| gate | an approval point |
| the approved package | the approved screens |
| the frontier | the open questions |
| the brand pack | the brand folder |
| tokens, front matter | the exact values at the top of the file |
| lint | check the file for mistakes |
| the detector | the style checker |

The same holds for any heading written into a file a person opens: brands.md and design-file.md give
the plain headings, and the ones Google's format fixes keep their names with a plain line under them.

## 1. The design read

Read the brief before setting dials. Signals, in order:

1. **Mode**: what is the visitor there to do? (below)
2. **Page kind**: landing, pricing, portfolio, editorial, ecommerce, dashboard, editor, settings, docs.
3. **Vibe words** the user used: "calm", "Linear-style", "Awwwards", "brutalist", "premium", "playful", "serious B2B", "editorial", "dark tech".
4. **References**: URLs, screenshots, products named, brands competed with.
5. **Audience**: a procurement panel, a design-conscious consumer, a recruiter scanning. The audience picks the aesthetic.
6. **Brand assets that exist**: logo, colour, type, photography. For an existing surface these are starting material.
7. **Quiet constraints**: accessibility-first audiences, public sector, regulated industries, trust-first commerce, children. These override aesthetic preference.

**The four modes.** Choose from the requested surface, not the product: a tool's landing page is
persuade; a fashion house's documentation is read.

- **Persuade**: the visitor decides and acts; design is the product. Landing pages, marketing, campaigns, pricing. Earn attention and action.
- **Operate**: the visitor completes a task. App UI, dashboards, editors, admin, settings, tools. Scanability, consistency, native expectations and the real usage scene outrank expression; brand lives in precise details.
- **Read**: the visitor understands something. Docs, articles, guides, help, changelogs. Structure for comprehension, then make the reading worth staying in.
- **Experience**: the visitor is inside the work itself. Portfolios, galleries, showcases. The artefact leads from the first viewport; the interface recedes.

**Five lenses, posed on every surface in this order:**

1. **Time to dopamine.** How fast does the person get something that rewards them? Front-load the value; the first minute matters most.
2. **Emulate the best.** The top products borrow each other's proven anatomy: modern but predictable, the way the best phone apps are, never a page shape reinvented for flavour.
3. **Build a world.** One palette, one plain voice, the same names carried through every screen.
4. **Cut the fluff.** Anything that is not the core value is a distraction: fewer sections, one action.
5. **Be opinionated.** Lead with the claims only this product can make.

**State the read in one line before anything else, in plain words:** "I am taking this to be a <page
kind> for <audience>, who come to <what the visitor came to do>. It should feel <vibe>, built on <design
system, aesthetic family, or native CSS>, with a <how symmetrical> layout, <how much> movement and <how
tightly packed> screens." Never the mode's label and never a dial's number. Then load the mode's
reference.

**The user leads the decisions, so every question goes through `grilling`, always, with
`domain-modeling` loaded beside it so each settled decision is written as a record and a glossary
entry as it lands** (what `/grill-with-docs` does; the agent cannot invoke that command itself).
Once the read is stated, make **two `Skill` calls in the same message**, `grilling` and
`domain-modeling`; one without the other is a defect, not a shortcut. Then hand grilling the open
decisions; every question this skill raises (which width
case, which font, whether to infer a dark mode, which brand folder, which kind of redesign, which
device types) joins its frontier, which to the person is "the open questions". Never ask for a fact available in the project.

**Anti-default discipline.** The generated-interface defaults are purple gradients, a centred hero
over a dark mesh, three equal feature cards, glass on everything, infinite micro-animations, Inter
plus slate-900. If someone could guess the aesthetic from the category alone, rework until they
could not.

## 2. The three dials

Stated with the read. Mode first; density usually follows it.

- **`DESIGN_VARIANCE`** 1 to 10: perfect symmetry to artsy chaos. 1 to 3: symmetrical grid, equal paddings, centred. 4 to 7: offsets, mixed aspect ratios, left-aligned headers over centred data. 8 to 10: masonry, fractional grids, large empty zones.
- **`MOTION_INTENSITY`** 1 to 10: the brief's appetite for motion; `animate` decides what moves. Low: motion only where it carries feedback. High: a scroll narrative is in scope, in motion.md's shape.
- **`VISUAL_DENSITY`** 1 to 10: airy to cockpit. Low: huge section gaps. High: tight, clearly grouped, tabular numerals where they aid scanning.

| Use case | Variance | Motion | Density |
|---|---|---|---|
| Landing (SaaS, mainstream) | 7 | 6 | 4 |
| Landing (agency, creative) | 9 | 8 | 3 |
| Landing (premium consumer) | 7 | 6 | 3 |
| Portfolio (designer) | 8 | 7 | 3 |
| Portfolio (developer) | 6 | 5 | 4 |
| Editorial, docs, blog | 6 | 4 | 3 |
| Public sector, trust-first, accessibility-critical | 3 | 2 | 5 |
| Dashboard, app, tool | 3 | 2 | 7 |
| Redesign, preserve | match | match | match |
| Redesign, overhaul | +2 | +2 | match |

Infer all three from the read and show them; the user changes them in conversation.

## 3. Conventions

- **Framework**: preserve the project's. React or Next.js are options for a new project. In Next.js, global state and anything with motion, scroll listeners or pointer physics lives in a client component leaf; server components render static layout only.
- **Styling**: the project's own system. For a new project, design-systems.md picks the foundation first; where nothing else applies, Tailwind v4 with `@tailwindcss/postcss` or the Vite plugin.
- **State**: local state for isolated UI; global state only to avoid deep prop drilling.
- **Icons**: approved brand icons, then the project's existing family; Phosphor, HugeIcons, Radix, Tabler and Lucide are options when none exists. One family, one stroke width, drawn icons.
- **Emoji**: only when the brief asks for a chat-style or playful voice, and then sparingly.
- **Layout mechanics**: standard breakpoints (640, 768, 1024, 1280, 1536). `min-h-[100dvh]` for full-height sections, since `h-screen` jumps when a phone's address bar moves. CSS Grid over flex percentage arithmetic. `min-width: 0` on flex and grid children that must shrink below their content.
- **Dependencies**: check `package.json` before importing anything. If the package is missing, give the install command first.

## 4. Directives for every surface

### Width

Any pane a person can resize fills its space and follows the divider when it moves. A reading
column, which is any read surface and any document opened to be read inside an app, is capped with
its holder at 65 to 75 characters, never the column alone inside a holder that fills. A marketing
page may use a page container. When it is unclear which case applies, ask. `overflow-wrap` is
`break-word`, never `anywhere`.

### Typography

- **Brand fonts always win**, and a project with a design file has already chosen. With neither, suggest a face with a reason and ask.
- **Guidance on what to reach for**: Cabinet Grotesk, Satoshi, Söhne or Schibsted Grotesk for a modern sans; for a serif that fits an editorial or heritage brief, Tiempos, GT Sectra, Canela, Domaine or EB Garamond, named for this brand. Operate and read surfaces may use a familiar sans, including the system stack. The detector reports Inter and Geist as overused; when a brand names one, or an operate or read surface chose one on purpose, record the exception with that reason.
- **Rules on what not to default to**: Fraunces, Playfair Display, Cormorant, Lora, Crimson, Newsreader, Syne, Space Grotesk, Space Mono, IBM Plex, Inter as display type, DM Sans, DM Serif, Outfit, Plus Jakarta Sans, Instrument Sans and Instrument Serif. Choose a serif only when the brand names one, or the brief is editorial, luxury or heritage and you can say why this serif fits this brand.
- **Emphasis inside a headline** is italic or bold of the same family.
- **Display type**: tracking floor -0.04em, balanced headings, obvious steps of scale and weight. Italic display type with descenders needs line height of at least 1.1 and a little reserve below, or the descender clips.
- **Body**: 16px is the ordinary floor; line height tuned to measure; prose stays readable and zoomable; numerals tabular where they align data.

### Colour

- **Pick a colour strategy before picking colours**: restrained (neutrals plus one accent; the default when the visitor came to operate or read), committed (one saturated colour carries a third to a half of the surface), full palette (three or four named roles), or drenched (the surface is the colour). Persuade and experience have permission for the bolder strategies.
- **Brand colours are the palette.** Multiple brand colours and distinct semantic success, warning and error colours are valid. Pure black and pure white are valid brand colours.
- **Roles, not swatches**: accent for primary action, selection and state; a second neutral layer for sidebars and panels; consistent semantic colours for hover, focus, active, disabled, selected, loading, error, warning, success and info.
- **One palette per project**; warm and cool greys never mix.
- **Contrast**: body and placeholder text 4.5:1, large text (24px regular or about 18.7px bold) 3:1, controls, icons and focus rings 3:1. Secondary text on a coloured surface is tinted from that hue or the foreground, never grey.

### Light and dark

Light by default. A project whose design file has settled the theme is not asked. When the brand
guidelines carry a dark mode, build it to them. When they carry none, offer to infer a dark theme
as a switcher and ask; when the brand is dark, offer light and ask. Theme through the project's
mechanism: the `dark:` variant in utility projects, semantic CSS
variables swapped under a theme attribute otherwise. Hierarchy that works in one mode works in the
other, and the brand colour stays recognisable in both.

### Materiality and shape

- Cards only when elevation communicates real hierarchy; otherwise group with a top border, dividers or space. Never nest cards outside a named visual language (styles.md).
- Declare elevation once, border or shadow, never a 1px border under a wide soft shadow. A shadow carries an offset and a soft blur, tinted to the background hue.
- One corner-radius system per page: all sharp, all soft, or all pill, or a documented rule ("buttons pill, cards 16px, inputs 8px") applied everywhere.
- Glass and blur are a specific effect with a solid fallback under `prefers-reduced-transparency`.

### States, forms, copy

- States, forms and error wording follow `ux-playbook`. Beside it: a label sits above its input, and a placeholder is an example, never the label.
- Button text readable against its background.
- Copy: controls name their action; helper text answers an implicit question rather than restating the control. Re-read every visible string before delivery. Numbers are real, or labelled synthetic.
- One tone of writing per page unless the brand voice calls for more.

### Assets

Approved assets first: supplied brand artwork, real product imagery, source-system assets. Licensed
or generated assets second, with subject, rights and provenance checked. Otherwise leave a clearly
labelled placeholder slot and say at the end which placements need real images. A text-led design
or a tool may need no images at all. Images reserve their layout space; off-screen ones load lazily.

## 5. The quality floor

Verified before anything ships, with the real copy at every breakpoint:

- **Depth** declared once. **Spacing**: tight groups, generous separation, more space above a heading than below it, on a documented scale with a 4-unit base; read the computed values.
- **Type**: run the real copy and fix what overflows.
- **States**: every state the state pass named, with real content and working controls.
- **Browser surfaces**: text selection, the caret, scrollbars, focus rings, underline offset and tabular numerals all ship with browser defaults; theme them from the palette.
- **Copy**: the product's own language, in the reader's words.
- **Coverage**: every brief requirement present and findable within seconds.
- **Performance**: LCP under 2.5s, INP under 200ms, CLS under 0.1; grain and noise filters only on fixed, pointer-transparent pseudo-elements; lazy-load below the fold; z-index from the project's scale.
- **Keyboard**: visible focus, logical order, accessible names, dialogs that trap and return focus.

## 6. Tells

Rewrite any element that uses one of these; only a brief's own words earn one back, and the one
item no brief earns back is a kicker or eyebrow above a heading.

- Neon or outer glows; oversaturated accents; gradient text on large headings; custom cursors.
- Oversized headlines that shout instead of controlling hierarchy with weight and colour.
- Three equal feature cards; the hero-metric template (big number, small label, supporting stats, accent) as a page's story, where an operate surface's row of real figures is data and fine.
- Section numbers (01 / 02 / 03) unless the sequence carries information; "LABEL // YEAR" formatting; a coloured left or right border above 1px on cards, list items or callouts, unless the colour carries state such as an alert's severity; hard offset shadows outside a genuinely neobrutalist world.
- Micro-UI clutter: dots, pills, tags and badges scattered to look busy; a coloured status dot that carries no state.
- Sparklines, progress rings and soft-shadowed rectangles standing in for content; monospace as a costume for "technical" rather than for code, data or measurement.
- Generic names ("John Doe"), egg avatars, startup-slop brand names ("Acme", "Nexus"), filler verbs ("Elevate", "Seamless", "Unleash"), and a placeholder image service in a deliverable.
- Div-built fake screenshots of a product; hand-rolled decorative SVG illustrations; a component library shipped in its default state.
- A modal for a task that needs neither interruption nor protected focus.
