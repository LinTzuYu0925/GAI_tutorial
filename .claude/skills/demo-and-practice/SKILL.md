---
name: demo-and-practice
description: The instructor's preferences for when a concept gets a live demo, a short practice page, or a Colab lab; how practice pages are built (individual, short answers typed into the slide, no turn-in, answer page hidden from the student site); and how Colab labs are structured to fit a free T4 session. Use when planning or adding demos, practices, labs, answer pages, or a teaching plan for any deck of the 生成式AI原理 course.
---

# Demo, Practice and Lab Skill

How this instructor wants concepts taught. Ported from the Vibe Coding with Python course (`C:\Users\lspss\Documents\Vibe_coding_python/.claude/skills/demo-and-practice`), where the page formats were developed with the same students; its catalogue of Vibe decks is not copied here. Follow this together with `instructional-design` (sequencing), `slide-diagram` (drawing) and `slide-order-sync` (after any page is added or removed).

## 1. Who the students are
- Career-switching trainees in a three-month 產業新尖兵 program for 「AI 代理人與自動化工程師」. Before this module they took Vibe Coding with Python, ML (sklearn) and DL (TF/Keras); see `planning/curriculum-analysis.md` for what each covered, with page citations.
- They can read and run Python with an AI coding agent's help, have trained a Keras CNN on Colab, and know loss, optimizer, epochs and transfer learning. They have **not** written PyTorch, an RNN, or any generative model in code, and their probability is thin.
- They do not know each other well and do not want forced interaction. **No games, role-play, forced pair work or group discussion.** Every practice is individual.
- Compute is **free Colab with a T4 (16 GB)**. Sessions disconnect, GPU quota runs out, and downloads are slow. Every lab needs a fallback (§3d).
- They use free or low-tier AI coding agents; budget about 8 agent messages per lab step and always provide a finished notebook as the no-quota fallback.
- Slides are **digital only**; most practices are **not collected**.

## 2. Demo, practice or lab? Decide with these tests
A **lab** (Colab notebook, 20-60 min) is the default for every key point: CLAUDE.md requires a hands-on lab per concept. A lab is broken into slide pages with steps (§3c).

A short **practice page** (5-15 min, answers typed into the slide) when all are true:
1. The student can do it alone, in the notebook or by hand (a shape, a number, a sampling result).
2. They will **discover something the slide does not already say**.
3. There is something checkable: a typed value, a shape, an image they describe in one line.

