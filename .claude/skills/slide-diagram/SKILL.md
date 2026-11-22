---
name: slide-diagram
description: Choose, sketch, and build the diagram for a teaching slide (Slidev, Traditional Chinese). Covers the diagram styles available, how to pick one, drawing rules learned from reviewing Vibe Coding deck 01, and a gallery of finished examples with the corrections the instructor asked for.
---

# Slide Diagram Skill

## Purpose
Pick the diagram that fits the idea, draw it the way this instructor wants it drawn, and avoid the mistakes that were already corrected once. This skill is the practical companion to `visual-storytelling` (what a visual should teach) and `slide-design-system` (colors, type, readability rules). If they conflict with this file, `CLAUDE.md` wins, then `slide-design-system`.

Ported from the Vibe Coding with Python course (same instructor). The gallery in section 6 refers to that course's deck 01 (`C:\Users\lspss\Documents\Vibe_coding_python\01-ai-core-concepts`); open it there to copy a diagram. Add this course's diagrams to section 6b as the instructor approves them.

## When to use
Whenever a slide needs a diagram, flow, mock-up, or visual comparison, and whenever the instructor asks to "change the diagram", "make it look like this picture", or "use a real scenario instead of a table".

Reusable code lives in `snippets.md` next to this file. Decks must not import from each other: copy a snippet or component into the deck that needs it.

## Workflow
1. **State the teaching point**: "This diagram helps the learner see that ______." (from `visual-storytelling`).
2. **Choose a style** with the decision guide below. Prefer a realistic scenario over a table or a list of boxes.
3. **Sketch in words first** for non-trivial diagrams: list participants, the order of arrows, who owns each decision, and what the learner should notice. Check this against the verified facts (`technical-research-fact-checking`).
4. **Build** with the style's rules (section 4) and the shared color roles (section 5).
5. **Check** with the review list (section 8). Estimate the height before claiming it fits. Do not build or export unless the user asks (standing rule in this project); the dev server reloads on save.
6. **Iterate on feedback without changing structure**: when the user asks to change content ("change the prompts", "shorten the summary"), keep the layout and only edit the text.

## 1. Diagram styles you can choose from

| Style | Shows | Use when | Example in Vibe deck 01 |
|---|---|---|---|
| Flow / pipeline (left to right) | Steps in order | A process with one direction and ≤ 6 steps | Text completion rows; RAG offline and online rows |
| Two-way flow | Input one way, output the other way | Something is sent in and a result comes back | Tokenizer: encode left to right, decode right to left |
| Lanes with a loop | Who does what, repeated | A cycle in which several roles take turns | Agentic loop: user, Agent app, LLM |
| Sequence diagram | Messages between roles over time | "Who talks to whom, in what order" | Tool-call flow with 8 arrows |
| Container (cup) | Capacity and what fills it | Limits, budgets, memory, context | Context cup, compact vs clear |
| Mock UI window | What the user actually sees | Anything students will meet in a real app | Windows-style chat window; "Worked for 47s" log |
| Fan-out and fan-in | Work split, results merged | Parallel tasks, sub-agents | Three sub-agents returning summaries |
| Side-by-side comparison | Two designs or states | Before and after, with and without | MCP versus no MCP; vague versus precise prompt |
| Table or matrix | Many items, several attributes | Reference data, numbers, growth | N × N attention table; context-window limits with logos |
| File or code block | What a real file looks like | Config, rules files, prompts | Markdown AGENTS.md block |
| Layered stack | Nested or ordered layers | Parts that contain parts | Concept map of the whole chain |
| Timeline | Change over time | History, versions | "Where do large models come from" |
| Original figure | A published diagram | A paper's architecture, with attribution | Transformer figure from the arXiv source |

## 2. How to choose

Ask in this order and take the first match.

1. **Will students see this on a real screen?** Draw the real thing as a mock window (chat, terminal, file) rather than an abstract box. The instructor repeatedly replaced tables and box lists with realistic windows.
2. **Is it about who does what over time?** Use a sequence diagram (one-shot exchange) or lanes with a loop (repeated cycle). Never a plain list of steps.
3. **Is something filled up or limited?** Use the cup. Blocks inside must carry readable names, never ids or color codes.
4. **Is it a pipeline with one direction?** Flow nodes. If a result returns, use the two-way flow with arrows pointing the true direction.
5. **Is the point a difference?** Side by side, same frame on both sides, one changed element highlighted.
6. **Are there many parallel items?** Fan-out and fan-in with one real example per branch.
7. **Is it data to look up?** Table, with logos or icons when brands are named.
8. **Otherwise** write the concrete scenario first and draw only what the scenario needs.

Prefer a real scenario over an abstract one. Examples that worked: fixing `app.py`, the expense-tracker demo, planning an Okinawa trip with three sub-agents, reading a file as the example of a Tool, getting the weather as the example of an external service (MCP).

Keep one dominant visual per slide. If a slide needs a second diagram, a table, and a paragraph, split it or move the paragraph to speaker notes.

