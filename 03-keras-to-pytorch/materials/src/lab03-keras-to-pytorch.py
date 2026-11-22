# Source of lab03-keras-to-pytorch(.ipynb / -solution.ipynb). Build: python -X utf8 scripts/py2nb.py <this file>

# %% [markdown]
# # Lab L1-3：把 Keras 的 CIFAR-10 CNN 搬到 PyTorch（D1-3）
#
# **需求單 #D1-3**（虛構公司：曜嶼電子，工廠資訊組）：瑕疵分類器是 Keras 寫的；生成式工具都以 PyTorch 為主，所以要先搬家。
# **驗收**：同樣的架構、同樣的 epoch 數，PyTorch 版測試準確率和 Keras 版差距在 ±2 個百分點內；權重存成 `state_dict`。
#
# CIFAR-10 代替公司的瑕疵影像（DL 課 LabDay3-2 用過）。
#
# > 架構說明：這裡用經典的 Keras CIFAR-10 CNN（Conv32-Conv32-Pool-Conv64-Conv64-Pool-Dense512-Dense10）。**DL 課 LabDay3-2 的實際層數待講師核對**，不同時請改 `Net` 與第 2 格的 Keras 模型，兩邊保持一致。
#
# > 狀態：本筆記本尚未在 Colab T4 實跑（見 `research/lab-runs.md`）。

# %%
# 第 1 格：環境
import torch, torchvision, platform
print("torch", torch.__version__, "| torchvision", torchvision.__version__, "| python", platform.python_version())
device = "cuda" if torch.cuda.is_available() else "cpu"
print("device:", device, "|", torch.cuda.get_device_name(0) if device == "cuda" else "CPU（較慢：把 EPOCHS 改成 1）")
torch.manual_seed(0)
EPOCHS = 10
BATCH = 64

# %% [markdown]
# ## Try：Keras 參考版（選做，約數分鐘）
# 如果你保留了 DL 課的準確率，直接填在下面的 `KERAS_ACC`，跳過這格的訓練。

# %%
KERAS_ACC = None  # 例：填入 DL 課的測試準確率 0.7x；或執行下面的訓練
RUN_KERAS = False  # 改成 True 才會在這裡訓練 Keras 版
if RUN_KERAS:
    import keras
    from keras import layers
    (xtr, ytr), (xte, yte) = keras.datasets.cifar10.load_data()
    xtr, xte = xtr / 255.0, xte / 255.0
    km = keras.Sequential([
        keras.Input((32, 32, 3)),
        layers.Conv2D(32, 3, padding="same", activation="relu"), layers.Conv2D(32, 3, activation="relu"),
        layers.MaxPooling2D(), layers.Dropout(0.25),
        layers.Conv2D(64, 3, padding="same", activation="relu"), layers.Conv2D(64, 3, activation="relu"),
        layers.MaxPooling2D(), layers.Dropout(0.25),
        layers.Flatten(), layers.Dense(512, activation="relu"), layers.Dropout(0.5), layers.Dense(10),
    ])
    km.compile(optimizer=keras.optimizers.Adam(1e-3),
               loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=["accuracy"])
    km.fit(xtr, ytr, batch_size=BATCH, epochs=EPOCHS, verbose=2)
    KERAS_ACC = km.evaluate(xte, yte, verbose=0)[1]
print("Keras 參考準確率：", KERAS_ACC)

# %% [markdown]
# ## Open：Tensor、dtype、device、通道順序

# %%
x = torch.rand(64, 32, 32, 3)          # 像 Keras：[B, H, W, C]
print("Keras 排法", tuple(x.shape), x.dtype, x.device)
x = x.permute(0, 3, 1, 2)              # 換成 PyTorch：[B, C, H, W]
print("PyTorch 排法", tuple(x.shape))
x = x.to(device)
print("搬到", x.device)

# %% [markdown]
# ## Dataset 與 DataLoader
# `ToTensor()` 做兩件事：HWC → CHW，0–255 → 0–1（和 Keras 版的 `/255.0` 一樣）。

# %%
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

tf = transforms.ToTensor()
train_ds = datasets.CIFAR10("data", train=True, download=True, transform=tf)
test_ds = datasets.CIFAR10("data", train=False, download=True, transform=tf)

# >>> TODO: 建立 train_loader（shuffle=True）與 test_loader（shuffle=False），batch_size=BATCH
train_loader = DataLoader(train_ds, batch_size=BATCH, shuffle=True, num_workers=2)
test_loader = DataLoader(test_ds, batch_size=256, shuffle=False, num_workers=2)
# <<< TODO

xb, yb = next(iter(train_loader))
print("一個 batch：x", tuple(xb.shape), xb.dtype, "| y", tuple(yb.shape), yb.dtype, "| 像素範圍", xb.min().item(), xb.max().item())

# %% [markdown]
# ## nn.Module：`__init__` 建層，`forward` 接線
# **先別執行**：在投影片「練習：預測每一層的輸出 shape」寫下預測，再執行下一格對答案。

