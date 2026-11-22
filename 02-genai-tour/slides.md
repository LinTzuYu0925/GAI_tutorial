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

<div class="chain flex flex-nowrap items-center gap-2 mt-8">
  <span class="chip">開 T4</span><span class="arrow">→</span>
  <span class="chip">文案</span><span class="arrow">→</span>
  <span class="chip">產品圖</span><span class="arrow">→</span>
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

1. **執行**文字生成 `pipeline` 與 fp16 的 `DiffusionPipeline`（Colab T4）
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

<div class="eyebrow">01 · Try（先用現成的）</div>

# 打開 T4：先確認 GPU 真的在

<div class="grid grid-cols-[1fr_1.15fr] gap-6 mt-2">
<div class="steps">
  <div><span class="num">1</span>功能表「執行階段」→「變更執行階段類型」</div>
  <div><span class="num">2</span>硬體加速器選 <strong>T4 GPU</strong> → 儲存</div>
  <div><span class="num">3</span>執行第 1 格，看印出的 GPU 名稱</div>
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

<div class="takeaway mt-4">先看到 True 再往下做；False 代表在 CPU 上，影像模型會非常慢。</div>

<div class="src">回顧：ML pp.5–6（Colab 執行階段）</div>

<!--
★ T4（3 分）：大家一起做。常見狀況：GPU 額度用完 → 筆記本會印出「沒有 GPU」，Part A、D 仍可在 CPU 跑，Part B 看解答筆記本的已存輸出。
-->

---

<div class="eyebrow">01 · Try · 文字</div>

# 三行程式寫文案：<code>pipeline</code>

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

<div class="muted mt-1" style="font-size:16px"><code>messages</code>：system 給角色，user 給規格與任務（筆記本 Part A）</div>

</div>
<div>

<div class="placeholder" style="height:200px">三版文案（字數）<small>講師在 Colab T4 實跑後替換</small></div>

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
    torch_dtype=torch.float16).to("cuda")
pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
pipe.load_lora_weights("latent-consistency/lcm-lora-sdv1-5")
g = torch.Generator("cuda").manual_seed(42)
img = pipe(PROMPT, num_inference_steps=4,
           guidance_scale=1.0, generator=g).images[0]
```

</div>
<div>

<div class="placeholder" style="height:230px">512×512 產品圖<small>講師實跑後替換（SD1.5＋LCM-LoRA，seed 42，4 步）</small></div>

</div>
</div>

<div class="takeaway mt-3">LCM-LoRA 是一個「加速外掛」：原本要幾十步的模型，4 步就出圖。</div>

<div class="src">S3、S4；為什麼能變快在 D4-4 說明，今天只會用</div>

<!--
★ 影像（6 分）：只解釋三個參數：num_inference_steps（幾步）、guidance_scale（LCM 用 1.0）、generator（seed）。
LoRA 是什麼在 D4-3；擴散模型怎麼運作在 D3-3。今天的重點是「能跑、能重現」。
-->

---

<div class="eyebrow">01 · Try · 雲端 API</div>

# 第一次呼叫雲端 LLM：金鑰不進程式碼

<div class="grid grid-cols-[1.3fr_1fr] gap-5 mt-1">
<div>

```python
key = userdata.get("ANTHROPIC_API_KEY")  # Colab 密鑰
client = anthropic.Anthropic(api_key=key)
msg = client.messages.create(
    model="claude-opus-5-5", max_tokens=1024,
    system=SYSTEM, messages=[{"role": "user",
                              "content": TASK}])
print("".join(b.text for b in msg.content
              if b.type == "text"))  # 只取文字區塊
