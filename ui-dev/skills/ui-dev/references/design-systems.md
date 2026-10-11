# Design systems

Read when the design read names a design system or an aesthetic family, or a new project needs a
foundation. Use the official package, and only when the brief needs that system; the existing stack
comes first. One system per project.

## A real design system

| Brief reads as | Reach for | Why |
|---|---|---|
| Microsoft, enterprise SaaS, dashboards | `@fluentui/react-components` or `@fluentui/web-components` | Official Fluent UI, with Microsoft's tokens and accessibility built in |
| Google-ish UI, Material-flavoured product | `@material/web` with Material 3 tokens | Official, themed through Material Theming |
| IBM-style B2B, enterprise analytics | `@carbon/react` and `@carbon/styles` | Official Carbon, mature data-density patterns |
| Shopify app surfaces | Polaris web components or Polaris React | Required for Shopify admin UI |
| Atlassian, Jira-style product | `@atlaskit/*` and `@atlaskit/tokens` | Official Atlassian design system |
| GitHub-style devtool or community page | `@primer/css` or `@primer/react-brand` | Official Primer; the Brand variant for marketing |
| UK public-sector service | `govuk-frontend` | Expected under the Service Standard |
| US public-sector, trust-first | `uswds` | Expected for US federal services |
| Fast local-business or agency MVP | Bootstrap 5.3 | Boring, fast and reliable |
| Modern accessible React foundation | `@radix-ui/themes` | Primitives with a polished theme |
| Modern SaaS where you own the components | shadcn/ui (`npx shadcn@latest add ...`) | You own the code and customise it; never ship the default state |
| Tailwind-based modern SaaS or AI marketing | Tailwind v4 utilities with the `dark:` variant | The default for indie and small-team builds |

## An aesthetic, not a system

None of these has an official package. Build in native CSS, Tailwind and a maintained component
library, and say in code comments which parts are borrowed inspiration.

| Aesthetic | Implementation |
|---|---|
| Glassmorphism, frosted glass | `backdrop-filter`, layered borders, highlight overlays |
| Bento, Apple-style tile grids | CSS Grid with mixed cell sizes |
| Brutalism | Native CSS, monospace, raw borders |
| Editorial, magazine | Serif type, asymmetric grid, generous whitespace |
| Dark tech, hacker | Mono with a neon accent, terminal motifs |
| Aurora, mesh gradients | SVG or layered radial gradients |
| Kinetic typography | Native CSS animations, scroll-driven animations, GSAP for pinned choreography |
| Apple Liquid Glass | Apple documents Liquid Glass for Apple platforms only. A web version is a glassmorphism approximation; label it as one in comments. |
