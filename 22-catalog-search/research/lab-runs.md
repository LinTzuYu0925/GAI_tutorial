# 22-catalog-search 實跑紀錄

## 商品照生成（2026-11-26，講師本機 CPU）

- `materials/src/make_catalog.py`：SD1.5（`stable-diffusion-v1-5/stable-diffusion-v1-5`）＋LCM-LoRA，4 步、guidance 1.0、512 px → 縮成 320 px。
- 共 40 張，每張約 30–35 秒，seed＝100 × 類別＋變化編號。
- 原本要用 Wikimedia Commons，但 API 回 HTTP 429（重試到 960 秒仍被擋），所以改用生成。

## lab22 講師本機 CPU 實跑（2026-11-26）

- **環境**：Windows、Python 3.12.16、torch 2.15.0+cpu、transformers 5.24.0；設定 `LAB_NO_LAUNCH=1`。
- **tokenizer**：
  - CLIP 把「一副耳機」切成 11 個位元組碎片；
  - SigLIP 2 切成「一副、耳、機」。
- **向量形狀**：CLIP (40, 512)、SigLIP 2 (40, 768)。
- **零樣本標籤**：

  | 模型 | 正確率 | 錯誤 |
  |---|---|---|
  | CLIP | 22% | 耳機大多被標成行動電源 |
  | SigLIP 2 | 82% | 掃地機器人有 3 張標錯 |

- **平均 precision@5**（8 個查詢）：CLIP 0.20、SigLIP 2 0.82。
  - 查詢「會自己打掃地板的機器人」：CLIP 0／5；SigLIP 2 3／5，錯的兩張是地毯上的背包和木地板上的筆電。
- **VLM**：Qwen2-VL-2B-Instruct，CPU 上只跑 2 張。
  - 耳機（14.6 秒）：「黑色頭戴式耳機，適用於各種音頻設備。」
  - 電熱水壺（9.4 秒）：「黑色電熱壺，適用於電熱壺底座，方便使用。」
  - 兩句都沒有簡體字。
- **輸出**：`public/catalog_grid.png`、`public/search_top5.png`。

## Colab T4 實跑

- [ ] 尚未執行（由講師執行）：VRAM、8 張 VLM 說明、Gradio 截圖。
- 重跑（審查後）：數字相同；新增大陸用語檢查抓到 1／2（音頻→音訊）；圖重畫（字 22–26 pt）。

## 2026-11-27 Gradio 截圖（講師）
- `public/lab22-gradio-ui.png`（原圖在 `shots/`）：中文搜尋框、範例、「前 5 名」圖片區；尚未送出搜尋。已換掉 Lab 7／7 的佔位圖。
