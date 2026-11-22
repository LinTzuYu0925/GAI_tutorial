# 生成式AI原理 (48hr): Curriculum Gap Analysis

This is a planning input for building the GAI slide decks. It answers four questions:

1. What should be taught so that students understand frontier Generative AI (as of late 2026)?
2. For each key point, which parts were already taught in earlier modules, and which are new?
3. What background knowledge does the class require?
4. Was that background taught?

**Design stance:** the course trains working *AI 代理人與自動化工程師*. Every key point therefore pairs the core idea with a **hands-on lab that runs on Google Colab (T4)**. Labs use **PyTorch + Hugging Face**.

**Order constraint:** the GAI module runs **before** the Agent 自動化實務 module. GAI must therefore introduce basic LLM API usage. Tool calling, MCP, RAG and multi-agent work are left to the Agent module.

---

## 0. Evidence base

| Module | Source | How it was read | Notes |
|---|---|---|---|
| Course roadmap and goals | [references.md](../references/references.md), official brochure (課程簡章) | Full text | 12 course goals; 14 GAI syllabus items |
| Vibe Coding: AI 協作 Python 開發 (48hr) | `C:\Users\lspss\Documents\Vibe_coding_python`, 17 Slidev decks | Full text | Decks 11–13 were planned for the last two days (see open items) |
| 數據分析代理人實務 (24hr, Wei) | Google Drive PDF, 81 pp | Full text via Drive viewer | **Content differs from the brochure** (see below) |
| 機器學習 (32hr, Alan) | Google Drive PDF, 78 pp | Full text via Drive viewer | Optimiser slides are image-only, so only their titles were readable |
| 深度學習 (40hr, Wei) | Google Drive PDF, 97 pp | Full text via Drive viewer | **Content differs from the roadmap** (see below) |
| Prior GAI offering | [4_02_GAI_20240901_.pdf](../references/4_02_GAI_20240901_.pdf), 88 pp | Full text | Keras; content from roughly 2020–22 |

Legend: ✅ taught (verified in slides) · 🔹 introduced at concept or overview level only · ❌ not taught

### ⚠️ Two places where the slides do not match the official roadmap

1. **The 深度學習 slides contain no RNN, LSTM or Seq2Seq lessons.** The roadmap lists RNN/LSTM, the KKTV prediction case, Seq2Seq and translation, but the deck only mentions RNN and Transformer in passing (pp. 7, 29).
   - The deck instead teaches: YOLOv8 with a GUI (pp. 56–62); model compression and knowledge distillation (pp. 67–72); **intro-level AE, U-Net and VAE (pp. 72–79)**; and a GenAI overview covering GPT next-token training, GAN and diffusion (pp. 80–87).
   - So students have **already seen AE, U-Net, VAE, GAN and diffusion at concept level**, but have **no sequence-model background** for the Transformer.
2. **The 數據分析代理人實務 slides are a data analysis and visualisation course.** They cover pandas, outliers, seaborn/pyplot, plotly express, sklearn performance plots and Plotly Dash, plus two "AI agent" collaboration exercises (pp. 62–63). There is **no PandasAI, SQL or LLM API**, even though the brochure lists them.

---

## 1–2. Key points: what has been taught vs what is new

### Syllabus mapping (official item → key point)

Every official item is covered. Items marked *(updated)* are taught with a 2026-relevant scope.

| # | Official syllabus item | Key point |
|---|---|---|
| 1 | Introduction to Generative AI | K1 |
| 2 | GAI 必要的數學基礎 | K1 (plus the prerequisite refresher in §3) |
| 3 | AutoEncoder 工作原理與實作 | K2 |
| 4 | U-net 原理與實作 | K2 (and as the diffusion backbone in K3) |
| 5 | VAE 原理與實作 | K2 |
| 6 | VQ-VAEs 實作 | K2 |
| 7 | Diffusion 模型工作原理 | K3 |
| 8 | Anomaly detection 使用 Diffusion 模型 | K3 (plus AE-based anomaly detection in K2) |
| 9 | Conditional Diffusion 模型工作原理 | K3 *(updated: CFG, latent diffusion, flow matching)* |
| 10 | GAN 原理與實作 | K4 |
| 11 | CycleGAN 原理與實作 | K4 |
| 12 | Transformer 原理與實作 | K5 |
| 13 | Transformer 應用於文字生成-GPT | K5, K6 *(updated: LLM training pipeline, practical usage)* |
| 14 | 音樂生成-MusicNet | K8 *(updated: MusicNet is a dataset; use MusicGen / audio tokens)* |
| — | Course goal 8 「生成式 AI 模型進行影像處理與應用」 | K3, K7, K8 |
| — | Course goal 9 (lightweight models, Edge) | K10 |
| — | 學習評量: 說明 Diffusion 與 GAN 差異並實作條件生成 | K3 + K4 |

