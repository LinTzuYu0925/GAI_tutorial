---
theme: default
title: AE 熱圖太模糊？用擴散模型修好板子再比對
info: |
  生成式AI原理 · D3-4
  D2-1 的 AE 重建太模糊，細紋路一直過殺。把板子加噪到第 t 步、再用擴散模型去噪回來，得到「這片板子的正常版」；和 AE 比 AUROC、過殺與每片幾毫秒。第三天總整理、iPAS 小考與作業。
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
exportFilename: 12-diffusion-anomaly
layout: center
class: cover
---

<div class="eyebrow">生成式AI原理 · D3-4</div>

# AE 熱圖太模糊？用擴散模型修好板子再比對

<p class="subtitle">加噪到一半、再擦回來：得到「這片板子的正常版」，和原圖相減就是瑕疵</p>

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-8">
  <span class="chip">AE 太糊 → 過殺</span><span class="arrow">→</span>
  <span class="chip">加噪到第 t 步</span><span class="arrow">→</span>
  <span class="chip">去噪回來</span><span class="arrow">→</span>
  <span class="chip">t 選多少？</span><span class="arrow">→</span>
  <span class="chip">DDIM 省時間</span><span class="arrow">→</span>
  <span class="chip">趕得上節拍嗎？</span>
</div>

<!--
★ 開場（2 分）：第三天最後一堂。D2-1 的品保部回來了：昨天（D3-3）學會的「加噪、去噪」原封不動拿來做檢測，只是起點不是純雜訊。
-->

---

<div class="eyebrow">00 · Frame（定義問題）</div>

# 品保部 A 線回來了：AE 熱圖太模糊，細紋路一直過殺

<div class="ticket mt-2">
  <div class="ticket-head">【需求單 #D3-4】部門：製造品保部（A 線）<span>公司：曜嶼電子 <span class="fiction" style="color:#fff;border-color:#fff">虛構</span></span></div>
  <dl>
    <dt>問題</dt><dd>D2-1 的 AE 重建偏模糊，板子上的細紋路、文字誤差大，被判成瑕疵（過殺）</dd>
    <dt>現況痛點</dt><dd>過殺的板子要人工複判，複判人力沒有減少</dd>
    <dt>成功指標（KPI）</dt><dd>漏檢 ≤ 5% 時，過殺比 AE 低；每片處理時間趕得上產線節拍時間</dd>
    <dt>可用資料</dt><dd>D2-1 的 VisA PCB1 切分（同一批訓練、驗證、測試板子）</dd>
    <dt>限制與法規</dt><dd>Colab T4；講師在良品上訓練好的擴散模型檢查點；64 × 64</dd>
    <dt>為何現有工具不夠</dt><dd>AE 的重建一定要擠過瓶頸，細節回不來 → 細節處誤差大</dd>
  </dl>
</div>

<!--
★ 需求單（2 分）：過殺／漏檢是 D2-1 的工廠用語（過殺＝FP、漏檢＝FN）。今天多一個指標：時間。產線每隔幾秒就送來一片板子（節拍時間），檢測太慢就會塞車。
-->

---

<div class="eyebrow">學習目標</div>

# 今天結束時，你能夠……

1. **說明**「加噪到第 t 步、再去噪」為什麼會得到一片正常的板子
2. **選擇**加噪步數 t，說出太小、太大各會怎樣
3. **用** DDIM 縮短每片的檢測時間，並換算成每秒幾片
4. **比較** AE 和擴散：AUROC、過殺、每片毫秒數 vs 節拍時間
5. **整理**第三天的生成三難表格，當成學習評量備忘錄的證據

<!--
★ 目標（1 分）。不教：simplex 雜訊的實作（○ 點名）、DDAD（△ 點名）、PatchCore／EfficientAD 的實作（D2-1 點名過）。
-->

---

<div class="eyebrow">00 · Frame · 驗收標準</div>

# 準度和速度都要過關

<table class="mt-2" style="font-size:18px">
<thead><tr><th style="width:30%">指標</th><th>怎麼量</th><th style="width:28%">今天的門檻</th></tr></thead>
<tbody>
<tr><td>AUROC</td><td>不挑門檻，看良品和不良品的分數排得開不開（D2-1）</td><td>比 AE 高</td></tr>
<tr><td>過殺（漏檢 ≤ 5% 時）</td><td>門檻在驗證集上選，讓不良品最多漏 5%；再到測試集算一次</td><td>比 AE 低</td></tr>
<tr><td>每片幾毫秒</td><td>64 片一批，總時間 ÷ 64</td><td>≤ 節拍時間</td></tr>
</tbody>
</table>

<div class="node node--warm mt-3" style="font-size:18px"><strong>節拍時間（takt time）</strong><small>產線每隔多久送來一片板子。今天假設 1 秒／片（虛構；筆記本的 <code>TAKT_S</code> 可以改成你們產線的數字）</small></div>

<div class="takeaway mt-3">檢測比節拍慢，產線就要等：準度再好，也上不了線。</div>

