---
theme: default
title: 客服單要花多少 token？注意力從哪裡來
info: |
  生成式AI原理 · L17
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

<div class="eyebrow">生成式AI原理 · L17</div>

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
  <div class="ticket-head">【需求單 #L17】部門：客服中心<span>公司：曜嶼電子 <span class="fiction" style="color:#fff;border-color:#fff">虛構</span></span></div>
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
★ 目標（1 分）。不教：LSTM／GRU 的閘門公式（只認名字）、Bahdanau 注意力的細節（附錄）、多頭注意力與 Transformer 整體（L18）、tokenizer 的訓練細節（只看合併的概念）。
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
Claude 的 tokenizer 沒有公開：要用 API 的 token 計數或回傳的 usage（L19）。
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
★ 解答（2 分）：lab 印出 27.19 和 15.30（用沒四捨五入的平均）。提醒：真實系統還有每次都要送的系統提示詞，L19 會從 API 回傳的 usage 直接讀。
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
★ 嵌入（6 分）：和 L13 的類別嵌入 nn.Embedding 是同一個東西，只是表更大。讀圖：退貨／換貨／退款彼此比較像（0.34～0.54），和耳機、手錶、發票不像（0.1～0.2）。
誠實提醒：退貨和換貨都含「貨」這個 token，所以 0.54 有一部分是共用 token 的關係；這個小實驗只能說「同主題比較近」。cosine 相似度在 L14 用過。
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

# 回覆客服單就是 seq2seq：一串字進、一串字出

<svg viewBox="0 0 900 200" style="width:100%" aria-label="左邊是客服單的一串字，中間一個方塊，右邊是回覆的一串字；輸入和輸出長度不一定一樣">
  <defs><marker id="t2t-a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--warm-accent)"/></marker></defs>
  <text x="10" y="30" style="font-size:18px" fill="var(--primary)">輸入：客服單</text>
  <g style="font-size:18px" fill="var(--text)">
  <g stroke="var(--primary)" fill="var(--soft-blue)"><rect x="10" y="60" width="52" height="44" rx="6"/><rect x="68" y="60" width="52" height="44" rx="6"/><rect x="126" y="60" width="52" height="44" rx="6"/><rect x="184" y="60" width="52" height="44" rx="6"/><rect x="242" y="60" width="52" height="44" rx="6"/></g>
  <text x="22" y="89">左</text><text x="80" y="89">耳</text><text x="138" y="89">壞</text><text x="196" y="89">了</text><text x="254" y="89">……</text>
  </g>
  <line x1="300" y1="82" x2="360" y2="82" stroke="var(--warm-accent)" stroke-width="3" marker-end="url(#t2t-a)"/>
  <rect x="364" y="46" width="170" height="72" rx="10" fill="var(--soft-amber)" stroke="var(--warm-accent)" stroke-width="2"/>
  <text x="392" y="90" style="font-size:20px" fill="var(--text)">seq2seq 模型</text>
  <line x1="538" y1="82" x2="598" y2="82" stroke="var(--warm-accent)" stroke-width="3" marker-end="url(#t2t-a)"/>
  <text x="604" y="30" style="font-size:18px" fill="var(--secondary)">輸出：回覆（長度不同）</text>
  <g stroke="var(--secondary)" fill="var(--soft-teal)"><rect x="604" y="60" width="52" height="44" rx="6"/><rect x="662" y="60" width="52" height="44" rx="6"/><rect x="720" y="60" width="52" height="44" rx="6"/><rect x="778" y="60" width="52" height="44" rx="6"/></g>
  <g style="font-size:18px" fill="var(--text)"><text x="616" y="89">您</text><text x="674" y="89">好</text><text x="732" y="89">請</text><text x="790" y="89">……</text></g>
  <text x="10" y="170" style="font-size:17px" fill="var(--muted-text)">seq2seq（序列到序列）：翻譯、摘要、寫客服回覆，都是這個形狀</text>
</svg>

<div class="grid grid-cols-2 gap-6 mt-3" style="font-size:19px">
<div class="node node--primary"><strong>編碼器（encoder）</strong><small>把客服單「讀懂」</small></div>
<div class="node node--warm"><strong>解碼器（decoder）</strong><small>一個字一個字把回覆「寫出來」</small></div>
</div>

<div class="takeaway mt-3">要自動回覆客服單，模型得先讀懂整張單，再一個字一個字寫回覆。</div>

<!--
★ 橋 2（4 分）：先把任務講清楚：客服單是一串字、回覆也是一串字，長度不一樣。這個形狀叫 seq2seq。接下來兩頁：傳統做法是用 RNN 來蓋編碼器和解碼器，然後看它哪裡卡住。
-->

---

<div class="eyebrow">03 · 序列 → 注意力的橋 · 3</div>

# 傳統做法：RNN 一個字一個字讀，只帶一個小筆記本

<svg viewBox="0 0 900 200" style="width:66%;margin:0 auto;display:block" aria-label="五個方塊排成一列，每個方塊讀一個字，往右傳一個小向量 h；越往右，第一個字的資訊越淡">
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

<div class="grid grid-cols-2 gap-6 mt-1" style="font-size:17px">
<div>

- RNN（循環神經網路）每一步：讀一個字 ＋ 上一步的 **h**（隱藏狀態，hidden state）→ 新的 h
- 順序有了：「先」一定比「退款」早進來
- LSTM、GRU：加了「閘門」的 RNN，記得久一點（選修頁再提）

</div>
<div class="node node--warm"><strong>瓶頸</strong><small>整句話的記憶都塞在一個固定長度的 h；句子一長，前面的字被一路改寫、越來越淡。而且要一個字等一個字，不能平行算</small></div>
</div>

<div class="takeaway mt-2">RNN 解決了順序，卻把所有記憶塞進同一本小筆記本。</div>

<div class="src">DL 課第 7、29 頁提過 RNN 的名字，沒有實作（curriculum-analysis）</div>

<!--
★ 橋 3（6 分）：比喻：一個人聽電話，只准在一張便利貼上記筆記，每聽一個字就擦掉一點重寫。聽完 50 個字，第一個字還剩多少？這張圖只有一種讀法：從左到右。LSTM／GRU 一句帶過：幫便利貼加了「要擦哪些、要留哪些」的開關，還是同一張便利貼。
常見誤解：「RNN 看得到整句」。它每一步只看得到現在這個字和 h。
-->

---

<div class="eyebrow">03 · 序列 → 注意力的橋 · 4</div>

# 用 RNN 做 seq2seq：整句話壓成一個向量，再展開

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

