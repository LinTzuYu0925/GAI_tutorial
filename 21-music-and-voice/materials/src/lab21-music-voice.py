# Source of lab21-music-voice(.ipynb / -solution.ipynb). Build: python -X utf8 scripts/py2nb.py <this file>

# %% [markdown]
# # Lab L6-1：活動影片的配樂與旁白（D6-1）
#
# **需求單 #D6-1**（虛構公司：曜嶼電子，行銷部）：活動影片需要免版稅配樂與國語旁白。
#
# | 部分 | 做什麼 | 輸出 |
# |---|---|---|
# | 1 | MusicGen-small：一句文字 → 5 秒配樂；波形與頻譜圖 | `jingle.wav`、圖 |
# | 2 | 聲音變 token：EnCodec 把配樂變成約 4 × 250 個整數（實跑 247 個時間點） | token 形狀 |
# | 3 | 提示詞掃描、長度掃描：生成時間和片長的關係 | 三段配樂、時間圖 |
# | 4 | 旁白：Kokoro 中文 TTS（Apache-2.0） | `voiceover.wav` |
# | 5 | 交付：配樂＋授權說明 | 一段文字 |
#
# 執行階段：**T4 GPU**（CPU 也能跑，但每 5 秒配樂要等約 20～30 秒）。
#
# ⚠️ **授權**：MusicGen 的權重是 **CC-BY-NC 4.0（非商用）**。今天的配樂只能用在課堂練習，**不能放進公司的正式廣告**。

# %%
# 第 1 格：環境
%pip install -q "kokoro>=0.9.4" "misaki[zh]>=0.9.4" soundfile
import time, platform, glob, subprocess
import numpy as np
import matplotlib.pyplot as plt
import torch, transformers, soundfile as sf
from IPython.display import Audio, display
from matplotlib import font_manager
NOTO = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
if not glob.glob(NOTO) and platform.system() == "Linux":
    subprocess.run("apt-get -qq install -y fonts-noto-cjk > /dev/null", shell=True)
for f in glob.glob(NOTO):
    font_manager.fontManager.addfont(f)
    plt.rcParams["font.family"] = font_manager.FontProperties(fname=f).get_name()
print("torch", torch.__version__, "| transformers", transformers.__version__, "| python", platform.python_version())
device = "cuda" if torch.cuda.is_available() else "cpu"
if device == "cuda":
    free, total = torch.cuda.mem_get_info()
    print("GPU:", torch.cuda.get_device_name(0), f"| 可用 VRAM {free/1e9:.1f} / {total/1e9:.1f} GB")
SEED = 0

# %% [markdown]
# ## 1. 一句文字 → 5 秒配樂
# MusicGen 每秒產生 50 個「時間點」，每個時間點 4 個 token。`max_new_tokens=250` ≈ 5 秒。

# %%
from transformers import AutoProcessor, MusicgenForConditionalGeneration
MG = "facebook/musicgen-small"            # 權重授權：CC-BY-NC 4.0（非商用）
proc = AutoProcessor.from_pretrained(MG)
mg = MusicgenForConditionalGeneration.from_pretrained(MG).to(device).eval()
SR = mg.config.audio_encoder.sampling_rate
print("取樣率（每秒幾個數字）：", SR)

def make_music(prompt, seconds=5, seed=SEED):
    torch.manual_seed(seed)
    inputs = proc(text=[prompt], padding=True, return_tensors="pt").to(device)
    t0 = time.time()
    with torch.no_grad():
        audio = mg.generate(**inputs, do_sample=True, guidance_scale=3.0, max_new_tokens=int(seconds * 50))
    if device == "cuda":
        torch.cuda.synchronize()
    return audio[0, 0].float().cpu().numpy(), time.time() - t0

PROMPT = "upbeat electronic jingle for a tech product launch, bright synth, 120 bpm"
wav, sec = make_music(PROMPT)
sf.write("jingle.wav", wav, SR)
print(f"{len(wav)/SR:.1f} 秒的配樂，生成花了 {sec:.1f} 秒；一共 {len(wav):,} 個數字")
display(Audio(wav, rate=SR))

# %%
# 聲音長什麼樣：波形（每個時間點的振幅）與頻譜圖（每個時間點有哪些頻率）
plt.rcParams.update({"font.size": 16, "axes.unicode_minus": False})
fig, ax = plt.subplots(2, 1, figsize=(9, 6.5))
t = np.arange(len(wav)) / SR
ax[0].plot(t, wav, lw=0.4, color="#2f5fd0"); ax[0].set_xlim(0, t[-1]); ax[0].set_ylabel("振幅"); ax[0].set_title("波形")
ax[1].specgram(wav, NFFT=1024, Fs=SR, noverlap=512, cmap="magma"); ax[1].set_ylabel("頻率（Hz）"); ax[1].set_xlabel("秒")
ax[1].set_title("頻譜圖（越亮＝那個頻率越大聲）")
plt.tight_layout(); plt.savefig("waveform_spectrogram.png", dpi=150); plt.show()

