# 13-conditional-diffusion-cfg 查證紀錄

依 `technical-research-fact-checking`：只列實際讀過的來源；論文結果標明出處；無法查證者標「待確認」。

| id | 主張 | 來源（標題、URL、章節／頁） | 狀態 | 日期 |
|---|---|---|---|---|
| S1 | Classifier guidance：用另外訓練的分類器梯度 ∇log p(y｜x_t) 引導取樣 | Dhariwal & Nichol, *Diffusion Models Beat GANs on Image Synthesis*, NeurIPS 2021, §4 | 待確認（未逐字核對） | 2026-11-25 |
| S2 | Classifier-free guidance：同一個模型以機率 p_uncond 丟掉條件來訓練；取樣時 ε̃ ＝ (1＋w)ε(z,c) − w·ε(z)。本課寫成 ε_uncond ＋ w·(ε_cond − ε_uncond)，本課的 w 等於論文的 1＋w（diffusers 的 `guidance_scale` 也採本課寫法） | Ho & Salimans, *Classifier-Free Diffusion Guidance*, 2022, arXiv:2207.12598, §3 | 待確認（未逐字核對） | 2026-11-25 |
| S3 | DDPM 排程 T＝1000、β 從 1e-4 線性到 0.02；預測雜訊的 MSE 損失 | Ho, Jain, Abbeel, *Denoising Diffusion Probabilistic Models*, NeurIPS 2020, §4 | 待確認（與 D3-3 共用） | 2026-11-25 |
| S4 | FID：兩組 Inception 特徵各擬合高斯，算 Fréchet 距離 ‖μ₁−μ₂‖² ＋ Tr(Σ₁＋Σ₂−2(Σ₁Σ₂)^½) | Heusel et al., *GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium*, NeurIPS 2017 | 待確認 | 2026-11-25 |
| S5 | KID：特徵上的 MMD（三次多項式核），無偏估計，小樣本較穩 | Bińkowski et al., *Demystifying MMD GANs*, ICLR 2018 | 待確認 | 2026-11-25 |
| S6 | Fashion-MNIST：10 類、60 000 訓練＋10 000 測試、28 × 28 灰階，MIT 授權 | Xiao, Rasul, Vollgraf, 2017；github.com/zalandoresearch/fashion-mnist | 待確認 | 2026-11-25 |
| S7 | 合成資料可能放大偏差、要用真實資料驗收 | 一般原則；本課以 lab 延伸題示範 | 推論（不引用數字） | 2026-11-25 |
