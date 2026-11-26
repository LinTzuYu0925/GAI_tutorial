---
theme: default
title: 用中文搜尋商品照
info: |
  生成式AI原理 · D6-2
  電商部有一萬張沒有標籤的商品照，顧客用中文搜尋：用多語對比模型（SigLIP 2）做零樣本標籤與以文搜圖，量 precision@k；再用小型 VLM 寫繁中替代文字。
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
exportFilename: 22-catalog-search
layout: center
class: cover
---

<div class="eyebrow">生成式AI原理 · D6-2</div>

# 用中文搜尋商品照

<p class="subtitle">圖片和中文放進同一個空間：零樣本標籤、以文搜圖、VLM 寫替代文字</p>

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-8">
  <span class="chip">檔名搜尋不夠</span><span class="arrow">→</span>
  <span class="chip">對比學習的共同空間</span><span class="arrow">→</span>
  <span class="chip">零樣本標籤</span><span class="arrow">→</span>
  <span class="chip">以文搜圖＋precision@k</span><span class="arrow">→</span>
  <span class="chip">多語模型</span><span class="arrow">→</span>
  <span class="chip">VLM 替代文字</span>
</div>

<!--
★ 開場（2 分）：D4-2 用 CLIP 量「圖和文字像不像」。今天把它反過來用：拿一句中文，從一堆圖裡找出最像的。
-->

---

<div class="eyebrow">00 · Frame（定義問題）</div>

# 電商部：一萬張沒有標籤的商品照，顧客用中文搜尋

<div class="ticket mt-2">
  <div class="ticket-head">【需求單 #D6-2】部門：電商部<span>公司：曜嶼電子 <span class="fiction" style="color:#fff;border-color:#fff">虛構</span></span></div>
  <dl>
    <dt>問題</dt><dd>一萬張沒有標籤的商品照，顧客用中文搜尋</dd>
    <dt>現況痛點</dt><dd>只能靠檔名搜尋，找不到就不會買</dd>
    <dt>成功指標（KPI）</dt><dd>小型標註集上的 precision@5；繁中替代文字（alt-text）的品質與簡體字比例</dd>
    <dt>可用資料</dt><dd>課程示範商品照 40 張（8 類 × 5，<b>Stable Diffusion 1.5 生成</b>，不是真實商品）</dd>
    <dt>限制與法規</dt><dd>Colab T4；零樣本標籤可能有偏差</dd>
    <dt>為何現有工具不夠</dt><dd>分類器只認得訓練過的類別；英文 CLIP 不懂中文</dd>
  </dl>
</div>

<!--
★ 需求單（3 分）：一萬張用 40 張代表。照片是用 D4-4 的 SD1.5＋LCM-LoRA 生成的（授權單純、每個學員都能重現）；真實上線要用公司自己的商品照重新量。
-->

---

<div class="eyebrow">學習目標</div>

# 今天結束時，你能夠……

1. **說明**對比學習怎麼把圖片和文字放進同一個空間（D4-2 的 CLIP）
2. **做出**零樣本標籤：把類別寫成一句話，不用訓練
3. **做出**以文搜圖：查詢向量、cosine 相似度、前 k 名；並算 precision@k（前 k 名精確率）
4. **選擇**懂中文的多語模型，並說出理由（tokenizer 是線索）
5. **用** VLM（視覺語言模型）寫繁中替代文字，檢查簡體字

<div class="takeaway mt-4">搜尋＝把「查詢」和「每張圖」都變成向量，比誰最近。</div>

<!--
★ 目標（1 分）。不教：影片生成（○ 只認名字）、向量資料庫（△，Text-to-SQL 模組與 Agent 模組）、對比學習的訓練細節。
-->

---

<div class="eyebrow">00 · Frame · 從檔名到意思</div>

# 檔名搜尋 vs 用意思搜尋

