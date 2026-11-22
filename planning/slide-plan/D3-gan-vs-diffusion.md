# Day 3 slide plan · 「GAN 還是擴散？」

> **Status:** draft, awaiting instructor approval (written 2026-11-23, phase 3 of the /goal). Not auto-approved: only D1-1…D2-1 were.
> **Source:** [course_roadmap.md](../course_roadmap.md) §7 Day 3, §9 L3-1…L3-4, §11. Conventions as in [D1-value-and-tooling.md](D1-value-and-tooling.md); compact slide tables as in [D2-factory-qa.md](D2-factory-qa.md).
> **Decks:** D3-1 `09-gan-upscaling` · D3-2 `10-cyclegan-line-b` · D3-3 `11-ddpm-from-scratch` · D3-4 `12-diffusion-anomaly`.

**Day goal.** A student can explain a GAN as forger vs inspector and spot mode collapse; use CycleGAN for unpaired translation and check that defects survive; build a tiny DDPM (noise → predict noise → sample); and reuse diffusion for anomaly detection, comparing it with the D2-1 AE. The day fills the first rows of the **generative trilemma** table (quality, diversity, speed), which becomes the 學習評量 memo.

**Recurring visual.** The trilemma triangle; each session places one model on it with the student's own evidence.

---

## D3-1 · E-commerce: 「舊型錄照片解析度太低，網站改版用不了」 (#10) → `09-gan-upscaling`

```
【需求單 #D3-1】部門：電商部（虛構公司：曜嶼電子）
問題：           數千張舊型錄照片解析度太低，網站改版用不了
現況痛點：       重拍一張要上千元，數千張不可能
成功指標（KPI）： 4× 放大後細節清楚、沒有假細節誤導顧客；每張處理時間
可用資料：       舊型錄風格的低解析度照片（自有或 CC0）；Fashion-MNIST
限制與法規：     Colab T4；產品照不能誇大產品（消費者保護）
為何現有工具不夠： 一般放大（雙線性插值）只會變模糊；VAE 的樣本也偏模糊
今天要用的工具：  Real-ESRGAN、DCGAN
```

Objectives: name G and D roles; read the adversarial objective as one line and the non-saturating fix; apply DCGAN rules; recognise instability and mode collapse; list where adversarial losses still ship.

| # | Title | Mark | Takeaway | Content / visual | Lab · cite |
|---|---|---|---|---|---|
| 1–3 | Cover · Ticket · Objectives | ★ | — | — | — |
| 4 | Frame: blurry upscaling loses sales | ★ | We need plausible sharp detail | Bilinear vs target (placeholder) | — |
| 5 | Try: Real-ESRGAN 4× | ★ | Sharp detail in seconds | Before/after (placeholder, timing from lab) | L3-1 B |
| 6 | Open: forger vs inspector | ★ | G makes fakes; D says real/fake; both improve | Two-player picture | DL pp.82–84 |
| 7 | D is a classifier you already know | ★ | Binary CNN from DL | Code excerpt | DL pp.38–55 |
| 8 | The objective as one line | ★ | D maximises, G minimises the same score | One annotated line, every symbol named | roadmap §11 |
| 9 | Non-saturating G loss | ★ | Early on D wins and G gets no gradient → flip the label trick | Two curves picture | — |
| 10 | DCGAN rules | ★ | Strided conv, BatchNorm, LeakyReLU, no FC | Architecture strip with shapes | Radford et al. |
| 11 | Practice: shapes through G | ★ | No-AI checkpoint: z [B,100] → [B,1,28,28] | FillIn | L3-1 |
| 12 | Answer (hostOnly) | ★ | — | — | — |
| 13 | Training loop: two optimisers, alternate steps | ★ | D step then G step | Code excerpt (10 lines) | D1-3 loop |
| 14 | Instability: loss ≠ quality | ★ | GAN losses oscillate; judge by grids | Loss curves + grids over epochs (from lab) | L3-1 |
| 15 | Mode collapse | ★ | G finds one sample that fools D and repeats it | Grid with repeated items (from lab) | L3-1 |
| 16 | Practice: spot the collapse | ★ | Student labels grids from epochs 1/5/20 | FillIn | L3-1 |
| 17 | Answer (hostOnly) | ★ | — | — | — |
| 18 | GAN isn't legacy: where adversarial losses ship | ★ | Real-ESRGAN, SD VAE decoder, ADD/Turbo, HiFi-GAN/EnCodec | Map with links to D2-3, D2-4, D4-4 | CLAUDE.md decision |
| 19 | Conditional GAN preview; perceptual loss | ○ | Label in → chosen class out | Picture | D4-1 |
| 20 | WGAN / gradient penalty | △ | Named only | — | — |
| 21–27 | Lab L3-1 pages 1–7 | ★ | DCGAN on Fashion-MNIST + Real-ESRGAN | `lab09-dcgan-esrgan.ipynb` | L3-1 |
| 28 | Trilemma row 1: GAN | ★ | Quality ✓ speed ✓ diversity ✗ | Triangle with GAN placed | memo |
| 29 | Risk: invented detail | ★ | Upscaled photos must not misrepresent the product | Example | — |
| 30–32 | Summary · 隨堂檢核 · 下一步 (hostOnly) | ★ | — | MCQ ×4 | — |