- 一個 RNN 讀完整句（**編碼器**），另一個 RNN 照著寫（**解碼器**）
- 解碼器寫每一個字時，**只能看那一個向量 c**，看不到原句
- 更麻煩的是：寫「換貨」時，它**不知道該回頭看原句的哪一個位置**，因為位置資訊早被壓進 c 了

</div>

<div class="takeaway mt-3">句子越長，c 越裝不下：寫到「換貨」時，早就忘了是「左耳」壞掉。</div>

<!--
★ 橋 4（5 分）：同一個漏斗的比喻：電話聽完，只交出一張便利貼給寫回信的人。2014 年的機器翻譯就是這樣，長句翻得特別差。重點有兩個：(1) c 裝不下；(2) 解碼器不知道「現在該看原句的哪個位置」。下一頁的想法很直接：寫回信的人，能不能隨時翻回原句、自己決定看哪裡？
-->

---

<div class="eyebrow">03 · 注意力 · 1：為什麼需要上下文</div>

# 嵌入是查表：同一個字，不管上下文，拿到同一個向量

<div class="grid grid-cols-3 gap-4 mt-3" style="font-size:19px">
<div class="node"><strong>蘋果手機的螢幕破了</strong><small>指的是手機</small></div>
<div class="node"><strong>這顆蘋果很甜</strong><small>指的是水果</small></div>
<div class="node"><strong>蘋果發表新機</strong><small>指的是公司</small></div>
</div>

<div class="grid grid-cols-[1fr_auto_1fr] gap-4 mt-3 items-center" style="font-size:18px">
<div class="node node--warm"><strong>查表之後（第 9 頁）</strong><small>三句話裡的「蘋果」拿到<b>同一個</b>向量，因為查表看不到旁邊的字</small></div>
<div style="font-size:40px;color:var(--warm-accent)">→</div>
<div class="node node--primary"><strong>注意力之後</strong><small>旁邊的字把資訊「傳」進來，同一個「蘋果」變成三個不同的向量：手機、水果、公司</small></div>
</div>

<div class="takeaway mt-3">注意力的工作：把「上下文」加進每個字的向量，讓它從通用的意思，變成這句話裡的意思。</div>

<div class="src">概念順序與例子結構參考 3Blue1Brown〈Visualizing Attention〉（mole 的三種意思）；例子改成繁中客服情境，圖為自製</div>

<!--
★ 注意力 1（4 分）：先講「為什麼要有它」，再講怎麼算（影片的順序：先看想要的行為，才看矩陣）。影片用 mole（鼴鼠／莫耳／痣）；我們用蘋果。重點：嵌入是查表（第 9 頁），查表的時候旁邊有什麼字完全沒用到。
-->

---

<div class="eyebrow">03 · 注意力 · 2：目標與記號</div>

# 目標：讓每個字的向量，吸收旁邊相關字的意思

<svg viewBox="0 0 900 270" style="width:100%" aria-label="三個字螢幕、破了、退貨，各有一個向量 e1、e2、e3，向量裡同時含有字義和位置；經過注意力之後，變成更新後的 e1 prime、e2 prime、e3 prime">
  <defs><marker id="goal-a" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="var(--warm-accent)"/></marker></defs>
  <g style="font-size:20px" fill="var(--text)">
  <text x="20" y="28" style="font-size:17px" fill="var(--muted-text)">輸入：查表得到的向量（字義＋位置）</text>
  <rect x="40" y="50" width="200" height="64" rx="8" fill="var(--soft-blue)" stroke="var(--primary)"/><text x="62" y="78">e₁　螢幕</text><text x="62" y="104" style="font-size:15px" fill="var(--muted-text)">字義 ＋ 位置 1</text>
  <rect x="350" y="50" width="200" height="64" rx="8" fill="var(--soft-blue)" stroke="var(--primary)"/><text x="372" y="78">e₂　破了</text><text x="372" y="104" style="font-size:15px" fill="var(--muted-text)">字義 ＋ 位置 2</text>
  <rect x="660" y="50" width="200" height="64" rx="8" fill="var(--soft-blue)" stroke="var(--primary)"/><text x="682" y="78">e₃　退貨</text><text x="682" y="104" style="font-size:15px" fill="var(--muted-text)">字義 ＋ 位置 3</text>
  </g>
  <rect x="40" y="136" width="820" height="50" rx="10" fill="var(--soft-amber)" stroke="var(--warm-accent)" stroke-width="2"/>
  <text x="300" y="168" style="font-size:20px" fill="var(--text)">注意力：字和字之間互相傳資訊</text>
  <g stroke="var(--warm-accent)" stroke-width="3"><line x1="140" y1="116" x2="140" y2="132" marker-end="url(#goal-a)"/><line x1="450" y1="116" x2="450" y2="132" marker-end="url(#goal-a)"/><line x1="760" y1="116" x2="760" y2="132" marker-end="url(#goal-a)"/>
  <line x1="140" y1="190" x2="140" y2="206" marker-end="url(#goal-a)"/><line x1="450" y1="190" x2="450" y2="206" marker-end="url(#goal-a)"/><line x1="760" y1="190" x2="760" y2="206" marker-end="url(#goal-a)"/></g>
  <g style="font-size:20px" fill="var(--text)">
  <rect x="40" y="210" width="200" height="46" rx="8" fill="var(--soft-teal)" stroke="var(--secondary)"/><text x="62" y="240">e′₁　更新後</text>
  <rect x="350" y="210" width="200" height="46" rx="8" fill="var(--soft-teal)" stroke="var(--secondary)"/><text x="372" y="240">e′₂　更新後</text>
  <rect x="660" y="210" width="200" height="46" rx="8" fill="var(--soft-teal)" stroke="var(--secondary)"/><text x="682" y="240">e′₃　更新後</text>
  </g>
</svg>

<div class="mt-1" style="font-size:18px">

- 向量裡**同時含有「這是什麼字」和「它在第幾個位置」**，所以注意力才知道誰在誰前面，也就是前面 RNN／seq2seq 缺的「位置」
- 我們只看一個注意力「頭」（single head）；真實模型會並排很多個

</div>

<!--
★ 注意力 2（4 分）：影片這一步先定記號 e，並提醒「嵌入其實也編碼了位置」。位置怎麼編碼（位置編碼）留到 L18，這裡只要知道：向量同時帶有字義和位置。
影片用「a fluffy blue creature roamed the verdant forest」，形容詞更新名詞；我們用三個字的客服句，後面手算也是這三個字。
-->

---

<div class="eyebrow">03 · 注意力 · 3：一圖看懂 Q、K、V</div>

# 注意力（attention）：每寫一個字，都回頭看每一個字

<div class="grid grid-cols-[1.1fr_1fr] gap-6 mt-1 items-center">
<div>