<div class="grid grid-cols-2 gap-6 mt-3" style="font-size:18px">
<div class="node node--warm"><strong>檔名搜尋</strong><small>顧客打「燒開水的水壺」→ 檔名是 <code>IMG_0234.jpg</code> → 找不到。要人工替一萬張圖寫標籤</small></div>
<div class="node node--primary"><strong>用意思搜尋</strong><small>「燒開水的水壺」變成一個向量；每張圖也是一個向量；找最接近的幾張。不需要事先寫標籤</small></div>
</div>

<div class="takeaway mt-4">只要圖片和文字在同一個空間，搜尋就是「量距離、排名次」。</div>

<!--
★ Frame（4 分）：先問學員：一萬張圖人工標籤要多久？（一張 10 秒 → 約 28 小時，而且新商品每天進來）。
-->

---

<div class="eyebrow">01 · Try（先看結果）</div>

# 零樣本標籤：類別寫成一句話，不用訓練

<div class="grid grid-cols-[1.1fr_1fr] gap-6 mt-2 items-center">
<div>

<img class="photo" src="/catalog_grid.png" alt="8 類商品照，每類兩張：耳機、行動電源、智慧手錶、掃地機器人、電熱水壺、筆電、背包、馬克杯" style="width:100%">
<div class="shot-cap">課程示範商品照：Stable Diffusion 1.5 ＋ LCM-LoRA 生成，4 步、seed＝100×類別＋變化（見 catalog.csv），320 px；每類顯示 2 張</div>

</div>
<div style="font-size:18px">

- 8 個類別寫成 8 句話：「一張耳機的照片」……
- 每張圖和 8 句話比相似度，選最像的那一句
- 沒有任何訓練：換一組類別，只要改句子

<table class="mt-2" style="font-size:17px"><thead><tr><th>40 張的零樣本標籤</th><th>正確率</th></tr></thead><tbody><tr><td>CLIP（英文）</td><td>22%</td></tr><tr><td>SigLIP 2（多語）</td><td><b>82%</b></td></tr></tbody></table>
<div class="shot-cap">lab 第 2 部分，講師本機 CPU 實跑（結果是決定性的）</div>

</div>
</div>

<div class="takeaway mt-2">零樣本（zero-shot）：模型沒看過這個分類任務，靠「圖文共同空間」直接判斷。</div>

<!--
★ Try（5 分）：先請學員猜英文 CLIP 和多語 SigLIP 2，用中文句子當類別時誰比較準。
-->

---

<div class="eyebrow">02 · Open（打開黑盒子）· 對比學習</div>

# 對比學習：對的配對拉近，錯的推遠（D4-2）

<div class="grid grid-cols-[1fr_1.1fr] gap-6 mt-2 items-center">
<div>

<table class="vlines" style="font-size:17px;text-align:center">
<thead><tr><th></th><th>「耳機」</th><th>「水壺」</th><th>「背包」</th></tr></thead>
<tbody>
<tr><td>🎧 圖</td><td><b>高</b></td><td>低</td><td>低</td></tr>
<tr><td>🫖 圖</td><td>低</td><td><b>高</b></td><td>低</td></tr>
<tr><td>🎒 圖</td><td>低</td><td>低</td><td><b>高</b></td></tr>
</tbody>
</table>
<div class="shot-cap">示意：訓練時，對角線（配對正確）的相似度要高，其他要低</div>

</div>
<div style="font-size:18px">

- 訓練資料：網路上幾億組「圖＋說明文字」
- 圖片編碼器、文字編碼器各自把輸入變成向量
- 目標：同一組的兩個向量靠近，不同組的遠離
- 結果：「水壺的圖」和「水壺這句話」落在同一個地方

</div>
</div>

<div class="takeaway mt-2">搜尋只是這張表的一欄：拿一句查詢，對所有圖算相似度，排序。</div>

<div class="src">CLIP 論文圖 1 的相似度矩陣是最常見的畫法（Radford et al., 2021，S1）</div>

<!--
★ 對比學習（6 分）：D4-2 量 CLIP 分數時看過「圖和文字的 cosine 相似度」。這張表就是 CLIP 論文最有名的那張圖：對角線亮、其他暗。
-->

---

<div class="eyebrow">02 · Open · 以文搜圖</div>

# 以文搜圖：三行程式

