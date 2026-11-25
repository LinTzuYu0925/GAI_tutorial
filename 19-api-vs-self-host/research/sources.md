# 19-api-vs-self-host 查證紀錄

| id | 主張 | 來源 | 狀態 | 日期 |
|---|---|---|---|---|
| S1 | `client.messages.create(model, max_tokens, system, messages, output_config)`；`usage.input_tokens／output_tokens`；`messages.count_tokens`；回應可能含思考區塊 | Claude Code 內建 claude-api 參考資料（Python README、token-counting） | 參考資料已讀 | 2026-11-26 |
| S2 | 2026-10-21 版 API 起，送 `temperature`／`top_p`／`top_k` 會回 400；`claude-opus-5-5` 思考不能關、effort 預設 medium | 同上（Thinking & Effort 表） | 參考資料已讀；官方文件待確認 | 2026-11-26 |
| S3 | 單價：`claude-opus-5-5` 4／20、`claude-haiku-5-5` 0.10／0.50 美元／百萬 token（Haiku 5.5 為 10 萬 token 以內的提示） | 同上（價格表，2026-11-03 快取） | 上線前請查官方價格頁 | 2026-11-26 |
| S4 | `parse_reply` 四個例子的結果；0.5B 本機測試的有效 JSON 與正確率 | lab19 本機 CPU 煙霧測試（`research/lab-runs.md`） | 已實跑 | 2026-11-26 |
| S5 | Qwen2.5-1.5B-Instruct 授權 Apache-2.0；Qwen2.5-3B-Instruct 為 Qwen Research License | HF 模型卡 license 欄位；課程地圖 §9.2 | 待確認 | 2026-11-26 |
| S6 | Gradio `share=True` 連結 72 小時有效 | Gradio 文件 | 待確認 | 2026-11-26 |
| S7 | NF4（QLoRA 論文）、GPTQ、AWQ | Dettmers et al. 2023；Frantar et al. 2022；Lin et al. 2023 | 待確認 | 2026-11-26 |
| S8 | 量化圖解（刻度、bytes／參數） | Grootendorst, *A Visual Guide to Quantization*（`planning/research/visual-survey-d5-d6.md`） | 搜尋摘要 | 2026-11-26 |
