---
theme: default
title: 告訴我瑕疵在哪、有多大
info: |
  生成式AI原理 · D2-2
  在自編碼器上加跳接，變成 U-Net；沒有瑕疵遮罩，就自己合成瑕疵來訓練，再用真實遮罩量 IoU、Dice 與面積。
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
exportFilename: 06-unet-defect-mask
layout: center
class: cover
---

<div class="eyebrow">生成式AI原理 · D2-2</div>

# 告訴我瑕疵在哪、有多大

<p class="subtitle">加上跳接的 U-Net：每個像素都回答「是不是瑕疵」</p>

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-8">
  <span class="chip">AE 熱力圖太模糊</span><span class="arrow">→</span>
  <span class="chip">加跳接＝U-Net</span><span class="arrow">→</span>
  <span class="chip">合成瑕疵</span><span class="arrow">→</span>
  <span class="chip">BCE＋Dice</span><span class="arrow">→</span>
  <span class="chip">IoU／面積</span><span class="arrow">→</span>
  <span class="chip">維修站工具</span>
</div>

<!--
★ 開場（2 分）：上一堂的 AE 能說「這片怪怪的」，但熱力圖是一團霧。今天把同一張「壓扁再還原」的圖加上跳接，讓模型對每個像素回答「是／不是瑕疵」。
-->

---

<div class="eyebrow">00 · Frame（定義問題）</div>

# 維修站：不只要「有問題」，還要「在哪、多大」

<div class="ticket mt-2">
  <div class="ticket-head">【需求單 #D2-2】部門：製造品保部（維修站）<span>公司：曜嶼電子 <span class="fiction" style="color:#fff;border-color:#fff">虛構</span></span></div>
  <dl>
    <dt>問題</dt><dd>維修站要知道每個瑕疵的位置與面積，不只是「這片有問題」</dd>
    <dt>現況痛點</dt><dd>技術員拿放大鏡找瑕疵，一片要好幾分鐘</dd>
    <dt>成功指標（KPI）</dt><dd>在真實瑕疵遮罩上的 IoU、Dice（重疊程度，第 13 頁）；面積誤差（mm²）</dd>
    <dt>可用資料</dt><dd>大量良品；幾乎沒有瑕疵遮罩（用 VisA PCB1；真實遮罩只拿來測試）</dd>
    <dt>限制與法規</dt><dd>Colab T4；不能用來路不明的紋理資料集</dd>
    <dt>為何現有工具不夠</dt><dd>D2-1 的自編碼器只給一張模糊的誤差圖，沒有清楚的邊界</dd>
  </dl>
</div>

<!--
★ 需求單（3 分）：「遮罩」（mask）＝和影像一樣大的黑白圖，白色的像素就是瑕疵。今天模型的輸出就是一張遮罩。
-->

---

<div class="eyebrow">學習目標</div>

# 今天結束時，你能夠……

1. **說明**為什麼跳接適合「切割」，卻會讓 D2-1 的重建式偵測失效
2. **建立** U-Net，對每個像素輸出瑕疵機率，並**預測**每一層的 shape
3. **合成**瑕疵（自帶遮罩），在沒有標註的情況下訓練
4. **計算** IoU、Dice 與面積（mm²），並在**真實遮罩**上驗收

<!--
★ 目標（1 分）。不教：DRAEM 的完整雙網路（第 17 頁點名）、其他切割架構（DeepLab 等）。
-->

---

<div class="eyebrow">00 · Frame</div>

# 「這片有問題」不等於「問題在這裡」

<div class="grid grid-cols-[1.25fr_1fr_1fr] gap-4 mt-2 items-start">
<div>
  <img class="photo" src="/pcb1-scratch-outline.jpg" alt="VisA PCB1 一片有刮痕的 HC-SR04 板子，綠線圈出人工標註的刮痕" style="width:100%">
  <div class="shot-cap">真實不良品，綠線＝人工標註的遮罩</div>
</div>
<div>
  <img class="photo" src="/pcb1-scratch-zoom.jpg" alt="刮痕放大：Gnd 字樣旁幾道細白線" style="width:100%">
  <div class="shot-cap">放大：刮痕只佔原圖的 0.15%</div>
</div>
<div>
  <div class="placeholder" style="height:205px">D2-1 AE 的誤差熱力圖<small>講師實跑後替換</small></div>
  <div class="shot-cap">上一堂的輸出：只有亮暗，沒有邊界</div>
</div>
</div>

<div class="takeaway mt-4">維修站要的是綠線那樣「清楚的邊界」：有邊界，才量得出面積。</div>

<div class="src">影像與遮罩：VisA PCB1 第 087 張（Zou et al., 2022，CC BY 4.0，S1）；0.15% 為講師本機從遮罩計算</div>

<!--
★ Frame（4 分）：先讓學員找刮痕——不放大幾乎看不到。這片板子是 HC-SR04 超音波模組（VisA PCB1 全部都是這個型號）。
熱力圖的位置要等講師用 D2-1 的檢查點在 T4 跑出來再放；如果熱力圖剛好很準，也照實說，重點是「沒有邊界、量不出面積」。
-->

---

<div class="eyebrow">01 · Try（先用現成的）</div>

# 講師訓練好的 U-Net：遮罩疊在板子上

