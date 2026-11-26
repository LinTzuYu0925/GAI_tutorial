# 06-unet-defect-mask 查證紀錄

| id | 主張 | 來源 | 狀態 | 日期 |
|---|---|---|---|---|
| S1 | VisA 資料集：PCB1 良品 1004 張、不良品 100 張（bent／melt／missing／scratch），遮罩在 `pcb1/Data/Masks/Anomaly`；授權 CC BY 4.0；下載網址 `https://amazon-visual-anomaly.s3.us-west-2.amazonaws.com/VisA_20220922.tar`（約 1.9 GB） | github.com/amazon-science/spot-diff README（"The data is released under the CC BY 4.0 license."）；張數與結構由講師下載後計數 | 已確認 | 2026-11-24 |
| S2 | U-Net：編碼－解碼＋跳接（concatenate），用於生醫影像切割 | Ronneberger et al., *U-Net*, MICCAI 2015, arXiv 1505.04597 | 待確認 | 2026-11-24 |
| S3 | ResNet 的跳接是相加 | He et al., *Deep Residual Learning*, CVPR 2016 | 待確認 | 2026-11-24 |
| S4 | DRAEM：Perlin 雜訊遮罩＋DTD 紋理合成瑕疵；重建網路＋判別網路；輸入與重建「接起來」送進判別網路；判別網路用 Focal loss | Zavrtanik et al., *DRAEM*, ICCV 2021, arXiv 2108.07610，Fig. 3 說明文字 | 架構與 Focal loss 已核對 Fig. 3 說明（2026-11-26）；重建損失 L2＋SSIM 待核對內文。**論文授權 CC BY-NC-SA 4.0（非商用）→ 投影片重繪，不放原圖** | 2026-11-26 |
| S5 | HC-SR04 模組板子約 45 × 20 mm | 常見模組規格書；講師量測原圖板子 946 × 418 像素（長寬比 2.26，與 2.25 相符） | 待確認（尺寸）；量測已完成 | 2026-11-24 |
| S6 | ConvTranspose 的棋盤格假影 | Odena et al., *Deconvolution and Checkerboard Artifacts*, Distill 2016 | 待確認 | 2026-11-24 |
| S7 | U-Net 架構圖（往下 max pool、往上 up sample、同層 concat） | Mehrdad Yazdani, *Example architecture of U-Net for producing k 256-by-256 image masks for a 256-by-256 RGB image*, Wikimedia Commons, CC BY-SA 4.0；`public/unet-commons.png` 為原圖 711×360，未修改 | 已確認（Commons 檔案頁） | 2026-11-26 |
