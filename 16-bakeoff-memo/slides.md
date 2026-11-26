---
theme: default
title: GAN 還是擴散？
info: |
  生成式AI原理 · L16
  技術長室要定季節性產品照編修的公司標準：同一張照片、三種方法（CycleGAN、InstructPix2Pix、SD1.5＋LCM-LoRA）比品質、速度、穩定、可控與授權；擴散怎麼變快；寫學習評量備忘錄、選期末專題。第四天總整理、小考與作業。
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
exportFilename: 16-bakeoff-memo
layout: center
class: cover
---

<div class="eyebrow">生成式AI原理 · L16</div>

# GAN 還是擴散？

<p class="subtitle">同一張照片、三種方法、一把尺：寫給技術長的備忘錄</p>

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-8">
  <span class="chip">決策準則</span><span class="arrow">→</span>
  <span class="chip">三方比賽</span><span class="arrow">→</span>
  <span class="chip">擴散怎麼變快</span><span class="arrow">→</span>
  <span class="chip">人的評分</span><span class="arrow">→</span>
  <span class="chip">備忘錄</span><span class="arrow">→</span>
  <span class="chip">期末專題</span>
</div>

<!--
★ 開場（2 分）：第三天的生成三難表，今天變成一份真正的決策文件。這是學習評量（a）「說明 Diffusion vs GAN」。
-->

---

<div class="eyebrow">00 · Frame（定義問題）</div>

# 技術長室：GAN 還是擴散？要定公司標準

<div class="ticket mt-2">
  <div class="ticket-head">【需求單 #L16】部門：技術長室<span>公司：曜嶼電子 <span class="fiction" style="color:#fff;border-color:#fff">虛構</span></span></div>
  <dl>
    <dt>問題</dt><dd>季節性產品照編修要定一個公司標準：GAN 還是擴散？能不能接近即時？</dd>
    <dt>現況痛點</dt><dd>各部門各用各的工具，品質與授權風險不一</dd>
    <dt>成功指標（KPI）</dt><dd>比較表（品質、多樣性、速度、穩定性、可控性、授權）＋一頁備忘錄</dd>
    <dt>可用資料</dt><dd>一張季節性產品照（夏天 → 改成冬天）</dd>
    <dt>限制與法規</dt><dd>Colab T4；三種方法各自的授權</dd>
    <dt>為何現有工具不夠</dt><dd>從來沒有用同一個任務、同一把尺比較過</dd>
  </dl>
</div>

<!--
★ 需求單（3 分）：前三個需求單（L09、L10、L14）各自選了工具；技術長要的是「一個標準」，所以要在同一個任務上比。
-->

---

<div class="eyebrow">學習目標</div>

# 今天結束時，你能夠……

1. **執行**同一個編修任務的三方比賽，量出秒數與 VRAM
2. **說明**擴散怎麼變快：蒸餾（LCM）、ADD、flow matching
3. **收集**個人評分，說出為什麼這裡人的評分比單一指標可靠
4. **寫出**給技術長的一頁備忘錄（學習評量 a）
5. **選定**自己的期末專題需求單

<!--
★ 目標（1 分）。不教：consistency model 的訓練、rectified flow 的數學（附錄）、DiT（L18 學完 Transformer 才講）。
-->

---

<div class="eyebrow">00 · Frame · 一把尺</div>

# 決策準則：三難，再加三項

<table class="mt-2" style="font-size:17px">
<thead><tr><th style="width:18%">準則</th><th>怎麼量</th><th style="width:34%">已經有的證據</th></tr></thead>
<tbody>
<tr><td>品質</td><td>人的評分（今天的練習）</td><td>L09 網格、L14 CLIP 分數</td></tr>
<tr><td>多樣性</td><td>同一輸入換 seed 的差異</td><td>L09、L13 同類兩兩距離</td></tr>
<tr><td>速度</td><td>秒／張（暖機後平均）</td><td>L11 取樣時間、L12 DDIM</td></tr>
<tr><td><b>穩定性</b></td><td>結果「壞掉、不能用」的比例（每種方法看 3 張）</td><td>今天的 seed 網格（訓練穩不穩是另一件事：L09）</td></tr>
<tr><td><b>可控性</b></td><td>能不能用文字、遮罩指定改哪裡</td><td>L13 CFG、L14 inpainting</td></tr>
<tr><td><b>授權</b></td><td>能不能商用</td><td>L14 OpenRAIL-M</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">公司標準不是「畫質比賽」：六項都要有證據，而且證據來自同一個任務。</div>

<!--
★ 準則（5 分）：前三列是第三天的生成三難（L09 起的三角形）；後三列是上線時才會遇到的問題。請學員拿出自己的三難表。
-->

---

<div class="eyebrow">01 · Try（先看結果）</div>

# 同一張夏天的照片，三種方法「改成冬天」

