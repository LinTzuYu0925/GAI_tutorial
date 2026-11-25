---
theme: default
title: 指定生成第 k 類
info: |
  生成式AI原理 · D4-1
  數據組要補少數類別的資料：在 D3-3 的 DDPM 加上類別嵌入、label dropout 和 classifier-free guidance，指定生成第 k 類，並量忠實度、多樣性與 FID／KID。
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
exportFilename: 13-conditional-diffusion-cfg
layout: center
class: cover
---

<div class="eyebrow">生成式AI原理 · D4-1</div>

# 指定生成第 k 類

<p class="subtitle">類別條件擴散模型 ＋ classifier-free guidance：說「我要運動鞋」，它就畫運動鞋</p>

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-8">
  <span class="chip">只能隨機生成</span><span class="arrow">→</span>
  <span class="chip">類別嵌入</span><span class="arrow">→</span>
  <span class="chip">label dropout</span><span class="arrow">→</span>
  <span class="chip">CFG 那一行</span><span class="arrow">→</span>
  <span class="chip">忠實 vs 多樣</span><span class="arrow">→</span>
  <span class="chip">FID／KID</span>
</div>

<!--
★ 開場（2 分）：D3-3 的 DDPM 從雜訊畫出衣服、鞋子，但畫哪一種是隨機的。今天讓它「聽話」。這一堂的筆記本就是學習評量（b）「實作條件生成」的作業。
-->

---

<div class="eyebrow">00 · Frame（定義問題）</div>

# 數據組：少數類別只有幾十張，能不能指定生成？

<div class="ticket mt-2">
  <div class="ticket-head">【需求單 #D4-1】部門：數據組<span>公司：曜嶼電子 <span class="fiction" style="color:#fff;border-color:#fff">虛構</span></span></div>
  <dl>
    <dt>問題</dt><dd>網店商品分類器對少數類別很弱，能不能「指定」生成第 k 類的圖來補資料？</dd>
    <dt>現況痛點</dt><dd>少數類別只有幾十張，分類器常認錯</dd>
    <dt>成功指標（KPI）</dt><dd>生成圖被分類器認對的比例（忠實度）；同類樣本夠不夠多樣；FID／KID（生成圖與真實圖的距離，今天會教）</dd>
    <dt>可用資料</dt><dd>Fashion-MNIST（10 類）；D3-3 的 DDPM 做法</dd>
    <dt>限制與法規</dt><dd>Colab T4；合成資料可能放大偏差，要用真實資料驗收</dd>
    <dt>為何現有工具不夠</dt><dd>D3-3 的 DDPM 只能「隨機」生成，不能指定類別</dd>
  </dl>
</div>

<!--
★ 需求單（3 分）：Fashion-MNIST 當作網店的十種商品。真實情況是「少數類別」只有幾十張；今天先學會指定生成，延伸題再試補資料。
-->

---

<div class="eyebrow">學習目標</div>

# 今天結束時，你能夠……

1. **加上**類別嵌入：標籤 → 向量，和時間向量相加
2. **說明** label dropout 為什麼讓一個模型同時學會「有條件」和「沒條件」
3. **不靠 AI 口頭解釋** CFG 那一行：ε ＝ ε_uncond ＋ w ·（ε_cond − ε_uncond）
4. **量測**不同 w 的忠實度與多樣性，說出取捨
5. **說明** FID／KID 是「兩團特徵點雲的距離」，以及小樣本的限制

<div class="takeaway mt-4">學習評量（b）「實作條件生成」：交今天跑完的筆記本，加上第 3 點的口頭說明。</div>

<!--
★ 目標（1 分）。不教：classifier guidance 的實作（只看圖）、Bayes 推導（附錄）、Inception 版 FID 的細節、文字當條件（下一堂 D4-2）。
-->

---

<div class="eyebrow">00 · Frame · 回到 D1-1</div>

# 條件 p(x｜y)：D1-1 的那張圖，今天寫成程式

<div class="grid grid-cols-[1fr_1.1fr] gap-6 mt-2 items-center">
<div>

<svg viewBox="0 0 380 230" style="width:100%" aria-label="兩個橢圓：左邊標 y 等於運動鞋、右邊標 y 等於包包；同一個模型換條件，抽樣範圍就換了">
  <ellipse cx="115" cy="110" rx="85" ry="60" fill="var(--soft-blue)" stroke="var(--primary)" stroke-width="2"/>
  <ellipse cx="270" cy="110" rx="85" ry="60" fill="var(--surface)" stroke="var(--warm-accent)" stroke-width="2" stroke-dasharray="6 4"/>
  <text x="62" y="116" style="font-size:18px" fill="var(--primary)">y＝運動鞋</text>
  <text x="230" y="116" style="font-size:18px" fill="var(--warm-accent)">y＝包包</text>
  <text x="40" y="210" style="font-size:17px" fill="var(--muted-text)">同一個模型，換 y，抽樣範圍就換了</text>
</svg>

</div>
<div style="font-size:19px">

- **D3-3**：p(x)：從雜訊抽出「任何一件」衣物
- **今天**：p(x｜y)：先指定 y（10 類之一），再抽 x
- 讀作：「在條件 y 之下，x 出現的機率」（D1-1 學過）
- 你們在 D1-2 的提示詞也是 y；今天先用最簡單的 y：**一個類別編號**

</div>
</div>

<div class="takeaway mt-3">條件生成＝把 y 也交給去噪的 U-Net：它要學「在 y 之下，雜訊長什麼樣」。</div>

