---
theme: default
title: 告訴我瑕疵在哪、有多大
info: |
  生成式AI原理 · L06
  在自編碼器上加跳接，變成 U-Net；用合成瑕疵加上少量真實遮罩訓練，再用沒看過的真實遮罩量 IoU、Dice 與面積。
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

<div class="eyebrow">生成式AI原理 · L06</div>

# 告訴我瑕疵在哪、有多大

<p class="subtitle">加上跳接的 U-Net：每個像素都回答「是不是瑕疵」</p>

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-8">
  <span class="chip">AE 熱力圖太模糊</span><span class="arrow">→</span>
  <span class="chip">加跳接＝U-Net</span><span class="arrow">→</span>
  <span class="chip">合成＋少量真實遮罩</span><span class="arrow">→</span>
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
  <div class="ticket-head">【需求單 #L06】部門：製造品保部（維修站）<span>公司：曜嶼電子 <span class="fiction" style="color:#fff;border-color:#fff">虛構</span></span></div>
  <dl>
    <dt>問題</dt><dd>維修站要知道每個瑕疵的位置與面積，不只是「這片有問題」</dd>
    <dt>現況痛點</dt><dd>技術員拿放大鏡找瑕疵，一片要好幾分鐘</dd>
    <dt>成功指標（KPI）</dt><dd>在真實瑕疵遮罩上的 IoU、Dice（重疊程度，第 16 頁）；面積誤差（mm²）</dd>
    <dt>可用資料</dt><dd>大量良品；技術員一個下午能標約 50 張瑕疵遮罩（用 VisA PCB1：50 張拿來訓練，另外 50 張只拿來測試）</dd>
    <dt>限制與法規</dt><dd>Colab T4；不能用來路不明的紋理資料集</dd>
    <dt>為何現有工具不夠</dt><dd>L05 的自編碼器只給一張模糊的誤差圖，沒有清楚的邊界</dd>
  </dl>
</div>

<!--
★ 需求單（3 分）：「遮罩」（mask）＝和影像一樣大的黑白圖，白色的像素就是瑕疵。今天模型的輸出就是一張遮罩。
-->

---

<div class="eyebrow">學習目標</div>

# 今天結束時，你能夠……

1. **說明**為什麼跳接適合「切割」，卻會讓 L05 的重建式偵測失效
2. **建立** U-Net，對每個像素輸出瑕疵機率，並**預測**每一層的 shape
3. **合成**瑕疵（自帶遮罩），並說明為什麼還需要**少量真實遮罩**
4. **計算** IoU、Dice 與面積（mm²），並在**真實遮罩**上驗收

<!--
★ 目標（1 分）。不教：DRAEM 的完整雙網路（第 20 頁點名）、其他切割架構（DeepLab 等）。
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
  <img class="photo" src="/lab05-bent-error.png" alt="L05 自編碼器的誤差熱力圖：黑底上零星的亮點，散在零件邊緣與彎針附近" style="width:100%">
  <div class="shot-cap">上一堂 L05 的誤差熱力圖（另一片彎針板）：只有零星亮點，沒有邊界</div>
</div>
</div>

<div class="takeaway mt-4">維修站要的是綠線那樣「清楚的邊界」：有邊界，才量得出面積。</div>

<div class="src">影像與遮罩：VisA PCB1 第 087 張（Zou et al., 2022，CC BY 4.0，S1）；0.15% 為講師本機從遮罩計算；熱力圖：lab05 解答筆記本「熱力圖」格，Colab T4 實跑（L05 research/lab-runs.md）</div>

<!--
★ Frame（4 分）：先讓學員找刮痕——不放大幾乎看不到。這片板子是 HC-SR04 超音波模組（VisA PCB1 全部都是這個型號）。
右邊的熱力圖來自 L05 的 T4 實跑（測試集第 2 張不良品，針腳彎掉）。它確實在彎針附近最亮，但亮點零零星星、零件邊緣也在亮：沒有一條可以拿來量面積的邊界。
-->

---

<div class="eyebrow">00 · Frame · 今天的新工具</div>

# U-Net：同時記得「這是什麼」和「邊界在哪」

<div class="grid grid-cols-[1.35fr_1fr] gap-5 mt-0 items-center">
<div>
  <img class="photo" src="/unet-commons.png" alt="U-Net 架構圖：左邊往下經過 max pool，右邊往上經過 up sample，同一層之間有橫向箭頭連到 concat" style="width:100%;border:none">
</div>
<div style="font-size:16.5px">
  <div class="node node--primary" style="padding:6px 12px"><strong>左邊往下（Down conv ＋ max pool）</strong><small>每次高寬減半，一格看到的範圍越來越大 → 懂「這是針腳、那是探頭」（<strong>整體的意思</strong>），但精確的邊緣位置一路流失</small></div>
  <div class="node node--secondary mt-2" style="padding:6px 12px"><strong>右邊往上（up sample）</strong><small>放大回原尺寸，每個像素都要給答案</small></div>
  <div class="node node--warm mt-2" style="padding:6px 12px"><strong>橫向箭頭 → concat（跳接）</strong><small>往下同一層、還保有<strong>細節</strong>的特徵圖，直接接過來</small></div>
