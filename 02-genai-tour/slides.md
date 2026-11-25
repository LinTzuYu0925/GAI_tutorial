---
theme: default
title: 今晚就要文案和產品圖
info: |
  生成式AI原理 · D1-2
  在 Colab T4 跑文字模型與影像模型，弄懂「為什麼每次輸出都不一樣」，並能重現與查授權。
colorSchema: light
fonts:
  provider: none
  sans: '"Noto Sans TC", "Microsoft JhengHei", "PingFang TC", Inter, Arial'
  mono: '"JetBrains Mono", Consolas'
lineNumbers: false
drawings:
  persist: false
transition: fade
mdc: true
exportFilename: 02-genai-tour
layout: center
class: cover
---

<div class="eyebrow">生成式AI原理 · D1-2</div>

# 今晚就要文案和產品圖

<p class="subtitle">自己在 Colab T4 跑文字模型和影像模型，而且能重現</p>

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-8">
  <span class="chip">開 T4</span><span class="arrow">→</span>
  <span class="chip">文案</span><span class="arrow">→</span>
  <span class="chip">產品圖</span><span class="arrow">→</span>
  <span class="chip">雲端 API</span><span class="arrow">→</span>
  <span class="chip">機率與溫度</span><span class="arrow">→</span>
  <span class="chip">seed</span><span class="arrow">→</span>
  <span class="chip">授權</span>
</div>

<!--
★ 開場（2 分）：上一堂看講師跑；這一堂自己跑。今天第一次碰到程式，但只用現成的模型（Try），不訓練。
-->

---

<div class="eyebrow">00 · Frame（定義問題）</div>

# 行銷部今晚就要東西

<div class="ticket mt-2">
  <div class="ticket-head">【需求單 #D1-2】部門：行銷部<span>公司：曜嶼電子 <span class="fiction" style="color:#fff;border-color:#fff">虛構</span></span></div>
  <dl>
    <dt>問題</dt><dd>新款藍牙耳機今晚上架預告，需要三版文案與一張產品情境圖</dd>
    <dt>現況痛點</dt><dd>外包文案三天、攝影一週，趕不上檔期</dd>
    <dt>成功指標（KPI）</dt><dd>3 版文案（每版 ≤ 80 字）＋ 1 張 512×512 圖；同樣設定能重現同一張圖</dd>
    <dt>可用資料</dt><dd>產品規格一段（虛構）</dd>
    <dt>限制與法規</dt><dd>免費 Colab T4；不能出現他牌商標；模型授權要能商用</dd>
    <dt>為何現有工具不夠</dt><dd>分類器、迴歸模型都不會「寫」或「畫」</dd>
  </dl>
</div>

<!--
★ 需求單（2 分）。特別點出「能重現」這個 KPI：今天的原理（機率與 seed）就是為了它。
-->

---

<div class="eyebrow">學習目標</div>

# 今天結束時，你能夠……

1. **執行**文字生成 `pipeline` 與 fp16（半精度：每個數字用 16 位元存，省一半 VRAM）的 `DiffusionPipeline`（Colab T4）
2. **呼叫**一次雲端 LLM，而且金鑰不寫在程式裡
3. **說明**輸出為什麼每次不同：從下一個 token 的機率抽樣；溫度改變機率的形狀
4. **重現**同一個輸出（seed），並從模型卡**讀出**授權

<!--
★ 目標（1 分）。不教：模型怎麼訓練（D3、D5）；提示工程進階（Agent 模組）。
-->

---

<div class="eyebrow">00 · Frame</div>

# 先寫好驗收清單，再開始生成

<table style="font-size:19px">
<thead><tr><th style="width:8%">#</th><th>驗收項目</th><th style="width:36%">怎麼檢查</th></tr></thead>
<tbody>
<tr><td>1</td><td>每版文案 ≤ 80 字，規格沒寫錯</td><td>印出字數；對照規格</td></tr>
<tr><td>2</td><td>圖裡沒有他牌商標或文字</td><td>人工看圖</td></tr>
<tr><td>3</td><td>同樣設定能重現同一張圖</td><td>跑兩次，像素差 ＝ 0</td></tr>
<tr><td>4</td><td>模型授權允許商用</td><td>從模型卡讀出 license 欄位</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">和 Vibe Coding 一樣：驗收標準在執行之前寫好，才分得清「跑完」和「可以交」。</div>

<!--
★ 驗收清單（3 分）：回扣 Vibe Coding 單元 01 的「④ 驗收」。最後的 Audit 頁會逐項對照這張表。
-->

---

<div class="eyebrow">01 · Try（先用現成的）· 環境</div>

# 打開 T4 1／2：在 VS Code 裝 Colab 擴充功能

<div class="grid grid-cols-[1.1fr_1fr] gap-6 mt-2">
<div class="steps">
  <div><span class="num">1</span>VS Code 左側「擴充功能」（<code>Ctrl+Shift+X</code>）</div>
  <div><span class="num">2</span>搜尋 <strong>Colab</strong>，選發行者是 <strong>Google</strong> 的那個 → Install（會一起裝好 Jupyter 擴充功能）</div>
  <div><span class="num">3</span>打開這堂的筆記本 <code>lab02-genai-tour.ipynb</code></div>
</div>
<div>

<div class="node node--primary"><strong>為什麼用 VS Code 連 Colab？</strong><small>程式在你熟悉的 VS Code 裡寫，算力用 Google 的免費 T4；檔案留在自己電腦</small></div>
<div class="node mt-3"><strong>沒有 VS Code？</strong><small>用瀏覽器開 Colab 網頁版也可以：功能表「執行階段 → 變更執行階段類型 → T4 GPU」</small></div>

</div>
</div>

<div class="takeaway mt-4">擴充功能（extension）只要裝一次；之後每本筆記本都能連 Colab 的 GPU。</div>

<div class="src">Google Colab VS Code 擴充功能 README 與 User Guide（research/sources.md S8）</div>

<!--
★ 安裝（3 分）：大家一起做。學員在 Vibe Coding 已經用過 VS Code 與擴充功能，這裡只多裝一個。
提醒看清楚發行者是 Google，市集裡有同名的第三方擴充功能。
沒有 VS Code 的學員改用 Colab 網頁版，後面的程式完全一樣；只有 Part C 放金鑰的方法不同（後面會講）。
-->

---

<div class="eyebrow">01 · Try · 環境</div>

# 打開 T4 2／2：連上 Colab 伺服器，確認 GPU 真的在

<div class="grid grid-cols-[1fr_1.1fr] gap-6 mt-2">
<div class="steps">
  <div><span class="num">1</span>筆記本右上角 <strong>Select Kernel</strong> → <strong>Colab</strong> → <strong>New Colab Server</strong></div>
  <div><span class="num">2</span>第一次會要你登入 Google：按 <strong>Allow</strong>，在瀏覽器完成授權</div>
  <div><span class="num">3</span>機器類型選 <strong>GPU</strong> 的 <strong>T4</strong>（選單字樣以畫面為準）</div>
  <div><span class="num">4</span>執行第 1 格，看印出的 GPU 名稱</div>
</div>
<div>

```python
import torch
torch.cuda.is_available()      # True 才有 GPU
torch.cuda.get_device_name(0)  # 'Tesla T4'
```