# %% [markdown]
# ## 2. 聲音變 token：EnCodec（D2-4 學過）
# 32,000 個數字／秒太多了。EnCodec 把每 20 毫秒壓成 4 個整數（4 本編碼簿，每本 2048 個碼）。
# MusicGen 的 Transformer 就是在「接」這種 token，和 D5-2 接文字是同一件事。

# %%
with torch.no_grad():
    x = torch.tensor(wav)[None, None].to(device)              # [batch, 聲道, 樣本數]
    enc = mg.audio_encoder.encode(x)
codes = enc.audio_codes                                       # [1 段, batch, 編碼簿數, 時間點]
print("audio_codes 形狀：", tuple(codes.shape))
print("第一個時間點的 4 個 token：", codes[0, 0, :, 0].tolist())

def tokens_per_second(n_codebooks, frame_rate):
    # >>> TODO: 每秒幾個 token＝編碼簿數 × 每秒幾個時間點
    return n_codebooks * frame_rate
    # <<< TODO

n_cb, n_frames = codes.shape[-2], codes.shape[-1]
frame_rate = round(n_frames / (len(wav) / SR))
print(f"每秒 {frame_rate} 個時間點 × {n_cb} 本編碼簿 ＝ 每秒 {tokens_per_second(n_cb, frame_rate)} 個 token")
print(f"30 秒的廣告配樂 ≈ {tokens_per_second(n_cb, frame_rate) * 30:,} 個 token（D5 一封客服回覆約 150 個）")

# %% [markdown]
# ## 3. 掃描：提示詞、長度
# 一次只改一件事：先固定長度換提示詞，再固定提示詞換長度。

# %%
PROMPTS = {
    "科技新品": "upbeat electronic jingle for a tech product launch, bright synth, 120 bpm",
    "溫馨家電": "warm acoustic guitar and soft piano, cozy home, gentle",
    "年終特賣": "energetic pop with drums and claps, festive sale, exciting",
}
clips = {}
for name, p in PROMPTS.items():
    clips[name], s = make_music(p, seconds=5)
    sf.write(f"jingle_{name}.wav", clips[name], SR)
    print(f"{name}：{s:.1f} 秒"); display(Audio(clips[name], rate=SR))

# %%
LENGTHS = [5, 10, 15]
gen_sec = []
for L in LENGTHS:
    _, s = make_music(PROMPT, seconds=L)
    gen_sec.append(s); print(f"片長 {L} 秒 → 生成 {s:.1f} 秒")
plt.figure(figsize=(5, 3.5)); plt.plot(LENGTHS, gen_sec, "o-")
plt.xlabel("片長（秒）"); plt.ylabel("生成時間（秒）"); plt.title(f"MusicGen-small（{device}）")
plt.tight_layout(); plt.savefig("length_vs_time.png", dpi=150); plt.show()

# %% [markdown]
# ## 4. 旁白：Kokoro 中文 TTS
# 文字 → 音素（注音）→ 聲學特徵 → 波形。Kokoro-82M-v1.1-zh：Apache-2.0、8,200 萬參數、CPU 也能跑。
# 它的中文聲音是大陸口音；台灣口音可以試 BreezyVoice（講師示範，安裝較複雜）。

# %%
VO = "曜嶼電子新品上市，藍牙耳機限時優惠，歡迎到官網選購。"
try:
    from kokoro import KPipeline
    tts = KPipeline(lang_code="z", repo_id="hexgrad/Kokoro-82M-v1.1-zh")
    t0 = time.time()
    parts = [a.numpy() if hasattr(a, "numpy") else a for _, ps, a in tts(VO, voice="zf_001")]
    vo = np.concatenate(parts)
    sf.write("voiceover.wav", vo, 24000)
    print(f"旁白 {len(vo)/24000:.1f} 秒，生成 {time.time()-t0:.1f} 秒")
    display(Audio(vo, rate=24000))
except Exception as e:
    print("TTS 沒有成功（套件版本或下載問題）：", type(e).__name__, e)
    import urllib.request
    os.makedirs("data/download", exist_ok=True)
    urllib.request.urlretrieve("https://raw.githubusercontent.com/LinTzuYu0925/GAI_tutorial/day6-done/21-music-and-voice/materials/data/voiceover.wav", "data/download/voiceover_instructor.wav")
    print("備案：改聽講師的旁白（Kokoro，講師本機生成）")
    display(Audio("data/download/voiceover_instructor.wav"))

# %% [markdown]
# ## 5. 交付：配樂＋授權說明
# 在下面寫三行，交給行銷部：
# 1. 你選哪一段配樂、用的提示詞
# 2. **授權**：MusicGen 權重 CC-BY-NC 4.0 → 只能內部試聽，不能用在公開廣告；正式版要換可商用的方案或買授權
# 3. **旁白**：用的是合成聲音；若要用真人（例如代言人）的聲音做聲音複製，必須有當事人書面同意
