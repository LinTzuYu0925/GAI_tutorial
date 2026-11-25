---
theme: default
title: 把影像和聲音變成編號
info: |
  生成式AI原理 · D2-4
  VQ-VAE 把瓶頸對到一本編碼簿，每個位置變成一個整數編號；位元數＝編號個數 × log2(編碼簿大小)。EnCodec 用同樣的想法把聲音壓到 1.5–24 kbps。第二天總整理、iPAS 小考與作業。
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
exportFilename: 08-vqvae-tokens
layout: center
class: cover
---

<div class="eyebrow">生成式AI原理 · D2-4</div>

# 把影像和聲音變成編號

<p class="subtitle">VQ-VAE：瓶頸對到一本編碼簿，資料變成一串整數</p>

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-8">
  <span class="chip">位元率 vs 品質</span><span class="arrow">→</span>
  <span class="chip">編碼簿</span><span class="arrow">→</span>
  <span class="chip">最近的一格</span><span class="arrow">→</span>
  <span class="chip">直通估計器</span><span class="arrow">→</span>
  <span class="chip">bits ＝ 個數 × log2(K)</span><span class="arrow">→</span>
  <span class="chip">token</span>
</div>

<!--
★ 開場（2 分）：第二天最後一堂。主角圖的瓶頸第四次變身：AE 的點 → VAE 的雲 → 今天變成「編碼簿裡的編號」。編號就是 token，第五天的 GPT、第六天的 MusicGen 都在生成這種編號。
-->

---

<div class="eyebrow">00 · Frame（定義問題）</div>

# 資訊部：錄音和影像把硬碟塞滿了

<div class="ticket mt-2">
  <div class="ticket-head">【需求單 #D2-4】部門：資訊部／客服中心<span>公司：曜嶼電子 <span class="fiction" style="color:#fff;border-color:#fff">虛構</span></span></div>
  <dl>
    <dt>問題</dt><dd>通話錄音與產線影像佔滿儲存空間，要用低位元率儲存與串流</dd>
    <dt>現況痛點</dt><dd>每月儲存費持續上升；串流到分廠很慢</dd>
    <dt>成功指標（KPI）</dt><dd>位元率與品質對照表（kbps：每秒幾千個位元）；每種設定實際用到幾個編號</dd>
    <dt>可用資料</dt><dd>公開的國語朗讀錄音（代替通話）；Fashion-MNIST（代替產線縮圖）</dd>
    <dt>限制與法規</dt><dd>不能用真實客戶錄音（個資法）</dd>
    <dt>為何現有工具不夠</dt><dd>VAE 的潛在表示是連續的小數，沒辦法變成固定位元數的編號</dd>
  </dl>
</div>

<!--
★ 需求單（3 分）：kbps（kilobits per second）：每秒要存或傳幾千個 0／1。位元率越低越省，但聲音越差——今天要量出這條取捨曲線。
-->

---

<div class="eyebrow">學習目標</div>

# 今天結束時，你能夠……

1. **說明**編碼簿查表：每個位置換成最近的那一格的編號
2. **讀懂**直通估計器 <code>z + (z_q − z).detach()</code> 為什麼讓梯度過得去
3. **計算**每張圖幾個 bits ＝ 編號個數 × log2(K)
4. **診斷**編碼簿的死碼（從沒被用到的格子）
5. **聽出** EnCodec 在不同位元率下的品質差異，並說出「影像和聲音都能變成 token」

<!--
★ 目標（1 分）。不教：EnCodec 的訓練、VQGAN 的完整訓練（只點名）、EMA 更新（△）。
-->

---

<div class="eyebrow">00 · Frame</div>

# 位元率 × 時間 ＝ 儲存成本

<div class="grid grid-cols-[1fr_1fr] gap-6 mt-3">
<div style="font-size:19px">

**照著算**：一通 10 分鐘的通話

| 格式 | 位元率 | 10 分鐘 |
|---|---|---|
| 未壓縮（24 kHz、16 位元） | <span class="nw">384 kbps</span> | <span class="nw">約 28.8 MB</span> |
| EnCodec 6 kbps | <span class="nw">6 kbps</span> | <span class="nw">約 0.45 MB</span> |
| EnCodec 1.5 kbps | <span class="nw">1.5 kbps</span> | <span class="nw">約 0.11 MB</span> |

</div>
<div>

<div class="node node--primary"><strong>算法</strong><small>MB ＝ kbps × 1000 × 秒數 ÷ 8 ÷ 1,000,000<br>例：384 × 1000 × 600 ÷ 8 ＝ 28,800,000 bytes</small></div>

<div class="node node--warm mt-3"><strong>但是</strong><small>位元率越低，聲音越糊；客服中心要的是「聽得懂、還能拿來做品質抽查」的最低位元率</small></div>

</div>
</div>

<div class="takeaway mt-3">儲存成本和位元率成正比；今天的問題是「最低能壓到多少 kbps，品質還能接受？」</div>

<!--
★ Frame（4 分）：表格只是算術，不是實驗結果。哪一個位元率「可接受」要聽過才知道（下一頁）。
未壓縮：24,000 個取樣／秒 × 16 位元 ＝ 384,000 位元／秒。
-->

---

<div class="eyebrow">01 · Try（先用現成的）</div>

# EnCodec：同一段錄音，不同位元率

<div class="grid grid-cols-[1.25fr_1fr] gap-6 mt-2">
<div>

<div class="placeholder" style="height:220px;min-height:0;padding:16px 24px">輸入：10 秒國語朗讀的頻譜圖（橫軸秒、縱軸頻率）<small>講師下載錄音後替換</small></div>

