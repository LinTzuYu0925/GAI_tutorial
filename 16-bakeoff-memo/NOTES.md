# D4-4 · GAN 還是擴散？ · 工作筆記

最後更新：2026-11-25。

## 1. 檔案

| 檔案 | 用途 |
|---|---|
| `outline.md` | 大綱（講師以 /goal 指示自動核准） |
| `slides.md` | 投影片（26 頁，其中 2 頁 hostOnly；含第四天總整理、小考、作業） |
| `teaching-plan.md` | 時間表 |
| `materials/src/lab16-bakeoff.py` | 筆記本原始檔 |
| `materials/lab16-bakeoff.ipynb`、`-solution.ipynb` | Lab L4-4 |

## 2. 進度

- [x] 大綱、投影片、筆記本
- [x] 本機 CPU 煙霧測試（CycleGAN、flow 玩具；SD 部分待 T4）
- [ ] Colab T4 實跑；第 5、8、17、18 頁
- [x] build、PNG 檢視、`check-order.cjs`、`scan-zh.py`
- [ ] slide-reviewer 審查（`planning/reviews-d4.md`）

## 3. 決定

| 日期 | 內容 |
|---|---|
| 2026-11-25 | 原圖用 SD1.5＋LCM-LoRA 4 步生成（沒有授權問題；任何學員都能重現） |
| 2026-11-25 | CycleGAN 用官方 `summer2winter_yosemite`：它沒看過產品照，這正是「專門模型」的限制，寫進可控性 |
| 2026-11-25 | flow 玩具不宣稱軌跡是直的：本機試跑看到軌跡彎曲、1 步塌到中間；改成預測練習，並以 rectified flow 附錄解釋 |
| 2026-11-25 | 秒數一律暖機一次後再量：擴散 3 次平均、CycleGAN 10 次平均 |
| 2026-11-25 | 穩定性定義為「結果壞掉、不能用的比例」，和多樣性、訓練穩定性分開（審查意見） |
| 2026-11-25 | flow matching 的 x₀＝雜訊、x₁＝資料（沿用論文），和 D3-3 的 x₀＝原圖相反：第 8 頁講者備註提醒 |

## 4. 本單元詞彙（中文統一）

| 英文 | 中文 | 首次出現頁 |
|---|---|---|
| distillation (few-step) | 蒸餾（少步數） | 6 |
| LCM | LCM（潛在一致性模型） | 6 |
| ADD (Adversarial Diffusion Distillation) | 對抗式擴散蒸餾 | 7 |
| flow matching | flow matching（流匹配） | 8 |
| velocity | 速度 | 8 |
| InstructPix2Pix | InstructPix2Pix（文字指令編修） | 9 |
| human preference evaluation | 人的偏好評分 | 11 |
| consistency model | 一致性模型 | 12 |
| rectified flow | 整流（rectified flow） | 13 |

## 5. 待講師注意

- T4 實跑後替換佔位圖、填表；授權逐一確認。
- 學習評量（a）評分比重是建議值。
