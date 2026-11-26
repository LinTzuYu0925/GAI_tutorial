# 09-gan-upscaling 查證紀錄

依 `technical-research-fact-checking`：只列實際讀過的來源；論文結果標明出處；無法查證者標「待確認」。

| id | 主張 | 來源（標題、URL、章節／頁） | 狀態 | 日期 |
|---|---|---|---|---|
| S1 | 耳機照片 233 × 263，CC0 | Wikimedia Commons：File:Headphones_on_white_background.jpg（作者 Sprinno；Commons API extmetadata 授權欄位） | 已確認 | 2026-11-24 |
| S2 | Real-ESRGAN x4plus：4 倍放大；權重由 GitHub release v0.1.0 下載；程式授權 BSD-3-Clause | Wang et al., *Real-ESRGAN*, ICCVW 2021；github.com/xinntao/Real-ESRGAN（LICENSE）；`spandrel` 載入後印出 ESRGAN、scale 4（講師本機試跑） | 已確認（載入與倍數）；權重授權依 repo BSD-3 | 2026-11-24 |
| S3 | GAN 的 minimax 目標；G 改用 non-saturating 寫法（最大化 log D(G(z))）以免早期梯度太小 | Goodfellow et al., *Generative Adversarial Nets*, NeurIPS 2014, §3 | 待確認（未逐字核對） | 2026-11-24 |
| S4 | DCGAN 架構規則：stride 卷積取代 pooling、BatchNorm、G 用 ReLU＋最後 tanh、D 用 LeakyReLU；Adam lr 2e-4、β1 0.5 | Radford et al., arXiv 1511.06434, §3–4 | 待確認（未逐字核對） | 2026-11-24 |
| S5 | 對抗損失仍用在 Real-ESRGAN、SD 的 VAE 解碼器、HiFi-GAN、EnCodec、ADD（SDXL-Turbo） | Wang 2021；Rombach 2022；Kong 2020；Défossez 2022；Sauer 2023 | 待確認 | 2026-11-24 |
| S6 | WGAN、WGAN-GP | Arjovsky et al. 2017；Gulrajani et al. 2017 | 待確認 | 2026-11-24 |
| S7 | 生成三難（品質、多樣性、速度） | Xiao et al., *Tackling the Generative Learning Trilemma*, ICLR 2022 | 待確認 | 2026-11-24 |
| S8 | 不實廣告的法規 | 消費者保護法、公平交易法（全國法規資料庫） | 待確認（條號） | 2026-11-24 |
| S9 | Fashion-MNIST，MIT 授權 | github.com/zalandoresearch/fashion-mnist | 待確認 | 2026-11-24 |
| S10 | spandrel：MIT 授權，支援 ESRGAN 權重 | github.com/chaiNNer-org/spandrel | 待確認（授權）；載入已實測 | 2026-11-24 |
| S11 | GAN 概念圖的標準畫法（z → G → 假圖；真圖與假圖進 D；回饋給兩邊） | Google ML「Overview of GAN Structure」；CMU 11-785 GAN 講義（2026-11-26 搜尋，未逐頁核對） | 已確認圖型；gan-noise-z.png、gan-fake-early-sketch.png 為 PIL 示意圖（非模型輸出） | 2026-11-26 |
