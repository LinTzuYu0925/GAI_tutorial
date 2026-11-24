---
theme: default
title: 舊照片放大：偽造者與鑑定師
info: |
  生成式AI原理 · D3-1
  GAN：生成器偽造、鑑別器鑑定，兩個一起進步。用 Real-ESRGAN 把舊型錄照片放大 4 倍，自己訓練 DCGAN，認出不穩定與 mode collapse；對抗損失今天仍在很多產品裡。
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
exportFilename: 09-gan-upscaling
layout: center
class: cover
---

<div class="eyebrow">生成式AI原理 · D3-1</div>

# 舊照片放大：偽造者與鑑定師

<p class="subtitle">GAN：一個網路偽造、一個網路鑑定，兩個一起變強</p>

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-8">
  <span class="chip">放大只會糊</span><span class="arrow">→</span>
  <span class="chip">Real-ESRGAN</span><span class="arrow">→</span>
  <span class="chip">G 偽造、D 鑑定</span><span class="arrow">→</span>
  <span class="chip">輪流訓練</span><span class="arrow">→</span>
  <span class="chip">mode collapse</span><span class="arrow">→</span>
  <span class="chip">生成三難</span>
</div>

<!--
★ 開場（2 分）：第三天的主題是「GAN 還是擴散？」。今天上午學 GAN；今天下午（D3-3）學擴散；第四天寫比較備忘錄（學習評量）。
第二天作業（門檻建議）的回顧放在 D3-2 開場前，不佔本堂時間。
-->

---

<div class="eyebrow">00 · Frame（定義問題）</div>

# 電商部：舊型錄照片太小，網站改版用不了

<div class="ticket mt-2">
  <div class="ticket-head">【需求單 #D3-1】部門：電商部<span>公司：曜嶼電子 <span class="fiction" style="color:#fff;border-color:#fff">虛構</span></span></div>
  <dl>
    <dt>問題</dt><dd>數千張舊型錄照片解析度太低，網站改版用不了</dd>
    <dt>現況痛點</dt><dd>重拍一張要上千元，數千張不可能</dd>
    <dt>成功指標（KPI）</dt><dd>4 倍放大後細節清楚、沒有誤導顧客的假細節；每張處理時間</dd>
    <dt>可用資料</dt><dd>舊型錄風格的低解析度照片（CC0）；Fashion-MNIST</dd>
    <dt>限制與法規</dt><dd>Colab T4；產品照不能誇大產品（消費者保護）</dd>
    <dt>為何現有工具不夠</dt><dd>一般放大（bicubic 內插）只會變糊；D2-3 的 VAE 樣本也偏糊</dd>
  </dl>
</div>

<!--
★ 需求單（3 分）：「假細節」是今天的關鍵風險：放大模型會「畫」出原圖沒有的紋理。對商品照來說，畫錯可能就是誇大不實。
-->

---

<div class="eyebrow">學習目標</div>

# 今天結束時，你能夠……

1. **說出** GAN 裡生成器（G）與鑑別器（D）的角色
2. **讀懂**對抗目標的一行式，以及 G 為什麼改用「假圖標成真」的寫法
3. **寫出**兩個優化器輪流更新的訓練迴圈，並**預測** G 每一層的 shape
4. **判斷**訓練好壞：看固定 z 的網格、量 mode collapse（一直畫同樣的東西），不看 loss
5. **使用** Real-ESRGAN 放大舊照片，指出「假細節」風險；說出對抗損失今天還用在哪裡

<!--
★ 目標（1 分）。不教：WGAN 的數學（△ 點名）、StyleGAN 架構、條件式 GAN 的實作（D4-1 用擴散做）。
-->

---

<div class="eyebrow">00 · Frame</div>

# 一般放大只會變糊

<div class="grid grid-cols-[1fr_1fr_1fr] gap-5 mt-2 items-start">
<div>
  <img class="photo" src="/headphones-lowres.jpg" alt="一副黑色頭戴式耳機的小照片，233 乘 263 像素" style="height:250px;margin:0 auto">
  <div class="shot-cap">舊照片：只有 233 × 263</div>
</div>
<div>
  <img class="photo" src="/headphones-bicubic-crop.png" alt="把左邊耳罩放大四倍：邊緣模糊、有方塊感" style="height:250px;width:100%">
  <div class="shot-cap">一般放大 4 倍（bicubic），左耳罩局部</div>
</div>
<div style="font-size:18px">

- bicubic（雙三次內插）：用周圍 16 個像素「平均」出新像素
- 原本沒有的細節，平均不出來 → **糊**
- 我們要的是「看起來合理的銳利細節」

</div>
</div>

<div class="takeaway mt-3">放大不是「算」出細節，是「畫」出細節：這需要一個學過「真實照片長什麼樣」的生成模型。</div>

<div class="src">照片：Sprinno，CC0，Wikimedia Commons（S1）；bicubic 用 PIL 產生（固定公式，不是模型輸出）</div>

<!--
★ Frame（3 分）：bicubic（雙三次內插）讀作「用附近的像素加權平均」。問學員：「如果只能平均，耳罩的皮革紋路從哪裡來？」→ 從沒有地方來，所以要「畫」。
-->

---

<div class="eyebrow">01 · Try（先用現成的）</div>

# Real-ESRGAN：幾秒鐘放大 4 倍

