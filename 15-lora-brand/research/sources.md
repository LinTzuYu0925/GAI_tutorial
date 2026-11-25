# 15-lora-brand 查證紀錄

依 `technical-research-fact-checking`：只列實際讀過的來源；論文結果標明出處；無法查證者標「待確認」。

| id | 主張 | 來源（標題、URL、章節／頁） | 狀態 | 日期 |
|---|---|---|---|---|
| S1 | DreamBooth 資料集 `backpack` 00–05 來自 Unsplash（@laurachouette），每張的網址列在 `references_and_licenses.txt` | github.com/google/dreambooth/blob/main/dataset/references_and_licenses.txt | 已確認（2026-11-25 讀取該檔） | 2026-11-25 |
| S2 | LoRA：W 凍結，ΔW ＝ B·A，A 為 r × d、B 為 d × r，B 初始化為 0；縮放 α／r | Hu et al., *LoRA: Low-Rank Adaptation of Large Language Models*, ICLR 2022, §4.1 | 待確認（未逐字核對） | 2026-11-25 |
| S3 | DreamBooth：罕見識別字＋類別詞；3–5 張照片；prior preservation 損失對抗語言漂移與過度擬合 | Ruiz et al., *DreamBooth: Fine Tuning Text-to-Image Diffusion Models for Subject-Driven Generation*, CVPR 2023 | 待確認 | 2026-11-25 |
| S4 | IP-Adapter：參考影像經 CLIP 影像編碼器，以解耦的交叉注意力接入 U-Net；`h94/IP-Adapter` 的 `ip-adapter_sd15.bin` | Ye et al., *IP-Adapter*, 2023；Hugging Face `h94/IP-Adapter` | 待確認 | 2026-11-25 |
| S5 | Textual inversion：只學一個新字的嵌入向量 | Gal et al., *An Image is Worth One Word*, ICLR 2023 | 待確認 | 2026-11-25 |
| S6 | Unsplash License：可免費商用，不可轉售未修改的照片、不可用來建立競爭服務 | unsplash.com/license | 待確認 | 2026-11-25 |
| S7 | 梯度檢查點：反向傳播時重算中間結果以節省記憶體 | Chen et al., *Training Deep Nets with Sublinear Memory Cost*, 2016；PyTorch `torch.utils.checkpoint` 文件 | 待確認 | 2026-11-25 |
