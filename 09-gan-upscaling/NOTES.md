# D3-1 · 舊照片放大：偽造者與鑑定師 · 工作筆記

最後更新：2026-11-24。

## 1. 檔案

| 檔案 | 用途 |
|---|---|
| `outline.md` | 大綱（講師以 /goal 指示自動核准） |
| `slides.md` | 投影片（32 頁，其中 3 頁 hostOnly） |
| `teaching-plan.md` | 時間表 |
| `materials/src/lab09-dcgan-esrgan.py` | 筆記本原始檔 |
| `materials/lab09-dcgan-esrgan.ipynb`、`-solution.ipynb` | Lab L3-1 |
| `public/headphones-lowres.jpg` | 耳機照片原圖 233 × 263（Sprinno，CC0） |
| `materials/headphones.jpg` | 照片下載失敗時讓學員上傳（同一張 CC0 照片） |
| `public/lab09-run-*.png` | 講師 T4 實跑截圖（loss、網格、對照圖） |
| `public/headphones-bicubic-crop.png`、`headphones-esrgan-crop.png` | 4 倍放大後左耳罩同一塊：bicubic（PIL）與 Real-ESRGAN（本機實跑） |
| `research/sources.md`、`research/lab-runs.md` | 查證紀錄；實跑紀錄 |

## 2. 進度

- [x] 大綱、投影片、筆記本
- [x] 本機 CPU 煙霧測試（EPOCHS＝2，見 lab-runs）
- [x] Colab T4 實跑（舊版筆記本，見 lab-runs）；loss 曲線、網格、秒數、VRAM 已上投影片
- [ ] 重建後的筆記本在 T4 從頭重跑
- [x] build、PNG 檢視、`check-order.cjs`、`scan-zh.py`
- [x] slide-reviewer 審查（結果記在 `planning/reviews-2026-11-24.md`）

## 3. 決定

| 日期 | 內容 |
|---|---|
| 2026-11-24 | 放大用「真實」低解析商品照（CC0 耳機），不用合成縮小圖：學員看到的是真正的舊照片問題 |
| 2026-11-24 | Real-ESRGAN 用 `spandrel` 載入，不用 basicsr（basicsr 在新版 torchvision 常壞） |
| 2026-11-24 | DCGAN 用 Fashion-MNIST 28 × 28：T4 上幾分鐘就能看到網格變化；mode collapse 用「兩兩平均距離」量 |
| 2026-11-24 | 崩塌練習移到 Lab 5／7 之後：要用學員自己跑出的網格（審查意見） |
| 2026-11-24 | 本單元示範「假細節」：Real-ESRGAN 抹平耳罩凹紋、多出小亮點，連到風險頁 |

## 4. 本單元詞彙（中文統一）

| 英文 | 中文 | 首次出現頁 |
|---|---|---|
| super-resolution | 超解析（放大） | 2 |
| bicubic | 雙三次內插 | 4 |
| GAN | 生成對抗網路 | 6 |
| generator / discriminator | 生成器（偽造者）／鑑別器（鑑定師） | 6 |
| logit | 分數（還沒變成機率） | 7 |
| non-saturating loss | 不飽和損失 | 9 |
| transposed convolution | 轉置卷積 | 10 |
| mode collapse | 模式崩塌 | 15 |
| perceptual loss | 感知損失 | 17 |
| generative trilemma | 生成三難 | 28 |

## 5. 翻譯略過與待講師注意

- 第 15 頁的崩塌例子是「只有短靴的真圖」模擬（本機計算）；調大 LR_G 的實驗沒有崩塌，見 lab-runs。
- 第 29 頁的法規條號待確認（S8）。