<div class="grid grid-cols-3 gap-4 mt-2">
<div><img class="photo" src="/headphones-bicubic-crop.png" alt="一般放大的左耳罩局部" style="height:200px;width:100%"><div class="shot-cap">一般放大（bicubic）</div></div>
<div><img class="photo" src="/headphones-esrgan-crop.png" alt="Real-ESRGAN 放大的左耳罩局部：邊緣銳利、表面變平滑，還多了幾個小亮點" style="height:200px;width:100%"><div class="shot-cap">Real-ESRGAN（同一塊）</div></div>
<div style="border:1px solid var(--border);border-radius:8px;padding:12px;height:200px;display:flex;flex-direction:column;justify-content:center;font-size:20px;line-height:1.7"><div><strong>Colab T4</strong></div><div>233×263 → 932×1052</div><div>每張 <strong>0.59 秒</strong></div><div style="font-size:16px" class="muted">第一次含暖機 2.46 秒</div><div>VRAM 峰值 <strong>0.62 GB</strong></div></div>
</div>

<div class="takeaway mt-4">邊緣變銳利了；但耳罩的凹凸紋被抹平，還多了幾個原圖沒有的小亮點。哪一張比較「真」？</div>

<div class="src">Real-ESRGAN x4plus（Wang et al., 2021；BSD-3-Clause，S2）；lab09 Part A；兩張局部圖來自講師本機 CPU 實跑，秒數與 VRAM 為 Colab T4 實跑（research/lab-runs.md）</div>

<!--
★ 示範（5 分）：用 lab09 解答筆記本 Part A 現場跑一次。請學員指出右圖的小亮點：原圖沒有，是模型「畫」的；凹凸紋反而被抹平。這就是後面「假細節」風險頁的伏筆。
-->

---

<div class="eyebrow">02 · Open（打開黑盒子）</div>

# 偽造者與鑑定師

<div class="grid items-center mt-3" style="font-size:18px;grid-template-columns:15% 5% 25% 5% 25% 5% 15%;row-gap:4px">
  <div class="node">隨機數字 z</div><span class="arrow text-center">→</span>
  <div class="node node--warm"><strong>G 生成器</strong><small class="nw">偽造者：畫一張假圖</small></div><span class="arrow text-center">→</span>
  <div class="node node--primary"><strong>D 鑑別器</strong><small class="nw">鑑定師：真的還是假的？</small></div><span class="arrow text-center">→</span>
  <div class="node">分數<small>越大越像真的</small></div>
  <div style="grid-column:5" class="arrow text-center">↑</div>
  <div style="grid-column:5" class="node">真實照片<small>也交給 D 看</small></div>
</div>

<div class="grid grid-cols-2 gap-6 mt-4" style="font-size:18px">
<div class="node node--primary"><strong>D 想要</strong><small>真圖給高分、假圖給低分</small></div>
<div class="node node--warm"><strong>G 想要</strong><small>讓 D 把假圖也打高分</small></div>
</div>

<div class="muted mt-2" style="font-size:17px">GAN（生成對抗網路）。注意：G 從頭到尾<strong>沒看過真圖</strong>，只能從 D 的分數學「怎樣比較像真的」。</div>

<div class="takeaway mt-2">兩個網路互相較勁：鑑定師越會挑毛病，偽造者就被逼得越像真的。</div>

<div class="src">回顧：DL pp.82–84（GAN 概念）；Goodfellow et al., 2014（S3，待逐字核對）</div>

<!--
★ 主角（5 分）：GAN（Generative Adversarial Network，生成對抗網路）。G＝generator（生成器），D＝discriminator（鑑別器）。DL 課看過概念（DL pp.82–84），今天寫程式。
注意：G 從頭到尾沒看過真圖！它只能從 D 的分數學到「怎樣比較像真的」。
-->

---

<div class="eyebrow">02 · Open · D 就是分類器</div>

# D 是你早就會的東西：二元分類 CNN

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-2">
<div>

```python
D = nn.Sequential(
    nn.Conv2d(1, 64, 4, 2, 1),   nn.LeakyReLU(0.2),  # 28 → 14；負的一邊乘 0.2
    nn.Conv2d(64, 128, 4, 2, 1), nn.BatchNorm2d(128),
    nn.LeakyReLU(0.2),                               # 14 → 7
    nn.Flatten(), nn.Linear(128 * 7 * 7, 1))         # [B,1]；筆記本再 .view(-1) → [B]
```

</div>
<div style="font-size:18px">

- 輸入一張圖，輸出一個 logit（還沒變成機率的分數）
- 損失：<code>BCEWithLogitsLoss</code>，真＝1、假＝0
- 和 D1-3 的 CIFAR-10 分類器一樣，只是「類別」換成真／假

</div>
</div>

<div class="takeaway mt-3">GAN 一半的程式你已經會了；新的只有「G」和「輪流訓練」。</div>

<div class="src">回顧：DL pp.38–55（CNN 分類）；D1-3 的訓練迴圈</div>

<!--
★ D（3 分）：LeakyReLU：負的那一邊不是 0，而是乘 0.2，讓梯度不會完全消失（DCGAN 的建議）。
-->

---

<div class="eyebrow">02 · Open · 目標</div>

# 一行目標：D 想讓它變大，G 想讓它變小

<div style="font-size:23px" class="mt-3 text-center">

$$\min_G \max_D \; \mathbb{E}_{x}\big[\log D(x)\big] + \mathbb{E}_{z}\big[\log\big(1 - D(G(z))\big)\big]$$

</div>

