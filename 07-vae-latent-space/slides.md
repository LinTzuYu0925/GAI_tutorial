---
theme: default
title: 一張 T4 跑得動 512px 嗎？
info: |
  生成式AI原理 · D2-3
  自編碼器的潛在空間有洞；VAE 讓瓶頸變成一團機率雲，把洞補起來，才能「隨便取一點」生成新東西。Stable Diffusion 先用 VAE 把 512px 照片壓小 48 倍。
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
exportFilename: 07-vae-latent-space
layout: center
class: cover
---

<div class="eyebrow">生成式AI原理 · D2-3</div>

# 一張 T4 跑得動 512px 嗎？

<p class="subtitle">VAE：把瓶頸變成一團雲，潛在空間才能拿來生成</p>

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-8">
  <span class="chip">像素太貴</span><span class="arrow">→</span>
  <span class="chip">AE 的洞</span><span class="arrow">→</span>
  <span class="chip">μ、σ 與重參數化</span><span class="arrow">→</span>
  <span class="chip">重建＋KL</span><span class="arrow">→</span>
  <span class="chip">取樣與內插</span><span class="arrow">→</span>
  <span class="chip">SD 的 VAE</span>
</div>

<!--
★ 開場（2 分）：前兩堂的主角圖用來「檢查」；今天開始用它來「生成」。同一張編碼器→瓶頸→解碼器的圖，這次瓶頸變成一團機率雲。
-->

---

<div class="eyebrow">00 · Frame（定義問題）</div>

# 行銷科技組：一週上千張 512px 商品圖

<div class="ticket mt-2">
  <div class="ticket-head">【需求單 #D2-3】部門：行銷科技組<span>公司：曜嶼電子 <span class="fiction" style="color:#fff;border-color:#fff">虛構</span></span></div>
  <dl>
    <dt>問題</dt><dd>第四天要大量生成 512px 商品圖，一張 T4 跑得動嗎？</dd>
    <dt>現況痛點</dt><dd>直接在像素上生成太貴：一張 512×512 彩色圖有 786,432 個數字</dd>
    <dt>成功指標（KPI）</dt><dd>壓縮比與重建品質（PSNR：峰值訊噪比，越高越像）；潛在空間內插是否平滑</dd>
    <dt>可用資料</dt><dd>Fashion-MNIST（代替型錄縮圖）；一張 CC0 街景照片</dd>
    <dt>限制與法規</dt><dd>Colab T4；照片要自有或 CC0</dd>
    <dt>為何現有工具不夠</dt><dd>D2-1 的自編碼器的潛在空間有「洞」：隨便取一點，解碼出來是垃圾</dd>
  </dl>
</div>

<!--
★ 需求單（3 分）：今天要回答兩件事：① 為什麼 Stable Diffusion 不直接在像素上生成；② 為什麼它的壓縮器是 VAE 而不是 D2-1 的 AE。
-->

---

<div class="eyebrow">學習目標</div>

# 今天結束時，你能夠……

1. **說明**為什麼 AE 的潛在空間有洞，不能直接拿來生成
2. **寫出**輸出 μ、σ 的編碼器與重參數化 <code>z = μ + σ·ε</code>
3. **讀懂**一行損失：重建 ＋ KL，並說出 KL 在做什麼
4. **取樣與內插**：從潛在空間生成新的商品圖
5. **量測** Stable Diffusion 的 VAE 把 512px 照片壓小多少、損失多少

<!--
★ 目標（1 分）。不教：ELBO 的推導（只放 △ 附錄）、VQ-VAE（下一堂）、擴散模型（第三天）。
數學只出現一行：損失＝重建＋KL；KL 用圖和程式說明，不推導（roadmap §11）。
-->

---

<div class="eyebrow">00 · Frame</div>

# 像素很貴：一張 512px 照片有多少個數字？

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-2 items-start">
<div>
  <img class="photo" src="/taipei-street.jpg" alt="黃昏的台北街道，滿是中文招牌、一輛公車和幾台車" style="width:100%;max-height:300px">
  <div class="shot-cap">台北街景（lumoplank，CC0，Wikimedia Commons）</div>
</div>
<div style="font-size:19px">

**照著算**

- 512 × 512 × 3（RGB）＝ **786,432** 個數字
- fp16 每個 2 bytes → 約 1.5 MB（D1-4 的 N × b）
- 生成模型每一步都要處理這麼多數字，還要跑幾十步

<div class="node node--primary mt-3"><strong>Stable Diffusion 的作法</strong><small>先壓成 4 × 64 × 64 ＝ 16,384 個數字，在小空間裡生成，最後才還原成照片</small></div>