<div class="grid grid-cols-3 gap-4 mt-2">
<div><div class="placeholder" style="height:190px">輸入（真實不良品）<small>講師實跑後替換</small></div></div>
<div><div class="placeholder" style="height:190px">預測遮罩（機率 &gt; 0.5）<small>講師實跑後替換</small></div></div>
<div><div class="placeholder" style="height:190px">疊圖：紅＝預測、綠＝真實<small>講師實跑後替換（附 IoU）</small></div></div>
</div>

<div class="takeaway mt-4">先看結果：模型從沒看過真的瑕疵（只看過自己合成的），能圈出多少？</div>

<div class="src">模型為講師以 lab06 訓練的檢查點 unet_pcb1.pt；資料 VisA PCB1（S1）</div>

<!--
★ 示範（5 分）：用 lab06 解答筆記本的 overlays.png（最好、中間、最差各一張）。一定要給學員看「最差」那張，第 27 頁的風險就是在講它。
-->

---

<div class="eyebrow">02 · Open（打開黑盒子）· 今天的主角圖</div>

# 同一張圖，加上跳接＝U-Net

<div class="flex items-center justify-center gap-2 mt-3" style="font-size:17px">
  <div class="node" style="width:15%">輸入 x<small class="nw">&#91;B,3,256,256&#93;</small></div><span class="arrow">→</span>
  <div class="node node--primary" style="width:17%"><strong>往下</strong><small>三次池化，高寬 ÷8</small></div><span class="arrow">→</span>
  <div class="node node--warm" style="width:15%"><strong>瓶頸</strong><small class="nw">&#91;B,256,32,32&#93;</small></div><span class="arrow">→</span>
  <div class="node node--secondary" style="width:17%"><strong>往上</strong><small>三次放大，高寬 ×8</small></div><span class="arrow">→</span>
  <div class="node" style="width:15%">輸出<small class="nw">&#91;B,1,256,256&#93;</small></div>
</div>

<svg viewBox="0 0 900 70" style="width:100%;height:70px" aria-label="跳接箭頭從往下那一側連到往上那一側">
  <path d="M250,8 C330,60 570,60 650,8" fill="none" stroke="var(--primary)" stroke-width="3" marker-end="url(#sk)"/>
  <defs><marker id="sk" markerWidth="10" markerHeight="10" refX="7" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--primary)"/></marker></defs>
  <text x="450" y="64" text-anchor="middle" style="font-size:18px" fill="var(--primary)">跳接：往下每一層的輸出，直接接到往上同一層</text>
</svg>

<div class="grid grid-cols-2 gap-6 mt-1" style="font-size:18px">
<div class="node"><strong>D2-1 自編碼器</strong><small>輸出＝重建的影像 &#91;B, 3, H, W&#93;；所有資訊都要擠過瓶頸</small></div>
<div class="node node--primary"><strong>D2-2 U-Net</strong><small>輸出＝每個像素一個分數 &#91;B, 1, H, W&#93;；細節走跳接，不必擠過瓶頸</small></div>
</div>

<div class="takeaway mt-3">瓶頸負責「看懂整體」，跳接負責「把邊界畫準」。</div>

<div class="src">回顧：DL pp.72–79（U-Net 概念）；Ronneberger et al., U-Net (2015)（S2）</div>

<!--
★ 主角圖（6 分）：DL 課看過 U-Net 的圖（DL pp.72–79），今天看它為什麼適合切割。跳接（skip connection）是新詞：往下那一側的特徵圖保留了很細的邊緣位置，直接送到往上那一側。
-->

---

<div class="eyebrow">02 · Open · 為什麼 AE 不加跳接？</div>

# 跳接會把瑕疵「直接抄過去」

<div class="grid grid-cols-2 gap-6 mt-4" style="font-size:18px">
<div class="node node--warm"><strong>D2-1 的偵測靠「修不好」</strong><small>瑕疵擠不過瓶頸 → 重建圖沒有瑕疵 → 相減後瑕疵處誤差大</small></div>
<div class="node node--warm"><strong>AE 加了跳接會怎樣？</strong><small>瑕疵從跳接直接抄到輸出 → 重建得「太好」 → 誤差圖一片黑 → 漏檢</small></div>
</div>

<table class="mt-5" style="font-size:18px">
<thead><tr><th style="width:24%"></th><th>D2-1 自編碼器</th><th>D2-2 U-Net</th></tr></thead>
<tbody>
<tr><td>要學的答案</td><td>輸入本身（重建）</td><td>遮罩（哪些像素是瑕疵）</td></tr>
<tr><td>跳接</td><td>不能有（會照抄）</td><td>一定要有（邊界才準）</td></tr>
<tr><td>需要什麼資料</td><td>只要良品</td><td>要有遮罩 → 今天用合成的</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">同一個零件，用在不同的「答案」上，效果剛好相反：架構要配合你要模型學的東西。</div>

<!--
★ 關鍵對比（5 分）：這是 D2-1 第 19 頁「照抄」（identity shortcut）的延伸。問學員：「U-Net 也會照抄，為什麼它沒問題？」→ 因為 U-Net 要輸出的是遮罩，不是輸入本身；照抄輸入得不到遮罩。
-->

---

<div class="eyebrow">02 · Open · 接起來還是加起來</div>

# 跳接怎麼「接」：concatenate，不是相加

<div class="grid grid-cols-2 gap-6 mt-3" style="font-size:18px">
<div>

<div class="node node--primary"><strong>U-Net：接起來（concatenate）</strong><small>通道數相加</small></div>

