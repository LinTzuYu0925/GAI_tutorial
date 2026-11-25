# Source of lab13-cfg(.ipynb / -solution.ipynb). Build: python -X utf8 scripts/py2nb.py <this file>

# %% [markdown]
# # Lab L4-1：指定生成第 k 類——類別條件 DDPM ＋ classifier-free guidance（D4-1）
#
# **需求單 #D4-1**（虛構公司：曜嶼電子，數據組）：網店商品分類器對少數類別很弱，能不能「指定」生成第 k 類的圖來補資料？
# D3-3 的 DDPM 只能隨機生成；今天讓它聽懂「我要第 k 類」。
#
# | 部分 | 做什麼 | 輸出 |
# |---|---|---|
# | 1 | 資料與雜訊排程（和 D3-3 相同：T＝1000，β 從 0.0001 線性增加到 0.02） | ᾱ_t 曲線 |
# | 2 | 小 U-Net ＋ **類別嵌入**；訓練時隨機把 10% 的標籤換成「沒有標籤」（label dropout） | 每個 epoch 的損失 |
# | 3 | 取樣時用 **CFG**：ε ＝ ε_uncond ＋ w ·（ε_cond − ε_uncond） | w ＝ 0、1、3、7 的網格 |
# | 4 | 量測：分類器認對的比例（忠實度）、同類兩兩距離（多樣性）、特徵空間的 FID／KID | 對照表 |
#
# **學習評量（b）「實作條件生成」就是這本筆記本**：交出跑完的筆記本，並能不靠 AI 口頭解釋你的 CFG 那一行。

# %%
# 第 1 格：環境
import torch, time, platform, random, math
import numpy as np
import matplotlib.pyplot as plt
import torch.nn as nn
import torch.nn.functional as F
print("torch", torch.__version__, "| python", platform.python_version())
device = "cuda" if torch.cuda.is_available() else "cpu"
if device == "cuda":
    free, total = torch.cuda.mem_get_info()
    print("GPU:", torch.cuda.get_device_name(0), f"| 可用 VRAM {free/1e9:.1f} / {total/1e9:.1f} GB")
SEED = 0            # 想和隔壁同學比較時，改成你的座號
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
EPOCHS = 10         # 沒有 GPU：改成 1（並把下面的 SUBSET 設成 3000）
SUBSET = None       # None＝用全部 60000 張訓練圖
P_UNCOND = 0.1      # label dropout：每張圖有 10% 的機率被藏起標籤
N_PER_CLASS = 100   # 量測時每一類生成幾張（沒有 GPU：改成 10）
W_LIST = [0, 1, 3, 7]

# %% [markdown]
# ## 1. 資料與雜訊排程
# Fashion-MNIST 28 × 28，四邊各補 2 個像素變成 32 × 32（U-Net 要能一直除以 2），值域 −1～1（和 D3-1、D3-3 一樣）。
#
# 排程和 D3-3 相同：T ＝ 1000 步，β_t 從 0.0001 線性增加到 0.02，ᾱ_t ＝ (1−β_1)(1−β_2)…(1−β_t)。

# %%
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, Subset
CLASSES = ["T恤", "褲子", "套頭衫", "洋裝", "外套", "涼鞋", "襯衫", "運動鞋", "包包", "短靴"]
tf = transforms.Compose([transforms.Pad(2), transforms.ToTensor(), transforms.Normalize([0.5], [0.5])])
train_ds = datasets.FashionMNIST("data", train=True, download=True, transform=tf)
test_ds = datasets.FashionMNIST("data", train=False, download=True, transform=tf)
if SUBSET:
    train_ds = Subset(train_ds, range(SUBSET))
loader = DataLoader(train_ds, batch_size=128, shuffle=True, drop_last=True, num_workers=2)
x0, y = next(iter(loader))
print("一批圖", tuple(x0.shape), "| 值域", round(x0.min().item(), 2), "～", round(x0.max().item(), 2), "| 標籤", y[:8].tolist())

T = 1000
betas = torch.linspace(1e-4, 0.02, T, device=device)
alphas = 1 - betas
abar = torch.cumprod(alphas, dim=0)
plt.figure(figsize=(5, 2.6)); plt.plot(abar.cpu()); plt.xlabel("t"); plt.ylabel("ᾱ_t"); plt.title("剩下多少原圖"); plt.tight_layout(); plt.show()