</div>
</div>

<div class="takeaway mt-2">往下的路負責「看懂」，橫向的跳接負責「畫準」：兩種資訊在 concat 會合，才畫得出清楚的邊界。</div>

<div class="src">圖：Mehrdad Yazdani, Example architecture of U-Net…, Wikimedia Commons, CC BY-SA 4.0（S7）；原始論文：Ronneberger et al., U-Net, 2015（S2）；回顧 DL pp.72–79</div>

<!--
★ 介紹 U-Net（5 分）：先接回上一頁的問題——維修站要邊界，L05 的 AE 給不出來。
看圖的順序：① 從左上往下走：每經過一次 max pool，圖變小一半，但每一格「看到」更大的範圍，所以越往下越懂「整體」（高階語意：這一區是探頭、這一區是針腳）。代價是位置變模糊：32×32 的一格對到原圖 8×8 個像素。
② 從下往右上走：up sample 一路放大回 256×256。
③ 重點在橫向箭頭：左邊每一層的輸出直接送到右邊同一層的 concat。左邊上層還是 256×256、邊緣清楚——這就是「細節」。
一句話：瓶頸說「這是什麼」，跳接說「邊界在哪」。DL 課看過這張 U 字形的圖（DL pp.72–79），今天看它為什麼適合切割。
-->

---

<div class="eyebrow">01 · Try（先用現成的）</div>

# 實際比一比：AE 的誤差圖 vs U-Net 的遮罩

<div class="grid grid-cols-[0.75fr_1.5fr] gap-5 mt-1 items-start">
<div>
  <img class="photo" src="/lab05-bent-error.png" alt="L05 自編碼器的誤差熱力圖：零星亮點散在零件邊緣與彎針附近" style="width:100%;max-height:220px;object-fit:contain">
  <div class="shot-cap"><strong>L05 自編碼器</strong>（T4，彎針板）：只靠瓶頸的「整體」重建，亮點散在每條邊緣</div>
</div>
<div>
  <img class="photo" src="/lab06-overlays.png" alt="三片沒看過的真實不良品：最好 IoU 0.81（焊點熔化圈得很準）、中間 0.29、最差 0（左邊探頭整片網子不見，沒圈到）" style="width:100%;border:none">
  <div class="shot-cap"><strong>L06 U-Net</strong>（T4，紅＝預測、綠＝真實）：最好 0.81、中間 0.29、最差 0——整片探頭網子不見，訓練裡幾乎沒有這種大面積缺件</div>
</div>
</div>

<div class="takeaway mt-2">整體＋細節：U-Net 直接畫出瑕疵範圍；50 張沒看過的真實不良品，平均 IoU 0.30。</div>

<div class="src">左：lab05「熱力圖」格；右：lab06 v2 第 5 步 overlays.png（皆 Colab T4，見各自 research/lab-runs.md）；VisA PCB1（S1）</div>


<!--
★ 示範（5 分）：接上一頁「整體＋細節」：左邊的 AE 只有整體，重建模糊，誤差到處都有；右邊的 U-Net 有跳接帶細節，可以直接畫出邊界。右邊用 lab06 解答筆記本的 overlays.png（最好、中間、最差各一張）。一定要給學員看「最差」那張，第 30 頁的風險就是在講它。
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
<div class="node"><strong>L05 自編碼器</strong><small>輸出＝重建的影像 &#91;B, 3, H, W&#93;；所有資訊都要擠過瓶頸</small></div>
<div class="node node--primary"><strong>L06 U-Net</strong><small>輸出＝每個像素一個分數 &#91;B, 1, H, W&#93;；細節走跳接，不必擠過瓶頸</small></div>
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
<div class="node node--warm"><strong>L05 的偵測靠「修不好」</strong><small>瑕疵擠不過瓶頸 → 重建圖沒有瑕疵 → 相減後瑕疵處誤差大</small></div>
<div class="node node--warm"><strong>AE 加了跳接會怎樣？</strong><small>瑕疵從跳接直接抄到輸出 → 重建得「太好」 → 誤差圖一片黑 → 漏檢</small></div>
</div>

<table class="mt-5" style="font-size:18px">
<thead><tr><th style="width:24%"></th><th>L05 自編碼器</th><th>L06 U-Net</th></tr></thead>
<tbody>
<tr><td>要學的答案</td><td>輸入本身（重建）</td><td>遮罩（哪些像素是瑕疵）</td></tr>
<tr><td>跳接</td><td>不能有（會照抄）</td><td>一定要有（邊界才準）</td></tr>
<tr><td>需要什麼資料</td><td>只要良品</td><td>要有遮罩 → 合成的＋少量真實的</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">同一個零件，用在不同的「答案」上，效果剛好相反：架構要配合你要模型學的東西。</div>

<!--
★ 關鍵對比（5 分）：這是 L05 第 23 頁「照抄」（identity shortcut）的延伸。問學員：「U-Net 也會照抄，為什麼它沒問題？」→ 因為 U-Net 要輸出的是遮罩，不是輸入本身；照抄輸入得不到遮罩。
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

<div class="muted mt-2" style="font-size:17px"><code>dim=1</code> 是通道那一維（L03 的 &#91;B, C, H, W&#93;）：接起來之後，下一層卷積自己決定要用多少「細節」、多少「整體」。</div>

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

