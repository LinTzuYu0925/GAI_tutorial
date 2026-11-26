---
theme: default
title: 模型怎麼寫出一封回覆
info: |
  生成式AI原理 · L18
  客服主管不信任黑盒子：把 L17 的注意力疊成 Transformer 區塊，訓練一個迷你字元 GPT，看懂 next-token、cross-entropy、溫度／top-k／top-p 與 KV cache。
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
exportFilename: 18-mini-gpt
layout: center
class: cover
---

<div class="eyebrow">生成式AI原理 · L18</div>

# 模型怎麼寫出一封回覆

<p class="subtitle">把昨天的注意力疊成 Transformer：自己訓練一個會寫繁中客服回覆的迷你 GPT</p>

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-8">
  <span class="chip">文字接龍</span><span class="arrow">→</span>
  <span class="chip">多頭注意力</span><span class="arrow">→</span>
  <span class="chip">不准偷看</span><span class="arrow">→</span>
  <span class="chip">位置編碼</span><span class="arrow">→</span>
  <span class="chip">Transformer 區塊</span><span class="arrow">→</span>
  <span class="chip">cross-entropy</span><span class="arrow">→</span>
  <span class="chip">溫度／top-k／top-p</span>
</div>

<!--
★ 開場（2 分）：昨天手算了一格注意力。今天把它疊起來，變成會寫字的模型，而且自己從零訓練一個。客服主管的問題是：「它到底怎麼寫出來的？我能不能控制它？」
-->

---

<div class="eyebrow">00 · Frame（定義問題）</div>

# 客服中心：把回覆交給模型寫之前，要先懂它怎麼「寫」

<div class="ticket mt-2">
  <div class="ticket-head">【需求單 #L18】部門：客服中心<span>公司：曜嶼電子 <span class="fiction" style="color:#fff;border-color:#fff">虛構</span></span></div>
  <dl>
    <dt>問題</dt><dd>模型寫客服回覆時，到底在做什麼？哪些旋鈕能讓它保守一點？</dd>
    <dt>現況痛點</dt><dd>主管不信任黑盒子</dd>
    <dt>成功指標（KPI）</dt><dd>loss 曲線下降；一張「設定 → 樣本 → 照抄率」的樣本表</dd>
    <dt>可用資料</dt><dd>5,606 封合成繁中客服回覆（課程用模板產生）</dd>
    <dt>限制與法規</dt><dd>Colab T4；小模型</dd>
    <dt>為何現有工具不夠</dt><dd>L17 只有一層注意力，還不會生成</dd>
  </dl>
</div>

<!--
★ 需求單（3 分）：「照抄率」今天會定義：寫出的句子有幾成和訓練資料一字不差。這是我們用來量「保守 vs 亂寫」的尺。
-->

---

<div class="eyebrow">學習目標</div>

# 今天結束時，你能夠……

1. **畫出** Transformer 區塊：多頭注意力、causal mask（因果遮罩）、位置編碼、殘差 ＋ LayerNorm（層正規化）
2. **分辨** BERT、T5、GPT 是 Transformer 的哪一種用法
3. **讀懂** next-token cross-entropy 的 loss 曲線：它就是「最大概似」
4. **使用**溫度、top-k、top-p，說出各自怎麼改變樣本
5. **說明** KV cache 為什麼讓生成變快

<div class="takeaway mt-4">今天訓練的迷你 GPT 和 ChatGPT、Claude 是同一個家族：差在大小、資料和後續訓練（L20）。</div>

<!--
★ 目標（1 分）。不教：GQA／MQA 的實作（只認名字）、注意力複雜度的推導（附錄）、RoPE 的公式（只認名字）、預訓練以外的訓練階段（L20）。
-->

---

<div class="eyebrow">00 · Frame · 回到 L02</div>

# 寫字 ＝ 預測下一個 token，一直重複

<svg viewBox="0 0 900 190" style="width:100%" aria-label="文字接龍的迴圈：目前的文字送進模型，得到下一個 token 的機率，抽一個接到後面，再送回模型">
  <defs><marker id="loop-a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--primary)"/></marker></defs>
  <g style="font-size:18px">
  <rect x="10" y="50" width="250" height="60" rx="8" fill="var(--soft-blue)" stroke="var(--primary)"/><text x="24" y="86" fill="var(--text)">您好，關於您的耳機…我們</text>
  <rect x="330" y="50" width="150" height="60" rx="8" fill="var(--surface)" stroke="var(--secondary)" stroke-width="2"/><text x="372" y="86" fill="var(--text)">模型</text>
  <rect x="550" y="40" width="150" height="80" rx="8" fill="var(--soft-amber)" stroke="var(--warm-accent)"/><text x="562" y="72" fill="var(--text)">可以 0.21</text><text x="562" y="100" fill="var(--text)">需要 0.06 …</text>
  <rect x="770" y="50" width="120" height="60" rx="8" fill="var(--soft-blue)" stroke="var(--primary)"/><text x="782" y="86" fill="var(--text)">抽一個</text>
  </g>
  <g stroke="var(--primary)" stroke-width="2.5" fill="none"><line x1="260" y1="80" x2="326" y2="80" marker-end="url(#loop-a)"/><line x1="480" y1="80" x2="546" y2="80" marker-end="url(#loop-a)"/><line x1="700" y1="80" x2="766" y2="80" marker-end="url(#loop-a)"/>
  <path d="M830,112 L830,165 L135,165 L135,114" marker-end="url(#loop-a)"/></g>
  <text x="330" y="186" style="font-size:17px" fill="var(--primary)">接到後面（＋可以），再送回去</text>
</svg>

<div class="takeaway mt-3">一封回覆＝這個迴圈跑幾百次；每次只決定一個 token。</div>

<!--
★ Frame（4 分）：L02 已經看過「文字接龍」。今天要打開中間那個「模型」方塊，並且自己訓練一個。圖裡的機率是下一頁真實模型的輸出。
-->

---

<div class="eyebrow">01 · Try（先看結果）</div>

# 真的小模型：下一個 token 的前 10 名

<img class="photo" src="/qwen_next_token.png" alt="三張長條圖：同一組前 10 名 token，溫度 0.5 時「可以」約 0.82，溫度 1.0 時約 0.21，溫度 1.5 時全部都很低" style="width:100%">
<div class="shot-cap">Qwen2.5-0.5B-Instruct，提示「您好，關於您的耳機左耳沒有聲音，我們」；lab 第 1 部分，講師本機實跑（CPU，fp32）</div>