def add_noise(x0, t, eps):
    """D3-3 的「一步跳到第 t 步」：x_t = √ᾱ_t · x₀ + √(1−ᾱ_t) · ε"""
    a = abar[t].view(-1, 1, 1, 1)
    return a.sqrt() * x0 + (1 - a).sqrt() * eps

# %% [markdown]
# ## 2. 小 U-Net ＋ 類別嵌入
# 和 D3-3 的小 U-Net 一樣接收 x_t 和 t；**今天多一個輸入：類別 y**。
#
# - `nn.Embedding(11, 128)`：10 個類別 ＋ 第 11 個「沒有標籤」（編號 `NULL = 10`）
# - 類別向量和時間向量**相加**，送進每一個殘差區塊（和時間嵌入同一條路）

# %%
NULL = 10   # 「沒有標籤」的編號

def time_embedding(t, dim=128):
    """D3-3 的正弦時間嵌入：t → 128 維向量"""
    half = dim // 2
    freqs = torch.exp(-math.log(10000) * torch.arange(half, device=t.device) / half)
    ang = t.float()[:, None] * freqs[None]
    return torch.cat([ang.sin(), ang.cos()], dim=1)

class ResBlock(nn.Module):
    def __init__(self, cin, cout, emb=128):
        super().__init__()
        self.n1, self.c1 = nn.GroupNorm(8, cin), nn.Conv2d(cin, cout, 3, padding=1)
        self.e = nn.Linear(emb, cout)
        self.n2, self.c2 = nn.GroupNorm(8, cout), nn.Conv2d(cout, cout, 3, padding=1)
        self.skip = nn.Conv2d(cin, cout, 1) if cin != cout else nn.Identity()
    def forward(self, x, e):
        h = self.c1(F.silu(self.n1(x)))
        h = h + self.e(e)[:, :, None, None]           # 嵌入（時間＋類別）加到每個像素
        h = self.c2(F.silu(self.n2(h)))
        return h + self.skip(x)

class CondUNet(nn.Module):
    def __init__(self, ch=(64, 128, 256), emb=128, n_classes=10):
        super().__init__()
        self.t_mlp = nn.Sequential(nn.Linear(emb, emb), nn.SiLU(), nn.Linear(emb, emb))
        self.y_emb = nn.Embedding(n_classes + 1, emb)  # 多一格給「沒有標籤」
        self.inp = nn.Conv2d(1, ch[0], 3, padding=1)
        self.d1, self.d2 = ResBlock(ch[0], ch[0]), ResBlock(ch[0], ch[1])
        self.d3 = ResBlock(ch[1], ch[2])
        self.mid = ResBlock(ch[2], ch[2])
        self.u3 = ResBlock(ch[2] + ch[2], ch[1])
        self.u2 = ResBlock(ch[1] + ch[1], ch[0])
        self.u1 = ResBlock(ch[0] + ch[0], ch[0])
        self.out = nn.Conv2d(ch[0], 1, 3, padding=1)
    def forward(self, x, t, y):
        e = self.t_mlp(time_embedding(t)) + self.y_emb(y)   # 時間向量 ＋ 類別向量
        h1 = self.d1(self.inp(x), e)                  # [B, 64, 32, 32]
        h2 = self.d2(F.avg_pool2d(h1, 2), e)          # [B,128, 16, 16]
        h3 = self.d3(F.avg_pool2d(h2, 2), e)          # [B,256,  8,  8]
        m = self.mid(F.avg_pool2d(h3, 2), e)          # [B,256,  4,  4]
        u = self.u3(torch.cat([F.interpolate(m, scale_factor=2), h3], 1), e)
        u = self.u2(torch.cat([F.interpolate(u, scale_factor=2), h2], 1), e)
        u = self.u1(torch.cat([F.interpolate(u, scale_factor=2), h1], 1), e)
        return self.out(u)                            # 預測的雜訊 ε̂，[B, 1, 32, 32]

model = CondUNet().to(device)
print(f"參數量 {sum(p.numel() for p in model.parameters()):,}")
with torch.no_grad():
    t_try = torch.randint(0, T, (4,), device=device)
    print("輸入", (4, 1, 32, 32), "→ 輸出", tuple(model(x0[:4].to(device), t_try, y[:4].to(device)).shape))