Lab L3-1 (`lab09-dcgan-esrgan.ipynb`, ~55 min): DCGAN on Fashion-MNIST (grids saved every epoch, losses logged); Real-ESRGAN 4× on owned/CC0 low-res photos with timing. Watch-out: `basicsr` breaks with torchvision ≥ 0.17 → pin or patch, or use a loader without basicsr (to verify before class).

---

## D3-2 · QA Line B: 「新廠相機拍出來的影像不一樣，A 線模型一直誤報，又沒有成對影像」 (#11) → `10-cyclegan-line-b`

```
【需求單 #D3-2】部門：製造品保部（B 線）（虛構公司：曜嶼電子）
問題：           B 線換了相機，A 線的瑕疵模型在 B 線一直誤報
現況痛點：       B 線過殺率高；沒有「同一片板子在兩條線各拍一張」的成對影像
成功指標（KPI）： 轉換後 A 線模型在 B 線的過殺下降，且真實瑕疵沒有被抹掉
可用資料：       VisA PCB1（A 線）；合成的 B 線偏移（色溫、模糊、雜訊、光照）
限制與法規：     Colab T4；64–128px 短時間訓練
為何現有工具不夠： pix2pix 需要成對影像；重新標註 B 線太慢
今天要用的工具：  CycleGAN（參考實作）、D2-1 的 AE 檢測器
```

Objectives: distinguish paired vs unpaired translation; draw the CycleGAN (two G, two D); read cycle-consistency and identity losses; explain PatchGAN; evaluate whether defects survive translation.

| # | Title | Mark | Takeaway | Content / visual | Lab · cite |
|---|---|---|---|---|---|
| 1–3 | Cover · Ticket · Objectives | ★ | — | — | — |
| 4 | Frame: domain shift | ★ | Same board, different camera → different pixels → false alarms | A vs B image + D2-1 score histograms shifted (from lab) | L2-1 |
| 5 | Paired vs unpaired | ★ | No pairs → pix2pix impossible | Two diagrams | Isola et al. |
| 6 | Try: instructor snapshots B→A | ★ | Translation over epochs | Snapshot strip (placeholder) | L3-2 |
| 7 | CycleGAN = 2 generators + 2 discriminators | ★ | G: B→A, F: A→B; D_A, D_B | Architecture diagram | Zhu et al. |
| 8 | Cycle-consistency: A→B→A ≈ A | ★ | Without it, G can output any A-looking board | Round-trip picture + one annotated line | — |
| 9 | Identity loss | ★ | An A image fed to G should stay unchanged (keeps colour) | Picture | — |
| 10 | PatchGAN | ★ | D judges patches, not the whole image | Grid of patch verdicts | — |
| 11 | Practice: which loss stops which failure? | ★ | Match loss ↔ failure | FillIn | — |
| 12 | Answer (hostOnly) | ★ | — | — | — |
| 13 | The failure that matters: invented or erased features | ★ | A scratch can vanish in translation | Before/after with a defect (from lab) | L3-2 |
| 14 | Simpler fixes first | ○ | Colour normalisation; retrain AE on Line-B good images | Comparison table | — |
| 15 | Domain adaptation (CyCADA) | △ | Named only | — | — |
| 16–22 | Lab L3-2 pages 1–7 | ★ | Short CycleGAN run + measure 過殺 before/after + defect survival | `lab10-cyclegan.ipynb` | L3-2 |
| 23 | Risk: hallucinated features; deepfakes | ★ | High-stakes images need defect-level checks | — | — |
| 24–26 | Summary · 隨堂檢核 · 下一步 (hostOnly) | ★ | — | MCQ ×4 | — |