<div class="takeaway mt-2">模型給的是一整排機率，不是一個答案；溫度只是把同一排機率變尖或變平。</div>

<!--
★ Try（5 分）：先請學員猜「我們」後面最可能是什麼。T＝1.0 時「可以」0.21、「需要」0.06。T＝1.5 時前 10 名加起來都很小：機率被攤給其他十幾萬個 token，這就是「溫度高 → 亂寫」的來源。第 14 頁會把三個旋鈕講清楚。
-->

---

<div class="eyebrow">02 · Open（打開黑盒子）· 多頭注意力</div>

# 多頭注意力（multi-head attention）：好幾組查表同時做

<div class="grid grid-cols-[1.1fr_1fr] gap-6 mt-2 items-center">
<div>

<svg viewBox="0 0 400 230" style="width:100%" aria-label="同一句話送進四個注意力頭，每個頭輸出 32 維，接起來變成 128 維，再經過一層混合">
  <defs><marker id="mh-a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--primary)"/></marker></defs>
  <g style="font-size:16px">
  <rect x="10" y="95" width="90" height="44" rx="8" fill="var(--soft-blue)" stroke="var(--primary)"/><text x="18" y="122" fill="var(--text)">x：128 維</text>
  <rect x="150" y="10" width="100" height="36" rx="6" fill="var(--soft-amber)" stroke="var(--warm-accent)"/><text x="160" y="34" fill="var(--text)">頭 1：32 維</text>
  <rect x="150" y="65" width="100" height="36" rx="6" fill="var(--soft-amber)" stroke="var(--warm-accent)"/><text x="160" y="89" fill="var(--text)">頭 2：32 維</text>
  <rect x="150" y="120" width="100" height="36" rx="6" fill="var(--soft-amber)" stroke="var(--warm-accent)"/><text x="160" y="144" fill="var(--text)">頭 3：32 維</text>
  <rect x="150" y="175" width="100" height="36" rx="6" fill="var(--soft-amber)" stroke="var(--warm-accent)"/><text x="160" y="199" fill="var(--text)">頭 4：32 維</text>
  <rect x="290" y="88" width="105" height="58" rx="8" fill="var(--soft-blue)" stroke="var(--primary)"/><text x="298" y="112" fill="var(--text)">接起來</text><text x="298" y="134" fill="var(--text)">128 → 混合</text>
  </g>
  <g stroke="var(--primary)" stroke-width="1.8"><line x1="100" y1="117" x2="146" y2="28" marker-end="url(#mh-a)"/><line x1="100" y1="117" x2="146" y2="83" marker-end="url(#mh-a)"/><line x1="100" y1="117" x2="146" y2="138" marker-end="url(#mh-a)"/><line x1="100" y1="117" x2="146" y2="193" marker-end="url(#mh-a)"/>
  <line x1="250" y1="28" x2="288" y2="105" marker-end="url(#mh-a)"/><line x1="250" y1="83" x2="288" y2="110" marker-end="url(#mh-a)"/><line x1="250" y1="138" x2="288" y2="120" marker-end="url(#mh-a)"/><line x1="250" y1="193" x2="288" y2="128" marker-end="url(#mh-a)"/></g>
</svg>

</div>
<div style="font-size:18px">

- 每個頭是一次 L17 的注意力，有自己的 W_Q、W_K、W_V
- 不同的頭可以學會看不同的關係，例如有的看前一個字、有的看產品名稱（示意）
- 頭數 × 每頭維度 ＝ 原本維度（4 × 32 ＝ 128）

</div>
</div>

<div class="takeaway mt-2">一個頭只能用一種角度查表；多頭讓模型同時用好幾種角度看同一句話。</div>

<!--
★ 多頭（5 分）：比喻：同一張客服單，請四個同事各看一個重點（產品、情緒、要求、時間），最後把四份筆記合在一起。昨天熱力圖說的「頭平均」就是把這幾個頭平均起來。
-->

---

<div class="eyebrow">02 · Open · causal mask</div>

# Causal mask（因果遮罩）：寫字時不准偷看後面

<div class="grid grid-cols-[1fr_1.2fr] gap-6 mt-2 items-center">
<div>

<table class="vlines" style="font-size:18px;text-align:center">
<thead><tr><th></th><th>您</th><th>好</th><th>，</th><th>請</th></tr></thead>
<tbody>
<tr><td><b>您</b></td><td>✓</td><td>✕</td><td>✕</td><td>✕</td></tr>
<tr><td><b>好</b></td><td>✓</td><td>✓</td><td>✕</td><td>✕</td></tr>
<tr><td><b>，</b></td><td>✓</td><td>✓</td><td>✓</td><td>✕</td></tr>
<tr><td><b>請</b></td><td>✓</td><td>✓</td><td>✓</td><td>✓</td></tr>
</tbody>
</table>

</div>
<div style="font-size:18px">

- 每一列是「正在讀的字」，每一欄是「被看的字」
- ✕ 的格子：分數換成 −∞，softmax 後權重 ＝ 0
- 為什麼：訓練時整句一次送進去，每個位置都要猜下一個字；不遮的話，答案就在旁邊

```python
att = att.masked_fill(self.tril[:T, :T] == 0, float("-inf"))
```
<div class="muted" style="font-size:15px">讀作：「下三角以外（未來的字）的分數，全部換成負無限大」</div>

</div>
</div>

<div class="takeaway mt-2">昨天的熱力圖只有左下三角有顏色，就是因為這個遮罩。</div>

<!--
★ causal mask（5 分）：e 的負無限大次方 ＝ 0，所以 softmax 後權重是 0。這是 lab 的第一個 TODO。
常見誤解：「遮罩是為了讓模型變笨」。不是：是讓訓練和生成的情況一樣：生成時本來就還沒有後面的字。
-->

---

<div class="eyebrow">02 · Open · 位置編碼</div>

# 位置編碼（positional encoding）：告訴模型「第幾個字」

<div class="grid grid-cols-[1fr_1.1fr] gap-6 mt-2 items-center">
<div style="font-size:18px">

- 注意力本身**不知道順序**：打亂字序，分數都一樣
- 每個位置加上一條**獨特的條紋**：和 **L11 的時間嵌入**同一個公式，「第幾步」換成「第幾個字」

</div>
<div>