<!--
★ Frame（4 分）：指著兩個橢圓：同一個模型，換條件 y，就從不同的範圍抽樣。D1-1 第一次出現這個符號時只是概念，今天要讓 U-Net 真的收到 y。
-->

---

<div class="eyebrow">01 · Try（先看結果）</div>

# 講師的模型：指定「運動鞋」，就出現運動鞋

<img class="photo" src="/lab13-run-sneakers.png" alt="指定第 7 類運動鞋，模型畫出的 8 張運動鞋，每張角度和花紋略有不同" style="width:100%">
<div class="shot-cap">lab13 解答筆記本，Colab T4 實跑：8 張「運動鞋」、1000 步、7.0 秒（w＝3、seed 0；模型訓練 10 個 epoch、369 秒）</div>

<div class="takeaway mt-3">先猜：同一個模型，只換類別編號就能換商品；那「多聽話」又是誰決定的？（答案：w，第 9 頁）</div>

<!--
★ 示範（4 分）：用 lab13 解答筆記本在 T4 跑好的輸出。強調：這個模型只訓練了一次，10 個類別都是同一個模型畫的；差別只在餵進去的 y。
-->

---

<div class="eyebrow">02 · Open（打開黑盒子）· 類別嵌入</div>

# 類別嵌入（class embedding）：標籤查表，加到時間向量

<div class="grid items-center mt-3" style="font-size:17px;grid-template-columns:22% 5% 28% 5% 40%;row-gap:10px">
  <div class="node">t（第幾步）<small>&#91;B&#93;</small></div><span class="arrow text-center">→</span>
  <div class="node">正弦嵌入 ＋ MLP（兩層全連接）<small>D3-3 的時間嵌入 → &#91;B, 128&#93;</small></div><span class="arrow text-center">↘</span>
  <div class="node node--primary" style="grid-row:span 2"><strong>e ＝ 時間向量 ＋ 類別向量</strong><small>&#91;B, 128&#93;，送進 U-Net 的每一個殘差區塊（和 D3-3 時間嵌入同一條路）</small></div>
  <div class="node node--warm">y（類別 0～9，或 10＝沒有標籤）<small>&#91;B&#93;</small></div><span class="arrow text-center">→</span>
  <div class="node node--warm"><strong>y_emb</strong><small>nn.Embedding(11, 128)：每一類一列可訓練的向量</small></div><span class="arrow text-center">↗</span>
</div>

```python
e = self.t_mlp(time_embedding(t)) + self.y_emb(y)   # 時間向量 ＋ 類別向量，[B, 128]
```

<div class="muted mt-1" style="font-size:16px">讀作：「先把 t 變成向量、把 y 查表變成向量，兩個相加，當作這張圖的『說明書』交給 U-Net」。U-Net 的輸入圖 x_t 和輸出 ε̂ 都還是 &#91;B, 1, 32, 32&#93;，和 D3-3 一樣。</div>

<div class="takeaway mt-2">不把類別直接當一個數字丟進去：查表讓每一類有自己的向量，「7 號比 6 號大」這種假關係就不存在。</div>

<!--
★ 類別嵌入（6 分）：embedding（嵌入）讀作「把一個編號換成一列可學的數字」。第 11 格（編號 10）是「沒有標籤」，下下頁會用到。
常見誤解：把 y 當成 0～9 的一個數字直接加進去 → 模型會以為「褲子（1）和套頭衫（2）很接近」。nn.Embedding 等於 one-hot 再乘一個矩陣（DL 學過 one-hot）。
-->

---

<div class="eyebrow">02 · Open · 先看另一種做法</div>

# Classifier guidance（分類器引導）：外部分類器在旁邊推

<div class="grid grid-cols-[1fr_1.1fr] gap-6 mt-2 items-center">
<div>

<svg viewBox="0 0 320 220" style="width:100%" aria-label="一個雜訊點沿著去噪路徑移動，每一步旁邊有一個小箭頭把它推向運動鞋的區域">
  <defs><marker id="cg-a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--warm-accent)"/></marker>
  <marker id="cg-b" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--primary)"/></marker></defs>
  <ellipse cx="250" cy="60" rx="58" ry="38" fill="var(--soft-blue)" stroke="var(--primary)" stroke-width="2"/>
  <text x="215" y="66" style="font-size:16px" fill="var(--primary)">運動鞋</text>
  <path d="M30,190 C80,170 110,140 150,120 C180,105 200,90 225,72" stroke="var(--primary)" stroke-width="2.5" fill="none" marker-end="url(#cg-b)"/>
  <line x1="80" y1="170" x2="100" y2="148" stroke="var(--warm-accent)" stroke-width="2" marker-end="url(#cg-a)"/>
  <line x1="150" y1="120" x2="172" y2="100" stroke="var(--warm-accent)" stroke-width="2" marker-end="url(#cg-a)"/>
  <circle cx="30" cy="190" r="6" fill="var(--muted-text)"/>
  <text x="12" y="214" style="font-size:16px" fill="var(--muted-text)">x_T（純雜訊）</text>
  <text x="175" y="122" style="font-size:16px" fill="var(--warm-accent)">← 推力</text>
</svg>

</div>
<div style="font-size:18px">

- 另外訓練一個「看雜訊圖也能分類」的分類器
- 每一步去噪時，問它「往哪裡改會更像運動鞋」，順著推一下
- 缺點：要多訓練、多維護一個專門的分類器

</div>
</div>

<div class="takeaway mt-3">想法很好：去噪時「推向指定類別」。但能不能不要外部分類器？下一頁。</div>

