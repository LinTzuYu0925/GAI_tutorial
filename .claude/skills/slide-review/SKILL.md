---
name: slide-review
description: Pass/fail rubric for judging whether a teaching slide, practice page, lab or whole Slidev deck of the 生成式AI原理 course is "good" for its trainees. Use when reviewing or self-checking any deck, and as the standard a reviewer agent or a /goal completion check must apply. Anchored on golden-example.md.
---

# Slide Review Skill

Defines "a good teaching slide" for this course so a reviewer (you, a subagent, or a goal checker) can judge it without guessing. The standard is **written down here and in `golden-example.md` (in this skill's folder, next to this file)**; when they disagree with your taste, they win.

Ported from the Vibe Coding with Python course (`C:\Users\lspss\Documents\Vibe_coding_python`), whose instructor and students are the same program. The golden examples come from that course's Python decks: copy their *patterns* (metaphor, before/after, Chinese reading of code, guided lab), not their content.

Related skills: `slide-design-system` (visuals), `slide-diagram` (drawing), `demo-and-practice` (practice pages and Colab labs), `instructional-design` (sequence), `technical-research-fact-checking` (claims), `slide-order-sync` (order). This skill does not repeat their details; it says how to *judge* against them.

## 0. The one test
For every slide ask: **"Could a trainee who has trained a Keras CNN but never seen this topic say this slide's single takeaway in one sentence after 30 seconds?"** If not, it fails, whatever else it does well.

## 1. How to review
1. Read `golden-example.md`, the deck's `outline.md`, `slides.md`, and (if available) rendered PNGs from `npm run export:png` in `dist/png/`. Looking at the render is required for rules R-V*; do not claim visual checks from source alone.
2. Judge **every slide** against sections 2-6. Mark each rule PASS / FAIL / N/A. Slides marked ★ must have zero FAIL; ○ and △ may carry FAILs of severity "minor" only.
3. Severity: **blocker** (wrong fact or wrong math, fabricated output, Simplified Chinese, overflow/cut-off, unexplained jargon on a ★ slide, lab that does not run on a Colab T4, practice with no way to check) / **major** (two ideas on one slide, no concrete example, diagram contradicts code, formula with no plain reading) / **minor** (spacing, wording polish).
4. Do not rewrite slides unless asked. Report; the author fixes; re-review. Max 3 rounds, then list what remains.
5. End with a summary line exactly in this form so a completion check can read it:
   `REVIEW <deck>: <n> FAIL (<b> blocker, <m> major, <i> minor) / <N> slides, ★ slides with FAIL: <list or none>`

## 2. Content rules (R-C)
- **R-C1 One idea.** One takeaway per slide; a `.takeaway` line (or equivalent) states it. A purposeful comparison/summary may hold several items.
- **R-C2 Problem first.** The concept appears because a generation task needs it (for example "the AE's samples are blurry → why? → KL / VAE"), not as a list of definitions. The slide or its neighbor shows the need before the mechanism.
- **R-C3 Concrete before abstract.** A visible example (a real image grid, a real token sequence, real tensor shapes, a number computed by hand) precedes the general formula. Same numbers and names run through the figure, the code and the takeaway (golden examples 1, 2, 4).
- **R-C4 Say it in Chinese.** Every formula, operator or line of code shown has a plain Traditional-Chinese reading next to it (KL 讀作「用 q 去近似 p 要多付出的代價」; `loss.backward()` 讀作「算出每個參數該往哪裡調」). Not only in speaker notes (golden example 4).
- **R-C5 Name the misconception.** Where trainees predictably go wrong (Keras `fit()` hides the loop; `model.eval()` forgotten; the latent is not the image; GAN loss going down ≠ better images; diffusion predicts noise, not the image), the slide states it; the speaker note says how to teach it (golden example 2).
- **R-C6 Minimal scope.** Only the math and API the slide needs; the outline's 「不教」 list and the CLAUDE.md out-of-scope list (tool calling, MCP, RAG, CoT/ToT, multi-agent → Agent module) are respected.
- **R-C7 Loop visible.** Labs follow Specify → Generate → Execute → Audit → Iterate where an AI coding agent is used (the agent writes the scaffold, the trainee audits shapes, math and outputs). Verification (predict a shape or a number, run, compare, edge cases, look at the samples) is taught, not just running cells.
- **R-C8 Honest output.** Every shown output, loss curve, image grid, VRAM number, timing and Traceback was actually produced, on a stated runtime (for example "Colab T4，torch 2.x，實測"), and is reproducible from `materials/`. Fabricated or "typical" output = blocker. Images or screenshots not yet produced must be `.placeholder` and listed for the instructor.
- **R-C9 Facts.** Claims about models, papers, library APIs, versions, licenses, Colab limits are in `research/sources.md` with a source; unverified ones are marked 「待確認」 and not stated as certain. Paper results are attributed to the paper.
- **R-C10 Agent-output slides** separate prompt / generated code / observed result / verification (CLAUDE.md). A fallback exists when there is no AI quota or no GPU (a finished notebook in `materials/`, or saved outputs).
- **R-C11 Bridges, not repeats.** Material the DL course already taught (CNN, backprop, softmax, transfer learning; see `planning/curriculum-analysis.md`) is recalled in one line with a citation, not re-taught. Gaps it did not teach (RNN/attention bridge, probability/KL/MLE/ELBO, PyTorch) get a full explanation.

## 3. Language rules (R-L)
- **R-L1 Traditional Chinese only** for student-facing text, Taiwan vocabulary (程式 / 資料 / 函式 / 變數 / 執行 / 預設 / 參數 / 模型 / 訓練…). Zero Simplified characters or Mainland terms (scan with `python -X utf8 scripts/scan-zh.py <deck>`).
- **R-L2 Gloss new terms only.** An English technical term gets its Traditional-Chinese gloss in parentheses on the slide where it is *new to the students*. Do not require a gloss for a term in the **familiar list** (3b) or already glossed on an earlier slide or in an earlier deck's `NOTES.md` glossary. Never gloss file names, commands, code, model names or quoted paper titles. If a new term cannot take a gloss on its first slide (narrow chip, SVG label), use its next occurrence; if none fits, report slide + term to the instructor.

### 3b. Familiar terms (no gloss needed)
- From Vibe Coding (same program, decks 01-14, see that repo's `NOTES.md` glossaries): LLM, Token, Tokenizer, Token ID, Context, Context Window, Prompt, System Prompt, User Prompt, Tool, tool call, MCP, Agent, Skill, Vibe Coding, Specify / Generate / Execute / Audit / Iterate, diff, terminal, package, environment, Python keywords, NumPy, pandas, matplotlib, shape, dtype, tensor, JSON, API, `.env`, Git, commit; product names Claude, Claude Code, Codex, ChatGPT, VS Code, Colab.
- From the ML and DL courses (see `planning/curriculum-analysis.md` §prerequisites): model, training, loss, MSE, cross-entropy, softmax, sigmoid, optimizer, SGD, Adam, learning rate, epoch, batch, overfitting, dropout, CNN, pooling, BatchNorm, ResNet, skip connection, transfer learning, pretrained model, fine-tuning, distillation, GPU, Keras, layer, accuracy, precision/recall.
- Terms glossed in an earlier deck of *this* course join the list for later decks (read their `NOTES.md` glossaries before judging).

- **R-L3 Consistent wording** of a term across the deck and with the glossary in `NOTES.md` (for example always 潛在空間 for latent space, 去噪 for denoising).
- **R-L4 Jargon defined** the first time it is used in the deck. Math symbols are jargon: every symbol (z, x̂, μ, σ, β_t, ε_θ) is named in words on the slide where it first appears.

## 4. Visual rules (R-V) — check on the render
- **R-V1 Fits the canvas** (Slidev default 16:9, 980×552 logical, exported 1280×720 / 1920×1080). No overflow, clipped text, overlapping labels, or content touching edges.
- **R-V2 Screen-readable.** White is the default background; a large color or dark panel is fine if it has a teaching purpose. Strong contrast; meaning does not rely on color alone.
- **R-V3 Size.** Body ≥ ~20px, diagram labels ≥ ~17px, code ≥ ~16px, nothing essential below 12px. Fix by splitting the slide, never by shrinking.
- **R-V4 Density.** About 3-5 short bullets at most; no wall of text; no derivation longer than ~4 lines on one slide (split it, golden example 2's before/during/after style).
- **R-V5 Tokens.** Colors via CSS variables from `style.css` (gray `#b8b8b8` and white excepted); same role = same color across the deck.
- **R-V6 Diagram teaches.** Shows the *mechanism/change* (input → encoder → z → decoder → output, x₀ → noise → x_T and back), with tensor shapes on the arrows where shape matters; every shape/arrow has a label or purpose; one reading path (`slide-diagram` rules; SVG font sizes via `style="font-size:..px"`; unique `<marker>` ids).
- **R-V7 Code slide.** Smallest meaningful excerpt (≤ ~15 lines), relevant lines highlighted, expected output or shape shown, readable size. Full code lives in the notebook, not on the slide.
- **R-V8 Consistent chrome.** Eyebrow `NN · 小節`, title style, takeaway and `.src` placement follow earlier decks.
- **R-V9 Generated images** shown as evidence (samples, before/after LoRA) are real outputs from the lab, with seed and step count in the caption.

## 5. Practice, demo and lab pages (R-P)
- **R-P1 Individual, low typing, typed blanks.** No pairs/games; mostly predict-run-compare, short typed answers. Every blank on the slide is a working `FillIn` input with a `FillClear` line after the table (`demo-and-practice` §3). Not collected.
- **R-P2 Worked example first.** A 「照著做」 demo with a *different* item than the practice (golden example 3), covering which notebook cell, what to change, where output appears.
- **R-P3 Discovery.** The student finds something the slide does not already say (otherwise make it a demo).
- **R-P4 Answers.** If there is a checkable answer, a `hostOnly: true` answer page follows with the same layout and one line of how to tell. Answer numbers come from a real run.
- **R-P5 Fits Colab free tier.** Each lab runs on a Colab T4 (16 GB) in a free session: stated VRAM peak and wall time, small models, fp16/4-bit where needed, no step over ~10 minutes of waiting without something to look at. A practice inside a lab takes ~10-15 minutes.
- **R-P6 Guided lab sequence** (golden example 5, adapted in `demo-and-practice` §3c): goal → Specify → Generate/Execute → Audit/Iterate → independent extension → hostOnly answer; each page = numbered steps, one-line "why", expected shape/number/image; acceptance criteria written *before* running.
- **R-P7 Notebook and data students can find.** Each lab's notebook is a `materials/<file>.ipynb` citation with an "Open in Colab" path, and any dataset or checkpoint it needs is downloadable from inside the notebook (HF Hub, torchvision) or from `materials/`. Severity: major; blocker if the notebook or its data do not exist or do not run.

## 6. Deck-level rules (R-D)
- **R-D1 Structure.** Slides follow the approved `outline.md` (from the slide plan in `planning/`); every slide has ★/○/△ in its speaker note; summary and quick check (隨堂檢核) exist, and every multiple-choice question is a clickable `<Mcq>` with a `why` line for each wrong option and an `explain` (`demo-and-practice` §3e; plain-text `A.… B.…` options fail, severity major); next-unit preview exists and is `hostOnly: true`.
- **R-D2 Continuity.** Builds on earlier decks' code (the PyTorch training loop from the bridge deck is reused, not rewritten) and does not re-teach earlier explanations.
- **R-D3 Time.** Total estimate recorded in `teaching-plan.md` (all slides vs ★ only) against the block's budget in the slide plan.
- **R-D4 Build checks run.** `npm run build` ok, QA PDF exported, page count equals slides minus hostOnly, `check-order.cjs` consistent, `scan-zh.py` clean, every lab notebook run top to bottom on Colab T4 (record date and versions in `research/`). Say which were actually run.
- **R-D5 Notes.** Every slide has speaker notes in Traditional Chinese: teaching action, how to say it, known pitfalls.
- **R-D6 Assessment link.** Decks covering GAN and diffusion contribute to the 學習評量 (explain Diffusion vs GAN; implement conditional generation); the deck says where.

## 7. Gold standards
Judge by comparison with `golden-example.md`. When the instructor says a page of *this* course is easy for students to understand, add it to that file, then add a row here:
| Pattern | Golden example | What "good" looks like |
|---|---|---|
| Concept with a physical metaphor + before/during/after | 1 (box with label), 2 (`x = x + 1`) | same object repeated, old value struck out, arrow shows the action, numbered captions, code + takeaway use the same numbers |
| Reading code or a formula aloud | 4 (`and/or/not`) | each symbol has a Chinese spoken form; example in life language; reasoning arrow shown; bridged to the real lab line |
| Practice page | 3 | different-topic worked example above, 3 numbered steps, grey hints, short answers typed into input cells |
| Guided lab | 5, 6 | goal and data first, split into parts, Specify with 【目標】【輸入與輸出】【限制】【驗收】, then generate, run, audit |

## 8. Anti-examples (automatic FAIL)
- A slide of formulas with no example numbers and no Chinese reading (R-C3, R-C4).
- A slide that re-explains what an AE or a CNN is from scratch (R-C11).
- An image grid, loss curve or VRAM number from memory, a paper figure presented as our result, or "typical" output (R-C8, blocker).
- A diagram that only decorates or needs color to be understood (R-V2, R-V6).
- A practice whose answer is already on the slide, or that asks for paragraphs (R-P1, R-P3).
- A lab that needs an A100, a paid API key with no free fallback, or more than a free Colab session (R-P5).
- Text shrunk below ~16px to fit (R-V3); an English term used with no gloss on a ★ slide (R-L2).
- Claiming a deck was rendered or a notebook was run when only the source was read.

## 9. Report format
Per slide: `#<n> <title> [★/○/△]: PASS` or `FAIL R-xx (severity): what is wrong -> suggested fix`. Then the summary line from section 1. Keep it short; do not praise passing slides.