```python
torch.cat([up, e3], dim=1)
# [B,128,64,64] + [B,128,64,64]
# → [B,256,64,64]
```

</div>
<div>

<div class="node"><strong>ResNet：加起來（add）</strong><small>通道數不變</small></div>

```python
up + e3
# [B,128,64,64] + [B,128,64,64]
# → [B,128,64,64]
```

</div>
</div>

<div class="muted mt-2" style="font-size:17px"><code>dim=1</code> 是通道那一維（D1-3 的 &#91;B, C, H, W&#93;）：接起來之後，下一層卷積自己決定要用多少「細節」、多少「整體」。</div>

<div class="takeaway mt-3">接起來 → 通道變兩倍，所以往上那一側的卷積輸入通道要算對。</div>

<div class="src">回顧：DL pp.38–55（CNN）；ResNet 的相加式跳接 He et al. 2016（S3）</div>

<!--
★ 接 vs 加（4 分）：學員最常寫錯的地方就是往上那一層的輸入通道。練習頁會要他們算。
-->

---

<div class="eyebrow">02 · Open · 練習</div>

# 練習：U-Net 每一層的 shape

<div class="muted" style="font-size:17px">不用 AI、先不執行。<code>block</code>：兩次 3×3 卷積（padding=1），高寬不變；<code>pool</code>：高寬 ÷2；<code>up</code>：ConvTranspose（stride 2），高寬 ×2。B ＝ 16，c ＝ 32</div>

<table class="fill tight vlines mt-1">
<thead><tr><th style="width:34%">程式</th><th>輸出 shape</th></tr></thead>
<tbody>
<tr><td><code>x</code>（輸入）</td><td>&#91;16, 3, 256, 256&#93;</td></tr>
<tr><td><code>e1 = enc1(x)</code>　3→32 通道</td><td>&#91;16, 32, 256, 256&#93;（照著做：通道變 32，高寬不變）</td></tr>
<tr><td><code>e2 = enc2(pool(e1))</code>　32→64</td><td class="blank"><FillIn id="unet.e2" /></td></tr>
<tr><td><code>e3 = enc3(pool(e2))</code>　64→128</td><td class="blank"><FillIn id="unet.e3" /></td></tr>
<tr><td><code>b = mid(pool(e3))</code>　128→256</td><td class="blank"><FillIn id="unet.b" /></td></tr>
<tr><td><code>up3(b)</code>　256→128</td><td class="blank"><FillIn id="unet.up3" /></td></tr>
<tr><td><code>torch.cat([up3(b), e3], 1)</code></td><td class="blank"><FillIn id="unet.cat" hint="通道：兩個加起來……" /></td></tr>
<tr><td><code>out = head(d1)</code>　32→1</td><td class="blank"><FillIn id="unet.out" /></td></tr>
</tbody>
</table>

<FillClear group="unet" corner />

<!--
★ 無 AI 檢核點（8 分）：第二列已填好當示範。對答案：筆記本 U-Net 那一格會用 show=True 印出每一層的 shape。不收回。
-->

---
hostOnly: true
---

<div class="eyebrow">02 · Open · 練習解答</div>

# 練習解答：U-Net 每一層的 shape

<table class="vlines" style="font-size:18px">
<thead><tr><th style="width:38%">程式</th><th>輸出 shape</th><th>說明</th></tr></thead>
<tbody>
<tr><td><code>e2</code></td><td>&#91;16, 64, 128, 128&#93;</td><td>池化 ÷2</td></tr>
<tr><td><code>e3</code></td><td>&#91;16, 128, 64, 64&#93;</td><td>再 ÷2</td></tr>
<tr><td><code>b</code></td><td>&#91;16, 256, 32, 32&#93;</td><td>瓶頸：高寬 ÷8</td></tr>
<tr><td><code>up3(b)</code></td><td>&#91;16, 128, 64, 64&#93;</td><td>放大 ×2，和 e3 一樣大</td></tr>
<tr><td><code>cat</code></td><td>&#91;16, 256, 64, 64&#93;</td><td>128 ＋ 128 通道</td></tr>
<tr><td><code>out</code></td><td>&#91;16, 1, 256, 256&#93;</td><td>每個像素一個 logit</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">怎麼對答案：筆記本 U-Net 格印出的 shape 表（本機 CPU 煙霧測試已確認，見 research/lab-runs.md）。</div>

<!--
★ 解答（2 分）：常見錯誤：cat 之後以為通道還是 128，於是 dec3 的輸入通道寫錯 → RuntimeError。
-->

---

<div class="eyebrow">03 · Adapt（調整）· 沒有遮罩怎麼辦</div>

# 沒有瑕疵遮罩？自己做（DRAEM 的想法）

<img class="photo mt-1" src="/synth-strip.png" alt="四格：真實良品、隨機斑塊遮罩、程式產生的彩色紋理、貼上紋理後的合成瑕疵" style="width:100%;max-height:205px;object-fit:contain;border:none">

<div class="grid grid-cols-4 gap-4 shot-cap" style="margin-top:0"><div>良品</div><div>① 遮罩</div><div>② 紋理</div><div>③ 合成瑕疵</div></div>

<div class="grid grid-cols-3 gap-4 mt-2" style="font-size:17px">
<div class="node"><strong>① 遮罩</strong><small>平滑的隨機雜訊，取最亮的一小塊 → 不規則斑塊</small></div>
<div class="node"><strong>② 紋理</strong><small>程式產生的彩色雜訊（不用來路不明的圖庫）</small></div>
<div class="node node--warm"><strong>③ 混合</strong><small>斑塊內：原圖和紋理混在一起；斑塊外不動</small></div>
</div>

