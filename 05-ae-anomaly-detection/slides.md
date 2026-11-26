---
theme: default
title: 找出從沒看過的瑕疵
info: |
  生成式AI原理 · L05
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

<div class="eyebrow">生成式AI原理 · L05</div>

# 找出從沒看過的瑕疵

<p class="subtitle">只看過良品的自編碼器，把「重建不好」變成瑕疵分數</p>

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-8">
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
  <div class="ticket-head">【需求單 #L05】部門：製造品保部（A 線）<span>公司：曜嶼電子 <span class="fiction" style="color:#fff;border-color:#fff">虛構</span></span></div>
  <dl>
    <dt>問題</dt><dd>AOI（自動光學檢測）把太多好板判成不良（過殺），新型瑕疵卻會漏掉（漏檢）</dd>
    <dt>現況痛點</dt><dd>每天人工複判大量過殺板；新瑕疵每月出現，來不及標註</dd>
    <dt>成功指標（KPI）</dt><dd>漏檢率 ≤ 5% 的前提下，過殺率比現況低；附 AUROC（排序品質指標，第 19 頁）</dd>
    <dt>可用資料</dt><dd>數百張良品；瑕疵很少、沒有新瑕疵（用公開資料集 VisA PCB1 代替）</dd>
    <dt>限制與法規</dt><dd>Colab T4；資料集授權（VisA：CC BY 4.0，待確認）</dd>
    <dt>為何現有工具不夠</dt><dd>CNN 分類器需要每一類瑕疵都有標註，沒看過的瑕疵分不出來</dd>
  </dl>
</div>

<!--
★ 需求單（3 分）：三個工廠用語：過殺（好的被判壞）、漏檢（壞的被放過）、AOI（自動光學檢測）。第 16 頁會對應到 FP、FN。
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
★ 目標（1 分）。不教：U-Net 定位（L06）、VAE（L07）、擴散模型異常偵測（L12）；PatchCore 等方法只點名。
-->

---

<div class="eyebrow">00 · Frame</div>

# 為什麼 DL 課的 CNN 分類器做不到？

<div class="flex items-center justify-center gap-3 mt-4" style="font-size:18px">
  <div class="node" style="width:28%">新型瑕疵的板子<small>訓練時從沒出現</small></div><span class="arrow">→</span>
  <div class="node" style="width:28%">CNN 分類器<small>只認得「良品、刮傷、短路」</small></div><span class="arrow">→</span>
  <div class="node node--warm" style="width:28%">硬塞進一類<small>常被判成「良品」</small></div>
</div>

<div class="grid grid-cols-3 gap-4 mt-5" style="font-size:18px">
<div class="node">分類器只能回答<strong>看過的類別</strong></div>
<div class="node">新瑕疵沒有標註，也來不及標</div>
<div class="node">瑕疵樣本又少：資料嚴重不平衡</div>
</div>

<div class="takeaway mt-6">問題不在 CNN 不夠好，而是「沒看過的類別」根本不在它的選項裡。</div>

<div class="src">回顧：DL pp.38–55（CNN 分類）</div>

<!--
★ Frame（4 分）：請學員回想 L03 的 CIFAR-10：如果輸入一張 10 類以外的新東西（例如蛋糕），分類器還是會從 10 類裡挑一個。
-->

---

<div class="eyebrow">01 · 先認識工具 · 自編碼器</div>

# 自編碼器（Autoencoder）：把圖壓扁，再畫回來

<div class="grid grid-cols-[0.62fr_1.38fr] gap-6 mt-0 items-center">
<div>
  <img class="photo" src="/ae-schema.png" alt="自編碼器示意圖：輸入 X 經過 Encoder 變成較窄的 Code h，再經過 Decoder 輸出 X′" style="width:100%;max-height:230px;object-fit:contain;border:none">
</div>
<div style="font-size:17px">
  <div class="node node--primary" style="padding:6px 12px"><strong>Encoder（編碼器）</strong><small>把一張圖的幾萬個數字，壓成少很多的一串數字</small></div>
  <div class="node node--warm mt-2" style="padding:6px 12px"><strong>Code（中間的摘要，常寫成 z 或 h）</strong><small>這張圖的「重點筆記」，放不下每一個像素</small></div>
  <div class="node node--secondary mt-2" style="padding:6px 12px"><strong>Decoder（解碼器）</strong><small>只看這份筆記，把圖畫回來，得到 X′</small></div>
  <div class="mt-2"><strong>訓練目標</strong>：X′ 和 X 越像越好。<span class="key">答案就是輸入自己</span>，所以不用標註。</div>
</div>
</div>

<img class="photo mt-2" src="/lab05-recon.png" alt="四對 PCB 影像，每一對左邊是輸入、右邊是自編碼器的重建，稍微模糊但板子、針腳、方向都畫回來了" style="width:100%;border:none">
<div class="shot-cap">實跑（lab05，Colab T4）：每一對左＝輸入、右＝重建。細節略糊，但板子、針腳、拍攝方向都畫回來了</div>

<div class="src">左圖：Michela Massi, Autoencoder schema, Wikimedia Commons, CC BY-SA 4.0（S10）；下排：lab05 解答筆記本「重建網格」格，測試集前 4 張（VisA PCB1，CC BY 4.0，S1）</div>

