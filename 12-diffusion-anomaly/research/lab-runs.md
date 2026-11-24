# 12-diffusion-anomaly 實跑紀錄

投影片上的數字、圖片、VRAM 和時間都要來自這裡記錄的執行。

## 本機 CPU 煙霧測試（2026-11-25，不是 T4 實跑；數字不上投影片）

- 環境：torch 2.15.0+cpu、Python 3.14.9；VisA PCB1 本機副本；runlab（去掉 `%pip`）。
- 設定：EPOCHS_AE＝1、TRAIN_DDPM＝True、STEPS_DDPM＝30、EVAL_N＝8（每類 8 張）。全部格子可執行到存檔前一格。
- 切分：train 702 良品（加旋轉後 1404）、val 151／50、test 151／50，和 D2-1 相同。
- TinyUNet（3 通道）參數 1,982,563；CPU 每步約 1.3 秒（batch 32）。
- 時間（CPU）：DDIM 20 步每張約 326 ms；每步都走（t＝400）每張約 6,386 ms；AE 每張約 1.4–2.6 ms。
- 模型只訓練 30 步、每類 8 張：AUROC 數字無意義。
- 修正：`results.json` 在 Windows 預設 cp1252 寫入失敗 → 改 `encoding="utf-8"`（lab11 一併改）。STEPS_DDPM 由 6000 提高到 10000（T4 時間待實測）。

## Colab T4 實跑

- [ ] 尚未執行。檢查點還沒放上 GitHub，第一次執行會自動「自己訓練」並產生 `ddpm_pcb1_64.pt`。要記錄：下載時間、AE 與 DDPM 訓練時間、VRAM、t 掃描、步數表、測試對照表；圖片放 `public/`。