<svg viewBox="0 0 400 300" style="width:100%" aria-label="上方黃色的 query「螢幕」發出三條線，分別連到下方青色的 key（螢幕、破了、退貨），線的粗細代表權重 0.38、0.23、0.38；每個 key 下方是紅色的 value，權重決定各拿多少 value">
  <rect x="130" y="8" width="140" height="44" rx="8" fill="var(--q-soft)" stroke="var(--q)" stroke-width="3"/>
  <text x="140" y="36" style="font-size:17px" fill="var(--text)">query：螢幕</text>
  <g style="font-size:17px" fill="var(--text)">
  <rect x="10" y="150" width="110" height="40" rx="8" fill="var(--k-soft)" stroke="var(--k)" stroke-width="2.5"/><text x="30" y="177">key 螢幕</text>
  <rect x="145" y="150" width="110" height="40" rx="8" fill="var(--k-soft)" stroke="var(--k)" stroke-width="2.5"/><text x="165" y="177">key 破了</text>
  <rect x="280" y="150" width="110" height="40" rx="8" fill="var(--k-soft)" stroke="var(--k)" stroke-width="2.5"/><text x="300" y="177">key 退貨</text>
  <rect x="10" y="236" width="110" height="40" rx="8" fill="var(--v-soft)" stroke="var(--v)" stroke-width="2.5"/><text x="22" y="263">value 螢幕</text>
  <rect x="145" y="236" width="110" height="40" rx="8" fill="var(--v-soft)" stroke="var(--v)" stroke-width="2.5"/><text x="157" y="263">value 破了</text>
  <rect x="280" y="236" width="110" height="40" rx="8" fill="var(--v-soft)" stroke="var(--v)" stroke-width="2.5"/><text x="292" y="263">value 退貨</text>
  </g>
  <line x1="200" y1="52" x2="65" y2="148" stroke="var(--q)" stroke-width="7"/>
  <line x1="200" y1="52" x2="200" y2="148" stroke="var(--q)" stroke-width="3"/>
  <line x1="200" y1="52" x2="335" y2="148" stroke="var(--q)" stroke-width="7"/>
  <line x1="65" y1="190" x2="65" y2="234" stroke="#b8b8b8" stroke-width="2"/><line x1="200" y1="190" x2="200" y2="234" stroke="#b8b8b8" stroke-width="2"/><line x1="335" y1="190" x2="335" y2="234" stroke="#b8b8b8" stroke-width="2"/>
  <text x="62" y="108" style="font-size:17px" fill="var(--q-text)">0.38</text><text x="208" y="112" style="font-size:17px" fill="var(--q-text)">0.23</text><text x="312" y="108" style="font-size:17px" fill="var(--q-text)">0.38</text>
</svg>

</div>
<div style="font-size:18px">

**像去圖書館查資料**

- <span class="cq">query（查詢）</span>：我現在想找什麼
- <span class="ck">key（鍵）</span>：每本書的書背標籤，拿來和 query **比**
- <span class="cv">value（值）</span>：書的內容，比完之後**拿**來混
- 每本都翻一下，**越符合的看越多**，最後把看到的內容按比例混在一起

</div>
</div>

<div class="takeaway mt-2">注意力是「軟性查表」：不是只挑一本，而是每本都拿一點，比例由 <span class="cq">Q</span>·<span class="ck">K</span> 的相似度決定。</div>

<!--
★ 橋 6（7 分）：線的粗細就是權重，加起來等於 1。和 seq2seq 比：不再只給一張便利貼，每寫一個字都能翻回原句的任何一個字，而且是模型自己決定看哪裡（解決「不知道該看哪個位置」）。3Blue1Brown、李宏毅老師的 self-attention 投影片都是「一個 query 連到每一個 key」這張圖，我們用同一個畫法與配色：黃＝Q、青＝K、紅＝V，從這頁到後面的計算頁都一致。
同一個字的 key 和 value 是兩個不同的向量：key 用來「比」，value 用來「拿」。
這張是總覽，接下來五頁（Query、Key、內積方格、softmax、Value）一步一步拆開；三個字和權重就是「照著算一次」的例子，「退貨」那一列留給練習。
-->

---

<div class="eyebrow">03 · 注意力 · 4：Query，每個字提問</div>

# 第一步：每個字問一個問題（query）

<div class="grid grid-cols-[1.25fr_1fr] gap-4 items-center mt-1">
<div>

<svg viewBox="0 0 680 250" style="width:100%" aria-label="退貨的向量 e3 乘上矩陣 W_Q，得到黃色的 query 向量 q3；另外兩個字也各自乘同一個 W_Q 得到 q1、q2">
  <defs><marker id="q-a" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="var(--q)"/></marker></defs>
  <g style="font-size:19px" fill="var(--text)">
  <rect x="20" y="30" width="150" height="46" rx="8" fill="var(--soft-blue)" stroke="var(--primary)"/><text x="40" y="60">e₁　螢幕</text>
  <rect x="20" y="100" width="150" height="46" rx="8" fill="var(--soft-blue)" stroke="var(--primary)"/><text x="40" y="130">e₂　破了</text>
  <rect x="20" y="170" width="150" height="46" rx="8" fill="var(--soft-blue)" stroke="var(--primary)"/><text x="40" y="200">e₃　退貨</text>
  <rect x="290" y="95" width="120" height="60" rx="8" fill="var(--q-soft)" stroke="var(--q)" stroke-width="3"/><text x="318" y="132" fill="var(--q-text)">W_Q</text>
  <rect x="540" y="30" width="110" height="46" rx="8" fill="var(--q-soft)" stroke="var(--q)" stroke-width="3"/><text x="565" y="60" fill="var(--q-text)">q₁</text>
  <rect x="540" y="100" width="110" height="46" rx="8" fill="var(--q-soft)" stroke="var(--q)" stroke-width="3"/><text x="565" y="130" fill="var(--q-text)">q₂</text>
  <rect x="540" y="170" width="110" height="46" rx="8" fill="var(--q-soft)" stroke="var(--q)" stroke-width="3"/><text x="565" y="200" fill="var(--q-text)">q₃</text>
  </g>
  <g stroke="var(--q)" stroke-width="3"><line x1="170" y1="53" x2="286" y2="115" marker-end="url(#q-a)"/><line x1="170" y1="123" x2="286" y2="125" marker-end="url(#q-a)"/><line x1="170" y1="193" x2="286" y2="140" marker-end="url(#q-a)"/>
  <line x1="410" y1="115" x2="536" y2="53" marker-end="url(#q-a)"/><line x1="410" y1="125" x2="536" y2="123" marker-end="url(#q-a)"/><line x1="410" y1="140" x2="536" y2="193" marker-end="url(#q-a)"/></g>
</svg>

</div>
<div>