</div>
<div>

<div class="placeholder" style="height:105px;min-height:0">1.5 kbps 的音檔與頻譜<small>講師實跑後替換</small></div>
<div class="placeholder mt-2" style="height:105px;min-height:0">24 kbps 的音檔與頻譜<small>講師實跑後替換</small></div>

</div>
</div>

<div class="takeaway mt-3">先聽再猜：1.5 kbps 還聽得懂嗎？哪些聲音最先壞掉？（筆記本會跑 1.5、3、6、12、24 五種）</div>

<div class="src">錄音：維基百科「畢業（演藝界）」朗讀，Wikimedia Commons，CC BY-SA 4.0（S1）；模型 facebook/encodec_24khz（S2）</div>

<!--
★ 示範（5 分）：用 lab08 解答筆記本 Part A 的三個播放器（原始、1.5、24 kbps）。頻譜圖（spectrogram）：把聲音拆成「每個時間點、每個頻率有多少能量」，越亮越大聲。
不能用真實客服錄音（個資），所以用公開授權的朗讀。2026-11-24 下載錄音時 Wikimedia 回傳 429 限流，課前要先下載好。
-->

---

<div class="eyebrow">02 · Open（打開黑盒子）· 今天的主角圖</div>

# 瓶頸對到一本編碼簿（向量量化，VQ）

<div class="flex items-center justify-center gap-1 mt-3" style="font-size:16px">
  <div class="node" style="width:11%">輸入 x<small class="nw">&#91;B,1,28,28&#93;</small></div><span class="arrow">→</span>
  <div class="node node--primary" style="width:11%"><strong>Encoder</strong></div><span class="arrow">→</span>
  <div class="node" style="width:11%">z<small class="nw">&#91;B,16,7,7&#93;</small></div><span class="arrow">→</span>
  <div class="node node--warm" style="width:17%"><strong>查編碼簿</strong><small class="nw">每格 → 最近一格</small></div><span class="arrow">→</span>
  <div class="node" style="width:11%">z_q<small class="nw">&#91;B,16,7,7&#93;</small></div><span class="arrow">→</span>
  <div class="node node--secondary" style="width:11%"><strong>Decoder</strong></div><span class="arrow">→</span>
  <div class="node" style="width:11%">x̂<small class="nw">&#91;B,1,28,28&#93;</small></div>
</div>

<div class="grid grid-cols-[1fr_1.2fr] gap-6 mt-4 items-center">
<div>

<table style="font-size:16px">
<thead><tr><th>編號</th><th>這一格的向量（16 維）</th></tr></thead>
<tbody>
<tr><td>0</td><td>(0.12, −0.40, …)</td></tr>
<tr><td>1</td><td>(−0.85, 0.07, …)</td></tr>
<tr><td>…</td><td>…</td></tr>
<tr><td>K − 1</td><td>(0.33, 0.91, …)</td></tr>
</tbody>
</table>
<div class="shot-cap">編碼簿（codebook）：K 格，每格一個向量（數字為示意）</div>

</div>
<div style="font-size:18px">

- 每張圖變成 7 × 7 ＝ **49 個整數編號**
- 存檔、傳輸時只要存編號（和一本共用的編碼簿）
- 解碼器拿編號查回向量，再還原成圖

</div>
</div>

<div class="takeaway mt-2">AE 的點、VAE 的雲，今天變成「編號」：可以數、可以存、也可以拿給語言模型去「寫」。</div>

<div class="src">van den Oord et al., Neural Discrete Representation Learning (VQ-VAE), 2017（S3）</div>

<!--
★ 主角圖（6 分）：VQ（vector quantization，向量量化）。編碼簿（codebook）是模型的一部分，訓練時一起學。
編碼簿是共用的：所有圖片、所有通話都用同一本，所以只要存一次。
-->

---

<div class="eyebrow">02 · Open · 查表</div>

# 查表：找最近的那一格

<div class="grid grid-cols-[1fr_1.15fr] gap-6 mt-2 items-center">
<div>

<svg viewBox="0 0 300 230" style="width:100%;max-height:250px" aria-label="二維平面上五個編碼簿格子和一個編碼器輸出，虛線連到最近的格子">
  <line x1="20" y1="210" x2="290" y2="210" stroke="var(--muted-text)" stroke-width="1.2"/>
  <line x1="20" y1="210" x2="20" y2="15" stroke="var(--muted-text)" stroke-width="1.2"/>
  <circle cx="70" cy="60" r="9" fill="var(--soft-blue)" stroke="var(--primary)" stroke-width="2"/><text x="56" y="44" style="font-size:17px" fill="var(--primary)">0</text>
  <circle cx="200" cy="50" r="9" fill="var(--soft-blue)" stroke="var(--primary)" stroke-width="2"/><text x="190" y="34" style="font-size:17px" fill="var(--primary)">1</text>
  <circle cx="240" cy="160" r="9" fill="var(--soft-blue)" stroke="var(--primary)" stroke-width="2"/><text x="252" y="166" style="font-size:17px" fill="var(--primary)">2</text>
  <circle cx="110" cy="170" r="9" fill="var(--soft-blue)" stroke="var(--primary)" stroke-width="2"/><text x="90" y="196" style="font-size:17px" fill="var(--primary)">3</text>
  <circle cx="150" cy="110" r="9" fill="var(--soft-blue)" stroke="var(--primary)" stroke-width="2"/><text x="164" y="104" style="font-size:17px" fill="var(--primary)">4</text>
  <path d="M182,130 L158,115" stroke="var(--warm-accent)" stroke-width="2.5" stroke-dasharray="5 4"/>
  <rect x="178" y="126" width="14" height="14" fill="var(--warm-accent)"/>
  <text x="196" y="142" style="font-size:17px" fill="var(--warm-accent)">z</text>
