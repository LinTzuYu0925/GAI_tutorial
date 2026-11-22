# 生成式AI原理 (48hr): Course Roadmap

> **Status:** draft for instructor approval (2026-11-22). This is step 1 of phase 2 (slide plan) in the [CLAUDE.md](../CLAUDE.md) workflow.
>
> **Inputs:**
> - [curriculum-analysis.md](curriculum-analysis.md): scope K1–K10, syllabus #1–#14, what earlier courses taught.
> - [references.md](../references/references.md): the official syllabus and course goals.
> - [research/university-survey.md](research/university-survey.md): the survey of 24 university and practitioner courses.
>
> **Next:** after approval, the slide-by-slide plan in `planning/slide-plan/` (see §15).

The plan follows three decisions the instructor made on 2026-11-22:

1. **Business problem first.** Every session opens with a "ticket" from one department of a single fictional company, then introduces the tools that solve it.
2. **Math just-in-time only.** There is no math session. Each idea in syllabus #2 appears inside the ticket that needs it.
3. **LLMs on Day 5**, just before the Agent module.

---

## 1. Course at a glance

| | |
|---|---|
| Module | 生成式AI原理, 48 hours = 6 days × 4 sessions × 2h |
| Audience | Career-switching trainees in the 產業新尖兵 program for 「AI 代理人與自動化工程師」 |
| Already taught | Python via AI coding agents (Vibe Coding); sklearn ML; TF/Keras DL (DNN, CNN, transfer learning, YOLOv8). AE, U-Net, VAE, GAN and diffusion only at concept level (DL pp.72–87). **No** RNN/LSTM/Seq2Seq, PyTorch or LLM SDK calls (see curriculum-analysis.md) |
| Compute | Google Colab free tier, T4 16GB. Kaggle is the backup GPU when Colab quota runs out |
| Framework | PyTorch + Hugging Face (`transformers`, `diffusers`, `peft`, `trl`), Gradio for demos |
| Place in program | After 深度學習; before Agent 自動化實務 (tool calling, MCP, RAG, multi-agent) and Text-to-SQL 與向量資料庫 |
| Session shape | Hook (2 min) → concept slides (5–8 min each) → one or two individual practice pages (10–15 min) → one Colab lab (20–60 min) → Measure & Risk close. This follows the time budget in `demo-and-practice` §6. Slides are made full and marked ★ must / ○ optional / △ backup so the instructor can trim |
| Official assessment (學習評量) | 說明 Diffusion 與 GAN 差異並實作條件生成: a memo to the CTO plus a conditional-generation notebook (§12) |
| Course deliverable | An **individual** capstone: Gradio demo, one-page memo and a 3-minute demo. There is no group work (`demo-and-practice` §1) |

---

## 2. Teaching stance

### 2.1 Business problem first

Each session starts from a business problem a Taiwanese company could really have. Only then does it introduce the model and library that solve it.

The evidence for this approach:
- **Merrill's First Principles of Instruction.** Learning improves when instruction is centred on real-world problems and moves through activation → demonstration → application → integration.
- **Top-down courses.** NTU 李宏毅's GenAI courses, fast.ai and MIT 6.S191 all show that top-down openings work for beginners.
- **Business schools.** They stress that translating a business objective into an AI problem is the hard part. Stanford GSB MKTG 321: "The most difficult part of applying AI to solve a business problem is not building a fancy model". We train engineers to do that translation.

### 2.2 原理 means mechanism, not derivation

Math appears only when a ticket needs it, in this order:

1. a **picture**;
2. an **analogy**;
3. at most **one annotated formula** (every symbol labelled in Chinese);
4. a **code cell** that makes the formula concrete.

Rules:
- MLE, KL and the ELBO are **named and used** in words and code (D2-3, D5-2).
- Derivations (ELBO via Jensen, score matching, the Bayes rule behind guidance, the DPO objective) live only in optional △ appendix slides.
- The math map (§11) shows where every syllabus #2 idea is taught, so the official item stays traceable.

### 2.3 The six-step case loop

Every session runs the same loop. It parallels Vibe Coding's Specify → Generate → Execute → Audit → Iterate, which students already know.

| Step | Question | Merrill phase | Vibe Coding analogue |
|---|---|---|---|
| **Frame** (定義問題) | What is the ticket's KPI, data, constraints and law? Why don't the tools we know suffice? | Activation | Specify |
| **Try** (先用現成的) | What does a pretrained model or pipeline already give us? | Demonstration | Generate + Execute |
| **Open** (打開黑盒子) | How does it work? Picture, analogy, then a tiny from-scratch build | Demonstration | — |
| **Adapt** (調成我們的) | Condition, fine-tune or set a threshold on our data | Application | Iterate |
| **Measure** (量化驗收) | Business KPI + technical metric + risk | Application | Audit |
| **Ship** (交付展示) | Gradio demo or a cost/licence note for the department head | Integration | — |

A **Gradio app ships once per day** (§7). Other sessions ship a short cost or licence note.

### 2.4 Dual labs

Most sessions pair a **Try** part (pretrained pipeline: what an engineer uses) with an **Open** part (a tiny from-scratch model: how it works). The survey found the same pairing in the HF Diffusion course, MIT 6.S184, KAIST CS492 and fast.ai Part 2.

The lab budget is 20–60 minutes. To fit it, the Try part is usually an instructor demo or a short practice page, and the Open part is the Colab lab. When both are hands-on, they are two parts of one notebook.

### 2.5 AI-assisted coding policy

Students learned to code with AI agents, and they keep using them in labs: the agent writes the scaffold, the student audits the math and the shapes.

Every lab still has **predict → run → audit** checkpoints and at least one **no-AI checkpoint**, such as predicting a tensor shape or explaining a line. These checkpoints are individual practice pages, for example the lab's 「練習：每一塊的輸入與輸出」 shape table (`demo-and-practice` §3c). The 學習評量 includes a no-AI or oral "explain your CFG line" check. This follows CMU 10-423's split of no-AI and AI-assisted deadlines, and Stanford CS336's warning that AI tools can complete assignments for students.

**All practice is individual:** no games, role-play, pair work or group discussion (`demo-and-practice` §1; `slide-review` R-P1). The company tickets are a narrative device on the slides. Students never act out roles.

### 2.6 Slide conventions (carried into the slide plan)

- Every session's first slides are the **ticket card**.
- Every day ends with a **Measure & Risk** close and **iPAS-style multiple-choice questions** (goal 10).
- One teaching point per slide.
- Recall slides cite the earlier deck and page.
- Two recurring visuals:
  - **D2:** one encoder–decoder diagram that changes one part per session: AE → U-Net (skips) → VAE (stochastic bottleneck) → VQ-VAE (discrete bottleneck).
  - **D3–D4 and the memo:** the **generative trilemma** of quality, diversity and speed.
- Two running datasets, as `visual-storytelling` recommends, so samples can be compared side by side:
  - **Fashion-MNIST**, used as the store's lifestyle-catalog thumbnails, runs through VAE (D2-3) → VQ-VAE (D2-4) → DCGAN (D3-1) → DDPM (D3-3) → conditional DDPM (D4-1). These grids become the memo's evidence.
  - **One VisA PCB category** runs through AE (D2-1) → U-Net (D2-2) → CycleGAN (D3-2) → diffusion anomaly detection (D3-4).

---

## 3. What we learned from the survey

The full survey, with sources, is in [research/university-survey.md](research/university-survey.md).

| Course (term read) | Type | What we borrow |
|---|---|---|
| NTU 李宏毅 生成式AI導論 (2024) and 生成式人工智慧與機器學習導論 (2025) | Top-down, Colab homework | Use first, internals later; HF + Colab + Gradio from HW1; diffusion customisation and speech homework |
| fast.ai Practical Deep Learning | Examples first | Start with a complete working model and dig deeper; math taught when needed |
| MIT 6.S191 (2026) | Bootcamp | Music generation as an early lab; bias lab; a final project demo |
| CMU 10-423 Generative AI (S26) | Mixed | PyTorch primer first; "applying and adapting" unit; "what can go wrong" lecture; no-AI / AI-assisted deadlines |
| MIT 6.S184 (IAP26), KAIST CS492 (F24/F25), HF Diffusion course | Lab ladders | Dual labs; the ladder DDPM → DDIM/CFG → ControlNet/LoRA → distillation → flow |
| Stanford CME 296 (S26), CME 295 (A26) | Lectures + exams | Modern topic lists (flow matching, DiT, LLM pipeline); evaluation lectures |
| Stanford CS236, Berkeley CS294-158, Cornell CS 5788, MIT 6.S978 | Math-first | The canonical model families. We keep the families but not the math |
| MIT 6.5940 TinyML (F26) | Efficiency | Quantisation and LLM-on-laptop for goal 9 |
| Stanford GSB MKTG 321, MIT Sloan GenAI-Lab, Columbia B8631 | Business school | Business translation; company "tickets"; prototype + strategy memo |
| McKinsey (2023); Merrill (2002) | Evidence | Which departments to use (~75% of GenAI value: customer ops, marketing & sales, software, R&D); the problem-centred loop |

**What we deliberately do differently**