<svg viewBox="0 0 430 250" style="width:100%" aria-label="左邊是嵌入空間裡的一個向量，經過矩陣 W_Q 後，到右邊較小的 Query／Key 空間裡變成另一個向量">
  <defs><marker id="sp-q" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="var(--q)"/></marker><marker id="sp-k" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="var(--k)"/></marker><marker id="sp-b" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="var(--primary)"/></marker></defs>
  <text x="8" y="22" style="font-size:15px" fill="var(--muted-text)">嵌入空間（維度很多）</text>
  <rect x="8" y="34" width="170" height="150" fill="var(--surface)" stroke="#b8b8b8"/><line x1="93" y1="34" x2="93" y2="184" stroke="#d0d0d0"/><line x1="8" y1="109" x2="178" y2="109" stroke="#d0d0d0"/>
  <line x1="93" y1="109" x2="150" y2="55" stroke="var(--primary)" stroke-width="4" marker-end="url(#sp-b)"/>
  <text x="8" y="206" style="font-size:15px" fill="var(--primary)">e₃　退貨（位置 3）</text>
  <text x="188" y="96" style="font-size:22px;font-weight:700" fill="var(--q-text)">W_Q</text><line x1="186" y1="108" x2="232" y2="108" stroke="var(--q)" stroke-width="4" marker-end="url(#sp-q)"/>
  <text x="238" y="22" style="font-size:15px" fill="var(--muted-text)">Query/Key 空間（較少維）</text>
  <rect x="244" y="34" width="170" height="150" fill="var(--surface)" stroke="#b8b8b8"/><line x1="329" y1="34" x2="329" y2="184" stroke="#d0d0d0"/><line x1="244" y1="109" x2="414" y2="109" stroke="#d0d0d0"/>
  <g transform="translate(-6,-16)"><line x1="335" y1="125" x2="285" y2="170" stroke="var(--q)" stroke-width="4" marker-end="url(#sp-q)"/></g>
  <text x="228" y="226" style="font-size:15px" fill="var(--q-text)">「前面有說明原因的字嗎？」</text>
</svg>

</div>
</div>

<div class="mt-1" style="font-size:18px">

- <span class="cq">query q</span> ＝ 一個比 e 短的向量，把「這個字想找什麼」編成數字：<span class="cq">q</span> ＝ <span class="cq">W_Q</span> × e
- **每個字**都乘同一個矩陣 <span class="cq">W_Q</span>，各得一個 q。W_Q 裡的數字是訓練學出來的參數

</div>

<div class="takeaway mt-2"><span class="cq">Query</span>：每個字想找什麼樣的字。</div>

<!--
★ 注意力 3（5 分）：對應影片 6:14–7:44：「每個名詞問：我前面有沒有形容詞？」用我們的例子：退貨問「有沒有說明原因的字在我前面？」。
誠實提醒：影片也強調，這個「問題」是為了講解而想像的；真實的 W_Q 學到什麼很難讀。我們今天的玩具直接給 Q，不從 W_Q 算（lab 第 4 部分）。
-->

---

<div class="eyebrow">03 · 注意力 · 5：Key，每個字回答</div>

# 第二步：每個字準備一個答案（key），拿來和 query 對

<div class="grid grid-cols-[1.25fr_1fr] gap-4 items-center mt-1">
<div>

<svg viewBox="0 0 680 230" style="width:100%" aria-label="三個字的向量各乘上矩陣 W_K，得到青色的 key 向量 k1、k2、k3；破了的 key 和退貨的 query 方向一致，表示它能回答退貨的問題">
  <defs><marker id="k-a" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="var(--k)"/></marker></defs>
  <g style="font-size:19px" fill="var(--text)">
  <rect x="20" y="20" width="150" height="46" rx="8" fill="var(--soft-blue)" stroke="var(--primary)"/><text x="40" y="50">e₁　螢幕</text>
  <rect x="20" y="90" width="150" height="46" rx="8" fill="var(--soft-blue)" stroke="var(--primary)"/><text x="40" y="120">e₂　破了</text>
  <rect x="20" y="160" width="150" height="46" rx="8" fill="var(--soft-blue)" stroke="var(--primary)"/><text x="40" y="190">e₃　退貨</text>
  <rect x="290" y="85" width="120" height="60" rx="8" fill="var(--k-soft)" stroke="var(--k)" stroke-width="3"/><text x="318" y="122" fill="var(--k-text)">W_K</text>
  <rect x="540" y="20" width="110" height="46" rx="8" fill="var(--k-soft)" stroke="var(--k)" stroke-width="3"/><text x="565" y="50" fill="var(--k-text)">k₁</text>
  <rect x="540" y="90" width="110" height="46" rx="8" fill="var(--k-soft)" stroke="var(--k)" stroke-width="3"/><text x="565" y="120" fill="var(--k-text)">k₂</text>
  <rect x="540" y="160" width="110" height="46" rx="8" fill="var(--k-soft)" stroke="var(--k)" stroke-width="3"/><text x="565" y="190" fill="var(--k-text)">k₃</text>
  </g>
  <g stroke="var(--k)" stroke-width="3"><line x1="170" y1="43" x2="286" y2="105" marker-end="url(#k-a)"/><line x1="170" y1="113" x2="286" y2="115" marker-end="url(#k-a)"/><line x1="170" y1="183" x2="286" y2="130" marker-end="url(#k-a)"/>
  <line x1="410" y1="105" x2="536" y2="43" marker-end="url(#k-a)"/><line x1="410" y1="115" x2="536" y2="113" marker-end="url(#k-a)"/><line x1="410" y1="130" x2="536" y2="183" marker-end="url(#k-a)"/></g>
</svg>

</div>
<div>

