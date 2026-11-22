---
theme: default
title: 找出從沒看過的瑕疵
info: |
  生成式AI原理 · D2-1
  只用良品訓練卷積自編碼器，把重建誤差變成瑕疵分數與熱力圖；用門檻管理過殺與漏檢，用 AUROC 評估。
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
exportFilename: 05-ae-anomaly-detection
layout: center
class: cover
---

<div class="eyebrow">生成式AI原理 · D2-1</div>

# 找出從沒看過的瑕疵

<p class="subtitle">只看過良品的自編碼器，把「重建不好」變成瑕疵分數</p>

<div class="chain flex flex-nowrap items-center gap-2 mt-8">
  <span class="chip">只有良品</span><span class="arrow">→</span>
  <span class="chip">自編碼器</span><span class="arrow">→</span>
  <span class="chip">重建誤差</span><span class="arrow">→</span>
  <span class="chip">門檻</span><span class="arrow">→</span>
  <span class="chip">過殺／漏檢</span><span class="arrow">→</span>
  <span class="chip">檢測站</span>
</div>

<!--
★ 開場（2 分）：第二天整天都在品保部和行銷科技之間：同一張「編碼器→瓶頸→解碼器」的圖，每一堂改一個地方。今天是最基本的版本。
作業回顧（5 分，可放在開場前）：第一天作業第 3 題的 VRAM 表。
-->

---

<div class="eyebrow">00 · Frame（定義問題）</div>

# 品保部 A 線：過殺太多，新瑕疵又漏掉

<div class="ticket mt-2">
  <div class="ticket-head">【需求單 #D2-1】部門：製造品保部（A 線）<span>公司：曜嶼電子 <span class="fiction" style="color:#fff;border-color:#fff">虛構</span></span></div>
  <dl>
    <dt>問題</dt><dd>AOI 把太多好板判成不良（過殺），新型瑕疵卻會漏掉（漏檢）</dd>
    <dt>現況痛點</dt><dd>每天人工複判大量過殺板；新瑕疵每月出現，來不及標註</dd>
    <dt>成功指標（KPI）</dt><dd>漏檢率 ≤ 5% 的前提下，過殺率比現況低；附 AUROC</dd>
    <dt>可用資料</dt><dd>數百張良品；瑕疵很少、沒有新瑕疵（用公開資料集 VisA PCB1 代替）</dd>
    <dt>限制與法規</dt><dd>Colab T4；資料集授權（VisA：CC BY 4.0，待確認）</dd>
    <dt>為何現有工具不夠</dt><dd>CNN 分類器需要每一類瑕疵都有標註，沒看過的瑕疵分不出來</dd>
  </dl>
</div>

<!--
★ 需求單（3 分）：三個工廠用語：過殺（好的被判壞）、漏檢（壞的被放過）、AOI（自動光學檢測）。第 13 頁會對應到 FP、FN。
-->

---

<div class="eyebrow">學習目標</div>

# 今天結束時，你能夠……

1. **說明**為什麼監督式 CNN 抓不到沒看過的瑕疵，而只看過良品的自編碼器可以
2. **計算**重建誤差分數並**畫出**誤差熱力圖
3. **選擇**門檻（漏檢 ≤ 5%），並把過殺／漏檢對應到 FP／FN
4. **解讀** AUROC：不挑門檻的排序品質
5. **交付** Gradio 檢測站（第二天的成品）

<!--
★ 目標（1 分）。不教：U-Net 定位（D2-2）、VAE（D2-3）、擴散模型異常偵測（D3-4）；PatchCore 等方法只點名。
-->

---

<div class="eyebrow">00 · Frame</div>

# 為什麼 DL 課的 CNN 分類器做不到？

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-3">
<div>

<div class="flex items-center gap-2" style="font-size:18px">
  <div class="node">新型瑕疵的板子<small>訓練時從沒出現</small></div><span class="arrow">→</span>
  <div class="node">CNN 分類器<small>只認得「良品、刮傷、短路」</small></div><span class="arrow">→</span>
  <div class="node node--warm">硬塞進一類<small>常被判成「良品」</small></div>
</div>

</div>
<div style="font-size:18px">

- 分類器只能回答**看過的類別**
- 新瑕疵沒有標註，也來不及標
- 瑕疵樣本又少：資料嚴重不平衡

</div>
</div>

<div class="takeaway mt-6">問題不在 CNN 不夠好，而是「沒看過的類別」根本不在它的選項裡。</div>

<div class="src">回顧：DL pp.38–55（CNN 分類）</div>

<!--
★ Frame（4 分）：請學員回想 D1-3 的 CIFAR-10：如果輸入一張「船」以外的新東西（例如蛋糕），分類器還是會從 10 類裡挑一個。
-->

---

<div class="eyebrow">00 · Frame</div>

# 換個問法：只學「正常長什麼樣」

<div class="grid grid-cols-2 gap-8 mt-4" style="font-size:19px">
<div class="node"><strong>舊問法（分類）</strong><small>「這是哪一種瑕疵？」→ 需要每一種瑕疵的樣本</small></div>
<div class="node node--primary"><strong>新問法（異常偵測）</strong><small>「這片板子和平常的良品像不像？」→ 只需要良品</small></div>
</div>