</svg>

</div>
<div>

```python
d = torch.cdist(flat, codebook.weight)  # 每個 z 到每一格的距離
idx = d.argmin(dim=1)                   # 最近的那一格的編號
z_q = codebook(idx)                     # 查回那一格的向量
```

<div class="muted mt-2" style="font-size:16px"><code>flat</code>：把 z 攤平成「一列一個 16 維向量」<span class="nw">&#91;B·49, 16&#93;</span> → <code>d</code> <span class="nw">&#91;B·49, K&#93;</span> → <code>idx</code> <span class="nw">&#91;B·49&#93;</span></div>
<div class="muted mt-1" style="font-size:17px">讀作：算距離 → 挑最小的 → 換成那一格。圖上的 z 最近的是第 4 格，所以這個位置記成「4」。</div>

</div>
</div>

<div class="takeaway mt-3">「換成最近的一格」會丟掉一點資訊：z 和 z_q 之間的差距就是壓縮的代價。</div>

<!--
★ 查表（5 分）：cdist 讀作「兩兩之間的距離表」；argmin 讀作「最小值在第幾個」。這三行就是 lab Part B 的第一個 TODO。
-->

---

<div class="eyebrow">02 · Open · 直通估計器</div>

# 「挑最近的」不能微分：直通估計器

<div class="grid grid-cols-2 gap-6 mt-3" style="font-size:18px">
<div class="node node--warm"><strong>問題</strong><small>argmin 是「挑一個」：輸入稍微動一點，輸出不是不變就是跳到另一格，梯度不是 0 就是不存在 → 編碼器學不到東西</small></div>
<div class="node node--primary"><strong>解法：假裝查表是「直接通過」</strong><small>前向時用 z_q；反向時把 z_q 的梯度原封不動交給 z</small></div>
</div>

```python
z_st = z + (z_q - z).detach()   # 數值上 ＝ z_q；梯度上 ＝ z
```

<div class="muted mt-2" style="font-size:17px">讀作：<code>.detach()</code> 讓括號裡那段「不算梯度」。所以往前算時 z ＋ (z_q − z) ＝ z_q；往回傳時括號消失，只剩 z。</div>

<div class="takeaway mt-3">一行程式騙過反向傳播，在「不能微分的地方」開一條路。常見誤解：「detach 放哪裡都一樣」——放錯位置，梯度方向就錯了。</div>

<div class="src">直通估計器（straight-through estimator）：Bengio et al. 2013（S9）；VQ-VAE 論文（S3）</div>

<!--
★ 直通估計器（6 分）：straight-through estimator（直通估計器）。對照 D2-3 第 8 頁：重參數化把「抽樣」變成可微分；直通估計器把「查表」變成可微分。兩種都是工程技巧，不是數學推導。
常見誤解：detach 放哪裡都一樣。Lab 6／7 會看到放錯的後果。
-->

---

<div class="eyebrow">02 · Open · 損失</div>

# 兩個額外的損失：把編碼簿和編碼器拉近

```python
codebook_loss = mse(z_q, z.detach())   # 編碼簿往編碼器的輸出移動
commit_loss   = mse(z, z_q.detach())   # 編碼器別離編碼簿太遠
loss = mse(x_hat, x) + codebook_loss + 0.25 * commit_loss
```

<div class="grid grid-cols-2 gap-6 mt-3" style="font-size:18px">
<div class="node"><strong>codebook loss</strong><small>只更新編碼簿：讓被選到的格子靠近它代表的那些 z</small></div>
<div class="node"><strong>commitment loss（承諾損失）</strong><small>只更新編碼器：讓 z 乖乖待在某一格附近，不要到處跑；0.25 是論文用的權重（β）</small></div>
</div>

<div class="takeaway mt-3">重建損失管「還原得像」，另外兩項管「格子和 z 互相靠近」。</div>

<!--
★ 損失（5 分）：注意兩項的 detach 位置剛好相反：誰被 detach，誰就不動。
-->

---

<div class="eyebrow">03 · Measure（量測驗收）· 位元數</div>

# 一張圖幾個 bits？個數 × log2(K)

<div class="grid grid-cols-[1.1fr_1fr] gap-6 mt-2">
<div style="font-size:19px">

**照著做**：7 × 7 個編號、編碼簿 K ＝ 512

- 一個編號要幾個 bits？2⁹ ＝ 512 → **9 bits**
- 一張圖：49 × 9 ＝ **441 bits**
- 原圖：28 × 28 × 8 bits ＝ **6,272 bits**
- 壓縮比：6,272 ÷ 441 ≈ **14 倍**

</div>
<div>

<div class="node node--primary"><strong>為什麼是 log2(K)</strong><small>K 格要用幾個 0／1 才編得完：2 格要 1 位元、4 格要 2 位元、512 格要 9 位元</small></div>

<div class="node mt-3"><strong>EnCodec 也一樣</strong><small>每秒 75 步 × 每步 2 本編碼簿 × 每本 1024 格（10 bits）＝ 1,500 bits ＝ 1.5 kbps</small></div>

</div>
</div>

<div class="takeaway mt-3">位元數只看「幾個編號」和「編碼簿多大」，跟編號是什麼無關。</div>

<div class="src">EnCodec 24 kHz：75 步／秒、每本 1024 格（Défossez et al. 2022，S4）；筆記本 Part A 會印出 n_q 與步數</div>

