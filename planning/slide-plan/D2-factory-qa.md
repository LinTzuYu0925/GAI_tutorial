# Day 2 slide plan · 「找出從沒看過的瑕疵」

> **Status:** D2-1 auto-approved for production (2026-11-23, instructor /goal). D2-2…D2-4 are drafts awaiting approval (see bottom).
> **Source:** [course_roadmap.md](../course_roadmap.md) §7 Day 2, §9 L2-1…L2-4, §11. Conventions as in [D1-value-and-tooling.md](D1-value-and-tooling.md).
> **Decks:** D2-1 `05-ae-anomaly-detection` · D2-2 `06-unet-defect-mask` · D2-3 `07-vae-latent-space` · D2-4 `08-vqvae-tokens`.

**Day goal.** A student can train an autoencoder on good boards only, turn reconstruction error into a defect score and heatmap, pick a threshold from a business 漏檢 target, and then see how the same encoder–decoder diagram changes with skips (U-Net), a stochastic bottleneck (VAE) and a discrete bottleneck (VQ-VAE).

**Recurring visual.** One encoder–decoder diagram (encoder → bottleneck z → decoder). Each session changes one part; D2-1 introduces it.

---

## D2-1 · QA Line A: 「AOI 過殺太高，新瑕疵又漏檢；瑕疵樣本幾乎沒有」 (#3, #8 baseline, #2) → deck `05-ae-anomaly-detection`

### Ticket card

```
【需求單 #D2-1】部門：製造品保部（A 線）（虛構公司：曜嶼電子）
問題：           AOI 把太多好板判成不良（過殺），新型瑕疵卻會漏掉（漏檢）
現況痛點：       每天人工複判大量過殺板；新瑕疵每月出現，來不及標註
成功指標（KPI）： 在漏檢率 ≤ 5% 的前提下，過殺率比現況低；AUROC 報告
可用資料：       數百張良品影像；瑕疵影像很少而且沒有新瑕疵（用公開資料集 VisA PCB1 代替）
限制與法規：     Colab T4；資料集授權（VisA：CC BY 4.0，待確認）
為何現有工具不夠： DL 課的 CNN 分類器需要每一類瑕疵都有標註，沒看過的瑕疵分不出來
今天要用的工具：  卷積自編碼器（Conv AE）、重建誤差、門檻、AUROC、Gradio
```

### Objectives
1. **說明** why a supervised CNN fails on unseen defects and why an AE trained only on good boards can flag them.
2. **計算** a defect score from reconstruction error and **畫出** an error heatmap.
3. **選擇** a threshold from score histograms for a 漏檢 target and **換算** 過殺/漏檢 ↔ FP/FN.
4. **解讀** AUROC as threshold-free ranking quality.
5. **交付** a Gradio inspector (Day 2 ship).

### Slides (30, of which 3 hostOnly)