<div class="src">Dhariwal &amp; Nichol, 2021（S1，待確認）</div>

<!--
○ 選修（3 分）：只看圖、不寫程式。分類器要能看「很吵的 x_t」，所以不能直接用 D1-3 訓練的分類器。這是今天主角 classifier-free 名字的由來：不需要分類器。
-->

---

<div class="eyebrow">02 · Open · label dropout</div>

# label dropout（標籤丟棄）：訓練時偶爾藏起標籤

<div class="flex gap-2 mt-4 justify-center" style="font-size:17px">
  <div class="node" style="width:11%">運動鞋<small>y＝7</small></div>
  <div class="node" style="width:11%">褲子<small>y＝1</small></div>
  <div class="node node--dashed" style="width:11%"><strong>？</strong><small>y＝10（NULL）</small></div>
  <div class="node" style="width:11%">包包<small>y＝8</small></div>
  <div class="node" style="width:11%">T恤<small>y＝0</small></div>
  <div class="node" style="width:11%">短靴<small>y＝9</small></div>
  <div class="node" style="width:11%">洋裝<small>y＝3</small></div>
  <div class="node" style="width:11%">外套<small>y＝4</small></div>
</div>
<div class="muted mt-1" style="font-size:16px;text-align:center">同一批 128 張圖：每張有 10% 的機率，標籤被換成「沒有標籤」（NULL）；圖本身不變</div>

<div class="grid grid-cols-2 gap-6 mt-4" style="font-size:18px">
<div class="node node--primary"><strong>有標籤的 90%</strong><small>學「在 y 之下」的雜訊預測：ε_cond（有條件）</small></div>
<div class="node node--dashed"><strong>NULL 的 10%</strong><small>學「什麼都不知道」時的雜訊預測：ε_uncond（沒條件），就是 D3-3 的模型</small></div>
</div>

```python
drop = torch.rand(y.shape[0], device=device) < P_UNCOND   # 每張抽一個亂數，< 0.1 就藏
y_in = torch.where(drop, torch.full_like(y, NULL), y)      # 藏的換成 NULL，其餘照舊
```

<div class="takeaway mt-2">一個模型、一次訓練，學會兩種預測：有條件、沒條件。下一頁把兩者相減。</div>

<!--
★ label dropout（5 分）：讀作：「抽一個 0～1 的亂數，小於 0.1 就把標籤換成 NULL」。和 DL 學過的 dropout（丟掉神經元）是不同的東西，只是名字像：這裡丟的是「標籤」。
常見誤解：藏標籤會讓模型變差。實際上 90% 的時間還是有標籤；藏起來的 10% 讓它學會「沒條件時該怎麼猜」，這是 CFG 的前提。
-->

---

<div class="eyebrow">02 · Open · 今天的主角</div>

# Classifier-free guidance（CFG，無分類器引導）的那一行

<div class="node node--primary" style="font-size:24px;padding:10px;text-align:center">ε ＝ ε_uncond ＋ w ·（ε_cond − ε_uncond）</div>

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-2 items-center">
<div>

<table style="font-size:16px">
<tbody>
<tr><td style="width:34%"><b>ε_uncond</b></td><td>給 NULL：沒條件的雜訊預測</td></tr>
<tr><td><b>ε_cond</b></td><td>給 y＝k：有條件的雜訊預測</td></tr>
<tr><td><b>ε_cond − ε_uncond</b></td><td>「知道類別」多出來的方向</td></tr>
<tr><td><b>w</b></td><td>指導強度（guidance scale）：走幾倍</td></tr>
</tbody>
</table>

</div>
<div>

<svg viewBox="0 0 300 150" style="width:100%" aria-label="一條數線：ε_uncond 在左，ε_cond 在中間，w 等於 3 的點在更右邊，箭頭表示沿著同一方向延伸">
  <defs><marker id="cfg-a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--warm-accent)"/></marker></defs>
  <line x1="20" y1="70" x2="285" y2="70" stroke="#b8b8b8" stroke-width="1.5"/>
  <line x1="50" y1="70" x2="248" y2="70" stroke="var(--warm-accent)" stroke-width="3" marker-end="url(#cfg-a)"/>
  <circle cx="50" cy="70" r="7" fill="var(--muted-text)"/><text x="28" y="50" style="font-size:16px" fill="var(--muted-text)">w＝0</text><text x="18" y="98" style="font-size:16px" fill="var(--muted-text)">ε_uncond</text>
  <circle cx="120" cy="70" r="7" fill="var(--primary)"/><text x="100" y="50" style="font-size:16px" fill="var(--primary)">w＝1</text><text x="98" y="98" style="font-size:15px" fill="var(--primary)">ε_cond</text>
  <circle cx="260" cy="70" r="7" fill="var(--warm-accent)"/><text x="240" y="50" style="font-size:16px" fill="var(--warm-accent)">w＝3</text>
  <text x="40" y="135" style="font-size:16px" fill="var(--muted-text)">w＞1：比「有條件」走得更遠</text>
</svg>

</div>
</div>

<div class="takeaway mt-2">讀作：「從沒條件的猜測出發，朝『知道類別多出來的方向』走 w 倍」。</div>

<div class="src">Ho &amp; Salimans, 2022（S2，待確認）：論文的 w 比本課的小 1；diffusers 的 <code>guidance_scale</code> 用本課寫法。算出的 ε 進入 D3-3 的取樣迴圈</div>

