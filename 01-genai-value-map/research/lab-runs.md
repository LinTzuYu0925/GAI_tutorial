# 01-genai-value-map Lab 實跑紀錄

每本筆記本在 Colab 從頭跑完後記一列。投影片上的數字、圖片、VRAM 與時間只能引用這裡有紀錄的實跑。

| 日期 | 筆記本 | GPU | torch | 其他套件版本 | VRAM 峰值 | 總時間 | seed | 結果／備註 |
|---|---|---|---|---|---|---|---|---|
| 2026-11-24 | 02-genai-tour `lab02-genai-tour-solution.ipynb` ＋ MusicGen 一格（講師導覽，第 6 頁） | Colab T4 | 待補 | Python 3.13；torchao 0.10.0（diffusers 停用）；其餘待補 | 待補 | 文案格 49 秒（含下載）；產品圖 4 步約 3 秒（1.84 it/s） | 圖 42（2026-11-26 用同一本解答筆記本 seed 42 重跑，構圖相同，見 02 deck lab-runs）；音樂未記錄 seed | 文案三版 162／158／165 字，皆超過 80 字；第 1 版「續航 30 小時」與「2 小時」矛盾；第 2、3 版混入簡體字。圖 → `public/tour-product-seed42.png`（從 Colab 截圖裁切，410×391，底部約 19 px 被視窗切掉）。音樂 → `public/tour-jingle.wav`（9.94 秒，32 kHz 單聲道）。原始截圖在 `shots/`。 |
| 2026-11-26 | MusicGen 一格整理成 `materials/tour-musicgen.py`（可重現版本，torch.manual_seed(0)、max_new_tokens=500） | — | — | — | — | — | 0 | 2026-11-26 講師本機 CPU（ml-helper，transformers 5.x）把 `.to("cuda")` 換成自動選裝置後跑完：99 秒，輸出 9.94 秒、32 kHz，與 `public/tour-jingle.wav` 長度、取樣率相同；T4 尚未跑（T4 上不需改裝置）。`public/tour-jingle.wav` 仍是 2026-11-24 那次，重跑的旋律不會完全相同 |
| 2026-11-26 | 第 6 頁產品圖換成 02 deck 2026-11-26 T4 實跑的完整 512×512 圖（`02-genai-tour/public/lab02-run-product_seed42.png`，seed 42，同 seed 像素差 0）；文案與音樂仍是 2026-11-24 那次 | Tesla T4 | 2.14.1+cu130 | transformers 5.24.1；diffusers 0.43.0 | 4.56 GB（文字＋影像，不含 MusicGen） | — | 42 | 取代原本底部被裁掉的截圖；本次未計時，投影片「T4 約 3 秒」來自 2026-11-24 那次（1.84 it/s） |