<!--
★ 位元數（5 分）：這是今天唯一的公式。log2(K) 讀作「K 是 2 的幾次方」。
-->

---

<div class="eyebrow">03 · Measure · 練習</div>

# 練習：一張圖要幾個 bits？

<div class="muted" style="font-size:17px">不用 AI。原圖 6,272 bits。照上一頁的步驟算；第一列已填好。</div>

<table class="fill tight vlines mt-1">
<thead><tr><th style="width:24%">設定</th><th>每個編號幾 bits</th><th>一張圖幾 bits</th><th>壓縮幾倍</th></tr></thead>
<tbody>
<tr><td>7 × 7、K ＝ 512</td><td>9</td><td>441</td><td>約 14</td></tr>
<tr><td>7 × 7、K ＝ 16</td><td class="blank"><FillIn id="bits.a-b" /></td><td class="blank"><FillIn id="bits.a-total" /></td><td class="blank"><FillIn id="bits.a-ratio" /></td></tr>
<tr><td>7 × 7、K ＝ 128</td><td class="blank"><FillIn id="bits.b-b" /></td><td class="blank"><FillIn id="bits.b-total" /></td><td class="blank"><FillIn id="bits.b-ratio" /></td></tr>
<tr><td>14 × 14、K ＝ 512</td><td class="blank"><FillIn id="bits.c-b" /></td><td class="blank"><FillIn id="bits.c-total" hint="例：個數變幾倍……" /></td><td class="blank"><FillIn id="bits.c-ratio" /></td></tr>
<tr><td colspan="2">哪一個設定最省？你猜它的重建也最好嗎？</td><td class="blank" colspan="2"><FillIn id="bits.guess" /></td></tr>
</tbody>
</table>

<FillClear group="bits" />

<!--
★ 練習（6 分）：個人作業，不收回。最後一題的答案要等 lab Part B 跑完：K 越小越省，但重建誤差通常越大。
-->

---
hostOnly: true
---

<div class="eyebrow">03 · Measure · 練習解答</div>

# 練習解答：省位元，就要付出品質

<table class="vlines" style="font-size:19px">
<thead><tr><th style="width:26%">設定</th><th>每個編號</th><th>一張圖</th><th>壓縮</th></tr></thead>
<tbody>
<tr><td>7 × 7、K ＝ 16</td><td>4 bits</td><td>196</td><td>32 倍</td></tr>
<tr><td>7 × 7、K ＝ 128</td><td>7 bits</td><td>343</td><td>約 18 倍</td></tr>
<tr><td>14 × 14、K ＝ 512</td><td>9 bits</td><td>1,764</td><td>約 3.6 倍</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">最省的是 K ＝ 16，但只有 16 種「積木」可用，重建通常最差；對答案看 lab Part B 的 bits vs MSE 圖。</div>

<!--
★ 解答（2 分）：6272 ÷ 196 ＝ 32；6272 ÷ 343 ≈ 18.3；6272 ÷ 1764 ≈ 3.6。
-->

---

<div class="eyebrow">03 · Measure · 使用率</div>

# 死碼：有些格子從來沒被選過

<div class="grid grid-cols-[1.15fr_1fr] gap-6 mt-2">
<div>

<div class="placeholder" style="height:240px;padding:16px 24px">K ＝ 512 每一格被選幾次<small>直方圖，由多到少排序；講師實跑後替換（lab Part C）</small></div>

</div>
<div style="font-size:18px">

- 每一格被選了幾次，排序後畫成長條圖
- 很多格子次數 ＝ 0 → **死碼**（dead code）
- 死碼一樣佔位元：K ＝ 512 用 9 bits，但如果只用到 100 格，7 bits 就夠

</div>
</div>

<div class="takeaway mt-3">編碼簿越大不一定越好：用不到的格子是白付的位元。</div>

<!--
★ 死碼（5 分）：常見原因：編碼簿初始化離資料太遠，一開始沒被選到，就永遠不會被更新（codebook loss 只更新被選到的格子）。解法：EMA 更新、把死碼重新放到資料附近（附錄 △）。
-->

---

<div class="eyebrow">03 · Adapt（調整）· EnCodec 的做法</div>

# 殘差向量量化：一本不夠，就疊好幾本

<table class="vlines mt-3" style="font-size:17px">
<thead><tr><th style="width:18%">第幾本</th><th>收到什麼</th><th>查到的近似</th><th style="width:30%">交給下一本（剩下的）</th></tr></thead>
<tbody>
<tr><td>第 1 本</td><td>z</td><td>q₁（粗略）</td><td>r₁ ＝ z − q₁</td></tr>
<tr><td>第 2 本</td><td>r₁</td><td>q₂</td><td>r₂ ＝ r₁ − q₂</td></tr>
<tr><td>第 3 本…</td><td>r₂</td><td>q₃</td><td>…</td></tr>
<tr><td colspan="4"><strong>還原：</strong>z ≈ q₁ ＋ q₂ ＋ q₃ ＋ …（每一本都加進來，越多本越準）</td></tr>
</tbody>
</table>

<div class="grid grid-cols-2 gap-6 mt-5" style="font-size:18px">
<div class="node"><strong>位元率怎麼調</strong><small>用幾本編碼簿：1.5 kbps ＝ 2 本、24 kbps ＝ 32 本（每秒 75 步、每本 10 bits）</small></div>
<div class="node"><strong>好處</strong><small>同一個模型，只要少傳幾本，就能降低位元率</small></div>
</div>