<div style="width:660px;margin:0 auto"><img class="photo" src="/lab16-bakeoff.png" alt="同一張夏天的照片：原圖、A CycleGAN、B InstructPix2Pix、C SD1.5 加 LCM-LoRA 的結果" style="width:100%;height:auto">
<div class="grid grid-cols-4 gap-2 shot-cap" style="text-align:center;font-size:14px"><div>原圖<br>（SD1.5＋LCM 4 步生成）</div><div>A：CycleGAN<br>0.12 秒／張</div><div>B：InstructPix2Pix<br>5.47 秒／張</div><div>C：SD1.5＋LCM-LoRA<br>0.65 秒／張</div></div></div>

<div class="grid grid-cols-3 gap-4 mt-3" style="font-size:16px">
<div class="node node--warm"><strong>A：GAN</strong><small>一次前向；沒有提示詞、沒有 seed</small></div>
<div class="node node--primary"><strong>B：擴散＋文字指令</strong><small>「make it winter, with snow」，20 步</small></div>
<div class="node node--primary"><strong>C：擴散，蒸餾成 4 步</strong><small>L14 的 img2img ＋ L15 的 LoRA 開關</small></div>
</div>

<div class="takeaway mt-2">先不要看別人的意見：你覺得哪一張最能用？待會在「練習：幫三張冬天照打分數」寫下來。</div>

<!--
★ 示範（5 分）：三張圖都來自 lab16 的 T4 實跑（同一張原圖、同一個 seed）。CycleGAN 是用優勝美地的風景照訓練的，從沒看過耳機：先請學員猜它會怎麼處理產品。
-->

---

<div class="eyebrow">02 · Open（打開黑盒子）· 擴散怎麼變快 1</div>

# 蒸餾：多步的老師，教出少步的學生

<div class="grid grid-cols-2 gap-6 mt-3" style="font-size:18px">
<div class="node"><strong>老師：SD1.5</strong><small>25～50 步、每步算兩次（CFG）：L14 量過每張幾秒</small></div>
<div class="node node--primary"><strong>學生：LCM（潛在一致性模型）</strong><small>學「從任何一步，直接跳到老師最後會到的地方」：4 步、不用 CFG（guidance＝1.0）</small></div>
</div>

<div class="grid grid-cols-[1fr_1.3fr] gap-6 mt-3" style="font-size:18px">
<div>

- 蒸餾：DL 課學過（大模型教小模型）；這裡是「多步教少步」
- LCM-LoRA：把這個能力存成一個 LoRA（L15），掛到 SD1.5 上就變快

</div>
<div>

```python
sd.scheduler = LCMScheduler.from_config(sd.scheduler.config)
sd.load_lora_weights(LCM_LORA)   # lcm-lora-sdv1-5
sd(prompt, num_inference_steps=4, guidance_scale=1.0)
```

<div class="muted" style="font-size:15px">讀作：換成 LCM 排程器、掛上 LCM 的 LoRA、走 4 步、不做 CFG</div>

</div>
</div>

<div class="takeaway mt-2">擴散慢，是因為步數多；蒸餾把「很多小步」壓成「幾個大步」。</div>

<div class="src">DL 課 pp.67–72（蒸餾）；Luo et al., LCM／LCM-LoRA, 2023（S2，待確認）。L02 用的就是 LCM（guidance 1.0）</div>

<!--
★ 蒸餾（5 分）：讀程式：「換成 LCM 排程器、掛上 LCM 的 LoRA、走 4 步、不做 CFG」。回扣 L02：當時 guidance_scale＝1.0、負面提示沒作用，就是因為用了 LCM。
-->

---

<div class="eyebrow">02 · Open · 擴散怎麼變快 2</div>

# ADD／Turbo：GAN 的損失又回來了

<div class="muted" style="font-size:17px">ADD＝Adversarial Diffusion Distillation（對抗式擴散蒸餾）</div>

<div class="grid items-center mt-4" style="font-size:17px;grid-template-columns:22% 4% 26% 4% 44%">
  <div class="node">雜訊＋文字</div><span class="arrow text-center">→</span>
  <div class="node node--primary"><strong>學生（1～4 步）</strong><small>擴散模型</small></div><span class="arrow text-center">→</span>
  <div class="grid gap-2">
    <div class="node"><strong>蒸餾損失</strong><small>和老師多步的結果比：內容對不對</small></div>
    <div class="node node--warm"><strong>對抗損失（L09）</strong><small>鑑別器判斷：看起來像不像真照片</small></div>
  </div>
</div>

<div style="font-size:18px" class="mt-4">

- 只有蒸餾：步數太少時圖會糊（和 L07 VAE 的糊是同一種原因：平均）
- 加上鑑別器：逼學生畫出清楚的細節（L09 GAN 的強項）

</div>

<div class="takeaway mt-3">「GAN 還是擴散」不一定二選一：有些少步數的擴散模型，就是靠 GAN 的鑑別器訓練出來的（鑑別器只在訓練時用）。</div>

<div class="src">Sauer et al., Adversarial Diffusion Distillation, 2023（SDXL-Turbo，S3，待確認）；L09「GAN 不是過時技術」那一頁的延伸</div>