<table class="mt-3" style="font-size:17px">
<thead><tr><th style="width:26%">符號</th><th>讀作</th></tr></thead>
<tbody>
<tr><td>𝔼_x、𝔼_z</td><td>平均：對所有真圖 x、所有隨機數字 z 取平均（程式裡就是一個 batch 的平均）</td></tr>
<tr><td>D(x)</td><td>D 認為真圖 x「是真的」的機率（第 7 頁的 logit 經過 sigmoid）</td></tr>
<tr><td>G(z)</td><td>G 用隨機數字 z 畫出的假圖</td></tr>
<tr><td>log D(x) ＋ log(1 − D(G(z)))</td><td>D 判對的程度：真圖說真、假圖說假，就變大</td></tr>
<tr><td>max_D、min_G</td><td>D 要把它推高；G 要把它壓低（讓 D 判錯）</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">同一個分數，兩個人搶方向：這就是「對抗」（adversarial）。</div>

<!--
★ 目標（5 分）：這是今天唯一的公式。𝔼 讀作「平均」：真圖那一項對所有真圖平均，假圖那一項對所有 z 平均。程式裡就是 BCE 的兩項。
-->

---

<div class="eyebrow">02 · Open · 一個實際的修正</div>

# G 的損失改寫：「假圖標成真」

<div class="grid grid-cols-2 gap-6 mt-3" style="font-size:18px">
<div class="node node--warm"><strong>問題</strong><small>訓練剛開始，G 畫得很爛，D 一眼看穿：D(G(z)) ≈ 0。這時 log(1 − D(G(z))) 幾乎是平的 → G 收到的梯度幾乎是 0，學不動</small></div>
<div class="node node--primary"><strong>修正（non-saturating，不飽和）</strong><small>G 改成「讓 D 把假圖判成真」：把假圖標成 1 去算 BCE。D 越看穿，這個損失越大、梯度越大</small></div>
</div>

```python
loss_g = bce(d(fake), ones)      # 假圖，但標成「真」(1)
```

<div class="takeaway mt-3">目標的方向一樣（讓 D 判錯），只是換一種寫法，讓 G 一開始就學得動。</div>

<div class="src">Goodfellow et al., 2014 §3（S3，待逐字核對）</div>

<!--
★ 改寫（5 分）：non-saturating（不飽和）讀作「梯度不會被壓到 0」。這是幾乎所有 GAN 程式碼的預設寫法，lab 也這樣寫。
-->

---

<div class="eyebrow">02 · Open · DCGAN</div>

# DCGAN 的架構規則

<div class="flex items-center justify-center gap-2 mt-4" style="font-size:17px">
  <div class="node" style="width:14%">z<small class="nw">&#91;B,100&#93;</small></div><span class="arrow">→</span>
  <div class="node node--warm" style="width:18%"><strong>Linear</strong><small>攤平的小特徵圖</small></div><span class="arrow">→</span>
  <div class="node node--warm" style="width:18%"><strong>轉置卷積</strong><small style="font-size:14px">ConvTranspose2d<br>高寬 ×2</small></div><span class="arrow">→</span>
  <div class="node node--warm" style="width:18%"><strong>轉置卷積</strong><small style="font-size:14px">ConvTranspose2d<br>高寬 ×2，tanh</small></div><span class="arrow">→</span>
  <div class="node" style="width:14%">假圖<small>28 × 28</small></div>
</div>

<table class="mt-5" style="font-size:17px">
<thead><tr><th style="width:34%">規則</th><th>為什麼</th></tr></thead>
<tbody>
<tr><td>用 stride 2 的卷積取代池化</td><td>讓網路自己學怎麼縮小／放大（D2-1 的 down／up）</td></tr>
<tr><td>BatchNorm</td><td>讓兩個網路的訓練比較穩</td></tr>
<tr><td>G 用 ReLU、最後一層 tanh；D 用 LeakyReLU</td><td>tanh 輸出 −1～1，所以真圖也要正規化到 −1～1</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">G 就是一個「從小放大」的解碼器：每一層高寬加倍，最後用 tanh 輸出 −1～1。</div>

<div class="src">Radford et al., DCGAN, 2015（S4，待逐字核對）</div>

<!--
★ DCGAN（5 分）：DCGAN（Deep Convolutional GAN）。轉置卷積（transposed convolution）：和卷積相反，把高寬放大；stride 2 讓高寬加倍。最常見的錯誤：真圖還在 0～1、G 輸出 −1～1，D 只要看範圍就分得出真假。
-->

---

<div class="eyebrow">02 · Open · 練習</div>

# 練習：G 每一層的 shape

<div class="muted" style="font-size:17px">不用 AI、先不執行。<code>ConvTranspose2d(…, 4, 2, 1)</code> 讓高寬加倍。B ＝ 16。照著做：第一列已填好。</div>

<table class="fill tight vlines mt-1">
<thead><tr><th style="width:44%">程式</th><th>輸出 shape</th></tr></thead>
<tbody>
<tr><td>例（D 的第一層）：<code>Conv2d(1, 64, 4, 2, 1)</code> 吃 &#91;16, 1, 28, 28&#93;</td><td>&#91;16, 64, 14, 14&#93;（stride 2：高寬減半）</td></tr>
<tr><td><code>z = torch.randn(16, 100)</code></td><td>&#91;16, 100&#93;</td></tr>
<tr><td><code>fc(z)</code>：Linear(100, 128·7·7)</td><td class="blank"><FillIn id="g.fc" hint="例：&#91;16, 某個乘積&#93;……" /></td></tr>
<tr><td><code>.view(-1, 128, 7, 7)</code></td><td class="blank"><FillIn id="g.view" /></td></tr>
<tr><td><code>ConvTranspose2d(128, 64, 4, 2, 1)</code></td><td class="blank"><FillIn id="g.ct1" /></td></tr>
<tr><td><code>ConvTranspose2d(64, 1, 4, 2, 1)</code> ＋ tanh</td><td class="blank"><FillIn id="g.ct2" /></td></tr>
<tr><td>D 吃下這張圖，輸出？</td><td class="blank"><FillIn id="g.d" /></td></tr>
</tbody>
</table>

