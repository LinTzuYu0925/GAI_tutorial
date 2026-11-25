# Source of lab16-bakeoff(.ipynb / -solution.ipynb). Build: python -X utf8 scripts/py2nb.py <this file>

# %% [markdown]
# # Lab L4-4：GAN 還是擴散？同一張照片、三種方法的比賽（D4-4）
#
# **需求單 #D4-4**（虛構公司：曜嶼電子，技術長室）：季節性產品照編修要定一個公司標準——GAN 還是擴散？能不能接近即時？
#
# | 部分 | 做什麼 | 輸出 |
# |---|---|---|
# | 0 | 一張「夏天」的產品照（SD1.5 ＋ LCM-LoRA 4 步生成，當作現有照片） | 原圖 |
# | 1 | 同一個任務「改成冬天」：CycleGAN（GAN）、InstructPix2Pix（擴散，用文字指令）、SD1.5 img2img ＋ LCM-LoRA（擴散，4 步） | 三張結果、每張秒數、VRAM |
# | 2 | 2D 玩具：flow matching 為什麼走直線、步數可以很少（CPU） | 軌跡圖、1／2／10 步的結果 |
# | 3 | 比較表：品質（你的評分）、速度、穩定性（換 seed）、可控性、授權 | 備忘錄要用的表 |
#
# 執行階段：**T4 GPU**（第 2 部分在 CPU 也能跑）。

# %%
# 第 1 格：環境
%pip install -q -U diffusers transformers accelerate peft
import torch, time, platform, gc, urllib.request, os
import numpy as np
import matplotlib.pyplot as plt
import torch.nn as nn
from PIL import Image
import diffusers
import glob, subprocess
from matplotlib import font_manager
# Colab 預設沒有中文字型：安裝 Noto CJK，否則圖上的中文會變成方框（D1-2 同樣做法）
NOTO = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
if not glob.glob(NOTO) and platform.system() == "Linux":
    subprocess.run("apt-get -qq install -y fonts-noto-cjk > /dev/null", shell=True)
for f in glob.glob(NOTO):
    font_manager.fontManager.addfont(f)
    plt.rcParams["font.family"] = font_manager.FontProperties(fname=f).get_name()
print("torch", torch.__version__, "| diffusers", diffusers.__version__, "| python", platform.python_version())
device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32
if device == "cuda":
    free, total = torch.cuda.mem_get_info()
    print("GPU:", torch.cuda.get_device_name(0), f"| 可用 VRAM {free/1e9:.1f} / {total/1e9:.1f} GB")
SEED = 0
RESULTS = {}   # 方法 → {"秒": …, "VRAM": …}

def timed(fn, n=3):
    """先暖機一次（第一次含載入、編譯），再量 n 次取平均；GPU 要同步才量得準"""
    fn()
    if device == "cuda":
        torch.cuda.synchronize(); torch.cuda.reset_peak_memory_stats()
    t0 = time.time()
    for _ in range(n):
        out = fn()
    if device == "cuda":
        torch.cuda.synchronize()
    sec = (time.time() - t0) / n
    vram = torch.cuda.max_memory_allocated() / 1e9 if device == "cuda" else float("nan")
    return out, sec, vram

def free_gpu(*objs):
    for o in objs:
        del o
    gc.collect()
    if device == "cuda":
        torch.cuda.empty_cache()

# %% [markdown]
# ## 0. 一張夏天的產品照
# 用 SD1.5 ＋ LCM-LoRA（D4-3 學過的 LoRA；這一個學的是「4 步就畫完」）生成，當作行銷部現有的照片。

# %%
from diffusers import StableDiffusionPipeline, LCMScheduler
MODEL = "stable-diffusion-v1-5/stable-diffusion-v1-5"
sd = StableDiffusionPipeline.from_pretrained(MODEL, torch_dtype=dtype, safety_checker=None).to(device)
sd.scheduler = LCMScheduler.from_config(sd.scheduler.config)
sd.load_lora_weights("latent-consistency/lcm-lora-sdv1-5")
sd.set_progress_bar_config(disable=True)
SUMMER = "product photo of white wireless earbuds with charging case on a wooden table outdoors, green trees, bright summer sunlight"
photo = sd(SUMMER, num_inference_steps=4, guidance_scale=1.0, generator=torch.Generator(device).manual_seed(SEED)).images[0]
photo.save("summer.png")
plt.figure(figsize=(4, 4)); plt.imshow(photo); plt.axis("off"); plt.title("原圖（夏天）"); plt.show()

