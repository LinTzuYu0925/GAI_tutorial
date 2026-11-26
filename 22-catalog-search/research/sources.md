# 22-catalog-search 查證紀錄

| id | 主張 | 來源 | 狀態 | 日期 |
|---|---|---|---|---|
| S1 | CLIP：對比學習、圖文相似度矩陣、零樣本分類與提示寫法的影響 | Radford et al., *Learning Transferable Visual Models From Natural Language Supervision*, 2021 | 待確認 | 2026-11-26 |
| S2 | 授權：`google/siglip2-base-patch16-224` apache-2.0、`Qwen/Qwen2-VL-2B-Instruct` apache-2.0（HF API 讀取）；`openai/clip-vit-base-patch32` 模型卡沒有 license 欄位；程式 MIT 依 openai/CLIP GitHub；模型卡的 Intended Use 據稱把部署用途列在範圍外（審查意見，待讀原文） | HF 模型卡；GitHub | SigLIP 2、Qwen2-VL 已確認；CLIP 待確認 | 2026-11-26 |
| S3 | 商品照的生成授權：SD1.5 creativeml-openrail-m、LCM-LoRA openrail++ | HF 模型卡（API 讀取） | 已確認 | 2026-11-26 |
| S4 | VLM：視覺編碼器把圖片變成 token，接在文字前面給語言模型 | Qwen2-VL 技術報告（Wang et al., 2024） | 待確認 | 2026-11-26 |
| S5 | 標籤正確率、precision@5、tokenizer 輸出、VLM 說明 | lab22 本機實跑（`research/lab-runs.md`） | 已實跑 | 2026-11-26 |
| S6 | jina-clip-v2 授權 CC BY-NC | 課程地圖 §9.2；HF 模型卡 | 待確認 | 2026-11-26 |
