# D3-2 · 沒有成對影像的 B 線 · 工作筆記

最後更新：2026-11-24。

## 1. 檔案

| 檔案 | 用途 |
|---|---|
| `outline.md` | 大綱（講師以 /goal 指示自動核准） |
| `slides.md` | 投影片（26 頁，其中 2 頁 hostOnly） |
| `teaching-plan.md` | 時間表 |
| `materials/src/lab10-cyclegan.py` | 筆記本原始檔 |
| `materials/lab10-cyclegan.ipynb`、`-solution.ipynb` | Lab L3-2 |
| `public/line-a-vs-b.png` | A 線 vs 合成 B 線（VisA PCB1，CC BY 4.0；固定公式） |
| `public/horse.jpg`、`public/zebras.jpg` | 不成對資料的例子（CC0） |

## 2. 進度

- [x] 大綱、投影片、筆記本
- [x] 本機 CPU 煙霧測試（見 lab-runs）
- [ ] Colab T4 實跑；第 6、13、16 頁圖與 Lab 表格
- [x] build、PNG 檢視、`check-order.cjs`、`scan-zh.py`
- [x] slide-reviewer 審查（結果記在 `planning/reviews-2026-11-24.md`）

## 3. 決定

| 日期 | 內容 |
|---|---|
| 2026-11-24 | B 線用程式合成（偏暖、偏亮、對比、雜訊），因為沒有公開的「同類板子、兩台相機」資料；投影片明說是合成 |
| 2026-11-24 | 不用模糊／變暗：本機試跑發現會讓 AE 誤報變少，與需求單相反 |
| 2026-11-24 | 加入顏色正規化當基準：CycleGAN 要贏過簡單方法才值得用 |
| 2026-11-24 | 新增「瑕疵存活」指標（遮罩內 ÷ 遮罩外誤差）：只看過殺會選到把瑕疵也修掉的 G |

## 4. 本單元詞彙（中文統一）

| 英文 | 中文 | 首次出現頁 |
|---|---|---|
| domain shift | 分布偏移 | 4 |
| paired / unpaired | 成對／不成對 | 5 |
| cycle consistency | 循環一致 | 8 |
| identity loss | identity 損失（恆等） | 9 |
| PatchGAN | PatchGAN（分塊鑑別器） | 10 |
| deepfake | 深度偽造 | 23 |

## 5. 待講師注意

- 第 6、13、16 頁佔位圖與 Lab 6／7、7／7 表格要等 T4 實跑。