A **demo** (instructor operates, students watch; steps in the speaker notes) when any is true:
- It needs more than a T4 or a free session (SDXL full model, long fine-tuning runs, a paid API): demo it, or show saved results, labelled as the instructor's run.
- Students only need to see an effect, not operate it (a training run's progression, a failure mode such as GAN mode collapse filmed earlier).
- A practice would be trivial or already stated on the slide.
- The behaviour is uncertain on Colab free tier (package version churn, gated model access): test before class.

Never keep a practice whose answer is "read this text and predict" with nothing to run.

## 3. How a practice page looks
- Eyebrow `NN · Term（中文）· 練習`, title starts with 「練習：」.
- Instruction: one short line, or 2-3 short numbered steps. The goal and the reasoning go in the **speaker notes**.
- **No 完成標準 / 交出 / 目標 boxes** on the page. Do not say "turn in".
- **Students type directly into the slide.** Every blank is a text input on the student site, saved only in their own browser.
- **Components** live in each deck's `components/`, copied from `templates/deck/components/` (`FillIn.vue`, `FillClear.vue`, `answerStore.ts`, `PromptBox.vue`, `PromptBlank.vue`, `Mcq.vue` for quiz questions §3e, `PickIn.vue`/`ScoreSum.vue` for dropdown choices in tables). The deck's frontmatter needs `exportFilename`, which keeps answers separate between decks.
- **How to write a blank:** `<td class="blank"><FillIn id="vae.kl-value" hint="例：0.3……" /></td>`. Ids are `group.item`, unique in the deck, without slide numbers. One group per practice page; put `<FillClear group="vae" />` right after the table (or `<FillClear group="vae" corner />` when the page is tight).
- **Hints fit on one line,** gray italic, a mimic example ending in "……" that is clearly not the real result.
- **Ticks are clickable checkboxes:** `<FillIn id="lab1.ran" check />`, for checklists only.
- `FillIn` is one line; a multi-line option must be added and tested before the first `td.xtall` cell.
- **Test on a built site, not only a PNG:** type and reload; arrow keys while typing must not change slide; Enter then arrow does; clearing one page leaves others intact.
- Tables: `table.fill` with `td.blank`; `vlines` for separators, `tight` for short rows.
- When a result depends on a seed, model or runtime, add a 「你的 seed／GPU」 input.
- Predict → run → observe → explain is the learning loop (predict the output shape before running the cell; predict whether a higher temperature makes text more or less repetitive).

## 3a. Prompts students send to an AI coding agent
| Category | When | How to show it |
|---|---|---|
| a. Free | Changing it changes nothing that follows | Plain text, no copy button |
| b. Some choices | Students decide some values (latent size, number of epochs, a prompt subject) | `<PromptBox>` with `<PromptBlank id="lab.zdim" hint="潛在維度" />`; copy is blocked until filled; say the shown output is the instructor's choice |
| c. Exact | Output is compared with the slide, or names carry into later cells | `<PromptBox>` with no blanks |

Write line breaks as `<br>`, `>` as `&gt;`, no blank lines inside the box, indent with a full-width space. Prompts to an LLM *inside* a lab (K6, JSON output) are shown as code, not `PromptBox`.

## 3b. Notebooks and data
- One lab = one notebook in the deck's `materials/`, named `labNN-<topic>.ipynb` (student version, with `# TODO` cells) plus `labNN-<topic>-solution.ipynb` (finished, the no-quota/no-time fallback). Do not cite the solution as the place to "get" anything else.
- The first cell installs pinned versions (`pip install -q transformers==… diffusers==…`) and prints `torch.__version__`, the GPU name and free VRAM. Pin versions that were actually tested; record them in `research/lab-runs.md`.
- Data and weights load from inside the notebook (torchvision datasets, HF Hub). Prefer ungated models; if a model is gated, say how to accept the license and provide an ungated fallback.
- Every number, shape and image a slide shows is produced by the solution notebook, with the seed fixed. Save the outputs (`materials/outputs/` or the notebook's stored outputs) so slides and answer pages can cite them.
- Long-running steps (training, fine-tuning) state the expected wall time on a T4 and offer a pre-trained checkpoint so a student who disconnects can continue.

## 3c. The lab page sequence (adapted from Vibe Coding golden examples 5-6)
Students think **goal → split into parts → what each part does** before generating code; this is the four Prompt checkpoints from Vibe Coding unit 01 (① 目標 ② 輸入與輸出 ③ 限制 ④ 驗收).

| # | Title pattern | What is on it | Checkpoint |
|---|---|---|---|
| 1 | Lab k／N：我們要生成什麼？ | Left: the notebook link (`materials/labNN-….ipynb` → Open in Colab), dataset, runtime type (T4). Right: what the result should look like (a target sample grid, labelled 示意 until real), 1-3 plain-language questions. | ① 目標 |
| 2 | Lab k／N：模型拆成哪幾塊？ | Diagram from data to output split into named parts (encoder, decoder, loss, sampler…) with tensor shapes on the arrows. Names match the notebook. | (thinking) |
| 3 | 練習：每一塊的輸入與輸出 | `FillIn` table: part │ 輸入 shape │ 輸出 shape │ 做什麼（一句話）. First row filled. | ② 輸入與輸出 |
| 3a | (hostOnly) 練習解答 | Same table filled, with how to check (`print(x.shape)`). | |
| 4 | Lab k／N：Specify | Skeleton **【目標】【輸入與輸出】【限制】【驗收】**. 限制 includes T4 VRAM and time; 驗收 lists real expected numbers (loss after N epochs, sample grid). | ③ ④ |
| 5 | Lab k／N：Generate → Execute | `<PromptBox>` for the agent (or "fill the TODO cells"); excerpt of the key code beside its real output; fallback line. | |
| 6 | Lab k／N：Audit → Iterate | Audit table: shapes right? loss falling? samples plausible? one likely mistake (missing `model.eval()`, wrong normalization range, `[0,1]` vs `[-1,1]`) and a one-change fix. | |
| 7 | 延伸 (optional) + hostOnly answer | One change to try (conditional label, different β schedule, LoRA rank) with a predicted effect. | |

Rules:
- Questions on page 1 are about *what we want to see*, never about code.
- Parts on page 2 match the notebook exactly (class and function names).
- The PyTorch bridge deck and the sequence→attention bridge keep a simpler three-page pattern (golden example 5), because the goal there is the loop itself.

## 3d. Fallbacks (every lab)
- **No GPU quota:** a CPU-feasible reduced setting (fewer steps, smaller images) or the solution notebook's saved outputs.
- **No agent quota:** fill the TODO cells by hand from the slide excerpts, or open the solution.
- **Disconnected mid-training:** load the provided checkpoint and continue from the sampling cell.
- **Package break:** pinned versions in the first cell; the instructor re-runs every notebook within a week of class and logs it in `research/lab-runs.md`.

## 3e. 隨堂檢核: iPAS-style multiple choice as clickable buttons (standard, decided 2026-11-26)
Every multiple-choice question on a slide (隨堂檢核, iPAS 題型, end-of-day quiz) is a `<Mcq>` button question. Do not write plain-text `A.…　B.…` options or `（　）` blanks. Golden example: deck 01 「隨堂檢核 1／2（iPAS 題型）：點選答案」.
- **Component:** `components/Mcq.vue` (copy from `templates/deck/components/` with `answerStore.ts` and `FillClear.vue` if the deck lacks it).
- **Page:** eyebrow `隨堂檢核`; title `隨堂檢核 k／m（iPAS 題型）：點選答案`; **2 questions per slide** (4 options each shown as a 2×2 grid; 3 only if the stems and options are short), then `<FillClear group="quizK" corner />`. A deck's 3-4 questions → two slides. The end-of-day quiz (last deck of a day, 6 questions → three slides) keeps eyebrow `第N天 · iPAS 小考` and title `第N天小考 k／m（iPAS 題型）：點選答案` (decks 04, 08, 12).
- **Markup:**
  ```html
  <Mcq id="quiz1.q1" :n="1" :answer="2"
    :options="['選項 A', '選項 B', '選項 C', '選項 D']"
    :why="['A 為什麼錯', 'B 為什麼錯', '', 'D 為什麼錯']"
    explain="答對時顯示：為什麼 C 對（一句）。">
  題幹，關鍵否定詞用 <b>最不適合</b> 加粗？
  </Mcq>
  ```
  - `id` = `quizK.qN`, group = `quizK` matches the `FillClear`; `:n` numbers continuously across the deck's quiz slides (1-4, not 1-2 and 1-2).
  - `:answer` is the **0-based** index. Spread correct answers across A-D within a deck.
  - `:why` has one entry per option; the correct option's entry is `''`. Each wrong-option line says *why that option is wrong* in student terms (what that option actually describes), not just 「不對」. `explain` says why the right one is right, ideally pointing back to the slide or business ticket that taught it.
  - Distractors are plausible misconceptions from this deck (common-misconceptions list in `outline.md` §5), not jokes.
- **Behaviour:** student clicks; a wrong pick shows ✗ and 「再想想：」 + that option's `why`, and they can click again; a right pick shows ✓ and 「答對了！」 + `explain`. Answers persist in the browser like `FillIn`.
- **Speaker note:** `★ 檢核 k／m（N 分）。答案：1 C、2 B。` plus one line of reasoning per question. The answer key lives only in the note and the component props, so no hostOnly answer page is needed.
- `outline.md` §6 lists each question with its answer, so the instructor approves the questions with the outline.
- Use `PickIn` (dropdown in a table cell) for choices *inside* a practice table (e.g. a use-case canvas), not for quiz questions; `ScoreSum` totals `PickIn` scores.
- **QA:** on the built site click a wrong and a right option for each question and check the feedback text fits the slide without overflow.

## 4. Answer pages
- If a practice has a clear answer, put it on the **next** page with `hostOnly: true` (frontmatter `---\nhostOnly: true\n---` at the start of that slide). `scripts/make-print.mjs` writes `slides.print.md` without hostOnly pages; the student site and QA exports use that file. Do not hide answers with `v-click`.
- The closing **next-unit preview** (eyebrow 「下一步」, title 「下個單元：……」) is also `hostOnly: true`, last slide, still listed in `outline.md`.
- Same layout as the practice, answers filled, plus one line on how to tell. Eyebrow `… · 練習解答`.
- After adding one, run `slide-order-sync` and re-export to confirm the QA PDF has fewer pages.

## 5. Real screenshots and generated images
- Prefer real Colab screenshots and real generated samples. Never present invented output as real; a mock-up is labelled 示意 and listed for the instructor.
- Crop with CSS, put images in `public/`. Caption generated images with model, seed and steps.
- Paper figures are allowed with attribution (`slide-diagram` §1 "Original figure"), never as our result.

## 6. Planning checklist for a new deck
1. List the concepts from the slide plan. For each, decide lab / practice / demo / none with §2.
2. Budget time against the slide plan's block: hook 2 min, concept slides 5-8 min each, practice 10-15, lab 20-60, check 2.
3. Write demo steps and expected results in speaker notes; state the fallback.
4. Facts that depend on a library version, Colab UI or model license are 「待確認」 until checked, and go in `research/sources.md`.
5. Record the plan in `teaching-plan.md` (schedule table, prep checklist incl. "run every notebook on T4") and keep `outline.md` and `NOTES.md` in sync.
6. Do not build or export unless asked. List the pages with layout risk for the instructor.

## 7. Lessons inherited from Vibe Coding (do not relearn)
- Games, role-play and group sorting were rejected: adults who do not know each other.
- "Read and predict" practices with nothing to run were dropped.
- Practices whose result the UI hides after a few seconds failed; make them demos.
- Students asked repeatedly where the data was when it sat only inside the answer program: always give the data or notebook its own visible link.
- A fallback nobody ran turned out empty: run every fallback alone before class.
- `csv.DictReader`-style extra machinery in a prompt confused students; keep prompts to the concept being taught.

## 8. Things to ask the instructor before assuming
- Whether a Colab free-tier feature or quota really behaves as stated (they test on a real account).
- Whether a gated model (Llama, SD3) is acceptable, or an ungated alternative must be used.
- Whether TF is mandated program-wide (open item in CLAUDE.md).
