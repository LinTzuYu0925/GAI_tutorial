---
theme: default
title: 斷線不怕、主管點得到
info: |
  生成式AI原理 · D1-4
  Drive 檢查點與續訓、Hugging Face Hub、VRAM 估算、T4 注意事項、Gradio 展示（第一天的交付）。
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
exportFilename: 04-colab-hub-gradio
layout: center
class: cover
---

<div class="eyebrow">生成式AI原理 · D1-4</div>

# 斷線不怕、主管點得到

<p class="subtitle">檢查點、Hugging Face Hub、VRAM 估算，最後做出一個能點的網頁</p>

<div class="chain flex flex-nowrap items-center gap-2 mt-8">
  <span class="chip">Colab 限制</span><span class="arrow">→</span>
  <span class="chip">檢查點與續訓</span><span class="arrow">→</span>
  <span class="chip">Hub 與模型卡</span><span class="arrow">→</span>
  <span class="chip">VRAM 估算</span><span class="arrow">→</span>
  <span class="chip">Gradio</span>
</div>

<!--
★ 開場（2 分）：今天第一天的最後一堂，要交出第一個「能點的東西」。這一堂的技巧（檢查點、VRAM、Gradio）每一天都會用到。
-->

---

<div class="eyebrow">00 · Frame（定義問題）</div>

# 資訊部：白訓練一天，主管只看到截圖

<div class="ticket mt-2">
  <div class="ticket-head">【需求單 #D1-4】部門：資訊部<span>公司：曜嶼電子 <span class="fiction" style="color:#fff;border-color:#fff">虛構</span></span></div>
  <dl>
    <dt>問題</dt><dd>訓練到一半 Colab 斷線就全部重來；主管想要自己點得到的展示</dd>
    <dt>現況痛點</dt><dd>上週白訓練一天；成果只有截圖</dd>
    <dt>成功指標（KPI）</dt><dd>斷線後從最後一個 epoch 接著訓練；給主管一個能上傳圖片的網址</dd>
    <dt>可用資料</dt><dd>D1-3 的 CIFAR-10 分類器</dd>
    <dt>限制與法規</dt><dd>免費 Colab（連線時間、閒置中斷、GPU 額度都有限）；模型授權</dd>
    <dt>為何現有工具不夠</dt><dd>模型只在記憶體裡，斷線就沒了；筆記本不是給主管用的介面</dd>
  </dl>
</div>

<!--
★ 需求單（2 分）。
-->

---

<div class="eyebrow">學習目標</div>

# 今天結束時，你能夠……

1. **存與接續**訓練：檢查點存到 Drive（模型＋優化器＋epoch）
2. **說明**模型倉庫裡有什麼，以及為什麼用 safetensors 而不是 pickle
3. **估算** VRAM（參數 × 位元組），並**實測**一個模型的 fp32 與 fp16
4. **處理** CUDA out of memory
5. **交付**一個 Gradio 網頁（第一天的成品）

<!--
★ 目標（1 分）。不教：HF Spaces 部署（D6-3）、量化（D5-3）。
-->

---

<div class="eyebrow">00 · Frame</div>

# 免費 Colab 的三個限制

<div class="grid grid-cols-3 gap-4 mt-4" style="font-size:18px">
<div class="node node--warm"><strong>連線時間有上限</strong><small>一次連線最長數小時，時間到就中斷</small></div>
<div class="node node--warm"><strong>閒置會中斷</strong><small>一段時間沒有互動，執行階段被回收</small></div>
<div class="node node--warm"><strong>GPU 不保證</strong><small>額度用完或尖峰時段，可能拿不到 T4</small></div>
</div>

<div class="takeaway mt-6">斷線時，記憶體裡的變數和模型全部消失；只有存到 Drive 的檔案會留下。</div>

<div class="src">實際時間與額度依 Colab 官方說明，會變動（research/sources.md S1，待確認）。回顧：ML pp.5–6、DL pp.34–35</div>

<!--
★ 限制（3 分）：不要背數字，Colab 會改。重點是：任何超過幾分鐘的訓練，都要存檔。
備案：GPU 額度用完時用 Kaggle（roadmap §1）。
-->

---

