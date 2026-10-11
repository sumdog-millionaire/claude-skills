# The brand folder

A brand lives under `docs/` in the working repository, tracked in git, so the identity travels with
the code that wears it. `DESIGN.md` carries everything visual in Google's open DESIGN.md format
(design-file.md), and the brand folder beside it carries what that format has no place for: the
written voice, the files, and the evidence.

**Every heading a person reads is plain words.** A senior business person with no design training opens
these files, so a heading says the thing: "Spelling, capitals, numbers and dates", never "Mechanics". A
heading the format fixes keeps its exact name, because tools find a section by it, and gets one plain
line under it (design-file.md has the lines). The words here are the same ones the brand skill in the
Shoulders of Giants product uses for the same section, so a person meets one vocabulary in both.

```text
docs/
  DESIGN.md               # Visual identity: exact values, reasons, logos, motion (design-file.md)
  PRODUCT.md              # Product record (design-file.md)
  brand/
    TONE-OF-VOICE.md      # Written voice
    assets/
      logos/
      fonts/
      images/
      icons/
      patterns/
    sources/              # Original guidelines and supplied evidence, unchanged
      README.md           # What was read, where it came from, rights and restrictions
      _research/          # Extraction notes, each rule cited to document and page
```

`DESIGN.md` sits in `docs/` and not inside `docs/brand/` because the style checker looks for it in
exactly three places, a project's own folder, its `docs/` and its `.agents/context/`, and its
design-system rules switch off silently when the file is anywhere else (design-file.md says how it
picks the project folder and how to prove the rules fire). `PRODUCT.md` sits beside it because the
style checker takes both from one folder.

A value is written once. Colours, fonts, corner rounding, spacing and component styling are
`DESIGN.md`'s and appear nowhere in the brand folder; the audience, what makes this different and the
brands we do not want to look like are `PRODUCT.md`'s and `DESIGN.md` points at them. A layout task
reads `DESIGN.md`; a writing task reads TONE-OF-VOICE.md.

Create only directories with supplied material; a sparse brand folder is valid. Use portable relative paths,
written from the repo root. Where a client's assets may not be committed, gitignore
`docs/brand/assets/` and `docs/brand/sources/` alone and say so; the markdown stays tracked. A repo
holding more than one product gives each its own `docs/` inside that product's folder, which is how
the detector resolves the file that governs an edit.

Onboarding a brand may be the whole task; it has no opening summary of the page and ends at the
approval step below.

## What the brand folder adds to DESIGN.md

The format's block of exact values and its eight sections are in design-file.md. A tool that reads the
format keeps a section it does not know, so the brand's remaining facts go in the same file, after the
format's sections:

```markdown
---
status: draft | approved
approved: <who and when, only after actual approval>
sources: <files, dates or version labels>
stitch: <assets/{id} and its scope, once a design system is registered (stitch.md)>
# then the format's keys: version, name, description, colors, typography, ...
---

## Overview
The one idea behind the brand, where it has one: the idea everything else serves. Then the
place and the moment the interface is used in. The audience and what makes this different are
PRODUCT.md's.

<!-- Colors to Do's and Don'ts, in the format's order, each with its plain line (design-file.md) -->

## Logos
Which file for which background and space, as a table that ends at a file. The empty space that must
stay around the logo, its minimum size, allowed backgrounds, colour treatments and what may never be
done to it, moving it included.

## Imagery and icons
Approved assets, subject and style guidance, cropping and credit requirements.

## Motion
Durations, curves and what motion is for. Say when none were supplied.

## Writing voice
The two or three governing lines a layout task needs, quoted; everything else is in
docs/brand/TONE-OF-VOICE.md.

## What the brand does, where its guidelines say nothing
Patterns read off the brand's finished digital work where the guidelines are silent, each
naming the work it was read from.

## Decisions made for this project, not brand rules
What the agent proposed and the user approved for this project where the brand is silent: a set of
text sizes, a dark theme, how things move. Never presented as the brand's own rule.

## Unknowns and conflicts
Missing information, unreadable evidence and unresolved contradictory sources.
```