<!--
★ 認識自編碼器（5 分）：先不談瑕疵，只談它會做什麼——「看一眼、寫筆記、只看筆記畫回來」。
DL 課看過 AE 的概念圖（DL pp.72–79），今天把它講清楚：Encoder 壓縮、Code 是摘要、Decoder 還原。
重點句：訓練時「答案就是輸入自己」，所以只要有圖就能訓練，不用人工標註。這一點等一下會變成關鍵。
指著右下的實跑：重建很像，但有點糊——因為筆記放不下每個細節。
-->

---

<div class="eyebrow">01 · 先認識工具 · 潛在空間</div>

# 中間那份「筆記」記了什麼？Latent space（潛在空間）

<div class="flex items-center justify-center gap-2 mt-2" style="font-size:17px">
  <div style="width:17%"><img class="photo" src="/pcb1-normal.jpg" alt="一片正常的 HC-SR04 板子" style="width:100%"><div class="shot-cap text-center">輸入：一張圖</div></div>
  <span class="arrow">→</span>
  <div class="node node--primary" style="width:12%"><strong>Encoder</strong></div>
  <span class="arrow">→</span>
  <div class="node node--warm" style="width:34%">
    <strong>z：一串數字（示意）</strong>
    <div class="lat"><span>z₁</span><i style="width:80%"></i><em>拍攝方向（正／倒）</em></div>
    <div class="lat"><span>z₂</span><i style="width:35%"></i><em>板子偏左還是偏右</em></div>
    <div class="lat"><span>z₃</span><i style="width:60%"></i><em>整體亮度</em></div>
    <div class="lat"><span>z₄</span><i style="width:90%"></i><em>四根針腳直不直</em></div>
    <div class="lat"><span>⋮</span><i style="width:0"></i><em>今天的模型共 8,192 個數字</em></div>
  </div>
  <span class="arrow">→</span>
  <div class="node node--secondary" style="width:12%"><strong>Decoder</strong></div>
  <span class="arrow">→</span>
  <div class="node" style="width:12%">重建圖</div>
</div>

<div class="grid grid-cols-2 gap-6 mt-4" style="font-size:18px">
<div class="node"><strong>類比：打電話描述一片板子</strong><small>「倒著放、偏左一點、有點暗、四根針都直的」——對方照著描述畫，就能畫出差不多的板子</small></div>
<div class="node"><strong>潛在空間＝所有可能的 z 組成的空間</strong><small>每張圖是裡面的一個點；長得像的圖，點也靠得近</small></div>
</div>

<div class="takeaway mt-3">筆記的格子有限：常見的特徵（方向、位置、亮度）會被記下；少見的小細節記不下，畫回來時就不見了。</div>

<div class="src">z 每一格的名稱是示意：真正的 AE 不會替每一維取名字，一個特徵常分散在好幾維。L07 會畫出真實的 2 維潛在空間</div>

<!--
★ 潛在空間（5 分）：Latent space（潛在空間）是新詞：「潛在」＝看不到、但藏在背後的因素。
用打電話的類比：Encoder 是描述的人，Decoder 是照描述畫的人，z 就是電話裡講的那幾句話。
誠實說明：z 每一格「拍攝方向、亮度……」是為了好懂而取的名字；模型自己學出來的維度通常沒有這麼乾淨的意思。L07（VAE）會用 2 維的 z 畫出真的散佈圖。
最後一句埋伏筆：「少見的小細節記不下」——等一下就會用到。
-->

---

<div class="eyebrow">01 · 先認識工具 · 今天的主角圖</div>

# 自編碼器：壓扁，再還原

<div class="flex items-center justify-center gap-2 mt-4" style="font-size:18px">
  <div class="node" style="width:16%">輸入 x<small class="nw">&#91;B,3,128,128&#93;</small></div><span class="arrow">→</span>
  <div class="node node--primary" style="width:18%"><strong>Encoder</strong><small>每層高寬減半</small></div><span class="arrow">→</span>
  <div class="node node--warm" style="width:16%"><strong>瓶頸 z</strong><small class="nw">&#91;B,128,8,8&#93;</small></div><span class="arrow">→</span>
  <div class="node node--secondary" style="width:18%"><strong>Decoder</strong><small>每層高寬加倍</small></div><span class="arrow">→</span>
  <div class="node" style="width:16%">重建 x̂<small class="nw">&#91;B,3,128,128&#93;</small></div>
</div>

<div class="grid grid-cols-2 gap-6 mt-6" style="font-size:18px">
<div>

- **瓶頸**（bottleneck）：z 比 x 小約 6 倍，放不下每個細節
- **訓練目標**：讓 x̂ 和 x 越像越好（MSE）

</div>
<div class="node node--dashed"><strong>這張圖整天都會出現</strong><small>L06 加跳接（U-Net）、L07 瓶頸變成機率（VAE）、L08 瓶頸變成編碼簿裡的編號（VQ-VAE）</small></div>
</div>

<div class="takeaway mt-4">瓶頸放不下每個細節：模型只能記住「這類圖共同的樣子」，個別的小地方會被抹掉。</div>

<div class="src">回顧：DL pp.72–79（AE、U-Net、VAE 概念）——今天直接看程式與用途</div>

<!--
★ 主角圖（4 分）：前兩頁講了「做什麼」，這頁換成今天 Lab 的真實尺寸。重點放在 shape：3×128×128 ＝ 49152 個數字 → 128×8×8 ＝ 8192 個數字，約 1/6。
x̂ 讀作「x hat」：模型重建出來的 x。
-->

---

<div class="eyebrow">02 · 連起來</div>

# AE 很會「重建」……這跟抓瑕疵有什麼關係？

