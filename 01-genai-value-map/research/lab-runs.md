# 01-genai-value-map Lab 實跑紀錄

每本筆記本在 Colab 從頭跑完後記一列。投影片上的數字、圖片、VRAM 與時間只能引用這裡有紀錄的實跑。

| 日期 | 筆記本 | GPU | torch | 其他套件版本 | VRAM 峰值 | 總時間 | seed | 結果／備註 |
|---|---|---|---|---|---|---|---|---|
| 2026-11-24 | 02-genai-tour `lab02-genai-tour-solution.ipynb` ＋ MusicGen 一格（講師導覽，第 6 頁） | Colab T4 | 待補 | Python 3.13；torchao 0.10.0（diffusers 停用）；其餘待補 | 待補 | 文案格 49 秒（含下載）；產品圖 4 步約 3 秒（1.84 it/s） | 圖 42（待確認）；音樂待補 | 文案三版 162／158／165 字，皆超過 80 字；第 1 版「續航 30 小時」與「2 小時」矛盾；第 2、3 版混入簡體字。圖 → `public/tour-product-seed42.png`（從 Colab 截圖裁切，410×391，底部約 19 px 被視窗切掉）。音樂 → `public/tour-jingle.wav`（9.94 秒，32 kHz 單聲道）。原始截圖在 `shots/`。 |
