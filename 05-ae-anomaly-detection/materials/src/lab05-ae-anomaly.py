# Source of lab05-ae-anomaly(.ipynb / -solution.ipynb). Build: python -X utf8 scripts/py2nb.py <this file>

# %% [markdown]
# # Lab L2-1：只看過良品的自編碼器，找出沒看過的瑕疵（D2-1）
#
# **需求單 #D2-1**（虛構公司：曜嶼電子，製造品保部 A 線）：AOI 過殺太高、新瑕疵又漏檢，而且瑕疵樣本幾乎沒有。
# 公司的影像用公開資料集 **VisA 的 PCB1 類別**代替（授權 CC BY 4.0，待確認）。
#
# | 步驟 | 做什麼 | 輸出 |
# |---|---|---|
# | 1 | 下載並切分資料：訓練集**只有良品** | train／val／test 張數 |
# | 2 | 卷積自編碼器 `ConvAE` | 每一塊的 shape |
# | 3 | 訓練（重用 D1-3 的迴圈、D1-4 的檢查點） | loss 曲線、重建網格 |
# | 4 | 誤差圖 → 分數 → 直方圖、AUROC | 熱力圖、AUROC |
# | 5 | 門檻：驗證集上漏檢 ≤ 5% | 測試集的過殺率、漏檢率 |
# | 6 | Gradio 檢測站（第二天的交付） | 網頁 |
#
# > 狀態：本筆記本尚未在 Colab T4 實跑。VisA 網址、壓縮檔結構與張數已於 2026-11-24 確認（見 `research/sources.md`）。

# %%
# 第 1 格：環境
%pip install -q -U gradio scikit-learn
import torch, os, glob, random, platform, time
print("torch", torch.__version__, "| python", platform.python_version())
device = "cuda" if torch.cuda.is_available() else "cpu"
if device == "cuda":
    free, total = torch.cuda.mem_get_info()
    print("GPU:", torch.cuda.get_device_name(0), f"| 可用 VRAM {free/1e9:.1f} / {total/1e9:.1f} GB")
SEED = 0
random.seed(SEED); torch.manual_seed(SEED)
SIZE = 128          # 沒有 GPU：改成 64
EPOCHS = 30         # 沒有 GPU：改成 3

# %% [markdown]
# ## 1. 資料：VisA PCB1
# 預設從官方網址下載整包 VisA（約 1.9 GB，下載時間待實測），只解壓 `pcb1`（良品 1004 張、不良品 100 張）。
# 講師若已經把 PCB1 放到雲端硬碟，把 `PCB1_DIR` 改成那個資料夾即可跳過下載。

# %%
VISA_URL = "https://amazon-visual-anomaly.s3.us-west-2.amazonaws.com/VisA_20220922.tar"  # 約 1.9 GB（2026-11-24 確認）
CATEGORY = "pcb1"        # 回家作業：換成 VisA 的其他類別，例如 "pcb2"、"capsules"
PCB1_DIR = f"visa/{CATEGORY}"   # 或講師提供的路徑，例如 /content/drive/MyDrive/GAI/visa/pcb1

if not os.path.isdir(PCB1_DIR):
    os.makedirs("visa", exist_ok=True)
    if not os.path.exists("visa/VisA.tar"):
        os.system(f"wget -q -O visa/VisA.tar {VISA_URL}")
    os.system(f"tar -xf visa/VisA.tar -C visa --wildcards '{CATEGORY}/*'")
normal = sorted(glob.glob(f"{PCB1_DIR}/**/Normal/*.*", recursive=True))
anomaly = sorted(glob.glob(f"{PCB1_DIR}/**/Anomaly/*.*", recursive=True))
anomaly = [p for p in anomaly if "/Masks/" not in p.replace("\\", "/")]
print("良品", len(normal), "張；不良品", len(anomaly), "張")

