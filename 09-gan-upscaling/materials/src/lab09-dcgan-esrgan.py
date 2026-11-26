# Source of lab09-dcgan-esrgan(.ipynb / -solution.ipynb). Build: python -X utf8 scripts/py2nb.py <this file>

# %% [markdown]
# # Lab L3-1：偽造者與鑑定師——DCGAN 與 Real-ESRGAN（D3-1）
#
# **需求單 #D3-1**（虛構公司：曜嶼電子，電商部）：數千張舊型錄照片解析度太低，網站改版用不了。
#
# | 步驟 | 做什麼 | 輸出 |
# |---|---|---|
# | A | Real-ESRGAN：把一張 233×263 的舊照片放大 4 倍，和一般放大（bicubic）比較 | 對照圖、每張秒數 |
# | B | 自己訓練 DCGAN（Fashion-MNIST）：G 偽造、D 鑑定 | 兩條 loss、每個 epoch 的網格 |
# | C | 看網格：哪裡開始像？有沒有一直重複的圖（mode collapse）？ | 你的判斷 |
#
# > 狀態：講師已在 Colab T4 跑過（Real-ESRGAN 一張約 0.6 秒、VRAM 約 0.6 GB；DCGAN 20 個 epoch 約 6 分鐘），見 `research/lab-runs.md`。

# %%
# 第 1 格：環境（spandrel 用來載入 Real-ESRGAN 的權重，不需要 basicsr）
%pip install -q -U spandrel
import torch, time, platform, random, io, os, urllib.request
import numpy as np
import matplotlib.pyplot as plt
print("torch", torch.__version__, "| python", platform.python_version())
device = "cuda" if torch.cuda.is_available() else "cpu"
if device == "cuda":
    free, total = torch.cuda.mem_get_info()
    print("GPU:", torch.cuda.get_device_name(0), f"| 可用 VRAM {free/1e9:.1f} / {total/1e9:.1f} GB")
SEED = 0            # Lab 5／7：改成你的座號，和講師的 SEED＝0 比較
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
EPOCHS = 20         # 沒有 GPU：改成 2
LR_G = 2e-4         # Lab 6／7 的實驗：一次只改一件事，例如把 G 的學習率調大，看會不會崩塌

# %% [markdown]
# ## A. Real-ESRGAN：舊照片放大 4 倍
# 照片：耳機（Sprinno，CC0，Wikimedia Commons），原圖只有 233 × 263。
# 模型：Real-ESRGAN x4plus（BSD-3-Clause），用 `spandrel` 載入。

# %%
from PIL import Image
from torchvision.transforms.functional import to_tensor, to_pil_image

def fetch(url, path, tries=3):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    for attempt in range(tries):
        if os.path.exists(path):
            break
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "gai-course-lab/1.0 (classroom notebook)"})
            open(path, "wb").write(urllib.request.urlopen(req, timeout=300).read())
        except Exception as e:
            print("下載失敗，10 秒後重試：", e); time.sleep(10)
    if not os.path.exists(path):
        raise SystemExit(f"還是下載不到 {path}：請從左邊的「檔案」面板上傳課程資料夾 data/download/headphones.jpg（同一張照片，CC0）")
    return path

# 全班同時下載時，Wikimedia 可能回 HTTP 429（限流）；重試三次後還不行，就手動上傳 data/download/headphones.jpg
PHOTO = fetch("https://upload.wikimedia.org/wikipedia/commons/6/63/Headphones_on_white_background.jpg", "data/download/headphones.jpg")
WEIGHTS = fetch("https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth", "data/download/RealESRGAN_x4plus.pth")
low = Image.open(PHOTO).convert("RGB")
print("原圖", low.size)

from spandrel import ModelLoader
sr_model = ModelLoader().load_from_file(WEIGHTS).to(device).eval()
print("模型：", sr_model.architecture.name, "| 放大倍數", sr_model.scale)

# %%
x = to_tensor(low).unsqueeze(0).to(device)                 # [1, 3, 263, 233]，0–1
if device == "cuda":
    torch.cuda.synchronize(); torch.cuda.reset_peak_memory_stats()
t0 = time.time()
with torch.no_grad():
    # >>> TODO: 把 x 交給 sr_model，結果夾在 0–1 之間
    y = sr_model(x).clamp(0, 1)
    # <<< TODO
if device == "cuda":
    torch.cuda.synchronize()
print(f"Real-ESRGAN：{tuple(x.shape)} → {tuple(y.shape)}，{time.time()-t0:.2f} 秒")
if device == "cuda":
    print(f"VRAM 峰值 {torch.cuda.max_memory_allocated()/1e9:.2f} GB")

big_esrgan = to_pil_image(y[0].cpu())
big_bicubic = low.resize(big_esrgan.size, Image.BICUBIC)     # 一般放大：只用周圍像素內插
big_esrgan.save("headphones_esrgan_x4.png"); big_bicubic.save("headphones_bicubic_x4.png")

box = (150, 480, 450, 780)                                   # 放大看左邊耳罩的一塊
fig, ax = plt.subplots(1, 3, figsize=(14, 5))
ax[0].imshow(low); ax[0].set_title(f"original {low.size[0]}x{low.size[1]}")
ax[1].imshow(big_bicubic.crop(box)); ax[1].set_title("bicubic x4 (crop)")
ax[2].imshow(big_esrgan.crop(box)); ax[2].set_title("Real-ESRGAN x4 (crop)")
for a in ax: a.axis("off")
plt.tight_layout(); plt.savefig("esrgan_compare.png", dpi=120); plt.show()

# %% [markdown]
# ## B. 自己訓練 DCGAN
# - **G（偽造者）**：隨機數字 z [B, 100] → 一張 28×28 的圖
# - **D（鑑定師）**：一張圖 → 一個分數（logit），越大越像「真的」
#
# **先別執行**：在投影片「練習：G 每一層的 shape」寫下預測。