<div class="takeaway mt-3">每一張合成瑕疵都「自帶正確答案」：遮罩是我們畫的，所以不用人工標註。</div>

<div class="src">左一為 VisA PCB1 真實良品（S1）；其餘三格由 lab06 的 <code>synth_defect</code> 在講師本機產生（random.seed(1)、SIZE 256；資料增強，不是模型輸出）；DRAEM：Zavrtanik et al., ICCV 2021（S4）</div>

<!--
★ 合成瑕疵（6 分）：DRAEM 原論文用 Perlin 雜訊做遮罩、DTD 紋理資料集當紋理；我們把紋理換成程式產生的雜訊，避開紋理資料集的授權問題（需求單的限制）。
一半的訓練圖不加瑕疵：模型也要學會回答「這片沒有」。
-->

---

<div class="eyebrow">03 · Adapt · 損失函數</div>

# 損失：逐像素 BCE ＋ Dice

<div class="grid grid-cols-[1fr_1.15fr] gap-6 mt-2">
<div>

<div class="node"><strong>BCE（二元交叉熵）</strong><small>每個像素都是一題「瑕疵／背景」的是非題（DL 課的二元分類）</small></div>

<div class="node node--warm mt-3"><strong>問題：瑕疵太少</strong><small>真實瑕疵常不到畫面的 1%：全部猜「背景」，BCE 就很低</small></div>

</div>
<div style="font-size:18px">

**4×4 的例子**：16 個像素裡 2 個是瑕疵

| 預測 | 像素正確率 | Dice |
|---|---|---|
| 全部猜背景 | 14／16 ＝ 87.5% | 0 |
| 圈對那 2 個 | 16／16 ＝ 100% | 1 |

```python
loss = bce(logits, m) + (1 - dice(sigmoid(logits), m))
```

</div>
</div>

<div class="muted" style="font-size:16px">讀作：<code>m</code>＝真實遮罩、<code>logits</code>＝模型輸出（還沒變成機率）；Dice 越大越好，所以用「1 − Dice」當損失。Dice 的算法在下一頁。</div>

<div class="takeaway mt-2">BCE 管每個像素；Dice 只看「瑕疵那幾個像素有沒有對到」，所以不會被大片背景騙。</div>

<!--
★ 損失（6 分）：Dice 的公式下一頁說。sigmoid 把 logit 變成 0–1 的機率（DL 課的二元分類最後一層）。
BCEWithLogitsLoss 會自己做 sigmoid，所以 BCE 那一項直接吃 logits。
-->

---

<div class="eyebrow">04 · Measure（量測驗收）</div>

# IoU 與 Dice：預測和答案重疊多少？

<div class="grid grid-cols-[1fr_1.2fr] gap-6 mt-2 items-center">
<div>

<svg viewBox="0 0 300 215" style="width:100%;max-height:230px" aria-label="兩個重疊的圓：真實遮罩與預測遮罩">
  <circle cx="115" cy="120" r="75" fill="var(--soft-blue)" fill-opacity="0.7" stroke="var(--primary)" stroke-width="2.5"/>
  <circle cx="185" cy="120" r="75" fill="var(--soft-amber)" fill-opacity="0.7" stroke="var(--warm-accent)" stroke-width="2.5"/>
  <text x="70" y="28" text-anchor="middle" style="font-size:18px" fill="var(--primary)">真實：共 10</text>
  <text x="235" y="28" text-anchor="middle" style="font-size:18px" fill="var(--warm-accent)">預測：共 10</text>
  <text x="150" y="126" text-anchor="middle" style="font-size:18px" fill="var(--text)">重疊 5</text>
</svg>

</div>
<div style="font-size:19px">

- **IoU** ＝ 重疊 ÷ 聯集（合起來的面積）
- **Dice** ＝ 2 × 重疊 ÷（預測面積 ＋ 真實面積）

**照著做**：真實 10 像素、預測 10 像素、重疊 5

- 聯集 ＝ 10 ＋ 10 − 5 ＝ 15 → IoU ＝ 5 ÷ 15 ≈ 0.33
- Dice ＝ 2 × 5 ÷ 20 ＝ 0.5

</div>
</div>

<div class="takeaway mt-3">兩個都在 0（完全沒對到）到 1（完全一樣）之間；報告時寫清楚用哪一個。</div>

<!--
★ IoU／Dice（5 分）：IoU（Intersection over Union，交集比聯集）。下一頁的練習讓學員自己發現 Dice 永遠 ≥ IoU。
-->

---

<div class="eyebrow">04 · Measure · 練習</div>

# 練習：在 5×5 的格子上算 IoU 和 Dice

<div class="grid grid-cols-[auto_1fr] gap-8 mt-2 items-start">
<div>
<div style="display:grid;grid-template-columns:repeat(5,44px);gap:3px">
  <div class="cg"></div><div class="cg"></div><div class="cg"></div><div class="cg"></div><div class="cg"></div>
  <div class="cg"></div><div class="cg ct">真</div><div class="cg cb">疊</div><div class="cg"></div><div class="cg"></div>
  <div class="cg"></div><div class="cg cb">疊</div><div class="cg cb">疊</div><div class="cg cp">預</div><div class="cg"></div>
  <div class="cg"></div><div class="cg ct">真</div><div class="cg cb">疊</div><div class="cg cp">預</div><div class="cg"></div>
  <div class="cg"></div><div class="cg"></div><div class="cg"></div><div class="cg"></div><div class="cg"></div>
