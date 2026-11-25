---
theme: default
title: 客服單要花多少 token？注意力從哪裡來
info: |
  生成式AI原理 · D5-1
  客服中心每天 2,000 張繁中客服單：先用 tokenizer 算成本，再從「字序」出發，走過 RNN、seq2seq 的瓶頸，手算一次注意力（Q、K、V）。
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
exportFilename: 17-tokens-attention-bridge
layout: center
class: cover
---

<div class="eyebrow">生成式AI原理 · D5-1</div>

# 客服單要花多少 token？注意力從哪裡來

<p class="subtitle">先算錢，再弄懂模型怎麼「讀」一句話：從字序、RNN、seq2seq 走到注意力</p>

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-8">
  <span class="chip">token 與成本</span><span class="arrow">→</span>
  <span class="chip">BPE</span><span class="arrow">→</span>
  <span class="chip">嵌入＝查表</span><span class="arrow">→</span>
  <span class="chip">字序很重要</span><span class="arrow">→</span>
  <span class="chip">RNN／seq2seq 的瓶頸</span><span class="arrow">→</span>
  <span class="chip">注意力 Q、K、V</span>
</div>

<!--
★ 開場（2 分）：第五天整天都在客服中心。今天先回答兩個問題：用 LLM 處理客服單要花多少錢？模型怎麼知道「先退款再寄回」和「先寄回再退款」不一樣？後半段是 DL 課沒有教的「序列 → 注意力」橋接，約一小時。
-->

---

<div class="eyebrow">00 · Frame（定義問題）</div>

# 客服中心：每天 2,000 張繁中客服單，用 LLM 要花多少？

<div class="ticket mt-2">
  <div class="ticket-head">【需求單 #D5-1】部門：客服中心<span>公司：曜嶼電子 <span class="fiction" style="color:#fff;border-color:#fff">虛構</span></span></div>
  <dl>
    <dt>問題</dt><dd>每天 2,000 張繁中客服單，交給 LLM 處理，每月要花多少？</dd>
    <dt>現況痛點</dt><dd>沒人算過 token；繁中比英文貴多少也不知道</dd>
    <dt>成功指標（KPI）</dt><dd>一張每月成本估算（寫出單價與查價日期）；能手算注意力，並說出詞袋為什麼不夠</dd>
    <dt>可用資料</dt><dd>講師製作的 40 張合成繁中客服單（附英文翻譯）</dd>
    <dt>限制與法規</dt><dd>不能把真實客服單送到免費 API（個資法）</dd>
    <dt>為何現有工具不夠</dt><dd>只數關鍵字的做法，分不出「先退款再寄回」和「先寄回再退款」</dd>
  </dl>
</div>

<!--
★ 需求單（3 分）：強調資料是合成的：每一張都是講師寫的，沒有真實姓名、電話、地址。最後一列是今天後半段的伏筆：字一樣、順序不同，意思相反。
-->

---

<div class="eyebrow">學習目標</div>

# 今天結束時，你能夠……

1. **數出**同一張客服單在 3 種 tokenizer 下的 token 數，**算出**每月成本
2. **說明** BPE 怎麼把常一起出現的字合併成一個 token
3. **說明**嵌入（embedding）就是「編號 → 查表 → 一個向量」
4. **說明**字序為什麼重要，以及 RNN、seq2seq 卡在哪裡
5. **手算**一次注意力：query（查詢）和每個 key（鍵）比 → softmax → 把 value（值）加權相加

<div class="takeaway mt-4">後半段是 DL 課沒教過的橋：今天手算的那一格，就是明天 GPT 每一層在做的事。</div>

<!--
★ 目標（1 分）。不教：LSTM／GRU 的閘門公式（只認名字）、Bahdanau 注意力的細節（附錄）、多頭注意力與 Transformer 整體（D5-2）、tokenizer 的訓練細節（只看合併的概念）。
-->

---

<div class="eyebrow">00 · Frame · 一條算式</div>

# 成本 ＝ token 數 × 單價

<div class="node node--primary mt-2" style="font-size:22px;text-align:center;padding:10px">每月成本 ＝ 每月張數 ×（輸入 token × 輸入單價 ＋ 輸出 token × 輸出單價）</div>

<div class="grid grid-cols-2 gap-6 mt-4" style="font-size:18px">
<div>

- **token**：模型讀寫的最小單位（Vibe 01 學過）
- 廠商**按 token 收費**，單價寫成「每 100 萬個 token 多少美元」
- **輸出通常比輸入貴**：一次只能生一個 token，比較慢、比較佔機器
- 每月張數：2,000 × 30 ＝ **60,000 張**

</div>
<div class="node"><strong>先用假設的單價練習</strong><small>輸入 1 美元／百萬 token、輸出 5 美元／百萬 token（<b>假設值</b>，不是任何廠商的報價）<br>回覆長度 ≈ 客服單的 2 倍<br>→ 每張 token 數 × (1 ＋ 2 × 5) ÷ 1,000,000 × 60,000<br>＝ 每張 token 數 × <b>11 × 0.06</b> 美元</small></div>
</div>

<div class="takeaway mt-3">成本只差在一個數字：「一張客服單是幾個 token」。所以先數 token。</div>

<!--
★ Frame（5 分）：把算式拆開念：「張數乘上每張的錢；每張的錢＝讀進去的 token 乘讀的單價，加上寫出來的 token 乘寫的單價」。單價刻意用假設值，lab 裡請學員自己去價格頁查真實價格、寫上查價日期（價格會變）。
常見誤解：「一個中文字＝一個 token」。下一頁就會看到不是。
-->

---

<div class="eyebrow">01 · Try（先看結果）</div>

# 同一張客服單，三種 tokenizer 切出來不一樣

