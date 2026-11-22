# Homework, labs and assignments in the surveyed courses

This file lists the homework, labs and assignments of each course in [university-survey.md](university-survey.md). The source pages were read on 2026-11-22.

**Rules for reading this file:**
- Titles are copied as each course page states them.
- **(s)** means the fact comes from a search-result snippet, not a page that was read.
- "Not stated" means the page gives no topic. Nothing has been filled in from memory or inferred.
- Handouts themselves were not read, so the one-line descriptions come from titles only.

---

## 1. Math-first, model-family courses

### Stanford CS236 Deep Generative Models (Fall 2023 page)
- **HW1, HW2, HW3:** topics not stated. The schedule only says they are implemented in PyTorch. HW1 is released in week 2, HW2 in week 4 and HW3 in week 7.
- **Project:** proposal → progress report → poster → final report.
- **Exam:** one midterm.

### Stanford CME 296 Diffusion & Large Vision Models (Spring 2026)
- **No homework** ("No homework. However, there are two exams: a midterm and a final.").

### UC Berkeley CS294-158 Deep Unsupervised Learning (Spring 2024)
| Homework | Topic | Weight |
|---|---|---|
| HW1 | Autoregressive Models | 15% |
| HW2 | Latent Variable Models | 15% |
| HW3 | GANs / Implicit Models | 15% |
| HW4 | Diffusion Models | 15% |

- **Code:** all four homeworks are in the `rll/deepul` GitHub repository.
- **Final project (30%):** open scope (new algorithms, applications, benchmarking or compression). It has a 1-page proposal, a 3-page milestone, a 6-page report and a 5-minute video.

### Cornell CS 5788 (Spring 2026)
| Problem set | Topic |
|---|---|
| ps1 | Simple generative models |
| ps2 | Not stated |
| ps3 | Diffusion models |
| ps4 | Language models |

- **Format:** Python with numpy and PyTorch, "generally using Google Colab".
- **Final project:** proposal, midway and final presentations.

### MIT 6.S978 Deep Generative Models (Fall 2024)
- **Six assignments**, due Sep 24, Oct 8, Oct 22, Nov 5, Nov 19 and Dec 3. Their titles were not fetched; they sit in linked Google Drive folders.
- **Other work:** paper presentations and a final project presentation.

### MIT 6.S184 Introduction to Flow Matching and Diffusion Models
All three labs are Colab notebooks that build the models from scratch. Students submit the notebook as a PDF.

| Lab | 2026 (IAP) | 2025 |
|---|---|---|
| Lab 1 | Working with ODEs and SDEs | Working with SDEs |
| Lab 2 | Flow Matching and Score Matching | Flow Matching and Score Matching |
| Lab 3 | Diffusion Transformer and VAEs | Conditional Image Generation |

- **End goal:** students "will have built a latent diffusion model from scratch".

---

## 2. LLM-focused courses

### Stanford CME 295 Transformers & LLMs (Autumn 2026)
- **No homework:** two exams only.

### Stanford CS336 Language Modeling from Scratch (Spring 2026) (s)
| Assignment | Repository name | What it covers |
|---|---|---|
| 1 | `assignment1-basics` | Build the components of a Transformer language model |
| 2 | `assignment2-systems` | Not stated beyond the name |
| 3 | `assignment3-scaling` | Not stated beyond the name |
| 4 | `assignment4-data` | Not stated beyond the name |
| 5 | `assignment5-alignment` | Not stated beyond the name |

- **Leaderboard:** Assignment 1 links to a leaderboard.
- **AI-tools warning:** the handout warns that AI tools can complete many parts autonomously.

### MIT 6.5940 TinyML and Efficient Deep Learning Computing (s)
| Lab | Fall 2026 | Fall 2023 |
|---|---|---|
| 1 | GPU Basics | Pruning |
| 2 | Pruning | Quantization |
| 3 | Neural architecture search | Neural architecture search |
| 4 | Quantization | LLM compression |
| 5 | LLM deployment on laptop | LLM deployment on laptop |

- **Also:** a final project. There are no exams.

---

## 3. Application-first / top-down courses

### CMU 10-423/623/723 Generative AI (Spring 2026)
| Homework | Topic |
|---|---|
| HW0 | PyTorch Primer |
| HW1 | Large Language Models |
| HW2 | Image Generation |
| HW3 | Applying and Adapting LLMs |
| HW4 | Multimodal Foundation Models |
| HW623 | Literature evaluation (10-623 and 10-723 only) |

