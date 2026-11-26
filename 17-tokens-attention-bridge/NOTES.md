# D5-1 · 客服單要花多少 token？注意力從哪裡來 · 工作筆記

最後更新：2026-11-26。

## 1. 檔案

| 檔案 | 用途 |
|---|---|
| `outline.md` | 大綱（講師指示自動核准） |
| `slides.md` | 投影片（26 頁，其中 3 頁 hostOnly） |
| `teaching-plan.md` | 時間表 |
| `materials/data/tickets.jsonl` | 40 張合成繁中客服單（附英文、類別、緊急程度）；D5-3、D5-4 複製使用 |
| `materials/src/lab17-tokens-attention.py` | 筆記本原始檔 |
| `materials/lab17-tokens-attention.ipynb`、`-solution.ipynb` | Lab L5-1 |
| `public/embed_sim.png`、`public/attention_heatmap.png` | 講師本機 CPU 實跑的輸出 |

## 2. 進度

- [x] 大綱、投影片、筆記本、合成資料
- [x] 本機 CPU 實跑（數字是決定性的：tokenizer 計數、BPE、fp32 注意力）
- [ ] 講師在 Colab 從頭跑一次，核對第 5、6、9、15、22 頁的數字（`research/lab-runs.md`）
- [x] build、PNG 檢視、`check-order.cjs`、`scan-zh.py`
- [x] slide-reviewer 審查

## 3. 決定

| 日期 | 內容 |
|---|---|
| 2026-11-26 | 單價用**假設值**（輸入 1、輸出 5 美元／百萬 token），不寫任何廠商報價；lab 要學員自己查價並寫日期 |
| 2026-11-26 | 成本模型去掉固定的系統提示詞：它會蓋掉語言差異；改成「回覆 ≈ 客服單 2 倍、同語言」，系統提示詞留給 D5-3 的 usage |
| 2026-11-26 | 熱力圖拿掉第一個 token（平均拿 0.47 的注意力，像休息站）再重新正規化，並在投影片說明 |
| 2026-11-26 | 誠實呈現：繁中比英文貴多少依 tokenizer 而定（1.02～1.84 倍），不寫成「繁中一定貴很多」 |
| 2026-11-26 | 手算練習用 d＝4（√d＝2），只需要 e^0、e^0.5、e^1 三個數 |

## 4. 本單元詞彙（中文統一）

| 英文 | 中文 | 首次出現頁 |
|---|---|---|
| BPE (Byte Pair Encoding) | 位元組對編碼 | 6 |
| embedding | 嵌入 | 3、9 |
| bag of words | 詞袋 | 10 |
| RNN | 循環神經網路 | 11 |
| hidden state | 隱藏狀態 | 11 |
| seq2seq | 序列到序列 | 12 |
| encoder / decoder | 編碼器／解碼器 | 12 |
| attention | 注意力 | 13 |
| query / key / value | 查詢／鍵／值 | 13 |
| self-attention | 自注意力 | 19 |
| LSTM / GRU | 長短期記憶／閘門循環單元 | 18 |

## 5. 待講師注意

- 第 5、6、9、15、22 頁的數字來自講師本機 CPU（tiktoken 0.14.0、transformers 5.24.0）；Colab 版本不同時 token 數可能有小差異，跑完請核對。