```python
q = embed_texts(name, [query])            # 查詢 → 向量 [1, d]
scores = (IMG[name] @ q.T).squeeze(-1)    # 和 40 張圖的 cosine 相似度 [40]
top = torch.topk(scores, k)               # 取最高的 k 張
```

<div class="muted" style="font-size:16px">讀作：「把查詢句變成向量；和每張圖的向量做內積（向量都先正規化過，所以內積就是 cosine 相似度）；取前 k 名」。圖片的向量 <code>IMG</code> 只要算一次、存起來。</div>

<div class="grid grid-cols-2 gap-5 mt-3" style="font-size:17px">
<div class="node"><strong>一萬張也一樣</strong><small>一萬個向量 × 768 維，矩陣乘一次，記憶體裡就算得完</small></div>
<div class="node node--secondary"><strong>一億張呢？</strong><small>才需要向量資料庫（只認名字，後面的模組）</small></div>
</div>

<div class="takeaway mt-2">搜尋＝一次矩陣乘法＋排序：先在記憶體裡做到對，再談規模。</div>

<!--
★ 以文搜圖（5 分）：正規化（normalize）讓每個向量長度＝1，內積就等於 cosine 相似度（D4-2 學過）。
-->

---

<div class="eyebrow">02 · Open · 選模型</div>

# 選模型：英文 CLIP 讀不懂中文

<table class="mt-2" style="font-size:17px">
<thead><tr><th style="width:26%">模型</th><th style="width:30%">「一副耳機」被切成</th><th style="width:16%">授權</th><th>適合</th></tr></thead>
<tbody>
<tr><td>openai/clip-vit-base-patch32</td><td>一串位元組碎片（像 D5-1 的 ▯）</td><td>程式 MIT；模型卡限研究用途（待確認）</td><td>英文、研究比較</td></tr>
<tr><td>google/siglip2-base-patch16-224</td><td>一副｜耳｜機</td><td>Apache-2.0</td><td>多語、中文查詢</td></tr>
</tbody>
</table>

<div class="mt-3" style="font-size:18px">

- tokenizer 是第一個線索：把中文切成看不懂的位元組，文字編碼器就很難學到意思（D5-1）
- 授權也要看：SigLIP 2 是 Apache-2.0；CLIP 的模型卡把部署用途寫在範圍外（待確認）；有些多語模型是非商用授權

</div>

<div class="takeaway mt-3">選模型先問兩件事：它看得懂我們的語言嗎？我們能用它的授權嗎？</div>

<div class="src">tokenizer 輸出：講師本機實跑；授權：HF 模型卡（SigLIP 2 apache-2.0，2026-11-26 API 讀取；CLIP 程式 MIT、模型卡用途限制待確認，S2）</div>

<!--
★ 選模型（5 分）：講師本機實跑：CLIP 把「一副耳機」切成 11 個位元組碎片；SigLIP 2 切成「一副、耳、機」。結果：零樣本標籤 22% vs 82%、precision@5 0.20 vs 0.82。課程地圖 §9.2 提到的 jina-clip-v2 列為 CC BY-NC（S6，待確認）。
-->

---

<div class="eyebrow">03 · Measure（量測驗收）· 練習</div>

# 練習：手算 precision@5

<div class="grid grid-cols-[1fr_1.35fr] gap-5 mt-1" style="font-size:17px">
<div class="node"><strong>照著做</strong><small>查詢「可以聽音樂的耳機」，前 5 名的類別：<br>耳機、耳機、行動電源、耳機、耳機<br>對的有 4 張 → precision@5 ＝ 4 ÷ 5 ＝ <b>0.8</b></small></div>
<div>

<table class="fill tight vlines">
<thead><tr><th style="width:52%">前 5 名的類別（查詢「燒開水的水壺」）</th><th>precision@5</th></tr></thead>
<tbody>
<tr><td>水壺、馬克杯、水壺、水壺、背包</td><td class="blank"><FillIn id="p5.a" hint="例：0.4……" /></td></tr>
<tr><td>水壺、水壺、水壺、水壺、水壺</td><td class="blank"><FillIn id="p5.b" /></td></tr>
<tr><td colspan="1">這個資料集每類只有 5 張；precision@10 最高能到多少？</td><td class="blank"><FillIn id="p5.c" /></td></tr>
</tbody>
</table>