<div class="muted" style="font-size:18px">想一想（30 秒）：如果這個 AE 從頭到尾<strong>只看過良品</strong>，現在給它一片針腳彎掉的板子——</div>

<div class="flex items-center justify-center gap-3 mt-4" style="font-size:18px">
  <div style="width:24%"><img class="photo" src="/pcb1-bent-zoom.jpg" alt="放大：一支針腳往左彎" style="width:100%"><div class="shot-cap text-center">輸入：彎針</div></div>
  <span class="arrow">→</span>
  <div class="node node--primary" style="width:22%"><strong>AE</strong><small>只看過幾百片良品</small></div>
  <span class="arrow">→</span>
  <div class="node node--dashed" style="width:24%;height:150px;display:flex;align-items:center;justify-content:center;font-size:40px;color:var(--muted-text)">？</div>
</div>

<div class="grid grid-cols-2 gap-6 mt-5" style="font-size:18px">
<div class="node">① 重建圖會畫出彎針，還是直針？</div>
<div class="node">② 輸入減掉重建，哪裡的差最大？</div>
</div>

<div class="takeaway mt-3">線索：上一頁說過，筆記只記得下「常見的樣子」。</div>

<!--
★ 提問（3 分）：先不給答案，讓學員和隔壁討論 30 秒。
期待的答案：AE 沒看過彎針，筆記裡沒有「彎針」這種寫法，只能畫出它最熟的直針 → 輸入和重建在彎針處差最多。
接下來三頁：換個問法（只學正常）→ 修掉的機制 → 實跑結果。
-->

---

<div class="eyebrow">02 · 連起來 · 換個問法</div>

# 換個問法：只學「正常長什麼樣」

<div class="grid grid-cols-[1.25fr_1fr] gap-6 mt-1 items-start">
<div>
  <img class="photo" src="/pcb1-grid9.jpg" alt="九片 HC-SR04 板子的照片，其中一片有焊錫熔化的瑕疵" style="width:100%">
  <div class="shot-cap">九片 A 線的板子，只有一片有問題：是哪一片？</div>
</div>
<div style="font-size:18px">

<div class="node"><strong>舊問法（分類）</strong><small>「這是哪一種瑕疵？」→ 需要每一種瑕疵的樣本</small></div>
<div class="node node--primary mt-3"><strong>新問法（異常偵測）</strong><small>「這片和平常的良品像不像？」→ 只需要良品</small></div>
<div class="node node--secondary mt-3"><strong>類比：老師傅</strong><small>看久了好板，任何「怪怪的」地方一眼就看出來——就算那種瑕疵他從沒見過</small></div>

</div>
</div>

<div class="takeaway mt-3">生成模型學的是「良品通常長什麼樣」（L01 的 p_data），不像的就是可疑。</div>

<div class="src">VisA PCB1（Zou et al., 2022，CC BY 4.0，S1）：良品 0612、0640、0661、0689、0702、0733、0758、0790 與不良品 016，講師裁切</div>

<!--
★ 換問法（4 分）：先讓學員挑（30 秒）。答案是第 6 張：Echo、Gnd 兩支針腳的焊錫熔化（下一頁有放大）。挑不出來很正常——這就是老師傅花好幾年學的事。
再連回 L01 第 8 頁的分布圖：良品是黑點，模型學出藍色區域；落在區域外的板子就可疑。
-->

---

<div class="eyebrow">02 · 連起來 · 為什麼抓得到</div>

# 只學過良品，所以會把瑕疵「修掉」

<div class="grid grid-cols-[1.4fr_1fr] gap-5 mt-2 items-start">
<div class="grid grid-cols-[1.6fr_1fr] gap-3">
  <div><img class="photo" src="/pcb1-bent-outline.jpg" alt="一片 Trig 針腳彎掉的 HC-SR04 板子，綠線圈出人工標註" style="width:100%"><div class="shot-cap">真實不良品：綠線＝人工標註</div></div>
  <div><img class="photo" src="/pcb1-bent-zoom.jpg" alt="放大：Trig 針腳往左彎" style="width:100%"><div class="shot-cap">放大：彎掉的針腳</div></div>
</div>
<div style="font-size:17px">
  <div class="node"><strong>① 輸入</strong><small>有一支彎針的板子</small></div>
  <div class="node node--secondary mt-2"><strong>② 重建</strong><small>模型沒看過彎針，畫出「正常」的直針</small></div>
  <div class="node node--warm mt-2"><strong>③ 相減</strong><small>(x − x̂)² 只在彎針處很大</small></div>
</div>
</div>

<div class="takeaway mt-3">誤差大＝「這裡和模型學到的良品不一樣」；綠線就是我們希望熱力圖亮起來的地方。</div>

<div class="src">VisA PCB1 不良品 001 與遮罩（CC BY 4.0，S1），講師裁切</div>

<!--
★ 機制（5 分）：這頁是整堂的核心。用「修圖」比喻：模型是只會修成良品樣子的修圖師。
常見誤解：「AE 是用來抓瑕疵的模型」——不對，AE 只會重建；抓瑕疵的是我們拿「重建誤差」去比。
-->

---

<div class="eyebrow">03 · Try（實際跑跑看）</div>

# 實跑：熱力圖會亮在瑕疵上嗎？

<div class="grid grid-cols-[1.25fr_1fr] gap-5 mt-0 items-start">
<div>
  <img class="photo" src="/lab05-heatmaps.png" alt="四張測試集不良品：第一排輸入、第二排重建、第三排誤差熱力圖" style="width:100%;max-height:345px;object-fit:contain;border:none">