- **Format:** each homework mixes written analysis with programming.
- **Two deadlines:** each has a **Slot A (no AI)** and a **Slot B (AI-assisted)** deadline.
- **Also:** 2 programming tests, 6 in-class quizzes, and a team project of 3 (proposal, midway, report, poster).

### NTU 李宏毅 生成式AI導論 (Spring 2024)
| Homework | Title | Colab |
|---|---|---|
| HW1 | 真假難辨的世界 | No code |
| HW2 | 都是 AI 的作文比賽 | No code |
| HW3 | 以 AI 搭建自己的應用 | Yes |
| HW4 | Become an AI Hypnosis Master | Yes |
| HW5 | LLM Fine-tuning | Yes |
| HW6 | Learning from Human Preferences | Yes |
| HW7 | Understanding what AI is thinking | Yes |
| HW8 | Safety Issue of Generative AI | Yes |
| HW9 | Quick Summary of Lecture Video | Yes |
| HW10 | Stable Diffusion Fine-tuning | Yes |

### NTU 李宏毅 生成式人工智慧與機器學習導論 (Fall 2025)
All homework is linked to Colab. The course also provides a PyTorch Guide, a Judge Boi Guide and a bonus homework. Per the course policy (s), the bonus is an optional NVIDIA DLI self-paced course.

| Homework | Title | Extra detail |
|---|---|---|
| HW1 | Understand the fundamentals of GenAI | (s) covers NTU COOL, Hugging Face, Colab and Gradio |
| HW2 | Build a Basic RAG System | |
| HW3 | Exploring Generative AI | (s) interpretability: Logit Lens and Function Vector |
| HW4 | LLM Malicious Instruction Defense | |
| HW5 | Regression | |
| HW6 | Deep Learning for Image Classification | |
| HW7 | Finetuning LLM | |
| HW8 | Fine-tuning Leads to Forgetting | |
| HW9 | Diffusion Model and Its Customization | |
| HW10 | Speech Generation | |

### NTU 李宏毅 Machine Learning (Spring 2026; the follow-on course)
This course starts with tutorials: a Colab and Kaggle tutorial, a PyTorch tutorial, a JudgeBoi guide and a bonus competition.

| Homework | Title |
|---|---|
| HW1 | LLM Malicious Instruction Defense |
| HW2 | AI Agent as an AI Engineer |
| HW3 | LLM Fast Inference |
| HW4 | Training Transformer |
| HW5 | Finetuning without Forgetting |
| HW6 | Model Editing |
| HW7 | Model Merging |
| HW8 | Test-Time Scaling |
| HW9 | Flow Matching |
| HW10 | Spoken Language Model |

### MIT 6.S191 Introduction to Deep Learning (2026)
| Lab | Title |
|---|---|
| Software Lab 1 | Deep Learning in Python; Music Generation |
| Software Lab 2 | Facial Detection Systems (linked to a bias-mitigation paper) |
| Software Lab 3 | "Fine-Tune an LLM, You Must!" |

- **Final:** a project proposal competition judged with feedback from staff and an industry-sponsor panel. The course is graded P/D/F on the project proposal.

### KAIST CS492(D) / CS492(C) (s)
**Fall 2024: CS492(D) Diffusion Models and Their Applications** (assignments 45%, project 45%, participation 10%):

| # | Programming assignment |
|---|---|
| 1 | DDPM |
| 2 | DDIM / CFG |
| 3 | ControlNet / LoRA |
| 4 | Distillation |
| 5 | Synchronization |
| 6 | DPMSolver |
| 7 | Flow |

**Fall 2025: CS492(C) Diffusion and Flow Models** (programming assignments 20%):
- Assignment 2 is DPM-Solver and Assignment 3 is Flow Matching. The full list was not seen.
- There is an optional session on Distillation and Synchronization.
- The project components are an **Image Generation Challenge** and a **Visual Generation Contest**, plus in-class tests.

---

## 4. Business-school courses

### Stanford GSB MKTG 321 Understanding AI Technology for Business Problems
- **In class (week 2):** students tune neural-network hyperparameters on a simulated classification problem ("distinguishing a cat from a dog").
- **Homework:** "additional algorithmic training involving a much larger data set".
- No capstone or student project is described.

### MIT Sloan 15.S04 GenAI-Lab (s)
- **One semester-long team project** with a host company. Deliverables can include **AI prototypes** and **strategy memos** on what recent GenAI developments mean for the business.

### Columbia B8631, HBS DSAIL, Wharton AI major
- **Homework not stated** in any source that could be reached. The Columbia pages returned 403 and 500.