# %% [markdown]
# ## 1. 同一個任務：「改成冬天」
# ### 1a. SD1.5 img2img ＋ LCM-LoRA（擴散，蒸餾成 4 步）
# D4-2 的 img2img，但用 LCM-LoRA：`guidance_scale=1.0`（LCM 不用 CFG）、4 步。

# %%
from diffusers import StableDiffusionImg2ImgPipeline
lcm_i2i = StableDiffusionImg2ImgPipeline(**sd.components)
WINTER_PROMPT = "product photo of white wireless earbuds with charging case on a wooden table outdoors, snowy winter, snow on trees, cold light"
def run_lcm(seed=SEED):
    return lcm_i2i(WINTER_PROMPT, image=photo, strength=0.6, num_inference_steps=4, guidance_scale=1.0,
                   generator=torch.Generator(device).manual_seed(seed)).images[0]
out_lcm, sec, vr = timed(run_lcm)
RESULTS["SD1.5＋LCM-LoRA（4 步）"] = {"秒": sec, "VRAM": vr}
print(f"LCM img2img：{sec:.2f} 秒／張 | VRAM 峰值 {vr:.2f} GB")
lcm_seeds = [run_lcm(s) for s in [1, 2]]          # 穩定性：換 seed 看變化
free_gpu(lcm_i2i, sd); del lcm_i2i, sd

# %% [markdown]
# ### 1b. InstructPix2Pix（擴散，直接下文字指令）
# 輸入一張圖＋一句「指令」：make it winter。有兩個指導強度：文字的（`guidance_scale`）和原圖的（`image_guidance_scale`，越大越像原圖）。

# %%
from diffusers import StableDiffusionInstructPix2PixPipeline
ip2p = StableDiffusionInstructPix2PixPipeline.from_pretrained("timbrooks/instruct-pix2pix", torch_dtype=dtype, safety_checker=None).to(device)
ip2p.set_progress_bar_config(disable=True)
def run_ip2p(seed=SEED):
    return ip2p("make it winter, with snow", image=photo, num_inference_steps=20, guidance_scale=7.5,
                image_guidance_scale=1.5, generator=torch.Generator(device).manual_seed(seed)).images[0]
out_ip2p, sec, vr = timed(run_ip2p)
RESULTS["InstructPix2Pix（20 步）"] = {"秒": sec, "VRAM": vr}
print(f"InstructPix2Pix：{sec:.2f} 秒／張 | VRAM 峰值 {vr:.2f} GB")
ip2p_seeds = [run_ip2p(s) for s in [1, 2]]
free_gpu(ip2p); del ip2p

# %% [markdown]
# ### 1c. CycleGAN（GAN，一次前向就完成）
# 官方預訓練的 `summer2winter_yosemite`（優勝美地國家公園的夏天 ↔ 冬天風景照，不成對訓練，D3-2 學過）。
# 生成器是 D3-2 那種殘差區塊結構（這裡是原始尺寸：9 個殘差區塊）。**沒有提示詞、沒有 seed**：同一張圖永遠得到同一個結果。

# %%
class ResBlock(nn.Module):
    def __init__(self, c):
        super().__init__()
        self.conv_block = nn.Sequential(nn.ReflectionPad2d(1), nn.Conv2d(c, c, 3), nn.InstanceNorm2d(c), nn.ReLU(True),
                                        nn.ReflectionPad2d(1), nn.Conv2d(c, c, 3), nn.InstanceNorm2d(c))
    def forward(self, x):
        return x + self.conv_block(x)