| # | Title | ★/○/△ | Objective | Takeaway | Content | Visual / example | Lab hook | Prior cite | Source |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Cover | ★ | — | Learn "normal", flag everything else | Chain 只有良品→AE→重建誤差→門檻→過殺/漏檢→檢測站 | Chain | — | — | — |
| 2 | 需求單 #D2-1 | ★ | Frame | — | Ticket card | Card | — | — | roadmap §4 |
| 3 | 學習目標 | ★ | — | — | — | List | — | — | — |
| 4 | Frame：為什麼 CNN 分類器做不到？ | ★ | Frame | No labels for defects nobody has seen yet | Classifier needs every class; new defect → forced into a known class | Classifier diagram with "？" class | — | DL pp.38–55 | — |
| 5 | 換個問法：只學「正常長什麼樣」 | ★ | Frame | Model normal; anything unusual is suspicious | Good-only training; analogy: 老師傅看久了，一眼看出怪怪的 | Analogy picture | — | — | — |
| 6 | Try：講師訓練好的 AE 標出瑕疵 | ★ | Try | The AE's heatmap lights up where the defect is | Input / reconstruction / heatmap for 2 boards | Placeholders until instructor run | L2-1 part D | — | S1 |
| 7 | AE 一頁回顧 → 今天的主角圖 | ★ | Open | Encoder squeezes, decoder rebuilds; z is the bottleneck | Recap in one line + the day's recurring diagram with shapes [B,3,128,128]→[B,128,8,8]→[B,3,128,128] | Recurring encoder–decoder diagram | L2-1 model | DL pp.72–79 | — |
| 8 | 為什麼重建誤差能抓瑕疵？ | ★ | Open | It rebuilds what it has seen; a defect is rebuilt as "normal" | Defect board → reconstruction without the scratch → difference = scratch | Before/during/after strip | L2-1 | — | — |
| 9 | 解碼器怎麼放大：ConvTranspose vs Upsample | ★ | Open | Two ways to go 16→32; same output shape | Code for both + shapes | Code | L2-1 | DL p.74 | S2 |
| 10 | 重建誤差熱力圖 | ★ | Open | Per-pixel \|x − x̂\|², averaged over channels → heatmap; mean → one score | Formula with Chinese reading; code 3 lines | Code + placeholder heatmap | L2-1 | — | — |
| 11 | 分數 = 有多「不典型」 | ★ | Open | Likelihood as typicality: low score = typical | Score histogram picture: good scores left, defect right, overlap in middle (教學示意) | Two histograms | L2-1 | — | roadmap §11 |
| 12 | 門檻：一條線決定判良或判不良 | ★ | Adapt | Moving the line trades 過殺 for 漏檢 | Histogram + movable threshold (two positions) | Two-panel | L2-1 | — | — |
| 13 | 過殺／漏檢 = FP／FN | ★ | Measure | 過殺 = good judged bad (FP); 漏檢 = bad judged good (FN) | 2×2 confusion table with factory words | Confusion table | L2-1 | ML pp.9–10 | — |
| 14 | 練習：移動門檻，算過殺與漏檢 | ★ | Measure | Student discovers the trade-off by counting | 10 good + 5 defect scores (教學用數字); thresholds 0.30/0.45/0.60 → count 過殺, 漏檢 | `table.fill` | — | — | — |
| 15 | 練習解答 (hostOnly) | ★ | — | — | Counts + how to tell | — | — | — | — |
| 16 | AUROC：不挑門檻，看排序好不好 | ★ | Measure | Probability a random defect scores above a random good board | ROC curve sketch; 0.5 = coin, 1.0 = perfect; `roc_auc_score` | ROC picture + code | L2-1 | ML pp.9–10 | S3 |
| 17 | 業界基準：PatchCore、EfficientAD | ★ | Measure | Our AE is the baseline; production uses stronger methods | Two named methods, one line each | Two boxes | — | — | S4, S5 |
| 18 | SSIM vs MSE；anomalib | ○ | Adapt | SSIM compares structure, MSE compares pixels | Comparison + library name | Table | Lab extension | — | S6 |
| 19 | AE 有時連瑕疵也重建得很好 | △ | Open | Identity shortcut: too much capacity copies everything | Sets up D2-2 (skips) and D3-4 | Picture | — | — | — |
| 20 | Lab 1/7：我們要做出什麼？ | ★ | Lab | Heatmaps + AUROC + threshold at 漏檢 ≤ 5% | Notebook link, VisA PCB1, T4, target placeholders, 3 questions | Page 1 | L2-1 | — | — |
| 21 | Lab 2/7：模型拆成哪幾塊？ | ★ | Lab | data → Encoder → z → Decoder → error map → score → threshold | Diagram with shapes; names match notebook (`ConvAE.encoder`, `.decoder`, `anomaly_map`, `score`) | Page 2 | L2-1 | — | — |
| 22 | 練習：每一塊的輸入與輸出 | ★ | Lab | No-AI checkpoint | FillIn table, first row filled | Page 3 | L2-1 | — | — |
| 23 | 練習解答 (hostOnly) | ★ | — | — | Filled + `print(x.shape)` | — | — | — | — |
| 24 | Lab 4/7：Specify | ★ | Lab | Four checkpoints before code | 【目標】【輸入與輸出】【限制】【驗收】 | Page 4 | L2-1 | — | — |
| 25 | Lab 5/7：Generate → Execute | ★ | Lab | Training loop reused from D1-3 | PromptBox; key excerpt (loss = MSE(x̂, x)); checkpoint fallback | Page 5 | L2-1 | D1-3 deck | — |
| 26 | Lab 6/7：Audit → Iterate | ★ | Lab | Check range, train-only-good, threshold from validation | Audit table + likely mistakes ([0,1] vs normalized, test leakage) | Page 6 | L2-1 | — | — |
| 27 | Lab 7/7：Ship — Gradio 檢測站 | ★ | Ship | Upload a board → heatmap + 判定 | Gradio code excerpt reusing D1-4 | Page 7 | L2-1 | D1-4 deck | — |
| 28 | Risk：過殺與漏檢的成本；資料集授權 | ★ | Measure | 漏檢 costs a customer return; 過殺 costs labour; VisA CC BY vs MVTec NC vs DeepPCB ambiguous | Cost table + licence table | Two tables | — | — | S7–S9 |
| 29 | 總整理 / 隨堂檢核 | ★ | — | (two slides) | MCQ ×4 | — | — | — | — |
| 30 | 下一步 (hostOnly) | ★ | — | — | D2-2 preview: 「瑕疵在哪、有多大」 | — | — | — | — |