<!--
★ CFG（7 分）：這一行就是學習評量口試要講的。請學員跟著念一次：「從沒條件出發，朝有條件多出來的方向走 w 倍」。
D1-2 的 guidance_scale＝1.0 就是這裡的 w＝1：只用有條件的預測，所以負面提示沒作用（D4-2 會說明負面提示其實是換掉 ε_uncond）。
每一步要算兩次 U-Net（有 y、NULL 各一次），lab 把兩批接成一批一起算。
-->

---

<div class="eyebrow">02 · Open · 練習（不用 AI）</div>

# 練習：用數字解釋你的 CFG 那一行

<div class="grid grid-cols-[1fr_1.35fr] gap-6 mt-1" style="font-size:17px">
<div class="node"><strong>照著做（某一個像素）</strong><small>ε_uncond ＝ 0.2、ε_cond ＝ 0.5、w ＝ 2<br>差 ＝ 0.5 − 0.2 ＝ 0.3<br>ε ＝ 0.2 ＋ 2 × 0.3 ＝ <b>0.8</b><br>→ 比有條件的 0.5 更偏向「知道類別」那一邊</small></div>
<div>

另一個像素：ε_uncond ＝ 0.1、ε_cond ＝ 0.4。

<table class="fill tight vlines mt-1">
<thead><tr><th style="width:14%">w</th><th style="width:22%">ε ＝ ？</th><th>這時模型「聽不聽話」？一句話</th></tr></thead>
<tbody>
<tr><td>0</td><td class="blank"><FillIn id="cfg.w0" /></td><td class="blank"><FillIn id="cfg.w0-why" hint="例：完全不看……" /></td></tr>
<tr><td>1</td><td class="blank"><FillIn id="cfg.w1" /></td><td class="blank"><FillIn id="cfg.w1-why" /></td></tr>
<tr><td>7</td><td class="blank"><FillIn id="cfg.w7" /></td><td class="blank"><FillIn id="cfg.w7-why" /></td></tr>
</tbody>
</table>

<FillClear group="cfg" />

</div>
</div>

<div class="muted mt-2" style="font-size:16px">做完後：在 lab 第 3 部分把 w 換成這三個值，看網格是否符合你寫的句子。</div>

<!--
★ 無 AI 檢核點（7 分）：個人作業、不收回，是學習評量口試的演練。先自己算，再用一句話描述。lab 的網格會讓學員驗證 w＝0 時類別亂掉、w＝7 時很像但很單調。
-->

---
hostOnly: true
---

<div class="eyebrow">02 · Open · 練習解答</div>

# 練習解答：w 決定「多聽話」

<table class="vlines" style="font-size:18px">
<thead><tr><th style="width:12%">w</th><th style="width:28%">ε</th><th>意思</th></tr></thead>
<tbody>
<tr><td>0</td><td>0.1 ＋ 0 × 0.3 ＝ 0.1</td><td>等於 ε_uncond：完全不看類別，畫出隨機一類（就是 D3-3）</td></tr>
<tr><td>1</td><td>0.1 ＋ 1 × 0.3 ＝ 0.4</td><td>等於 ε_cond：一般的條件模型</td></tr>
<tr><td>7</td><td>0.1 ＋ 7 × 0.3 ＝ 2.2</td><td>遠超過 ε_cond：非常像指定類別，但每張都很像（多樣性下降）</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">怎麼判斷：w＝0 和 w＝1 一定剛好落在兩個端點；w＞1 一定比 ε_cond 走得更遠。</div>

<!--
★ 解答（2 分）：補一句：w 太大時，數值超出訓練時見過的範圍，圖可能過飽和、出現怪紋路（lab 的 w＝7 可以看到程度）。
-->

---

<div class="eyebrow">03 · Measure（量測驗收）· 取捨</div>

# w 越大：越像指定類別，但同一類越單調

<img class="photo" src="/lab13-run-cfg-grid.png" alt="四個網格，w 等於 0、1、3、7；每一列是一個類別的 8 張圖。w 等於 0 時每列類別混雜，w 越大每列越整齊、8 張越像" style="width:100%">
<div class="shot-cap">Colab T4 實跑（lab13 第 3 部分，seed 0、T＝1000 步；四格共 139 秒）。<b>由左到右 w＝0、1、3、7</b>；由上到下：T恤、褲子、套頭衫、洋裝、外套、涼鞋、襯衫、運動鞋、包包、短靴</div>

<div class="takeaway mt-3">同樣的起始雜訊、只差 w：看每一列的 8 張越來越像。w 是「忠實」和「多樣」的旋鈕。</div>

<!--
★ 取捨（4 分）：請學員找 w＝0 那一格：每一列應該是混雜的類別（模型沒在聽）。w＝7：每一列很整齊，但 8 張幾乎同一個樣子。數字在下兩頁。
-->

---

<div class="eyebrow">03 · Measure · FID／KID</div>

# FID／KID：比較「真實」和「生成」兩團特徵點雲有多遠

<div class="grid grid-cols-[1fr_1.2fr] gap-6 mt-1 items-center">
<div>

