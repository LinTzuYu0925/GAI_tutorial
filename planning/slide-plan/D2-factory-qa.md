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
| 7 | AE 一頁回顧 → 今天的主角圖 | ★ | Open | Encoder squeezes, decoder rebuilds; z is the bottleneck | Recap in one line + the day's recurring diagram with shapes [B,3,128,128]→[B,64,16,16]→[B,3,128,128] | Recurring encoder–decoder diagram | L2-1 model | DL pp.72–79 | — |
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

## D2-2…D2-4 (drafts, to be expanded in phase 3)

See the end of this file once written.