</div>
</div>

<div class="takeaway mt-3">786,432 ÷ 16,384 ＝ 48：先壓縮，生成時每一步要處理的數字少 48 倍。</div>

<!--
★ Frame（4 分）：連回 D1-4 的 VRAM 估算：數字個數 × 每個的 bytes。只是一張圖的「資料」，還不含模型本身。
壓縮器就是今天的 VAE。先不說為什麼一定要 VAE，第 6 頁看到 AE 的洞就懂了。
-->

---

<div class="eyebrow">01 · Try（先用現成的）</div>

# Stable Diffusion 的 VAE：壓 48 倍，再還原

<div class="grid grid-cols-3 gap-4 mt-2">
<div><img class="photo" src="/taipei-street.jpg" alt="原始街景照片" style="height:180px;width:100%"><div class="shot-cap">輸入：3 × 512 × 512</div></div>
<div><div class="placeholder" style="height:180px">潛在表示 4 × 64 × 64<small>講師實跑後替換（四個通道的灰階圖）</small></div></div>
<div><div class="placeholder" style="height:180px">還原的照片<small>講師實跑後替換（附 PSNR、秒數）</small></div></div>
</div>

<div class="takeaway mt-4">先猜：大部分看起來一樣——哪裡最容易壞掉？（提示：招牌上的小字）</div>

<div class="src">模型：stable-diffusion-v1-5 的 VAE（AutoencoderKL，S2）；照片 CC0（S1）；lab07 第 6 步</div>

<!--
★ 示範（5 分）：用 lab07 解答筆記本最後一格。講師本機 CPU 試跑時，招牌小字（例如「大苑子」）明顯變形，整體顏色和結構都保留——T4 實跑後放真實結果。
重點：這個 VAE 就是 Stable Diffusion 的一部分；第四天生成商品圖時，最後一步就是它的解碼器。
-->

---

<div class="eyebrow">02 · Open（打開黑盒子）· AE 的洞</div>

# 自編碼器的潛在空間：一群一群，中間是洞

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-2 items-center">
<div>

<div class="placeholder" style="height:280px">Fashion-MNIST 測試集在 AE 2 維潛在空間的散佈圖（依類別上色）<small>講師實跑後替換（lab07 第 3 步）</small></div>

</div>
<div style="font-size:18px">

- 把每張圖壓成 2 個數字，畫成一個點
- 同一類聚在一起；類和類之間是**空的**
- 範圍也沒有規定：點可能散得很遠、偏到一邊
- 在空的地方取一點交給解碼器 → 它從沒學過那裡 → **垃圾**

</div>
</div>

<div class="takeaway mt-3">AE 只學「壓縮再還原」，從沒被要求「每一點都要能解碼」。所以不能隨便取點生成。</div>

<!--
★ AE 的洞（5 分）：這是 D2-1 的 AE（只是換成 2 維，方便畫圖）。實際範圍等 T4 實跑後再說（第 11 頁練習會讓學員先預測）。
問學員：「如果要生成一雙新的鞋子，你要在這張圖的哪裡取點？」→ 不知道，因為沒有規則。
-->

---

<div class="eyebrow">02 · Open · 今天的主角圖</div>

# VAE（變分自編碼器）：瓶頸變成一團雲

<div class="flex items-center justify-center gap-2 mt-4" style="font-size:18px">
  <div class="node" style="width:15%">輸入 x<small class="nw">&#91;B,1,28,28&#93;</small></div><span class="arrow">→</span>
  <div class="node node--primary" style="width:16%"><strong>Encoder</strong></div><span class="arrow">→</span>
  <div class="node node--warm" style="width:24%"><strong>μ 和 σ</strong><small>各 &#91;B,2&#93;：一團雲</small></div><span class="arrow">→</span>
  <div class="node node--warm" style="width:13%"><strong>抽一點 z</strong></div><span class="arrow">→</span>
  <div class="node node--secondary" style="width:16%"><strong>Decoder</strong></div>
</div>

<div class="grid grid-cols-2 gap-6 mt-6" style="font-size:18px">
<div class="node"><strong>AE（D2-1）</strong><small>同一張圖 → 永遠同一個點；點和點之間沒人管</small></div>
<div class="node node--primary"><strong>VAE</strong><small>同一張圖 → 一團雲裡的任一點都要能還原；雲會互相重疊，把洞填起來</small></div>
</div>

