# D4-1 · 指定生成第 k 類 · 工作筆記

最後更新：2026-11-25。

## 1. 檔案

| 檔案 | 用途 |
|---|---|
| `outline.md` | 大綱（講師以 /goal 指示自動核准） |
| `slides.md` | 投影片（27 頁，其中 2 頁 hostOnly） |
| `teaching-plan.md` | 時間表 |
| `materials/src/lab13-cfg.py` | 筆記本原始檔 |
| `materials/lab13-cfg.ipynb`、`-solution.ipynb` | Lab L4-1（學習評量 b） |

## 2. 進度

- [x] 大綱、投影片、筆記本
- [x] 本機 CPU 煙霧測試（見 lab-runs）
- [ ] Colab T4 實跑；第 5、12、14、16、22 頁
- [ ] build、PNG 檢視、`check-order.cjs`、`scan-zh.py`
- [ ] slide-reviewer 審查（結果記在 `planning/reviews-d4.md`）

## 3. 決定

| 日期 | 內容 |
|---|---|
| 2026-11-25 | FID／KID 用 lab 自己訓練的分類器特徵（128 維，以真實圖標準化），不下載 Inception：少一個相依套件，且讓學員看到「特徵點雲」的完整程式；投影片明說數字不能和論文比 |
| 2026-11-25 | 多樣性沿用 D3-1 的 `mean_pairwise`（同類兩兩距離），讓 GAN 與擴散用同一把尺 |
| 2026-11-25 | CFG 採 diffusers 的寫法 ε_uncond ＋ w·(ε_cond − ε_uncond)，w＝1 即一般條件模型；論文寫法差 1 在第 9 頁註明 |
| 2026-11-25 | D3-3 的 lab11 還不存在（平行建置中），lab13 自帶完整的小 U-Net 與排程，不載入 L3-3 的檢查點；第二階段再對齊符號 |

## 4. 本單元詞彙（中文統一）

| 英文 | 中文 | 首次出現頁 |
|---|---|---|
| class embedding | 類別嵌入 | 6 |
| embedding | 嵌入 | 6 |
| classifier guidance | 分類器引導 | 7 |
| label dropout | 標籤丟棄 | 8 |
| classifier-free guidance (CFG) | 無分類器引導 | 9 |
| guidance scale (w) | 指導強度 | 9 |
| fidelity | 忠實度 | 2 |
| FID / KID | FID／KID（特徵點雲的距離） | 13 |

## 5. 待講師注意

- 第 5、12、16、22 頁佔位圖與第 14 頁表格要等 T4 實跑。
- 學習評量（b）繳交方式。
