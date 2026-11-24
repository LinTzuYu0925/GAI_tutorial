---
theme: default
title: GAN 一直畫一樣的圖？從零寫一個擴散模型
info: |
  生成式AI原理 · D3-3
  行銷部嫌 GAN 的型錄縮圖變化不夠。把圖一步一步弄髒，再訓練網路一步一步「猜出雜訊、扣掉雜訊」：從零寫一個小 DDPM，和 D3-1 的 DCGAN 比多樣性與速度。
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
exportFilename: 11-ddpm-from-scratch
layout: center
class: cover
---

<div class="eyebrow">生成式AI原理 · D3-3</div>

# GAN 一直畫一樣的圖？從零寫一個擴散模型

<p class="subtitle">先把圖弄髒，再學會一步一步擦乾淨：自己寫一個小 DDPM，和 D3-1 的 GAN 比一比</p>

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-8">
  <span class="chip">多樣性不夠</span><span class="arrow">→</span>
  <span class="chip">往前加噪</span><span class="arrow">→</span>
  <span class="chip">預測雜訊</span><span class="arrow">→</span>
  <span class="chip">U-Net ＋ 時間</span><span class="arrow">→</span>
  <span class="chip">走 1000 步回來</span><span class="arrow">→</span>
  <span class="chip">生成三難第二列</span>
</div>

<!--
★ 開場（2 分）：D3-1 的 GAN 一次就畫完，很快；今天的擴散模型要走很多步，慢，但多樣性好。今天要用自己的數字說「好多少、慢多少」。
-->

---

<div class="eyebrow">00 · Frame（定義問題）</div>

# 行銷部：GAN 畫的型錄縮圖，變化不夠

<div class="ticket mt-2">
  <div class="ticket-head">【需求單 #D3-3】部門：行銷部<span>公司：曜嶼電子 <span class="fiction" style="color:#fff;border-color:#fff">虛構</span></span></div>
  <dl>
    <dt>問題</dt><dd>GAN 生成器畫出來的圖常常差不多（D3-1 的 mode collapse），要不要改用擴散模型？</dd>
    <dt>現況痛點</dt><dd>型錄縮圖缺乏變化，設計師要一張一張手動挑</dd>
    <dt>成功指標（KPI）</dt><dd>樣本多樣性不低於 DCGAN（用 D3-1 同一個量法）；記下取樣時間和步數的關係</dd>
    <dt>可用資料</dt><dd>Fashion-MNIST（和 D3-1 一樣，代替商品縮圖）</dd>
    <dt>限制與法規</dt><dd>Colab T4；32 × 32 小圖、小模型；生成圖不能是訓練圖的翻版</dd>
    <dt>為何現有工具不夠</dt><dd>GAN 的多樣性沒有保證：D3-1 要另外量，才知道有沒有崩塌</dd>
  </dl>
</div>

<!--
★ 需求單（2 分）：今天的問題是「要不要換工具」。答案不是「擴散比較新所以比較好」，而是拿 D3-1 同一個量法、同一份資料比出來。
-->

---

<div class="eyebrow">學習目標</div>

# 今天結束時，你能夠……

1. **畫出**往前加噪的一排圖：x₀ → x_t → x_T
2. **讀懂**「一行跳到第 t 步」的公式，說出每個符號
3. **說明**訓練時網路在猜什麼：**雜訊**，不是原圖
4. **寫出**時間嵌入和 1000 步的取樣迴圈（Colab T4）
5. **把擴散模型放上生成三難**：用自己量到的多樣性和秒數

<!--
★ 目標（2 分）。不教：分數匹配（score matching）與 ELBO 的推導（△ 附錄只認名字）、條件式生成（D4-1）、潛在擴散／Stable Diffusion（D4-2）。
-->

---

<div class="eyebrow">00 · Frame · 回到 D3-1 的三角形</div>

# 生成三難：GAN 快又清楚，但多樣性沒保證

<div class="grid grid-cols-[1fr_1.15fr] gap-6 mt-1 items-center">
<div>

<svg viewBox="0 0 320 260" style="width:100%;max-height:260px" aria-label="三角形，三個角是品質、多樣性、速度；GAN 放在品質和速度那一邊，多樣性那一角打上問號">
  <polygon points="160,25 30,230 290,230" fill="var(--surface)" stroke="var(--muted-text)" stroke-width="2"/>
  <text x="160" y="18" text-anchor="middle" style="font-size:18px" fill="var(--text)">品質</text>
  <text x="22" y="252" style="font-size:18px" fill="var(--text)">多樣性 ？</text>
  <text x="262" y="252" style="font-size:18px" fill="var(--text)">速度</text>
  <circle cx="210" cy="120" r="12" fill="var(--warm-accent)"/>
  <text x="228" y="126" style="font-size:18px" fill="var(--warm-accent)">GAN</text>
</svg>

</div>
<div style="font-size:18px">

| D3-1 的 DCGAN（講師 T4 實跑） | |
|---|---|
| 品質 | 看得出衣物 |
| 速度 | 一次前向就畫完 |
| 多樣性 | 這次**沒有**崩塌：兩兩距離 22.08（真圖 22.90） |

<div class="muted mt-2" style="font-size:16px">但 GAN 沒有任何一項損失在要求「畫得多樣」：換資料、換參數，就可能崩塌（D3-1 第 15 頁）。</div>

</div>
</div>

<div class="takeaway mt-2">換工具之前先定好量法：今天用 D3-1 同一個「兩兩距離」，和 DCGAN 比。</div>

<div class="src">DCGAN 數字：lab09 講師 Colab T4 實跑（SEED 0，20 epochs）；生成三難：Xiao et al., ICLR 2022（S3）</div>

