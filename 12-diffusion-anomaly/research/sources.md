# 12-diffusion-anomaly 查證紀錄

依 `technical-research-fact-checking`：只列實際讀過的來源；無法查證者標「待確認」。

| id | 主張 | 來源 | 狀態 | 日期 |
|---|---|---|---|---|
| S1 | 部分擴散（partial diffusion）：只加噪到某個中間步數 λ，再用 DDPM 去噪，和原圖逐像素比較平方誤差；不需要完整長度的馬可夫鏈；高斯雜訊抓不到較大的異常 → 改用 simplex 雜訊 | Wyatt, Leach, Schmon, Willcocks, *AnoDDPM: Anomaly Detection with Denoising Diffusion Probabilistic Models using Simplex Noise*, CVPR Workshops (NTIRE) 2022, pp. 650–656；作者專案頁 julianwyatt.co.uk/anoddpm 與 GitHub Julian-Wyatt/AnoDDPM README | 已確認（摘要與 README；全文 PDF 403 未讀） | 2026-11-25 |
| S2 | DDIM：同一個模型、不需重新訓練；η＝0 為確定性 | Song et al., ICLR 2021, arXiv:2010.02502 §4.1、§5 | 已確認（arXiv HTML 逐字，見 11 的 S2） | 2026-11-25 |
| S3 | DDPM 一行加噪與預測雜訊 | Ho et al., NeurIPS 2020 §2、§3.2（見 11 的 S1） | 已確認 | 2026-11-25 |
| S4 | VisA PCB1，CC BY 4.0；1004 良品、100 不良品附遮罩 | amazon-science/spot-diff README；講師本機計數（D2-1 已確認） | 已確認 | 2026-11-24 |
| S5 | DDAD：以目標影像為條件的去噪重建，逐像素與特徵比較定位異常；論文報告 VisA 影像層級 AUROC 98.9% | Mousakhan et al., *Anomaly Detection with Conditioned Denoising Diffusion Models*, arXiv:2305.15956 摘要 | 已確認（摘要） | 2026-11-25 |
| S6 | 詐欺犯罪危害防制條例第 31 條第 1 項第 4 款：網路廣告平臺業者刊登或推播廣告時，應揭露「廣告使用深度偽造技術或人工智慧生成之個人影像」；同條第 4 項定義深度偽造；第 40 條第 1 項第 4 款罰鍰 20 萬～500 萬元；第 27 條：適用於達一定規模的平臺業者 | 全國法規資料庫 pcode=D0080226（113 年 7 月 31 日制定；頁面修正日期 115 年 1 月 21 日） | 已確認（條文）；公布日期待確認 | 2026-11-25 |
| S7 | PatchCore、EfficientAD 是工業異常偵測常用的基準 | Roth et al., CVPR 2022；Batzner et al., WACV 2024 | 待確認（未讀原文；D2-1 已點名） | 2026-11-25 |