<img class="photo mt-1" src="/synth-strip.png" alt="五格：真實良品、板子範圍、只留在板子上的隨機斑塊、另一片板子當紋理、貼上後的合成瑕疵" style="width:100%;max-height:165px;object-fit:contain;border:none">

<div class="grid grid-cols-5 gap-3 shot-cap text-center" style="margin-top:0"><div>良品</div><div>① 板子範圍</div><div>② 斑塊（只留板子上）</div><div>③ 紋理：另一片板子</div><div>④ 合成瑕疵</div></div>

<div class="grid grid-cols-3 gap-4 mt-1" style="font-size:16px">
<div class="node" style="padding:6px 12px"><strong>① ② 遮罩</strong><small>平滑的隨機雜訊取最亮的一小塊 → 不規則斑塊；真實瑕疵不會在桌面上，所以只留板子上的部分</small></div>
<div class="node" style="padding:6px 12px"><strong>③ 紋理</strong><small>從另一片良品剪一塊（轉向、平移、調亮暗）：像「零件長錯地方」，也不用來路不明的圖庫</small></div>
<div class="node node--warm" style="padding:6px 12px"><strong>④ 混合</strong><small>斑塊內：原圖和紋理混在一起；斑塊外不動</small></div>
</div>

<div class="takeaway mt-2">每一張合成瑕疵都「自帶正確答案」：遮罩是我們畫的，這部分不用人工標註。</div>

<div class="src">左一為 VisA PCB1 真實良品（S1）；其餘為 lab06 v2 第 2 步的輸出（Colab T4 實跑，random.seed(1)、SIZE 256；資料增強，不是模型輸出）；DRAEM：Zavrtanik et al., ICCV 2021（S4）</div>

<!--
★ 合成瑕疵（6 分）：DRAEM 原論文用 Perlin 雜訊做遮罩、DTD 紋理資料集當紋理；我們把紋理換成「另一片良品」，避開紋理資料集的授權問題（需求單的限制）。
第一版用程式產生的彩色雜訊當紋理、斑塊也會落在桌面上——下一頁會看到它在真實瑕疵上完全失敗。
一半的訓練圖不加瑕疵：模型也要學會回答「這片沒有」。
-->

---

<div class="eyebrow">03 · Adapt · 只靠合成，夠嗎？</div>

# 只用合成瑕疵訓練：真實瑕疵一個都沒圈到

<div class="grid grid-cols-[1.35fr_1fr] gap-5 mt-0 items-start">
<div>
  <img class="photo" src="/lab06-v1-overlays.png" alt="三片真實不良品的疊圖：綠線是人工標的瑕疵，模型沒有塗任何紅色，三張的 IoU 都是 0.00" style="width:100%;border:none">
  <div class="shot-cap">第一版的 T4 實跑：綠線＝真實瑕疵，紅色＝模型預測——一點紅都沒有</div>
</div>
<div style="font-size:16px">

<table style="font-size:16px">
<thead><tr><th></th><th>平均 IoU</th></tr></thead>
<tbody>
<tr><td>合成瑕疵上</td><td>0.800</td></tr>
<tr><td>真實瑕疵上（100 張）</td><td class="key">0.000</td></tr>
</tbody>
</table>

<div class="node node--warm mt-2" style="padding:6px 12px"><strong>兩個原因</strong><small>① 合成瑕疵是彩色雜訊、常落在桌面上，不像真的彎針、刮痕　② 沒瑕疵的圖也算 Dice：「什麼都不畫」就滿分，模型學會偷懶</small></div>
<div class="node node--primary mt-2" style="padding:6px 12px"><strong>今天的做法</strong><small>合成改得更像＋<strong>技術員標 50 張</strong>（40 訓練、10 驗證）；Dice 只算有瑕疵的圖；另外 50 張只測試</small></div>

</div>
</div>

<div class="takeaway mt-1">合成資料分數高，只代表模型學會了「我們的合成規則」；要在沒看過的真實遮罩上驗收。</div>

<div class="src">實跑：lab06 第一版解答筆記本，Colab T4，20 epochs、372 秒（research/lab-runs.md，2026-11-26 紀錄）；VisA PCB1（CC BY 4.0，S1）</div>

<!--
★ 失敗的實跑（4 分）：這是真的發生過的事，不是編的。講師第一次在 T4 上跑 lab06，合成瑕疵上 IoU 0.80，看起來很成功；換成真實不良品，100 張全部 0。
問學員：「如果只看合成資料的分數，你會不會就交差了？」——這就是為什麼驗收一定要用真實、沒看過的資料。
失敗有兩個原因（講師本機 CPU 實驗確認，research/lab-runs.md）：① 合成的彩色雜訊和真實瑕疵差太多——修好損失之後，只用這種合成資料，真實 IoU 還是接近 0；② 損失函數的陷阱：沒有瑕疵的圖也算 Dice，「什麼都不畫」就拿滿分，模型訓練到一半會突然變成什麼都不畫（下一頁的 Dice 會再提）。
改法：合成規則更像真的（只貼在板子上、用別片板子當紋理）；花一個下午標 50 張真實遮罩（工廠裡最有效：標 50 張比標 5,000 張便宜得多）；Dice 只算有瑕疵的圖；用 10 張驗證圖挑最好的 epoch。
-->