<div class="node node--secondary mt-5" style="font-size:18px"><strong>類比：老師傅</strong><small>每天看幾千片好板，看久了，任何「怪怪的」地方一眼就看出來——就算那種瑕疵他從沒見過</small></div>

<div class="takeaway mt-4">生成模型學的是「良品通常長什麼樣」（D1-1 的 p_data），不像的就是可疑。</div>

<!--
★ 換問法（3 分）：連回 D1-1 第 8 頁的分布圖：良品是黑點，模型學出藍色區域；落在區域外的板子就可疑。
-->

---

<div class="eyebrow">01 · Try（先用現成的）</div>

# 講師訓練好的自編碼器：熱力圖亮在瑕疵上

<div class="grid grid-cols-3 gap-4 mt-2">
<div><div class="placeholder" style="height:190px">輸入（不良品）<small>VisA PCB1，講師實跑後替換</small></div></div>
<div><div class="placeholder" style="height:190px">重建<small>講師實跑後替換</small></div></div>
<div><div class="placeholder" style="height:190px">誤差熱力圖<small>講師實跑後替換</small></div></div>
</div>

<div class="takeaway mt-4">先看結果：重建圖「修好」了瑕疵，所以輸入和重建的差，剛好落在瑕疵上。</div>

<div class="src">資料：VisA（Zou et al., 2022），CC BY 4.0（待確認）；模型為講師以 lab05 訓練的檢查點</div>

<!--
★ 示範（5 分）：用 lab05 解答筆記本的「熱力圖」格（或講師檢查點）。如果某一張熱力圖沒亮在瑕疵上，也直接給學員看——這是誠實的基準線，第 19 頁會說明原因。
-->

---

<div class="eyebrow">02 · Open（打開黑盒子）· 今天的主角圖</div>

# 自編碼器：壓扁，再還原

<div class="flex items-center justify-center gap-2 mt-4" style="font-size:18px">
  <div class="node" style="width:16%">輸入 x<small>[B, 3, 128, 128]</small></div><span class="arrow">→</span>
  <div class="node node--primary" style="width:18%"><strong>Encoder</strong><small>每層高寬減半</small></div><span class="arrow">→</span>
  <div class="node node--warm" style="width:16%"><strong>瓶頸 z</strong><small>[B, 128, 8, 8]</small></div><span class="arrow">→</span>
  <div class="node node--secondary" style="width:18%"><strong>Decoder</strong><small>每層高寬加倍</small></div><span class="arrow">→</span>
  <div class="node" style="width:16%">重建 x̂<small>[B, 3, 128, 128]</small></div>
</div>

<div class="grid grid-cols-2 gap-6 mt-6" style="font-size:18px">
<div>

- **瓶頸**（bottleneck）：z 比 x 小約 6 倍，放不下每個細節
- **訓練目標**：讓 x̂ 和 x 越像越好（MSE）

</div>
<div class="node node--dashed"><strong>這張圖整天都會出現</strong><small>D2-2 加跳接（U-Net）、D2-3 瓶頸變成機率（VAE）、D2-4 瓶頸變成編碼簿裡的編號（VQ-VAE）</small></div>
</div>

<div class="takeaway mt-4">瓶頸逼模型只記住「良品共同的樣子」，記不住個別的怪東西。</div>

<div class="src">回顧：DL pp.72–79（AE、U-Net、VAE 概念）——今天直接看程式與用途</div>

<!--
★ 主角圖（6 分）：DL 課已經介紹過 AE 的概念（DL pp.72–79），一句帶過，不重講（R-C11）。重點放在 shape：3×128×128 ＝ 49152 個數字 → 128×8×8 ＝ 8192 個數字，約 1/6。
x̂ 讀作「x hat」：模型重建出來的 x。
-->

---

<div class="eyebrow">02 · Open · 為什麼抓得到</div>

# 只學過良品，所以會把瑕疵「修掉」

<div class="flex items-center justify-center gap-3 mt-5" style="font-size:18px">
  <div class="node" style="width:26%"><strong>① 輸入</strong><small>有一道刮痕的板子</small></div><span class="arrow">→</span>
  <div class="node node--secondary" style="width:26%"><strong>② 重建</strong><small>模型沒看過刮痕，畫出「正常」的那一塊</small></div><span class="arrow">→</span>
  <div class="node node--warm" style="width:26%"><strong>③ 相減</strong><small>|x − x̂| 只在刮痕處很大</small></div>
</div>

<table class="mt-6" style="font-size:18px">
<thead><tr><th style="width:24%"></th><th>良品</th><th>不良品</th></tr></thead>
<tbody>
<tr><td>重建得像嗎？</td><td>像（看過很多）</td><td>瑕疵處不像</td></tr>
<tr><td>誤差</td><td>小</td><td>瑕疵處大</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">誤差大＝「這裡和模型學到的良品不一樣」。</div>