---

## 5. Practitioner and open courses

### fast.ai Practical Deep Learning for Coders
- **No formal homework is listed.** By lesson 2, learners "built and deployed your own deep learning model on data you collect".
- **Part 2:** learners implement Stable Diffusion; the from-scratch parts use "nothing other than Python and its standard library".

### Hugging Face Diffusion Models Course
Each unit has "two notebooks". The notebook titles were not on the page read.

| Unit | Hands-on topic |
|---|---|
| 1 | Introduction to 🤗 Diffusers and implementation from 0 |
| 2 | Fine-tuning on new data and adding guidance |
| 3 | Stable Diffusion |
| 4 | Advanced techniques |

### Hugging Face Audio Course
- **Certification:** "Complete 80% of the hands-on exercises" for completion, 100% for honors.
- **Project-style units:** Unit 4 builds a music genre classifier; Unit 5 transcribes meeting recordings; Unit 6 generates speech from text.

### DeepLearning.AI Generative AI for Everyone
- **Assessment:** 6 graded assignments (PRO tier) and 2 code examples.
- **Hands-on exercise:** using GPT-3.5 to "classify and summarize restaurant reviews".

### Johns Hopkins (Imagine) Hands-On Generative AI with Diffusion Models (s)
- **Homework not stated.** The listed topics are unconditional generation, text-guided generation, image-to-image translation and inpainting with `diffusers`.

---

## 6. Homework themes that recur, and where our labs cover them

| Homework theme | Courses that assign it | Our lab ([roadmap](../course_roadmap.md) §9) |
|---|---|---|
| PyTorch primer | CMU HW0, NTU 2025 PyTorch Guide, NTU 2026 PyTorch tutorial | L1-3, L1-4 |
| Colab / HF / Gradio setup | NTU 2025 HW1 (s) | L1-2, L1-4 |
| Autoregressive / language models | Berkeley HW1, Cornell ps4, CMU HW1, CS336 A1, NTU 2026 HW4 | L5-1, L5-2 |
| Latent variable models / VAE | Berkeley HW2, 6.S184 Lab 3 (2026) | L2-3 |
| GAN | Berkeley HW3 | L3-1 |
| Diffusion from scratch | Berkeley HW4, Cornell ps3, KAIST DDPM, HF Diffusion Unit 1 | L3-3 |
| Guidance / conditional generation | KAIST DDIM/CFG, 6.S184 Lab 3 (2025), HF Diffusion Unit 2 | L4-1 (學習評量) |
| Diffusion fine-tuning / customisation (LoRA, DreamBooth, ControlNet) | KAIST ControlNet/LoRA, NTU 2024 HW10, NTU 2025 HW9 | L4-2, L4-3 |
| Fast sampling / distillation | KAIST Distillation and DPMSolver | L3-4, L4-4 |
| Flow matching | 6.S184 Lab 2, KAIST Flow, NTU 2026 HW9 | L4-4 (2D toy) |
| LLM fine-tuning | NTU 2024 HW5, NTU 2025 HW7, MIT 6.S191 Lab 3, CMU HW3 | L5-4 |
| Forgetting / editing / merging | NTU 2025 HW8, NTU 2026 HW5–7 | Not covered (beyond scope) |
| Learning from human preferences | NTU 2024 HW6, CS336 A5 | D5-4 concept only |
| Interpretability | NTU 2024 HW7, NTU 2025 HW3 (s) | L5-2 (top-k logits) only |
| Safety / malicious instructions / bias | NTU 2024 HW8, NTU 2025 HW4, NTU 2026 HW1, MIT 6.S191 Lab 2 | Daily Measure & Risk; D4-2 bias audit |
| RAG / agents | NTU 2025 HW2, NTU 2026 HW2 | Deferred to the Agent module |
| Multimodal | CMU HW4 | L6-2 |
| Audio / music / speech | MIT 6.S191 Lab 1, NTU 2025 HW10, NTU 2026 HW10, HF Audio Unit 6 | L2-4, L6-1 |
| Efficiency / quantisation / inference speed | MIT 6.5940 labs, NTU 2026 HW3, CS336 A2 | L5-3 |
| Business application / prototype | NTU 2024 HW3, Sloan GenAI-Lab, DeepLearning.AI review exercise | Daily Gradio ship; capstone |
| Competition / leaderboard | KAIST challenge and contest, CS336 leaderboard, NTU JudgeBoi | Not planned (no competitive formats for this class) |
