# D4-3 · 我們的產品、我們的風格 · 工作筆記

最後更新：2026-11-25。

## 1. 檔案

| 檔案 | 用途 |
|---|---|
| `outline.md` | 大綱（講師以 /goal 指示自動核准） |
| `slides.md` | 投影片（25 頁，其中 2 頁 hostOnly） |
| `teaching-plan.md` | 時間表 |
| `materials/src/lab15-lora.py` | 筆記本原始檔 |
| `materials/lab15-lora.ipynb`、`-solution.ipynb` | Lab L4-3 |

## 2. 進度

- [x] 大綱、投影片、筆記本
- [x] 本機：筆記本建置＋語法檢查（SD／LoRA 不在 CPU 實跑，依 /goal 指示）
- [ ] Colab T4 實跑；佔位圖與 Lab 7／7 表格
- [x] build、PNG 檢視、`check-order.cjs`、`scan-zh.py`
- [ ] slide-reviewer 審查（`planning/reviews-d4.md`）

## 3. 決定

| 日期 | 內容 |
|---|---|
| 2026-11-25 | 產品照用 Google DreamBooth 資料集的 `backpack`（6 張，Unsplash 授權，出處逐張列在該資料集）：曜嶼電子的生活用品線；不用電子產品是因為找不到授權清楚、同一件產品多角度的公開照片 |
| 2026-11-25 | 訓練迴圈寫在筆記本裡（約 15 行），不呼叫 diffusers 的訓練腳本：學員能對照 D3-3 的預測雜訊迴圈 |
| 2026-11-25 | 不用 8-bit Adam：只訓練 LoRA 時優化器狀態很小，少一個相依套件（bitsandbytes）；投影片說明它是另一個常用選項 |
| 2026-11-25 | 過度擬合用「和最像訓練照的 CLIP 影像相似度」量化，並和訓練照彼此的平均比較 |
| 2026-11-25 | prior preservation 只講概念，不實作（時間） |
| 2026-11-25 | 審查後：加 GradScaler 與 lora_B 範數檢查；加 LoRA 前先生成對照圖（稽核「原 U-Net 沒被改」）；過度擬合參考線改成「每張訓練照和其他張裡最像的」平均 |

## 4. 本單元詞彙（中文統一）

| 英文 | 中文 | 首次出現頁 |
|---|---|---|
| LoRA (Low-Rank Adaptation) | 低秩適應 | 6 |
| rank (r) | 秩 | 7 |
| DreamBooth | DreamBooth | 10 |
| identifier token | 識別字 | 10 |
| class noun | 類別詞 | 10 |
| gradient checkpointing | 梯度檢查點 | 11 |
| mixed precision | 混合精度 | 11 |
| prior preservation | 先驗保留 | 12 |
| textual inversion | textual inversion（只學一個字） | 13 |

## 5. 待講師注意

- 佔位圖與 Lab 7／7 表格等 T4 實跑。
