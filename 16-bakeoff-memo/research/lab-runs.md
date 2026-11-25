# 16-bakeoff-memo 實跑紀錄

投影片上的數字、圖片、VRAM 和時間都要來自這裡記錄的執行。

## 本機 CPU 煙霧測試（2026-11-25，不是 T4 實跑；數字不上投影片）

- 環境：torch 2.15.0+cpu、Python 3.12；只跑第 1 格、CycleGAN、flow 玩具、比較表（SD 部分不在本機跑：SD1.5 權重未在本機快取）。原圖用 `10-cyclegan-line-b/public/horse.jpg` 代替。
- **發現並修正**：官方 `summer2winter_yosemite.pth`（2018）多存了 InstanceNorm 的 `running_mean`／`running_var`／`num_batches_tracked`，`load_state_dict` 會報錯 → 載入前刪掉這些鍵（官方程式也這樣做）。之後嚴格載入成功；生成器參數 11.4M。
- CycleGAN 512 × 512：CPU 約 1.93 秒／張（暖機後 10 次平均）。
- flow 玩具 3000 步：4 秒，最後 loss 1.404。**觀察**：20 步的軌跡明顯彎曲；1 步全部塌在原點附近；2 步呈一團；10 步大致沿著兩個月亮但散。→ 原本標題「幾乎是直線」不正確，改成預測練習（第 16 頁）。
- 發現：Colab 與本機都沒有中文字型，圖上中文變方框 → labs 13–16 第 1 格加入 Noto CJK 安裝（同 lab02）。

## Colab T4 實跑

- [ ] 尚未執行。要記錄：版本、三種方法秒／張與 VRAM、`bakeoff.png`、`bakeoff_seeds.png`、`flow_toy.png`。
