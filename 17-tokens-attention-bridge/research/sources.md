# 17-tokens-attention-bridge 查證紀錄

依 `technical-research-fact-checking`：只列實際讀過的來源；論文結果標明出處；無法查證者標「待確認」。

| id | 主張 | 來源 | 狀態 | 日期 |
|---|---|---|---|---|
| S1 | tiktoken 提供 `o200k_base`、`cl100k_base` 兩種編碼；o200k 詞彙表約 20 萬 | tiktoken 套件（本機 0.14.0 實際載入兩種編碼） | 編碼可用已驗證；對應哪些模型待確認 | 2026-11-26 |
| S2 | 40 張客服單的 token 數、BPE 合併、嵌入相似度、√d 實驗、熱力圖 | 本課 lab17 講師本機 CPU 實跑（`research/lab-runs.md`） | 已實跑；Colab 待核對 | 2026-11-26 |
| S3 | `Qwen/Qwen2.5-0.5B-Instruct`：詞彙表 151,936、隱藏維度 896；授權 Apache-2.0 | 本機載入的嵌入矩陣 shape；HF 模型卡 | shape 已驗證；授權待確認 | 2026-11-26 |
| S4 | BPE：重複合併最常出現的相鄰片段；GPT 系列從位元組開始 | HF LLM Course 第 6 章第 5 節；Karpathy minbpe（`planning/research/visual-survey-d5-d6.md`） | 搜尋結果摘要；頁面未完整閱讀 | 2026-11-26 |
| S5 | Bahdanau 注意力：解碼器對編碼器每個隱藏狀態算權重 | Bahdanau, Cho, Bengio, *Neural Machine Translation by Jointly Learning to Align and Translate*, 2014 | 待確認 | 2026-11-26 |
| S6 | 縮放內積注意力 softmax(QKᵀ/√d)V；Transformer 只用注意力 | Vaswani et al., *Attention Is All You Need*, 2017 | 待確認 | 2026-11-26 |
| S7 | 個資法：蒐集、處理、利用需特定目的與告知 | 個人資料保護法（全國法規資料庫） | 待確認（法務判斷，投影片只建立習慣） | 2026-11-26 |
| S8 | 注意力權重不一定是模型決策的解釋 | Jain & Wallace, *Attention is not Explanation*, 2019 | 待確認 | 2026-11-26 |
| S9 | 很多注意力集中在第一個 token（attention sink） | Xiao et al., *Efficient Streaming Language Models with Attention Sinks*, 2023；本 lab 量到 0.47 | 論文待確認；數字已實跑 | 2026-11-26 |
