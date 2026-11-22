---
name: visual-storytelling
description: Translate abstract technical concepts into clear diagrams, comparisons, examples, and visual narratives for presentations and learning materials.
---

# Visual Storytelling Skill

## Purpose
Make complex concepts easier to reason about by choosing visuals that explain structure, change, contrast, or cause and effect. Visuals must teach; decoration is secondary.

## When to use
Use while planning or authoring technical slides, diagrams, educational explainers, and presentations.

## Core principle
Choose the visual form based on the idea being taught:
- Sequence or lifecycle → process diagram
- System parts and connections → architecture diagram
- Differences and boundaries → comparison table or side-by-side layout
- Repeated decisions → loop or state diagram
- Abstract concept → concrete example, analogy, or annotated illustration
- Quantitative evidence → chart with labeled axes and source
- Nested concepts → hierarchy or layered diagram

Do not force every concept into the same diagram style.

## Procedure

### 1. Identify the teaching point
Before selecting a visual, complete this sentence:
"This visual helps the learner see that ______."

If the sentence is vague, refine the point before designing.

### 2. Choose one primary visual
Select the simplest visual that conveys the intended relationship. A slide may include supporting labels or a small example, but should have one dominant visual focus.

### 3. Use a consistent visual vocabulary
- Use the same shape for the same kind of entity throughout a deck.
- Use arrows only for meaningful flow, direction, dependency, or feedback.
- Label the meaning of non-obvious arrows and connectors.
- Distinguish inputs, processing, outputs, and external systems consistently.
- Use color sparingly and consistently; never rely on color alone to communicate meaning.
- Include a legend when symbols or line styles could be ambiguous.

### 4. Make abstract concepts concrete
For each major concept, consider:
- A short, realistic scenario
- An annotated example
- A before/after comparison
- A simple analogy, with its limitations stated
- A step-by-step trace of what happens

Use a running example across the presentation when it helps connect concepts. In this course a good running example is one dataset carried through several models (for example the same small image set through AE → VAE → GAN → diffusion, so samples can be compared side by side).

Do not let an analogy replace the actual technical explanation. Explain where the analogy stops being accurate.

### 5. Apply to the generative-AI topics
Use visuals such as:
- Keras → PyTorch: the same training step side by side, line for line (`fit()` unrolled into forward, loss, backward, step)
- Probability, KL, MLE: two histograms/densities overlaid, with the gap shaded and a number computed on the slide
- AE / VAE: data → encoder → z (with shape) → decoder → reconstruction; VAE adds μ, σ and the sampling step (reparameterization drawn as an explicit side input ε)
- Latent space: a 2-D scatter of real encodings, with decoded images at chosen points (interpolation strip)
- GAN: generator and discriminator as two players with their losses; alternating update steps over time
- Diffusion: forward noising strip x₀ → x_T, reverse denoising strip, the network predicting ε at one step
- Conditioning: the same sampler with and without a label/text, and classifier-free guidance as two predictions combined
- Attention: query–key score table with real tokens, then the weighted sum; causal mask as a triangle
- LLM sampling: next-token probability bars, then the same bars after temperature / top-p
- LoRA: frozen W plus a thin A·B path, with parameter counts
- Quantization: the same weight tensor at fp16 vs 4-bit with memory numbers

Do not draw these as a mandatory universal architecture. Mark the deck's overall progression as a teaching sequence, not a strict dependency graph. Tool calling, MCP, RAG and agents belong to the Agent module; do not draw them here except as a one-line forward pointer.

### 6. Design presentation slides
- Use Slidev's default 16:9 canvas (same as the Vibe Coding decks).
- Give each slide one principal takeaway.
- Prefer concise labels over paragraphs embedded in diagrams.
- Use readable type at presentation size and adequate whitespace.
- Keep diagram complexity low; split a diagram when labels or crossings become hard to follow.
- Avoid stock imagery when a diagram would explain the idea better.
- Use images only when they add meaning, context, or engagement.

### 7. Implement with Slidev
When Slidev is the target:
- Prefer Markdown, native layouts, Vue components, and Mermaid for suitable diagrams.
- Use code fences and supported syntax; check against the installed Slidev version.
- Keep reusable visual components in `components/` when they improve consistency.
- Ensure diagrams fit the slide viewport and remain legible when rendered.
- Avoid external assets that may fail offline unless there is a clear reason to use them.
- Do not embed large, uneditable screenshots of diagrams when a native diagram is practical.

### 8. Review the rendered visuals
Inspect every rendered slide:
- Is the main point obvious within a few seconds?
- Is the visual accurate and consistent with the verified technical explanation?
- Are text, arrows, labels, and legends readable?
- Does the eye know where to look first?
- Is anything clipped, crowded, redundant, or decorative?
- Does the slide connect naturally to the previous and next slide?

Revise visuals that fail these checks.

## Output
For each planned slide, specify:
- Main takeaway
- Visual type
- Essential labels and relationships
- Example or annotation
- Accessibility or readability considerations

During final QA, report any slide whose visual meaning remains ambiguous.

## Rules
- Never sacrifice technical accuracy for visual simplicity.
- Do not use arrows to imply a dependency that does not exist.
- Do not use decorative imagery as a substitute for an explanation.
- Do not overload one slide with an entire system architecture and all its details.
- Use charts only when there is meaningful data to represent.