</div>
<div style="font-size:17px">
  <div class="node node--secondary"><strong>第 2 張（針腳彎掉）</strong><small>重建把針「拉直」了，誤差最亮的地方就在彎針上 ✓</small></div>
  <div class="node mt-2"><strong>第 4 張（左邊探頭的網子不見）</strong><small>重建補回一部分網子，誤差散在整個探頭上</small></div>
  <div class="node node--warm mt-2"><strong>每一張的零件邊緣都有一點亮</strong><small>重建本來就比較糊，邊緣一定有誤差 → 良品也會有分數</small></div>
</div>
</div>

<div class="takeaway mt-2">會亮在瑕疵上，但不乾淨：這就是今天的基準線（測試集 AUROC 0.908，第 19 頁）。</div>

<div class="src">實跑：lab05 解答筆記本「熱力圖」格，Colab T4，2026-11-26 紀錄（research/lab-runs.md）；測試集前 4 張不良品，VisA PCB1（CC BY 4.0，S1）</div>

<!--
★ 實跑（5 分）：先問「哪一張最明顯？」再一張一張看。第 2 張是上一頁講的「修掉」：彎針被畫成直針。
誠實說明：第 1、3 張很難看出瑕疵在哪，邊緣的亮點反而比較多——這就是為什麼分數會重疊、需要門檻（第 15 頁），也是 L06 要換方法的原因。第 23 頁（附錄）說明 AE 為什麼有時連瑕疵也重建得很好。
-->

---

<div class="eyebrow">04 · Open（打開黑盒子）· 解碼器</div>

# 解碼器怎麼放大？ConvTranspose 與 Upsample

<div class="grid grid-cols-2 gap-5 mt-1">
<div>

```python
# 方法一：轉置卷積（本 Lab 用）
nn.ConvTranspose2d(128, 64, 4,
                   stride=2, padding=1)
# [B, 128, 16, 16] → [B, 64, 32, 32]
```

<div class="muted" style="font-size:17px">讀作：4＝核大小、stride 2＝高寬加倍；「學出來的放大」——放大的方式也是參數</div>

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
★ 解碼器（4 分）：ConvTranspose 有時會出現棋盤狀的假影（checkerboard），L06 的附錄會提到。這裡只要知道兩種都能把 16 變 32。
-->

---

<div class="eyebrow">04 · Open · 誤差圖</div>

# 重建誤差熱力圖：每個像素一個誤差

<div class="grid grid-cols-[1.15fr_1fr] gap-6 mt-1">
<div>

