# 04-colab-hub-gradio Lab 實跑紀錄

每本筆記本在 Colab 從頭跑完後記一列。投影片上的數字、圖片、VRAM 與時間只能引用這裡有紀錄的實跑。

| 日期 | 筆記本 | GPU | torch | 其他套件版本 | VRAM 峰值 | 總時間 | seed | 結果／備註 |
|---|---|---|---|---|---|---|---|---|
| 2026-11-23 | lab04-checkpoint-gradio-solution（煙霧測試） | 無（本機 CPU） | 2.15.0+cpu | torchvision 0.29.2 | — | — | 0 | **不是 T4 實跑**。CIFAR-10 以 FakeData（256 張）代替；續訓流程正確（第二次從 epoch 3 開始）；`predict` 接受灰階 800×600 圖。Part B、Gradio 未測。數字不可用於投影片 |
