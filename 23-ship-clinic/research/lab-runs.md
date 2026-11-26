# 23-ship-clinic 實跑紀錄

## 本機 CPU 煙霧測試（2026-11-26）

- **環境**：Windows、Python 3.12.16、gradio（ml-helper 環境）。
- **設定**：沒有 HF_TOKEN（跳過上傳）；`LAB_NO_LAUNCH=1`（不啟動分享連結）。
- **結果**：
  - 每一格都執行完成；
  - 示範模型 `my_model("我的包裹一直沒到")` → 物流；
  - 檢查表六項都有內容；
  - `ship/README.md` 模型卡產生成功，含 YAML 與五個小節；
  - 示範模型的延遲以微秒計（關鍵字規則）。

## Colab 實跑

- [ ] 尚未執行（由講師執行）：`share=True` 連結、HF 上傳。