<div class="muted mt-2" style="font-size:17px">讀作：「CUDA 能不能用？」CUDA 是 NVIDIA GPU 的運算平台。</div>

</div>
</div>

<div class="muted" style="font-size:16px">講師實跑第 1 格印出：<code>GPU: Tesla T4 | 可用 VRAM 15.5 / 15.6 GB</code></div>

<div class="takeaway mt-2">先看到「GPU: Tesla T4」再往下做；印出「沒有 GPU」代表在 CPU 上，影像模型會非常慢。</div>

<div class="src">連線步驟：colab-vscode User Guide（S8）；用完記得 <code>Colab: Remove Server</code> 釋放 GPU。回顧：ML pp.5–6（Colab 執行階段）</div>

<!--
★ 連線（4 分）：大家一起做。選 New Colab Server 才能指定 T4；Auto Connect 會連到預設機器（不一定有 GPU）。
常見狀況：GPU 額度用完 → 第 1 格印出「沒有 GPU」，Part A、D 仍可在 CPU 跑，Part B 看解答筆記本的已存輸出。
下課前提醒：命令選擇區（Ctrl+Shift+P）執行「Colab: Remove Server」，把 GPU 還回去，免費額度才不會被空轉吃掉。
-->

---

<div class="eyebrow">01 · Try · 模型從哪來</div>

# 今天自己跑的模型都放在 Hugging Face Hub

<div class="flex items-center justify-center gap-3 mt-6" style="font-size:19px">
  <div class="node" style="width:30%"><strong>Hugging Face Hub</strong><small>huggingface.co：放模型權重與模型卡的網站，像「模型界的 GitHub」</small></div><span class="arrow">→</span>
  <div class="node node--primary" style="width:28%"><strong>第一次執行時自動下載</strong><small>存在 Colab 伺服器的快取，第二次就不用再等</small></div><span class="arrow">→</span>
  <div class="node node--secondary" style="width:26%"><strong>在 T4 上跑</strong><small>資料不離開這台機器</small></div>
</div>

<table class="mt-6" style="font-size:18px">
<thead><tr><th style="width:40%">程式裡寫的名字</th><th>讀作</th></tr></thead>
<tbody>
<tr><td><code>"Qwen/Qwen2.5-0.5B-Instruct"</code></td><td>Qwen 這個組織的 Qwen2.5-0.5B-Instruct 模型（文字）</td></tr>
<tr><td><code>"stable-diffusion-v1-5/stable-diffusion-v1-5"</code></td><td>Stable Diffusion 1.5（影像）</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">名字＝「組織／模型」；寫進 <code>pipeline</code> 就會從 Hub 下載，今天從 Hub 下載的模型都不用帳號或金鑰。</div>

<div class="src">網址＝huggingface.co/＋名字；模型卡上有授權（今天最後一格會讀）</div>

<!--
★ Hugging Face（3 分）：打開 huggingface.co/Qwen/Qwen2.5-0.5B-Instruct 給學員看一眼：上方是名字、右邊有下載次數、Files 分頁是權重檔、Model card 是說明與授權。
說法：「等一下寫的 model="Qwen/…"，就是這一頁的名字。程式第一次執行會從這裡下載權重，之後在 T4 上跑，資料不會送出去。」
有些模型（例如 Llama）要先登入、同意授權才能下載，叫 gated model；今天用的都不需要。上傳自己的模型在 D1-4（把自己的模型傳上 Hub）。
-->

---

<div class="eyebrow">01 · Try · 文字</div>

# 三個步驟寫文案：<code>pipeline</code>

<div class="grid grid-cols-[1.25fr_1fr] gap-5 mt-1">
<div>

```python
from transformers import pipeline
gen = pipeline("text-generation",
               model="Qwen/Qwen2.5-0.5B-Instruct",
               dtype=torch.float16, device="cuda")
out = gen(messages, max_new_tokens=120,
          do_sample=True, temperature=0.8)
```

<div class="muted mt-1" style="font-size:16px"><code>messages</code>：system 給角色，user 給規格與任務（筆記本 Part A）。<code>dtype</code>：用 fp16 存權重；<code>do_sample=True</code>：照機率抽籤，不是每次拿最大的；<code>max_new_tokens=120</code>：最多再生 120 個 token；<code>temperature=0.8</code>：溫度（後面講）</div>

</div>
<div>

<div style="height:210px;overflow:hidden;border:1px solid var(--border);border-radius:8px;background:var(--surface);padding:8px 12px;font-size:16px;line-height:1.45">
  <b>第 1 版（157 字）節錄</b><br>
  🌟探索無線通勤新樂章！🌟<br>
  曜嶼 Breeze 藍牙耳機，專為通勤設計，讓您在忙碌的都市中也能享受寧靜的音質與便利的體驗。<br>
  <span class="muted">（中略，含簡體字）</span><br>
  💡快充功能，<b>一秒</b>就能將電池充至100%……
</div>
<div class="shot-cap">2026-11-26 Colab T4 實跑 · 三版 157／171／123 字，都超過 80 字；規格是「10 分鐘快充」</div>

</div>
</div>

<div class="takeaway mt-3"><code>pipeline</code> 把「切 token → 模型 → 抽樣 → 還原文字」包成一行。</div>

<div class="src">模型：Qwen2.5-0.5B-Instruct（約 5 億參數，授權見模型卡；research/sources.md S2）</div>

<!--
★ 文字（6 分）：學員跟著執行 Part A。強調 0.5B 是「小」模型：能在免費 T4 跑，但會寫錯規格——正好用來練習驗收。
dtype=torch.float16 讀作「每個參數用 16 位元存」，D1-4 會算記憶體。
-->

---

<div class="eyebrow">01 · Try · 影像</div>

# 一張產品情境圖：SD1.5 ＋ LCM-LoRA，4 步

<div class="grid grid-cols-[1.25fr_1fr] gap-5 mt-1">
<div>

```python
pipe = DiffusionPipeline.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    dtype=torch.float16).to("cuda")
pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
pipe.load_lora_weights("latent-consistency/lcm-lora-sdv1-5")
g = torch.Generator("cuda").manual_seed(42)
img = pipe(PROMPT, num_inference_steps=4,
           guidance_scale=1.0, generator=g).images[0]
```

<div class="muted mt-1" style="font-size:16px">讀作：<code>num_inference_steps=4</code> 去雜訊 4 步；<code>guidance_scale=1.0</code> 不加強提示詞（LCM 要用 1.0）；<code>generator</code> 固定 seed。LCM＝Latent Consistency Model（潛在一致性模型）</div>

</div>
<div>

<img src="/lab02-run-product_seed42.png" alt="SD1.5 產生的白色無線耳機放在木桌上" style="height:220px;border:1px solid var(--border);border-radius:8px">
<div class="shot-cap">512×512 · seed 42 · 4 步 · T4 實跑；同 seed 再跑一次，最大像素差 0</div>

</div>
</div>

<div class="takeaway mt-3">LCM-LoRA 是一個「加速外掛」：原本要幾十步的模型，4 步就出圖。</div>

<div class="src">S3、S4；為什麼能變快在 D4-4 說明，今天只會用</div>

