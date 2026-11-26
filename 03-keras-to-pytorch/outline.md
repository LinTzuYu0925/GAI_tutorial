# D1-3 · 從 Keras 到 PyTorch

> 依據：`planning/slide-plan/D1-value-and-tooling.md` 的 D1-3。**狀態：講師以 /goal 指示自動核准（2026-11-23）**。
> 時間：2 小時（橋接課，roadmap 估約 2 小時）。**不教**：Lightning、Accelerate、分散式訓練、自訂 CUDA。

## 1. 學員假設與學習目標

- **學員**：會 Keras 的 `Sequential`／繼承 `keras.Model`／`compile`／`fit`（DL pp.16–33、p.20）、CNN（DL pp.38–55）、類別（Vibe 13）、shape／dtype（Vibe 12a）；DL 課 LabDay3-2 跑過 CIFAR-10 CNN。**沒寫過** PyTorch（curriculum-analysis 前置缺口）。
- **不教**：新的 AI 概念。

學完後，學員能夠：

1. **對照** Keras 的每一步在 PyTorch 叫什麼。
2. **預測**卷積網路每一層的輸出 shape（不靠 AI）。
3. **寫出並解釋**訓練一步的五行程式。
4. **移植** CNN、比較準確率、存成 `state_dict`。

## 2. 概念地圖

| 概念 | 白話定義 | 解決的問題 | 先備 | 例子 | 常見誤解 |
|---|---|---|---|---|---|
| Tensor／device | 會自動微分、知道自己在哪個裝置的陣列 | GPU 計算 | Vibe 12a | `.to("cuda")` | Keras 會自動放 GPU，所以 PyTorch 也會 |
| [B, C, H, W] | 通道在前 | 對接所有影像模型 | DL CNN | permute | 和 Keras 一樣 |
| nn.Module | `__init__` 建層、`forward` 接線 | 定義模型 | DL p.20 | Net | 要呼叫 `forward()` |
| DataLoader | 一批一批、打亂地給資料 | 取代 `fit(batch_size)` | Vibe 13 | CIFAR10 | — |
| 五行迴圈 | forward、loss、zero_grad、backward、step | 取代 `fit()` | DL pp.25–27 | train_one_epoch | 忘了 zero_grad |
| eval／no_grad | 評估模式、不記梯度 | 正確評估 | DL Dropout | evaluate | 忘了 eval |
| state_dict | 層名稱→權重 | 存檔 | — | cifar_cnn.pt | 存了就能直接載，不用類別 |

## 3. 投影片順序

