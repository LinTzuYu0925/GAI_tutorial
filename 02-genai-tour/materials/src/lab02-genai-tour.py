# Source of lab02-genai-tour(.ipynb / -solution.ipynb). Build: python -X utf8 scripts/py2nb.py <this file>

# %% [markdown]
# # Lab L1-2：今晚就要文案和產品圖（D1-2）
#
# **需求單 #D1-2**（虛構公司：曜嶼電子，行銷部）：新款藍牙耳機今晚上架預告，需要三版文案（每版 ≤ 80 字）與一張 512×512 產品情境圖，而且**同樣設定要能重現同一張圖**。
#
# | Part | 做什麼 | 模型 |
# |---|---|---|
# | A | 用 `pipeline` 寫文案 | Qwen2.5-0.5B-Instruct（開放權重） |
# | B | 產生產品圖，固定 seed | SD1.5 ＋ LCM-LoRA（4 步） |
# | C | 呼叫一次雲端 LLM（沒有金鑰就跳過） | Gemini 免費方案（`google-genai` 套件） |
# | D | 打開黑盒子：下一個 token 的機率、溫度 | Part A 的模型 |
#
# **執行階段**：
# - Colab 網頁版：功能表「執行階段 → 變更執行階段類型 → T4 GPU」。
# - VS Code：右上角「Select Kernel → Colab → New Colab Server → GPU → T4」。
#
# 這本筆記本用的開放模型都放在 **Hugging Face Hub**（huggingface.co）：第一次執行時自動下載，不需要帳號或金鑰。

# %%
# 第 1 格：安裝套件並確認 GPU（transformers、diffusers 釘在 2026-11-26 T4 實跑的版本）
%pip install -q transformers==5.24.1 diffusers==0.43.0 accelerate peft google-genai python-dotenv  # 2026-11-26 T4 實跑版本
import torch, platform
print("torch", torch.__version__, "| python", platform.python_version())
if torch.cuda.is_available():
    free, total = torch.cuda.mem_get_info()
    print("GPU:", torch.cuda.get_device_name(0), f"| 可用 VRAM {free/1e9:.1f} / {total/1e9:.1f} GB")
else:
    print("沒有 GPU：Part A、D 可以在 CPU 跑（較慢）；Part B 請看解答筆記本的已存輸出")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32

# %% [markdown]
# ## Part A：三行程式寫文案
# `pipeline` 把「tokenizer → 模型 → 抽樣 → 解碼」包在一起。先把產品規格寫成一段文字（虛構規格）。

# %%
from transformers import pipeline

SPEC = "產品：曜嶼 Breeze 藍牙耳機（虛構）。特色：通勤降噪、續航 30 小時、10 分鐘快充可聽 2 小時、重量 5 公克。"
messages = [
    {"role": "system", "content": "你是曜嶼電子的行銷文案寫手，只用台灣繁體中文，不提其他品牌。"},
    {"role": "user", "content": SPEC + "請寫一段 80 字以內的上架文案。"},
]

# >>> TODO: 用 pipeline("text-generation") 載入 Qwen/Qwen2.5-0.5B-Instruct，dtype=DTYPE、device=DEVICE，存成 gen
gen = pipeline("text-generation", model="Qwen/Qwen2.5-0.5B-Instruct", dtype=DTYPE, device=DEVICE)
# <<< TODO

copies = []
for i in range(3):
    out = gen(messages, max_new_tokens=120, do_sample=True, temperature=0.8)
    text = out[0]["generated_text"][-1]["content"]
    copies.append(text)
    print(f"--- 第 {i+1} 版（{len(text)} 字）---\n{text}\n")

# %% [markdown]
# ## Part B：一張產品情境圖（固定 seed）
# SD1.5 原本要 25–50 步；載入 LCM-LoRA 後 4 步就能出圖。`generator` 的 seed 固定，圖就能重現。

# %%
from diffusers import DiffusionPipeline, LCMScheduler

pipe = DiffusionPipeline.from_pretrained("stable-diffusion-v1-5/stable-diffusion-v1-5", dtype=DTYPE).to(DEVICE)
pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
pipe.load_lora_weights("latent-consistency/lcm-lora-sdv1-5")

PROMPT = "product photo of minimalist white wireless earbuds on a wooden desk, morning light, commuter lifestyle, high detail"
NEG = "logo, text, watermark, brand name"
SEED = 42

# >>> TODO: 建立 torch.Generator(DEVICE).manual_seed(SEED)，用 4 步、guidance_scale=1.0 產生一張圖，存成 img
g = torch.Generator(DEVICE).manual_seed(SEED)
img = pipe(PROMPT, negative_prompt=NEG, num_inference_steps=4, guidance_scale=1.0, generator=g).images[0]
# <<< TODO

import os
os.makedirs("outputs", exist_ok=True)
img.save(f"outputs/product_seed{SEED}.png")
img

# %% [markdown]
# **可重現嗎？** 用同一個 seed 再產生一次，逐像素比較。

# %%
import numpy as np
g2 = torch.Generator(DEVICE).manual_seed(SEED)
img2 = pipe(PROMPT, negative_prompt=NEG, num_inference_steps=4, guidance_scale=1.0, generator=g2).images[0]
diff = np.abs(np.asarray(img, dtype=np.int16) - np.asarray(img2, dtype=np.int16)).max()
print("兩張圖最大像素差：", diff, "（0 代表完全相同）")