<div class="takeaway mt-4">每次從雲裡抽不同的點，解碼器被迫學會「這一帶都是鞋子」，而不是「這一個點是鞋子」。</div>

<div class="src">回顧：DL p.79（VAE 概念）；Kingma &amp; Welling, Auto-Encoding Variational Bayes, 2013（S3）</div>

<!--
★ 主角圖（6 分）：VAE（Variational Autoencoder，變分自編碼器）。DL 課看過概念（DL p.79），今天看程式。
程式裡 σ 存成 logvar（log σ²），因為 σ 一定要是正數，存 log 再取 exp 就不會出現負的寬度。
-->

---

<div class="eyebrow">02 · Open · 重參數化</div>

# 重參數化：<code>z = μ + σ · ε</code>

<div class="grid grid-cols-[1.15fr_1fr] gap-6 mt-2">
<div>

```python
std = torch.exp(0.5 * logvar)   # σ ＝ e^(½·log σ²)
eps = torch.randn_like(std)     # ε：從標準常態分布抽
z = mu + std * eps              # 從雲裡抽一點
```

<div class="muted mt-2" style="font-size:17px">讀作：先在「標準的雲」裡抽 ε，再放大 σ 倍、移到 μ。<code>logvar</code>＝log σ²：存 log 再取 exp，寬度就不會變成負的。<br><strong>照著算</strong>：μ ＝ 2、σ ＝ 0.5、抽到 ε ＝ −1 → z ＝ 2 ＋ 0.5 × (−1) ＝ 1.5</div>

</div>
<div style="font-size:18px">

<div class="node node--warm"><strong>為什麼不直接「從雲裡抽」？</strong><small>抽樣這個動作沒辦法微分，梯度傳不回 μ 和 σ</small></div>

<div class="node node--primary mt-3"><strong>重參數化的技巧</strong><small>隨機性全部放在 ε；μ、σ 只做加法和乘法 → 梯度流得回去</small></div>

</div>
</div>

<div class="takeaway mt-3">一行程式解決「隨機」和「反向傳播」的衝突：這是 VAE 能用一般訓練迴圈訓練的原因。</div>

<!--
★ 重參數化（5 分）：reparameterization（重參數化）。D1-3 的五行迴圈完全不用改：loss.backward() 會經過 mu + std * eps 流回編碼器。
Lab 的第一個 TODO 就是這三行。
-->

---

<div class="eyebrow">02 · Open · 損失</div>

# 損失 ＝ 重建 ＋ KL

<div class="grid grid-cols-[1fr_1.1fr] gap-6 mt-2 items-center">
<div>

<svg viewBox="0 0 320 200" style="width:100%;max-height:220px" aria-label="一團偏離中心的雲被 KL 拉回標準常態分布">
  <line x1="20" y1="170" x2="300" y2="170" stroke="var(--muted-text)" stroke-width="1.5"/>
  <path d="M60,170 C100,170 110,50 150,50 C190,50 200,170 240,170 Z" fill="var(--soft-blue)" stroke="var(--primary)" stroke-width="2"/>
  <path d="M190,170 C215,170 225,95 245,95 C265,95 275,170 295,170 Z" fill="var(--soft-amber)" stroke="var(--warm-accent)" stroke-width="2" stroke-dasharray="6 4"/>
  <path d="M232,82 C210,62 185,56 168,60" fill="none" stroke="var(--warm-accent)" stroke-width="2.5" marker-end="url(#kl)"/>
  <defs><marker id="kl" markerWidth="10" markerHeight="10" refX="7" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--warm-accent)"/></marker></defs>
  <text x="105" y="40" style="font-size:17px" fill="var(--primary)">標準常態 N(0, 1)</text>
  <text x="228" y="192" style="font-size:17px" fill="var(--warm-accent)">某張圖的雲</text>
</svg>

</div>
<div style="font-size:18px">

```python
recon = F.binary_cross_entropy(x_hat, x, reduction="sum") / len(x)
kl = -0.5 * torch.sum(1 + logvar - mu**2 - logvar.exp()) / len(x)
loss = recon + beta * kl          # beta 預設 1
```

- **重建**：和 D2-1 一樣，越像越好
- **KL（KL 散度）**：每團雲和「標準的雲」差多遠。讀法：<code>mu**2</code> 把中心拉向 0；<code>logvar</code> 那兩項把寬度拉向 1
- 不是越小越好：KL ＝ 0 代表雲完全不看輸入

</div>
</div>

<div class="takeaway mt-2">重建想把雲分開（各自好還原），KL 想把雲疊在中心：兩股力量的平衡讓空間「沒有洞」。</div>