<FillClear group="p5" />

</div>
</div>

<div class="muted mt-2" style="font-size:16px">做完後：lab 第 3 部分的 <code>precision_at_k()</code> 就是這個算法。</div>

<!--
★ 練習（7 分）：個人、不收回。第三題的發現：每類只有 5 張，前 10 名最多只有 5 張對，所以 precision@10 上限是 0.5。k 要配合資料量來選。
-->

---
hostOnly: true
---

<div class="eyebrow">03 · Measure · 練習解答</div>

# 練習解答：k 要配合每類有幾張

<table class="vlines" style="font-size:19px">
<thead><tr><th>前 5 名</th><th>precision@5</th></tr></thead>
<tbody>
<tr><td>水壺、馬克杯、水壺、水壺、背包</td><td>3 ÷ 5 ＝ 0.6</td></tr>
<tr><td>水壺 × 5</td><td>5 ÷ 5 ＝ 1.0</td></tr>
<tr><td>precision@10 的上限</td><td>每類只有 5 張 → 5 ÷ 10 ＝ 0.5</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">怎麼判斷：前 k 名裡對的張數 ÷ k；分母是 k，不是全部的張數。</div>

<!--
★ 解答（2 分）：precision@k 只看前 k 名「準不準」；漏掉多少要看 recall（ML 課學過 precision／recall）。
-->

---

<div class="eyebrow">03 · Open · VLM</div>

# VLM：圖片也變成 token，接在問題前面

<svg viewBox="0 0 900 170" style="width:100%" aria-label="商品照切成小塊，經過視覺編碼器變成視覺 token，和文字問題的 token 接在一起，交給語言模型接龍，輸出繁中說明">
  <defs><marker id="vlm-a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--primary)"/></marker></defs>
  <g style="font-size:17px">
  <rect x="10" y="40" width="90" height="90" fill="var(--surface)" stroke="#b8b8b8"/>
  <line x1="40" y1="40" x2="40" y2="130" stroke="#b8b8b8"/><line x1="70" y1="40" x2="70" y2="130" stroke="#b8b8b8"/><line x1="10" y1="70" x2="100" y2="70" stroke="#b8b8b8"/><line x1="10" y1="100" x2="100" y2="100" stroke="#b8b8b8"/>
  <text x="18" y="160" fill="var(--text)">商品照</text>
  <rect x="140" y="60" width="150" height="50" rx="8" fill="var(--soft-blue)" stroke="var(--primary)"/><text x="152" y="91" fill="var(--text)">視覺編碼器</text>
  <rect x="320" y="50" width="275" height="70" rx="8" fill="var(--soft-amber)" stroke="var(--warm-accent)"/><text x="332" y="80" fill="var(--text)">［視覺 token…］＋「請用</text><text x="332" y="105" fill="var(--text)">繁中寫一句商品說明」</text>
  <rect x="620" y="60" width="130" height="50" rx="8" fill="var(--soft-blue)" stroke="var(--primary)"/><text x="632" y="91" fill="var(--text)">語言模型</text>
  <rect x="780" y="60" width="110" height="50" rx="8" fill="var(--surface)" stroke="var(--secondary)"/><text x="790" y="91" fill="var(--text)">繁中說明</text>
  </g>
  <g stroke="var(--primary)" stroke-width="2.5"><line x1="100" y1="85" x2="136" y2="85" marker-end="url(#vlm-a)"/><line x1="290" y1="85" x2="316" y2="85" marker-end="url(#vlm-a)"/><line x1="595" y1="85" x2="616" y2="85" marker-end="url(#vlm-a)"/><line x1="750" y1="85" x2="776" y2="85" marker-end="url(#vlm-a)"/></g>
</svg>

