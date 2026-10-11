# Control placement

**Reach for this when** placing a standard control (cart, search, account menu, notifications,
primary action, navigation), when tempted to put one somewhere original, when adapting a layout
from desktop to phone, and when the product ships to a right-to-left locale.

## The rule

People spend most of their time on other sites, so they expect yours to work the way those do.
Put a persistent, repeatedly used control where the sites people already use put it, not where it
looks most original.

But "where they put it" is not one answer. The convention varies by three things, and all three are
checked, never assumed:

- **Platform.** On desktop, the cart sits top right (Amazon, Target, Lululemon). In the same stores'
  phone apps, it sits in the bottom navigation bar.
- **Ergonomics.** On a phone held one-handed, the thumb lives at the bottom; the top corners are the
  hardest place to reach. Primary actions go in the thumb-reachable lower half.
- **Locale.** In a right-to-left language (Arabic, Hebrew, Persian, Urdu), the whole layout is
  mirrored. Amazon's Arabic site has the cart top left.

Predictability in structural components is not boring; it is what lets attention go to the actual
task.

## Why

Reaching your cart is something you want zero friction on. If it is not where habit looks for it,
there is a microsecond of "where is it?", a tiny moment of wait, and that is unnecessary. Multiply
it across every structural element that has been placed creatively and the product feels harder
than it is, without anyone being able to say why. The structure being predictable is exactly what
frees the person to focus on what matters, which in a shop is deciding what to buy.

The device and locale rules follow from the same law: the convention people carry with them is the
one from the device in their hand and the reading direction of their language. A desktop pattern
shrunk onto a phone is not a convention there, and a left-to-right layout merely translated into
Arabic breaks the scanning path Arabic readers use.

## How to build it

1. Before treating a placement as a creative opportunity, ask whether the control is a standardised
   one that carries a strong convention across the sites the audience already uses. If so, match
   the convention.
2. Check the convention per platform. A header-mounted cart on desktop does not imply a
   header-mounted cart on a narrow viewport; check what mobile apps in the category actually do
   (usually a bottom tab bar).
3. On any layout meant for one-handed phone use, design the primary action into the lower half and
   reserve the top corners for rare or two-handed actions.
4. For right-to-left locales, mirror the layout, not only the text: navigation position, icon
   direction, carousel controls and alignment all flip.
5. Before mirroring, list what should not flip: clock faces, and anything tied to a physical
   convention rather than reading direction, stay as they are. Numerals and embedded Latin text are
   not mirrored either.
6. When a genuine improvement requires breaking a convention (a redesigned checkout, say), do not
   switch everyone at once. Give people a way to preview or revert to the familiar version for a
   while, as YouTube did with its 2017 redesign.
7. Treat where the audience is located as a design input on the same footing as which device they
   use, not something bolted on after the design is finished.

## Evidence and caveats

- Jakob's Law is Jakob Nielsen's (co-founder of Nielsen Norman Group, 1998), stated on Laws of UX
  as "Users spend most of their time on other sites. This means that users prefer your site to work
  the same way as all the other sites they already know." The source video quotes this verbatim on
  screen.
- Laws of UX adds the gradual-migration guidance (the YouTube 2017 Material Design rollout let
  desktop users preview and revert), which the source video does not cover.
- The thumb argument matches Steven Hoober's 2013 UXmatters study (about 1,300 people observed;
  roughly half use the phone one-handed with the thumb doing the work), which produced the
  green/yellow/red "thumb zone" model. The source video gives the argument in one sentence and
  names no source.
- RTL mirroring is standard localisation practice, with the nuance above about what does not
  mirror, which the source video omits.
- The source video's own first mock-up looked like a phone screen while arguing a desktop
  placement, which is what prompted its follow-up part. The exact cart position on Amazon's Arabic
  app rests on the creator's word; the captured frame did not show it.
- One minor simplification: Nielsen's web usability work dates from 1994 at Sun, not "the early
  '90s"; his broader HCI research goes back to 1988.

## Sources

- Synsation, Build for Good UX parts 12 (Jakob's Law) and 13 (Jakob's Law continued: device and
  locale).
- Laws of UX, Jakob's Law; Nielsen Norman Group, "Jakob's Law of Internet User Experience" (video).
- Hoober, "How Do Users Really Hold Mobile Devices?", UXmatters 2013.
- SimpleLocalize, RTL design guide; Argos Multilingual, localisation planning guide.