---

<div class="eyebrow">03 · Adapt（調整）· 損失函數 ①</div>

# BCE：每個像素都是一題「是不是瑕疵」的是非題

<div class="grid grid-cols-[1.05fr_1fr] gap-6 mt-1 items-start">
<div>

$$\text{BCE} = -\big[\, y \log p \;+\; (1-y) \log (1-p) \,\big]$$

<div style="font-size:17px" class="mt-1">

- <strong>y</strong>：正確答案（1＝瑕疵、0＝背景）
- <strong>p</strong>：模型說「是瑕疵」的機率（0–1）
- 兩項只會有一項起作用：答案是瑕疵看左項，答案是背景看右項
- 整張圖的 BCE ＝ 每個像素罰分的<strong>平均</strong>

</div>
</div>
<div>

<table style="font-size:17px">
<thead><tr><th>正確答案</th><th>模型猜 p</th><th>罰分</th></tr></thead>
<tbody>
<tr><td>瑕疵（y＝1）</td><td>0.9（猜對、有把握）</td><td>0.11</td></tr>
<tr><td>瑕疵（y＝1）</td><td>0.1（猜錯、很有把握）</td><td class="key">2.30</td></tr>
<tr><td>背景（y＝0）</td><td>0.1（猜對、有把握）</td><td>0.11</td></tr>
<tr><td>背景（y＝0）</td><td>0.9（猜錯、很有把握）</td><td class="key">2.30</td></tr>
</tbody>
</table>

</div>
</div>

<div class="takeaway mt-3">白話：猜對就少罰，<strong>猜錯又很有把握就重罰</strong>。DL 課的二元分類用的就是它，今天只是每個像素各算一次。</div>

<div class="src">罰分由公式直接計算（自然對數）：−log 0.9 ≈ 0.11、−log 0.1 ≈ 2.30</div>

<!--
★ BCE（4 分）：BCE（Binary Cross-Entropy，二元交叉熵）。不推導，只讀公式：y 是答案、p 是模型的信心。
帶學員念一次：「答案是瑕疵時，罰分是 −log p：p 越接近 1，罰越少」。表格右邊兩個 2.30 就是「猜錯又很有把握」。
DL 課的二元分類最後一層是 sigmoid＋binary_crossentropy，今天一模一樣，只是一張 256×256 的圖有 65,536 題。
-->

---

<div class="eyebrow">03 · Adapt · 損失函數 ②</div>

# 問題：全部猜「背景」，BCE 就很低

<div class="grid grid-cols-3 gap-5 mt-1" style="font-size:16px">
<div class="text-center"><div class="pxg"><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px px-d"></i><i class="px px-d"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px px-d"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i><i class="px"></i></div><div class="mt-1"><strong>正確答案</strong><br><span class="muted">100 個像素，3 個是瑕疵（橘）</span></div></div>
<div class="text-center"><div class="pxg"><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-bad"></i><i class="px px-bad"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-bad"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i></div><div class="mt-1"><strong>預測 A：全部猜背景</strong><br><span class="muted">每個像素都給 p＝0.03</span><br>像素正確率 97%<br>BCE <strong>0.135：已經很低</strong><br>Dice <span class="key">0：完全沒對到</span></div></div>
<div class="text-center"><div class="pxg"><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i><i class="px px-ok"></i></div><div class="mt-1"><strong>預測 B：圈對瑕疵</strong><br><span class="muted">瑕疵給 0.9、背景給 0.03</span><br>像素正確率 100%<br>BCE 0.033<br>Dice 1：完全對到</div></div>
</div>

<div class="muted text-center mt-1" style="font-size:15px"><span style="color:#16847a">綠</span>＝這格猜對、<span style="color:#c0392b">紅</span>＝這格猜錯；Dice 以「機率 &gt; 0.5 算瑕疵」計算</div>

<div class="takeaway mt-1">3 個紅格子罰得很重，但被 97 個綠格子平均掉了。所以再加上只看瑕疵的 Dice：<code>bce(logits, m) + (1 - dice(sigmoid(logits), m))</code></div>

<div class="src">教學示意（10×10），BCE 由公式計算。真實 PCB1 瑕疵平均只佔畫面 0.93%（research/lab-runs.md），比 3% 更少，平均掉得更嚴重</div>

<!--
★ 全猜背景（4 分）：讓學員先看中間那張：97 格綠、3 格紅，「準確率 97%」聽起來很厲害，但維修站要的那 3 格全錯。
BCE 0.135 是怎麼來的：3 個瑕疵格各罰 −log 0.03 ≈ 3.5，97 個背景格各罰 −log 0.97 ≈ 0.03，平均下來只有 0.135。
Dice 的算法在下一頁；這裡只要知道：它只看「瑕疵那幾格有沒有對到」，所以全猜背景會得到 0。
程式讀法：m＝真實遮罩、logits＝模型輸出（還沒變成機率）；BCEWithLogitsLoss 會自己做 sigmoid。
筆記本裡多一個細節：Dice 只算「有瑕疵的那幾張」。沒有瑕疵的圖如果也算 Dice，「什麼都不畫」就拿到滿分——第一版就是這樣訓練到一半突然什麼都不畫（第 13 頁）。
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