```python
def anomaly_map(x):      # 筆記本裡另有 model.eval() 與 no_grad
    x_hat = model(x)
    return ((x - x_hat) ** 2).mean(dim=1)
    # [B, 3, 128, 128] → [B, 128, 128]

def score(x):
    m = anomaly_map(x).flatten(1)      # [B, 16384]
    k = max(1, int(m.shape[1] * 0.01)) # 最大的 1%
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
這個分數設計是本 Lab 的選擇，不是標準答案；SSIM 等替代方法見第 22 頁。
-->

---

<div class="eyebrow">05 · Measure（量化驗收）· 分數</div>

# 分數＝有多「不典型」

<div class="grid grid-cols-[1.25fr_1fr] gap-6 mt-1 items-center">
<div>

<svg viewBox="0 0 460 230" style="width:100%">
  <defs><marker id="ax5" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--muted-text)"/></marker></defs>
  <line x1="30" y1="190" x2="440" y2="190" stroke="var(--muted-text)" stroke-width="1.5" marker-end="url(#ax5)"/>
  <text x="380" y="215" style="font-size:16px" fill="var(--muted-text)">分數 →</text>
  <path d="M40,190 C80,190 90,60 140,60 C190,60 200,190 260,190 Z" fill="var(--soft-teal)" stroke="var(--secondary)" stroke-width="2"/>
  <path d="M200,190 C250,190 270,110 310,110 C350,110 370,190 420,190 Z" fill="var(--soft-amber)" stroke="var(--warm-accent)" stroke-width="2" stroke-dasharray="6 4"/>
  <text x="100" y="50" style="font-size:17px" fill="var(--secondary)">良品</text>
  <text x="290" y="100" style="font-size:17px" fill="var(--warm-accent)">不良品</text>
  <text x="196" y="215" style="font-size:17px" fill="var(--muted-text)">↑ 重疊</text>
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
★ 典型性（5 分）：likelihood 讀作「概似」：模型認為這筆資料出現的可能性。AE 沒有直接算機率，但重建誤差扮演同樣的角色。L07 的 VAE 會更接近「機率」。
-->

---

<div class="eyebrow">05 · Measure · 門檻</div>

# 門檻：一條線決定判良或判不良

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-1 items-center">
<div>

<svg viewBox="0 0 460 235" style="width:100%" aria-label="良品與不良品的分數分布，中間一條垂直門檻線">
  <line x1="30" y1="190" x2="440" y2="190" stroke="var(--muted-text)" stroke-width="1.5"/>
  <path d="M40,190 C80,190 90,60 140,60 C190,60 200,190 260,190 Z" fill="var(--soft-teal)" stroke="var(--secondary)" stroke-width="2"/>
  <path d="M200,190 C250,190 270,110 310,110 C350,110 370,190 420,190 Z" fill="var(--soft-amber)" stroke="var(--warm-accent)" stroke-width="2" stroke-dasharray="6 4"/>
  <line x1="232" y1="30" x2="232" y2="195" stroke="var(--primary)" stroke-width="3"/>
  <text x="240" y="40" style="font-size:17px" fill="var(--primary)">門檻</text>
  <text x="238" y="180" style="font-size:17px" fill="var(--secondary)">過殺</text>
  <text x="180" y="180" style="font-size:17px" fill="var(--warm-accent)">漏檢</text>
  <text x="60" y="222" style="font-size:17px" fill="var(--muted-text)">← 判良品</text>
  <text x="330" y="222" style="font-size:17px" fill="var(--muted-text)">判不良 →</text>
</svg>

</div>
<div style="font-size:17px">

- 線往左：漏檢少、過殺多
- 線往右：過殺少、漏檢多

<table class="mt-2" style="font-size:16px">
<thead><tr><th></th><th>代價</th></tr></thead>
<tbody>
<tr><td><strong>漏檢</strong></td><td>客訴、退貨；嚴重時召回</td></tr>
<tr><td><strong>過殺</strong></td><td>複判人力、好板報廢</td></tr>
</tbody>
</table>

</div>
</div>

<div class="takeaway mt-2">門檻不是模型學出來的，是<strong>商業決定</strong>：今天的規則是「漏檢最多 5%」，再看過殺是多少。</div>

<div class="src">分布為教學示意，不是實測；門檻要和品保主管一起定</div>

<!--
★ 門檻（5 分）：重疊區域一定存在，所以不可能同時零過殺、零漏檢。下一頁把這兩個工廠用語對到 ML 課的混淆矩陣。
-->

---

<div class="eyebrow">05 · Measure · 工廠用語</div>

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

<div class="eyebrow">05 · Measure · 練習</div>

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

<div class="eyebrow">05 · Measure · 練習解答</div>

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

<div class="eyebrow">05 · Measure · AUROC</div>

# AUROC：不挑門檻，看排序好不好

<div class="grid grid-cols-[1fr_1.2fr] gap-6 mt-2 items-center">
<div>

<svg viewBox="0 0 260 240" style="width:100%;max-height:285px">
  <defs><marker id="ax6" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--muted-text)"/></marker></defs>
  <line x1="30" y1="210" x2="240" y2="210" stroke="var(--muted-text)" stroke-width="1.5" marker-end="url(#ax6)"/>
  <line x1="30" y1="210" x2="30" y2="15" stroke="var(--muted-text)" stroke-width="1.5" marker-end="url(#ax6)"/>
  <line x1="30" y1="210" x2="220" y2="25" stroke="var(--border)" stroke-width="1.5" stroke-dasharray="5 4"/>
  <path d="M30,210 L30,120 L60,80 L100,50 L160,35 L220,25" fill="none" stroke="var(--primary)" stroke-width="3"/>
  <text x="110" y="232" style="font-size:16px" fill="var(--muted-text)">過殺率（FP 率）</text>
  <text x="36" y="22" style="font-size:16px" fill="var(--muted-text)">抓到率（1 − 漏檢率）</text>
  <text x="130" y="150" style="font-size:16px" fill="var(--muted-text)">亂猜＝0.5</text>
</svg>

</div>
<div style="font-size:18px">

- 每個門檻畫一點，連成 ROC 曲線（不同門檻下「抓到率 vs 過殺率」）
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

<div class="eyebrow">05 · Measure · 資料陷阱</div>

# 稽核資料：良品和不良品，連拍攝方向都不一樣

<img class="photo mt-2" src="/pcb1-orientation.jpg" alt="三片板子：倒著拍的良品、正著拍的良品、正著拍的不良品" style="width:100%">

<div class="grid grid-cols-3 gap-4 mt-1" style="font-size:16px">
<div class="shot-cap">良品，倒著拍（針腳朝上）：約 79%</div>
<div class="shot-cap">良品，正著拍：約 21%</div>
<div class="shot-cap">不良品：95% 正著拍</div>
</div>

<div class="node node--warm mt-3" style="font-size:18px"><strong>會發生什麼事</strong><small>模型可能學到「方向不對＝瑕疵」：AUROC 很漂亮，上線遇到正著放的好板就過殺</small></div>

<div class="takeaway mt-3">高分不一定代表學對了：先看資料。Lab 的解法是訓練時加 180° 旋轉，兩種方向都算正常。</div>

<div class="src">VisA PCB1 良品 0000、0620 與不良品 001；比例為講師本機以針腳位置判斷全部 1,104 張並目視抽查（2026-11-24，research/lab-runs.md）</div>

<!--
★ 資料陷阱（3 分）：這是真的發生在公開資料集裡的事，不是編的。問學員：「如果模型只看方向，AUROC 大概會是多少？」→ 很高，因為幾乎所有不良品都是正的、大部分良品是倒的。
產線上也常見：不良品是另一個站、另一台相機、另一個時間拍的，模型就學到「哪一站拍的」而不是「有沒有瑕疵」（L10 的 B 線問題）。
-->

---

<div class="eyebrow">05 · Measure · 業界基準 · 選修</div>

# 我們的 AE 是基準線；產線用更強的方法

<div class="grid grid-cols-2 gap-6 mt-4" style="font-size:18px">
<div class="node"><strong>PatchCore</strong><small>用預訓練 CNN 的特徵，記住良品的「小區塊特徵庫」，比對最近的距離</small></div>
<div class="node"><strong>EfficientAD</strong><small>老師－學生網路＋小型自編碼器，強調速度（每片毫秒等級）</small></div>
</div>

<div class="takeaway mt-6">先用簡單的 AE 建立基準線與評估流程（分數、門檻、AUROC），換更強的方法時流程不變。</div>

<div class="src">Roth et al., PatchCore (CVPR 2022)；Batzner et al., EfficientAD (WACV 2024)（S4、S5，待確認）</div>

<!--
○ 基準（3 分）：只點名，不實作。重點：今天建立的「評估流程」才是可以帶走的東西。學員如果期末專題做異常偵測，可以用 anomalib（下一頁）。
-->

---

<div class="eyebrow">05 · Adapt · 選修</div>

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

<div class="takeaway mt-6">瓶頸太寬會照抄、太窄會模糊；L06 的跳接會讓照抄更嚴重，L12 用擴散模型換個做法。</div>

<!--
△ 備用（2 分）：學員發現熱力圖沒亮在瑕疵上時用。可以讓學員比較兩個方向：少一層 down（瓶頸變 16×16，反而「寬」4 倍，照抄更嚴重），或把最後一層 down 的通道 128→32（瓶頸變「窄」），比較 AUROC。
-->

---

<div class="eyebrow">06 · Lab L2-1</div>

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

<img class="photo" src="/lab05-hist.png" alt="驗證集分數直方圖：藍色良品集中在左邊，橘色不良品偏右，中間有重疊" style="width:100%;border:none">
<div class="shot-cap">講師實跑（Colab T4）：驗證集分數直方圖。測試集 AUROC 0.908；漏檢 ≤ 5% 的門檻下，測試集過殺 36.4%、漏檢 2.0%</div>

</div>
</div>

<div class="takeaway mt-3">這就是四個檢查點的 ① 目標。</div>

<!--
★ Lab 開始（3 分）：VisA 整包很大，下載時間待實測；建議講師課前把 PCB1 放到共用雲端硬碟，學員改 PCB1_DIR。
備案：沒有 GPU → SIZE＝64、EPOCHS＝3；斷線 → 把講師的 ae_pcb1.pt 放到工作目錄，會自動載入。
-->

---

<div class="eyebrow">06 · Lab L2-1</div>

# Lab 2／7：模型拆成哪幾塊？

<div class="mt-3" style="font-size:17px"><strong>訓練</strong></div>
<div class="flex items-center gap-2 mt-1" style="font-size:17px">
  <div class="node"><code>PCBDataset</code><small class="nw">&#91;B,3,128,128&#93;</small></div><span class="arrow">→</span>
  <div class="node node--primary"><code>encoder</code><small>4 次 down</small></div><span class="arrow">→</span>
  <div class="node node--warm"><code>z</code><small>瓶頸</small></div><span class="arrow">→</span>
  <div class="node node--secondary"><code>decoder</code><small>4 次放大</small></div><span class="arrow">→</span>
  <div class="node">x̂<small>MSE(x̂, x)</small></div>
</div>

<div class="mt-4" style="font-size:17px"><strong>評估與上線</strong></div>
<div class="flex items-center gap-2 mt-1" style="font-size:17px">
  <div class="node"><code>anomaly_map</code><small>誤差圖 &#91;B, H, W&#93;</small></div><span class="arrow">→</span>
  <div class="node"><code>score</code><small>每片一個分數</small></div><span class="arrow">→</span>
  <div class="node node--warm"><code>thr</code><small>判良／判不良</small></div>
</div>


<div class="takeaway mt-4">名稱和筆記本一樣：<code>PCBDataset</code>、<code>ConvAE.encoder</code>、<code>.decoder</code>、<code>anomaly_map</code>、<code>score</code>、<code>thr</code>。</div>

<!--
★ 拆塊（3 分）：先指出訓練和評估用的部分不同。下一頁填 shape。
-->

---

<div class="eyebrow">06 · Lab L2-1 · 練習</div>

# Lab 3／7 · 練習：每一塊的輸入與輸出

<div class="muted" style="font-size:17px">不用 AI。<code>down</code>：卷積 stride 2，高寬減半；<code>up</code>：ConvTranspose stride 2，高寬加倍。B ＝ 32</div>

<table class="fill tight vlines mt-1">
<thead><tr><th style="width:26%">塊</th><th>輸入 shape</th><th>輸出 shape</th><th>做什麼（一句話）</th></tr></thead>
<tbody>
<tr><td><code>encoder</code>（照著做）</td><td>&#91;32, 3, 128, 128&#93;</td><td>&#91;32, 128, 8, 8&#93;：高寬 ÷2 四次</td><td>壓成瓶頸</td></tr>
<tr><td><code>decoder</code></td><td class="blank"><FillIn id="ae.dec-in" /></td><td class="blank"><FillIn id="ae.dec-out" /></td><td class="blank"><FillIn id="ae.dec-do" /></td></tr>
<tr><td><code>anomaly_map</code></td><td class="blank"><FillIn id="ae.map-in" /></td><td class="blank"><FillIn id="ae.map-out" hint="例：少了一維……" /></td><td class="blank"><FillIn id="ae.map-do" /></td></tr>
<tr><td><code>score</code></td><td class="blank"><FillIn id="ae.score-in" /></td><td class="blank"><FillIn id="ae.score-out" /></td><td class="blank"><FillIn id="ae.score-do" /></td></tr>
</tbody>
</table>

<FillClear group="ae" />

<!--
★ 無 AI 檢核點（8 分）：第一列整列填好當示範。不收回。下一頁是解答。
-->

---
hostOnly: true
---

<div class="eyebrow">06 · Lab L2-1 · 練習解答</div>

# 練習解答：每一塊的輸入與輸出

<table class="vlines" style="font-size:18px">
<thead><tr><th style="width:24%">塊</th><th>輸入</th><th>輸出</th><th>做什麼</th></tr></thead>
<tbody>
<tr><td><code>encoder</code></td><td>&#91;32, 3, 128, 128&#93;</td><td>&#91;32, 128, 8, 8&#93;</td><td>128→64→32→16→8，壓成瓶頸</td></tr>
<tr><td><code>decoder</code></td><td>&#91;32, 128, 8, 8&#93;</td><td>&#91;32, 3, 128, 128&#93;</td><td>還原成原大小（Sigmoid → 0–1）</td></tr>
<tr><td><code>anomaly_map</code></td><td>&#91;32, 3, 128, 128&#93;</td><td>&#91;32, 128, 128&#93;</td><td>每像素平方誤差，通道平均</td></tr>
<tr><td><code>score</code></td><td>&#91;32, 3, 128, 128&#93;</td><td>&#91;32&#93;</td><td>每片板子一個分數</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">怎麼對答案：筆記本「模型」格印出 x、z、x̂ 的 shape（本機煙霧測試已確認 z ＝ &#91;B, 128, 8, 8&#93;）。</div>

<!--
★ 解答（2 分）：本機 CPU 煙霧測試（research/lab-runs.md）印出 z (8, 128, 8, 8)，壓縮成 1/6。
-->

---

<div class="eyebrow">06 · Lab L2-1</div>

# Lab 4／7：Specify

<div style="font-size:18px" class="mt-2">

<strong>【目標】</strong>只用良品訓練卷積自編碼器，輸出熱力圖、分數、AUROC 與門檻<br>
<strong>【輸入與輸出】</strong>PCB 影像 &#91;B, 3, 128, 128&#93;（0–1）→ 重建 &#91;B, 3, 128, 128&#93;；分數 &#91;B&#93;<br>
<strong>【限制】</strong>訓練集<strong>只有良品</strong>；門檻只能用驗證集選；Colab T4；每個 epoch 存檢查點<br>
<span class="muted" style="font-size:16px">為什麼：用測試集選門檻等於偷看答案，回報的數字會太漂亮</span><br>
<strong>【驗收】</strong>① loss 持續下降　② 良品的重建圖看得出電路　③ 驗證集不良品平均分數高於良品　④ 測試集回報 AUROC、門檻下的過殺與漏檢

</div>

<!--
★ Specify（3 分）：限制裡的「只用驗證集選門檻」很重要：用測試集選門檻等於偷看答案，回報的數字會太漂亮。
-->

---

<div class="eyebrow">06 · Lab L2-1</div>

# Lab 5／7：Generate → Execute

<PromptBox>
這是 PyTorch 筆記本，請只填四個 # TODO：<br>
① ConvAE 的 encoder（四次 down：3→32→64→128→128）與 decoder（三次 up 再接 ConvTranspose2d(32,3) 與 Sigmoid）<br>
② 訓練迴圈的五行（loss ＝ MSE(x_hat, xb)）<br>
③ anomaly_map：每像素平方誤差、通道平均，回傳 &#91;B,H,W&#93;<br>
④ 門檻：驗證集不良品分數排序，最多允許 5% 漏檢<br>
不要用測試集選門檻。每一格說明每一行在做什麼。
</PromptBox>

<div class="steps mt-2" style="font-size:17px">
  <div><span class="num">1</span>訓練迴圈和 L03 一樣，只換模型和損失（x 同時是輸入和答案）</div>
  <div><span class="num">2</span>訓練 30 個 epoch 約 30 秒（講師 T4 實測）；跑完先看重建網格</div>
  <div><span class="num">3</span>沒有 Agent 額度：照第 13 頁、L03 的五行與筆記本註解填；卡住開 <code>-solution.ipynb</code></div>
</div>

<!--
★ 執行（約 20 分）。
-->

---

<div class="eyebrow">06 · Lab L2-1</div>

# Lab 6／7：Audit → Iterate

<table style="font-size:17px">
<thead><tr><th style="width:30%">稽核問題</th><th>具體動作</th><th style="width:30%">應該是</th></tr></thead>
<tbody>
<tr><td>訓練集真的只有良品？</td><td>看切分格印出的張數</td><td>train 的「不良」＝ 0</td></tr>
<tr><td>兩種拍攝方向都學了？</td><td>看「加入 180° 旋轉」那一行</td><td>訓練良品變兩倍</td></tr>
<tr><td>輸入和輸出範圍一致？</td><td>x 是 0–1；decoder 最後是 Sigmoid</td><td>都是 0–1</td></tr>
<tr><td>門檻用哪個資料集選？</td><td>找 <code>thr</code> 那一行</td><td>只用 <code>s_val</code></td></tr>
<tr><td>熱力圖亮在瑕疵上？</td><td>看 4 張不良品的熱力圖</td><td>明顯的瑕疵（如彎針）會亮；零件邊緣也會有一點亮（第 11 頁）</td></tr>
<tr><td>測試集數字合理？</td><td>比較 val 與 test 的過殺、漏檢</td><td>接近；test 漏檢可能略高於 5%</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">一次只改一件事：例如瓶頸窄一點（最後一層 down 的通道 128→32），比較 AUROC。</div>

<!--
★ 稽核（8 分）：最常見錯誤：Agent 拿 Normalize 把輸入變成 −1～1，但 decoder 用 Sigmoid 只能輸出 0～1 → 誤差永遠很大。
-->

---

<div class="eyebrow">06 · Lab L2-1 · Ship</div>

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

<img class="photo" src="/lab05-gradio-station.png" alt="Gradio 檢測站：標題「曜嶼電子（虛構）A 線瑕疵檢測站 · AE 基準版」、上傳 PCB 影像的區塊、Clear 與 Submit 按鈕、誤差熱力圖輸出" style="height:220px;width:100%;object-fit:contain"><div class="shot-cap">講師 Colab T4 實跑的檢測站（上傳前的畫面）</div>

</div>
</div>

<div class="takeaway mt-3">L04 的 Gradio，換成今天的 <code>anomaly_map</code> 與 <code>thr</code>：品保部可以自己上傳板子看熱力圖。</div>

<!--
★ Ship（5 分）：把門檻和分數一起顯示，複判人員才知道「差一點就判不良」的板子。heatmap() 在筆記本裡是用 matplotlib 色表轉成圖片。
-->

---

<div class="eyebrow">07 · Measure & Risk</div>

# 風險：這份資料能不能用？

<table class="mt-3" style="font-size:19px">
<thead><tr><th style="width:22%">資料集</th><th style="width:32%">授權</th><th>付費課程／公司產品</th></tr></thead>
<tbody>
<tr><td>VisA</td><td>CC BY 4.0（已確認）</td><td>可商用，需標示來源</td></tr>
<tr><td>MVTec AD</td><td>CC BY-NC-SA 4.0（待確認）</td><td>非商用：不能用</td></tr>
<tr><td>DeepPCB</td><td>標示不一致（待確認）</td><td>有疑義：先不用</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">技術上能跑的資料集，不一定能用在付費課程或公司產品；先讀授權。</div>

<div class="src">VisA：spot-diff README（S6，2026-11-24 確認）；MVTec AD、DeepPCB 以官方頁面為準（S7、S8，待確認）</div>

<!--
★ 風險（3 分）：漏檢與過殺的代價已在門檻那一頁講過；這頁只談授權。這也是為什麼本課選 VisA 而不是最有名的 MVTec AD（roadmap §9.2）。
-->

---

<div class="eyebrow">總整理</div>

# 今天學到的概念鏈

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-4">
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

# 隨堂檢核 1／2（iPAS 題型）：點選答案

<Mcq id="quiz1.q1" :n="1" :answer="1"
  :options="['只有不良品', '只有良品', '良品與不良品各半', '不需要資料']"
  :why="['要學的是「正常長什麼樣」；只學不良品，正常板反而會被判成異常。', '', '各半就變成分類問題，需要大量瑕疵標註；而且沒見過的新瑕疵照樣抓不到。', 'AE 要從資料學會重建，沒有資料就沒有模型。']"
  explain="只用良品訓練，AE 只會重建良品；瑕疵重建不好、誤差變大，就報警。">
用 AE（自編碼器）做異常偵測，訓練資料應該是？
</Mcq>

<Mcq id="quiz1.q2" :n="2" :answer="2"
  :options="['TP', 'FN', 'FP', 'TN']"
  :why="['TP 是不良品被正確抓到。', 'FN 是不良品被放過，也就是漏檢。', '', 'TN 是良品被正確放行。']"
  explain="過殺是良品被判成不良：真實為負、預測為正，就是 FP（False Positive）。">
「過殺」對應混淆矩陣的哪一格？（不良為正類）
</Mcq>

<FillClear group="quiz1" corner />

<!--
★ 檢核 1／2（2 分）：學員自己點；點錯會出現「再想想」和那個選項錯在哪，可以再點一次。答案：1 B、2 C。
-->

---

<div class="eyebrow">隨堂檢核</div>

# 隨堂檢核 2／2（iPAS 題型）：點選答案

<Mcq id="quiz2.q3" :n="3" :answer="0"
  :options="['過殺增加、漏檢減少', '過殺減少、漏檢增加', '兩者都減少', '兩者都不變']"
  :why="['', '這是門檻調高的結果。', '只動門檻，過殺和漏檢是蹺蹺板，不可能兩者都減少；要換更好的模型。', '門檻一動，被判成不良的板子數就會變。']"
  explain="門檻低，誤差稍大就報警：更多良品被判不良（過殺↑），瑕疵更少被放過（漏檢↓）。">
把門檻調低，通常會？
</Mcq>

<Mcq id="quiz2.q4" :n="4" :answer="1"
  :options="['完美', '和亂猜差不多', '門檻設錯', '過殺率 50%']"
  :why="['完美是 1.0。', '', 'AUROC 把所有門檻都算過一遍，和門檻設在哪裡無關。', 'AUROC 不是過殺率；過殺率要先選定一個門檻才算得出來。']"
  explain="AUROC ＝ 隨機挑一片不良、一片良品，不良那片分數比較高的機率；0.5 就是丟銅板。">
AUROC ＝ 0.5 代表？
</Mcq>

<FillClear group="quiz2" corner />

<!--
★ 檢核 2／2（2 分）。答案：3 A、4 B。
全部答案與理由：1 B、2 C、3 A、4 B。
-->

---
hostOnly: true
---

<div class="eyebrow">下一步</div>

# 下一堂 L06：告訴我瑕疵在哪、有多大

<div class="node node--primary mt-2">維修站不只要「這片有問題」，還要每個瑕疵的位置與面積。下一堂在今天的主角圖上加「跳接」，變成 U-Net；但沒有瑕疵遮罩怎麼訓練？我們自己合成瑕疵。</div>

<!--
★ 只給講師的託管版看。
-->