<!--
★ 機制（5 分）：這頁是整堂的核心。用「修圖」比喻：模型是只會修成良品樣子的修圖師。
常見誤解：「AE 是用來抓瑕疵的模型」——不對，AE 只會重建；抓瑕疵的是我們拿「重建誤差」去比。
-->

---

<div class="eyebrow">02 · Open · 解碼器</div>

# 解碼器怎麼放大？ConvTranspose 與 Upsample

<div class="grid grid-cols-2 gap-5 mt-1">
<div>

```python
# 方法一：轉置卷積（本 Lab 用）
nn.ConvTranspose2d(128, 64, 4, stride=2, padding=1)
# [B, 128, 16, 16] → [B, 64, 32, 32]
```

<div class="muted" style="font-size:17px">讀作：「學出來的放大」——放大的方式也是參數</div>

</div>
<div>

```python
# 方法二：先放大，再卷積
nn.Upsample(scale_factor=2)
nn.Conv2d(128, 64, 3, padding=1)
# [B, 128, 16, 16] → [B, 64, 32, 32]
```

<div class="muted" style="font-size:17px">讀作：「固定的放大＋學出來的修飾」</div>

</div>
</div>

<div class="takeaway mt-4">兩種都把高寬加倍；DL 課用的是 UpSampling，今天的 Lab 用 ConvTranspose。</div>

<div class="src">回顧：DL p.74（UpSampling）；PyTorch 文件（S2）</div>

<!--
★ 解碼器（4 分）：ConvTranspose 有時會出現棋盤狀的假影（checkerboard），D2-2 的附錄會提到。這裡只要知道兩種都能把 16 變 32。
-->

---

<div class="eyebrow">02 · Open · 誤差圖</div>

# 重建誤差熱力圖：每個像素一個誤差

<div class="grid grid-cols-[1.15fr_1fr] gap-6 mt-1">
<div>

```python
def anomaly_map(x):
    x_hat = model(x)
    return ((x - x_hat) ** 2).mean(dim=1)
    # [B, 3, 128, 128] → [B, 128, 128]

def score(x):
    m = anomaly_map(x).flatten(1)      # [B, 16384]
    k = int(m.shape[1] * 0.01)         # 最大的 1%
    return m.topk(k, dim=1).values.mean(dim=1)
```

</div>
<div style="font-size:18px">

- **誤差圖**：每個像素 (x − x̂)²，三個顏色通道取平均
- **分數**：誤差最大的 1% 像素的平均
- 為什麼不用整張平均？瑕疵很小，會被大片正常區域稀釋

</div>
</div>

<div class="takeaway mt-3">誤差圖告訴我們「在哪裡」，分數告訴我們「這片板子有多可疑」。</div>

<!--
★ 誤差圖（6 分）：mean(dim=1) 讀作「沿著第 1 維（通道）取平均」。topk 讀作「拿最大的 k 個」。
這個分數設計是本 Lab 的選擇，不是標準答案；SSIM 等替代方法見第 18 頁。
-->

---

<div class="eyebrow">03 · Measure（量化驗收）· 分數</div>

# 分數＝有多「不典型」

<div class="grid grid-cols-[1.25fr_1fr] gap-6 mt-1 items-center">
<div>

<svg viewBox="0 0 460 230" style="width:100%">
  <defs><marker id="ax5" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#4b5563"/></marker></defs>
  <line x1="30" y1="190" x2="440" y2="190" stroke="#4b5563" stroke-width="1.5" marker-end="url(#ax5)"/>
  <text x="380" y="215" style="font-size:16px" fill="#4b5563">分數 →</text>
  <path d="M40,190 C80,190 90,60 140,60 C190,60 200,190 260,190 Z" fill="#e7f5f2" stroke="#16847a" stroke-width="2"/>
  <path d="M200,190 C250,190 270,110 310,110 C350,110 370,190 420,190 Z" fill="#fff2e3" stroke="#b85c20" stroke-width="2" stroke-dasharray="6 4"/>
  <text x="100" y="50" style="font-size:17px" fill="#16847a">良品</text>
  <text x="290" y="100" style="font-size:17px" fill="#b85c20">不良品</text>
  <text x="205" y="180" style="font-size:14px" fill="#4b5563">重疊</text>
</svg>

</div>
<div style="font-size:18px">

- 分數低：和學過的良品很像（**典型**）
- 分數高：和良品不像（**不典型**）
- 兩群會**重疊**：有些良品長得怪、有些瑕疵很小

</div>
</div>

<div class="takeaway mt-2">分數是「像不像良品」的反向量尺；這就是 likelihood（概似）的直覺：越典型，機率越高。</div>

<div class="src">教學示意圖，不是實際分布；Lab 第 4 步會畫出真的直方圖</div>

<!--
★ 典型性（5 分）：likelihood 讀作「概似」：模型認為這筆資料出現的可能性。AE 沒有直接算機率，但重建誤差扮演同樣的角色。D2-3 的 VAE 會更接近「機率」。
-->

---

<div class="eyebrow">04 · Adapt（調成我們的）· 門檻</div>

# 門檻：一條線決定判良或判不良

