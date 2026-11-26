# D5-2 · 模型怎麼寫出一封回覆 · 工作筆記

最後更新：2026-11-26。

## 1. 檔案

| 檔案 | 用途 |
|---|---|
| `outline.md` | 大綱（講師指示自動核准） |
| `slides.md` | 投影片（29 頁，其中 2 頁 hostOnly） |
| `teaching-plan.md` | 時間表 |
| `materials/src/make_replies.py` → `materials/data/replies.txt` | 合成客服回覆（模板、seed 2026） |
| `materials/data/minigpt_instructor.pt` | 講師權重（本機 CPU 2000 步，驗證 loss 0.172） |
| `materials/src/lab18-mini-gpt.py` | 筆記本原始檔 |
| `public/qwen_next_token.png`、`public/minigpt_loss.png` | 講師本機實跑輸出 |

## 2. 進度

- [x] 大綱、投影片、筆記本、語料
- [x] 本機 CPU 實跑（訓練 2000 步；`TRAIN=False` 備案路徑也跑過）
- [ ] 講師 Colab T4 實跑：訓練秒數、VRAM、KV cache 秒數（第 13、15、19、22 頁）
- [x] build、PNG 檢視、`check-order.cjs`、`scan-zh.py`
- [x] slide-reviewer 審查（12 FAIL：0 blocker、4 major；已修正，含新增「拿掉遮罩」實驗格與規格表）

## 3. 決定

| 日期 | 內容 |
|---|---|
| 2026-11-26 | 位置編碼用正弦（接 D3-3 時間嵌入），RoPE 只認名字 |
| 2026-11-26 | 語料是模板做的，loss 會低到 0.17：投影片直說「特別好猜」，用照抄率量「只會背 vs 亂寫」 |
| 2026-11-26 | 溫度掃 0.5／1.0／2.0（1.0 和 1.5 的樣本在本機完全相同，看不出差別），並示範 top-k／top-p 救回 T＝2.0 |
| 2026-11-26 | 不重複率一律 100%，沒有資訊量，刪掉 |
| 2026-11-26 | 「流暢≠正確」用語料裡真實存在的錯（電熱水壺支援 iPhone，52 次），不編造 |

## 4. 本單元詞彙（中文統一）

| 英文 | 中文 | 首次出現頁 |
|---|---|---|
| multi-head attention | 多頭注意力 | 6 |
| causal mask | 因果遮罩 | 3、7 |
| positional encoding | 位置編碼 | 8 |
| RoPE | 旋轉位置編碼 | 8 |
| LayerNorm | 層正規化 | 9 |
| feed-forward network | 前饋網路 | 9 |
| maximum likelihood | 最大概似 | 13 |
| temperature / top-k / top-p | 溫度／top-k／top-p | 14 |
| KV cache | KV 快取 | 15 |
| DiT | Diffusion Transformer | 16 |
| GQA / MQA | 分組／多查詢注意力 | 17 |
| hallucination | 幻覺 | 26 |