<svg viewBox="0 0 360 200" style="width:100%" aria-label="四條不同頻率的正弦波，對應向量的不同維度；同一個位置在每一條波上取一個值，組成那個位置的向量">
  <g fill="none" stroke-width="2">
  <path d="M10,40 Q30,10 50,40 T90,40 T130,40 T170,40 T210,40 T250,40 T290,40 T330,40" stroke="var(--primary)"/>
  <path d="M10,90 Q50,60 90,90 T170,90 T250,90 T330,90" stroke="var(--secondary)"/>
  <path d="M10,140 Q90,110 170,140 T330,140" stroke="var(--warm-accent)"/>
  </g>
  <line x1="130" y1="10" x2="130" y2="165" stroke="#b8b8b8" stroke-dasharray="4 3"/>
  <circle cx="130" cy="40" r="5" fill="var(--primary)"/><circle cx="130" cy="73" r="5" fill="var(--secondary)"/><circle cx="130" cy="126" r="5" fill="var(--warm-accent)"/>
  <text x="70" y="190" style="font-size:16px" fill="var(--muted-text)">第 5 個字：取三個點</text>
  <text x="230" y="190" style="font-size:16px" fill="var(--muted-text)">快 → 慢的條紋</text>
</svg>

</div>
</div>

```python
x = self.tok(idx) + self.pos[:T]     # 查表得到「是哪個字」＋「在第幾個位置」
```

<div class="takeaway mt-2">嵌入說「是哪個字」，位置說「在哪裡」：相加後，「先退款再寄回」和「先寄回再退款」才分得開。</div>

<!--
★ 位置編碼（5 分）：接回 L17 的詞袋問題：注意力如果沒有位置資訊，就和詞袋一樣分不出順序。指著虛線：第 5 個字在每一條波上各取一個值，組成它專屬的向量。L11 的時間嵌入用的是同一招，學員看過程式。新模型多用 RoPE（旋轉位置編碼），只認名字。
-->

---

<div class="eyebrow">02 · Open · Transformer 區塊</div>

# 殘差 ＋ LayerNorm：組成一個 Transformer 區塊

<div class="grid grid-cols-[1fr_1.15fr] gap-6 mt-1 items-center">
<div>

<svg viewBox="0 0 310 300" style="width:78%" aria-label="由下往上：輸入 x，經過 LayerNorm 與多頭注意力後加回 x，再經過 LayerNorm 與前饋網路後再加回去，輸出同樣形狀">
  <defs><marker id="blk-a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--primary)"/></marker></defs>
  <g style="font-size:16px">
  <text x="100" y="292" fill="var(--text)">x：[B, T, 128]</text>
  <rect x="60" y="215" width="150" height="34" rx="6" fill="var(--surface)" stroke="#b8b8b8"/><text x="92" y="237" fill="var(--text)">LayerNorm</text>
  <rect x="60" y="170" width="150" height="34" rx="6" fill="var(--soft-amber)" stroke="var(--warm-accent)"/><text x="82" y="192" fill="var(--text)">多頭注意力</text>
  <circle cx="135" cy="145" r="12" fill="#fff" stroke="var(--primary)"/><text x="129" y="150" fill="var(--primary)">＋</text>
  <rect x="60" y="85" width="150" height="34" rx="6" fill="var(--surface)" stroke="#b8b8b8"/><text x="92" y="107" fill="var(--text)">LayerNorm</text>
  <rect x="60" y="40" width="150" height="34" rx="6" fill="var(--soft-blue)" stroke="var(--primary)"/><text x="86" y="62" fill="var(--text)">前饋網路</text>
  <circle cx="135" cy="18" r="12" fill="#fff" stroke="var(--primary)"/><text x="129" y="23" fill="var(--primary)">＋</text>
  </g>
  <g stroke="var(--primary)" stroke-width="2" fill="none">
  <line x1="135" y1="275" x2="135" y2="251" marker-end="url(#blk-a)"/><line x1="135" y1="215" x2="135" y2="206" marker-end="url(#blk-a)"/><line x1="135" y1="170" x2="135" y2="159" marker-end="url(#blk-a)"/>
  <line x1="135" y1="133" x2="135" y2="121" marker-end="url(#blk-a)"/><line x1="135" y1="85" x2="135" y2="76" marker-end="url(#blk-a)"/><line x1="135" y1="40" x2="135" y2="32" marker-end="url(#blk-a)"/>
  <path d="M135,262 L250,262 L250,145 L149,145" stroke-dasharray="5 3" marker-end="url(#blk-a)"/>
  <path d="M135,138 L265,138 L265,18 L149,18" stroke-dasharray="5 3" marker-end="url(#blk-a)"/>
  </g>
  <text x="256" y="205" style="font-size:17px" fill="var(--primary)">殘差</text>
</svg>

</div>
<div style="font-size:18px">

- **注意力**：每個字去看別的字（交流）
- **前饋網路**：每個字自己想一想（兩層全連接）
- **殘差**（虛線）：原本的 x 直接加回來：DL 學過的 ResNet skip connection（DL 第 38–55 頁）
- **LayerNorm**（層正規化）：把每個字的向量拉回差不多的大小，深的網路才訓練得動
- 進出形狀一樣，所以可以**疊很多層**：lab 疊 4 層

</div>
</div>

<div class="takeaway mt-1">一個區塊＝「交流一次＋自己想一次」，各自加回 x；GPT 就是很多個區塊疊起來。</div>

<!--
★ 區塊（6 分）：殘差是 DL 課 ResNet 學過的，不重教；LayerNorm 和 BatchNorm 類似，但是對「每一個字」自己正規化，不看整個 batch。
lab 的 Block 類別就是這張圖由下往上念：x ＝ x ＋ attn(ln1(x))；x ＝ x ＋ ffwd(ln2(x))。
-->

---

<div class="eyebrow">02 · Open · 練習</div>

# 練習：形狀走過一個區塊

<div class="grid grid-cols-[1fr_1.6fr] gap-5 mt-1" style="font-size:17px">
<div class="node"><strong>lab 的設定</strong><small>B ＝ 64（一批幾段）、T ＝ 64（一段幾個字）<br>C ＝ 128（向量長度）、4 個頭<br>字的種類 ＝ 339</small></div>
<div>