<div class="grid grid-cols-2 gap-6 mt-2">
<div class="node"><strong>線往左移（門檻低）</strong><small>更多板子被判不良 → 漏檢少，但過殺多（好板也被攔下）</small></div>
<div class="node"><strong>線往右移（門檻高）</strong><small>更少板子被判不良 → 過殺少，但漏檢多（瑕疵被放過）</small></div>
</div>

<div class="node node--primary mt-5" style="font-size:18px"><strong>今天的規則</strong><small>在驗證集上選一條線，讓不良品最多漏掉 5%；再到測試集看過殺是多少</small></div>

<div class="takeaway mt-4">門檻不是模型學出來的，是<strong>商業決定</strong>：漏檢和過殺哪個比較貴？</div>

<!--
★ 門檻（5 分）：重疊區域一定存在，所以不可能同時零過殺、零漏檢。下一頁把這兩個工廠用語對到 ML 課的混淆矩陣。
-->

---

<div class="eyebrow">04 · Measure · 工廠用語</div>

# 過殺＝FP，漏檢＝FN

<table class="mt-2" style="font-size:19px">
<thead><tr><th style="width:24%"></th><th>模型判「不良」</th><th>模型判「良品」</th></tr></thead>
<tbody>
<tr><td><strong>真的不良</strong></td><td>✓ 抓到（TP）</td><td class="key">✗ <strong>漏檢</strong>（FN）：瑕疵出貨</td></tr>
<tr><td><strong>真的良品</strong></td><td class="key">✗ <strong>過殺</strong>（FP）：好板被攔</td><td>✓ 放行（TN）</td></tr>
</tbody>
</table>

<div class="grid grid-cols-2 gap-6 mt-4" style="font-size:18px">
<div>過殺率 ＝ 被判不良的良品 ÷ 全部良品</div>
<div>漏檢率 ＝ 被判良品的不良品 ÷ 全部不良品</div>
</div>

<div class="takeaway mt-4">「不良」是正類：漏掉正類是 FN，誤報正類是 FP。</div>

<div class="src">回顧：ML pp.9–10（混淆矩陣、precision／recall）</div>

<!--
★ 對應（4 分）：漏檢率 ＝ 1 − recall。工廠很少說 recall，說「漏檢」。之後的投影片和筆記本都用工廠用語。
-->

---

<div class="eyebrow">04 · Measure · 練習</div>

# 練習：移動門檻，算過殺與漏檢

<div class="muted" style="font-size:16px">教學用數字。分數 &gt; 門檻 → 判不良。<br>良品（10 片）：0.12　0.18　0.21　0.25　0.28　0.31　0.33　0.38　0.42　0.52<br>不良（5 片）：0.36　0.47　0.58　0.66　0.81</div>

<div class="muted" style="font-size:16px"><strong>照著做</strong>（門檻不同）：門檻 0.50 → 良品只有 0.52 超過 → 過殺 1 片；不良 0.36、0.47 沒超過 → 漏檢 2 片</div>

<table class="fill tight vlines mt-1">
<thead><tr><th style="width:16%">門檻</th><th>過殺（幾片／10）</th><th>漏檢（幾片／5）</th><th>品保部會選嗎？為什麼</th></tr></thead>
<tbody>
<tr><td>0.30</td><td class="blank"><FillIn id="thr.30-ok" hint="例：數一數良品……" /></td><td class="blank"><FillIn id="thr.30-es" /></td><td class="blank"><FillIn id="thr.30-why" /></td></tr>
<tr><td>0.45</td><td class="blank"><FillIn id="thr.45-ok" /></td><td class="blank"><FillIn id="thr.45-es" /></td><td class="blank"><FillIn id="thr.45-why" /></td></tr>
<tr><td>0.60</td><td class="blank"><FillIn id="thr.60-ok" /></td><td class="blank"><FillIn id="thr.60-es" /></td><td class="blank"><FillIn id="thr.60-why" hint="例：漏檢太……" /></td></tr>
</tbody>
</table>

<FillClear group="thr" />

<!--
★ 練習（8 分）：手算，不用程式。目的：自己發現「漏檢 ≤ 5%」在這組數字裡只有門檻 0.30 做得到，代價是一半的良品被過殺——所以需要更好的模型（AUROC 更高）。
投影片上的示範（照著做）：門檻 0.50 → 良品只有 0.52 超過 → 過殺 1 片；不良 0.36、0.47 沒超過 → 漏檢 2 片。
-->

---
hostOnly: true
---

<div class="eyebrow">04 · Measure · 練習解答</div>

# 練習解答：要漏檢少，就得付出過殺

<table class="vlines" style="font-size:18px">
<thead><tr><th style="width:16%">門檻</th><th>過殺</th><th>漏檢</th><th>說明</th></tr></thead>
<tbody>
<tr><td>0.30</td><td>5／10（50%）</td><td>0／5（0%）</td><td>唯一符合漏檢 ≤ 5%，但一半好板被攔</td></tr>
<tr><td>0.45</td><td>1／10（10%）</td><td>1／5（20%）</td><td>平衡，但漏檢超標</td></tr>
<tr><td>0.60</td><td>0／10（0%）</td><td>3／5（60%）</td><td>沒有過殺，但大部分瑕疵出貨</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">怎麼判斷：逐一數「良品 &gt; 門檻」與「不良 ≤ 門檻」。加分：這組數字的 AUROC ＝ 46／50 ＝ 0.92（下一頁）。</div>