<!--
★ ADD（5 分）：ADD（對抗式擴散蒸餾）。L09 的地圖上列過：Real-ESRGAN、SD 的 VAE 解碼器、ADD／Turbo、HiFi-GAN／EnCodec。今天補上 ADD 的位置。
-->

---

<div class="eyebrow">02 · Open · 擴散怎麼變快 3</div>

# Flow matching（流匹配）：訓練路線是直線

<div class="grid grid-cols-[1.25fr_1fr] gap-6 mt-2">
<div>

<img class="photo" src="/lab16-flow-toy.png" alt="2D 玩具：雜訊走向兩個月亮的 20 步軌跡，以及 1、2、10 步的生成結果" style="width:100%;object-fit:contain"><div class="shot-cap">20 步的軌跡；1、2、10 步的生成結果（lab16 第 2 部分，<code>flow_toy.png</code>）</div>

</div>
<div style="font-size:17px">

- 符號：**x₀＝雜訊**、**x₁＝資料**、t：0 → 1 的進度（和 L11 的 x₀＝原圖相反！）
- 訓練：隨機取 t，直線上的點 x_t ＝ (1 − t)·x₀ ＋ t·x₁
- 網路學「速度」：x₁ − x₀（直線的方向）
- 生成：從雜訊出發，沿速度走幾步（每步走 1／步數）

```python
xt = (1 - t) * x0 + t * x1
target = x1 - x0
loss = ((vnet(torch.cat([xt, t], 1)) - target) ** 2).mean()
```

</div>
</div>

<div class="takeaway mt-2">和 L11 同一家族（從雜訊走到資料）；路線設計成直線，步數就有機會很少。</div>

<div class="src">Lipman et al., Flow Matching, 2023（S4，待確認）；SD3、FLUX 等新模型採用這類訓練（待確認）</div>

<!--
★ flow matching（6 分）：x₀ 是雜訊、x₁ 是資料（注意：和 L11 的 x₀ 是「原圖」相反，這裡沿用 flow matching 論文的寫法）。讀作「在雜訊和資料連成的直線上取一點，學那條直線的方向」。
Lab 練習會發現：學出來的軌跡其實是彎的——伏筆，別先講破。
-->

---

<div class="eyebrow">02 · Open · 文字指令編修</div>

# InstructPix2Pix：直接說「改成冬天」

<div class="grid grid-cols-2 gap-6 mt-3" style="font-size:18px">
<div class="node node--primary"><strong>輸入</strong><small>一張圖 ＋ 一句指令（make it winter）。不用寫完整描述，只寫「要改什麼」</small></div>
<div class="node"><strong>兩個指導強度</strong><small><code>guidance_scale</code>：多聽指令（L13 的 w）<br><code>image_guidance_scale</code>：多像原圖（越大越保守）</small></div>
</div>

<div style="font-size:18px" class="mt-4">

- 訓練資料：用語言模型和 SD 合成的「原圖、指令、改後圖」三件組（成對資料，L10 學過成對 vs 不成對）
- 原圖接在 U-Net 的輸入通道上（L14 inpainting 的做法）

</div>

<div class="takeaway mt-3">好用，但「只改指定的地方」沒有保證：產品本身也可能被改，要和原圖對照。</div>

<div class="src">Brooks et al., InstructPix2Pix, CVPR 2023（S6，待確認）</div>

<!--
★ 文字指令（4 分）：和 L14 的三種條件方式對照：文字走交叉注意力、原圖接輸入通道。
-->

---

<div class="eyebrow">03 · Measure（量測驗收）· 練習</div>

# 練習：幫三張冬天照打分數（先別看別人的）

<div class="muted" style="font-size:17px">看「三種方法改成冬天」那頁講師跑的四格圖（lab 跑完後可以改看自己的）。1＝不能用、5＝可以直接給行銷部。只寫你自己的判斷。</div>

<table class="fill tight vlines mt-2">
<thead><tr><th style="width:22%">方法</th><th style="width:14%">像冬天</th><th style="width:14%">產品沒被改</th><th style="width:14%">整體可用</th><th>一句理由</th></tr></thead>
<tbody>
<tr><td>A：CycleGAN</td><td class="blank"><FillIn id="rate.a1" hint="1～5" /></td><td class="blank"><FillIn id="rate.a2" /></td><td class="blank"><FillIn id="rate.a3" /></td><td class="blank"><FillIn id="rate.a-why" hint="例：顏色變了但……" /></td></tr>
<tr><td>B：InstructPix2Pix</td><td class="blank"><FillIn id="rate.b1" /></td><td class="blank"><FillIn id="rate.b2" /></td><td class="blank"><FillIn id="rate.b3" /></td><td class="blank"><FillIn id="rate.b-why" /></td></tr>
<tr><td>C：SD1.5＋LCM</td><td class="blank"><FillIn id="rate.c1" /></td><td class="blank"><FillIn id="rate.c2" /></td><td class="blank"><FillIn id="rate.c3" /></td><td class="blank"><FillIn id="rate.c-why" /></td></tr>
</tbody>
</table>