<!--
★ 驗收（3 分）：takt time（節拍時間）。1 秒是課堂假設，不是業界標準；請學員想想自己待過的產線大約多少。三個指標都由 lab12 在同一個測試集上量。
-->

---

<div class="eyebrow">01 · Try（先看結果）</div>

# 擴散模型把有瑕疵的板子「修好」

<div class="placeholder mt-2" style="height:280px;padding:16px 24px">4 片測試集不良品：原圖 → 擴散「修好」的版本 → 誤差圖 → 真正的瑕疵遮罩<small>講師 T4 實跑後替換（lab12 <code>repair_examples.png</code>）</small></div>

<div class="takeaway mt-3">先猜：修好的版本裡，瑕疵還在嗎？板子上的元件和文字還在嗎？</div>

<div class="src">VisA PCB1（Zou et al., 2022，CC BY 4.0，S4），64 × 64</div>

<!--
★ 示範（4 分）：講師用 lab12 解答筆記本跑好的圖。先只看前兩列（原圖、修好的版本），請學員找出差異在哪；再看誤差圖和遮罩對答案。
-->

---

<div class="eyebrow">02 · Open（打開黑盒子）· 部分加噪</div>

# 不從純雜訊開始：加噪到第 t 步，再擦回來

<div class="flex items-center justify-center gap-2 mt-4" style="font-size:17px">
  <div class="node" style="width:17%">x₀<small>有瑕疵的板子</small></div><span class="arrow">→</span>
  <div class="node node--warm" style="width:19%"><strong>加噪到第 t 步</strong><small>一行 q_sample（D3-3）</small></div><span class="arrow">→</span>
  <div class="node" style="width:15%">x_t<small>瑕疵被雜訊蓋住</small></div><span class="arrow">→</span>
  <div class="node node--primary" style="width:19%"><strong>擴散模型去噪</strong><small>只看過良品</small></div><span class="arrow">→</span>
  <div class="node" style="width:17%">x̂₀<small>「正常版」的板子</small></div>
</div>

<div class="grid grid-cols-2 gap-6 mt-4" style="font-size:18px">
<div class="node"><strong>D3-3 的取樣</strong><small>從 t＝999 的純雜訊開始 → 畫出「任何一件」衣服</small></div>
<div class="node node--primary"><strong>今天</strong><small>從 t＝150 左右開始 → 板子的大結構還在，模型只補細節；瑕疵被當成雜訊擦掉</small></div>
</div>

<div class="takeaway mt-3">模型只看過良品，所以它「擦回來」的一定是良品的樣子：瑕疵沒有被畫回來。</div>

<div class="src">部分擴散（partial diffusion）：AnoDDPM，Wyatt et al., CVPR Workshops 2022（S1）</div>

<!--
★ 部分加噪（6 分）：partial diffusion（部分加噪）。和 D3-3 第 13 頁的練習連起來：t＝250 時短靴還看得出來，代表大結構還在。t 的數值待第 8 頁實驗決定；150 只是示意的起點。
-->

---

<div class="eyebrow">02 · Open · 誤差圖</div>

# 誤差圖和 D2-1 一樣算，只是重建更清楚

<div class="grid grid-cols-[1.3fr_1fr] gap-6 mt-2">
<div>

<div class="placeholder" style="height:250px;padding:16px 24px">同一片不良品：AE 的重建與誤差圖 vs 擴散的重建與誤差圖<small>講師 T4 實跑後替換（lab12 <code>t_three.png</code> 的右兩欄）</small></div>

</div>
<div style="font-size:18px">

```python
emap  = ((x - r) ** 2).mean(1)     # 每個像素的平方誤差
score = 誤差最大 1% 的平均            # D2-1 同一個分數
```

- AE：重建 r 要擠過瓶頸 → 模糊 → 細紋路處也有誤差
- 擴散：重建保留細節 → 誤差集中在瑕疵

</div>
</div>

<div class="takeaway mt-3">分數和門檻的算法完全不變，只換了「重建」這一步：差別全在重建清不清楚。</div>

<!--
★ 誤差圖（4 分）：「誤差集中在瑕疵」是我們希望的結果，要等測試集的數字（第 13 頁）才知道是否成立。讀 code：emap 讀作「原圖減重建，平方，三個通道平均」。
-->

---

<div class="eyebrow">02 · Open · 選 t</div>

# t 太小留下瑕疵，t 太大連板子都換掉

<div class="placeholder mt-2" style="height:250px;padding:16px 24px">同一片不良品：t＝25、150、500 修好的版本與誤差圖<small>講師 T4 實跑後替換（lab12 <code>t_three.png</code>）</small></div>

<div class="grid grid-cols-3 gap-4 mt-3" style="font-size:17px">
<div class="node"><strong>t 太小</strong><small>雜訊蓋不住瑕疵 → 瑕疵被原樣「擦回來」→ 誤差小 → 漏檢</small></div>
<div class="node node--primary"><strong>t 剛好</strong><small>瑕疵被蓋住、板子結構還在</small></div>
<div class="node node--warm"><strong>t 太大</strong><small>元件位置、文字也被重畫 → 良品也有誤差 → 過殺</small></div>
</div>

