# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

This repo holds course material for the 48hr **生成式AI原理** module of an 產業新尖兵 program that trains "AI 代理人與自動化工程師" in three months. The audience is career-switching trainees who already took Python (Vibe Coding), ML (sklearn) and DL (TF/Keras). The goal is a working engineer, so **every concept is paired with a hands-on lab**; theory alone is not enough.

There is no test suite. Slides are Slidev decks in an npm workspace (see **Slides** below); labs are Colab notebooks inside each deck's `materials/`.

## Workflow: three phases, done in order

Don't skip ahead. Check which phase the work is in before producing anything.

1. **Scope: what is in and out of the course.** Done in [planning/curriculum-analysis.md](planning/curriculum-analysis.md).
   - It defines key points K1–K10 and maps them to the official syllabus items #1–#14.
   - For each key point it marks what earlier courses taught (✅ taught, 🔹 concept-level only, ❌ not taught), with deck and page citations.
   - It also lists prerequisite gaps and open items.
   - K1–K10 are **knowledge areas, not a teaching order**.
2. **Slide plan: a thorough plan of every slide and what it covers.** It has two steps, both in `planning/`:
   - **Step 1 (draft, awaiting approval):** [planning/course_roadmap.md](planning/course_roadmap.md). It fixes the teaching order: 6 days × 4 sessions of 2h, each session opening with a business ticket.
     - The survey behind it is in [planning/research/university-survey.md](planning/research/university-survey.md).
   - **Step 2 (after the roadmap is approved):** `planning/slide-plan/D1…D6.md`. It lists slides one by one, with the lab or homework attached to each block.
     - Use the template in roadmap §15.
3. **Production: slides, practice homework, and labs.** Only after the plan is approved.

## Confirmed decisions (don't re-litigate)

- **Business problem first** (decided 2026-11-22). Every session opens with a ticket from one department of a single fictional Taiwanese consumer-electronics and lifestyle company.
  - The company name is a placeholder; slides mark the company 虛構.
  - The session then introduces the tools that solve the ticket, using the loop Frame → Try → Open → Adapt → Measure → Ship.
  - Don't open a block with theory.
- **LLMs are taught on Day 5** (decided 2026-11-22), just before the Agent module. Day 1's GenAI tour gives an early taste.
- **Labs use PyTorch + Hugging Face** (`transformers`, `diffusers`, `peft`, `trl`). This differs from the Keras used in the DL course and the 2024 deck.
  - Students know only Keras, so the course opens with a ~2hr **Keras→PyTorch bridge**.
  - The bridge re-implements a notebook every student has run: the DL course's LabDay3-2 CIFAR-10 CNN.
  - Open item: confirm with 艾鍗 that TF isn't mandated program-wide.
- **Compute is Google Colab, T4 (16GB).** Every lab must fit T4 VRAM and a free-tier session (use small models, fp16/4-bit, SD1.5/SDXL-Turbo class).
- **GAI runs before the Agent module.**
  - GAI teaches basic LLM SDK calls, local and quantized models, and JSON output (K6).
  - Tool calling, MCP, RAG, CoT/ToT and multi-agent belong to the Agent module and are out of scope here.
- **Avoid repeats from the DL course.** It already introduced AE, U-Net, VAE, GAN, diffusion and GPT at concept level (DL deck pp.72–87), but never in code. Skip "what is an AE" and go straight to mechanics and code.
- **Fill known prerequisite gaps.**
  - The DL course did **not** teach RNN/LSTM/Seq2Seq, despite the official roadmap. A ~1hr sequence→attention bridge precedes the Transformer.
  - Syllabus #2 (math) is taught **just-in-time only** (decided 2026-11-22; this replaces "Probability, KL, MLE and the ELBO must be taught").
    - There is no math session.
    - Each idea appears inside the business case that needs it: a picture, at most one annotated formula, and a code cell.
    - MLE, KL and the ELBO are named in words and code.
    - Derivations go only in optional △ appendix slides.
    - Roadmap §11 (math map) tracks where each idea is taught.
- **GAN isn't legacy.** Teach it as foundational. Adversarial losses still power Real-ESRGAN, the SD VAE decoder, ADD/SDXL-Turbo and HiFi-GAN/EnCodec.
  - curriculum-analysis.md K4 still says "mostly legacy"; that framing is outdated.
