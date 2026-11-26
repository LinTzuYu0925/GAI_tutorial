# D6-2 · 用中文搜尋商品照 · 工作筆記

最後更新：2026-11-26。

## 1. 檔案

| 檔案 | 用途 |
|---|---|
| `outline.md`、`slides.md`（25 頁，其中 2 頁 hostOnly）、`teaching-plan.md` | 大綱、投影片、時間表 |
| `materials/src/make_catalog.py` → `materials/data/catalog/*.jpg`、`catalog.csv` | 40 張生成商品照（SD1.5＋LCM-LoRA，4 步，seed 100·類別＋變化） |
| `materials/src/fetch_catalog.py` | Commons 抓圖腳本（被 429 擋下，保留備用） |
| `materials/src/lab22-catalog-search.py` | 筆記本原始檔 |

## 2. 進度

- [x] 大綱、投影片、筆記本、商品照
- [x] 本機 CPU 實跑（第 1～3、5 部分；VLM 見 `research/lab-runs.md`）
- [ ] 講師 Colab T4 實跑：VLM 8 張替代文字、Gradio 截圖、VRAM
- [x] build、PNG 檢視、`check-order.cjs`、`scan-zh.py`
- [x] slide-reviewer 審查（13 FAIL：0 blocker、4 major；已修正）

## 3. 決定

| 日期 | 內容 |
|---|---|
| 2026-11-26 | Commons 批次下載被擋（429）→ 用 SD1.5＋LCM-LoRA 生成商品照：授權單純、可重現；投影片與 App 標示 AI 生成 |
| 2026-11-26 | 比較英文 CLIP 與多語 SigLIP 2（apache-2.0）；不用 jina-clip-v2（非商用） |
| 2026-11-26 | VLM 用 Qwen2-VL-2B-Instruct（apache-2.0，API 讀取確認），輸出跑 D5-4 的簡體字檢查＋大陸用語詞表 |
| 2026-11-26 | `scan-zh` 例外：lab 的 MAINLAND 詞表刻意列出大陸用語（同 D5-4） |

## 4. 本單元詞彙（中文統一）

| 英文 | 中文 | 首次出現頁 |
|---|---|---|
| contrastive learning | 對比學習 | 3、6 |
| zero-shot | 零樣本 | 3、5 |
| precision@k | 前 k 名精確率 | 3、9 |
| VLM | 視覺語言模型 | 3、11 |
| alt-text | 替代文字 | 3、11 |
| vector database | 向量資料庫 | 14 |