<!--
★ 解答（2 分）：AUROC 計算：5×10＝50 組（不良, 良品），不良分數較高的有 7＋9＋10＋10＋10＝46 組。
-->

---

<div class="eyebrow">04 · Measure · AUROC</div>

# AUROC：不挑門檻，看排序好不好

<div class="grid grid-cols-[1fr_1.2fr] gap-6 mt-2 items-center">
<div>

<svg viewBox="0 0 260 240" style="width:100%;max-height:285px">
  <defs><marker id="ax6" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#4b5563"/></marker></defs>
  <line x1="30" y1="210" x2="240" y2="210" stroke="#4b5563" stroke-width="1.5" marker-end="url(#ax6)"/>
  <line x1="30" y1="210" x2="30" y2="15" stroke="#4b5563" stroke-width="1.5" marker-end="url(#ax6)"/>
  <line x1="30" y1="210" x2="220" y2="25" stroke="#b8b8b8" stroke-width="1.5" stroke-dasharray="5 4"/>
  <path d="M30,210 L30,120 L60,80 L100,50 L160,35 L220,25" fill="none" stroke="#2457c5" stroke-width="3"/>
  <text x="110" y="232" style="font-size:14px" fill="#4b5563">過殺率（FP 率）</text>
  <text x="36" y="22" style="font-size:14px" fill="#4b5563">抓到率（1 − 漏檢率）</text>
  <text x="130" y="150" style="font-size:14px" fill="#4b5563">亂猜＝0.5</text>
</svg>

</div>
<div style="font-size:18px">

- 每個門檻畫一點，連成 ROC 曲線
- **AUROC**＝曲線下的面積
- 白話：「隨機抽一片不良、一片良品，不良分數比較高的機率」
- 0.5 ＝ 亂猜；1.0 ＝ 完美排序

```python
roc_auc_score(y, scores)   # sklearn
```

</div>
</div>

<div class="takeaway mt-2">AUROC 評估「模型」；門檻上的過殺／漏檢評估「上線的決定」。兩個都要報。</div>

<div class="src">ROC 曲線為教學示意；sklearn 文件（S3）；回顧 ML pp.9–10</div>

<!--
★ AUROC（6 分）：用上一頁的教學數字：50 組裡 46 組排對 → 0.92。AUROC 高不保證「漏檢 ≤ 5%」時過殺低，所以品保部還要門檻上的數字。
-->

---

<div class="eyebrow">04 · Measure · 業界基準</div>

# 我們的 AE 是基準線；產線用更強的方法

<div class="grid grid-cols-2 gap-6 mt-4" style="font-size:18px">
<div class="node"><strong>PatchCore</strong><small>用預訓練 CNN 的特徵，記住良品的「小區塊特徵庫」，比對最近的距離</small></div>
<div class="node"><strong>EfficientAD</strong><small>老師－學生網路＋小型自編碼器，強調速度（每片毫秒等級）</small></div>
</div>

<div class="takeaway mt-6">先用簡單的 AE 建立基準線與評估流程（分數、門檻、AUROC），換更強的方法時流程不變。</div>

<div class="src">Roth et al., PatchCore (CVPR 2022)；Batzner et al., EfficientAD (WACV 2024)（S4、S5，待確認）</div>

<!--
★ 基準（3 分）：只點名，不實作。重點：今天建立的「評估流程」才是可以帶走的東西。學員如果期末專題做異常偵測，可以用 anomalib（下一頁）。
-->

---

<div class="eyebrow">04 · Adapt · 選修</div>

# 換一把尺：SSIM vs MSE；現成工具 anomalib

<table style="font-size:18px">
<thead><tr><th style="width:18%"></th><th>MSE</th><th>SSIM（結構相似度）</th></tr></thead>
<tbody>
<tr><td>比什麼</td><td>每個像素的數值差</td><td>局部的亮度、對比、紋理結構</td></tr>
<tr><td>對什麼敏感</td><td>亮度整體偏移也會變大</td><td>形狀、邊緣的改變</td></tr>
</tbody>
</table>

<div class="node mt-4" style="font-size:18px"><strong>anomalib</strong><small>開源的異常偵測函式庫，內建 PatchCore、EfficientAD 等方法與 VisA 資料載入</small></div>

<div class="takeaway mt-4">誤差的「尺」也是設計選擇；換尺之後，用同一套 AUROC 與門檻流程比較。</div>

<!--
○ 選修（3 分）：延伸練習：把 anomaly_map 換成 1 − SSIM（可用 torchmetrics 或 pytorch-msssim，套件待確認），比較 AUROC。
-->

---

<div class="eyebrow">附錄 · 備用</div>

# 自編碼器有時連瑕疵也重建得很好