</div>
<div class="muted mt-2" style="font-size:15px">真＝只有真實遮罩；預＝只有預測；疊＝兩個都有</div>
</div>
<div>

<table class="fill tight vlines">
<thead><tr><th style="width:44%">要算的</th><th>你的答案</th></tr></thead>
<tbody>
<tr><td>真實面積（真＋疊）</td><td class="blank"><FillIn id="iou.true" /></td></tr>
<tr><td>預測面積（預＋疊）</td><td class="blank"><FillIn id="iou.pred" /></td></tr>
<tr><td>聯集</td><td class="blank"><FillIn id="iou.union" /></td></tr>
<tr><td>IoU</td><td class="blank"><FillIn id="iou.iou" /></td></tr>
<tr><td>Dice</td><td class="blank"><FillIn id="iou.dice" /></td></tr>
<tr><td>Dice 和 IoU 哪個大？會不會反過來？</td><td class="blank"><FillIn id="iou.which" /></td></tr>
</tbody>
</table>

<FillClear group="iou" />

</div>
</div>

<!--
★ 練習（6 分）：照上一頁的「照著做」算。不用 AI。最後一題是要學員自己發現：Dice ＝ 2·IoU ÷（1 ＋ IoU），所以 Dice ≥ IoU，只有在 0 和 1 時相等。
-->

---
hostOnly: true
---

<div class="eyebrow">04 · Measure · 練習解答</div>

# 練習解答：IoU 與 Dice

<table class="vlines" style="font-size:19px">
<thead><tr><th style="width:40%">要算的</th><th>答案</th></tr></thead>
<tbody>
<tr><td>真實面積</td><td>2 ＋ 4 ＝ 6</td></tr>
<tr><td>預測面積</td><td>2 ＋ 4 ＝ 6</td></tr>
<tr><td>聯集</td><td>6 ＋ 6 − 4 ＝ 8</td></tr>
<tr><td>IoU</td><td>4 ÷ 8 ＝ 0.5</td></tr>
<tr><td>Dice</td><td>2 × 4 ÷ 12 ≈ 0.67</td></tr>
<tr><td>哪個大</td><td>Dice 永遠 ≥ IoU；只有完全沒對到（0）或完全一樣（1）時相等</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">所以「Dice 0.7」和「IoU 0.7」不是一樣好：同一個預測，Dice 的數字比較好看。</div>

<!--
★ 解答（2 分）：Dice ＝ 2·IoU ÷（1 ＋ IoU）。0.5 → 0.67。
-->

---

<div class="eyebrow">04 · Measure · 維修站的數字</div>

# 面積：像素 → mm²

<div class="grid grid-cols-[1.1fr_1fr] gap-6 mt-2" style="font-size:18px">
<div>

**校正值**從已知尺寸來：PCB1 是 HC-SR04 模組，板子約 **45 × 20 mm**

- 原圖 1404 × 1070 像素；板子約佔 946 × 418 像素
- 一個原圖像素 ≈ 45 ÷ 946 ≈ **0.048 mm**
- 縮成 256 × 256 後，寬和高的比例不同 → 分開算

```python
mm_x = 45 / 946 * 1404 / SIZE
mm_y = 20 / 418 * 1070 / SIZE
PX_MM2 = mm_x * mm_y        # 筆記本裡的名字
area = mask.sum() * PX_MM2
```

</div>
<div>

<div class="node node--primary"><strong>照著做：第 087 張的刮痕</strong><small>真實遮罩在原圖上約 2,330 個像素 × 0.0476 × 0.0478 mm² ≈ <strong>5.3 mm²</strong></small></div>

<div class="node node--warm mt-3"><strong>真實產線</strong><small>用相機校正片量 mm/像素，不要用「板子大概多大」估</small></div>

</div>
</div>

<div class="takeaway mt-3">面積 ＝ 瑕疵像素數 × 一個像素的面積；校正值錯了，每一個面積都錯。</div>

<div class="src">45 × 20 mm 為 HC-SR04 常見規格（S5，待確認）；946 × 418 像素與 2,330 像素為講師本機從 VisA 原圖與遮罩量測（research/lab-runs.md）</div>

<!--
★ 面積（4 分）：板子的長寬比 946 ÷ 418 ≈ 2.26，和 45 ÷ 20 ＝ 2.25 幾乎一樣，表示量測合理。
縮放：1404 × 1070 的原圖被壓成 256 × 256，水平方向縮了 5.48 倍、垂直方向縮了 4.18 倍，所以縮放後一個像素不是正方形。
-->

---

<div class="eyebrow">附錄 · 選修</div>

# DRAEM 的完整做法：兩個網路

<div class="flex items-center justify-center gap-3 mt-6" style="font-size:18px">
  <div class="node" style="width:22%">合成瑕疵影像</div><span class="arrow">→</span>
  <div class="node node--secondary" style="width:26%"><strong>重建網路</strong><small>像 D2-1 的 AE：把瑕疵「修掉」</small></div><span class="arrow">→</span>
  <div class="node node--primary" style="width:26%"><strong>判別網路（U-Net）</strong><small>把原圖和修好的圖「接起來」一起看，畫出遮罩</small></div>
</div>

