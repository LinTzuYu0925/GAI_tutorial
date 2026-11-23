# D2-4 · 把影像和聲音變成編號 · 工作筆記

最後更新：2026-11-24。

## 1. 檔案

| 檔案 | 用途 |
|---|---|
| `outline.md` | 大綱（自動核准） |
| `slides.md` | 投影片（29 頁，其中 2 頁 hostOnly） |
| `materials/src/lab08-vqvae.py` | 筆記本原始檔 |
| `materials/lab08-vqvae.ipynb`、`-solution.ipynb` | Lab L2-4 |
| `public/visa-pcb2-capsules.jpg` | VisA pcb2、capsules 良品各一張（CC BY 4.0），作業頁用 |

## 2. 進度

- [x] 大綱、投影片、筆記本
- [x] 本機 CPU 煙霧測試（音訊用合成檔，見 lab-runs）
- [ ] Colab T4 實跑；第 5 頁頻譜圖（錄音下載被限流，待補）
- [x] build、PNG 檢視、`check-order.cjs`、`scan-zh.py`
- [x] slide-reviewer 審查（結果記在 `planning/reviews-2026-11-24.md`）

## 3. 決定

| 日期 | 內容 |
|---|---|
| 2026-11-24 | 不用真實或合成「客服通話」，改用公開授權的國語朗讀（台灣口音）：沒有個資問題、聲音是真的 |
| 2026-11-24 | 品質指標用頻譜誤差，不用 SNR（神經網路編碼器不保證相位） |
| 2026-11-24 | 第二天的總整理、小考、作業放在本單元最後 |

## 4. 本單元詞彙（中文統一）

| 英文 | 中文 | 首次出現頁 |
|---|---|---|
| bitrate (kbps) | 位元率 | 2 |
| codebook | 編碼簿 | 6 |
| vector quantization | 向量量化 | 6 |
| straight-through estimator | 直通估計器 | 8 |
| commitment loss | 承諾損失 | 9 |
| dead code | 死碼 | 13 |
| residual VQ | 殘差向量量化 | 14 |
| spectrogram | 頻譜圖 | 5 |
