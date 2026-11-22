# Day 4 slide plan · 「行銷影像工作室」

> **Status:** draft, awaiting instructor approval (written 2026-11-23, phase 3 of the /goal).
> **Source:** [course_roadmap.md](../course_roadmap.md) §7 Day 4, §9 L4-1…L4-4, §11, §12 (學習評量). Compact slide tables as in [D2-factory-qa.md](D2-factory-qa.md).
> **Decks:** D4-1 `13-conditional-diffusion-cfg` · D4-2 `14-stable-diffusion-studio` · D4-3 `15-lora-brand` · D4-4 `16-bakeoff-memo`.

**Day goal.** A student can implement conditional generation with classifier-free guidance (the 學習評量 notebook), run and control Stable Diffusion (text, img2img, inpainting) with CLIP-score measurement, adapt it to the company's product with IP-Adapter or LoRA, and compare GAN vs diffusion approaches in a bake-off that becomes the CTO memo. Each student chooses a capstone ticket at the end of the day.

---

## D4-1 · Data team: 「網店分類器對少數類別很弱，能不能指定生成第 k 類？」 (#9, 學習評量) → `13-conditional-diffusion-cfg`

```
【需求單 #D4-1】部門：數據組（虛構公司：曜嶼電子）
問題：           網店商品分類器對少數類別很弱，能不能「指定」生成第 k 類的圖來補資料？
現況痛點：       少數類別只有幾十張，分類器常認錯
成功指標（KPI）： 生成圖被分類器認對的比例（忠實度）；FID／KID（多樣性與品質）
可用資料：       Fashion-MNIST（10 類）；D3-3 的 DDPM
限制與法規：     Colab T4；合成資料可能放大偏差
為何現有工具不夠： D3-3 的 DDPM 只能「隨機」生成，不能指定類別
今天要用的工具：  類別條件 DDPM、classifier-free guidance（CFG）
```

Objectives: add a class embedding; train with label dropout; read the CFG mixing rule as one line and **explain it without AI** (學習評量 oral check); measure fidelity vs diversity across guidance scales.

| # | Title | Mark | Takeaway | Content / visual | Lab · cite |
|---|---|---|---|---|---|
| 1–3 | Cover · Ticket · Objectives | ★ | — | — | — |
| 4 | Frame: p(x\|y) again | ★ | The D1-1 condition, now in code | Two-cluster picture recalled | D1-1 |
| 5 | Try: sample class k from the instructor model | ★ | Pick "sneaker" → sneakers | Grid placeholder | L4-1 |
| 6 | Class embedding + time embedding | ★ | Label → vector, added to t | Diagram on the D3-3 U-Net | D3-3 |
| 7 | Classifier guidance (picture) | ○ | An external classifier pushes samples | Arrow field picture | — |
| 8 | Label dropout | ★ | Sometimes hide the label → one model learns both | Training batch picture | — |
| 9 | The CFG line | ★ | ε = ε_uncond + w·(ε_cond − ε_uncond) | One annotated line, every symbol named + Chinese reading | roadmap §11 |
| 10 | Practice (no-AI): explain your CFG line | ★ | 學習評量 oral check rehearsal | FillIn: what happens at w = 0, 1, 7 | — |
| 11 | Answer (hostOnly) | ★ | — | — | — |
| 12 | Guidance trade-off | ★ | Higher w → more faithful, less diverse | Scale grid (from lab) | L4-1 |
| 13 | FID/KID as distance between feature clouds | ★ | Picture of two clouds; small-sample caveat | Picture + code | ML pp.9–10 |
| 14 | Fidelity: does a classifier recognise them? | ★ | Accuracy of a Fashion-MNIST classifier on samples | Table (from lab) | D1-3 |
| 15 | Bayes derivation of guidance | △ | Appendix | ≤ 4 lines | — |
| 16–22 | Lab L4-1 pages 1–7 | ★ | Conditional DDPM + CFG; scale grid; fidelity; FID/KID | `lab13-cfg.ipynb` | L4-1 |
| 23 | 學習評量 (b): what to submit | ★ | Notebook + oral "explain your CFG line" | Checklist | roadmap §12 |
| 24 | Risk: synthetic data amplifies bias | ★ | Validate on real data | — | — |
| 25–27 | Summary · 隨堂檢核 · 下一步 (hostOnly) | ★ | — | MCQ ×4 | — |

Lab L4-1 (`lab13-cfg.ipynb`, ~60 min): warm start from L3-3; class embedding; label dropout p ≈ 0.1; guidance-scale grid; classifier accuracy on samples; FID/KID with small-sample settings (to verify). **This is the 學習評量 「實作條件生成」 notebook.**

---

## D4-2 · Marketing: 「依企劃文字生成產品情境照，還要換背景」 (#9, goal 8, K8, K9) → `14-stable-diffusion-studio`

```
【需求單 #D4-2】部門：行銷部（虛構公司：曜嶼電子）
問題：           依企劃文字生成產品情境照，並替現有產品照換背景
現況痛點：       每次活動都要外拍
成功指標（KPI）： CLIP 分數；行銷部可用率；人物提示的偏差檢查
可用資料：       企劃文字；自有產品照
限制與法規：     Colab T4（512px、fp16）；著作權與風格模仿
為何現有工具不夠： D4-1 只能用類別當條件，不能用一段文字
今天要用的工具：  CLIP、Stable Diffusion 1.5、img2img、inpainting
```