<!--
★ 損失（7 分）：KL（Kullback–Leibler divergence，KL 散度）：衡量兩個分布差多少，0 代表一樣。
那一行 KL 公式是「兩個常態分布的 KL」算出來的結果，不推導；學員只要讀得懂：mu² 讓中心靠近 0，logvar 和 exp(logvar) 那兩項讓寬度靠近 1。
常見誤解：KL 越小越好——不對，KL＝0 代表雲完全不看輸入，解碼器什麼都還原不了。
-->

---

<div class="eyebrow">02 · Open · 名字</div>

# 為什麼叫「變分」？它在最佳化一個下界

<div class="grid grid-cols-2 gap-6 mt-4" style="font-size:18px">
<div class="node"><strong>真正想要的</strong><small>讓訓練資料出現的機率最大（D1-3 附錄的「最大概似」）；但對 VAE 來說，這個機率算不出來</small></div>
<div class="node node--primary"><strong>退而求其次</strong><small>最佳化它的一個<strong>下界</strong>：ELBO（證據下界）。ELBO ＝ −重建損失 − KL，所以「損失＝重建損失＋KL」越小，下界就越高</small></div>
</div>

<div class="takeaway mt-6">看到 ELBO 這個字時記得：就是今天這一行「重建損失＋KL」再加一個負號。</div>

<div class="src">推導見附錄「ELBO 從哪裡來」（△）；roadmap §11 數學地圖</div>

<!--
★ 命名（3 分）：ELBO（Evidence Lower BOund，證據下界）。只講文字，不推導。iPAS 題目可能出現 ELBO 這個詞，學員要知道它對應到哪一行程式。
-->

---

<div class="eyebrow">02 · Open · 練習</div>

# 練習：KL 會讓散佈圖變成什麼樣子？

<div class="muted" style="font-size:17px">不用 AI。先別執行 lab07 第 3 步。同一個網路、同一份資料，只差有沒有 KL。照著做：第一列已填好。</div>

<table class="fill tight vlines mt-1">
<thead><tr><th style="width:38%">問題</th><th>AE（沒有 KL）</th><th>VAE（有 KL）</th></tr></thead>
<tbody>
<tr><td>點的中心大約在哪？</td><td>沒有規定，可能偏到一邊</td><td>接近 (0, 0)（KL 把中心拉向 0）</td></tr>
<tr><td>座標的範圍大約多大？</td><td class="blank"><FillIn id="kl.ae-range" hint="例：比 ±3 大或小……" /></td><td class="blank"><FillIn id="kl.vae-range" /></td></tr>
<tr><td>哪兩類最可能挨在一起？為什麼？</td><td class="blank"><FillIn id="kl.ae-gap" /></td><td class="blank"><FillIn id="kl.vae-gap" /></td></tr>
<tr><td>在 (0, 0) 附近取點解碼，會是什麼？</td><td class="blank"><FillIn id="kl.ae-decode" /></td><td class="blank"><FillIn id="kl.vae-decode" /></td></tr>
</tbody>
</table>

<FillClear group="kl" />

<!--
★ 練習（6 分）：寫完預測再執行第 3、4 步，對照散佈圖與解碼網格。不收回。
-->

---
hostOnly: true
---

<div class="eyebrow">02 · Open · 練習解答</div>

# 練習解答：KL 把雲拉到中心、填滿空隙

<table class="vlines" style="font-size:18px">
<thead><tr><th style="width:36%">問題</th><th>AE</th><th>VAE</th></tr></thead>
<tbody>
<tr><td>範圍</td><td>大而且不對稱（沒有東西限制它）</td><td>大約 ±3 以內（KL 拉向 N(0, 1)）</td></tr>
<tr><td>挨在一起的類</td><td colspan="2">長得像的類：例如 Sneaker／Sandal／Ankle boot（都是鞋）、Pullover／Coat／Shirt（上衣）。兩種模型都會，VAE 的群之間空隙較小</td></tr>
<tr><td>(0, 0) 附近解碼</td><td>可能是幾類混在一起的模糊圖</td><td>看得出是某種衣物</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">怎麼對答案：看 lab07 第 3 步印出的座標範圍，和第 4 步左右兩張解碼網格。</div>

<!--
★ 解答（2 分）：講師本機 CPU 試跑（3 epochs）印出：AE z1 約 −14.7～5.8、z2 約 −8.0～4.4；VAE z1 約 −2.9～2.4、z2 約 −3.5～3.1。T4 實跑後以實跑為準。
-->

---