<div class="eyebrow">01 · Adapt（調成我們的）· 檢查點</div>

# 檢查點要存三樣：權重、優化器、epoch

<div class="grid grid-cols-[1.25fr_1fr] gap-5 mt-1">
<div>

```python
drive.mount("/content/drive")
CKPT = "/content/drive/MyDrive/GAI/ckpt/cifar_cnn_ckpt.pt"

torch.save({"epoch": epoch,
            "model": model.state_dict(),
            "optimizer": optimizer.state_dict(),
            "history": history}, CKPT)
```

</div>
<div style="font-size:18px">

- **model**：權重（D1-3 學過）
- **optimizer**：Adam 的動量；沒存，接續時像重新起步
- **epoch**：知道從哪裡接
- 每個 epoch 結束就存一次

</div>
</div>

<div class="takeaway mt-3">只存權重＝能用模型；存三樣＝能接著訓練。</div>

<!--
★ 存檔（5 分）：比較 D1-3 只存 state_dict。Drive 授權視窗會跳出來，請學員用自己的帳號。
-->

---

<div class="eyebrow">01 · Adapt · 續訓</div>

# 斷線後：載入檢查點，從下一個 epoch 接著跑

<div class="flex items-center gap-2 mt-3" style="font-size:18px">
  <div class="node">epoch 1 ✓<small>已存</small></div><span class="arrow">→</span>
  <div class="node">epoch 2 ✓<small>已存</small></div><span class="arrow">→</span>
  <div class="node node--warm node--dashed">epoch 3 ✗<small>斷線</small></div><span class="arrow">→</span>
  <div class="node node--primary">重新連線<small>載入檢查點</small></div><span class="arrow">→</span>
  <div class="node node--primary">epoch 3 起<small>接著跑</small></div>
</div>

```python
if os.path.exists(CKPT):
    ck = torch.load(CKPT, map_location=device)
    model.load_state_dict(ck["model"])
    optimizer.load_state_dict(ck["optimizer"])
    start_epoch = ck["epoch"] + 1
for epoch in range(start_epoch, EPOCHS + 1): ...
```

<div class="takeaway mt-2">斷線最多損失「一個 epoch」，不是一整天。</div>

<!--
★ 續訓（5 分）：筆記本用 STOP_AFTER=2 模擬斷線，第二次執行改成 None，應該印出「從 epoch 3 接著訓練」。
-->

---

<div class="eyebrow">02 · Try（先用現成的）· Hub</div>

# <code>from_pretrained</code>：一行下載別人訓練好的模型

```python
from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct",
                                             dtype=torch.float16)
```

<div class="grid grid-cols-2 gap-4 mt-4" style="font-size:18px">
<div class="node"><strong>"Qwen/Qwen2.5-0.5B-Instruct"</strong><small>「組織／模型名稱」：Hugging Face Hub 上的倉庫</small></div>
<div class="node"><strong>第一次下載、之後讀快取</strong><small>存在 <code>~/.cache/huggingface</code>，斷線後要重下</small></div>
</div>

<div class="takeaway mt-4">Hugging Face Hub 就像「放模型的 GitHub」。</div>

<!--
★ Hub（4 分）：D1-2 的 pipeline 背後就是 from_pretrained。整班同一個 IP 下載容易被限速，所以課前準備要求每人登入 HF 帳號。
-->

---

<div class="eyebrow">02 · Open（打開黑盒子）· 模型倉庫</div>

# 模型倉庫裡有什麼？

<div class="grid grid-cols-[1fr_1.2fr] gap-6 mt-2">
<div>

```text
Qwen/Qwen2.5-0.5B-Instruct
├── config.json
├── model.safetensors
├── tokenizer.json …
├── generation_config.json
└── README.md   ← 模型卡
```

</div>
<div style="font-size:18px">

- **config.json**：架構設定（幾層、多寬）
- **model.safetensors**：權重（一堆數字）
- **tokenizer**：怎麼切 token
- **README.md（模型卡）**：用途、限制、**授權**

</div>
</div>

<div class="takeaway mt-3">架構（config）＋權重（safetensors）＝能用的模型；授權寫在模型卡。</div>