<div class="takeaway mt-2">t 是今天唯一要調的旋鈕：在驗證集上掃一輪，挑 AUROC 最高的。</div>

<div class="src">AnoDDPM：太小的雜訊抓不到大的異常（S1）</div>

<!--
★ 選 t（4 分）：和 D3-3 練習的結論連起來：t＝500 時短靴已經認不出來，板子也一樣。
-->

---

<div class="eyebrow">02 · Open · 練習</div>

# 練習：t 該選多少？

<div class="muted" style="font-size:17px">不用 AI。① 先猜「驗證集 AUROC 最高的 t」② 執行 lab12 第 4 部分的掃描格 ③ 填 AUROC。第一列已填好（AE 對照）。</div>

<table class="fill tight vlines mt-1">
<thead><tr><th style="width:28%">做法</th><th style="width:36%">驗證集 AUROC</th><th>一句話：為什麼？</th></tr></thead>
<tbody>
<tr><td>AE（D2-1）</td><td>實跑後填入</td><td>重建模糊，細紋路也有誤差</td></tr>
<tr><td>先猜：最好的 t ＝</td><td class="blank"><FillIn id="tsel.guess" hint="例：t＝……" /></td><td class="blank"><FillIn id="tsel.why" /></td></tr>
<tr><td>擴散 t＝25</td><td class="blank"><FillIn id="tsel.a25" /></td><td class="blank"><FillIn id="tsel.w25" /></td></tr>
<tr><td>擴散 t＝150</td><td class="blank"><FillIn id="tsel.a150" /></td><td class="blank"><FillIn id="tsel.w150" /></td></tr>
<tr><td>擴散 t＝400</td><td class="blank"><FillIn id="tsel.a400" /></td><td class="blank"><FillIn id="tsel.w400" /></td></tr>
<tr><td>實際最好的 t ＝</td><td class="blank" colspan="2"><FillIn id="tsel.best" /></td></tr>
</tbody>
</table>

<FillClear group="tsel" />

<!--
★ 無 AI 檢核點（8 分）：個人作業，不收回。掃描在 T4 上的時間待實測；等待時請學員先填「先猜」那一列。重點是發現 AUROC 對 t 的曲線有高有低，不是越大越好。
-->

---
hostOnly: true
---

<div class="eyebrow">02 · Open · 練習解答</div>

# 練習解答：t 的曲線先升後降

<div class="placeholder" style="height:210px;padding:16px 24px">驗證集 AUROC vs t（擴散）與 AE 的水平線<small>講師 T4 實跑後替換（lab12 <code>t_sweep.png</code>）</small></div>

<table class="vlines mt-2" style="font-size:17px">
<thead><tr><th>做法</th><th>AE</th><th>t＝25</th><th>t＝150</th><th>t＝400</th><th>最好的 t</th></tr></thead>
<tbody>
<tr><td>驗證集 AUROC</td><td>實跑後填入</td><td>實跑後填入</td><td>實跑後填入</td><td>實跑後填入</td><td>實跑後填入</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">怎麼判斷：最好的 t 落在中間；太小、太大都比較差。t 要在驗證集上選，不能看測試集。</div>

<!--
★ 解答（2 分）：數字來自講師 T4 實跑（SEED 0，research/lab-runs.md）；學員的數字會略有不同，因為加噪是隨機的。
-->

---

<div class="eyebrow">03 · Adapt（調整）· DDIM</div>

# DDIM：從 t 跳回 0，只走幾步

<div class="grid grid-cols-[1.15fr_1fr] gap-6 mt-2">
<div>

```python
for t, t_prev in zip(ts[:-1], ts[1:]):         # 例：150 → 143 → … → 0
    eps_hat = net(x_t, t)                       # 猜雜訊
    x0_hat = (x_t - s1mab[t]*eps_hat) / sab[t]  # 估出乾淨版
    x_t = sab[t_prev]*x0_hat + s1mab[t_prev]*eps_hat   # 放回 t_prev
```

</div>
<div>

<div class="placeholder" style="height:200px;padding:16px 24px">步數 vs 驗證集 AUROC vs 每片毫秒<small>講師 T4 實跑後替換（lab12 第 5 部分的表）</small></div>

</div>
</div>

<div class="muted mt-2" style="font-size:16px">讀法：先用猜到的雜訊估出「乾淨版」x̂₀，再把它加回「比較少」的雜訊，跳到下一個步數。不加新的隨機雜訊，所以可以跳大步。</div>

<div class="takeaway mt-2">每步都走＝網路跑 t 次；DDIM 20 步＝跑 20 次：時間差好幾倍，準度要量了才知道掉多少。</div>

<div class="src">Song et al., DDIM, ICLR 2021（S2）；D3-3 第 17 頁</div>

<!--
★ DDIM（5 分）：D3-3 用的是 diffusers 的 DDIMScheduler；今天把同一件事寫成四行，好看清楚每一步在做什麼。第 3 行就是 D3-3 一行公式反過來解 x₀。
-->

