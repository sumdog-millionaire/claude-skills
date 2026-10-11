# Persuade, and experience

Read when the design read picks persuade (landing pages, marketing, campaigns, pricing) or
experience (portfolios, galleries, showcases). Never cut protected text or remove functionality to
satisfy a cap.

## The first viewport

The first viewport must leave one describable idea, not a mood. Show the subject doing its job, with
demonstration data authored at full fidelity and labelled synthetic. Commercial and factual claims
stay uninventable: prices, customers, benchmarks, capabilities the product does not have.

- The hero carries the purpose and the next action, findable at once. A compact hero often fits the first viewport; an approved scroll narrative may span several.
- Plan font size and image size together. Most heroes sit at `text-4xl md:text-5xl lg:text-6xl`; the largest sizes only when the headline is three to five words. A four-line headline is a font-size error.
- Hero top padding stops at about 6rem at desktop; more, and the content floats halfway down the viewport. Breathing room comes from type scale or asset size.
- At most four text elements in a hero: one small element (the brand's mark or a row of client logos, never a label over the headline, or nothing), the headline (two lines), the subtext (about twenty words), the calls to action (one primary, at most one secondary). Taglines under the buttons, trust strips, pricing teasers, feature bullets and avatar rows move to their own sections below.
- A logo wall sits under the hero as its own section, never inside it.
- A centred hero belongs to editorial, manifesto and launch briefs where the message is the design; above design variance 4, prefer a split, a left-aligned composition with the asset opposite, asymmetric space, or a pinned structure.
- Strong typography can carry a hero without an image; a gradient blob is not a composition.

## Navigation

One line at desktop; if items do not fit at 1024px, condense labels, drop secondary items or move
to a menu. Height at most 80px, usually 64 to 72.

## Composition and rhythm

- Repeat a layout when items need direct comparison or benefit from predictable scanning; vary it on expressive pages. At most two consecutive image-and-text splits; the third breaks the pattern with a full-width section, a vertical stack, a bento grid or a marquee.
- A bento grid has exactly as many cells as there is content for. Its cells vary: at least two or three carry real visual difference, an image, a brand-appropriate tint or gradient, a pattern. It has rhythm: full-width rows, asymmetric tiles, vertical breaks, never six identical left-image right-text rows.
- A section carries one message. A headline with an explainer stacks vertically, the body under the headline within the reading measure; a split header with a small paragraph floating opposite is only for a column that carries a visual or an interaction.
- Declare the mobile collapse of every multi-column section in the same component.
- One marquee per page at most.

## Content density

- Default section shape: a headline of at most eight words, a paragraph of at most twenty-five, and one visual or one call to action. More needs the section's job to justify it.
- A long list gets a different component. Above five items: two grouped columns, a card grid with image and label, tabs or an accordion when items categorise, scroll-snap pills, a carousel for breadth, a marquee for things that need no individual attention. A spec sheet groups its rows into two or three clusters with one soft divider each, or gives each spec a card with its name, its value large, and one line on why it matters.
- A twenty-row table or a full pricing matrix on a marketing page is the wrong layout: the top three to five plus a link to the full list, or a page of its own.

## Calls to action

- Button text fits on one line at desktop: shorten the label (three words at most for a primary) or widen the button.
- One label per intent on a page. "Get in touch", "Contact us" and "Let's talk" are one intent; pick one and use it in the nav, the hero and the footer alike.

## Colour

Persuade and experience may take the bolder colour strategies. For a premium-consumer brief
(cookware, wellness, artisan, luxury, heritage craft, home goods) the generated default is warm
cream, brass or clay or oxblood, and espresso text, a palette common enough that the brand
disappears into it. Base the palette on this brand and brief; it earns that palette only when the
brand names those colours or is genuinely vintage or warm-craft and you can say why. Directions that
are not it: cold luxury (silver, chrome, smoke), forest (deep green, bone, amber), black and tan,
cobalt and cream, terracotta and slate, olive and brick and paper, or monochrome with one saturated
pop.

## Assets

- A "trusted by" wall uses real logos: Simple Icons (`https://cdn.simpleicons.org/{slug}/{hex}`) or devicon for tech marks. An invented brand gets an invented mark, a monogram or a simple glyph as inline SVG in the page's style, never a styled text wordmark. Logos only, no category labels under them; the brand name lives in the alt text.
- A product preview is a real screenshot, a generated image, or a real component rendered in the page. Otherwise editorial photography, or no preview.
- A hand-rolled decorative SVG is for a brief that asks for it, or a single simple geometric mark.

## Quotes and testimonials

Preserve the exact words and the supplied attribution; use an authorised excerpt or an expandable
full quotation rather than cutting the source. Include a role or company only when known. Real
typographic quotation marks, or none.

## The tells of a generated landing page

In addition to the body's list; rewrite the element rather than soften it.

- Version labels in the hero (`BETA`, `v2.0`, `EARLY ACCESS`) unless the brief is a launch; "Brand · No. 01" micro-meta lines.
- Pagination on images or tiles (`01 / 4`); range labels as headings ("Index of Work, 2018 to 2026").
- The middle dot as the default separator.
- Headlines broken with `<br>` and an italic word as a design move; vertical rotated text; hairline crosshair grid lines drawn to feel designed.
- Fake version footers inside a product preview.
- "Quietly in use at" as a social-proof heading (say "Trusted by", "Used at", or let the logos speak); "From the field", "On our desks", "Loose plates" as section labels (say "Testimonials", "Latest writing", or nothing); mock-humble industry asides in body copy; micro-meta sentences under a heading; generic step labels ("Step 1", "Phase 01") where the step's own verb is the label.
- Tags overlaid on images; photo-credit captions under stock images; version strings or build numbers in a marketing footer; live-stock counters ("412 of 800") without real data.
- A mono-caps decoration strip at the hero's foot (`BRAND. MOTION. SPATIAL.`); a small paragraph floating in the top-right corner of a section header.
- Hairlines above and below every row of a long list; comparison bars with a filled background track.
- Locale, city, time or weather strips, unless the studio is genuinely distributed or the brand is a place; scroll cues of any kind.

## Experience

A portfolio, gallery or showcase shares everything above, with these differences:

- The work leads from the first viewport and the interface recedes; navigation, labels and chrome are as quiet as the work allows.
- How the visitor moves through the work, and which interaction or transition matters, are decided in the design read and rendered in Stitch before build.
- The tells that apply hardest: scroll cues, decorative status dots, rotated text, hairline grids, decoration strips.