<div class="src">實際檔案清單由筆記本 <code>list_repo_files</code> 印出，以實跑為準</div>

<!--
★ 倉庫（4 分）：左邊是示意，筆記本 Part B 第一格會印出真的清單。
-->

---

<div class="eyebrow">02 · Open · 安全</div>

# 為什麼用 safetensors，不用 pickle？

<div class="grid grid-cols-2 gap-6 mt-4" style="font-size:18px">
<div class="node node--warm"><strong>pickle（.bin、.pt 的傳統格式）</strong><small>載入時可以執行任意程式碼 → 下載來路不明的檔案有風險</small></div>
<div class="node node--primary"><strong>safetensors</strong><small>只存數字和 shape，載入時不執行程式碼，而且讀取快</small></div>
</div>

<div class="takeaway mt-6">別人的模型優先選 safetensors；自己的檢查點用 <code>torch.load</code> 時只載自己存的檔案。</div>

<div class="src">回顧：Vibe 12（pickle 的風險）；safetensors 文件（S4）</div>

<!--
★ 安全（3 分）：新版 PyTorch 的 torch.load 預設 weights_only=True，會擋下大部分可執行內容（版本細節待確認）。
-->

---

<div class="eyebrow">03 · Measure（量化驗收）· VRAM</div>

# VRAM 估算：參數量 × 每個參數的位元組

<div class="grid grid-cols-[1fr_1.1fr] gap-6 mt-2 items-center">
<div style="font-size:20px">

$$\text{權重記憶體} \approx N \times b$$

- **N**：參數量
- **b**：每個參數幾個位元組（fp32 ＝ 4，fp16 ＝ 2）

</div>
<div>

<table style="font-size:18px">
<thead><tr><th>例：0.5B 參數</th><th>計算</th><th>權重</th></tr></thead>
<tbody>
<tr><td>fp32</td><td>0.5 × 10⁹ × 4 B</td><td>2 GB</td></tr>
<tr><td>fp16</td><td>0.5 × 10⁹ × 2 B</td><td>1 GB</td></tr>
</tbody>
</table>

</div>
</div>

<div class="takeaway mt-4">這只是權重；訓練還要梯度、優化器狀態、中間結果，實際會大好幾倍。</div>

<!--
★ VRAM（5 分）：0.5B 讀作「五億」。1 GB 這裡取 10⁹ 位元組。推論時大約是權重再加一些；訓練時 Adam 要再存兩份狀態＋梯度。
-->

---

<div class="eyebrow">03 · Measure · VRAM · 練習</div>

# 練習：T4（16 GB）跑得動嗎？

<div class="muted" style="font-size:17px">用上一頁的公式手算權重大小；最後一欄寫「可以／勉強／不行」並說一句理由</div>

<table class="fill vlines mt-1">
<thead><tr><th style="width:30%">模型（題目給定參數量）</th><th>fp32 權重</th><th>fp16 權重</th><th>T4 推論跑得動嗎？</th></tr></thead>
<tbody>
<tr><td>小型 LLM，1.5B</td><td class="blank"><FillIn id="vram.a32" hint="例：?× 4……" /></td><td class="blank"><FillIn id="vram.a16" /></td><td class="blank"><FillIn id="vram.afit" /></td></tr>
<tr><td>影像 U-Net，0.86B</td><td class="blank"><FillIn id="vram.b32" /></td><td class="blank"><FillIn id="vram.b16" /></td><td class="blank"><FillIn id="vram.bfit" /></td></tr>
<tr><td>中型 LLM，7B</td><td class="blank"><FillIn id="vram.c32" /></td><td class="blank"><FillIn id="vram.c16" /></td><td class="blank"><FillIn id="vram.cfit" hint="例：權重剛好……" /></td></tr>
</tbody>
</table>

<FillClear group="vram" />

<div class="muted mt-2" style="font-size:16px">之後在筆記本 Part B 實測 0.5B 模型，看估算和實測差多少。</div>

<!--
★ 練習（8 分）：參數量是題目給的整數，方便手算（真實模型的參數量以模型卡為準）。不收回。
目的：自己發現 7B 在 fp16 的權重就 14 GB，加上其他東西就超過 16 GB → D5-3 的 4-bit 量化就是為了這個。
-->