# DRAEM 的完整做法：兩個網路，先修好、再比較

<div class="flex items-center justify-center gap-2 mt-2" style="font-size:15.5px">
  <div class="text-center" style="width:12%"><img class="photo" src="/draem-synth.png" alt="合成瑕疵影像" style="width:100%"><div class="shot-cap">合成瑕疵影像</div></div>
  <span class="arrow">→</span>
  <div class="node node--secondary text-center" style="width:17%"><strong>重建網路</strong><small>編碼器－解碼器（像 L05 的 AE）</small></div>
  <span class="arrow">→</span>
  <div class="text-center" style="width:12%"><img class="photo" src="/draem-good.png" alt="修好的影像（目標是原本的良品）" style="width:100%"><div class="shot-cap">修好的圖<br>（目標＝原本的良品）</div></div>
  <span class="arrow">→</span>
  <div class="node node--warm text-center" style="width:15%"><strong>接起來</strong><small>原圖＋修好的圖<br>（6 通道）</small></div>
  <span class="arrow">→</span>
  <div class="node node--primary text-center" style="width:16%"><strong>判別網路</strong><small>U-Net：哪裡不一樣？</small></div>
  <span class="arrow">→</span>
  <div class="text-center" style="width:12%"><img class="photo" src="/draem-mask.png" alt="瑕疵遮罩" style="width:100%"><div class="shot-cap">瑕疵遮罩</div></div>
</div>

<div class="grid grid-cols-3 gap-4 mt-3" style="font-size:16px">
<div class="node"><strong>重建網路的損失</strong><small>修好的圖 vs 原本的良品（L2 ＋ SSIM）</small></div>
<div class="node"><strong>判別網路的損失</strong><small>預測遮罩 vs 合成時畫的遮罩（Focal loss，和 BCE 同一家族）</small></div>
<div class="node node--primary"><strong>今天的 Lab</strong><small>只做右半邊：U-Net 直接看原圖，沒有「修好的圖」可以比</small></div>
</div>

<div class="takeaway mt-3">DRAEM ＝ L05 的重建 ＋ 今天的 U-Net：判別網路看的是「原圖和修好的圖哪裡不同」，比只看原圖容易得多。</div>

<div class="src">依 Zavrtanik et al., DRAEM, ICCV 2021, Fig. 3 重繪（S4；原圖見 arxiv.org/abs/2108.07610，授權 CC BY-NC-SA 4.0，非商用，故不直接放）；縮圖為 lab06 的合成瑕疵（講師本機，示意，不是 DRAEM 的輸出）</div>

<!--
○ 選修（3 分）：對照論文 Fig. 3 講：左邊重建網路把瑕疵「修掉」（L05 的想法），中間把原圖和修好的圖在通道維度接起來（今天的 concat），右邊 U-Net 判斷兩張圖哪裡不同，輸出遮罩。
中間那張「修好的圖」是示意：我們放的是合成前的良品，也就是重建網路「應該」修成的樣子，不是真的模型輸出。
為什麼不直接放論文的圖：arXiv 上這篇的授權是 CC BY-NC-SA 4.0（非商用），和 L05 不用 MVTec AD 是同一個理由。講師上課可以直接開 arXiv 頁面給學員看原圖。
學員專題要更準時，可以把 L05 的 AE 輸出也接進 U-Net 當第 4–6 個通道。
-->

---

<div class="eyebrow">附錄 · 選修</div>

# U-Net 還會回來：擴散模型的去雜訊器

<div class="grid grid-cols-2 gap-6 mt-5" style="font-size:18px">
<div class="node"><strong>今天（L06）</strong><small>輸入：PCB 影像 → 輸出：每個像素「是不是瑕疵」</small></div>
<div class="node node--primary"><strong>L11 擴散模型</strong><small>輸入：加了雜訊的影像 → 輸出：每個像素「雜訊是多少」</small></div>
</div>

<div class="takeaway mt-6">輸入和輸出一樣大、要逐像素回答的工作，U-Net 都是常見選擇。</div>

<!--
○ 預告（2 分）：Stable Diffusion 的去雜訊網路就是一個（加了注意力的）U-Net。L11 的去雜訊 U-Net 結構和今天很像，但還要多一個輸入：現在是第幾步（timestep），所以不能原封不動搬過去。
-->

---

<div class="eyebrow">附錄 · 備用</div>

# 遮罩出現格子紋？棋盤格假影

<div class="grid grid-cols-2 gap-6 mt-4" style="font-size:18px">
<div class="node node--warm"><strong>現象</strong><small>預測遮罩或影像出現規則的格子狀紋路</small></div>
<div class="node"><strong>原因與解法</strong><small>ConvTranspose 的核大小不能被 stride 整除時，有些像素被「蓋」到兩次。主要解法：換成「先 Upsample 再卷積」（L05 第 12 頁的方法二）</small></div>
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