# %% [markdown]
# **切分**：訓練集只放良品（模型永遠沒看過瑕疵）。驗證集用來選門檻，測試集只在最後算一次成績。

# %%
random.shuffle(normal); random.shuffle(anomaly)
n70, n85 = int(len(normal) * 0.70), int(len(normal) * 0.85)
a50 = len(anomaly) // 2
split = {
    "train": [(p, 0) for p in normal[:n70]],
    "val":   [(p, 0) for p in normal[n70:n85]] + [(p, 1) for p in anomaly[:a50]],
    "test":  [(p, 0) for p in normal[n85:]] + [(p, 1) for p in anomaly[a50:]],
}
for k, v in split.items():
    print(f"{k:5s} 良品 {sum(1 for _, y in v if y == 0):4d}  不良 {sum(1 for _, y in v if y == 1):4d}")

# %%
from PIL import Image
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader

tf = transforms.Compose([transforms.Resize((SIZE, SIZE)), transforms.ToTensor()])   # 範圍 0–1

class PCBDataset(Dataset):
    """一次讀進記憶體（縮小後很小），之後每個 epoch 不用再讀硬碟。"""
    def __init__(self, items):
        self.x = torch.stack([tf(Image.open(p).convert("RGB")) for p, _ in items])
        self.y = torch.tensor([y for _, y in items])
        self.paths = [p for p, _ in items]
    def __len__(self):
        return len(self.y)
    def __getitem__(self, i):
        return self.x[i], self.y[i]

t0 = time.time()
ds = {k: PCBDataset(v) for k, v in split.items()}
print("讀取並縮小完成", f"{time.time()-t0:.0f}s", "| 一張圖", tuple(ds["train"][0][0].shape))

# 資料陷阱：VisA PCB1 的良品約八成是「倒過來」拍的（針腳朝上），不良品幾乎都是正的（講師本機檢查，2026-11-24）。
# 不處理的話，模型可能學到「方向不對＝瑕疵」，AUROC 會好看得不真實。
# 解法：訓練集加入旋轉 180° 的版本，兩種方向都算「正常」。
ds["train"].x = torch.cat([ds["train"].x, ds["train"].x.flip(-2, -1)])
ds["train"].y = torch.cat([ds["train"].y, ds["train"].y])
print("加入 180° 旋轉後，訓練良品", len(ds["train"]), "張")
train_loader = DataLoader(ds["train"], batch_size=32, shuffle=True)

# %% [markdown]
# ## 2. 模型：卷積自編碼器
# 編碼器每一層把高寬減半；解碼器用 `ConvTranspose2d` 每一層放大兩倍。
# **先別執行**：在投影片「練習：每一塊的輸入與輸出」寫下預測。

# %%
import torch.nn as nn

def down(cin, cout):   # 高寬減半
    return nn.Sequential(nn.Conv2d(cin, cout, 4, stride=2, padding=1), nn.BatchNorm2d(cout), nn.LeakyReLU(0.2))

def up(cin, cout):     # 高寬加倍
    return nn.Sequential(nn.ConvTranspose2d(cin, cout, 4, stride=2, padding=1), nn.BatchNorm2d(cout), nn.ReLU())

class ConvAE(nn.Module):
    def __init__(self):
        super().__init__()
        # >>> TODO: encoder：3→32→64→128→128（四次 down）；decoder：128→128→64→32（三次 up），最後一層 ConvTranspose2d(32, 3) 接 Sigmoid
        self.encoder = nn.Sequential(down(3, 32), down(32, 64), down(64, 128), down(128, 128))
        self.decoder = nn.Sequential(up(128, 128), up(128, 64), up(64, 32),
                                     nn.ConvTranspose2d(32, 3, 4, stride=2, padding=1), nn.Sigmoid())
        # <<< TODO

    def forward(self, x):
        z = self.encoder(x)          # 瓶頸（bottleneck）
        return self.decoder(z)