# %% [markdown]
# ### 訓練：和 D3-3 只差一行
# 每一批先把 10% 的標籤換成 `NULL`：同一個模型就同時學會「有條件」和「沒條件」兩種預測。
# 這就是 classifier-free：**不需要另外訓練一個分類器**來引導。

# %%
opt = torch.optim.AdamW(model.parameters(), lr=2e-4)
use_amp = device == "cuda"
scaler = torch.amp.GradScaler("cuda", enabled=use_amp)
if device == "cuda":
    torch.cuda.reset_peak_memory_stats()
losses, t0 = [], time.time()
for epoch in range(EPOCHS):
    model.train(); run = 0.0
    for x0, y in loader:
        x0, y = x0.to(device), y.to(device)
        t = torch.randint(0, T, (x0.shape[0],), device=device)
        eps = torch.randn_like(x0)
        # >>> TODO: label dropout——每張圖有 P_UNCOND 的機率把標籤換成 NULL
        drop = torch.rand(y.shape[0], device=device) < P_UNCOND
        y_in = torch.where(drop, torch.full_like(y, NULL), y)
        # <<< TODO
        with torch.autocast(device_type=device, dtype=torch.float16, enabled=use_amp):
            loss = F.mse_loss(model(add_noise(x0, t, eps), t, y_in), eps)   # 預測雜訊（D3-3）
        opt.zero_grad(); scaler.scale(loss).backward(); scaler.step(opt); scaler.update()
        run += loss.item()
    losses.append(run / len(loader))
    print(f"epoch {epoch+1:2d}/{EPOCHS} | loss {losses[-1]:.4f} | 累計 {time.time()-t0:.0f}s")
if device == "cuda":
    print(f"VRAM 峰值 {torch.cuda.max_memory_allocated()/1e9:.2f} GB")
torch.save(model.state_dict(), "cfg_unet.pt")   # 斷線後：重新執行 1–2 部分的定義，再 model.load_state_dict(torch.load("cfg_unet.pt"))

# %% [markdown]
# ## 3. 取樣：classifier-free guidance（CFG）
# 每一步都讓模型預測兩次雜訊：**有給類別**（ε_cond）和**沒給類別**（ε_uncond），再混合：
#
# **ε ＝ ε_uncond ＋ w ·（ε_cond − ε_uncond）**
#
# 讀作：「從『沒條件的猜測』出發，朝『有條件比沒條件多出來的方向』走 w 倍」。
# w ＝ 0 → 完全不看類別；w ＝ 1 → 一般的條件模型；w ＞ 1 → 刻意放大類別的影響。
#
# 取樣迴圈本身和 D3-3 一樣（從純雜訊 x_T 走 T 步回到 x₀）；兩次預測合成一批一起算，速度只慢不到一倍。

# %%
@torch.no_grad()
def sample(labels, w, seed=0):
    model.eval()
    g = torch.Generator(device=device).manual_seed(seed)
    n = len(labels)
    y_c = torch.as_tensor(labels, device=device)
    y_u = torch.full_like(y_c, NULL)
    x = torch.randn(n, 1, 32, 32, device=device, generator=g)          # x_T：純雜訊
    for t in reversed(range(T)):
        tt = torch.full((n,), t, device=device)
        with torch.autocast(device_type=device, dtype=torch.float16, enabled=use_amp):
            out = model(torch.cat([x, x]), torch.cat([tt, tt]), torch.cat([y_c, y_u])).float()
        eps_c, eps_u = out[:n], out[n:]
        # >>> TODO: CFG 那一行——用 eps_u、eps_c、w 算出混合後的 eps
        eps = eps_u + w * (eps_c - eps_u)
        # <<< TODO
        # D3-3 的一步去噪：減掉預測的雜訊，再加一點新雜訊（最後一步不加）
        x = (x - betas[t] / (1 - abar[t]).sqrt() * eps) / alphas[t].sqrt()
        if t > 0:
            x = x + betas[t].sqrt() * torch.randn(x.shape, device=device, generator=g)
    return x.clamp(-1, 1)

def show_grid(imgs, nrow, title=None, ax=None):
    imgs = (imgs.cpu() + 1) / 2
    n = imgs.shape[0]; ncol = math.ceil(n / nrow)
    canvas = torch.ones(nrow * 34, ncol * 34)
    for i in range(n):
        r, c = divmod(i, ncol)
        canvas[r*34+1:r*34+33, c*34+1:c*34+33] = imgs[i, 0]
    ax = ax or plt.gca()
    ax.imshow(canvas, cmap="gray", vmin=0, vmax=1); ax.axis("off")
    if title: ax.set_title(title)