1. 用合成瑕疵＋50 張真實遮罩訓練的 U-Net，能圈出**沒看過的**真實瑕疵嗎？
2. 在真實遮罩上，IoU、Dice 是多少？
3. 面積估得準嗎（mm²）？

</div>
<div>

<img class="photo" src="/lab06-overlays.png" alt="最好、中間、最差三張疊圖：IoU 0.81、0.29、0.00" style="width:100%;border:none">
<div class="shot-cap">講師實跑（Colab T4，v2）：50 張沒看過的真實不良品，平均 IoU 0.304、Dice 0.411；11 張完全沒對到</div>

</div>
</div>

<div class="takeaway mt-3">驗收看的是<strong>沒看過的真實</strong>遮罩上的成績，不是合成瑕疵上的。</div>

<!--
★ Lab 開始（3 分）：先執行前兩格（下載與讀圖），等待時講下一頁。
備案：沒有 GPU → SIZE＝64、EPOCHS＝2，只能確認程式跑得通（本機 CPU 試跑 1 epoch 的真實 IoU 是 0，不能當成績）；斷線 → 講師課前在 T4 訓練並分享 unet_pcb1.pt（見 teaching-plan 課前清單），放到工作目錄會自動載入、跳過訓練。
-->

---

<div class="eyebrow">05 · Lab L2-2</div>

# Lab 2／7：筆記本拆成哪幾塊？

<div class="mt-3" style="font-size:17px"><strong>訓練（良品＋技術員標的 50 張）</strong></div>
<div class="flex items-center gap-2 mt-1" style="font-size:17px">
  <div class="node"><code>X_good</code>＋<code>X_lab</code><small>良品＋40 張真實遮罩</small></div><span class="arrow">→</span>
  <div class="node node--warm"><code>synth_defect</code><small class="nw">&#91;3,H,W&#93;＋&#91;1,H,W&#93;</small></div><span class="arrow">→</span>
  <div class="node node--primary"><code>UNet</code><small>logits &#91;B,1,H,W&#93;</small></div><span class="arrow">→</span>
  <div class="node"><code>loss_fn</code><small>BCE＋(1−Dice)</small></div>
</div>

<div class="mt-4" style="font-size:17px"><strong>驗收（另外 50 張，訓練沒看過）</strong></div>
<div class="flex items-center gap-2 mt-1" style="font-size:17px">
  <div class="node"><code>X_bad</code>、<code>M_bad</code><small>真實影像與遮罩</small></div><span class="arrow">→</span>
  <div class="node"><code>predict</code><small>機率 &gt; 0.5</small></div><span class="arrow">→</span>
  <div class="node"><code>iou_dice</code><small>每張一個分數</small></div><span class="arrow">→</span>
  <div class="node"><code>area_pred</code><small>mm²</small></div>
</div>

<div class="takeaway mt-4">五個 TODO：<code>synth_defect</code> 的混合、<code>UNet.forward</code> 往上三次、<code>loss_fn</code>、<code>iou_dice</code>、面積。</div>

<!--
★ 拆塊（3 分）：訓練和驗收用的資料完全分開：100 張真實不良品先洗牌，前 50 張（X_lab）進訓練，後 50 張（X_bad）從頭到尾沒進過訓練。
-->

---

<div class="eyebrow">05 · Lab L2-2</div>

# Lab 3／7：先檢查合成瑕疵，再訓練

<div class="grid grid-cols-[1.25fr_1fr] gap-5 mt-1 items-start">
<div>
  <img class="photo" src="/train-batch.png" alt="八張訓練樣本，紅線是遮罩邊界：上排是良品加合成瑕疵或沒有瑕疵，下排是技術員標的真實不良品（彎針、刮痕、焊錫）" style="width:100%;border:none">
  <div class="shot-cap">筆記本第 2 步的「批次網格」：上排合成、下排真實（Colab T4 實跑，SIZE 256）</div>
</div>
<div style="font-size:17px">

執行第 2 步的三格，回答：

1. 紅線（遮罩）和瑕疵的位置對得上嗎？
2. 上排有沒有斑塊落在桌面上？（應該沒有）
3. 合成瑕疵和下排真的瑕疵，哪裡像、哪裡不像？

<div class="node node--warm mt-2"><strong>為什麼要先看</strong><small>資料錯了（遮罩沒對齊、全部都有瑕疵），loss 照樣會降——但學到的是錯的東西</small></div>

</div>
</div>

<div class="takeaway mt-2">訓練之前先看資料：這是第 6／7 頁稽核的第一題。</div>

<!--
★ 檢查（4 分）：第 3 題沒有標準答案。合成的瑕疵是「別片板子的一塊貼錯地方」，真實的 PCB1 瑕疵是彎針、熔化、刮痕、缺件——這個落差就是為什麼還要 50 張真實遮罩，也是風險頁要講的。
-->

---

<div class="eyebrow">05 · Lab L2-2</div>

# Lab 4／7：Specify

<div style="font-size:18px" class="mt-2">

