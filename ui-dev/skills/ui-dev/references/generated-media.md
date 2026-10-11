# Generated media

Read when a page uses generated images or video as a designed asset, especially a background video or
sequence tied to scroll. This branch extends the normal UI Dev workflow; it does not replace it.

Start with [workflow.md](workflow.md). Load [brands.md](brands.md), [persuade.md](persuade.md),
[styles.md](styles.md), [patterns.md](patterns.md), [motion.md](motion.md) and
[verification.md](verification.md) where their conditions apply, plus any other UI Dev reference the
task needs. `animate` owns motion code and constants.

## 1. Define the asset

Enter this branch after the direction is approved, so generated media serves the design rather than
becoming the design by accident. Name each asset's role: hero atmosphere, product demonstration,
transition, or sequence scroll.

For each asset, specify:

- subject and composition;
- source facts or supplied imagery that must remain intact;
- aspect ratio and minimum useful resolution from its real container;
- start, middle and end state;
- camera movement and subject movement separately;
- what stays fixed, including centre of mass when rotation must not translate;
- background colour from the approved design, or transparent output when the generator supports it;
- frame-bound constraints, including what must never leave the crop;
- duration, loop point and whether reversal must work; and
- text policy: keep text in accessible HTML unless the brief explicitly requires it inside the media.

A precise moving object normally starts from an approved still image. Generate from text alone when
variation is welcome. Use the available image or video generator; do not pretend a provider is
available. When generation needs a person or another tool, provide the complete prompt, settings and
input file, then wait for the returned candidates.

Agree candidate count before paid generation. One candidate is the default; propose two or three
only when selection value justifies the extra cost.

## 2. Record provenance and selection

Add a `## Generated media` section to the project's `DESIGN.md`. For each selected asset record its
role, prompt, generator and model, settings, date, input asset, output path, known rights or
restrictions, and why this candidate was chosen. Record uncertainty rather than inventing licence
terms.

Review the candidate at full size and in its intended crop. Check subject fidelity, unwanted text,
edge integrity, background consistency, loop or reversal, and visible generation artefacts. Approval
of the page direction does not approve a later generated asset; show the selected candidate before
production integration.

## 3. Prepare the selected file

Use [`../scripts/prepare_media.py`](../scripts/prepare_media.py); it requires `ffmpeg` and `ffprobe`.
Keep the source video. First extract a local master sequence:

```powershell
python "$HOME/.claude/skills/ui-dev/skills/ui-dev/scripts/prepare_media.py" extract input.mp4
```

By default this creates `input_frames/` beside the video. It writes every decoded source frame at the
source dimensions as lossless PNG, without frame-rate conversion or image alteration. Its manifest
records each stable filename, source index and presentation timestamp. This prevents further loss; it
cannot restore detail already lost in the source video.

Create a separate web derivative only after inspecting the master and deciding what the page needs:

```powershell
python "$HOME/.claude/skills/ui-dev/skills/ui-dev/scripts/prepare_media.py" optimise input_frames public/media/sequence --frame-count 80 --width 960 --quality 5
```

`optimise` uses all master frames and their original dimensions unless `--frame-count` or `--width`
is supplied. JPEG quality ranges from 2, highest, to 31, lowest. When `--frame-count` is supplied, the
current baseline selects evenly spaced frames including both endpoints. Do not assume this is the
best selection for uneven or significant motion: keep all frames instead. The master manifest leaves
a future semantic or LLM selector free to choose exact source frames without changing extraction.

For a muted hero background, prepare the video separately from the untouched source:

```powershell
python "$HOME/.claude/skills/ui-dev/skills/ui-dev/scripts/prepare_media.py" hero input.mp4 public/media/hero.mp4 --poster public/media/hero.jpg
```

A uniform studio background can be keyed into transparent PNG derivatives:

```powershell
python "$HOME/.claude/skills/ui-dev/skills/ui-dev/scripts/prepare_media.py" optimise input_frames public/media/sequence-alpha --chroma-key FFFFFF
```

Flat-colour keying is not semantic background removal. Inspect edges at full size; generated shadows,
reflections, hair and subject details matching the background often key badly. Keep the background
and blend it with the page when the keyed result is worse. Use a dedicated segmentation tool only
when the brief requires arbitrary background removal and that tool is actually available.

## 4. Integrate by role

### Hero background

Use a real `<video>` with `autoplay`, `muted`, `loop`, `playsinline`, `preload="metadata"` and the
generated poster. Reserve its aspect ratio. Use `object-fit: cover` only after checking every target
crop. Blend a flat media background into the page with a restrained radial or linear mask rather than
hiding content under blur.

Keep headings, calls to action and factual content in HTML above the media. Contrast must pass over
every frame, not just the poster. Reduced motion and failed video loading show the poster without a
compulsory delay.

### Sequence scroll

Use normal document scrolling and a sticky scene as described in [motion.md](motion.md). The text
remains semantic HTML; the canvas or image is decoration unless it conveys information that needs an
accessible equivalent.

- Let `animate` choose CSS scroll-driven animation, Motion or GSAP for progress and interruption.
- Map clamped scroll progress to `round(progress * (frameCount - 1))`; continuous progress never
  lives in React state.
- Load the poster and current frame first. Begin neighbouring-frame preload near the section rather
  than delaying the page on every frame.
- Draw at the rendered size and device-pixel ratio, update geometry through `ResizeObserver`, and
  coalesce repeated draws with `requestAnimationFrame`.
- Keep the last valid frame when one image fails; the base content remains readable when enhancement
  fails.
- Reduced motion removes pinning and frame travel and shows one representative frame with all content
  reachable.
- Reverse scrolling, resize, touch, keyboard and scrollbar movement must preserve the same sequence.

Start with direct video seeking only when it is smooth on target devices. Extract frames when measured
seeking is choppy; an image sequence trades more files and decoded memory for deterministic frame
selection.

## 5. Verify

Run the normal checks in [verification.md](verification.md), then verify the media-specific risks:

- source and prepared-file dimensions, duration and byte size are recorded;
- the poster, first useful frame and loop point do not flash or jump;
- text contrast passes across the complete moving background;
- slow loading and a failed video or frame leave the page usable;
- a narrow phone, touch scrolling, resize, reverse scroll and reduced motion keep all content
  reachable;
- the sequence starts loading near its section rather than blocking the page's main image;
- decoded memory, main-thread work, LCP and scroll smoothness are measured on a target device; and
- the selected media still matches the approved direction and recorded provenance.

Complete when every requested asset is selected and recorded, every selected file has a prepared
output, every role has a working fallback, and all required UI Dev and media-specific checks have an
honest result.