## 3. Content rules that come from the instructor's corrections

1. **Direction must match reality.** Input flows toward the model; output flows back. Draw both, with arrows pointing the true way. Put the user's window on the left and the model on the right.
2. **Name every box.** Show real names such as the previous conversation, the current prompt, the part being compacted. Never show ids, hex codes, or generic "block 1".
3. **Examples go inside the box they explain.** For encode and decode, the example and the one-sentence explanation sit in the box, not in a caption underneath.
4. **Show who decides.** If the model decides the next step or when to stop, the arrow belongs on the model's lane. The Agent app only executes and reports.
5. **Role colors are fixed across the deck** (section 5). Never recolor a role for decoration.
6. **Do not emphasize one concept in every slide** (Agent Skill was over-highlighted and removed). Use emphasis once, where it teaches.
7. **Terms must be accurate.** Token ID is an integer; the Token vector (embedding) is looked up from it. Tool is a general concept (any function a model can call), not only built-in functions. Do not blur these for visual simplicity.
8. **Remove what the slide does not need.** When a concept is not part of the example (for example MCP in the tool-call flow), leave it out. When the instructor says a topic is too big (RAG practice), cover only the main concept.
9. **Shorten.** Prompts and summaries inside diagrams should be keywords: "A 天氣：10/31 晴", not full sentences. Details go to speaker notes.
10. **Keep Traditional Chinese with Taiwan vocabulary**; keep standard English terms (Token, Prompt, Agent, MCP, API, tool names, product UI strings) in English.
11. **No video information on slides**: no source notes, timestamps, or creator names from reference videos. Cite official documentation instead; keep video notes in `research/sources.md` only.
12. **Real examples need honesty.** Label illustrative numbers as illustrative ("為示意"), label third-party figures, and keep source footers.

## 4. Drawing rules