# 先試一個：指定「運動鞋」（類別 7），w ＝ 3
K = 7
t0 = time.time()
x = sample([K] * 8, w=3, seed=SEED)
print(f"8 張「{CLASSES[K]}」，{T} 步，{time.time()-t0:.1f}s")
plt.figure(figsize=(8, 1.4)); show_grid(x, 1, f"指定第 {K} 類（{CLASSES[K]}），w = 3，seed {SEED}"); plt.show()

# %% [markdown]
# ### 指導強度 w 的網格
# 每一列是一個類別，每一個 w 用**同樣的起始雜訊**（同一個 seed），只差 w。先猜：w 越大，同一列的 8 張會越像還是越不像？

# %%
labels = [k for k in range(10) for _ in range(8)]
fig, axes = plt.subplots(1, len(W_LIST), figsize=(4 * len(W_LIST), 5.2))
grids, t0 = {}, time.time()
for ax, w in zip(axes, W_LIST):
    grids[w] = sample(labels, w, seed=SEED)
    show_grid(grids[w], 10, f"w = {w}", ax)
print(f"4 個 w × 80 張，共 {time.time()-t0:.0f}s")
plt.tight_layout(); plt.savefig("cfg_scale_grid.png", dpi=120); plt.show()

# %% [markdown]
# ## 4. 量測：忠實度、多樣性、FID／KID
# 1. **忠實度**：先在真實圖上訓練一個小分類器（D1-3 的 CNN 寫法），再看它把生成圖認成「指定的類別」的比例
# 2. **多樣性**：同一類生成圖兩兩之間的平均距離（D3-1 量 mode collapse 用的同一把尺）
# 3. **FID／KID**：把真實圖和生成圖都丟進分類器，取倒數第二層的 128 維特徵（用真實圖的平均、標準差標準化），比較兩團點雲有多遠
#    （論文的 FID 用 Inception 網路的特徵；我們用自己的分類器，數字**不能**和論文比，只能在同一本筆記本裡互相比）