<div class="eyebrow">02 · Open · 生成</div>

# 取樣與內插：每一點都解碼得出東西

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-2">
<div>

```python
z = torch.randn(16, 2)        # 從 N(0, I) 抽 16 點
new_items = vae.decode(z)

za, zb = mu[0], mu[1]         # 兩件商品
strip = [vae.decode(za + (zb - za) * t)
         for t in torch.linspace(0, 1, 10)]
```

<div class="muted mt-1" style="font-size:16px">讀作：N(0, I)＝每一維都是平均 0、寬度 1 的常態分布（I 是單位矩陣）；內插＝兩點之間等距取 10 點</div>

</div>
<div>

<div class="placeholder" style="height:90px;min-height:0">16 張取樣<small>講師實跑後替換</small></div>
<div class="placeholder mt-2" style="height:90px;min-height:0">鞋子 → 毛衣 的 10 步內插<small>講師實跑後替換</small></div>

</div>
</div>

<div class="takeaway mt-2">訓練時 KL 把雲拉向 N(0, I)，所以生成時從 N(0, I) 抽點才有意義。</div>

<!--
★ 取樣與內插（6 分）：內插（interpolation）的中間幾格會是「半鞋半毛衣」——這就是「潛在空間平滑」的意思，也是需求單的 KPI 之一。
-->

---

<div class="eyebrow">03 · Adapt · 選修</div>

# 為什麼 VAE 的圖有點糊？

<div class="grid grid-cols-2 gap-6 mt-4" style="font-size:18px">
<div class="node node--warm"><strong>原因</strong><small>不同圖片的雲會互相重疊：同一個 z 可能來自好幾張不同的圖，解碼器只好畫「它們的平均」，平均就會糊</small></div>
<div class="node"><strong>後來的解法</strong><small>SD 的 VAE 解碼器多加了對抗損失（D3-1 的 GAN）和感知損失，讓細節銳利；真正的生成交給擴散模型（D3）</small></div>
</div>

<div class="takeaway mt-6">VAE 適合當「壓縮器」：好壓、好還原、空間平滑；畫細節的工作交給別人。</div>

<div class="src">Rombach et al., High-Resolution Image Synthesis with Latent Diffusion Models, 2022（S4）</div>

<!--
○ 選修（3 分）：這頁連到第三天的「生成三難」：VAE 快、多樣，但品質（銳利度）較差。
-->

---

<div class="eyebrow">03 · Adapt · 選修</div>

# β-VAE：一個旋鈕，清楚 vs 平滑

<table class="mt-4" style="font-size:18px">
<thead><tr><th style="width:24%">beta</th><th>KL 的力量</th><th>結果</th></tr></thead>
<tbody>
<tr><td>小（例如 0.1）</td><td>弱：雲可以分得很開</td><td>還原清楚，但又開始有洞</td></tr>
<tr><td>1（標準 VAE）</td><td>平衡</td><td>今天的設定</td></tr>
<tr><td>大（例如 4）</td><td>強：雲被壓在中心</td><td>空間很平滑，但還原更糊</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">延伸練習：把 <code>train(..., beta=1.0)</code> 改成 0.1 和 4，比較散佈圖與取樣。</div>

<div class="src">Higgins et al., β-VAE, ICLR 2017（S5）</div>

<!--
○ 選修（3 分）：早做完的學員可以做這個延伸，每個 beta 約多花一次訓練時間。
-->

---

<div class="eyebrow">附錄 · 備用</div>

# ELBO 從哪裡來（給想看推導的人）

<div style="font-size:19px" class="mt-4">

log p(x) ＝ log 𝔼<sub>q(z|x)</sub>&#91; p(x|z) p(z) ／ q(z|x) &#93;<br>
　　　　≥ 𝔼<sub>q(z|x)</sub>&#91; log p(x|z) &#93; − KL( q(z|x) ‖ p(z) )　　（Jensen 不等式）<br>
　　　　＝ −重建損失 − KL ＝ <strong>ELBO</strong>

</div>

<div class="muted mt-3" style="font-size:17px">q(z|x)＝編碼器給的雲；p(x|z)＝解碼器；p(z)＝N(0, I)</div>

<div class="takeaway mt-3">不考推導。只要記得：最後一行就是 lab07 的 <code>-(recon + kl)</code>。</div>

<!--
△ 備用（3 分）：只有學員問「下界是怎麼來的」才用。q(z|x) 是編碼器給的雲，p(z) 是 N(0, I)，p(x|z) 是解碼器。
-->

---

<div class="eyebrow">05 · Lab L2-3</div>

