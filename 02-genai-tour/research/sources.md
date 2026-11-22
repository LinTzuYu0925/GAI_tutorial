# 02-genai-tour 查證紀錄

**本次製作（2026-11-23）沒有上網核對；下列各項依作者既有知識撰寫，標「待確認」。** 筆記本最後一格會從 Hugging Face 讀出授權欄位，實跑時以其輸出為準。

| id | 主張 | 來源 | 狀態 | 日期 |
|---|---|---|---|---|
| S1 | Colab 可選 T4 GPU 執行階段 | Colab 說明文件 | 待確認 | 2026-11-23 |
| S2 | Qwen2.5-0.5B-Instruct：約 0.5B 參數、Apache-2.0 | https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct | 待確認 | 2026-11-23 |
| S3 | SD1.5 鏡像 `stable-diffusion-v1-5/stable-diffusion-v1-5`（原 runwayml 倉庫已移除），CreativeML OpenRAIL-M | Hugging Face 模型卡 | 待確認 | 2026-11-23 |
| S4 | LCM-LoRA `latent-consistency/lcm-lora-sdv1-5`，約 4 步，guidance_scale 約 1 | Luo et al. arXiv 2311.05556；diffusers LCM 文件 | 待確認 | 2026-11-23 |
| S5 | Anthropic Python SDK `client.messages.create(model, max_tokens, system, messages)`；回應為內容區塊列表，可能包含 thinking 區塊，所以只取 `type == "text"` | Claude API 文件（作者工具內建參考，2026-11） | 已依參考文件撰寫，待實跑 | 2026-11-23 |
| S6 | 不同 GPU、版本下相同 seed 不保證相同結果 | PyTorch 文件 *Reproducibility* | 待確認 | 2026-11-23 |
| S7 | 免費方案提示詞可能被用於改進服務；AI 生成物著作權保護在台灣仍在討論 | 各服務條款；經濟部智慧財產局相關函釋 | 待確認 | 2026-11-23 |
