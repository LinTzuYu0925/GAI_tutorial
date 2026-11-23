# 07-vae-latent-space 查證紀錄

| id | 主張 | 來源 | 狀態 | 日期 |
|---|---|---|---|---|
| S1 | 台北街景照片 CC0 | lumoplank，經 Wikimedia Commons：https://commons.wikimedia.org/wiki/File:Night_markets_of_Taipei_-_TaipeiNM4948.jpg | 已確認（Commons API 授權欄位） | 2026-11-24 |
| S2 | SD1.5 VAE：3×512×512 → 4×64×64 | `stable-diffusion-v1-5/stable-diffusion-v1-5` 的 `vae` 子資料夾；講師本機 CPU 試跑印出 shape | 已確認（shape） | 2026-11-24 |
| S3 | VAE、重參數化 | Kingma & Welling, *Auto-Encoding Variational Bayes*, arXiv 1312.6114 | 待確認 | 2026-11-24 |
| S4 | 潛在擴散；SD 的 VAE 用對抗＋感知損失 | Rombach et al., arXiv 2112.10752 | 待確認 | 2026-11-24 |
| S5 | β-VAE | Higgins et al., ICLR 2017 | 待確認 | 2026-11-24 |
| S6 | 擴散模型可重現訓練圖片 | Carlini et al., arXiv 2301.13188 | 待確認 | 2026-11-24 |
| S7 | Fashion-MNIST 授權 MIT | github.com/zalandoresearch/fashion-mnist LICENSE | 已確認 | 2026-11-24 |
