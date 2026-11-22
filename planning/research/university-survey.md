# How frontier universities teach Generative AI: a survey (2026-11-22)

This survey is an input to [course_roadmap.md](../course_roadmap.md). It records how 24 courses and programmes teach generative AI, and what the 48hr 生成式AI原理 module borrows from them.

**Method.**
- Course pages were read on 2026-11-22 with a web fetch.
- Where a page could not be fetched, facts come from search-result snippets and are marked **(s)**.
- Pages that failed are listed in §5 as failures. They are not filled in from memory.
- Assignment handouts and lecture videos were not read unless stated.

**Why the survey matters.** The instructor wants a course that starts from business problems and keeps the math light. The survey checks two things:
1. which topics the field now treats as core;
2. which teaching patterns work for that goal.

---

## 1. Summary table

Archetype key:
- **M**: math-first, organised by model family
- **L**: LLM-focused
- **A**: application-first / top-down
- **B**: business school
- **P**: practitioner or open course

| # | Institution | Course | Term read | Type | Labs / assessment | What we borrow |
|---|---|---|---|---|---|---|
| 1 | Stanford | CS236 Deep Generative Models | Fall 2023 page | M | PyTorch HW1–3, midterm, project, poster | Canonical model families; "evaluation of generative models" as a topic of its own |
| 2 | Stanford | CME 296 Diffusion & Large Vision Models | Spring 2026 | M | No homework; midterm + final | Modern diffusion topic list (flow matching, DiT, LoRA/DreamBooth, distillation); its evaluation lecture |
| 3 | UC Berkeley | CS294-158 Deep Unsupervised Learning | Spring 2024 | M | 4 HW (AR, LVM, GAN, diffusion), midterm, project | Compression as a generative application (supports the VQ-VAE ticket) |
| 4 | Cornell Tech | CS 5788 (generative models) | Spring 2026 | M | 4 problem sets on Colab, midterm, project | Provenance and evaluation lectures; Colab for GPU homework |
| 5 | MIT | 6.S978 Deep Generative Models | Fall 2024 | M | 6 assignments, paper readings, final presentation | "AR and tokenizers" as the bridge to tokens; data ownership as a topic |
| 6 | MIT | 6.S184 Flow Matching and Diffusion Models | IAP 2026 | M | 3 Colab labs, from scratch | From-scratch Colab labs; flow matching as the modern core |
| 7 | Stanford | CME 295 Transformers & LLMs | Autumn 2026 | L | No homework; midterm + final | Order of the LLM training pipeline; LLM evaluation content |
| 8 | Stanford | CS336 Language Modeling from Scratch | Spring 2026 (s) | L | 5 implementation-heavy assignments | Build-to-understand (we do it at toy scale); caution about AI tools doing the assignments |
| 9 | CMU | 10-423/623/723 Generative AI | Spring 2026 | A | HW0 PyTorch primer + HW1–4, quizzes, exam, project + poster | PyTorch primer first; "applying and adapting" unit; no-AI vs AI-assisted deadlines |
| 10 | NTU 台大 (李宏毅) | 生成式AI導論 | Spring 2024 | A | HW1–HW10 | Top-down order; beginner-friendly; SD fine-tuning homework |
| 11 | NTU 台大 (李宏毅) | 生成式人工智慧與機器學習導論 | Fall 2025 | A | HW1–HW10 in Colab | HF + Colab + Gradio in HW1; diffusion customisation and speech homework; Chinese preview material |
| 12 | MIT | 6.S191 Introduction to Deep Learning | 2026 | A | 3 software labs + project pitch | Music generation as an early lab; bias lab; a final project demo |
| 13 | KAIST | CS492(D) Diffusion Models and Their Applications → CS492(C) Diffusion and Flow Models | Fall 2024 / Fall 2025 (s) | A | 7 programming assignments; project; generation contest | The diffusion assignment ladder |
| 14 | MIT | 6.5940 TinyML and Efficient Deep Learning Computing | Fall 2026 (s) | L | 5 labs + project, no exams | Quantisation and LLM-on-laptop as the reference for course goal 9 |
| 15 | Stanford GSB | MKTG 321 Understanding AI Technology for Business Problems | since Jan 2025 | B | Lectures, mini-cases, practitioner visits | Translating a business objective into an AI problem is the hard part |
| 16 | MIT Sloan | 15.S04 GenAI-Lab (action learning) | 2025–2026 (s) | B | Semester-long corporate projects | Real company "tickets"; prototype + strategy memo |
| 17 | Columbia Business School | B8631 Generative AI for Business | Spring 2026 (s) | B | Block week | Business use beyond chat tools; reported to rely on APIs |
| 18 | Harvard Business School | Data Science and AI for Leaders (DSAIL) | 2025 (s) | B | Required first-year course | AI-native business teaching without a coding prerequisite |
| 19 | Wharton | AI for Business MBA major | from Fall 2025 (s) | B | Major + electives | Governance and accountability as required content |
| 20 | fast.ai | Practical Deep Learning for Coders, Parts 1–2 | 2022–2023 | P | Notebooks; Part 2 builds Stable Diffusion | Examples first; "dig deeper" later; math when needed |
| 21 | Hugging Face | Diffusion Models Course | current page | P | 4 units, 2 notebooks each | Diffusers plus an implementation "from 0" |
| 22 | Hugging Face | Audio Course | current page | P | 7 units; quizzes and exercises | TTS unit as reference for #14 |
| 23 | DeepLearning.AI | Generative AI for Everyone | current page | P / B | 3 weeks, non-coding | Business use cases and strategy framing |
| 24 | Johns Hopkins (Imagine) | Hands-On Generative AI with Diffusion Models: Building Real-World Applications | (s) | P | Diffusers-based | Real-world diffusion tasks: text-guided generation, img2img, inpainting |