<FillClear group="g" />

<!--
★ 無 AI 檢核點（5 分）：對答案：筆記本 Part B 第一格用 show=True 印出 shape。不收回。
-->

---
hostOnly: true
---

<div class="eyebrow">02 · Open · 練習解答</div>

# 練習解答：G 每一層的 shape

<table class="vlines" style="font-size:19px">
<thead><tr><th style="width:44%">程式</th><th>輸出 shape</th></tr></thead>
<tbody>
<tr><td><code>fc(z)</code></td><td>&#91;16, 6272&#93;（128 × 7 × 7）</td></tr>
<tr><td><code>.view(...)</code></td><td>&#91;16, 128, 7, 7&#93;</td></tr>
<tr><td>第一個 ConvTranspose</td><td>&#91;16, 64, 14, 14&#93;</td></tr>
<tr><td>第二個 ConvTranspose ＋ tanh</td><td>&#91;16, 1, 28, 28&#93;，值在 −1～1</td></tr>
<tr><td>D 的輸出</td><td>&#91;16&#93;：每張一個分數</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">G 和 D2-1 的解碼器幾乎一樣：從小小的瓶頸一路放大。差別在 G 的輸入是隨機數字，不是編碼器給的。</div>

<!--
★ 解答（2 分）：本機 CPU 煙霧測試印出 z (16,100) → fc 後 (16,128,7,7) → 輸出 (16,1,28,28)（research/lab-runs.md）。
-->

---

<div class="eyebrow">02 · Open · 訓練迴圈</div>

# 兩個優化器，輪流走一步

```python
fake = g(torch.randn(B, 100))
# ① D 這一步：真圖標 1、假圖標 0；假圖 detach，不更新 G
loss_d = bce(d(real), ones) + bce(d(fake.detach()), zeros)
opt_d.zero_grad(); loss_d.backward(); opt_d.step()
# ② G 這一步：假圖標成 1，想騙過 D
loss_g = bce(d(fake), ones)
opt_g.zero_grad(); loss_g.backward(); opt_g.step()
```

<div class="takeaway mt-3">還是 D1-3 的五行迴圈，只是做兩次：一次給 D、一次給 G。</div>

<!--
★ 迴圈（5 分）：fake.detach() 讀作「這一步把假圖當成固定的資料」，不然 D 的 backward 會一路傳進 G，把 G 也改掉。
-->

---

<div class="eyebrow">03 · Measure（量測驗收）· 不穩定</div>

# GAN 的 loss 不會告訴你品質

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-2">
<div>

<img class="photo" src="/lab09-run-loss.png" alt="DCGAN 訓練 20 個 epoch 的 D 與 G 的 loss：兩條線持續上下跳動，沒有穩定下降" style="width:100%;object-fit:contain"><div class="shot-cap">Colab T4 實跑：20 epoch、約 9,360 步（Fashion-MNIST）</div>

</div>
<div style="font-size:18px">

- 一般訓練：loss 往下 ＝ 越來越好
- GAN：D 和 G 在拔河，loss **上下跳**是正常的
- loss 沒告訴你圖好不好 → **要看圖**
- 所以每個 epoch 都用**同一批 z** 存一張網格

</div>
</div>

<div class="takeaway mt-3">判斷 GAN 好不好：看固定 z 的網格怎麼變，不是看 loss。</div>

<!--
★ 不穩定（5 分）：固定 z（fixed_z）讀作「每次都用同一組隨機數字」，這樣網格上同一格就是同一張圖的演變。
-->

---

<div class="eyebrow">03 · Measure · mode collapse</div>

# mode collapse（模式崩塌）：一直畫同樣的東西

<div class="grid grid-cols-[1.25fr_1fr] gap-5 mt-1">
<div>

<img class="photo" src="/collapse-reference.png" alt="上排：16 張隨機的 Fashion-MNIST 真圖，有上衣、鞋子、洋裝；下排：16 張全是短靴" style="width:100%">
<div class="shot-cap">上：隨機 32 張真圖；下：只有短靴的 32 張真圖（像崩塌後的 G）</div>

<table class="mt-2" style="font-size:16px">
<thead><tr><th>32 張圖</th><th>兩兩平均距離</th></tr></thead>
<tbody>
<tr><td>隨機真圖（參考）</td><td>22.90</td></tr>
<tr><td>只有短靴（模擬崩塌）</td><td>19.90</td></tr>
<tr><td>講師的 G，epoch 1 → 20（T4）</td><td>20.97 → 22.08</td></tr>
</tbody>
</table>

</div>
<div style="font-size:17px">

<div class="node node--warm"><strong>現象</strong><small>G 找到一種能騙過 D 的圖，就一直畫那一種：網格上很多格幾乎一樣，有些類別從沒出現</small></div>

<div class="node node--primary mt-3"><strong>為什麼會發生</strong><small>G 的目標只有「騙過 D」，沒有「每一種都要畫到」；D 抓到那一種之後，G 又跳到另一種——繞圈圈</small></div>

<div class="node mt-3"><strong>怎麼判斷</strong><small>距離明顯低於真圖的 22.90，而且網格裡少了好幾類 → 崩塌。講師這次沒有崩塌</small></div>

