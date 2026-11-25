# D4-2 · 產品情境照工作室 · 工作筆記

最後更新：2026-11-25。

## 1. 檔案

| 檔案 | 用途 |
|---|---|
| `outline.md` | 大綱（講師以 /goal 指示自動核准） |
| `slides.md` | 投影片（31 頁，其中 2 頁 hostOnly） |
| `teaching-plan.md` | 時間表 |
| `materials/src/lab14-sd-studio.py` | 筆記本原始檔 |
| `materials/lab14-sd-studio.ipynb`、`-solution.ipynb` | Lab L4-2 |

## 2. 進度

- [x] 大綱、投影片、筆記本
- [x] 本機：筆記本建置＋語法檢查（SD 不在 CPU 實跑，依 /goal 指示）
- [ ] Colab T4 實跑；佔位圖與第 9 頁數字
- [ ] build、PNG 檢視、`check-order.cjs`、`scan-zh.py`
- [ ] slide-reviewer 審查（`planning/reviews-d4.md`）

## 3. 決定

| 日期 | 內容 |
|---|---|
| 2026-11-25 | 「現有產品照」用 SD 生成的白底照代替：不需要上傳檔案、沒有授權問題；學員可換成自己的照片 |
| 2026-11-25 | 排程器用 DPM-Solver（25 步）；DDPM／DDIM 只在附錄認名字 |
| 2026-11-25 | 偏差稽核由學員人工計數，不用自動分類器判斷性別或年齡 |
| 2026-11-25 | 負面提示放在 CFG 那一行裡解釋（取代 ε_uncond），回答 D1-2 的觀察 |

## 4. 本單元詞彙（中文統一）

| 英文 | 中文 | 首次出現頁 |
|---|---|---|
| contrastive learning | 對比式學習 | 6 |
| cosine similarity | 餘弦相似度 | 7 |
| text encoder | 文字編碼器 | 4 |
| scheduler | 排程器 | 10 |
| cross-attention | 交叉注意力 | 11 |
| img2img | img2img（以圖生圖） | 13 |
| inpainting | 局部重繪 | 14 |
| CLIP score | CLIP 分數 | 15 |
| ControlNet | ControlNet | 17 |
| C2PA | 內容憑證 | 28 |

## 5. 待講師注意

- 所有佔位圖與第 9 頁數字等 T4 實跑。