# %% [markdown]
# ## Part C：第一次呼叫雲端 LLM（選做）
# 金鑰**不寫在程式裡**。兩種放法，下面這格都會試：
# 1. **Colab 網頁版**：左側 🔑「密鑰（Secrets）」→ 新增 `GEMINI_API_KEY` → 打開「筆記本存取權」。
# 2. **`.env` 檔**（本機或 VS Code 連 Colab）：檔案內容一行 `GEMINI_API_KEY=你的金鑰`；VS Code 連 Colab 時，在檔案總管對 `.env` 按右鍵 →「Upload to Colab」。VS Code 連 Colab **不支援**方法 1。
#
# 沒有金鑰：這一格會印出備案訊息，改用 Part A 的開放模型，不影響後面。

# %%
import os
GEMINI_MODEL = "gemini-3.5-flash-lite"  # 免費方案可用的模型；名稱以 Google AI Studio 為準

key = None
try:                                    # 方法 1：Colab 網頁版的密鑰
    from google.colab import userdata
    key = userdata.get("GEMINI_API_KEY")
except Exception:
    pass
if not key:                             # 方法 2：.env 檔
    from dotenv import load_dotenv
    load_dotenv()
    key = os.environ.get("GEMINI_API_KEY")

if key:
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=key)
    resp = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=messages[1]["content"],
        config=types.GenerateContentConfig(system_instruction=messages[0]["content"]),
    )
    cloud_copy = resp.text
    print(cloud_copy)
    u = resp.usage_metadata
    print("用量：輸入", u.prompt_token_count, "tokens，輸出", u.candidates_token_count, "tokens")
else:
    print("沒有 API 金鑰：跳過雲端呼叫，使用 Part A 的開放模型文案（備案）。")

# %% [markdown]
# ## Part D：打開黑盒子——下一個 token 的機率
# 給模型一段開頭，看它對「下一個 token」的機率分布。

# %%
tok, model = gen.tokenizer, gen.model
prefix = "這款降噪耳機最大的特色是"
ids = tok(prefix, return_tensors="pt").to(model.device)
print("input_ids shape:", tuple(ids["input_ids"].shape))

# >>> TODO: 在 torch.no_grad() 下把 ids 丟進 model，取出 logits，印出 shape；再取最後一個位置的 logits 存成 last
with torch.no_grad():
    logits = model(**ids).logits
print("logits shape:", tuple(logits.shape), "| vocab_size =", model.config.vocab_size)
last = logits[0, -1].float()
# <<< TODO

probs = torch.softmax(last, dim=-1)
top = torch.topk(probs, 5)
for p, i in zip(top.values, top.indices):
    print(f"{tok.decode(int(i))!r:>8}  logit {last[i].item():7.2f}  →  機率 {p.item():.3f}")
print("全部 logits 加總：", round(last.sum().item(), 1), "｜全部機率加總：", round(probs.sum().item(), 4))

# %% [markdown]
# ### 溫度：把分布變尖或變平
# softmax(z / T)：T < 1 讓高的更高（變尖），T > 1 讓分布變平。

# %%
import matplotlib.pyplot as plt
from matplotlib import font_manager
# Colab 預設沒有中文字型：安裝 Noto CJK，否則 token 會顯示成方框
import subprocess, glob
if not glob.glob("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"):
    subprocess.run("apt-get -qq install -y fonts-noto-cjk > /dev/null", shell=True)
for f in glob.glob("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"):
    font_manager.fontManager.addfont(f)
    plt.rcParams["font.family"] = font_manager.FontProperties(fname=f).get_name()
labels = [tok.decode(int(i)) for i in top.indices]
fig, axes = plt.subplots(1, 3, figsize=(12, 3), sharey=True)
for ax, T in zip(axes, [0.5, 1.0, 2.0]):
    pT = torch.softmax(last / T, dim=-1)[top.indices].cpu()
    ax.bar(range(5), pT)
    ax.set_xticks(range(5), [repr(l) for l in labels], rotation=30)
    ax.set_title(f"T = {T}")
plt.tight_layout(); plt.savefig("outputs/temperature_bars.png", dpi=120); plt.show()

# %% [markdown]
# ### 練習（投影片「練習：溫度高低，文案怎麼變？」）
# 同一個提示，三種溫度各生成 3 次。先在投影片寫下預測，再執行。

# %%
for T in [0.2, 1.0, 1.5]:
    print(f"===== T = {T} =====")
    for k in range(3):
        out = gen(messages, max_new_tokens=60, do_sample=True, temperature=T, top_k=0, top_p=1.0)  # 關掉模型預設的 top_k／top_p，只看溫度的效果
        print(f"[{k+1}]", out[0]["generated_text"][-1]["content"].replace("\n", " "))

# %% [markdown]
# ### seed：讓文字也能重現

# %%
for k in range(2):
    torch.manual_seed(0)
    out = gen(messages, max_new_tokens=60, do_sample=True, temperature=1.0)
    print(f"[seed 0 第 {k+1} 次]", out[0]["generated_text"][-1]["content"].replace("\n", " "))

# %% [markdown]
# ## Ship：存檔＋授權欄
# 交付物要附上模型授權（從模型卡讀出來，不要憑記憶寫）。

# %%
from huggingface_hub import model_info

with open("outputs/copies.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(copies))
for repo in ["Qwen/Qwen2.5-0.5B-Instruct", "stable-diffusion-v1-5/stable-diffusion-v1-5", "latent-consistency/lcm-lora-sdv1-5"]:
    card = model_info(repo).card_data
    print(f"{repo:48s} license = {card.get('license') if card else '（模型卡沒有填）'}")

# %% [markdown]
# ### 實跑紀錄（講師用）
# 版本、VRAM 峰值：寫進 `research/lab-runs.md`。

# %%
import transformers, diffusers, huggingface_hub
print("torch", torch.__version__, "| transformers", transformers.__version__, "| diffusers", diffusers.__version__,
      "| huggingface_hub", huggingface_hub.__version__)
if torch.cuda.is_available():
    print(f"VRAM 峰值：{torch.cuda.max_memory_allocated()/1e9:.2f} GB")
