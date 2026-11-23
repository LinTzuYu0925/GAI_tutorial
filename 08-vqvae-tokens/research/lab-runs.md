# 08-vqvae-tokens Lab 實跑紀錄

每本筆記本在 Colab 從頭跑完後記一列。投影片上的數字、圖片、VRAM 與時間只能引用這裡有紀錄的實跑。

| 日期 | 筆記本 | GPU | torch | 其他套件版本 | VRAM 峰值 | 總時間 | seed | 結果／備註 |
|---|---|---|---|---|---|---|---|---|
| 2026-11-24 | lab08-vqvae-solution（煙霧測試） | 無（本機 CPU） | 2.15.0+cpu | transformers、torchaudio（CPU）、soundfile | — | 77 秒（EPOCHS 1） | 0 | **不是 T4 實跑；音訊是合成的 44.1 kHz 雙聲道正弦波**（Wikimedia 回傳 429）。EnCodec：1.5／3／6／12／24 kbps → 2／4／8／16／32 本 × 750 步，實際 kbps 與設定一致。SNR 在 24 kbps 仍約 1 dB → 改用頻譜誤差。Part B：K＝128 用到 69 格、K＝512 用到 62 格（1 epoch）。數字不可放投影片 |