---
hostOnly: true
---

<div class="eyebrow">03 · Measure · VRAM · 練習解答</div>

# 練習解答：7B 要等到 D5-3 的 4-bit

<table class="vlines" style="font-size:18px">
<thead><tr><th style="width:30%">模型</th><th>fp32</th><th>fp16</th><th>T4 推論</th></tr></thead>
<tbody>
<tr><td>小型 LLM，1.5B</td><td>6 GB</td><td>3 GB</td><td>可以（fp16 更寬裕）</td></tr>
<tr><td>影像 U-Net，0.86B</td><td>3.44 GB</td><td>1.72 GB</td><td>可以（還要加文字編碼器、VAE）</td></tr>
<tr><td>中型 LLM，7B</td><td>28 GB</td><td>14 GB</td><td>不行或非常勉強：權重就快滿，沒空間給其他東西</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">怎麼判斷：權重 ≤ 約一半 VRAM 才算舒服；接近上限就要量化（D5-3）。</div>

<!--
★ 解答（2 分）：這些是算術結果，不是實測。0.5B 的實測值在筆記本 Part B（講師實跑後寫進 lab-runs.md）。
-->

---

<div class="eyebrow">03 · Measure · T4</div>

# T4 的三件事

<table style="font-size:18px">
<thead><tr><th style="width:28%">項目</th><th style="width:20%">T4</th><th>所以我們……</th></tr></thead>
<tbody>
<tr><td>fp16（半精度）</td><td>✓ 支援</td><td>推論一律用 <code>torch.float16</code></td></tr>
<tr><td>bf16</td><td>✗ 沒有原生支援</td><td>看到教學用 <code>bfloat16</code>，改成 fp16（D5-4 微調特別注意）</td></tr>
<tr><td>FlashAttention-2</td><td>✗ 需要更新的 GPU</td><td>不要開 <code>attn_implementation="flash_attention_2"</code></td></tr>
</tbody>
</table>

<div class="takeaway mt-4">網路上的範例常為新 GPU 寫；搬到 T4 前先檢查這三項。</div>

<div class="src">T4 為 Turing 架構（compute capability 7.5）；FlashAttention-2 支援 Ampere 以上（S5、S6，待確認）</div>

<!--
★ T4（4 分）：學員用 AI Agent 寫程式時，Agent 常常預設 bf16 或 flash attention——這是 T4 上最常見的報錯來源。
-->

---

<div class="eyebrow">04 · Adapt · 記憶體不足</div>

# CUDA out of memory：照這個順序處理

<div class="flex items-center gap-2 mt-4" style="font-size:18px">
  <div class="node node--primary" style="width:23%"><strong>① batch 變小</strong><small>64 → 32 → 16</small></div><span class="arrow">→</span>
  <div class="node node--primary" style="width:23%"><strong>② 改 fp16</strong><small>權重少一半</small></div><span class="arrow">→</span>
  <div class="node node--primary" style="width:23%"><strong>③ 釋放記憶體</strong><small><code>del</code>、<code>gc.collect()</code>、<code>empty_cache()</code></small></div><span class="arrow">→</span>
  <div class="node node--warm" style="width:23%"><strong>④ 重新啟動</strong><small>執行階段 → 重新啟動</small></div>
</div>

```text
torch.OutOfMemoryError: CUDA out of memory. Tried to allocate … GiB.
```

<div class="takeaway mt-3">先改設定，再清記憶體，最後才重新啟動；重新啟動後從檢查點接著跑。</div>

<!--
★ OOM（4 分）：錯誤訊息只示範開頭（實際數字依狀況）。最常見原因：同一個筆記本載了兩次大模型。筆記本 measure() 示範了 del＋empty_cache。
-->

---

<div class="eyebrow">05 · Ship（交付）· 網格</div>

# 一張圖看一批樣本：matplotlib 網格

<div class="grid grid-cols-[1.2fr_1fr] gap-5 mt-1">
<div>

```python
fig, axes = plt.subplots(2, 8, figsize=(14, 4))
for ax, img, p in zip(axes.flat, x[:16], pred):
    ax.imshow(img.permute(1, 2, 0))   # CHW → HWC
    ax.set_title(CLASSES[p])
    ax.axis("off")
```