<table class="fill tight vlines">
<thead><tr><th style="width:30%">哪一塊</th><th style="width:30%">輸入</th><th>輸出</th></tr></thead>
<tbody>
<tr><td>嵌入 <code>tok</code></td><td>[64, 64]</td><td>[64, 64, 128]</td></tr>
<tr><td>一個頭的 q</td><td>[64, 64, 128]</td><td class="blank"><FillIn id="shape.q" hint="例：[8, 8, 8]……" /></td></tr>
<tr><td>分數 q·kᵀ</td><td>兩個 q、k</td><td class="blank"><FillIn id="shape.att" /></td></tr>
<tr><td>多頭接起來</td><td>4 個頭</td><td class="blank"><FillIn id="shape.mh" /></td></tr>
<tr><td>輸出層 <code>head</code></td><td>[64, 64, 128]</td><td class="blank"><FillIn id="shape.logits" /></td></tr>
</tbody>
</table>

<FillClear group="shape" />

</div>
</div>

<div class="muted mt-2" style="font-size:16px">第一列已填好。做完後：lab 第 2 部分印出 <code>輸入 (64, 64) → logits (64, 64, 339)</code>，對照最後一列。</div>

<!--
★ 無 AI 檢核點（8 分）：個人作業。關鍵是每個頭的維度 ＝ 128 ÷ 4；分數矩陣是「T × T」：每個字對每個字一個分數。
-->

---
hostOnly: true
---

<div class="eyebrow">02 · Open · 練習解答</div>

# 練習解答：只有分數矩陣是 T × T

<table class="vlines" style="font-size:19px">
<thead><tr><th style="width:30%">哪一塊</th><th style="width:30%">輸出</th><th>為什麼</th></tr></thead>
<tbody>
<tr><td>一個頭的 q</td><td>[64, 64, 32]</td><td>128 ÷ 4 個頭 ＝ 32</td></tr>
<tr><td>分數 q·kᵀ</td><td>[64, 64, 64]</td><td>每個字對每個字（T × T）</td></tr>
<tr><td>多頭接起來</td><td>[64, 64, 128]</td><td>4 × 32 ＝ 128，回到原本形狀</td></tr>
<tr><td>輸出層 <code>head</code></td><td>[64, 64, 339]</td><td>每個位置：339 種字各一個分數</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">怎麼判斷：在 <code>Head.forward</code> 裡加 <code>print(q.shape, att.shape)</code>。T × T 就是 context 變長時記憶體爆增的原因（第 17 頁）。</div>

<!--
★ 解答（2 分）：學員常把分數矩陣寫成 [64, 64, 32]。提醒：q 乘 k 的轉置，32 那一維被「內積」吃掉了。
-->

---

<div class="eyebrow">02 · Open · 三種用法</div>

# Transformer 的三種用法：BERT、T5、GPT

<div class="grid grid-cols-3 gap-4 mt-3" style="font-size:17px">
<div class="node"><strong>只有編碼器：BERT</strong><small>沒有遮罩，每個字都能看前後 → 擅長「讀懂」：分類、找關鍵字、做搜尋用的向量（L22）</small></div>
<div class="node node--secondary"><strong>編碼器－解碼器：T5</strong><small>一邊讀完整句、一邊寫：就是 L17 的 seq2seq，只是 RNN 換成 Transformer → 翻譯、摘要</small></div>
<div class="node node--primary"><strong>只有解碼器：GPT</strong><small>有 causal mask，只看前面 → 擅長「接著寫」。今天的迷你 GPT、Qwen、Claude 都是這一種</small></div>
</div>

<div class="takeaway mt-4">差別只在「能不能看後面」和「有沒有兩段」；區塊本身都是同一種。</div>

<!--
★ 地圖（5 分）：看到一個新模型名字，先問：它是讀的（編碼器）、寫的（解碼器），還是兩段的？Whisper（語音轉文字）就是編碼器－解碼器。
-->

---

<div class="eyebrow">02 · Open · loss</div>

# 猜下一個字的 cross-entropy ＝ 最大概似

<div class="grid grid-cols-[1.1fr_1fr] gap-6 mt-1 items-center">
<div>

<img class="photo" src="/minigpt_loss.png" alt="迷你 GPT 的 loss：從 6.03 在 100 步內掉到 0.37，2000 步後約 0.17；灰色點線是亂猜的 ln 339 等於 5.83" style="width:100%">
<div class="shot-cap">lab 第 3 部分：2000 步，講師本機 CPU 785 秒（T4 待講師實跑）；cross-entropy：DL 課第 25–27 頁</div>

</div>
<div style="font-size:18px">

- 每個位置：正確答案的機率取 −log，再平均
- 讓這個 loss 變小 ＝ 讓**訓練資料出現的機率最大**：最大概似（maximum likelihood）
- **起點 6.03**：比平均亂猜的 ln 339 ≈ 5.83 還差一點（隨機初始化的分數不平均）
- **終點約 0.17**：e^−0.17 ≈ 0.84，正確的下一個字平均拿到約 8 成機率

</div>
</div>

<div class="takeaway mt-1">loss 的白話：「平均給正確答案幾成把握」。語料是模板做的，特別好猜；真實文字低不到這麼多。</div>

<!--
★ MLE（5 分）：cross-entropy 是 DL 課分類學過的，不重教；新的是「每一個位置都是一題 339 選 1 的分類題」。e^−loss 是幾何平均的機率，白話說成「平均幾成把握」即可。
常見誤解：loss 很低 ＝ 模型很聰明。這裡低是因為語料只有幾十種句子：下一頁會看到它「只會背」。
-->

---

<div class="eyebrow">02 · Open · 三個旋鈕</div>

# 溫度、top-k、top-p：作用在同一排機率上

<div class="grid grid-cols-3 gap-4 mt-2" style="font-size:17px">
<div class="node node--primary"><strong>溫度 T</strong><small>分數 ÷ T 再 softmax：T＜1 更尖、更保守；T＞1 更平、更敢寫</small></div>
<div class="node node--secondary"><strong>top-k</strong><small>只留機率最高的 k 個，其他歸零</small></div>
<div class="node node--warm"><strong>top-p</strong><small>由高到低累加，留到累加 ≥ p 為止</small></div>
</div>

