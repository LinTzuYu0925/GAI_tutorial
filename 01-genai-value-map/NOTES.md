# D1-1 · GenAI 能為公司做什麼？ · 工作筆記

最後更新：2026-11-26。

## 1. 檔案

| 檔案 | 用途 |
|---|---|
| `outline.md` | 大綱（講師以 /goal 自動核准） |
| `slides.md` | 投影片（28 頁，其中 2 頁 hostOnly） |
| `components/` | 練習頁輸入欄位、下拉選單 `PickIn`、自動加總 `ScoreSum`、可點選的選擇題 `Mcq`（從 `templates/deck/` 複製） |
| `teaching-plan.md` | 時間表 |
| `materials/` | 本單元沒有筆記本；講師導覽用 D1-2 的解答筆記本，MusicGen 一格在 `materials/tour-musicgen.py` |
| `research/sources.md`、`research/lab-runs.md` | 查證紀錄；實跑紀錄 |

建置：本資料夾 `npm run dev`、`npm run build`、`npm run export:png`、`npm run export`。不要在此執行 `npm install`。

## 2. 進度

- [x] 大綱（自動核准）
- [x] 投影片
- [x] 講師導覽的三個輸出（第 6 頁）換成講師 T4 實跑結果（2026-11-24）
- [x] build、匯出 PNG 並逐頁檢視、`check-order.cjs`、`scan-zh.py`（2026-11-23）
- [x] polish_note01 修改（2026-11-26）：資料分布改成照片的亮度×鮮豔度（3 頁）、判別界線 vs 生成範圍、條件改成白貓／橘貓在 p_θ 裡；四面向加例子頁；用例畫布改名需求評估表，練習改成下拉選單＋自動加總並分成兩頁附圖；隨堂檢核改成可點選、答錯有解說
- [ ] slide-reviewer 審查

## 3. 決定

| 日期 | 內容 |
|---|---|
| 2026-11-23 | 一個 2 小時區塊一個 deck；本 deck 對應 D1-1 |
| 2026-11-23 | 練習不用分類任務題（只讀不跑），改成用例畫布（demo-and-practice §2） |
| 2026-11-26 | 「用例畫布」學員聽不懂，改叫「需求評估表」；第 18 頁註明英文 use-case canvas |
| 2026-11-26 | 資料分布的例子不用電路板（學員不熟線路密度），改用照片的亮度與鮮豔度 |

## 4. 本單元詞彙（中文統一）

| 英文 | 中文 | 首次出現頁 |
|---|---|---|
| discriminative model | 判別模型 | 7 |
| generative model | 生成模型 | 7 |
| data distribution | 資料分布 | 8 |
| sampling | 抽樣 | 9 |
| decision boundary | 界線 | 10 |
| condition | 條件 | 11 |
| SVM | 支援向量機 | 10 |
| Flow Matching | 流匹配 | 12 |
| multimodal | 多模態 | 12 |
| open weights | 開放權重 | 12 |
| use-case canvas | 需求評估表 | 18 |
| AOI | 自動光學檢測 | 21 |
| overkill (false reject) | 過殺（良品被誤判成瑕疵） | 21 |
| anomaly detection | 異常偵測 | 21 |
| hallucination | 幻覺 | 18 |
| Normalizing Flow | 正規化流 | 24 |

## 5. 翻譯略過與待講師注意

- 公司名稱為暫定，所有頁面標「虛構」。