</div>
<div>

<div class="placeholder" style="height:170px">2×8 測試圖＋預測類別<small>講師實跑後替換</small></div>

</div>
</div>

<div class="takeaway mt-3">之後判斷 AE、GAN、擴散模型的好壞，第一步都是「印一張網格來看」。</div>

<div class="src">回顧：Vibe 12a（matplotlib）</div>

<!--
★ 網格（3 分）：matplotlib 要 HWC，所以要 permute 回來——D1-3 的通道順序再出現一次。
-->

---

<div class="eyebrow">05 · Ship · Gradio</div>

# Gradio：幾行做出網頁

<div class="grid grid-cols-[1.3fr_1fr] gap-5 mt-1">
<div>

```python
def predict(img):            # 收到一張 PIL 圖
    x = tf(img.convert("RGB").resize((32, 32)))
    p = torch.softmax(model(x[None].to(device)), 1)[0]
    return {CLASSES[i]: float(p[i]) for i in range(10)}

gr.Interface(fn=predict,
             inputs=gr.Image(type="pil"),
             outputs=gr.Label(num_top_classes=3)
            ).launch(share=True)
```

</div>
<div style="font-size:18px">

- **fn**：你的函式
- **inputs／outputs**：網頁元件
- <code>share=True</code>：產生一個暫時的公開網址，主管用手機也能點

</div>
</div>

<div class="takeaway mt-3">把模型包成「一個函式」，Gradio 就能把它變成網頁。</div>

<div class="src">回顧：數據代理人 pp.50–61（Plotly Dash，同樣的想法）；Gradio 文件（S7）</div>

<!--
★ Gradio（5 分）：x[None] 讀作「在最前面加一個 batch 維度」。gr.Interface 適合「一個輸入、一個輸出」；需要多個按鈕、分頁或自訂版面時改用 gr.Blocks（期末專題會用到，D6-3 示範）。分享網址的有效期限依 Gradio 版本（待確認），正式上線在 D6-3 講 HF Spaces。
-->

---

<div class="eyebrow">05 · Ship · 選修</div>

# HF 快取與磁碟空間

```bash
!nvidia-smi                       # GPU 用了多少記憶體
!du -sh ~/.cache/huggingface      # 下載的模型佔多少空間
!df -h /content                   # Colab 磁碟還剩多少
```

<div class="takeaway mt-4">模型越下載越多，Colab 磁碟會滿；用不到的模型從快取刪掉。</div>

<!--
○ 快取（2 分）：D3–D4 會下載好幾個影像模型，那時候特別有用。
-->

---

<div class="eyebrow">附錄 · 預告</div>

# HF Spaces：網頁長期掛在網路上

<div class="node mt-4" style="font-size:18px"><strong>Hugging Face Spaces</strong><small>把 Gradio 程式放上去，有一個長期網址；免費方案可能沒有 GPU（D6-3 處理）</small></div>

<div class="takeaway mt-6">課堂上預設用 Colab 的 share 網址；期末專題再考慮 Spaces。</div>

<!--
△ 備用（1 分）。
-->

---

<div class="eyebrow">06 · Lab L1-4</div>

# Lab 1／6：我們要做出什麼？

<div class="grid grid-cols-2 gap-6 mt-2" style="font-size:19px">
<div>

**打開筆記本**：`materials/lab04-checkpoint-gradio.ipynb` → Open in Colab<br>
執行階段：**T4 GPU**<br>
資料：CIFAR-10（torchvision）、Qwen2.5-0.5B-Instruct（Hub）

1. 斷線後，訓練從第幾個 epoch 接著跑？
2. 0.5B 模型 fp16 實際用了多少 VRAM？
3. 主管上傳一張貓的照片，網頁會顯示什麼？

</div>
<div>

<div class="placeholder" style="height:250px">目標：續訓紀錄＋VRAM 表＋Gradio 畫面<small>講師實跑後換成真實截圖</small></div>

</div>
</div>

<div class="takeaway mt-3">這就是四個檢查點的 ① 目標。</div>

