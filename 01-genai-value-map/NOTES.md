# D1-1 · GenAI 能為公司做什麼？ · 工作筆記

最後更新：2026-11-23。

## 1. 檔案

| 檔案 | 用途 |
|---|---|
| `outline.md` | 大綱（講師以 /goal 自動核准） |
| `slides.md` | 投影片（23 頁，其中 2 頁 hostOnly） |
| `components/` | 練習頁輸入欄位（從 `templates/deck/` 複製） |
| `teaching-plan.md` | 時間表 |
| `materials/` | 本單元沒有筆記本；講師導覽用 D1-2 的解答筆記本 |
| `research/sources.md`、`research/lab-runs.md` | 查證紀錄；實跑紀錄 |

建置：本資料夾 `npm run dev`、`npm run build`、`npm run export:png`、`npm run export`。不要在此執行 `npm install`。

## 2. 進度

- [x] 大綱（自動核准）
- [x] 投影片
- [ ] 講師導覽的三個輸出（第 6 頁 placeholder）在 Colab T4 實跑後替換
- [x] build、匯出 PNG 並逐頁檢視、`check-order.cjs`、`scan-zh.py`（2026-11-23）
- [ ] slide-reviewer 審查

## 3. 決定

| 日期 | 內容 |
|---|---|
| 2026-11-23 | 一個 2 小時區塊一個 deck；本 deck 對應 D1-1 |
| 2026-11-23 | 練習不用分類任務題（只讀不跑），改成用例畫布（demo-and-practice §2） |

## 4. 本單元詞彙（中文統一）

| 英文 | 中文 | 首次出現頁 |
|---|---|---|
| discriminative model | 判別模型 | 7 |
| generative model | 生成模型 | 7 |
| data distribution | 資料分布 | 8 |
| sampling | 抽樣 | 8 |
| condition | 條件 | 9 |
| multimodal | 多模態 | 10 |
| open weights | 開放權重 | 10 |
| hallucination | 幻覺 | 19 |
| use-case canvas | 用例畫布 | 15 |
| Normalizing Flow | 正規化流 | 20 |

## 5. 翻譯略過與待講師注意

- 公司名稱為暫定，所有頁面標「虛構」。