Extensions beyond the official list (K6, K7, K9, K10) are what make the module practical for engineers.

---

### K1. GenAI foundations and the probabilistic view (#1, #2)

| | |
|---|---|
| **Already taught** | ✅ DL pp. 80–81: GenAI overview; GPT as "guess the next word" · ✅ ML pp. 42–43: logistic regression, a discriminative model with sigmoid · ✅ DL pp. 25–27: MSE vs cross-entropy · 🔹 Vibe 01: an LLM as next-token sampling |
| **Not yet taught** | Generative vs discriminative as a formal contrast; p_data vs p_θ; **likelihood and MLE**; **KL divergence**; latent variables and why log p(x) is intractable; **ELBO**; the 2026 landscape map (LLMs, diffusion/flow, multimodal, agents, open vs closed models) |
| **Hands-on** | Fit a Gaussian by MLE with PyTorch autograd; visualise KL between two Gaussians as the parameters move |

### K2. Representation learning: AE, U-Net, VAE, VQ-VAE (#3–#6)

| | |
|---|---|
| **Already taught** | 🔹 DL pp. 72–79: what an AE does, encoder/decoder, U-Net idea, VAE "latent as a Gaussian region" intuition, KL named · ✅ DL pp. 38–55: CNN, pooling, BatchNorm, ResNet skip connections · 🔹 DL p. 74: UpSampling |
| **Not yet taught** | **Don't re-introduce "what is an AE".** Go straight to the mechanics: ConvTranspose vs upsampling; the full U-Net architecture with skip *concatenation*; **VAE reparameterisation trick and ELBO loss in code**; latent interpolation; **VQ-VAE codebook, commitment loss and straight-through estimator** (no previous deck covers it); discrete image/audio tokens as the bridge to LLM-style generation; AE reconstruction error for **anomaly detection** (a common industrial use) |
| **Hands-on** | Fashion-MNIST: AE → VAE → VQ-VAE in PyTorch, comparing latent spaces; anomaly detection on an MVTec-style subset by reconstruction error |

### K3. Diffusion and flow models (#7–#9)

| | |
|---|---|
| **Already taught** | 🔹 DL pp. 85–87: what diffusion is, its architecture at diagram level, technical challenges |
| **Not yet taught** | DDPM forward and reverse process; noise schedule; closed-form x_t; why predict noise; the sampling loop · DDIM and fast samplers · conditioning by concatenation, classifier guidance and **classifier-free guidance (CFG)** · **latent diffusion** (VAE latent + U-Net/DiT), the Stable Diffusion architecture · **flow matching / rectified flow** (the SD3/FLUX generation) · diffusion for anomaly detection and repair · practical `diffusers` use: pipelines, schedulers, seeds and reproducibility, negative prompts, img2img, inpainting, ControlNet / IP-Adapter |
| **Hands-on** | A tiny DDPM from scratch on MNIST · a class-conditional DDPM with CFG (this covers the 學習評量 "條件生成") · `diffusers` SD 1.5 / SDXL-Turbo: compare schedulers, step counts and CFG scales |

### K4. GAN and CycleGAN (#10, #11)

| | |
|---|---|
| **Already taught** | 🔹 DL pp. 82–84: GAN's two parts (G and D) and its applications · ✅ DL: CNN classifiers (a discriminator is one) |
| **Not yet taught** | The adversarial objective; saturating vs non-saturating generator loss; training instability and mode collapse; DCGAN design rules · CycleGAN: unpaired translation, cycle-consistency and identity losses, PatchGAN · **framing for 2026:** GANs are mostly superseded for generation, but adversarial losses live on in super-resolution (ESRGAN family), VAE decoders and distilled fast samplers. Keep this shorter than in the 2024 deck |
| **Hands-on** | DCGAN on MNIST in PyTorch · run a pretrained CycleGAN or Real-ESRGAN · write-up comparing diffusion vs GAN (the 學習評量) |