<FillClear group="rate" />

<!--
★ 評分（6 分）：個人作業、沒有標準答案、不收回。寫完後講師開下一頁收集全班的「整體可用」分數（舉手或線上表單皆可，只統計數字、不記名）。
-->

---

<div class="eyebrow">03 · Measure · 人的評分</div>

# 為什麼這裡要用人的評分

<div class="grid grid-cols-[1fr_1fr] gap-6 mt-2">
<div>

<table class="vlines" style="font-size:17px;text-align:center">
<thead><tr><th>整體可用</th><th>A</th><th>B</th><th>C</th></tr></thead>
<tbody>
<tr><td>全班平均</td><td>現場統計</td><td>現場統計</td><td>現場統計</td></tr>
<tr><td>給 4～5 分的人數</td><td>現場統計</td><td>現場統計</td><td>現場統計</td></tr>
</tbody>
</table>

</div>
<div style="font-size:18px">

- CLIP 分數量「貼不貼題」，FID 量「整體分布」：都量不到「行銷部能不能用」
- 一個人說了算 → 個人偏好；**很多人各自打分** → 比較可靠
- 先各自寫、再統計：避免跟著第一個發言的人走

</div>
</div>

<div class="takeaway mt-3">任務的目標是「人覺得能用」時，就去量人：多人、各自、先寫再統計。</div>

<!--
★ 人的評分（5 分）：表格現場填。大型模型排行榜（例如文字生成圖的競技場）也是用很多人兩兩比較來排名（只認名字，不查證數字）。
-->

---

<div class="eyebrow">04 · 延伸</div>

# Consistency models、DiT（只認名字）

<div class="grid grid-cols-2 gap-6 mt-4" style="font-size:18px">
<div class="node"><strong>Consistency model（一致性模型）</strong><small>直接學「從任何雜訊程度，一步跳回資料」；LCM 就是它在潛在空間的版本</small></div>
<div class="node"><strong>DiT（Diffusion Transformer）</strong><small>把去噪的 U-Net 換成 Transformer；L18 學完 Transformer 就看得懂</small></div>
</div>

<div class="takeaway mt-4">Consistency model 回答「怎麼更少步」；DiT 回答「去噪網路用什麼架構」。看到名字，先問它改的是哪一塊。</div>

<div class="src">Song et al., 2023（S9）；Peebles &amp; Xie, 2023（S10），皆待確認</div>

<!--
○ 選修（2 分）：只認名字。
-->

---

<div class="eyebrow">附錄 · 備用</div>

# Rectified flow（整流）：把彎路再拉直一次（選讀）

<div style="font-size:19px" class="mt-4">

1. 先用一般的 flow matching 訓練（隨機配對雜訊和資料）
2. 用訓練好的模型，把每個雜訊點「走到」它的終點：得到新的配對
3. 用新的配對再訓練一次（reflow，重新配對再訓練）：路線交叉變少，軌跡更直
4. 夠直之後，1 步就能走到

</div>

<div class="takeaway mt-3">隨機配對的直線會互相交叉，網路只能學到「平均方向」，所以軌跡會彎；重新配對，交叉就少了。</div>

<div class="src">Liu et al., Flow Straight and Fast, 2023（S5，待確認）</div>

<!--
△ 附錄（1 分）：Lab 練習後學員問「為什麼是彎的」時再講。
-->

---

<div class="eyebrow">05 · Lab L4-4</div>

# Lab 1／3：Specify（比賽規則）

<div class="grid grid-cols-2 gap-6 mt-2" style="font-size:18px">
<div>

**打開筆記本**：<code>lab16-bakeoff.ipynb</code>（在 <code>materials/</code>）→ Open in Colab；執行階段 **T4 GPU**

<div style="font-size:17px">

<strong>【目標】</strong>同一張夏天產品照改成冬天：三種方法的品質、速度、穩定、可控<br>
<strong>【輸入與輸出】</strong>原圖 512 × 512 → 三張冬天圖；每種方法的秒／張、VRAM 峰值<br>
<strong>【限制】</strong>同一張原圖、同一張 T4；暖機一次後再量（擴散各 3 次、CycleGAN 10 次取平均）；第 2 部分 flow 玩具在 CPU

</div>

</div>
<div>

**【驗收】**

1. 三種方法都有結果圖、秒／張、VRAM 峰值
2. 秒數是「暖機後」的平均（第一次含載入，不算）
3. 兩個擴散方法各有 3 個 seed 的結果
4. flow 玩具 10 步的點落在兩個月亮附近

</div>
</div>

<div class="takeaway mt-3">公平比賽：同一張原圖、同一張 GPU、同樣的量法。</div>

<!--
★ Lab 開始（3 分）：為什麼要暖機：第一次執行包含把權重搬上 GPU、CUDA 初始化，會比之後慢很多（lab 的 timed 函式先跑一次不計時）。
-->

