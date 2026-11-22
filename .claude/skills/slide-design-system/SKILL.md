---
name: slide-design-system
description: Enforce a consistent, screen-readable visual system for technical teaching slides, inspired by clean, modern explainer videos: strong hierarchy, purposeful color, clear diagrams, and white as the default background.
---

# Slide Design System

## Purpose

Apply a consistent visual system across an instructional slide deck. The target is a clean, modern technical-explainer aesthetic similar to the referenced video: concise titles, clear conceptual diagrams, restrained color accents, and strong visual hierarchy. Do **not** copy exact frames, branding, or proprietary assets from the video. Translate its general visual language into an original Slidev theme that reads well on screen.

The deck is projected in class and read by students on their own screens (the student site). **Nothing is printed**, so readability on a projector and on a laptop is the first-class requirement.

## Design principles

1. **White by default:** Use white (`#FFFFFF`) as the default slide background, which also keeps new slides consistent with the existing decks. Near-white (`#FAFAF8`) is acceptable for section dividers.
2. **Richer visuals when they teach:** Large color panels, dark panels and dark code blocks are allowed when they direct attention or separate ideas. Text on them must keep strong contrast. Avoid decorative gradients and color that carries no meaning.
3. **Strong hierarchy:** Every slide has one clear headline, a small number of supporting points, and one primary visual or worked example.
4. **Color has meaning:** Use accent colors consistently to encode roles in diagrams; do not add colors only for decoration.
5. **Readable on screen:** Keep high contrast and sufficient font size for the back of the room, and do not rely on color alone (color-blind students must still follow the diagram).
6. **Explain, do not decorate:** Every shape, icon, arrow, label, and highlight must help explain the content.

## Visual direction

Use a restrained, modern technical-lecture style:

- White canvas with generous whitespace.
- Near-black headings and body text.
- One strong blue as the primary accent, with a small number of secondary accents.
- Thin borders, simple rounded rectangles, clean arrows, and minimal line icons.
- Flat diagrams rather than glossy 3D, skeuomorphic controls, or decorative illustrations.
- Occasional small section labels or eyebrow text, but no persistent oversized branding.
- Use a consistent layout grid and align titles, text blocks, and diagrams.
- Prefer editable SVG, Mermaid, HTML/CSS, or native Slidev/Vue elements over screenshots of diagrams.

This is an original interpretation of a clean explainer-video style, not a frame-by-frame reproduction.

## Color tokens

Use these defaults unless the subject requires an accessible alternative:

| Token | Hex | Intended use |
|---|---|---|
| `--slide-bg` | `#FFFFFF` | Main background |
| `--surface` | `#F5F7FA` | Light grouping areas |
| `--text` | `#172033` | Main text |
| `--muted-text` | `#4B5563` | Secondary text; must remain legible on a projector |
| `--border` | `#D7DEE8` | Dividers, card outlines, diagram boundaries |
| `--primary` | `#2457C5` | Main emphasis, active process, key concept |
| `--secondary` | `#16847A` | Supporting process or data flow |
| `--warm-accent` | `#B85C20` | Caution, contrast, exception |
| `--soft-blue` | `#EAF1FF` | Light highlight or panel background |
| `--soft-teal` | `#E7F5F2` | Light highlight or panel background |
| `--soft-amber` | `#FFF2E3` | Light highlight or panel background |

Rules:
- Use the primary accent for the main idea, not every heading.
- Use secondary colors only when they encode a different role.
- Keep text dark on light tints and light on dark panels.
- Avoid low-contrast pastel text and pure-color body text.
- Check that the diagram still works without relying on color alone. Use labels, line styles, shapes, and arrow direction in addition to color.

## Typography

Use a sans-serif font with broad language coverage and robust PDF rendering. Prefer fonts already available in the Slidev environment; do not depend on an external font download at build time.

Recommended stack:
- Latin: `Inter`, `Arial`, `Helvetica`, sans-serif.
- Chinese: `Noto Sans TC`, `Microsoft JhengHei`, `PingFang TC`, sans-serif.
- Monospace/code: `JetBrains Mono`, `Consolas`, monospace.

Use CSS fallbacks and test the actual rendered deck. If a font is missing, choose a reliable local fallback rather than leaving text dependent on a network resource.

### Font-size targets for 16:9 slides

The Vibe Coding decks use Slidev's default 16:9 canvas (980×552 logical); this course does the same. The 4:3 `艾鍗PPT版型2019-IT.pptx` template is not used for Slidev decks.

These are targets, not permission to squeeze content:

- Slide title: `30–36 px` (roughly 24–27 pt at typical 16:9 rendering).
- Section title: `36–44 px`.
- Main body: `20–24 px`.
- Diagram labels: `17–21 px`.
- Captions and source notes: `12–14 px`; avoid going below `12 px`.
- Code: `16–20 px`, with short examples only.
- Math (KaTeX, `$...$` / `$$...$$`): at least body size; one equation per line; every symbol named in words nearby.

Aim toward the upper end of body and label sizes so the back of a classroom can read them. Do not shrink text to fit an overloaded slide. Split the slide or simplify the content instead.

### Text hierarchy and density

- One key message per slide.
- Prefer a short, claim-like title over a generic label. Example: “An agent repeats the loop: plan → act → observe” rather than “Agent”.
- Normally use no more than 3–5 short bullets, each preferably one line.
- Keep paragraphs rare; use short statements, labeled diagrams, or a worked example.
- Highlight one or two terms, not whole paragraphs.
- Bold for emphasis; avoid underlining as a general design device.
- Do not use all caps for long labels.
- Do not put essential information only in a tiny footnote.
- If a slide contains more than one major idea, split it unless it is a purposeful comparison or summary.

