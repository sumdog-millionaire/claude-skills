# Sumplexity Brand Guidelines

Sumplexity is an AI-powered compliance inspection platform for UK regulatory bodies. Documents must project confident authority — the credibility of a McKinsey or PwC, combined with sharper value framing and a clear call to action. Think "we've done the analysis, here's why this matters to *you specifically*, and here's what to do next."

---

## Logo

Sumplexity's logo is a sigma (Σ) with data-burst particles — mathematical precision meets digital transformation. Four variants are bundled in `brand/assets/`:

| File | Variant | Use for |
|------|---------|---------|
| `brand/assets/logo_namebelow_taglinebelow_nobackg.png` | Full with tagline, transparent bg | Hero sections, title slides, letterheads |
| `brand/assets/logo_name_tagline_nobackg.png` | Name + tagline inline, transparent bg | Horizontal header bars |
| `brand/assets/logo_namebelow_nobackg.png` | Name below, transparent bg | Navigation bars, medium containers |
| `brand/assets/logo_nobackg.png` | Icon only, transparent bg | Slide corners, badges, small placements |

The logo should always appear in the top-left or top-centre of the first page/slide. On subsequent slides, use the icon-only variant in a corner. On dark backgrounds, apply a white colour filter to the icon-only variant.

Tagline: **"Automating the complex. Amplifying the human."**

---

## Typography

**Public Sans** is the sole typeface across all Sumplexity materials — UI, documents, presentations. This ensures full brand consistency.

| Element | Weight | Size guidance (PPTX) | Notes |
|---------|--------|---------------------|-------|
| Display title | 800 (ExtraBold) | 36-44pt | Tight letter-spacing (-0.02em). Used for hero statements. |
| Section heading | 700 (Bold) | 20-24pt | Used for slide titles, section headers on one-pagers. |
| Stat numbers | 800 (ExtraBold) | 20-28pt (one-pager) / 48-72pt (slides) | Colour-coded to section. Numbers already stand out as numericals — don't make them enormous on one-pagers. |
| Body text | 400 (Regular) | 14-16pt | Line-height 1.5-1.6. Left-aligned, never centred. |
| Callout text | 700 (Bold) | 16-18pt | Used for insight boxes, pull quotes. |
| Caption / label | 600 (SemiBold) | 10-12pt | Uppercase, wide letter-spacing (0.06-0.1em). |
| Footer | 400 (Regular) | 8-10pt | Muted colour. |

If Public Sans is unavailable in the output format, fall back to **Calibri** (closest system font in weight/proportion).

---

## Colour System

### Brand Core
| Name | Hex | Usage |
|------|-----|-------|
| Brand Green | `#0A4D1C` | Logo, headers, primary CTAs, top bars, brand anchors |
| Brand Dark | `#073914` | Dark slide backgrounds, deep headers |
| Brand Hover | `#0C5E22` | Interactive states, secondary green |
| Brand Subtle | `#E9F2EB` | Hero section tints, highlight backgrounds |

### Narrative Accents
These map to the narrative arc. Use them for section markers, stat numbers, icons, and tinted backgrounds — never for large background fills (keep backgrounds white or Brand Dark).

| Name | Hex | Narrative role | Light tint |
|------|-----|---------------|------------|
| Warm Coral | `#BF5A3A` | Pain / problem | `#FAEAE6` |
| Teal | `#0C7C6B` | Solution / technology | `#E6F3F1` |
| Amber Gold | `#C8952E` | Value / proof | `#FAF3E6` |
| Deep Navy | `#1A2B4D` | Context / situation | `#E8EBF0` |

### Neutrals
| Name | Hex | Usage |
|------|-----|-------|
| Text Primary | `#111111` | Headings, body text |
| Text Secondary | `#444444` | Supporting text |
| Text Muted | `#71717A` | Captions, labels, footers |
| Background | `#F5F5F3` | Page backgrounds (if not white) |
| Border Light | `#E5E4E1` | Dividers, card borders |