<!--
★ Frame（4 分）：誠實面對 D3-1 的結果：我們那次沒有崩塌。行銷部的抱怨來自真實商品圖（更複雜的資料、更大的模型），GAN 在那裡比較容易崩塌；Xiao et al. 也寫 GAN「mode coverage 差」。所以今天不是要證明 GAN 一定崩塌，而是看擴散模型的多樣性有沒有「保證」得比較好，代價是什麼。
兩兩距離：32 張圖兩兩之間的平均像素距離，越小代表越常畫同樣的東西（D3-1 第 15 頁）。
-->

---

<div class="eyebrow">01 · Try（先看結果）</div>

# 現成的擴散模型：16 張都不一樣，但要走 1000 步

<div class="grid grid-cols-[1.4fr_1fr] gap-6 mt-2">
<div>

<div class="placeholder" style="height:250px;padding:16px 24px">google/ddpm-cifar10-32：16 張 32 × 32 小照片（飛機、汽車、鳥、貓……），1000 步<small>講師 T4 實跑後替換（lab11 <code>try_pretrained.png</code>）</small></div>

</div>
<div style="font-size:18px">

- 擴散模型（diffusion model）：DDPM 論文作者在 CIFAR-10 上訓練的
- 一行就能用：<code>DDPMPipeline.from_pretrained(...)</code>
- 16 張 × 1000 步：講師 T4 實跑後填入 秒

</div>
</div>

<div class="takeaway mt-3">先猜：同一個網路要跑 1000 次才畫完一張，會比 GAN 慢幾倍？</div>

<div class="src">google/ddpm-cifar10-32，Apache-2.0（S4）；Ho et al., DDPM, NeurIPS 2020（S1）</div>

<!--
★ 示範（5 分）：講師執行 lab11 的 A 部分。問學員：「16 張裡有長得一樣的嗎？」再問：「GAN 畫 16 張要多久？」（一次前向，幾乎是瞬間）。DDPM（Denoising Diffusion Probabilistic Models，去噪擴散機率模型）是論文名稱，今天就叫它 DDPM。
-->

---

<div class="eyebrow">02 · Open（打開黑盒子）· 往前加噪</div>

# 先把圖弄髒：一步加一點雜訊，加 1000 步

<div class="placeholder mt-2" style="height:190px;padding:16px 24px">一隻短靴：t＝0、50、100、250、500、750、999 的 x_t，每格標 √ᾱ_t<small>講師 T4 實跑後替換（lab11 <code>forward_strip.png</code>）</small></div>

<div class="grid grid-cols-3 gap-4 mt-3" style="font-size:17px">
<div class="node"><strong>x₀</strong><small>原圖（t＝0）</small></div>
<div class="node node--warm"><strong>x_t</strong><small>第 t 步：原圖 ＋ 一些雜訊</small></div>
<div class="node"><strong>x_T</strong><small>T＝1000 步後：幾乎是純雜訊</small></div>
</div>

<div class="takeaway mt-3">弄髒很簡單，不用學；要學的是反過來：從雜訊一步一步擦回衣服。</div>

<div class="src">往前加噪（forward process）：Ho et al., 2020 §2（S1）；DL 課 pp.85–87 介紹過概念，沒有寫程式</div>

<!--
★ 往前加噪（4 分）：forward process（往前加噪）。DL 課 pp.85–87 看過「加噪、去噪」的示意圖；今天第一次寫成程式。強調：往前這一半沒有任何參數，是固定公式；整個模型只學「往回」那一半。
-->

---

<div class="eyebrow">02 · Open · 一行跳到第 t 步</div>

# 不用真的加 250 次：一行直接算出第 t 步

<div style="font-size:24px" class="mt-2 text-center">

$$x_t = \sqrt{\bar\alpha_t}\; x_0 \;+\; \sqrt{1-\bar\alpha_t}\;\varepsilon$$

</div>

<table class="mt-2" style="font-size:17px">
<thead><tr><th style="width:24%">符號</th><th>讀作</th></tr></thead>
<tbody>
<tr><td>x₀、x_t</td><td>原圖；第 t 步的髒圖（t 從 0 到 999）</td></tr>
<tr><td>ε（epsilon）</td><td>一張和圖一樣大的隨機雜訊（標準常態，<code>torch.randn_like(x0)</code>）</td></tr>
<tr><td>ᾱ_t（alpha bar）</td><td>到第 t 步為止，原圖還「留下」多少：t＝0 時是 1，越後面越接近 0</td></tr>
<tr><td>例：t＝250</td><td>√ᾱ ＝ 0.72、√(1−ᾱ) ＝ 0.69 → x₂₅₀ ＝ 0.72 × 短靴 ＋ 0.69 × 雜訊</td></tr>
</tbody>
</table>

```python
x_t = sqrt_ab[t] * x0 + sqrt_1mab[t] * eps     # 原圖乘一個數，加上雜訊乘一個數
```

<div class="takeaway mt-2">第 t 步的髒圖 ＝ 原圖「打幾折」＋ 雜訊「放多少」：訓練時可以隨便挑一個 t，一行做出題目。</div>

<!--
★ 一行公式（5 分）：這是今天唯一要讀懂的公式。讀法：「原圖乘上根號 alpha bar，加上雜訊乘上根號一減 alpha bar」。兩個係數的平方加起來是 1：圖越淡，雜訊越濃。
例子 0.72、0.69 由固定的排程公式算出（lab11 B 部分印出來的表，任何機器都一樣）。
為什麼能一行跳：每一步加的都是常態雜訊，很多個常態雜訊加起來還是一個常態雜訊（Ho et al. 式 4）。不用推導。
-->

---

<div class="eyebrow">02 · Open · 雜訊排程</div>

# 雜訊排程：每一步加多少，事先定好

<div class="grid grid-cols-[1.3fr_1fr] gap-6 mt-2">
<div>

<div class="placeholder" style="height:250px;padding:16px 24px">√ᾱ_t（原圖）往下、√(1−ᾱ_t)（雜訊）往上，兩條線在 t≈259 交叉<small>講師 T4 實跑後替換（lab11 <code>schedule.png</code>）</small></div>