<div class="takeaway mt-8">DRAEM ＝ D2-1 的重建 ＋ 今天的 U-Net：先修好，再比較兩張圖哪裡不同。</div>

<div class="src">Zavrtanik et al., DRAEM, ICCV 2021（S4）</div>

<!--
○ 選修（3 分）：今天的 lab 只做第二個網路（直接看原圖）。學員專題要更準時，可以把 D2-1 的 AE 輸出也接進 U-Net 當第 4–6 個通道。
-->

---

<div class="eyebrow">附錄 · 選修</div>

# U-Net 還會回來：擴散模型的去雜訊器

<div class="grid grid-cols-2 gap-6 mt-5" style="font-size:18px">
<div class="node"><strong>今天（D2-2）</strong><small>輸入：PCB 影像 → 輸出：每個像素「是不是瑕疵」</small></div>
<div class="node node--primary"><strong>D3-3 擴散模型</strong><small>輸入：加了雜訊的影像 → 輸出：每個像素「雜訊是多少」</small></div>
</div>

<div class="takeaway mt-6">輸入和輸出一樣大、要逐像素回答的工作，U-Net 都是常見選擇。</div>

<!--
○ 預告（2 分）：Stable Diffusion 的去雜訊網路就是一個（加了注意力的）U-Net。D3-3 的去雜訊 U-Net 結構和今天很像，但還要多一個輸入：現在是第幾步（timestep），所以不能原封不動搬過去。
-->

---

<div class="eyebrow">附錄 · 備用</div>

# 遮罩出現格子紋？棋盤格假影

<div class="grid grid-cols-2 gap-6 mt-4" style="font-size:18px">
<div class="node node--warm"><strong>現象</strong><small>預測遮罩或影像出現規則的格子狀紋路</small></div>
<div class="node"><strong>原因與解法</strong><small>ConvTranspose 的核大小不能被 stride 整除時，有些像素被「蓋」到兩次。主要解法：換成「先 Upsample 再卷積」（D2-1 第 9 頁的方法二）</small></div>
</div>

<div class="takeaway mt-6">今天的 <code>ConvTranspose2d(…, 2, stride=2)</code> 核大小＝stride，不會重疊；學員自己改架構時才會遇到。</div>

<div class="src">Odena et al., Deconvolution and Checkerboard Artifacts, Distill 2016（S6）</div>

<!--
△ 備用（2 分）：學員改成 kernel 3、stride 2 時看到格子紋再講。
-->

---

<div class="eyebrow">05 · Lab L2-2</div>

# Lab 1／7：我們要做出什麼？

<div class="grid grid-cols-2 gap-6 mt-2" style="font-size:19px">
<div>

**打開筆記本**：<code>materials/lab06-unet-defect.ipynb</code><br>
執行階段：**T4 GPU**<br>
資料：VisA PCB1（新的執行階段會重新下載約 1.9 GB；建議講師放共用雲端硬碟）

1. 只看過**合成**瑕疵的 U-Net，能圈出**真實**瑕疵嗎？
2. 在真實遮罩上，IoU、Dice 是多少？
3. 面積估得準嗎（mm²）？

</div>
<div>

<div class="placeholder" style="height:250px">目標：最好／中間／最差三張疊圖、IoU、Dice、面積誤差<small>講師實跑後換成真實輸出</small></div>

</div>
</div>

<div class="takeaway mt-3">驗收看的是<strong>真實</strong>遮罩上的成績，不是合成瑕疵上的。</div>

<!--
★ Lab 開始（3 分）：先執行前兩格（下載與讀圖），等待時講下一頁。
備案：沒有 GPU → SIZE＝64、EPOCHS＝2，只能確認程式跑得通（本機 CPU 試跑 1 epoch 的真實 IoU 是 0，不能當成績）；斷線 → 講師課前在 T4 訓練並分享 unet_pcb1.pt（見 teaching-plan 課前清單），放到工作目錄會自動載入、跳過訓練。
-->

---

<div class="eyebrow">05 · Lab L2-2</div>

# Lab 2／7：筆記本拆成哪幾塊？

<div class="mt-3" style="font-size:17px"><strong>訓練（只用良品）</strong></div>
<div class="flex items-center gap-2 mt-1" style="font-size:17px">
  <div class="node"><code>X_good</code><small class="nw">&#91;N,3,256,256&#93;</small></div><span class="arrow">→</span>
  <div class="node node--warm"><code>synth_defect</code><small class="nw">&#91;3,H,W&#93;＋&#91;1,H,W&#93;</small></div><span class="arrow">→</span>
  <div class="node node--primary"><code>UNet</code><small>logits &#91;B,1,H,W&#93;</small></div><span class="arrow">→</span>
  <div class="node"><code>loss_fn</code><small>BCE＋(1−Dice)</small></div>
</div>

<div class="mt-4" style="font-size:17px"><strong>驗收（只用真實不良品）</strong></div>
<div class="flex items-center gap-2 mt-1" style="font-size:17px">
  <div class="node"><code>X_bad</code>、<code>M_bad</code><small>真實影像與遮罩</small></div><span class="arrow">→</span>
  <div class="node"><code>predict</code><small>機率 &gt; 0.5</small></div><span class="arrow">→</span>
  <div class="node"><code>iou_dice</code><small>每張一個分數</small></div><span class="arrow">→</span>
  <div class="node"><code>area_pred</code><small>mm²</small></div>
</div>

