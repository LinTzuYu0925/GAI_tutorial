# 05-ae-anomaly-detection 查證紀錄

**2026-11-23 製作時沒有上網核對；2026-11-24 已核對 S1、S6（spot-diff README 與下載檔），其餘仍待確認。**

| id | 主張 | 來源 | 狀態 | 日期 |
|---|---|---|---|---|
| S1 | VisA 資料集（12 類），下載網址 `https://amazon-visual-anomaly.s3.us-west-2.amazonaws.com/VisA_20220922.tar`（1,929,840,640 bytes）；解壓後 `pcb1/Data/Images/{Normal,Anomaly}`、`pcb1/Data/Masks/Anomaly`；PCB1 良品 1004、不良品 100（bent 14＋、melt 46＋、missing 17、scratch 14＋，部分多標籤） | Zou et al., ECCV 2022；github.com/amazon-science/spot-diff README；講師下載後計數 | 已確認 | 2026-11-24 |
| S2 | `ConvTranspose2d(k=4, s=2, p=1)` 讓高寬加倍；`Conv2d(k=4, s=2, p=1)` 減半 | PyTorch 文件；本機煙霧測試已印出 shape | 已由煙霧測試確認 shape | 2026-11-23 |
| S3 | `roc_auc_score` | scikit-learn 文件 | 待確認 | 2026-11-23 |
| S4 | PatchCore：記憶庫＋最近鄰 | Roth et al., *Towards Total Recall in Industrial Anomaly Detection* (CVPR 2022) | 待確認 | 2026-11-23 |
| S5 | EfficientAD：學生－老師＋自編碼器，毫秒級 | Batzner et al., *EfficientAD* (WACV 2024) | 待確認 | 2026-11-23 |
| S6 | VisA 授權 CC BY 4.0 | spot-diff README："The data is released under the CC BY 4.0 license." | 已確認 | 2026-11-24 |
| S7 | MVTec AD 授權 CC BY-NC-SA 4.0 | MVTec 官網 | 待確認 | 2026-11-23 |
| S8 | DeepPCB 授權標示不一致 | roadmap §9.2 記錄（徽章 MIT，README 寫研究用途） | 待確認 | 2026-11-23 |

| S9 | anomalib 內建 PatchCore、EfficientAD 與 VisA 載入 | github.com/open-edge-platform/anomalib 文件 | 待確認 | 2026-11-24 |