<strong>【目標】</strong>用良品＋合成瑕疵＋50 張真實遮罩訓練 U-Net，對每個像素輸出瑕疵機率<br>
<strong>【輸入與輸出】</strong>PCB 影像 <code>&#91;B, 3, 256, 256&#93;</code>（0–1）→ logits <code>&#91;B, 1, 256, 256&#93;</code><br>
<strong>【限制】</strong>測試用的 50 張真實不良品<strong>不能進訓練</strong>，也不能拿來挑 epoch（用 10 張驗證圖）；Colab T4；只存驗證 IoU 最好的檢查點<br>
<span class="muted" style="font-size:16px">為什麼：測試的遮罩一進訓練，驗收分數就不再代表「沒看過的瑕疵」</span><br>
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
③ loss_fn：BCEWithLogits ＋（1 − 有瑕疵那幾張的平均 Dice），Dice 用 sigmoid 後的機率<br>
④ iou_dice：每張的 IoU 與 Dice，分母為 0 時記 1.0<br>
⑤ 面積：像素數 × PX_MM2<br>
不要把測試用的 X_bad、M_bad 放進訓練。每一格說明每一行在做什麼。
</PromptBox>

<div class="steps mt-2" style="font-size:17px">
  <div><span class="num">1</span>20 epochs 約 13 分鐘（講師 T4 實測 777 秒，VRAM 峰值 3.41 GB）；等待時看驗證 IoU 有沒有往上</div>
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
<tr><td>合成資料對齊嗎？</td><td>看批次網格：紅線和瑕疵位置一樣</td><td>一樣；斑塊都在板子上</td></tr>
<tr><td>測試的遮罩有沒有混進訓練？</td><td>找 <code>M_bad</code> 出現在哪幾格</td><td>只在驗收格；訓練只用 <code>M_lab</code></td></tr>
<tr><td>Dice 用的是機率還是 logits？只算有瑕疵的圖嗎？</td><td>看 <code>loss_fn</code></td><td><code>sigmoid(logits[has])</code></td></tr>
<tr><td>合成 vs 真實差多少？</td><td>比較兩行 IoU</td><td>合成較高（T4：0.47 vs 0.30）</td></tr>
<tr><td>最差的一張錯在哪？</td><td>看最差那張疊圖</td><td>說出是哪一類瑕疵</td></tr>
<tr><td>面積合理嗎？</td><td>看三張的預測與真實 mm²</td><td>小瑕疵接近（T4：7.10 vs 6.78 mm²）；大片缺件會嚴重低估（0.63 vs 216.5）</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">一次只改一件事：例如合成瑕疵加一種「細長的線」（像刮痕），比較真實 IoU。</div>

<!--
★ 稽核（8 分）：最常見錯誤：Agent 把測試用的 50 張也丟進訓練（「資料多一點比較好」）→ 真實 IoU 變得很漂亮，但已經不能代表沒看過的瑕疵。
-->

---

<div class="eyebrow">05 · Lab L2-2 · Ship</div>

# Lab 7／7：Gradio 維修站工具

<div class="smallcode">

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

<div class="grid grid-cols-[1.35fr_1fr] gap-5 mt-2 items-start">
<div>
  <div class="shot"><img src="/lab06-gradio-ui.png" alt="lab06 的 Gradio 維修站工具：左邊上傳 PCB 影像，右邊顯示紅色預測瑕疵與面積" /></div>
  <div class="shot-cap">講師實跑截圖（Colab T4，尚未上傳圖片時的畫面）</div>
</div>
<div class="muted" style="font-size:16px">讀作：<code>tf</code> 縮成 256×256；機率 &gt; 0.5 的像素算瑕疵；像素數 × <code>PX_MM2</code>（一個像素幾 mm²）＝面積；<code>overlay</code> 把瑕疵像素塗紅。</div>
</div>

<div class="takeaway mt-2">L05 的檢測站回答「要不要送修」；今天的工具回答「修哪裡、多大」。</div>

<!--
★ Ship（4 分）：overlay() 在筆記本裡把預測的像素塗紅。可以和 L05 的檢測站放在同一個 gr.Blocks 裡（L04 提過）。
-->

---

<div class="eyebrow">06 · Measure & Risk（風險）</div>

# 風險：合成的瑕疵不等於真實的瑕疵

<div class="grid grid-cols-2 gap-6 mt-3" style="font-size:18px">
<div class="node node--warm"><strong>合成資料沒涵蓋的瑕疵，模型可能完全看不到</strong><small>第一版只用合成瑕疵：真實 IoU 0（第 13 頁）。標的 50 張也只涵蓋彎針、熔化、刮痕、缺件四類；產線上出現第五類，一樣可能漏掉</small></div>
<div class="node"><strong>一定要在沒看過的真實遮罩上驗收</strong><small>合成資料上的 IoU 只代表「模型學會了我們的合成規則」；拿訓練用過的遮罩來驗收也不算</small></div>
</div>

<table class="mt-4" style="font-size:18px">
<thead><tr><th></th><th>合成瑕疵上</th><th>沒看過的真實遮罩上</th></tr></thead>
<tbody>
<tr><td>第一版：只用合成（T4 實跑）</td><td>0.800</td><td>0.000（100 張）</td></tr>
<tr><td>今天的版本：合成＋40 張真實（T4 實跑）</td><td>0.468</td><td class="key">0.304（50 張；11 張是 0）</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">合成資料讓你「開始」，真實資料決定你「能不能上線」。</div>

