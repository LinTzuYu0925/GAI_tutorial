# 教學計畫：D1-3 從 Keras 到 PyTorch

更新：2026-11-23　對應投影片：`slides.md`（25 頁，其中 2 頁 hostOnly）。預算：120 分鐘。

## 1. 怎麼使用這份計畫

- **學員**：Colab（T4）跑 `lab03-keras-to-pytorch.ipynb`；第 10 頁輸入 shape 預測。
- **沒有 GPU 額度**：`EPOCHS = 1` 在 CPU 跑。
- **沒有 Agent 額度**：照第 9、12、13 頁填 TODO。
- **誠實原則**：準確率、時間、梯度值都來自實跑（`research/lab-runs.md`）。

## 2. 時間表

| 區塊 | 頁 | 分鐘 | 標記 |
|---|---|---|---|
| 開場、需求單、目標、為什麼 | 1–4 | 8 | ★ |
| Keras 回顧、對照表 | 5–6 | 9 | ★ |
| Tensor、通道、nn.Module | 7–9 | 15 | ★ |
| 練習＋解答 | 10–11 | 13 | ★ |
| DataLoader、五行、zero_grad、eval、存檔 | 12–16 | 25 | ★ |
| Broadcasting、MLE 暖身 | 17–18 | 7 | ○ |
| Lab 1–3 | 19–21 | 34 | ★ |
| Lightning | 22 | 1 | △ |
| 總整理、檢核 | 23–24 | 6 | ★ |

合計：★ 110 分、★＋○ 117 分、全部 118 分（預算 120；建議中間休息 10 分時讓訓練跑著）。

## 3. 課前準備清單

- [ ] 核對 DL 課 LabDay3-2 架構，必要時改 `Net` 與 Keras 參考格
- [ ] Colab T4 實跑解答筆記本，記錄每 epoch 時間與準確率
- [ ] 替換第 14 頁 placeholder（梯度值）