---

<div class="eyebrow">05 · Lab L4-4</div>

# Lab 2／3：Generate → Execute

<PromptBox>
這是 PyTorch 筆記本，請只填第 2 部分的 # TODO（flow matching 的一步）：<br>
xt ＝ 直線上的點 (1 − t)·x0 ＋ t·x1；target ＝ x1 − x0；<br>
loss ＝ vnet(把 xt 和 t 接起來) 和 target 的 MSE。不要改其他格，說明每一行。
</PromptBox>

<div class="steps mt-2" style="font-size:17px">
  <div><span class="num">1</span>三個模型的下載量與每張秒數待 T4 實測；等待時先用講師的四格圖寫「幫三張冬天照打分數」</div>
  <div><span class="num">2</span>沒有 Agent 額度：照「Flow matching」那頁的兩行程式填；卡住開 <code>-solution.ipynb</code></div>
  <div><span class="num">3</span>預期輸出：每種方法一行「秒／張｜VRAM 峰值」；flow 訓練「3000 步（CPU）＿秒」</div>
</div>

<div class="node node--warm mt-2" style="font-size:16px"><strong>常見錯誤</strong><small>target 寫成 <code>x1</code>（終點）而不是 <code>x1 - x0</code>（方向）：網路學到的是位置不是速度，沿著它一步步走（Euler 法）會飛走</small></div>

<!--
★ 執行（約 18 分）：CycleGAN 的權重從 Berkeley 的伺服器下載；InstructPix2Pix 與 SD1.5 的下載量待 T4 實測（lab-runs.md）。下載慢時先做 flow 玩具（CPU）。
-->

---

<div class="eyebrow">05 · Lab L4-4 · 練習</div>

# 練習：flow 玩具，1 步、2 步、10 步會畫成什麼？

<div class="node" style="font-size:16px"><strong>照著做（另一個例子）</strong><small>如果資料只有「一個點」x₁：每條訓練路線都指向同一點，網路學到的速度就是那條直線 → 1 步就走到。現在資料是兩個月亮（4000 個點），會一樣嗎？</small></div>

<table class="fill tight vlines mt-2">
<thead><tr><th style="width:24%">問題</th><th>你的預測</th><th>實際（看圖）</th></tr></thead>
<tbody>
<tr><td>20 步的軌跡是直的嗎？</td><td class="blank"><FillIn id="flow.path-p" hint="例：直的，因為……" /></td><td class="blank"><FillIn id="flow.path-a" /></td></tr>
<tr><td>1 步的結果</td><td class="blank"><FillIn id="flow.s1-p" /></td><td class="blank"><FillIn id="flow.s1-a" /></td></tr>
<tr><td>2 步的結果</td><td class="blank"><FillIn id="flow.s2-p" /></td><td class="blank"><FillIn id="flow.s2-a" /></td></tr>
<tr><td>10 步的結果</td><td class="blank"><FillIn id="flow.s10-p" /></td><td class="blank"><FillIn id="flow.s10-a" /></td></tr>
</tbody>
</table>

<FillClear group="flow" />

<!--
★ 練習（6 分）：個人作業，不收回。重點是發現「訓練路線直，學出來的軌跡卻彎」。
-->

---
hostOnly: true
---

<div class="eyebrow">05 · Lab L4-4 · 練習解答</div>

# 練習解答：每條路線是直的，學到的卻是彎的

<table class="vlines" style="font-size:18px">
<thead><tr><th style="width:24%">問題</th><th>實際（T4 實跑，seed 0）</th></tr></thead>
<tbody>
<tr><td>20 步的軌跡</td><td>實跑後填入</td></tr>
<tr><td>1 步</td><td>實跑後填入</td></tr>
<tr><td>2 步</td><td>實跑後填入</td></tr>
<tr><td>10 步</td><td>實跑後填入</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">為什麼：同一個點可能在好幾條訓練直線上，網路學到的是它們的平均方向，所以會彎；1 步只能走到「平均」的位置。</div>

<!--
★ 解答（2 分）：所以真正 1～4 步的模型還要再加工：rectified flow（附錄）或蒸餾（LCM）。本機 CPU 試跑看到同樣現象（lab-runs.md），以 T4 實跑圖為準。
-->

---

<div class="eyebrow">05 · Lab L4-4 · Audit</div>

# Lab 3／3：Audit → 比較表（備忘錄的骨架）