<!--
★ Lab 開始（3 分）。備案：沒有 Drive → 自動存在 /content/ckpt；沒有 GPU → Part B 只做估算；share 網址打不開 → 用筆記本內嵌的介面。
-->

---

<div class="eyebrow">06 · Lab L1-4</div>

# Lab 2／6：拆成哪幾塊？

<div class="flex items-center gap-2 mt-4" style="font-size:17px">
  <div class="node">CKPT 檔<small>Drive</small></div><span class="arrow">→</span>
  <div class="node node--primary">載入檢查點<small>model、optimizer、epoch</small></div><span class="arrow">→</span>
  <div class="node node--primary">訓練迴圈<small>每 epoch 存檔</small></div><span class="arrow">→</span>
  <div class="node node--secondary"><code>predict(img)</code><small>一張圖 → 機率</small></div><span class="arrow">→</span>
  <div class="node node--secondary"><code>gr.Interface</code><small>網頁</small></div>
</div>

<div class="node mt-5" style="font-size:17px"><strong>Part B（獨立）</strong><small><code>measure(dtype)</code>：載入 → 量峰值 VRAM → 刪除</small></div>

<div class="takeaway mt-4">名稱和筆記本一樣：<code>CKPT</code>、<code>train_one_epoch</code>、<code>measure</code>、<code>predict</code>、<code>demo</code>。</div>

<!--
★ 拆塊（3 分）：下一頁只填 predict 的輸入輸出——那是最容易寫錯的一塊。
-->

---

<div class="eyebrow">06 · Lab L1-4 · 練習</div>

# 練習：<code>predict</code> 裡每一步的輸入與輸出

<div class="muted" style="font-size:17px">不用 AI。主管上傳一張 800×600 的照片（PIL 圖）</div>

<table class="fill vlines mt-1">
<thead><tr><th style="width:34%">步驟</th><th>輸出（型別或 shape）</th><th>為什麼需要這步</th></tr></thead>
<tbody>
<tr><td><code>img.convert("RGB").resize((32, 32))</code></td><td>PIL 圖，32×32，3 通道</td><td>和訓練資料一樣大小</td></tr>
<tr><td><code>tf(...)</code>（ToTensor）</td><td class="blank"><FillIn id="pred.tt" hint="例：[?, ?, ?]……" /></td><td class="blank"><FillIn id="pred.tt-why" /></td></tr>
<tr><td><code>.unsqueeze(0)</code></td><td class="blank"><FillIn id="pred.us" /></td><td class="blank"><FillIn id="pred.us-why" /></td></tr>
<tr><td><code>model(x)</code></td><td class="blank"><FillIn id="pred.m" /></td><td class="blank"><FillIn id="pred.m-why" /></td></tr>
<tr><td><code>softmax(..., 1)[0]</code></td><td class="blank"><FillIn id="pred.sm" /></td><td class="blank"><FillIn id="pred.sm-why" /></td></tr>
</tbody>
</table>

<FillClear group="pred" />

<!--
★ 無 AI 檢核點（7 分）：第一列已填好。不收回。下一頁是解答。
-->

---
hostOnly: true
---

<div class="eyebrow">06 · Lab L1-4 · 練習解答</div>

# 練習解答：<code>predict</code> 的每一步

<table class="vlines" style="font-size:18px">
<thead><tr><th style="width:34%">步驟</th><th>輸出</th><th>為什麼</th></tr></thead>
<tbody>
<tr><td>convert＋resize</td><td>PIL 32×32 RGB</td><td>和訓練資料一樣</td></tr>
<tr><td><code>tf(...)</code></td><td>[3, 32, 32]，0–1</td><td>CHW、和訓練時同樣的範圍</td></tr>
<tr><td><code>.unsqueeze(0)</code></td><td>[1, 3, 32, 32]</td><td>模型要一個 batch</td></tr>
<tr><td><code>model(x)</code></td><td>[1, 10]</td><td>10 類的分數</td></tr>
<tr><td><code>softmax(..., 1)[0]</code></td><td>[10]，總和 1</td><td>變成機率，拿掉 batch 維度</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">怎麼對答案：在 <code>predict</code> 裡每一步後面加 <code>print(x.shape)</code>，上傳一張圖看輸出。</div>

