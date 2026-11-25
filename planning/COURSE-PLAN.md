# 生成式AI原理 · Course plan (deck index)

> Index of all 24 sessions → decks, in the structure of Vibe Coding's `COURSE-PLAN.md`. Source of truth for content: [course_roadmap.md](course_roadmap.md) (order, ★ items) and `slide-plan/D1…D6` (slide by slide). Updated 2026-11-23.

## Decisions recorded here

- **Deck split (2026-11-23, closes roadmap §14 open item):** one deck per 2-hour session, `NN-kebab-topic/`, numbered 01–24 in teaching order. Day-end quiz and homework live in the last deck of each day.
- **Phase status:** D1-1…D2-1 were auto-approved by the instructor's /goal and produced. Everything else is a slide plan **awaiting approval**; no outline or slides are written for it yet.
- **Lab notebooks** are written as percent-format sources in `<deck>/materials/src/*.py` and built into student + solution notebooks with `python -X utf8 scripts/py2nb.py <source>` (`# >>> TODO: …` / `# <<< TODO` mark the student blanks).
- **Outline slide tables** are generated from `slides.md` with `node scripts/outline-rows.mjs <deck> --write` so titles always match `check-order.cjs`.

## Deck table

| Day | Session | Deck | Business ticket | Syllabus | Lab | Status |
|---|---|---|---|---|---|---|
| D1 | D1-1 | `01-genai-value-map` | CEO: where is the value? | #1, #2 | L1-1 canvas | **Built** (23 slides; outputs pending T4 run) |
| D1 | D1-2 | `02-genai-tour` | Marketing: copy + product image tonight | #1, #2 | L1-2 | **Built** (26; notebook not yet run) |
| D1 | D1-3 | `03-keras-to-pytorch` | Factory IT: Keras → PyTorch | bridge | L1-3 | **Built** (25; CPU smoke test passed) |
| D1 | D1-4 | `04-colab-hub-gradio` | IT: disconnects + clickable demo | K10, #2 | L1-4 | **Built** (30; CPU smoke test passed) |
| D2 | D2-1 | `05-ae-anomaly-detection` | QA Line A: unseen defects | #3, #8, #2 | L2-1 | **Built + reviewed** (32; real VisA PCB1 CPU smoke test; T4 run pending) |
| D2 | D2-2 | `06-unet-defect-mask` | QA: where and how big | #4 | L2-2 | **Built + reviewed** (30; CPU smoke test on VisA; T4 run pending) |
| D2 | D2-3 | `07-vae-latent-space` | Marketing-tech: 512px on one T4 | #5, #2 | L2-3 | **Built + reviewed** (27; CPU smoke test; T4 run pending) |
| D2 | D2-4 | `08-vqvae-tokens` | IT/Support: low-bitrate storage | #6 | L2-4 | **Built + reviewed** (29, incl. Day 2 summary/quiz/homework; CPU smoke test; T4 run pending) |
| D3 | D3-1 | `09-gan-upscaling` | E-commerce: low-res catalog | #10 | L3-1 | **Built + reviewed** (32; T4 run recorded on an older build) |
| D3 | D3-2 | `10-cyclegan-line-b` | QA Line B: domain shift, no pairs | #11 | L3-2 | **Built + reviewed** (26; CPU smoke test; T4 run pending) |
| D3 | D3-3 | `11-ddpm-from-scratch` | Marketing: GAN mode collapse | #7, #2 | L3-3 | **Built** (31; T4 run 2 recorded on slides; slide-reviewer pending) |
| D3 | D3-4 | `12-diffusion-anomaly` | QA return: blurry AE heatmaps | #8 | L3-4 | **Built** (30, incl. Day 3 summary/quiz/homework; T4 run 1 recorded: AE beat diffusion; slide-reviewer pending) |
| D4 | D4-1 | `13-conditional-diffusion-cfg` | Data team: generate class k | #9, 學習評量 | L4-1 | Plan draft |
| D4 | D4-2 | `14-stable-diffusion-studio` | Marketing: brief → photo, new background | #9, K8, K9 | L4-2 | Plan draft |
| D4 | D4-3 | `15-lora-brand` | Brand: our product, our style | K7, #9 | L4-3 | Plan draft |
| D4 | D4-4 | `16-bakeoff-memo` | CTO: GAN or diffusion as standard? | 學習評量, K9 | L4-4 | Plan draft |
| D5 | D5-1 | `17-tokens-attention-bridge` | Support: token cost, word order | #12, #2 | L5-1 | Plan draft |
| D5 | D5-2 | `18-mini-gpt` | Support: how does it write? | #12, #13, #2 | L5-2 | Plan draft |
| D5 | D5-3 | `19-api-vs-self-host` | IT/Legal: API or self-host? | K6 | L5-3 | Plan draft |
| D5 | D5-4 | `20-qlora-sft` | Support: Simplified drift, broken JSON | K5, K7, K9 | L5-4 | Plan draft |
| D6 | D6-1 | `21-music-and-voice` | Marketing: royalty-free music, voice-over | #14 | L6-1 | Plan draft |
| D6 | D6-2 | `22-catalog-search` | E-commerce: 繁中 photo search | K8 | L6-2 | Plan draft |
| D6 | D6-3 | `23-ship-clinic` | Compliance: launch checklist + build | K9, K10 | L6-3 | Plan draft |
| D6 | D6-4 | `24-demo-day` | CEO office: demo day | all | — | Plan draft |

## What "built" does not yet include (honest status)

- No notebook has been run on a **Colab T4**. Every output slot on the slides is a `.placeholder` labelled 「講師實跑後替換」; each deck's `research/lab-runs.md` lists only local CPU smoke tests.
- Sources in each deck's `research/sources.md` are marked 「待確認」: they were written from the author's knowledge without opening the pages.
- The slide-reviewer agent has not reviewed the decks; self-review used the rendered PNGs, `check-order.cjs` and `scan-zh.py`.

## Before the next production round

1. Instructor approves (or edits) the D2-2…D6-4 slide plans.
2. Instructor runs decks 02–05 notebooks on Colab T4, pins versions, replaces placeholders.
3. Open items carried from roadmap §14: company name, cloud-LLM key policy, NC assets in a paid course, VisA hosting, delivery channel.