<!--
★ 影像（6 分）：第一次下載 SD1.5＋LCM-LoRA 要等幾分鐘，請學員一進這頁就先執行 Part B 的格子，邊等邊聽。只解釋三個參數：num_inference_steps（幾步）、guidance_scale（LCM 用 1.0）、generator（seed）。
LoRA 是什麼在 D4-3；擴散模型怎麼運作在 D3-3。今天的重點是「能跑、能重現」。
-->

---

<div class="eyebrow">01 · Try · 雲端 API</div>

# 自己跑 vs 呼叫 API：模型在誰的機器上？

<div class="grid grid-cols-2 gap-8 mt-2">
<div>

<div style="font-size:20px"><strong>自己跑開放模型</strong><span class="muted" style="font-size:17px">　Part A、B 的做法</span></div>
<div class="flex flex-col items-center gap-1 mt-2" style="font-size:17px">
  <div class="node" style="width:88%"><strong>Hugging Face Hub</strong><small>只在第一次下載權重</small></div>
  <span class="arrow">↓</span>
  <div class="node node--secondary" style="width:88%"><strong>你的 Colab T4</strong><small>你的程式＋模型權重都在這台；在這裡算</small></div>
  <span class="arrow">↓</span>
  <div class="node" style="width:88%"><strong>文案、圖片</strong><small>資料沒有離開這台機器</small></div>
</div>

</div>
<div>

<div style="font-size:20px"><strong>呼叫雲端 API</strong><span class="muted" style="font-size:17px">　Part C 的做法</span></div>
<div class="flex flex-col items-center gap-1 mt-2" style="font-size:17px">
  <div class="node" style="width:88%"><strong>你的程式</strong><small>只有提示詞＋API 金鑰，沒有模型</small></div>
  <div class="flex items-center gap-2"><span class="arrow">↓</span><span class="muted" style="font-size:16px">網路送出提示詞</span></div>
  <div class="node node--warm" style="width:88%"><strong>廠商的伺服器（Google Gemini）</strong><small>模型在這裡算；用金鑰確認你是誰、算用量</small></div>
  <div class="flex items-center gap-2"><span class="arrow">↓</span><span class="muted" style="font-size:16px">回傳文字</span></div>
  <div class="node" style="width:88%"><strong>文案</strong><small>提示詞已經送到廠商那裡</small></div>
</div>

</div>
</div>

<div class="takeaway mt-3">自己跑：模型和資料都在你的 GPU；API：模型在廠商那邊，你送出提示詞、拿回結果。</div>

<!--
★ 兩種跑法（3 分）：連回 D1-1 的「買 API，還是自己跑開放權重？」。
指左邊：模型權重下載到我們租的 T4 上，計算也在 T4，所以客戶資料不會送出去。
指右邊：我們的程式裡根本沒有模型，只是把提示詞透過網路送到 Google，由 Google 的伺服器算完再傳回來；金鑰就是「證明你是誰」的通行證，用量也照它計算。
-->

---

<div class="eyebrow">01 · Try · 雲端 API</div>

# 拿一把免費的 Gemini API 金鑰

<div class="grid grid-cols-[1.25fr_1fr] gap-6 mt-2">
<div class="steps">
  <div><span class="num">1</span>瀏覽器打開 <strong>aistudio.google.com/apikey</strong>，用 Google 帳號登入</div>
  <div><span class="num">2</span>第一次會請你同意服務條款；同意後 AI Studio 會<strong>自動建立專案</strong>，不用綁信用卡</div>
  <div><span class="num">3</span>按 <strong>Create API key</strong> → 複製那一長串字</div>
  <div><span class="num">4</span>先貼到記事本，下一頁放進 Colab；<strong>不要</strong>貼進程式碼</div>
</div>
<div style="font-size:18px">

<div class="node node--warm"><strong>金鑰＝密碼</strong><small>別人拿到就能用你的額度；不要截圖、不要上傳 GitHub</small></div>
<div class="node node--warm mt-3"><strong>免費方案的代價</strong><small>Google 可能用你的提示詞改進產品 → 不放個資、未公開規格</small></div>

</div>
</div>

<div class="takeaway mt-4">金鑰只放在「密鑰」或 <code>.env</code> 這種不會被分享的地方，程式只讀它的名字。</div>

<div class="src">Gemini API 文件：API keys、Pricing（免費方案「Used to improve our products：Yes」）、Rate limits（research/sources.md S9、S10）</div>

<!--
★ 拿金鑰（3 分）：大家一起做，講師投影自己的畫面但遮住金鑰。
已經用過 Google Cloud 的學員，畫面可能要求「Import projects」選既有專案，選任一個即可；少數專案要先驗證。
免費方案有每分鐘、每天的次數上限，以 AI Studio 的 rate limit 頁為準；課堂上每人呼叫幾次不會碰到。
連回第一頁的風險：免費方案的提示詞可能被用來改進產品，所以不要放個資。
-->

---

<div class="eyebrow">01 · Try · 雲端 API</div>

# 把金鑰交給程式：兩種放法

<div class="grid grid-cols-2 gap-6 mt-1">
<div>

<div class="node node--primary"><strong>方法 1：Colab 網頁版「密鑰」</strong><small>只有在瀏覽器開 Colab 時能用</small></div>
<div class="steps mt-2" style="font-size:17px">
  <div><span class="num">1</span>左側 🔑「密鑰（Secrets）」→ 新增</div>
  <div><span class="num">2</span>名稱 <code>GEMINI_API_KEY</code>，值貼上金鑰</div>
  <div><span class="num">3</span>打開「筆記本存取權」</div>
</div>

```python
from google.colab import userdata
key = userdata.get("GEMINI_API_KEY")
```

</div>
<div>

<div class="node node--secondary"><strong>方法 2：<code>.env</code> 檔</strong><small>VS Code 連 Colab、本機都能用</small></div>
<div class="steps mt-2" style="font-size:17px">
  <div><span class="num">1</span>新增 <code>.env</code>，一行：<code class="nw">GEMINI_API_KEY=金鑰</code></div>
  <div><span class="num">2</span>檔案總管對它按右鍵 → <strong>Upload to Colab</strong>（<code>.gitignore</code> 要有 <code>.env</code>）</div>
</div>

```python
from dotenv import load_dotenv
import os
load_dotenv()   # 讀 .env 放進環境變數
key = os.environ.get("GEMINI_API_KEY")
```

</div>
</div>

<div class="takeaway mt-2">VS Code 連 Colab <strong>不支援方法 1</strong>，要用方法 2；筆記本兩種都會試，哪個有就用哪個。</div>

<div class="src">userdata.get 在 VS Code 擴充功能會出錯（S8）；<code>.env</code>：Vibe 單元 12</div>

<!--
★ 放金鑰（3 分）：先問：「Vibe 單元 12 把金鑰放在哪？」→ .env。今天多一個 Colab 網頁版專用的密鑰功能。
用 VS Code 連 Colab 的學員一定要用方法 2：Colab 的密鑰需要網頁版的畫面，VS Code 擴充功能呼叫 userdata.get 會直接出錯（官方 Known Issues 有寫）。
上傳後可以在 VS Code 左側 Colab 的 Contents 檢視看到 /content/.env。課程結束、Remove Server 之後檔案會跟著伺服器消失。
常見錯誤：.env 寫成 GEMINI_API_KEY = "xxx"（多了空格和引號）多數時候也能讀，但最保險是等號兩邊不留空格、不加引號。
-->

