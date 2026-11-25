# 14-stable-diffusion-studio 實跑紀錄

投影片上的數字、圖片、VRAM 和時間都要來自這裡記錄的執行。

## 本機檢查（2026-11-25）

- `python -X utf8 scripts/py2nb.py …/lab14-sd-studio.py`：學員版與解答版都建出來，解答版語法檢查通過。
- 依 /goal 指示，SD 筆記本不在本機 CPU 實跑；T4 實跑才是真正的測試。

## Colab T4 實跑

- [ ] 尚未執行。要記錄：版本、載入時間、每張圖時間、VRAM 峰值、U-Net 參數與 in_channels、CLIP 表、參數網格、img2img、換背景（產品區／背景區改變）、CLIP 分數 vs w、偏差稽核 12 張。