# %%
import torch.nn as nn
import torch.nn.functional as F
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

tf = transforms.Compose([transforms.ToTensor(), transforms.Normalize([0.5], [0.5])])   # −1～1，配合 G 最後的 tanh
train_ds = datasets.FashionMNIST("data/download", train=True, download=True, transform=tf)
loader = DataLoader(train_ds, batch_size=128, shuffle=True, drop_last=True)
Z = 100

class G(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Sequential(nn.Linear(Z, 128 * 7 * 7), nn.BatchNorm1d(128 * 7 * 7), nn.ReLU())
        self.net = nn.Sequential(
            nn.ConvTranspose2d(128, 64, 4, 2, 1), nn.BatchNorm2d(64), nn.ReLU(),     # 7 → 14
            nn.ConvTranspose2d(64, 1, 4, 2, 1), nn.Tanh())                            # 14 → 28
    def forward(self, z, show=False):
        h = self.fc(z).view(-1, 128, 7, 7)
        out = self.net(h)
        if show:
            print("z", tuple(z.shape), "→ fc 後", tuple(h.shape), "→ 輸出", tuple(out.shape))
        return out

class D(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(1, 64, 4, 2, 1), nn.LeakyReLU(0.2),                             # 28 → 14
            nn.Conv2d(64, 128, 4, 2, 1), nn.BatchNorm2d(128), nn.LeakyReLU(0.2),      # 14 → 7
            nn.Flatten(), nn.Linear(128 * 7 * 7, 1))                                  # 一個 logit
    def forward(self, x):
        return self.net(x).view(-1)

g, d = G().to(device), D().to(device)
with torch.no_grad():
    g(torch.randn(16, Z, device=device), show=True)
print("D 的輸出", tuple(d(torch.randn(16, 1, 28, 28, device=device)).shape))

# %% [markdown]
# **訓練迴圈：兩個優化器，輪流走一步**
# 1. **D 這一步**：真圖標 1、假圖標 0，D 學著分辨（假圖要 `detach()`，這一步不更新 G）
# 2. **G 這一步**：把假圖交給 D，但標成 **1**——G 想讓 D 以為是真的（non-saturating 寫法）

# %%
bce = nn.BCEWithLogitsLoss()
opt_g = torch.optim.Adam(g.parameters(), lr=LR_G, betas=(0.5, 0.999))
opt_d = torch.optim.Adam(d.parameters(), lr=2e-4, betas=(0.5, 0.999))
fixed_z = torch.randn(32, Z, device=device)                  # 固定同一批 z，才看得出同一張圖怎麼變
hist, grids = [], {}
t0 = time.time()
for epoch in range(1, EPOCHS + 1):
    for real, _ in loader:
        real = real.to(device); B = len(real)
        ones, zeros = torch.ones(B, device=device), torch.zeros(B, device=device)
        fake = g(torch.randn(B, Z, device=device))
        # >>> TODO: D 這一步：loss_d ＝ bce(d(real), ones) ＋ bce(d(fake.detach()), zeros)；zero_grad、backward、step
        loss_d = bce(d(real), ones) + bce(d(fake.detach()), zeros)
        opt_d.zero_grad(); loss_d.backward(); opt_d.step()
        # <<< TODO
        # >>> TODO: G 這一步：loss_g ＝ bce(d(fake), ones)（假圖標成「真」）；zero_grad、backward、step
        loss_g = bce(d(fake), ones)
        opt_g.zero_grad(); loss_g.backward(); opt_g.step()
        # <<< TODO
        hist.append((loss_d.item(), loss_g.item()))
    g.eval()
    with torch.no_grad():
        grids[epoch] = g(fixed_z).cpu()
    g.train()
    print(f"epoch {epoch:2d}  loss_D {loss_d.item():.3f}  loss_G {loss_g.item():.3f}  ({time.time()-t0:.0f}s)")
torch.save(g.state_dict(), "dcgan_g.pt")

# %%
h = np.array(hist)
plt.figure(figsize=(10, 3)); plt.plot(h[:, 0], label="D", alpha=0.7); plt.plot(h[:, 1], label="G", alpha=0.7)
plt.xlabel("step"); plt.ylabel("loss"); plt.legend(); plt.title("GAN losses go up and down: they do not tell you quality"); plt.show()

show = sorted({e for e in [1, EPOCHS // 4, EPOCHS // 2, EPOCHS] if e in grids})
fig, ax = plt.subplots(len(show), 1, figsize=(12, 1.9 * len(show)))
for a, e in zip(np.atleast_1d(ax), show):
    a.imshow(torch.cat(list(grids[e][:16, 0]), 1) * 0.5 + 0.5, cmap="gray"); a.set_title(f"epoch {e}", loc="left"); a.axis("off")
plt.tight_layout(); plt.savefig("dcgan_grids.png", dpi=120); plt.show()

# %% [markdown]
# ## C. 有沒有 mode collapse？
# 同一批 32 個 z 產生的圖，彼此有多像？算兩兩之間的平均像素距離：**越小，代表越常畫出同樣的東西**。
# 拿真實圖片的同一個數字當參考。

# %%
def mean_pairwise(x):
    f = x.view(len(x), -1)
    dmat = torch.cdist(f, f)
    return dmat.sum() / (len(x) * (len(x) - 1))

real32 = torch.stack([train_ds[i][0] for i in range(32)])
print("真實 32 張的兩兩平均距離：%.2f" % mean_pairwise(real32))
for e in show:
    print(f"epoch {e:2d} 生成 32 張的兩兩平均距離：{mean_pairwise(grids[e]):.2f}")