<svg viewBox="0 0 430 250" style="width:100%" aria-label="左邊是嵌入空間裡的一個向量，經過矩陣 W_K 後，到右邊較小的 Query／Key 空間裡變成另一個向量">
  <defs><marker id="sp-q" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="var(--q)"/></marker><marker id="sp-k" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="var(--k)"/></marker><marker id="sp-b" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="var(--primary)"/></marker></defs>
  <text x="8" y="22" style="font-size:15px" fill="var(--muted-text)">嵌入空間（維度很多）</text>
  <rect x="8" y="34" width="170" height="150" fill="var(--surface)" stroke="#b8b8b8"/><line x1="93" y1="34" x2="93" y2="184" stroke="#d0d0d0"/><line x1="8" y1="109" x2="178" y2="109" stroke="#d0d0d0"/>
  <line x1="93" y1="109" x2="150" y2="55" stroke="var(--primary)" stroke-width="4" marker-end="url(#sp-b)"/>
  <text x="8" y="206" style="font-size:15px" fill="var(--primary)">e₂　破了（位置 2）</text>
  <text x="188" y="96" style="font-size:22px;font-weight:700" fill="var(--k-text)">W_K</text><line x1="186" y1="108" x2="232" y2="108" stroke="var(--k)" stroke-width="4" marker-end="url(#sp-k)"/>
  <text x="238" y="22" style="font-size:15px" fill="var(--muted-text)">Query/Key 空間（較少維）</text>
  <rect x="244" y="34" width="170" height="150" fill="var(--surface)" stroke="#b8b8b8"/><line x1="329" y1="34" x2="329" y2="184" stroke="#d0d0d0"/><line x1="244" y1="109" x2="414" y2="109" stroke="#d0d0d0"/>
  <g transform="translate(-6,-16)"><line x1="335" y1="125" x2="280" y2="165" stroke="var(--q)" stroke-width="3" stroke-dasharray="5 4" opacity=".7"/><line x1="335" y1="125" x2="286" y2="172" stroke="var(--k)" stroke-width="4" marker-end="url(#sp-k)"/></g>
  <text x="228" y="226" style="font-size:15px" fill="var(--k-text)">「我是原因，在位置 2」</text>
</svg>

</div>
</div>

<div class="mt-1" style="font-size:18px">

- <span class="ck">key k</span> ＝ <span class="ck">W_K</span> × e：每個字「能回答什麼問題」的標籤，和 q 住在**同一個**較小的空間（右圖）
- **q 和 k 方向越接近，就越「對得上」**：「退貨」的 <span class="cq">q</span> 和「破了」的 <span class="ck">k</span> 對得上（右圖：黃色虛線的 q 和青色的 k 幾乎同方向），意思是「破了」能回答「為什麼退貨」

</div>

<div class="takeaway mt-2"><span class="ck">Key</span>：每個字能回答什麼；對得上，就是 q 和 k 方向接近。</div>

<!--
★ 注意力 4（4 分）：對應影片 7:47–8:27：key 是「可能回答 query 的東西」，兩者「對齊」就代表 match。query 和 key 住在同一個較小的空間，才能比。
-->

---

<div class="eyebrow">03 · 注意力 · 6：內積方格</div>

# 第三步：每個 query 和每個 key 做內積，得到一格分數

<div class="grid grid-cols-[1.05fr_1fr] gap-6 items-center mt-1">
<div>

<svg viewBox="0 0 430 300" style="width:100%" aria-label="三乘三的方格：橫列是 query 螢幕、破了、退貨，直欄是 key 螢幕、破了、退貨；圓點越大分數越高，分數依序為 1 0 1、0 0 0、1 2 2">
  <g style="font-size:17px">
  <text x="130" y="30" fill="var(--k-text)">k 螢幕</text><text x="228" y="30" fill="var(--k-text)">k 破了</text><text x="326" y="30" fill="var(--k-text)">k 退貨</text>
  <text x="10" y="94" fill="var(--q-text)">q 螢幕</text><text x="10" y="184" fill="var(--q-text)">q 破了</text><text x="10" y="274" fill="var(--q-text)">q 退貨</text>
  </g>
  <rect x="108" y="40" width="96" height="250" fill="var(--k-soft)" opacity=".55"/><rect x="206" y="40" width="96" height="250" fill="var(--k-soft)" opacity=".55"/><rect x="304" y="40" width="96" height="250" fill="var(--k-soft)" opacity=".55"/>
  <rect x="0" y="40" width="430" height="2" fill="none"/>
  <g fill="var(--text)" style="font-size:18px;font-weight:700" text-anchor="middle">
  <circle cx="156" cy="85" r="17" fill="var(--warm-accent)" opacity=".75"/><text x="156" y="91" fill="#fff">1</text>
  <circle cx="254" cy="85" r="5" fill="var(--warm-accent)" opacity=".75"/><text x="254" y="112" fill="var(--muted-text)">0</text>
  <circle cx="352" cy="85" r="17" fill="var(--warm-accent)" opacity=".75"/><text x="352" y="91" fill="#fff">1</text>
  <circle cx="156" cy="175" r="5" fill="var(--warm-accent)" opacity=".75"/><text x="156" y="202" fill="var(--muted-text)">0</text>
  <circle cx="254" cy="175" r="5" fill="var(--warm-accent)" opacity=".75"/><text x="254" y="202" fill="var(--muted-text)">0</text>
  <circle cx="352" cy="175" r="5" fill="var(--warm-accent)" opacity=".75"/><text x="352" y="202" fill="var(--muted-text)">0</text>
  <circle cx="156" cy="265" r="17" fill="var(--warm-accent)" opacity=".75"/><text x="156" y="271" fill="#fff">1</text>
  <circle cx="254" cy="265" r="29" fill="var(--warm-accent)" opacity=".75"/><text x="254" y="271" fill="#fff">2</text>
  <circle cx="352" cy="265" r="29" fill="var(--warm-accent)" opacity=".75"/><text x="352" y="271" fill="#fff">2</text>
  </g>
</svg>

</div>
<div style="font-size:18px">

- 格子（第 i 列、第 j 欄）＝ <span class="cq">qᵢ</span> · <span class="ck">kⱼ</span>（內積：對應位置相乘再相加）
- **圓點越大，分數越高**＝這個 key 越對得上這個 query
- 看「q 退貨」那一列：和「破了」「退貨」的分數都是 2，和「螢幕」只有 1
- 全部一次算完：Q × Kᵀ（矩陣相乘）

</div>
</div>

<div class="shot-cap">分數是 lab 第 4 部分同一組玩具 Q、K 算出來的（不是訓練出來的），格子畫法沿用 3Blue1Brown〈Visualizing Attention〉；他的 query 在直欄，這裡擺成橫列，意思一樣</div>

<!--
★ 注意力 5（5 分）：對應影片 8:27–9:17：「我喜歡想成一個全是圓點的方格，圓越大＝內積越大」。內積的意思在 ML 課學過：兩個向量越朝同方向，內積越大。
「q 破了」那一列全是 0：玩具數字讓這個 query 對誰都沒意見，下一頁 softmax 之後會變成平均看。
-->

---

<div class="eyebrow">03 · 注意力 · 7：softmax，變成權重</div>

# 第四步：除以 √d、softmax，每一列變成「加起來＝1」的權重

<div class="grid grid-cols-[1fr_auto_1fr] gap-3 items-center mt-1">
<div>

