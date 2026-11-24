# 09-gan-upscaling 實跑紀錄

投影片上的數字、圖片、VRAM 和時間都要來自這裡記錄的執行。

## 本機 CPU 煙霧測試（2026-11-24，不是 T4 實跑）

- 環境：torch 2.15.0+cpu、Python 3.14、spandrel；`EPOCHS=2`；用講師的 runlab 腳本（去掉 `%pip`）。
- Part A：原圖 (233, 263)；spandrel 載入「ESRGAN，放大倍數 4」；`(1, 3, 263, 233) → (1, 3, 1052, 932)`，CPU 12.24 秒。
- Part B：`z (16, 100) → fc 後 (16, 128, 7, 7) → 輸出 (16, 1, 28, 28)`；D 的輸出 `(16,)`。
- 訓練：epoch 1 loss_D 0.202、loss_G 2.849（81 秒）；epoch 2 loss_D 0.154、loss_G 3.577（163 秒）。
- Part C：真實 32 張兩兩平均距離 22.90；epoch 1 生成 21.96；epoch 2 生成 22.36。
- 發現並修正：`EPOCHS=2` 時網格會重複畫 epoch 1（`show` 改成去重複）；放大圖的裁切框原本落在白底上，改成 (150, 480, 450, 780)（左耳罩）。

**投影片使用的輸出**：第 5 頁 `public/headphones-esrgan-crop.png`（Real-ESRGAN 4 倍輸出的同一塊裁切）。模型權重固定、推論沒有隨機性；下方 T4 實跑的對照圖（`public/lab09-run-esrgan-compare.png`）與這張裁切看起來一致（目視比對）。`public/headphones-bicubic-crop.png` 是 PIL 的 bicubic（固定公式）。

## Colab T4 實跑

| 日期 | 筆記本 | 環境 | torch | 版本與資料 | VRAM 峰值 | 時間 | 種子 | 備註 |
|---|---|---|---|---|---|---|---|---|
| 2026-11-24 | `lab09-dcgan-esrgan-solution.ipynb`（從 `src/lab09-dcgan-esrgan.py` 重建前的版本，見備註） | Colab T4（Tesla T4，15.5/15.6 GB 可用） | 2.14.1+cu130 | Python 3.13.16；spandrel 最新版（版本號未記）；Fashion-MNIST 經 torchvision 下載 | A：Real-ESRGAN 0.57 GB（第 1 次）、0.62 GB（第 2 次，重跑同一格） | A：第 1 次 2.46 秒（含冷啟動）、第 2 次 0.59 秒；(1,3,263,233)→(1,3,1052,932)。B：20 epoch 共 349 秒（約 17–18 秒／epoch）；loss_D／loss_G 第 20 epoch 為 0.594／2.436 | SEED=0 | **照片**：Wikimedia 對 Colab 回 HTTP 429（Too many requests），`fetch` 下載失敗；改手動上傳 `public/headphones-lowres.jpg`（233×263）為 `headphones.jpg` 後才通過。權重從 GitHub Release 下載成功。**C**：真實 32 張兩兩平均距離 22.90；生成 epoch 1／5／10／20 為 20.97／21.93／21.67／22.08，無 mode collapse 跡象。**備註**：上傳的 `.ipynb` 是舊版，ESRGAN 對照圖的裁切框為 (300,350,600,650)（落在白底），已在 Colab 內取代為 `.py` 的 (150,480,450,780) 後只重跑該格（0.59 秒那次）；其他格未用新框重跑。尚未以重建後的 notebook 從頭完整重跑。圖：`public/lab09-run-esrgan-compare.png`、`lab09-run-loss.png`、`lab09-run-dcgan-grids.png`（Colab 截圖裁切，非 notebook 存檔 PNG；解析度為螢幕解析度）。 |


## 實跑後的修改（2026-11-24）

- `fetch()` 改成：照片網址換成 `upload.wikimedia.org` 直連（本機 curl 回 200；**Colab 上尚未測**），失敗重試 3 次，再失敗就提示學員手動上傳 `headphones.jpg`。
- 網格的 epoch 清單去重複（`EPOCHS=2` 時不再畫兩次 epoch 1）。
- [ ] 用重建後的筆記本在 Colab T4 從頭完整重跑一次（上面那次是舊版、只重跑對照圖那一格）。

## 崩塌參考（2026-11-24，本機 CPU；第 15 頁）

- 用 lab09 的 `mean_pairwise`、同樣的正規化（−1～1），在 Fashion-MNIST 訓練集上計算：隨機前 32 張 22.90（與 T4 的參考值相同）；只取短靴（類別 9）前 32 張 19.90。圖：`public/collapse-reference.png`。
- 嘗試做出真的崩塌：`LR_G=5e-3`、EPOCHS＝3（CPU，每個 epoch 約 75 秒）：epoch 1／3 距離 21.91／23.97，網格仍有多種衣物 → **沒有崩塌**。所以第 15 頁用「只有短靴」當模擬，並標明。