<table class="mt-2" style="font-size:16px">
<thead><tr><th style="width:20%">準則</th><th>A：CycleGAN</th><th>B：InstructPix2Pix</th><th>C：SD1.5＋LCM</th></tr></thead>
<tbody>
<tr><td>秒／張（T4）</td><td>實跑後填入</td><td>實跑後填入</td><td>實跑後填入</td></tr>
<tr><td>VRAM 峰值</td><td>實跑後填入</td><td>實跑後填入</td><td>實跑後填入</td></tr>
<tr><td>穩定性（壞掉的比例）</td><td>只有 1 張（沒有 seed）：看它能不能用</td><td>3 個 seed 中壞掉幾張</td><td>3 個 seed 中壞掉幾張</td></tr>
<tr><td>可控性</td><td>只能「夏 → 冬」</td><td>一句指令</td><td>完整提示詞＋strength</td></tr>
<tr><td>品質（你的評分）</td><td colspan="3">「幫三張冬天照打分數」那頁</td></tr>
<tr><td>授權</td><td colspan="3">「授權比較」那頁</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">稽核：秒數是暖機後的平均嗎？三種方法用的是同一張原圖、同一張 GPU 嗎？</div>

<!--
★ 稽核（5 分）：CycleGAN 是專門模型：只會它訓練過的那一種轉換（優勝美地的夏 → 冬），換任務就要重新收資料、重新訓練。這一點要寫進可控性。
-->

---

<div class="eyebrow">06 · 學習評量（a）</div>

# 備忘錄：GAN 還是擴散？用你自己的證據

<div class="grid grid-cols-[1.1fr_1fr] gap-6 mt-2" style="font-size:17px">
<div class="node node--primary"><strong>題目</strong><small>給技術長的一頁備忘錄：季節性產品照編修，公司標準選 GAN 還是擴散（或兩者分工）？說明 Diffusion 和 GAN 的差別，並用你自己跑出來的數字支持</small></div>
<div>

<table style="font-size:16px">
<thead><tr><th>評分重點</th><th style="width:22%">比重</th></tr></thead>
<tbody>
<tr><td>正確說明兩者的原理差異</td><td>30%</td></tr>
<tr><td>用自己的證據（D3、D4 的數字與圖）</td><td>30%</td></tr>
<tr><td>六項準則都考慮到</td><td>20%</td></tr>
<tr><td>建議清楚、寫出風險與還不確定的事</td><td>20%</td></tr>
</tbody>
</table>

</div>
</div>

<div class="takeaway mt-3">好的備忘錄：一句建議、三個證據、一個風險；技術長 2 分鐘看得完。</div>

<!--
★ 學習評量 a（6 分）：評分比重是講師的建議值，可依班級調整（outline 待講師決定）。強調「自己的證據」：直接引用 lab 輸出的數字，不要引用網路上的排行榜。
-->

---

<div class="eyebrow">06 · 學習評量（a）· 範本</div>

# 從比較表到備忘錄：每一列變成一段

<div class="node mt-2" style="font-size:17px;line-height:1.6"><strong>備忘錄骨架</strong><small>
<b>建議</b>：季節性編修以 ＿＿ 為標準；＿＿ 的情況改用 ＿＿。<br>
<b>原理差異</b>：GAN 是 ＿＿（一次前向、對抗訓練）；擴散是 ＿＿（從雜訊一步步去噪）。<br>
<b>證據 1（品質）</b>：全班評分 ＿＿；我的評分 ＿＿。<br>
<b>證據 2（速度）</b>：T4 上 A ＿＿ 秒、B ＿＿ 秒、C ＿＿ 秒（暖機後平均）。<br>
<b>證據 3（多樣性、穩定性）</b>：L09 GAN 的 ＿＿；今天換 seed 的結果 ＿＿。<br>
<b>可控性與授權</b>：＿＿。<b>風險與未確認</b>：＿＿。
</small></div>

<div class="takeaway mt-3">把第三天的三難表、今天的比較表，一列一列翻成句子，就是備忘錄。</div>

<!--
★ 範本（6 分）：空格不是填空題，是提醒「每一段都要有數字」。可以請 Agent 幫忙潤稿，但數字和判斷必須是自己的。
-->

---

<div class="eyebrow">07 · 期末專題</div>

# 選一張你的期末專題需求單

<table class="fill tight vlines mt-2">
<thead><tr><th style="width:24%">欄位</th><th>你的提案</th></tr></thead>
<tbody>
<tr><td>部門與問題</td><td class="blank"><FillIn id="cap.problem" hint="例：客服部，回覆太慢……" /></td></tr>
<tr><td>資料（來源、授權）</td><td class="blank"><FillIn id="cap.data" /></td></tr>
<tr><td>模型或方法</td><td class="blank"><FillIn id="cap.model" /></td></tr>
<tr><td>成功指標（KPI）</td><td class="blank"><FillIn id="cap.kpi" /></td></tr>
<tr><td>T4 放得下嗎？風險？</td><td class="blank"><FillIn id="cap.risk" /></td></tr>
</tbody>
</table>

<FillClear group="cap" />

<div class="muted mt-1" style="font-size:16px">可以延續任何一張需求單（D1–D4），或用第五天的語言模型主題；第六天 Demo Day 展示。</div>

<!--
★ 期末專題（6 分）：個人提案，回家作業第 3 項會寫完整版。提醒：資料要有授權、要放得進 T4。
-->

---

<div class="eyebrow">08 · 風險（Risk）· 授權</div>