Lab L3-2 (`lab10-cyclegan.ipynb`, ~55 min): reference CycleGAN at 64–128px for a few epochs on synthetic Line-B shift; instructor snapshots from several epochs as fallback; L2-1 AE 過殺 before/after; defect-survival check on anomalous boards.

---

## D3-3 · Marketing: 「我們的 GAN 一直生出同樣的圖；要不要改用擴散模型？」 (#7, #2) → `11-ddpm-from-scratch`

```
【需求單 #D3-3】部門：行銷部（虛構公司：曜嶼電子）
問題：           GAN 生成器一直產生差不多的圖（模式崩塌），要不要改用擴散模型？
現況痛點：       型錄縮圖缺乏變化，設計師要手動挑
成功指標（KPI）： 樣本多樣性高於 DCGAN；取樣時間與步數的關係
可用資料：       Fashion-MNIST
限制與法規：     Colab T4；28–32px 小模型
為何現有工具不夠： GAN 多樣性差（D3-1 親眼看到）
今天要用的工具：  DDPMPipeline、自己訓練的小 DDPM
```

Objectives: draw the forward-noising strip; read one-step noising as one annotated line; explain predict-the-noise training; implement the time embedding and sampling loop; place diffusion on the trilemma.

| # | Title | Mark | Takeaway | Content / visual | Lab · cite |
|---|---|---|---|---|---|
| 1–3 | Cover · Ticket · Objectives | ★ | — | — | — |
| 4 | Frame: the trilemma | ★ | GAN: quality + speed, weak diversity | Triangle (from D3-1) | D3-1 |
| 5 | Try: a pretrained DDPM | ★ | Diverse samples, many steps | Grid + timing (placeholder) | L3-3 A |
| 6 | Open: dirty it, then learn to clean | ★ | Forward: add noise step by step | Strip x₀ … x_T (from lab) | DL pp.85–87 |
| 7 | Jump straight to step t | ★ | x_t from x₀ in one line | One annotated line: x_t = √ᾱ_t·x₀ + √(1−ᾱ_t)·ε, every symbol named | roadmap §11 |
| 8 | Noise schedule | ★ | β_t grows; ᾱ_t shrinks | Plot of ᾱ_t (from lab) | — |
| 9 | Training: predict the noise | ★ | MSE between true ε and predicted ε | Code excerpt (6 lines) | — |
| 10 | Misconception: it predicts noise, not the image | ★ | Named misconception | Before/after | slide-review R-C5 |
| 11 | The U-Net from D2-2 is the denoiser | ★ | Same diagram, input x_t + t | Recurring diagram | D2-2 |
| 12 | Time embedding (sinusoidal) | ★ | The network must know how noisy x_t is | Sin/cos stripe picture; returns in D5-2 | — |
| 13 | Practice: predict the strip | ★ | Which t looks like pure noise? | FillIn on slider values | L3-3 |
| 14 | Answer (hostOnly) | ★ | — | — | — |
| 15 | Sampling loop: T steps back | ★ | Start from noise, subtract predicted noise | Loop picture + code | — |
| 16 | Why diffusion trains stably | ○ | Plain regression loss, no two-player game | Comparison with D3-1 curves | — |
| 17 | HF schedulers | ○ | DDPM, DDIM in `diffusers` | Code | — |
| 18 | Score-matching view; ELBO link | △ | Appendix | — | — |
| 19–25 | Lab L3-3 pages 1–7 | ★ | Tiny DDPM, provided small U-Net, fallback checkpoint | `lab11-ddpm.ipynb` | L3-3 |
| 26 | Trilemma row 2: diffusion | ★ | Quality ✓ diversity ✓ speed ✗ | Triangle + student's own timing | memo |
| 27 | Risk: memorisation and copyright | ★ | Nearest-neighbour check against training set | — | — |
| 28–30 | Summary · 隨堂檢核 · 下一步 (hostOnly) | ★ | — | MCQ ×4 | — |