<table class="mt-3" style="font-size:17px">
<thead><tr><th style="width:24%">設定</th><th style="width:20%">照抄率</th><th>迷你 GPT 寫出來（seed 0）</th></tr></thead>
<tbody>
<tr><td>T＝0.5</td><td>100%</td><td>…電熱水壺有保溫功能，可以設定 40 到 100 度。…</td></tr>
<tr><td>T＝2.0</td><td>6%</td><td>您好，感謝您的來擇超前凍問題都可以直接回覆這封信。</td></tr>
<tr><td>T＝2.0、top-k＝5</td><td>67%</td><td>…可以設定 到 40 100 度。…</td></tr>
<tr><td>T＝2.0、top-p＝0.9</td><td>36%</td><td>…點選「忘記密碼祝您會謝謝您的謝您的耐心與支持。</td></tr>
</tbody>
</table>
<div class="shot-cap">照抄率＝寫出的句子有幾成和訓練資料一字不差（每種設定 20 封）；lab 第 4 部分，講師本機實跑</div>

<div class="takeaway mt-1">溫度決定「多敢」；top-k／top-p 剪掉機率很低的尾巴，T 高時能救回一部分。</div>

<!--
★ 三個旋鈕（6 分）：照抄率太高＝只會背、太低＝亂寫。客服回覆通常要保守：低溫度＋top-p。T＝1.0 的照抄率是 99%（lab 印出），表上省略。
常見誤解：top-k 和 top-p 一樣。top-k 固定留幾個；top-p 依「把握」決定留幾個：模型很確定時可能只留 1 個，不確定時留很多個。
-->

---

<div class="eyebrow">02 · Open · KV cache</div>

# KV cache：前面的 key、value 不用每次重算

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-2 items-center">
<div>

<svg viewBox="0 0 420 210" style="width:100%" aria-label="第 1 步算了三個字的 K 和 V；第 2 步只多算一個新字的 K 和 V，其餘從快取拿">
  <g style="font-size:16px">
  <text x="10" y="30" fill="var(--text)">第 1 步</text>
  <rect x="80" y="12" width="60" height="28" rx="4" fill="var(--soft-amber)" stroke="var(--warm-accent)"/><text x="94" y="32" fill="var(--text)">您</text>
  <rect x="145" y="12" width="60" height="28" rx="4" fill="var(--soft-amber)" stroke="var(--warm-accent)"/><text x="159" y="32" fill="var(--text)">好</text>
  <rect x="210" y="12" width="60" height="28" rx="4" fill="var(--soft-amber)" stroke="var(--warm-accent)"/><text x="228" y="32" fill="var(--text)">，</text>
  <text x="285" y="32" fill="var(--warm-accent)">算 3 組 K、V</text>
  <text x="10" y="100" fill="var(--text)">第 2 步</text>
  <rect x="80" y="82" width="60" height="28" rx="4" fill="var(--soft-blue)" stroke="var(--primary)"/><text x="94" y="102" fill="var(--text)">您</text>
  <rect x="145" y="82" width="60" height="28" rx="4" fill="var(--soft-blue)" stroke="var(--primary)"/><text x="159" y="102" fill="var(--text)">好</text>
  <rect x="210" y="82" width="60" height="28" rx="4" fill="var(--soft-blue)" stroke="var(--primary)"/><text x="228" y="102" fill="var(--text)">，</text>
  <rect x="275" y="82" width="60" height="28" rx="4" fill="var(--soft-amber)" stroke="var(--warm-accent)"/><text x="289" y="102" fill="var(--text)">請</text>
  <text x="80" y="140" fill="var(--primary)">藍色：從快取拿</text><text x="240" y="140" fill="var(--warm-accent)">橘色：只算新的 1 組</text>
  <text x="10" y="190" fill="var(--muted-text)">代價：快取要放在 VRAM，context 越長越大</text>
  </g>
</svg>

</div>
<div>

<table style="font-size:18px">
<thead><tr><th>Qwen2.5-0.5B，生成 100 個 token</th><th>秒</th></tr></thead>
<tbody>
<tr><td>開 KV cache</td><td>8.2</td></tr>
<tr><td>關 KV cache</td><td>37.5</td></tr>
</tbody>
</table>
<div class="shot-cap">lab 第 5 部分，講師本機 CPU 實跑（同一台機器另一次 15.0 vs 53.3 秒）；T4 待講師實跑</div>

</div>
</div>

<div class="takeaway mt-2">因為有 causal mask，舊字的 K、V 不會因為新字而改變，所以可以存起來重用。</div>

<!--
★ KV cache（5 分）：為什麼可以存：舊的字看不到新的字（遮罩），所以它們的 K、V 永遠一樣。每一步只要算新字的 q、k、v。代價是記憶體：這也是 L19 算 VRAM 時，context 長度會影響的原因。
-->

---

<div class="eyebrow">02 · Open · 回到第四天</div>

# DiT：現在換 Transformer 來畫圖

<svg viewBox="0 0 900 170" style="width:100%" aria-label="雜訊的潛在圖切成小方塊，每塊變成一個 token，和時間步、文字條件一起送進 Transformer 區塊，輸出每一塊的雜訊預測">
  <defs><marker id="dit-a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--primary)"/></marker></defs>
  <g style="font-size:17px">
  <rect x="10" y="40" width="90" height="90" fill="var(--surface)" stroke="#b8b8b8"/>
  <line x1="40" y1="40" x2="40" y2="130" stroke="#b8b8b8"/><line x1="70" y1="40" x2="70" y2="130" stroke="#b8b8b8"/><line x1="10" y1="70" x2="100" y2="70" stroke="#b8b8b8"/><line x1="10" y1="100" x2="100" y2="100" stroke="#b8b8b8"/>
  <text x="10" y="160" fill="var(--text)">有雜訊的潛在圖</text>
  <rect x="160" y="65" width="170" height="40" rx="6" fill="var(--soft-amber)" stroke="var(--warm-accent)"/><text x="170" y="91" fill="var(--text)">切塊 → 9 個 token</text>
  <rect x="390" y="45" width="210" height="80" rx="8" fill="var(--soft-blue)" stroke="var(--primary)" stroke-width="2"/><text x="410" y="80" fill="var(--text)">Transformer 區塊 × N</text><text x="410" y="108" style="font-size:15px" fill="var(--muted-text)">＋ 時間 t ＋ 條件（類別）</text>
  <rect x="660" y="65" width="220" height="40" rx="6" fill="var(--soft-amber)" stroke="var(--warm-accent)"/><text x="672" y="91" fill="var(--text)">每一塊的雜訊預測 ε̂</text>
  </g>
  <g stroke="var(--primary)" stroke-width="2.5"><line x1="100" y1="85" x2="156" y2="85" marker-end="url(#dit-a)"/><line x1="330" y1="85" x2="386" y2="85" marker-end="url(#dit-a)"/><line x1="600" y1="85" x2="656" y2="85" marker-end="url(#dit-a)"/></g>
