# D1-2 · 今晚就要文案和產品圖 · 工作筆記

最後更新：2026-11-26。

## 1. 檔案

| 檔案 | 用途 |
|---|---|
| `outline.md` | 大綱（講師以 /goal 自動核准） |
| `slides.md` | 投影片（34 頁，其中 3 頁 hostOnly） |
| `materials/src/lab02-genai-tour.py` | 筆記本原始檔；`python -X utf8 ../scripts/py2nb.py materials/src/lab02-genai-tour.py` 產生學員版與解答版 |
| `materials/lab02-genai-tour.ipynb`、`-solution.ipynb` | Lab L1-2 |
| `teaching-plan.md` | 時間表 |
| `research/sources.md`、`research/lab-runs.md` | 查證紀錄；實跑紀錄 |

## 2. 進度

- [x] 大綱（自動核准）
- [x] 投影片、Lab 筆記本（學員版、解答版）
- [x] Colab T4 從頭跑完解答筆記本（2026-11-26，VS Code＋Colab 擴充功能；Part C 另在本機用金鑰跑）
- [x] build、匯出 PNG 並逐頁檢視、`check-order.cjs`、`scan-zh.py`（2026-11-23；polish 後 2026-11-26 重做）
- [ ] 解答筆記本保留 2026-11-26 實跑版本（未釘版本、`torch_dtype`）；原始檔已改 `dtype` 並釘版本，學員版尚未在 T4 從頭跑過
- [x] polish_note02 修改（2026-11-26）：VS Code 連 Colab 兩頁、Hugging Face Hub 一頁；雲端 API 改 Gemini 並拆成四頁（自己跑 vs API 圖、拿金鑰、兩種放金鑰、呼叫）；溫度前加 logit→softmax 圖；隨堂檢核改成可點選
- [ ] slide-reviewer 審查

## 3. 決定

| 日期 | 內容 |
|---|---|
| 2026-11-23 | ~~雲端 LLM 用 Anthropic Python SDK~~（2026-11-26 改為 Gemini） |
| 2026-11-26 | 雲端 LLM 用 Gemini 免費方案（`google-genai`），金鑰兩種放法：Colab 網頁版密鑰、`.env`（VS Code 連 Colab 只能用 `.env`） |
| 2026-11-26 | 學員用 VS Code＋Google Colab 擴充功能連 T4；Colab 網頁版為備案 |
| 2026-11-23 | 影像用 SD1.5 鏡像＋LCM-LoRA（不用非商用的 SDXL-Turbo，roadmap §9.2） |
| 2026-11-23 | Lab 用 4 頁版本（目標／拆塊＋練習／Specify＋執行／稽核＋交付），因為本 Lab 只有 Try，沒有訓練 |

## 4. 本單元詞彙（中文統一）

| 英文 | 中文 | 首次出現頁 |
|---|---|---|
| extension | 擴充功能 | 5 |
| Hugging Face Hub | （保留英文）放模型的網站 | 7 |
| pipeline | 管線（保留英文） | 8 |
| API key | API 金鑰 | 11 |
| Secrets | 密鑰（Colab 網頁版） | 12 |
| logit | 分數（logit） | 14 |
| sampling | 抽樣 | 15 |
| greedy decoding | 貪婪法 | 15 |
| temperature | 溫度 | 17 |
| seed | 亂數種子（seed） | 20 |
| negative prompt | 負面提示詞 | 22 |
| model card | 模型卡 | 7 |

## 5. 翻譯略過與待講師注意

- 所有輸出頁已換成 2026-11-26 實跑結果（research/lab-runs.md）。
- 待講師：第 5、6 頁可加 VS Code 連 Colab 的截圖；整本筆記本的總時間未計時；學員怎麼拿到筆記本（GitHub／雲端硬碟／課程網站）尚未決定（CLAUDE.md「Not ported」）。