# Lab 1／7：我們要做出什麼？

<div class="grid grid-cols-[1fr_1.15fr] gap-6 mt-2" style="font-size:19px">
<div>

**打開筆記本**：<code>lab07-vae.ipynb</code>（在 <code>materials/</code>）→ Open in Colab<br>
執行階段：**T4 GPU**

1. AE 的潛在空間真的有洞嗎？
2. VAE 抽出來的「新商品」像不像？
3. SD 的 VAE 把 512px 照片壓小幾倍？還原後 PSNR 多少？

</div>
<div>

<img class="photo" src="/fmnist-samples.png" alt="Fashion-MNIST 測試集前 16 張：靴子、毛衣、褲子、T 恤等 28×28 灰階圖" style="width:100%;border:none">
<div class="shot-cap">今天的資料：Fashion-MNIST 測試集前 16 張（Zalando，MIT）</div>

</div>
</div>

<div class="takeaway mt-3">驗收看兩件事：潛在空間能不能「隨便取點」，和 512px 照片壓縮後還剩多少品質。</div>

<!--
★ Lab 開始（3 分）：Fashion-MNIST 下載很快（約 30 MB）。SD 的 VAE 第一次下載約數百 MB（時間待實測）。
備案：沒有 GPU → EPOCHS＝3（本機 CPU 每個 epoch 約 10 秒）。
-->

---

<div class="eyebrow">05 · Lab L2-3</div>

# Lab 2／7：筆記本拆成哪幾塊？

<div class="flex items-center gap-2 mt-4" style="font-size:17px">
  <div class="node"><code>VAE.encode</code><small>→ mu、logvar</small></div><span class="arrow">→</span>
  <div class="node node--warm"><code>forward</code><small>重參數化 → z</small></div><span class="arrow">→</span>
  <div class="node node--secondary"><code>VAE.decode</code><small>→ x_hat</small></div><span class="arrow">→</span>
  <div class="node"><code>loss_fn</code><small>重建＋beta×KL</small></div>
</div>

<div class="flex items-center gap-2 mt-4" style="font-size:17px">
  <div class="node"><code>embed</code><small>散佈圖</small></div><span class="arrow">→</span>
  <div class="node"><code>decode_grid</code><small>找洞</small></div><span class="arrow">→</span>
  <div class="node node--primary"><code>sample</code><small>生成</small></div><span class="arrow">→</span>
  <div class="node"><code>AutoencoderKL</code><small>SD 的 VAE</small></div>
</div>

<div class="takeaway mt-4">四個 TODO：重參數化、KL、<code>sample</code>、SD VAE 的編碼與解碼。AE 和 VAE 是同一個類別，只差 <code>variational</code> 開關。</div>

<!--
★ 拆塊（3 分）：強調「同一個類別、同一個訓練迴圈」：AE ＝ variational=False、beta=0。這樣比較才公平。
-->

---

<div class="eyebrow">05 · Lab L2-3</div>

# Lab 3／7：Specify

<div style="font-size:18px" class="mt-2">

<strong>【目標】</strong>同一個網路訓練成 AE 與 VAE，比較潛在空間；用 SD 的 VAE 量 512px 照片的壓縮與品質<br>
<strong>【輸入與輸出】</strong>Fashion-MNIST <code>&#91;B, 1, 28, 28&#93;</code>（0–1）→ mu、logvar <code>&#91;B, 2&#93;</code> → 還原 <code>&#91;B, 1, 28, 28&#93;</code><br>
<strong>【限制】</strong>潛在空間 2 維（為了畫圖）；AE 與 VAE 用同樣的 epochs；Colab T4<br>
<span class="muted" style="font-size:16px">為什麼：只差一個變因（有沒有 KL），比較才有意義</span><br>
<strong>【驗收】</strong>① VAE 的 KL 比 AE 小、重建略差　② VAE 座標大約在 ±3 內　③ 取樣看得出是衣物　④ SD VAE：印出 48 倍與 PSNR、秒數、VRAM

</div>

<!--
★ Specify（3 分）：驗收 ① 是「預期的取捨」：VAE 為了平滑放棄一點重建品質。
-->

---

<div class="eyebrow">05 · Lab L2-3</div>

# Lab 4／7：Generate → Execute