<div class="grid grid-cols-2 gap-6 mt-4" style="font-size:18px">
<div class="node node--warm"><strong>原因：容量太大</strong><small>瓶頸不夠窄，模型學會「照抄輸入」（identity shortcut），瑕疵也一起抄過去</small></div>
<div class="node"><strong>後果</strong><small>瑕疵處誤差不大 → 分數不夠高 → 漏檢</small></div>
</div>

<div class="takeaway mt-6">瓶頸太寬會照抄、太窄會模糊；D2-2 的跳接會讓照抄更嚴重，D3-4 用擴散模型換個做法。</div>

<!--
△ 備用（2 分）：學員發現熱力圖沒亮在瑕疵上時用。可以讓學員把 encoder 少一層 down（瓶頸變 16×16）比較 AUROC。
-->

---

<div class="eyebrow">05 · Lab L2-1</div>

# Lab 1／7：我們要做出什麼？

<div class="grid grid-cols-2 gap-6 mt-2" style="font-size:19px">
<div>

**打開筆記本**：`materials/lab05-ae-anomaly.ipynb` → Open in Colab<br>
執行階段：**T4 GPU**<br>
資料：VisA PCB1（筆記本下載；或講師提供的資料夾）

1. 重建圖會不會把瑕疵「修掉」？
2. 良品和不良品的分數分得開嗎？
3. 漏檢 ≤ 5% 時，要攔下多少好板？

</div>
<div>

<div class="placeholder" style="height:250px">目標：熱力圖、分數直方圖、AUROC、過殺／漏檢表<small>講師實跑後換成真實輸出</small></div>

</div>
</div>

<div class="takeaway mt-3">這就是四個檢查點的 ① 目標。</div>

<!--
★ Lab 開始（3 分）：VisA 整包很大，下載時間待實測；建議講師課前把 PCB1 放到共用雲端硬碟，學員改 PCB1_DIR。
備案：沒有 GPU → SIZE＝64、EPOCHS＝3；斷線 → 把講師的 ae_pcb1.pt 放到工作目錄，會自動載入。
-->

---

<div class="eyebrow">05 · Lab L2-1</div>

# Lab 2／7：模型拆成哪幾塊？

<div class="mt-3" style="font-size:17px"><strong>訓練</strong></div>
<div class="flex items-center gap-2 mt-1" style="font-size:17px">
  <div class="node"><code>PCBDataset</code><small>[B, 3, 128, 128]</small></div><span class="arrow">→</span>
  <div class="node node--primary"><code>encoder</code><small>4 次 down</small></div><span class="arrow">→</span>
  <div class="node node--warm"><code>z</code><small>瓶頸</small></div><span class="arrow">→</span>
  <div class="node node--secondary"><code>decoder</code><small>4 次放大</small></div><span class="arrow">→</span>
  <div class="node">x̂<small>MSE(x̂, x)</small></div>
</div>

<div class="mt-4" style="font-size:17px"><strong>評估與上線</strong></div>
<div class="flex items-center gap-2 mt-1" style="font-size:17px">
  <div class="node"><code>anomaly_map</code><small>誤差圖 [B, H, W]</small></div><span class="arrow">→</span>
  <div class="node"><code>score</code><small>每片一個分數</small></div><span class="arrow">→</span>
  <div class="node node--primary"><code>thr</code><small>判良／判不良</small></div>
</div>


<div class="takeaway mt-4">名稱和筆記本一樣：<code>PCBDataset</code>、<code>ConvAE.encoder</code>、<code>.decoder</code>、<code>anomaly_map</code>、<code>score</code>、<code>thr</code>。</div>

<!--
★ 拆塊（3 分）：先指出訓練和評估用的部分不同。下一頁填 shape。
-->

---

<div class="eyebrow">05 · Lab L2-1 · 練習</div>

# 練習：每一塊的輸入與輸出

<div class="muted" style="font-size:17px">不用 AI。<code>down</code>：卷積 stride 2，高寬減半；<code>up</code>：ConvTranspose stride 2，高寬加倍。B ＝ 32</div>

<table class="fill tight vlines mt-1">
<thead><tr><th style="width:26%">塊</th><th>輸入 shape</th><th>輸出 shape</th><th>做什麼（一句話）</th></tr></thead>
<tbody>
<tr><td><code>encoder</code></td><td>[32, 3, 128, 128]</td><td class="blank"><FillIn id="ae.enc-out" hint="例：通道 128、高寬……" /></td><td>壓成瓶頸</td></tr>
<tr><td><code>decoder</code></td><td class="blank"><FillIn id="ae.dec-in" /></td><td class="blank"><FillIn id="ae.dec-out" /></td><td class="blank"><FillIn id="ae.dec-do" /></td></tr>
<tr><td><code>anomaly_map</code></td><td class="blank"><FillIn id="ae.map-in" /></td><td class="blank"><FillIn id="ae.map-out" hint="例：少了一維……" /></td><td class="blank"><FillIn id="ae.map-do" /></td></tr>
<tr><td><code>score</code></td><td class="blank"><FillIn id="ae.score-in" /></td><td class="blank"><FillIn id="ae.score-out" /></td><td class="blank"><FillIn id="ae.score-do" /></td></tr>
</tbody>
</table>

<FillClear group="ae" />

