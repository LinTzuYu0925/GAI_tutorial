# D1-3 · 從 Keras 到 PyTorch · 工作筆記

最後更新：2026-11-23。

## 1. 檔案

| 檔案 | 用途 |
|---|---|
| `outline.md` | 大綱（講師以 /goal 自動核准） |
| `slides.md` | 投影片（25 頁，其中 2 頁 hostOnly） |
| `materials/src/lab03-keras-to-pytorch.py` | 筆記本原始檔（`python -X utf8 ../scripts/py2nb.py materials/src/lab03-keras-to-pytorch.py`） |
| `materials/lab03-keras-to-pytorch.ipynb`、`-solution.ipynb` | Lab L1-3 |

## 2. 進度

- [x] 大綱、投影片、筆記本
- [ ] Colab T4 實跑（尚未）
- [x] build、PNG 檢視、`check-order.cjs`、`scan-zh.py`
- [ ] slide-reviewer 審查

## 3. 決定

| 日期 | 內容 |
|---|---|
| 2026-11-23 | Lab 用橋接課三頁版（demo-and-practice §3c） |
| 2026-11-23 | 架構用經典 Keras CIFAR-10 CNN，待核對 LabDay3-2 |
| 2026-11-23 | 優化器兩邊都用 Adam 1e-3、batch 64、10 epochs |

## 4. 本單元詞彙（中文統一）

| 英文 | 中文 | 首次出現頁 |
|---|---|---|
| device | 裝置（cpu、cuda） | 7 |
| channel | 通道 | 8 |
| DataLoader | 資料載入器（保留英文） | 12 |
| gradient | 梯度 | 13 |
| decorator | 裝飾器 | 15 |
| state_dict | 權重字典（保留英文） | 16 |
| broadcasting | 廣播（保留英文） | 17 |
| maximum likelihood | 最大概似 | 18 |