Objectives: explain CLIP's shared embedding and compute cosine similarity; draw the SD anatomy (VAE + U-Net + text encoder + scheduler); control steps, scheduler, CFG, seed, negative prompt; use img2img and inpainting; measure CLIP score; run a bias audit.

| # | Title | Mark | Takeaway | Content / visual | Lab · cite |
|---|---|---|---|---|---|
| 1–3 | Cover · Ticket · Objectives | ★ | — | — | — |
| 4 | Frame: text as the condition, 512px on a T4 | ★ | Latent space makes it affordable | Recall D2-3 numbers | D2-3 |
| 5 | Try: SD1.5 text-to-image | ★ | Brief → photo | Placeholder + seed caption | L4-2 |
| 6 | CLIP block 1: one space for text and images | ★ | Contrastive training pulls pairs together | Matrix picture | — |
| 7 | CLIP block 2: cosine similarity in code | ★ | Dot product of unit vectors | Code cell + worked numbers | ML pp.64–67 |
| 8 | Practice: which caption matches? | ★ | Predict, then compute | FillIn | L4-2 |
| 9 | Answer (hostOnly) | ★ | — | — | — |
| 10 | SD anatomy | ★ | VAE (D2-3) + U-Net (D3-3) + text encoder + scheduler | Anatomy diagram with shapes | D2-3, D3-3 |
| 11 | Cross-attention (picture only) | ★ | Image patches look up words | Picture; details in D5 | D5-1 |
| 12 | Pipeline parameters | ★ | Steps, scheduler, CFG, seed, negative prompt | Parameter sweep grid (from lab) | D1-2, D4-1 |
| 13 | img2img strength | ★ | How much noise to add to the starting photo | Strength strip | D3-4 |
| 14 | Inpainting: mask + 9-channel input | ★ | Conditioning by concatenation | Channel diagram 4+1+4 | — |
| 15 | CLIP score across CFG | ★ | Higher CFG → higher CLIP score up to a point | Plot (from lab) | — |
| 16 | Bias audit on prompts with people | ★ | Count attributes across seeds | Tally table | — |
| 17 | ControlNet (instructor demo) | ○ | Layout/pose control | Demo placeholder | — |
| 18 | Inpaint synthetic defects for YOLOv8 | ○ | Data augmentation | Picture | DL pp.56–62 |
| 19 | Scheduler math | △ | Appendix | — | — |
| 20–26 | Lab L4-2 pages 1–7 | ★ | SD1.5 studio: sweeps, background swap, CLIP score | `lab14-sd-studio.ipynb` | L4-2 |
| 27 | Ship: product image studio (Day 4 ship) | ★ | Gradio Blocks with tabs | Screenshot placeholder | D1-4 |
| 28 | Risk: copyright, style imitation, bias, watermark/C2PA | ★ | — | Checklist | — |
| 29–31 | Summary · 隨堂檢核 · 下一步 (hostOnly) | ★ | — | MCQ ×4 | — |

Lab L4-2 (`lab14-sd-studio.ipynb`, ~60 min): SD1.5 mirror fp16 (pin mirror and check hashes); parameter sweeps; inpainting background swap; CLIP score; Gradio studio.

---

## D4-3 · Brand: 「生成的圖必須是我們的產品、我們的風格」 (K7, #9) → `15-lora-brand`

```
【需求單 #D4-3】部門：品牌部（虛構公司：曜嶼電子）
問題：           生成的圖必須是「我們的」產品、品牌一致的風格
現況痛點：       提示詞描述不出我們的產品外觀，每次都不一樣
成功指標（KPI）： 前後對照網格；產品辨識度；沒有過度擬合（姿勢背景都一樣）
可用資料：       約 10 張學員自己拍的產品照（自有、同意使用）
限制與法規：     Colab T4（512px、梯度檢查點、8-bit Adam）；訓練圖的授權與同意
為何現有工具不夠： 只靠提示詞無法描述特定產品
今天要用的工具：  IP-Adapter、DreamBooth-LoRA
```

Objectives: use IP-Adapter as the no-training baseline; draw W + B·A and count parameters; explain DreamBooth's identifier token; train a LoRA within T4 limits; detect overfitting.