</div>
</div>

<div class="takeaway mt-2">GAN 的圖可以很清楚，但不一定多樣：要同時看網格和距離。</div>

<div class="src">Fashion-MNIST 真圖（S9）；「只有短靴」與隨機 32 張的距離由講師本機計算（同一個 <code>mean_pairwise</code>）；G 的數字來自 T4 實跑</div>

<!--
★ mode collapse（5 分）：mode（眾數、模式）指資料分布裡的「一群」；collapse（崩塌）指只剩下少數幾群。中文常說「模式崩塌」。
-->

---

<div class="eyebrow">04 · Adapt · GAN 不是過時技術</div>

# 對抗損失今天還在哪裡？

<table class="mt-2" style="font-size:18px">
<thead><tr><th style="width:30%">產品／模型</th><th>對抗損失做什麼</th><th style="width:16%">本課</th></tr></thead>
<tbody>
<tr><td>Real-ESRGAN</td><td>放大時畫出銳利的細節</td><td>今天</td></tr>
<tr><td>Stable Diffusion 的 VAE 解碼器</td><td>還原照片時不要糊</td><td>D2-3</td></tr>
<tr><td>EnCodec、HiFi-GAN</td><td>還原聲音時聽起來自然</td><td>D2-4、D6-1</td></tr>
<tr><td>SDXL-Turbo（ADD，對抗擴散蒸餾）</td><td>讓擴散模型 1–4 步就畫完</td><td>D4-4</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">很少有人再「只用 GAN」生成整張圖，但「加一個鑑定師讓輸出更銳利」到處都是。</div>

<div class="src">Wang et al. 2021（S2）；Rombach et al. 2022；Défossez et al. 2022；Kong et al. 2020；Sauer et al. 2023（S5，待確認）</div>

<!--
★ 不過時（3 分）：這頁回應一個常見說法「GAN 已經被擴散取代」。整張圖的生成確實多半交給擴散模型，但對抗損失是很多系統裡的一個零件。
-->

---

<div class="eyebrow">附錄 · 選修</div>

# 條件式 GAN 與感知損失

<div class="grid grid-cols-2 gap-6 mt-5" style="font-size:18px">
<div class="node"><strong>條件式 GAN</strong><small>G 和 D 都多吃一個標籤（例如「鞋子」）→ 想要哪一類就畫哪一類；D4-1 用擴散模型做同樣的事</small></div>
<div class="node"><strong>感知損失（perceptual loss）</strong><small>不比像素，比「預訓練 CNN 看到的特徵」；Real-ESRGAN 同時用 L1、感知、對抗三種損失（S2，待確認）</small></div>
</div>

<div class="takeaway mt-4">想控制「畫哪一類」就加條件；想讓細節更像人眼看到的，就加感知損失。</div>

<!--
○ 選修（2 分）：早做完的學員可以把 lab 的 G 改成條件式（多一個 nn.Embedding(10, 100) 加到 z 上）。
-->

---

<div class="eyebrow">附錄 · 備用</div>

# WGAN 與梯度懲罰（只認名字）

<div style="font-size:19px" class="mt-4">

- 把 D 的「真／假機率」換成「真假之間的距離」，訓練比較穩
- 需要限制 D 不能變化太快：梯度懲罰（gradient penalty）
- 看到 <code>WGAN-GP</code> 知道是這個

<div class="takeaway mt-4">訓練一直崩塌或發散時，換成 WGAN-GP 是常見的第一個嘗試。</div>

</div>

<div class="src">Arjovsky et al. 2017；Gulrajani et al. 2017（S6，待確認）</div>

<!--
△ 備用（2 分）：學員問「GAN 不穩有沒有解」時用。
-->

---

<div class="eyebrow">05 · Lab L3-1</div>

# Lab 1／7：我們要做出什麼？

<div class="grid grid-cols-2 gap-6 mt-2" style="font-size:19px">
<div>

**打開筆記本**：<code>lab09-dcgan-esrgan.ipynb</code>（在 <code>materials/</code>）→ Open in Colab<br>
執行階段：**T4 GPU**<br><span class="muted" style="font-size:16px">照片下載失敗（HTTP 429）：上傳 <code>materials/headphones.jpg</code></span>

1. Real-ESRGAN 放大一張舊照片要幾秒？細節是真的嗎？
2. 自己的 DCGAN：幾個 epoch 開始像衣物？
3. 有沒有 mode collapse？用什麼證據說？

</div>
<div>

<img class="photo" src="/lab09-run-dcgan-grids.png" alt="同一批 16 個 z 在 epoch 1、5、10、20 產生的衣物圖：從模糊團塊逐漸變成看得出鞋、上衣、褲子" style="width:100%;object-fit:contain"><div class="shot-cap">目標之一：固定 z 的網格（Colab T4 實跑）</div>

</div>
</div>

<div class="takeaway mt-3">交付給電商部：放大的對照圖＋每張秒數＋一句風險說明。</div>

<!--
★ Lab 開始（3 分）：Real-ESRGAN 權重 67 MB（講師本機下載的檔案大小）。照片下載失敗時，學員上傳 materials/headphones.jpg（和投影片同一張，CC0）。備案：沒有 GPU → EPOCHS＝2（本機 CPU 可跑完全部步驟，見 lab-runs）。
-->

---

<div class="eyebrow">05 · Lab L3-1</div>

# Lab 2／7：筆記本拆成哪幾塊？

