# 16-bakeoff-memo 查證紀錄

依 `technical-research-fact-checking`：只列實際讀過的來源；論文結果標明出處；無法查證者標「待確認」。

| id | 主張 | 來源（標題、URL、章節／頁） | 狀態 | 日期 |
|---|---|---|---|---|
| S1 | CycleGAN 預訓練模型 `summer2winter_yosemite`；`resnet_9blocks` 生成器；官方程式載入舊檔時刪除 InstanceNorm 的 running stats | junyanz/pytorch-CycleGAN-and-pix2pix（`scripts/download_cyclegan_model.sh`、`models/base_model.py` 的 `__patch_instance_norm_state_dict`） | 權重網址 2026-11-25 回應 HTTP 200；載入行為本機已驗證；程式碼細節待確認 | 2026-11-25 |
| S2 | LCM／LCM-LoRA：把 SD 蒸餾成 2～8 步；`latent-consistency/lcm-lora-sdv1-5`，guidance 1.0 | Luo et al., *Latent Consistency Models*, 2023；*LCM-LoRA*, 2023；HF 模型卡 | 待確認 | 2026-11-25 |
| S3 | ADD（Adversarial Diffusion Distillation）：蒸餾損失＋對抗損失，SDXL-Turbo 1～4 步 | Sauer et al., *Adversarial Diffusion Distillation*, 2023 | 待確認 | 2026-11-25 |
| S4 | Flow matching：沿 x_t＝(1−t)x₀＋t·x₁ 回歸速度 x₁ − x₀ | Lipman et al., *Flow Matching for Generative Modeling*, ICLR 2023 | 待確認 | 2026-11-25 |
| S5 | Rectified flow／reflow：用模型自己的配對重新訓練，讓軌跡更直，可 1 步生成 | Liu, Gong, Liu, *Flow Straight and Fast*, ICLR 2023 | 待確認 | 2026-11-25 |
| S6 | InstructPix2Pix：用 GPT-3 與 Prompt-to-Prompt 合成的成對編修資料訓練；文字與影像兩個 guidance | Brooks, Holynski, Efros, *InstructPix2Pix*, CVPR 2023 | 待確認 | 2026-11-25 |
| S7 | 授權：CycleGAN 程式 BSD；InstructPix2Pix 權重的授權；LCM-LoRA openrail++；SD1.5 CreativeML OpenRAIL-M | 各 GitHub LICENSE、HF 模型卡 | 待確認（逐一開模型卡核對） | 2026-11-25 |
| S8 | SDXL-Turbo 採非商業授權（反例：快，但不能直接商用） | `stabilityai/sdxl-turbo` 模型卡 | 待確認 | 2026-11-25 |
| S9 | Consistency models：一步從任何雜訊程度跳回資料 | Song et al., *Consistency Models*, ICML 2023 | 待確認 | 2026-11-25 |
| S10 | DiT：把 U-Net 換成 Transformer | Peebles & Xie, *Scalable Diffusion Models with Transformers*, ICCV 2023 | 待確認 | 2026-11-25 |
