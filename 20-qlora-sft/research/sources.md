# 20-qlora-sft 查證紀錄

| id | 主張 | 來源 | 狀態 | 日期 |
|---|---|---|---|---|
| S1 | 可訓練參數 8,798,208（1.7497%）、轉接器 35.2 MB、前後回覆例子、提示注入結果 | lab20 講師本機 CPU 煙霧測試（`research/lab-runs.md`） | 已實跑（參數數為決定性） | 2026-11-26 |
| S2 | 訓練流程圖（預訓練 → SFT → 獎勵模型／偏好 → RL） | HF 部落格 *Illustrating RLHF*；InstructGPT（Ouyang et al., 2022） | 搜尋摘要；待確認 | 2026-11-26 |
| S3 | QLoRA：4-bit NF4 凍結基礎模型＋LoRA | Dettmers et al., *QLoRA*, 2023 | 待確認 | 2026-11-26 |
| S4 | LLM 評審的位置、長度、自我偏好偏差 | Zheng et al., *Judging LLM-as-a-Judge with MT-Bench*, 2023 | 待確認 | 2026-11-26 |
| S5 | DPO：用成對偏好資料、相對參考模型調整 | Rafailov et al., *Direct Preference Optimization*, 2023 | 待確認 | 2026-11-26 |
| S6 | Qwen2.5-0.5B-Instruct 授權 Apache-2.0 | HF 模型卡 | 待確認 | 2026-11-26 |
| S7 | trl 1.19 的 `SFTConfig(max_length, completion_only_loss…)`、`SFTTrainer(peft_config=…)`；prompt／completion 對話格式 | 本機 trl 1.19.0 實際執行 | 本機已驗證；Colab 版本待確認 | 2026-11-26 |
| S8 | T4 不支援 bf16 | NVIDIA T4（Turing 架構）規格 | 待確認 | 2026-11-26 |