File names rarely say which logo to reach for, because the choice turns on the background, the space
and what must be legible, so the Logos table is ordered by those questions and ends at a path.

## When there is no brand folder

If the repo has no `docs/DESIGN.md` and no brand folder, offer onboarding or a proposed look that is
openly unbranded. Do not silently create an identity.

Read the original guidance in `sources/` before relying on a rule whose meaning is uncertain. Resolve
logo versions, backgrounds and fonts by their documented job, not by whichever file is easiest to
find. For conflicting versions, ask which source is authoritative.

## Onboarding

1. Accept guidelines, examples, URLs and asset folders. Inspect the actual supplied material with suitable document/image tools. Identify unreadable files or missing capabilities; never claim to have extracted them.
2. Copy originals without modification into `sources/` and approved reusable assets into the relevant `assets/` directory. Where a source already lives in this repository under version control, record its path and the extraction commit in `sources/README.md` rather than copying it. Preserve existing files; do not overwrite a different asset with the same filename. Record each asset's relative path, source location and the applicable rights and restrictions in `sources/README.md`.
3. Draft `DESIGN.md`: the block of exact values and the format's sections from the brand's stated values (design-file.md), then the sections above. Each sourced rule names its source file and page or section where available. Mark unknowns and contradictory evidence rather than manufacturing certainty. Summarise sources; retain exact required wording separately where precision matters.
4. Draft TONE-OF-VOICE.md using the outline below, wherever voice material exists. Preserve approved and rejected copy verbatim, because a paraphrased example teaches the wrong thing. Reproduce banned lists in full rather than summarising them. Correct source typos before an example reaches a prompt, and list every correction so the change is visible.
5. Check what the material does not cover. Brand guidelines are often written for print and may state no text sizes, grid, spacing, components or motion. Say so plainly rather than inventing rules. Read the missing patterns off the client's own finished digital work and record them under "What the brand does, where its guidelines say nothing", so a reader can tell what the brand said from what the brand did.
6. Check the file for mistakes with the format's checker (design-file.md), then show the draft, the questions still open and the list of assets. Ask for approval once before first use. For material later changes, show the changes and obtain approval again. Record only approval actually given.

## TONE-OF-VOICE.md outline

```markdown
# <Brand name>: tone of voice

Status: draft | approved
Approved by/date: <only after actual approval>
Source versions: <files, dates or version labels>

## The one idea behind it
The one idea the voice serves, stated first, with its source.

## How to use this document for prompts
Which sections to paste into a writing prompt, and in what order.

## How formal the writing is
The brand's own scale (for example formal to conversational, or expert to friendly),
where it sits by default, and what moves it.

## How it should sound, and what it must never become
Three or four pairs, such as "plain, but never blunt", where the brand gives them or its
writing shows them.

## How the writing sounds by default
Default sentence length, whether it says "we" or the brand's name, tense, how warm and how
confident, with sources.

## How it changes for a web page, an email, a post or a product screen
One entry for each kind of writing the brand produces (web pages, email, social, product
screens, legal), each saying how it differs from the default.

## Spelling, capitals, numbers and dates
Spelling, punctuation, capitals, numbers, dates, units and formatting rules.

## Vocabulary
Preferred words, banned words in full, product and feature names as written.

## Worked examples
Approved writing word for word, and rejected writing word for word with the reason it was
rejected.

## Where these rules change for another product or audience
Where a second product line or a different audience changes any of the above.

## Unknowns
Voice questions the sources do not answer.

## Source typos
Each correction made to a source example before it was used, old and new. Omit when empty.
```

## Creative freedom

An omitted rule is not a prohibition. A brand folder containing only a logo and palette can support a
complete project design. The agent may propose fonts, motion and a dark theme that respect the
supplied rules; record these under "Decisions made for this project, not brand rules", never among the
brand's sourced rules.

Pause for material ambiguity, not every missing field. Altering or deforming an existing logo needs a clear decision if permissions are uncertain. Keep sourced logos intact while that decision is open. Functional accessibility and project constraints remain requirements; report a conflict rather than quietly substituting a different brand treatment.
