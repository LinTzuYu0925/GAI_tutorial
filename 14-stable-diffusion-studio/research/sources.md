# 14-stable-diffusion-studio 查證紀錄

依 `technical-research-fact-checking`：只列實際讀過的來源；論文結果標明出處；無法查證者標「待確認」。

| id | 主張 | 來源（標題、URL、章節／頁） | 狀態 | 日期 |
|---|---|---|---|---|
| S1 | SD1.5 權重鏡像 `stable-diffusion-v1-5/stable-diffusion-v1-5`、`stable-diffusion-v1-5/stable-diffusion-inpainting`；CreativeML OpenRAIL-M | Hugging Face 模型卡 | 授權標籤已確認（2026-11-25）：creativeml-openrail-m；卡片寫「intended for research purposes only」，並說明是已下架 runwayml 版的鏡像 | 2026-11-25 |
| S2 | CLIP：4 億組圖文配對的對比式學習；圖與文字投影到同一空間 | Radford et al., *Learning Transferable Visual Models From Natural Language Supervision*, ICML 2021 | 待確認 | 2026-11-25 |
| S3 | `openai/clip-vit-base-patch32` 的投影維度 512 | 模型 config（`projection_dim`） | 待確認（以筆記本輸出為準） | 2026-11-25 |
| S4 | Latent Diffusion：VAE 潛在空間、U-Net 去噪、文字以 cross-attention 進入 U-Net | Rombach et al., *High-Resolution Image Synthesis with Latent Diffusion Models*, CVPR 2022 | 待確認 | 2026-11-25 |
| S5 | SD inpainting 模型 U-Net 有 9 個輸入通道（4 潛在＋1 遮罩＋4 遮罩後影像潛在） | `stable-diffusion-inpainting` 模型卡；筆記本印出 `in_channels` | 待 T4 輸出確認 | 2026-11-25 |
| S6 | diffusers 的 `guidance_scale`：ε_uncond ＋ w·(ε_cond − ε_uncond)；有負面提示時以它取代空字串的 ε_uncond；w ≤ 1 時不做 CFG | diffusers `StableDiffusionPipeline` 原始碼（`do_classifier_free_guidance`） | 待確認（D1-2 已觀察到 w＝1 時負面提示無效） | 2026-11-25 |
| S7 | CLIP score ＝ 100 × max(cos, 0) | Hessel et al., *CLIPScore*, EMNLP 2021（原式有權重 2.5）；torchmetrics `CLIPScore` 用 100× | 待確認：本 lab 用 100 × cos | 2026-11-25 |
| S8 | C2PA 內容憑證；生成圖加浮水印或標示 | c2pa.org 規格 | 待確認 | 2026-11-25 |
| S9 | ControlNet：以邊緣、姿勢等額外條件控制 SD | Zhang, Rao, Agrawala, *Adding Conditional Control to Text-to-Image Diffusion Models*, ICCV 2023 | 待確認 | 2026-11-25 |
| S10 | 文字生成圖模型對職業提示詞有性別、膚色偏差 | Luccioni et al., *Stable Bias: Analyzing Societal Representations in Diffusion Models*, NeurIPS 2023 Datasets & Benchmarks | 待確認 | 2026-11-25 |
| S11 | ControlNet Canny 權重（講師示範用） | Hugging Face `lllyasviel/sd-controlnet-canny`（model card，授權 OpenRAIL） | 待確認 | 2026-11-26 |
| S12 | CLIP 3 維示意圖、餘弦示意圖的縮圖 `clip-headphones.jpg`、`clip-backpack.jpg`、`clip-mug.jpg` | L22 `materials/data/catalog/` 的 c0_2、c6_0、c7_0（SD1.5 生成的虛構商品照，creativeml-openrail-m，見 L22 S3），縮成 112 px | 已確認（來源與授權） | 2026-11-27 |