</svg>

<div class="mt-2" style="font-size:18px">

- L14 的 Stable Diffusion 用 U-Net 去噪；DiT 把 U-Net 換成今天的 Transformer 區塊
- 圖片切成小方塊，**每一塊當一個 token**；注意力讓每一塊看其他塊（這裡不用 causal mask）
- DiT 原論文用類別當條件；後來不少文字生圖模型也改用 Transformer 去噪（S9，待確認）

</div>

<div class="takeaway mt-2">Transformer 不只會寫字：任何東西切成 token，它都能處理。</div>

<div class="src">Peebles &amp; Xie, 2023（S6，待確認）；L16 只認過名字</div>

<!--
★ DiT（4 分）：把第四天和第五天接起來：去噪的流程（L11）不變，只換了「誰來預測雜訊」。明天 L21 的 MusicGen 也是：聲音切成 token，交給 Transformer。
-->

---

<div class="eyebrow">03 · 延伸 · 只認名字</div>

# GQA／MQA 與 context 的代價

<div class="grid grid-cols-2 gap-6 mt-4" style="font-size:19px">
<div class="node"><strong>context 越長越貴</strong><small>分數矩陣是 T × T：context 加倍，注意力的計算和記憶體大約變 4 倍；KV cache 也跟著 T 變大（Vibe 01 提過 N × N）</small></div>
<div class="node node--secondary"><strong>GQA／MQA（分組／多查詢注意力）</strong><small>讓好幾個頭共用同一組 K、V：快取變小、生成變快。Qwen2.5 就有用（看模型設定檔的 <code>num_key_value_heads</code>）</small></div>
</div>

<div class="takeaway mt-4">長 context 不是免費的：時間、VRAM、帳單（L17 的 token 成本）都會跟著漲。</div>

<!--
○ 選修（2 分）：只認名字。學員之後讀模型卡看到 GQA，知道是「省 KV cache 的做法」就夠了。
-->

---

<div class="eyebrow">附錄 · 備用</div>

# 注意力的計算量（選讀）

<div class="mt-4" style="font-size:19px">

1. 分數 QKᵀ：T 個字 × T 個字，每對做一次長度 d 的內積 → 約 **T² · d** 次乘法
2. 加權相加 V：同樣約 **T² · d**
3. 記憶體：要存 T × T 的分數矩陣（每個頭一份）
4. 例：T 從 1,000 變 2,000，T² 從 100 萬變 400 萬：**4 倍**

</div>

<div class="takeaway mt-4">「平方」來自每個字都要看每個字；FlashAttention 等技巧不改結果，只是算得更省記憶體。</div>

<!--
△ 附錄（1 分）：學員問「為什麼 context 有上限」時再講。FlashAttention 只認名字。
-->

---

<div class="eyebrow">04 · Lab L5-2</div>

# Lab 1／7：我們要做出什麼？

<div class="grid grid-cols-2 gap-6 mt-2" style="font-size:18px">
<div>

**打開筆記本**：<code>lab18-mini-gpt.ipynb</code>（在 <code>materials/</code>）→ Open in Colab<br>
執行階段：**T4 GPU**；資料：5,606 封合成客服回覆（筆記本自動下載）

1. 一個只有 88 萬參數的模型，學得會繁中客服回覆嗎？
2. 溫度調高，它會開始亂寫嗎？
3. 它寫的句子，事實都對嗎？

</div>
<div>

<div class="node node--primary"><strong>目標樣本（T＝1.0、seed 0）</strong><small>您好，感謝您的來信。非常抱歉，讓您久等了。手機號碼變更需要先驗證舊號碼，再輸入新的號碼。請到登入頁面點選「忘記密碼」，重設信件會在五分鐘內寄出。謝謝您的耐心與支持。</small></div>
<div class="shot-cap">講師本機實跑的迷你 GPT（2000 步）</div>

</div>
</div>

<div class="muted mt-1" style="font-size:14px">Colab：<code>colab.research.google.com/github/LinTzuYu0925/GAI_tutorial/blob/day5-done/18-mini-gpt/materials/lab18-mini-gpt.ipynb</code></div>

<div class="takeaway mt-1">交付給客服主管：一張樣本表（設定 → 樣本 → 照抄率 → 你的評語）。</div>

<!--
★ Lab 開始（3 分）：講師本機 CPU 訓練 2000 步要 785 秒；T4 上應該快很多（待講師實跑）。沒有 GPU：TRAIN＝False，直接載入講師的權重（從 GitHub 下載，約 3.5 MB）。
-->

---

<div class="eyebrow">04 · Lab L5-2</div>

# Lab 2／7：筆記本拆成哪幾塊？

<div class="steps mt-2" style="font-size:18px">
  <div><span class="num">1</span><strong>Qwen 的下一個 token</strong>：<code>qwen(**ids).logits[0, -1]</code> → 前 10 名、三種溫度的長條圖</div>
  <div><span class="num">2</span><strong>MiniGPT</strong>：<code>Head</code>（含遮罩）→ <code>MultiHead</code> → <code>Block</code> × 4；<code>sinusoidal()</code> 位置編碼；輸入 <code>[64, 64]</code> → logits <code>[64, 64, 339]</code></div>
  <div><span class="num">3</span><strong>訓練</strong>：<code>get_batch()</code> 的 y ＝ x 往右移一格；AdamW、2000 步；loss 曲線</div>
  <div><span class="num">4</span><strong>取樣</strong>：<code>filter_logits()</code>（溫度、top-k、top-p）→ <code>generate()</code>；<code>measure()</code> 算照抄率</div>
  <div><span class="num">5</span><strong>KV cache</strong>：Qwen <code>generate(use_cache=True／False)</code> 計時</div>
</div>

<div class="takeaway mt-3">兩個 TODO：causal mask 一行（第 2 部分）、top-p 幾行（第 4 部分）。</div>

<!--
★ 拆塊（3 分）：第 2 部分的類別名稱和投影片的區塊圖一一對應：Head＝一次查表、MultiHead＝多頭、Block＝區塊。
-->

---

<div class="eyebrow">04 · Lab L5-2</div>

# Lab 3／7：Specify

<div style="font-size:18px" class="mt-2">

