# D2-3 · 一張 T4 跑得動 512px 嗎？ · 工作筆記

最後更新：2026-11-24。

## 1. 檔案

| 檔案 | 用途 |
|---|---|
| `outline.md` | 大綱（自動核准） |
| `slides.md` | 投影片（28 頁，其中 2 頁 hostOnly） |
| `materials/src/lab07-vae.py` | 筆記本原始檔 |
| `materials/lab07-vae.ipynb`、`-solution.ipynb` | Lab L2-3 |
| `public/taipei-street.jpg` | 台北街景，lumoplank，CC0（Commons API 確認） |
| `public/fmnist-samples.png` | Fashion-MNIST 測試集前 16 張（資料本身，非模型輸出） |

## 2. 進度

- [x] 大綱、投影片、筆記本
- [x] 本機 CPU 煙霧測試
- [ ] Colab T4 實跑
- [x] build、PNG 檢視、`check-order.cjs`、`scan-zh.py`
- [x] slide-reviewer 審查（結果記在 `planning/reviews-2026-11-24.md`）

## 3. 決定

| 日期 | 內容 |
|---|---|
| 2026-11-24 | 潛在空間 2 維（畫得出散佈圖）；用同一個類別的 `variational` 開關做 AE 對照 |
| 2026-11-24 | SD VAE 用 `latent_dist.mode()`（不抽樣，結果可重現） |
| 2026-11-24 | 照片改用 CC0 台北街景（招牌小字最能看出壓縮損失），不用品牌耳機照 |

## 4. 本單元詞彙（中文統一）

| 英文 | 中文 | 首次出現頁 |
|---|---|---|
| latent space | 潛在空間 | 1 |
| VAE | 變分自編碼器 | 7 |
| reparameterization | 重參數化 | 8 |
| KL divergence | KL 散度 | 9 |
| ELBO | 證據下界 | 10 |
| interpolation | 內插 | 13 |
| PSNR | 峰值訊噪比 | 22 |
| memorisation | 背下訓練資料 | 24 |