<div class="grid grid-cols-2 gap-5 mt-1" style="font-size:17px">
<div class="node"><strong>替代文字（alt-text）</strong><small>給看不到圖的人（螢幕報讀）和搜尋引擎讀的一句說明</small></div>
<div class="node node--warm"><strong>要檢查</strong><small>簡體字（D5-4 的老問題）、看錯顏色或類別、加了圖裡沒有的賣點</small></div>
</div>

<div class="takeaway mt-2">VLM ＝ D5-2 的接龍，只是開頭多了「圖片切成的 token」（和 D5-2 的 DiT 同一招）。</div>

<!--
★ VLM（6 分）：lab 用 Qwen2-VL-2B-Instruct（Apache-2.0，模型卡 API 讀取確認）。它的輸出可能混入簡體字或大陸用語（D5-4、D5-3 都看過），所以要檢查。
-->

---

<div class="eyebrow">03 · Measure · VLM 的輸出</div>

# 替代文字：寫得通順，也要寫得對

<table class="mt-3" style="font-size:18px">
<thead><tr><th style="width:18%">商品照</th><th>Qwen2-VL-2B 寫的替代文字</th><th style="width:26%">檢查</th></tr></thead>
<tbody>
<tr><td>黑色耳機</td><td>黑色頭戴式耳機，適用於各種音頻設備。</td><td>沒有簡體字；但「音頻」是大陸用語（台灣說「音訊」）</td></tr>
<tr><td>黑色電熱水壺</td><td>黑色電熱壺，適用於電熱壺底座，方便使用。</td><td>通順，但「適用於電熱壺底座」沒有資訊量</td></tr>
</tbody>
</table>
<div class="shot-cap">lab 第 4 部分，講師本機 CPU 實跑（只跑 2 張；T4 會跑 8 張）；貪婪解碼</div>

<div class="takeaway mt-2">字是繁體，用語不一定是台灣的：自動說明是草稿，上架前要檢查用語並抽查內容。</div>

<!--
★ VLM 輸出（4 分）：D5-4 的簡體字檢查抓不到「用語」：「音頻」字是繁體，用語卻是大陸的。所以檢查要加 D5-4 的用語詞表，最後還是要人工抽查。
-->

---

<div class="eyebrow">04 · 延伸 · 只認名字</div>

# 影片生成：從圖片到影片

<div class="grid grid-cols-2 gap-6 mt-4" style="font-size:18px">
<div class="node"><strong>文字或圖片 → 影片</strong><small>把擴散模型（D3、D4）從「一張圖」延伸到「一連串圖」：多了時間這一維，要讓每一格前後連貫</small></div>
<div class="node node--warm"><strong>代價</strong><small>計算量大、免費 T4 跑不動長影片；授權與肖像風險和圖片一樣（D6-3 檢查表）</small></div>
</div>

<div class="takeaway mt-4">影片＝多了時間軸的圖片生成：同一套去噪，加上「前後要一致」。</div>

<!--
○ 選修（2 分）：只認名字。多數新影片模型用 DiT（D5-2）。
-->

---

<div class="eyebrow">附錄 · 備用</div>

# 向量資料庫（選讀）

<div class="mt-4" style="font-size:19px">

- 一億張圖時，「和每一張都比一次」太慢
- 向量資料庫：事先把向量分群、建索引，查詢時只比最可能的那幾群（近似最近鄰）
- 代價：可能漏掉少數真正最近的；換來快很多
- 後面的模組（Text-to-SQL、Agent 的 RAG）會實作

</div>

<div class="takeaway mt-4">今天的「記憶體裡全部比一次」是正確答案的基準：用向量資料庫後，要用它檢查有沒有漏。</div>

<!--
△ 附錄（1 分）：有時間才講。
-->

---

<div class="eyebrow">05 · Lab L6-2</div>

# Lab 1／7：我們要做出什麼？

<div class="grid grid-cols-2 gap-6 mt-2" style="font-size:18px">
<div>

**打開筆記本**：<code>lab22-catalog-search.ipynb</code>（在 <code>materials/</code>）→ Open in Colab；執行階段：**T4 GPU**；商品照從課程 GitHub 自動下載