# %%
class Clf(nn.Module):
    def __init__(self):
        super().__init__()
        self.f = nn.Sequential(nn.Conv2d(1, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
                               nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
                               nn.Flatten(), nn.Linear(64 * 8 * 8, 128), nn.ReLU())
        self.head = nn.Linear(128, 10)
    def forward(self, x):
        return self.head(self.f(x))

clf = Clf().to(device)
copt = torch.optim.Adam(clf.parameters(), lr=1e-3)
for ep in range(2):
    clf.train()
    for xb, yb in loader:
        xb, yb = xb.to(device), yb.to(device)
        l = F.cross_entropy(clf(xb), yb); copt.zero_grad(); l.backward(); copt.step()
clf.eval()
test_loader = DataLoader(test_ds, batch_size=500)
with torch.no_grad():
    acc = np.mean([(clf(xb.to(device)).argmax(1).cpu() == yb).float().mean().item() for xb, yb in test_loader])
print(f"分類器在真實測試圖的準確率 {acc:.1%}（這是忠實度的天花板參考）")

# %%
def mean_pairwise(x):
    """同一批圖兩兩之間的平均歐氏距離（D3-1 的多樣性指標）"""
    f = x.flatten(1)
    d = torch.cdist(f, f)
    n = f.shape[0]
    return (d.sum() / (n * (n - 1))).item()

@torch.no_grad()
def raw_feats(x):
    return torch.cat([clf.f(x[i:i+500].to(device)).cpu() for i in range(0, len(x), 500)]).double().numpy()

def feats(x):
    """128 維特徵，用真實圖的平均與標準差標準化（每一維都變成「幾個標準差」）"""
    return (raw_feats(x) - F_MU) / F_SD

def fid(a, b):
    """兩團點雲的 Fréchet 距離：平均值差多少 ＋ 散佈形狀差多少"""
    from scipy import linalg
    mu1, mu2 = a.mean(0), b.mean(0)
    s1, s2 = np.cov(a, rowvar=False), np.cov(b, rowvar=False)
    covmean = linalg.sqrtm(s1 @ s2).real
    return float(((mu1 - mu2) ** 2).sum() + np.trace(s1 + s2 - 2 * covmean))

def kid(a, b, n_sub=10, size=100, seed=0):
    """KID：多次抽小樣本算 MMD（多項式核）再平均；小樣本時比 FID 穩"""
    rng = np.random.default_rng(seed); d = a.shape[1]; vals = []
    for _ in range(n_sub):
        x = a[rng.choice(len(a), size, replace=False)]; y = b[rng.choice(len(b), size, replace=False)]
        k = lambda p, q: (p @ q.T / d + 1) ** 3
        kxx, kyy, kxy = k(x, x), k(y, y), k(x, y)
        m = size
        vals.append((kxx.sum() - np.trace(kxx)) / (m * (m - 1)) + (kyy.sum() - np.trace(kyy)) / (m * (m - 1)) - 2 * kxy.mean())
    return float(np.mean(vals))

# 真實參考：測試集每類取 N_PER_CLASS 張
ty = test_ds.targets
real = torch.stack([test_ds[i][0] for k in range(10) for i in (ty == k).nonzero().flatten()[:N_PER_CLASS].tolist()])
real_y = torch.arange(10).repeat_interleave(N_PER_CLASS)
f_raw = raw_feats(real)
F_MU, F_SD = f_raw.mean(0), f_raw.std(0) + 1e-6
f_real = feats(real)
div_real = np.mean([mean_pairwise(real[real_y == k]) for k in range(10)])
print(f"真實圖：每類 {N_PER_CLASS} 張 | 同類兩兩距離 {div_real:.2f}")

# %%
rows, t0 = [], time.time()
eval_labels = torch.arange(10).repeat_interleave(N_PER_CLASS).tolist()
for w in W_LIST:
    gen = torch.cat([sample(eval_labels[i:i+500], w, seed=SEED + 1 + i) for i in range(0, len(eval_labels), 500)]).cpu()
    with torch.no_grad():
        pred = torch.cat([clf(gen[i:i+500].to(device)).argmax(1).cpu() for i in range(0, len(gen), 500)])
    faithful = (pred == torch.tensor(eval_labels)).float().mean().item()
    div = np.mean([mean_pairwise(gen[torch.tensor(eval_labels) == k]) for k in range(10)])
    f_gen = feats(gen)
    rows.append((w, faithful, div, fid(f_real, f_gen), kid(f_real, f_gen, size=min(100, len(gen) // 2))))
    print(f"w={w}: 忠實度 {faithful:.1%} | 同類距離 {div:.2f} | FID {rows[-1][3]:.2f} | KID {rows[-1][4]:.4f} | 累計 {time.time()-t0:.0f}s")

print(f"\n{'w':>3} | {'忠實度':>6} | {'同類距離':>6} | {'FID(特徵)':>9} | {'KID(特徵)':>9}")
for w, a_, d_, f_, k_ in rows:
    print(f"{w:>3} | {a_:>7.1%} | {d_:>8.2f} | {f_:>9.2f} | {k_:>9.4f}")
print(f"真實 | {acc:>7.1%} | {div_real:>8.2f} |      0.00 |    0.0000")

# %%
fig, ax1 = plt.subplots(figsize=(6, 3.2))
ws = [r[0] for r in rows]
ax1.plot(ws, [r[1] * 100 for r in rows], "o-", color="#0b6bcb", label="忠實度（%）")
ax1.set_xlabel("指導強度 w"); ax1.set_ylabel("忠實度（%）", color="#0b6bcb")
ax2 = ax1.twinx()
ax2.plot(ws, [r[2] for r in rows], "s--", color="#d9480f", label="同類兩兩距離")
ax2.axhline(div_real, color="#d9480f", lw=0.8, ls=":"); ax2.set_ylabel("同類兩兩距離（多樣性）", color="#d9480f")
plt.title("w 越大：越像指定類別，但同類越不多樣"); fig.tight_layout(); plt.savefig("cfg_tradeoff.png", dpi=120); plt.show()

# %% [markdown]
# ## 5. 延伸（選做）
# 1. 把 `P_UNCOND` 改成 0（永遠給標籤）重新訓練：w ＝ 3 還能用嗎？為什麼？（提示：ε_uncond 從來沒學過）
# 2. 只生成少數類別（例如「襯衫」，類別 6），把生成圖加進一個只有 50 張真實襯衫的訓練集，分類器對襯衫的召回率有沒有變好？用**真實**測試圖驗收。
