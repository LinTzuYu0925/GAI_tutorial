# 18-mini-gpt 查證紀錄

| id | 主張 | 來源 | 狀態 | 日期 |
|---|---|---|---|---|
| S1 | 迷你 GPT 的 loss、樣本、照抄率、Qwen 前 10 名、KV cache 秒數 | lab18 講師本機 CPU 實跑（`research/lab-runs.md`） | 已實跑；T4 待講師 | 2026-11-26 |
| S2 | Qwen2.5-0.5B：24 層、14 個注意力頭、2 個 KV 頭（GQA）、隱藏維度 896 | 本機快取的 `config.json` | 已確認 | 2026-11-26 |
| S3 | `Qwen/Qwen2.5-0.5B-Instruct` 授權 Apache-2.0 | HF 模型卡 | 待確認 | 2026-11-26 |
| S4 | 迷你字元 GPT 的結構（Head／MultiHead／Block） | Karpathy, nanoGPT 與 *Let's build GPT*（結構參考，程式為本課重寫） | 參考 | 2026-11-26 |
| S5 | Transformer、正弦位置編碼、縮放內積注意力 | Vaswani et al., *Attention Is All You Need*, 2017 | 待確認 | 2026-11-26 |
| S6 | DiT：以 Transformer 取代 U-Net、切塊成 token | Peebles & Xie, *Scalable Diffusion Models with Transformers*, ICCV 2023 | 待確認 | 2026-11-26 |
| S7 | GQA：多個頭共用 K、V | Ainslie et al., *GQA*, 2023 | 待確認 | 2026-11-26 |
| S8 | 圖解方式（文字接龍迴圈、區塊圖、溫度長條圖） | `planning/research/visual-survey-d5-d6.md`（李宏毅 GenAI 2024、Transformer Explainer、Illustrated GPT-2） | 搜尋摘要 | 2026-11-26 |
| S9 | 後來不少文字生圖模型改用 Transformer 去噪（例如 PixArt-α、SD3、FLUX） | 各模型的論文／模型卡 | 待確認 | 2026-11-26 |