### Layout
- Slidev canvas is about 980 × 552. Title block uses roughly 150 px, the footer source line about 30 px, so a diagram has at most about 330 px of height. Estimate before adding rows. Overflow happened on slides 8, 10, 13, 15, and 18.
- Prefer compact padding (`padding:4px 12px`), 14–16 px labels inside dense diagrams, and 18 px or larger for anything students must read from the back.
- Equalize widths so columns align (for example, all output boxes in a column share one width).
- Leave a gap between an object and the container it is not part of (the user's prompt sits outside the loop frame, not overlapping it).

### Arrows
- Marker size must not scale with stroke width: use `markerUnits="userSpaceOnUse"`. A thick line with a default marker produces a huge head.
- For a very thick emphasis arrow (such as "repeat"), draw the line and a separate `<polygon>` head with a visible gap or clean butt joint. Do not let the head overlap the label or the box.
- Give each marker a unique id per slide deck (ids are global in the page).
- Label non-obvious arrows. Put labels above the line with a white halo (`paint-order: stroke`, white stroke) so a lifeline never strikes through text.
- Emphasize at most two arrows per diagram (model-only action in blue, real execution in green).

### SVG in Slidev
- Text needs inline `style` for font family and size; class-based sizes are unreliable inside SVG.
- Keep text baselines inside the viewBox (labels at y < 12 get clipped).
- Use `role="img"` and an `aria-label` that describes the diagram in words.
- HTML tables need `<tbody>`. Markdown inside HTML needs blank lines around it.
- Deck-local Vue components live in `components/`. Do not let a style spread overwrite a prop (the cup once showed color codes because `{...block, ...tone}` overwrote `text`).
- Logos: use a local SVG in `public/` (for example from simple-icons), sized 22 px, with an `alt`.

## 5. Role colors and tokens
Use the design tokens in `style.css` (white background, no dark panels).

| Role | Color | Token |
|---|---|---|
| User, human, input | orange | `--warm-accent` `#b85c20`, fill `#fff2e3` |
| Agent app, platform, executor | green | `--secondary` `#16847a`, fill `#e7f5f2` |
| LLM, model | blue | `--primary` `#2457c5`, fill `#eaf1ff` |
| Neutral, tool, storage | gray | `#9aa5b4`, fill `#f5f7fa` or white |
| Emphasis line (repeat, key path) | near-black | `--text` `#172033` |

Context cup blocks: gray = rules and tool list, teal = history, blue = current prompt or file read, orange = output, dashed gray = ignored or discarded content.

## 6. Gallery: diagrams we built and what the instructor changed

Use these as starting points. "Corrections" are the changes the instructor asked for; apply them from the start next time.

**Agentic loop** (Agent chapter, slide 26)
- Final design: three horizontal lanes, user on top, Agent app in the middle, LLM at the bottom. Three phases run left to right (gather information, take action, verify). A large dashed frame marks the loop. A thick return arrow marks "repeat". The user's prompt sits left of the frame; "interrupt, add context, approve" is a dashed box above it. The done arrow leaves from the LLM lane.
- Corrections: layered vertically instead of one row; arrows between phases belong on the LLM lane because the LLM decides; note that the LLM decides when the loop ends after seeing the result; arrow line and head separated; prompt moved out of the frame and renamed "你的 Prompt"; boxes narrowed so spacing is even; lower boxes enlarged; explanation boxes removed; slide moved into the Agent chapter.

**Tokenizer** (slide 9)
- Final design: chat window on the left, LLM on the right. Encode arrow goes left to right; the LLM emits one Token ID and decode arrow returns right to left to the chat. Encode and decode boxes contain example and one-line explanation. Strong sentence: language does not matter, every Token maps to a Token vector, and closer meaning means closer vectors.
- Corrections: direction of output reversed; realistic window; examples moved into boxes; two-column explanation restored then removed; Token ID versus Token vector clarified.

**Context cup** (slides 12–19)
- Final design: open-top cup with stacked named blocks and the limit at the rim; narrow Windows-style chat window beside it. Reused for rules file, pointers, compact versus clear, notes file, sub-agents.
- Corrections: narrower conversation and larger context; names instead of ids; top open like a cup so more can be added; conversation inside a Windows-style window with bubbles on the right for the user.

**Context-window limits table** (slide 12)
- Final design: rows for Claude, OpenAI GPT-6, ChatGPT with logo, limit, and approximate English and Chinese length. Third-party figures labeled.
- Correction: add logos next to names; replace the list of techniques with real limits.

**Tool-call sequence** (slide 23)
- Final design: four lifelines (user, platform (Agent), model, tool), eight labeled arrows, blue for model output, green for real execution. Example: `read_file(app.py)`.
- Corrections: draw like a sequence diagram; rename Cline to 平台 (Agent); no MCP in this example; use file reading for Tool and the weather for MCP; Tool is a general term, not only built-in functions.

**Agent work log** (slide 25)
- Final design: Windows-style chat window, user bubble, expanded "Worked for 47s" with tool-loading and web-search lines, each with the model's thought, then the final answer.
- Correction: replace the table with a real conversation that shows the working phase.

**Sub-agents** (slide 18)
- Final design: main-agent cup on the left with named summary blocks; three sub-agent cups on the right, each with a task and a one-line return; why, when, how strip below; user's instruction box above.
- Corrections: one sub-agent became several with real tasks; the real Okinawa-trip session supplied the example; prompts and summaries cut to keywords ("A 天氣：10/31 晴"); layout kept when content changed.

**Text completion with a tool call** (slide 8)
- Final design: three completion rows plus a fourth row where the output is a tool call, with the output column the same width in every row.
- Corrections: add the tool-call output as a technical term (tool call, function calling); align it with the next-token column; compress vertical spacing.

**Rules file and pointers** (slides 13–14)
- Final design: a real Markdown block in the style of `claude.md` next to a named cup; pointer example with unused files dashed.
- Corrections: Markdown layout; every cup block named; file boxes kept inside the slide width; RAG merged into the pointer idea, then split back and trimmed to concepts.

**RAG** (slide 15)
- Final design: offline row (document, chunk, embed, vector store) and online row (question, retrieve, rerank, augment and generate).
- Correction: show how it works in detail; the practice slide was removed because RAG is its own topic.

**Attention and Transformer** (slides 6–7)
- Final design: original architecture figure with attribution beside a short explanation; an N × N attention table and a growth table showing the context limit.
- Correction: bring in the paper figure and connect the N × N table to the context-window limit.

## 6b. Gallery: diagrams in this course
(Empty. Add each diagram the instructor approves: deck, slide, final design, corrections.)

Role colors for model diagrams (extends section 5; keep consistent across decks):

| Role | Color |
|---|---|
| Data, real samples, user input | orange (`--warm-accent`) |
| Network being trained (encoder, generator, denoiser, LLM) | blue (`--primary`) |
| Loss, discriminator, critic, evaluation | green (`--secondary`) |
| Frozen parts, noise, storage | gray |

Tensor shapes go on arrows in monospace (`[B, 3, 32, 32]`).

## 7. Choosing between a table and a scenario
Tables are for reference data. If the content narrates a process (rounds, steps, turns), turn it into a scenario the student could see on a screen: a chat window with a log, a sequence of arrows, or real output. The instructor replaced the umbrella-round table and the six-step list this way.

## 8. Review checklist (before saying the slide is done)
- Can a student state the point of the diagram within five seconds?
- Do arrows point the way data really flows, and are the important ones labeled?
- Are all roles in their fixed colors? Is anything named with an id or code?
- Is any text clipped, crowded, or overlapping a frame or lifeline?
- Does the height fit (estimate) with the title and the source footer?
- Are terms accurate (Token ID versus vector, Tool as a general concept, who decides)?
- Are numbers either verified with a source or labeled as illustrative?
- Is the Traditional Chinese Taiwan-standard, and are English product terms kept?
- Did the change keep the existing layout when the request was only about content?
- Are outline, claim ledger, and notes updated if the slide's content or number changed?

Report what was checked statically and what still needs a visual check in the browser. Do not claim to have rendered or inspected the slide unless that actually happened.
