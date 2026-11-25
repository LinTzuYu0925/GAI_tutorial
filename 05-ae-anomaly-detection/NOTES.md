# D2-1 · 找出從沒看過的瑕疵 · 工作筆記

最後更新：2026-11-23。

## 1. 檔案

| 檔案 | 用途 |
|---|---|
| `outline.md` | 大綱（自動核准） |
| `slides.md` | 投影片（33 頁，其中 3 頁 hostOnly） |
| `materials/src/lab05-ae-anomaly.py` | 筆記本原始檔 |
| `materials/lab05-ae-anomaly.ipynb`、`-solution.ipynb` | Lab L2-1 |

## 2. 進度

- [x] 大綱、投影片、筆記本
- [x] 本機 CPU 煙霧測試（合成資料）
- [ ] Colab T4 以 VisA PCB1 實跑
- [x] build、PNG 檢視、`check-order.cjs`、`scan-zh.py`
- [ ] slide-reviewer 審查

## 3. 決定

| 日期 | 內容 |
|---|---|
| 2026-11-23 | 瓶頸改成 [B,128,8,8]（計畫原寫 [B,64,16,16]）：窄一點，減少「照抄」 |
| 2026-11-23 | 分數用「誤差最大 1% 像素的平均」（瑕疵小，整張平均會稀釋） |
| 2026-11-23 | 門檻：驗證集上依排序計數，保證漏檢 ≤ 5%；測試集只算一次 |
| 2026-11-23 | 切分：良品 70／15／15；不良品一半驗證、一半測試（seed 0） |

## 4. 本單元詞彙（中文統一）

| 英文 | 中文 | 首次出現頁 |
|---|---|---|
| anomaly detection | 異常偵測 | 5 |
| autoencoder | 自編碼器 | 7 |
| bottleneck | 瓶頸 | 7 |
| reconstruction error | 重建誤差 | 8 |
| ConvTranspose | 轉置卷積 | 9 |
| heatmap | 熱力圖 | 10 |
| likelihood | 概似 | 11 |
| threshold | 門檻 | 12 |
| overkill／escape | 過殺／漏檢 | 2、13 |
| AUROC | （保留英文） | 16 |
| SSIM | 結構相似度 | 18 |
| identity shortcut | 照抄 | 19 |