<!--
★ 無 AI 檢核點（8 分）：第一列的「輸入」和「做什麼」已填好當示範。不收回。下一頁是解答。
-->

---
hostOnly: true
---

<div class="eyebrow">05 · Lab L2-1 · 練習解答</div>

# 練習解答：每一塊的輸入與輸出

<table class="vlines" style="font-size:18px">
<thead><tr><th style="width:24%">塊</th><th>輸入</th><th>輸出</th><th>做什麼</th></tr></thead>
<tbody>
<tr><td><code>encoder</code></td><td>[32, 3, 128, 128]</td><td>[32, 128, 8, 8]</td><td>128→64→32→16→8，壓成瓶頸</td></tr>
<tr><td><code>decoder</code></td><td>[32, 128, 8, 8]</td><td>[32, 3, 128, 128]</td><td>還原成原大小（Sigmoid → 0–1）</td></tr>
<tr><td><code>anomaly_map</code></td><td>[32, 3, 128, 128]</td><td>[32, 128, 128]</td><td>每像素平方誤差，通道平均</td></tr>
<tr><td><code>score</code></td><td>[32, 3, 128, 128]</td><td>[32]</td><td>每片板子一個分數</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">怎麼對答案：筆記本「模型」格印出 x、z、x̂ 的 shape（本機煙霧測試已確認 z ＝ [B, 128, 8, 8]）。</div>

<!--
★ 解答（2 分）：本機 CPU 煙霧測試（research/lab-runs.md）印出 z (8, 128, 8, 8)，壓縮成 1/6。
-->

---

<div class="eyebrow">05 · Lab L2-1</div>

# Lab 4／7：Specify

<div style="font-size:18px" class="mt-2">

<strong>【目標】</strong>只用良品訓練卷積自編碼器，輸出熱力圖、分數、AUROC 與門檻<br>
<strong>【輸入與輸出】</strong>PCB 影像 [B, 3, 128, 128]（0–1）→ 重建 [B, 3, 128, 128]；分數 [B]<br>
<strong>【限制】</strong>訓練集<strong>只有良品</strong>；門檻只能用驗證集選；Colab T4；每個 epoch 存檢查點<br>
<strong>【驗收】</strong>① loss 持續下降　② 良品的重建圖看得出電路　③ 驗證集不良品平均分數高於良品　④ 測試集回報 AUROC、門檻下的過殺與漏檢

</div>

<!--
★ Specify（3 分）：限制裡的「只用驗證集選門檻」很重要：用測試集選門檻等於偷看答案，回報的數字會太漂亮。
-->

---

<div class="eyebrow">05 · Lab L2-1</div>

# Lab 5／7：Generate → Execute

<PromptBox>
這是 PyTorch 筆記本，請只填四個 # TODO：<br>
① ConvAE 的 encoder（四次 down：3→32→64→128→128）與 decoder（三次 up 再接 ConvTranspose2d(32,3) 與 Sigmoid）<br>
② 訓練迴圈的五行（loss ＝ MSE(x_hat, xb)）<br>
③ anomaly_map：每像素平方誤差、通道平均，回傳 [B,H,W]<br>
④ 門檻：驗證集不良品分數排序，最多允許 5% 漏檢<br>
不要用測試集選門檻。每一格說明每一行在做什麼。
</PromptBox>

<div class="steps mt-2" style="font-size:17px">
  <div><span class="num">1</span>訓練迴圈和 D1-3 一樣，只換模型和損失（x 同時是輸入和答案）</div>
  <div><span class="num">2</span>訓練約數分鐘（待實測）；等待時看重建網格</div>
  <div><span class="num">3</span>沒有 Agent 額度：照第 10 頁、D1-3 的五行與筆記本註解填；卡住開 <code>-solution.ipynb</code></div>
</div>

<!--
★ 執行（約 20 分）。
-->

---

<div class="eyebrow">05 · Lab L2-1</div>

# Lab 6／7：Audit → Iterate

<table style="font-size:17px">
<thead><tr><th style="width:30%">稽核問題</th><th>具體動作</th><th style="width:30%">應該是</th></tr></thead>
<tbody>
<tr><td>訓練集真的只有良品？</td><td>看切分格印出的張數</td><td>train 的「不良」＝ 0</td></tr>
<tr><td>輸入和輸出範圍一致？</td><td>x 是 0–1；decoder 最後是 Sigmoid</td><td>都是 0–1</td></tr>
<tr><td>門檻用哪個資料集選？</td><td>找 <code>thr</code> 那一行</td><td>只用 <code>s_val</code></td></tr>
<tr><td>熱力圖亮在瑕疵上？</td><td>看 4 張不良品的熱力圖</td><td>多數亮在瑕疵附近（講師實跑填入）</td></tr>
<tr><td>測試集數字合理？</td><td>比較 val 與 test 的過殺、漏檢</td><td>接近；test 漏檢可能略高於 5%</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">一次只改一件事：例如瓶頸窄一點（少一層 up／down），比較 AUROC。</div>

