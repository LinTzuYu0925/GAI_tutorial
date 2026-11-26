# 05-ae-anomaly-detection Lab 實跑紀錄

每本筆記本在 Colab 從頭跑完後記一列。投影片上的數字、圖片、VRAM 與時間只能引用這裡有紀錄的實跑。

| 日期 | 筆記本 | GPU | torch | 其他套件版本 | VRAM 峰值 | 總時間 | seed | 結果／備註 |
|---|---|---|---|---|---|---|---|---|
| 2026-11-23 | lab05-ae-anomaly-solution（煙霧測試） | 無（本機 CPU） | 2.15.0+cpu | torchvision 0.29.2、scikit-learn | — | 約 1 分 | 0 | **不是 T4 實跑、不是 VisA**。合成 PCB 圖（60 良品、20 不良）；z shape (8,128,8,8)，壓縮 1/6；全部步驟可執行；`inspect` 回傳 (128,128,3) 熱力圖與判定。數字不可用於投影片。修正：門檻改為依排序計數 |
| 2026-11-24 | 資料檢查（非筆記本） | — | — | PIL、numpy | — | — | — | 真實 VisA PCB1 下載確認。拍攝方向：良品 790／1004（約 79%）針腳朝上、不良品 5／100 針腳朝上；以針腳區域紋理判斷，目視抽查 16 張一致。→ lab05 訓練集加入 180° 旋轉。投影片圖片（`public/pcb1-*.jpg`）由講師本機從原圖裁切 |
| 2026-11-26 紀錄（輸出存於 `materials/lab05-ae-anomaly-solution.ipynb`） | lab05-ae-anomaly-solution | Colab Tesla T4（可用 15.3／15.6 GB） | 2.14.1+cu130 | python 3.13.16、scikit-learn | 未印出 | 讀圖 19 秒；訓練 30 epochs 約 30 秒 | 0 | **講師 T4 實跑**。切分 train 良品 702／val 151 良＋50 不良／test 151 良＋50 不良；加 180° 旋轉後訓練良品 1404。z (8,128,8,8)。loss 0.01614 → 0.00082。驗證集平均分數 良品 0.01723、不良 0.02368。AUROC val 0.855、test 0.908；門檻 0.01654；val 過殺 44.4%／漏檢 4.0%，test 過殺 36.4%／漏檢 2.0%。投影片用圖：`public/lab05-recon.png`（重建網格前 4 張重排成一列）、`lab05-heatmaps.png`（熱力圖格原圖）、`lab05-hist.png`（直方圖）；L06 `public/lab05-bent-error.png` 為熱力圖第 2 張的誤差圖裁切 |
