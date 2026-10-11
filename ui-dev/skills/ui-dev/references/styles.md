# Visual languages

Read when the brief names a language. Name a chosen
language in the Stitch brief using the words below.

## Stitch's style vocabulary

The terms Stitch's engines act on. Combine one from each group that applies.

- **Layout and structure**: bento grid (modular, boxy, card compartments), editorial (magazine feel, large serif headings, generous space, asymmetric images), Swiss (grid systems, sans-serif, flush-left), split-screen (a solid colour block paired with full-bleed imagery).
- **Texture and depth**: glassmorphism (translucency, backdrop blur, subtle white borders), claymorphism (soft inflated shapes with inner shadows), skeuomorphic (realistic textures and physical controls), grainy (film grain over gradients to reduce digital shine).
- **Atmosphere and era**: brutalist (raw, default system fonts, high contrast, hard edges), cyberpunk (dark, neon cyan and magenta, glitch), Y2K (chrome, bubble letters, bright blues and pinks, pill buttons), retro-futurism (synthwave sunsets, wireframe grids, glowing lines).
- **Colour and contrast**: duotone (two contrasting colours and their shades), monochromatic (one base hue), pastel goth (milky pastels with stark black type and borders), OLED dark (true black backgrounds for contrast and pop).

## Soft

Polished, calm, expensive. Stitch words: editorial or split-screen, glassmorphism, monochromatic.

- **Nested enclosures.** Here, and only here, a container inside a container is the language itself. A premium card, image or container never sits flat on the background. An outer shell with a faint tint (`bg-black/5` or `bg-white/5`), a hairline ring, a little padding and a large radius; an inner core with its own surface, an inner highlight (`shadow-[inset_0_1px_1px_rgba(255,255,255,0.15)]`) and a radius calculated smaller so the curves stay concentric (`rounded-[calc(2rem-0.375rem)]`).
- **Pill buttons** with generous padding. A trailing arrow sits inside its own small circular wrapper flush with the button's right padding, never naked beside the text.
- **Macro whitespace**: section padding doubled (`py-24` to `py-40`).
- **Floating island navigation**: a glass pill detached from the top (`mt-6 mx-auto w-max rounded-full`), a hamburger whose lines rotate into an X, a menu that opens as a full-screen glass overlay with links staggering up from below.
- Any asymmetric layout above `md:` falls back to full width with modest padding below 768px.

## Minimalist

Document-style product UI in the Notion and Linear family. Stitch words: Swiss or editorial,
monochromatic.

- **Type**: a clean geometric or system-native sans for body, UI and buttons; a serif for hero headings and quotes only where the brand or brief earns one, tightly tracked (-0.02em to -0.04em) at line height 1.1; a mono for code, keystrokes and metadata. Body in off-black (`#111111` or `#2F3437`) at line height 1.6; secondary text in muted grey (`#787774`).
- **Palette**: warm monochrome. Canvas `#FFFFFF` or warm bone (`#F7F6F3`, `#FBFBFA`); card surfaces `#FFFFFF` or `#F9F9F8`; structural borders `#EAEAEA` or `rgba(0,0,0,0.06)`; accents only as washed-out pastels for tags, inline code and icon backgrounds: pale red `#FDEBEC` on `#9F2F2D`, pale blue `#E1F3FE` on `#1F6C9F`, pale green `#EDF3EC` on `#346538`, pale yellow `#FBF3DB` on `#956400`.
- **Components**: asymmetric grid cards with exactly `1px solid #EAEAEA`, radius 8 to 12px, generous padding (24 to 40px). Primary buttons solid `#111111` on white, radius 4 to 6px, no shadow, hover to `#333333` or a micro scale. Tags as small uppercase pills in the pastels. Accordions stripped of boxes, separated by a bottom hairline, toggled by a plain plus and minus. Keystrokes as `<kbd>` with a hairline border, 4px radius and the bone background, in the mono.
- **Motion**: quiet; nothing decorative.

## Brutalist

Two coherent languages; pick one per project and never mix them. Stitch words: brutalist, Swiss,
grainy, duotone or OLED dark.

- **Swiss industrial print (light)**: matte paper backgrounds (`#F4F4F0`, `#EAE8E3`), carbon ink (`#050505` to `#111111`), one accent, hazard red (`#E61919` or `#FF2A2A`), for strike-throughs, thick dividing rules and vital highlights.
- **Tactical telemetry (dark)**: deactivated-CRT backgrounds (`#0A0A0A`, `#121212`), white phosphor text (`#EAEAEA`), the same red on the same rules, and terminal green (`#4AF626`) for at most one element with a purpose.
- **Type**: structural headers in a heavy neo-grotesque (Neue Haas Grotesk Black, Archivo Black, Roboto Flex heavy, Monument Extended) at fluid scale (`clamp(4rem, 10vw, 15rem)`), tracking -0.03em to -0.06em, leading 0.85 to 0.95, uppercase. Data and telemetry in a mono (JetBrains Mono, IBM Plex Mono, Space Mono, VT323, Courier Prime) at 10 to 14px, tracking 0.05em to 0.1em, uppercase. A high-contrast serif only as a rare textural disruption, degraded with halftone or dithering.
- **Layout**: a strict grid with elements anchored to tracks; visible compartments by 1px or 2px solid borders and full-width rules; density that oscillates between packed mono metadata and vast negative space around macro type; no radius anywhere. `display: grid; gap: 1px` with contrasting parent and child backgrounds draws razor-thin dividers without border declarations.
- **Symbology**: ASCII framing (`[ DELIVERY SYSTEMS ]`, `>>>`, `///`), registration and copyright marks as geometric elements, crosshairs at grid intersections, barcode stripes, warning stripes. Here, and only here, the crosshair grid lines and uppercase metadata that the tells list names are the language itself.
- **Texture**: halftone and 1-bit dithering on images and serif type; CRT scanlines by `repeating-linear-gradient` on dark backgrounds; a global low-opacity noise filter on a fixed pointer-transparent layer.
- **Markup**: `<data>`, `<samp>`, `<kbd>`, `<output>`, `<dl>` where the content is technical.
