# D5-3 · 雲端 API 還是自架模型 · 工作筆記

最後更新：2026-11-26。

## 1. 檔案

| 檔案 | 用途 |
|---|---|
| `outline.md` | 大綱（講師指示自動核准） |
| `slides.md` | 投影片（28 頁，其中 3 頁 hostOnly） |
| `teaching-plan.md` | 時間表 |
| `materials/data/tickets.jsonl` | 40 張合成客服單（從 D5-1 複製） |
| `materials/src/lab19-triage.py` | 筆記本原始檔 |

## 2. 進度

- [x] 大綱、投影片、筆記本
- [x] 本機 CPU 煙霧測試（Qwen2.5-0.5B 代替 1.5B、沒有金鑰；見 `research/lab-runs.md`）
- [ ] 講師 Colab T4 實跑（含 API 金鑰）：比較表、Gradio 畫面（第 17、21、24 頁佔位圖）
- [x] build、PNG 檢視、`check-order.cjs`、`scan-zh.py`
- [x] slide-reviewer 審查（17 FAIL：1 blocker、5 major；已修正）

## 3. 決定

| 日期 | 內容 |
|---|---|
| 2026-11-26 | 雲端模型預設 `claude-opus-5-5`（課程技能的預設），註解提供 `claude-haiku-5-5` 當便宜選項；單價寫在程式並標查價日期 |
| 2026-11-26 | 不在 API 呼叫送 `temperature`：2026-10-21 版 API 起會回 400；用 `output_config.effort="low"` |
| 2026-11-26 | 回應可能含思考區塊，只取 `type == "text"` 的區塊 |
| 2026-11-26 | 自架成本＝秒數 × 假設 GPU 租金（0.5 美元／小時），標示為假設 |
| 2026-11-26 | 0.5B 本機測試的摘要出現簡體字：留作 D5-4 的伏筆（不上投影片數字，只在講者備註提） |

## 4. 本單元詞彙（中文統一）

| 英文 | 中文 | 首次出現頁 |
|---|---|---|
| SDK | 軟體開發套件 | 3 |
| usage | 用量（token 數） | 5 |
| effort | 思考量 | 5 |
| chat template | 對話範本 | 10 |
| quantization | 量化 | 11 |
| GGUF / Ollama | — | 14 |
| streaming | 串流 | 16 |
| JSON schema | 欄位與型別的規格 | 16 |
| structured outputs | schema 強制輸出 | 16 |
