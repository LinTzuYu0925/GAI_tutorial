# 05-ae-anomaly-detection 查證紀錄

**2026-11-23 製作時沒有上網核對；下列標「待確認」。**

| id | 主張 | 來源 | 狀態 | 日期 |
|---|---|---|---|---|
| S1 | VisA 資料集（12 類，含 PCB1–4，像素級遮罩），下載網址 `https://amazon-visual-anomaly.s3.us-west-2.amazonaws.com/VisA_20220922.tar` | Zou et al., *SPot-the-Difference Self-Supervised Pre-training for Anomaly Detection and Segmentation* (ECCV 2022)；github.com/amazon-science/spot-diff | 待確認 | 2026-11-23 |
| S2 | `ConvTranspose2d(k=4, s=2, p=1)` 讓高寬加倍；`Conv2d(k=4, s=2, p=1)` 減半 | PyTorch 文件；本機煙霧測試已印出 shape | 已由煙霧測試確認 shape | 2026-11-23 |
| S3 | `roc_auc_score` | scikit-learn 文件 | 待確認 | 2026-11-23 |
| S4 | PatchCore：記憶庫＋最近鄰 | Roth et al., *Towards Total Recall in Industrial Anomaly Detection* (CVPR 2022) | 待確認 | 2026-11-23 |
| S5 | EfficientAD：學生－老師＋自編碼器，毫秒級 | Batzner et al., *EfficientAD* (WACV 2024) | 待確認 | 2026-11-23 |
| S6 | VisA 授權 CC BY 4.0 | spot-diff 倉庫 LICENSE | 待確認 | 2026-11-23 |
| S7 | MVTec AD 授權 CC BY-NC-SA 4.0 | MVTec 官網 | 待確認 | 2026-11-23 |
| S8 | DeepPCB 授權標示不一致 | roadmap §9.2 記錄（徽章 MIT，README 寫研究用途） | 待確認 | 2026-11-23 |