<div class="grid grid-cols-[1.35fr_1fr] gap-5 mt-1 items-start">
<div style="font-size:16px;line-height:1.5">
<div class="node"><strong>o200k_base：38 個 token</strong><small>您好｜，我｜上｜週｜在｜官｜網｜買｜的｜▯｜▯｜牙｜耳｜機｜左｜耳｜沒有｜…</small></div>
<div class="node mt-1"><strong>cl100k_base：67 個 token</strong><small>您｜好｜，｜我｜上｜▯｜▯｜在｜▯｜▯｜▯｜▯｜▯｜▯｜▯｜的｜▯｜▯｜…</small></div>
<div class="node mt-1"><strong>Qwen2.5：35 個 token</strong><small>您好｜，｜我｜上｜週｜在｜官｜網｜買｜的｜藍｜牙｜耳｜機｜…</small></div>
</div>
<div>

<table style="font-size:16px">
<thead><tr><th>40 張平均</th><th>繁中</th><th>英文</th><th>÷</th></tr></thead>
<tbody>
<tr><td>o200k</td><td>26.4</td><td>22.2</td><td>1.19</td></tr>
<tr><td>cl100k</td><td>41.2</td><td>22.4</td><td><b>1.84</b></td></tr>
<tr><td>Qwen2.5</td><td>23.2</td><td>22.7</td><td>1.02</td></tr>
</tbody>
</table>

</div>
</div>

<div class="shot-cap">第一張客服單（43 個字）的前幾個 token。▯＝一個字的一部分位元組（一個字被拆成 2～3 個 token）；÷＝繁中 ÷ 英文。講師本機實跑（CPU；tiktoken 0.14.0、transformers 5.24.0）</div>

<div class="takeaway mt-1">繁中常常比較貴，但貴多少看 tokenizer：cl100k 1.84 倍，o200k 和 Qwen2.5 只差 0～2 成。</div>

<!--
★ Try（6 分）：先請學員猜「43 個字會是幾個 token」，再揭曉。▯ 是重點：cl100k 不認得「週」「藍」這些字，只好拆成位元組，一個字變 2～3 個 token。新的 tokenizer 詞彙表比較大（o200k 約 20 萬個），收進比較多中文。
Claude 的 tokenizer 沒有公開：要用 API 的 token 計數或回傳的 usage（D5-3）。
-->

---

<div class="eyebrow">02 · Open（打開黑盒子）· BPE</div>

# BPE（位元組對編碼）：最常黏在一起的兩塊，合併成一塊

<div class="grid grid-cols-[1.1fr_1fr] gap-6 mt-2 items-start">
<div>

<table style="font-size:17px">
<thead><tr><th style="width:18%">第幾次</th><th>合併</th><th style="width:28%">出現次數</th></tr></thead>
<tbody>
<tr><td>1</td><td>嗎 ＋ ？ → <b>嗎？</b></td><td>19</td></tr>
<tr><td>2</td><td>可 ＋ 以 → <b>可以</b></td><td>15</td></tr>
<tr><td>4</td><td>沒 ＋ 有 → <b>沒有</b></td><td>7</td></tr>
<tr><td>5</td><td>耳 ＋ 機 → <b>耳機</b></td><td>6</td></tr>
<tr><td>9</td><td>手 ＋ 錶 → <b>手錶</b></td><td>5</td></tr>
</tbody>
</table>
<div class="shot-cap">在 40 張客服單上從「一個字一塊」開始合併（lab 第 2 部分，講師本機實跑）</div>

</div>
<div style="font-size:18px">

1. 數每一對**相鄰**片段出現幾次
2. 最多的那一對 → 合併成新片段，加進詞彙表
3. 回到 1，重複幾萬次

<div class="node node--primary mt-3"><strong>結果</strong><small>常見的詞（可以、耳機）變成 1 個 token；少見的字被拆成位元組。訓練資料裡中文越多，中文越「便宜」</small></div>

</div>
</div>

<div class="takeaway mt-3">tokenizer 是「從資料統計出來的」：它常看到什麼，什麼就便宜。</div>

<!--
★ BPE（6 分）：這就是前一頁的原因。真正的 tokenizer 從位元組（byte）開始、在大量網路文字上合併：英文多，英文就便宜。HF LLM Course 第 6 章用 hug／pug／pun 的小例子講同一件事；我們用自己的客服單。
注意：第 3 次合併「，請」跨過了標點：BPE 只看次數，不懂文法。
-->

---

<div class="eyebrow">02 · Open · 練習</div>

# 練習：估算每月帳單

<div class="grid grid-cols-[1fr_1.35fr] gap-6 mt-1" style="font-size:17px">
<div class="node"><strong>照著做：o200k_base</strong><small>每張平均 26.4 個 token<br>每月 ＝ 26.4 × 11 × 0.06<br>＝ 26.4 × 0.66 ≈ <b>17.4 美元</b><br>（11 ＝ 輸入 1 ＋ 回覆 2 倍 × 5；0.06 ＝ 60,000 張 ÷ 100 萬）</small></div>
<div>

用「Try」那一頁的表，算另外兩個：

<table class="fill tight vlines mt-1">
<thead><tr><th style="width:30%">tokenizer</th><th style="width:22%">每張 token</th><th>每月（美元）</th></tr></thead>
<tbody>
<tr><td>cl100k_base</td><td>41.2</td><td class="blank"><FillIn id="cost.cl100k" hint="例：12.3……" /></td></tr>
<tr><td>Qwen2.5</td><td>23.2</td><td class="blank"><FillIn id="cost.qwen" /></td></tr>
<tr><td colspan="2">最貴的是最便宜的幾倍？</td><td class="blank"><FillIn id="cost.ratio" /></td></tr>
</tbody>
</table>

<FillClear group="cost" />

</div>
</div>

<div class="muted mt-2" style="font-size:16px">做完後：lab 第 1 部分的 <code>monthly_cost()</code> 會印出同樣的數字，對一下。</div>

<!--
★ 練習（8 分）：個人、不收回。先手算，再到 lab 對照。重點不是金額本身（單價是假設的），而是「同樣的客服單，換 tokenizer 就差將近一倍」：選模型時 token 效率也是成本的一部分。
-->

---
hostOnly: true
---

<div class="eyebrow">02 · Open · 練習解答</div>

