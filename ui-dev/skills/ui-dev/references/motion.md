# Scroll storytelling

Read when a persuade or experience direction carries narrative motion: a section that pins while a
scene advances, or a horizontal pan. Curves, durations and springs come from `animate`.

## Before building

Describe the trigger, the moving subject, the start, middle and end states, what happens on
interruption and reversal, the responsive geometry, and the reduced-motion alternative. A storyboard
at 0, 25, 50 and 100 percent is usually enough; a runnable prototype only when behaviour cannot be
judged from it. Record what was observed running; a static screen or a click-through does not show
scroll-linked motion.

## Principles

- Normal document scrolling. Native sticky positioning holds a scene while its container's scroll distance advances the animation, and the container ends naturally so following content stays reachable. Keyboard, touch, wheel and scrollbar all keep working.
- Geometry comes from the actual containers, refreshed after resize or asset layout, with function-based dimensions and cleanup of every listener and trigger.
- The base content reads if enhancement fails. Reduced motion removes travel, parallax and pinning while keeping the content and the useful state changes.
- A travelling subject may follow a different path on desktop and mobile while keeping its narrative.
- `transform` and `opacity` where they achieve the effect; blur, large filters and canvas work need measured justification on target devices. Never the same entrance on every section, and essential content never waits for an animation.
- Split display text keeps its reading order and copy for assistive technology; animated spans never duplicate screen-reader content. A price, date or other authoritative number is never counted up from zero for decoration.
- Navigation stays interruptible and reflects real completion, never a fixed timeout; a failed animation never strands the person behind an overlay.
- A supplied logo is translated along a path, never deformed or redrawn; a decision on altering a mark comes from brands.md.

## Sticky stack

```tsx
"use client";
import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "motion/react";

gsap.registerPlugin(ScrollTrigger);

export function StickyStack({ cards }: { cards: React.ReactNode[] }) {
  const ref = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();

  useEffect(() => {
    if (reduce || !ref.current) return;
    const ctx = gsap.context(() => {
      const cardEls = gsap.utils.toArray<HTMLElement>(".stack-card");
      cardEls.forEach((card, i) => {
        if (i === cardEls.length - 1) return;
        ScrollTrigger.create({
          trigger: card,
          start: "top top",                              // pin at viewport top
          endTrigger: cardEls[cardEls.length - 1],
          end: "top top",
          pin: true,
          pinSpacing: false,
        });
        gsap.to(card, {
          scale: 0.92,
          opacity: 0.55,
          ease: "none",
          scrollTrigger: {
            trigger: cardEls[i + 1],
            start: "top bottom",
            end: "top top",
            scrub: true,
          },
        });
      });
    }, ref);
    return () => ctx.revert();
  }, [reduce]);

  return (
    <div ref={ref} className="relative">
      {cards.map((card, i) => (
        <div
          key={i}
          className="stack-card min-h-[100dvh] flex items-center justify-center"
        >
          {card}
        </div>
      ))}
    </div>
  );
}
```

The scale and opacity transform is driven by the next card's trigger, so the previous card shrinks as the next arrives.

## Horizontal pan

```tsx
"use client";
import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "motion/react";

gsap.registerPlugin(ScrollTrigger);

export function HorizontalPan({ children }: { children: React.ReactNode }) {
  const wrap = useRef<HTMLDivElement>(null);
  const track = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();

  useEffect(() => {
    const root = wrap.current;
    const trackElement = track.current;
    if (reduce || !root || !trackElement) return;

    root.classList.add("is-enhanced");
    try {
      const ctx = gsap.context(() => {
        const distance = (): number => Math.max(0, trackElement.scrollWidth - root.clientWidth);
        gsap.to(trackElement, {
          x: () => -distance(),
          ease: "none",
          scrollTrigger: {
            trigger: root,
            start: "top top",                            // pin starts when section top hits viewport top
            end: () => `+=${Math.max(1, distance())}`,   // recompute when ScrollTrigger refreshes
            pin: true,
            scrub: 1,
            invalidateOnRefresh: true,
          },
        });
      }, root);
      ScrollTrigger.refresh();
      return () => {
        ctx.revert();
        root.classList.remove("is-enhanced");
      };
    } catch (error) {
      root.classList.remove("is-enhanced");
      throw error;
    }
  }, [reduce]);

  return (
    <section
      ref={wrap}
      className="relative [&.is-enhanced]:overflow-hidden [&.is-enhanced_.horizontal-pan-track]:flex [&.is-enhanced_.horizontal-pan-track]:h-[100dvh] [&.is-enhanced_.horizontal-pan-track]:items-center"
    >
      <div ref={track} className="horizontal-pan-track grid">
        {children}
      </div>
    </section>
  );
}
```

The wrapper is pinned and the inner track slides horizontally as the person scrolls vertically; the scroll length equals the horizontal travel.

## Scroll mechanics

- A scroll listener on `window` runs on every frame with no batching; scroll progress lives in Motion's `useScroll()`, GSAP's `ScrollTrigger`, an IntersectionObserver, or CSS scroll-driven animations (`animation-timeline: view()`).
- Scroll progress and pointer position never live in React state, which re-renders the tree on every frame; they live in motion values (`useMotionValue`, `useTransform`), and a `requestAnimationFrame` loop never writes state either.