<div class="takeaway mt-3">每一本編碼簿只負責「上一本沒編好的部分」：所以位元率可以一格一格往上加。</div>

<div class="src">Zeghidour et al., SoundStream (2021)；Défossez et al., EnCodec (2022)（S4、S5）</div>

<!--
★ 殘差量化（5 分）：RVQ（residual vector quantization，殘差向量量化）。lab Part A 每個位元率印出的「編碼簿 n_q 本」就是這個數字，請學員對照。
-->

---

<div class="eyebrow">04 · Open · 預告</div>

# 編號就是 token：語言模型也能「寫」圖和聲音

<div class="flex items-center justify-center gap-3 mt-5" style="font-size:18px">
  <div class="node" style="width:22%"><span class="nw">一張圖 →</span> <span class="nw">49 個編號</span><small>&#91;12, 407, 3, …&#93;</small></div><span class="arrow">→</span>
  <div class="node node--primary" style="width:22%"><strong>排成一列</strong><small>像一句話裡的字</small></div><span class="arrow">→</span>
  <div class="node node--secondary" style="width:26%"><strong>語言模型</strong><small>預測「下一個編號」</small></div>
</div>

<div class="grid grid-cols-2 gap-6 mt-5" style="font-size:18px">
<div class="node"><strong>D5-2 mini-GPT</strong><small>預測下一個字的編號</small></div>
<div class="node"><strong>D6-1 MusicGen</strong><small>預測下一個 EnCodec 編號 → 解碼成音樂</small></div>
</div>

<div class="takeaway mt-4">把資料變成編號之後，「生成圖片／音樂」就變成「寫一串編號」：這是向量量化（VQ）最大的用處。</div>

<!--
★ token（3 分）：token 這個字第一天已經出現過（文字的 token）。今天把它推廣到影像和聲音。
-->

---

<div class="eyebrow">附錄 · 選修</div>

# VQGAN：編碼簿＋對抗損失，畫得更清楚

<div class="grid grid-cols-2 gap-6 mt-5" style="font-size:18px">
<div class="node"><strong>VQ-VAE 的問題</strong><small>只用 MSE 重建，細節偏糊（和 D2-3 的 VAE 一樣）</small></div>
<div class="node node--primary"><strong>VQGAN 的做法</strong><small>解碼器多一個「鑑定師」（D3-1 的 GAN）和感知損失，讓還原的圖更銳利；許多影像 token 化工具都從這裡出發</small></div>
</div>

<div class="muted mt-3" style="font-size:16px">感知損失（perceptual loss）：不比逐像素的差，改比「預訓練影像模型看到的特徵」差多少，比較接近人眼的感覺。</div>

<div class="takeaway mt-3">想讓 VQ 的還原更清楚：加上鑑定師（對抗損失）和感知損失；鑑定師 D3-1 會學。</div>

<div class="src">Esser et al., Taming Transformers (VQGAN), 2021（S6）</div>

<!--
○ 選修（2 分）：D3-1 學 GAN 時會回來提：「對抗損失讓解碼器畫出細節」。
-->

---

<div class="eyebrow">附錄 · 備用</div>

# 不用 codebook loss：EMA 更新

<div style="font-size:19px" class="mt-4">

- 每一格 ＝ 最近被分到這一格的那些 z 的**移動平均**（EMA）
- 不用梯度更新編碼簿 → 訓練更穩
- 搭配「死碼重新放到資料附近」，使用率會好很多

</div>

<div class="takeaway mt-4">死碼太多時：換成 EMA 更新，再把沒用到的格子重新放到資料附近。</div>

<!--
△ 備用（2 分）：學員發現死碼很多時再講。EMA（exponential moving average，指數移動平均）。
-->

---

<div class="eyebrow">05 · Lab L2-4</div>

# Lab 1／7：我們要做出什麼？

<div class="grid grid-cols-2 gap-6 mt-2" style="font-size:19px">
<div>

**打開筆記本**：<code>lab08-vqvae.ipynb</code>（在 <code>materials/</code>）→ Open in Colab<br>
執行階段：**T4 GPU**

1. EnCodec 壓到 1.5 kbps 還聽得懂嗎？
2. 自己的 VQ-VAE：K ＝ 16／128／512，bits 和誤差怎麼變？
3. 編碼簿用到幾格？

</div>
<div>

<div class="placeholder" style="height:250px;padding:16px 24px">目標：位元率表、三個播放器、bits vs 誤差圖、使用率直方圖<small>講師 T4 實跑後換成真實輸出（含 VRAM 峰值與總時間）</small></div>

</div>
</div>

<div class="takeaway mt-3">交付給資訊部的是一張「位元率 vs 品質」對照表，不是一句「壓得很小」。</div>

<!--
★ Lab 開始（3 分）：錄音檔約 54 MB、EnCodec 模型約數十 MB；下載時間、VRAM 峰值與總時間待 T4 實測（teaching-plan 課前清單）。錄音備案：講師課前把錄音放在共用雲端硬碟，學員改 LOCAL 路徑；拿不到錄音也可以先做 Part B、C。沒有 GPU → EPOCHS＝1（Part A 在 CPU 也跑得動）。
-->

---

<div class="eyebrow">05 · Lab L2-4</div>

# Lab 2／7：筆記本拆成哪幾塊？

<div class="mt-2" style="font-size:17px"><strong>Part A：EnCodec（現成模型）</strong></div>
<div class="flex items-center gap-2 mt-1" style="font-size:17px">
  <div class="node"><code>wave</code><small>10 秒、24 kHz</small></div><span class="arrow">→</span>
  <div class="node node--primary"><code>codec.encode</code><small>bandwidth＝1.5…24</small></div><span class="arrow">→</span>
  <div class="node node--warm"><code>audio_codes</code><small>n_q 本 × T 步</small></div><span class="arrow">→</span>
  <div class="node node--secondary"><code>codec.decode</code><small>還原音訊</small></div>