<table class="vlines" style="font-size:19px;text-align:center">
<thead><tr><th></th><th><span class="ck">k 螢幕</span></th><th><span class="ck">k 破了</span></th><th><span class="ck">k 退貨</span></th></tr></thead>
<tbody>
<tr><td><span class="cq">q 螢幕</span></td><td>0.5</td><td>0</td><td>0.5</td></tr>
<tr><td><span class="cq">q 破了</span></td><td>0</td><td>0</td><td>0</td></tr>
<tr><td><span class="cq">q 退貨</span></td><td>0.5</td><td>1</td><td>1</td></tr>
</tbody>
</table>
<div class="shot-cap" style="text-align:center">分數 ÷ √d（√d ＝ 2）</div>

</div>
<div style="font-size:34px;color:var(--warm-accent)">→<div style="font-size:15px;text-align:center">softmax<br>每一列</div></div>
<div>

<table class="vlines" style="font-size:19px;text-align:center">
<thead><tr><th><span class="ck">螢幕</span></th><th><span class="ck">破了</span></th><th><span class="ck">退貨</span></th><th>列和</th></tr></thead>
<tbody>
<tr><td>0.38</td><td>0.23</td><td>0.38</td><td>1</td></tr>
<tr><td>0.33</td><td>0.33</td><td>0.33</td><td>1</td></tr>
<tr><td>0.23</td><td><b>0.38</b></td><td><b>0.38</b></td><td>1</td></tr>
</tbody>
</table>
<div class="shot-cap" style="text-align:center">注意力圖樣（attention pattern）</div>

</div>
</div>

<div class="mt-2" style="font-size:19px;text-align:center">
softmax（ <span class="cq">Q</span> <span class="ck">Kᵀ</span> ÷ √d ）：論文裡的那一半公式，就是這張方格
</div>

<div class="takeaway mt-2">原始分數可以是任何實數；softmax 把每一列變成 0～1、加起來＝1 的「看多少」。這張權重方格就叫注意力圖樣。</div>

<!--
★ 注意力 6（5 分）：對應影片 9:17–11:01。影片按「欄」做 softmax（每欄＝一個 query）；我們和 lab 一樣按「列」，意思相同。
√d 的原因下一頁再講，這裡只要記得「分數先除以 √d 再 softmax」。權重方格的數字和 lab 印出的一樣：[0.384, 0.233, 0.384]、[0.333, 0.333, 0.333]、[0.233, 0.384, 0.384]。
-->

---

<div class="eyebrow">03 · 注意力 · 8：Value，要加進去的內容</div>

# 第五步：按權重把每個字的 value 加起來，得到「要加進去的變化」

<div class="grid grid-cols-[1.25fr_1fr] gap-6 items-center mt-1">
<div>

<svg viewBox="0 0 520 290" style="width:100%" aria-label="以退貨為例：螢幕的 value [1,0] 乘 0.23、破了的 value [0,1] 乘 0.38、退貨的 value [1,1] 乘 0.38，加起來得到 [0.62, 0.77]，記為更新量">
  <defs><marker id="v-a" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="var(--v)"/></marker></defs>
  <g style="font-size:18px" fill="var(--text)">
  <rect x="0" y="10" width="170" height="44" rx="8" fill="var(--v-soft)" stroke="var(--v)" stroke-width="2.5"/><text x="12" y="38">v₁　螢幕 [1, 0]</text>
  <rect x="0" y="80" width="170" height="44" rx="8" fill="var(--v-soft)" stroke="var(--v)" stroke-width="2.5"/><text x="12" y="108">v₂　破了 [0, 1]</text>
  <rect x="0" y="150" width="170" height="44" rx="8" fill="var(--v-soft)" stroke="var(--v)" stroke-width="2.5"/><text x="12" y="178">v₃　退貨 [1, 1]</text>
  <text x="196" y="38">× 0.23</text><text x="196" y="108">× 0.38</text><text x="196" y="178">× 0.38</text>
  </g>
  <g stroke="var(--v)" stroke-width="2.5"><line x1="172" y1="32" x2="192" y2="32"/><line x1="172" y1="102" x2="192" y2="102"/><line x1="172" y1="172" x2="192" y2="172"/>
  <path d="M290,32 L340,100" fill="none" marker-end="url(#v-a)"/><path d="M290,102 L335,104" fill="none" marker-end="url(#v-a)"/><path d="M290,172 L340,112" fill="none" marker-end="url(#v-a)"/></g>
  <rect x="344" y="78" width="170" height="60" rx="10" fill="var(--v-soft)" stroke="var(--v)" stroke-width="3"/>
  <text x="360" y="104" style="font-size:18px" fill="var(--v-text)">加總＝Δe</text><text x="360" y="128" style="font-size:18px" fill="var(--v-text)">[0.62, 0.77]</text>
  <text x="0" y="240" style="font-size:17px" fill="var(--muted-text)">以「退貨」為例：用它那一列的權重（0.23、0.38、0.38）</text>
  <text x="0" y="266" style="font-size:17px" fill="var(--muted-text)">其他列做一樣的事，三個字同時更新</text>
</svg>

</div>
<div style="font-size:18px">

- <span class="cv">value v</span> ＝ <span class="cv">W_V</span> × e：這個字「如果被注意到，要送出什麼內容」
- <span class="ck">key</span> 用來**比**，<span class="cv">value</span> 用來**拿**
- 權重大的字，貢獻多；加總就是這個字要**加到自己向量上的變化**
- 真實模型：<b>e′₃ ＝ e₃ ＋ <span class="cv">Δe</span></b>（原本的向量，加上這個變化）：「退貨」變成「有原因的退貨」

</div>
</div>

<div class="takeaway mt-2">把全部放在一起：Attention（Q, K, V）＝ softmax（<span class="cq">Q</span><span class="ck">Kᵀ</span> ÷ √d）<span class="cv">V</span></div>

<!--
★ 注意力 7（6 分）：對應影片 13:10–15:44。影片：value 矩陣乘上第一個字的 e 得到 value 向量，按權重縮放，加總得到 Δe，再加回原本的 embedding。我們玩具的 V 只有 2 個數字，讓加總可以手算；真實 V 和 e 一樣長。
lab 的輸出（只做到加權和，沒有「加回 e」）：[0.767, 0.616]、[0.667, 0.667]、[0.616, 0.767]。
-->

---

<div class="eyebrow">03 · 注意力 · 9：照著算一次</div>

# 照著算一次：「螢幕」這個 query 怎麼看三個字

<div class="grid grid-cols-[1fr_1.15fr] gap-6 mt-1" style="font-size:17px">
<div>

<table class="vlines">
<thead><tr><th></th><th><span class="ck">key（k）</span></th><th><span class="cv">value（v）</span></th></tr></thead>
<tbody>
<tr><td>螢幕</td><td>[1, 0, 0, 0]</td><td>[1, 0]</td></tr>
<tr><td>破了</td><td>[0, 0, 2, 0]</td><td>[0, 1]</td></tr>
<tr><td>退貨</td><td>[1, 0, 1, 0]</td><td>[1, 1]</td></tr>
</tbody>
</table>
<div class="mt-2"><span class="cq">query「螢幕」</span>：q ＝ &#91;1, 0, 0, 0&#93;<br>d ＝ 每個 key 向量的長度（這裡 4 個數），√d ＝ 2</div>