# 練習解答：同一批客服單，最多差 1.8 倍

<table class="vlines" style="font-size:19px">
<thead><tr><th style="width:30%">tokenizer</th><th>算式</th><th style="width:24%">每月</th></tr></thead>
<tbody>
<tr><td>o200k_base</td><td>26.4 × 0.66</td><td>≈ 17.4 美元</td></tr>
<tr><td>cl100k_base</td><td>41.2 × 0.66</td><td>≈ 27.2 美元</td></tr>
<tr><td>Qwen2.5</td><td>23.2 × 0.66</td><td>≈ 15.3 美元</td></tr>
<tr><td colspan="2">最貴 ÷ 最便宜</td><td>27.2 ÷ 15.3 ≈ 1.8 倍</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">怎麼判斷：成本和 token 數成正比，所以倍數就是 token 數的比：41.2 ÷ 23.2 ≈ 1.8。</div>

<!--
★ 解答（2 分）：lab 印出 27.19 和 15.30（用沒四捨五入的平均）。提醒：真實系統還有每次都要送的系統提示詞，D5-3 會從 API 回傳的 usage 直接讀。
-->

---

<div class="eyebrow">02 · Open · 嵌入（embedding）</div>

# 嵌入：token 編號 → 查表 → 一個向量

<div class="grid grid-cols-[1fr_1fr] gap-6 mt-2 items-center">
<div>

<svg viewBox="0 0 360 250" style="width:100%" aria-label="token 編號 113794 指向一張很高的表格中的一列，那一列是 896 個數字">
  <defs><marker id="emb-a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--primary)"/></marker></defs>
  <rect x="0" y="92" width="118" height="56" rx="6" fill="var(--soft-blue)" stroke="var(--primary)"/>
  <text x="34" y="116" style="font-size:16px" fill="var(--text)">退款</text><text x="10" y="138" style="font-size:16px" fill="var(--text)">＝113794</text>
  <line x1="118" y1="120" x2="148" y2="120" stroke="var(--primary)" stroke-width="2.5" marker-end="url(#emb-a)"/>
  <rect x="150" y="20" width="200" height="200" fill="var(--surface)" stroke="#b8b8b8"/>
  <line x1="150" y1="60" x2="350" y2="60" stroke="#b8b8b8"/><line x1="150" y1="100" x2="350" y2="100" stroke="#b8b8b8"/>
  <rect x="150" y="105" width="200" height="30" fill="var(--soft-amber)" stroke="var(--warm-accent)" stroke-width="2"/>
  <text x="160" y="126" style="font-size:16px" fill="var(--text)">第 113794 列：896 個數字</text>
  <line x1="150" y1="140" x2="350" y2="140" stroke="#b8b8b8"/><line x1="150" y1="180" x2="350" y2="180" stroke="#b8b8b8"/>
  <text x="150" y="242" style="font-size:16px" fill="var(--muted-text)">151,936 列 × 896 欄</text>
</svg>

</div>
<div>

<img class="photo" src="/embed_sim.png" alt="6 個詞兩兩的 cosine 相似度：退貨和換貨 0.54、退貨和退款 0.34，耳機和手錶只有 0.16" style="width:88%">
<div class="shot-cap">Qwen2.5-0.5B 的嵌入，兩兩 cosine 相似度（lab 第 3 部分，講師本機實跑）。「退款」是 1 個 token；其他詞是 2～3 個 token，取平均；退貨和換貨共用「貨」</div>

</div>
</div>

<div class="takeaway mt-2">嵌入是一張可訓練的大表：編號＝第幾列；訓練後，相近的詞，向量也接近。</div>

<!--
★ 嵌入（6 分）：和 D4-1 的類別嵌入 nn.Embedding 是同一個東西，只是表更大。讀圖：退貨／換貨／退款彼此比較像（0.34～0.54），和耳機、手錶、發票不像（0.1～0.2）。
誠實提醒：退貨和換貨都含「貨」這個 token，所以 0.54 有一部分是共用 token 的關係；這個小實驗只能說「同主題比較近」。cosine 相似度在 D4-2 用過。
-->

---

<div class="eyebrow">03 · 序列 → 注意力的橋 · 1</div>

# 只數字的詞袋，分不出順序

<div class="grid grid-cols-2 gap-6 mt-3" style="font-size:20px">
<div class="node node--primary"><strong>先退款再寄回</strong><small>客人想要的流程</small></div>
<div class="node node--warm"><strong>先寄回再退款</strong><small>公司規定的流程</small></div>
</div>

<div class="mt-3" style="font-size:18px">

- 詞袋（bag of words）：只記「每個字出現幾次」，例如「先 1、退 1、款 1、再 1、寄 1、回 1」
- 兩句的詞袋**完全一樣**（lab 印出 <code>True</code>），意思卻相反
- 客服單裡還有：「**不是不喜歡**這支手錶，是錶帶太短」：「不」出現兩次，意思是「喜歡」

</div>

<div class="takeaway mt-3">意思藏在順序裡：模型要知道「哪個字在哪個字前面」。</div>

<!--
★ 橋 1（4 分）：ML 課用過的詞袋／TF-IDF 特徵就是這樣，不管順序。請學員想一個自己工作上「字一樣、順序不同、意思相反」的例子（不用說出來）。
-->

---

<div class="eyebrow">03 · 序列 → 注意力的橋 · 2</div>

# RNN（循環神經網路）：一個字一個字讀，只帶一個小筆記本