<div class="mt-2" style="font-size:17px"><strong>Part A：用現成的 Real-ESRGAN</strong></div>
<div class="flex items-center gap-2 mt-1" style="font-size:17px">
  <div class="node"><code>low</code><small>233×263 照片</small></div><span class="arrow">→</span>
  <div class="node node--primary"><code>sr_model</code><small>spandrel 載入</small></div><span class="arrow">→</span>
  <div class="node"><code>big_esrgan</code><small>4 倍大</small></div><span class="arrow">↔</span>
  <div class="node"><code>big_bicubic</code><small>對照</small></div>
</div>

<div class="mt-4" style="font-size:17px"><strong>Part B、C：自己訓練 DCGAN</strong></div>
<div class="flex items-center gap-2 mt-1" style="font-size:17px">
  <div class="node node--warm"><code>G</code><small class="nw">&#91;B,100&#93;→&#91;B,1,28,28&#93;</small></div><span class="arrow">→</span>
  <div class="node node--primary"><code>D</code><small>一個分數</small></div><span class="arrow">→</span>
  <div class="node"><code>grids</code><small>固定 z 的網格</small></div><span class="arrow">→</span>
  <div class="node"><code>mean_pairwise</code><small>崩塌檢查</small></div>
</div>

<div class="takeaway mt-4">三個 TODO：Real-ESRGAN 推論一行、D 這一步、G 這一步。</div>

<!--
★ 拆塊（3 分）：spandrel 是一個「認得很多種放大模型權重檔」的載入器；用它就不需要原作者那套容易壞的 basicsr 套件。
-->

---

<div class="eyebrow">05 · Lab L3-1</div>

# Lab 3／7：Specify

<div style="font-size:18px" class="mt-2">

<strong>【目標】</strong>Real-ESRGAN 放大舊照片並計時；自己訓練 DCGAN，判斷有沒有 mode collapse<br>
<strong>【輸入與輸出】</strong>照片 <code>&#91;1,3,263,233&#93;</code> → <code>&#91;1,3,1052,932&#93;</code>；z <code>&#91;B,100&#93;</code> → 假圖 <code>&#91;B,1,28,28&#93;</code>（−1～1）<br>
<strong>【限制】</strong>真圖正規化到 −1～1；Adam lr 2e-4、betas (0.5, 0.999)；Colab T4<br>
<span class="muted" style="font-size:16px">為什麼：範圍不一致，D 看範圍就能分真假；betas 0.5 是 DCGAN 論文的建議（S4，待確認），比較不會震盪</span><br>
<strong>【驗收】</strong>① 放大後大小是 4 倍　② 有 bicubic 對照　③ 網格看得出衣物　④ 用網格＋距離回答「有沒有崩塌」

</div>

<!--
★ Specify（3 分）：驗收沒有寫「loss 下降」——因為 GAN 的 loss 不會單調下降（第 14 頁）。
-->

---

<div class="eyebrow">05 · Lab L3-1</div>

# Lab 4／7：Generate → Execute

<PromptBox>
這是 PyTorch 筆記本，請只填三個 # TODO：<br>
① Part A：y ＝ sr_model(x) 再 clamp 到 0–1（已在 no_grad 裡）<br>
② D 這一步：loss_d ＝ bce(d(real), 1) ＋ bce(d(fake.detach()), 0)，再 zero_grad、backward、step<br>
③ G 這一步：loss_g ＝ bce(d(fake), 1)，再 zero_grad、backward、step<br>
不要改網路和學習率。每一格說明每一行在做什麼。
</PromptBox>

<div class="steps mt-2" style="font-size:17px">
  <div><span class="num">1</span>T4 上 20 個 epoch 約 6 分鐘（實測 349 秒）；等待時看每個 epoch 印出的兩個 loss</div>
  <div><span class="num">2</span>沒有 Agent 額度：照「兩個優化器，輪流走一步」那一頁的程式填；卡住開 <code>-solution.ipynb</code></div>
</div>

<!--
★ 執行（約 14 分，訓練時先看 Part A 的放大圖）：最常見錯誤：D 那一步忘了 detach → G 的參數也被 D 的損失改到；或 G 那一步把假圖標成 0（等於幫 D 訓練）。
-->

---

<div class="eyebrow">05 · Lab L3-1</div>

# Lab 5／7：看網格，做練習

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-2" style="font-size:18px">
<div>

訓練完執行 Part C，再做下一頁的「練習：你的 GAN 崩塌了嗎？」：

1. 從哪個 epoch 開始看得出是衣物？
2. 最後的網格有沒有好幾格長得一樣？
3. 你的距離數字和真實圖片比，是大、是小、還是差不多？

</div>
<div>

<div class="node node--primary"><strong>換一個種子</strong><small>把第 1 格的 <code>SEED</code> 改成你的座號再跑一次，和講師的 SEED＝0（第 19 頁 Lab 1／7 的網格）比：只換隨機性，結果差多少？</small></div>

</div>
</div>

<div class="takeaway mt-4">GAN 的品質要「看」，而且要用證據說話。</div>

<!--
★ 對照（4 分）：SEED 一樣，大家的結果幾乎一樣（所以要改座號才看得出隨機性的影響）。個人作業，不必互相交卷。
-->

---

<div class="eyebrow">05 · Lab L3-1 · 練習</div>

# 練習：你的 GAN 崩塌了嗎？

<div class="muted" style="font-size:17px">看自己筆記本 Part B 的網格與 Part C 印出的距離（epoch 1、10、20），填下表。照著做：第一列已填好。</div>