</div>
<div class="steps">
  <div><span class="num">1</span>內積 <span class="cq">q</span>·<span class="ck">k</span>（對應位置相乘再相加）：<b>1、0、1</b></div>
  <div><span class="num">2</span>÷ √d：<b>0.5、0、0.5</b></div>
  <div><span class="num">3</span>softmax：e^0.5 ≈ 1.65、e^0 ＝ 1 → 1.65 ÷ 4.30 … → <b>0.38、0.23、0.38</b></div>
  <div><span class="num">4</span>加權相加 <span class="cv">value</span>：0.38×[1,0] ＋ 0.23×[0,1] ＋ 0.38×[1,1] ＝ <b>[0.77, 0.62]</b></div>
</div>
</div>

```python
weights = torch.softmax(Q @ K.T / math.sqrt(d), dim=-1)   # 每個 query 對每個 key 的權重
out = weights @ V                                          # 按權重把 value 加起來
```

<div class="muted" style="font-size:16px">讀作：「<span class="cq">Q</span> 和每個 <span class="ck">K</span> 做內積、除以根號 d、變成加總為 1 的權重，再拿權重去混合 <span class="cv">V</span>」。lab 印出的第一列：<code>[0.384, 0.233, 0.384]</code>。</div>

<!--
★ Q、K、V（7 分）：一步一步在白板上寫。softmax 是 DL 課第 16 頁學過的（把分數變成加起來為 1 的機率），這裡不重教。
Q、K、V 從哪來？真實模型裡是同一個字的嵌入乘上三個不同的可訓練矩陣（W_Q、W_K、W_V）；今天的玩具直接給數字，讓手算可行。
常見誤解：key 和 value 是同一個東西。key 用來「比」，value 用來「拿」。
-->

---

<div class="eyebrow">03 · 注意力 · 10：為什麼除以 √d</div>

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

用「照著算一次」頁的 key 和 value 表；<br><span class="cq">query「退貨」</span>：q ＝ <code>&#91;1, 0, 1, 0&#93;</code>，<span class="nw">√d ＝ 2</span>

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

<div class="eyebrow">03 · 注意力 · 回到客服單</div>

# 回到回覆客服單：解碼器當 query，客服單當 key 和 value

<svg viewBox="0 0 900 250" style="width:100%" aria-label="左邊客服單的每個字都有青色 key 和紅色 value；右邊解碼器正在寫換貨，發出黃色 query，用權重從客服單裡取資訊">
  <defs><marker id="x-a" markerUnits="userSpaceOnUse" markerWidth="14" markerHeight="14" refX="12" refY="7" orient="auto"><path d="M0,0 L14,7 L0,14 z" fill="var(--q)"/></marker></defs>
  <text x="20" y="28" style="font-size:18px" fill="var(--primary)">編碼器讀完的客服單（每個字都留著，不壓成一個 c）</text>
  <g style="font-size:17px" fill="var(--text)">
  <rect x="20" y="50" width="100" height="40" rx="8" fill="var(--k-soft)" stroke="var(--k)" stroke-width="2.5"/><text x="36" y="76">左耳</text>
  <rect x="140" y="50" width="130" height="40" rx="8" fill="var(--k-soft)" stroke="var(--k)" stroke-width="2.5"/><text x="156" y="76">沒有聲音</text>
  <rect x="290" y="50" width="90" height="40" rx="8" fill="var(--k-soft)" stroke="var(--k)" stroke-width="2.5"/><text x="312" y="76">……</text>
  <rect x="400" y="50" width="110" height="40" rx="8" fill="var(--k-soft)" stroke="var(--k)" stroke-width="2.5"/><text x="416" y="76">換貨嗎</text>
  <rect x="20" y="96" width="100" height="30" rx="8" fill="var(--v-soft)" stroke="var(--v)" stroke-width="2"/><text x="40" y="118" style="font-size:15px" fill="var(--v-text)">value</text>
  <rect x="140" y="96" width="130" height="30" rx="8" fill="var(--v-soft)" stroke="var(--v)" stroke-width="2"/><text x="180" y="118" style="font-size:15px" fill="var(--v-text)">value</text>
  <rect x="290" y="96" width="90" height="30" rx="8" fill="var(--v-soft)" stroke="var(--v)" stroke-width="2"/><text x="312" y="118" style="font-size:15px" fill="var(--v-text)">value</text>
  <rect x="400" y="96" width="110" height="30" rx="8" fill="var(--v-soft)" stroke="var(--v)" stroke-width="2"/><text x="430" y="118" style="font-size:15px" fill="var(--v-text)">value</text>
  </g>
  <text x="600" y="28" style="font-size:18px" fill="var(--secondary)">解碼器（正在寫回覆）</text>
  <rect x="610" y="150" width="200" height="50" rx="8" fill="var(--q-soft)" stroke="var(--q)" stroke-width="3"/><text x="630" y="182" style="font-size:18px" fill="var(--q-text)">query：下一個字…</text>
  <g stroke="var(--q)" stroke-width="3" fill="none"><path d="M610,172 C400,215 150,190 70,132" marker-end="url(#x-a)" stroke-dasharray="6 4"/><path d="M610,174 C500,200 250,175 205,132" marker-end="url(#x-a)" stroke-dasharray="6 4"/><path d="M610,178 C560,178 480,160 455,132" marker-end="url(#x-a)" stroke-width="5"/></g>
  <text x="20" y="236" style="font-size:17px" fill="var(--muted-text)">粗線＝這一步看最多的字；每寫一個字，query 都不一樣，看的位置也跟著變</text>
</svg>

<div class="mt-1" style="font-size:18px">

- 這就是 seq2seq 缺的那一塊：解碼器每寫一個字，用自己的 <span class="cq">query</span> 去比客服單每個字的 <span class="ck">key</span>，**自己決定要回頭看哪個位置**
- 取回來的是 <span class="cv">value</span> 的加權和，不再是被壓扁的單一向量 c
- query 和 key 來自**不同**的序列：這叫交叉注意力（cross-attention）。前面手算的是同一句話的字互看，叫自注意力（self-attention）

</div>

<!--
★ 橋 7（5 分）：回扣開場的問題：「解碼器不知道該看原句哪個位置」。影片 17:57–19:10 也講到 cross-attention：翻譯時，key 來自一個語言、query 來自另一個語言，注意力圖樣就是兩種語言的字對字對應；而且通常不需要遮罩。
這張圖是示意（沒有實跑的權重）；真實的熱力圖在 lab 第 5 部分。
-->

