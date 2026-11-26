# 04-colab-hub-gradio Lab 實跑紀錄

每本筆記本在 Colab 從頭跑完後記一列。投影片上的數字、圖片、VRAM 與時間只能引用這裡有紀錄的實跑。

| 日期 | 筆記本 | GPU | torch | 其他套件版本 | VRAM 峰值 | 總時間 | seed | 結果／備註 |
|---|---|---|---|---|---|---|---|---|
| 2026-11-23 | lab04-checkpoint-gradio-solution（煙霧測試） | 無（本機 CPU） | 2.15.0+cpu | torchvision 0.29.2 | — | — | 0 | **不是 T4 實跑**。CIFAR-10 以 FakeData（256 張）代替；續訓流程正確（第二次從 epoch 3 開始）；`predict` 接受灰階 800×600 圖。Part B、Gradio 未測。數字不可用於投影片 |
| 2026-11-26 | lab04-checkpoint-gradio-solution（講師在 Colab 實跑，輸出存在 solution.ipynb） | Tesla T4（可用 VRAM 14.9 / 15.6 GB） | 2.14.1+cu130 | python 3.13.16；transformers、gradio 為當時 `pip -U` 版本 | fp16 峰值 1.19 GB | — | 0 | Part A 只跑到 STOP_AFTER=2（epoch 1 acc 0.528、epoch 2 acc 0.611），續訓那次的輸出未存。Part B（Qwen2.5-0.5B-Instruct，494M 參數）：fp32 估算 1.98 GB／實測峰值 2.17 GB；fp16 估算 0.99 GB／實測峰值 1.19 GB。網格格（2 epoch 模型）：16 張對 13 張 → 投影片「matplotlib 網格」`public/lab04-pred-grid.png`。Gradio 介面截圖 → 「Lab 1／6」`public/lab04-gradio-ui.png`（講師截圖，未上傳圖片狀態） |
