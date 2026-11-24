# D3-3 · GAN 一直畫一樣的圖？從零寫一個擴散模型 · 工作筆記

最後更新：2026-11-25。

## 1. 檔案

| 檔案 | 用途 |
|---|---|
| `outline.md` | 大綱（講師以 /goal 指示自動核准） |
| `slides.md` | 投影片（30 頁，其中 2 頁 hostOnly） |
| `teaching-plan.md` | 時間表 |
| `materials/src/lab11-ddpm.py` | 筆記本原始檔 |
| `materials/lab11-ddpm.ipynb`、`-solution.ipynb` | Lab L3-3 |
| `public/lab09-run-loss.png` | D3-1 的 GAN 損失曲線（lab09 講師 T4 實跑，從 09 複製） |

## 2. 進度

- [x] 大綱、投影片、筆記本
- [x] 本機 CPU 煙霧測試（見 lab-runs）
- [ ] Colab T4 實跑；換掉佔位圖、填 Lab 7／7 表格
- [ ] build、PNG 檢視、`check-order.cjs`、`scan-zh.py`
- [ ] slide-reviewer 審查（結果記在 `planning/reviews-d3.md`）

## 3. 決定

| 日期 | 內容 |
|---|---|
| 2026-11-25 | 和 D3-1 用同一個多樣性量法（32 張兩兩平均距離，28 × 28、−1～1），才能直接比 DCGAN 的 22.08 |
| 2026-11-25 | 第 4 頁照實說：D3-1 的 DCGAN 實跑沒有崩塌；今天比的是「多樣性有沒有保證」 |
| 2026-11-25 | 去噪網路沿用 D2-2 的 U-Net 結構（BatchNorm、MaxPool、`torch.cat` 跳接），只加時間嵌入；不換成論文的 GroupNorm，少一個新名詞 |
| 2026-11-25 | 資料整包放進 GPU，不用 DataLoader（Windows 本機測試時 worker 會出錯；T4 上也比較快） |
| 2026-11-25 | 檢查點用 fp16 存（約 4 MB），T4 實跑後放進 `materials/`，筆記本 `USE_CKPT＝True` 時從 raw.githubusercontent.com 下載 |

## 4. 本單元詞彙（中文統一）

| 英文 | 中文 | 首次出現頁 |
|---|---|---|
| diffusion model | 擴散模型 | 5 |
| DDPM | （保留英文；去噪擴散機率模型） | 5 |
| forward process | 往前加噪 | 6 |
| noise schedule | 雜訊排程 | 8 |
| timestep | 步數 t | 7 |
| time embedding | 時間嵌入 | 12 |
| sampling | 取樣 | 15 |
| scheduler | 排程器 | 17 |
| DDIM | （保留英文） | 17 |
| score matching | 分數匹配 | 18 |
| nearest neighbour | 最近鄰 | 27 |

## 5. 待講師注意

- 第 5、6、8、12、15、16、23、27 頁佔位圖與 Lab 7／7、三難表格要等 T4 實跑。
- 第 4 頁：D3-1 實跑沒有崩塌，講法見備註。
