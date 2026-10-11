# The items

Each item has three parts: what **in place** means, how to **detect** it from a repo, and what
**building** it involves. Stack notes are inline where stacks differ. Items are numbered as Alex
Yates read them out; the groups are the walk order.

Contents
- [Detecting the stack](#detecting-the-stack)
- [Conversion](#conversion) — 2, 4, 8, 9, 15, 20
- [Discoverability](#discoverability) — 3, 5, 10, 11, 12, 13, 16, 17
- [Trust and housekeeping](#trust-and-housekeeping) — 1, 6, 7, 14, 18, 19
- [Security (from the comments)](#security-from-the-comments) — 21, 22, 23
- [Stack extras (not in the reel)](#stack-extras-not-in-the-reel)

## Detecting the stack

Look for the lock file and the framework config before anything else; nearly every check below
depends on where pages and the `<head>` live.

| Signal | Stack | Pages | `<head>` / metadata | Static files |
|---|---|---|---|---|
| `next.config.*`, `app/` | Next.js App Router | `app/**/page.tsx` | `export const metadata` / `generateMetadata` per route; `app/layout.tsx` | `public/` |
| `next.config.*`, `pages/` | Next.js Pages Router | `pages/**/*.tsx` | `next/head` per page; `pages/_document.tsx` | `public/` |
| `astro.config.*` | Astro | `src/pages/**` | the layout's `<head>`; `astro:seo` or manual tags | `public/` |
| `nuxt.config.*` | Nuxt | `pages/**` | `useHead` / `useSeoMeta`; `app.vue` | `public/` |
| `svelte.config.*` | SvelteKit | `src/routes/**/+page.svelte` | `<svelte:head>` per page | `static/` |
| `gatsby-config.*` | Gatsby | `src/pages/**` | Head API export per page | `static/` |
| `*.html` at root, no framework | static HTML | the files | each file's `<head>` | wherever it is served from |
| `templates/*.html`, `main.py`, `app.py` | Python server (FastAPI / Flask / Django) with Jinja | templates | base template `<head>` | `static/` mounted in the app |
| `wp-content/` | WordPress | theme + editor | theme `header.php` or an SEO plugin | theme dir / uploads |

Also record: is there a backend at all; are there forms, and do they POST to it; is an LLM wired in
(an Anthropic / OpenAI client, a chat route); how is it hosted if the repo says (`vercel.json`,
`netlify.toml`, `firebase.json`, `cloudbuild.yaml`, `Dockerfile`, `nginx.conf`, `_headers`).

---

## Conversion

### 2. CTA above the fold
**In place**: the first screen of the home page, on mobile and desktop, holds one clear primary
action — a button or link to the thing the site wants (book, enquire, sign up, call). One, not three.
**Detect**: read the home page's hero section. Is there a button/link styled as primary in the first
section? On a static site, the first `<section>` or the first element after the nav. Check it is not
only visible after scrolling on a phone (a hero image taller than the viewport pushes it under).
**Build**: add the primary action to the hero, wired to the enquiry form, booking page or sign-up
route that exists. Do not invent a destination — if there is no form and no booking route, that is
the real gap; say so.

### 4. Thank-you page after an enquiry
**In place**: submitting the contact/enquiry form lands on a page (or a state) that confirms it went
through, says what happens next, and ideally when (ties to item 8). Not a bare "Success" toast.
**Detect**: find the form's submit handler or `action`. Where does it go? Look for `/thank-you`,
`/thanks`, `/contact/success`, a `redirect(` after the POST, or a success state in the component.
**Build**: a route or state reached only after submit. Copy: one sentence confirming, one saying
what happens next and when. Make it unreachable by the sitemap (`noindex`) — it is not a landing
page. If the site has analytics (item 19), this is where a conversion event fires.

### 8. Response-time promise
**In place**: near the form or contact details, a concrete promise — "We reply within one working
day". Concrete means a number.
**Detect**: grep the contact page, the form component and the thank-you page for "within", "reply",
"respond", "hours", "working day".
**Build**: **needs you** — the owner names the time they will honour. Put it beside the form and on
the thank-you page. Never pick a number for them; a promise they cannot keep is worse than none.

### 9. Sticky mobile CTA
**In place**: on narrow viewports, the primary action (call, book, enquire) stays reachable while
scrolling — a fixed bar at the bottom, or a sticky header button.
**Detect**: look for `position: fixed` / `sticky` / Tailwind `fixed bottom-0` / `sticky top-0`
wrapping a CTA, gated to a mobile breakpoint (`md:hidden`, a media query). Read the header component
too — a sticky header with the CTA in it counts.
**Build**: a fixed bottom bar on small screens with the one action, hidden once the page's own CTA
or the form is in view (an IntersectionObserver, or simply hide on the contact page). Respect safe
areas (`env(safe-area-inset-bottom)`). Give it a `z-index` above content and below any modal.
**n/a** for docs sites and most SaaS apps — the CTA there is the product.

### 15. Real customer reviews
**In place**: a reviews or testimonials section with named, attributable reviews — a real name, and
ideally where the review came from (Google, Trustpilot, a linked source).
**Detect**: grep for "testimonial", "review", `★`, `Review` schema. If found, read them: are they
placeholder lorem, or suspiciously generic? Generic five-stars with first-name-only attribution are
a *partial* at best.
**Build**: **needs you** — the owner supplies the reviews, verbatim, with names and sources they have
permission to use. Build the section and the `Review`/`AggregateRating` schema only around real
content. Never draft a review. If they have none yet, the honest build is a section that links out
to their live Google profile, or nothing.

### 20. Real team photo
**In place**: a photograph of the actual people, on the about page or the home page. Not stock, not
an AI render, not an illustration standing in for one.
**Detect**: find the about/team section; inspect the image filenames and sources (`unsplash`,
`pexels`, `stock`, `placeholder`, `generated` are all tells). If the image is a real file, you cannot
tell from the repo that it is them — mark *blocked* and ask.
**Build**: **needs you** — the owner supplies the image. Place it with real alt text (item 16) naming
who is in it, sized and compressed for the web.

---

## Discoverability

### 3. Internal links
**In place**: pages link to each other in the body copy and in a footer nav — service pages to case
studies, FAQs to the contact page, the blog to the services it mentions. Every public page is
reachable from at least one other page's content, not only the nav.
**Detect**: collect the routes; for each, count inbound `<a href>`s from other pages (excluding the
header nav). Orphans — pages with zero inbound links — are the finding. A footer with a sitemap-style
nav largely satisfies this.
**Build**: a footer nav listing every public page; contextual links where the copy already names
another page's subject. Do not stuff — one or two per page where they help.

### 5. Breadcrumbs
**In place**: on pages deeper than one level (`/services/roofing`, `/blog/post`), a breadcrumb trail
in the page and `BreadcrumbList` JSON-LD in the head.
**Detect**: grep for `breadcrumb`, `aria-label="Breadcrumb"`, `BreadcrumbList`. Check whether the
site *has* depth — a five-page flat site does not need them, mark *n/a*.
**Build**: a small component rendered on nested routes from the path segments, with the schema
alongside. Home › Section › Page. The last crumb is text, not a link.

### 10. robots.txt
**In place**: `/robots.txt` is served, allows the crawlers the owner wants, and points at the sitemap.
Staging or preview deploys should *disallow* — check the config does not do the opposite.
**Detect**: `public/robots.txt` or `static/robots.txt`; Next.js App Router can generate it from
`app/robots.ts`; Astro/Nuxt often via a plugin. If the site is live, `curl https://…/robots.txt`.
Check for an accidental `Disallow: /` left over from staging. Decide with the owner about AI
crawlers (`GPTBot`, `ClaudeBot`, `PerplexityBot`, `CCBot`) — blocking the search ones removes the
site from AI answers; blocking training-only ones is a separate choice. Ask only if they have a view.
**Build**: a `robots.txt` allowing `/` for all, `Sitemap:` pointing at the sitemap URL, and disallow
rules for the thank-you page, API routes and admin. Environment-aware if the stack supports it.

### 11. Unique page titles
**In place**: every page has a `<title>` of its own, 30–65 characters, the page subject first and the
brand last ("Roof repairs in Bristol | Acme Roofing"). No two pages share one.
**Detect**: App Router — `metadata.title` per `page.tsx`, or a `title.template` in the layout; Pages
Router — `<Head><title>` per page; Astro — the layout prop; static — each file's `<title>`. List
them; duplicates and missing ones are the finding.
**Build**: a title per page in the stack's idiom. Use a layout-level template for the brand suffix
so pages set only their subject.

### 12. Meta descriptions
**In place**: every indexable page has a `<meta name="description">`, 120–160 characters, unique,
written as the line you want under the result — what this page is and why click.
**Detect**: same places as item 11. Same duplicates-and-missing pass.
**Build**: one per page. Write them from the page's actual content; if a page has no content yet
(a placeholder route), the description is not the problem.

### 13. Social share images
**In place**: Open Graph tags — `og:title`, `og:description`, `og:image` (1200×630, absolute URL),
`og:url`, `og:type` — and `twitter:card` (`summary_large_image`) on every page, at least a site-wide
default image plus per-page where it matters.
**Detect**: grep for `og:image`, `openGraph`, `twitter:card`. Check the image exists at the path
named and is 1200×630 (read its dimensions). App Router can generate per-route with
`opengraph-image.tsx`. If live, the share-debugger tools verify it; otherwise *verify after deploy*.
**Build**: a default image (the owner supplies or approves one — a logo on brand colour is the
honest default), the tags in the layout/base template with per-page overrides for title and
description, absolute URLs built from the site's canonical origin.

### 16. Alt text on images
**In place**: every `<img>` (and framework `<Image>`) has an `alt`. Meaningful images describe what
is shown; decorative ones have `alt=""` explicitly, not a missing attribute.
**Detect**: grep `<img` / `<Image` without `alt=`; also `alt=""` on images that are clearly content
(team photo, product shot). A lint rule (`jsx-a11y/alt-text`, `markuplint`) does this if present.
**Build**: write the alt from what the image shows and what it is for on that page. For the team
photo, name the people only if the owner says. For logos, the company name. Decorative → `alt=""`.

### 17. Local business schema
**In place**: JSON-LD `LocalBusiness` (or a subtype: `Plumber`, `Dentist`, `Restaurant` — the
subtype is better) on the home page, with `name`, `address` (`PostalAddress`), `telephone`, `url`,
`openingHoursSpecification`, `geo` where known, `image`, `priceRange` optional, `sameAs` to the
Google profile and socials. Matches the footer's NAP (name, address, phone) exactly.
**Detect**: grep `application/ld+json`, `LocalBusiness`, `@type`. Validate any found block parses
and its address matches what the footer says. *n/a* for a SaaS with no premises — `Organization`
is the equivalent there, and is a stack extra, not this item.
**Build**: **needs you** for the address, phone, hours and subtype — ask in the walk if not already in
the repo. Then a JSON-LD block in the home page head (or a shared component), one source of truth
for NAP shared with the footer and the contact page so they cannot drift.

---

## Trust and housekeeping

### 1. Custom 404 page
**In place**: unknown URLs return HTTP status 404 *and* a branded page — nav, a sentence, a link home
and to the main thing. Both halves matter: a pretty page served with 200 tells search engines the
junk URL is real.
**Detect**: App Router `app/not-found.tsx`; Pages Router `pages/404.tsx`; Astro `src/pages/404.astro`;
SvelteKit `+error.svelte`; Nuxt `error.vue`; static hosting `404.html` + the host's config; Python
server — an exception handler for 404 rendering a template. If live: `curl -sI https://…/definitely-
not-a-page | head -1` and confirm `404`. Otherwise *verify after deploy*.
**Build**: the framework's file, with the site's layout, a line of copy in the site's voice, links to
home and the primary action. Confirm the status code, not only the page.

### 6. Case studies
**In place**: at least one page or section showing real work — the problem, what was done, the
result — ideally with the customer's permission to name them. For a SaaS this is "customers" or
"how X uses us".
**Detect**: routes or sections named case-study, work, projects, portfolio, customers, results.
Read what is there — placeholder cards with "Project name" are *partial*.
**Build**: **needs you** — the owner supplies the cases. Build the route and the template; populate
only with what they give. An empty case-studies page is worse than none; if they have none, defer.

### 7. Five FAQs
**In place**: an FAQ section (home or its own page) with about five real questions customers ask,
answered plainly, with `FAQPage` JSON-LD so they can show as rich results.
**Detect**: grep `FAQ`, `faq`, `FAQPage`, `<details>`. Count them; read them for placeholder-ness.
**Build**: the owner supplies or approves the questions — ask for the five they actually get asked,
or draft five from the site's copy *and present them for approval* in the walk rather than
publishing a guess. Accordion or plain list, plus the schema built from the same data.

### 14. Maps and directions
**In place**: the contact page shows where the business is — an embedded map or a static map image
with a "Get directions" link to Google/Apple Maps — and the address in text beside it.
**Detect**: grep `maps.google`, `google.com/maps`, `maps.apple`, `<iframe`, `Map` component; check
the address is in text too.
**Build**: **needs you** for the address if not in the repo. Prefer a "Get directions" link (no
third-party script, no consent question) plus a static image; an embedded Google Maps iframe loads
Google scripts and cookies, which is a privacy-policy matter (item 18) — build it only if they chose
it. *n/a* for online-only businesses.

### 18. Privacy policy page
**In place**: a `/privacy` (or `/privacy-policy`) page, linked from the footer, that truthfully
describes what the site collects (forms, analytics, embedded maps, cookies), why, the lawful basis
where it applies, and how to contact the controller. Plus a cookie consent mechanism **if** the site
sets non-essential cookies (analytics with cookies, embedded video, maps) — in the UK/EU that is not
optional.
**Detect**: a route named privacy; a footer link to it; grep "privacy". Read it against the audit:
does it mention the analytics tool present (item 19)? The map embed? The form? A policy that does not
match what the site does is *partial* and a legal risk in itself.
**Build**: **needs you** for the substance — who the controller is, the contact address, what is
collected. The page structure and the list of processors can be written from the audit (you know
which scripts load), but the owner reviews every sentence and this is not legal advice — say so in
the summary. Add the footer link. If a consent banner is needed and they said yes, prefer a small
library over hand-rolling, and gate the analytics script behind consent.

### 19. Google Analytics
**In place**: an analytics tool installed, site-wide, loading on every page, with the thank-you page
(item 4) firing a conversion event. Whether it is GA4 specifically is a choice, not a requirement.
**Detect**: grep `gtag`, `G-`, `googletagmanager`, `plausible`, `posthog`, `umami`, `fathom`,
`@vercel/analytics`. Check it is in the layout, not one page. A snippet in source is not proof events
arrive — *verify after deploy* in the owner's dashboard.
**Build**: **ask how** — this item has a real fork: GA4 (free, richest, cookies → consent banner in
UK/EU); a privacy-first hosted tool (Plausible, Fathom, Simple Analytics — paid, cookieless, no
banner); self-hosted (Umami, PostHog). Build only what they chose, with the ID in an environment
variable, not hard-coded, and the conversion event on the thank-you page. Never add tracking without
an explicit yes, and note the privacy-policy consequence (item 18).

---

## Security (from the comments)

Raise each only when the audit shows it applies.

### 21. CSRF protection on forms
**Applies when**: forms POST to the site's own backend and the backend uses cookie sessions.
Token-in-header APIs and third-party form endpoints (Formspree, Netlify Forms) are not exposed this
way.
**In place**: the framework's CSRF mechanism is on — Django's middleware and `{% csrf_token %}`,
Flask-WTF, FastAPI with a token scheme, SvelteKit's built-in origin check, Next.js Server Actions'
origin check, `SameSite=Lax/Strict` on the session cookie.
**Detect**: read the form's POST handler and the session cookie settings.
**Build**: the framework's own mechanism, never a hand-rolled one.

### 22. Content Security Policy
**Applies when**: the site is served from somewhere headers can be set (almost everywhere —
`next.config.js` `headers()`, `netlify.toml`, Vercel `headers`, nginx, `_headers` on Cloudflare
Pages, a FastAPI middleware). Static hosts with no header control get *blocked*.
**In place**: a `Content-Security-Policy` header (or meta) that names the script and frame sources
the site actually uses — including the analytics and map domains chosen in items 14 and 19 — and
nothing broader. Plus the companions: `X-Content-Type-Options: nosniff`, `Referrer-Policy`,
`Permissions-Policy`, `Strict-Transport-Security` on HTTPS.
**Detect**: grep the hosting config and middleware for `Content-Security-Policy`; if live,
`curl -sI` the home page.
**Build**: start from the scripts the audit found, write the policy to allow exactly those, deploy
in `Content-Security-Policy-Report-Only` first if the site is live and there is any doubt. Say in the
summary that the policy must be updated when a new third-party script is added.

### 23. Prompt injection
**Applies when**: the site calls an LLM with content a visitor or a fetched page can influence — a
chat widget, a "summarise this", a form field that ends up in a prompt.
**In place**: visitor-supplied text is fenced in the prompt (clearly delimited, with an instruction
that it is data to be read, not instructions to follow), the model has only the tools the feature
needs, and nothing the model says is executed or rendered as HTML without sanitising.
**Detect**: find the LLM client call; trace what goes into the prompt and what is done with the
output.
**Build**: fence the untrusted text; strip tools the feature does not need; render model output as
text. This is hygiene, not a security audit — say so.

---

## Stack extras (not in the reel)

Offer only the ones the audit shows are missing *and* the stack plainly wants. Label each "not in
the reel" in the walk.

- **sitemap.xml** — generated from the routes (App Router `app/sitemap.ts`, `@astrojs/sitemap`,
  `@nuxtjs/sitemap`, a static file for small sites), referenced from `robots.txt` (item 10).
- **Canonical URL** — `<link rel="canonical">` per page, absolute, matching the `og:url`. Stops
  `?utm=` and trailing-slash variants splitting the page's ranking.
- **Favicon set** — `favicon.ico`, an SVG, `apple-touch-icon.png` (180×180), and a `site.webmanifest`
  with the 192/512 PNGs. App Router picks these up from `app/`; everyone else links them in the head.
- **Viewport meta** — `<meta name="viewport" content="width=device-width, initial-scale=1">`.
  Frameworks add it; static sites forget it.
- **`llms.txt`** — a short plain-text page at `/llms.txt` saying what the site is and linking its
  key pages, for AI crawlers. Cheap; only if the owner wants AI-search visibility.
- **`security.txt`** — `/.well-known/security.txt` with a contact for vulnerability reports. Only
  if the site has a backend worth reporting on.
- **Organization schema** — the SaaS/agency equivalent of item 17: `Organization` JSON-LD with
  `name`, `url`, `logo`, `sameAs`. Offer when item 17 was *n/a*.
- **`lang` attribute on `<html>`** — `lang="en-GB"` or whatever it is. Screen readers and search
  engines both use it; static sites and some templates omit it.
- **Redirect hygiene** — `www` → apex (or the reverse) and `http` → `https`, one hop. Only
  checkable live; *verify after deploy* otherwise.