<PromptBox>
這是 PyTorch 筆記本，請只填四個 # TODO：<br>
① VAE.forward 的重參數化：std ＝ exp(0.5×logvar)，eps 用 randn_like，z ＝ mu ＋ std×eps<br>
② loss_fn 的 KL：−0.5 × Σ(1 ＋ logvar − mu² − exp(logvar))，除以張數<br>
③ sample：z 從標準常態抽（n × 2），交給 decode<br>
④ SD VAE：encode(x).latent_dist.mode() 得到潛在表示，decode(lat).sample 還原<br>
不要改網路大小與 epochs。每一格說明每一行在做什麼。
</PromptBox>

<div class="steps mt-2" style="font-size:17px">
  <div><span class="num">1</span>兩次訓練（AE、VAE）時間待 T4 實測；等待時看 loss 的「重建」和「KL」兩欄</div>
  <div><span class="num">2</span>沒有 Agent 額度：照「重參數化」、「損失」、「取樣與內插」三頁的程式填；卡住開 <code>-solution.ipynb</code></div>
</div>

<!--
★ 執行（約 20 分）：先讓學員填 ①② 再執行訓練格；①② 沒填，第 2 步會出現 NameError（z、kl 沒有定義），這是正常的提醒。
常見錯誤：KL 少了負號（loss 越訓練越大）；用 Python 內建 sum 而不是 torch.sum（不會錯，但讀起來容易和 numpy 混淆）。
-->

---

<div class="eyebrow">05 · Lab L2-3</div>

# Lab 5／7：執行到散佈圖，對照你的預測

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-2" style="font-size:18px">
<div>

填完 TODO、執行第 1–4 步後，回到「練習：KL 會讓散佈圖變成什麼樣子？」：

1. 你預測對了幾格？
2. AE 的網格裡，哪一區是「垃圾」？在散佈圖上那一區有沒有點？
3. VAE 的網格從左上到右下，衣物是怎麼「漸漸變過去」的？

</div>
<div>

<div class="node node--primary"><strong>看圖的訣竅</strong><small>網格的每一格就是散佈圖上的一個座標：把兩張圖疊在腦中對照</small></div>

</div>
</div>

<div class="takeaway mt-4">洞不是比喻：網格上的垃圾，就落在散佈圖上沒有點的地方。</div>

<!--
★ 對照（5 分）：AE 的網格只涵蓋 ±3；AE 的點可能大多不在這個範圍，所以網格上很多格是「沒學過的地方」。
-->

---

<div class="eyebrow">05 · Lab L2-3</div>

# Lab 6／7：Audit → Iterate

<table style="font-size:17px">
<thead><tr><th style="width:30%">稽核問題</th><th>具體動作</th><th style="width:30%">應該是</th></tr></thead>
<tbody>
<tr><td>AE 真的沒有用 KL？</td><td>看 AE 那幾行 loss 的「0.0×KL」</td><td>總損失＝重建</td></tr>
<tr><td>KL 的正負號對嗎？</td><td>看 VAE 印出的 KL</td><td>正數；訓練中慢慢穩定</td></tr>
<tr><td>取樣用的分布和訓練一樣？</td><td>看 <code>sample</code></td><td><code>torch.randn</code>（標準常態）</td></tr>
<tr><td>SD VAE 的輸入範圍？</td><td>看 <code>* 2 - 1</code> 那一行</td><td>−1～1（不是 0–1）</td></tr>
<tr><td>還原哪裡最差？</td><td>看差異圖最亮的地方</td><td>小字、細線（實跑後填入）</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">一次只改一件事：例如 beta 改成 4，看散佈圖和取樣怎麼變。</div>

<!--
★ 稽核（8 分）：最常見錯誤：KL 少了負號 → KL 變成負的、越訓練越大，散佈圖炸開。第二常見：SD VAE 吃了 0–1 的輸入 → 還原的顏色整個偏掉。
-->

---

<div class="eyebrow">05 · Lab L2-3 · Ship</div>

# Lab 7／7：交給行銷科技組的一張表

<table class="mt-2" style="font-size:18px">
<thead><tr><th style="width:34%">項目</th><th>數字</th><th>來源</th></tr></thead>
<tbody>
<tr><td>輸入 → 潛在表示</td><td>3×512×512 → 4×64×64</td><td>第 6 步印出的 shape</td></tr>
<tr><td>數字個數</td><td>786,432 → 16,384（48 倍）</td><td>第 6 步</td></tr>
<tr><td>還原品質 PSNR</td><td>講師實跑後填入</td><td>第 6 步</td></tr>
<tr><td>編碼＋解碼時間（T4、fp16）</td><td>講師實跑後填入</td><td>第 6 步</td></tr>
<tr><td>VRAM 峰值</td><td>講師實跑後填入</td><td>第 6 步</td></tr>
<tr><td>已知弱點</td><td>講師實跑後填入（看差異圖最亮處）</td><td>差異圖</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">今天的交付是「事實表」：第四天決定要不要在 T4 上大量生成時，用的就是這幾個數字。</div>