</div>

<div class="mt-4" style="font-size:17px"><strong>Part B：自己的 VQ-VAE；Part C：編碼簿用了幾格</strong></div>
<div class="flex items-center gap-2 mt-1" style="font-size:17px">
  <div class="node"><code>enc</code><small class="nw">&#91;B,16,7,7&#93;</small></div><span class="arrow">→</span>
  <div class="node node--warm"><code>quantize</code><small>編號 idx</small></div><span class="arrow">→</span>
  <div class="node"><code>z_st</code><small>直通估計器</small></div><span class="arrow">→</span>
  <div class="node node--secondary"><code>dec</code><small>還原</small></div>
</div>

<div class="takeaway mt-4">四個 TODO：<code>codec.decode</code>、kbps 的算法、<code>quantize</code> 的查表、直通估計器。</div>

<!--
★ 拆塊（3 分）：Part A 是「用現成的」（Try），Part B 是「自己做一個小的」（Open）。
-->

---

<div class="eyebrow">05 · Lab L2-4</div>

# Lab 3／7：Specify

<div style="font-size:18px" class="mt-2">

<strong>【目標】</strong>量出 EnCodec 的位元率與品質；自己訓練 VQ-VAE，比較 K ＝ 16／128／512<br>
<strong>【輸入與輸出】</strong>10 秒錄音（24 kHz）→ 編號 → 還原音訊；Fashion-MNIST <code>&#91;B,1,28,28&#93;</code> → 49 個編號 → 還原<br>
<strong>【限制】</strong>只用公開授權的錄音；三個 K 用同樣的 epochs；Colab T4<br>
<span class="muted" style="font-size:16px">為什麼：真實通話是個資；只差一個變因（K），比較才有意義</span><br>
<strong>【驗收】</strong>① 位元率表的 kbps 和設定一致　② 頻譜誤差隨位元率下降　③ bits vs 誤差圖：K 越大誤差越小　④ 回報 K ＝ 512 的死碼數

</div>

<!--
★ Specify（3 分）：頻譜誤差：兩段聲音的頻譜（dB）平均差多少，越低越像。不用 SNR（逐點相減）：神經網路編碼器不保證波形相位一樣，聽起來很像、逐點相減卻差很多（講師本機試跑時 24 kbps 的 SNR 幾乎是 0 dB）。
-->

---

<div class="eyebrow">05 · Lab L2-4</div>

# Lab 4／7：Generate → Execute

<PromptBox>
這是 PyTorch 筆記本，請只填四個 # TODO：<br>
① Part A：codec.decode(enc.audio_codes, enc.audio_scales, mask)&#91;0&#93; 還原音訊<br>
② Part A：bits ＝ n_q × T × log2(1024)；kbps ＝ bits ÷ 秒數 ÷ 1000<br>
③ Part B：quantize 用 torch.cdist 算距離、argmin 取編號、codebook(idx) 查回向量並排回 &#91;B, D, H, W&#93;<br>
④ Part B：直通估計器 z ＋ (z_q − z).detach()<br>
不要改模型大小與 epochs。每一格說明每一行在做什麼。
</PromptBox>

<div class="steps mt-2" style="font-size:17px">
  <div><span class="num">1</span>三次訓練（K ＝ 16、128、512）時間待 T4 實測；等待時聽 Part A 的三個播放器</div>
  <div><span class="num">2</span>沒有 Agent 額度：照「查表」、「直通估計器」、「一張圖幾個 bits」三頁的程式填；卡住開 <code>-solution.ipynb</code></div>
</div>

<!--
★ 執行（約 14 分，訓練時聽 Part A 的播放器）：③ 最容易錯在 permute：z 是 [B, D, H, W]，要先把 D 移到最後再攤平成 [B·H·W, D]。
-->

---

<div class="eyebrow">05 · Lab L2-4</div>

# Lab 5／7：對照你的預測

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-2" style="font-size:18px">
<div>

跑完 Part B 後，回到「練習：一張圖要幾個 bits？」：

1. 筆記本印出的 bits 和你算的一樣嗎？
2. K ＝ 16 的重建真的最差嗎？差多少？
3. K ＝ 512 用到幾格？如果只用到那麼多格，其實需要幾 bits？

</div>
<div>

<div class="node node--primary"><strong>看 7 × 7 編號圖</strong><small>筆記本印出鞋子和褲子的 7 × 7 編號陣列：哪些編號兩張都有？圖的顏色只是輔助，要比的是印出來的數字。</small></div>

</div>
</div>

<div class="takeaway mt-4">位元數是算出來的，品質是量出來的：兩個都要報。</div>

<!--
★ 對照（4 分）：第 3 題：用到 N 格，就只需要 log2(N) 無條件進位的 bits。
-->

---

<div class="eyebrow">05 · Lab L2-4</div>

# Lab 6／7：Audit → Iterate