<div class="takeaway mt-4">五個 TODO：<code>synth_defect</code> 的混合、<code>UNet.forward</code> 往上三次、<code>loss_fn</code>、<code>iou_dice</code>、面積。</div>

<!--
★ 拆塊（3 分）：訓練和驗收用的資料完全分開：真實不良品從頭到尾沒進過訓練。
-->

---

<div class="eyebrow">05 · Lab L2-2</div>

# Lab 3／7：先檢查合成瑕疵，再訓練

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-2" style="font-size:18px">
<div>

執行「合成瑕疵」那兩格，回答：

1. 遮罩的白色斑塊，和第四格的瑕疵位置一樣嗎？
2. 一個批次 16 張裡，有瑕疵的大約幾張？（應該接近一半）
3. 合成瑕疵看起來像真的刮痕或焊錫熔化嗎？哪裡不像？

</div>
<div>

<div class="node node--warm"><strong>為什麼要先看</strong><small>合成資料錯了（遮罩和瑕疵沒對齊、全部都有瑕疵），模型照樣會訓練、loss 照樣會降——但學到的是錯的東西</small></div>

</div>
</div>

<div class="takeaway mt-4">訓練之前先看資料：這是第 6／7 頁稽核的第一題。</div>

<!--
★ 檢查（4 分）：第 3 題沒有標準答案。合成的瑕疵多半是「彩色的斑」，真實的 PCB1 瑕疵是彎針、熔化、刮痕、缺件——這個落差就是第 27 頁的風險。
-->

---

<div class="eyebrow">05 · Lab L2-2</div>

# Lab 4／7：Specify

<div style="font-size:18px" class="mt-2">

<strong>【目標】</strong>只用良品＋合成瑕疵訓練 U-Net，對每個像素輸出瑕疵機率<br>
<strong>【輸入與輸出】</strong>PCB 影像 <code>&#91;B, 3, 256, 256&#93;</code>（0–1）→ logits <code>&#91;B, 1, 256, 256&#93;</code><br>
<strong>【限制】</strong>真實不良品與遮罩<strong>只用來驗收</strong>；Colab T4；每個 epoch 存檢查點<br>
<span class="muted" style="font-size:16px">為什麼：真實遮罩一進訓練，驗收分數就不再代表「沒看過的瑕疵」</span><br>
<strong>【驗收】</strong>① shape 表和練習頁一致　② loss 下降　③ 在真實遮罩上回報平均 IoU、Dice 與最差的一張　④ 面積用 mm² 回報

</div>

<!--
★ Specify（3 分）：驗收第 ③ 項要回報「最差的一張」，不只平均：維修站最在意的是漏掉的那種瑕疵。
-->

---

<div class="eyebrow">05 · Lab L2-2</div>

# Lab 5／7：Generate → Execute

<PromptBox>
這是 PyTorch 筆記本，請只填五個 # TODO：<br>
① synth_defect：斑塊內換成 beta*x ＋ (1−beta)*紋理，斑塊外不動<br>
② UNet.forward：往上三次，每次 up 放大後和同層的 e 用 torch.cat（dim=1）接起來，再進 dec；最後 head<br>
③ loss_fn：BCEWithLogits ＋（1 − 平均 Dice），Dice 用 sigmoid 後的機率<br>
④ iou_dice：每張的 IoU 與 Dice，分母為 0 時記 1.0<br>
⑤ 面積：像素數 × PX_MM2<br>
不要把真實遮罩放進訓練。每一格說明每一行在做什麼。
</PromptBox>

<div class="steps mt-2" style="font-size:17px">
  <div><span class="num">1</span>訓練時間待 T4 實測；等待時看 loss 有沒有往下</div>
  <div><span class="num">2</span>沒有 Agent 額度：照「接起來」、「損失」、「IoU 與 Dice」、「面積」四頁的程式填；卡住開 <code>-solution.ipynb</code></div>
</div>

<!--
★ 執行（約 20 分）：forward 是最容易錯的一格，先對照練習頁的 shape。
-->

---

<div class="eyebrow">05 · Lab L2-2</div>

# Lab 6／7：Audit → Iterate

<table style="font-size:17px">
<thead><tr><th style="width:30%">稽核問題</th><th>具體動作</th><th style="width:32%">應該是</th></tr></thead>
<tbody>
<tr><td>合成資料對齊嗎？</td><td>看條帶圖：遮罩和瑕疵位置一樣</td><td>一樣；約一半有瑕疵</td></tr>
<tr><td>訓練有沒有用到真實遮罩？</td><td>找 <code>M_bad</code> 出現在哪幾格</td><td>只在驗收格</td></tr>
<tr><td>Dice 用的是機率還是 logits？</td><td>看 <code>loss_fn</code></td><td><code>sigmoid(logits)</code></td></tr>
<tr><td>合成 vs 真實差多少？</td><td>比較兩行 IoU</td><td>合成的通常高很多（實測後填入）</td></tr>
<tr><td>最差的一張錯在哪？</td><td>看最差那張疊圖</td><td>說出是哪一類瑕疵</td></tr>
<tr><td>面積合理嗎？</td><td>看三張的預測與真實 mm²</td><td>同一個數量級（實測後填入）</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">一次只改一件事：例如合成瑕疵加一種「細長的線」（像刮痕），比較真實 IoU。</div>

<!--
★ 稽核（8 分）：最常見錯誤：Agent 把真實不良品也丟進訓練（「資料多一點比較好」）→ 真實 IoU 變得很漂亮，但已經不能代表沒看過的瑕疵。
-->