---

<div class="eyebrow">03 · Measure · 節拍時間</div>

# 每片幾毫秒，換算成趕不趕得上產線

<div class="grid grid-cols-2 gap-6 mt-3">
<div style="font-size:19px">

**照著算**（例子的數字是假設，不是實測）：

- 每片 40 ms → 每秒 1000 ÷ 40 ＝ **25 片**
- 節拍 1 秒／片 → 一秒只需要 1 片 → **趕得上**
- 每片 1,500 ms → 每秒 0.67 片 → **趕不上**

</div>
<div>

<div class="placeholder" style="height:210px;padding:16px 24px">實測：AE、擴散每步都走、擴散 DDIM 的每片毫秒與每秒片數<small>講師 T4 實跑後替換（lab12 第 6 部分）</small></div>

</div>
</div>

<div class="takeaway mt-3">每秒片數 ＝ 1000 ÷ 每片毫秒；要 ≥ 1 ÷ 節拍秒數，才趕得上。</div>

<!--
★ 節拍（4 分）：throughput（處理量、每秒幾片）。左邊是算法練習，數字是假設；右邊是 T4 實測。提醒：Colab T4 不等於產線的電腦，上線前要在實際硬體上重量。
-->

---

<div class="eyebrow">03 · Measure · 對照表</div>

# AE vs 擴散：在同一個測試集上比

<table class="mt-2" style="font-size:18px">
<thead><tr><th style="width:30%">做法</th><th>AUROC</th><th>過殺（漏檢 ≤ 5% 的門檻）</th><th>漏檢</th><th>每片 ms</th><th>趕得上 1 秒節拍？</th></tr></thead>
<tbody>
<tr><td>AE（D2-1）</td><td>實跑後填入</td><td>實跑後填入</td><td>實跑後填入</td><td>實跑後填入</td><td>實跑後填入</td></tr>
<tr><td>擴散，每步都走</td><td>實跑後填入</td><td>實跑後填入</td><td>實跑後填入</td><td>實跑後填入</td><td>實跑後填入</td></tr>
<tr><td>擴散，DDIM</td><td>實跑後填入</td><td>實跑後填入</td><td>實跑後填入</td><td>實跑後填入</td><td>實跑後填入</td></tr>
</tbody>
</table>

<div class="muted mt-2" style="font-size:16px">門檻在驗證集選，測試集只算一次。測試集只有 151 片良品、50 片不良品：1 片就是 0.7% 或 2%，差一兩片不代表一定比較好。</div>

<div class="takeaway mt-2">需求單問的是「過殺有沒有比 AE 低、趕不趕得上節拍」：兩個都要回答。</div>

<!--
★ 對照表（5 分）：這是今天交給品保部的核心數字（Lab 7／7 會抄一次）。測試集張數來自 D2-1 的切分（良品 1004 的 15%、不良品 100 的一半）。
-->

---

<div class="eyebrow">04 · Ship · 給作業員看</div>

# 給作業員看「修好的板子」，不只是一個分數

<div class="grid grid-cols-[1fr_1.1fr] gap-6 mt-2">
<div>

<div class="placeholder" style="height:260px;padding:16px 24px">作業員畫面：左原圖、中「正常版」、右誤差熱力圖，標出分數與判定<small>示意，講師 T4 實跑後用 lab12 <code>repair_examples.png</code> 的一片替換</small></div>

</div>
<div style="font-size:18px">

- AE 的重建糊成一片，作業員看不出「哪裡不一樣」
- 擴散的「正常版」清楚：原圖和正常版並排，眼睛就能比
- 複判時間短，判錯也找得到原因

</div>
</div>

<div class="takeaway mt-3">能解釋的檢測比較容易被產線接受：讓作業員看到「應該長怎樣」。</div>

<!--
★ 作業員畫面（3 分）：explainability（可解釋性）。這頁接 D2-1 的 Gradio 檢測站：把「修好的版本」也放進去，就是三欄畫面。
-->

---

<div class="eyebrow">04 · Adapt · 選修</div>

# 產線上常見的其他做法

<table class="mt-2" style="font-size:17px">
<thead><tr><th style="width:24%">方法</th><th>做什麼</th><th style="width:28%">和今天比</th></tr></thead>
<tbody>
<tr><td>PatchCore</td><td>記住良品的小區塊特徵，比對最近的距離（D2-1 點名過）</td><td>不用生成，通常很快</td></tr>
<tr><td>EfficientAD</td><td>小網路學老師網路的特徵，毫秒級</td><td>為速度設計</td></tr>
<tr><td>simplex 雜訊</td><td>AnoDDPM 把高斯雜訊換成一塊一塊的 simplex 雜訊，蓋得住比較大的瑕疵</td><td>今天的改良版</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">擴散不是唯一答案：上線前要和這些基準比過。</div>

<div class="src">Roth et al., CVPR 2022；Batzner et al., WACV 2024（S7，待確認）；AnoDDPM（S1）</div>

