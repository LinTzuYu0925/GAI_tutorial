# 07-vae-latent-space Lab 實跑紀錄

每本筆記本在 Colab 從頭跑完後記一列。投影片上的數字、圖片、VRAM 與時間只能引用這裡有紀錄的實跑。

| 日期 | 筆記本 | GPU | torch | 其他套件版本 | VRAM 峰值 | 總時間 | seed | 結果／備註 |
|---|---|---|---|---|---|---|---|---|
| 2026-11-24 | lab07-vae-solution（煙霧測試） | 無（本機 CPU） | 2.15.0+cpu | diffusers（最新版）、torchvision | — | 107 秒（EPOCHS 3） | 0 | **不是 T4 實跑，不可放投影片**。AE 座標 z1 −14.7～5.8、z2 −8.0～4.4；VAE z1 −2.9～2.4、z2 −3.5～3.1。SD VAE：(1,3,512,512)→(1,4,64,64)，48 倍；fp32 CPU PSNR 20.6 dB、13.5 秒；招牌小字明顯變形。修正 legend 呼叫錯誤 |
| 2026-11-26 | lab07-vae-solution | Colab T4 | 2.14.1+cu130 | Python 3.13.16 | SD VAE 段 0.86 GB | — | 0 | 講師 T4 實跑（解答筆記本存有輸出）。SD VAE：PSNR 20.6 dB、編碼＋解碼 0.36 秒；新增格：潛在 4 通道數值 ch0 −15.6～18.0、ch1 −17.2～16.4、ch2 −16.4～12.9、ch3 −12.8～13.3（`public/lab07-sd-latent-channels.png`）。投影片的 lab07 圖都取自此次輸出 |