---

<div class="eyebrow">01 · Try · 雲端 API</div>

# 第一次呼叫雲端 LLM：一樣的提示詞，送去 Gemini

<div class="grid grid-cols-[minmax(0,1.3fr)_minmax(0,1fr)] gap-5 mt-1">
<div>

```python
from google import genai
from google.genai import types
client = genai.Client(api_key=key)
resp = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=TASK,
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM))
print(resp.text)
u = resp.usage_metadata     # 用了幾個 token
print("用量：輸入", u.prompt_token_count, …)
```

<div class="muted mt-1" style="font-size:16px">讀作：「拿金鑰開連線，送出提示，印出回覆和用量」</div>

</div>
<div>

<div style="border:1px solid var(--border);border-radius:8px;background:var(--surface);padding:8px 12px;font-size:16px;line-height:1.5">
  通勤救星降臨！曜嶼 Breeze 藍牙耳機單耳僅 5g，輕若無物。強效降噪還你寧靜世界，30 小時超長續航。支援快充 10 分鐘，音樂即刻暢聽 2 小時！<br>
  <span class="muted">用量：輸入 87 tokens，輸出 64 tokens</span>
</div>
<div class="shot-cap">gemini-3.5-flash-lite · 講師 2026-11-26 在 VS Code 連 Colab 執行 Part C · 77 字，通過 ≤ 80 字；規格數字都對，但「單耳」是它自己加的。每次呼叫的回答都不同</div>
<div class="muted mt-2" style="font-size:16px">SYSTEM、TASK＝Part A 的兩段提示詞。SDK：google-genai（S9）</div>

</div>
</div>

<div class="takeaway mt-2">同一份提示詞，換成雲端模型只差幾行；沒有金鑰，這格印出備案訊息並跳過。</div>


<!--
★ 呼叫（3 分）：和 Part A 比較：Part A 用 pipeline 在自己的 T4 跑 Qwen；這裡用 google-genai 把同一段 SYSTEM、TASK 送到 Google。
usage_metadata 會印出輸入、輸出 token 數，這就是 API 的計費單位（D5-3 再算成本）。
和 Part A 比較（講師實跑）：Qwen 0.5B 三版 123–171 字、混簡體字、寫出「一秒充到 100%」；Gemini 77 字、全繁體、數字都對，但多寫了「單耳」——大模型也要人工核對。另一次本機呼叫得到 85 字的版本（research/lab-runs.md），說明雲端模型每次回答也不同。
備案：沒有金鑰的學員直接跳過，不影響後面。
-->

---

<div class="eyebrow">02 · Open（打開黑盒子）</div>

# 為什麼每次文案都不一樣？

<div class="grid grid-cols-[1fr_1fr] gap-6 mt-1 items-center">
<div>

```python
ids = tok("這款降噪耳機最大的特色是",
          return_tensors="pt")  # 切成 token ID
with torch.no_grad():
    logits = model(**ids).logits   # 每個位置一排分數
last = logits[0, -1]           # 最後一個位置
probs = torch.softmax(last, dim=-1)  # 分數變機率
top = torch.topk(probs, 5)     # 取機率最高的 5 個
```

</div>
<div>

<img src="/lab02-run-top5.png" alt="下一個 token 前 5 名的機率長條圖，第一名 0.190" style="height:230px">
<div class="shot-cap">數字來自 T4 實跑 Part D，圖在本機重畫：第一名也只有 0.19；第 2、4 名「采用了」「采用」是簡體字（模型輸出原樣）</div>

</div>
</div>

<div class="takeaway mt-3">模型不是給「一個答案」，而是給<strong>每一個可能的下一個 token 一個機率</strong>。</div>

<div class="src">回顧：DL pp.80–81（GPT＝猜下一個字）；Vibe 01（LLM 是 token 接龍）</div>

<!--
★ 機率（5 分）：先請學員猜：「這款降噪耳機最大的特色是」下一個字是什麼？再跑 Part D 看前 5 名。
logits 讀作「還沒變成機率的分數」，softmax 把分數變成加起來等於 1 的機率（DL 學過）。
-->

---

<div class="eyebrow">02 · Open · 抽樣</div>

# 生成＝依機率抽籤，一次一個 token

<div class="flex items-center justify-center gap-3 mt-6" style="font-size:20px">
  <div class="node" style="width:24%"><strong>① 算機率</strong><small>每個 token 一個機率</small></div><span class="arrow">→</span>
  <div class="node node--primary" style="width:24%"><strong>② 抽一個</strong><small>機率高的比較常被抽到</small></div><span class="arrow">→</span>
  <div class="node" style="width:24%"><strong>③ 接到後面</strong><small>變成新的開頭</small></div><span class="arrow">→</span>
  <div class="node node--dashed" style="width:14%"><strong>重複</strong><small>到結束為止</small></div>
</div>

<table class="mt-6" style="font-size:18px">
<thead><tr><th style="width:26%">設定</th><th>怎麼選下一個 token</th><th style="width:28%">結果</th></tr></thead>
<tbody>
<tr><td><code>do_sample=False</code></td><td>永遠選機率最高的（貪婪法，greedy）</td><td>每次都一樣</td></tr>
<tr><td><code>do_sample=True</code></td><td>照機率抽籤</td><td>每次不同</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">「每次不一樣」不是壞掉，是因為每一步都在抽籤。</div>

<!--
★ 抽樣（4 分）：對照 D1-1 的「從 p_θ 抽樣」：文字模型一次抽一個 token，接起來就是一段文字。
greedy 讀作「貪婪法」：每一步都拿最大的，所以沒有隨機性。
-->

---

<div class="eyebrow">02 · Open · 分數變機率</div>

# 模型吐出的是分數（logit），softmax 才把它變成機率