<svg viewBox="0 40 260 170" style="width:100%;min-width:300px" aria-label="兩團點：藍色是真實圖的特徵，橘色是生成圖的特徵；兩個平均位置之間有雙箭頭；橘色那團比較擠">
  <defs><marker id="fid-a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#444"/></marker>
  <marker id="fid-b" markerWidth="8" markerHeight="8" refX="1" refY="4" orient="auto"><path d="M8,0 L0,4 L8,8 z" fill="#444"/></marker></defs>
  <g fill="var(--primary)" opacity="0.75">
    <circle cx="60" cy="80" r="5"/><circle cx="85" cy="60" r="5"/><circle cx="110" cy="95" r="5"/><circle cx="70" cy="120" r="5"/><circle cx="100" cy="135" r="5"/><circle cx="45" cy="105" r="5"/><circle cx="125" cy="70" r="5"/><circle cx="90" cy="105" r="5"/>
  </g>
  <g fill="var(--warm-accent)" opacity="0.85">
    <rect x="195" y="95" width="9" height="9"/><rect x="210" y="105" width="9" height="9"/><rect x="200" y="115" width="9" height="9"/><rect x="220" y="95" width="9" height="9"/><rect x="215" y="120" width="9" height="9"/><rect x="190" y="108" width="9" height="9"/>
  </g>
  <line x1="95" y1="100" x2="200" y2="110" stroke="#444" stroke-width="1.5" marker-end="url(#fid-a)" marker-start="url(#fid-b)"/>
  <text x="15" y="178" style="font-size:17px" fill="var(--primary)">● 真實（散開）</text>
  <text x="15" y="200" style="font-size:17px" fill="var(--warm-accent)">■ 生成（擠在一起）</text>
  <text x="110" y="148" style="font-size:17px" fill="var(--text)">平均差多遠</text>
</svg>

</div>
<div style="font-size:17px">

1. 每張圖丟進分類器，取倒數第二層 → 128 個數字（特徵；真實圖上不動的維度去掉，實跑剩 77 個）
2. **FID**：兩團的平均差多遠 ＋ 散佈的形狀差多少；越小越好
3. **KID**：多次抽小樣本比較再平均；樣本少時比 FID 穩
4. 生成圖「全擠在一起」（多樣性差）時，即使每張都像，FID 也會變大

```python
f_real, f_gen = feats(real), feats(gen)   # 各 [500, 特徵維度]
fid(f_real, f_gen); kid(f_real, f_gen)
```

</div>
</div>

<div class="takeaway mt-2">FID／KID 一次看品質和多樣性；但特徵網路不同，數字就不能比：我們的值不能和論文比。</div>

<div class="src">FID：Heusel et al., 2017（S4）；KID：Bińkowski et al., 2018（S5），皆待確認。論文用 Inception 網路的特徵；本 lab 用自己訓練的分類器特徵</div>

<!--
★ FID／KID（6 分）：ML 課學過「兩點之間的距離」；這裡是「兩團點之間的距離」。平均差＝整體偏到哪裡；散佈形狀差＝一團散開、一團擠在一起。不推公式（附錄的 sources 有）。
常見誤解：FID 數字可以跨論文比較。只有「同樣的特徵網路、同樣的樣本數、同樣的真實參考」才能比；樣本只有幾百張時 FID 偏高，這是用 KID 的原因。
-->

---

<div class="eyebrow">03 · Measure · 忠實度</div>

# 忠實度：分類器認得出你指定的類別嗎？

<table class="mt-2" style="font-size:18px">
<thead><tr><th style="width:12%">w</th><th>忠實度（認對比例）</th><th>同類兩兩距離（多樣性）</th><th>FID（特徵）</th><th>KID（特徵）</th></tr></thead>
<tbody>
<tr><td>0</td><td>10.6%</td><td>19.59</td><td>20.18</td><td>0.405</td></tr>
<tr><td>1</td><td>80.8%</td><td>15.94</td><td>4.54</td><td>0.070</td></tr>
<tr><td>3</td><td><b>97.0%</b></td><td>14.19</td><td><b>4.51</b></td><td><b>0.030</b></td></tr>
<tr><td>7</td><td>99.0%</td><td>14.10</td><td>11.96</td><td>0.202</td></tr>
<tr><td>真實圖</td><td>88.2%（分類器準確率）</td><td>17.30</td><td>0</td><td>0</td></tr>
</tbody>
</table>

<div class="muted mt-2" style="font-size:16px">Colab T4 實跑（seed 0）：每個 w 生成 10 類 × 50 張；分類器是 lab 裡訓練 2 個 epoch 的小 CNN（D1-3 的寫法）；多樣性用 D3-1 量 mode collapse 的同一把尺；FID／KID 用分類器的 77 維特徵。</div>

<div class="takeaway mt-2">忠實度只量「有沒有聽話」：認對 100% 但每張一樣，對補資料沒有用。要和多樣性一起看。</div>

<!--
★ 忠實度（4 分）：讀表順序：忠實度隨 w 上升；同類距離隨 w 下降（w＝0 的 19.59 比真實圖還大，因為圖很亂）；FID／KID 在 w＝3 最好、w＝7 又變差（太單調，離真實分布遠）。生成圖忠實度 97% 高於分類器自己的 88.2%：生成圖比真實圖「典型」。
-->

---

<div class="eyebrow">附錄 · 備用</div>

# 為什麼 CFG 有效：用 Bayes 拆開（選讀）

<div style="font-size:19px" class="mt-3">

1. Bayes：p(x_t｜y) ∝ p(x_t) · p(y｜x_t)（∝ 讀作「正比於」）
2. 取 log 再對 x_t 微分（∇ 讀作「往哪個方向改會變大」）：∇log p(x_t｜y) ＝ ∇log p(x_t) ＋ ∇log p(y｜x_t)
3. 擴散模型預測的雜訊 ≈ −σ_t · ∇log p(x_t)，所以「ε_cond − ε_uncond」≈「−σ_t · ∇log p(y｜x_t)」：一個**隱含的分類器**
4. 乘上 w：把這個隱含分類器的推力放大 w 倍

</div>