<!--
○ 選修（3 分）：simplex noise（simplex 雜訊）。AnoDDPM 的觀察：高斯雜訊蓋不住大的異常（S1）。PatchCore、EfficientAD 的細節不教。
-->

---

<div class="eyebrow">附錄 · 備用</div>

# DDAD：讓去噪「參考」原圖（只認名字）

<div style="font-size:19px" class="mt-4">

- 今天的問題：t 大一點，模型就自由發揮，連正常的地方都改掉
- DDAD：去噪的每一步都「看著」輸入的板子，只修不像良品的地方
- 論文報告在 VisA 上影像層級 AUROC 98.9%（論文的數字，不是我們的）

</div>

<div class="takeaway mt-4">看到「conditioned denoising」的異常偵測，知道是在解決今天「t 太大會改掉板子」的問題。</div>

<div class="src">Mousakhan et al., arXiv:2305.15956（S5）</div>

<!--
△ 備用（2 分）：學員問「能不能讓它別亂改」時再講。
-->

---

<div class="eyebrow">05 · Lab L3-4</div>

# Lab 1／7：我們要做出什麼？

<div class="grid grid-cols-2 gap-6 mt-2" style="font-size:19px">
<div>

**打開筆記本**：<code>lab12-diffusion-ad.ipynb</code>（在 <code>materials/</code>）→ Open in Colab<br>
執行階段：**T4 GPU**；資料：VisA PCB1（約 1.9 GB，自動下載）

1. 擴散的過殺比 AE 低嗎？
2. 最好的 t 是多少？
3. 每片幾毫秒？趕得上 1 秒的節拍嗎？

</div>
<div>

<div class="placeholder" style="height:250px;padding:16px 24px">目標：t 掃描曲線、步數表、AE vs 擴散對照表、作業員畫面<small>講師 T4 實跑後替換（含 VRAM 峰值與總時間）</small></div>

</div>
</div>

<div class="takeaway mt-3">交給品保部：一張「AUROC、過殺、每片毫秒」對照表，加上一句建議。</div>

<!--
★ Lab 開始（3 分）：先執行第 1 格和資料那一格（下載 VisA）。D2-1 下載過的，把 DATA_DIR 改成雲端硬碟資料夾。擴散模型預設下載講師的檢查點（TRAIN_DDPM＝False）；下載不到會自動改成自己訓練。沒有 GPU → EPOCHS_AE＝3、EVAL_N＝20、STEPS_DDPM＝200。
-->

---

<div class="eyebrow">05 · Lab L3-4</div>

# Lab 2／7：筆記本拆成哪幾塊？

<div class="steps mt-2" style="font-size:17px">
  <div><span class="num">1</span><strong>資料</strong>：和 D2-1 同一個切分；訓練良品加 180° 旋轉；驗證、測試各有良品和不良品</div>
  <div><span class="num">2</span><strong>AE 對照組</strong>：D2-1 的 AE；<code>evaluate</code> 回傳重建、誤差圖、分數、每片毫秒</div>
  <div><span class="num">3</span><strong>擴散模型</strong>：D3-3 的 <code>TinyUNet</code>（3 通道、64 × 64）；載入講師檢查點</div>
  <div><span class="num">4</span><strong><code>diffusion_repair</code></strong>：加噪到 t（TODO ①）、DDIM 走回 0；t 掃描</div>
  <div><span class="num">5</span><strong>測試</strong>：步數表；<code>report</code>（TODO ②：過殺、漏檢、AUROC）；作業員畫面</div>
</div>

<div class="takeaway mt-3">兩個 TODO：加噪那一行（D3-3 學過），和過殺、漏檢、AUROC（D2-1 學過）。</div>

<!--
★ 拆塊（3 分）：今天沒有新的網路，全部是 D2-1 和 D3-3 的零件重組。
-->

---

<div class="eyebrow">05 · Lab L3-4</div>

# Lab 3／7：Specify

<div style="font-size:18px" class="mt-2">

<strong>【目標】</strong>用「加噪到第 t 步、再去噪」做 PCB1 的瑕疵檢測，和 D2-1 的 AE 比準度與速度<br>
<strong>【輸入與輸出】</strong>板子 <code>&#91;B,3,64,64&#93;</code>（0～1）→ 修好的板子 <code>&#91;B,3,64,64&#93;</code> → 誤差圖 <code>&#91;B,64,64&#93;</code> → 分數 <code>&#91;B&#93;</code><br>
<strong>【限制】</strong>t 和步數只能在**驗證集**上選；門檻也在驗證集上選；測試集只算一次；Colab T4<br>
<span class="muted" style="font-size:16px">為什麼：在測試集上挑 t，等於偷看考題，數字會好看得不真實</span><br>
<strong>【驗收】</strong>① 修好的板子 shape 和輸入一樣　② t 掃描有高有低，挑最高的　③ 對照表三列都有 AUROC、過殺、漏檢、毫秒　④ 寫一句建議：上線用 AE 還是擴散、用幾步

</div>

<!--
★ Specify（3 分）：驗收寫的是「要做到什麼」，不是預測結果。擴散一定比 AE 好嗎？不一定，T4 實跑才知道。
-->