Lab L3-3 (`lab11-ddpm.ipynb`, ~60 min): forward strip, schedule plot, training a tiny DDPM on Fashion-MNIST at 28–32px with a provided small U-Net, sampling grid vs DCGAN grid, sampling time vs steps; fallback checkpoint.

---

## D3-4 · QA (return): 「AE 熱圖太模糊，細紋路一直過殺」 (#8) → `12-diffusion-anomaly`

```
【需求單 #D3-4】部門：製造品保部（A 線）（虛構公司：曜嶼電子）
問題：           D2-1 的 AE 熱力圖太模糊，細紋路一直被判成瑕疵（過殺）
現況痛點：       複判人力沒有減少
成功指標（KPI）： 同樣漏檢率下過殺低於 AE；每張處理時間符合產線節拍時間
可用資料：       D2-1 的 VisA PCB1 切分
限制與法規：     Colab T4；講師訓練好的擴散模型檢查點
為何現有工具不夠： AE 重建偏模糊，細節處誤差大
今天要用的工具：  部分加噪再去噪（AnoDDPM 想法）、DDIM
```

Objectives: explain partial-noise reconstruction; choose noise level t; cut latency with DDIM; compare with the AE on AUROC, 過殺 and throughput vs takt time.

| # | Title | Mark | Takeaway | Content / visual | Lab · cite |
|---|---|---|---|---|---|
| 1–3 | Cover · Ticket · Objectives | ★ | — | — | — |
| 4 | Frame: KPI + takt time | ★ | Accuracy and speed both count | KPI table | D2-1 |
| 5 | Try: diffusion "repairs" a board | ★ | Original / repaired / residual | Three placeholders | L3-4 |
| 6 | Partial noising to step t, then denoise | ★ | The result is a normal version of this board | Strip with t marked | AnoDDPM |
| 7 | Residual map | ★ | Same as D2-1, sharper reconstruction | Side-by-side with AE | D2-1 |
| 8 | Choosing t | ★ | Too low keeps the defect; too high loses the board | Three-t picture (from lab) | L3-4 |
| 9 | Practice: predict the best t | ★ | FillIn, then sweep | FillIn | L3-4 |
| 10 | Answer (hostOnly) | ★ | — | — | — |
| 11 | DDIM: fewer steps | ★ | Skip steps deterministically → lower latency | Step count vs time (from lab) | — |
| 12 | Throughput vs takt time | ★ | Images/s must beat the line | Arithmetic with measured time | — |
| 13 | AE vs diffusion table | ★ | AUROC, 過殺 at 漏檢 ≤ 5%, ms/image | Table (from lab) | L2-1, L3-4 |
| 14 | Show the operator the repaired board | ★ | Explainability | Operator view mock | — |
| 15 | PatchCore, EfficientAD again; simplex noise | ○ | Production baselines | — | — |
| 16 | DDAD | △ | Named only | — | — |
| 17–23 | Lab L3-4 pages 1–7 | ★ | t and step sweeps, AUROC vs AE, throughput | `lab12-diffusion-ad.ipynb` | L3-4 |
| 24 | Risk: deepfake-ad disclosure; misuse | ★ | 詐欺犯罪危害防制條例 (article to verify) | — | — |
| 25 | Day 3 summary: the trilemma table | ★ | GAN vs diffusion with own evidence | Table → memo | memo |
| 26 | Day 3 iPAS quiz (6) | ★ | — | MCQ | — |
| 27 | Day 3 homework | ★ | Extend the trilemma table; optional CycleGAN failure write-up | — | — |
| 28 | 下一步 (hostOnly) | ★ | D4-1 conditional generation | — | — |

Lab L3-4 (`lab12-diffusion-ad.ipynb`, ~50 min): instructor-trained DDPM checkpoint on the L2-1 category; t sweep and DDIM step sweep; AUROC and 過殺 vs L2-1; images per second.