</div>
<div style="font-size:18px">

- β_t（beta）：第 t 步**加**的雜訊量，從 0.0001 線性增加到 0.02
- ᾱ_t：把每一步「留下的 1 − β」全部乘起來 → 越乘越小
- t＝259 之後，雜訊就比原圖多

```python
betas = torch.linspace(1e-4, 0.02, 1000)
alpha_bar = torch.cumprod(1 - betas, 0)
```

</div>
</div>

<div class="takeaway mt-3">排程是寫死的兩行：β_t 越來越大，ᾱ_t 就越來越小。</div>

<div class="src">線性排程 β₁＝10⁻⁴ 到 β_T＝0.02、T＝1000：Ho et al., 2020 §4（S1）</div>

<!--
★ 排程（3 分）：noise schedule（雜訊排程）。cumprod 讀作「累乘」：第 t 個數＝前面全部乘起來。t＝259 是 lab11 印出來的交叉點（固定公式）。
-->

---

<div class="eyebrow">02 · Open · 訓練</div>

# 訓練：給網路一張髒圖，叫它猜「加了什麼雜訊」

<div class="grid grid-cols-[1.15fr_1fr] gap-6 mt-2">
<div>

```python
t   = torch.randint(0, T, (B,))       # 每張圖隨機挑一個步數
eps = torch.randn_like(x0)            # 隨機雜訊（正確答案）
x_t = sab[t]*x0 + s1mab[t]*eps        # 一行做出題目
eps_hat = model(x_t, t)               # 網路猜雜訊
loss = F.mse_loss(eps_hat, eps)       # 猜得多準？MSE
opt.zero_grad(); loss.backward(); opt.step()
```

</div>
<div style="font-size:18px">

- 題目和答案都是**程式自己出的**：不用標註
- 損失就是 DL 課的 **MSE**：每個像素「猜的雜訊 − 真的雜訊」的平方，再平均
- 最後一行和 D1-3 的訓練迴圈一模一樣

</div>
</div>

<div class="takeaway mt-3">擴散模型的訓練＝一個很普通的迴歸問題：輸入髒圖和 t，輸出雜訊。</div>

<div class="src">預測雜訊與簡化損失 L_simple：Ho et al., 2020 §3.2、§3.4 式 14（S1）</div>

<!--
★ 訓練（5 分）：逐行用中文讀。強調第一行：每張圖的 t 都不一樣，同一個 batch 裡有乾淨的、也有幾乎全是雜訊的，網路要全部都會。最後一行就是 D1-3 的三行，學員已經寫過。
-->

---

<div class="eyebrow">02 · Open · 常見誤解</div>

# 網路猜的是「雜訊」，不是「乾淨的圖」

<div class="grid grid-cols-2 gap-6 mt-3" style="font-size:18px">
<div class="node node--warm"><strong>常見誤解</strong><small>「model(x_t, t) 會直接吐出一張乾淨的衣服」→ 寫成 <code>F.mse_loss(model(x_t, t), x0)</code></small></div>
<div class="node node--primary"><strong>DDPM 的做法</strong><small>model(x_t, t) 吐出 ε̂：「這張圖裡的雜訊長這樣」。乾淨的圖是用 x_t <strong>扣掉</strong> ε̂ 算出來的</small></div>
</div>

<div class="flex items-center justify-center gap-2 mt-4" style="font-size:17px">
  <div class="node" style="width:18%">x_t<small>髒圖 &#91;B,1,32,32&#93;</small></div><span class="arrow">→</span>
  <div class="node node--warm" style="width:18%"><strong>U-Net</strong><small>＋ 步數 t</small></div><span class="arrow">→</span>
  <div class="node node--primary" style="width:20%">ε̂<small>預測的雜訊 &#91;B,1,32,32&#93;</small></div><span class="arrow">→</span>
  <div class="node" style="width:24%">x_t 扣掉一點 ε̂<small>→ 稍微乾淨的 x_{t−1}</small></div>
</div>

<div class="takeaway mt-4">輸出和輸入一樣大，但內容是「雜訊」；每一步只扣掉一點點，要扣 1000 次。</div>

<div class="src">Ho et al., 2020 §3.2：ε_θ 預測 ε（S1）</div>

<!--
★ 誤解（3 分）：這是 lab 最常見的錯誤（Lab 6／7 會再稽核一次）。「也可以預測 x₀ 嗎？」可以，有的論文這樣做，但 DDPM 論文發現預測雜訊的樣本品質比較好（S1 §3.4）。今天統一預測雜訊。
-->

---

<div class="eyebrow">02 · Open · 去噪網路</div>

# 去噪網路就是 D2-2 的 U-Net，多一個輸入 t

<div class="flex items-center justify-center gap-2 mt-3" style="font-size:17px">
  <div class="node" style="width:15%">x_t<small class="nw">&#91;B,1,32,32&#93;</small></div><span class="arrow">→</span>
  <div class="node node--primary" style="width:17%"><strong>往下</strong><small>三次池化，32 → 4</small></div><span class="arrow">→</span>
  <div class="node node--warm" style="width:15%"><strong>瓶頸</strong><small class="nw">&#91;B,256,4,4&#93;</small></div><span class="arrow">→</span>
  <div class="node node--secondary" style="width:17%"><strong>往上</strong><small>三次放大，4 → 32</small></div><span class="arrow">→</span>
  <div class="node" style="width:15%">ε̂<small class="nw">&#91;B,1,32,32&#93;</small></div>
</div>