<strong>【目標】</strong>在合成客服回覆上訓練迷你字元 GPT；比較五種取樣設定<br>
<strong>【輸入與輸出】</strong>x <code>&#91;64, 64&#93;</code>（字的編號）→ logits <code>&#91;64, 64, 339&#93;</code>；y ＝ x 往右移一格；生成：一次一個字<br>
<strong>【限制】</strong>4 層、4 頭、128 維、context 64；不改資料；Colab T4<br>
<strong>【驗收】</strong>① 還沒訓練的 loss ≈ ln 339 ≈ 5.8　② 2000 步後驗證 loss ＜ 0.5　③ 遮罩正確：T＝0.5 的照抄率接近 100%　④ top-p 檢查格：p＝0.8 只留前 3 個

</div>

<div class="muted mt-3" style="font-size:16px">為什麼 ③ 能檢查遮罩：遮罩寫錯時，訓練能「偷看答案」，loss 會降得很低，但生成時沒有答案可看，樣本會亂掉。</div>

<!--
★ Specify（3 分）：驗收 ③ 是這個 lab 最重要的稽核：loss 低不代表對。遮罩漏寫的模型，訓練 loss 甚至更低，但生成一團亂。
-->

---

<div class="eyebrow">04 · Lab L5-2</div>

# Lab 4／7：Generate → Execute

<PromptBox>
這是 PyTorch 筆記本，請只填兩個 # TODO：<br>
① Head.forward()：用 self.tril 做 causal mask：tril 是 0 的位置，att 換成 -inf<br>
② filter_logits() 的 top-p：機率由大到小排序、累加；「累加到前一個為止」已經 ≥ top_p 的字設成 0，再重新加總成 1<br>
不要改模型大小、BLOCK、STEPS。每一行加中文註解。
</PromptBox>

<div class="steps mt-2" style="font-size:17px">
  <div><span class="num">1</span>預期：<code>還沒訓練的 loss：6.0…；全部亂猜…會是 ln(339) = 5.826</code></div>
  <div><span class="num">2</span>預期：每 100 步印一行 loss，100 步內就掉到 0.4 左右</div>
  <div><span class="num">3</span>沒有 Agent 額度：遮罩照「causal mask」頁那一行；top-p 開 <code>-solution.ipynb</code> 對照</div>
</div>

<div class="node node--warm mt-2" style="font-size:16px"><strong>常見錯誤</strong><small>top-p 用「累加含自己」判斷：機率最大的那個字也可能被丟掉，分布變成全 0 → <code>torch.multinomial</code> 報錯。要用「累加到前一個」</small></div>

<!--
★ 執行（約 13 分，含訓練）：訓練時先講下一頁的 loss 怎麼讀。T4 訓練時間待講師實跑後填入。
-->

---

<div class="eyebrow">04 · Lab L5-2</div>

# Lab 5／7：看樣本、量照抄率

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-2" style="font-size:18px">
<div>

跑完第 4 部分後：

1. T＝0.5 和 T＝2.0：哪一個比較像真的客服？
2. T＝2.0 加上 top-k＝5 或 top-p＝0.9：照抄率回升多少？
3. 你會給客服系統用哪一組？寫一句理由

</div>
<div>

<div class="node node--primary"><strong>和隔壁同學比</strong><small>在第 4 部分最上面新增一格 <code>SEED = 你的座號</code>，執行它，再重跑第 4 部分的兩格（不要「全部執行」，否則會重新訓練）</small></div>

</div>
</div>

<div class="takeaway mt-4">「像不像」用眼睛看，「多保守」用照抄率量：兩個都要寫進樣本表。</div>

<!--
★ 對照（6 分）：講師本機的照抄率：T＝0.5 100%、T＝1.0 99%、T＝2.0 6%、＋top-k 67%、＋top-p 36%。學員的數字因 seed、GPU 會略有不同。
-->

---

<div class="eyebrow">04 · Lab L5-2</div>

# Lab 6／7：Audit → Iterate

<table style="font-size:17px">
<thead><tr><th style="width:30%">稽核問題</th><th>具體動作</th><th style="width:32%">應該是</th></tr></thead>
<tbody>
<tr><td>遮罩真的擋住未來嗎？</td><td>跑第 4 部分的「拿掉遮罩」實驗格（新模型、300 步，跑完自動改回）</td><td>loss 降得更低，但樣本亂掉（見講者備註的實跑數字）</td></tr>
<tr><td>top-p 沒有丟掉第一名？</td><td>看檢查格 <code>p＝0.8</code> 的輸出</td><td>前 3 個非 0，加總 ＝ 1</td></tr>
<tr><td>過度擬合了嗎？</td><td>比較最後的 train 和 val loss</td><td>兩者接近（實跑 0.172 vs 0.175）</td></tr>
<tr><td>寫的事實對嗎？</td><td>筆記本列出「訓練資料裡沒有的句子」，對照規格表</td><td>見「風險：流暢 ≠ 正確」</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">一次只改一件事：拿掉遮罩的實驗用另一個模型做，不會動到你訓練好的 <code>model</code>。</div>

<!--
★ 稽核（6 分）：拿掉遮罩的實驗是「loss 低 ≠ 會寫」的最好證據。講師本機 CPU 實跑：不遮罩 300 步 train loss 0.028（有遮罩 2000 步才 0.172），樣本卻是「您好，了解您錶工作天。凍問題都可以直接回覆這封信。……」這種亂接（約 1.5～2.5 分鐘）。
-->

---

<div class="eyebrow">04 · Lab L5-2 · 延伸</div>

# Lab 7／7：延伸：同一個旋鈕，換成真的模型

<div class="grid grid-cols-[1.1fr_1fr] gap-6 mt-2" style="font-size:18px">
<div>

1. 用第 1 部分的 Qwen：<code>qwen.generate(**ids, do_sample=True, temperature=…, top_p=…)</code>
2. 溫度 0.3、1.0、1.5 各生成一次同一封回覆
3. 預測：哪一個比較可能出現簡體字或不通順的句子？

</div>
<div class="node node--warm"><strong>L20 的伏筆</strong><small>L19 的 lab 裡，Qwen 已經在摘要寫出簡體字（講師本機實跑）；L20 用微調修</small></div>
</div>

<div class="takeaway mt-3">迷你 GPT 和 Qwen 用的是同一組旋鈕：今天學的直接用在 L19 的分流助理。</div>

<!--
★ 延伸（3 分）：不給答案頁：結果依模型與 seed 而定，請學員把觀察寫進樣本表。講師可以現場用 T＝1.5 示範一次。
-->