# %%
import torch.nn as nn

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        # >>> TODO: 照 Keras 版建立 features（兩個卷積區塊）與 classifier（Flatten→512→10）
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1), nn.ReLU(),
            nn.Conv2d(32, 32, 3), nn.ReLU(),
            nn.MaxPool2d(2), nn.Dropout(0.25),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(),
            nn.Conv2d(64, 64, 3), nn.ReLU(),
            nn.MaxPool2d(2), nn.Dropout(0.25),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(), nn.Linear(64 * 6 * 6, 512), nn.ReLU(), nn.Dropout(0.5), nn.Linear(512, 10),
        )
        # <<< TODO

    def forward(self, x):
        return self.classifier(self.features(x))

model = Net().to(device)
print("參數量：", sum(p.numel() for p in model.parameters()))

# 逐層印出 shape（對答案用）
h = xb[:64].to(device)
print(f"{'input':28s} {tuple(h.shape)}")
for layer in list(model.features) + list(model.classifier):
    h = layer(h)
    if not isinstance(layer, (nn.ReLU, nn.Dropout)):
        print(f"{layer.__class__.__name__ + str(tuple(getattr(layer, 'kernel_size', ()))):28s} {tuple(h.shape)}")

# %% [markdown]
# ## 常見錯誤：忘了 `zero_grad()`
# 同一個 batch 做兩次 `backward()`，看同一個梯度值怎麼變。

# %%
loss_fn = nn.CrossEntropyLoss()
w = model.classifier[-1].weight
xs, ys = xb[:8].to(device), yb[:8].to(device)
model.eval()  # 關掉 Dropout，讓兩次計算一樣
model.zero_grad()
loss_fn(model(xs), ys).backward(); g1 = w.grad[0, 0].item()
loss_fn(model(xs), ys).backward(); g2 = w.grad[0, 0].item()
print(f"第一次 backward 後：{g1:.6f}\n沒有 zero_grad 再一次：{g2:.6f}（約為 2 倍＝梯度被加總了）")
model.zero_grad()
model.train()

# %% [markdown]
# ## 訓練一步＝五行
# forward → loss → zero_grad → backward → step。Keras 的 `fit()` 幫你做了這五行。

# %%
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

def train_one_epoch(model, loader):
    model.train()
    total, n = 0.0, 0
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        # >>> TODO: 五行：算 logits、算 loss、清梯度、反向傳播、更新參數
        logits = model(x)
        loss = loss_fn(logits, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        # <<< TODO
        total += loss.item() * len(x); n += len(x)
    return total / n

@torch.no_grad()  # 裝飾器：整個函式都不記錄梯度（省記憶體、比較快）
def evaluate(model, loader):
    model.eval()  # 關掉 Dropout；BatchNorm 改用訓練時的統計值
    correct, n = 0, 0
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        correct += (model(x).argmax(1) == y).sum().item(); n += len(x)
    return correct / n

# %%
import time
history = []
t0 = time.time()
for epoch in range(1, EPOCHS + 1):
    tr_loss = train_one_epoch(model, train_loader)
    acc = evaluate(model, test_loader)
    history.append((epoch, tr_loss, acc))
    print(f"epoch {epoch:2d}  train loss {tr_loss:.3f}  test acc {acc:.3f}  ({time.time()-t0:.0f}s)")

# %% [markdown]
# ## Audit：和 Keras 版比較

# %%
pt_acc = history[-1][2]
print(f"PyTorch 準確率 {pt_acc:.3f}")
if KERAS_ACC is not None:
    gap = (pt_acc - KERAS_ACC) * 100
    print(f"Keras 準確率 {KERAS_ACC:.3f}，差距 {gap:+.1f} 個百分點 →", "通過" if abs(gap) <= 2 else "不通過：檢查架構、正規化、epoch 數")
else:
    print("沒有 Keras 參考值：請填 KERAS_ACC 或把 RUN_KERAS 改成 True")

import matplotlib.pyplot as plt
ep, ls, ac = zip(*history)
fig, ax = plt.subplots(1, 2, figsize=(9, 3))
ax[0].plot(ep, ls, marker="o"); ax[0].set_title("train loss")
ax[1].plot(ep, ac, marker="o"); ax[1].set_title("test accuracy")
plt.tight_layout(); plt.show()

# %% [markdown]
# ## Ship：存成 `state_dict`，再載回來驗證

# %%
torch.save(model.state_dict(), "cifar_cnn.pt")
model2 = Net().to(device)
model2.load_state_dict(torch.load("cifar_cnn.pt", map_location=device))
print("載回後準確率：", evaluate(model2, test_loader), "（應與上面相同）")

# %% [markdown]
# ## 選做：用梯度下降找平均值（最大概似的直覺）
# 讓「平方誤差最小」的 μ，就是資料的平均。之後 D5-2 的交叉熵也是同一個想法：讓資料出現的機率最大。

# %%
data = torch.randn(1000) * 2 + 5
mu = torch.zeros(1, requires_grad=True)
opt = torch.optim.SGD([mu], lr=0.1)
for step in range(100):
    loss = ((data - mu) ** 2).mean()
    opt.zero_grad(); loss.backward(); opt.step()
print(f"梯度下降找到 μ = {mu.item():.3f}；資料平均 = {data.mean().item():.3f}")