<svg viewBox="0 0 900 275" style="width:100%;max-height:255px" class="mt-1">
  <defs><marker id="arl" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--muted-text)"/></marker></defs>
  <text x="20" y="24" style="font-size:19px;font-weight:700" fill="var(--text)">① 模型輸出：分數 z（logit）</text>
  <line x1="40" y1="200" x2="290" y2="200" stroke="var(--muted-text)" stroke-width="1.5"/>
  <rect x="60" y="80" width="50" height="120" fill="var(--primary)"/><text x="70" y="72" style="font-size:18px" fill="var(--text)">2.0</text>
  <rect x="140" y="140" width="50" height="60" fill="var(--primary)"/><text x="150" y="132" style="font-size:18px" fill="var(--text)">1.0</text>
  <rect x="220" y="199" width="50" height="2" fill="var(--primary)"/><text x="230" y="190" style="font-size:18px" fill="var(--text)">0.0</text>
  <text x="72" y="226" style="font-size:18px" fill="var(--muted-text)">A</text><text x="152" y="226" style="font-size:18px" fill="var(--muted-text)">B</text><text x="232" y="226" style="font-size:18px" fill="var(--muted-text)">C</text>
  <text x="40" y="260" style="font-size:17px" fill="var(--warm-accent)">分數可正可負；這三個加起來 3.0 ≠ 1</text>

  <line x1="310" y1="140" x2="560" y2="140" stroke="var(--muted-text)" stroke-width="2" marker-end="url(#arl)"/>
  <rect x="330" y="96" width="94" height="34" rx="6" fill="var(--soft-amber)" stroke="var(--warm-accent)" stroke-width="2"/>
  <text x="344" y="119" style="font-size:18px;font-weight:700" fill="var(--warm-accent)">② ÷ T</text>
  <rect x="440" y="96" width="104" height="34" rx="6" fill="var(--soft-blue)" stroke="var(--primary)" stroke-width="2"/>
  <text x="450" y="119" style="font-size:18px;font-weight:700" fill="var(--primary)">softmax</text>
  <text x="326" y="172" style="font-size:16px" fill="var(--warm-accent)">溫度 T 在這裡</text>
  <text x="326" y="194" style="font-size:16px" fill="var(--muted-text)">（T＝1 時不改變分數）</text>

  <text x="590" y="24" style="font-size:19px;font-weight:700" fill="var(--text)">③ 機率 p（T＝1）</text>
  <line x1="600" y1="200" x2="870" y2="200" stroke="var(--muted-text)" stroke-width="1.5"/>
  <rect x="620" y="66" width="50" height="134" fill="var(--secondary)"/><text x="622" y="58" style="font-size:18px" fill="var(--text)">0.67</text>
  <rect x="700" y="152" width="50" height="48" fill="var(--secondary)"/><text x="702" y="144" style="font-size:18px" fill="var(--text)">0.24</text>
  <rect x="780" y="182" width="50" height="18" fill="var(--secondary)"/><text x="782" y="174" style="font-size:18px" fill="var(--text)">0.09</text>
  <text x="632" y="226" style="font-size:18px" fill="var(--muted-text)">A</text><text x="712" y="226" style="font-size:18px" fill="var(--muted-text)">B</text><text x="792" y="226" style="font-size:18px" fill="var(--muted-text)">C</text>
  <text x="600" y="260" style="font-size:17px" fill="var(--secondary)">都在 0–1 之間；加起來剛好 1</text>
</svg>

<div class="muted" style="font-size:16px">T4 實跑 Part D：前 5 名 logit 是 12.78、11.78……；全部 151,936 個 logit 加總 −601,090，softmax 後才是 1</div>

<div class="takeaway mt-1">模型只給分數；softmax 把分數換成「加起來等於 1」的機率，抽籤用的是機率。溫度 T 就插在 softmax 之前。</div>

