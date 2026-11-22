# 03-keras-to-pytorch 查證紀錄

**2026-11-23 製作時沒有上網核對；下列標「待確認」。** shape 由卷積規則推算，筆記本會逐層印出驗證。

| id | 主張 | 來源 | 狀態 | 日期 |
|---|---|---|---|---|
| S1–S4 | transformers、diffusers、peft、trl 以 PyTorch 為主要後端 | 各套件官方文件 | 待確認 | 2026-11-23 |
| S5 | `nn.Module`、`DataLoader`、`zero_grad` 累加梯度、`eval()`、`no_grad`、`state_dict` 用法 | PyTorch 官方文件與教學 *Learn the Basics* | 待確認（API 穩定，作者熟悉） | 2026-11-23 |
| S6 | Conv2d 輸出大小 ⌊(H+2p−k)/s⌋+1；MaxPool2d 向下取整 | PyTorch `Conv2d`、`MaxPool2d` 文件 | 待確認 | 2026-11-23 |