<!--
★ Ship（4 分）：PSNR（Peak Signal-to-Noise Ratio，峰值訊噪比）：單位 dB，越高越像；PSNR＝10·log10(1／MSE)，像素範圍 0–1。
48 倍是由 shape 算出來的，不是實驗數字；PSNR、時間、VRAM 一定要等 T4 實跑。
-->

---

<div class="eyebrow">06 · Measure & Risk（風險）</div>

# 風險：生成的「新」商品，會不會是抄來的？

<div class="grid grid-cols-[1.1fr_1fr] gap-6 mt-2">
<div>

<div class="placeholder" style="height:200px">上排：VAE 生成的 8 張；下排：訓練集裡最像的那張（附距離）<small>講師實跑後替換（lab07 第 5 步）</small></div>

</div>
<div style="font-size:18px">

- 生成模型可能「背下」訓練資料，原封不動吐出來
- 檢查法：每張生成圖找訓練集裡最近的一張，比距離、用眼睛看
- 訓練資料若有別人的設計或個人照片 → 侵權與隱私問題

</div>
</div>

<div class="takeaway mt-3">「新」要自己驗證：第四天用 Stable Diffusion 生成商品圖時，同樣要做最近鄰檢查。</div>

<div class="src">大型擴散模型可重現訓練圖片的研究：Carlini et al., Extracting Training Data from Diffusion Models, 2023（S6）</div>

<!--
★ 風險（4 分）：今天的小 VAE 只有 2 維潛在空間，很難背下 60,000 張圖；但大模型會。這個檢查方法會在 D4-3（LoRA 品牌風格）再用一次。
-->

---

<div class="eyebrow">總整理</div>

# 今天學到的概念鏈

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-4">
  <span class="chip">像素太貴</span><span class="arrow">→</span>
  <span class="chip">AE 有洞</span><span class="arrow">→</span>
  <span class="chip">μ、σ：一團雲</span><span class="arrow">→</span>
  <span class="chip">z ＝ μ ＋ σ·ε</span><span class="arrow">→</span>
  <span class="chip">重建＋KL（ELBO）</span><span class="arrow">→</span>
  <span class="chip">取樣、內插</span><span class="arrow">→</span>
  <span class="chip">SD 的 VAE：48 倍</span>
</div>

<div class="takeaway mt-6">KL 把雲拉到同一個中心，空間才沒有洞；沒有洞，才能「隨便取一點」生成。</div>

<!--
★ 總整理（2 分）：請一位學員用自己的話說「為什麼 Stable Diffusion 的壓縮器是 VAE 不是 AE」。答案要包含「洞」和「在潛在空間生成」。
-->

---

<div class="eyebrow">隨堂檢核</div>

# 選擇題（iPAS 題型）

<div class="mcq">

1. VAE 的編碼器輸出什麼？（　）<br><span class="opts">A. 一個點 z　B. 一個類別標籤　C. 平均 μ 與寬度 σ　D. 重建的影像</span>
2. 重參數化 z ＝ μ ＋ σ·ε 的主要目的？（　）<br><span class="opts">A. 讓梯度能傳回 μ 與 σ　B. 讓模型變小　C. 加快推論　D. 不需要 GPU</span>
3. 把 KL 項拿掉（beta ＝ 0），潛在空間最可能？（　）<br><span class="opts">A. 更平滑　B. 全部集中在原點　C. 不會改變　D. 出現大片空洞，隨機取點常解碼成垃圾</span>
4. Stable Diffusion 1.5 的 VAE 把 512×512×3 壓成？（　）<br><span class="opts">A. 4×64×64　B. 3×256×256　C. 1×28×28　D. 768 維向量</span>

</div>

<!--
★ 檢核（4 分）。答案：1 C、2 A、3 D、4 A。
-->

---
hostOnly: true
---

<div class="eyebrow">下一步</div>

# 下一堂 D2-4：把影像和聲音變成編號

<div class="node node--primary mt-2">資訊部與客服中心要用低位元率儲存通話錄音與產線影像。VAE 的潛在表示是連續的小數，沒辦法變成固定位元數的「編號」；下一堂把瓶頸變成一本編碼簿（VQ-VAE），也聽聽 EnCodec 在不同位元率下的聲音。</div>

<!--
★ 只給講師的託管版看。
-->
