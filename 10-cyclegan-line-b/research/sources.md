# 10-cyclegan-line-b 查證紀錄

依 `technical-research-fact-checking`：只列實際讀過的來源；無法查證者標「待確認」。

| id | 主張 | 來源 | 狀態 | 日期 |
|---|---|---|---|---|
| S1 | VisA PCB1，CC BY 4.0；1004 良品、100 不良品附遮罩 | amazon-science/spot-diff README；講師本機計數（D2-1 已確認） | 已確認 | 2026-11-24 |
| S2 | pix2pix 需要成對資料；PatchGAN 鑑別器 | Isola et al., *Image-to-Image Translation with Conditional Adversarial Networks*, CVPR 2017, §3.2 | 待確認（未逐字核對） | 2026-11-24 |
| S3 | CycleGAN：兩個 G、兩個 D；循環一致 λ＝10；identity 損失保留顏色；LSGAN | Zhu et al., *Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial Networks*, ICCV 2017 | 待確認（未逐字核對） | 2026-11-24 |
| S4 | lab 的 identity 權重 5（＝0.5 × λ_cyc）沿用官方實作預設 | junyanz/pytorch-CycleGAN-and-pix2pix 的 `lambda_identity 0.5` | 待確認 | 2026-11-24 |
| S7 | 馬的照片，CC0 | Chad Madden，Wikimedia Commons：File:Gray_horse_on_green_and_yellow_meadow_(Unsplash).jpg | 已確認（Commons API 授權欄位） | 2026-11-24 |
| S8 | 斑馬的照片，CC0 | Agness Abubakar Saidi，Wikimedia Commons：File:Zebras_grazing_among_acacia_trees,_Serengeti_National_Park.jpg | 已確認（Commons API 授權欄位） | 2026-11-24 |
| S9 | CycleGAN 可能把資訊藏在細微雜訊裡（steganography） | Chu, Zhmoginov, Sandler, *CycleGAN, a Master of Steganography*, 2017 | 待確認 | 2026-11-24 |
| S10 | CyCADA | Hoffman et al., ICML 2018 | 待確認 | 2026-11-24 |
