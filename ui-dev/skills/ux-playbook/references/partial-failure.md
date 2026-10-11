# Partial failure

**Reach for this when** a page is made of sections that come from different places (a profile
header and a feed, a sidebar and its charts, a list and its comments), and when deciding what
happens if one section is slow or fails. Also when a page has a single spinner gating everything, or
a single "something went wrong" that replaces the whole page.

## The rule

Every section of a page is responsible for its own data, its own loading state and its own errors.

- Each section fetches on its own, against its own request.
- Each section shows its own loading state, in its own space.
- If a section fails, it shows its own error and its own retry button, and the rest of the page stays
  completely usable.
- The page's first paint is never gated on the slowest section. Whatever has arrived is shown.
- Where a section has a previous value cached, show that immediately and swap in the fresh data when
  it arrives, so a slow fetch never looks like a failure.

This is graceful degradation in the fault-isolation sense: the app keeps working with whatever it
has.

## Why

A screen looks like one page, but almost nothing on it comes from the same place. Your profile
picture is one server, your feed is another, and they arrive at different speeds. If you ordered
from three restaurants and one was late, you would not throw the other two away. Gating the whole
page on the last section, or blanking it all because one section errored, is that overreaction.

Instagram shows stories before the feed is ready. A dashboard shows its sidebar before its charts.
The BBC News homepage shows navigation and text before images. A broken escalator still works as
stairs. Each is the same idea: fail in pieces, so the important parts remain.

The cache-then-swap trick goes further: the person is scrolling content the whole time and never
sees a loading state at all, because a slightly stale feed is better than an empty one.

## How to build it

1. Structure the fetches so that each section is a separate request. This is the precondition;
   nothing else here works if one call blocks the page until everything is ready.
2. Each section owns its loading state, rendered in its own space. Skeleton for a first full-page
   load; a plain spinner for one module refreshing inside an already-loaded page.
3. Each section has its own error boundary. On failure it renders a small local error with a retry
   that re-fetches only that section. Test by forcing one endpoint to return a 500 and confirming the
   rest of the page renders and works.
4. Never delay the first appearance of ready sections for one still loading.
5. Where a section has a cached previous value, render it on the first frame and replace it when the
   fresh fetch resolves (stale-while-revalidate). Anywhere staleness could mislead (prices, stock,
   anything time-sensitive) needs a visible "last updated" or a revalidation window short enough
   that it never matters.
6. Design each section in at least three states (loaded, loading, failed with retry) before build
   starts. This is a design-time decision, not something improvised in implementation.
7. Be precise about which sense of graceful degradation a piece of work is. Browser fallback
   (polyfills, feature detection) and section fault isolation (independent fetch, error boundaries)
   are both called by the name and are solved by different code.

## Evidence and caveats

- "Graceful degradation" is a real, old engineering term (fault-tolerant systems from the 1960s
  onward). In web development it classically means fallback for older browsers (MDN), with
  progressive enhancement as its complement. The per-section sense used here is the broader
  reliability-engineering sense applied to the front end, and it is current and accepted (Smashing
  Magazine, 2024), but the two senses are distinct and should not be conflated.
- It is not one of the Laws of UX and has no Nielsen Norman Group article; it is the source
  creator's own application of a real term.
- The cache-then-swap technique is a named, standardised pattern: stale-while-revalidate, RFC 5861,
  an HTTP Cache-Control extension. The source video never names it and hedges whether Instagram
  really works this way; the mechanism it describes is exactly what the RFC defines, however it is
  implemented.
- The source video's own restaurant mock-up resolves to all three orders delivered at the moment it
  discusses one failing, so the failure case is only ever described, never drawn. The wireframe in
  part 10 (header loaded, one card succeeded, one card "Failed / Retry") is the picture to hold in
  mind.

## Sources

- Synsation, Build for Good UX parts 9 and 10 (graceful degradation).
- MDN Web Docs, Glossary: Graceful degradation; Progressive enhancement.
- Smashing Magazine, "The Importance Of Graceful Degradation In Accessible Interface Design" (2024).
- Nielsen Norman Group, "Skeleton Screens 101" (full page versus single module).
- RFC 5861, HTTP Cache-Control Extensions for Stale Content; MDN, Cache-Control.