1. 用中文搜尋，英文 CLIP 和 SigLIP 2 差多少？
2. 哪一類最容易被搜錯？
3. VLM 寫的說明能直接上架嗎？

</div>
<div>

<div class="node node--primary"><strong>要交出的東西</strong><small>① 兩個模型的零樣本標籤正確率與平均 precision@5<br>② 一個中文搜尋 App<br>③ 替代文字草稿＋檢查結果</small></div>

</div>
</div>

<div class="src">Colab：colab.research.google.com/github/LinTzuYu0925/GAI_tutorial/blob/day6-done/22-catalog-search/materials/lab22-catalog-search.ipynb</div>

<div class="takeaway mt-1">交付給電商部：一個中文搜尋 App，加上兩個模型的 precision@5 對照。</div>

<!--
★ Lab 開始（5 分）：第 1～3 部分 CPU 也能跑；第 4 部分 VLM（2B）需要 GPU。
-->

---

<div class="eyebrow">05 · Lab L6-2</div>

# Lab 2／7：筆記本拆成哪幾塊？

<div class="steps mt-2" style="font-size:18px">
  <div><span class="num">1</span><strong>資料與模型</strong>：<code>catalog.csv</code>＋40 張圖；<code>MODELS</code>（CLIP、SigLIP 2）；<code>embed_images()</code>、<code>embed_texts()</code> → <code>IMG[name]</code> <code>[40, d]</code></div>
  <div><span class="num">2</span><strong>零樣本標籤</strong>：<code>LABEL_TEXT</code> 8 句 → <code>[40, 8]</code> 相似度 → 每列取最大</div>
  <div><span class="num">3</span><strong>以文搜圖</strong>：<code>search()</code> → 前 5 名；<code>precision_at_k()</code>；8 個查詢的平均</div>
  <div><span class="num">4</span><strong>VLM 替代文字</strong>：Qwen2-VL-2B；<code>simplified_chars()</code>（D5-4）</div>
  <div><span class="num">5</span><strong>Gradio 搜尋 App</strong>：輸入一句中文，回傳前 5 張圖</div>
</div>

<div class="takeaway mt-3">一個 TODO：<code>precision_at_k()</code>，就是練習頁的算法。</div>

<!--
★ 拆塊（3 分）：圖片向量只算一次（IMG），每次查詢只算一句文字的向量。
-->

---

<div class="eyebrow">05 · Lab L6-2</div>

# Lab 3／7：Specify

<div style="font-size:18px" class="mt-2">

<strong>【目標】</strong>比較兩個模型的中文搜尋；做出搜尋 App；替商品照寫繁中替代文字<br>
<strong>【輸入與輸出】</strong>40 張圖 → <code>&#91;40, d&#93;</code>；查詢句 → <code>&#91;1, d&#93;</code> → 相似度 <code>&#91;40&#93;</code> → 前 5 名的索引<br>
<strong>【限制】</strong>不訓練任何模型（零樣本）；同一組 8 個查詢、同一個 k＝5；Colab T4<br>
<strong>【驗收】</strong>① 向量都正規化過（長度 1）　② SigLIP 2 的平均 precision@5 高於英文 CLIP　③ App 打得開、回傳 5 張圖　④ 替代文字標出含簡體字或大陸用語（例：音頻）的那幾句

</div>

<!--
★ Specify（3 分）：驗收 ② 是今天的假設，實跑前寫下；若結果相反，就是一個值得報告的發現。
-->

---

<div class="eyebrow">05 · Lab L6-2</div>

# Lab 4／7：Generate → Execute

<PromptBox>
這是商品照搜尋筆記本，請只填一個 # TODO：<br>
precision_at_k(retrieved, relevant_cat, k)：retrieved 是前幾名的圖片索引；回傳前 k 個裡 rows[i]["category"] 等於 relevant_cat 的比例<br>
不要改模型、查詢句和 k。每一行加中文註解。
</PromptBox>