<svg viewBox="0 0 900 200" style="width:100%" aria-label="五個方塊排成一列，每個方塊讀一個字，往右傳一個小向量 h；越往右，第一個字的資訊越淡">
  <defs><marker id="rnn-a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--warm-accent)"/></marker>
  <marker id="rnn-b" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--primary)"/></marker></defs>
  <g style="font-size:18px">
  <rect x="20" y="60" width="110" height="60" rx="8" fill="var(--soft-blue)" stroke="var(--primary)"/><text x="62" y="96" fill="var(--text)">RNN</text>
  <rect x="200" y="60" width="110" height="60" rx="8" fill="var(--soft-blue)" stroke="var(--primary)"/><text x="242" y="96" fill="var(--text)">RNN</text>
  <rect x="380" y="60" width="110" height="60" rx="8" fill="var(--soft-blue)" stroke="var(--primary)"/><text x="422" y="96" fill="var(--text)">RNN</text>
  <rect x="560" y="60" width="110" height="60" rx="8" fill="var(--soft-blue)" stroke="var(--primary)"/><text x="602" y="96" fill="var(--text)">RNN</text>
  <rect x="740" y="60" width="110" height="60" rx="8" fill="var(--soft-blue)" stroke="var(--primary)"/><text x="782" y="96" fill="var(--text)">RNN</text>
  <text x="60" y="180" fill="var(--text)">先</text><text x="240" y="180" fill="var(--text)">退款</text><text x="420" y="180" fill="var(--text)">再</text><text x="600" y="180" fill="var(--text)">寄回</text><text x="780" y="180" fill="var(--text)">嗎</text>
  </g>
  <g stroke="var(--primary)" stroke-width="2"><line x1="75" y1="160" x2="75" y2="124" marker-end="url(#rnn-b)"/><line x1="255" y1="160" x2="255" y2="124" marker-end="url(#rnn-b)"/><line x1="435" y1="160" x2="435" y2="124" marker-end="url(#rnn-b)"/><line x1="615" y1="160" x2="615" y2="124" marker-end="url(#rnn-b)"/><line x1="795" y1="160" x2="795" y2="124" marker-end="url(#rnn-b)"/></g>
  <g stroke="var(--warm-accent)" stroke-width="3"><line x1="130" y1="90" x2="196" y2="90" marker-end="url(#rnn-a)"/><line x1="310" y1="90" x2="376" y2="90" marker-end="url(#rnn-a)"/><line x1="490" y1="90" x2="556" y2="90" marker-end="url(#rnn-a)"/><line x1="670" y1="90" x2="736" y2="90" marker-end="url(#rnn-a)"/></g>
  <text x="140" y="50" style="font-size:17px" fill="var(--warm-accent)">h₁</text><text x="320" y="50" style="font-size:17px" fill="var(--warm-accent)">h₂</text><text x="500" y="50" style="font-size:17px" fill="var(--warm-accent)">h₃</text><text x="680" y="50" style="font-size:17px" fill="var(--warm-accent)">h₄</text>
</svg>

<div class="grid grid-cols-2 gap-6 mt-1" style="font-size:18px">
<div>

- 每一步：讀一個字 ＋ 上一步的 **h**（隱藏狀態，hidden state）→ 新的 h
- 順序有了：「先」一定比「退款」早進來

</div>
<div class="node node--warm"><strong>瓶頸</strong><small>整句話的記憶都塞在一個固定長度的 h；句子一長，前面的字被一路改寫、越來越淡。而且要一個字等一個字，不能平行算</small></div>
</div>

<div class="takeaway mt-2">RNN 解決了順序，卻把所有記憶塞進同一本小筆記本。</div>

<div class="src">DL 課第 7、29 頁提過 RNN 的名字，沒有實作（curriculum-analysis）</div>

<!--
★ 橋 2（6 分）：比喻：一個人聽電話，只准在一張便利貼上記筆記，每聽一個字就擦掉一點重寫。聽完 50 個字，第一個字還剩多少？這張圖只有一種讀法：從左到右。
常見誤解：「RNN 看得到整句」。它每一步只看得到現在這個字和 h。
-->

---

<div class="eyebrow">03 · 序列 → 注意力的橋 · 3</div>

# seq2seq（序列到序列）：整句話壓成一個向量，再展開

<svg viewBox="0 0 900 190" style="width:100%" aria-label="左邊四個編碼器方塊把客服單讀完，最後只留下一個向量 c，像漏斗；右邊解碼器只能看 c 來寫回覆">
  <defs><marker id="s2s-a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--warm-accent)"/></marker></defs>
  <g style="font-size:17px">
  <rect x="10" y="60" width="80" height="50" rx="8" fill="var(--soft-blue)" stroke="var(--primary)"/><rect x="110" y="60" width="80" height="50" rx="8" fill="var(--soft-blue)" stroke="var(--primary)"/><rect x="210" y="60" width="80" height="50" rx="8" fill="var(--soft-blue)" stroke="var(--primary)"/><rect x="310" y="60" width="80" height="50" rx="8" fill="var(--soft-blue)" stroke="var(--primary)"/>
  <text x="28" y="90" style="font-size:15px" fill="var(--text)">RNN</text><text x="128" y="90" style="font-size:15px" fill="var(--text)">RNN</text><text x="228" y="90" style="font-size:15px" fill="var(--text)">RNN</text><text x="328" y="90" style="font-size:15px" fill="var(--text)">RNN</text>
  <text x="20" y="140" fill="var(--text)">左耳</text><text x="115" y="140" fill="var(--text)">沒有聲音</text><text x="230" y="140" fill="var(--text)">……</text><text x="320" y="140" fill="var(--text)">換貨嗎</text>
  <text x="120" y="40" fill="var(--primary)">編碼器（讀客服單）</text>
  <circle cx="470" cy="85" r="26" fill="var(--soft-amber)" stroke="var(--warm-accent)" stroke-width="3"/><text x="462" y="91" fill="var(--text)">c</text>
  <text x="400" y="150" fill="var(--warm-accent)">只剩一個向量</text>
  <rect x="560" y="60" width="80" height="50" rx="8" fill="var(--surface)" stroke="var(--secondary)"/><rect x="660" y="60" width="80" height="50" rx="8" fill="var(--surface)" stroke="var(--secondary)"/><rect x="760" y="60" width="80" height="50" rx="8" fill="var(--surface)" stroke="var(--secondary)"/>
  <text x="575" y="140" fill="var(--text)">您好</text><text x="680" y="140" fill="var(--text)">請</text><text x="770" y="140" fill="var(--text)">……</text>
  <text x="600" y="40" fill="var(--secondary)">解碼器（寫回覆）</text>
  </g>
  <g stroke="var(--warm-accent)" stroke-width="2.5"><line x1="90" y1="85" x2="106" y2="85" marker-end="url(#s2s-a)"/><line x1="190" y1="85" x2="206" y2="85" marker-end="url(#s2s-a)"/><line x1="290" y1="85" x2="306" y2="85" marker-end="url(#s2s-a)"/><line x1="640" y1="85" x2="656" y2="85" marker-end="url(#s2s-a)"/><line x1="740" y1="85" x2="756" y2="85" marker-end="url(#s2s-a)"/></g>
  <line x1="390" y1="85" x2="440" y2="85" stroke="var(--warm-accent)" stroke-width="3" marker-end="url(#s2s-a)"/>
  <line x1="496" y1="85" x2="556" y2="85" stroke="var(--warm-accent)" stroke-width="3" marker-end="url(#s2s-a)"/>