<svg viewBox="0 0 900 70" style="width:100%;height:70px" aria-label="跳接箭頭從往下那一側連到往上那一側">
  <path d="M250,8 C330,60 570,60 650,8" fill="none" stroke="var(--primary)" stroke-width="3" marker-end="url(#sk11)"/>
  <defs><marker id="sk11" markerWidth="10" markerHeight="10" refX="7" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--primary)"/></marker></defs>
  <text x="450" y="64" text-anchor="middle" style="font-size:18px" fill="var(--primary)">跳接：和 D2-2 一樣，用 torch.cat 接起來</text>
</svg>

<div class="grid grid-cols-2 gap-6 mt-1" style="font-size:18px">
<div class="node"><strong>D2-2 U-Net</strong><small>PCB 影像 → 每個像素「是不是瑕疵」&#91;B,1,H,W&#93;</small></div>
<div class="node node--primary"><strong>今天的 TinyUNet</strong><small>髒圖 x_t ＋ 步數 t → 每個像素「雜訊是多少」&#91;B,1,32,32&#93;；參數約 198 萬</small></div>
</div>

<div class="takeaway mt-3">輸入輸出一樣大、逐像素回答：U-Net 正好；只差要告訴它「現在是第幾步」（下一頁）。</div>

<div class="src">D2-2 第 6 頁（同一張圖）；Ho et al., 2020 §4 用 U-Net 當去噪網路（S1）</div>

<!--
★ U-Net（4 分）：直接拿 D2-2 的主角圖。學員應該能自己說出 shape：32 → 16 → 8 → 4。參數 1,981,921 是 TinyUNet 的架構固定值（lab11 C 部分印出）。
-->

---

<div class="eyebrow">02 · Open · 時間嵌入</div>

# 時間嵌入：讓網路知道「現在有多髒」

<div class="grid grid-cols-[1.25fr_1fr] gap-6 mt-2">
<div>

<div class="placeholder" style="height:210px;padding:16px 24px">每一直行是一個 t（0～999）的 64 維 sin／cos 向量：上面幾維變化快、下面幾維變化慢<small>講師 T4 實跑後替換（lab11 <code>time_embedding.png</code>）</small></div>

```python
h = self.conv1(x)
h = h + self.time(temb)[:, :, None, None]   # 每個通道加一個數
```

</div>
<div style="font-size:18px">

- t＝50 的圖只要擦一點；t＝900 的圖幾乎要重畫：**同一個網路，要做不同的事**
- 把 t 變成一條 64 個數的向量：不同頻率的 sin、cos（**時間嵌入**，time embedding）
- 每一個區塊都把它加進特徵圖

</div>
</div>

<div class="takeaway mt-3">t 不能只當一個數字丟進去：變成 sin／cos 向量，相近的 t 得到相近的向量。</div>

<div class="src">Ho et al., 2020 §4：Transformer 的 sinusoidal position embedding（S1）；D5-2 的 Transformer 會再看到它</div>

<!--
★ 時間嵌入（4 分）：embedding（嵌入）：把一個東西變成一串數字。這個 sin／cos 的做法來自 Transformer 的「位置編碼」，D5-2 會再看到，到時候說「D3-3 看過」。[:, :, None, None] 讀作「多兩個長度 1 的維度，好加到每個像素上」。
-->

---

<div class="eyebrow">02 · Open · 練習</div>

# 練習：第幾步就認不出來了？

<div class="muted" style="font-size:17px">不用 AI。① 先在「先猜」欄寫「看得出／看不出」② 打開 lab11，執行到 B 部分的練習格，改 <code>t</code> ③ 填 √ᾱ_t。第一列已填好。</div>

<table class="fill tight vlines mt-1">
<thead><tr><th style="width:12%">t</th><th style="width:30%">先猜：看得出是短靴嗎？</th><th style="width:28%">執行後：看得出嗎？</th><th>√ᾱ_t（原圖佔）</th></tr></thead>
<tbody>
<tr><td>50</td><td>看得出</td><td>看得出，有一點雜點</td><td>0.985</td></tr>
<tr><td>250</td><td class="blank"><FillIn id="strip.p250" /></td><td class="blank"><FillIn id="strip.r250" /></td><td class="blank"><FillIn id="strip.a250" /></td></tr>
<tr><td>500</td><td class="blank"><FillIn id="strip.p500" /></td><td class="blank"><FillIn id="strip.r500" /></td><td class="blank"><FillIn id="strip.a500" /></td></tr>
<tr><td>750</td><td class="blank"><FillIn id="strip.p750" /></td><td class="blank"><FillIn id="strip.r750" /></td><td class="blank"><FillIn id="strip.a750" /></td></tr>
<tr><td colspan="2">「已經認不出來」的最小 t 大約是？</td><td class="blank" colspan="2"><FillIn id="strip.first" hint="例：t＝……，√ᾱ 大約……" /></td></tr>
</tbody>
</table>

<FillClear group="strip" />

<!--
★ 無 AI 檢核點（6 分）：個人作業，不收回。讓學員自己發現：1000 步裡，後面好幾百步其實「已經看不出來」。這會在 Lab 和第 15 頁的取樣迴圈用到：取樣時前面幾百步，網路是在「從一片雜訊裡決定要畫什麼」。
-->

---
hostOnly: true
---

<div class="eyebrow">02 · Open · 練習解答</div>

# 練習解答：一半的步數還沒走完，短靴就不見了

<table class="vlines" style="font-size:18px">
<thead><tr><th style="width:12%">t</th><th style="width:40%">看得出是短靴嗎？</th><th>√ᾱ_t（原圖佔）</th></tr></thead>
<tbody>
<tr><td>250</td><td>看得出，但雜訊已經和原圖差不多濃</td><td>0.722（雜訊 0.692）</td></tr>
<tr><td>500</td><td>看不出：只剩一片雜點</td><td>0.279</td></tr>
<tr><td>750</td><td>看不出</td><td>0.057</td></tr>
<tr><td colspan="2">雜訊開始比原圖多的 t</td><td>259（lab11 印出）</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">還不到第 500 步就認不出來：線性排程的後半段幾乎都是雜訊。</div>