### K5. Transformer and LLM internals (#12, #13)

| | |
|---|---|
| **Already taught** | 🔹 Vibe 01: tokens and token IDs, context window, attention as an N×N cost, sampling from probabilities, the Transformer figure (not explained) · 🔹 DL p. 81: GPT trained to "continue the text" · ✅ DL pp. 69–71: **softmax temperature** (in knowledge distillation) |
| **Not yet taught** | **Gap: no RNN/LSTM/Seq2Seq background.** Add a ~1hr "sequence modelling → why attention" bridge · token embeddings · **Q/K/V scaled dot-product attention**, multi-head attention, causal mask, positional encoding (RoPE) · BPE tokenisation in code · decoder-only GPT · sampling: temperature (reuse the distillation intuition), top-k / top-p · KV cache · scaling laws, MoE · the modern training pipeline: pre-train → SFT → RLHF/DPO → reasoning RL ("thinking" models) |
| **Hands-on** | Build a mini character-level GPT from scratch · load a small open model (~1–3B, e.g. Qwen/Llama/Gemma class) with HF `transformers`; inspect tokens and logits; vary sampling parameters |

### K6. Using LLMs as an engineer (extends #13; needed because GAI precedes the Agent module)

| | |
|---|---|
| **Already taught** | ✅ Vibe 11–12: `requests`, JSON, `.env` secrets with python-dotenv · ✅ Vibe 01–02: prompt clarity, system vs user prompts, writing requirements · ✅ Vibe 02–04: heavy Claude Code / Codex use *as a user* · ✅ 數據代理人 pp. 62–63: building a Dash app with an AI agent · ❌ **No LLM SDK call anywhere** |
| **Not yet taught** | Calling an LLM API from Python (Anthropic / OpenAI / Gemini SDK); messages, parameters and streaming; token counting and cost · basic structured (JSON) output · running open-weight models: HF on Colab, Ollama locally · quantisation (4-bit, GGUF) and the VRAM arithmetic behind it · choosing between open and closed models (cost, privacy, licence, latency) · **hand-off to the Agent module:** tool calling, MCP, RAG, CoT/ToT and multi-agent are named and deferred |
| **Hands-on** | Do the same task three ways: a cloud API, a full-precision HF model, and a 4-bit quantised model. Compare quality, latency and cost |

### K7. Adapting models: fine-tuning and PEFT (extension; course goal 8)

| | |
|---|---|
| **Already taught** | ✅ DL pp. 56–66: pretrained models (YOLOv8), transfer learning ("接頭霸王", attaching a new head) |
| **Not yet taught** | Full fine-tuning vs **LoRA / QLoRA**: what the low-rank update is and why it fits in a T4 · dataset formatting and chat templates · LoRA for diffusion (style or subject, DreamBooth-lite) · decision guide: prompting vs RAG vs fine-tuning |
| **Hands-on** | QLoRA on a ~1B LLM with PEFT/TRL on Colab · train a diffusion LoRA on about 10 images and compare before and after |

### K8. Multimodal and other modalities (#14, course goal 8)

| | |
|---|---|
| **Already taught** | 🔹 Vibe 01: "token vectors" / embeddings as a concept · ✅ DL pp. 57–62: YOLOv8 vision models · ✅ 數據代理人 pp. 47–49: images as 3D/4D NumPy arrays |
| **Not yet taught** | **CLIP**: contrastive text-image embeddings, and cosine similarity in code (the glue for text-to-image) · vision-language models (image → text) · text-guided image editing · a video generation overview · **audio:** audio tokens / codecs, **MusicGen** (replacing the dated "MusicNet" item), and a TTS overview |
| **Hands-on** | CLIP zero-shot classification and text→image search over a folder · MusicGen-small generation from prompts · VLM image captioning |

### K9. Evaluation, safety and responsible use (cross-cutting)