<table style="font-size:17px">
<thead><tr><th style="width:30%">稽核問題</th><th>具體動作</th><th style="width:30%">應該是</th></tr></thead>
<tbody>
<tr><td>kbps 算對了嗎？</td><td>比較「設定」和「實際」兩欄</td><td>幾乎一樣</td></tr>
<tr><td>錄音的授權？</td><td>看 Part A 的說明</td><td>CC BY-SA 4.0，要標示來源</td></tr>
<tr><td>直通估計器的 detach 位置？</td><td>看 <code>z_st</code> 那一行</td><td>只 detach (z_q − z)</td></tr>
<tr><td>K 越大誤差越小？</td><td>看 bits vs MSE 圖</td><td>講師實跑後填入</td></tr>
<tr><td>死碼多少？</td><td>看直方圖標題</td><td>講師實跑後填入</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">一次只改一件事：例如把 K ＝ 512 的 epochs 加倍，看死碼會不會變少。</div>

<!--
★ 稽核（6 分）：最常見錯誤：detach 放錯位置。例如寫成 z.detach() ＋ (z_q − z)：數值一樣是 z_q，但傳回 z 的梯度變成上游梯度的相反數，編碼器被往錯的方向推，loss 不降甚至發散；編碼簿還會直接收到重建梯度。完全不寫直通估計器（直接用 z_q）才是「編碼器收不到重建梯度」。
-->

---

<div class="eyebrow">05 · Lab L2-4 · Ship</div>

# Lab 7／7：交給資訊部的位元率表

<table class="mt-2" style="font-size:18px">
<thead><tr><th>位元率</th><th>編碼簿本數</th><th>10 分鐘大小</th><th>頻譜誤差（dB）</th><th>聽起來</th></tr></thead>
<tbody>
<tr><td>1.5 kbps</td><td>2</td><td>約 0.11 MB</td><td>實跑後填入</td><td>實跑後填入</td></tr>
<tr><td>6 kbps</td><td>8</td><td>約 0.45 MB</td><td>實跑後填入</td><td>實跑後填入</td></tr>
<tr><td>24 kbps</td><td>32</td><td>約 1.8 MB</td><td>實跑後填入</td><td>實跑後填入</td></tr>
<tr><td>未壓縮</td><td>—</td><td>約 28.8 MB</td><td>—</td><td>原音</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">建議要附理由：「客服抽查用 ＿＿ kbps：大小約未壓縮的 1/＿＿，聽起來 ＿＿」——空格等實跑後再填。</div>

<!--
★ Ship（3 分）：大小與本數是算術（本機試跑已印出 2／8／32 本、每秒 75 步）；頻譜誤差與「聽起來」一定要等 T4 實跑。
-->

---

<div class="eyebrow">06 · Measure & Risk（風險）</div>

# 風險：通話錄音是個資

<div class="grid grid-cols-2 gap-6 mt-3" style="font-size:18px">
<div class="node node--warm"><strong>不能拿來練習的</strong><small>真實客服錄音：有姓名、電話、聲音本身也能認出人；原則上要先告知並取得同意，才能拿來訓練或展示（法條依據待確認）</small></div>
<div class="node"><strong>今天的做法</strong><small>公開授權的朗讀錄音（標示作者與授權）；真的要用公司資料時，先去識別化、取得同意、限制存取</small></div>
</div>

<div class="node mt-4" style="font-size:18px"><strong>壓縮也是處理</strong><small>壓縮後的通話一樣是個資；位元率再低，聽得懂就要照個資規定保存與刪除</small></div>

<div class="takeaway mt-3">「壓得很小」不會讓個資變成不是個資。</div>

<div class="src">個人資料保護法（法務部全國法規資料庫，S7，待確認條號）</div>

<!--
★ 風險（4 分）：D6-1 會再談聲音複製（voice cloning）需要當事人同意。
-->

---

<div class="eyebrow">第二天總整理</div>

# 一張主角圖，四種瓶頸