<!--
★ 解答（2 分）：√ᾱ 是固定公式算出的，每個人一樣；「看得出嗎」每個人判斷不同，t 落在 300～450 之間都合理。延伸（不考）：Nichol & Dhariwal（2021）指出線性排程「太快把資訊破壞掉」，改用 cosine 排程（S5）。
-->

---

<div class="eyebrow">02 · Open · 取樣</div>

# 取樣：從純雜訊出發，走 1000 步回來

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-2">
<div>

```python
x = torch.randn(n, 1, 32, 32)              # x_T：純雜訊
for t in reversed(range(1000)):            # 999, 998, …, 0
    eps_hat = model(x, t)                  # 猜這張圖的雜訊
    mean = (x - betas[t]/sqrt_1mab[t]*eps_hat) / alphas[t].sqrt()
    x = mean + betas[t].sqrt()*torch.randn_like(x) if t > 0 else mean
```

</div>
<div style="font-size:18px">

- 第 3 行：**扣掉一點**猜到的雜訊（係數很小），再放大一點點
- 第 4 行：除了最後一步，**再加回一點新的雜訊**
- 每張圖都從不同的雜訊出發 → 畫出不同的衣服

</div>
</div>

<div class="placeholder mt-2" style="height:120px;padding:12px 24px">同一張圖在 t＝999、750、500、250、100、0 的樣子<small>講師 T4 實跑後替換（lab11 <code>reverse_strip.png</code>）</small></div>

<div class="takeaway mt-2">1000 步＝網路跑 1000 次：這就是擴散模型慢的原因。</div>

<div class="src">Ho et al., 2020 Algorithm 2（σ_t² ＝ β_t）（S1）</div>

<!--
★ 取樣（5 分）：sampling（取樣）。不用背係數，讀法是「扣掉一小部分雜訊，再加一點新的隨機」。為什麼要加回雜訊？每一步都留一點隨機性，結果才會多樣；DDIM（Lab 的 F 部分）把它拿掉，可以跳著走。
-->

---

<div class="eyebrow">03 · Measure · 為什麼好訓練</div>

# 為什麼擴散模型比 GAN 好訓練？

<div class="grid grid-cols-2 gap-6 mt-2">
<div>

<img class="photo" src="/lab09-run-loss.png" alt="D3-1 的 GAN 損失曲線：D 和 G 的損失整段上下劇烈跳動" style="width:100%;max-height:200px;object-fit:contain">
<div class="shot-cap">D3-1 的 GAN：兩個損失一直搶（講師 T4 實跑）</div>

</div>
<div>

<div class="placeholder" style="height:200px;padding:16px 24px">擴散模型的損失：一條線，一路往下、慢慢變平<small>講師 T4 實跑後替換（lab11 <code>loss.png</code>）</small></div>

</div>
</div>

<div class="grid grid-cols-2 gap-6 mt-2" style="font-size:17px">
<div class="node"><strong>GAN</strong><small>兩個網路互相比賽；loss 下降 ≠ 圖變好</small></div>
<div class="node node--primary"><strong>擴散</strong><small>一個網路、一個 MSE；loss 下降 ≈ 猜雜訊猜得更準</small></div>
</div>

<div class="takeaway mt-2">沒有對手，就沒有「誰贏誰輸」的震盪：損失曲線又能拿來判斷訓練了。</div>

<!--
○ 選修（3 分）：左圖是 D3-1 的 lab09 實跑截圖。提醒：擴散模型的 loss 很早就變平，但樣本還在進步，所以最後一樣要看樣本網格。
-->

---

<div class="eyebrow">04 · Adapt · 現成的工具</div>

# diffusers 的排程器：同一個網路，換一種走法

```python
from diffusers import DDIMScheduler
sched = DDIMScheduler(num_train_timesteps=1000, beta_start=1e-4, beta_end=0.02, beta_schedule="linear")
sched.set_timesteps(50)                       # 只走 50 步
for t in sched.timesteps:                     # 980, 960, …, 0
    x = sched.step(model(x, t), t, x).prev_sample
```

<div class="grid grid-cols-2 gap-6 mt-3" style="font-size:18px">
<div class="node"><strong>DDPMScheduler</strong><small>就是第 15 頁那個迴圈：1000 步、每步加回雜訊</small></div>
<div class="node node--primary"><strong>DDIMScheduler</strong><small>不加回雜訊，可以一次跳好幾步；<strong>網路不用重新訓練</strong></small></div>
</div>

<div class="takeaway mt-3">排程器（scheduler）只管「怎麼走回來」；學到的網路不變，所以可以直接換。</div>

<div class="src">Song et al., DDIM, ICLR 2021 §4.1、§5（S2）；diffusers <code>DDIMScheduler</code>（S6）</div>

<!--
○ 選修（3 分）：scheduler（排程器）。DDIM 論文寫：同一個訓練好的模型，不需要重新訓練（S2 §4.1）。實際快幾倍、圖差多少：Lab 的 F 部分自己量。D3-4 會用 DDIM 縮短檢測時間。
-->

---

<div class="eyebrow">附錄 · 備用</div>

# 另外兩種看法：分數匹配、ELBO（只認名字）

<div style="font-size:19px" class="mt-4">

- **分數匹配**（score matching）：猜雜訊的方向，等於猜「往資料比較多的方向走」
- **ELBO**（D2-3 學過的證據下界）：DDPM 的 MSE 損失，是 ELBO 拿掉權重後的簡化版
- 兩條路推到最後，訓練程式都長得像今天這幾行

</div>

<div class="takeaway mt-4">看到 score-based model、variational bound，知道說的是同一種模型。</div>

<div class="src">Ho et al., 2020 §3.4（L_simple 是加權版的變分下界）（S1）</div>

