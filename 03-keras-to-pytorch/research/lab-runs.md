# 03-keras-to-pytorch Lab 實跑紀錄

每本筆記本在 Colab 從頭跑完後記一列。投影片上的數字、圖片、VRAM 與時間只能引用這裡有紀錄的實跑。

| 日期 | 筆記本 | GPU | torch | 其他套件版本 | VRAM 峰值 | 總時間 | seed | 結果／備註 |
|---|---|---|---|---|---|---|---|---|
| 2026-11-23 | lab03-keras-to-pytorch-solution（煙霧測試） | 無（本機 CPU） | 2.15.0+cpu | torchvision 0.29.2 | — | — | 0 | **不是 T4 實跑**。CIFAR-10 以 FakeData 代替、EPOCHS=1。逐層 shape 與練習解答一致：[64,32,32,32]→[64,32,30,30]→[64,32,15,15]→[64,64,15,15]→[64,64,13,13]→[64,64,6,6]→[64,2304]→[64,512]→[64,10]；參數量 1,250,858；存檔載回準確率不變；梯度下降 μ 收斂到資料平均。發現並修正兩個錯誤：逐層列印對 `MaxPool2d` 失敗；zero_grad 示範選到為 0 的梯度（改用最後一層 bias） |
| 2026-11-26 | lab03-keras-to-pytorch-solution，第 1 格到「常見錯誤」格（不含 Keras、不含訓練） | 無（本機 CPU） | 2.15.0+cpu | torchvision 0.29.2；num_workers 改 0（Windows） | — | — | 0 | **不是 T4 實跑**。真實 CIFAR-10。zero_grad 示範：第一次 backward 後 -0.149505；沒有 zero_grad 再一次 -0.299010（恰為 2 倍）。投影片「忘了 zero_grad()」引用此列 |