(Slide 29 is two slides → deck total 31 incl. 3 hostOnly.)

### Lab L2-1 spec (`lab05-ae-anomaly.ipynb`, ~55 min)
- Data: VisA PCB1. Train = `train/good` subset; validation = held-out good + a few anomalies; test = remaining. The VisA archive is large (待確認 size); the instructor pre-extracts PCB1 to a shared Drive/HF dataset (open item). The notebook downloads from the official URL as the default and accepts a pre-extracted path.
- Resolution 128×128; Conv AE (3 down / 3 up), MSE loss, Adam 1e-3, 20 epochs (time 待實測), checkpoint every epoch (from D1-4).
- Outputs: loss curve; reconstruction grid; heatmaps; score histograms; AUROC; threshold at 漏檢 ≤ 5% on validation; 過殺 at that threshold on test.
- No-AI checkpoint: slide 22.
- Fallback: no GPU → 64×64, 3 epochs; disconnect → instructor checkpoint `ae_pcb1.pt`; dataset download fails → instructor mirror.

### Homework (Day 2, given at D2-4): second VisA category with a half-page threshold recommendation.

---

## D2-2…D2-4 · status

Drafts written 2026-11-23 (phase 3 of the /goal). **Awaiting instructor approval** before outlines are written. Same conventions as D2-1: ticket → objectives → loop blocks → 7-page lab → Measure & Risk → summary → 隨堂檢核 → hostOnly 下一步. Slide tables use a compact form (# · title · mark · takeaway · content/visual · lab/cite); the full ten-column table is filled when the deck's `outline.md` is written.

---

## D2-2 · QA: 「告訴我瑕疵在哪、有多大」 (#4) → deck `06-unet-defect-mask`

```
【需求單 #D2-2】部門：製造品保部（維修站）（虛構公司：曜嶼電子）
問題：           維修站要知道每個瑕疵的位置與面積，不只是「這片有問題」
現況痛點：       技術員拿放大鏡找瑕疵，一片要幾分鐘
成功指標（KPI）： 真實瑕疵遮罩上的 IoU／Dice；面積誤差（像素）
可用資料：       大量良品；幾乎沒有瑕疵遮罩（VisA PCB1；真實遮罩只用來測試）
限制與法規：     Colab T4；不能用來路不明的紋理資料集
為何現有工具不夠： D2-1 的 AE 只給一張模糊的誤差圖，沒有清楚的邊界
今天要用的工具：  U-Net、合成瑕疵（DRAEM 想法）、BCE＋Dice、IoU
```

Objectives: explain why skips suit segmentation but break reconstruction-based detection; build a U-Net and predict per-pixel masks; generate synthetic defects; measure IoU/Dice and area.

| # | Title | Mark | Takeaway | Content / visual | Lab · cite |
|---|---|---|---|---|---|
| 1–3 | Cover · Ticket · Objectives | ★ | Add skips → per-pixel answers | Chain; ticket card | — |
| 4 | Frame: a flag is not a location | ★ | Repair needs where + how big | D2-1 heatmap vs crisp mask, side by side | L2-1 output |
| 5 | Try: instructor U-Net overlay | ★ | Mask outlines the defect | Placeholders (input / mask / overlay) | L2-2 |
| 6 | The day's diagram + skips = U-Net | ★ | Skips carry fine detail across the bottleneck | Recurring diagram, skip arrows labelled with shapes | DL pp.72–79 |
| 7 | Why not add skips to the AE? | ★ | Skips copy the defect straight through → reconstruction looks perfect | Before/after: AE vs AE+skips residual | D2-1 △ slide |
| 8 | Concatenate vs add | ★ | U-Net concatenates channels; ResNet adds | [B,64,H,W]+[B,64,H,W] → [B,128,H,W] vs [B,64,H,W] | DL pp.38–55 |
| 9 | Practice: shapes through the U-Net | ★ | No-AI checkpoint | FillIn: down path, bottleneck, each up+concat | L2-2 |
| 10 | Answer (hostOnly) | ★ | — | — | — |
| 11 | No masks? Make defects (DRAEM idea) | ★ | Paste procedural textures with Perlin-style masks onto good boards | Strip: good → mask → texture → synthetic defect | DRAEM paper |
| 12 | Loss: per-pixel BCE + Dice | ★ | BCE per pixel; Dice fixes "most pixels are background" | One annotated line each; 4×4 worked example | DL pp.25–27 |
| 13 | IoU and Dice | ★ | Overlap ÷ union; Dice = 2·overlap ÷ total | Venn picture + numbers | — |
| 14 | Practice: IoU/Dice by hand | ★ | Discover Dice ≥ IoU | Two 5×5 masks, FillIn | — |
| 15 | Answer (hostOnly) | ★ | — | — | — |
| 16 | Area in pixels → mm² | ★ | The repair station's number | Pixel area × (mm/pixel)² with a given calibration | — |
| 17 | DRAEM's two networks | ○ | Reconstruct, then discriminate | Two-box picture | DRAEM |
| 18 | The U-Net returns as the diffusion denoiser | ○ | Same diagram, new job in D3-3 | Preview | D3-3 |
| 19 | Checkerboard artefacts | △ | ConvTranspose overlap → grid pattern | Picture | — |
| 20–26 | Lab L2-2 pages 1–7 | ★ | Goal → parts → practice/answer → Specify → Generate/Execute → Audit/Iterate → Ship overlay | `lab06-unet-defect.ipynb` | L2-2 |
| 27 | Risk: synthetic ≠ real | ★ | Always validate on real masks | Synthetic vs real IoU | — |
| 28–30 | Summary · 隨堂檢核 · 下一步 (hostOnly) | ★ | — | MCQ ×4 | — |

Lab L2-2 (`lab06-unet-defect.ipynb`, ~50 min): a 3-level U-Net on VisA PCB1 good images + synthetic defects (procedural noise textures only); tested on real VisA masks (instructor-prepared split). Outputs: overlays, IoU/Dice on real masks, area estimate. Checkpoint fallback. No-AI checkpoint: slide 9.

---

## D2-3 · Marketing-tech: 「每週要在一張 T4 上生成上千張 512px 圖」 (#5, #2) → deck `07-vae-latent-space`

```
【需求單 #D2-3】部門：行銷科技組（虛構公司：曜嶼電子）
問題：           第四天要大量生成 512px 商品圖，一張 T4 跑得動嗎？
現況痛點：       直接在像素上生成太貴（512×512×3 個數字）
成功指標（KPI）： 壓縮比與重建品質；潛在空間內插是否平滑
可用資料：       Fashion-MNIST（代替生活風格型錄縮圖）；一張自有產品照
限制與法規：     Colab T4；照片要自有或 CC0
為何現有工具不夠： AE 的潛在空間有「洞」，隨便取一點解碼出來是垃圾
今天要用的工具：  VAE、重參數化、KL、SD 的 AutoencoderKL
```

Objectives: explain why an AE latent space has holes; implement the μ/σ encoder and reparameterisation; read loss = reconstruction + KL as one annotated line; sample and interpolate; measure SD-VAE compression.

| # | Title | Mark | Takeaway | Content / visual | Lab · cite |
|---|---|---|---|---|---|
| 1–3 | Cover · Ticket · Objectives | ★ | — | — | — |
| 4 | Frame: pixels are expensive | ★ | 786,432 numbers per image | Arithmetic; link to D1-4 VRAM | — |
| 5 | Try: SD VAE round trip | ★ | 512×512×3 → 64×64×4 → back, almost identical | Placeholder pair + 48× fewer values | L2-3 B |
| 6 | Open: the AE latent space has holes | ★ | Points cluster; gaps decode to garbage | 2-D latent scatter (from lab) | L2-3 |
| 7 | The day's diagram: the bottleneck becomes a cloud | ★ | The encoder outputs μ and σ, not a point | Recurring diagram with a Gaussian at z | DL p.79 |
| 8 | Reparameterisation: z = μ + σ·ε | ★ | Randomness moves into ε so gradients flow | Code line + Chinese reading | — |
| 9 | Loss = reconstruction + KL | ★ | KL pulls each cloud toward the centre | Two-Gaussian picture + one annotated line + code | roadmap §11 |
| 10 | Why exact likelihood is hard; the ELBO named | ★ | We optimise a lower bound (ELBO), in words | Words only; derivation in △ | — |
| 11 | Practice: predict KL's effect | ★ | Without vs with KL scatter | FillIn prediction → run | L2-3 |
| 12 | Answer (hostOnly) | ★ | — | — | — |
| 13 | Sample new items; interpolate | ★ | Every point decodes to a plausible item | Sample grid + interpolation strip (from lab) | L2-3 |
| 14 | Why VAE samples are blurry | ○ | Averaging; GAN/diffusion decoders fix it | Picture | D3 |
| 15 | β-VAE | ○ | Sharpness vs smoothness knob | Grid | — |
| 16 | ELBO via Jensen | △ | Appendix derivation | ≤ 4 lines | — |
| 17–23 | Lab L2-3 pages 1–7 | ★ | VAE on Fashion-MNIST + SD-VAE round trip | `lab07-vae.ipynb` | L2-3 |
| 24 | Risk: memorisation | ★ | Generators can reproduce training items | Nearest-neighbour check | — |
| 25–27 | Summary · 隨堂檢核 · 下一步 (hostOnly) | ★ | — | MCQ ×4 | — |

Lab L2-3 (`lab07-vae.ipynb`, ~50 min): Fashion-MNIST VAE (latent 2 for the scatter, 16 for quality), AE vs VAE scatter, samples, interpolation; SD `AutoencoderKL` fp16 round trip on an owned/CC0 photo with compression ratio and PSNR.

---

## D2-4 · IT/Support: 「通話錄音與產線影像要低位元率儲存與串流」 (#6) → deck `08-vqvae-tokens`

```
【需求單 #D2-4】部門：資訊部／客服中心（虛構公司：曜嶼電子）
問題：           通話錄音與產線影像佔滿儲存空間，要用低位元率儲存與串流
現況痛點：       每月儲存費持續上升；串流到分廠很慢
成功指標（KPI）： 位元率與品質對照表；編碼簿使用率
可用資料：       合成客服通話音檔（講師製作）；Fashion-MNIST
限制與法規：     不能用真實客戶錄音（個資法）
為何現有工具不夠： VAE 的連續向量無法直接變成固定位元數的編號
今天要用的工具：  EnCodec、VQ-VAE、直通估計器
```

Objectives: explain codebook lookup and the straight-through estimator; compute bits per image; diagnose dead codes; see images and audio as tokens (preview of D5 and D6-1).

| # | Title | Mark | Takeaway | Content / visual | Lab · cite |
|---|---|---|---|---|---|
| 1–3 | Cover · Ticket · Objectives | ★ | — | — | — |
| 4 | Frame: bitrate vs quality | ★ | Storage cost ∝ bits | Cost table | — |
| 5 | Try: EnCodec at 1.5–24 kbps | ★ | Quality drops with bitrate | Audio players (placeholder) | L2-4 A |
| 6 | The day's diagram: the bottleneck snaps to a codebook | ★ | Each latent → nearest entry → an integer | Recurring diagram + codebook table | — |
| 7 | Nearest-neighbour lookup | ★ | argmin distance | 2-D picture + code | — |
| 8 | Straight-through estimator | ★ | Pretend the snap is the identity for gradients | `z_q = z + (z_q - z).detach()` with reading | — |
| 9 | Commitment + codebook losses | ★ | Pull codes and encoder outputs together | One annotated line | — |
| 10 | Bits per image = tokens × log2(K) | ★ | 7×7 tokens, K = 512 → 441 bits | Worked arithmetic | — |
| 11 | Practice: bits and compression ratio | ★ | Three configurations | FillIn | — |
| 12 | Answer (hostOnly) | ★ | — | — | — |
| 13 | Codebook usage and dead codes | ★ | Unused entries waste bits | Usage histogram (from lab) | L2-4 |
| 14 | Residual VQ = stacked codebooks (EnCodec) | ★ | Each stage codes the remaining error | Stack picture | EnCodec paper |
| 15 | Tokens = image/audio "words" | ★ | A language model can generate them (D5, D6-1) | Token grid → sequence | — |
| 16 | VQGAN | ○ | Adds adversarial + perceptual losses | Box diagram | D3-1 |
| 17 | EMA codebook updates | △ | Alternative to the codebook loss | — | — |
| 18–24 | Lab L2-4 pages 1–7 | ★ | EnCodec sweep + tiny VQ-VAE | `lab08-vqvae.ipynb` | L2-4 |
| 25 | Risk: real recordings are personal data | ★ | Synthetic audio only | — | 個資法 |
| 26 | Day 2 summary: one diagram, four bottlenecks | ★ | AE → U-Net → VAE → VQ-VAE | Recurring diagram ×4 | — |
| 27 | Day 2 iPAS quiz (6) | ★ | — | MCQ | — |
| 28 | Day 2 homework | ★ | Second VisA category + half-page threshold recommendation | — | — |
| 29 | 下一步 (hostOnly) | ★ | D3-1 GAN | — | — |

Lab L2-4 (`lab08-vqvae.ipynb`, ~50 min): EnCodec 24 kHz inference at 1.5/3/6/12/24 kbps on synthetic support-call audio (bits vs error table); tiny VQ-VAE (K = 64–512) on Fashion-MNIST with bits-vs-error and code-usage plots.