<table class="mt-2" style="font-size:18px">
<thead><tr><th style="width:16%">單元</th><th style="width:22%">瓶頸變成</th><th>解決的需求單</th><th>關鍵一行</th></tr></thead>
<tbody>
<tr><td>D2-1 AE</td><td>窄的點</td><td>品保：沒看過的瑕疵</td><td><code>score ＝ 誤差最大 1%</code></td></tr>
<tr><td>D2-2 U-Net</td><td>點＋跳接</td><td>維修站：在哪、多大</td><td><code>torch.cat(&#91;up, e&#93;, 1)</code></td></tr>
<tr><td>D2-3 VAE</td><td>一團雲</td><td>行銷科技：512px 壓 48 倍</td><td><code>z ＝ μ ＋ σ·ε</code></td></tr>
<tr><td>D2-4 VQ-VAE</td><td>編碼簿的編號</td><td>資訊部：低位元率</td><td><code>z ＋ (z_q − z).detach()</code></td></tr>
</tbody>
</table>

<div class="takeaway mt-4">同一張「編碼器 → 瓶頸 → 解碼器」，只改瓶頸，就解決了四種不同的商業問題。</div>

<!--
★ 第二天總整理（4 分）：請學員對每一列說一句「為什麼要這樣改」。第三天換一種完全不同的生成方式：GAN（偽造者與鑑定師）和擴散模型。
-->

---

<div class="eyebrow">第二天 · iPAS 小考</div>

# 第二天小考 1／3（iPAS 題型）：點選答案

<Mcq id="quiz1.q1" :n="1" :answer="2"
  :options="['只有不良品', '良品與不良品各半', '只有良品', '不需要資料']"
  :why="['要學的是「正常長什麼樣」；只學不良品，正常板反而會被判成異常。', '各半就變成分類問題，需要大量瑕疵標註；而且沒見過的新瑕疵照樣抓不到。', '', 'AE 要從資料學會重建，沒有資料就沒有模型。']"
  explain="只用良品訓練，AE 只會重建良品；瑕疵重建不好、誤差變大，就報警。">
用 AE（自編碼器）做異常偵測，訓練資料應該是？
</Mcq>

<Mcq id="quiz1.q2" :n="2" :answer="1"
  :options="['參數變少', '保留細節、畫準邊界', '不需要訓練', '輸出類別標籤']"
  :why="['跳接會多一些通道，參數不會變少。', '', '有跳接一樣要訓練。', 'U-Net 輸出的是每個像素的遮罩，不是一個標籤。']"
  explain="編碼器的高解析度特徵直接接到解碼器，瑕疵的邊界畫得準。">
U-Net 的跳接主要讓模型？
</Mcq>

<FillClear group="quiz1" corner />

<!--
★ 檢核 1／3（2 分）：學員自己點；點錯會出現「再想想」和那個選項錯在哪，可以再點一次。答案：1 C、2 B。
-->

---

<div class="eyebrow">第二天 · iPAS 小考</div>

# 第二天小考 2／3（iPAS 題型）：點選答案

<Mcq id="quiz2.q3" :n="3" :answer="3"
  :options="['0.67', '0.33', '0.25', '0.5']"
  :why="['4 ÷ 6 是重疊除以預測，只算了一邊；分母要用聯集。', '4 ÷ 12 是把兩邊直接相加當分母，重疊的 4 個被算了兩次。', '太小了：聯集只有 8，4 ÷ 8 不會是 0.25。', '']"
  explain="聯集 ＝ 6 ＋ 6 − 4 ＝ 8，IoU ＝ 4 ÷ 8 ＝ 0.5。">
預測 6 像素、真實 6 像素、重疊 4，IoU ＝？
</Mcq>

<Mcq id="quiz2.q4" :n="4" :answer="0"
  :options="['把每團雲拉向標準常態分布', '讓重建更清楚', '減少參數', '加快推論']"
  :why="['', '讓重建清楚的是重建損失；KL 反而會讓重建稍微模糊。', 'KL 是損失的一項，不改變參數數量。', '推論速度和損失函數無關。']"
  explain="KL 把每張圖的雲拉向標準常態分布，雲彼此靠攏、沒有空洞，才能隨機取點生成。">
VAE 損失中的 KL 項作用是？
</Mcq>

<FillClear group="quiz2" corner />

<!--
★ 檢核 2／3（2 分）。答案：3 D、4 A。
-->

---

<div class="eyebrow">第二天 · iPAS 小考</div>

# 第二天小考 3／3（iPAS 題型）：點選答案

<Mcq id="quiz3.q5" :n="5" :answer="2"
  :options="['49', '256', '392', '12,544']"
  :why="['49 是編號的個數，每個編號還要 8 bits。', '256 是編碼簿的格數，不是 bits。', '', '12,544 是 49 × 256：把格數當成 bits 了，應該用 log2(256) ＝ 8。']"
  explain="每個編號從 256 格選一格，要 log2(256) ＝ 8 bits；49 × 8 ＝ 392 bits。">
7 × 7 個編號、編碼簿 256 格，一張圖幾 bits？
</Mcq>

<Mcq id="quiz3.q6" :n="6" :answer="1"
  :options="['過擬合', '查表（argmin）不能微分', '資料太少', '學習率太大']"
  :why="['直通估計器和過擬合無關。', '', '直通估計器不會增加資料。', '問題不是梯度太大，而是梯度根本傳不過去。']"
  explain="從編碼簿挑最近的一格（argmin）沒有梯度；直通估計器在反向傳播時把梯度直接抄回編碼器。">
VQ-VAE 的直通估計器解決什麼問題？
</Mcq>

<FillClear group="quiz3" corner />

<!--
★ 檢核 3／3（2 分）。答案：5 C、6 B。
全部答案與理由：1 C、2 B、3 D（4 ÷ 8）、4 A、5 C（49 × 8）、6 B。
-->

---

<div class="eyebrow">第二天 · 回家作業</div>

# 回家作業：換一個 VisA 類別，寫半頁門檻建議

<div class="grid grid-cols-[1fr_1.1fr] gap-6 mt-2">
<div>

<img class="photo" src="/visa-pcb2-capsules.jpg" alt="VisA 的另外兩個類別：一片 PCB2 電路板和一盤膠囊" style="width:100%">
<div class="shot-cap">可選的類別（例）：PCB2、capsules</div>

</div>
<div style="font-size:18px">

1. 用 lab05，把載入資料那一格的 <code>CATEGORY</code> 換成 VisA 的另一個類別（例如 <code>"pcb2"</code>）
2. 記錄 AUROC、漏檢 ≤ 5% 時的過殺率
3. 先檢查資料：良品和不良品的拍攝條件一樣嗎？
4. 寫半頁給品保主管：建議門檻、理由、代價、還不確定的地方

</div>
</div>

<div class="takeaway mt-3">作業的重點是第 4 點：數字要能變成主管看得懂的決定。</div>

<div class="src">影像：VisA pcb2、capsules 類別（Zou et al., 2022，CC BY 4.0），講師裁切</div>

<!--
★ 作業（3 分）：第 3 點是 D2-1「拍攝方向」資料陷阱的延伸。下一次上課（D3-1）開場 5 分鐘回顧。
-->

---
hostOnly: true
---

<div class="eyebrow">下一步</div>

# 下一堂 D3-1：舊照片放大，偽造者與鑑定師

<div class="node node--primary mt-2">電商部有幾千張解析度太低的舊型錄照片。一般放大只會變糊；明天用 GAN：一個網路負責「偽造」細節、另一個負責「鑑定」真假，兩個一起進步。</div>

<!--
★ 只給講師的託管版看。
-->