### Colour Rules
- Brand Green is the dominant colour (60%+ visual weight). Accents are subordinate.
- Every section has a 4px left-edge bar in its narrative colour (coral, teal, amber).
- Stat numbers take the colour of their section (e.g. pain stats are coral).
- Icons sit inside coloured circles (28-36px diameter) using the section's accent colour with white icon strokes.
- Light tints are used for card/section backgrounds — never use full-saturation accents as large fills.
- On dark backgrounds (Brand Dark), use white text and amber gold for emphasis.

### CSS Variables (include in every HTML document)
```css
:root {
    --brand-green: #0A4D1C;
    --brand-dark: #073914;
    --coral: #BF5A3A;
    --teal: #0C7C6B;
    --amber: #C8952E;
    --navy: #1A2B4D;
    --coral-light: #FAEAE6;
    --teal-light: #E6F3F1;
    --amber-light: #FAF3E6;
    --navy-light: #E8EBF0;
    --text-primary: #111111;
    --text-secondary: #444444;
    --text-muted: #71717A;
    --bg: #F5F5F3;
    --border-light: #E5E4E1;
}
```

---

## Tone

- **Confident authority** — not aggressive sales. Assertive but earned.
- **Value-from-the-recipient's-perspective** — always frame in terms of what they gain, not what Sumplexity does.
- **Technical depth: hint only** — "powered by AI" or "AI-powered document analysis." Never mention LLMs, Gemini, specific architectures, or implementation details in external documents.
- **UK English** throughout (analyse, colour, organisation, programme).
- Short paragraphs. No fluff. Every sentence earns its place.

---

## Audience Adaptation

Before creating any document, determine the audience. If not explicitly stated, infer from context or ask. The narrative structure stays the same; the emphasis and depth shift.

### Regulatory Body (e.g. CLC, SRA)
- **Emphasis**: Compliance rigour, audit trail, consistency, accountability to oversight bodies (e.g. LSB)
- **Pain framing**: Inspector capacity constraints, coverage gaps, quality variability
- **Proof framing**: Evidence traceability, standardised process, regulatory alignment
- **Tone adjustment**: Slightly more formal. Reference specific code areas and regulatory frameworks.
- **Technical depth**: Can mention "document analysis" and "automated classification" — these are operational concepts regulators understand.

### Law Firm / Conveyancing Practice
- **Emphasis**: Speed, client service, competitive advantage, cost reduction
- **Pain framing**: Manual bottlenecks, transaction delays, compliance burden
- **Proof framing**: Time savings, error reduction, client satisfaction
- **Tone adjustment**: More commercial. Focus on business outcomes.
- **Technical depth**: Minimal. "AI-powered" is sufficient.

### Investor / VC
- **Emphasis**: Market size, traction, defensibility, team
- **Pain framing**: Market-wide inefficiency, TAM/SAM sizing
- **Proof framing**: Growth metrics, pipeline, competitive moat
- **Tone adjustment**: Sharper, more metrics-driven. Include forward-looking statements.
- **Technical depth**: Can reference AI capabilities at a high level as part of the moat narrative.

### Internal / Strategic Partner
- **Emphasis**: Integration opportunity, mutual value, technical compatibility
- **Pain framing**: Shared customer problems, ecosystem gaps
- **Proof framing**: Technical capabilities, API readiness, case studies
- **Tone adjustment**: Collaborative rather than persuasive.
- **Technical depth**: Can go deeper — mention document analysis pipelines, API integration, data flows.

---

## Common Content Elements

These are reusable content patterns that appear across Sumplexity documents. Adapt the specifics to the audience and context.

### Boilerplate (adapt, don't copy verbatim)
- **What Sumplexity is**: "An AI-powered compliance inspection platform that turns document-heavy regulatory reviews into structured, auditable findings."
- **How it works (simple)**: "Upload documents → AI classifies and analyses → Review findings with evidence → Generate inspection report"
- **Key value props**: 10× faster document review · Full evidence traceability · Consistent quality standard · Built for existing regulatory workflows
- **Tagline**: "Automating the complex. Amplifying the human."

### Contact / CTA
- Website: sumplexity.com
- Email: hello@sumplexity.com
- CTA text options: "Book a Demo" / "Let's talk" / "See it in action" / "Run a pilot inspection together"
- Always end with a clear, specific next step — never a vague "learn more."