| | |
|---|---|
| **Already taught** | ✅ ML pp. 9–10: evaluation metrics (Acc, P/R/F1, AUC, MSE/MAE), K-fold CV, the habit of measuring · 🔹 Intro AI: Explainable AI · ✅ Vibe 02: "the agent says tests pass ≠ correct", a verification mindset |
| **Not yet taught** | Generative metrics: **FID, CLIP score**, human preference evaluation · LLM evaluation: test sets and LLM-as-judge · hallucination, bias · **model licences and copyright** of training data and outputs · content provenance and watermarking (C2PA) · prompt-injection awareness (a preview for the Agent module) · cost and latency budgeting |
| **Hands-on** | Compute FID and CLIP score across CFG scales · write a small LLM eval script that scores answers |

### K10. Shipping and efficiency (cross-cutting; final project and course goal 9)

| | |
|---|---|
| **Already taught** | ✅ DL pp. 67–72: model compression and knowledge distillation · ✅ DL pp. 60–61: YOLO in a GUI · ✅ 數據代理人 pp. 50–61: Plotly Dash apps · ✅ Vibe 02, 07a, 11: local Git, conda/pip · ❌ GitHub remotes, HF Hub/Spaces |
| **Not yet taught** | A Gradio demo app · HF Hub (model cards, licences, `safetensors`) and **HF Spaces** deployment · distilled fast generators (LCM / Turbo / few-step), linked to the DL distillation lesson · quantisation and size budgets for Edge deployment |
| **Hands-on** | Wrap an earlier lab (e.g. the diffusion LoRA or the QLoRA model) in Gradio and publish it to HF Spaces |

### What changes compared with the 2024 GAI deck

- **Framework:** TensorFlow/Keras → **PyTorch + Hugging Face** (`transformers`, `diffusers`, `peft`).
- **Added:** VQ-VAE, CFG done properly, latent diffusion, flow matching, Transformer/GPT internals, the LLM training pipeline, practical LLM usage, LoRA/QLoRA, CLIP and multimodal, music and audio, evaluation, deployment.
- **Trimmed:** GAN and CycleGAN (pp. 63–88 of the old deck); BEGAN dropped.
- **Labs:** 28×28 toys alone → a mix of **from-scratch models** (to understand the mechanism) and **real pipelines** (what an engineer actually uses).
- **Avoid duplicating DL:** AE, U-Net, VAE, GAN and diffusion were introduced in DL pp. 72–87. Open each topic with a one-slide recap, then go to mechanics and code.

---

## 3–4. Required background knowledge, and whether it was taught

### Math

| Background | Needed for | Status (source) | Action in GAI |
|---|---|---|---|
| Vectors, dot product, matrix multiply, cosine similarity | Attention, CLIP, embeddings | 🔹 ML pp. 64–67 (PCA eigenvectors); DL pp. 32, 41 (matrix in NN/CNN context) | 30-min refresher focused on dot-product similarity |
| Probability: random variables, Gaussian, conditional probability, Bayes, expectation | VAE, diffusion, sampling | 🔹 DL p. 79 (normal distribution in the VAE intuition); Intro AI (hypothesis testing) | **Teach in #2** |
| Derivatives, gradient descent, backprop | All training | ✅ ML pp. 24–34 (SGD/Momentum/Adagrad/Adam); ✅ DL pp. 23–30 (forward/backprop, Adam, learning rate) | Recap only |
| Softmax, cross-entropy, temperature | LLM loss and sampling, distillation | ✅ DL pp. 16, 25–27, 69–71 | Reuse |
| Likelihood, MLE, KL divergence, Jensen's inequality, ELBO | VAE, diffusion, LLM objective | ❌ (KL only named in DL p. 79) | **Teach; the core of #2** |

### Deep learning

| Background | Needed for | Status (source) | Action in GAI |
|---|---|---|---|
| CNN, pooling, BatchNorm, ResNet, dropout, overfitting | AE, U-Net, GAN | ✅ DL pp. 38–55 | Assume it |
| ConvTranspose and upsampling | Decoders, U-Net | 🔹 DL p. 74 (UpSampling) | Short slide |
| Training loop (data → model → loss → optimiser → epochs) | All labs | ✅ in Keras (DL pp. 16–33); 🔹 PyTorch appendix (DL pp. 94–97) | **PyTorch bridge (~2hr)** mapping each Keras step to PyTorch |
| RNN, LSTM, Seq2Seq, encoder–decoder for text | Motivating attention | ❌ **roadmap mismatch** | ~1hr bridge before the Transformer |
| Transfer learning, pretrained models | LoRA, HF models | ✅ DL pp. 56–66 | Bridge to PEFT |
| Distillation and compression | Fast samplers, Edge | ✅ DL pp. 67–72 | Reuse |