<!--
△ 備用（2 分）：學員問「為什麼猜雜訊就能生成」時再講。推導不在本課範圍（CLAUDE.md：數學只在需要時講，推導放附錄）。
-->

---

<div class="eyebrow">05 · Lab L3-3</div>

# Lab 1／7：我們要生成什麼？

<div class="grid grid-cols-2 gap-6 mt-2" style="font-size:19px">
<div>

**打開筆記本**：<code>lab11-ddpm.ipynb</code>（在 <code>materials/</code>）→ Open in Colab<br>
執行階段：**T4 GPU**；資料：Fashion-MNIST（自動下載）

1. 64 張樣本，會比 DCGAN 的更多樣嗎？
2. 1000 步要幾秒？少走幾步會怎樣？
3. 生成的圖，是新的，還是背下來的？

</div>
<div>

<div class="placeholder" style="height:250px;padding:16px 24px">目標：64 張樣本、兩兩距離、步數 vs 秒數表、最近鄰對照<small>講師 T4 實跑後替換（含 VRAM 峰值與訓練時間）</small></div>

</div>
</div>

<div class="takeaway mt-3">交給行銷部：一張「DCGAN vs 擴散」的多樣性與速度對照表，不是一句「擴散比較好」。</div>

<!--
★ Lab 開始（3 分）：先執行第 1 格和 A 部分（下載 DDPM 權重）。訓練時間待 T4 實測。沒有 GPU → EPOCHS＝1、TRAIN_SUBSET＝5000；斷線 → USE_CKPT＝True 下載講師的檢查點。
-->

---

<div class="eyebrow">05 · Lab L3-3</div>

# Lab 2／7：筆記本拆成哪幾塊？

<div class="steps mt-2" style="font-size:17px">
  <div><span class="num">1</span><strong>A、B</strong>：現成 DDPM；<code>q_sample</code> 一行加噪、<code>betas</code>／<code>alpha_bar</code> 排程</div>
  <div><span class="num">2</span><strong>C</strong>：<code>time_embedding</code>、<code>Block</code>（D2-2 的 block ＋ 時間）、<code>TinyUNet</code></div>
  <div><span class="num">3</span><strong>D</strong>：訓練迴圈（TODO ①：出題、猜雜訊、MSE）</div>
  <div><span class="num">4</span><strong>E</strong>：<code>sample</code>（TODO ②：扣掉雜訊）；<code>mean_pairwise</code> 和 DCGAN 比</div>
  <div><span class="num">5</span><strong>F、G</strong>：<code>sample_ddim</code> 步數 vs 秒數；<code>nearest</code> 找最像的訓練圖</div>
</div>

<div class="takeaway mt-3">兩個 TODO 都只有幾行：一個是「出題＋猜雜訊」，一個是「扣掉雜訊」。</div>

<!--
★ 拆塊（3 分）：名字和筆記本一模一樣，學員卡住時可以用名字搜尋。
-->

---

<div class="eyebrow">05 · Lab L3-3</div>

# Lab 3／7：Specify

<div style="font-size:18px" class="mt-2">

<strong>【目標】</strong>訓練一個小 DDPM，畫出 64 張 Fashion-MNIST 風格的圖，和 DCGAN 比多樣性與速度<br>
<strong>【輸入與輸出】</strong>x_t <code>&#91;B,1,32,32&#93;</code>（−1～1）＋ t <code>&#91;B&#93;</code> → TinyUNet → ε̂ <code>&#91;B,1,32,32&#93;</code><br>
<strong>【限制】</strong>Colab T4；32 × 32；不改模型大小、排程和 epochs；預測的是雜訊<br>
<span class="muted" style="font-size:16px">為什麼：大家設定一樣，才能和隔壁、和 DCGAN 比</span><br>
<strong>【驗收】</strong>① <code>out</code> 的 shape 和 x_t 一樣　② loss 一路往下，沒有 GAN 那種劇烈震盪　③ 64 張樣本看得出衣物，而且種類很多　④ 兩兩距離 ≥ DCGAN 的 22.08　⑤ 記下 1000 步和 50 步的秒數

</div>

<!--
★ Specify（3 分）：驗收第 ④ 點用的是 D3-1 講師實跑的數字。驗收是課前寫好的門檻，不是預測結果；T4 實跑後以實際數字為準。
-->

---

<div class="eyebrow">05 · Lab L3-3</div>

# Lab 4／7：Generate → Execute