</svg>

<div class="mt-2" style="font-size:19px">

- 用在翻譯、摘要、寫回覆：一個 RNN 讀完整句（**編碼器**），另一個 RNN 照著寫（**解碼器**）
- 解碼器寫每一個字時，**只能看那一個向量 c**，看不到原句

</div>

<div class="takeaway mt-3">句子越長，c 越裝不下：寫到「換貨」時，早就忘了是「左耳」壞掉。</div>

<!--
★ 橋 3（5 分）：同一個漏斗的比喻：電話聽完，只交出一張便利貼給寫回信的人。2014 年的機器翻譯就是這樣，長句翻得特別差。下一頁的想法很直接：寫回信的人，能不能隨時翻回原句看？
-->

---

<div class="eyebrow">03 · 序列 → 注意力的橋 · 4</div>

# 注意力（attention）：每寫一個字，都回頭看每一個字

<div class="grid grid-cols-[1.1fr_1fr] gap-6 mt-1 items-center">
<div>

<svg viewBox="0 0 400 240" style="width:100%" aria-label="上方一個字「螢幕」發出三條線，分別連到下方的螢幕、破了、退貨；線的粗細代表權重 0.38、0.23、0.38">
  <rect x="140" y="10" width="120" height="44" rx="8" fill="var(--soft-amber)" stroke="var(--warm-accent)" stroke-width="2"/>
  <text x="150" y="38" style="font-size:17px" fill="var(--text)">query：螢幕</text>
  <rect x="10" y="170" width="110" height="44" rx="8" fill="var(--soft-blue)" stroke="var(--primary)"/><text x="40" y="198" style="font-size:17px" fill="var(--text)">螢幕</text>
  <rect x="145" y="170" width="110" height="44" rx="8" fill="var(--soft-blue)" stroke="var(--primary)"/><text x="175" y="198" style="font-size:17px" fill="var(--text)">破了</text>
  <rect x="280" y="170" width="110" height="44" rx="8" fill="var(--soft-blue)" stroke="var(--primary)"/><text x="310" y="198" style="font-size:17px" fill="var(--text)">退貨</text>
  <line x1="200" y1="54" x2="65" y2="168" stroke="var(--warm-accent)" stroke-width="7"/>
  <line x1="200" y1="54" x2="200" y2="168" stroke="var(--warm-accent)" stroke-width="3"/>
  <line x1="200" y1="54" x2="335" y2="168" stroke="var(--warm-accent)" stroke-width="7"/>
  <text x="70" y="120" style="font-size:17px" fill="var(--warm-accent)">0.38</text><text x="208" y="125" style="font-size:17px" fill="var(--warm-accent)">0.23</text><text x="300" y="120" style="font-size:17px" fill="var(--warm-accent)">0.38</text>
</svg>

</div>
<div style="font-size:18px">

**像去圖書館查資料**

- **query（查詢）**：我現在想找什麼
- **key（鍵）**：每本書的書背標籤
- **value（值）**：書的內容
- 每本都翻一下，**越符合的看越多**，最後把看到的內容按比例混在一起

</div>
</div>

<div class="takeaway mt-2">注意力是「軟性查表」：不是只挑一本，而是每本都拿一點，比例由相似度決定。</div>

<!--
★ 橋 4（7 分）：線的粗細就是權重，加起來等於 1。和 seq2seq 比：不再只給一張便利貼，每寫一個字都能翻回原句的任何一個字。3Blue1Brown、李宏毅老師的 self-attention 投影片都是「一個 query 連到每一個 key」這張圖，我們用同一個畫法。
這三個字和權重就是下一頁「照著算」的例子；「退貨」那一列留給練習。
-->

---

<div class="eyebrow">03 · 注意力 · Q、K、V 一步一步</div>

# 照著算一次：「螢幕」這個 query 怎麼看三個字

<div class="grid grid-cols-[1fr_1.15fr] gap-6 mt-1" style="font-size:17px">
<div>

<table class="vlines">
<thead><tr><th></th><th>key（k）</th><th>value（v）</th></tr></thead>
<tbody>
<tr><td>螢幕</td><td>[1, 0, 0, 0]</td><td>[1, 0]</td></tr>
<tr><td>破了</td><td>[0, 0, 2, 0]</td><td>[0, 1]</td></tr>
<tr><td>退貨</td><td>[1, 0, 1, 0]</td><td>[1, 1]</td></tr>
</tbody>
</table>
<div class="mt-2">query「螢幕」：q ＝ &#91;1, 0, 0, 0&#93;<br>d ＝ 每個 key 向量的長度（這裡 4 個數），√d ＝ 2</div>

</div>
<div class="steps">
  <div><span class="num">1</span>內積 q·k（對應位置相乘再相加）：<b>1、0、1</b></div>
  <div><span class="num">2</span>÷ √d：<b>0.5、0、0.5</b></div>
  <div><span class="num">3</span>softmax：e^0.5 ≈ 1.65、e^0 ＝ 1 → 1.65 ÷ 4.30 … → <b>0.38、0.23、0.38</b></div>
  <div><span class="num">4</span>加權相加 value：0.38×[1,0] ＋ 0.23×[0,1] ＋ 0.38×[1,1] ＝ <b>[0.77, 0.62]</b></div>
