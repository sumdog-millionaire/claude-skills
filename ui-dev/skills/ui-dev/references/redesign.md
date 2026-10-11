# Redesign

Read when the surface already exists and is being changed. Name the kind of change first.

## Which kind of change

- **Preserve**: modernise without breaking the brand. Audit first, extract the brand tokens, evolve gradually.
- **Overhaul**: a new visual language on top of existing content. The old look is evidence and anti-reference, never something to split the difference with; content, function, native affordances and constraints stay.
- **Greenfield**: the brand itself is changing. Nothing is inherited but the facts.

A section, component, feature or state inside an established surface inherits that surface; a local
addition never becomes a new identity exercise. A missing DESIGN.md does not make a project
greenfield: a coherent identity already in the code is documented, then extended.

If ambiguous, put it to the round: "Should this redesign preserve the existing brand, or are we
starting visually from scratch?"

## Audit before touching

Document the current state before proposing anything. When `extract-design-md` is installed, run it
first so the audit is against real tokens rather than a reading of screenshots; when the surface is
running, `extract-static-html` captures it for Stitch.

- **Brand tokens**: primary and accent colours, type stack, logo treatment, radii.
- **Information architecture**: page tree, primary navigation, key conversion paths.
- **Content blocks**: what exists, what is doing work, what is filler.
- **Patterns to preserve**: signature interactions, a recognisable hero, the copy voice.
- **Patterns to retire**: generated-interface tells, broken layouts, dead links, generic stock imagery, performance traps.
- **The dial reading of the existing surface**: its current variance, motion and density are the starting point.
- **SEO baseline**: ranking pages, meta titles, structured data, social cards. SEO migration is a leading redesign risk.

The checklist, by area:

- **Typography**: browser defaults; headlines without presence (size, tighter tracking, lower line height); body wider than the measure; only regular and bold in use (add medium and semibold for hierarchy); proportional numerals in data (tabular figures); missing tracking adjustments (negative for large, positive for small caps); all-caps subheads everywhere; orphaned last words (`text-wrap: balance` or `pretty`).
- **Layout**: everything centred and symmetrical; three equal feature cards; `100vh` sections (use `100dvh`); flex percentage arithmetic (use grid); equal-height cards forced by flex when content varies; a single radius applied without a documented rule; no depth or overlap; identical top and bottom padding where the eye wants slightly more below; a dashboard that always has a left sidebar; buttons not aligned to the bottom of sibling cards; feature lists starting at different heights across pricing columns; misaligned baselines in side-by-side panels; mathematically centred icons that look off by a pixel or two.
- **Interaction and states**: no hover state; no pressed feedback; zero-duration transitions; no visible focus ring; loading, empty, error or success states missing or wrong for their situation (`ux-playbook`); links to `#`; no current-page indication in navigation; instant anchor jumps; animations on `top`, `left`, `width` or `height`.
- **Iconography**: mixed stroke widths; cliché metaphors (a rocket for launch, a shield for security); a missing favicon; stock "diverse team" photography where a real photo or one illustration style belongs.
- **Code**: div soup where semantic elements belong; inline styles beside a styling system; hard-coded pixel widths; missing alt text; arbitrary z-index values; commented-out code; imports that do not exist in the dependencies; missing title, description and social meta tags.
- **What gets forgotten**: legal links in the footer; a way back from every page; a branded 404; client-side validation; a skip-to-content link; cookie consent where the jurisdiction requires it.

## Preservation rules

- Information architecture stays unless asked: slugs, anchor ids and primary navigation labels carry SEO and muscle memory.
- Extract the brand colours before applying any colour directive; a brand that is purple stays purple.
- The copy voice stays unless a rewrite is asked for; visual modernisation is not a content rewrite.
- Existing accessibility wins stay: focus states, alt text, keyboard navigation, contrast.
- Analytics events stay: buttons, form fields and section ids that tracking depends on keep their names.

## Levers, in priority order

Apply in order and stop when the brief is satisfied:

1. Typography refresh: high visual lift for low risk.
2. Spacing and rhythm: section padding, vertical rhythm.
3. Colour recalibration: unify the neutrals, keep the brand accent.
4. Motion, through `animate`, on existing components.
5. Hero and key-section recomposition, using patterns.md.
6. Full block replacement, only when a block is unsalvageable.

Sound architecture, content and SEO call for targeted evolution, levers 1 to 4. Structural visual
debt (broken architecture, no design system, broken mobile) calls for a full redesign with strict
content preservation.

## What never changes silently

Without explicit approval: URL structure and route slugs, primary navigation labels, form field
names or order (analytics and autofill depend on them), the logo or wordmark, existing legal,
consent or cookie copy.