<!--
★ 解答（2 分）。
-->

---

<div class="eyebrow">06 · Lab L1-4</div>

# Lab 4／6：Specify

<div style="font-size:18px" class="mt-2">

<strong>【目標】</strong>可以續訓的訓練＋VRAM 實測表＋Gradio 網頁<br>
<strong>【輸入與輸出】</strong>CIFAR-10 → 檢查點檔；上傳的圖 → 前 3 名類別與機率<br>
<strong>【限制】</strong>免費 T4；檢查點存 Drive；網頁只用 <code>share=True</code>（不部署）<br>
<strong>【驗收】</strong>① 第二次執行印出「從 epoch 3 接著訓練」　② fp16 實測約為 fp32 的一半　③ 上傳任一張圖都不報錯（大小、灰階都可以）

</div>

<!--
★ Specify（3 分）：驗收③特別重要：主管會上傳各種圖（直式、灰階、PNG 透明背景），convert("RGB") 就是為了這個。
-->

---

<div class="eyebrow">06 · Lab L1-4</div>

# Lab 5／6：Generate → Execute

<PromptBox>
這個 PyTorch 筆記本有四個 # TODO，請只填這四格：<br>
① 若檢查點檔存在，載入 model、optimizer 狀態，start_epoch 設為存檔 epoch + 1<br>
② 每個 epoch 結束存檔：epoch、model、optimizer 的 state_dict、history<br>
③ 呼叫 measure(dtype) 並用「參數量 × 位元組」算估算值<br>
④ predict(img)：轉 RGB、縮成 32×32、ToTensor、加 batch 維度，回傳 {類別: 機率}<br>
不要改其他格，並逐行說明。
</PromptBox>

<div class="steps mt-2" style="font-size:17px">
  <div><span class="num">1</span>Part A 執行兩次：第一次 <code>STOP_AFTER = 2</code>，第二次改成 <code>None</code></div>
  <div><span class="num">2</span>Part B 先把練習頁的估算寫好再執行</div>
  <div><span class="num">3</span>沒有 Agent 額度：照第 5、6、10、16 頁的程式填；卡住開 <code>-solution.ipynb</code></div>
</div>

<!--
★ 執行（約 20 分）。
-->

---

<div class="eyebrow">06 · Lab L1-4</div>

# Lab 6／6：Audit → Iterate

<table style="font-size:17px">
<thead><tr><th style="width:30%">稽核問題</th><th>具體動作</th><th style="width:30%">應該是</th></tr></thead>
<tbody>
<tr><td>真的接續了嗎？</td><td>看第二次執行的第一行</td><td>「從 epoch 3 接著訓練」</td></tr>
<tr><td>優化器也接回來了嗎？</td><td>找 <code>optimizer.load_state_dict</code></td><td>有</td></tr>
<tr><td>估算 vs 實測？</td><td>看 Part B 的表</td><td>實測略大於估算（講師實跑填入）</td></tr>
<tr><td>灰階圖會不會壞？</td><td>上傳一張黑白照片</td><td>正常顯示前 3 名</td></tr>
<tr><td>網頁的預測和筆記本一致嗎？</td><td>同一張測試圖兩邊各跑一次</td><td>機率相同</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">常見錯誤：<code>predict</code> 沒呼叫 <code>model.eval()</code>，同一張圖每次機率都不一樣（Dropout 還開著）。</div>

<!--
★ 稽核（8 分）。
-->

---

<div class="eyebrow">07 · Measure & Risk</div>

# 授權家族：這個模型可以拿來賺錢嗎？

<table style="font-size:18px">
<thead><tr><th style="width:24%">授權</th><th>大意</th><th style="width:26%">本課例子</th></tr></thead>
<tbody>
<tr><td><strong>Apache-2.0、MIT</strong></td><td>寬鬆：可商用，保留授權聲明</td><td>Qwen2.5-0.5B（待確認）</td></tr>
<tr><td><strong>OpenRAIL</strong></td><td>可商用，但列出禁止的用途</td><td>SD1.5</td></tr>
<tr><td><strong>NC（非商用）</strong></td><td>只能研究、個人使用</td><td>MusicGen 權重</td></tr>
<tr><td><strong>自訂授權</strong></td><td>逐條讀；可能限制使用人數或用途</td><td>部分大型模型</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">授權寫在模型卡，而且同一家族不同大小可能不同；用之前讀，交付時寫下來。</div>