```

</div>
<div style="font-size:18px">

<div class="node node--warm"><strong>金鑰放哪裡</strong><small>Colab 左側 🔑 密鑰，或 <code>.env</code>（Vibe 單元 12）</small></div>

<div class="node mt-3"><strong>沒有金鑰？</strong><small>這格會印出備案訊息，改用 Part A 的開放模型</small></div>

</div>
</div>

<div class="takeaway mt-3">開放模型在你的 GPU 上跑；API 是把文字送到廠商的伺服器跑。</div>

<div class="src">Anthropic Python SDK（S5）。課堂用哪個模型與金鑰由講師決定</div>

<!--
★ 雲端 API（5 分）：連回 D1-1 的「開放權重 vs 封閉 API」。msg.usage 會印出輸入、輸出 token 數——這就是計費單位（D5-3 再算成本）。
備案：沒有金鑰的學員直接跳過，不影響後面。
-->

---

<div class="eyebrow">02 · Open（打開黑盒子）</div>

# 為什麼每次文案都不一樣？

<div class="grid grid-cols-[1fr_1fr] gap-6 mt-1 items-center">
<div>

```python
ids = tok("這款降噪耳機最大的特色是",
          return_tensors="pt")
logits = model(**ids).logits   # 每個位置一排分數
probs = softmax(logits[0, -1]) # 最後一個位置
torch.topk(probs, 5)
```

</div>
<div>

<div class="placeholder" style="height:220px">前 5 名下一個 token 與機率（長條圖）<small>講師實跑 Part D 後替換</small></div>

</div>
</div>

<div class="takeaway mt-3">模型不是給「一個答案」，而是給<strong>每一個可能的下一個 token 一個機率</strong>。</div>

<div class="src">回顧：DL pp.80–81（GPT＝猜下一個字）；Vibe 01（LLM 是 token 接龍）</div>

<!--
★ 機率（6 分）：先請學員猜：「這款降噪耳機最大的特色是」下一個字是什麼？再跑 Part D 看前 5 名。
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
<tr><td><code>do_sample=False</code></td><td>永遠選機率最高的（greedy）</td><td>每次都一樣</td></tr>
<tr><td><code>do_sample=True</code></td><td>照機率抽籤</td><td>每次不同</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">「每次不一樣」不是壞掉，是因為每一步都在抽籤。</div>

<!--
★ 抽樣（5 分）：對照 D1-1 的「從 p_θ 抽樣」：文字模型一次抽一個 token，接起來就是一段文字。
greedy 讀作「貪婪法」：每一步都拿最大的，所以沒有隨機性。
-->

---

<div class="eyebrow">02 · Open · 溫度</div>

# 溫度：把機率分布變尖或變平

<div class="grid grid-cols-[1fr_1.2fr] gap-6 mt-1 items-center">
<div style="font-size:19px">

$$p_i = \mathrm{softmax}\!\left(\frac{z_i}{T}\right)$$

- **z<sub>i</sub>**：第 i 個 token 的分數（logit）
- **T**：溫度
- **讀作**：「每個分數先除以溫度，再變成機率」

</div>
<div>

<table style="font-size:17px">
<thead><tr><th>分數 z ＝ [2, 1, 0]</th><th>T ＝ 0.5</th><th>T ＝ 1</th><th>T ＝ 2</th></tr></thead>
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
★ 溫度（6 分）：公式只有一條。用表格的手算數字說明：T=0.5 時 A 從 0.67 變 0.87（變尖），T=2 時變 0.51（變平）。
學員在 DL 課的知識蒸餾看過同一個 softmax(z/T)，那裡是為了讓學生模型看到「軟標籤」。
計算：softmax([4,2,0])=[0.867,0.117,0.016]；softmax([2,1,0])=[0.665,0.245,0.090]；softmax([1,0.5,0])=[0.506,0.307,0.186]。
-->

---

<div class="eyebrow">02 · Open · 溫度 · 練習</div>

# 練習：溫度高低，文案怎麼變？

<div class="muted" style="font-size:17px">1. 先寫預測　2. 執行筆記本 Part D 的「練習」格（每種溫度跑 3 次）　3. 填實際觀察</div>

<table class="fill vlines mt-1">
<thead><tr><th style="width:14%">溫度</th><th>我預測：3 次一樣嗎？</th><th>實際：3 次一樣嗎？</th><th>實際：通順、規格正確嗎？</th></tr></thead>
<tbody>
<tr><td>T ＝ 0.2</td><td class="blank"><FillIn id="temp.t02-pred" hint="例：幾乎一樣……" /></td><td class="blank"><FillIn id="temp.t02-same" /></td><td class="blank"><FillIn id="temp.t02-ok" /></td></tr>
<tr><td>T ＝ 1.0</td><td class="blank"><FillIn id="temp.t10-pred" /></td><td class="blank"><FillIn id="temp.t10-same" /></td><td class="blank"><FillIn id="temp.t10-ok" /></td></tr>
<tr><td>T ＝ 1.5</td><td class="blank"><FillIn id="temp.t15-pred" /></td><td class="blank"><FillIn id="temp.t15-same" /></td><td class="blank"><FillIn id="temp.t15-ok" hint="例：開始出現……" /></td></tr>
<tr><td>你的 GPU</td><td class="blank" colspan="3"><FillIn id="temp.gpu" hint="例：Tesla T4……" /></td></tr>
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
<tr><td>T ＝ 0.2</td><td>幾乎一樣（可能完全相同）</td><td>通順，但句型重複</td></tr>
<tr><td>T ＝ 1.0</td><td>每次不同</td><td>大多通順，偶爾規格寫錯</td></tr>
<tr><td>T ＝ 1.5</td><td>差異很大</td><td>開始出現怪詞、簡體字或規格錯誤</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">怎麼判斷：趨勢對就對——T 越高，多樣性上升、可靠度下降。實際句子以講師實跑為準（research/lab-runs.md）。</div>

<!--
★ 解答（2 分）：這是預期趨勢；講師實跑後，把一組真實輸出貼到講者備註當例子。
-->

---

<div class="eyebrow">03 · Adapt（調成我們的）</div>

# seed：讓「隨機」可以重現

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
<div class="node node--warm mt-3"><strong>可能不同</strong><small>換 GPU、換版本、換步數，同一個 seed 也可能出不同的圖</small></div>

</div>
</div>

<div class="takeaway mt-3">交付時記錄 seed、步數、模型與版本，別人才能重做出同一張圖。</div>

<div class="src">PyTorch Reproducibility 說明（S6）</div>

<!--
★ seed（5 分）：筆記本 Part B 會用同一個 seed 跑兩次，印出最大像素差；預期是 0（講師實跑確認）。
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

<div class="takeaway mt-4">負面提示詞幫忙守住驗收第 2 項（沒有他牌商標），但仍然要人工看圖。</div>

<div class="src">D4-2 會解釋它為什麼有用（和 guidance 有關）</div>

<!--
○ 負面提示（2 分）：注意：LCM 搭配 guidance_scale=1.0 時，負面提示的效果有限（待講師實跑確認）；D4-2 用一般取樣再比較。
-->

---

<div class="eyebrow">04 · Lab L1-2</div>

# Lab 1／4：我們要生成什麼？

<div class="grid grid-cols-2 gap-6 mt-2" style="font-size:19px">
<div>

**打開筆記本**：`materials/lab02-genai-tour.ipynb` → Open in Colab<br>
執行階段：**T4 GPU**<br>
資料：一段虛構產品規格（筆記本裡）

1. 三版文案，哪一版你敢直接上架？
2. 圖裡有沒有不該出現的東西？
3. 再跑一次，圖還一樣嗎？

</div>
<div>

<div class="placeholder" style="height:250px">目標：3 版文案＋1 張圖＋授權清單<small>講師實跑後換成真實輸出</small></div>

</div>
</div>

<div class="takeaway mt-3">這就是四個檢查點的 ① 目標。</div>

<!--
★ Lab 開始（3 分）。備案：沒有 GPU 額度 → 打開 lab02-genai-tour-solution.ipynb 看已存輸出；Part A、D 也能在 CPU 跑（慢）。
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
★ 拆塊（4 分）：文字那一列是今天的重點，下一頁要填每一塊的輸入輸出。影像那一列只是預告：U-Net 在 D2-2、VAE 在 D2-3、擴散在 D3-3。
-->

---

<div class="eyebrow">04 · Lab L1-2 · 練習</div>

# 練習：每一塊的輸入與輸出

<div class="muted" style="font-size:17px">先不用 AI、不用執行，自己預測；之後用 Part D 的 <code>print</code> 對答案。n ＝ 提示詞的 token 數</div>

<table class="fill vlines mt-1">
<thead><tr><th style="width:18%">塊</th><th>輸入</th><th>輸出（型別或 shape）</th><th>做什麼（一句話）</th></tr></thead>
<tbody>
<tr><td>tokenizer</td><td>字串</td><td><code>input_ids</code>：[1, n]</td><td>把文字切成 token ID</td></tr>
<tr><td>model</td><td class="blank"><FillIn id="io.model-in" hint="例：一排整數……" /></td><td class="blank"><FillIn id="io.model-out" hint="例：幾維、每維多大……" /></td><td class="blank"><FillIn id="io.model-do" /></td></tr>
<tr><td>取最後位置＋softmax</td><td class="blank"><FillIn id="io.sm-in" /></td><td class="blank"><FillIn id="io.sm-out" /></td><td class="blank"><FillIn id="io.sm-do" /></td></tr>
<tr><td>抽樣</td><td class="blank"><FillIn id="io.samp-in" /></td><td class="blank"><FillIn id="io.samp-out" /></td><td class="blank"><FillIn id="io.samp-do" /></td></tr>
</tbody>
</table>

<FillClear group="io" />

<!--
★ 無 AI 檢核點（8 分）：第一列已填好當示範。提示：vocab_size 是詞彙表大小，學員可以先寫「詞彙表大小」，跑完 Part D 再填數字。
-->

---
hostOnly: true
---

<div class="eyebrow">04 · Lab L1-2 · 練習解答</div>

# 練習解答：每一塊的輸入與輸出

<table class="vlines" style="font-size:18px">
<thead><tr><th style="width:18%">塊</th><th>輸入</th><th>輸出</th><th>做什麼</th></tr></thead>
<tbody>
<tr><td>tokenizer</td><td>字串</td><td><code>input_ids</code>：[1, n]</td><td>把文字切成 token ID</td></tr>
<tr><td>model</td><td><code>input_ids</code> [1, n]</td><td><code>logits</code> [1, n, vocab_size]</td><td>每個位置對每個 token 打分數</td></tr>
<tr><td>最後位置＋softmax</td><td><code>logits[0, -1]</code> [vocab_size]</td><td>機率 [vocab_size]，總和 1</td><td>分數變機率</td></tr>
<tr><td>抽樣</td><td>機率 [vocab_size]</td><td>1 個 token ID</td><td>照機率抽一個</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">怎麼對答案：Part D 印出 <code>input_ids shape</code>、<code>logits shape</code> 與 <code>vocab_size</code>；數字以實跑為準。</div>

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
<strong>【驗收】</strong>第 4 頁的四項；同 seed 兩張圖像素差 ＝ 0

</div>
<div>

<div class="steps" style="font-size:17px">
  <div><span class="num">1</span>依序執行，遇到 <code># TODO</code> 自己填（或請 Agent 填，再逐行讀懂）</div>
  <div><span class="num">2</span>三個 TODO（Part A、B、D）的寫法在投影片第 6、7、9 頁</div>
  <div><span class="num">3</span>每格跑完先看輸出，再往下</div>
</div>

<div class="muted mt-2" style="font-size:16px">沒有 Agent 額度：照第 6、7、9 頁的程式填。卡住：打開 <code>-solution.ipynb</code>。</div>

</div>
</div>

<!--
★ Specify＋執行（約 20 分，含等待下載）：第一次下載 SD1.5 需要幾分鐘（時間待實測），請學員先跑 Part B 的下載格，等待時做 Part A。
-->

---

<div class="eyebrow">04 · Lab L1-2</div>

# Lab 4／4：Audit → Iterate，然後交付

<table style="font-size:17px">
<thead><tr><th style="width:30%">稽核問題</th><th>具體動作</th><th style="width:28%">應該是</th></tr></thead>
<tbody>
<tr><td>字數 ≤ 80？規格對嗎？</td><td>看印出的字數；對照「續航 30 小時」</td><td>三版都過，或改提示再跑</td></tr>
<tr><td>圖有沒有商標或文字？</td><td>放大看圖</td><td>沒有；有就換 seed</td></tr>
<tr><td>能重現嗎？</td><td>看「最大像素差」</td><td>0（講師實跑確認）</td></tr>
<tr><td>能商用嗎？</td><td>最後一格印出 license</td><td>讀出來的值，不憑記憶</td></tr>
</tbody>
</table>

<div class="node node--primary mt-3" style="font-size:17px"><strong>Ship</strong>：<code>outputs/</code> 裡的 <code>copies.txt</code>、<code>product_seed42.png</code>，加上一行授權與 seed 紀錄</div>

<div class="takeaway mt-2">最常見的錯：文案把規格寫錯（小模型的幻覺）——所以第 1 項一定要人工核對。</div>

<!--
★ 稽核（8 分）：請學員找出至少一個規格錯誤，改提示詞（例如「只能使用規格裡的數字」）再跑一次，比較。
-->

---

<div class="eyebrow">05 · Measure & Risk</div>

# 風險：提示詞隱私與生成物歸屬

<div class="grid grid-cols-2 gap-6 mt-3" style="font-size:18px">
<div class="node node--warm"><strong>提示詞會送到哪裡？</strong><small>免費方案的服務條款可能允許把提示詞用於改進服務 → 不要放個資、未公開規格</small></div>
<div class="node node--warm"><strong>生成的圖與文，誰擁有？</strong><small>各國看法不同，台灣著作權法對 AI 生成物的保護仍在討論 → 重要素材保留人工修改紀錄</small></div>
</div>

<div class="takeaway mt-6">開放模型在自己的 GPU 跑，資料不出門；用 API 前先讀服務條款。</div>

<div class="src">具體條款與法規見 research/sources.md S7（待確認，以官方文字為準）</div>

<!--
★ 風險（4 分）：不要給法律意見，只給工程師的行為規則：不放個資、讀條款、留紀錄。D6-3 的上市檢查會再完整處理。
-->

---

<div class="eyebrow">總整理</div>

# 今天學到的概念鏈

<div class="chain flex flex-nowrap items-center gap-2 mt-4">
  <span class="chip">開 T4</span><span class="arrow">→</span>
  <span class="chip">pipeline 文案</span><span class="arrow">→</span>
  <span class="chip">SD1.5 產品圖</span><span class="arrow">→</span>
  <span class="chip">下一個 token 機率</span><span class="arrow">→</span>
  <span class="chip">溫度</span><span class="arrow">→</span>
  <span class="chip">seed</span><span class="arrow">→</span>
  <span class="chip">授權</span>
</div>

<div class="takeaway mt-6">生成＝從機率分布抽樣；溫度改形狀、seed 固定抽籤，交付時記下設定與授權。</div>

<!--
★ 總整理（2 分）。
-->

---

<div class="eyebrow">隨堂檢核</div>

# 選擇題（iPAS 題型）

<div class="mcq">

1. 把溫度 T 從 1.0 調到 0.2，文字輸出通常會？（　）<br><span class="opts">(A) 更多樣　(B) 更穩定、更重複　(C) 變成英文　(D) 速度變快十倍</span>
2. 固定 seed 的主要目的？（　）<br><span class="opts">(A) 提高畫質　(B) 讓結果可以重現　(C) 降低記憶體　(D) 避免商標</span>
3. 模型輸出的 <code>logits</code> 經過哪個函式變成機率？（　）<br><span class="opts">(A) ReLU　(B) softmax　(C) MSE　(D) sigmoid 後再相加</span>
4. 判斷一個模型能不能商用，最可靠的做法？（　）<br><span class="opts">(A) 看下載次數　(B) 問同學　(C) 讀模型卡的授權欄位與授權全文　(D) 看模型大小</span>

</div>

<!--
★ 檢核（4 分）。答案：1 (B)、2 (B)、3 (B)、4 (C)。
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