model = ConvAE().to(device)
x = ds["train"].x[:8].to(device)
z = model.encoder(x)
print("x    ", tuple(x.shape))
print("z    ", tuple(z.shape), f"→ 壓縮成原本的 1/{x[0].numel() // z[0].numel()}")
print("x_hat", tuple(model(x).shape))

# %% [markdown]
# ## 3. 訓練：只用良品
# 損失＝重建誤差（MSE）。迴圈和 D1-3 一樣，只換了「模型」和「損失」；每個 epoch 存檢查點（D1-4）。

# %%
CKPT = "ae_pcb1.pt"            # 講師提供的檢查點也用這個檔名；放好就會直接載入、跳過訓練
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
loss_fn = nn.MSELoss()
history = []

if os.path.exists(CKPT):
    ck = torch.load(CKPT, map_location=device)
    model.load_state_dict(ck["model"]); history = ck.get("history", [])
    print("載入檢查點", CKPT, "（已訓練", len(history), "epochs）")
else:
    t0 = time.time()
    for epoch in range(1, EPOCHS + 1):
        model.train(); total = 0.0
        for xb, _ in train_loader:
            xb = xb.to(device)
            # >>> TODO: 五行：x_hat = model(xb)；loss = loss_fn(x_hat, xb)；zero_grad、backward、step
            x_hat = model(xb)
            loss = loss_fn(x_hat, xb)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            # <<< TODO
            total += loss.item() * len(xb)
        history.append(total / len(ds["train"]))
        torch.save({"model": model.state_dict(), "history": history}, CKPT)
        if epoch % 5 == 0 or epoch == 1:
            print(f"epoch {epoch:2d}  loss {history[-1]:.5f}  ({time.time()-t0:.0f}s)")

# %%
import matplotlib.pyplot as plt
plt.figure(figsize=(4, 2.5)); plt.plot(history); plt.xlabel("epoch"); plt.ylabel("MSE"); plt.title("train loss"); plt.show()

model.eval()
with torch.no_grad():
    xs = ds["test"].x[:8].to(device); xr = model(xs).cpu()
fig, ax = plt.subplots(2, 8, figsize=(14, 3.6))
for i in range(8):
    ax[0, i].imshow(xs[i].cpu().permute(1, 2, 0)); ax[0, i].axis("off")
    ax[1, i].imshow(xr[i].permute(1, 2, 0)); ax[1, i].axis("off")
ax[0, 0].set_title("input", loc="left"); ax[1, 0].set_title("reconstruction", loc="left")
plt.tight_layout(); plt.show()

# %% [markdown]
# ## 4. 誤差圖 → 分數
# - **誤差圖**：每個像素 (x − x̂)²，三個通道平均 → [B, H, W]
# - **分數**：誤差最大的 1% 像素的平均。瑕疵通常很小，整張平均會被大片正常區域稀釋。

# %%
@torch.no_grad()
def anomaly_map(x):
    model.eval()
    x = x.to(device)
    # >>> TODO: 回傳每個像素的平方誤差，三個通道平均，shape [B, H, W]
    return ((x - model(x)) ** 2).mean(dim=1)
    # <<< TODO

@torch.no_grad()
def score(x):
    m = anomaly_map(x).flatten(1)                    # [B, H*W]
    k = max(1, int(m.shape[1] * 0.01))
    return m.topk(k, dim=1).values.mean(dim=1).cpu()  # [B]

def scores_of(d):
    return torch.cat([score(d.x[i:i + 64]) for i in range(0, len(d), 64)]), d.y

s_val, y_val = scores_of(ds["val"])
s_test, y_test = scores_of(ds["test"])
print("驗證集分數：良品平均 %.5f｜不良平均 %.5f" % (s_val[y_val == 0].mean(), s_val[y_val == 1].mean()))