- **"MusicNet" (#14) → MusicGen.** Treat it as audio and music generation with current models.
- Assessment (學習評量): explain Diffusion vs GAN and implement conditional generation.

## References (`references/`)

- [references/references.md](references/references.md): the official roadmap, 12 course goals, and the GAI syllabus #1–#14. It is the source of truth for scope. Earlier course decks are linked there as Google Drive links, which need the user's login; read them through Claude in Chrome, never by bypassing auth.
- `references/4_02_GAI_20240901_.pdf`: the 2024 GAI deck (Keras, math-heavy). Use it as a content reference, not a template. Read it with `pdftotext` (pypdf isn't installed).
- `references/艾鍗PPT版型2019-IT.pptx`: the training organisation's PowerPoint template (4:3). Not used: the decks are Slidev (see **Slides**).
- The user's previous course (Vibe Coding) lives at `C:\Users\lspss\Documents\Vibe_coding_python`, with 17 numbered Slidev decks (Slidev default 16:9) and its own CLAUDE.md. This course's slide format, skills and deck template were ported from it on 2026-11-22; look there for finished examples of a pattern.

## Conventions

- Write in English but keep the official Chinese syllabus terms (e.g. 生成式AI原理, 學習評量) as they appear in references.md.
- Cite deck and page when claiming students already know something.
- On Windows, run Python with `sys.stdout.reconfigure(encoding='utf-8')` when printing Chinese text (the console is cp1252).

## Slides (same format as Vibe Coding)

Decided 2026-11-22: **Slidev, in the Vibe Coding style.** Do not use PowerPoint or hosted slide artifacts unless asked.

- **Language of slides:** student-facing content (slides, speaker notes, practice text, notebook markdown and comments, each deck's `outline.md`, `NOTES.md`, `teaching-plan.md`) is **Traditional Chinese with Taiwan vocabulary**, as in Vibe Coding CLAUDE.md §2. Planning documents in `planning/` and the skills stay in English (Conventions above).
  - Keep standard English terms (PyTorch, Tensor, VAE, GAN, Diffusion, Transformer, LoRA, Token…). A term *new to the students* gets its Chinese gloss in parentheses on its first slide, e.g. Latent space（潛在空間）. The familiar-terms list is in `.claude/skills/slide-review/SKILL.md` §3b; each deck's `NOTES.md` glossary extends it. Do not gloss code, model names or paper titles.
  - Fonts: `Noto Sans TC`, `Microsoft JhengHei`; never SC variants.
  - Scan before delivering: `python -X utf8 scripts/scan-zh.py <deck>`.
- **Layout:** one directory per deck, `NN-kebab-topic/` (letter suffix allowed: `02a-…`), all sharing the root npm workspace. Dependencies only in the root `package.json` (Slidev 53.0.0, theme-default 0.25.0, playwright-chromium 1.64.1, Node ≥ 22.12). Never `npm install` inside a deck.
  - New deck: `npm run new-deck -- NN-topic "標題" "單元 NN"`, then `npm install` at the root. It copies `templates/deck/` (`style.css` design tokens, `components/` FillIn/FillClear/PromptBox/PromptBlank/Mcq/PickIn/ScoreSum, `scripts/make-print.mjs`, `slides.md` skeleton, `outline.md`, `NOTES.md`, `teaching-plan.md`, `research/sources.md`, `research/lab-runs.md`).
  - **Quiz questions are clickable buttons** (decided 2026-11-26): every 隨堂檢核 / iPAS-style multiple-choice question uses `<Mcq>`, with feedback for each option. Never plain-text `A.… B.…` options. Spec: `demo-and-practice` §3e.
  - Decks never import from each other; copy what is reused. Improvements to the template go into `templates/deck/` and are copied into existing decks deliberately.
  - Slides students should not see (practice answers, the closing 「下一步」 preview) carry `hostOnly: true`; `make-print.mjs` drops them from `slides.print.md`, which the QA exports use.
- **Per deck:** `outline.md` is approved by the instructor before `slides.md` is written (instructional-design §6). Every slide has ★/○/△ and Traditional Chinese speaker notes. Every shown number, image, VRAM figure and timing comes from a recorded Colab T4 run (`research/lab-runs.md`); never fabricate output.
- **Real images for contrast concepts** (decided 2026-11-26). When a concept is a contrast or a "what it looks like" claim (discriminative vs generative, real vs generated, before vs after), show a **real, freely licensed image** instead of a drawn placeholder or abstract chips. Source order: Wikimedia Commons (CC0 / public domain / CC BY(-SA)), then the deck's own recorded Colab outputs.
  - Download into the deck's `public/`, at ≤ 500 px; fetch thumbnails from `thumb.wikimedia.org` with a descriptive User-Agent, one file at a time (the original `upload.wikimedia.org` rate-limits with 429).
  - Read the Commons file page for author and license; put attribution in the slide's `.src` line and a row in `research/sources.md`.
  - A label or output that was not actually run is marked 「示意」; a generated image says which model made it.
  - Add the real-image layout CSS to the deck's `style.css`, and check the slide with `npx slidev export slides.print.md --format png --range N`.
- **QA** (from inside the deck): `npm run build`; `npm run export:png` and inspect every PNG; `npm run export` (PDF, internal check only); `node ../.claude/skills/slide-order-sync/check-order.cjs .`; `python -X utf8 ../scripts/scan-zh.py .`; run every notebook top to bottom on Colab T4. Do not claim a render, run or inspection that did not happen.
- **Deck index and status:** [planning/COURSE-PLAN.md](planning/COURSE-PLAN.md) (one deck per session, 01–24).
- **Lab notebooks** are built from percent-format sources: `python -X utf8 scripts/py2nb.py <deck>/materials/src/labNN-topic.py` writes the student notebook (TODO blocks emptied) and `-solution.ipynb`, and syntax-checks the solution. **Outline slide tables** are generated with `node scripts/outline-rows.mjs <deck> --write`.
- **Not ported (yet):** Vibe Coding's student site and online judge (`public-site/`, `publish-site.mjs`, `deploy-site.mjs`). Decide how students receive slides and notebooks (Colab links, GitHub repo, a site) before production.

### Skills (`.claude/skills/`) and agent

| Skill | Use it for |
|---|---|
| `instructional-design` | Objectives, concept map, sequencing, outline approval gate. |
| `technical-research-fact-checking` | Claim ledger, source hierarchy, GAI distinctions (KL direction, ε vs x₀ prediction, LoRA vs full fine-tuning…). |
| `visual-storytelling` | Choosing the visual per concept (AE/VAE, GAN, diffusion, attention, sampling, LoRA). |
| `slide-design-system` | Colors, type, layout, render/export QA. |
| `slide-diagram` | Diagram styles, drawing rules, role colors for model diagrams, gallery. |
| `slide-order-sync` | After any slide move/add/remove; `check-order.cjs`. |
| `demo-and-practice` | Demo vs practice vs Colab lab; practice-page format; lab page sequence; fallbacks. |
| `slide-review` | Pass/fail rubric (+ `golden-example.md`); also used by the `slide-reviewer` agent (`.claude/agents/`). |

If a skill conflicts with this file, this file wins.