## Layout system

Use a consistent 16:9 canvas and a stable grid.

- Keep a safe margin of approximately 5–7% of slide width on all sides.
- Align titles to a consistent left edge unless the slide type deliberately uses a centered opening title.
- Keep title and content spacing consistent.
- Use two-column layouts only when the relationship is meaningful, such as “concept / example” or “before / after”.
- Prefer one large central diagram over several small unrelated diagrams.
- Use whitespace to separate groups instead of thick colored bars.
- Avoid unnecessary card grids. Use outlined groups only when boundaries represent a real conceptual grouping.
- Keep source notes in a consistent footer area; make them readable, but visually secondary.
- Do not place important text close to slide edges, in slide numbers, or behind decorative shapes.

## Diagram and visual rules

Choose a visual form based on the relationship being taught:

- Sequence or pipeline → left-to-right flow with labeled arrows.
- Feedback or agent loop → loop diagram with explicit “observe / decide / act” labels.
- Architecture → labeled components and data-flow arrows.
- Comparison → aligned columns or a compact table.
- Hierarchy → nested layers or a tree.
- Abstract concept → concrete example plus a restrained analogy.
- Quantitative evidence → chart with units, source, and legible axis labels.

Diagram requirements:
- Label important arrows when the type of flow matters.
- Avoid crossing connectors where possible.
- Keep label text short and large enough to read on a projector.
- Use shape, label, and position as well as color to communicate meaning.
- Use consistent visual grammar: the same concept should look the same throughout the deck.
- Avoid gradients, glow, shadows, complex textures, decorative 3D, and tiny icons.
- Do not use screenshots of text-heavy diagrams if an editable diagram can be made.
- Ensure diagrams still make sense without color vision.

## Slidev implementation guidance

When authoring Slidev slides:

- Define a small set of reusable CSS variables and component styles in the theme or `style` block.
- Prefer CSS variables for colors, spacing, border, and typography so the deck can be updated consistently.
- Use native Slidev layouts and simple HTML/Vue elements where that improves alignment.
- Mermaid is acceptable for quick diagrams, but inspect the rendered result for small labels, awkward line breaks, and theme inconsistencies. Use custom SVG or Vue/CSS if Mermaid cannot meet the readability standard.
- Avoid remote assets, external fonts, or image URLs that may fail during offline rendering or PDF export.
- Prefer light fills and thin outlines in diagrams; use a dark or strongly colored panel only when it helps the reader, not merely to look “technical”.
- Code examples may use a light or dark background; keep strong contrast and match the other code blocks in the same deck.
- Keep important information as selectable text when possible, so students can copy it from the student site.

### Starter CSS

Adapt to the existing Slidev project rather than blindly replacing its theme. If a compatible theme already exists, preserve it and merge these tokens.

```css
:root {
  --slide-bg: #ffffff;
  --surface: #f5f7fa;
  --text: #172033;
  --muted-text: #4b5563;
  --border: #d7dee8;
  --primary: #2457c5;
  --secondary: #16847a;
  --warm-accent: #b85c20;
  --soft-blue: #eaf1ff;
  --soft-teal: #e7f5f2;
  --soft-amber: #fff2e3;
}

.slidev-layout {
  background: var(--slide-bg);
  color: var(--text);
  font-family: Inter, "Noto Sans TC", "Microsoft JhengHei", Arial, sans-serif;
}

h1, h2, h3 {
  color: var(--text);
  letter-spacing: -0.02em;
  line-height: 1.2;
}

p, li {
  color: var(--text);
  line-height: 1.45;
}

.caption, .source-note {
  color: var(--muted-text);
  font-size: 12px;
}

.diagram-node {
  border: 1px solid var(--border);
  border-radius: 10px;
  background: #ffffff;
  padding: 0.65em 0.85em;
}

.diagram-node--primary {
  border-color: var(--primary);
  background: var(--soft-blue);
}

.diagram-node--secondary {
  border-color: var(--secondary);
  background: var(--soft-teal);
}
```

## Render and export requirements

Before considering the deck complete:

1. Render the slides and inspect the whole deck, not only the source Markdown.
2. Export a PDF if the environment supports it (an internal check, not a student copy); check for clipping, font substitution, missing glyphs, and broken diagrams.
3. Check at least one representative slide at 100% zoom on a laptop-sized window.
4. Confirm that all body text, diagram labels, code, and source notes remain legible.
5. Check that hierarchy and meaning do not depend on color alone.
6. Check every slide for overflow, collisions, and content too close to the edges.
7. Do not claim visual validation unless the rendered output was actually inspected.

## Final review checklist

- [ ] White background on standard content slides.
- [ ] Any large color or dark panel has a teaching purpose and strong text contrast; no decorative gradients.
- [ ] Consistent title placement, font family, spacing, and accent usage.
- [ ] One key message per slide.
- [ ] Text is concise and readable on a projector and a laptop.
- [ ] Diagram arrows, labels, and groups are clear without relying on color alone.
- [ ] Colors encode meaning rather than decoration.
- [ ] Source notes are present where claims require sourcing.
- [ ] No remote asset or font dependency that could break rendering.
- [ ] Rendered slides were inspected before delivery.

## Output behavior

When starting a new deck, state the design tokens and layout rules briefly, then apply them consistently. If the user provides a reference video or deck, use it to infer broad design traits but do not invent exact color values or claim pixel-level matching without examining the reference visuals. Prioritize legibility over dramatic screen effects.
