# D2-2 · 告訴我瑕疵在哪、有多大 · 工作筆記

最後更新：2026-11-24。

## 1. 檔案

| 檔案 | 用途 |
|---|---|
| `outline.md` | 大綱（自動核准） |
| `slides.md` | 投影片（30 頁，其中 3 頁 hostOnly） |
| `materials/src/lab06-unet-defect.py` | 筆記本原始檔 |
| `materials/lab06-unet-defect.ipynb`、`-solution.ipynb` | Lab L2-2 |
| `public/pcb1-scratch-*.{jpg,png}` | VisA PCB1 第 087 張（刮痕）與遮罩，講師本機裁切 |
| `public/synth-strip.png` | lab06 `synth_defect` 在講師本機產生的合成瑕疵條帶圖 |

## 2. 進度

- [x] 大綱、投影片、筆記本
- [x] 本機 CPU 煙霧測試（真實 VisA PCB1）
- [ ] Colab T4 實跑
- [x] build、PNG 檢視、`check-order.cjs`、`scan-zh.py`
- [x] slide-reviewer 審查（結果與修正記在 `planning/reviews-2026-11-24.md`）

## 3. 決定

| 日期 | 內容 |
|---|---|
| 2026-11-24 | 輸入 256×256（PCB1 瑕疵很小，128 會糊掉）；U-Net 三層、c＝32 |
| 2026-11-24 | 紋理只用程式產生的雜訊（不用 DTD 紋理資料集） |
| 2026-11-24 | 訓練加 180° 旋轉：PCB1 良品約八成倒著拍（D2-1 的資料陷阱） |
| 2026-11-24 | 面積校正用板寬 45 mm ÷ 946 像素（講師量測），取代假設值 |

## 4. 本單元詞彙（中文統一）

| 英文 | 中文 | 首次出現頁 |
|---|---|---|
| mask | 遮罩 | 2 |
| segmentation | 切割 | 3 |
| skip connection | 跳接 | 6 |
| concatenate | 接起來 | 8 |
| synthetic defect | 合成瑕疵 | 11 |
| BCE | 二元交叉熵 | 12 |
| Dice | （保留英文） | 12 |
| IoU | 交集比聯集 | 13 |
| calibration | 校正值 | 16 |
| checkerboard artifact | 棋盤格假影 | 19 |