### Programming and tools

| Background | Needed for | Status (source) | Action in GAI |
|---|---|---|---|
| Google Colab, GPU runtime, `nvidia-smi` | All labs | ✅ ML pp. 5–6 (T4 GPU); ✅ DL pp. 34–35 | Reuse; add VRAM budgeting, fp16/bf16, handling OOM |
| Jupyter, Anaconda environments | Notebooks | ✅ ML pp. 3–4; ✅ Vibe 11 (conda, pip) | Reuse |
| PyTorch: tensors, autograd, `nn.Module`, `DataLoader`, `.to(device)` | All labs | 🔹 DL pp. 36–37 (TF vs PyTorch), pp. 94–97 (appendix MNIST CNN) | **Bridge lesson** |
| NumPy: ndarray, images as 3D/4D arrays, reshape | Tensors, image data | ✅ 數據代理人 pp. 47–49; ✅ Vibe 12a (shape, dtype) | Add broadcasting, CHW vs HWC |
| PIL / image I/O | Image datasets and outputs | 🔹 named in 數據代理人 p. 49 | Small utility slide |
| matplotlib, seaborn, plotly | Image grids, loss curves | ✅ 數據代理人 (throughout); ✅ Vibe 12a | Reuse; show `imshow` grids |
| Hugging Face Hub, `transformers`, `diffusers`, `peft` | K3, K5–K8, K10 | 🔹 listed as a resource in DL p. 2; ❌ no usage | **Teach** |
| Python OOP, inheritance, `super()` | `nn.Module` subclasses | ✅ Vibe 13 (needs confirming); ✅ DL p. 20 (subclassing `keras.Model`) | Reuse; point out the identical pattern |
| Decorators, generators | `@torch.no_grad`, streaming | 🔹 Vibe 13 (self-study only) | Brief explanation where it first appears |
| `requests`, JSON, `.env` secrets | LLM API calls | ✅ Vibe 11–12 | Reuse directly |
| LLM SDK calls | K6 | ❌ | **Teach** |
| Git (local) / GitHub (remote) | HF Spaces, final project | ✅ local (Vibe 02, 07a); ❌ remote | Short remote/push lesson before K10 |
| Prompt clarity, system vs user prompts | K6, diffusion prompting | ✅ Vibe 01–02 | Reuse |
| AI-assisted coding (Claude Code / Codex) | Lab productivity | ✅ Vibe (heavy); ✅ 數據代理人 pp. 62–63 | Use it in labs: *the agent writes the scaffold, the student audits the math and shapes* |

### The prerequisite gaps to close in the first ~6 hours

1. **PyTorch bridge** (~2hr): mapping Keras to PyTorch; tensors, autograd and the training loop on Colab.
2. **Probability, MLE, KL and ELBO refresher** (~2hr): this is official item #2.
3. **Sequence modelling → why attention** (~1hr): it replaces the RNN/LSTM/Seq2Seq background that DL did not deliver.
4. **Hugging Face and GPU-memory practice** (~1hr): Hub, `from_pretrained`, fp16 and 4-bit, VRAM arithmetic.

---

## Open items

- [ ] **Vibe decks 11–13** (modules, file I/O, numpy/pandas, classes and pytest) were planned for the last two days. Confirm they were delivered.
- [ ] **Confirm the DL roadmap mismatch** with the DL instructor: RNN, LSTM and Seq2Seq are absent from the slides. Were they taught in some other way?
- [ ] **Agree the K6 boundary** with the Agent module instructor. Basic LLM calls belong to GAI; tool calling, MCP and RAG belong to the Agent module.
- [ ] The ML slides contain no XGBoost/LightGBM text even though the roadmap lists them. This is not relevant to GAI and is recorded only for completeness.