<div class="takeaway mt-3">CFG 沒有拿掉分類器，而是讓同一個模型「自己當分類器」：有條件減沒條件，就是分類器的推力。</div>

<div class="src">Ho &amp; Salimans, 2022（S2）；σ_t ＝ √(1−ᾱ_t)，即 D3-3 一步加噪公式裡雜訊前面的係數</div>

<!--
△ 附錄（2 分）：學員問「為什麼相減就有用」時再講。∝ 讀作「正比於」；∇ 讀作「往哪個方向改會變大」。第 3 行是 score matching 的結論（D3-3 附錄），不推導。
-->

---

<div class="eyebrow">04 · Lab L4-1</div>

# Lab 1／7：我們要做出什麼？

<div class="grid grid-cols-2 gap-6 mt-2" style="font-size:19px">
<div>

**打開筆記本**：<code>lab13-cfg.ipynb</code>（在 <code>materials/</code>）→ Open in Colab<br>
執行階段：**T4 GPU**

1. 指定「運動鞋」，真的會畫出運動鞋嗎？
2. w 從 0 調到 7，網格怎麼變？
3. 哪一個 w 最適合拿來補資料？用數字說

</div>
<div>

<img class="photo" src="/lab13-run-tradeoff.png" alt="取捨曲線：w 從 0 到 7，忠實度從約 10% 升到約 99%，同類兩兩距離從約 19.6 降到約 14.1" style="width:100%">
<div class="shot-cap">目標之一：取捨曲線（講師 Colab T4 實跑；全程約 25 分鐘，VRAM 峰值 0.95 GB）</div>

</div>
</div>

<div class="takeaway mt-3">交付給數據組：一張「w 對忠實度、多樣性、FID／KID」的表，加上你建議的 w。</div>

<!--
★ Lab 開始（3 分）：Fashion-MNIST 由 torchvision 下載（約 30 MB）。講師 T4 實跑：訓練 10 epochs 369 秒、VRAM 峰值 0.95 GB、四個 w 的量測 891 秒（每個 w 約 3.7 分鐘印一行）。沒有 GPU：EPOCHS＝1、SUBSET＝3000、N_PER_CLASS＝10，圖會很糊，但流程一樣。
-->

---

<div class="eyebrow">04 · Lab L4-1</div>

# Lab 2／7：筆記本拆成哪幾塊？

<div class="steps mt-2" style="font-size:18px">
  <div><span class="num">1</span><strong>資料與排程</strong>：Fashion-MNIST 補成 32 × 32、值域 −1～1；T＝1000、β 從 0.0001 到 0.02；<code>add_noise</code>（D3-3）</div>
  <div><span class="num">2</span><strong>CondUNet</strong>：D3-3 的小 U-Net ＋ <code>y_emb</code>；訓練迴圈加一行 label dropout；存 <code>cfg_unet.pt</code></div>
  <div><span class="num">3</span><strong>sample(labels, w)</strong>：每一步算 ε_cond、ε_uncond，套 CFG 那一行；四個 w 的網格</div>
  <div><span class="num">4</span><strong>量測</strong>：小分類器 <code>Clf</code>；忠實度、<code>mean_pairwise</code>、<code>fid</code>、<code>kid</code></div>
</div>

<div class="takeaway mt-4">兩個 TODO，各一兩行：label dropout（第 2 部分）、CFG 那一行（第 3 部分）。</div>

<!--
★ 拆塊（3 分）：第 1、2 部分大多是 D3-3 的程式，只多了 y。時間留給第 3、4 部分。
-->

---

<div class="eyebrow">04 · Lab L4-1</div>

# Lab 3／7：Specify

<div style="font-size:18px" class="mt-2">

<strong>【目標】</strong>指定類別 k，生成第 k 類的 Fashion-MNIST 圖；找出忠實度和多樣性兼顧的 w<br>
<strong>【輸入與輸出】</strong>x_t <code>&#91;B,1,32,32&#93;</code>、t <code>&#91;B&#93;</code>、y <code>&#91;B&#93;</code>（0～9，或 10＝NULL）→ U-Net → ε̂ <code>&#91;B,1,32,32&#93;</code>；取樣時兩種 y 接成一批：<code>&#91;2n,1,32,32&#93;</code><br>
<strong>【限制】</strong>label dropout 10%；不改模型大小和 T；Colab T4<br>
<span class="muted" style="font-size:16px">為什麼：P_UNCOND 是 0 的話，NULL 從來沒學過，ε_uncond 就是亂猜（延伸題 1）</span><br>
<strong>【驗收】</strong>① w＝0 時忠實度明顯低於 w＝3（模型沒在聽）　② w＝3 的忠實度 ≥ 80%　③ 同類兩兩距離隨 w 變小　④ 選出的 w，KID 不是四個裡最差的

</div>

<!--
★ Specify（3 分）：驗收門檻是課前定的，不是預測結果；T4 實跑後若明顯不合理再調。強調第 ③④ 點：只看忠實度會選到最大的 w。
-->

---

<div class="eyebrow">04 · Lab L4-1</div>

# Lab 4／7：Generate → Execute

<PromptBox>
這是 PyTorch 筆記本，請只填兩個 # TODO：<br>
① 訓練迴圈：每張圖有 P_UNCOND 的機率把標籤換成 NULL，結果存在 y_in（用 torch.rand 和 torch.where）<br>
② sample()：eps ＝ eps_u ＋ w ×（eps_c − eps_u）<br>
不要改模型、T、P_UNCOND 和 EPOCHS。每一格說明每一行在做什麼。
</PromptBox>

