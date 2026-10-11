# Optimising choices

**Reach for this when** a screen asks a person to choose between many things: a landing page with
several calls to action, a long form, a menu or dropdown that scrolls, a catalogue, a settings page,
a homepage for a large library of content.

## The rule

The time it takes to make a decision increases with the number and complexity of choices. So keep
what the person has to perceive and compare small, without cutting what the product can do.

- **Landing and entry screens** get one or two clear actions, not a dozen competing ones. Google's
  homepage is the extreme; Yahoo's portal is the clutter.
- **Forms longer than about seven fields** are split into steps, one grouped set at a time.
- **Large option sets** (a category menu, a catalogue) are not printed in full. Show a handful of
  the most relevant groups and let search or filtering absorb the rest.
- **Unavoidable complexity is grouped**, not flattened. Fourteen items under three headings read as
  less effort than fourteen in one list, though the count is unchanged.
- **Where usage data exists**, a short curated or personalised default beats an exhaustive one.
  Netflix's homepage is a few rows out of thousands of titles.

It is not about limiting what a person can do. It is about keeping the options manageable.

## Why

Twenty-four jars of jam draw more browsers to the table than six, but far fewer of them buy. A
menu of 250 items takes longer to order from than a menu of four. Every extra option on a screen is
something the person has to notice, weigh and reject before acting, and a landing page where a
dozen things compete for attention is measurably harder to decide on than one with two.

The relationship is logarithmic, not linear: the first few added choices cost far more decision time
than later ones. Going from two options to four hurts more than going from twenty to twenty-two.
That is why the fix is usually to cut the top level rather than trim the long tail, and why grouping
works: the person decides between three headings, then between a few items, rather than between
fourteen at once.

## How to build it

1. Cap top-level actions on any entry screen to the one or two most people came for. Everything
   else moves down a level (see `progressive-disclosure.md`).
2. Split any form past roughly seven fields into steps with a visible position indicator.
3. Replace long flat menus with a few categories plus filtering or search. Count the items in every
   dropdown; one that needs scrolling has failed.
4. Group related options under headings rather than listing them flat.
5. Build a curated default view only once real usage data exists to base it on. An arbitrary short
   list is not the mechanism Netflix is using.
6. Do not treat "fewer choices" as the goal. The question is whether what the person must compare at
   one time is small, not whether the product does less.

## Evidence and caveats

- **Hick's Law** (Hick 1952, Hyman 1953): decision time T = b·log₂(n+1) for n equally likely
  options. The source video's spoken definition matches Laws of UX word for word; what it omits is
  the logarithmic shape. The law models simple, comparable choices; it does not hold for highly
  familiar responses or for items searched from an alphabetical list.
- **The jam study is contested.** Iyengar and Lepper (2000): about 30% of six-jam browsers bought
  against about 3% of twenty-four-jam browsers. A 2010 meta-analysis of fifty choice-overload
  studies (Scheibehenne, Greifeneder and Todd) found the average effect near zero with high variance.
  Chernev et al. (2015) found the effect reliable only when options are complex, the decision is
  hard, preferences are uncertain and the chooser wants to minimise effort. Present choice overload
  as conditional, not universal.
- **The "over seven fields, multi-page converts 300% better" statistic** circulates through
  marketing blogs citing each other; no primary experiment was found, and other sources give
  different sizes for the same claim (Formstack 4.5% to 13.9%; HubSpot "86% higher"). The direction
  is consistent; the number is directional, not one to promise a stakeholder.
- **Netflix's "80% from recommendations"** is Netflix-sourced (Gomez-Uribe and Hunt, ACM TMIS 2016;
  an earlier 2012 Netflix blog put it at about 75%). The paper itself was paywalled during research.
- Nielsen Norman Group has no standalone article on Hick's Law, only a video on long menu lists.

## Sources

- Synsation, Build for Good UX part 14 (Hick's Law).
- Laws of UX, Hick's Law; Wikipedia, Hick's law.
- Iyengar and Lepper, "When Choice Is Demotivating", 2000; Scheibehenne, Greifeneder and Todd,
  "Can There Ever Be Too Many Options?", 2010; Chernev, Böckenholt and Goodman, 2015.
- Gomez-Uribe and Hunt, "The Netflix Recommender System", ACM TMIS 2016.
- Nielsen Norman Group, "Hick's Law: Designing Long Menu Lists" (video).