</div>
</div>

```python
weights = torch.softmax(Q @ K.T / math.sqrt(d), dim=-1)   # 每個 query 對每個 key 的權重
out = weights @ V                                          # 按權重把 value 加起來
```

<div class="muted" style="font-size:16px">讀作：「Q 和每個 K 做內積、除以根號 d、變成加總為 1 的權重，再拿權重去混合 V」。lab 印出的第一列：<code>[0.384, 0.233, 0.384]</code>。</div>

<!--
★ Q、K、V（7 分）：一步一步在白板上寫。softmax 是 DL 課第 16 頁學過的（把分數變成加起來為 1 的機率），這裡不重教。
Q、K、V 從哪來？真實模型裡是同一個字的嵌入乘上三個不同的可訓練矩陣（W_Q、W_K、W_V）；今天的玩具直接給數字，讓手算可行。
常見誤解：key 和 value 是同一個東西。key 用來「比」，value 用來「拿」。
-->

---

<div class="eyebrow">03 · 注意力 · 為什麼除以 √d</div>

# 為什麼要除以 √d：不讓 softmax 變成「只看一個」

<div class="grid grid-cols-2 gap-6 mt-4" style="font-size:19px">
<div class="node node--warm"><strong>不除：最大權重 0.812</strong><small>d ＝ 64 的隨機向量，內積是 64 項相加，數字很大；softmax 幾乎把全部權重給一個字，其他字的梯度接近 0，學不動</small></div>
<div class="node node--primary"><strong>除以 √64 ＝ 8：最大權重 0.273</strong><small>分數縮回合理範圍，8 個字都分得到一些注意力</small></div>
</div>

<div class="shot-cap mt-2">lab 第 4 部分：1 個 query、8 個 key、d ＝ 64、seed 0（講師本機實跑）</div>

<div class="takeaway mt-4">向量越長，內積越大；除以 √d 把分數拉回來，softmax 才不會太早「只看一個」。</div>

<!--
★ √d（3 分）：只要一句話：d 越大，內積的數值範圍越大（大約跟 √d 成正比），所以除以 √d。不推導。
-->

---

<div class="eyebrow">03 · 注意力 · 練習</div>

# 練習：手算「退貨」這個 query

<div class="grid grid-cols-[1fr_1.3fr] gap-6 mt-1" style="font-size:17px">
<div>

用上一頁的 key 和 value 表；<br>query「退貨」：q ＝ <code>&#91;1, 0, 1, 0&#93;</code>，<span class="nw">√d ＝ 2</span>

<div class="node mt-2"><strong>用得到的數字</strong><small>e^0 ＝ 1、e^0.5 ≈ 1.65、e^1 ≈ 2.72</small></div>

</div>
<div>

<table class="fill tight vlines">
<thead><tr><th style="width:22%">步驟</th><th>螢幕</th><th>破了</th><th>退貨</th></tr></thead>
<tbody>
<tr><td>q·k</td><td class="blank"><FillIn id="att.s1" hint="例：3……" /></td><td class="blank"><FillIn id="att.s2" /></td><td class="blank"><FillIn id="att.s3" /></td></tr>
<tr><td>÷ √d</td><td class="blank"><FillIn id="att.d1" /></td><td class="blank"><FillIn id="att.d2" /></td><td class="blank"><FillIn id="att.d3" /></td></tr>
<tr><td>權重</td><td class="blank"><FillIn id="att.w1" /></td><td class="blank"><FillIn id="att.w2" /></td><td class="blank"><FillIn id="att.w3" /></td></tr>
<tr><td>輸出</td><td colspan="3" class="blank"><FillIn id="att.out" hint="例：[0.1, 0.9]……" /></td></tr>
</tbody>
</table>

<FillClear group="att" />

</div>
</div>

<div class="muted mt-2" style="font-size:16px">做完後：lab 第 4 部分印出的「退貨」那一列，就是你的權重列。</div>

<!--
★ 無 AI 檢核點（8 分）：個人作業、不收回。要學員自己發現：「退貨」最注意的不是「螢幕」，而是「破了」和自己。權重的三個數加起來一定等於 1，可以自我檢查。
-->

---
hostOnly: true
---

<div class="eyebrow">03 · 注意力 · 練習解答</div>

# 練習解答：「退貨」看「破了」和自己最多

<table class="vlines" style="font-size:19px">
<thead><tr><th style="width:22%">步驟</th><th>螢幕</th><th>破了</th><th>退貨</th></tr></thead>
<tbody>
<tr><td>q·k</td><td>1</td><td>2</td><td>2</td></tr>
<tr><td>÷ √d</td><td>0.5</td><td>1</td><td>1</td></tr>
<tr><td>權重</td><td>1.65 ÷ 7.09 ≈ 0.23</td><td>2.72 ÷ 7.09 ≈ 0.38</td><td>≈ 0.38</td></tr>
<tr><td>輸出</td><td colspan="3">0.23×[1,0] ＋ 0.38×[0,1] ＋ 0.38×[1,1] ≈ [0.62, 0.77]</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">怎麼判斷：權重加起來 ＝ 1；lab 印出 <code>[0.233, 0.384, 0.384]</code>、輸出 <code>[0.616, 0.767]</code>。</div>

<!--
★ 解答（2 分）：7.09 ＝ 1.65 ＋ 2.72 ＋ 2.72。和「螢幕」那一列比：同一組 key 和 value，換一個 query，權重就換了：這就是「軟性查表」。
-->

---

<div class="eyebrow">04 · 延伸 · 只認名字</div>

# LSTM、GRU：幫 RNN 加上「閘門」

