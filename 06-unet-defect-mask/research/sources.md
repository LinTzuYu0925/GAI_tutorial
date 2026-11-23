# 06-unet-defect-mask 查證紀錄

| id | 主張 | 來源 | 狀態 | 日期 |
|---|---|---|---|---|
| S1 | VisA 資料集：PCB1 良品 1004 張、不良品 100 張（bent／melt／missing／scratch），遮罩在 `pcb1/Data/Masks/Anomaly`；授權 CC BY 4.0；下載網址 `https://amazon-visual-anomaly.s3.us-west-2.amazonaws.com/VisA_20220922.tar`（約 1.9 GB） | github.com/amazon-science/spot-diff README（"The data is released under the CC BY 4.0 license."）；張數與結構由講師下載後計數 | 已確認 | 2026-11-24 |
| S2 | U-Net：編碼－解碼＋跳接（concatenate），用於生醫影像切割 | Ronneberger et al., *U-Net*, MICCAI 2015, arXiv 1505.04597 | 待確認 | 2026-11-24 |
| S3 | ResNet 的跳接是相加 | He et al., *Deep Residual Learning*, CVPR 2016 | 待確認 | 2026-11-24 |
| S4 | DRAEM：Perlin 雜訊遮罩＋DTD 紋理合成瑕疵；重建網路＋判別網路 | Zavrtanik et al., *DRAEM*, ICCV 2021, arXiv 2108.07610 | 待確認 | 2026-11-24 |
| S5 | HC-SR04 模組板子約 45 × 20 mm | 常見模組規格書；講師量測原圖板子 946 × 418 像素（長寬比 2.26，與 2.25 相符） | 待確認（尺寸）；量測已完成 | 2026-11-24 |
| S6 | ConvTranspose 的棋盤格假影 | Odena et al., *Deconvolution and Checkerboard Artifacts*, Distill 2016 | 待確認 | 2026-11-24 |