| # | Title | Mark | Takeaway | Content / visual | Lab · cite |
|---|---|---|---|---|---|
| 1–3 | Cover · Ticket · Objectives | ★ | — | — | — |
| 4 | Frame: a prompt can't describe our product | ★ | — | Failed prompt grid (from lab) | D4-2 |
| 5 | Try: IP-Adapter with one reference photo | ★ | No training, decent likeness | Placeholder | L4-3 A |
| 6 | Full fine-tuning vs LoRA | ★ | Freeze W, learn a thin update | Two diagrams | DL pp.56–66 |
| 7 | LoRA picture: W + B·A | ★ | Two thin matrices | Picture + parameter count arithmetic | roadmap §11 |
| 8 | Practice: count LoRA parameters | ★ | 768×768 layer, rank 4/8/16 | FillIn | — |
| 9 | Answer (hostOnly) | ★ | — | — | — |
| 10 | DreamBooth: identifier token + few images | ★ | "a photo of sks earbuds" | Picture | — |
| 11 | T4 configuration | ★ | 512px, gradient checkpointing, 8-bit Adam, fp16 | Config table | D1-4 |
| 12 | Overfitting and prior preservation | ★ | Same pose everywhere = memorised | Grid comparison (from lab) | — |
| 13 | Textual inversion | ○ | Named only | — | — |
| 14 | Rank and alpha math | △ | Appendix | — | — |
| 15–21 | Lab L4-3 pages 1–7 | ★ | IP-Adapter vs DreamBooth-LoRA | `lab15-lora.ipynb` | L4-3 |
| 22 | Risk: consent, IP, imitating other brands | ★ | Only owned photos | — | — |
| 23–25 | Summary · 隨堂檢核 · 下一步 (hostOnly) | ★ | — | MCQ ×4 | — |

Lab L4-3 (`lab15-lora.ipynb`, ~60 min): IP-Adapter baseline; DreamBooth-LoRA on ~10 owned photos at 512px (training time to measure; instructor LoRA as fallback); before/after grid; SDXL only as instructor demo.

---

## D4-4 · CTO: 「GAN 還是擴散？哪個當公司標準？能不能即時？」 (學習評量, K9) → `16-bakeoff-memo`

```
【需求單 #D4-4】部門：技術長室（虛構公司：曜嶼電子）
問題：           季節性產品照編修要定一個公司標準：GAN 還是擴散？能不能接近即時？
現況痛點：       各部門各用各的工具，品質與授權風險不一
成功指標（KPI）： 比較表（品質、多樣性、速度、穩定性、可控性、授權）＋一頁備忘錄
可用資料：       一張季節性產品照
限制與法規：     Colab T4；三種方法的授權
為何現有工具不夠： 沒有用同一個任務、同一把尺比較過
今天要用的工具：  CycleGAN、InstructPix2Pix、SD1.5＋LCM-LoRA；2D flow matching 玩具
```

Objectives: run a three-way bake-off on one edit; explain how diffusion became fast (distillation → LCM; ADD = diffusion + adversarial loss; flow matching straight paths); collect individual preference ratings; draft the CTO memo; choose a capstone ticket.

| # | Title | Mark | Takeaway | Content / visual | Lab · cite |
|---|---|---|---|---|---|
| 1–3 | Cover · Ticket · Objectives | ★ | — | — | — |
| 4 | Frame: decision criteria | ★ | Trilemma + stability + control + licence | Criteria table | D3 |
| 5 | Try: one edit, three ways | ★ | CycleGAN / InstructPix2Pix / SD+LCM | Three placeholders + timings | L4-4 |
| 6 | Distillation recap → few-step generators | ★ | Teacher many steps → student few steps | Picture | DL pp.67–72 |
| 7 | ADD/Turbo: the GAN loss lives on | ★ | Diffusion + adversarial loss | Diagram | D3-1 |
| 8 | Flow matching: straight paths (2D toy) | ★ | Curved vs straight trajectories | 2D toy plot (from lab) | — |
| 9 | Text-guided editing | ★ | "Make it winter" | Placeholder | — |
| 10 | Practice: rate the three outputs | ★ | Individual preference (FillIn), then class tally | FillIn | — |
| 11 | Human preference evaluation | ★ | Why ratings beat a single metric here | Tally table (live) | — |
| 12 | Consistency models; DiT preview | ○ | Named; DiT payoff in D5-2 | — | D5-2 |
| 13 | Rectified-flow math | △ | Appendix | — | — |
| 14–18 | Lab L4-4 (3-page pattern + practice) | ★ | Bake-off + 2D flow toy (CPU) | `lab16-bakeoff.ipynb` | L4-4 |
| 19 | The memo brief (學習評量 a) | ★ | Recommend GAN or diffusion with own evidence | Brief + rubric | roadmap §12 |
| 20 | Memo skeleton from the trilemma table | ★ | Table → paragraphs | Template | — |
| 21 | Choose your capstone ticket | ★ | One ticket, data, model, KPI | Proposal template (FillIn) | roadmap §12 |
| 22 | Risk: licence comparison | ★ | CycleGAN BSD, InstructPix2Pix (verify), LCM-LoRA openrail++; SDXL-Turbo NC counter-example | Table | §9.2 |
| 23 | Day 4 summary | ★ | — | Chain | — |
| 24 | Day 4 iPAS quiz (6) | ★ | — | MCQ | — |
| 25 | Day 4 homework | ★ | Memo draft, finish L4-1, capstone proposal | — | — |
| 26 | 下一步 (hostOnly) | ★ | D5 support desk | — | — |

Lab L4-4 (`lab16-bakeoff.ipynb`, ~45 min): pretrained CycleGAN, InstructPix2Pix, SD1.5 + LCM-LoRA on the same photo with timings; 2D flow-matching toy on CPU.