<div class="src">各模型授權以模型卡與授權全文為準（research/sources.md S8，待確認）</div>

<!--
★ 授權（4 分）：這不是法律意見；工程師的責任是「讀出來、寫下來、有疑問問法務」。roadmap §9.2：Qwen2.5 不同大小授權不同，D5 會再看。
-->

---

<div class="eyebrow">第一天總整理</div>

# 第一天：從「能做什麼」到「做出能點的東西」

<div class="chain flex flex-nowrap items-center gap-2 mt-4">
  <span class="chip">D1-1 用例畫布</span><span class="arrow">→</span>
  <span class="chip">D1-2 文字與影像生成</span><span class="arrow">→</span>
  <span class="chip">D1-3 PyTorch 迴圈</span><span class="arrow">→</span>
  <span class="chip">D1-4 檢查點＋Gradio</span>
</div>

<div class="takeaway mt-6">明天開始打開生成模型的黑盒子：先從「只看過良品」的自編碼器開始。</div>

<!--
★ 總整理（2 分）。
-->

---

<div class="eyebrow">第一天隨堂檢核</div>

# 選擇題（iPAS 題型）

<div class="mcq">

1. 下列何者是**生成**模型的輸出？（　）<span class="opts">A. 類別標籤　B. 一張新的產品圖　C. 迴歸數值　D. 混淆矩陣</span>
2. 提高溫度 T，抽樣結果會？（　）<span class="opts">A. 更穩定　B. 更多樣　C. 不變　D. 變成 greedy</span>
3. 固定 seed 是為了？（　）<span class="opts">A. 可重現　B. 更快　C. 更省記憶體　D. 提高準確率</span>
4. 1B 參數的模型以 fp16 載入，權重約多少？（　）<span class="opts">A. 0.5 GB　B. 1 GB　C. 2 GB　D. 4 GB</span>
5. 能接續訓練的檢查點至少要存？（　）<span class="opts">A. 只有權重　B. 權重、優化器狀態、epoch　C. 只有 loss　D. 訓練資料</span>
6. 標示 NC 的模型權重？（　）<span class="opts">A. 可任意商用　B. 限非商業用途　C. 只能在 GPU 用　D. 不能下載</span>

</div>

<!--
★ 檢核（5 分）。答案：1 B、2 B、3 A、4 C、5 B、6 B。第 4 題：1×10⁹×2 B ＝ 2 GB。
-->

---

<div class="eyebrow">第一天作業</div>

# 回家作業（不收回，下次上課開頭對答案）

<div class="steps mt-3">
  <div><span class="num">1</span><strong>第三張用例畫布</strong>：挑課程地圖上任一張需求單（D3–D6），填 D1-1 的八格</div>
  <div><span class="num">2</span><strong>完成移植</strong>：lab03 跑完 10 個 epoch，和 Keras 版比較準確率</div>
  <div><span class="num">3</span><strong>VRAM 實測</strong>：lab04 Part B 的表填完，換一個 1.5B 模型再量一次（記得先估算）</div>
</div>

<div class="takeaway mt-6">每一題都對應今天的一個交付物：畫布、移植、VRAM 表。</div>

<!--
★ 作業（2 分）：1.5B 模型可以用 Qwen/Qwen2.5-1.5B-Instruct（授權待確認，roadmap §9.2 提到不同大小授權可能不同——這也是作業的一部分：讀出它的授權）。
-->

---
hostOnly: true
---

<div class="eyebrow">下一步</div>

# 下一堂 D2-1：找出從沒看過的瑕疵

<div class="node node--primary mt-2">品保部 A 線的 AOI 過殺太高，新瑕疵又漏檢，而且幾乎沒有瑕疵樣本。明天用「只看過良品」的自編碼器，把重建誤差變成瑕疵分數，並交出一個 Gradio 檢測站。</div>

<!--
★ 只給講師的託管版看。
-->