<div class="steps mt-2" style="font-size:17px">
  <div><span class="num">1</span>預期：<code>「耳機」被切成</code> 兩行，CLIP 是一串碎片、SigLIP 2 是「一副、耳、機」</div>
  <div><span class="num">2</span>預期：CLIP 22%／0.20、SigLIP 2 82%／0.82（講師本機 CPU；T4 用 fp16 可能略有差異）</div>
  <div><span class="num">3</span>沒有 Agent 額度：照練習頁的算法寫一行；卡住開 <code>-solution.ipynb</code></div>
</div>

<!--
★ 執行（約 22 分，含下載 CLIP、SigLIP 2、Qwen2-VL-2B）：時間待講師實跑後填入。
-->

---

<div class="eyebrow">05 · Lab L6-2</div>

# Lab 5／7：看前 5 名，找錯在哪

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-2" style="font-size:18px">
<div>

1. 「會自己打掃地板的機器人」：兩個模型的前 5 名各有幾張對？
2. 錯的那幾張，看起來像什麼？（顏色？形狀？背景？）
3. 自己想一個新查詢（例：「送媽媽的禮物」），看結果合不合理

</div>
<div>

<img class="photo" src="/search_top5.png" alt="查詢「會自己打掃地板的機器人」：上排英文 CLIP 的前 5 名全錯；下排 SigLIP 2 前兩名和第五名是掃地機器人，另外兩張是放在地毯和地板上的背包和筆電" style="width:100%">
<div class="shot-cap">講師本機實跑；上排 CLIP（英文）、下排 SigLIP 2（多語）；✓＝類別正確</div>

<div class="muted mt-1" style="font-size:15px">新增查詢：第 3 部分最下面新增一格 <code>search("SigLIP 2（多語）", "你的查詢")</code></div>

</div>
</div>

<div class="takeaway mt-4">「像不像」要對照圖片看：分數高不代表類別對。</div>

<!--
★ 看結果（9 分）：講師實跑：CLIP 0／5、SigLIP 2 3／5；SigLIP 2 錯的兩張是地毯上的背包、木地板上的筆電：模型抓到「地板」的背景（第 2 題的答案，讓學員自己發現）。「送媽媽的禮物」這種抽象查詢沒有標準答案，正好討論「搜尋的定義」。
-->

---

<div class="eyebrow">05 · Lab L6-2</div>

# Lab 6／7：Audit → Iterate

<table style="font-size:17px">
<thead><tr><th style="width:30%">稽核問題</th><th>具體動作</th><th style="width:30%">應該是</th></tr></thead>
<tbody>
<tr><td>向量正規化了嗎？</td><td><code>IMG[name].norm(dim=-1)</code></td><td>全部約 1.0</td></tr>
<tr><td>比較公平嗎？</td><td>兩個模型用同一組查詢、同一個 k</td><td>相同</td></tr>
<tr><td>零樣本句子的寫法有影響嗎？</td><td>把「一張○○的照片」改成「○○」重跑第 2 部分</td><td>先預測，再看正確率有沒有變</td></tr>
<tr><td>VLM 說明可信嗎？</td><td>對照圖片，看顏色、類別</td><td>抽查才知道</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">一次只改一件事：例如只改句子的寫法，看零樣本正確率怎麼變。</div>

<!--
★ 稽核（9 分）：句子寫法的影響常常很大（CLIP 論文稱為 prompt engineering），這是零樣本的一個弱點。
-->

---

<div class="eyebrow">05 · Lab L6-2 · Ship</div>

# Lab 7／7：交付：中文搜尋 App

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-2" style="font-size:18px">
<div>

<div class="placeholder" style="height:220px">Gradio 搜尋 App 畫面（輸入中文 → 5 張圖）<br>講師實跑後替換</div>

</div>
<div>

- 用 SigLIP 2，同一個 <code>search()</code>
- 標題寫明「示範：AI 生成的商品照」
- 交付時附上兩個模型的 precision@5 對照與你的建議

</div>
</div>

<div class="takeaway mt-2">交付的不只是 App：要說得出「為什麼選這個模型」的數字。</div>

<!--
★ Ship（7 分）：這也是期末專題可以延伸的方向（加上替代文字、加上類別篩選）。
-->

---

