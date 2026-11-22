# D1-2 · 今晚就要文案和產品圖 · 工作筆記

最後更新：2026-11-23。

## 1. 檔案

| 檔案 | 用途 |
|---|---|
| `outline.md` | 大綱（講師以 /goal 自動核准） |
| `slides.md` | 投影片（26 頁，其中 3 頁 hostOnly） |
| `materials/src/lab02-genai-tour.py` | 筆記本原始檔；`python -X utf8 ../scripts/py2nb.py materials/src/lab02-genai-tour.py` 產生學員版與解答版 |
| `materials/lab02-genai-tour.ipynb`、`-solution.ipynb` | Lab L1-2 |
| `teaching-plan.md` | 時間表 |
| `research/sources.md`、`research/lab-runs.md` | 查證紀錄；實跑紀錄 |

## 2. 進度

- [x] 大綱（自動核准）
- [x] 投影片、Lab 筆記本（學員版、解答版）
- [ ] Colab T4 從頭跑完筆記本（尚未；所有輸出頁是 placeholder）
- [x] build、匯出 PNG 並逐頁檢視、`check-order.cjs`、`scan-zh.py`（2026-11-23）
- [ ] slide-reviewer 審查

## 3. 決定

| 日期 | 內容 |
|---|---|
| 2026-11-23 | 雲端 LLM 用 Anthropic Python SDK，模型 `claude-opus-5-5`；沒有金鑰自動跳過（開放模型備案） |
| 2026-11-23 | 影像用 SD1.5 鏡像＋LCM-LoRA（不用非商用的 SDXL-Turbo，roadmap §9.2） |
| 2026-11-23 | Lab 用 4 頁版本（目標／拆塊＋練習／Specify＋執行／稽核＋交付），因為本 Lab 只有 Try，沒有訓練 |

## 4. 本單元詞彙（中文統一）

| 英文 | 中文 | 首次出現頁 |
|---|---|---|
| pipeline | 管線（保留英文） | 6 |
| logit | 分數（logit） | 9 |
| sampling | 抽樣 | 10 |
| greedy decoding | 貪婪法 | 10 |
| temperature | 溫度 | 11 |
| seed | 亂數種子（seed） | 14 |
| negative prompt | 負面提示詞 | 16 |
| model card | 模型卡 | 22 |

## 5. 翻譯略過與待講師注意

- 第 6、7、9 頁與 Lab 第 1 頁的輸出是 placeholder，講師實跑後替換。