<div class="src">手算的教學用數字：softmax(&#91;2, 1, 0&#93;) ＝ &#91;0.665, 0.245, 0.090&#93;。回顧：DL pp.69–71（softmax 與溫度）</div>

<!--
★ logit 到機率（4 分）：連回「為什麼每次文案都不一樣」那頁的程式：logits = model(...).logits 拿到的是左邊這種分數，probs = torch.softmax(...) 才是右邊的機率。
logit 讀作「還沒變成機率的分數」：可以是負的，也可以大於 1，加起來也不是 1（Part D 會印出真實的 logits 加總）。
softmax 讀作「先取指數變成正數，再除以總和」，所以每個都在 0 到 1 之間、加起來是 1。DL 課學過，這裡只回顧。
溫度 T 就是在 softmax 之前，先把每個分數除以 T。下一頁看 T 改變之後機率怎麼變。
-->

---

<div class="eyebrow">02 · Open · 溫度</div>

# 溫度：把機率分布變尖或變平

<div class="grid grid-cols-[1fr_1.2fr] gap-6 mt-1 items-center">
<div style="font-size:19px">

$$p_i = \mathrm{softmax}\!\left(\frac{z_i}{T}\right)$$

- **p<sub>i</sub>**：第 i 個 token 的機率
- **z<sub>i</sub>**：第 i 個 token 的分數（logit）
- **T**：溫度
- **讀作**：「每個分數先除以溫度，再變成機率」

</div>
<div>

<table style="font-size:17px">
<thead><tr><th>分數 z ＝ &#91;2, 1, 0&#93;</th><th>T ＝ 0.5</th><th>T ＝ 1</th><th>T ＝ 2</th></tr></thead>
<tbody>
<tr><td>token A</td><td><strong>0.87</strong></td><td>0.67</td><td>0.51</td></tr>
<tr><td>token B</td><td>0.12</td><td>0.24</td><td>0.31</td></tr>
<tr><td>token C</td><td>0.02</td><td>0.09</td><td>0.19</td></tr>
</tbody>
</table>

<div class="muted mt-1" style="font-size:15px">手算的教學用數字（四捨五入到小數兩位）</div>

</div>
</div>

<div class="takeaway mt-3">T 小 → 幾乎只選第一名（穩定、重複）；T 大 → 冷門 token 也有機會（多樣、可能亂）。</div>

<div class="src">回顧：DL pp.69–71（知識蒸餾的溫度，同一個公式）</div>

<!--
★ 溫度（5 分）：公式只有一條。用表格的手算數字說明：T=0.5 時 A 從 0.67 變 0.87（變尖），T=2 時變 0.51（變平）。
學員在 DL 課的知識蒸餾看過同一個 softmax(z/T)，那裡是為了讓學生模型看到「軟標籤」。
計算：softmax([4,2,0])=[0.867,0.117,0.016]；softmax([2,1,0])=[0.665,0.245,0.090]；softmax([1,0.5,0])=[0.506,0.307,0.186]。
-->

---

<div class="eyebrow">02 · Open · 溫度 · 練習</div>

# 練習：溫度高低，文案怎麼變？

<div class="muted" style="font-size:17px">照著做：Part A 用 T＝0.8 跑了 3 次，三版開頭、長度都不同 → 「不一樣」。注意：這格關掉 top_k／top_p（Part A 沒關），只看溫度本身的效果。換你：1. 先寫預測　2. 執行 Part D 的「練習」格（每種溫度 3 次）　3. 填實際觀察</div>

<table class="fill vlines mt-1">
<thead><tr><th style="width:14%">溫度</th><th>我預測：3 次一樣嗎？</th><th>實際：3 次一樣嗎？</th><th>實際：通順、規格正確嗎？</th></tr></thead>
<tbody>
<tr><td>T ＝ 0.2</td><td class="blank"><FillIn id="temp.t02-pred" hint="例：幾乎一樣……" /></td><td class="blank"><FillIn id="temp.t02-same" /></td><td class="blank"><FillIn id="temp.t02-ok" /></td></tr>
<tr><td>T ＝ 1.0</td><td class="blank"><FillIn id="temp.t10-pred" /></td><td class="blank"><FillIn id="temp.t10-same" /></td><td class="blank"><FillIn id="temp.t10-ok" /></td></tr>
<tr><td>T ＝ 1.5</td><td class="blank"><FillIn id="temp.t15-pred" /></td><td class="blank"><FillIn id="temp.t15-same" /></td><td class="blank"><FillIn id="temp.t15-ok" hint="例：開始出現……" /></td></tr>
</tbody>
</table>

<FillClear group="temp" />

<!--
★ 練習（10 分）：個人作業，不收回。目的是自己發現：T 低 → 三次幾乎一樣、句子安全但重複；T 高 → 多樣，但開始出現錯字、怪詞或規格錯誤。
下一頁是答案（學員網站不含）。因為抽樣有隨機性，每個人的文字不同，但趨勢一樣。
-->

---
hostOnly: true
---

<div class="eyebrow">02 · Open · 溫度 · 練習解答</div>

# 練習解答：溫度越高，越多樣也越容易出錯

<table class="vlines" style="font-size:18px">
<thead><tr><th style="width:14%">溫度</th><th>3 次一樣嗎？</th><th>通順、規格正確嗎？</th></tr></thead>
<tbody>
<tr><td>T ＝ 0.2</td><td>很像：三次都用「探索……」開頭、句型幾乎一樣</td><td>通順，但仍混進簡體字</td></tr>
<tr><td>T ＝ 1.0</td><td>每次不同</td><td>開始冒出整段英文、「$(店名)$」這種怪字串</td></tr>
<tr><td>T ＝ 1.5</td><td>完全不同</td><td>多國文字亂碼，看不懂</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">怎麼判斷：趨勢對就對——T 越高，多樣性上升、可靠度下降。上表是講師 2026-11-26 T4 實跑的觀察；每個人抽到的句子不同。</div>

<!--
★ 解答（2 分）：講師實跑例子（2026-11-26，research/lab02-t4-run1-outputs.txt）：T=0.2 三次都以「探索」開頭；T=1.0 第 1 次整段英文；T=1.5 是多國文字亂碼。
注意：這格關掉了 top_k／top_p（top_k=0, top_p=1.0），只看溫度；所以 T=1.0 就已經比 Part A（有預設 top_k／top_p）亂很多。這正好說明 top_k／top_p 的用處（D5 再教）。
-->

---

<div class="eyebrow">03 · Adapt（調成我們的）</div>

# seed（亂數種子）：讓「隨機」可以重現

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-1">
<div>

```python
g = torch.Generator("cuda").manual_seed(42)  # 影像
img = pipe(PROMPT, generator=g, ...)

torch.manual_seed(0)                          # 文字
out = gen(messages, do_sample=True, ...)
```

<div class="muted mt-1" style="font-size:17px">讀作：「把亂數產生器的起點固定在 42」</div>

</div>
<div style="font-size:18px">

<div class="node node--primary"><strong>會重現</strong><small>同 seed ＋ 同提示詞 ＋ 同參數 ＋ 同套件版本 ＋ 同類 GPU</small></div>
<div class="node node--warm mt-3"><strong>可能不同</strong><small>換 GPU、換套件版本，或用到不保證結果一致的 GPU 運算，同一個 seed 也可能出不同的圖</small></div>

</div>
</div>

<div class="takeaway mt-3">交付時記錄 seed、步數、模型與版本，別人才能重做出同一張圖。</div>

<div class="src">PyTorch Reproducibility 說明（S6）</div>

<!--
★ seed（5 分）：筆記本 Part B 會用同一個 seed 跑兩次，印出最大像素差；2026-11-26 Colab T4 實跑結果是 0。
常見誤解：「固定 seed 就保證到處都一樣」——不同 GPU 或版本可能不同，所以要記錄環境。
-->

---

<div class="eyebrow">03 · Adapt · 提示詞</div>

# system 提示給角色，user 提示給任務

```python
messages = [
  {"role": "system", "content": "你是曜嶼電子的行銷文案寫手，只用台灣繁體中文，不提其他品牌。"},
  {"role": "user",   "content": SPEC + "請寫一段 80 字以內的上架文案。"},
]
```

<div class="takeaway mt-4">把「每次都一樣的規則」放 system，把「這次的任務」放 user。</div>

<div class="src">回顧：Vibe 01–02（system 與 user 提示）</div>

<!--
○ 提示詞（3 分）：學員在 Vibe Coding 學過，這裡只指出在程式裡長什麼樣。可以讓學員把「只用台灣繁體中文」拿掉，看輸出會不會出現簡體字。
-->

---

<div class="eyebrow">03 · Adapt · 影像</div>

# 負面提示：告訴影像模型「不要什麼」

```python
img = pipe(PROMPT, negative_prompt="logo, text, watermark, brand name", ...)
```

<div class="node node--warm mt-3" style="font-size:18px"><strong>注意：今天的設定它沒有作用</strong><small>guidance＝讓圖更貼近提示詞、遠離負面提示的加強。diffusers 在 guidance_scale ≤ 1 時不做 guidance，負面提示會被忽略；LCM 用 1.0，所以驗收第 2 項靠「看圖＋換 seed」。D4-2 用 guidance 大於 1 的設定時才有效</small></div>

<div class="takeaway mt-3">負面提示要搭配 guidance 才有用；不管有沒有用，最後都要人工看圖。</div>

<div class="src">diffusers 0.43.0 原始碼：<code>do_classifier_free_guidance = guidance_scale &gt; 1 …</code>（research/sources.md S12）；D4-2 解釋 guidance</div>

<!--
○ 負面提示（2 分）：LCM 搭配 guidance_scale=1.0 時，diffusers 根本不做 guidance，負面提示完全被忽略（已讀 diffusers 0.43.0 原始碼確認）。D4-2 用 guidance 大於 1 的一般取樣再比較。
-->

---

<div class="eyebrow">04 · Lab L1-2</div>

# Lab 1／4：我們要生成什麼？

<div class="grid grid-cols-2 gap-6 mt-2" style="font-size:19px">
<div>

**打開筆記本**：`lab02-genai-tour.ipynb`（<span class="placeholder" style="display:inline;padding:0 6px">下載連結：講師決定發放方式後補上</span>）<br>
執行階段：**Select Kernel → Colab → New Colab Server → T4**<br>
資料：一段虛構產品規格（筆記本裡）

1. 三版文案，哪一版你敢直接上架？
2. 圖裡有沒有不該出現的東西？
3. 再跑一次，圖還一樣嗎？

</div>
<div>

<div class="flex gap-3 items-start">
<img src="/lab02-run-product_seed42.png" alt="產品圖" style="width:150px;border:1px solid var(--border);border-radius:8px">
<div style="font-size:15px;line-height:1.5"><b>copies.txt</b>：三版文案<br><b>product_seed42.png</b>：左圖<br><b>授權（模型卡讀出）</b><br>Qwen2.5-0.5B-Instruct：apache-2.0<br>SD1.5：creativeml-openrail-m<br>LCM-LoRA：openrail++</div>
</div>
<div class="shot-cap">講師 2026-11-26 Colab T4 實跑的交付物</div>

</div>
</div>

<div class="takeaway mt-3">這就是四個檢查點的 ① 目標。</div>

<!--
★ Lab 開始（2 分）。備案：沒有 GPU 額度 → 打開 lab02-genai-tour-solution.ipynb 看已存輸出；Part A、D 也能在 CPU 跑（慢）。
-->

---

<div class="eyebrow">04 · Lab L1-2</div>

# Lab 2／4：pipeline 拆成哪幾塊？

<div class="mt-2" style="font-size:18px"><strong>文字</strong></div>
<div class="flex items-center gap-2 mt-1" style="font-size:17px">
  <div class="node">提示詞<small>字串</small></div><span class="arrow">→</span>
  <div class="node node--primary">tokenizer<small>切成 token ID</small></div><span class="arrow">→</span>
  <div class="node node--primary">model<small>每個 token 的分數</small></div><span class="arrow">→</span>
  <div class="node node--secondary">抽樣<small>選一個 token</small></div><span class="arrow">→</span>
  <div class="node">decode<small>變回文字</small></div>
</div>

<div class="mt-5" style="font-size:18px"><strong>影像</strong>（今天只認名字，D3–D4 打開）</div>
<div class="flex items-center gap-2 mt-1" style="font-size:17px">
  <div class="node">提示詞</div><span class="arrow">→</span>
  <div class="node node--primary">text encoder<small>文字變向量</small></div><span class="arrow">→</span>
  <div class="node node--primary">U-Net × 4 步<small>一步步去掉雜訊</small></div><span class="arrow">→</span>
  <div class="node node--primary">VAE decoder<small>變回 512×512 圖</small></div>
</div>

<div class="takeaway mt-4">一行 <code>pipeline</code> 背後是好幾個模型接力；名稱和筆記本裡的物件一樣。</div>

<!--
★ 拆塊（3 分）：文字那一列是今天的重點，下一頁要填每一塊的輸入輸出。影像那一列只是預告：U-Net 在 D2-2、VAE 在 D2-3、擴散在 D3-3。
-->

---

<div class="eyebrow">04 · Lab L1-2 · 練習</div>

# 練習：每一塊的輸入與輸出

<div class="muted" style="font-size:17px">先不用 AI、不用執行，自己預測；之後用 Part D 的 <code>print</code> 對答案。n ＝ 提示詞的 token 數</div>

<table class="fill vlines mt-1">
<thead><tr><th style="width:18%">塊</th><th>輸入</th><th>輸出（型別或 shape）</th><th>做什麼（一句話）</th></tr></thead>
<tbody>
<tr><td>tokenizer</td><td>字串</td><td><code>input_ids</code>：&#91;1, n&#93;</td><td>把文字切成 token ID</td></tr>
<tr><td>model</td><td class="blank"><FillIn id="io.model-in" hint="例：一排整數……" /></td><td class="blank"><FillIn id="io.model-out" hint="例：幾維、每維多大……" /></td><td class="blank"><FillIn id="io.model-do" /></td></tr>
<tr><td>取最後位置＋softmax</td><td class="blank"><FillIn id="io.sm-in" /></td><td class="blank"><FillIn id="io.sm-out" /></td><td class="blank"><FillIn id="io.sm-do" /></td></tr>
<tr><td>抽樣</td><td class="blank"><FillIn id="io.samp-in" /></td><td class="blank"><FillIn id="io.samp-out" /></td><td class="blank"><FillIn id="io.samp-do" /></td></tr>
</tbody>
</table>

<FillClear group="io" />

<!--
★ 無 AI 檢核點（6 分）：第一列已填好當示範。提示：vocab_size 是詞彙表大小，學員可以先寫「詞彙表大小」，跑完 Part D 再填數字。
-->

---
hostOnly: true
---

<div class="eyebrow">04 · Lab L1-2 · 練習解答</div>

# 練習解答：每一塊的輸入與輸出

<table class="vlines" style="font-size:18px">
<thead><tr><th style="width:18%">塊</th><th>輸入</th><th>輸出</th><th>做什麼</th></tr></thead>
<tbody>
<tr><td>tokenizer</td><td>字串</td><td><code>input_ids</code>：&#91;1, n&#93;</td><td>把文字切成 token ID</td></tr>
<tr><td>model</td><td><code>input_ids</code> &#91;1, n&#93;</td><td><code>logits</code> &#91;1, n, vocab_size&#93;</td><td>每個位置對每個 token 打分數</td></tr>
<tr><td>最後位置＋softmax</td><td><code>logits&#91;0, -1&#93;</code> &#91;vocab_size&#93;</td><td>機率 &#91;vocab_size&#93;，總和 1</td><td>分數變機率</td></tr>
<tr><td>抽樣</td><td>機率 &#91;vocab_size&#93;</td><td>1 個 token ID</td><td>照機率抽一個</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">怎麼對答案：Part D 印出 <code>input_ids shape</code>、<code>logits shape</code> 與 <code>vocab_size</code>。T4 實跑：(1, 9)、(1, 9, 151936)、151936。</div>

<!--
★ 解答（2 分）：vocab_size 用 model.config.vocab_size 印出來，不要背。注意 logits 的最後一維可能比 tokenizer 真正用到的詞彙數大一點（模型會補齊），以實跑為準。
-->

---

<div class="eyebrow">04 · Lab L1-2</div>

# Lab 3／4：Specify → Generate → Execute

<div class="grid grid-cols-[1.1fr_1fr] gap-5 mt-1" style="font-size:17px">
<div>

<strong>【目標】</strong>3 版文案＋1 張圖＋授權清單<br>
<strong>【輸入與輸出】</strong>規格字串 → 文案字串；英文提示詞 → 512×512 PNG<br>
<strong>【限制】</strong>免費 T4、fp16、4 步、seed 42；不提他牌<br>
<strong>【驗收】</strong>「先寫好驗收清單」那頁的四項；同 seed 兩張圖像素差 ＝ 0

</div>
<div>

<div class="steps" style="font-size:17px">
  <div><span class="num">1</span>依序執行，遇到 <code># TODO</code> 自己填（或請 Agent 填，再逐行讀懂）</div>
  <div><span class="num">2</span>三個 TODO（Part A、B、D）的寫法在「三個步驟寫文案」、「一張產品情境圖」、「為什麼每次文案都不一樣？」三頁</div>
  <div><span class="num">3</span>每格跑完先看輸出，再往下</div>
</div>

<div class="muted mt-2" style="font-size:16px">沒有 Agent 額度：照上面三頁的程式填。卡住：打開解答筆記本 <code class="nw">lab02-genai-tour-solution.ipynb</code>。</div>

</div>
</div>

<!--
★ Specify（4 分）：Part A–D 學員在第 8–17 頁已經邊聽邊跑，這頁只對照【目標】【輸入與輸出】【限制】【驗收】，確認每一格都跑過、TODO 都填好。第一次下載 SD1.5 的等待放在第 9 頁。VRAM 峰值 4.56 GB（2026-11-26 T4）；整本時間待實測。
-->

---

<div class="eyebrow">04 · Lab L1-2</div>

# Lab 4／4：Audit → Iterate，然後交付

<table style="font-size:17px">
<thead><tr><th style="width:30%">稽核問題</th><th>具體動作</th><th style="width:28%">應該是</th></tr></thead>
<tbody>
<tr><td>字數 ≤ 80？規格對嗎？</td><td>看印出的字數；對照「續航 30 小時」</td><td>常常不過：改提示、調低 max_new_tokens，或挑一版再人工修</td></tr>
<tr><td>有沒有簡體字？</td><td>逐字看；或請 AI 助手列出所有簡體字</td><td>小模型常混進簡體字，要改掉</td></tr>
<tr><td>圖有沒有商標或文字？</td><td>放大看圖</td><td>沒有；有就換 seed</td></tr>
<tr><td>能重現嗎？</td><td>看「最大像素差」</td><td>0（T4 實跑）</td></tr>
<tr><td>能商用嗎？</td><td>最後一格印出 license</td><td>讀出來的值，不憑記憶</td></tr>
</tbody>
</table>

<div class="node node--primary mt-3" style="font-size:17px"><strong>Ship</strong>：<code>outputs/</code> 裡的 <code>copies.txt</code>、<code>product_seed42.png</code>，加上一行授權與 seed 紀錄</div>

<div class="takeaway mt-2">最常見的錯：文案把規格寫錯（小模型的幻覺）——所以第 1 項一定要人工核對。</div>

<!--
★ 稽核（5 分）：請學員找出至少一個規格錯誤，改提示詞（例如「只能使用規格裡的數字」）再跑一次，比較。
-->

---

<div class="eyebrow">05 · Measure & Risk</div>

# 風險：提示詞隱私與生成物歸屬

<div class="grid grid-cols-2 gap-6 mt-3" style="font-size:18px">
<div class="node node--warm"><strong>提示詞會送到哪裡？</strong><small>Gemini 免費方案會把提示詞用於改進產品（付費方案不會）→ 不要放個資、未公開規格</small></div>
<div class="node node--warm"><strong>生成的圖與文，誰擁有？</strong><small>各國看法不同，台灣著作權法對 AI 生成物的保護仍在討論 → 重要素材保留人工修改紀錄</small></div>
</div>

<div class="takeaway mt-6">開放模型在自己的 GPU 跑，資料不出門；用 API 前先讀服務條款。</div>

<div class="src">Gemini 免費方案：Pricing 頁「Used to improve our products：Yes」（S10）；著作權部分見 S7（待確認，以官方文字為準）</div>

<!--
★ 風險（3 分）：不要給法律意見，只給工程師的行為規則：不放個資、讀條款、留紀錄。D6-3 的上市檢查會再完整處理。
-->

---

<div class="eyebrow">總整理</div>

# 今天學到的概念鏈

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-4">
  <span class="chip">開 T4</span><span class="arrow">→</span>
  <span class="chip">pipeline 文案</span><span class="arrow">→</span>
  <span class="chip">SD1.5 產品圖</span><span class="arrow">→</span>
  <span class="chip">雲端 API＋金鑰</span><span class="arrow">→</span>
  <span class="chip">logit→softmax 機率</span><span class="arrow">→</span>
  <span class="chip">溫度</span><span class="arrow">→</span>
  <span class="chip">seed</span><span class="arrow">→</span>
  <span class="chip">授權</span>
</div>

<div class="takeaway mt-6">生成＝從機率分布抽樣；溫度改形狀、seed 固定抽籤，交付時記下設定與授權。</div>

<!--
★ 總整理（1 分）。
-->

---

<div class="eyebrow">隨堂檢核</div>

# 隨堂檢核 1／3（iPAS 題型）：點選答案

<Mcq id="quiz1.q1" :n="1" :answer="1"
  :options="['更多樣', '更穩定、更重複', '變成英文', '速度變快十倍']"
  :why="['相反：T 變小，分數差距被放大，第一名的機率更高，所以更不多樣。', '', '溫度只改變機率的形狀，不會換語言。', '溫度不影響計算量，速度幾乎一樣。']"
  explain="T 小 → 分數除以小數字，差距變大 → 幾乎只抽第一名，所以穩定但重複。">
把溫度 T 從 1.0 調到 0.2，文字輸出通常會？
</Mcq>

<Mcq id="quiz1.q2" :n="2" :answer="1"
  :options="['提高畫質', '讓結果可以重現', '降低記憶體', '避免商標']"
  :why="['畫質看模型和步數，seed 只決定抽到哪一組亂數。', '', 'seed 不影響記憶體用量。', '要避免商標得靠人工看圖、換 seed，seed 本身不會過濾商標。']"
  explain="固定 seed＝固定亂數的起點，同樣設定就抽到同一組亂數，得到同一張圖。">
固定 seed 的主要目的？
</Mcq>

<FillClear group="quiz1" corner />

<!--
★ 檢核 1／3（2 分）：學員自己點；點錯會出現「再想想」和錯在哪，可以再點一次。答案：1 B、2 B。
-->

---

<div class="eyebrow">隨堂檢核</div>

# 隨堂檢核 2／3（iPAS 題型）：點選答案

<Mcq id="quiz2.q3" :n="3" :answer="1"
  :options="['ReLU', 'softmax', 'MSE', 'sigmoid 後再相加']"
  :why="['ReLU 只把負數變 0，結果加起來不會等於 1。', '', 'MSE 是損失函數，用來訓練，不是把分數變機率。', '每個 sigmoid 各自在 0–1，但全部加起來不保證是 1。']"
  explain="softmax 讓每個值都在 0–1 之間，而且全部加起來剛好 1，才能拿來抽籤。">
模型輸出的 logits 經過哪個函式變成機率？
</Mcq>

<Mcq id="quiz2.q4" :n="4" :answer="2"
  :options="['看下載次數', '問同學', '讀模型卡的授權欄位與授權全文', '看模型大小']"
  :why="['下載次數多不代表能商用。', '同學的記憶可能錯，授權也可能改過。', '', '模型大小和授權無關。']"
  explain="授權寫在模型卡上（筆記本最後一格直接讀出來）；重要用途再讀授權全文。">
判斷一個模型能不能商用，最可靠的做法？
</Mcq>

<FillClear group="quiz2" corner />

<!--
★ 檢核 2／3（2 分）。答案：3 B、4 C。
-->

---

<div class="eyebrow">隨堂檢核</div>

# 隨堂檢核 3／3（iPAS 題型）：點選答案

<Mcq id="quiz3.q5" :n="5" :answer="1"
  :options="['Part A：pipeline 跑 Qwen', 'Part C：呼叫 Gemini API', 'Part B：DiffusionPipeline 產生圖', 'Part B：固定 seed 再跑一次']"
  :why="['Qwen 的權重下載到你的 T4，在你的機器上算，提示詞不會送到廠商。', '', '影像模型也在你的 T4 上算，資料不出去。', 'seed 只是固定亂數，不會把資料送出去。']"
  explain="呼叫 API 時，模型在廠商的伺服器；提示詞會透過網路送到 Google，所以不要放個資。">
哪一步會把提示詞送到廠商的伺服器？
</Mcq>

<Mcq id="quiz3.q6" :n="6" :answer="2"
  :options="['直接寫在程式碼裡', 'Colab 網頁版的密鑰（userdata.get）', '寫進 .env，再對它按右鍵 Upload to Colab', '貼在筆記本的文字格']"
  :why="['程式碼會被分享、上傳，金鑰就外流了。', 'VS Code 連 Colab 不支援 userdata.get，會直接出錯。', '', '文字格和程式碼一樣會被分享。']"
  explain="VS Code 連 Colab 只能用 .env：上傳到伺服器，load_dotenv() 讀進環境變數，程式只寫金鑰的名字。">
用 VS Code 連 Colab 跑 Part C，Gemini 金鑰應該怎麼給程式？
</Mcq>

<FillClear group="quiz3" corner />

<!--
★ 檢核 3／3（2 分）。答案：5 B、6 C。對應學習目標 2（呼叫雲端 LLM、金鑰不寫在程式裡）。
-->

---
hostOnly: true
---

<div class="eyebrow">下一步</div>

# 下一堂 D1-3：從 Keras 到 PyTorch

<div class="node node--primary mt-2">今天用的 transformers、diffusers 都是 PyTorch。下一堂把你在 DL 課跑過的 CIFAR-10 CNN 從 Keras 搬到 PyTorch，自己寫訓練迴圈。</div>

<!--
★ 只給講師的託管版看。請學員回家把 lab02 跑完並存檔。
-->