---

<div class="eyebrow">04 · 延伸 · 只認名字</div>

# 注意力還有三個延伸：遮罩、多頭、n² 成本（只認名字）

<div class="grid grid-cols-3 gap-4 mt-3" style="font-size:18px">
<div class="node"><strong>遮罩（masking）</strong><small>GPT 寫字時，後面的字還沒出現，所以後面的字不能影響前面的字：softmax 前把那些格子設成 −∞。L18 再講</small></div>
<div class="node"><strong>多頭（multi-head）</strong><small>同時跑很多組 Q、K、V，每一組學一種「上下文怎麼改意思」（例：形容詞改名詞、代名詞指誰）。L18 再講</small></div>
<div class="node node--warm"><strong>成本是 n²</strong><small>注意力圖樣是 n × n 的方格，字數加倍，格子變 4 倍：這就是 context window 很貴的原因</small></div>
</div>

<div class="takeaway mt-4">注意力＝ Q、K、V 三個矩陣＋一張權重方格。其餘都是這個基本款的變化。</div>

<div class="src">內容對應 3Blue1Brown〈Visualizing Attention〉的後半段（masking、multi-head、n² 的 context 成本）</div>

<!--
○ 選修（2 分）：只讓學員聽過名字，不展開。「n² 是 context window 昂貴的原因」可以呼應今天前半段的成本計算：token 越多，錢越多，算得越慢。
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
★ Lab 開始（3 分）：這是橋接 lab，用三頁的簡化流程（和 L03 一樣）。第 3、4 部分會下載 Qwen2.5-0.5B（約 1 GB），CPU 執行階段也跑得動：講師本機 CPU 讀模型約 5 秒、熱力圖不到 1 秒。
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
<div class="node node--primary"><strong>今天的做法</strong><small>只用合成資料；正式上線前先去識別化（遮掉個資），並讀清楚服務條款與資料存放地區（L19）</small></div>
</div>

<div class="takeaway mt-4">算成本用合成資料就夠了：token 數只跟長度、語言和 tokenizer 有關，不需要真的個資。</div>

<!--
★ 風險（3 分）：法條細節由法務判斷，這裡只建立習慣：送出去之前先問「裡面有沒有個資」。L19 會把資料落地、服務條款、授權放進決策表。
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

# 隨堂檢核 1／2（iPAS 題型）：點選答案

<Mcq id="quiz1.q1" :n="1" :answer="1"
  :options="['中文字數不同', '詞彙表從不同的訓練資料統計出來', '網路速度不同', '模型參數量不同']"
  :why="['字數是同一張單的字數，不會變；差別在切法。', '', '網路速度和 token 數無關。', '參數量是模型大小，tokenizer 是獨立的前處理。']"
  explain="每個 tokenizer 的詞彙表來自自己的訓練資料，繁中常用字詞有沒有收進去，決定一句話被切成幾個 token。">
同一張繁中客服單，用不同 tokenizer 算出的 token 數不同，主要原因是？
</Mcq>

<Mcq id="quiz1.q2" :n="2" :answer="0"
  :options="['取出表格中對應的那一列向量', '把編號除以詞彙表大小', '把編號轉成 one-hot 後輸出', '計算編號的雜湊值']"
  :why="['', '除以詞彙表大小是正規化，不是嵌入。', 'one-hot 乘嵌入矩陣的結果等於查表，但嵌入層輸出的是那一列向量，不是 one-hot。', '雜湊沒有可學習的參數，嵌入向量是訓練出來的。']"
  explain="嵌入層是一張「詞彙表大小 × d」的表，編號就是列號，直接取出那一列向量。">
嵌入層（embedding）對一個 token 編號做的事是？
</Mcq>

<FillClear group="quiz1" corner />

<!--
★ 檢核 1／2（2 分）：學員自己點；點錯會出現「再想想」和該選項錯在哪，可再點一次。答案：1 B、2 A。
-->

---

<div class="eyebrow">隨堂檢核</div>

# 隨堂檢核 2／2（iPAS 題型）：點選答案

<Mcq id="quiz2.q3" :n="3" :answer="1"
  :options="['詞彙表太小', '整句被壓成一個固定長度的向量', 'softmax 太慢', '不能用 GPU']"
  :why="['詞彙表大小和 seq2seq 的瓶頸無關。', '', 'softmax 不是瓶頸。', 'RNN 能用 GPU，只是不能平行處理整句。']"
  explain="編碼器把整句壓成一個固定長度的向量交給解碼器，句子越長越塞不下；注意力就是為了解這個瓶頸。">
seq2seq（RNN 編碼器－解碼器）處理長句時的主要瓶頸是？
</Mcq>

<Mcq id="quiz2.q4" :n="4" :answer="2"
  :options="['讓權重加起來等於 1', '減少參數量', '避免分數太大、softmax 只集中在一個字', '讓輸出變成正數']"
  :why="['讓權重加總為 1 是 softmax 本身的作用，不是除以 √d。', '除以 √d 不改變參數量。', '', 'softmax 的輸出本來就是正數，和除以 √d 無關。']"
  explain="d 大時內積變大，softmax 會幾乎只剩一個字有權重；除以 √d 把分數縮回合理範圍。">
注意力分數除以 √d 的目的？
</Mcq>

<FillClear group="quiz2" corner />

<!--
★ 檢核 2／2（2 分）：學員自己點；點錯會出現「再想想」和該選項錯在哪，可再點一次。答案：3 B、4 C。
全部答案與理由：
1 B：每個 tokenizer 的詞彙表來自自己的訓練資料，繁中常用字詞有沒有收進去，決定一句話被切成幾個 token。
2 A：嵌入層是一張「詞彙表大小 × d」的表，編號就是列號，直接取出那一列向量。
3 B：編碼器把整句壓成一個固定長度的向量交給解碼器，句子越長越塞不下；注意力就是為了解這個瓶頸。
4 C：d 大時內積變大，softmax 會幾乎只剩一個字有權重；除以 √d 把分數縮回合理範圍。
-->


---
hostOnly: true
---

<div class="eyebrow">下一步</div>

# 下一堂 L18：模型怎麼「寫」出一封回覆

<div style="font-size:19px" class="mt-4">

- 客服主管：不信任黑盒子，先懂它怎麼寫
- 寫字 ＝ 預測下一個 token，一直重複（L02 的文字接龍）
- 今天的注意力 → 多頭、遮罩、位置編碼 → Transformer 區塊 → 自己訓練一個迷你 GPT

</div>

<!--
★ 下一步（1 分）：預告。今天的 attention() 明天會直接用到。
-->