---

<div class="eyebrow">05 · Lab L3-4</div>

# Lab 4／7：Generate → Execute

<PromptBox>
這是 PyTorch 筆記本，請只填兩個 # TODO：<br>
① diffusion_repair：x_t ＝ sab&#91;t_start&#93; · x0 ＋ s1mab&#91;t_start&#93; · 隨機雜訊（用 generator g）<br>
② report：over ＝ 良品分數 ＞ thr 的比例；miss ＝ 不良品分數 ≤ thr 的比例；auroc ＝ roc_auc_score(y, s)<br>
不要改 t 的清單、步數和門檻的選法。每一格說明每一行在做什麼。
</PromptBox>

<div class="steps mt-2" style="font-size:17px">
  <div><span class="num">1</span>VisA 下載、AE 訓練、t 掃描的時間待 T4 實測；等待時做「練習：t 該選多少？」的先猜</div>
  <div><span class="num">2</span>沒有 Agent 額度：照「部分加噪」頁和 D2-1 的過殺／漏檢填；卡住開 <code>-solution.ipynb</code></div>
  <div><span class="num">3</span>預期輸出：<code>t=25  驗證集 AUROC …  每張 … ms</code>，一共 6 行</div>
</div>

<div class="node node--warm mt-2" style="font-size:16px"><strong>常見錯誤</strong><small>加噪寫成 <code>torch.randn(...)</code>（純雜訊）：那是 D3-3 的取樣起點，模型會畫出「任何一片」板子，和輸入對不上，每片都過殺</small></div>

<!--
★ 執行（約 16 分）：常見錯誤第二名：門檻在測試集上選（看 threshold_for_miss 用的是 s_val）。
-->

---

<div class="eyebrow">05 · Lab L3-4</div>

# Lab 5／7：看修好的板子、對照預測

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-2" style="font-size:18px">
<div>

跑完第 4 部分後：

1. t＝25 的版本，瑕疵還在嗎？t＝500 的版本，元件還在原位嗎？
2. 你猜的 t 和實際最好的 t 差多少？
3. AE 的誤差圖和擴散的誤差圖，哪一個比較集中在瑕疵？

</div>
<div>

<div class="node node--primary"><strong>和隔壁同學比</strong><small>加噪是隨機的：同樣的 t，不同的 seed，AUROC 會差一點。差多少？這也是要報告的「不確定」</small></div>

</div>
</div>

<div class="takeaway mt-4">「修得好不好」用眼睛看，「選哪個 t」用驗證集的數字決定。</div>

<!--
★ 對照（5 分）：第 3 題連到第 7 頁：我們希望擴散的誤差集中在瑕疵，以實跑結果為準。
-->

---

<div class="eyebrow">05 · Lab L3-4</div>

# Lab 6／7：Audit → Iterate

<table style="font-size:15px">
<thead><tr><th style="width:28%">稽核問題</th><th>具體動作</th><th style="width:32%">應該是</th></tr></thead>
<tbody>
<tr><td>加噪的起點是輸入的板子嗎？</td><td>看 TODO ① 那一行</td><td>有 <code>x0</code>，不是純 <code>randn</code></td></tr>
<tr><td>t 是在哪裡選的？</td><td>看 <code>sweep</code> 用的資料</td><td><code>data&#91;"val"&#93;</code></td></tr>
<tr><td>門檻是在哪裡選的？</td><td>看 <code>threshold_for_miss</code> 的輸入</td><td>驗證集分數 <code>s_val</code></td></tr>
<tr><td>測試集漏檢真的 ≤ 5% 嗎？</td><td>看對照表的漏檢欄</td><td>接近 5%；差一點是正常（測試集只有 50 片不良）</td></tr>
<tr><td>毫秒怎麼量的？</td><td>看 <code>evaluate</code></td><td>有 <code>cuda.synchronize()</code>，64 片一批</td></tr>
<tr><td>擴散比 AE 好嗎？</td><td>對照表</td><td>講師實跑後填入</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">一次只改一件事：例如把 DDIM 步數從 20 改成 5，看 AUROC 掉多少、快多少。</div>

<!--
★ 稽核（6 分）：第 5 列：GPU 是非同步的，不 synchronize 就計時，量到的是「把工作丟出去」的時間，會少算很多。
-->

---

<div class="eyebrow">05 · Lab L3-4 · Ship</div>

# Lab 7／7：交給品保部的建議

<table class="fill tight vlines mt-2">
<thead><tr><th style="width:34%">項目</th><th>你的數字（T4）</th></tr></thead>
<tbody>
<tr><td>AE：AUROC／過殺／每片 ms</td><td class="blank"><FillIn id="ship.ae" hint="例：0.……／……%／…… ms" /></td></tr>
<tr><td>擴散（t＝？、DDIM ？步）：AUROC／過殺／每片 ms</td><td class="blank"><FillIn id="ship.diff" /></td></tr>
<tr><td>趕得上 1 秒節拍嗎？</td><td class="blank"><FillIn id="ship.takt" /></td></tr>
<tr><td>建議：上線用哪一個？為什麼？</td><td class="blank"><FillIn id="ship.rec" hint="例：先用……，因為過殺……，速度……" /></td></tr>
</tbody>
</table>