- **No exam-only format.** Every concept has a lab, unlike CME 295/296.
- **No derivations**, unlike all the math-first courses.
- **Industrial anomaly detection (#3, #8) and music generation (#14)** appear in almost none of the surveyed courses, but our syllabus requires them. We teach them through tickets.
- **Agents and RAG are deferred** to the Agent and Text-to-SQL modules, even though NTU 2025 and CME 295 now include them.

---

## 4. The running case: a fictional company

**Placeholder name: 曜嶼電子 (Yaoyu Electronics).** Every slide marks it 虛構. The instructor should confirm the name and check that it is not a real company before slides are made.

**Profile.** A Taiwanese consumer-electronics and lifestyle brand. It designs and assembles small devices (PCB assembly lines **A** and **B**, both with AOI inspection). It sells gadgets and lifestyle goods in its own **online store** and runs a **support desk** for Traditional-Chinese-speaking customers.

| Department | Who sends tickets | Sessions |
|---|---|---|
| 執行長室 / 技術長 (CEO / CTO) | Strategy questions; reads the memos | D1-1, D4-4, D6-4 |
| 製造品保部 (QA, Lines A & B) | Defect inspection, localisation, domain shift | D2-1, D2-2, D3-2, D3-4 |
| 行銷部 / 行銷科技 (Marketing, marketing-tech) | Product images, campaigns, music | D1-2, D2-3, D3-3, D4-2, D6-1 |
| 品牌部 (Brand) | Brand-faithful images | D4-3 |
| 電商部 (E-commerce) | Legacy photos, catalog search | D3-1, D6-2 |
| 數據組 (Data team) | Synthetic data for rare classes | D4-1 |
| 客服中心 (Support desk) | Ticket triage, reply drafting, tone | D2-4, D5-1, D5-2, D5-4 |
| 資訊 / 法務 (IT / Legal & compliance) | Compute, licences, privacy, launch checks | D1-3, D1-4, D5-3, D6-3 |

**Ticket card template.** Slides are written in Traditional Chinese.

```
【需求單 #D2-1】部門：製造品保部（A 線）
問題：           一句話說明要解決什麼
現況痛點：       目前的做法與損失（時間、金錢、品質）
成功指標（KPI）： 可量化的驗收標準
可用資料：       有什麼資料、多少、是否有標註
限制與法規：     預算、算力（T4）、延遲、個資法、授權
為何現有工具不夠： 機器學習／CNN 分類器做不到的原因
今天要用的工具：  模型、套件、資料集
```

**Industry terms used on tickets:**
- **過殺** (overkill): a good part rejected, i.e. a false positive.
- **漏檢** (escape): a defective part passed, i.e. a false negative.
- **節拍時間** (takt time): the time the line allows per unit.

**Local-law notes for ticket cards.** Each must be verified against the official text before slides are made.

- 個人資料保護法: tickets, call recordings and photos of people.
- 著作權法: training data and generated outputs.
- 人工智慧基本法: reported to have passed on 2025-12-23.
- 詐欺犯罪危害防制條例: reported disclosure duty for ads that use deepfake or AI-generated likenesses. The article number is to be checked.

---

## 5. Course learning outcomes

By the end of the module, a student can:

1. **Frame** a business problem as a generative-AI task: KPI, data, constraints, risk, and which model family fits (use-case canvas).
2. **Run and configure** pretrained text, image and audio generators with Hugging Face on a Colab T4, within VRAM, time and cost budgets.
3. **Explain** how a model generates data, with a picture and code rather than derivations:
   - AE, U-Net, VAE, VQ-VAE;
   - GAN, CycleGAN;
   - diffusion (conditional and latent);
   - Transformer and GPT.
4. **Implement** small generative models from scratch in PyTorch (AE, VAE, VQ-VAE, DCGAN, DDPM with CFG, attention, mini-GPT). **Diagnose** common failures: blurry reconstructions, mode collapse, noisy samples, format drift.
5. **Adapt** a pretrained model to company data with conditioning, LoRA or QLoRA, and judge when prompting alone is enough.
6. **Measure** output against a business KPI and a technical metric (過殺/漏檢, AUROC, FID/KID, CLIP score, LLM-as-judge). **Identify** licence, copyright, privacy and safety risks.
7. **Distinguish** diffusion from GAN on quality, diversity, speed, stability and control, and **implement** conditional generation (學習評量).
8. **Ship** a working demo (Gradio, share link or HF), then **defend** the model choice, cost and risk in a memo and a short demo.

---

## 6. Pre-work (課前準備, outside the 48 hours)

- [ ] A Google account. Open the GPU smoke-test notebook in Colab and confirm `torch.cuda.is_available()`.
- [ ] A Hugging Face account and access token. The whole classroom shares one IP address, so anonymous downloads get rate-limited.
- [ ] A Google Drive folder `GAI/` for checkpoints and outputs.
- [ ] A cloud-LLM key: a free tier or the instructor's key policy (open item). The open-model fallback works without one.
- [ ] Optional preview in Chinese: NTU 李宏毅 2025 lecture 1, 「一堂課搞懂生成式人工智慧的基本原理」.

---

## 7. Day-by-day roadmap

### 7.0 Overview

| Day | Business question | Departments | Syllabus | Daily ship (Gradio) |
|---|---|---|---|---|
| D1 | 「GenAI 能為我們做什麼？跑得動嗎？」 Where is the value, and can we run it? | CEO, Marketing, IT | #1, #2 (just-in-time), PyTorch bridge | App over the ported classifier |
| D2 | 「找出從沒看過的瑕疵」 Find defects we have never seen; compress before generating | QA (Line A), Marketing-tech, IT/Support | #3, #4, #5, #6, #8 baseline | AE inspector |
| D3 | 「GAN 還是擴散？」 Images at scale, then back to the factory | E-commerce, QA (Line B), Marketing | #10, #11, #7, #8 | Upscaler or Line-B translator |
| D4 | 「行銷影像工作室」 Controllable image generation | Data team, Marketing, Brand, CTO | #9, 學習評量, K7–K9 | Product image studio |
| D5 | 「客服中心」 Text generation and the LLM engineer's choices | Support, IT/Legal | #12, #13, K6, K7 | Ticket-triage assistant |
| D6 | 「上市與交付」 Audio, search, compliance, capstone | Marketing, E-commerce, Compliance, CEO office | #14, K8–K10 | Capstone app |

Each session block below lists:
- **Ticket:** the business problem.
- **Steps:** the six-step loop.
- **★ / ○ / △:** must / optional / backup knowledge points.
- **Recall:** earlier deck and page citations.
- **Lab:** with ID, matching the inventory in §10.
- **Risk:** items for the Measure & Risk close.

---

### Day 1 · 「GenAI 能為我們做什麼？跑得動嗎？」

#### D1-1 · CEO: 「競爭對手都在用 GenAI，我們的價值在哪？」 (#1, #2)
- **Ticket.** The CEO wants a one-page answer: where GenAI creates value for the company, what it costs, what can go wrong.
- **Steps.**
  - Frame: the company, its departments and their tickets, which double as the course map.
  - Try: instructor live tour: product copy (LLM), product image (diffusion), a 10-second jingle (MusicGen).
  - Open: what makes these models "generative".
  - Measure: triage each ticket on value × feasibility × data × risk.
  - Ship: a use-case canvas.
- **★**
  - Course map and the six-step loop.
  - Generative vs discriminative by example: a classifier answers 「瑕疵或不是」; a generator draws a new board.
  - p_data vs p_θ as a picture: the model learns "what our products usually look like".
  - A prompt is a condition: p(x|y). This returns in D4-1 and D5-2.
  - The 2026 landscape map: LLMs, diffusion/flow, multimodal, audio, agents; open vs closed weights.
  - Use-case triage on McKinsey's four high-value functions.
  - Build vs buy (API vs open weights), linked to iPAS 導入評估 and 導入規劃.
- **○** A history timeline from VAE and GAN to today's models (dates verified in the slide plan); where GenAI should *not* be used.
- **△** Normalizing flows and autoregressive image models (named only).
- **Recall.** DL pp.80–81 (GenAI overview, GPT as next-word guessing); ML pp.42–43 (logistic regression, a discriminative model); Vibe 01 (LLM as next-token sampling).
- **Lab L1-1.** Use-case canvas for two tickets. No GPU.
- **Risk.** Hallucination; review requirements for high-stakes use.

#### D1-2 · Marketing: 「今晚就要新品文案和一張產品圖」 (#1, #2)
- **Ticket.** Marketing needs prototype product copy and one product image by tonight.
- **Steps.**
  - Frame: deliverables and brand constraints.
  - Try: HF `pipeline` for text, `diffusers` for an image, one cloud-LLM call.
  - Open: why outputs change from run to run: sampling from a probability distribution.
  - Adapt: change prompt, temperature and seed.
  - Measure: which outputs are usable? Can we reproduce one?
  - Ship: saved outputs plus the licence line from each model card.
- **★**
  - Colab GPU runtime.
  - `pipeline`; `DiffusionPipeline` in fp16.
  - The first SDK call, with the key read from `.env`.
  - The next-token probability bar chart.
  - Temperature, reusing the distillation intuition.
  - Seeds and reproducibility.
  - Reading the licence field of a model card.
- **○** System vs user prompt (reuses Vibe 01–02); negative prompts as a preview of D4-2.
- **Recall.** DL pp.69–71 (softmax temperature); Vibe 11–12 (`requests`, JSON, `.env`); Vibe 01–02 (prompts); ML pp.5–6 (Colab T4).
- **Lab L1-2.** The GenAI tour, text + image: a small open instruct LLM, plus SD1.5 + LCM-LoRA for few-step images, plus one cloud call. Fallback: open models only.
- **Risk.** Prompt privacy on free tiers (prompts may be reused); who owns generated output.

#### D1-3 · Factory IT: 「瑕疵分類器是 Keras 寫的，生成式工具卻都是 PyTorch」 (bridge)
- **Ticket.** Port the existing Keras defect classifier to PyTorch so it fits the Hugging Face ecosystem. The DL course's LabDay3-2 CIFAR-10 CNN stands in for the classifier.
- **Steps.**
  - Frame: why PyTorch (HF, diffusers, peft and trl are PyTorch-first).
  - Try: re-run the familiar Keras notebook.
  - Open: map each Keras step to PyTorch.
  - Adapt: port it.
  - Measure: accuracy matches the Keras version within tolerance.
  - Ship: a saved `state_dict`.
- **★**
  - Keras→PyTorch mapping table: `Model`/`compile`/`fit` ↔ `nn.Module`/optimizer/loop.
  - Tensors, dtype, device, `.to(device)`.
  - CHW vs HWC.
  - Autograd: `backward()`, `optimizer.step()`, `zero_grad()`.
  - `nn.Module` subclassing, the same pattern as subclassing `keras.Model`.
  - `Dataset` and `DataLoader`.
  - Training and evaluation loop.
  - `model.eval()` + `torch.no_grad()`; decorator syntax is explained here, at first use.
  - Saving and loading a `state_dict`.
- **○** Broadcasting; PIL image I/O; a 5-line autograd warm-up that fits a Gaussian to data (MLE intuition, also used again in D5-2).
- **△** PyTorch Lightning / Accelerate (named only).
- **Recall.** DL pp.16–33 (Keras training loop); DL p.20 (subclassing `keras.Model`); DL pp.36–37, 94–97 (TF vs PyTorch; PyTorch appendix); DL pp.38–55 (CNN); Vibe 12a (shape, dtype); Vibe 13 (classes).
- **Lab L1-3.** Port LabDay3-2 to PyTorch and compare accuracy. No-AI checkpoint: predict each layer's output shape before running.
- **Risk.** "The agent's port runs" ≠ "the port is correct".

#### D1-4 · IT: 「Colab 斷線害我們白訓練一天；主管要能點的展示」 (K10, #2)
- **Ticket.** Make training survive Colab disconnects, and show results as something a manager can click.
- **Steps.**
  - Frame: Colab limits (session length, idle timeout, GPU quota).
  - Try: load a Hub model with `from_pretrained`.
  - Open: what is inside a model repo (config, safetensors weights, model card, licence).
  - Adapt: checkpoint to Drive and resume.
  - Measure: memory at fp32 vs fp16.
  - Ship: a Gradio app over the D1-3 classifier.
- **★**
  - Mounting Drive; checkpoint and resume.
  - HF Hub: `from_pretrained`, model cards, the licence field, safetensors and why they replace pickle.
  - The VRAM rule of thumb: parameters × bytes (fp32 = 4, fp16 = 2).
  - T4 notes: fp16 yes, no native bf16, no FlashAttention-2.
  - Handling out-of-memory errors: batch size, fp16, freeing memory, restarting.
  - matplotlib image grids.
  - Gradio `Interface`/`Blocks` and `share=True`.
- **○** HF cache location and Colab disk space; `nvidia-smi`.
- **△** HF Spaces (preview of D6-3).
- **Recall.** ML pp.5–6 and DL pp.34–35 (Colab GPU); Vibe 12 (pickle risk); 數據代理人 pp.50–61 (Plotly Dash apps: Gradio is the same idea).
- **Lab L1-4.** Resumable training plus a Gradio app; measure one Hub model's memory at fp32 vs fp16. **Day 1 ship.**
- **Risk.** Licence families: Apache / MIT / OpenRAIL / non-commercial.

**Day 1 homework.** A use-case canvas for a third ticket; finish the port; iPAS-style quiz.

---

### Day 2 · 「找出從沒看過的瑕疵」

The day uses one recurring encoder–decoder diagram. Each session changes one part:
- D2-1 plain AE;
- D2-2 add skips (U-Net);
- D2-3 a stochastic bottleneck (VAE);
- D2-4 a discrete bottleneck (VQ-VAE).

#### D2-1 · QA Line A: 「AOI 過殺太高，新瑕疵又漏檢；瑕疵樣本幾乎沒有」 (#3, #8 baseline, #2)
- **Ticket.** QA has thousands of good PCB images and very few defect images, and new defect types keep appearing. AOI rejects too many good boards (過殺) yet some defects escape (漏檢).
- **Steps.**
  - Frame: why the DL course's supervised CNN fails: there are no labels for defects nobody has seen yet.
  - Try: the instructor's trained AE flags defects on sample boards.
  - Open: an AE learns "normal"; reconstruction error measures how untypical a board is.
  - Adapt: train on good boards only; set a threshold.
  - Measure: 過殺 at a fixed 漏檢; AUROC.
  - Ship: a Gradio inspector.
- **★**
  - One-slide AE recap (DL pp.72–79), then the day's diagram.
  - ConvTranspose vs upsampling.
  - The reconstruction-error heatmap.
  - Likelihood as typicality, shown as a picture.
  - Choosing a threshold from score histograms.
  - 過殺/漏檢 mapped to FP/FN.
  - AUROC.
  - Production baselines named: PatchCore, EfficientAD.
- **○** SSIM vs MSE as the error measure; the anomalib library.
- **△** AEs can reconstruct anomalies too well (the "identity shortcut"). This sets up D2-2 and D3-4.
- **Recall.** DL pp.72–79 (AE, U-Net, VAE intro); DL p.74 (UpSampling); DL pp.38–55 (CNN); ML pp.9–10 (metrics).
- **Lab L2-1.** Conv AE on one VisA PCB category, trained on good images only: heatmaps, AUROC, threshold at a fixed 漏檢. **Day 2 ship:** the Gradio inspector.
- **Risk.** The business cost of 過殺 vs 漏檢. Dataset licences: VisA (CC BY) vs MVTec AD (non-commercial); DeepPCB's ambiguous licence.

#### D2-2 · QA: 「告訴我瑕疵在哪、有多大」 (#4)
- **Ticket.** The repair station needs each defect's location and size, not just a flag.
- **Steps.**
  - Frame: the output must be per pixel.
  - Try: the instructor's U-Net mask overlay.
  - Open: *"Why not add skips to the AE? They would copy the defect straight through."* Skips are right for segmentation and wrong for reconstruction-based detection.
  - Adapt: there are no masks, so generate synthetic defects (the DRAEM idea).
  - Measure: IoU/Dice on real masks; defect area in pixels.
  - Ship: an overlay with an area estimate.
- **★**
  - The U-Net diagram (the day's diagram plus skips).
  - Skip *concatenation* vs ResNet *addition*.
  - Per-pixel BCE + Dice loss.
  - Synthetic anomaly generation: Perlin-style masks with procedurally generated textures.
  - IoU and Dice.
- **○** DRAEM's two sub-networks (reconstructive + discriminative); the U-Net returns as the diffusion denoiser in D3-3.
- **△** Checkerboard artefacts from transposed convolutions.
- **Recall.** DL pp.72–79 (U-Net idea); DL pp.38–55 (ResNet skips).
- **Lab L2-2.** U-Net trained on synthetic defects over good VisA images, tested on real VisA masks (a split the instructor prepares).
- **Risk.** Synthetic defects ≠ real defects; always validate on real samples.

#### D2-3 · Marketing-tech: 「每週要在一張 T4 上生成上千張 512px 圖」 (#5, #2)
- **Ticket.** The image generation planned for D4 must be affordable on one T4. Compress images into a small, smooth latent space first.
- **Steps.**
  - Frame: pixels are expensive (512×512×3 values).
  - Try: a round trip through Stable Diffusion's `AutoencoderKL` on a product photo: compression ratio vs quality.
  - Open: an AE's latent space has holes. A VAE maps each image to a cloud (μ, σ); KL keeps the clouds near the centre; reparameterisation lets gradients flow.
  - Adapt: train a VAE on Fashion-MNIST, used as the store's lifestyle-catalog thumbnails.
  - Measure: reconstruction vs sample quality; smoothness via interpolation.
  - Ship: a compression-ratio note.
- **★**
  - AE vs VAE latent scatter plots.
  - The encoder outputs μ and σ.
  - Reparameterisation in code: `z = mu + sigma * eps`.
  - Loss = reconstruction + KL: one annotated line, a two-Gaussian picture and code.
  - Why exact likelihood is intractable (in words).
  - The **ELBO** named in words.
  - Sampling new items; interpolating between two products.
  - The SD VAE turns 512×512×3 into a 64×64×4 latent.
- **○** β-VAE (sharpness vs smoothness); why VAE samples are blurry and why GAN or diffusion decoders matter.
- **△** ELBO derivation (Jensen) in the appendix.
- **Recall.** DL p.79 (VAE intuition; normal distribution; KL named); DL pp.72–79.
- **Lab L2-3.** Fashion-MNIST VAE (sample, interpolate, compare AE vs VAE latents), plus an SD-VAE round trip on a product photo.
- **Risk.** Generative models can memorise training examples (a privacy concern).

#### D2-4 · IT/Support: 「通話錄音與產線影像要低位元率儲存與串流」 (#6)
- **Ticket.** Call-centre recordings and line images fill storage. Store and stream them at low bitrate.
- **Steps.**
  - Frame: the bitrate vs quality trade-off.
  - Try: EnCodec at 1.5–24 kbps on a synthetic support call.
  - Open: vector quantisation snaps each latent to the nearest codebook entry, turning images and audio into discrete tokens.
  - Adapt: train a tiny VQ-VAE.
  - Measure: bits per image vs reconstruction error; codebook usage (dead codes).
  - Ship: a bitrate/quality table.
- **★**
  - Codebook lookup (nearest neighbour).
  - The straight-through estimator: "pretend the snap is the identity for gradients".
  - Commitment and codebook losses.
  - Bits per image = number of tokens × log2(K).
  - Codebook usage and dead codes.
  - Residual VQ (EnCodec) as stacked codebooks.
  - Tokens as "image/audio words" that a language model can generate. This previews D5 (GPT) and D6-1 (MusicGen).
- **○** VQGAN (adds adversarial and perceptual losses; links to D3-1).
- **△** EMA codebook updates.
- **Recall.** D2-1, D2-3; DL pp.72–79.
- **Lab L2-4.** EnCodec bitrate sweep, plus a tiny VQ-VAE on Fashion-MNIST with bits-vs-error and code-usage plots.
- **Risk.** Real call recordings contain personal data (個資法), so use synthetic recordings only.

**Day 2 homework.** Anomaly detection on a second VisA category, with a half-page 過殺/漏檢 threshold recommendation. iPAS-style quiz.

---

### Day 3 · 「GAN 還是擴散？」

#### D3-1 · E-commerce: 「舊型錄照片解析度太低，網站改版用不了」 (#10)
- **Ticket.** Thousands of legacy low-resolution catalog photos; reshooting is too expensive.
- **Steps.**
  - Frame: we need sharp, plausible detail, fast.
  - Try: Real-ESRGAN on legacy photos.
  - Open: a GAN is a forger (G) against an inspector (D), which is why GANs produce sharp detail.
  - Adapt: train a DCGAN on Fashion-MNIST and watch it struggle.
  - Measure: sample grids over epochs; spot mode collapse.
  - Ship: an upscaler app (Day 3 ship option A).
- **★**
  - The roles of G and D (recall DL pp.82–84).
  - The adversarial objective as one annotated line.
  - The **non-saturating** generator loss, and why: early on D wins easily and G gets no gradient.
  - DCGAN rules: strided conv, BatchNorm, LeakyReLU, no fully connected layers.
  - Instability and mode collapse, and how to spot them.
  - Where adversarial losses still ship: Real-ESRGAN, the SD VAE decoder, ADD/Turbo, HiFi-GAN/EnCodec (links to D2-4).
- **○** Conditional GAN preview; perceptual loss.
- **△** WGAN / gradient penalty (named only).
- **Recall.** DL pp.82–84 (GAN parts and applications); the DL course's CNN classifiers (a discriminator is one).
- **Lab L3-1.** DCGAN on Fashion-MNIST, plus Real-ESRGAN upscaling (pinned working install, §10).
- **Risk.** Super-resolution invents detail. Product photos must not misrepresent the product.

#### D3-2 · QA Line B: 「新廠相機拍出來的影像不一樣，A 線模型一直誤報，又沒有成對影像」 (#11)
- **Ticket.** The new plant's Line B uses a different camera. The Line-A detector keeps raising false alarms (domain shift), and there are no aligned before/after image pairs.
- **Steps.**
  - Frame: domain shift; paired translation is impossible.
  - Try: the instructor's CycleGAN snapshots translating B→A.
  - Open: two generators and two discriminators; cycle-consistency (A→B→A ≈ A); identity loss; PatchGAN.
  - Adapt: a brief training run.
  - Measure: 過殺 from the D2-1 AE before and after translation. Do real defects survive?
  - Ship: a before/after report, or a translator app (Day 3 ship option B).
- **★**
  - Paired (pix2pix) vs unpaired translation.
  - The CycleGAN architecture.
  - Cycle-consistency and identity losses.
  - PatchGAN.
  - The failure that matters here: translation can **invent or erase features** (hallucination). Evaluate on defects explicitly.
- **○** Simpler fixes first: colour normalisation, or retraining the AE on Line-B good images.
- **△** The domain-adaptation literature (CyCADA).
- **Recall.** D3-1 (GAN); D2-1 (AE detector).
- **Lab L3-2.** A brief CycleGAN run at 64–128px on a synthetic Line-B shift (colour temperature, blur, noise, lighting), with instructor snapshots from several epochs. Measure 過殺 before and after with the L2-1 AE, and check that defects survive.
- **Risk.** Hallucinated features in high-stakes images; deepfakes and GAN misuse.

#### D3-3 · Marketing: 「我們的 GAN 一直生出同樣的圖；要不要改用擴散模型？」 (#7, #2)
- **Ticket.** Marketing's GAN-based generator lacks diversity: the mode collapse seen in D3-1.
- **Steps.**
  - Frame: the trilemma. GANs give quality and speed but weak diversity.
  - Try: sample from a pretrained small DDPM (`DDPMPipeline`).
  - Open: destroy images with noise step by step, then learn to undo one step by predicting the noise.
  - Adapt: train a tiny DDPM.
  - Measure: sample diversity vs the DCGAN; sampling time vs number of steps.
  - Ship: a sample grid with a timing note.
- **★**
  - The forward-noising strip x₀…x_T.
  - One-step noising, x_t computed directly from x₀ (one annotated line).
  - The predict-the-noise objective (MSE on the noise).
  - The noise schedule.
  - The **time-step embedding**, sinusoidal; it returns as positional encoding in D5-2.
  - The U-Net from D2-2 as the denoiser.
  - The sampling loop.
  - The trilemma visual.
- **○** Why diffusion trains stably (a plain regression loss); HF schedulers.
- **△** The score-matching view; the ELBO connection.
- **Recall.** DL pp.85–87 (diffusion overview); D2-2 (U-Net).
- **Lab L3-3.** A tiny DDPM on Fashion-MNIST at 28–32px, with a provided small U-Net and a fallback checkpoint.
- **Risk.** Memorisation of training data and copyright in generated images.

#### D3-4 · QA (return): 「AE 熱圖太模糊，細紋路一直過殺」 (#8)
- **Ticket.** AE heatmaps are blurry on fine textures, which causes 過殺. The line also needs results within its takt time.
- **Steps.**
  - Frame: KPI = 過殺 at a fixed 漏檢, plus localisation; throughput vs takt time.
  - Try: the instructor's diffusion model "repairs" a defective board.
  - Open: partially noise the image to step t, then denoise. The result is a "normal" version, and the residual is the anomaly map.
  - Adapt: choose t and the number of DDIM steps.
  - Measure: AUROC and 過殺 vs the D2-1 AE; images per second vs takt time.
  - Ship: an operator view (original / repaired / residual).
- **★**
  - Partial-noise reconstruction (the AnoDDPM idea).
  - Residual maps.
  - Choosing the noise level t: too low keeps the defect, too high loses the board.
  - DDIM and fewer steps to cut latency.
  - The comparison table, AE vs diffusion.
  - Showing the operator the "repaired" board, for explainability.
- **○** PatchCore and EfficientAD named again as production baselines; simplex noise.
- **△** Conditioned diffusion anomaly detection (DDAD) named.
- **Recall.** D2-1, D3-3.
- **Lab L3-4.** Diffusion anomaly detection with an instructor-trained checkpoint on the L2-1 category: t and step sweeps, AUROC vs L2-1, throughput.
- **Risk.** Deepfake-ad disclosure duties (詐欺犯罪危害防制條例, to be verified); GAN and diffusion misuse.

**Day 3 homework.** Extend the trilemma table with your own DCGAN and DDPM evidence; this feeds the memo. Optional: a write-up of a CycleGAN failure case. iPAS-style quiz.

---

### Day 4 · 「行銷影像工作室」

#### D4-1 · Data team: 「網店分類器對少數類別很弱，能不能指定生成第 k 類？」 (#9, 學習評量)
- **Ticket.** The store's product classifier underperforms on rare categories. Generate images of a chosen category on demand.
- **Steps.**
  - Frame: conditional generation p(x|y) (recall D1-1).
  - Try: sample a class from the instructor's conditional model.
  - Open: feed the class in as an embedding. Classifier guidance gets one slide. Classifier-free guidance trains with label dropout and mixes the conditional and unconditional predictions when sampling.
  - Adapt: add class conditioning to the D3-3 DDPM (warm start).
  - Measure: fidelity (a Fashion-MNIST classifier's accuracy on generated samples) and diversity (FID/KID) across guidance scales.
  - Ship: a guidance-scale grid.
- **★**
  - The class embedding added to the time embedding.
  - Label dropout.
  - The CFG mixing rule (one annotated line).
  - The guidance-scale trade-off: higher fidelity, lower diversity.
  - FID/KID as a distance between feature clouds (picture).
  - **No-AI checkpoint:** "explain your CFG line".
- **○** Classifier guidance as a picture.
- **△** The Bayes-rule derivation of guidance.
- **Recall.** D3-3, D1-1; ML pp.9–10 (metrics).
- **Lab L4-1.** Class-conditional DDPM + CFG, a scale grid, fidelity and FID/KID. **This is the 學習評量 「實作條件生成」 notebook.**
- **Risk.** Synthetic data can amplify bias and artefacts. Always validate on real data.

#### D4-2 · Marketing: 「依企劃文字生成產品情境照，還要換背景」 (#9, goal 8, K8, K9)
- **Ticket.** Generate lifestyle shots from a text brief, and replace the backgrounds of existing product photos.
- **Steps.**
  - Frame: text conditioning at 512px on a T4.
  - Try: SD1.5 text-to-image.
  - Open:
    - A 15-minute **CLIP block**: text and images in one embedding space.
    - Latent diffusion = the SD VAE (D2-3) + a U-Net + the CLIP text encoder + a scheduler.
    - Cross-attention, as a picture.
  - Adapt: schedulers, steps, CFG, seeds, negative prompts; img2img; inpainting to swap backgrounds.
  - Measure: CLIP score across CFG scales; a bias audit on prompts with people.
  - Ship: the product image studio (**Day 4 ship**).
- **★**
  - CLIP's contrastive training (picture).
  - A **cosine-similarity code cell**; this doubles as the dot-product refresher.
  - The Stable Diffusion anatomy diagram.
  - Cross-attention (picture only; the Transformer details come in D5).
  - Pipeline parameters: steps, scheduler, guidance scale, seed, negative prompt.
  - img2img strength.
  - Inpainting: the mask and the 9-channel input, which is **conditioning by concatenation**.
  - CLIP score.
  - A bias audit.
- **○** ControlNet (instructor demo: layout and pose control); inpainting synthetic defects to augment YOLOv8 training (DL pp.56–62).
- **△** The math of the DDIM and DPM-Solver schedulers.
- **Recall.** D2-3 (SD VAE); D4-1 (CFG); DL pp.56–62 (YOLOv8).
- **Lab L4-2.** SD1.5 studio (pinned mirror, fp16): parameter sweeps, inpainting background swap, CLIP score.
- **Risk.** Copyright and style imitation; bias; invisible watermarks and C2PA provenance.

#### D4-3 · Brand: 「生成的圖必須是我們的產品、我們的風格」 (K7, #9)
- **Ticket.** Generated images must show the actual product, in the brand's look.
- **Steps.**
  - Frame: a prompt alone cannot describe our product.
  - Try: IP-Adapter with one reference photo, no training.
  - Open: full fine-tuning vs LoRA. LoRA freezes W and learns a low-rank update B·A ("two thin matrices"). DreamBooth adds an identifier token.
  - Adapt: train a subject LoRA on about 10 owned photos.
  - Measure: a before/after grid; signs of overfitting (the same pose and background everywhere).
  - Ship: the LoRA weights with a usage note.
- **★**
  - IP-Adapter as the no-training baseline.
  - The LoRA picture W + B·A and its parameter count.
  - The DreamBooth idea: an identifier token and a few images.
  - T4 configuration: 512px, gradient checkpointing, 8-bit Adam.
  - Overfitting and prior preservation (concept).
  - Consent and IP of training images.
- **○** Textual inversion (named only).
- **△** The math of LoRA rank and alpha.
- **Recall.** DL pp.56–66 (transfer learning, 「接頭霸王」); D4-2.
- **Lab L4-3.** IP-Adapter vs DreamBooth-LoRA on about 10 photos the students take themselves.
- **Risk.** Training on images you do not own; imitating other brands.

#### D4-4 · CTO: 「GAN 還是擴散？哪個當公司標準？能不能即時？」 (學習評量, K9)
- **Ticket.** The CTO must choose a standard approach for a recurring task, the seasonal edit of product photos, and wants it near real time.
- **Steps.**
  - Frame: decision criteria = the trilemma + stability + control + licence.
  - Try: three pretrained approaches on the same edit:
    - CycleGAN (summer→winter);
    - InstructPix2Pix (text-instructed diffusion editing);
    - SD1.5 + LCM-LoRA (few-step diffusion).
  - Open: how diffusion became fast.
    - Distillation (recall DL) leads to LCM.
    - Adversarial diffusion distillation (Turbo) shows the GAN loss lives on.
    - Flow matching follows straight paths (2D toy); it is the method behind SD3/FLUX.
  - Adapt: tune steps and guidance for speed.
  - Measure: individual preference ratings (a FillIn practice page, then the class tally), timing, diversity, failure cases.
  - Ship: the bake-off table, which becomes the memo skeleton.
- **★**
  - Distillation recap leading to few-step generators (LCM/Turbo).
  - ADD = diffusion + an adversarial loss.
  - Flow-matching intuition with a 2D toy.
  - Text-guided editing.
  - Human preference evaluation.
  - The trilemma as the memo scaffold.
  - The memo brief.
  - **Each student chooses a capstone ticket.**
- **○** Consistency models (named only); DiT preview (payoff in D5-2).
- **△** The rectified-flow math.
- **Recall.** DL pp.67–72 (distillation); D3-1, D3-2, D3-3, D4-1.
- **Lab L4-4.** The three-way bake-off, plus a 2D flow-matching toy (runs on CPU).
- **Risk.** Compare the licences of the three: CycleGAN (BSD), InstructPix2Pix, LCM-LoRA (openrail++). SDXL-Turbo (non-commercial) is the counter-example.

**Day 4 homework.** Draft the 學習評量 memo and finish the L4-1 notebook. Write a one-paragraph capstone proposal (ticket, data, model, KPI). iPAS-style quiz.

---

### Day 5 · 「客服中心」

#### D5-1 · Support: 「每天 2,000 張繁中客服單：用 LLM 要花多少？為什麼字序很重要？」 (#12, #2)
- **Ticket.** 2,000 Traditional-Chinese tickets arrive per day. Estimate the LLM cost; meaning depends on word order and context.
- **Steps.**
  - Frame: cost = tokens × price; meaning needs order.
  - Try: count the tokens of the same ticket in 繁中 and in English with 2–3 tokenizers, then estimate the monthly bill.
  - Open, as the **~1h sequence→attention bridge** confirmed in CLAUDE.md:
    1. Bag-of-words fails on 「不是不好」.
    2. An RNN reads word by word and hits a memory bottleneck.
    3. Seq2seq squeezes a whole sentence into one vector.
    4. Attention looks back at every word and weights them, a soft lookup.
  - Adapt: compute attention by hand on a toy sentence.
  - Measure: does attention focus on the right words?
  - Ship: a cost-estimate note.
- **★**
  - BPE and tokens in code.
  - The token cost of 繁中.
  - Embeddings as a lookup table, with similar words close together.
  - Why order matters.
  - The RNN (one diagram) and its bottleneck; the seq2seq bottleneck.
  - Attention as a soft lookup: query vs keys → dot product → softmax weights → weighted sum of values. Single head; Q, K and V named.
  - Why we scale by √d (one line).
- **○** LSTM/GRU gates (named only; on the official roadmap but not taught in DL).
- **△** The history of Bahdanau attention.
- **Recall.** Vibe 01 (tokens, context window, attention as an N×N cost); DL pp.7, 29 (RNN mentioned); DL pp.16, 25–27 (softmax, cross-entropy).
- **Lab L5-1.** A token-cost calculator, plus attention from scratch on toy sentences with a heatmap.
- **Risk.** 個資法: never send real customer tickets to a free-tier API.

#### D5-2 · Support: 「模型到底怎麼『寫』出一封回覆？」 (#12, #13, #2)
- **Ticket.** Understand how a model writes a reply before trusting it with customers.
- **Steps.**
  - Frame: writing = predicting the next token, over and over.
  - Try: inspect a real 0.5–1.5B model's top-k next tokens for a ticket.
  - Open: the Transformer block and the decoder-only GPT.
  - Adapt: train a mini character-level GPT on synthetic 繁中 replies.
  - Measure: the loss curve; sample quality vs temperature, top-k and top-p.
  - Ship: a sample sheet.
- **★**
  - Multi-head attention.
  - The causal mask.
  - Positional encoding: sinusoidal, with RoPE named. It refers back to the D3-3 time embedding.
  - Residual connections + LayerNorm.
  - The encoder / encoder–decoder / decoder map: BERT, T5, GPT.
  - Next-token cross-entropy = **maximum likelihood**, in words (DL pp.25–27).
  - Temperature, top-k, top-p.
  - The KV cache: why generation speeds up.
  - The DiT payoff: 「現在換 Transformer 來畫圖」 (links to D4-2).
- **○** GQA/MQA (named only); the context window and its cost.
- **△** The complexity math of attention.
- **Recall.** D5-1; DL pp.25–27 (cross-entropy); DL pp.69–71 and D1-2 (temperature, sampling).
- **Lab L5-2.** A mini character-level GPT on synthetic 繁中 replies, plus the top-k logits of a real small model.
- **Risk.** Fluent ≠ correct (hallucination preview).

#### D5-3 · IT/Legal: 「雲端 API 還是自架模型？成本、個資法、延遲」 (K6, goal 9)
- **Ticket.** Choose between a cloud API and a self-hosted open model for ticket triage.
- **Steps.**
  - Frame: the decision table: cost, privacy (個資法), licence, latency, quality.
  - Try: one SDK call with messages, a system prompt and parameters; read the token usage and compute the cost.
  - Open: quantisation means fewer bits per weight and less VRAM (bytes per parameter, recall D1-4).
  - Adapt: run the same triage prompt on HF at fp16 and at 4-bit. Ask for JSON in the prompt and validate it with `json.loads`.
  - Measure: quality (rubric), latency, cost per 1,000 tickets.
  - Ship: the triage assistant (**Day 5 ship**).
- **★**
  - Anatomy of an SDK call: messages, roles, system prompt, temperature, max tokens; the API key from `.env`.
  - Token usage and cost.
  - JSON via the prompt + `json.loads` + retry on failure.
  - `transformers` `generate`.
  - Chat templates (preview of D5-4).
  - 4-bit loading and VRAM arithmetic.
  - The open vs closed decision table.
- **○** Ollama/GGUF on a laptop (instructor demo); latency and time-to-first-token.
- **△** Quantisation formats (NF4, GPTQ, AWQ) named.
- **Named only and deferred to the Agent module:** streaming, schema-enforced output, tool calling.
- **Recall.** Vibe 11–12 (`requests`, JSON, `.env`); D1-4 (VRAM rule of thumb); DL pp.67–72 (compression).
- **Lab L5-3.** The same triage task three ways on synthetic tickets: cloud API, HF fp16, 4-bit.
- **Risk.** Data residency and 個資法; free-tier prompt reuse; open-weight licences differ even between sizes of the same model family.

#### D5-4 · Support: 「模型回覆混進簡體字和大陸用語，格式也不聽話」 (K5, K7, K9)
- **Ticket.** Replies drift into Simplified characters and mainland usage, and ignore the JSON format.
- **Steps.**
  - Frame: how LLMs are trained explains this behaviour.
  - Try: prompt fixes first (system prompt, examples).
  - Open: pretrain → SFT → RLHF/DPO → reasoning RL. 繁中 drift comes from the training data mix.
  - Adapt: QLoRA SFT on a small dataset of 繁中台灣用語 + JSON.
  - Measure, before and after on an eval set:
    - LLM-as-judge (with its biases);
    - the rate of Simplified characters;
    - the rate of valid JSON.
  - Ship: the adapter and an eval report.
- **★**
  - The training-pipeline picture.
  - SFT data format and chat templates.
  - The decision guide: prompting vs RAG vs fine-tuning (RAG belongs to the later modules).
  - QLoRA = a 4-bit base model + LoRA adapters (recall D4-3).
  - T4 configuration: fp16 compute, short sequences, pinned versions.
  - Eval-set design.
  - LLM-as-judge and its biases.
  - Hallucination.
- **○** Scaling laws and MoE (concept); reasoning models, i.e. "thinking" trained with RL (prompting methods such as CoT/ToT belong to Agent #2).
- **△** The DPO objective.
- **Recall.** D4-3 (LoRA); D5-3; ML pp.9–10 (the habit of evaluating).
- **Lab L5-4.** QLoRA on a 0.5–1.5B instruct model, with a before/after eval.
- **Risk.** Prompt injection preview (tickets can contain instructions); LLM-judge bias.

**Day 5 homework.** Improve the triage assistant, driven by the eval; build the capstone; iPAS-style quiz.

---

### Day 6 · 「上市與交付」

#### D6-1 · Marketing: 「活動影片需要免版稅配樂和旁白」 (#14 → MusicGen)
- **Ticket.** Campaign videos need royalty-free background music and a Mandarin voice-over.
- **Steps.**
  - Frame: licensing is the real constraint.
  - Try: MusicGen-small text-to-music.
  - Open: the waveform becomes EnCodec tokens (D2-4), and a Transformer predicts audio tokens like words (D5-2), with text and melody conditioning.
  - Adapt: prompt and duration sweeps.
  - Measure: a listening test; generation time vs clip length.
  - Ship: a jingle with a licence note.
- **★**
  - Audio basics: sample rate, waveform, spectrogram (picture).
  - Codec tokens (EnCodec, D2-4).
  - MusicGen = a Transformer over audio tokens with text conditioning.
  - Why syllabus item 「MusicNet」 became MusicGen: MusicNet is a dataset.
  - A TTS overview: text → acoustic tokens → waveform.
  - **The licence lesson:** MusicGen's weights are non-commercial.
  - Consent for voice cloning.
- **○** Melody conditioning; commercial-friendly alternatives (terms to verify).
- **△** Codebook interleaving (the delay pattern).
- **Recall.** D2-4 (EnCodec, VQ); D5-2 (GPT).
- **Lab L6-1.** MusicGen-small jingles with sweeps, plus a TTS demo with a model that speaks Taiwanese Mandarin (licence to verify).
- **Risk.** Music copyright; voice consent; deepfake audio.

#### D6-2 · E-commerce: 「一萬張沒有標籤的商品照，顧客用中文搜尋」 (K8)
- **Ticket.** 10,000 untagged product photos, and customers search in 繁中.
- **Steps.**
  - Frame: search by meaning, not by filename.
  - Try: zero-shot tagging with a multilingual CLIP-class model.
  - Open: contrastive embeddings (recall D4-2) put images and text in one space, compared by cosine similarity.
  - Adapt: build an in-memory text→image search; generate alt-text with a VLM.
  - Measure: precision@k on a small labelled set; quality of 繁中 captions.
  - Ship: a search app.
- **★**
  - Applied CLIP: embed the catalog, embed the query, cosine similarity, top-k.
  - Zero-shot classification with text prompts.
  - Choosing a multilingual model: the SigLIP 2 class; OpenAI CLIP is English-only.
  - VLM captioning (image → text) for alt-text and SEO.
  - precision@k.
- **○** A video-generation overview; image-to-video.
- **△** Vector databases (Text-to-SQL module).
- **Recall.** D4-2 (CLIP); D5-2 (Transformer).
- **Lab L6-2.** Catalog search, zero-shot tags and VLM alt-text.
- **Risk.** Bias in zero-shot tags; misleading auto-captions.

#### D6-3 · Compliance & Ops: ship clinic (K9, K10, goals 9/11)
- **Ticket.** Before launch, every prototype must pass a compliance checklist and be demo-ready.
- **First 30 minutes: the compliance checklist (★).**
  - Licences of code, weights and data.
  - Copyright and consent.
  - Deepfake and AI-content disclosure.
  - Watermarking and C2PA.
  - 個資法 and AI 基本法 (status to verify).
  - Prompt injection.
  - Cost and latency budget.
  - Edge notes: quantisation and distilled models (goal 9).
- **Remaining 90 minutes: individual build with instructor help (★).** Package the capstone:
  - a Gradio app;
  - a model card;
  - a **GitHub remote push** (goal 11; local Git was taught in Vibe 02 and 07a);
  - an HF Hub push or a Colab share link.
- **○** HF Spaces (free-tier limits).
- **△** Monitoring in production (Agent #10).
- **Lab L6-3.** Capstone build.

#### D6-4 · CEO office: demo day (all)
- **Format.** 3 minutes per student: ticket → model choice → live demo → one metric → one risk or cost.
  - With a large class, students submit a 3-minute screen recording and a selection is shown live (class size is an open item).
- **★**
  - The demos.
  - Submitting the 學習評量 (memo + notebook; the oral CFG check if not done yet).
  - The final iPAS-style quiz.
  - A course recap built on the six-step loop and the trilemma.
  - The hand-off: tool calling, MCP and RAG are named as the next module.

---

## 8. Syllabus coverage matrix

| Official item | Main session(s) | Also in |
|---|---|---|
| #1 Introduction to Generative AI | D1-1, D1-2 | D6-4 recap |
| #2 GAI 必要的數學基礎 | Just-in-time; see §11 | — |
| #3 AutoEncoder 工作原理與實作 | D2-1 | D2-3, D2-4 |
| #4 U-net 原理與實作 | D2-2 | D3-3, D4-2 |
| #5 VAE 原理與實作 | D2-3 | D4-2 |
| #6 VQ-VAEs 實作 | D2-4 | D6-1 |
| #7 Diffusion 模型工作原理 | D3-3 | D3-4, D4 |
| #8 Anomaly detection 使用 Diffusion 模型 | D3-4 | D2-1 (AE baseline) |
| #9 Conditional Diffusion 模型工作原理 | D4-1 | D4-2, D4-3 |
| #10 GAN 原理與實作 | D3-1 | D4-4 |
| #11 CycleGAN 原理與實作 | D3-2 | D4-4 |
| #12 Transformer 原理與實作 | D5-1, D5-2 | D6-1 |
| #13 Transformer 應用於文字生成-GPT | D5-2 | D5-3, D5-4 |
| #14 音樂生成-MusicNet (→ MusicGen) | D6-1 | D2-4 |
| Goal 8 生成式 AI 模型進行影像處理與應用 | D2–D4 | D6-2 |
| Goal 9 輕量化模型、Edge | D5-3, D6-3 | D1-4, D4-4 |
| Goal 10 iPAS AI 應用規劃師 | D1-1 (導入評估/規劃), D6-3 (風險管理), daily quizzes | Memo |
| Goal 11 版本控制 | D6-3 (GitHub remote) | — |
| 學習評量: 說明 Diffusion 與 GAN 差異 | Memo started D4-4, submitted D6-4 | Evidence from D3-1, D3-3, D4-1 |
| 學習評量: 實作條件生成 | D4-1 notebook | Oral or no-AI check |

**iPAS mapping (goal 10, to verify).** According to secondary sources:
- 初級 科目二 生成式AI應用與規劃 covers No/Low Code, common GenAI tools, 導入評估, 導入規劃 and 風險管理. This maps onto D1-1, D6-3 and the memo.
- 科目一's 鑑別式 vs 生成式 AI basics map onto D1-1.

The official indicator page returned 404 on 2026-11-22, so check against the official 學習指引 before writing the quiz questions.

---

## 9. Lab inventory

### 9.1 Labs

Mode:
- **T** = Try (pretrained pipeline)
- **O** = Open (from scratch)
- **C** = instructor checkpoint used

| Lab | Mode | Data | Model | T4 configuration and fallback | Watch-outs |
|---|---|---|---|---|---|
| L1-1 | — | Ticket briefs | — | No GPU | — |
| L1-2 | T | Course briefs | Small open instruct LLM (Apache-2.0 class); SD1.5 mirror + LCM-LoRA; one cloud API | fp16; open-model fallback without a key | Avoid non-commercial SDXL-Turbo in labs |
| L1-3 | O | CIFAR-10 (torchvision) | LabDay3-2 CNN in PyTorch | Small; fast | Compare with the Keras accuracy |
| L1-4 | O/T | CIFAR-10 | L1-3 model + one Hub model | Drive checkpoints | Disk space for the HF cache |
| L2-1 | O (C) | VisA, one PCB category, good-only training | Conv AE | Low resolution; instructor checkpoint | Confirm the AE baseline works at the chosen resolution |
| L2-2 | O (C) | VisA good images + synthetic defects; real VisA masks for testing | U-Net | Instructor-prepared test split | Procedural textures only (no unlicensed texture sets) |
| L2-3 | O + T | Fashion-MNIST; one product photo | VAE; SD `AutoencoderKL` | Small VAE; SD VAE in fp16 | Photo owned or CC0 |
| L2-4 | T + O | Synthetic support-call audio; Fashion-MNIST | EnCodec 24 kHz; tiny VQ-VAE | EnCodec inference only | No real customer audio |
| L3-1 | O + T | Fashion-MNIST; legacy-style low-res photos | DCGAN; Real-ESRGAN | Small DCGAN | `basicsr` breaks with torchvision ≥ 0.17: pin or patch, or use another loader |
| L3-2 | O (C) | VisA + synthetic Line-B shift | CycleGAN (reference implementation) | 64–128px, short run; snapshots from several epochs | Check that defects survive translation |
| L3-3 | O (C) | Fashion-MNIST | Tiny DDPM, small U-Net provided | 28–32px; fallback checkpoint | — |
| L3-4 | C | L2-1 VisA category | DDPM trained by the instructor | Low resolution; few test images | Measure throughput honestly |
| L4-1 | O (C) | Fashion-MNIST | Class-conditional DDPM + CFG (warm start from L3-3) | Fallback checkpoint | FID/KID settings for small sample sizes |
| L4-2 | T | Text briefs; product photos | SD1.5 mirror, SD1.5 inpainting; ControlNet demo | fp16 | Original runwayml repo was removed; pin a mirror and check hashes |
| L4-3 | T + O | About 10 photos the students took | IP-Adapter; DreamBooth-LoRA on SD1.5 | 512px, gradient checkpointing, 8-bit Adam; SDXL as demo only | Consent and IP of training images |
| L4-4 | T | One seasonal product photo | Pretrained CycleGAN; InstructPix2Pix; SD1.5 + LCM-LoRA; 2D toy | 2D toy on CPU | Licence comparison |
| L5-1 | O | Synthetic 繁中 tickets | 2–3 tokenizers; attention from scratch | CPU is fine | — |
| L5-2 | O + T | Synthetic 繁中 replies (course-made corpus) | Mini character-level GPT; a 0.5–1.5B open model | Small GPT; fallback checkpoint | — |
| L5-3 | T | Synthetic 繁中 tickets | Cloud API; HF fp16; 4-bit (bitsandbytes) | 4-bit on T4 to verify | Synthetic data only |
| L5-4 | O | Synthetic SFT set (繁中台灣用語 + JSON) | QLoRA on a 0.5–1.5B instruct model | fp16 compute (no bf16 on T4), short sequences, pinned `trl`/`peft`/`bitsandbytes` | — |
| L6-1 | T | Prompts | MusicGen-small; a Taiwanese-Mandarin TTS model | Inference only | Non-commercial MusicGen weights (see §14) |
| L6-2 | T | Course product-photo set | Multilingual CLIP-class (SigLIP 2 class); a small VLM | fp16 | Check the VLM's 繁中 output and fp16 stability |
| L6-3 | — | Capstone | Student's choice | — | Free HF Spaces limits; the Colab share link is the default |

No timings or VRAM numbers are given here on purpose. Each lab gets measured on a real Colab T4 during production, and the numbers are recorded in that deck's `research/lab-runs.md` (CLAUDE.md, Slides).

**Lab conventions** follow `demo-and-practice` §3b–3d:
- each lab has a student notebook `labNN-<topic>.ipynb` and a finished `-solution.ipynb`;
- the first cell pins versions and prints the GPU name and free VRAM;
- every lab has a fallback for no GPU quota, no agent quota, a disconnect and a package break;
- each lab follows the 7-page lab sequence; the PyTorch bridge (D1-3) and the sequence→attention bridge (D5-1) use the simpler 3-page pattern.

### 9.2 Licence notes

These are as reported on 2026-11-22. **Verify every row against the official licence before production.**

| Asset | Reported licence | Use in this course |
|---|---|---|
| VisA (PCB1–4, pixel masks) | CC BY 4.0 | Main factory dataset |
| MVTec AD | CC BY-NC-SA 4.0 | Licence example only (non-commercial; a grey zone in a paid course) |
| DeepPCB | MIT badge, but the README says "research only" | Example of an ambiguous licence |
| Fashion-MNIST | MIT | Small from-scratch labs |
| SD1.5 (community mirror) | CreativeML OpenRAIL-M | D1-2, D2-3, D4-2, D4-3 |
| LCM-LoRA (SD1.5) | openrail++ | Fast sampling (D1-2, D4-4) |
| SDXL-Turbo | non-commercial community licence | Counter-example; not used in labs |
| InstructPix2Pix | to verify | D4-4 bake-off |
| Real-ESRGAN; CycleGAN reference code | BSD | D3-1, D3-2, D4-4 |
| Qwen2.5-1.5B vs Qwen2.5-3B | Apache 2.0 vs a research licence | Shows licences can differ by model size within one family |
| OpenAI CLIP / SigLIP 2 / jina-clip-v2 | MIT (English-only) / Apache 2.0 / CC BY-NC | Choosing a model for 繁中 search |
| MusicGen weights | CC BY-NC 4.0 | D6-1; this is the licence lesson |
| EnCodec | to verify (code and weights separately) | D2-4 |
| BreezyVoice (Taiwanese-Mandarin TTS) | Apache 2.0; voice cloning needs consent | D6-1 TTS candidate |
| Stable Audio Open Small | community licence | Possible alternative to MusicGen |

---

## 10. Datasets made for the course

All of these are made synthetically by the instructor, so no real personal data is used:
- **繁中 support tickets.**
- **Replies** in 台灣用語.
- **SFT pairs.**
- **Support-call audio.**
- **The product-photo set.** Photos the instructor or students take, or CC0 images.

This keeps 個資法 out of scope, and it is safe to send to free-tier APIs.

---

## 11. Math map (syllabus #2, just-in-time)

| Math idea | Session | Business moment | Form | Reuses |
|---|---|---|---|---|
| Data distribution p_data vs model p_θ; conditional p(x\|y) | D1-1 | 「生成模型學的是『我們的產品通常長什麼樣』」 | Picture | DL pp.80–81 |
| Probability, sampling, temperature, seeds | D1-2 | 「為什麼每次文案都不一樣？要怎麼重現？」 | Bar chart + slider + code | DL pp.69–71 |
| Bytes per parameter | D1-4, D5-3 | 「我們的 GPU 跑得動嗎？要花多少？」 | Calculator cell | — |
| Likelihood as typicality; threshold; AUROC | D2-1 | 「這片板子有多『正常』？」 | Score histogram + code | ML pp.9–10 |
| Gaussian; KL as a regulariser; intractability; ELBO named | D2-3 | 「讓設計空間平滑，每一點都是合理的圖」 | Two-Gaussian picture + one annotated line + code | DL p.79 |
| Nearest-codeword snapping; straight-through gradient | D2-4 | 「把影像和聲音變成一串 token」 | Picture + code | — |
| Two-player objective; non-saturating loss | D3-1 | 「偽造者 vs 檢查員」 | Loss curves + one annotated line | DL pp.82–84 |
| Noise schedule; one-step x_t; time embedding | D3-3 | 「先把圖弄髒，再學會還原」 | Strip x₀…x_T + one annotated line + code | — |
| Guidance as mixing two predictions; FID/KID | D4-1 | 「要多嚴格照著指定類別畫？」 | One annotated line + scale grid | — |
| Cosine similarity; CLIP score | D4-2 | 「文字和圖片怎麼比相似度？」 | Code cell | ML pp.64–67 (vectors) |
| Low-rank update | D4-3 | 「便宜地微調大模型」 | W + B·A picture + parameter count | — |
| Dot-product attention; softmax weights | D5-1 | 「這張客服單哪些字最重要？」 | Heatmap + tiny matrix | DL p.16 (softmax) |
| Cross-entropy = maximum likelihood | D5-2 | 「模型怎麼學會寫字」 | Loss curve | DL pp.25–27 |
| Contrastive embeddings (applied) | D6-2 | 「用文字搜尋商品照」 | Similarity-matrix picture | D4-2 |

**Excluded on purpose** (△ appendix slides only):
- the ELBO derivation via Jensen's inequality;
- SDEs and score matching;
- the Bayes-rule derivation of classifier guidance;
- the DPO objective;
- rectified-flow math;
- scheduler math.

---

## 12. Assessment

| Component | When | Purpose | Notes |
|---|---|---|---|
| Daily homework | D1–D5 | Formative practice | Colab notebooks with self-checks where possible |
| iPAS-style quiz | End of every day | Goal 10 | 5–10 multiple-choice questions per day, written in the slide plan |
| **學習評量 (a): memo to the CTO** | Started D4-4, submitted D6-4 | Official: 說明 Diffusion 與 GAN 差異 | 1–2 pages; see the brief below |
| **學習評量 (b): conditional generation** | D4-1 (lab), submitted D6-4 | Official: 實作條件生成 | L4-1 notebook plus a no-AI written or 3-minute oral "explain your CFG line" |
| Capstone | Ticket chosen D4-4; built D5–D6 and in D6-3; demo D6-4 | Integration | **Individual**: Gradio demo + one-page memo + 3-minute demo |

**Memo brief.** Recommend GAN or diffusion for the D4-4 bake-off task. Compare them on the trilemma (quality, diversity, speed) plus training stability and controllability. Cite evidence from your own labs:
- L3-1 sample grids and mode collapse;
- L3-3 and L4-1 samples and FID/KID;
- L4-4 timings and the preference ratings.

**Proposed rubrics** (weights are a suggestion for the instructor to change):

| Memo | Weight |
|---|---|
| Correct comparison of GAN vs diffusion | 40% |
| Evidence from own labs | 30% |
| Clear business recommendation | 20% |
| Risks and licences | 10% |

| Capstone | Weight |
|---|---|
| Business framing (ticket, KPI) | 20% |
| Technical soundness | 25% |
| Measurement (business + technical metric) | 20% |
| Risk and licence awareness | 15% |
| Demo and communication | 20% |

---

## 13. Hand-off to later modules

| Topic | Where GAI stops | Who continues |
|---|---|---|
| LLM API | One SDK call, token cost, JSON via prompt + `json.loads` | Agent #3 (structured output control), #4 (APIs, tool calling) |
| Streaming, schema-enforced output, tool calling, MCP | Named only | Agent #4, #5 |
| Prompt engineering in depth; CoT/ToT/GoT | Basic prompting; reasoning models as a *training stage* (D5-4) | Agent #2, #3 |
| Transformer and LLM internals | Taught in D5-1/D5-2 | Agent #1 should build on them rather than repeat them (agree with that instructor) |
| RAG, embeddings at scale, vector databases | In-memory cosine search only (D6-2) | Agent #9; Text-to-SQL module |
| Multi-agent systems, deployment, monitoring | Gradio demo + share link | Agent #10 |
| Capstone prototypes | One-ticket prototype | 學員結訓AI專題製作輔導 (64hr) may extend them |

---

## 14. Risks and open items

- [ ] **K6 boundary with the Agent module.** D5-3 overlaps Agent #3 and #4; Agent #1 overlaps D5-1/D5-2. Agree the split with that instructor (also an open item in curriculum-analysis.md).
- [ ] **Cloud-LLM access.** Will students use a free tier or an instructor key? The labs must still work with the open-model fallback.
- [ ] **Non-commercial assets in a paid course.** Ask 艾鍗 whether NC-licensed data and weights may be used in class.
  - The default plan avoids them where a permissive option exists: VisA over MVTec AD, LCM-LoRA over SDXL-Turbo.
  - MusicGen is the exception. If NC weights are not acceptable, the instructor demos it and students use a permissive alternative (terms to verify).
- [ ] **T4 feasibility, measured in production.** Diffusion anomaly detection, CycleGAN, DreamBooth-LoRA, QLoRA, the Real-ESRGAN install, and the VisA AE at the chosen resolution. Every risky lab has an instructor checkpoint.
- [ ] **Free-GPU quota.** Colab quotas can run out on the heavy days (D3–D4). Kaggle is the backup, and GPUs should be switched on only when needed.
- [ ] **Hosting.** HF Spaces free tiers may not run GPU demos, so the Colab share link is the default.
- [ ] **Local law.** Verify the status of the AI 基本法 and the anti-fraud ad-disclosure article before writing slides.
- [ ] **iPAS mapping.** Check against the official 學習指引 (the indicator page returned 404).
- [ ] **Company name** (曜嶼電子 is a placeholder).
- [x] **Slide format:** decided 2026-11-22. Slidev in the Vibe Coding style (CLAUDE.md, Slides).
- [ ] **Deck split.** One deck per day or one per session? The slide plan proposes it.
- [ ] **Delivery channel.** How do students receive slides and notebooks? The Vibe Coding student site is not ported yet (CLAUDE.md).
- [ ] **Class size.** It decides whether D6-4 demos are live or recorded.
- [ ] **Calendar.** Are the six days consecutive 8-hour days? If so, D6-3's capstone build time is essential.
- [ ] **TensorFlow mandate.** Confirm with 艾鍗 that TensorFlow is not required program-wide (existing item).

---

## 15. Next step: the slide-by-slide plan

After this roadmap is approved, write one file per day:

```
planning/slide-plan/
├── D1-value-and-tooling.md
├── D2-factory-qa.md
├── D3-gan-vs-diffusion.md
├── D4-image-studio.md
├── D5-support-desk.md
└── D6-launch-and-ship.md
```

Each file has a day goal. Each session in it has:
- the ticket card, written in Traditional Chinese;
- the session objectives;
- the slide list;
- the lab spec: steps, expected outputs, checkpoints, no-AI checkpoint, fallback;
- the Measure & Risk slide;
- the homework;
- iPAS-style questions.

Fields for each slide:

| # | Title | ★/○/△ | Objective | One-sentence takeaway | Content | Visual / example | Lab hook | Prior-knowledge cite | Source |
|---|---|---|---|---|---|---|---|---|---|

The target is about 15–20 slides per 2-hour session, with one teaching point per slide; the count is set in the slide plan. The appendix (△) slides that hold the derivations are listed separately at the end of each day.

**How the slide plan feeds production:**
- The slide plan stays in English, like the rest of `planning/`.
- It proposes the deck split; each deck is created with `npm run new-deck`.
- Each deck's Traditional-Chinese `outline.md` (template: `templates/deck/outline.md`) is filled from the slide plan and approved before any `slides.md` is written.
- Slide counts include the lab page sequence (`demo-and-practice` §3c) and the hidden answer pages.

---

## Appendix A. Coverage check against curriculum-analysis.md

Every "Not yet taught" point from K1–K10, and every prerequisite gap, is mapped to a session. The session's ★/○/△ marking is shown.

| Area | Point | Session |
|---|---|---|
| K1 | Generative vs discriminative | D1-1 ★ |
| K1 | p_data vs p_θ | D1-1 ★ |
| K1 | Likelihood and MLE | D2-1 ★ (typicality), D5-2 ★ (MLE = cross-entropy), D1-3 ○ (Gaussian fit) |
| K1 | KL divergence | D2-3 ★ |
| K1 | Latent variables; why log p(x) is intractable | D2-3 ★ (words) |
| K1 | ELBO | D2-3 ★ (named, code); derivation △ |
| K1 | 2026 landscape (LLM, diffusion/flow, multimodal, agents, open vs closed) | D1-1 ★ |
| K2 | ConvTranspose vs upsampling | D2-1 ★ |
| K2 | U-Net with skip concatenation | D2-2 ★ |
| K2 | VAE reparameterisation, ELBO loss in code | D2-3 ★ |
| K2 | Latent interpolation | D2-3 ★ |
| K2 | VQ-VAE codebook, commitment loss, straight-through estimator | D2-4 ★ |
| K2 | Discrete tokens as the bridge to LLM-style generation | D2-4 ★, D6-1 ★ |
| K2 | AE reconstruction error for anomaly detection | D2-1 ★ |
| K3 | DDPM forward/reverse, schedule, closed-form x_t, predict noise, sampling loop | D3-3 ★ |
| K3 | DDIM and fast samplers | D3-4 ★, D4-4 ★ |
| K3 | Conditioning by concatenation | D4-2 ★ (inpainting) |
| K3 | Classifier guidance | D4-1 ★ (1 slide); derivation △ |
| K3 | Classifier-free guidance | D4-1 ★ |
| K3 | Latent diffusion and SD architecture (VAE + U-Net/DiT) | D4-2 ★; DiT D5-2 ★ |
| K3 | Flow matching / rectified flow | D4-4 ★ (intuition) |
| K3 | Diffusion for anomaly detection and repair | D3-4 ★ |
| K3 | `diffusers`: pipelines, schedulers, seeds, negative prompts, img2img, inpainting | D1-2 ★, D4-2 ★ |
| K3 | ControlNet / IP-Adapter | D4-2 ○ (ControlNet demo), D4-3 ★ (IP-Adapter) |
| K4 | Adversarial objective | D3-1 ★ |
| K4 | Saturating vs non-saturating G loss | D3-1 ★ |
| K4 | Instability, mode collapse, DCGAN rules | D3-1 ★ |
| K4 | CycleGAN: unpaired, cycle-consistency, identity loss, PatchGAN | D3-2 ★ |
| K4 | Where adversarial losses live on (ESRGAN, VAE decoder, ADD/Turbo, HiFi-GAN/EnCodec) | D3-1 ★, D4-4 ★ |
| K5 | Sequence modelling → why attention (~1h bridge) | D5-1 ★ |
| K5 | Token embeddings | D5-1 ★ |
| K5 | Scaled dot-product attention (Q/K/V) | D5-1 ★ |
| K5 | Multi-head attention, causal mask | D5-2 ★ |
| K5 | Positional encoding (RoPE) | D5-2 ★ (sinusoidal), RoPE named |
| K5 | BPE tokenisation in code | D5-1 ★ |
| K5 | Decoder-only GPT | D5-2 ★ |
| K5 | Temperature, top-k, top-p | D1-2 ★, D5-2 ★ |
| K5 | KV cache | D5-2 ★ |
| K5 | Scaling laws, MoE | D5-4 ○ |
| K5 | Pretrain → SFT → RLHF/DPO → reasoning RL | D5-4 ★ |
| K6 | Calling an LLM API from Python | D1-2 ★, D5-3 ★ |
| K6 | Messages and parameters | D5-3 ★ |
| K6 | Streaming | Named only (Agent module) |
| K6 | Token counting and cost | D5-1 ★, D5-3 ★ |
| K6 | Basic JSON output | D5-3 ★ |
| K6 | Open-weight models: HF on Colab | D1-2 ★, D5-3 ★ |
| K6 | Open-weight models: Ollama | D5-3 ○ |
| K6 | Quantisation (4-bit, GGUF) and VRAM arithmetic | D1-4 ★ (rule of thumb), D5-3 ★ (4-bit), GGUF ○ |
| K6 | Open vs closed models | D5-3 ★ |
| K6 | Hand-off to the Agent module | D5-3, D6-4 ★ |
| K7 | Full fine-tuning vs LoRA/QLoRA; why it fits a T4 | D4-3 ★, D5-4 ★ |
| K7 | Dataset formatting, chat templates | D5-4 ★ |
| K7 | LoRA for diffusion (DreamBooth-lite) | D4-3 ★ |
| K7 | Prompting vs RAG vs fine-tuning | D5-4 ★ |
| K8 | CLIP contrastive embeddings, cosine similarity in code | D4-2 ★, D6-2 ★ |
| K8 | Vision-language models | D6-2 ★ |
| K8 | Text-guided image editing | D4-4 ★ |
| K8 | Video generation overview | D6-2 ○ |
| K8 | Audio tokens / codecs | D2-4 ★ |
| K8 | MusicGen; TTS overview | D6-1 ★ |
| K9 | FID, CLIP score, human preference | D4-1 ★, D4-2 ★, D4-4 ★ |
| K9 | LLM test sets, LLM-as-judge | D5-4 ★ |
| K9 | Hallucination | D1-1, D5-2, D5-4 ★ |
| K9 | Bias | D4-2 ★, D6-2 ★ |
| K9 | Model licences and copyright | D1-2, D1-4, D2-1, D4-2, D4-4, D6-1, D6-3 ★ |
| K9 | Provenance and watermarking (C2PA) | D4-2 ★, D6-3 ★ |
| K9 | Prompt-injection awareness | D5-4 ★, D6-3 ★ |
| K9 | Cost and latency budgeting | D3-4 ★, D5-1 ★, D5-3 ★, D6-3 ★ |
| K10 | Gradio demo | D1-4 ★, daily |
| K10 | HF Hub (model cards, licences, safetensors) | D1-4 ★ |
| K10 | HF Spaces | D6-3 ○ |
| K10 | Distilled fast generators linked to DL distillation | D4-4 ★ |
| K10 | Quantisation and size budgets for edge | D5-3 ★, D6-3 ★ |
| Gap | PyTorch bridge (~2hr) | D1-3 ★ (+ D1-4 workbench) |
| Gap | Probability, MLE, KL, ELBO | Just-in-time (§11) |
| Gap | Sequence → attention (~1hr) | D5-1 ★ |
| Gap | HF and GPU-memory practice (~1hr) | D1-4 ★ |
| Gap | Vectors, dot product, cosine similarity | D4-2 ★, D5-1 ★ |
| Gap | CHW vs HWC, broadcasting | D1-3 ★ / ○ |
| Gap | Decorators (`@torch.no_grad`) | D1-3 ★ (at first use) |
| Gap | `.env` secrets, JSON | D1-2 ★, D5-3 ★ |
| Gap | Git remote (GitHub) | D6-3 ★ |
| Gap | Prompt clarity, system vs user | D1-2 ○, D5-3 ★ |
