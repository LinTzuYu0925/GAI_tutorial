# 11-ddpm-from-scratch 查證紀錄

依 `technical-research-fact-checking`：只列實際讀過的來源；無法查證者標「待確認」。

| id | 主張 | 來源 | 狀態 | 日期 |
|---|---|---|---|---|
| S1 | T＝1000；β 從 10⁻⁴ 線性增加到 0.02；q(x_t｜x₀) 的一行式（式 4）；ε_θ 預測 ε；L_simple（式 14）是變分下界的簡化版；§3.2：ε 預測的式子和去噪分數匹配（denoising score matching）、Langevin 動力學相似；Algorithm 2 取樣，σ_t²＝β_t；U-Net＋Transformer sinusoidal 時間嵌入；CIFAR-10 FID 3.17 | Ho, Jain, Abbeel, *Denoising Diffusion Probabilistic Models*, NeurIPS 2020, arXiv:2006.11239 §2、§3.2、§3.4、§4 | 已確認（arXiv HTML 逐字） | 2026-11-25 |
| S2 | DDIM 用同一個訓練好的模型，不需重新訓練；η＝0 為確定性；牆鐘時間快 10×～50× | Song, Meng, Ermon, *Denoising Diffusion Implicit Models*, ICLR 2021, arXiv:2010.02502 摘要、§4.1、§5 | 已確認（arXiv HTML 逐字） | 2026-11-25 |
| S3 | 生成三難：高品質、mode coverage／多樣性、快速取樣；GAN 快但 mode coverage 差；擴散取樣要數千次網路運算 | Xiao, Kreis, Vahdat, *Tackling the Generative Learning Trilemma with Denoising Diffusion GANs*, ICLR 2022, arXiv:2112.07804 摘要、§1 | 已確認（arXiv HTML 逐字） | 2026-11-25 |
| S4 | google/ddpm-cifar10-32：DDPMPipeline、Apache-2.0、不需同意條款 | Hugging Face 模型頁與 API（license: apache-2.0，gated: false） | 已確認 | 2026-11-25 |
| S5 | 線性排程太快破壞資訊、後段幾乎是雜訊 → cosine 排程 | Nichol & Dhariwal, *Improved Denoising Diffusion Probabilistic Models*, ICML 2021, arXiv:2102.09672 §3.2 | 已確認（arXiv HTML 逐字） | 2026-11-25 |
| S6 | `DDIMScheduler(num_train_timesteps, beta_start, beta_end, beta_schedule="linear")`、`set_timesteps`、`step(...).prev_sample` | diffusers 0.43.0（本機煙霧測試實際呼叫成功） | 已確認（程式可執行） | 2026-11-25 |
| S7 | Fashion-MNIST：60,000 訓練、10,000 測試、28 × 28 | torchvision `FashionMNIST`（本機載入計數） | 已確認 | 2026-11-25 |
| S11 | 去噪方塊示意圖（remove-one-noise.png：髒圖＋步數 → Noise Predicter → 減去 → 較乾淨圖） | 教學網站轉載（raw.githubusercontent.com/Emisaber/pic_obsidian，Pasted image 20240709152625.png）；授權未確認，僅課堂教學引用 | 待確認授權（講師指定使用） | 2026-11-26 |
| S12 | 倒序圖 lab11-forward_strip-reversed.png | 由 lab11-run-forward_strip.png 七格重新排列（講師 T4 實跑輸出） | 已確認 | 2026-11-26 |