# 授權比較：快不等於能用

<table class="mt-2" style="font-size:17px">
<thead><tr><th style="width:28%">方法</th><th>授權（模型卡標籤，2026-11-25）</th><th style="width:36%">對公司標準的意義</th></tr></thead>
<tbody>
<tr><td>CycleGAN（程式與權重）</td><td>BSD（待確認）</td><td>寬鬆；但優勝美地權重只會那一種轉換</td></tr>
<tr><td>InstructPix2Pix</td><td>MIT</td><td>寬鬆；但它是從 SD1.5 微調來的，上游授權也要看</td></tr>
<tr><td>SD1.5 ＋ LCM-LoRA</td><td>CreativeML OpenRAIL-M ＋ openrail++</td><td>授權列了禁止用途；SD1.5 模型卡寫「僅供研究」：商用前法務確認</td></tr>
<tr><td><b>反例</b>：SDXL-Turbo</td><td>sai-nc-community（商用要另外依 Stability AI 會員條款）</td><td>又快又好，但不能直接拿來做商品圖</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">標準要寫進授權：最快的模型，可能是公司不能用的模型。</div>

<div class="src">Hugging Face 模型卡的授權標籤（S7、S8，2026-11-25 讀取；CycleGAN 待確認）；授權會變動，法律問題以公司法務意見為準</div>

<!--
★ 授權（4 分）：這一欄每個學員的備忘錄都要有。授權會變動：寫備忘錄當天，要再開一次模型卡確認。
-->

---

<div class="eyebrow">第四天總整理</div>

# 第四天：從「指定類別」到「公司標準」

<table class="mt-2" style="font-size:17px">
<thead><tr><th style="width:15%">單元</th><th style="width:22%">條件／控制</th><th>解決的需求單</th><th>關鍵一行</th></tr></thead>
<tbody>
<tr><td>L13</td><td>類別編號</td><td>數據組：指定生成第 k 類</td><td><code>ε_u ＋ w·(ε_c − ε_u)</code></td></tr>
<tr><td>L14</td><td>文字、遮罩、起始圖</td><td>行銷部：情境照、換背景</td><td><code>guidance_scale</code>、<code>strength</code></td></tr>
<tr><td>L15</td><td>參考照、LoRA</td><td>品牌部：我們的產品</td><td><code>W·x ＋ B·(A·x)</code></td></tr>
<tr><td>L16</td><td>少步數、指令</td><td>技術長：選標準</td><td>比較表 → 備忘錄</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">第四天的主軸：同一套去噪流程，換條件、加 LoRA、減步數，就解決了四種商業問題。</div>

<!--
★ 第四天總整理（4 分）：請學員說出三種把條件交給 U-Net 的方式（嵌入相加、交叉注意力、接成輸入通道）。第五天換主角：語言模型（Transformer、GPT）。
-->

---

<div class="eyebrow">第四天 · iPAS 小考</div>

# 第四天小考 1／3（iPAS 題型）：點選答案

<Mcq id="quiz1.q1" :n="1" :answer="1"
  :options="['另外訓練一個分類器', '隨機把部分標籤換成「沒有標籤」', '把 T 減半', '凍結 U-Net']"
  :why="['另外訓練分類器是 classifier guidance（分類器引導），CFG 的 free 就是不需要它。', '', 'T 是擴散總步數，和 CFG 無關。', 'U-Net 就是要訓練的對象，不能凍結。']"
  explain="訓練時隨機把部分標籤換成「沒有標籤」，同一個網路就能算 ε_cond 和 ε_uncond。">
Classifier-free guidance 訓練時要做什麼？
</Mcq>

<Mcq id="quiz1.q2" :n="2" :answer="2"
  :options="['VAE 編碼器', '排程器', 'CLIP 的文字編碼器', '鑑別器']"
  :why="['VAE 編碼器把圖壓成潛在，不處理文字。', '排程器決定每一步怎麼走，不處理文字。', '', '鑑別器是 GAN 的零件。']"
  explain="CLIP 的文字編碼器把提示詞變成 77 × 768 的向量，交給 U-Net 的交叉注意力。">
Stable Diffusion 用哪個零件把提示詞變成向量？
</Mcq>

<FillClear group="quiz1" corner />

<!--
★ 小考 1／3（2 分）：學員自己點；點錯會出現「再想想」和該選項錯在哪，可再點一次。答案：1 B、2 C。
-->

---

<div class="eyebrow">第四天 · iPAS 小考</div>

# 第四天小考 2／3（iPAS 題型）：點選答案

<Mcq id="quiz2.q3" :n="3" :answer="0"
  :options="['遮罩和挖空的原圖潛在', '一個類別編號', '鑑別器的分數', '第二段提示詞']"
  :why="['', '類別編號是 L13 條件生成的做法，不是 inpainting。', '鑑別器分數屬於 GAN。', 'inpainting 不需要第二段提示詞。']"
  explain="inpainting 的 U-Net 多收遮罩和被挖空的原圖潛在，才知道哪裡要重畫、哪裡要保留。">
