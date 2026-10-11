---
name: launch-checklist
description: Walk a website's repo before it goes live — check which of the twenty pre-launch essentials (custom 404, CTA above the fold, thank-you page, breadcrumbs, FAQs, robots.txt, unique titles, meta descriptions, social share images, alt text, local-business schema, privacy policy, analytics, real reviews, team photo and the rest) are in place, then ask the user about each missing one, one question at a time — build it, skip it as overkill for now, or leave it for them — and build only what they approved. Use whenever the user says "pre-launch check", "launch checklist", "is this site ready to ship / go live?", "what am I missing before launch?", "yates check", "run the 20", or asks what a marketing site, landing page or small-business website still needs before it is published. Use it even when they only mention one or two items (a 404 page, meta tags, SEO basics) in a pre-launch context — the rest of the list is what they will forget.
---

# Launch checklist

Twenty things a website should have before it goes live, checked against the repo, then decided on
one at a time with the person who owns the site. The list is Alex Yates's
([@yatesvids](https://www.instagram.com/reel/Db15Zn0hSmH/), August 2026) — "20 things to tell
Claude to add to your site before launching" — plus three his commenters added and whatever the
stack in front of you obviously wants.

The value here is not the list. Anyone can find twenty launch items. The value is that the decision
about each one is made by the owner, with the evidence in front of them, and that the build touches
only what they said yes to. Somebody who asked for a launch check and got twenty unasked-for changes
has been handed a pile of review work, not a finished site.

## The shape of a run

Three stages, and they do not overlap:

1. **Audit** — read-only. Detect the stack, then check every item and write down what you found.
2. **Walk** — one item per question, using AskUserQuestion. Nothing is built during the walk.
3. **Build** — the approved set, in one pass, then a summary. No commits.

Keeping the walk free of building is what makes it bearable: the owner answers twenty-odd short
questions in a row with the evidence fresh, rather than waiting for a build between each. Keeping the
build free of new questions is what lets it run straight through.

## Before running

Ask, using AskUserQuestion, before touching anything — unless the request already answered it:

- **Which site, and what kind?** The root to audit (if the repo holds more than one surface), and
  whether it is a marketing site for a local business, a product site for a SaaS or app, a portfolio,
  or documentation. This decides relevance: a docs site has no use for a sticky mobile CTA or
  customer reviews, and a SaaS has no shop to put on a map. Irrelevant items are still listed in the
  audit, marked *not applicable*, so the owner can overrule.
- **Is it deployed anywhere yet?** A live URL lets you verify the things a repo cannot prove — that
  unknown paths really return HTTP 404, that `robots.txt` is served, that the share image resolves.
  Without one, those items are *blocked, verify after deploy* rather than green.

Two questions, once. Do not ask anything else up front — the per-item questions come in the walk.

## Stage 1 — audit

Detect the stack first (framework, router, where pages and the `<head>` live, how static files are
served, whether there is a backend, whether there are forms, whether an LLM is wired in). Write the
detection down in one line; every later check depends on it.

Then go through `references/items.md` in order and, for each item, record one of:

| Verdict | Meaning |
|---|---|
| **in place** | present, with the file and line that shows it |
| **partial** | some of it exists — say which half |
| **missing** | not there |
| **blocked** | cannot be verified from the repo (needs the live site, an account, or the owner's knowledge); say what would unblock it |
| **needs you** | missing, and the thing that is missing is content only the owner has — real reviews, the team photo, the office address, a response-time promise they will honour, the substance of a privacy policy |
| **n/a** | irrelevant to this kind of site, and why |

Every verdict carries evidence: a path and line for *in place* or *partial*, the search you ran for
*missing*. Evidence is what lets the owner answer the next stage's question in five seconds rather
than going to look. A verdict with no evidence is a guess; the one thing this skill must not do is
mark something green because it probably exists.

Keep the ledger in a file outside the repo (the scratchpad directory, not `/tmp`), because the
conversation may be compacted mid-walk and the ledger is the run. Do not write it into the repo —
nothing is written into the repo until the build.

**Owner-only content is never invented.** A reviews section with plausible-sounding quotes, a
"team" of stock faces, a made-up response time, a privacy policy that names data the site does not
collect — each is worse than the gap it fills, and the legal ones are worse than that. These get
*needs you*, and in the walk the owner is asked to supply the content or to defer the item.

After the 23, look at what the stack itself wants and was not on Yates's list — a sitemap, a favicon
set, a canonical tag, `llms.txt`, `security.txt`, the viewport meta, correct Open Graph image
dimensions. `references/items.md` ends with these. Add the few that genuinely apply, labelled
*not in the reel* so the owner knows where they came from. Do not pad the list to look thorough.

## Stage 2 — walk

**Brief first, in prose.** Before any question: the stack you found, the items that are in place
(one line each, with the evidence — so the owner can reopen one if they disagree), and how many are
left to decide. A person answering twenty questions deserves to know how many there are.

**Then one AskUserQuestion call per item.** The tool can carry four questions at once; do not use
that here, and never bundle items into a multi-select. Each question carries its own evidence and
gets its own answer; a form of twenty tickboxes gets twenty reflexive ticks. The question is the item in plain words plus what you found — "There is no 404
route; Next.js falls back to its default page. Build a custom one?" — and the options are always
from this set, fewest that apply:

- **Build it** — add it in the build pass
- **Overkill for now** — skip, noted in the summary so it can be picked up later
- **Fine as it is** — for *partial*: the owner accepts what exists
- **I'll supply the content** — for *needs you*: they give it now or after the run; ask for it in
  the same question's follow-up where it is short (an address, a response time), and otherwise leave a
  clearly marked placeholder only if they say so
- **Verify after deploy** — for *blocked*: note it for the summary's manual list

**Ask "how?" only where there is a real fork.** Analytics has one — GA4, a privacy-first alternative,
or a self-hosted one. Schema has one — LocalBusiness, Organization, or a specific subtype. A 404 page
mostly does not; the framework has one way to do it. When the fork is real, ask it as the next
question, after the yes, with the options spelled out and the trade-off in a clause each. When it is
not, decide and say what you decided in the build summary. Asking how to do something that has one
sensible way reads as not knowing the stack.

**Order**: walk the groups as `references/items.md` orders them — conversion, discoverability,
trust and housekeeping, security (only the ones that apply), then stack extras. Items marked *in
place* or *n/a* are not asked; they were in the brief.

Do not start building when the first yes arrives. Collect every answer, then move on.

## Stage 3 — build

Build the approved items in one pass, in the same order, using each item's build notes in
`references/items.md` and the stack you detected. Three rules govern the pass:

- **Touch only approved items.** A build that also "fixes" something nearby is a build the owner
  did not ask for. If you notice something while building, it goes in the summary as a finding.
- **Owner content stays the owner's.** Where they said they would supply it, leave the slot
  obviously unfilled — a named placeholder they will see, never prose that reads as real. Where they
  gave it, use it verbatim.
- **Nothing is tracked without a yes.** Analytics, tag managers, chat widgets, embedded maps that
  load third-party scripts — each is a data-processing decision with a privacy-policy consequence,
  so each was its own question and is built only if the answer was yes.

Do not commit. Leave the working tree for the owner to read; say so.

## Summary

End with one table — item, verdict before, what was done — grouped into **built**, **left for
later** (overkill for now), **needs you** (with exactly what to supply and where it goes), and
**verify after deploy** (with the command or check for each — `curl -I https://…/does-not-exist`,
the share-image debugger, a rich-results test). Then a short list of anything you noticed and did
not touch. That table is what the owner reads after the run and what the next run reads before it,
so it has to stand on its own.

## Why this shape

- **One question at a time** because the owner's objection to checklists is that they get rubber-
  stamped. Each item with its own evidence gets a real answer.
- **Audit before any question** because a question without evidence sends them off to look.
- **Build only what was approved** because a launch check that rewrites the site is a review
  burden, and a wrong unasked-for change is indistinguishable from a bug.
- **Blocked is not green** because a tracking snippet in the source is not proof analytics receives
  events, and a 404 component is not proof unknown URLs return 404 — the owner needs to know what
  was checked and what was assumed.