<div class="grid grid-cols-2 gap-6 mt-4" style="font-size:19px">
<div class="node"><strong>LSTM（長短期記憶）、GRU（閘門循環單元）</strong><small>在 RNN 的小筆記本上加幾個「閘門」：決定哪些舊筆記要擦、哪些新內容要寫進去。比 RNN 記得久</small></div>
<div class="node node--warm"><strong>還是同一個瓶頸</strong><small>仍然一個字等一個字算；仍然只有一本固定大小的筆記本。注意力和 Transformer 讓它們在 LLM 裡退場</small></div>
</div>

<div class="takeaway mt-4">看到 LSTM、GRU：知道是「加了閘門的 RNN」就夠了。</div>

<div class="src">官方課程地圖列有 LSTM／GRU；DL 課沒有教（curriculum-analysis）</div>

<!--
○ 選修（2 分）：只認名字，不講閘門公式。語音、感測器時間序列等小型任務仍然常用。
-->

---

<div class="eyebrow">附錄 · 備用</div>

# 注意力的由來：翻譯模型「回頭看」原句（選讀）

<div class="mt-4" style="font-size:19px">

- 2014 年 Bahdanau 等人：seq2seq 的解碼器每寫一個字，對編碼器的**每一個** h 算分數、softmax、加權相加
- 它是「解碼器看編碼器」（跨序列）；今天手算的是「一句話裡的字互相看」（self-attention，自注意力）
- 2017 年 *Attention Is All You Need*：乾脆拿掉 RNN，只留注意力 → Transformer（明天）

</div>

<div class="takeaway mt-4">從「RNN ＋ 注意力」到「只要注意力」：拿掉一個字等一個字的限制，才能用 GPU 平行算。</div>

<div class="src">Bahdanau, Cho, Bengio, 2014（S5，待確認）；Vaswani et al., 2017（S6，待確認）</div>

<!--
△ 附錄（1 分）：學員問「注意力是誰發明的」時再講。
-->

---

<div class="eyebrow">05 · Lab L5-1</div>

# Lab 1／3：Specify

<div style="font-size:17px" class="mt-1">

**打開筆記本**：<code>lab17-tokens-attention.ipynb</code>（在 <code>materials/</code>）→ Open in Colab（<code>colab.research.google.com/github/LinTzuYu0925/GAI_tutorial/blob/day5-done/17-tokens-attention-bridge/materials/lab17-tokens-attention.ipynb</code>）；執行階段：**CPU 就可以**（Colab「執行階段 → 變更執行階段類型 → CPU」）；四個部分：token 與成本 → 自己寫 BPE → 嵌入與詞袋 → 注意力

<strong>【目標】</strong>估出每月成本；手寫注意力，再看真實模型在看哪裡<br>
<strong>【輸入與輸出】</strong>40 張合成客服單（從課程 GitHub 下載）→ token 表、每月成本；Q <code>&#91;3,4&#93;</code>、K <code>&#91;3,4&#93;</code>、V <code>&#91;3,2&#93;</code> → 權重 <code>&#91;3,3&#93;</code>、輸出 <code>&#91;3,2&#93;</code><br>
<strong>【限制】</strong>只用合成資料；不呼叫任何付費 API<br>
<strong>【驗收】</strong>① 成本和你的手算一致　② 權重每一列加起來 ＝ 1　③ 「退貨」那一列 ＝ 練習答案

</div>

<div class="takeaway mt-3">兩個 TODO：<code>monthly_cost()</code> 的算式、<code>attention()</code> 的三行。</div>

<!--
★ Lab 開始（3 分）：這是橋接 lab，用三頁的簡化流程（和 D1-3 一樣）。第 3、4 部分會下載 Qwen2.5-0.5B（約 1 GB），CPU 執行階段也跑得動：講師本機 CPU 讀模型約 5 秒、熱力圖不到 1 秒。
-->

---

<div class="eyebrow">05 · Lab L5-1</div>

# Lab 2／3：Generate → Execute

<PromptBox>
這是 PyTorch 筆記本，請只填兩個 # TODO：<br>
① monthly_cost()：每張輸入＝客服單 token，輸出＝REPLY_RATIO 倍；乘單價（每 100 萬 token），再乘 TICKETS_PER_DAY × DAYS<br>
② attention()：scores ＝ Q @ K.T ÷ √d；weights ＝ 每一列 softmax；out ＝ weights @ V<br>
不要改資料和其他格子。每一行加中文註解。
</PromptBox>

<div class="muted" style="font-size:15px">Agent 寫出來應該像這樣（對照用）：</div>

```python
scores = Q @ K.T / math.sqrt(d)          # 每個 query 和每個 key 的相似度
weights = torch.softmax(scores, dim=-1)  # 每一列加起來 = 1
out = weights @ V                        # 按權重混合 value
```

<div class="steps mt-1" style="font-size:16px">
  <div><span class="num">1</span>預期輸出：<code>「退貨」那一列： {'螢幕': 0.23…, '破了': 0.38…, '退貨': 0.38…}</code></div>
  <div><span class="num">2</span>沒有 Agent 額度：照上面三行填；卡住開 <code>-solution.ipynb</code></div>
</div>

<div class="node node--warm mt-1" style="font-size:16px"><strong>常見錯誤</strong><small><code>softmax(dim=0)</code>：變成每一「欄」加起來 ＝ 1，權重的意思就錯了。驗收 ② 會抓到</small></div>

<!--
★ 執行（16 分）：dim＝-1 是「沿著最後一個維度」，也就是每一列。學員最常寫成 dim=0，數字看起來也是 0～1 之間，但每一列加起來不是 1。
-->

---

<div class="eyebrow">05 · Lab L5-1</div>

# Lab 3／3：Audit：真實模型在看哪裡？

<div class="grid grid-cols-[0.8fr_1.2fr] gap-5 mt-1 items-start">
<div>

<img class="photo" src="/attention_heatmap.png" alt="Qwen2.5-0.5B 第 12 層的注意力熱力圖，只有左下三角形有顏色，大多集中在對角線附近" style="width:100%">
<div class="shot-cap">第 12 層；每層有好幾組 Q、K、V（頭，明天細講），這裡取平均、拿掉第一欄。講師本機實跑；＊＝一個字的部分位元組</div>