class ResnetGenerator(nn.Module):
    """和官方 pytorch-CycleGAN-and-pix2pix 的 resnet_9blocks 同樣的層與名稱，才能直接載入權重"""
    def __init__(self, ngf=64, n_blocks=9):
        super().__init__()
        m = [nn.ReflectionPad2d(3), nn.Conv2d(3, ngf, 7), nn.InstanceNorm2d(ngf), nn.ReLU(True)]
        for i in range(2):
            m += [nn.Conv2d(ngf * 2**i, ngf * 2**(i+1), 3, stride=2, padding=1), nn.InstanceNorm2d(ngf * 2**(i+1)), nn.ReLU(True)]
        m += [ResBlock(ngf * 4) for _ in range(n_blocks)]
        for i in range(2):
            c = ngf * 2**(2 - i)
            m += [nn.ConvTranspose2d(c, c // 2, 3, stride=2, padding=1, output_padding=1), nn.InstanceNorm2d(c // 2), nn.ReLU(True)]
        m += [nn.ReflectionPad2d(3), nn.Conv2d(ngf, 3, 7), nn.Tanh()]
        self.model = nn.Sequential(*m)
    def forward(self, x):
        return self.model(x)

URL = "http://efrosgans.eecs.berkeley.edu/cyclegan/pretrained_models/summer2winter_yosemite.pth"
if not os.path.exists("summer2winter.pth"):
    urllib.request.urlretrieve(URL, "summer2winter.pth")
G = ResnetGenerator().to(device).eval()
sd_gan = torch.load("summer2winter.pth", map_location=device)
# 2018 年的檔案多存了 InstanceNorm 的統計量（現在的 PyTorch 不用）；官方程式載入時也是把它們丟掉
sd_gan = {k: v for k, v in sd_gan.items() if not k.endswith(("running_mean", "running_var", "num_batches_tracked"))}
G.load_state_dict(sd_gan)
print(f"CycleGAN 生成器參數 {sum(p.numel() for p in G.parameters())/1e6:.1f}M（SD1.5 的 U-Net 約 860M）")

x = torch.from_numpy(np.asarray(photo.resize((512, 512)))).permute(2, 0, 1)[None].float().to(device) / 127.5 - 1
@torch.no_grad()
def run_gan():
    return G(x)
y, sec, vr = timed(run_gan, n=10)
out_gan = Image.fromarray(((y[0].permute(1, 2, 0).cpu().numpy() + 1) * 127.5).clip(0, 255).astype(np.uint8))
RESULTS["CycleGAN（1 次前向）"] = {"秒": sec, "VRAM": vr}
print(f"CycleGAN：{sec*1000:.1f} 毫秒／張 | VRAM 峰值 {vr:.2f} GB")

# %%
fig, axes = plt.subplots(1, 4, figsize=(16, 4.4))
for ax, im, t in zip(axes, [photo, out_gan, out_ip2p, out_lcm],
                     ["原圖（夏天）", "A：CycleGAN", "B：InstructPix2Pix", "C：SD1.5＋LCM-LoRA"]):
    ax.imshow(im); ax.set_title(t); ax.axis("off")
plt.tight_layout(); plt.savefig("bakeoff.png", dpi=100); plt.show()

fig, axes = plt.subplots(2, 3, figsize=(10, 7))
for j, (im, t) in enumerate(zip([out_ip2p] + ip2p_seeds, ["seed 0", "seed 1", "seed 2"])):
    axes[0, j].imshow(im); axes[0, j].set_title("InstructPix2Pix " + t, fontsize=9); axes[0, j].axis("off")
for j, (im, t) in enumerate(zip([out_lcm] + lcm_seeds, ["seed 0", "seed 1", "seed 2"])):
    axes[1, j].imshow(im); axes[1, j].set_title("LCM " + t, fontsize=9); axes[1, j].axis("off")
plt.tight_layout(); plt.savefig("bakeoff_seeds.png", dpi=90); plt.show()

# %% [markdown]
# **先別看別人的答案**：在投影片「練習：幫三張冬天照打分數」填你自己的分數（1～5），再往下。

# %% [markdown]
# ## 2. 2D 玩具：flow matching 為什麼可以很少步
# 從標準常態分布（雜訊）的點 x₀，走到「兩個月亮」形狀的資料點 x₁。
#
# **flow matching** 的訓練：隨機取 t（0～1），站在直線上的點 x_t ＝ (1 − t)·x₀ ＋ t·x₁，
# 讓網路學「速度」v ＝ x₁ − x₀（往資料點的直線方向）。生成時從雜訊出發，沿著網路給的速度走幾步。
#
# 和 D3-3 的 DDPM 是同一家族：都是「學會從雜訊走到資料」；差別在訓練路線設計成直線。
#
# **先猜再看**：每一條訓練路線都是直線，學出來的軌跡也會是直線嗎？1 步能不能畫出兩個月亮？
# （提示：同一個 x_t 可能在很多條直線上，網路學到的是它們的**平均**方向。）

# %%
from sklearn.datasets import make_moons
torch.manual_seed(SEED)
data = torch.tensor(make_moons(4000, noise=0.05, random_state=SEED)[0], dtype=torch.float32)
data = (data - data.mean(0)) / data.std(0)
vnet = nn.Sequential(nn.Linear(3, 128), nn.SiLU(), nn.Linear(128, 128), nn.SiLU(), nn.Linear(128, 2))
opt = torch.optim.Adam(vnet.parameters(), lr=2e-3)
t0 = time.time()
for step in range(3000):
    x1 = data[torch.randint(0, len(data), (256,))]
    x0 = torch.randn_like(x1)
    t = torch.rand(256, 1)
    # >>> TODO: flow matching 的一步——直線上的點 xt、目標速度 target，損失是 MSE
    xt = (1 - t) * x0 + t * x1
    target = x1 - x0
    loss = ((vnet(torch.cat([xt, t], 1)) - target) ** 2).mean()
    # <<< TODO
    opt.zero_grad(); loss.backward(); opt.step()
print(f"訓練 3000 步（CPU）{time.time()-t0:.0f}s | 最後 loss {loss.item():.3f}")

@torch.no_grad()
def euler(n_steps, n=1000, seed=1, keep_path=False):
    g = torch.Generator().manual_seed(seed)
    x = torch.randn(n, 2, generator=g); path = [x]
    for k in range(n_steps):
        t = torch.full((n, 1), k / n_steps)
        x = x + vnet(torch.cat([x, t], 1)) / n_steps      # 沿速度走一小步
        path.append(x)
    return (x, torch.stack(path)) if keep_path else x

fig, axes = plt.subplots(1, 4, figsize=(16, 4))
_, path = euler(20, n=60, keep_path=True)
axes[0].scatter(data[:, 0], data[:, 1], s=2, c="#bbb")
for i in range(60):
    axes[0].plot(path[:, i, 0], path[:, i, 1], lw=0.8, c="#0b6bcb")
axes[0].scatter(path[0, :, 0], path[0, :, 1], s=8, c="k", label="起點（雜訊）"); axes[0].legend(fontsize=8)
axes[0].set_title("20 步的軌跡")
for ax, k in zip(axes[1:], [1, 2, 10]):
    s = euler(k)
    ax.scatter(data[:, 0], data[:, 1], s=2, c="#ddd"); ax.scatter(s[:, 0], s[:, 1], s=3, c="#d9480f")
    ax.set_title(f"{k} 步生成")
for ax in axes:
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_aspect("equal")
plt.tight_layout(); plt.savefig("flow_toy.png", dpi=100); plt.show()

# %% [markdown]
# **觀察**：軌跡是彎的，1 步只會走到中間（所有方向的平均）。把彎路再「拉直」一次（rectified flow，投影片附錄）、
# 或把多步的老師蒸餾成少步的學生（LCM，第 1a 部分），才能 1～4 步就畫好。
#
# ## 3. 比較表（備忘錄的骨架）
# 速度與 VRAM 是量出來的；品質請填你自己的評分（投影片練習頁），可控性與授權照投影片的表。

# %%
print(f"{'方法':26s} | {'秒／張':>8s} | {'VRAM 峰值':>9s}")
for k, v in RESULTS.items():
    print(f"{k:26s} | {v['秒']:8.3f} | {v['VRAM']:7.2f} GB")
print("\n穩定性：換 seed 結果會變嗎？CycleGAN 沒有 seed（同一張圖永遠同一個結果）；兩個擴散方法看上面的 seed 網格。")