<!--
★ 風險（4 分）：兩列都是 T4 實跑（research/lab-runs.md）。0.30 不是很高：50 張裡 11 張完全沒對到，最差的是整片探頭網子不見這種大面積缺件——訓練的 40 張裡幾乎沒有。真實 IoU 一定比合成低很多，照實說：這是誠實的基準線。上線前還要定期收集新的瑕疵、補標遮罩。
-->

---

<div class="eyebrow">總整理</div>

# 今天學到的概念鏈

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-4">
  <span class="chip">位置＋面積</span><span class="arrow">→</span>
  <span class="chip">跳接＝U-Net</span><span class="arrow">→</span>
  <span class="chip">AE 不能加跳接</span><span class="arrow">→</span>
  <span class="chip">合成＋少量真實遮罩</span><span class="arrow">→</span>
  <span class="chip">BCE＋Dice</span><span class="arrow">→</span>
  <span class="chip">IoU／Dice</span><span class="arrow">→</span>
  <span class="chip">mm²</span>
</div>

<div class="takeaway mt-6">跳接讓每個像素都能回答；合成資料讓標註少一點，少量真實遮罩讓模型看得到真的瑕疵；沒看過的真實遮罩才是驗收。</div>

<!--
★ 總整理（2 分）：請學員用一句話回答「為什麼 AE 不能加跳接，U-Net 卻一定要」。常見錯答：「U-Net 比較新」——重點是兩個模型要學的答案不同（重建 vs 遮罩）。
-->

---

<div class="eyebrow">隨堂檢核</div>

# 隨堂檢核 1／2（iPAS 題型）：點選答案

<Mcq id="quiz1.q1" :n="1" :answer="1"
  :options="['丟掉', '在通道維度接起來', '取平均', '只在訓練時使用']"
  :why="['丟掉就是一般的自編碼器，細節回不來。', '', 'U-Net 不取平均，而是把兩份特徵圖並排接起來。', '跳接是架構的一部分，推論時一樣要用。']"
  explain="編碼器那層的特徵圖和解碼器同尺寸的特徵圖用 torch.cat 在通道維度接起來，細節直接送到輸出端。">
U-Net 的跳接把往下那一層的特徵圖怎麼處理？
</Mcq>

<Mcq id="quiz1.q2" :n="2" :answer="2"
  :options="['會變慢', '參數太多', '瑕疵會被直接抄到輸出，誤差變小', '不能用 GPU']"
  :why="['跳接只多一次接合，速度不是問題。', '參數增加不多，也不是重點。', '', '跳接和 GPU 無關。']"
  explain="異常偵測靠「瑕疵重建不好」；有跳接，瑕疵從捷徑直接抄過去，重建誤差變小，就抓不到了。">
為什麼 L05 用來偵測瑕疵的自編碼器不能加跳接？
</Mcq>

<FillClear group="quiz1" corner />

<!--
★ 檢核 1／2（2 分）：學員自己點；點錯會出現「再想想」和那個選項錯在哪，可以再點一次。答案：1 B、2 C。
-->

---

<div class="eyebrow">隨堂檢核</div>

# 隨堂檢核 2／2（iPAS 題型）：點選答案

<Mcq id="quiz2.q3" :n="3" :answer="0"
  :options="['0.33', '0.25', '0.67', '0.5']"
  :why="['', '3 ÷ 12 是把兩邊直接相加當分母，重疊的 3 個被算了兩次。', 'IoU 不可能比「重疊 ÷ 預測」還大；分母是聯集，比任何一邊都大。', '3 ÷ 6 是重疊除以預測，只算了一邊；分母要用聯集。']"
  explain="聯集 ＝ 6 ＋ 6 − 3 ＝ 9，IoU ＝ 交集 ÷ 聯集 ＝ 3 ÷ 9 ≈ 0.33。">
預測 6 個像素、真實 6 個像素、重疊 3 個，IoU 是？
</Mcq>

<Mcq id="quiz2.q4" :n="4" :answer="3"
  :options="['讓訓練更快', 'BCE 不能微分', '為了算面積', '瑕疵像素太少，全部猜背景 BCE 也很低']"
  :why="['Dice 不會讓每一步變快。', 'BCE 可以微分，本來就是常用的損失。', '面積是預測完數像素就有，不需要放進損失。', '']"
  explain="瑕疵只佔很小一塊，全部猜背景 BCE 就很低；Dice 看重疊比例，全猜背景會得到最差的分數。">
為什麼損失要加 Dice？
</Mcq>

<FillClear group="quiz2" corner />

<!--
★ 檢核 2／2（2 分）。答案：3 A、4 D。
全部答案與理由：1 B、2 C、3 A（3 ÷ 9）、4 D。
-->

---
hostOnly: true
---

<div class="eyebrow">下一步</div>

# 下一堂 L07：一張 T4 跑得動 512px 嗎？

<div class="node node--primary mt-2">行銷科技組第四天要大量生成 512px 商品圖。直接在像素上生成太貴；下一堂把主角圖的瓶頸變成「一團機率雲」（VAE），也看 Stable Diffusion 怎麼先壓縮再生成。</div>

<!--
★ 只給講師的託管版看。
-->