<FillClear group="ship" />

<div class="takeaway mt-2">建議要包含代價：「擴散的過殺 ＿＿，但每片慢 ＿＿ 倍；在 ＿＿ 節拍下還趕得上」。</div>

<!--
★ Ship（4 分）：講師實跑的答案寫在第 13 頁的對照表。如果擴散沒有贏，照實寫：「這個設定下 AE 仍然比較好」也是有價值的結論。
-->

---

<div class="eyebrow">06 · Measure & Risk（風險）</div>

# 風險：同一套技術，也能做出假的代言廣告

<div class="grid grid-cols-2 gap-6 mt-3" style="font-size:18px">
<div class="node node--warm"><strong>修板子 vs 改照片</strong><small>今天的「加噪再去噪」是在改一張真實的照片。同樣的技術加上條件（D4），就能把真人改成在說他沒說過的話、代言他沒代言的產品</small></div>
<div class="node"><strong>台灣的規定</strong><small>詐欺犯罪危害防制條例第 31 條：網路廣告平臺刊登廣告時，要揭露「廣告使用深度偽造技術或人工智慧生成之個人影像」</small></div>
</div>

<div class="takeaway mt-4">公司用 AI 做含有人像的廣告：要有當事人同意，並準備好讓平臺揭露。</div>

<div class="src">詐欺犯罪危害防制條例第 31 條第 1 項第 4 款、第 4 項（深度偽造定義）、第 40 條（罰鍰），全國法規資料庫（S6）</div>

<!--
★ 風險（4 分）：揭露義務在「網路廣告平臺業者」（而且是達一定規模者，第 27 條），不是直接規定廣告主；但廣告主要提供資訊給平臺。未揭露的罰鍰 20 萬到 500 萬元（第 40 條）。D3-2 已經提過 deepfake 與同意，今天補上法條。
-->

---

<div class="eyebrow">第三天總整理</div>

# 第三天的生成三難表格

<table class="mt-2" style="font-size:17px">
<thead><tr><th style="width:18%">單元</th><th style="width:22%">模型</th><th>品質</th><th>多樣性</th><th>速度</th><th style="width:24%">你的證據</th></tr></thead>
<tbody>
<tr><td>D3-1</td><td>DCGAN、Real-ESRGAN</td><td>✓</td><td>沒保證</td><td>✓ 1 次</td><td>網格、兩兩距離</td></tr>
<tr><td>D3-2</td><td>CycleGAN</td><td>✓</td><td>—（轉換）</td><td>✓ 1 次</td><td>過殺、瑕疵存活</td></tr>
<tr><td>D3-3</td><td>DDPM、DDIM</td><td>✓</td><td>✓</td><td>✗ 1000 次</td><td>兩兩距離、秒數</td></tr>
<tr><td>D3-4</td><td>部分加噪＋DDIM</td><td>✓ 修得清楚</td><td>—（重建）</td><td>t 步或幾步</td><td>AUROC、每片 ms</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">GAN 一次畫完但多樣性沒保證；擴散多樣、好訓練但要走很多步：這就是學習評量要你用自己的數字解釋的取捨。</div>

<!--
★ 第三天總整理（4 分）：請學員把每一列換成自己 lab 的數字。D4-1 會開始做「條件式生成」（學習評量的第二部分）。
-->

---

<div class="eyebrow">第三天 · iPAS 小考</div>

# 第三天小考 1／3（iPAS 題型）：點選答案

<Mcq id="quiz1.q1" :n="1" :answer="1"
  :options="['互相合作', '一個偽造、一個鑑定，互相對抗', '共用參數', '輪流當分類器']"
  :why="['兩者目標相反：G 想騙過 D，D 想抓出 G。', '', 'G 和 D 是兩個獨立的網路，各有各的參數。', 'G 一直是生成器，D 一直是鑑別器，不會輪流。']"
  explain="G 偽造、D 鑑定，兩邊輪流訓練、互相對抗，G 就越畫越像。">
GAN 的生成器和鑑別器的關係？
</Mcq>

<Mcq id="quiz1.q2" :n="2" :answer="2"
  :options="['過擬合', '梯度消失', 'mode collapse', '分布偏移']"
  :why="['過擬合是把訓練集背起來；這裡是 G 只會畫少數幾種。', '梯度消失是訓練學不動，圖通常也不會清楚。', '', '分布偏移是資料換了來源（例如換相機），不是生成器的問題。']"
  explain="G 找到一種能騙過 D 的圖就一直畫它，多樣性崩掉，叫 mode collapse（模式崩潰）。">
「生成的圖很清楚，但幾乎都長一樣」稱為？
</Mcq>

<FillClear group="quiz1" corner />

<!--
★ 檢核 1／3（2 分）：學員自己點；點錯會出現「再想想」和那個選項錯在哪，可以再點一次。答案：1 B、2 C。
-->