<div class="steps mt-2" style="font-size:17px">
  <div><span class="num">1</span>T4 上訓練約 6 分鐘（每個 epoch 約 37 秒）；loss 從 0.092 降到約 0.032</div>
  <div><span class="num">2</span>沒有 Agent 額度：照「label dropout」頁的兩行、「CFG 那一行」頁的公式填；卡住開 <code>-solution.ipynb</code></div>
  <div><span class="num">3</span>預期輸出：<code>輸入 (4, 1, 32, 32) → 輸出 (4, 1, 32, 32)</code>，之後每個 epoch 一行 loss</div>
</div>

<div class="node node--warm mt-2" style="font-size:16px"><strong>常見錯誤</strong><small>CFG 寫成 <code>eps_c + w * (eps_c - eps_u)</code>：起點錯了，w＝0 時不會回到「沒條件」。起點一定是 <code>eps_u</code></small></div>

<!--
★ 執行（約 23 分，含訓練與取樣）：最常見錯誤是起點寫成 eps_c。另一個：label dropout 用了 y.shape 以外的長度，或忘了 device。
訓練時先講下一頁要對照的問題。
-->

---

<div class="eyebrow">04 · Lab L4-1</div>

# Lab 5／7：看網格、對照你的預測

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-2" style="font-size:18px">
<div>

跑完第 3 部分後：

1. w＝0 那一格：每一列還是同一類嗎？
2. w 從 1 到 7：每一列的 8 張越來越像嗎？
3. 回到「練習：用數字解釋你的 CFG 那一行」：你寫的三句話，網格裡看得到嗎？

</div>
<div>

<div class="node node--primary"><strong>和隔壁同學比</strong><small>在網格那一格最上面加一行 <code>SEED = 你的座號</code>，只重跑那一格（不要「全部執行」，否則會重新訓練）</small></div>

</div>
</div>

<div class="takeaway mt-4">「像不像」用眼睛看，「多像、多單調」用數字量：下一頁的表。</div>

<!--
★ 對照（6 分）：第 1 題是 w＝0 的直接證據：模型完全不看 y，就是 D3-3 的無條件模型。
-->

---

<div class="eyebrow">04 · Lab L4-1</div>

# Lab 6／7：Audit → Iterate

<table style="font-size:17px">
<thead><tr><th style="width:28%">稽核問題</th><th>具體動作</th><th style="width:34%">應該是</th></tr></thead>
<tbody>
<tr><td>Agent 寫的 label dropout 對嗎？</td><td>印出 <code>(y_in == NULL).float().mean()</code></td><td>約 0.1</td></tr>
<tr><td>Agent 寫的 CFG 起點對嗎？</td><td>w＝0 取樣一次</td><td>每一列類別混雜（＝ε_uncond）</td></tr>
<tr><td>分類器本身可靠嗎？</td><td>看真實測試圖的準確率</td><td>約 85–90%（實跑 88.2%）</td></tr>
<tr><td>FID／KID 是同樣的參考嗎？</td><td>看 <code>real</code> 的張數</td><td>每個 w 都和同一組 500 張真實圖比</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">一次只改一件事：例如把 P_UNCOND 改成 0 重新訓練，看 w＝3 會怎樣（延伸題 1）。</div>

<!--
★ 稽核（6 分）：T4 實跑：分類器在真實圖上 88.2%，但 w＝3 的生成圖忠實度 97.0%。生成圖比真實圖更「典型」（每類都畫最標準的樣子），分類器反而更好認——這正是多樣性下降的另一個訊號。
-->

---

<div class="eyebrow">04 · Lab L4-1 · Ship</div>

# Lab 7／7：交給數據組的建議

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-2" style="font-size:18px">
<div>

<img class="photo" src="/lab13-run-tradeoff.png" alt="取捨曲線：藍線忠實度隨 w 上升，橘色虛線同類兩兩距離隨 w 下降，橘色點線是真實圖的距離 17.30" style="width:100%">
<div class="shot-cap">Colab T4 實跑（lab13 <code>cfg_tradeoff.png</code>，seed 0）；點線＝真實圖的同類距離 17.30</div>

</div>
<div>

<div class="node node--primary"><strong>建議句型</strong><small>「補資料時用 w＝＿＿：忠實度 ＿＿%、同類距離 ＿＿（真實圖 ＿＿）、KID ＿＿。理由：＿＿。上線前要用真實測試圖驗收分類器有沒有變好。」</small></div>

</div>
</div>

<div class="takeaway mt-3">沒有「最好的 w」：FID／KID 同時看品質和多樣性，可以當主要依據；要更多樣就往小的 w 退一步。</div>

<!--
★ Ship（4 分）：講師的例子（不要先給學員看）：w＝3，FID 4.51、KID 0.030 都是四個裡最好；但同類距離 14.19 和 w＝7 差不多，若更在乎多樣性可退到 w＝1（距離 15.94、忠實度 80.8%）。注意：今天的模型用完整、平衡的 Fashion-MNIST 訓練，「少數類別」的情況是延伸題 2。下一堂 D4-2 的 guidance_scale 預設 7.5，就是同一個旋鈕。
-->

---

<div class="eyebrow">05 · 學習評量</div>

# 學習評量（b）「實作條件生成」：要交什麼