---

<div class="eyebrow">05 · Lab L2-2 · Ship</div>

# Lab 7／7：Gradio 維修站工具

<div class="grid grid-cols-[1.3fr_1fr] gap-5 mt-1">
<div>

```python
def locate(img):
    x = tf(img.convert("RGB"))
    p = (predict(x.unsqueeze(0))[0] > 0.5).float()
    area = p.sum().item() * PX_MM2
    return overlay(x, p), f"瑕疵面積約 {area:.2f} mm²"

gr.Interface(fn=locate, inputs=gr.Image(type="pil"),
             outputs=[gr.Image(), gr.Textbox()]).launch(share=True)
```

</div>
<div>

<div class="placeholder" style="height:200px">維修站工具畫面<small>講師實跑後替換</small></div>

</div>
</div>

<div class="muted mt-2" style="font-size:16px">讀作：<code>tf</code> 縮成 256×256；機率 &gt; 0.5 的像素算瑕疵；像素數 × <code>PX_MM2</code>（一個像素幾 mm²）＝面積；<code>overlay</code> 把瑕疵像素塗紅。</div>

<div class="takeaway mt-2">D2-1 的檢測站回答「要不要送修」；今天的工具回答「修哪裡、多大」。</div>

<!--
★ Ship（4 分）：overlay() 在筆記本裡把預測的像素塗紅。可以和 D2-1 的檢測站放在同一個 gr.Blocks 裡（D1-4 提過）。
-->

---

<div class="eyebrow">06 · Measure & Risk（風險）</div>

# 風險：合成的瑕疵不等於真實的瑕疵

<div class="grid grid-cols-2 gap-6 mt-3" style="font-size:18px">
<div class="node node--warm"><strong>模型只學到「彩色斑塊」</strong><small>真實 PCB1 的瑕疵是彎針、焊錫熔化、刮痕、缺件；合成資料沒有涵蓋的類型，模型可能完全看不到</small></div>
<div class="node"><strong>一定要在真實遮罩上驗收</strong><small>合成資料上的 IoU 只代表「模型學會了我們的合成規則」</small></div>
</div>

<table class="mt-4" style="font-size:18px">
<thead><tr><th></th><th>合成瑕疵上</th><th>真實遮罩上</th></tr></thead>
<tbody>
<tr><td>平均 IoU</td><td>講師實跑後填入</td><td>講師實跑後填入</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">合成資料讓你「開始」，真實資料決定你「能不能上線」。</div>

<!--
★ 風險（4 分）：數字來自 lab06 驗收格的兩行輸出。如果真實 IoU 很低，就照實說：這是誠實的基準線；改進方向是讓合成規則更像真實瑕疵，或收集少量真實遮罩微調。
-->

---

<div class="eyebrow">總整理</div>

# 今天學到的概念鏈

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-4">
  <span class="chip">位置＋面積</span><span class="arrow">→</span>
  <span class="chip">跳接＝U-Net</span><span class="arrow">→</span>
  <span class="chip">AE 不能加跳接</span><span class="arrow">→</span>
  <span class="chip">合成瑕疵</span><span class="arrow">→</span>
  <span class="chip">BCE＋Dice</span><span class="arrow">→</span>
  <span class="chip">IoU／Dice</span><span class="arrow">→</span>
  <span class="chip">mm²</span>
</div>

<div class="takeaway mt-6">跳接讓每個像素都能回答；合成資料解決「沒有標註」；真實遮罩才是驗收。</div>

<!--
★ 總整理（2 分）：請學員用一句話回答「為什麼 AE 不能加跳接，U-Net 卻一定要」。常見錯答：「U-Net 比較新」——重點是兩個模型要學的答案不同（重建 vs 遮罩）。
-->

---

<div class="eyebrow">隨堂檢核</div>

# 選擇題（iPAS 題型）

<div class="mcq">

1. U-Net 的跳接把往下那一層的特徵圖怎麼處理？（　）<br><span class="opts">A. 丟掉　B. 在通道維度接起來　C. 取平均　D. 只在訓練時使用</span>
2. 為什麼 D2-1 用來偵測瑕疵的自編碼器不能加跳接？（　）<br><span class="opts">A. 會變慢　B. 參數太多　C. 瑕疵會被直接抄到輸出，誤差變小　D. 不能用 GPU</span>
3. 預測 6 個像素、真實 6 個像素、重疊 3 個，IoU 是？（　）<br><span class="opts">A. 0.33　B. 0.25　C. 0.67　D. 0.5</span>
4. 為什麼損失要加 Dice？（　）<br><span class="opts">A. 讓訓練更快　B. BCE 不能微分　C. 為了算面積　D. 瑕疵像素太少，全部猜背景 BCE 也很低</span>

</div>

<!--
★ 檢核（4 分）。答案：1 B、2 C、3 A（3 ÷ 9）、4 D。
-->

---
hostOnly: true
---

<div class="eyebrow">下一步</div>

# 下一堂 D2-3：一張 T4 跑得動 512px 嗎？

<div class="node node--primary mt-2">行銷科技組第四天要大量生成 512px 商品圖。直接在像素上生成太貴；下一堂把主角圖的瓶頸變成「一團機率雲」（VAE），也看 Stable Diffusion 怎麼先壓縮再生成。</div>

<!--
★ 只給講師的託管版看。
-->