<div class="eyebrow">06 · 風險（Risk）</div>

# 風險：標籤的偏差、誤導的說明

<table class="mt-2" style="font-size:17px">
<thead><tr><th style="width:22%">風險</th><th>例子</th><th style="width:34%">怎麼做</th></tr></thead>
<tbody>
<tr><td>零樣本標籤偏差</td><td>模型學自網路圖片：某些類別、顏色、族群的照片特別容易被標錯或標上刻板的標籤</td><td>用自己的標註集量每一類的正確率，不只看平均</td></tr>
<tr><td>誤導的說明</td><td>VLM 寫「防水」「最新款」，圖裡根本看不出來</td><td>替代文字只描述看得到的；規格從資料庫來，不讓模型猜</td></tr>
<tr><td>人物照片</td><td>對模特兒照片描述外貌、推測身分</td><td>只描述商品；不推測人的特徵</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">自動標籤和說明會被顧客看到：錯誤和偏見會直接變成公司的形象。</div>

<!--
★ 風險（3 分）：「看平均不夠」接回 D4-1 的「少數類別」和 D5-4 的評估集設計。
-->

---

<div class="eyebrow">總整理</div>

# 今天學到的概念鏈

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-4">
  <span class="chip">檔名 → 意思</span><span class="arrow">→</span>
  <span class="chip">對比學習的共同空間</span><span class="arrow">→</span>
  <span class="chip">零樣本：類別寫成句子</span><span class="arrow">→</span>
  <span class="chip">搜尋＝矩陣乘＋排序</span><span class="arrow">→</span>
  <span class="chip">precision@k</span><span class="arrow">→</span>
  <span class="chip">多語模型</span><span class="arrow">→</span>
  <span class="chip">VLM 替代文字</span>
</div>

<div class="takeaway mt-6">圖和文字在同一個空間：分類、搜尋都是「比距離」；選模型先看它懂不懂我們的語言。</div>

<!--
★ 總整理（2 分）：請學員說出 precision@5 的算法。
-->

---

<div class="eyebrow">隨堂檢核</div>

# 選擇題（iPAS 題型）

<div class="mcq" style="font-size:17px">

1. 零樣本標籤（zero-shot）的做法是？（　）<br><span class="opts"><span class="nw">A. 先用標註資料訓練分類器</span>　<span class="nw">B. 把類別寫成句子，和圖片比相似度</span>　<span class="nw">C. 人工逐張標籤</span>　<span class="nw">D. 用檔名分類</span></span>
2. 前 5 名搜尋結果有 3 張正確，precision@5 是？（　）<br><span class="opts"><span class="nw">A. 0.3</span>　<span class="nw">B. 0.5</span>　<span class="nw">C. 0.6</span>　<span class="nw">D. 3</span></span>
3. 英文 CLIP 不適合中文搜尋，最直接的線索是？（　）<br><span class="opts"><span class="nw">A. 模型太小</span>　<span class="nw">B. tokenizer 把中文切成看不懂的位元組碎片</span>　<span class="nw">C. 圖片解析度</span>　<span class="nw">D. 沒有 GPU</span></span>
4. VLM 寫的替代文字，上架前最需要做的是？（　）<br><span class="opts"><span class="nw">A. 直接上架</span>　<span class="nw">B. 抽查顏色、類別、規格，並檢查簡體字</span>　<span class="nw">C. 調高溫度</span>　<span class="nw">D. 換成英文</span></span>

</div>

<!--
★ 檢核（3 分）。答案：1 B、2 C、3 B、4 B。
-->

---
hostOnly: true
---

<div class="eyebrow">下一步</div>

# 下一堂 D6-3：上市前的合規與打包

<div style="font-size:19px" class="mt-4">

- 法遵部：每個原型展示前都要過合規檢查表
- 授權、著作權與同意、AI 生成標示、個資與 AI 基本法、提示注入、成本
- 然後 90 分鐘：把你的期末專題打包成 App、模型卡、GitHub

</div>

<!--
★ 下一步（1 分）：請學員帶著自己的期末專題 Colab。
-->