<!--
★ 稽核（8 分）：最常見錯誤：Agent 拿 Normalize 把輸入變成 −1～1，但 decoder 用 Sigmoid 只能輸出 0～1 → 誤差永遠很大。
-->

---

<div class="eyebrow">05 · Lab L2-1 · Ship</div>

# Lab 7／7：Gradio 檢測站（第二天的交付）

<div class="grid grid-cols-[1.3fr_1fr] gap-5 mt-1">
<div>

```python
def inspect(img):
    x = tf(img.convert("RGB")).unsqueeze(0)
    m = anomaly_map(x)[0]          # 熱力圖
    s = score(x).item()            # 分數
    return heatmap(m), "疑似不良" if s > thr else "良品"

gr.Interface(fn=inspect, inputs=gr.Image(type="pil"),
             outputs=[gr.Image(), gr.Textbox()]).launch(share=True)
```

</div>
<div>

<div class="placeholder" style="height:200px">檢測站畫面<small>講師實跑後替換</small></div>

</div>
</div>

<div class="takeaway mt-3">D1-4 的 Gradio，換成今天的 <code>anomaly_map</code> 與 <code>thr</code>：品保部可以自己上傳板子看熱力圖。</div>

<!--
★ Ship（5 分）：把門檻和分數一起顯示，複判人員才知道「差一點就判不良」的板子。heatmap() 在筆記本裡是用 matplotlib 色表轉成圖片。
-->

---

<div class="eyebrow">06 · Measure & Risk</div>

# 風險：誰的成本比較高？資料能不能用？

<div class="grid grid-cols-2 gap-6 mt-2">
<div>

<table style="font-size:17px">
<thead><tr><th></th><th>代價</th></tr></thead>
<tbody>
<tr><td><strong>漏檢</strong></td><td>客訴、退貨、商譽；嚴重時召回</td></tr>
<tr><td><strong>過殺</strong></td><td>複判人力、產線變慢、好板報廢</td></tr>
</tbody>
</table>

<div class="muted mt-2" style="font-size:16px">門檻要和品保主管一起定，不是工程師自己定</div>

</div>
<div>

<table style="font-size:17px">
<thead><tr><th>資料集</th><th>授權（待確認）</th></tr></thead>
<tbody>
<tr><td>VisA</td><td>CC BY 4.0：可商用，需標示</td></tr>
<tr><td>MVTec AD</td><td>CC BY-NC-SA：非商用</td></tr>
<tr><td>DeepPCB</td><td>標示不一致，有疑義</td></tr>
</tbody>
</table>

</div>
</div>

<div class="takeaway mt-4">技術上能跑的資料集，不一定能用在付費課程或公司產品；先讀授權。</div>

<div class="src">各資料集授權以官方頁面為準（S6–S8，待確認）</div>

<!--
★ 風險（4 分）：這也是為什麼本課選 VisA 而不是最有名的 MVTec AD（roadmap §9.2）。
-->

---

<div class="eyebrow">總整理</div>

# 今天學到的概念鏈

<div class="chain flex flex-nowrap items-center gap-2 mt-4">
  <span class="chip">只有良品</span><span class="arrow">→</span>
  <span class="chip">AE 壓扁再還原</span><span class="arrow">→</span>
  <span class="chip">誤差圖與分數</span><span class="arrow">→</span>
  <span class="chip">門檻</span><span class="arrow">→</span>
  <span class="chip">過殺／漏檢</span><span class="arrow">→</span>
  <span class="chip">AUROC</span><span class="arrow">→</span>
  <span class="chip">檢測站</span>
</div>

<div class="takeaway mt-6">生成模型學會「正常」，重建不好的地方就是可疑；門檻是商業決定，AUROC 是模型品質。</div>

<!--
★ 總整理（2 分）。
-->

---

<div class="eyebrow">隨堂檢核</div>

# 選擇題（iPAS 題型）

<div class="mcq">

1. 用自編碼器做異常偵測，訓練資料應該是？（　）<br><span class="opts">A. 只有不良品　B. 只有良品　C. 良品與不良品各半　D. 不需要資料</span>
2. 「過殺」對應混淆矩陣的哪一格？（不良為正類）（　）<br><span class="opts">A. TP　B. FN　C. FP　D. TN</span>
3. 把門檻調低，通常會？（　）<br><span class="opts">A. 過殺增加、漏檢減少　B. 過殺減少、漏檢增加　C. 兩者都減少　D. 兩者都不變</span>
4. AUROC ＝ 0.5 代表？（　）<br><span class="opts">A. 完美　B. 和亂猜差不多　C. 門檻設錯　D. 過殺率 50%</span>

</div>

<!--
★ 檢核（4 分）。答案：1 B、2 C、3 A、4 B。
-->

---
hostOnly: true
---

<div class="eyebrow">下一步</div>

# 下一堂 D2-2：告訴我瑕疵在哪、有多大

<div class="node node--primary mt-2">維修站不只要「這片有問題」，還要每個瑕疵的位置與面積。下一堂在今天的主角圖上加「跳接」，變成 U-Net；但沒有瑕疵遮罩怎麼訓練？我們自己合成瑕疵。</div>

<!--
★ 只給講師的託管版看。
-->