---

## 2. Course notes

### 2.1 Math-first, model-family courses (M)

**1. Stanford CS236 Deep Generative Models.**
- **Source:** the [syllabus page](https://deepgenerativemodels.github.io/syllabus.html), headed "CS236 - Fall 2023".
- **Instructor:** not named on the page; the course is associated with Stefano Ermon (s).
- **Order:**
  1. Introduction, with a probability and linear algebra review
  2. Background and autoregressive models
  3. Maximum likelihood learning and VAEs
  4. Normalizing flows
  5. GANs
  6. Energy-based models
  7. Score-based models
  8. Evaluation of generative models
  9. Score-based diffusion models and discrete latent variable models
  10. Diffusion models for discrete data
- **Assessment:** HW1–3 implemented in PyTorch; project proposal, progress report, poster and final report; a midterm.
- **Stance:** math-first; there is no applied framing on the page.

**2. Stanford CME 296 Diffusion & Large Vision Models.**
- **Source:** the [course site](https://cme296.stanford.edu/) and its [syllabus](https://cme296.stanford.edu/syllabus).
- **Term and instructors:** Spring 2026, Afshine and Shervine Amidi.
- **Format:** "No homework. However, there are two exams: a midterm and a final."
- **Lectures:**
  1. Diffusion: DDPM, ELBO-based training derivation, DDIM
  2. Score matching: denoising score matching, SDEs, probability flows
  3. Flow matching: conditional flow matching, rectified flow
  4. Latent space and guidance: VAEs, latent diffusion, CLIP/SigLIP, classifier and classifier-free guidance
  5. Architectures: U-Net, attention, Diffusion Transformers, multimodal DiT
  6. Training: pretraining, SFT, Flow-GRPO, Diffusion-DPO, DreamBooth, LoRA, distillation
  7. Evaluation: human ratings, Elo, FID, CLIPScore, LPIPS, MLLM-as-a-judge
  8. "Trending topics": image-to-video
- **Stance:** theory-first and derivation-heavy. It is useful to us as a **topic checklist**.

**3. UC Berkeley CS294-158 Deep Unsupervised Learning.**
- **Source:** the [Spring 2024 site](https://sites.google.com/view/berkeley-cs294-158-sp24/).
- **Lectures:** Intro, Autoregressive Models, Flow Models, Latent Variable Models, GANs / Implicit Models, Diffusion Models, Self-Supervised Learning, Large Language Models (guest), Video Generation, Semi-Supervised Learning and Unsupervised Distribution Alignment, Compression, Multimodal Models, Parallelization, AI for Science (guest), Neural Radiance Fields (guest).
- **Assessment:**
  - HW1–HW4 (autoregressive, latent variable, GAN, diffusion), 15% each.
  - Midterm 10%.
  - Final project 30%.
- **Stance:** the FAQ says the course "is targeted towards a PhD level audience". It is not a pacing model for us.

**4. Cornell CS 5788 (Spring 2026).**
- **Source:** the [course site](https://www.cs.cornell.edu/courses/cs5788/2026sp).
- **Instructor:** Andrew Owens (Cornell Tech).
- **27 lectures:**
  - Foundations: introduction, maximum likelihood, Gaussian mixture models, neural network review.
  - Model families: VAEs, normalizing flows, GANs (×2), energy-based models, diffusion models, autoregressive models, diffusion for discrete data, autoregressive language models, more diffusion, flow matching.
  - Applications and training: applying generative models to downstream tasks, image manipulation with diffusion, post-training (×2), scaling.
  - Impact and other modalities: **generated media provenance**, generative models for audio, **evaluating generative models**, robotics.
  - Project presentations.
- **Assessment:** 4 problem sets in numpy/PyTorch, "generally using Google Colab". Homework 40%, midterm 30%, final project 30%.
- **Stance:** "This course puts a strong emphasis on mathematical methods."

**5. MIT 6.S978 Deep Generative Models (Kaiming He, Fall 2024).**
- **Source:** the [schedule](https://mit-6s978.github.io/schedule.html).
- **Format:** a research seminar built on paper readings.
- **Topics:** image priors, VAE, normalizing flows, autoregressive models, **AR and tokenizers**, AR and diffusion, GAN, energy-based models / score matching / diffusion, discrete diffusion, flow matching.
- **Applications:** video, 3D, robotics, materials, protein.
- **Guest lectures:** "Ensuring Data Ownership in Generative Models" (Jun-Yan Zhu) and "Consistency Models" (Yang Song).
- **Assessment:** 6 assignments and final presentations.

**6. MIT 6.S184 Introduction to Flow Matching and Diffusion Models (IAP 2026).**
- **Source:** the [course site](https://diffusion.csail.mit.edu/2026/).
- **People:** Peter Holderrieth and Ezra Erives (lectures); Ron Shprints (labs).
- **Lectures:**
  1. Flow and diffusion models (ODEs/SDEs)
  2. Flow matching
  3. Score matching and classifier-free guidance
  4. Latent spaces and architectures (VAEs, DiT, U-Nets)
  5. Discrete diffusion
- **Labs (Colab):** Lab 1 ODEs and SDEs; Lab 2 flow matching and score matching; Lab 3 Diffusion Transformer and VAEs.
  - The labs guide students to "building a flow matching and diffusion model from scratch step-by-step".
  - By the end, students "will have built a latent diffusion model from scratch".
- **Prerequisites:** linear algebra, multivariate calculus, basic probability and some PyTorch.

### 2.2 LLM-focused courses (L)

**7. Stanford CME 295 Transformers & Large Language Models.**
- **Source:** the [course site](https://cme295.stanford.edu/) and its [syllabus](https://cme295.stanford.edu/syllabus).
- **Term and format:** Autumn 2026, Amidi twins; no homework, two exams.
- **Lectures:**
  1. Transformers: tokenization, embeddings, word2vec, RNN/LSTM, attention
  2. LLMs: MoE, MHA/MQA/GQA, RoPE, sampling
  3. LLM training: pretraining, SFT, LoRA, RLHF/DPO, reasoning, distillation
  4. RL with LLMs: PPO, GRPO
  5. LLM systems: KV caching, speculative decoding, FlashAttention
  6. **AI agents**: tool calling, MCP, memory and retrieval, coding agents
  7. LLM evaluation: LLM-as-a-judge, biases, benchmarks
  8. Diffusion LLMs
  9. Trending topics

**8. Stanford CS336 Language Modeling from Scratch (Spring 2026) (s).**
- **Sources:** the [course site](https://cs336.stanford.edu) (not fully read) and the [GitHub organisation](https://github.com/stanford-cs336).
- **Instructors:** Tatsunori Hashimoto and Percy Liang.
- **Assignments:** five implementation-heavy assignments: basics (build Transformer LM components), systems, scaling, data, alignment.
- **AI-tools warning (s):** the Assignment 1 handout warns that AI tools can complete many parts autonomously. That makes it harder to engage with and learn from the material.

**14. MIT 6.5940 TinyML and Efficient Deep Learning Computing (Fall 2026) (s).**
- **Source:** the [course page](https://hanlab.mit.edu/courses/2026-fall-65940); instructor Song Han.
- **Five labs:** GPU basics, pruning, neural architecture search, quantization, LLM deployment on a laptop.
- **Assessment:** no exams. It is our reference for quantisation and edge deployment (course goal 9).

### 2.3 Application-first / top-down courses (A)

**9. CMU 10-423/623/723 Generative AI (Spring 2026).**
- **Sources:** the [schedule](https://www.cs.cmu.edu/~mgormley/courses/10423/schedule.html), [coursework](https://www.cs.cmu.edu/~mgormley/courses/10423/coursework.html) and [home page](https://www.cs.cmu.edu/~mgormley/courses/10423/).
- **Instructors:** Aran Nayebi and Matt Gormley.
- **Units:**
  - Generative models of text: RNN LMs, Transformer LMs, decoding, pre-training/fine-tuning.
  - Generative models of images: ViT, GANs, diffusion I–II, VAEs.
  - **Applying and adapting foundation models:** PEFT; ICL / prompt engineering / instruction fine-tuning / RLHF.
  - Multimodal foundation models: DPO, text-to-image, latent diffusion, VLMs, cross-attention, DiT.
  - Scaling up: scaling laws, MoE, distributed training, FlashAttention.
  - Advanced: long context, reasoning models, state-space models, **"Real-world Issues / What can go wrong?"**, code generation / agents, audio understanding and synthesis, video, world models and alignment.
- **Homework:** HW0 is a **PyTorch primer**. HW1 LLMs; HW2 image generation; HW3 applying and adapting LLMs; HW4 multimodal foundation models.
- **AI policy:** each homework has a **Slot A (no AI) and a Slot B (AI-assisted)** deadline.
- **Grading (10-423):** 30% homework, 10% quizzes, 10% programming tests, 20% exam, 25% project (teams of 3, with a poster), 5% participation.
- **Stated aim:** "Apply existing models to real-world generation problems".

**10. NTU 李宏毅 生成式AI導論 (Spring 2024).**
- **Source:** the [course page](https://speech.ee.ntu.edu.tw/~hylee/genai/2024-spring.php).
- **Audience:** for beginners, with no prerequisites.
- **Lecture order (top-down):**
  1. What GenAI is
  2. 提示工程 & AI 代理人
  3. Generation strategies, and from specialist to generalist
  4. Deep learning & Transformer
  5. LLM training stages 1–3: pretraining, instruction tuning, RLHF
  6. LLM-based agents
  7. Transformer & interpretability
  8. Evaluation & ethics; jailbreaks
  9. Text vs image generation; speculative decoding
  10. Image and video generation: VAE, flow, diffusion, GAN
- **Homework:**
  - HW1 真假難辨的世界
  - HW2 都是 AI 的作文比賽
  - HW3 以 AI 搭建自己的應用
  - HW4 Become an AI Hypnosis Master
  - HW5 LLM Fine-tuning
  - HW6 Learning from Human Preferences
  - HW7 Understanding what AI is thinking
  - HW8 Safety Issue of Generative AI
  - HW9 Quick Summary of Lecture Video
  - HW10 Stable Diffusion Fine-tuning

**11. NTU 李宏毅 生成式人工智慧與機器學習導論 (Fall 2025).**
- **Source:** the [course page](https://speech.ee.ntu.edu.tw/~hylee/GenAI-ML/2025-fall.php).
- **Lectures:**
  1. 一堂課搞懂生成式人工智慧的基本原理
  2. 上下文工程 (Context Engineering)
  3. 解剖大型語言模型
  4. 評估生成式人工智慧能力時可能遇到的各種坑
  5. 一堂課搞懂機器學習與深度學習的基本原理
  6. 訓練類神經網路的各種訣竅
  7. 大型語言模型的學習歷程
  8. 通用模型的終身學習
  9. 影像和聲音上的生成策略
  10. 語音語言模型發展史
- **Order:** ML basics arrive only in lectures 5–6, after LLM use and internals.
- **Homework (all on Colab):**
  - HW1 fundamentals of GenAI; per the HW1 PDF (s) it covers NTU COOL, **Hugging Face, Colab and Gradio**
  - HW2 Build a Basic RAG System
  - HW3 Exploring Generative AI; per the HW3 PDF (s) it covers interpretability with Logit Lens and Function Vector
  - HW4 LLM Malicious Instruction Defense
  - HW5 Regression
  - HW6 Image Classification
  - HW7 Finetuning LLM
  - HW8 Fine-tuning Leads to Forgetting
  - HW9 **Diffusion Model and Its Customization**
  - HW10 **Speech Generation**
- **Spring 2026 ML course:** the follow-on [ML 2026 Spring](https://speech.ee.ntu.edu.tw/~hylee/ml/2026-spring.php) starts from AI agents and includes HW9 **Flow Matching** and HW10 Spoken Language Model.

**12. MIT 6.S191 Introduction to Deep Learning (2026).**
- **Source:** [introtodeeplearning.com](https://introtodeeplearning.com/).
- **Instructors:** Alexander and Ava Amini.
- **Format:** "an efficient and high-intensity bootcamp".
  - A snippet (s) gives an in-person week of Jan 5–9, 2026.
  - The fetched page lists weekly lectures from Mar 30 to May 25, 2026.
- **Prerequisites:** "very elementary knowledge of linear algebra and calculus"; described as "beginner friendly".
- **Labs:**
  - Lab 1 Deep Learning in Python; **Music Generation**
  - Lab 2 Facial Detection Systems (bias)
  - Lab 3 "Fine-Tune an LLM, You Must!"
- **Ending:** a project proposal competition with feedback from a "panel of industry sponsors".

**13. KAIST CS492(D) / CS492(C) (s).**
- **Fall 2024:** [CS492(D) Diffusion Models and Their Applications](https://mhsung.github.io/kaist-cs492d-fall-2024/programming-assignments), Minhyuk Sung.
  - Seven programming assignments: DDPM, DDIM/CFG, ControlNet/LoRA, Distillation, Synchronization, DPMSolver, Flow.
  - Grading: assignments 45%, project 45%, participation 10%.
- **Fall 2025:** [CS492(C) Diffusion and Flow Models](https://diffusion.kaist.ac.kr/).
  - Adds an Image Generation Challenge and a Visual Generation Contest.

### 2.4 Business-school courses (B)

**15. Stanford GSB MKTG 321 Understanding AI Technology for Business Problems.**
- **Source:** the [GSB article, April 2026](https://www.gsb.stanford.edu/experience/news-history/back-class-understanding-ai-technology-business-problems) and the [Bulletin](https://bulletin.stanford.edu/courses/2264141) (s).
- **Instructor and format:** Yuyan Wang. The course mixes "lectures and mini-case studies to practitioner visits".
- **Key quotes:**
  - "The most difficult part of applying AI to solve a business problem is not building a fancy model"
  - "That translation part is not something technical people are capable of doing."
- **Our response:** we train engineers to do that translation. That is the "Frame" step of our loop.

**16. MIT Sloan 15.S04 GenAI-Lab (s).**
- **Sources:** [GenAI-Lab impact stories](https://mitsloan.mit.edu/node/49116) and [GenAI-Lab at a glance](https://mitsloan.mit.edu/node/49117).
- **Format:** teams work on **semester-long corporate projects** tied to generative AI. Deliverables can include **AI prototypes and strategy memos**.
- **Hosts** include Schneider Electric, Verizon, Wayfair and Workday.

**17. Columbia Business School B8631 Generative AI for Business (s).**
- **Sources:** the [Spring 2026 listing](https://doc.sis.columbia.edu/subj/MRKT/B8631-20261-001): block week, Tue–Sat, 9am–5pm, 3 points.
- **Catalog description:** for students interested in GenAI applications "that go beyond personal productivity enhancement tools like ChatGPT".
- **API claim (unconfirmed link):** a Columbia CTL page (s) says a course called Generative AI for Business (Olivier Toubia, co-developed with Malek Ben Sliman) "relies heavily on the use of APIs". Its link to B8631 is likely but unconfirmed.

**18. Harvard Business School DSAIL (s).**
- **Sources:** an [HBS faculty post](https://professorkl.substack.com/p/and-we-are-launcheddata-science-and) and a [news report](https://www.businessbecause.com/news/in-the-news/9736/harvard-new-mba-artificial-intelligence-course).
- **Details:** a required, "AI-native" course for all first-year MBA students, co-led by Karim Lakhani and Iavor Bojinov. Students use Julius.ai to work in R and Python without learning to code.

**19. Wharton (s).**
- **Sources:** the [AI for Business MBA major](https://catalog.upenn.edu/graduate/programs/artificial-intelligence-business-mba/), from Fall 2025, and the [Wharton OID page](https://oid.wharton.upenn.edu/artificial-intelligence-mba/).
- **Required course:** LGST 6420 on accountable AI.
- **Elective:** MKTG 8530 Designing and Deploying AI Agents.

### 2.5 Practitioner and open courses (P)

**20. fast.ai Practical Deep Learning for Coders.**
- **Sources:** [course.fast.ai](https://course.fast.ai/) and [Part 2](https://course.fast.ai/Lessons/part2.html).
- **Teaching approach, in their words:**
  - "We always teach through examples."
  - The course starts "by showing how to use a complete, working, very usable, state-of-the-art deep learning network", then lets you "gradually dig deeper and deeper".
  - "we'll teach you the calculus and linear algebra you need during the course"
- **Part 2 (lessons 9–25):** Stable Diffusion (Diffusers pipelines first) → foundations → autoencoders → DDPM → mixed precision → DDIM → Karras et al. → super-resolution → attention & transformers → latent diffusion.

**21. Hugging Face Diffusion Models Course.**
- **Source:** the [course](https://huggingface.co/learn/diffusion-course/unit0/1).
- **Units:**
  1. "Introduction to 🤗 Diffusers and implementation from 0"
  2. Fine-tuning and guidance
  3. Stable Diffusion
  4. Doing more with diffusion
- Each unit has theory and two notebooks.

**22. Hugging Face Audio Course.**
- **Source:** the [course](https://huggingface.co/learn/audio-course/chapter0/introduction).
- **Units:** audio data, pipelines, transformer architectures, music genre classification, speech recognition, **speech from text (TTS)**, real-world applications.
- There is no music-generation unit.

**23. DeepLearning.AI Generative AI for Everyone.**
- **Source:** the [course page](https://www.deeplearning.ai/courses/generative-ai-for-everyone/).
- **Weeks:**
  1. What is generative AI and its applications
  2. Generative AI projects, beyond prompting
  3. Generative AI in business and society
- A non-coding course. It promises to teach "how to develop a generative AI strategy to increase productivity".

**24. Johns Hopkins (Imagine) Hands-On Generative AI with Diffusion Models (s).**
- **Source:** the [course page](https://imagine.jhu.edu/classes/hands-on-generative-ai-with-diffusion-models-building-real-world-applications).
- **Content:** the Diffusers library; unconditional generation, text-guided generation, image-to-image translation and inpainting.

### 2.6 Supporting references

- **McKinsey, "The economic potential of generative AI" (June 2023) (s).** [Link](https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/the-economic-potential-of-generative-ai-the-next-productivity-frontier).
  - 63 use cases across 16 business functions, worth $2.6–4.4 trillion a year.
  - About 75% of the value lies in **customer operations, marketing and sales, software engineering and R&D**.
- **Merrill, M. D. (2002), "First Principles of Instruction", *ETR&D* 50(3), 43–59 (s).**
  - Learning is promoted when instruction is **centred on real-world problems**, moving through activation → demonstration → application → integration.
  - It gives more guidance than pure problem-based learning. See the [summary](https://en.wikipedia.org/wiki/First_Principles_of_Instruction) and [synthesis PDF](https://www.yorku.ca/unsdgs/toolkit/wp-content/uploads/sites/617/2023/04/Merrills-First_Principles_of_Instruction_A_synthesis.pdf).
- **iPAS AI應用規劃師 (course goal 10) (s).**
  - **初級:**
    - 科目一 人工智慧基礎概論 includes 鑑別式 vs 生成式 AI basics, AI governance, and data privacy and security.
    - 科目二 生成式AI應用與規劃 covers No Code / Low Code, common GenAI tools, 導入評估, 導入規劃 and 風險管理.
  - **中級:** L21 人工智慧技術應用與規劃, L22 大數據處理分析與應用, L23 機器學習技術與應用.
  - **Sources:** [104 blog](https://blog.104.com.tw/preparing-ipas-ai-notes-with-gemini-notebook/), [數位時代](https://www.bnext.com.tw/article/82484/ai-master-2025), and [slides citing iPAS](https://www.slideshare.net/slideshow/ai-ai-ipas/277233132).
  - **Not verified:** the official ability-index page failed (see §5), so this mapping still needs checking against the official 學習指引.

---

## 3. Cross-course synthesis

### 3.1 Which surveyed courses teach which topic

This table uses only what the pages above show. "Our session" refers to [course_roadmap.md](../course_roadmap.md).

| Topic | Courses that teach it | Our session |
|---|---|---|
| AE / VAE | CS236, CS294-158, CS5788, 6.S978, 6.S184, CME 296, 10-423, NTU 2024/2025, fast.ai P2 | D2-1, D2-3 |
| VQ / discrete tokenizers | 6.S978 (AR and tokenizers), CS236 (discrete latent variables), CS294-158 (compression) | D2-4 |
| GAN | CS236, CS294-158, CS5788 (2 lectures), 6.S978, 10-423 (1 lecture), NTU 2024/2025 (inside the image lecture) | D3-1 |
| Unpaired translation / editing | CS294-158 (distribution alignment), CS5788 (image manipulation with diffusion), 10-423 (prompt-to-prompt) | D3-2, D4-4 |
| Diffusion (DDPM / score) | All M courses, 10-423, NTU, KAIST, HF Diffusion, fast.ai P2 | D3-3 |
| Flow matching | CME 296, CS5788, 6.S978, 6.S184, KAIST, NTU ML 2026 HW9 | D4-4 (intuition) |
| Guidance / CFG | CME 296, CS5788, 6.S184, KAIST, HF Diffusion | D4-1 |
| Latent diffusion / Stable Diffusion | CME 296, 6.S184, 10-423, HF Diffusion, fast.ai P2 | D4-2 |
| Fast sampling / distillation | CME 296, KAIST, 6.S978 (consistency models), fast.ai P2 (DDIM) | D3-4, D4-4 |
| LoRA / fine-tuning | CME 296, CME 295, 10-423, NTU 2024/2025, 6.S191, KAIST | D4-3, D5-4 |
| Transformer / GPT internals | CME 295, CS336, 10-423, NTU, 6.S191, fast.ai P2, CS5788 | D5-1, D5-2 |
| LLM post-training (SFT/RLHF/DPO), reasoning | CME 295, CS336, 10-423, NTU 2024/2025, CS5788 | D5-4 |
| Multimodal / CLIP / VLM | CME 296, 10-423, CS294-158 | D4-2, D6-2 |
| Audio / music / speech | 6.S191 (music lab), 10-423, CS5788, NTU 2025 (speech HW), HF Audio | D2-4, D6-1 |
| Video generation | CME 296, CS294-158, 10-423, 6.S978, NTU 2024 | D6-2 (overview) |
| Evaluation | CS236, CME 296, CME 295, CS5788, NTU 2025 | Daily Measure step; D4-1, D4-2, D5-4 |
| Safety / provenance / ethics / data ownership | 10-423, CS5788, 6.S978, NTU 2024/2025, 6.S191 (bias lab) | Daily Measure & Risk; D6-3 |
| Agents / RAG / context engineering | CME 295, 10-423, NTU 2024/2025, NTU ML 2026 | **Deferred** to the Agent and Text-to-SQL modules |
| Efficiency / quantisation / deployment | CME 295, 10-423, 6.5940, CS336 | D1-4, D5-3, D6-3 |
| **Industrial anomaly detection** | **None of the surveyed courses** | D2-1, D2-2, D3-2, D3-4 (required by our syllabus #3, #8) |
| **Business framing / use-case selection** | Business schools; among technical courses only 6.S191 (industry panel) and 10-423 ("real-world generation problems") | Every ticket; D1-1; D6-4 |

### 3.2 Teaching patterns

1. **Top-down openings work for beginners.**
   - NTU 2024 and 2025 start with using GenAI and with prompting and agents; ML basics come only in lectures 5–6.
   - fast.ai starts with "a complete, working ... network" and digs deeper later.
   - MIT 6.S191 puts music generation in Lab 1.
2. **Dual labs are common in lab-heavy courses.**
   - The HF Diffusion course pairs Diffusers with an implementation from 0.
   - MIT 6.S184 and KAIST build models from scratch.
   - fast.ai Part 2 uses Diffusers first, then rebuilds Stable Diffusion.
3. **Free GPUs (Colab) are the norm for homework.** This holds for NTU, MIT 6.S191, 6.S184 and Cornell CS 5788. It matches our T4 constraint.
4. **Exam-only lecture courses exist (CME 295/296)**, but they are not a model for a course whose goal is a working engineer.
5. **AI-tool policy is now explicit.** CMU uses split no-AI / AI-assisted deadlines; CS336 warns that AI tools can do the assignments.
6. **Real deliverables to real audiences.** Examples:
   - MIT Sloan: prototypes and strategy memos for host companies.
   - MIT 6.S191: pitch to an industry panel.
   - CMU: poster session.

### 3.3 Trends, 2024 → 2026

- **Flow matching is rising.** It is in 6.S184, CME 296 and CS5788, and in KAIST's renamed course and NTU's 2026 HW9.
- **GAN is shrinking but not gone.** CMU gives it one lecture, and NTU folds it into one image lecture.
- **Evaluation and provenance are becoming lectures of their own** (CME 296, CS5788, NTU 2025).
- **Agents and context engineering now enter introductory GenAI courses** (NTU 2025, CME 295).
- **Reasoning models and RL post-training** appear in every LLM-focused course from 2025 on.
- **Audio is small but present.** It usually gets one lecture or one homework.

---

## 4. Implications for 生成式AI原理

| # | Decision | Survey evidence |
|---|---|---|
| 1 | Open every session top-down: a business ticket and a pretrained quick win before the internals | NTU 2024/2025, fast.ai, 6.S191 |
| 2 | Dual labs: "Try" a pipeline, then "Open" a tiny from-scratch build | HF Diffusion, 6.S184, KAIST, fast.ai P2 |
| 3 | Follow the diffusion ladder: DDPM → DDIM/CFG → LoRA/ControlNet → distillation → flow | KAIST CS492(D) assignments |
| 4 | Teach flow matching at intuition level (2D toy) | 6.S184, CME 296, CS5788, KAIST, NTU 2026 |
| 5 | Keep GAN and CycleGAN short. Frame them by where adversarial losses still ship | CMU, NTU; our syllabus #10–#11 |
| 6 | Make Measure & Risk a daily step, plus a compliance clinic | CMU "What can go wrong?", CS5788 provenance/evaluation, CME 296 evaluation, NTU 2025 |
| 7 | Add a no-AI checkpoint in labs and the 學習評量 | CMU Slot A/B, CS336 warning |
| 8 | Make the capstone a prototype + memo + a short **individual** demo (no group work, per the instructor's rule in `demo-and-practice` §1) | Sloan GenAI-Lab (prototype + memo); 6.S191 and CMU (final project presentations) |
| 9 | Put the PyTorch primer before any model | CMU HW0 |
| 10 | Defer agents, RAG and vector databases to later modules, but name them | NTU 2025 and CME 295 teach them; our program assigns them to the Agent and Text-to-SQL modules |
| 11 | Treat industrial anomaly detection and music generation as our own additions | Not found in the surveyed courses; required by syllabus #8 and #14 |

---

## 5. Fetch log and limitations

- **Fetched successfully:**
  - Stanford: CS236 syllabus, CME 296, CME 295, the GSB MKTG 321 article.
  - Berkeley: CS294-158 (sp24).
  - Cornell: CS 5788.
  - MIT: 6.S978 schedule, 6.S184 2026, 6.S191.
  - CMU: 10-423 schedule, home page and coursework.
  - NTU: 2024 and 2025 course pages, and ML 2026 Spring.
  - Practitioner courses: fast.ai (home page and Part 2), HF Diffusion and Audio course introductions, DeepLearning.AI GenAI for Everyone.
- **Failed:**
  - Columbia B8631 course page: HTTP 403.
  - Columbia CTL Toubia page: HTTP 500.
  - MIT Sloan GenAI-Lab page and 15.S04 node page: HTTP 404.
  - iPAS ability index (`ipas.org.tw/AIAP/AbilityIndex.aspx`): HTTP 301 → 404.
- **Search-snippet facts only (s):** CS336, 6.5940, KAIST, MIT Sloan, Columbia, HBS, Wharton, JHU, McKinsey, Merrill, iPAS, and the CS236 instructor.
- **Not read:**
  - assignment handouts (except the NTU HW1/HW3 snippets);
  - lecture videos;
  - KAIST assignment READMEs;
  - 6.S978 assignment folders.
- **Stale page:** the CS236 page shows Fall 2023 and is not a current offering.