inpainting 模型的 U-Net 比一般 SD 多了什麼輸入？
</Mcq>

<Mcq id="quiz2.q4" :n="4" :answer="1"
  :options="['把模型改成 8 層', '只訓練很細的 B、A，原權重凍結', '不需要反向傳播', '只用 CPU']"
  :why="['LoRA 不改模型的層數。', '', '還是要反向傳播，只是只更新 B、A。', 'CPU 太慢，LoRA 訓練還是用 GPU。']"
  explain="原權重凍結，只訓練很細的 B、A，要訓練的參數和優化器狀態都少很多，T4 放得下。">
LoRA 為什麼能在 T4 上微調 SD？
</Mcq>

<FillClear group="quiz2" corner />

<!--
★ 小考 2／3（2 分）：學員自己點；點錯會出現「再想想」和該選項錯在哪，可再點一次。答案：3 A、4 B。
-->

---

<div class="eyebrow">第四天 · iPAS 小考</div>

# 第四天小考 3／3（iPAS 題型）：點選答案

<Mcq id="quiz3.q5" :n="5" :answer="3"
  :options="['降低解析度', '換成 GAN', '刪掉 VAE', '蒸餾成少步數']"
  :why="['降低解析度是另一種加速，不是 LCM 的主要做法。', 'LCM 仍是擴散模型，不是 GAN。', 'VAE 還是需要，潛在要靠它解回圖。', '']"
  explain="LCM 把原本要幾十步的模型蒸餾成很少的步數（LCM-LoRA 是它的輕量版）。">
LCM 讓 SD 變快的主要方法是？
</Mcq>

<Mcq id="quiz3.q6" :n="6" :answer="1"
  :options="['它是 GAN', '授權有限制，要先查模型卡', 'T4 跑不動', '不支援英文']"
  :why="['它是擴散模型蒸餾來的，這不是不能採用的原因。', '', 'T4 跑不跑得動要看實測；真正卡住的是授權。', '它支援英文，限制不在語言。']"
  explain="模型卡的授權（sai-nc-community）限制商用，商用要另依 Stability AI 會員條款；選公司標準前要先查授權。">
選公司標準時，SDXL-Turbo 又快又清楚，為什麼不能直接採用？
</Mcq>

<FillClear group="quiz3" corner />

<!--
★ 小考 3／3（2 分）：學員自己點；點錯會出現「再想想」和該選項錯在哪，可再點一次。答案：5 D、6 B。
全部答案與理由：
1 B：訓練時隨機把部分標籤換成「沒有標籤」，同一個網路就能算 ε_cond 和 ε_uncond。
2 C：CLIP 的文字編碼器把提示詞變成 77 × 768 的向量，交給 U-Net 的交叉注意力。
3 A：inpainting 的 U-Net 多收遮罩和被挖空的原圖潛在，才知道哪裡要重畫、哪裡要保留。
4 B：原權重凍結，只訓練很細的 B、A，要訓練的參數和優化器狀態都少很多，T4 放得下。
5 D：LCM 把原本要幾十步的模型蒸餾成很少的步數（LCM-LoRA 是它的輕量版）。
6 B：模型卡的授權（sai-nc-community）限制商用，商用要另依 Stability AI 會員條款；選公司標準前要先查授權。
-->


---

<div class="eyebrow">第四天 · 回家作業</div>

# 回家作業：備忘錄、學習評量筆記本、專題提案

<div class="steps mt-3" style="font-size:18px">
  <div><span class="num">1</span><strong>備忘錄（學習評量 a）</strong>：一頁，照「從比較表到備忘錄」那頁的骨架；數字只用自己跑出來的</div>
  <div><span class="num">2</span><strong>完成 L4-1（學習評量 b）</strong>：<code>lab13-cfg.ipynb</code> 兩個 TODO 自己填、從頭跑完、寫下建議的 w；準備口頭說明 CFG 那一行</div>
  <div><span class="num">3</span><strong>期末專題提案</strong>：把「選一張你的期末專題需求單」那頁的五個欄位寫成半頁，附資料的來源與授權</div>
</div>

<div class="takeaway mt-4">三份作業都在回答同一件事：你能用自己的證據，說清楚一個生成模型該不該用、怎麼用。</div>

<!--
★ 作業（3 分）：繳交方式與期限由講師宣布。下一次上課（L17）開場 5 分鐘回顧備忘錄的常見問題。
-->

---
hostOnly: true
---

<div class="eyebrow">下一步</div>

# 下一堂 L17：客服部的 token 成本

<div style="font-size:19px" class="mt-4">

- 第五天換主角：語言模型
- 客服部：回覆按 token 計費，為什麼同一句話中文比英文貴？字的順序為什麼重要？
- 從序列模型走到注意力（L14 學過的交叉注意力，明天看懂它怎麼算）

</div>

<!--
★ 下一步（1 分）：預告。
-->