<table class="fill tight vlines mt-1">
<thead><tr><th style="width:18%">epoch</th><th>看得出是什麼衣物嗎？</th><th>有幾格長得幾乎一樣？</th><th>兩兩平均距離</th></tr></thead>
<tbody>
<tr><td>真實圖片</td><td>是</td><td>0</td><td>（看 Part C 第一行）</td></tr>
<tr><td>1</td><td class="blank"><FillIn id="mc.e1-what" /></td><td class="blank"><FillIn id="mc.e1-same" /></td><td class="blank"><FillIn id="mc.e1-d" /></td></tr>
<tr><td>10</td><td class="blank"><FillIn id="mc.mid-what" /></td><td class="blank"><FillIn id="mc.mid-same" /></td><td class="blank"><FillIn id="mc.mid-d" /></td></tr>
<tr><td>20</td><td class="blank"><FillIn id="mc.last-what" /></td><td class="blank"><FillIn id="mc.last-same" /></td><td class="blank"><FillIn id="mc.last-d" /></td></tr>
<tr><td colspan="2">結論：有沒有崩塌？證據是什麼？</td><td class="blank" colspan="2"><FillIn id="mc.verdict" /></td></tr>
</tbody>
</table>

<FillClear group="mc" />

<!--
★ 練習（5 分）：每個人的結果不同，沒有標準答案；重點是「用網格＋數字當證據」下結論。下一頁是判斷方法。
-->

---
hostOnly: true
---

<div class="eyebrow">05 · Lab L3-1 · 練習解答</div>

# 練習解答：怎麼判斷

<div style="font-size:19px" class="mt-3">

- **epoch 1**：多半是模糊的團塊，距離可能很小（全部都糊成類似的樣子）
- **中間到最後**：衣物輪廓出現；距離應該往真實圖片的數字靠近
- **崩塌的證據**：最後的距離明顯小於真實圖片，而且網格裡有好幾格幾乎一樣、某些類別完全沒出現

</div>

<div class="takeaway mt-4">只有「網格」或只有「數字」都不夠：兩個一起看，才能說「崩塌了」或「沒崩塌」。</div>

<!--
★ 解答（2 分）：Colab T4 一次實跑（SEED=0，20 epoch）的參考值：真實圖片 22.90；epoch 1／5／10／20 為 20.97／21.93／21.67／22.08。距離與真實圖片相近、網格裡的衣物種類齊全，所以判斷「沒有崩塌」。每個人的數字會不同（research/lab-runs.md）。
-->

---

<div class="eyebrow">05 · Lab L3-1</div>

# Lab 6／7：Audit → Iterate

<table style="font-size:17px">
<thead><tr><th style="width:30%">稽核問題</th><th>具體動作</th><th style="width:30%">應該是</th></tr></thead>
<tbody>
<tr><td>真圖範圍和 G 輸出一致？</td><td>看 <code>Normalize</code> 與 <code>Tanh</code></td><td>都是 −1～1</td></tr>
<tr><td>D 那一步有 detach？</td><td>找 <code>fake.detach()</code></td><td>有</td></tr>
<tr><td>G 那一步的標籤？</td><td>看 <code>loss_g</code></td><td>ones（標成真）</td></tr>
<tr><td>網格用固定 z？</td><td>找 <code>fixed_z</code></td><td>整個訓練同一組</td></tr>
<tr><td>放大有沒有亂畫？</td><td>放大看耳罩紋理、邊緣（和原圖比）</td><td>耳罩多了小亮點、凹紋變淡</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">一次只改一件事：例如把第 1 格的 <code>LR_G</code> 調大，看網格會不會崩塌。</div>

<!--
★ 稽核（5 分）：第五列連到風險頁。今天的照片沒有文字；真實型錄有商標、文字時，也要逐張比對原圖。
-->

---

<div class="eyebrow">05 · Lab L3-1 · Ship</div>

# Lab 7／7：交給電商部的一頁

<table class="mt-2" style="font-size:18px">
<thead><tr><th style="width:34%">項目</th><th>內容</th></tr></thead>
<tbody>
<tr><td>放大前後對照</td><td>原圖、bicubic、Real-ESRGAN（同一塊局部）</td></tr>
<tr><td>每張處理時間（T4）</td><td>0.59 秒（233×263 → 4 倍；第一次含暖機 2.46 秒）</td></tr>
<tr><td>VRAM 峰值</td><td>0.62 GB</td></tr>
<tr><td>已知風險</td><td>會畫出原圖沒有的紋理；商標與文字要人工檢查</td></tr>
<tr><td>授權</td><td>Real-ESRGAN 程式與權重 BSD-3-Clause（待確認權重條款）</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">數千張乘上每張秒數，就是電商部要等的時間：這個數字比「很清楚」更有用。</div>

<!--
★ Ship（3 分）：以 T4 實測的 0.59 秒計：3000 張約 30 分鐘（0.59 × 3000 ≈ 1,770 秒）；這是 233×263 這種尺寸，目錄裡的圖更大就要重測。
-->

---

<div class="eyebrow">06 · Measure · 生成三難</div>

# 生成三難：品質、多樣性、速度

<div class="grid grid-cols-[1fr_1.1fr] gap-6 mt-1 items-center">
<div>