# %%
plt.figure(figsize=(6, 3))
plt.hist(s_val[y_val == 0], bins=30, alpha=0.6, label="good (val)")
plt.hist(s_val[y_val == 1], bins=30, alpha=0.6, label="defect (val)")
plt.xlabel("score"); plt.legend(); plt.title("score histogram"); plt.show()

# %% [markdown]
# **熱力圖**：測試集裡的 4 張不良品。

# %%
idx = [i for i in range(len(ds["test"])) if ds["test"].y[i] == 1][:4]
xa = ds["test"].x[idx]
maps = anomaly_map(xa).cpu()
with torch.no_grad():
    ra = model(xa.to(device)).cpu()
fig, ax = plt.subplots(3, 4, figsize=(10, 7.5))
for j in range(4):
    ax[0, j].imshow(xa[j].permute(1, 2, 0)); ax[1, j].imshow(ra[j].permute(1, 2, 0)); ax[2, j].imshow(maps[j], cmap="inferno")
    for r in range(3): ax[r, j].axis("off")
for r, t in enumerate(["input", "reconstruction", "error map"]):
    ax[r, 0].set_title(t, loc="left")
plt.tight_layout(); plt.savefig("heatmaps.png", dpi=120); plt.show()

# %% [markdown]
# ## 5. AUROC 與門檻
# - **AUROC**：不挑門檻，看「隨機一張不良品的分數高於隨機一張良品」的機率。
# - **門檻**：在**驗證集**上選，讓漏檢 ≤ 5%；再到**測試集**算一次過殺與漏檢。

# %%
from sklearn.metrics import roc_auc_score
print("AUROC（val） = %.3f" % roc_auc_score(y_val, s_val))
print("AUROC（test）= %.3f" % roc_auc_score(y_test, s_test))

TARGET_MISS = 0.05
# >>> TODO: 不良品分數由小到大排序；最多允許 k = floor(5% × 不良張數) 張漏檢；門檻設在第 k 個（從 0 數）分數的正下方
bad_sorted = s_val[y_val == 1].sort().values
k = int(TARGET_MISS * len(bad_sorted))
thr = bad_sorted[k].item() * (1 - 1e-6)
# <<< TODO

def rates(s, y, thr):
    pred_bad = s > thr
    overkill = (pred_bad & (y == 0)).sum().item() / (y == 0).sum().item()   # 過殺：良品判不良
    escape = (~pred_bad & (y == 1)).sum().item() / (y == 1).sum().item()    # 漏檢：不良判良品
    return overkill, escape

ok_v, es_v = rates(s_val, y_val, thr)
ok_t, es_t = rates(s_test, y_test, thr)
print(f"門檻 {thr:.5f}")
print(f"驗證集：過殺 {ok_v:.1%}  漏檢 {es_v:.1%}")
print(f"測試集：過殺 {ok_t:.1%}  漏檢 {es_t:.1%}   ← 這才是回報給品保部的數字")

# %% [markdown]
# ## 6. Ship：Gradio 檢測站

# %%
import gradio as gr
import numpy as np

def inspect(img):
    x = tf(img.convert("RGB")).unsqueeze(0)
    m = anomaly_map(x)[0].cpu().numpy()
    s = score(x).item()
    heat = (plt.cm.inferno(m / max(m.max(), 1e-8))[..., :3] * 255).astype(np.uint8)
    verdict = f"{'疑似不良' if s > thr else '良品'}（分數 {s:.5f}，門檻 {thr:.5f}）"
    return heat, verdict

demo = gr.Interface(
    fn=inspect,
    inputs=gr.Image(type="pil", label="上傳 PCB 影像"),
    outputs=[gr.Image(label="誤差熱力圖"), gr.Textbox(label="判定")],
    title="曜嶼電子（虛構）A 線瑕疵檢測站 · AE 基準版",
    description="只用良品訓練的卷積自編碼器。資料：VisA PCB1（CC BY 4.0）。",
)
demo.launch(share=True)