<div class="grid grid-cols-2 gap-6 mt-3" style="font-size:18px">
<div class="node node--primary"><strong>筆記本</strong><small>你的 <code>lab13-cfg.ipynb</code>：兩個 TODO 自己填、從頭跑完，輸出都保留（網格、對照表、取捨曲線）；最後一格寫你建議的 w 和一句理由</small></div>
<div class="node node--warm"><strong>口頭說明（不用 AI）</strong><small>講師指著你的 CFG 那一行，你要說出：ε_uncond、ε_cond、w 各是什麼；w＝0、1、大於 1 各會怎樣；label dropout 為什麼必要</small></div>
</div>

<div class="muted mt-3" style="font-size:17px">另一半（a）「說明 Diffusion vs GAN」是 D4-4 的備忘錄，會用到 D3 的生成三難表和今天的數字。</div>

<div class="takeaway mt-3">能用自己的話講清楚那一行，才算「實作」：程式可以請 Agent 幫忙，說明不行。</div>

<!--
★ 學習評量（3 分）：繳交方式（Colab 連結或 .ipynb 檔）與口試時間由講師宣布（outline 待講師決定）。口試大約 2 分鐘一人，題目就是「練習：用數字解釋你的 CFG 那一行」。
-->

---

<div class="eyebrow">06 · 風險（Risk）</div>

# 風險：合成資料會放大原本的偏差

<div class="grid grid-cols-2 gap-6 mt-3" style="font-size:18px">
<div class="node node--warm"><strong>模型只會畫它學過的樣子</strong><small>少數類別的真實圖本來就少，模型對那一類學得最差；生成圖可能都是同一種款式（高 w 時更明顯），分類器反而學得更偏</small></div>
<div class="node node--primary"><strong>驗收一定用真實資料</strong><small>生成圖只能進訓練集，不能進測試集；比較「加生成圖前後」分類器在<b>真實</b>測試圖上的表現（延伸題 2）</small></div>
</div>

<div class="takeaway mt-4">合成資料是「補充」，不是「證據」：測試集永遠只放真實資料。</div>

<!--
★ 風險（3 分）：舉例：如果真實的少數類別裡某種顏色或款式特別少，生成圖會更少，分類器在那種款式上會更差。人臉、醫療等資料這種偏差的後果更嚴重。
-->

---

<div class="eyebrow">總整理</div>

# 今天學到的概念鏈

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-4">
  <span class="chip">p(x｜y)</span><span class="arrow">→</span>
  <span class="chip">類別嵌入 ＋ 時間嵌入</span><span class="arrow">→</span>
  <span class="chip">label dropout 10%</span><span class="arrow">→</span>
  <span class="chip">ε_uncond ＋ w·(ε_cond − ε_uncond)</span><span class="arrow">→</span>
  <span class="chip">忠實 vs 多樣</span><span class="arrow">→</span>
  <span class="chip">FID／KID</span>
</div>

<div class="takeaway mt-6">一個模型、一次訓練、偶爾藏起標籤；取樣時把「有條件」和「沒條件」的差放大 w 倍。</div>

<div class="muted mt-3" style="font-size:17px">下一堂把「類別編號」換成「一段文字」：Stable Diffusion 的 guidance_scale 就是今天的 w。</div>

<!--
★ 總整理（2 分）：請學員不看投影片，念一次 CFG 那一行的讀法。
-->

---

<div class="eyebrow">隨堂檢核</div>

# 選擇題（iPAS 題型）

<div class="mcq" style="font-size:17px">

1. 本課的 lab 中，類別 y 是怎麼交給 U-Net 的？（　）<br><span class="opts"><span class="nw">A. 把 y 寫在圖片角落</span>　<span class="nw">B. 把 y 當成第 2 個輸入通道的像素值</span>　<span class="nw">C. 查表成向量，和時間向量相加</span>　<span class="nw">D. 只在最後一層加上 y</span></span>
2. 訓練時把 10% 的標籤換成「沒有標籤」，目的是？（　）<br><span class="opts"><span class="nw">A. 防止過度擬合</span>　<span class="nw">B. 讓同一個模型也學會沒條件的預測</span>　<span class="nw">C. 加快訓練</span>　<span class="nw">D. 減少 VRAM</span></span>
3. ε ＝ ε_uncond ＋ w·(ε_cond − ε_uncond) 中，w＝1 時等於？（　）<br><span class="opts"><span class="nw">A. ε_uncond</span>　<span class="nw">B. 0</span>　<span class="nw">C. 兩者平均</span>　<span class="nw">D. ε_cond</span></span>
4. 把 w 從 1 調到 7，最可能的結果？（　）<br><span class="opts"><span class="nw">A. 更像指定類別，但同類更單調</span>　<span class="nw">B. 更多樣，但類別更亂</span>　<span class="nw">C. 取樣變快 7 倍</span>　<span class="nw">D. FID 一定變小</span></span>

</div>

<!--
★ 檢核（3 分）。答案：1 C（B 在別的模型裡也有人用，但本課 lab 不是這樣做）、2 B（A 是 DL 的 dropout，名字像但目的不同）、3 D、4 A（D 錯：太單調時 FID 反而可能變大）。
-->

---
hostOnly: true
---

<div class="eyebrow">下一步</div>

# 下一堂 D4-2：依企劃文字生成產品情境照

<div style="font-size:19px" class="mt-4">

- 行銷部：每次活動都要外拍，能不能用一段企劃文字直接生成？
- 條件從「類別編號」換成「一段文字」：CLIP 把文字變成向量
- Stable Diffusion = D2-3 的 VAE ＋ 今天的條件 U-Net ＋ 文字編碼器 ＋ 排程器

</div>

<!--
★ 下一步（1 分）：預告。提醒學員把今天的筆記本跑完、存到雲端硬碟：學習評量要交。
-->