---

<div class="eyebrow">第三天 · iPAS 小考</div>

# 第三天小考 2／3（iPAS 題型）：點選答案

<Mcq id="quiz2.q3" :n="3" :answer="0"
  :options="['F(G(b)) 和 b 一樣', 'G(b) 和 b 一樣', 'D 判成真', '兩個 G 參數相同']"
  :why="['', 'G(b) 要像 A 線，不該和 b 一樣；這是最常見的錯誤。', '這是對抗損失，不是循環一致。', '兩個生成器方向相反，參數各自學。']"
  explain="b 轉到 A 線再轉回來，F(G(b)) 要和原本的 b 一樣，板子的內容才不會在轉換中被換掉。">
CycleGAN 的循環一致損失要求？
</Mcq>

<Mcq id="quiz2.q4" :n="4" :answer="2"
  :options="['乾淨的原圖', '類別', '加進去的雜訊', '鑑別器分數']"
  :why="['有些模型改成預測 x₀，但標準 DDPM（也是本課 lab 的做法）預測的是 ε。這是常見誤解。', '類別標籤是條件，不是要預測的目標。', '', 'DDPM 沒有鑑別器，那是 GAN。']"
  explain="加進去的雜訊是自己抽的，答案已知：網路看 x_t 和 t 猜出 ε，和真的 ε 比 MSE。">
DDPM 訓練時，網路要預測？
</Mcq>

<FillClear group="quiz2" corner />

<!--
★ 檢核 2／3（2 分）。答案：3 A、4 C。
-->

---

<div class="eyebrow">第三天 · iPAS 小考</div>

# 第三天小考 3／3（iPAS 題型）：點選答案

<Mcq id="quiz3.q5" :n="5" :answer="1"
  :options="['瑕疵留下來，漏檢', '正常的結構也被重畫，過殺', '速度變快', '沒有影響']"
  :why="['瑕疵留下來是 t 太小：雜訊不夠蓋掉瑕疵。', '', '加噪越多，去噪要走的步數越多，不會變快。', 't 是這個方法最重要的旋鈕：AUROC 隨 t 有高有低。']"
  explain="t 太大，連正常的細紋路都被雜訊蓋掉、重畫成別的樣子，正常板也和原圖差很多，就過殺。">
用擴散做異常偵測時，加噪步數 t 太大會？
</Mcq>

<Mcq id="quiz3.q6" :n="6" :answer="2"
  :options="['不用訓練網路', '多樣性變高', '用同一個網路、少走很多步', '不需要 GPU']"
  :why="['網路還是要訓練，只是不用「重新」訓練：DDPM 訓練好的網路直接拿來用。', 'DDIM 常用決定性取樣，多樣性不會因此變高。', '', 'DDIM 照樣要跑網路，只是次數少很多。']"
  explain="DDIM 換了取樣公式，同一個 DDPM 網路跳著走、少走很多步，速度快很多。">
DDIM 的主要好處？
</Mcq>

<FillClear group="quiz3" corner />

<!--
★ 檢核 3／3（1 分）。答案：5 B、6 C。
全部答案與理由：1 B、2 C、3 A（B 是常見錯誤）、4 C（A 是 D3-3 的常見誤解）、5 B（A 是 t 太小）、6 C（A 錯：網路還是要訓練，只是不用「重新」訓練）。
-->

---

<div class="eyebrow">第三天 · 回家作業</div>

# 回家作業：用自己的數字寫「GAN vs 擴散」半頁

<div style="font-size:18px" class="mt-2">

1. 把「第三天的生成三難表格」每一列換成你自己 lab 的數字（D3-1 的兩兩距離、D3-3 的秒數、D3-4 的每片 ms）
2. 用半頁回答：行銷部的縮圖、品保部的檢測，各該用 GAN 還是擴散？代價是什麼？
3. （選做）D3-2：找一片被 CycleGAN「抹淡」瑕疵的板子，寫三句話說明為什麼會這樣

</div>

<div class="node node--primary mt-4" style="font-size:17px"><strong>這是學習評量的草稿</strong><small>學習評量第一部分「解釋 Diffusion vs GAN」：第四天會在這份半頁上加條件式生成的證據</small></div>

<div class="takeaway mt-3">作業的重點是第 2 點：每一個「比較好」都要配上一個你量到的數字。</div>

<!--
★ 作業（3 分）：下一次上課（D4-1）開場 5 分鐘回顧。選做第 3 點用 D3-2 lab10 的 defect_survival.png。
-->

---
hostOnly: true
---

<div class="eyebrow">下一步</div>

# 下一堂 D4-1：指定要畫哪一類，條件式生成

<div class="node node--primary mt-2">今天的擴散模型只會「畫一片正常的板子」或「畫任何一件衣服」。D4-1：把類別標籤也交給去噪網路，指定要畫什麼——這是學習評量的第二部分「實作條件式生成」。</div>

<!--
★ 下一步（1 分）：只給講師的託管版看。預告 D4-1：classifier-free guidance。
-->