<!-- slide-table:start -->
| # | 標題 | 區塊 | 一句話重點 | ★/○/△ | 學員看得到 |
|---|---|---|---|---|---|
| 1 | 從 Keras 到 PyTorch | 生成式AI原理 · L03 |  | ★ | 是 |
| 2 | 工廠資訊組：分類器要搬家 | 00 · Frame（定義問題） |  | ★ | 是 |
| 3 | 今天結束時，你能夠…… | 學習目標 |  | ★ | 是 |
| 4 | 為什麼要搬到 PyTorch？ | 00 · Frame | 不是 Keras 不好，而是這門課要用的生成式工具都建在 PyTorch 上。 | ★ | 是 |
| 5 | 先回顧：你在 DL 課跑過的 Keras 版 | 01 · Try（先用現成的） | 你已經會每一步；只是 fit() 一行把「訓練迴圈」藏起來了。 | ★ | 是 |
| 6 | Keras ↔ PyTorch 對照表 | 02 · Open（打開黑盒子） | 只有「訓練」那一列差最多：Keras 一行，PyTorch 自己寫。 | ★ | 是 |
| 7 | Tensor：資料和模型要在同一個 device | 02 · Open · Tensor | Keras 自動決定 GPU；PyTorch 要你自己把模型和每個 batch 搬過去。 | ★ | 是 |
| 8 | 通道放哪裡？Keras 放最後，PyTorch 放前面 | 02 · Open · 通道順序 | 同一張圖，只是軸的順序不同；看到 shape 先問「通道在哪一維」。 | ★ | 是 |
| 9 | nn.Module：和繼承 keras.Model 一樣 | 02 · Open · nn.Module | PyTorch 的卷積要寫「輸入通道數」；Keras 會自己推。 | ★ | 是 |
| 10 | 練習：預測每一層的輸出 shape | 02 · Open · nn.Module · 練習 |  | ★ | 是 |
| 11 | 練習解答：64 × 6 × 6 ＝ 2304 是這樣來的 | 02 · Open · nn.Module · 練習解答 | 怎麼對答案：筆記本逐層 print(h.shape)；Flatten 的數字寫錯，第一個 Linear 就會報 shape 錯誤。 | ★ | 否（hostOnly） |
| 12 | Dataset 與 DataLoader：取代 <code>fit(batch_size=…)</code> | 02 · Open · 資料 | Dataset 回答「一筆」，DataLoader 負責「一批一批、打亂地給」。 | ★ | 是 |
| 13 | 訓練一步＝五行程式 | 03 · Adapt（調成我們的）· 訓練迴圈 | Keras 的 fit() 每一批都在做這五件事；PyTorch 讓你看見、也讓你改。 | ★ | 是 |
| 14 | 忘了 <code>zero_grad()</code>：梯度會一直加上去 | 03 · Adapt · 常見錯誤 | PyTorch 預設把梯度「累加」；每一批開始前都要清空。 | ★ | 是 |
| 15 | 評估前：<code>model.eval()</code> ＋ <code>torch.no_grad()</code> | 03 · Adapt · 評估 | 忘了 eval()：準確率會忽高忽低；訓練時記得切回 model.train()。 | ★ | 是 |
| 16 | 存檔：只存權重（state_dict） | 04 · Ship（交付） | state_dict 只有數字，沒有程式；載入時要先有同樣的 Net 類別。 | ★ | 是 |
| 17 | Broadcasting（廣播）：shape 不同也能相減 | 附錄 · 選修 | 從最後一維往前對齊；大小是 1 的維度會自動延伸。 | ○ | 是 |
| 18 | 加碼：用梯度下降找平均值 | 附錄 · 選修 | 「找參數讓資料最像模型會產生的」——這就是訓練生成模型的核心。 | ○ | 是 |
| 19 | Lab 1／3：Specify | 05 · Lab L1-3 |  | ★ | 是 |
| 20 | Lab 2／3：Generate → Execute | 05 · Lab L1-3 |  | ★ | 是 |
| 21 | Lab 3／3：Audit → Iterate——「跑得動」不等於「搬對了」 | 05 · Lab L1-3 | 差太多時一次只改一件事（例如補上 Dropout），再跑一次比較。 | ★ | 是 |
| 22 | PyTorch Lightning、Accelerate | 附錄 · 只認名字 | 先會自己寫迴圈，再用工具省事；這門課不用它們。 | △ | 是 |
| 23 | 今天學到的概念鏈 | 總整理 | 之後每個生成模型都用同一個迴圈，只換模型和損失函數。 | ★ | 是 |
| 24 | 隨堂檢核 1／2（iPAS 題型）：點選答案 | 隨堂檢核 |  | ★ | 是 |
| 25 | 隨堂檢核 2／2（iPAS 題型）：點選答案 | 隨堂檢核 |  | ★ | 是 |
| 26 | 下一堂 L04：斷線不怕、主管點得到 | 下一步 |  | ★ | 否（hostOnly） |
<!-- slide-table:end -->

## 4. Lab

| Lab | 筆記本 | 模型／資料 | T4 VRAM 峰值 | 時間 | 備案 |
|---|---|---|---|---|---|
| L1-3 | `materials/lab03-keras-to-pytorch.ipynb`（解答：`-solution.ipynb`；原始檔 `materials/src/`） | CIFAR-10（torchvision）；Keras 參考版選做 | 待實測 | 約 45 分（10 epochs，待實測） | CPU：EPOCHS=1；無 Agent：照投影片填；斷線：解答筆記本 |

## 5. 常見誤解

- 呼叫 `model.forward(x)`（第 9 頁備註）。
- 忘了 `zero_grad()`，梯度累加（第 14 頁）。
- 忘了 `model.eval()`（第 15 頁）。
- 「Agent 移植的程式跑得動」＝「搬對了」（第 21 頁）。

## 6. 隨堂檢核

第 24–25 頁四題（點選式，每頁兩題），答案在講者備註。

## 7. 待查證

- DL 課 LabDay3-2 的實際架構與準確率（本 deck 用經典 Keras CIFAR-10 CNN）。
- `keras` 在 Colab 是否預裝（Keras 參考格）。
- 每 epoch 時間、VRAM。

## 8. 待講師決定

- 是否現場訓練 Keras 參考版（多幾分鐘），或請學員填自己 DL 課的準確率。
