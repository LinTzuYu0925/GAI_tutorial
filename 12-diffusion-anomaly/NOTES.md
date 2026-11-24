# D3-4 · AE 熱圖太模糊？用擴散模型修好板子再比對 · 工作筆記

最後更新：2026-11-25。

## 1. 檔案

| 檔案 | 用途 |
|---|---|
| `outline.md` | 大綱（講師以 /goal 指示自動核准） |
| `slides.md` | 投影片（28 頁，其中 2 頁 hostOnly） |
| `teaching-plan.md` | 時間表 |
| `materials/src/lab12-diffusion-ad.py` | 筆記本原始檔 |
| `materials/lab12-diffusion-ad.ipynb`、`-solution.ipynb` | Lab L3-4 |
| `materials/ddpm_pcb1_64.pt` | 講師檢查點（T4 實跑後放入） |

## 2. 進度

- [x] 大綱、投影片、筆記本
- [ ] 本機 CPU 煙霧測試（見 lab-runs）
- [ ] Colab T4 實跑；換掉佔位圖、填對照表
- [ ] build、PNG 檢視、`check-order.cjs`、`scan-zh.py`
- [ ] slide-reviewer 審查（結果記在 `planning/reviews-d3.md`）

## 3. 決定

| 日期 | 內容 |
|---|---|
| 2026-11-25 | 用 D2-1 同一個切分（SEED 0、70／15／15、不良品對半），AE 在 64 × 64 重新訓練，兩者同解析度比較 |
| 2026-11-25 | 去噪用自己寫的 DDIM（四行），比 diffusers 的排程器更看得清楚部分加噪的起點 |
| 2026-11-25 | t 與步數都在驗證集上選，測試集只算一次；門檻同 D2-1（驗證集漏檢 ≤ 5%） |
| 2026-11-25 | 檢查點預設從 GitHub 下載；下載不到會自動自己訓練（STEPS_DDPM）。第一次 T4 實跑就是走「自己訓練」，產生講師檢查點 |
| 2026-11-25 | 節拍時間假設 1 秒／片（虛構），筆記本 `TAKT_S` 可改 |

## 4. 本單元詞彙（中文統一）

| 英文 | 中文 | 首次出現頁 |
|---|---|---|
| takt time | 節拍時間 | 4 |
| partial diffusion | 部分加噪 | 6 |
| throughput | 處理量（每秒片數） | 12 |
| explainability | 可解釋性 | 14 |
| simplex noise | simplex 雜訊 | 15 |

## 5. 待講師注意

- 第 5、7、8、10、11、12、13、14 頁佔位圖與表格要等 T4 實跑。