<PromptBox>
這是 PyTorch 筆記本，請只填兩個 # TODO：<br>
① 訓練迴圈：t ＝ 每張圖隨機一個 0～T−1 的整數；eps ＝ randn_like(x0)；x_t ＝ sab&#91;t&#93;·x0 ＋ s1mab&#91;t&#93;·eps（view 成 &#91;B,1,1,1&#93;）；loss ＝ MSE(model(x_t, t), eps)<br>
② sample：mean ＝ (x − betas&#91;t&#93; / sqrt_1mab&#91;t&#93; · eps_hat) / √alphas&#91;t&#93;；t ＞ 0 時 x ＝ mean ＋ √betas&#91;t&#93; · 新的雜訊，否則 x ＝ mean<br>
不要改模型、排程和 epochs。每一格說明每一行在做什麼。
</PromptBox>

<div class="steps mt-2" style="font-size:17px">
  <div><span class="num">1</span>訓練時間待 T4 實測；等待時看每個 epoch 印出的 loss</div>
  <div><span class="num">2</span>沒有 Agent 額度：照「訓練」和「取樣」兩頁的程式填；卡住開 <code>-solution.ipynb</code></div>
  <div><span class="num">3</span>預期輸出：<code>out＝預測的雜訊 (8, 1, 32, 32)</code>、<code>參數 1,981,921</code></div>
</div>

<div class="node node--warm mt-2" style="font-size:16px"><strong>常見錯誤</strong><small>loss 寫成 <code>F.mse_loss(model(x_t, t), x0)</code>：網路改學「猜原圖」，取樣公式就對不上，畫出來是一片灰</small></div>

<!--
★ 執行（約 18 分，訓練時先做 Lab 5／7 的預測）：最常見錯誤就是第 10 頁的誤解。第二常見：model(x0, t)（把乾淨圖丟進去），loss 會很快變得很小，但取樣全是雜訊。
-->

---

<div class="eyebrow">05 · Lab L3-3</div>

# Lab 5／7：看樣本、對照預測

<div class="grid grid-cols-[1.3fr_1fr] gap-6 mt-2">
<div>

<div class="placeholder" style="height:250px;padding:16px 24px">我們的 DDPM：64 張樣本（1000 步，seed 0）<small>講師 T4 實跑後替換（lab11 <code>samples.png</code>）</small></div>

</div>
<div style="font-size:18px">

1. 64 張裡，數得出幾種衣物？有沒有兩張幾乎一樣？
2. 和 D3-1 的 DCGAN 網格比：哪一個比較清楚？
3. 兩兩距離是多少？比 22.08 大還是小？

</div>
</div>

<div class="takeaway mt-3">多樣性用「網格＋數字」一起說，和 D3-1 判斷崩塌的方法一樣。</div>

<!--
★ 對照（6 分）：學員的數字會因為 GPU 和隨機性略有不同。第 2 題常見答案：擴散的圖比較「乾淨」但有時邊緣有雜點，小模型、短訓練的正常現象。
-->

---

<div class="eyebrow">05 · Lab L3-3</div>

# Lab 6／7：Audit → Iterate

<table style="font-size:15px">
<thead><tr><th style="width:28%">稽核問題</th><th>具體動作</th><th style="width:32%">應該是</th></tr></thead>
<tbody>
<tr><td>網路猜的是雜訊嗎？</td><td>看 loss 那一行</td><td><code>mse_loss(model(x_t, t), eps)</code></td></tr>
<tr><td>丟進網路的是髒圖嗎？</td><td>看 <code>model(...)</code> 的第一個參數</td><td><code>x_t</code>，不是 <code>x0</code></td></tr>
<tr><td>t 是每張圖各自隨機嗎？</td><td>看 <code>randint</code> 的 shape</td><td><code>(len(x0),)</code>，不是一個數</td></tr>
<tr><td>取樣最後一步有沒有加雜訊？</td><td>看 <code>if t &gt; 0</code></td><td>t＝0 時不加</td></tr>
<tr><td>樣本範圍對嗎？</td><td>畫圖的 <code>vmin</code>、<code>vmax</code></td><td>−1～1（和訓練資料一樣）</td></tr>
<tr><td>DDIM 少走幾步，代價是什麼？</td><td>F 部分的表和圖</td><td>講師實跑後填入</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">一次只改一件事：例如把 EPOCHS 從 20 改成 5，看樣本和兩兩距離怎麼變。</div>

<!--
★ 稽核（6 分）：前三列對應三個最常見的錯誤。第 5 列：如果把 −1～1 的圖當 0～1 畫，整張會變得很亮或很暗。
-->

---

<div class="eyebrow">05 · Lab L3-3 · Ship</div>

# Lab 7／7：交給行銷部的對照表

<table class="mt-2" style="font-size:17px">
<thead><tr><th style="width:30%">做法</th><th>兩兩距離（真圖 22.90）</th><th>64 張的秒數（T4）</th><th>網路跑幾次</th></tr></thead>
<tbody>
<tr><td>D3-1 DCGAN（20 epochs）</td><td>22.08</td><td>沒有量（一次前向）</td><td>1</td></tr>
<tr><td>DDPM 1000 步</td><td>實跑後填入</td><td>實跑後填入</td><td>1000</td></tr>
<tr><td>DDIM 50 步</td><td>實跑後填入</td><td>實跑後填入</td><td>50</td></tr>
<tr><td>DDIM 10 步</td><td>實跑後填入</td><td>實跑後填入</td><td>10</td></tr>
</tbody>
</table>

<div class="muted mt-2" style="font-size:16px">兩兩距離只量「彼此差多少」，不量「像不像衣服」：一片亂雜訊的距離也很大。所以一定要配網格看。</div>

<div class="takeaway mt-2">建議要附理由：「型錄縮圖改用 ＿＿：多樣性 ＿＿，每 64 張 ＿＿ 秒，用 DDIM ＿＿ 步時圖 ＿＿」。</div>

<!--
★ Ship（4 分）：DCGAN 的數字來自 D3-1 的講師 T4 實跑（lab09，research/lab-runs.md）。提醒：兩兩距離太大也可能是壞事（樣本是雜訊）。
-->

---

<div class="eyebrow">06 · Measure · 生成三難</div>

# 生成三難第二列：擴散模型

<div class="grid grid-cols-[1fr_1.2fr] gap-6 mt-1 items-center">
<div>

<svg viewBox="0 0 320 260" style="width:100%;max-height:260px" aria-label="三角形，三個角是品質、多樣性、速度；GAN 在品質和速度那一邊，擴散在品質和多樣性那一邊">
  <polygon points="160,25 30,230 290,230" fill="var(--surface)" stroke="var(--muted-text)" stroke-width="2"/>
  <text x="160" y="18" text-anchor="middle" style="font-size:18px" fill="var(--text)">品質</text>
  <text x="22" y="252" style="font-size:18px" fill="var(--text)">多樣性</text>
  <text x="262" y="252" style="font-size:18px" fill="var(--text)">速度</text>
  <circle cx="210" cy="120" r="12" fill="var(--warm-accent)"/>
  <text x="228" y="126" style="font-size:18px" fill="var(--warm-accent)">GAN</text>
  <circle cx="110" cy="120" r="12" fill="var(--primary)"/>
  <text x="36" y="110" style="font-size:18px" fill="var(--primary)">擴散</text>
</svg>

</div>
<div style="font-size:17px">

| | GAN（D3-1） | 擴散（今天） |
|---|---|---|
| 品質 | ✓ | ✓ |
| 多樣性 | 沒保證（要量） | ✓ 你的距離：＿＿ |
| 速度 | ✓ 1 次前向 | ✗ 1000 次；你的秒數：＿＿ |

<div class="muted mt-2" style="font-size:16px">DDIM 用較少步數換速度；D4-2 的潛在擴散再把圖縮小來省時間。</div>

</div>
</div>

<div class="takeaway mt-2">擴散用「慢」換來「多樣而且好訓練」：這一列和 D3-1 那一列，就是學習評量「Diffusion vs GAN」的證據。</div>

<div class="src">Xiao et al., 2022：GAN 快但 mode coverage 差、擴散要數千次網路運算（S3）</div>

<!--
★ 三難（3 分）：請學員把自己的數字填進三難表格第二列（Lab 7／7 的表）。這張表第四天變成學習評量的備忘錄。
-->

---

<div class="eyebrow">06 · Measure & Risk（風險）</div>

# 風險：生成的圖，是不是背下來的訓練圖？

<div class="grid grid-cols-[1.3fr_1fr] gap-6 mt-2">
<div>

<div class="placeholder" style="height:240px;padding:16px 24px">上排：8 張生成圖；下排：每張在 60,000 張訓練圖裡最像的一張（標距離）<small>講師 T4 實跑後替換（lab11 <code>nearest.png</code>）</small></div>

</div>
<div style="font-size:18px">

- **最近鄰檢查**：每張生成圖，找訓練集裡距離最小的一張
- 參考值：沒參加訓練的測試圖，最近鄰距離是多少
- 生成圖的距離明顯更小 → 可能是背下來的
- 型錄、廣告用圖：背下來的圖可能是別人的作品

</div>
</div>

<div class="takeaway mt-3">「新」要自己驗證：上架前，生成圖都要做一次最近鄰檢查。</div>

<div class="src">D2-3 第 24 頁（背下訓練資料）；D4-3 的 LoRA 會再用同一個方法</div>

<!--
★ 風險（4 分）：nearest neighbour（最近鄰）。我們的小模型、Fashion-MNIST 背下來的機會不大，但大模型會（D2-3 已提過）。著作權的細節 D6 再談；今天只要會做檢查。
-->

---

<div class="eyebrow">總整理</div>

# 今天學到的概念鏈

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-4">
  <span class="chip">往前加噪（固定公式）</span><span class="arrow">→</span>
  <span class="chip">一行跳到第 t 步</span><span class="arrow">→</span>
  <span class="chip">網路猜雜訊（MSE）</span><span class="arrow">→</span>
  <span class="chip">U-Net ＋ 時間嵌入</span><span class="arrow">→</span>
  <span class="chip">1000 步取樣</span><span class="arrow">→</span>
  <span class="chip">DDIM 少走幾步</span>
</div>

<div class="takeaway mt-6">擴散模型＝學會「猜雜訊」的 U-Net，加上一個一步一步扣掉雜訊的迴圈。</div>

<div class="muted mt-3" style="font-size:17px">和學習評量的關係：「解釋 Diffusion vs GAN」用今天和 D3-1 的三難表格；D4-1 會在這個迴圈裡加上「條件」（要畫哪一類）。</div>

<!--
★ 總整理（2 分）：請學員用一句話回答「擴散模型的網路在猜什麼？」（雜訊）。
-->

---

<div class="eyebrow">隨堂檢核</div>

# 選擇題（iPAS 題型）

<div class="mcq" style="font-size:17px">

1. DDPM 訓練時，網路的輸出要和什麼比 MSE？（　）<br><span class="opts"><span class="nw">A. 原圖 x₀</span>　<span class="nw">B. 加進去的雜訊 ε</span>　<span class="nw">C. 鑑別器的分數</span>　<span class="nw">D. 類別標籤</span></span>
2. x_t ＝ √ᾱ_t·x₀ ＋ √(1−ᾱ_t)·ε 中，t 越大？（　）<br><span class="opts"><span class="nw">A. 原圖的比例越大</span>　<span class="nw">B. 兩者不變</span>　<span class="nw">C. 雜訊的比例越大</span>　<span class="nw">D. 圖越來越清楚</span></span>
3. 去噪網路為什麼需要時間嵌入？（　）<br><span class="opts"><span class="nw">A. 讓網路知道現在的圖有多髒</span>　<span class="nw">B. 讓訓練更快</span>　<span class="nw">C. 讓輸出變成彩色</span>　<span class="nw">D. 取代跳接</span></span>
4. 和 GAN 比，擴散模型取樣最主要的缺點？（　）<br><span class="opts"><span class="nw">A. 多樣性差</span>　<span class="nw">B. 要重複執行網路很多次，比較慢</span>　<span class="nw">C. 一定要成對資料</span>　<span class="nw">D. 損失震盪</span></span>

</div>

<!--
★ 檢核（3 分）。答案：1 B（A 是第 10 頁的常見誤解）、2 C、3 A、4 B（A、D 是 GAN 的問題）。
-->

---
hostOnly: true
---

<div class="eyebrow">下一步</div>

# 下一堂 D3-4：AE 熱圖太模糊？用擴散模型「修好」板子

<div style="font-size:19px" class="mt-4">

- 品保部回來了：D2-1 的 AE 重建太模糊，細紋路一直被判成瑕疵
- 不從純雜訊開始：把板子**加噪到一半**再擦回來 → 一張「正常版」的板子
- 和 AE 比 AUROC、過殺、每張幾毫秒；用今天的 DDIM 加速

</div>

<!--
★ 下一步（1 分）：預告。今天的「加噪、去噪」原封不動用在檢測上，只是起點不是純雜訊。
-->