---

<div class="eyebrow">05 · 風險（Risk）</div>

# 風險：流暢 ≠ 正確

<div class="grid grid-cols-2 gap-6 mt-3" style="font-size:18px">
<div class="node node--warm"><strong>資料錯：模型照抄</strong><small>語料裡「電熱水壺支援 iPhone 和 Android，安裝 App 後就能設定。」出現 52 次（模板把產品隨機填進句子；電熱水壺其實沒有 App）。模型會流暢地照寫</small></div>
<div class="node node--primary"><strong>幻覺（hallucination）：模型自己拼錯</strong><small>迷你 GPT 寫出「您好，行動電源容量 2000mAh，……」：訓練資料只有 20000mAh，這句是它把片段拼出來的，語氣通順、數字錯了（lab 第 4 部分，T＝1.3，講師本機實跑）</small></div>
</div>

<div class="takeaway mt-4">模型的目標是「像訓練資料」，不是「說真話」：資料錯它照抄，拼錯它也說得很順。上線前要量（L20）。</div>

<!--
★ 風險（3 分）：左邊是資料錯（我們的模板故意留下的），右邊才是幻覺：模型把「容量 20000mAh」拼成 2000mAh。請學員在 lab 列出的「訓練資料裡沒有的句子」中，對照規格表找一句錯的。真實的大模型也一樣：訓練資料裡的錯、過時資訊，都會被流暢地寫出來。
-->

---

<div class="eyebrow">總整理</div>

# 今天學到的概念鏈

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-4">
  <span class="chip">預測下一個 token</span><span class="arrow">→</span>
  <span class="chip">多頭注意力</span><span class="arrow">→</span>
  <span class="chip">causal mask</span><span class="arrow">→</span>
  <span class="chip">位置編碼</span><span class="arrow">→</span>
  <span class="chip">殘差＋LayerNorm</span><span class="arrow">→</span>
  <span class="chip">cross-entropy＝最大概似</span><span class="arrow">→</span>
  <span class="chip">溫度／top-k／top-p</span><span class="arrow">→</span>
  <span class="chip">KV cache</span>
</div>

<div class="takeaway mt-6">GPT ＝ 嵌入 ＋ 位置 ＋ 很多個「交流＋自己想」區塊 ＋ 輸出層；寫字時每次只抽一個 token。</div>

<!--
★ 總整理（2 分）：請學員不看投影片，畫出 Transformer 區塊（四個方塊、兩條殘差線）。
-->

---

<div class="eyebrow">隨堂檢核</div>

# 隨堂檢核 1／2（iPAS 題型）：點選答案

<Mcq id="quiz1.q1" :n="1" :answer="1"
  :options="['減少參數', '讓每個位置只能看自己和前面的 token', '加快下載', '讓輸出變成繁體字']"
  :why="['mask 不減少參數。', '', '和下載無關。', '輸出用什麼字和 mask 無關。']"
  explain="生成時還沒有後面的字，所以訓練時也要遮住後面的 token，位置 i 只能看到 1…i，訓練和生成才一致。">
GPT 類模型在注意力加上 causal mask 的目的是？
</Mcq>

<Mcq id="quiz1.q2" :n="2" :answer="2"
  :options="['GPT', 'T5', 'BERT', 'Qwen']"
  :why="['GPT 是只有解碼器（有 causal mask）。', 'T5 是編碼器－解碼器。', '', 'Qwen 和 GPT 一樣是解碼器。']"
  explain="BERT 只有編碼器，每個位置能看整句（雙向），適合理解任務，不適合逐字生成。">
下列何者是「只有編碼器」的 Transformer？
</Mcq>

<FillClear group="quiz1" corner />

<!--
★ 檢核 1／2（2 分）：學員自己點；點錯會出現「再想想」和該選項錯在哪，可再點一次。答案：1 B、2 C。
-->

---

<div class="eyebrow">隨堂檢核</div>

# 隨堂檢核 2／2（iPAS 題型）：點選答案

<Mcq id="quiz2.q3" :n="3" :answer="1"
  :options="['輸出更保守、更常重複訓練資料', '機率分布變平，較常出現不通順的字', '生成速度變兩倍', '模型參數改變']"
  :why="['這是降溫（T ＜ 1）的效果。', '', '溫度只改機率分布，不改運算量。', '溫度只在取樣時用，不改參數。']"
  explain="T＝2 把 logits 除以 2，機率分布變平，低機率的字更常被抽中，輸出比較不通順。">
把溫度 T 從 1.0 調到 2.0，最可能的結果？
</Mcq>

<Mcq id="quiz2.q4" :n="4" :answer="0"
  :options="['前面 token 的 key、value 可重用，不必每步重算', '模型變小', '跳過 softmax', '改用 CPU']"
  :why="['', 'KV cache 不縮小模型，反而多用一些記憶體。', 'softmax 還是要算。', '和換 CPU 無關。']"
  explain="前面 token 的 key、value 不會變，存起來重用，每一步只算新 token 那一個。">
KV cache 讓生成變快，是因為？
</Mcq>

<FillClear group="quiz2" corner />

<!--
★ 檢核 2／2（2 分）：學員自己點；點錯會出現「再想想」和該選項錯在哪，可再點一次。答案：3 B、4 A。
全部答案與理由：
1 B：生成時還沒有後面的字，所以訓練時也要遮住後面的 token，位置 i 只能看到 1…i，訓練和生成才一致。
2 C：BERT 只有編碼器，每個位置能看整句（雙向），適合理解任務，不適合逐字生成。
3 B：T＝2 把 logits 除以 2，機率分布變平，低機率的字更常被抽中，輸出比較不通順。
4 A：前面 token 的 key、value 不會變，存起來重用，每一步只算新 token 那一個。
-->


---
hostOnly: true
---

<div class="eyebrow">下一步</div>

# 下一堂 L19：雲端 API 還是自架模型？

<div style="font-size:19px" class="mt-4">

- 資訊部和法務：客服單分類要用雲端 API，還是自架開放模型？
- 同一個分流任務做三次：Claude API、Qwen fp16、Qwen 4-bit
- 要求模型輸出 JSON，用 <code>json.loads</code> 驗證；算每 1,000 張的成本與延遲

</div>

<!--
★ 下一步（1 分）：預告。請學員課後把樣本表完成，明天的分流助理會用到今天的溫度旋鈕。
-->