<svg viewBox="0 0 320 260" style="width:100%;max-height:270px" aria-label="三角形，三個角是品質、多樣性、速度；GAN 放在品質和速度那一邊">
  <polygon points="160,25 30,230 290,230" fill="var(--surface)" stroke="var(--muted-text)" stroke-width="2"/>
  <text x="160" y="18" text-anchor="middle" style="font-size:18px" fill="var(--text)">品質</text>
  <text x="22" y="252" style="font-size:18px" fill="var(--text)">多樣性</text>
  <text x="262" y="252" style="font-size:18px" fill="var(--text)">速度</text>
  <circle cx="210" cy="120" r="12" fill="var(--warm-accent)"/>
  <text x="228" y="126" style="font-size:18px" fill="var(--warm-accent)">GAN</text>
</svg>

</div>
<div style="font-size:18px">

| | GAN（今天） |
|---|---|
| 品質 | ✓ 清楚 |
| 速度 | ✓ 一次前向就畫完 |
| 多樣性 | ✗ 容易崩塌 |

<div class="muted mt-2" style="font-size:16px">D2-3 的 VAE：快、多樣，但糊。D3-3 的擴散模型會填第三列。</div>

</div>
</div>

<div class="takeaway mt-2">很難三個都要：這張三角形就是第四天學習評量備忘錄的骨架。</div>

<div class="src">「生成三難」（generative learning trilemma）：Xiao et al., 2022（S7，待確認）</div>

<!--
★ 三難（3 分）：請學員把今天的證據（網格、距離、秒數）寫進自己的三難表格第一列。
-->

---

<div class="eyebrow">06 · Measure & Risk（風險）</div>

# 風險：放大畫出來的細節，不一定是真的

<div class="grid grid-cols-2 gap-6 mt-3" style="font-size:18px">
<div class="node node--warm"><strong>假細節</strong><small>模型畫的是「看起來合理」的紋理：布料的織紋、甚至商標上的字——原圖可能根本沒有</small></div>
<div class="node"><strong>對商品照的意思</strong><small>放大後看起來比實物精緻 → 可能變成誇大不實；文字與商標一定要人工比對原圖</small></div>
</div>

<div class="grid grid-cols-[1fr_1fr_1.3fr] gap-4 mt-3 items-center">
<div><img class="photo" src="/headphones-bicubic-crop.png" alt="bicubic 放大的耳罩：模糊，但凹紋還在" style="height:170px;width:100%"><div class="shot-cap">bicubic：糊，但凹紋還在</div></div>
<div><img class="photo" src="/headphones-esrgan-crop.png" alt="Real-ESRGAN 放大的耳罩：凹紋變淡，多出小亮點" style="height:170px;width:100%"><div class="shot-cap">Real-ESRGAN：凹紋變淡、多了亮點</div></div>
<div style="font-size:18px">第 5 頁的耳罩就是例子：看起來更「清楚」，但和原物不一樣的地方，顧客分不出來。</div>
</div>

<div class="takeaway mt-4">放大是「畫」，不是「還原」：商品照要標示有經過 AI 處理，並保留原圖。</div>

<div class="src">消費者保護法、公平交易法對不實廣告的規定（S8，待確認條號）</div>

<!--
★ 風險（4 分）：和 D2-3 的「VAE 會讓小字變形」對照：VAE 是糊掉，GAN 是畫錯。兩種都要人工檢查文字。
-->

---

<div class="eyebrow">總整理</div>

# 今天學到的概念鏈

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-4">
  <span class="chip">放大只會糊</span><span class="arrow">→</span>
  <span class="chip">G 偽造、D 鑑定</span><span class="arrow">→</span>
  <span class="chip">min_G max_D</span><span class="arrow">→</span>
  <span class="chip">假圖標成真</span><span class="arrow">→</span>
  <span class="chip">輪流訓練</span><span class="arrow">→</span>
  <span class="chip">看網格、量崩塌</span><span class="arrow">→</span>
  <span class="chip">三難：GAN</span>
</div>

<div class="takeaway mt-6">GAN 清楚又快，但不穩、容易崩塌；對抗損失則是今天許多產品的零件。</div>

<!--
★ 總整理（2 分）：請學員用一句話回答「為什麼 GAN 的 loss 不能拿來判斷好壞」。
-->

---

<div class="eyebrow">隨堂檢核</div>

# 選擇題（iPAS 題型）

<div class="mcq">

1. GAN 中，鑑別器 D 的工作是？（　）<br><span class="opts">A. 產生新圖片　B. 判斷輸入是真實資料還是生成的　C. 壓縮影像　D. 選擇學習率</span>
2. 訓練 D 時對假圖使用 <code>fake.detach()</code>，目的是？（　）<br><span class="opts">A. 加快速度　B. 減少記憶體　C. 這一步不要更新 G　D. 讓 D 看不到假圖</span>
3. 「生成的圖很清楚，但幾乎都長一樣」稱為？（　）<br><span class="opts">A. 過擬合　B. 梯度消失　C. 量化誤差　D. mode collapse</span>
4. 下列何者今天仍使用對抗損失？（　）<br><span class="opts">A. Real-ESRGAN　B. k-means　C. 線性迴歸　D. 決策樹</span>

</div>

<!--
★ 檢核（3 分）。答案：1 B、2 C、3 D、4 A。
-->

---
hostOnly: true
---

<div class="eyebrow">下一步</div>

# 下一堂 D3-2：沒有成對影像的 B 線

<div class="node node--primary mt-2">品保部 B 線換了相機，A 線的瑕疵模型一直誤報；而且沒有「同一片板子在兩條線各拍一張」的成對影像。下一堂用兩組 G 和 D：CycleGAN，把 B 線的影像「翻譯」成 A 線的樣子——還要檢查瑕疵有沒有被翻譯掉。</div>

<!--
★ 只給講師的託管版看。
-->