</div>
<div style="font-size:16px">

句子：「錶帶太短戴不上，可以只換錶帶嗎？」

| 看什麼 | 實際 |
|---|---|
| 只有左下三角有顏色？ | 是：每個字只看自己和**前面**的字（明天的 causal mask，因果遮罩） |
| 第一個 token 拿多少？ | 平均 0.47：模型的「休息站」，先拿掉 |
| 「換」最注意？ | 自己 0.26、只 0.16、可以 0.13 |

<div class="steps mt-1" style="font-size:16px"><div><span class="num">1</span>延伸：<code>LAYER</code> 改成 2 或 20，只重跑那一格</div><div><span class="num">2</span>交付三行成本便條：tokenizer、每月成本＋查價日期、個資風險</div></div>

</div>
</div>

<div class="takeaway mt-1">熱力圖是線索，不是模型做決定的理由。</div>

<!--
★ 稽核（8 分）：誠實講結果：這一層大多看附近的字，「換」最注意「只」和「可以」：合理，但不是每一層、每個頭都這樣。可以請學員把 LAYER 改成 2 或 20 重跑那一格，比較看看（一次只改一件事）。
注意力圖常被當成「模型的解釋」，但有研究指出它不一定反映模型做決定的原因（S8，待確認）：當線索看就好。
-->

---

<div class="eyebrow">06 · 風險（Risk）</div>

# 風險：真實客服單有個資，不能直接貼到免費 API

<div class="grid grid-cols-2 gap-6 mt-3" style="font-size:18px">
<div class="node node--warm"><strong>客服單裡常有</strong><small>姓名、電話、地址、訂單編號、信用卡末四碼。依個資法，蒐集、處理、利用個資都要有特定目的（細節由法務確認）；免費方案的服務條款可能允許廠商把輸入拿去改進模型</small></div>
<div class="node node--primary"><strong>今天的做法</strong><small>只用合成資料；正式上線前先去識別化（遮掉個資），並讀清楚服務條款與資料存放地區（D5-3）</small></div>
</div>

<div class="takeaway mt-4">算成本用合成資料就夠了：token 數只跟長度、語言和 tokenizer 有關，不需要真的個資。</div>

<!--
★ 風險（3 分）：法條細節由法務判斷，這裡只建立習慣：送出去之前先問「裡面有沒有個資」。D5-3 會把資料落地、服務條款、授權放進決策表。
-->

---

<div class="eyebrow">總整理</div>

# 今天學到的概念鏈

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-4">
  <span class="chip">token 數 × 單價</span><span class="arrow">→</span>
  <span class="chip">BPE：常見的合併</span><span class="arrow">→</span>
  <span class="chip">嵌入：編號查表</span><span class="arrow">→</span>
  <span class="chip">詞袋丟掉順序</span><span class="arrow">→</span>
  <span class="chip">RNN：一本小筆記本</span><span class="arrow">→</span>
  <span class="chip">seq2seq：一個向量</span><span class="arrow">→</span>
  <span class="chip">注意力：每個字都回頭看</span>
</div>

<div class="takeaway mt-6">注意力 ＝ query 和每個 key 比 → ÷√d → softmax → 按權重混合 value。</div>

<div class="muted mt-3" style="font-size:17px">明天的 GPT：把這一格疊很多層、開很多頭，再加上「不准偷看後面」的遮罩。</div>

<!--
★ 總整理（2 分）：請學員不看投影片，說出 Q、K、V 各是什麼（查詢、標籤、內容）。
-->

---

<div class="eyebrow">隨堂檢核</div>

# 選擇題（iPAS 題型）

<div class="mcq" style="font-size:17px">

1. 同一張繁中客服單，用不同 tokenizer 算出的 token 數不同，主要原因是？（　）<br><span class="opts"><span class="nw">A. 中文字數不同</span>　<span class="nw">B. 詞彙表從不同的訓練資料統計出來</span>　<span class="nw">C. 網路速度不同</span>　<span class="nw">D. 模型參數量不同</span></span>
2. 嵌入層（embedding）對一個 token 編號做的事是？（　）<br><span class="opts"><span class="nw">A. 取出表格中對應的那一列向量</span>　<span class="nw">B. 把編號除以詞彙表大小</span>　<span class="nw">C. 把編號轉成 one-hot 後輸出</span>　<span class="nw">D. 計算編號的雜湊值</span></span>
3. seq2seq（RNN 編碼器－解碼器）處理長句時的主要瓶頸是？（　）<br><span class="opts"><span class="nw">A. 詞彙表太小</span>　<span class="nw">B. 整句被壓成一個固定長度的向量</span>　<span class="nw">C. softmax 太慢</span>　<span class="nw">D. 不能用 GPU</span></span>
4. 注意力分數除以 √d 的目的？（　）<br><span class="opts"><span class="nw">A. 讓權重加起來等於 1</span>　<span class="nw">B. 減少參數量</span>　<span class="nw">C. 避免分數太大、softmax 只集中在一個字</span>　<span class="nw">D. 讓輸出變成正數</span></span>

</div>

<!--
★ 檢核（3 分）。答案：1 B、2 A（C 錯：one-hot 再乘矩陣的「結果」等於查表，但輸出的是那一列向量）、3 B（D 錯：RNN 能用 GPU，只是不能平行處理整句）、4 C（A 是 softmax 本身的作用）。
-->

---
hostOnly: true
---

<div class="eyebrow">下一步</div>

# 下一堂 D5-2：模型怎麼「寫」出一封回覆

<div style="font-size:19px" class="mt-4">

- 客服主管：不信任黑盒子，先懂它怎麼寫
- 寫字 ＝ 預測下一個 token，一直重複（D1-2 的文字接龍）
- 今天的注意力 → 多頭、遮罩、位置編碼 → Transformer 區塊 → 自己訓練一個迷你 GPT

</div>

<!--
★ 下一步（1 分）：預告。今天的 attention() 明天會直接用到。
-->
