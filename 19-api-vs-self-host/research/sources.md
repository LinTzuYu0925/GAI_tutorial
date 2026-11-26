# 19-api-vs-self-host 查證紀錄

| id | 主張 | 來源 | 狀態 | 日期 |
|---|---|---|---|---|
| S1 | `from google import genai; client.interactions.create(model, system_instruction, input, generation_config={"max_output_tokens"})`；`output_text`；用量 `usage.total_input_tokens／total_output_tokens`；套件 `google-genai`，金鑰環境變數 `GEMINI_API_KEY` | aistudio.google.com/docs（get-started、text-generation，由 ai.google.dev 轉址） | 文件已讀；用量欄位名稱文件只在 REST 範例出現，**尚未用真實金鑰在 Colab 跑過** | 2026-11-26 |
| S2 | 免費額度：輸入「可能被用來改進產品」（付費層不會）；有每分鐘／每天上限（數字在 AI Studio 儀表板，文件未列）；Gemini 4 與 3.6 以後模型會忽略 temperature／top_p／top_k | aistudio.google.com/docs（pricing、rate-limits） | 官方文件已讀；EEA／英國／瑞士免費層限制頁面未見，待確認 | 2026-11-26 |
| S3 | 單價：`gemini-3.5-flash-lite` 輸入 0.30／輸出 2.50 美元／百萬 token（付費層）；免費層不收費 | aistudio.google.com/docs/pricing | 官方價格頁；部分模型 2027-01-01 起調價，上線前請再查 | 2026-11-26 |
| S4 | `parse_reply` 四個例子的結果；0.5B 本機測試的有效 JSON 與正確率 | lab19 本機 CPU 煙霧測試（`research/lab-runs.md`） | 已實跑 | 2026-11-26 |
| S5 | Qwen2.5-1.5B-Instruct 授權 Apache-2.0；Qwen2.5-3B-Instruct 為 Qwen Research License | HF 模型卡 license 欄位；課程地圖 §9.2 | 待確認 | 2026-11-26 |
| S6 | Gradio `share=True` 連結 72 小時有效 | Gradio 文件 | 待確認 | 2026-11-26 |
| S7 | NF4（QLoRA 論文）、GPTQ、AWQ | Dettmers et al. 2023；Frantar et al. 2022；Lin et al. 2023 | 待確認 | 2026-11-26 |
| S8 | 量化圖解（刻度、bytes／參數） | Grootendorst, *A Visual Guide to Quantization*（`planning/research/visual-survey-d5-d6.md`） | 搜尋摘要 | 2026-11-26 |
